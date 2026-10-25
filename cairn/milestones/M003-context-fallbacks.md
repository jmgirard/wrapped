<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M003: Fall back in contexts that cannot wrap

- **Status:** review
- **Priority:** high
- **Depends on:** M002
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes what users see for wrapped figures in margins, lists, callouts, tables, books, and slides
- **Branch/PR:** m003-context-fallbacks

## Goal

Wrapped figures render as the research page's edge cases E3 to E8, E13, and E15 state, with E7 as D-003 states.

## Scope

**In:**
- Context detection in `wrapped.lua`. A wrapped float in a margin, an aside, a subfigure panel, a table float, a list, a callout, a column layout, or a tabset keeps its normal layout. Each such float prints one warning that names its id.
- The next-block rule. A wrapped figure whose next block is not a paragraph keeps a normal figure with no warning (E6, and the first figure of E7 as D-003 states).
- A contexts fixture, a two-chapter book fixture, and a revealjs fixture, all covered by `tests/verify.py`.
- README updates for the contexts that keep a normal figure and for revealjs.

**Out:**
- What LaTeX does with these fixtures → M004, which renders them to PDF.
- Other margin forms, such as `cap-location: margin` and `.column-page`, and nested or ordered lists → no milestone yet. A later plan adds them if users report them.

## Acceptance criteria

- [x] AC1: `tests/contexts.qmd` renders to HTML. It holds a wrapped float in each of the nine forms below, and the promise covers those forms. The E3 forms are a `.column-margin` figure, a figure in a `.aside` div, and a knitr cell with `#| column: margin`. The E4 form is a subfigure panel with `layout-ncol`, and the E5 form is a `#tbl-` float. The E8 forms are a bullet list item, a `callout-note`, a `.columns` layout, and a tabset. In the output, none of these floats carries a `wrap-left` or `wrap-right` class. For each one, the terminal output holds one extension warning that names the float's id. Each E3 figure sits in the same margin container as in a render of the same file without the extension.
- [x] AC2: In the same fixture, a wrapped figure is the last block before a heading. It renders without a wrap class, and no warning names its id (E6).
- [x] AC3: In the same fixture, two wrapped figures follow each other with no paragraph between them, and paragraphs follow the second. The first renders without a wrap class, and no warning names its id. The second keeps its wrap class. In the browser at 1200 px, the paragraph after the second sits beside it (E7, as D-003 states).
- [x] AC4: A two-chapter book fixture renders to HTML with exit status 0. The wrapped figure in chapter 1 carries its wrap class. In chapter 2, the `@fig-` link to it is an `<a>` whose `href` ends with that figure's id (E13).
- [x] AC5: `tests/revealjs.qmd` holds one slide with a wrapped figure and a paragraph after it. It renders with exit status 0. In the browser at a 1050 by 700 px viewport, the figure floats to its side by computed `float`, and the first line of the paragraph sits beside it. The README shows the revealjs case (E15).

## Coverage

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T3
- AC5 → T3, T4

## Tasks

- [x] T1: Context detection in `wrapped.lua`. Track the enclosing list, callout, column layout, tabset, aside, and margin block in the top-down pass. Detect subfigure panels and `#tbl-` floats. Remove the wrap class from each such float and print one warning that names its id. Leave the margin classes as Quarto sets them.
- [x] T2: The next-block rule. When the block after a wrapped figure is not a paragraph, remove the wrap class with no warning.
- [x] T3: Write `tests/contexts.qmd`, a two-chapter book under `tests/book/`, and `tests/revealjs.qmd`. Add them to `tests/verify.py` with snapshots.
- [x] T4: Check the revealjs layout in the built-in browser and adjust `wrapped.css` for slides if needed. Update `README.md` with the contexts that keep a normal figure and with the revealjs case.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: question set: back-to-back wrapped figures — the first falls back with no warning and the second wraps (D-003). The research page's E7 row is corrected to match.
- 2026-10-24: criteria audit: see the M002 work log. The fixes here name the float's id, compare the margin container with a render without the extension, add the knitr margin cell, and fix the revealjs viewport.
- 2026-10-24: a context fallback warns once for each float and names its id. A format fallback (M002) warns once for each render. The research page's "One warning" for each edge case and "warns once per document" for W5 support this reading.

