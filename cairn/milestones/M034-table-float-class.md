<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M034: Warn for wrap classes on table floats

- **Status:** review
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

- [x] AC1: In HTML, PDF through LaTeX, PDF through Typst, and Word, a `::: {#tbl-…}` div around a table captioned `: Cap {.wrap-left .striped}`, and a knitr cell with `#| tbl-cap: "Cap {.wrap-right}"`, each print one warning, "wrapped: the table #<id> is not a figure, so it does not wrap.", the warning that a `#tbl-` float with the class on its div prints. Shown by their warning lines in the four format snapshots of `tests/fixture.qmd`.
- [x] AC2: In HTML, the float divs of both AC1 tables, and of a knitr cell with `#| classes: wrap-right` and `#| tbl-cap: "Cap {.wrap-left}"`, carry no `wrap-left` or `wrap-right` class, and no caption of the three shows the attribute block's text. The first AC1 table's `<table>` carries `table-striped`. The third table prints one warning, as in AC1.
- [x] AC3: In HTML, a `::: {#tbl-…}` div around a table captioned `: Cap {.striped}` prints no warning, and its `<table>` carries `table-striped`.
- [x] AC4: The Tables section of `docs/normal-layout.qmd` says that a wrap class in a table float's caption block, as in `: A table {.wrap-left}` in a `#tbl-` div or in a knitr cell's `tbl-cap`, prints the same warning and that the table keeps its normal layout, in agreement with the page's list item on tables with no `#tbl-` id. Step 6 of DESIGN.md's filter steps says the filter reads that block on a table float and removes its wrap classes. `quarto render docs` exits 0.
- [x] AC5: `python3 tests/verify.py` passes on the review head.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T3

## Tasks

- [x] T1: Add four cases to `tests/fixture.qmd`, each with its own table and a paragraph after it: the `#tbl-` div with `: Cap {.wrap-left .striped}`, a knitr cell with `#| tbl-cap: "Cap {.wrap-right}"`, a knitr cell with `#| classes: wrap-right` and `#| tbl-cap: "Cap {.wrap-left}"`, and the `#tbl-` div with `: Cap {.striped}`. Render HTML before the fix and record which print no warning and which float with a wrap class.
- [x] T2: Factor the caption-block parse out of `unplaced_table` (`wrapped.lua:1998`) into a helper that returns the block's attributes and where it starts. In `float_target` (`wrapped.lua:1352`), for a table float, read the block from `float.caption_long`, take its wrap class for the warning when the float has none of its own, and rewrite the block without wrap classes on every table float, removing it when nothing is left.
- [x] T3: Update the four format snapshots of `tests/fixture.qmd` with `--update` and read the diff. The HTML snapshot records only wrap classes, so add a check to `tests/verify.py` that the AC2 and AC3 tables' `<table>` elements carry `table-striped` where named and that their captions hold no `{`. Plant a fault (skip the rewrite) and see the checks fail. Run `python3 tests/verify.py`.
- [x] T4: Edit the Tables section of `docs/normal-layout.qmd` and step 6 of `cairn/DESIGN.md`. Run `quarto render docs` and `python3 tests/docs_layout.py`.

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
- 2026-10-29: T3: `tests/verify.py --update` passed all 105 renders and changed only the four `fixture` snapshots, read in full. New `TABLE_IDS` and `table_summary` add a `# tables` part to the fixture's HTML snapshot (table classes, caption text). Plant 1 (rewrite skipped): the fixture HTML summary lost two warnings and showed `wrap-left`/`wrap-right` on three float divs and tables. Plant 2 (block written with no `}`): `tbl-caption-block` lost `table-striped` and its caption showed `{.striped`. Filter restored after each.
- 2026-10-29: claim audit: 21 claims read, 1 corrected — tests/verify.py (the `TABLE_IDS` comment said it records the classes that reach each table; it records only `table-striped` and wrap classes; re-read: holds). Other files read: wrapped.lua, docs/normal-layout.qmd, tests/fixture.qmd, cairn/DESIGN.md.
- 2026-10-29: T3, T4 done: `python3 tests/verify.py` (no `--update`) passed all 105 renders at 8f793f1's code; T4 edited the Tables section of `docs/normal-layout.qmd` and DESIGN.md step 6; `quarto render docs` exit 0; `python3 tests/docs_layout.py` 24 `ok`, none failed (`--html` not run). Status set to review.
- 2026-10-29: step-7 approval: m034-table-float-class approved for merge

## Decisions

## Review

Pass 1, 2026-10-29. Main had not moved since the branch was cut. Copilot round off.

spawned: diff-bug, blame-history, prior-review, ripple

Evidence at 3bf323c (after the fix-now commits), from `python3 tests/verify.py` (all 105 renders pass, exit 0) and the committed `tests/_snapshots/fixture.*.txt`:

