<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     The one size check that can fail is cairn_validate's <150 over the
     plan-owned body. -->
# M013: Fall back where a format cannot wrap

- **Status:** in-progress
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

- [ ] AC1: Two contexts keep their normal layout in HTML, PDF through LaTeX, PDF through Typst, and Word. They are a wrapped figure from a code cell with `#| fig-column: margin` and a wrapped figure in a loose definition list with a paragraph after the figure. The definition list also has a wrapped image with no id. For each case, the render prints one warning that names the figure's id or the image's file. `tests/contexts.qmd` holds the cases. Its four snapshots in `tests/_snapshots/` show no wrap markup for them and one warning line for each.
- [ ] AC2: A wrapped figure in a block quote keeps its normal layout in PDF through LaTeX, with one warning that names its id. It wraps with no warning in HTML, PDF through Typst, and Word. A wrapped figure in a grid-table cell keeps its normal layout in Word, with one warning that names its id. It wraps with no warning in HTML and PDF through Typst. In PDF through LaTeX, a wrapped image with no caption in a grid-table cell keeps its normal layout with one warning that names its file, and the render succeeds. Fixture snapshots in each named format show this. The captioned table-cell case is not rendered to PDF through LaTeX.
- [ ] AC3: In HTML, a wrapped figure whose caption goes to the margin keeps its normal layout, with one warning that names its id. This holds for six forms. The key is `cap-location` or `fig-cap-location`, set to `margin` on the figure, on its code cell, or in the document metadata. Each form is a fixture case rendered to HTML. A figure whose own `fig-cap-location="bottom"` overrides a metadata `cap-location: margin` wraps with no warning in HTML. A figure with the `cap-location="margin"` attribute wraps with no warning in PDF through LaTeX, PDF through Typst, and Word.
- [ ] AC4: Quarto has 16 page-wide column classes: `column-body-outset`, `column-page-inset`, `column-page`, `column-screen-inset`, and `column-screen`, each alone or with `-left` or `-right`, and `column-screen-inset-shaded`. A wrapped figure with one of them keeps its normal layout with one warning that names its id in HTML for all 16. In PDF through LaTeX it does so for the 9 that Quarto 1.10.19 makes page-wide there: the names that start with `column-page` or `column-screen` and do not end in `-left` (its `isStarEnv`). It wraps with no warning in PDF through Typst and Word, and in PDF through LaTeX for the other 7. The class is on a div around the figure, on the figure itself, or named by a code cell's `column` or `fig-column` option. Fixture snapshots in the four formats hold five cases: a `column-page` div, a `column-page-left` div, a `column-body-outset` div, a figure with its own `.column-page`, and a `fig-column: page` cell.
- [ ] AC5: No conversion of a CSS number in `wrapped.lua` does integer arithmetic. `grep -n 'tonumber(' _extensions/wrapped/wrapped.lua` lists the calls. Each call whose result enters `*`, `+`, or `-` as a CSS number gives a float (`math.type` is `float`). Regression fixtures that fail on `main` show the result. In Word, `width="9223372036854775807in"` takes the default with the warning that `width="9999in"` gets there. In Word, `wrap-gap="9223372036854775807in"` warns as `wrap-gap="9999in"` does. In Typst, `width="768614336404564651pc"` goes into the `.typ` as a positive `pt` width, and the render succeeds. In Typst, beside `width="50%"`, `wrap-gap="9223372036854775807%"` prints the warning that `wrap-gap="100%"` prints there.
- [ ] AC6: The README section "Where a figure keeps its normal layout" states the behavior of AC1 to AC4 and names the formats that each one applies to. Its margin rule names `#| fig-column: margin`, and its list rule names definition lists. Each statement matches a render of this milestone's fixtures.
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
- [ ] T4: Fall back for page-wide columns: in HTML for the 16 classes, in LaTeX for the 9 page-wide ones. Read the class on a div, on the figure, and in a cell's `column` or `fig-column` option. Add the five cases to a fixture rendered in four formats.
- [ ] T5: Remove integer arithmetic on CSS numbers: `docx_measure` (`wrapped.lua:667`), the `px` and `pc` cases of `typst_length` (`wrapped.lua:510`), and `typst_fills` (`wrapped.lua:543`). Add regression fixtures for Word and Typst, and show each failing on `main` first. Record the `grep -n 'tonumber('` ledger in the work log.
- [ ] T6: Update the README from this milestone's renders, in the section "Where a figure keeps its normal layout". Update DESIGN.md's Architecture step 2.
- [ ] T7: Run `python3 tests/verify.py` in full, then push and read CI.

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

## Decisions

## Review
