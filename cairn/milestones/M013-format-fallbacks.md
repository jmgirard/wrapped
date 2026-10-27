<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     The one size check that can fail is cairn_validate's <150 over the
     plan-owned body. -->
# M013: Fall back where a format cannot wrap

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — users see the layout and the warnings
- **Branch/PR:** m013-format-fallbacks

## Goal

If a format cannot wrap a figure where it sits, the figure keeps its normal layout with one warning. No CSS number overflows in the filter's conversions.

## Scope

**In:**
- Margin cells and definition lists in all four formats. A wrapped figure from a code cell with `#| fig-column: margin` keeps its normal layout with one warning. So does a wrapped figure in a definition list.
- Contexts that fail in only some formats. The figure falls back only where the render fails today, and the other formats keep wrapping. A block quote falls back in PDF through LaTeX. A table cell falls back in Word and in PDF through LaTeX. A margin caption falls back in HTML. A page-wide column falls back in HTML, and in PDF through LaTeX where Quarto makes it page-wide.
- The `.typ` summary in `tests/verify.py` reads a `wrap-content` call that is indented in a table cell.
- No integer arithmetic on CSS numbers, in Word and in Typst.
- The README, and DESIGN.md's Architecture step 2.

**Out:**
- A captioned figure in a table cell in PDF through LaTeX. The LaTeX build fails with or without the extension, because Quarto puts a figure float in a `longtable`. That is Quarto's limit, and no work is planned for it.
- Other ways to set a margin caption or a page-wide figure: the `.margin-caption` and `.caption-margin` classes, and a document-level `fig-column`. They go to the candidate row "Fall back in more margin and page forms".
- A metadata `cap-location: margin` in LaTeX, Typst, and Word. Only the attribute form is tested to keep wrapping there.
- Two figures in one wrapped cell, dashboards, and Typst columns stay in their candidate rows.

## Acceptance criteria

- [x] AC1: Two contexts keep their normal layout in HTML, PDF through LaTeX, PDF through Typst, and Word. They are a wrapped figure from a code cell with `#| fig-column: margin` and a wrapped figure in a loose definition list with a paragraph after the figure. The definition list also has a wrapped image with no id. For each case, the render prints one warning that names the figure's id or the image's file. `tests/contexts.qmd` holds the cases. Its four snapshots in `tests/_snapshots/` show no wrap markup for them and one warning line for each.
- [x] AC2: A wrapped figure in a block quote keeps its normal layout in PDF through LaTeX, with one warning that names its id. It wraps with no warning in HTML, PDF through Typst, and Word. A wrapped figure in a grid-table cell keeps its normal layout in Word, with one warning that names its id. It wraps with no warning in HTML and PDF through Typst. In PDF through LaTeX, a wrapped image with no caption in a grid-table cell keeps its normal layout with one warning that names its file, and the render succeeds. Fixture snapshots in each named format show this. The captioned table-cell case is not rendered to PDF through LaTeX.
- [x] AC3: In HTML, a wrapped figure whose caption goes to the margin keeps its normal layout, with one warning that names its id. This holds for six forms. The key is `cap-location` or `fig-cap-location`, set to `margin` on the figure, on its code cell, or in the document metadata. Each form is a fixture case rendered to HTML. A figure whose own `fig-cap-location="bottom"` overrides a metadata `cap-location: margin` wraps with no warning in HTML. A figure with the `cap-location="margin"` attribute wraps with no warning in PDF through LaTeX, PDF through Typst, and Word.
- [x] AC4: Quarto has 16 page-wide column classes: `column-body-outset`, `column-page-inset`, `column-page`, `column-screen-inset`, and `column-screen`, each alone or with `-left` or `-right`, and `column-screen-inset-shaded`. A wrapped figure with one of them keeps its normal layout with one warning that names its id in HTML for all 16. In PDF through LaTeX it does so for the 9 that Quarto 1.10.19 makes page-wide there: the names that start with `column-page` or `column-screen` and do not end in `-left` (its `isStarEnv`). It wraps with no warning in PDF through Typst and Word, and in PDF through LaTeX for the other 7. The class is on a div around the figure, on the figure itself, or named by a code cell's `column` or `fig-column` option. Fixture snapshots in the four formats hold five cases: a `column-page` div, a `column-page-left` div, a `column-body-outset` div, a figure with its own `.column-page`, and a `fig-column: page` cell.
- [x] AC5: No conversion of a CSS number in `wrapped.lua` does integer arithmetic. `grep -n 'tonumber(' _extensions/wrapped/wrapped.lua` lists the calls. Each call whose result enters `*`, `+`, or `-` as a CSS number gives a float (`math.type` is `float`). Regression fixtures that fail on `main` show the result. In Word, `width="9223372036854775807in"` takes the default with the warning that `width="9999in"` gets there. In Word, `wrap-gap="9223372036854775807in"` warns as `wrap-gap="9999in"` does. In Typst, `width="768614336404564651pc"` goes into the `.typ` as a positive `pt` width, and the render succeeds. In Typst, beside `width="50%"`, `wrap-gap="9223372036854775807%"` prints the warning that `wrap-gap="100%"` prints there.
- [x] AC6: The README section "Where a figure keeps its normal layout" states the behavior of AC1 to AC4 and names the formats that each one applies to. Its margin rule names `#| fig-column: margin`, and its list rule names definition lists. Each statement matches a render of this milestone's fixtures.
- [ ] AC7: `python3 tests/verify.py` exits with status 0 on the review head, locally and in CI.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T1, T2, T3, T4, T5, T7