- AC1: each of `fixture.html.txt`, `fixture.pdf.txt`, `fixture.typst.txt`, and `fixture.docx.txt` holds `1x wrapped: the table #tbl-caption-block is not a figure, so it does not wrap.` and the same line for `#tbl-cell-block`, the text the existing `#tbl-cars` line has.
- AC2: `fixture.html.txt` figures list reads `tbl-caption-block: - style=-`, `tbl-cell-block: - style=-`, `tbl-cell-both: - style=-` (no wrap class on the float divs); its `# tables` part reads `table=table-striped` for `tbl-caption-block` and `table=-` for the two cells (no wrap class on any `<table>`), and the three captions read `Table 2: A table float with a wrap class in its caption`, `Table 3: … in its caption`, `Table 4: … in two places`, with no block text. `#tbl-cell-both` has one warning line (`1x`) in all four snapshots.
- AC3: `fixture.html.txt` has no warning line naming `tbl-striped`, and its `# tables` part reads `tbl-striped: table=table-striped`.
- AC4: `docs/normal-layout.qmd` Tables section (read at 3bf323c) says a wrap class in a table float's caption block, `: A table {.wrap-left}` in a `#tbl-` div or `#| tbl-cap: "A table {.wrap-left}"` in a knitr cell, prints the same warning and keeps the normal layout; its list item on tables with no `#tbl-` id also says they warn and do not wrap. DESIGN.md step 6 says the filter reads that block on a `#tbl-` float, warns, and writes it again without wrap classes. `quarto render docs` exit 0 at 3bf323c.
- AC5: `python3 tests/verify.py` at 3bf323c: "all 105 renders pass", exit 0.
- Consistency gate: `cairn_validate.py` all checks passed; no principle changed, so no `cairn_impact` run; the one version marker, `_extension.yml` `version: 0.2.0`, is unchanged; verify passes (AC5); the diff touches `docs/` and `_extensions/`, so `python3 tests/docs_layout.py` ran at 3bf323c: 24 `ok`, none failed (`--html` not run on the Mac; the docs workflow on the PR runs it); changelog slot "none".
- snapshot: no `_snaps` or `__snapshots__` path in the diff; `tests/_snapshots/fixture.{html,pdf,typst,docx}.txt` changed, each by the cases and checks AC1 to AC3 call for (read in full).

- diff-bug #1: `drop_caption_wrap` keeps the Space before the block and adds another, so LaTeX and Word captions end in a space (`\caption{A table float with a wrap class in its caption␤}` in the fixture), and a block with an id or attribute left gets two spaces before it — fix now, fixed c184f34.
- diff-bug #2: `table_summary` whitespace-normalizes captions, so it cannot see finding #1, and searches past the float's end — fix now, fixed c184f34 (bounded at the float's `</figure>`; new `tex_table_summary` marks a LaTeX caption that ends in white space).
- diff-bug #3: the `table-striped` field for the two knitr tables records knitr's default, not the filter — fix now, fixed c184f34 (`TABLE_IDS` records `table-striped` only where the caption block sets `.striped`).
- diff-bug #4: the `tests/verify.py` docstring does not name `TABLE_IDS` or the `# tables` parts — fix now, fixed c184f34.
- diff-bug #5: the docs sentence reads as if `tbl-cap` takes the `: ` form — fix now, fixed c184f34 (names `#| tbl-cap: "A table {.wrap-left}"`).
- diff-bug #6: subtable panels now warn and lose the class too, with no fixture — reject, planned change: Scope Out names subtable panels as untested.
- blame-history #1: the fix rests on Quarto 1.10.19's order (block read from the float caption after pre-quarto filters), and older supported versions are untested — follow-up, absorbed into "Test the minimum Quarto version in CI".
- blame-history #2: removing the class reverses M033's keep-the-class choice with no D-entry — reject, planned change: the user chose removal at the question set (work log), and M033's choice covered elements that no style reads, while `wrapped.css` selects `.quarto-float.wrap-*`, M033's own falsifying condition.
- blame-history #3: a `#tbl-` float with a wrap class does not set `found_wrap`, so a format that does not wrap prints no format warning — follow-up, new row "Count table floats in the format warning" (predates M034).
- blame-history #4: `pairs(attr.attributes)` may reorder attributes — reject, false: `pandoc lua` iterated `z a m b y` in source order on three runs.
- blame-history #5: `table_summary` searches with no end bound — fix now, fixed c184f34 (same fix as diff-bug #2).
- prior-review #1: the 43 new fixture lines may worsen the known overfull LaTeX page 4 — reject, false: LaTeX renders of main's and the branch's fixture both end page 4's content at 1238 px on a 1188 px page (pdftohtml), the existing row "Fix the overfull LaTeX fixture page".
- prior-review #2: `cairn/references/wrap-mechanisms.md` row E5 not updated — reject, false: E5 reads "`#tbl-` float with a wrap class | Normal table. One warning.", which holds for the caption-block form.
- ripple #1: the candidate row "Warn for wrap classes on table floats" goes stale at merge — reject, planned change: post-merge hygiene graduates it.
- ripple #2: the `tests/verify.py` docstring omits the `# tables` part — fix now, fixed c184f34 (same fix as diff-bug #4).
