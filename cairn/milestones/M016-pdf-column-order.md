# M016: Read figure columns in Quarto's order in PDF

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes which wrapped figures wrap in PDF and what the render warns
- **Branch/PR:** m016-pdf-column-order

## Goal

In PDF through LaTeX and PDF through Typst, a wrapped figure keeps its
normal layout for its column only where Quarto 1.10.19 puts it in the
margin or a page-wide column.

## Scope

**In:** In LaTeX and Typst, `_extensions/wrapped/wrapped.lua` reads a
figure float's column in the order of `computeClassesForScopedColumns` in
Quarto's `filters/main.lua`. The order is the float's own `fig-column-*`
class, the document's `fig-column`, its own `column-*` class, and the
document's `column`. The first one set decides. `read_meta` keeps the two
document keys apart. For a code cell, the filter follows what bare renders
show (T1). A scratch render at plan time put a cell with `#| column:
margin` or `#| fig-column: margin` in the body under a document
`fig-column: body`. HTML and Word keep the current rule, which reads a
figure's own class first. The work adds four fixtures, each rendered to
PDF through LaTeX and PDF through Typst:

- `tests/column-order.qmd`, with document `fig-column: body` and
  `column: page`.
- `tests/column-order-page.qmd`, with document `column: page`.
- `tests/column-order-fig-margin.qmd`, with document `fig-column: margin`.
- `tests/column-order-margin.qmd`, with document `column: margin`.

It updates the README section "Where a figure keeps its normal layout",
row E21 of `cairn/references/wrap-mechanisms.md`, and steps 2 and 4 of the
Architecture in `cairn/DESIGN.md`.

**Out:** HTML and Word under keys that name different places stay as they
are. In a bare HTML render, Quarto puts column classes on the figure, its
image, and a container, so only a browser shows the place. That work is
the row "Check HTML column order in a browser". In LaTeX and Typst, a
captioned image with no id and `.column-margin` sits in the body, but the
filter keeps it normal with a margin warning. That is the row "Wrap no-id
margin images in PDF". Slides are M017. One warning for a cell is M018.

## Acceptance criteria

The snapshots are those that `python3 tests/verify.py` compares. These
terms apply to a figure with an id:

- If its format's line shows it, the figure **wraps**. In LaTeX, the
  `# tex` block has `wrappedfigure: <id>`. In Typst, the `# wraps` box
  field is `<id>`.
- If that line is absent, the figure **keeps its normal layout**. In
  Typst, the `# typ` block then has `figure: <id>` or no line for it.

A warning line reads `1x wrapped: the figure #<id> <reason>, so it does
not wrap.`. A **bare render** is a render of a copy of the fixture with
`filters:` removed. In its `.tex`, `\begin{figure}` is the body,
`\begin{figure*}` is a page-wide column, and `\begin{marginfigure}` is the
margin. In its `.typ`, `#notefigure` is the margin, a `#figure` inside a
`#wideblock` or a `#column-` function is a page-wide column, and any other
`#figure` is the body.

- [ ] AC1: This criterion covers the figures listed below, in the LaTeX
      and Typst snapshots. If the bare render of its fixture in that format
      puts the figure in the body, the figure wraps. If not, it keeps its
      normal layout with one warning. The reason is `is in the margin` for
      the margin and `is page-wide` for a page-wide column. The figures
      are these:
  - `column-order.qmd`: image-form floats with `.column-margin`, with
    `.column-page`, with `.fig-column-margin`, and with no column class,
    a figure div with `.column-margin`, a knitr cell with
    `#| column: margin`, and a knitr cell with `#| fig-column: margin`.
  - `column-order-page.qmd`: floats with `.column-body`, with
    `.column-margin`, and with no column class, a knitr cell with no
    column option, and a knitr cell with `#| column: margin`.
  - `column-order-fig-margin.qmd`: floats with `.fig-column-body`, with
    `.column-body`, and with no column class, a figure div with
    `.fig-column-body`, and a knitr cell with `#| fig-column: body`.
  - `column-order-margin.qmd`: floats with `.column-body` and with no
    column class, and a knitr cell with no column option.
- [ ] AC2: The README section "Where a figure keeps its normal layout"
      states the order in which the filter reads a figure's column in PDF
      through LaTeX and PDF through Typst, with the four sources that the
      Scope names. It states that HTML and Word read a figure's own class
      first. Its margin item names a document `column: margin`.
- [ ] AC3: `python3 tests/verify.py` exits 0 locally and in the verify
      workflow on the PR. Against `main`, the change to `tests/_snapshots/`
      adds the snapshot files of the four new fixtures and changes no
      other file.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T4
- AC3 → T2, T3, T5

## Tasks

- [x] T1: Write the four fixtures with the figures that AC1 lists, each
      followed by a paragraph. Render a bare copy of each to PDF through
      LaTeX and PDF through Typst, and write one work-log line for each
      fixture that names where each figure sits in each format.
- [x] T2: In `wrapped.lua`, keep the document's `fig-column` and `column`
      apart in `read_meta` (`wrapped.lua:1177`). In LaTeX and Typst, read
      a float's column in Quarto's order in `float_target`, where
      `class_context(float.classes, true)` and `meta_column_context` now
      decide (`wrapped.lua:1308-1312`). Keep HTML and Word on the current
      rule. Add the `tests/verify.py` entries for the four fixtures.