## Tasks

- [x] T1: In `find_contexts` (`wrapped.lua:953`), treat a definition list as a list context. Its items are a term and a list of definitions. Treat a code cell with `fig-column: margin` as a margin context. Add the cases to `tests/contexts.qmd`, and update its four snapshots.
- [x] T2: Add contexts that depend on the format: a block quote in LaTeX, and a table cell in Word and LaTeX. Add the block-quote case to `tests/contexts.qmd`. Add a new fixture with the captioned table-cell case, rendered to HTML, Typst, and Word, and a LaTeX fixture with the uncaptioned image. Make the `.typ` summary in `tests/verify.py` read an indented `wrap-content` call.
- [x] T3: In HTML, fall back for a margin caption in its six forms, with the figure's own key taking precedence over the metadata. The in-document forms and the override are cases in a fixture. The two metadata forms are two small HTML fixtures. The attribute form also renders in LaTeX, Typst, and Word.
- [x] T4: Fall back for page-wide columns: in HTML for the 16 classes, in LaTeX for the 9 page-wide ones. Read the class on a div, on the figure, and in a cell's `column` or `fig-column` option. Add the five cases to a fixture rendered in four formats.
- [x] T5: Remove integer arithmetic on CSS numbers: `docx_measure` (`wrapped.lua:667`), the `px` and `pc` cases of `typst_length` (`wrapped.lua:510`), and `typst_fills` (`wrapped.lua:543`). Add regression fixtures for Word and Typst, and show each failing on `main` first. Record the `grep -n 'tonumber('` ledger in the work log.
- [x] T6: Update the README from this milestone's renders, in the section "Where a figure keeps its normal layout". Update DESIGN.md's Architecture step 2.
- [x] T7: Run `python3 tests/verify.py` in full. CI runs on the PR, which `/milestone-review` opens after the merge approval.