- 2026-10-25: started by /milestone-implement on branch m003-context-fallbacks.
- 2026-10-25: T1 done. A `find_contexts` pre-pass marks floats in a list, callout, column layout, tabset, aside, margin block, or subfigure panel by custom id, because the float pass has no exit hook to track an enclosing block. The float pass also falls back for a table, a float's own margin class, and a `layout` attribute. Context warnings print in HTML only, like the other per-figure warnings. Choices: ordered lists count as lists; a captioned image with no id and a lone image in a context also fall back with a warning; the outermost context names the warning. The main fixture's snapshot gains the `#tbl-cars` warning (E5).
- 2026-10-25: T2 done. A `find_no_text` pre-pass records floats and cell floats whose next block, past comments, is not a joining paragraph, and strips the class from a no-id figure or lone image there. It skips lists inside a code cell or float, where the figure is the last block by design (a first version broke the main fixture's cell figure). The contexts fixture gains a no-id figure and a lone image, each in a context and before a heading.
- 2026-10-25: T3 done. `verify.py` now renders 14 fixtures: `contexts.html`, the `tests/book/` project (chapters `index.qmd` and `two.qmd`, with `_extensions` and `plot.png` links), and `revealjs.revealjs`. A folder fixture renders as a project and its snapshot lists each page plus xref hrefs. For `contexts`, the script renders a no-filter copy and records whether each E3 figure keeps the same column-margin container; all three do. Snapshots now list `tbl-` floats and read revealjs's `data-src`; the main fixture gains a `tbl-cars` line.
- 2026-10-25: T4 done. Built-in browser, `tests/layout.js`: revealjs slide at 1050x700, `#fig-slide` computed float right, first line at x=53 y=126 beside the box (620–998, top 115), all checks ok; contexts page at 1200, `#fig-second` float right, first line beside, fallback figures float none; main fixture all 12 figures ok. Fixes: `wrapped.css` sets `max-width: 100%` on wrapped images (revealjs caps images at 95%); `layout.js` scales the computed margin to screen px for scaled slides. A scratch render for the README claims found a panel with no wrap class warning because `image_wrap` read a subfigure's image; it now skips nested floats, and the contexts fixture gains `#fig-plain-panel` as its regression case. README gains the next-block rule, the contexts that keep a normal layout, and a Slides section.
- 2026-10-25: delegation: claim audit to a fresh Opus reader. It could not open the local server in the browser pane, so the `layout.js` scale comment rests on its code read and on this session's browser run (gap 40 to 36 px after the change).
- 2026-10-25: claim audit: 54 claims read, 3 corrected — README.md, tests/verify.py
- 2026-10-25: all tasks done; verify passes (14 renders). Status set to review.
- 2026-10-25: step-7 approval: m003-context-fallbacks approved for merge

## Decisions

## Review

Evidence gathered 2026-10-25 on head 447d193, branch contains origin/main e7f1b90. `python3 tests/verify.py`: all 14 renders pass.

- AC1: `quarto render contexts.qmd --to html` exit 0. Each of fig-margin, fig-aside, fig-margin-cell, fig-panel, tbl-wrapped, fig-list, fig-callout, fig-column, fig-tab has no wrap-left/wrap-right class in contexts.html, and exactly 1 warning in the render log names each id. `margin_summary("contexts")`: all three E3 figures have the same nearest column-margin div (`no-row-height column-margin column-container`) as a render with no filters.
- AC2: same render. fig-before-heading (last block before a `###` heading) has no wrap class, and 0 warnings name it.
- AC3: same render. fig-first has no wrap class and 0 warnings name it; fig-second keeps wrap-right and 0 warnings name it. Built-in browser at 1200x800, `tests/layout.js`: fig-second computed float right, box left 687 to right 927, top 6080; first line of the next paragraph at x=128, y=6082, `beside` true; fig-first computed float none.
- AC4: `quarto render book --to html` (tests/book, chapters index.qmd and two.qmd) exit 0. In `_book/index.html`, fig-book has class `wrap-right`. In `_book/two.html`, the `@fig-book` link is `<a href="index.html#fig-book" class="quarto-xref">`, an href ending with the id.
- AC5: `tests/revealjs.qmd` has one slide with fig-slide (.wrap-right) and a paragraph after it. `quarto render revealjs.qmd --to revealjs` exit 0, no extension warnings. Built-in browser at 1050x700: fig-slide computed float right, box 620 to 998, top 115 to 479; first line at x=53, y=126, `beside` true; all layout.js checks ok. README.md has a "Slides" section with a revealjs example and names revealjs in its intro.
- Gate: `cairn_validate.py` exit 0, all checks pass. Toolchain: one version marker, `_extension.yml` version 0.1.0 (unchanged); verify passes on the review head (14 renders); changelog slot is "none". No DESIGN.md principle changed, so `cairn_impact` is skipped.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: a `.column-margin` captioned image with no id, or a lone image, still wrapped, so the README overclaimed — fix now, fixed 0d81145 (`find_contexts` reads a Figure's or image's own margin class; fixture case added)
- diff-bug #2: a `::: {layout-ncol=2}` div that is not a float still wrapped and lost its second column — fix now, fixed 0d81145 (`block_context` treats a layout attribute as "a panel layout"; fixture case `#fig-layout-cell`)
- diff-bug #3: a knitr cell with `layout-ncol` and two plots, no `fig-subcap`, still wrapped — fix now, fixed 0d81145 (same check, on the cell div; scratch render: both plots warn "is in a panel layout")
- diff-bug #4: a `#| fig-column: margin` cell floats in the margin with no warning — follow-up, row "Fall back in other margin and list forms" (plan Out names other margin forms)
- diff-bug #5: the warning calls a listing "the table #lst-code" — fix now, fixed 0d81145 (noun from float type; scratch render prints "the float #lst-code")
- diff-bug #6: a figure in a loose definition list wraps — follow-up, row "Fall back in other margin and list forms"
- diff-bug #7: README says the warning "names it", but a figure with no id is named only as "a figure with no id" — fix now, fixed 0d81145 (README states what the warning names)
- diff-bug #8: a panel and its subfigure both carrying the class print two warnings — reject, planned change: one warning per float (work log 2026-10-24)
- diff-bug #9: `margin_summary` can pass without removing the filter — fix now, fixed 0d81145 (returns an error line when the copy is unchanged)
- diff-bug #10: contexts render in HTML only — reject, planned change: Scope Out sends other formats to M004
- diff-bug #11: DESIGN.md Architecture says five passes — fix now, fixed 0d81145
- diff-bug #12: a cell's last-block wrapped image might wrap with no text — reject, false: the reviewer's own `output: asis` render behaved correctly and no input reaches it
- diff-bug (c): `tbl-cars` and the revealjs snapshot repeat paths — reject, false: `tbl-cars` is the existing fixture's snapshot recording changed behavior, and the revealjs snapshot pins that revealjs takes the HTML path, which no other fixture checks
- blame-history #1: the revealjs `max-width` fix misses `.quarto-float` images — reject, false: the rule's selector list includes `.quarto-float.wrap-right img`, and the browser measured the slide image at 378 px in a 378 px box
- blame-history #2: a cell-level wrap class on a table now warns — reject, planned change: E5 and AC1
- blame-history #3: a table-only wrap class triggers the "does not wrap figures yet" format warning — fix now, fixed 0d81145 (tables do not set `found_wrap`; scratch docx render printed no warning)
- blame-history #4: `__quarto_custom_id` used as a table key without a nil check — fix now, fixed 0d81145
- blame-history #5: DESIGN.md five passes — fix now, fixed 0d81145 (same as diff-bug #11)
- blame-history #6: README "page with margin content still wraps" reads as a margin-figure claim — fix now, fixed 0d81145
- blame-history #7: `offsetWidth` rounding in layout.js — reject, false: under 0.5 px, inside the 1 px tolerance
- prior-review #1: `calc()` and other function lengths pass unchecked — follow-up, row "Check CSS function lengths before use" (pre-existing code the diff does not touch)
- prior-review #2: a document whose wrapped figures all fall back still loads `wrapped.css` — fix now, fixed 0d81145 (a `placed` flag gates the HTML assets; scratch table-only page has no `wrapped.css`)
- ripple #1: DESIGN.md "HTML output implements this syntax" omits revealjs — reject, false: revealjs is HTML output
- ripple #2: README margin-content line — fix now, fixed 0d81145 (same as blame-history #6)
- ripple #3: DESIGN.md five passes — fix now, fixed 0d81145 (same as diff-bug #11)
- ripple #4: `tests/readme.qmd` lacks the README Slides example — fix now, fixed 0d81145
- ripple #5: verify.py docstring says browser-check fixtures have no snapshot — fix now, fixed 0d81145 ("exist only for")
- ripple #6: README says no warning for a figure with no paragraph after it, but one in a context warns — fix now, fixed 0d81145
- ripple #7: ROADMAP row still lists the context fallbacks as left — reject, planned change: post-merge hygiene graduates the row
- ripple #8: ROADMAP two-figure row describes the `fig-subcap` empty group, which M003 fixed — fix now, fixed in the review tracking commit (row narrowed)
- ripple #9: DESIGN.md stop rule lacks the next-block rule — fix now, fixed 0d81145
- ripple #10: DESIGN.md says a captioned image with no id always gets a box — fix now, fixed 0d81145 (Architecture rewrite)
- ripple #11: README "a captioned image with no id wraps too" lacks the conditions — reject, false: the conditions in the sections above apply to every figure; the note is about numbering
- ripple #12: wrapped.lua "Only figures take the class" — fix now, fixed 0d81145
- ripple #13: wrapped.lua header omits revealjs and the pre-passes — fix now, fixed 0d81145
- ripple #14: PROFILE.md verify slot omits revealjs and the book — fix now, fixed 0d81145
- ripple #15: DESIGN.md "warn once" — fix now, fixed 0d81145 (once per render in a format, once per figure in a context)
- ripple #16: DESIGN.md non-goals no longer say what the filter does — reject, false: the non-goals stay true; they do not wrap
- Return floor: no finding shows an acceptance criterion failing. The fix-now defects (diff-bug #1 to #3) behave the same on main, so the agent judged them fix-now with no return. After 0d81145, verify passes (14 renders) and the contexts snapshot still shows all nine AC1 forms with one warning each and the same margin containers.
- snapshot: the step-7 definition (`_snaps`, `__snapshots__`) matches no path in this repo; `tests/_snapshots/` changes: new `contexts.html.txt`, `book.html.txt`, `revealjs.revealjs.txt` (AC1 to AC5), and `fixture.html.txt` gains the `#tbl-cars` warning and a `tbl-cars` line (E5, AC1).
