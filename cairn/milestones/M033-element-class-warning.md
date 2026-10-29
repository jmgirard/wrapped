# M033: Warn for a wrap class on a span

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — adds render warnings that users see
- **Branch/PR:** m033-element-class-warning

## Goal

In HTML, PDF through LaTeX, PDF through Typst, and Word, a span, heading, inline code, code block, or captioned table with no `#tbl-` id that carries a wrap class prints a warning, since the class wraps nothing there.

## Scope

**In:** Handlers in the filter's last pass in `_extensions/wrapped/wrapped.lua` (beside `unplaced_link`, about line 1939) for `Span`, `Header`, `Code`, `CodeBlock`, and `Table`, the Pandoc elements with attributes that the last pass does not read yet. For an element with `.wrap-left` or `.wrap-right`, a handler sets `found_wrap` as `unplaced_link` does and, where `wraps()` holds, prints `wrapped: the <kind> <where> is not a figure, so it does not wrap. A wrap class goes on an image or a figure.` The kind is `span`, `heading`, `inline code`, `code block`, or `table`. An element's text is `pandoc.utils.stringify` of it (an image counts as its alt text), its first line, with spaces trimmed at both ends. `<where>` is `#<id>` when a span, heading, inline code, or code block has an id; else `"` + the text + `"` when the text has 40 characters or fewer, or `"` + its first 40 characters (code points, not bytes; a space there stays) + `..."` when longer; else `with no text`. A table's classes are not on the `Table` when the filter runs: Quarto reads an attribute block at the caption's end later (`parseTableCaption` in Quarto 1.10.19's `filters/main.lua`). The table handler reads that block the same way: the caption's last inline is a `Str` ending in `}`, the block starts at the first `Str` that starts with `{`, and `pandoc.read("## " .. text)` gives its classes. A table is always named by its text, the caption's inlines before the block; it never takes an id from the block. Each element keeps its class, at the user's choice, and no output changes. New cases in `tests/fixture.qmd`, `tests/twocolumn.qmd`, and `tests/docx-columns.qmd`, a new Word fixture `tests/docx-columns-span.qmd`, their snapshots, a line in `docs/normal-layout.qmd`, the `found_wrap` comment (about line 54), and DESIGN.md's architecture step 6.

**Out:** A wrap class in raw HTML, such as `<table class="wrap-left">` or `<td class="wrap-right">`: Quarto reads raw HTML tables after the filter runs, and raw HTML is not attribute syntax; not planned. Table head, body, foot, row, and cell attributes: no markdown syntax sets them, so they come only from raw HTML; not planned. A table with a `#tbl-` id: Quarto makes it a float, and the float pass already warns. A code cell's `#| classes:` warning: unchanged. A test case for `#| class-source:` or `#| class-output:`: knitr puts the class on a `CodeBlock`, the same code path as a fenced code block. Test cases for an element inside a callout, a wrapped group, or a caption, or for a code block with an id: the last pass reaches them through the same handlers and helper as the cases below. The site's other pages and the README: no change.

## Acceptance criteria

- [x] AC1: In HTML, PDF through LaTeX, PDF through Typst, and Word, a render of `tests/fixture.qmd` prints exactly one warning of the Scope's form for each of these new cases, whose texts and ids no other case shares, as the `1x` lines of the four `fixture` snapshots show after `python3 tests/verify.py`: (a) a span with `.wrap-right`, text, and no id, named by its quoted text; (b) a span with an id, named `#<id>`; (c) a span with no id whose text has 39 ASCII characters, then a precomposed `é` (U+00E9), then more text, named `"` + those 40 characters + `..."` with the `é` whole; (d) a span that holds only an image with empty alt text, named `with no text`; (e) a heading with `.wrap-right`, named by Pandoc's automatic `#<id>`; (f) inline code, named by its quoted text; (g) a fenced code block of two lines with `.wrap-right` and no id, named by its quoted first line; (h) a pipe table with no id whose caption ends `{.wrap-left}`, named by the quoted caption text before the block, with no trailing space.
- [x] AC2: `git diff main -- tests/_snapshots/fixture.html.txt tests/_snapshots/fixture.pdf.txt tests/_snapshots/fixture.typst.txt tests/_snapshots/fixture.docx.txt` removes no line and adds no warning line other than AC1's. Its other added lines, such as an image line for case (d) or a Typst figure line for case (h), each name a new case.
- [x] AC3: `tests/twocolumn.qmd` (PDF through LaTeX) and `tests/docx-columns.qmd` (Word) each gain a span with a wrap class, and `git diff main` of their snapshots adds no warning line: the one columns warning already there stays the only one. A new Word fixture `tests/docx-columns-span.qmd`, with the same two-column reference doc and a wrap class on one span only, prints the one Word columns warning and no other warning.
- [x] AC4: `docs/normal-layout.qmd` states that a wrap class on a span, heading, inline code, code block, or table with no `#tbl-` id does not wrap and prints a warning in HTML, LaTeX, Typst, and Word, and that in Word with columns, or LaTeX with `classoption: twocolumn`, the one columns warning prints instead; `quarto render docs` exits 0.
- [x] AC5: `python3 tests/verify.py` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T2, T3

## Tasks

- [x] T1: Add cases (a) to (h) to `tests/fixture.qmd` after "A wrap class on a text link" (about line 162), each with its own text and, for (d), its own image copy; a span case to `tests/twocolumn.qmd` and `tests/docx-columns.qmd` beside their link cases; and `tests/docx-columns-span.qmd` with its entry in `tests/verify.py`'s render list. Render `fixture` in the four formats with the one-fixture command, confirm that none of the new cases prints a warning before T2, and confirm with a dump filter that the Typst render keeps the cases' classes and the table's caption block as in HTML; narrow AC1 by a gated amendment if it does not.
- [x] T2: Add the five handlers to the last pass of `wrapped.lua` with one shared helper for the message and `<where>`, comments in the style of `unplaced_link`'s, and register them in the returned filter list. Update the `found_wrap` comment. Write the `fixture`, `twocolumn`, `docx-columns`, and `docx-columns-span` snapshots, read each diff against AC1 to AC3, and run `python3 tests/verify.py`.
- [x] T3: Add the rule to the "Other notes" list of `docs/normal-layout.qmd` (about line 150, after the link note) and name the new elements in step 6 of DESIGN.md's architecture. Run `quarto render docs`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: question set: which candidate to plan — "Warn for a wrap class on a span"; keep or remove the class on the element — keep it, as for a link.
- 2026-10-29: idea vet: gap — a table's caption block reaches the filter as caption text, not as classes; took reading the block as Quarto's `parseTableCaption` does, since the row asks for every element with attributes. Gap — raw HTML such as `<table class="wrap-left">` is a RawBlock with no attributes at the filter's stage; took it as outside the row, whose examples are all attribute syntax. Gap — how a warning names the element; took `#id`, else quoted first line cut at 40 characters, else `with no text`. No flaw: a warning where a class wraps nothing matches DESIGN.md's goal to keep a normal layout and warn.
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render command; 2026-10-29 (M031) equal warnings count once, so each case gets its own text; 2026-10-29 (M032) the last pass sees title metadata, captions, and footnotes, and zsh does not split a loop variable.
- 2026-10-29: collision check: absorbs candidate row "Warn for a wrap class on a span" (M032 plan); M032 (done) warns for links only; no D-entry overlaps (D-001's code-cell class path is unchanged). Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-29: scratch probe (Quarto 1.10.19, HTML, LaTeX, Word): Span, Header (auto id), Code, and CodeBlock keep wrap classes at the last pass, a `#| class-source:` or `#| class-output:` class lands on a CodeBlock, a `#| classes:` cell's code block carries none, a pipe table's `{.wrap-left}` is still caption text, and raw HTML tables are RawBlocks; no docs or test page sets a wrap class on these elements today.
- 2026-10-29: plan gate chose to keep the class on each element over stripping it as `unplaced_div` does, at the user's choice; falsified by a stylesheet that selects a wrap class on a span, heading, code, or table.
- 2026-10-29: plan gate chose to read the caption block with Quarto's own rule over a pattern match on the caption text, so the filter agrees with what Quarto applies; falsified by a Quarto version whose caption parser differs.
- 2026-10-29: criteria audit (full, fresh Opus reader): 11 findings. Fixed 9: exact `"<40 characters>..."` form; trimmed text, so a table caption has no trailing space; a table is named by caption text only, never by an id from its block; case (d) needs empty alt text, since an image's text is its alt; case (c) uses a precomposed `é` after 39 ASCII characters; cases (a), (e), (g) use `.wrap-right`; new fixture `tests/docx-columns-span.qmd` tests `found_wrap` with no wrapped figure; AC1 states the render's warnings with the snapshot as evidence, and AC2 names expected non-warning additions; T1 checks the Typst AST; AC4 adds the columns sentence. Answered 2 with no change: elements in callouts, groups, captions, and a code block with an id run the same handlers and helper (Out names them); AC3 and AC5 had no finding.
- 2026-10-29: implement started on branch m033-element-class-warning.
- 2026-10-29: T1: cases (a) to (h) in `tests/fixture.qmd`, span cases in `twocolumn.qmd` and `docx-columns.qmd`, new `tests/docx-columns-span.qmd` in the render list, image copy `tests/span-class-image.png`. Before the handlers, no new case prints a warning in the four `fixture` formats, `twocolumn` (pdf), or `docx-columns`, and `docx-columns-span` prints none, not even the columns warning; the only summary change is the HTML image line for (d). A Typst dump (`fig-format: png`) shows the same Span, Header, Code, CodeBlock classes and table caption text as HTML.
- 2026-10-29: T2 in progress: handlers `unplaced_span`, `unplaced_header`, `unplaced_code`, `unplaced_code_block`, `unplaced_table` share `warn_unplaced` and `warning_name`; one-fixture renders print the 8 AC1 lines in all four `fixture` formats, no new line in `twocolumn` or `docx-columns`, and the one Word columns warning in `docx-columns-span`. Full `verify.py --update` and `quarto render docs` running; T3 docs and DESIGN step 6 text written.
- 2026-10-29: T2 done: `python3 tests/verify.py --update` exit 0, all 105 renders pass; `git diff main` of the four `fixture` snapshots adds the 8 AC1 lines in each, the HTML image line and one Word `image: cx=1066800` line for case (d), and removes none; `twocolumn.pdf` and `docx-columns.docx` snapshots unchanged; new `docx-columns-span.docx.txt` holds only the Word columns warning.
- 2026-10-29: T3 done: rule added to "Other notes" in `docs/normal-layout.qmd` with the columns sentence, DESIGN.md step 6 names the new elements; `quarto render docs` exit 0, whose one `(W)` line is the page's existing `#fig-callout` example.
- 2026-10-29: implementation choice: the cut keeps code points with `utf8.offset`, and text that is not valid UTF-8 is not cut; the table handler reads the caption's last block, as Quarto's `preprocessTable` does.
- 2026-10-29: `python3 tests/verify.py` (no update) exit 0, all 105 renders pass, at 21ff00b.
- 2026-10-29: claim audit: 32 claims read, 1 corrected — _extensions/wrapped/wrapped.lua. `unplaced_table` removed every trailing Space and SoftBreak, but Quarto's `stripTrailingSpace` removes one Space, so it now removes one Space and the comment says it reads the block's classes the same way. Kept the hint "A wrap class goes on an image or a figure.": it matches the shipped link warning. The reader also found `preprocessTable` has no callers in Quarto 1.10.19; the call that applies the classes is `table_classes()` in pre-combined-figures, which also reads the caption's last block.
- 2026-10-29: `python3 tests/verify.py` exit 0, all 105 renders pass, at 0d19458; status set to review.

## Review

Pass 1, 2026-10-29, review head 3f058f7 (main 21602e6 unmoved).

- AC1: `python3 tests/verify.py` at 3f058f7 exit 0, all 105 renders pass, so each snapshot matches its render. Each of `fixture.{html,pdf,typst,docx}.txt` holds 8 `1x` lines for the new cases: span "a span with a wrap class", span #span-class-id, span "This span runs on past forty charactersé..." (é whole), span with no text, heading #a-heading-with-a-wrap-class, inline code "span_class_code()", code block "wrap_class_block = 1", table "A table with a wrap class" (no trailing space); 11 lines with the hint sentence in each, the 3 link lines plus these 8.
- AC2: `git diff main --stat -- tests/_snapshots` shows insertions only (fixture html 9, pdf 8, typst 8, docx 9; new docx-columns-span 4). Added non-warning lines: HTML `span-class-image.png: wrap=- …` and Word `image: cx=1066800`, both case (d).
- AC3: `git diff main -- tests/_snapshots/twocolumn.pdf.txt tests/_snapshots/docx-columns.docx.txt` is empty at 3f058f7 while both fixtures gained a span with a wrap class; `docx-columns-span.docx.txt` holds one warning, the Word columns warning, and verify matched it.
- AC4: `docs/normal-layout.qmd:156` states the rule for span, heading, inline code, code block, and table with no `#tbl-` id in HTML, LaTeX, Typst, and Word, and the columns warning instead in Word with columns or LaTeX `classoption: twocolumn`; `quarto render docs` exit 0 (its one `(W)` line is the page's existing `#fig-callout` example); `tests/docs_layout.py` exit 0, 24 `ok` (`--html` not run).
- AC5: `python3 tests/verify.py` exit 0 at 3f058f7, all 105 renders pass.
- Gate: `cairn_validate.py` all checks passed; no principle changed, so `cairn_impact` skipped; version marker `_extension.yml` 0.2.0 unchanged; the PR's docs workflow is still to run.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a `#tbl-` float whose class is only in an inner caption block (a `::: {#tbl-x}` div around a captioned table, or a knitr `#| tbl-cap:` ending `{.wrap-left}`) prints no warning, and Quarto's `table_classes()` later puts the class on the float, so it floats in HTML when wrapped.css loads — follow-up: predates this branch, candidate row "Warn for wrap classes on table floats". The plan's Out line "the float pass already warns" holds only for `: Cap {#tbl-x .wrap-left}`.
- diff-bug #2: `: {Braces} first then {.wrap-left}` names the table `with no text`, since the block starts at the first `{` — reject (edge): a caption with a brace group before its attribute block falls outside common use, and the effect is only the warning's name; Quarto applies the class, so the warning itself is right.
- diff-bug #3: a code block whose first line is blank is named `with no text` — reject (edge): a fenced block that opens with a blank line is outside common use, and the effect is only the warning's name, which follows the Scope's "first line".
- diff-bug #4: a span alone sets `found_wrap`, so the unreadable-reference-doc warning in Word and the format or columns warning about figures can print with no figure — reject (planned change): the Scope sets `found_wrap` as `unplaced_link` does, and M032 rejected the same point.
- diff-bug #5: no defect in Quarto-made elements, title, callout, footnote, and Cite spans (one warning each), the `pandoc.read` call, the UTF-8 cut, the one-Space strip, or `table_classes()` agreement for non-float tables — noted.
- diff-bug #6: a caption whose last block holds blocks would make `pandoc.Inlines(last.content)` raise — reject (edge): Markdown cannot produce it, and Quarto's own Table handler assumes the same.
- diff-bug #7: the span in `tests/docx-columns.qmd` repeats the branch `docx-columns-span.qmd` covers, and `span-class-image.png` is a new binary — reject (planned change): AC3 names the span case, and the image keeps case (d)'s snapshot line unique.
- prior-review #1: the `found_wrap` comment says a table sets it, but a `#tbl-` float does not — fix now, fixed 3cb9c59 (comment now says a table with no tbl- id).
- prior-review #2: `unplaced_table` does not check for a `tbl-` id, so a `#tbl-` table might warn twice — reject (false): Quarto moves a float's caption off the inner table before the filter runs, and the plan probe printed only the float warning for `{#tbl-one .wrap-right}`.
- prior-review #3: the `docx-columns.qmd` span repeats `docx-columns-span.qmd` — reject (planned change): as diff-bug #7.
- prior-review #4: `verify.py` merges equal warnings into `Nx` — reject (false): no two new cases share a text, which AC1 requires.
- prior-review #5: the `found_wrap` comment's line breaks — fix now, fixed 3cb9c59.
- ripple #1: `cairn/ROADMAP.md` candidate "Warn for a wrap class on a span" still says no warning prints — reject (planned change): hygiene graduates the row at merge.
- ripple #2: `tests/reference_narrow.py` docstring names only `docx-columns.qmd` for `reference-columns.docx` — fix now, fixed 3cb9c59.
- ripple #3: `tests/verify.py` comment before `reference_narrow.main()` omits `docx-columns-span.qmd` — fix now, fixed 3cb9c59.
- ripple #4: `docs/formats/latex.qmd:84` "In those cases the render prints no warning" now has exceptions for a span or other element in class-set two-column text — reject (false): the sentence describes the figures of the bullet before it, and a link already warned there since M032.
- blame-history #1: a span-only document prints the columns, format, or reference-doc warning about figures, so "wrapped figures render as normal figures" is printed with no figure — reject (planned change): AC3's `docx-columns-span` case asks for the columns warning, and M032 rejected the same point for links.
- blame-history #2: a Jupyter cell with `#| classes:` might copy the class onto its code block, giving a working wrapped figure a false "code block" warning — reject (false): a scratch probe (Quarto 1.10.19, jupyter in a venv) of a `#| classes: wrap-right` figure cell, a no-figure cell, and a `#| class-source: wrap-left` cell printed no code-block warning in HTML or Word, the figure kept `wrap-right` on its float, and no `<pre>` carried a wrap class.
- blame-history #3: the `found_wrap` comment's line breaks — fix now, fixed 3cb9c59 (as prior-review #5).
