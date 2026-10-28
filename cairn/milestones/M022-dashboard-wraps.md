<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M022: Wrap figures in dashboard cards

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes how wrapped figures render in Quarto dashboards
- **Branch/PR:** m022-dashboard-wraps

## Goal

In a Quarto dashboard, a wrapped code-cell figure inside a `.card` div wraps the text after it in that card, and a wrapped code-cell figure outside a `.card` div keeps its normal layout with a warning.

## Scope

**In:**
- `_extensions/wrapped/wrapped.css`: inside a `.wrap-group`, a code cell's `.cell` and `.cell-output-display` wrappers that a dashboard marks `html-fill-container` (a flex column, where a float has no effect) display as blocks, so the cell figure's float reaches the paragraphs after the cell. A scratch render (Quarto 1.10.19) showed this with an injected rule: text top 540 px, level with the figure top. A `.wrap-group` that a dashboard marks `html-fill-item` takes `flex: 0 0 auto`, so a card that fills its height does not shrink the group below its content and lay the next block over the figure.
- `_extensions/wrapped/wrapped.lua`: in a dashboard (`quarto.doc.is_format("dashboard")`), a code cell that is not inside a `.card` div is a context that cannot wrap, found in pass 2 (`find_contexts`, `block_context`), with the context phrase "is outside a card in a dashboard". At the row and column level, Quarto's post-render dashboard filter makes such a cell a card of its own (`filters/main.lua`, the `Div` handler for `cell`), so the paragraphs after it fall outside that card. Its figure keeps its normal layout with one context warning, and a cell that makes more than one figure keeps its one cell warning, which then names the place (M018 rule, the `several and context` branch of `float_target`).
- `tests/layout.js`: `nextBlock` stops at the group's `.card-body`, skips `display: contents` elements, and reads classes with `getAttribute("class")`, so a group that ends its card gets no group entry instead of a false one (the audit measured `ok: false` for every in-card group and a `TypeError` for a group in a sidebar).
- A new fixture `tests/dashboard.qmd`, rendered with `--to dashboard`, a `RENDERS` row and snapshot in `tests/verify.py`, with `summary` reading a `dashboard` render as HTML.
- README: the intro's "Dashboards are not tested yet." goes; a "Dashboards" section and an item in "Where a figure keeps its normal layout" state the behavior. DESIGN.md step 2 names the dashboard context, and its `wrapped.css` text names the block display.
- A markdown figure and an image already wrap in a dashboard card: `wrapped.css` loads after Bootstrap, so `.wrap-group { display: flow-root }` wins over bslib's `.html-fill-container { display: flex }` (scratch render: figure floats right at 281 of 701 px, text beside it). The fixture records them as cases that must keep wrapping.

**Out:**
- Dashboard sidebars, tabsets (`{.tabset}` on a heading), value boxes, and card toolbars: not checked here. A cell in a `.sidebar`, `.toolbar`, or `.valuebox` div is outside a `.card` div, so it gets the same warning, unrendered → new `[low]` candidate row "Check wraps in dashboard sidebars".
- Phone widths: the 576 px breakpoint rule of every HTML page applies; no work owed.
- Making a cell outside a card wrap, for example by having the filter put the cell and its paragraphs in a card: not planned (work log); the README tells the user to write the `.card` div.

## Acceptance criteria