## Work log

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: milestone — changes behavior in four formats and needs a design decision on which formats fall back.
- 2026-10-27: idea vet: two concerns. (1) Several contexts wrap correctly in some formats today, so a fallback in every format would remove working wraps; question set chose falling back only where the format fails. (2) The Word overflow also occurs in Typst's `pc` conversion and percent sum; question set chose fixing Word and Typst.
- 2026-10-27: question set (first run): the twips row was folded into this milestone at the user's choice, so the goal covers two changes.
- 2026-10-27: question set: fallback rule — only where it fails. Overflow scope — Word and Typst.
- 2026-10-27: lessons used: 2026-10-24 (M001), 2026-10-25 (M003), 2026-10-27 (M011), 2026-10-27 (M012).
- 2026-10-27: collision check: absorbs candidate rows "Fall back in other margin and list forms" and "Read Word lengths as floats in twips". Extends M003's contexts (done). D-003's next-block rule does not block the warnings, because a context wins over it in `float_target`. No other D-entry overlaps. Inbox: 0 open issues, 0 open PRs.
- 2026-10-27: probe renders (Quarto 1.10.19): fig-column margin cell in the margin with no warning in HTML and wrapped in the body elsewhere; definition list never wraps and never warns; block quote fails only in LaTeX; table cell fails in Word, and the filter's raw `wrappedfigure` breaks the LaTeX build for an uncaptioned image; margin caption fails only in HTML; `.column-page` fails in HTML and LaTeX. Typst compiles a 21-digit `pt` length.
- 2026-10-27: criteria audit (full mode, Opus reader): 12 findings, all fixed. Added an image-with-no-id case and a loose-list case (AC1); named grid tables and added the LaTeX uncaptioned image case (AC2); bounded the margin caption to six forms and added an override case, with the class forms moved to a candidate row (AC3); split the page-wide domain into 16 in HTML and 9 in LaTeX, and added three cases (AC4); reworded AC5 to the arithmetic defect, a float result, and named formats; pointed AC6 at the one README section that holds the rules. AC7 kept as a gate.
- 2026-10-27: plan gate chose falling back per format over falling back in all formats because the second removes wraps that render correctly today; falsified by a render where a wrap kept as working renders wrong in that format.
- 2026-10-27: plan chose the LaTeX page-wide fallback for the 9 `isStarEnv` classes over all 16 because Quarto does not make the other 7 page-wide in LaTeX; falsified by a LaTeX render where one of the 7 fails to wrap.
- 2026-10-27: plan kept a figure's own page-wide class in scope, because the float pass already reads a float's own margin class, and moved the margin caption classes and document-level `fig-column` to the new candidate row "Fall back in more margin and page forms".

