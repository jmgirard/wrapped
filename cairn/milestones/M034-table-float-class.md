<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M034: Warn for wrap classes on table floats

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the filter's warnings and HTML output change for users' documents
- **Branch/PR:** m034-table-float-class

## Goal

A `#tbl-` float whose wrap class is in the attribute block at its caption's end prints the table warning and keeps its normal layout in HTML.

## Scope

**In:** In `float_target` (`_extensions/wrapped/wrapped.lua`), a table float reads the attribute block at its caption's end, the way `unplaced_table` reads a table's caption (M033). A wrap class there takes the table-float path: one "is not a figure" warning. On every table float, the filter removes the wrap classes from the block and keeps the block's other classes and attributes, so Quarto's `table_classes()` adds no wrap class to the float after the filter runs. The forms tested: a `::: {#tbl-…}` div around a table captioned `: Cap {.wrap-left}`, and a knitr cell with `#| tbl-cap: "Cap {.wrap-right}"`, with or without `#| classes: wrap-…`. Fixture cases, snapshots, and the docs and DESIGN.md text.

**Out:** A Jupyter cell's `tbl-cap` block, subtables in a `tbl-subcap` or `layout-ncol` panel, and a `#tbl-` div around a code cell: the same code path reads them, but no fixture renders them, so they stay untested, as M033's Jupyter case did. A pipe table captioned `: Cap {#tbl-x .wrap-left}` already warns and gets no class (probe 2026-10-29), so it needs no change.

## Acceptance criteria

- [ ] AC1: In HTML, PDF through LaTeX, PDF through Typst, and Word, a `::: {#tbl-…}` div around a table captioned `: Cap {.wrap-left .striped}`, and a knitr cell with `#| tbl-cap: "Cap {.wrap-right}"`, each print one warning, "wrapped: the table #<id> is not a figure, so it does not wrap.", the warning that a `#tbl-` float with the class on its div prints. Shown by their warning lines in the four format snapshots of `tests/fixture.qmd`.
- [ ] AC2: In HTML, the float divs of both AC1 tables, and of a knitr cell with `#| classes: wrap-right` and `#| tbl-cap: "Cap {.wrap-left}"`, carry no `wrap-left` or `wrap-right` class, and no caption of the three shows the attribute block's text. The first AC1 table's `<table>` carries `table-striped`. The third table prints one warning, as in AC1.
- [ ] AC3: In HTML, a `::: {#tbl-…}` div around a table captioned `: Cap {.striped}` prints no warning, and its `<table>` carries `table-striped`.
- [ ] AC4: The Tables section of `docs/normal-layout.qmd` says that a wrap class in a table float's caption block, as in `: A table {.wrap-left}` in a `#tbl-` div or in a knitr cell's `tbl-cap`, prints the same warning and that the table keeps its normal layout, in agreement with the page's list item on tables with no `#tbl-` id. Step 6 of DESIGN.md's filter steps says the filter reads that block on a table float and removes its wrap classes. `quarto render docs` exits 0.
- [ ] AC5: `python3 tests/verify.py` passes on the review head.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T3

## Tasks

- [x] T1: Add four cases to `tests/fixture.qmd`, each with its own table and a paragraph after it: the `#tbl-` div with `: Cap {.wrap-left .striped}`, a knitr cell with `#| tbl-cap: "Cap {.wrap-right}"`, a knitr cell with `#| classes: wrap-right` and `#| tbl-cap: "Cap {.wrap-left}"`, and the `#tbl-` div with `: Cap {.striped}`. Render HTML before the fix and record which print no warning and which float with a wrap class.
- [x] T2: Factor the caption-block parse out of `unplaced_table` (`wrapped.lua:1998`) into a helper that returns the block's attributes and where it starts. In `float_target` (`wrapped.lua:1352`), for a table float, read the block from `float.caption_long`, take its wrap class for the warning when the float has none of its own, and rewrite the block without wrap classes on every table float, removing it when nothing is left.
- [ ] T3: Update the four format snapshots of `tests/fixture.qmd` with `--update` and read the diff. The HTML snapshot records only wrap classes, so add a check to `tests/verify.py` that the AC2 and AC3 tables' `<table>` elements carry `table-striped` where named and that their captions hold no `{`. Plant a fault (skip the rewrite) and see the checks fail. Run `python3 tests/verify.py`.
- [ ] T4: Edit the Tables section of `docs/normal-layout.qmd` and step 6 of `cairn/DESIGN.md`. Run `quarto render docs` and `python3 tests/docs_layout.py`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: question set: what to work on — "Warn for wrap classes on table floats" (absorbs the candidate row of that title, from the M033 review); whether to remove the class or warn only — remove it, so the table keeps its normal layout as `docs/normal-layout.qmd` states.
- 2026-10-29: idea vet: one gap, warn only or also keep the table's normal layout; the user chose to remove the class (question set). No flaw.
- 2026-10-29: lessons used: 2026-10-29 (M033), 2026-10-27 (M013), 2026-10-27 (M012).
- 2026-10-29: collision check: candidate row "Warn for wrap classes on table floats" absorbed; M033 (done) is the source and covers tables with no `#tbl-` id only; no D-entry on table floats. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-29: probe (scratch render, Quarto 1.10.19): at pre-quarto the block sits in `float.caption_long` for both forms (`Cap {.wrap-left .striped}`, `Knitr cap {.wrap-right}`) with no class on the float; the HTML float divs then carry `wrap-left striped` and `cell wrap-right`; no warning prints.
- 2026-10-29: plan gate chose rewriting the caption block in the filter over narrowing the `.quarto-float.wrap-*` CSS selectors, because Quarto gives a table float the same `quarto-float quarto-figure` classes as a figure float, so the CSS cannot tell them apart without a new class on every wrapped float; falsified by a Quarto version that applies the block before pre-quarto filters or no longer reads it from the float caption.
- 2026-10-29: criteria audit (full, fresh Opus reader): 8 items, 6 findings, all fixed. AC1 named its two forms instead of every table float, with Jupyter, subtable panels, and a `#tbl-` div around a code cell moved to Out. AC2 gained a cell with both `classes:` and a caption-block class, since the rewrite must run when the float has its own class. AC2 and AC3 read `table-striped` on the `<table>` instead of `striped` on the float div. AC2 and AC3 are limited to HTML. AC4 says knitr cell. T3 names the `tests/verify.py` check, since the HTML snapshot records only wrap classes. AC3, AC5, and reachability: no finding.
- 2026-10-29: T1: four cases added to `tests/fixture.qmd` (`tbl-caption-block`, `tbl-cell-block`, `tbl-cell-both`, `tbl-striped`). HTML render before the fix: the first two print no warning; the first three float divs carry `wrap-left`, `wrap-right`, `wrap-left`, and their `<table>` elements carry the same class; `tbl-striped` has none and no warning.
- 2026-10-29: T2: `caption_block` (shared with `unplaced_table`) and `drop_caption_wrap` added to `wrapped.lua`; `float_target` runs the rewrite on every table float and takes its class last, after the float's own, a carried, and an image class. The block is written again from its parsed attributes, keeping an id only when the text opened with `{#`, as Quarto does. Scratch probes: a block with `data-x="1 \"q\""` leaves the same caption text as Quarto without the filter; a caption that is only `{.wrap-right}` leaves an empty caption. Checkpoint; T3 suite run and T4 docs render pending.