- [ ] AC1: In `tests/dashboard.qmd` rendered with `quarto render dashboard.qmd --to dashboard`, `report()` of `tests/layout.js`, run in a browser at 1280x900 after a reload, returns a figure entry with `ok: true` for each of these four: a captioned markdown figure in a `.card` div; an uncaptioned image with `.wrap-left` in the card Quarto makes from a column's content; a knitr cell figure with `#| classes: wrap-right` inside a `.card` div, followed in that card by a paragraph of at least 3 lines and then a bullet list; and a knitr cell figure with `#| classes: wrap-left` inside a `{.card fill="false"}` div, followed by a paragraph of at least 3 lines. The group entry of the third figure, whose next block is the list, has `ok: true`.
- [ ] AC2: In the same render, a knitr cell figure with `#| classes: wrap-left` that is not inside a `.card` div, followed by a paragraph, keeps its normal layout: the `dashboard` snapshot lists its figure div with no wrap class, and its `# warnings` section holds one warning that names its `fig-` id and reads "is outside a card in a dashboard, so it does not wrap". A knitr cell with a `fig-` label, outside a `.card` div, that draws two plots, followed by a paragraph, gets one warning that names the cell's label with the same phrase, and no warning names either of its figures.
- [ ] AC3: In the `dashboard` snapshot, the four figures of AC1 keep their wrap class, the `# groups` section holds exactly four lines, one for each AC1 figure, each listing its figure (a `cell` member for a cell figure) and the paragraphs after it, and no warning names any of the four.
- [ ] AC4: README states that in a dashboard a wrapped figure, image, or code-cell figure inside a card wraps the text after it in that card; that a code cell outside a `.card` div keeps its normal layout with a warning; and that a `.card` div around the cell and its paragraphs makes it wrap. The README no longer says that dashboards are not tested. DESIGN.md step 2 names the dashboard cell context, and the DESIGN.md text on `wrapped.css` names the block display of the cell wrappers.
- [ ] AC5: `python3 tests/verify.py` exits 0 on macOS, and the PR's `verify` check passes.

## Coverage

- AC1 → T1, T2, T3, T5
- AC2 → T1, T4, T5
- AC3 → T1, T4, T5
- AC4 → T6
- AC5 → T7

## Tasks

- [x] T1: Fixture first. Write `tests/dashboard.qmd` (`format: dashboard`, `filters: [wrapped]`, `fig-format: png`) with the six cases of AC1 and AC2, each figure followed by a paragraph of at least 3 lines; the two-plot cell needs a `fig-` label, or knitr makes no float. Add `("dashboard", "dashboard", True)` to `RENDERS` in `tests/verify.py` and make `summary` send a `dashboard` render to `html_summary`. Render with `main`'s filter, run `report()` at 1280x900, and confirm that each cell-in-card figure's entry has `ok: false` with `beside: false`, and that the cells outside a card keep a wrap class and print no warning.
- [x] T2: In `tests/layout.js`, make `nextBlock` stop at the group's closest `.card-body` (return null there), skip `display: contents` elements, and read the next block's classes with `getAttribute("class")`.
- [x] T3: In `wrapped.css`, give `.wrap-group .cell.html-fill-container` and `.wrap-group .cell-output-display.html-fill-container` `display: block`, with a comment that names the dashboard flex wrappers, and give `.wrap-group.html-fill-item` `flex: 0 0 auto`.
- [x] T4: In `wrapped.lua`, add an `is_dashboard` flag beside `is_revealjs` (line 38). In pass 2, mark a code cell Div that is not inside a `.card` Div as the context "is outside a card in a dashboard", so its floats get the context warning in the float pass and a two-figure cell gets the one cell warning. Contexts inside a `.card` div (a callout, a list) are still found.
- [x] T5: Run the fixture with `--update`, read the new snapshot, confirm that no other snapshot changes, and check AC1's figures and group with `report()` at 1280x900 in the built-in browser.
- [x] T6: Write the README and DESIGN.md text for AC4.
- [ ] T7: Run `python3 tests/verify.py` in full on macOS.