- 2026-10-27: implement started on m013-format-fallbacks. A pre-quarto dump shows that Quarto already copies a cell's cap-location options onto the float's `cap-location` attribute, and that `fig-column: margin` and `fig-column: page` reach the cell as the classes `fig-column-margin` and `fig-column-page`.
- 2026-10-27: checkpoint (T1 not checked off): definition lists and `fig-column-margin` cells are contexts, and the contexts fixture and its four snapshots are updated (each format renders with status 0). The fixtures for T2 to T5 are written but not yet in `tests/verify.py`. The full suite is running.
- 2026-10-27: T1 done: the full suite passed (60 renders).
- 2026-10-27: overflow fixtures on the code before T5: Word's huge width warns "is not a length that Word can use" where 9999in warns "leaves no room for text", and Word's huge gap prints no warning; Typst's huge pc width is written as -9223372036854775808pt, and its huge percent gap prints no warning where 100% warns.
- 2026-10-27: checkpoint (T2 not checked off): block quotes fall back in LaTeX, and tables in LaTeX and Word, through `block_context`. The `.typ` summary reads an indented call and its indented label. The table-cell fixtures are in the runner. The full suite is running.
- 2026-10-27: T2 done: the full suite passed (64 renders).
- 2026-10-27: substantive amendment: Scope Out no longer lists "a cell's `cap-location-margin` classes", because Quarto copies such a class to the figure's `cap-location` before the filter runs, so AC3's cell form covers it (the `fig-figcap-cell` case). The candidate row is corrected the same way. AC3 is unchanged, and what the user gets is unchanged.
- 2026-10-27: checkpoint (T3 not checked off): `caption_location` reads the figure's `fig-cap-location`, then its `cap-location`, then the metadata's, and HTML falls back on `margin`. The six forms and the override render as AC3 says. The full suite is running.
- 2026-10-27: T3 done: the full suite passed (70 renders).
- 2026-10-27: checkpoint (T4 not checked off): `page_context` reads the 16 page-wide classes (a `fig-` prefix stripped for a cell's `fig-column` class), in HTML for all and in LaTeX for the `isStarEnv` names, and `class_context` joins it with `margin_context` at each site that read a margin class. The warning reads "is page-wide". The LaTeX page images show `column-page-left` and `column-body-outset` wrapping with text beside the figure. The full suite is running.
- 2026-10-27: T4 done: the full suite passed (74 renders).
- 2026-10-27: tonumber ledger (`grep -n 'tonumber('` on wrapped.lua before T5, 12 calls): CSS numbers into `*` or `+` now read as floats at 485 (tex px), 515 and 516 (Typst px and pc), 546 (typst_fills, both terms), 670 (docx_measure); already a float at 245 (CSS parser); comparisons only, no arithmetic, at 409, 538, 830; `/` gives a float already at 483; not CSS numbers at 651 and 658 (reference doc twips).
- 2026-10-27: checkpoint (T5 not checked off): the overflow fixtures are in the runner. Word's huge width and gap now warn as 9999in does; Typst's huge pc width is `9223372036854775808pt` and renders, and its huge percent gap warns as 100% does. Each differs from the render before T5 recorded above. The full suite is running.
- 2026-10-27: T5 done: the full suite passed (76 renders).
- 2026-10-27: checkpoint (T6 not checked off): the README's "Where a figure keeps its normal layout" names `#| fig-column: margin` and definition lists, and a new list names the formats where block quotes, table cells, margin captions, and page-wide columns fall back. DESIGN.md's Architecture steps 2 and 4 say the same. Each claim is read from this milestone's renders; the margin figure sits in LaTeX's `marginfigure` and Typst's `notefigure`. Two claims the README adds got cases: a `#| column: page` cell (page-wide) and a figure whose `fig-cap-location="bottom"` overrides its own `cap-location="margin"` (cap-margin).
- 2026-10-27: minor amendment: T7 no longer pushes; the git model pushes the branch and opens the PR at `/milestone-review` after the merge approval, and AC7's CI half is read there.
- 2026-10-27: T6 done: the full suite passed (76 renders).
- 2026-10-27: claim audit: 44 claims read, 2 corrected — _extensions/wrapped/wrapped.lua (the Word table-cell comment now names the LibreOffice render it rests on; the margin-caption comment now says CSS places the caption in the margin). The same reader re-read both and found that they hold.
- 2026-10-27: T7 done: the full suite passed on ab1925c (76 renders). All tasks done; status set to review.

## Decisions

## Review

Pass 1, 2026-10-27, on 7c80a9a. `python3 tests/verify.py` exited 0 with all 76 renders passing, so each snapshot below matches a fresh render.

- AC1: `contexts` snapshots in html, pdf, typst, and docx each carry one warning for `#fig-deflist` ("is in a list"), `#fig-figcol-margin` ("is in the margin"), and `deflist.png` ("is in a list"). None of the three has wrap markup: no wrap class or group in HTML, a plain `figure` in the `.tex` (the margin cell is a `marginfigure`), no `wrap-content` call in Typst, no frame in Word.
- AC2: `contexts.pdf` warns "the figure #fig-quote is in a block quote" and writes a plain `figure`. `contexts.html` groups `fig-quote, p`, `contexts.typst` has its `wrap-content` call, and `contexts.docx` has its frame, each with no warning for it. `table-cell.docx` warns for `#fig-cell` and `cell.png` ("is in a table") and has no frame. `table-cell.html` groups `fig-cell, p` and `wrapped-image, p`, and `table-cell.typst` reads both indented calls, with no warnings. `table-cell-image.pdf` renders (status 0), warns "the image cell.png is in a table", and has no `wrappedfigure`. The captioned case is not in a LaTeX render.
- AC3: in HTML, "has its caption in the margin" warnings with no wrap markup for the six forms: `#fig-cap-attr` and `#fig-figcap-attr` (attributes), `#fig-cap-cell` and `#fig-figcap-cell` (cell options), `#fig-meta-margin` (metadata `cap-location`), and `#fig-meta-figcap` (metadata `fig-cap-location`). `#fig-meta-bottom` (its own `fig-cap-location="bottom"` over metadata `cap-location: margin`) groups `fig-meta-bottom, p` with no warning. `cap-margin` in pdf, typst, and docx wraps `#fig-cap-attr` (a `wrappedfigure`, a `wrap-content` call, a frame) with no warnings.
- AC4: `PAGE_WIDE` in wrapped.lua holds the five base names with and without `-left` and `-right` plus `column-screen-inset-shaded` (16), which matches the class list in Quarto's article layout guide (read 2026-10-27; it also lists `column-body` and `column-margin`) and the 16 classes Quarto 1.10.19's `_bootstrap-rules.scss` defines, and `page_context` takes the LaTeX subset by Quarto 1.10.19's `isStarEnv` rule (main.lua:20979). `page-wide.html` warns "is page-wide" for all six cases (the five planned plus a `column: page` cell). `page-wide.pdf` warns for `#fig-page-div`, `#fig-own-page`, `#fig-page-cell`, and `#fig-column-cell`, and writes a `wrappedfigure` for `#fig-page-left` and `#fig-outset` with no warning. `page-wide.typst` and `page-wide.docx` wrap all six with no warning.
- AC5: `grep -n 'tonumber('` on wrapped.lua lists 12 calls. Each whose result enters `*` or `+` as a CSS number adds `0.0` first: 485 (LaTeX px), 516 and 517 (Typst px and pc), 547 (both terms of `typst_fills`), 672 (`docx_measure`). The others: 245 adds `0.0` already, 483 divides (a float in Lua), 409, 539, and 832 only compare, and 652 and 659 read reference-doc twips, not CSS numbers. `docx-overflow.docx` gives the 9223372036854775807in width and gap the same warnings and the same w=3744 frames as 9999in. `typst-overflow.typst` writes `9223372036854775808pt` for the huge pc width and renders, and warns for the huge percent gap as for 100%. The renders before T5, in the work log, differ in each case: a wrong warning and no warning in Word, `-9223372036854775808pt` and no warning in Typst.
- AC6: README "Where a figure keeps its normal layout" (README.md:191) names `#| fig-column: margin` in its margin rule and definition lists in its list rule, and a second list names the formats for block quotes (LaTeX), table cells (Word, LaTeX), margin captions (HTML, with the six forms and their precedence), and page-wide columns (HTML for 16 classes, LaTeX for the isStarEnv subset). Each statement matches the snapshots above; the implement claim audit read 44 added claims against the code and renders and corrected 2 code comments, none in the README.
- AC7 (local half): `python3 tests/verify.py` exited 0 on 7c80a9a, all 76 renders. The CI half is read on the PR at step 8, and the box is ticked then.
- Gate: `cairn_validate.py` passes (all checks). No DESIGN.md principle changed, so no impact report. Profile consistency-gate: `_extensions/wrapped/_extension.yml` is the one version marker and the diff leaves it unchanged; the verify command passes (above); changelog "none", so no entry is read.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a bare image (or a captioned image with no id) with its own page-wide class fell back in LaTeX, where Quarto makes only floats and divs page-wide — fix now: own-class sites outside the float pass read margin classes only; page-wide.qmd gains an image case that wraps in all four formats, fixed ba48f24.
- diff-bug #2: the page-wide and margin-caption fallbacks fired in revealjs, which has neither layout — fix now: they key on `has_page_layout` (HTML, not revealjs); revealjs.qmd gains a page-wide slide and a margin-caption slide that wrap, and the README Slides section says so, fixed ba48f24.
- diff-bug #3: in HTML a captioned image with no id whose caption goes to the margin still floated — fix now: `figure_block` falls back with "a figure with no id has its caption in the margin"; cap-margin-meta.qmd gains the case, fixed ba48f24.
- diff-bug #4: the `# typ` summary skipped an indented `#figure(` in a table cell — fix now: the split allows an indent (Quarto's template call is `[#figure(`, still left out), fixed ba48f24.
- diff-bug #5: the TYPST_WRAP pattern lost its end anchor — fix now: `[\],]*$` ends a call at `]))` or a cell's `]))],`, fixed ba48f24. The part about `TYPST_WRAP_START` counting an indented call in a code listing — reject (edge): only a document whose code listing holds the filter's own `#layout(wrapped-size => wrap-content(` text reaches it, outside documented and common use, and the effect is an "unread" line in a test summary.
- diff-bug #6: `+ 0.0` before `* 0.75` in the px branches does nothing — reject (planned change): AC5 asks for a float at each call whose result enters `*`.
- diff-bug #7: a length of 310 or more digits reads as inf, so Typst gets `infpt` and LaTeX a dimension TeX rejects — follow-up: predates the branch (such a string already read as a float), new row "Reject infinite lengths in Typst and LaTeX".
- diff-bug #8: some tests run the same code path (cell caption forms, Typst and Word page-wide cases, the `column: page` cell, cap-margin outside HTML, two copies of one PNG) — reject (planned change): AC3 and AC4 name each form and case, the `column: page` cell backs a README claim, and the PNG names keep the image warnings apart.
- blame-history #1: a context still warns for a figure with no paragraph after it, while D-003 says such a figure keeps its normal layout with no warning — reject (false): the context-before-next-block order is M003's (208d0bf), the README states that each context prints one warning, and the branch only adds contexts to that rule.
- blame-history #2: same as diff-bug #4 — fix now, fixed ba48f24.
- blame-history #3: the removed `$` anchor — fix now, as diff-bug #5, fixed ba48f24.
- blame-history #4: a block quote, table, or definition list inside a `#fig-` div is never marked, as M003 left lists — reject (edge): a wrapped image inside a figure div inside such a block is outside documented and common use, and the effect is an error in a LaTeX table or a wrap that HTML renders.
- blame-history #5: same as diff-bug #2 — fix now, fixed ba48f24.
- blame-history #6: same as diff-bug #6 — reject (planned change).
- blame-history #7: `cell.png` and `deflist.png` are copies — reject (style): fixture hygiene; the names keep the warnings apart.
- blame-history #8: lines past 80 columns in a comment and the README — reject (style).
- prior-review #1: a figure in a Typst table cell still wraps, which the source row listed as a defect, with no Typst layout check — follow-up: the question set chose to keep working wraps, and the cramped caption in the probe render is unchecked; new row "Check wrapped figures in table cells".
- prior-review #2: the README's LaTeX table-cell failure has no render in the repo — reject (false): the claim audit rendered it with and without the extension, both failing with "Not in outer par mode", and a test of Quarto's own failure would test dependency behavior.
- prior-review #3: the Word table-cell fallback rests on a LibreOffice render while the README says "in Word" — follow-up: the README states what the filter does in Word, which `table-cell.docx` tests, and the reason (a frame in a cell not wrapping in Word itself) goes to "Check wrapped figures in table cells".
- prior-review #4: M005's indented-call miscount stood on main until this branch — reject (false): no defect, the branch fixes it.
- ripple #1: the README lead "a wrapped figure in one of these places does not wrap" could be read to cover the per-format list — fix now: it reads "in one of the places in this first list", fixed ba48f24.
- ripple #2: wrap-mechanisms.md E3 omits `fig-column: margin` — fix now (corrected M013), fixed ba48f24.
- ripple #3: wrap-mechanisms.md has no rows for the new contexts and E8 does not name definition lists — fix now: E8 names them and E18 to E21 are added, fixed ba48f24.
- After the fixes: `python3 tests/verify.py` exited 0 on ba48f24, all 76 renders. AC1 to AC6 hold on that head (the fixes add cases and change no criterion's evidence above).
- snapshot: none by step 7's definition (no `_snaps` or `__snapshots__` directory). The 21 changed files in `tests/_snapshots/` add lines for the new cases and remove only the `(none)` breakpoint line of `cap-margin.html.txt` and `page-wide.html.txt`, now `576px` because a figure there wraps; each change is called for by AC1 to AC5 or a fix above.
