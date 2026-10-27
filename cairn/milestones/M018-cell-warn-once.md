# M018: Warn once per cell under a context

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the warnings a render prints
- **Branch/PR:** —

## Goal

A wrapped code cell that makes more than one figure, in a place where
figures keep their normal layout, prints one warning for the cell.

## Scope

**In:** In `float_target` in `_extensions/wrapped/wrapped.lua`, a cell
with `several` set whose figures keep their normal layout for a place
prints one warning for the cell at its first figure, with the place as the
reason (`wrapped.lua:1317-1323`). D-010 sets one warning for such a cell.
The subject is `the code cell #<label>`, as D-010's warning names it. The
work adds a two-plot knitr cell to `tests/margin-meta.qmd`,
`tests/page-wide-meta.qmd`, and `tests/column-meta.qmd`, and two to
`tests/contexts.qmd`. It updates the README section "Where a figure keeps
its normal layout" and row E4 of `cairn/references/wrap-mechanisms.md`.

**Out:** A code cell that makes more than one table float keeps one
warning for each table. Tables are not figures, and D-010 covers figures
only.

## Acceptance criteria

The snapshots are those that `python3 tests/verify.py` compares. A figure
**keeps its normal layout** when its format's wrap line is absent: the
HTML `# figures` line shows no wrap class, the LaTeX `# tex` block has no
`wrappedfigure: <id>`, the Typst `# wraps` box field is not `<id>`, and
the Word `# frames` bookmark field is not `<id>`. A cell warning reads
`1x wrapped: the code cell #<label> <reason>, so it does not wrap.`.

- [ ] AC1: The work adds knitr cells with `#| classes: wrap-right` that
      draw two plots without `fig-subcap`, each followed by a paragraph.
      In every snapshot of their fixtures, both figures of each cell keep
      their normal layout. The `# warnings` block has exactly one line
      that names the cell, with the reason below, and no line that names
      either figure's id. The cells and reasons are these:
  - `tests/margin-meta.qmd` (document `fig-column: margin`): `is in the
    margin` in HTML, LaTeX, Typst, and Word.
  - `tests/page-wide-meta.qmd` (document `fig-column: page`): `is
    page-wide` in HTML, LaTeX, and Typst, and `makes more than one figure`
    in Word.
  - `tests/column-meta.qmd` (document `column: page`): `is page-wide` in
    HTML and LaTeX.
  - `tests/contexts.qmd`, a cell inside a callout: `is in a callout` in
    HTML, LaTeX, Typst, and Word.
  - `tests/contexts.qmd`, a cell with `#| column: margin`: `is in the
    margin` in HTML, LaTeX, Typst, and Word.
- [ ] AC2: The README section "Where a figure keeps its normal layout"
      states that a cell that makes more than one figure, in one of the
      places it lists, prints one warning that names the cell and the
      place.
- [ ] AC3: `python3 tests/verify.py` exits 0 locally and in the verify
      workflow on the PR. Against `main`, the change to `tests/_snapshots/`
      adds lines to the snapshot files of the four fixtures that AC1
      names. It removes or changes no line that is on `main`, and it
      changes no other file.

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T2, T4

## Tasks

- [ ] T1: Add the five cells of AC1 to their fixtures.
- [ ] T2: In `float_target`, print one warning for a cell with `several`
      set whose figures keep their normal layout for a place, and none for
      its figures. Write the snapshots.
- [ ] T3: Update the README section "Where a figure keeps its normal
      layout" and row E4 of `cairn/references/wrap-mechanisms.md`.
- [ ] T4: Run `python3 tests/verify.py` and compare `tests/_snapshots/`
      with `main`.

## Work log

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: question set: which work to take — the three margin follow-up rows; this milestone holds "Warn once per cell under a context".
- 2026-10-27: idea vet: no concern. D-010 already sets one warning for a multi-figure cell, and this extends it to a cell in a place.
- 2026-10-27: split from the one-milestone draft with M016 and M017. Each ships alone.
- 2026-10-27: criteria audit (full mode, on the one-milestone draft): two cases stood in for the row's family. Fixed by adding a page-wide document value, a document `column` value, and a cell's own `#| column: margin`. The diff criterion now forbids removing or changing a line on `main`, since summary lines such as `# images` name no case.
- 2026-10-27: plan chose the place as the cell warning's reason over D-010's `makes more than one figure`, because the place says why the cell does not wrap in the formats where it applies; falsified by a user report that the place reason hides the one-plot-per-cell advice.
- 2026-10-27: lessons used: 2026-10-27 (M014) cell float ids and `fig-subcap`.

## Decisions

## Review