## Work log

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: not run — work named at the question set
- 2026-10-28: question set: work to plan — candidate row "Check wrapped figures in dashboards"; run — full run through implement and review to the merge question.
- 2026-10-28: idea vet: no concern. The row's guess that a float has no effect in a dashboard is false for a markdown figure and an image: a scratch render (Quarto 1.10.19) floated each beside its text in a card. It holds for a code-cell figure, whose `.cell` and `.cell-output-display` are flex containers (text starts below the figure, no warning). A cell outside a `.card` div becomes a card of its own, where no float can reach the text; the fallback there is the user's answer recorded on the row at the M021 plan.
- 2026-10-28: lessons used: 2026-10-24 (M001), 2026-10-25 (M002), 2026-10-27 (M012), 2026-10-27 (M015), 2026-10-28 (M018), 2026-10-28 (M020)
- 2026-10-28: collision check: absorbs candidate row "Check wrapped figures in dashboards" (from M002; M015's question set passed it over). Works under D-001 (the filter reads the cell div) and D-010 (a two-figure cell keeps its figures normal); no D-entry changes. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-28: plan chose to scope the CSS rule to wrappers with `html-fill-container`, over setting every `.wrap-group .cell` to block, because only dashboards make those wrappers flex and the narrower rule leaves other HTML pages as they are; falsified by another Quarto HTML format that makes cell wrappers flex without that class.
- 2026-10-28: plan chose a normal layout with a warning for a cell outside a card, over having the filter put the cell and its paragraphs in a `.card` div, because a card the user did not write changes the dashboard's layout and the user chose the fallback where a float cannot work; falsified by user reports that want such cells to wrap without a hand-written card.
- 2026-10-28: criteria audit (full mode, fresh Opus reader): 11 items, 6 fixed, 5 no change. Fixed: `report()` gave false group entries in cards and threw in a sidebar (new T2 for `nextBlock`; AC1 names one in-card group, closed by a list); "becomes a card of its own" is false in sidebars, toolbars, and value boxes (neutral phrase "is outside a card in a dashboard"; Out names them); the snapshot records a cell group member as `cell` (AC3 counts exactly four group lines); AC2 names the warning phrase; one cell case stood in for fill and non-fill cards (fourth AC1 figure in a `fill="false"` card); a two-plot cell needs a `fig-` label (T1). No change: the T1 baselines, T3's CSS effect, the uncaptioned-image case (audit render `ok: true`), AC5, and the D-entries.
- 2026-10-28: T1: `tests/dashboard.qmd` (figures `fig-dash-md`, an uncaptioned `plot.png`, `fig-dash-card`, `fig-dash-nofill`, `fig-dash-bare`, `fig-dash-two`) and a `dashboard` row in `RENDERS`. Baseline with `main`'s filter: `report()` at 1280x900 gives `fig-dash-card` and `fig-dash-nofill` `ok: false`, `beside: false`; `fig-dash-bare` keeps `wrap-left` and the only warning is the two-plot cell's "makes more than one figure"; every group but `fig-dash-card`'s reads a `bslib-tooltip` at top 0.
- 2026-10-28: T2: `nextBlock` stops at the closest `.card-body`, skips `display: none` and `contents`, and the entry reads `getAttribute("class")`. The dashboard now gives one group entry (`fig-dash-card`, next `ul`, `ok: false` before T3); `stop-shortcode.html` still gives 13 of 13 figure and 13 of 13 group entries `ok: true`.
- 2026-10-28: substantive amendment: Scope In and T3 add `.wrap-group.html-fill-item { flex: 0 0 auto }`. With the cell rule alone, `fig-dash-card` and `fig-dash-nofill` reported `ok: true`, but the fill card shrank `fig-dash-card`'s group to 116 px and its list started at 516 px over a figure ending at 588 px (group entry `ok: false`). With the rule, the list starts at 629 px and the card body scrolls. No criterion changes; AC1's group clause needs it.
- 2026-10-28: T3: both rules in `wrapped.css`. After a cache-bypassing reload, `report()` at 1280x900 gives the four AC1 figures `ok: true` (the cell rule served from the render; the group rule injected in the page before the edit). Re-check from a fresh render at T5.
- 2026-10-28: T4: `is_dashboard` flag; `find_contexts` walks a `.card` div's content with `card_depth` raised, and `block_context` names a `cell` Div (not `.markdown`, which Quarto unwraps) "is outside a card in a dashboard" at depth 0. Render: `fig-dash-bare` and `fig-dash-two` warn with that phrase and lose the wrap class; the four card figures keep theirs. A scratch render of a callout inside a `.card` still warns "is in a callout".
- 2026-10-28: T6: README intro names dashboards, "Where a figure keeps its normal layout" gets a dashboard item, and a new "Dashboards" section (after "Slides") states the card rule, the fallback outside a `.card` div, a `.card` example, and that sidebars, tabsets, value boxes, and toolbars are not tested. DESIGN.md steps 2 and 5 name the context and the two CSS rules; the `verify.py` docstring names the dashboard snapshot.
- 2026-10-28: T5: `verify.py --update` passed all 103 renders and changed no snapshot but the new `dashboard.dashboard.txt` (two "is outside a card in a dashboard" warnings, `fig-dash-bare` and `fig-dash-two-*` with no wrap class, four group lines). `report()` at 1280x900 on the T4 render, after a cache-bypassing reload, gave the four AC1 figures `ok: true` and the `fig-dash-card` group (next `ul` at 629 px, figure bottom 588 px) `ok: true`.

## Decisions

## Review