- [x] T3: Make a code cell's figure follow T1's renders in LaTeX and
      Typst. A cell's own class reaches `block_context` through
      `find_contexts` (`wrapped.lua:1024`), and `meta_column_context.cell`
      gives the document value. Write the snapshots and check each line
      against T1's work-log lines.
- [x] T4: Update the README section "Where a figure keeps its normal
      layout", row E21 of `cairn/references/wrap-mechanisms.md`, and steps
      2 and 4 of the Architecture in `cairn/DESIGN.md`.
- [x] T5: Run `python3 tests/verify.py` and compare `tests/_snapshots/`
      with `main`.

## Work log

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: question set: which work to take — the margin follow-up rows "Read fig-column over a figure's class", "Let slides wrap under margin settings", and "Warn once per cell under a context".
- 2026-10-27: idea vet: one concern. The row assumes Quarto reads document keys over a figure's own class in every format. A bare HTML render keeps a `.column-margin` figure in a margin container and gives a `.column-page` figure's image both `column-body` and `column-page`, so HTML does not show that order. Disposed by narrowing this milestone to LaTeX and Typst, with HTML in a candidate row.
- 2026-10-27: collision check: D-010 (one warning for a multi-figure cell) and M013, M015 (archived margin and page forms) overlap and agree. No rejection stands. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-27: split: the three rows became M016 (this, column order in PDF), M017 (slides), and M018 (one warning per cell). Each goal needed "and" together, and each ships alone. HTML column order and no-id margin images in PDF became candidate rows.
- 2026-10-27: criteria audit (full mode, fresh Opus reader with scratch bare renders): 11 findings on the one-milestone draft. Fixed: HTML order differs (narrowed to LaTeX and Typst), HTML classes do not decide a place (bare-render rule now reads `.tex` and `.typ` only), the no-id image forced a change to existing snapshots (moved to a row), each source tested in one direction (added reverse cases and figure divs), formats unnamed and AC1 a fixture promise (folded into AC1's domain with LaTeX and Typst named), Goal "only" against Word (Goal now PDF only), AC4 forms and aside, AC5 family, and AC7's unlabeled lines went to M017 and M018. Answered: no D-entry conflict.
- 2026-10-27: plan chose to follow bare renders over coding Quarto's order alone because the M015 renders showed Quarto's cell handling differs from the float order; falsified by a bare render whose place differs from what the order gives for a float.
- 2026-10-27: lessons used: 2026-10-27 (M015) render without filters before trusting a placement, 2026-10-27 (M015) Typst widening and `#notefigure`, 2026-10-27 (M013) what the pre-quarto filter sees, 2026-10-27 (M012) checking one fixture.

- 2026-10-27: implement started on branch m016-pdf-column-order.
- 2026-10-27: T1 bare render, column-order (LaTeX and Typst agree): body for fig-order-margin, fig-order-page, fig-order-plain, fig-order-div, fig-order-cell-margin, fig-order-cell-figmargin; margin for fig-order-figmargin.
- 2026-10-27: T1 bare render, column-order-page (LaTeX and Typst agree): body for fig-page-body; margin for fig-page-margin; page-wide for fig-page-plain, fig-page-cell, and fig-page-cell-margin (`figure*` and a nested `#wideblock`).
- 2026-10-27: T1 bare render, column-order-fig-margin (LaTeX and Typst agree): body for fig-figm-figbody and fig-figm-div; margin for fig-figm-body, fig-figm-plain, and fig-figm-cell-body.
- 2026-10-27: T1 bare render, column-order-margin (LaTeX and Typst agree): body for fig-marg-body; margin for fig-marg-plain and fig-marg-cell.
- 2026-10-27: T1 reading: a float outside a cell follows Quarto's four-step order; a cell's figure follows the document's `fig-column`, then its `column`, and the cell's own option only when neither is set (fig-page-cell-margin is page-wide).
- 2026-10-27: checkpoint: T2 to T4 written (`column_context` and a cell rule in `block_context`, the eight snapshots, README, DESIGN, E21). The eight new summaries match T1's placements. Tasks stay unchecked until the full verify run passes.
- 2026-10-27: implementation choice: `column_context` keeps HTML and Word on the old chain (own class, then layout, then the document value), so their reasons and snapshots stay as on main. In LaTeX and Typst the column is read before a layout attribute.
- 2026-10-27: T2 to T5 done. `python3 tests/verify.py`: all 95 renders pass. Against main, `tests/_snapshots/` adds the eight column-order files and changes no other file.
- 2026-10-27: checkpoint: claim audit pass done, one README claim corrected (HTML and Word read a margin or page-wide class first; a body class does not override the document key), same wording fixed in DESIGN step 4 and E21; the HTML row gained the audit's bare-HTML evidence. Re-read of the corrected claim pending.
- 2026-10-27: claim audit: 16 claims read, 1 corrected — README.md (the HTML and Word column sentence; the re-read found Word reads a margin class only, so the sentence, DESIGN step 4, and E21 now say so).
- 2026-10-27: implement done, status review. No code change since the 95-render verify pass; later edits touched README.md and cairn/ only.

## Decisions

## Review
