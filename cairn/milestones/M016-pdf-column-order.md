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

- [x] AC1: This criterion covers the figures listed below, in the LaTeX
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
- [x] AC2: The README section "Where a figure keeps its normal layout"
      states the order in which the filter reads a figure's column in PDF
      through LaTeX and PDF through Typst, with the four sources that the
      Scope names. It states that HTML and Word read a figure's own class
      first. Its margin item names a document `column: margin`.
- [x] AC3: `python3 tests/verify.py` exits 0 locally and in the verify
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
- 2026-10-27: checkpoint (review): fix-now changes for the four-lens findings committed before the re-run of verify finished; the verify result is recorded next.
- 2026-10-27: implement done, status review. No code change since the 95-render verify pass; later edits touched README.md and cairn/ only.
- 2026-10-28: review resumed at the merge question (no PR, main unmoved, no code change since 5260ed7's 95-render run); the first chip was dismissed without an answer.
- 2026-10-28: step-7 approval: m016-pdf-column-order approved for merge
- 2026-10-28: PR #17 opened, CI green, squash-merged as c8b6613; post-merge hygiene on main.

## Decisions

## Review

- AC1: fresh bare renders of the four fixtures (scratchpad `review-bare`, LaTeX and Typst) read by `place.py` against the committed snapshots: 40 figure-format checks (the 20 figures AC1 lists, in two formats), 0 failures. Each body figure wraps with no warning, each margin figure warns `is in the margin`, each page-wide figure warns `is page-wide`, and no other warning appears. A planted copy (one wrap line removed, one reason changed) failed 4 checks, so the check can fail.
- AC2: README.md:220-236 states the order in LaTeX and Typst with the four sources (lines 224-227), the cell rule, and HTML and Word reading a margin or page-wide class (HTML) or a margin class (Word) first; the margin item names a document `column: margin` (line 208).
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a wrapped cell whose output writes a float with its own `.column-margin` lost that class in PDF (`if cell then return document end`), so the figure wrapped where Quarto puts it in the margin — fix now, fixed 5260ed7 (cell floats now take the float order; not judged load-bearing: it needs a cell that writes figure markdown)
- diff-bug #2: a layout float under a document key warned `is page-wide` in Typst, where Quarto keeps it in the body — fix now, fixed 5260ed7 (a document value is read after the layout check again, as on main)
- diff-bug #3: README "That value applies to every figure with a `#fig-` id" (margin and page-wide items) is false in PDF under the new order — fix now, fixed 5260ed7
- diff-bug #4: README "a `.column-margin` figure wraps in PDF" also covers a captioned image with no id, which does not wrap — fix now, fixed 5260ed7 (now "with a `#fig-` id")
- diff-bug #5: column-order fixtures repeat one filter code path across cases — reject, planned change: AC1 names each case, and the cases vary Quarto's placement input (form and source), which the plan's criteria audit asked for
- diff-bug #6: no test for #1 or #2 — fix now, fixed 5260ed7 (fig-page-asis-margin and fig-page-panel added to column-order-page.qmd)
- blame-history #1: README "applies to every figure" contradicts the order — fix now, fixed 5260ed7 (same as diff-bug #3)
- blame-history #2: a panel under a document key changed its reason from M015's order — fix now, fixed 5260ed7 (same as diff-bug #2); the M015 archive stays as history
- blame-history #3: the cell skip keys on any document value, `column: body` included, and drops a cell's margin context for a bare image — reject in part, false: the claim audit's bare render of `column: body` puts a `#| column: margin` cell's figure in the body; the bare-image part is follow-up, row "Read cell images by column order in PDF"
- blame-history #4: D-010's one warning per cell does not hold for a cell in a place, now also under PDF document keys — follow-up, row "Warn once per cell under a context" (M018)
- blame-history #5: README step 3 omits `.aside`, which the code and Quarto's `isColumnClass` count — fix now, fixed 5260ed7
- blame-history #6: README "in either format" can be read as PDF — fix now, fixed 5260ed7 (now "In HTML and in Word")
- blame-history #7: the `cell and .cell or .float` idiom — reject, false (the lens found no effect)
- prior-review #1: the README's HTML and Word sentence has no new render — reject, planned change: AC2 asks for it, it describes main's unchanged HTML and Word code (claim audit), column-meta's HTML snapshot pins a body option not overriding the document key, and HTML placement is the row "Check HTML column order in a browser"
- prior-review #2: a bare wrapped image in a margin cell under a document key — follow-up, row "Read cell images by column order in PDF"
- prior-review #3: a layout float's reason under a document key — fix now, fixed 5260ed7 (same as diff-bug #2)
- prior-review #4: README HTML sentence lacks the bare-render caveat — reject, false: part of prior-review #1, and the row holds the caveat
- ripple #1: E21 "A document-level value applies to every figure float" and "A margin value keeps the figure normal in every format" — fix now, fixed 5260ed7
- ripple #2: E3 "Margin wins" — fix now, fixed 5260ed7 (PDF exception added)
- ripple #3: README page-wide and margin items say the value applies to every figure — fix now, fixed 5260ed7 (same as diff-bug #3)
- ripple #4: README margin item "The figure stays in the margin" — fix now, fixed 5260ed7 (PDF exception named)
- ripple #5: DESIGN step 4 "any figure float when the document's `fig-column` or `column` names the margin" — fix now, fixed 5260ed7
- ripple #6: wrapped.lua comment in `float_target` "A document-level fig-column or column puts the float in the margin" — fix now, fixed 5260ed7
- ripple #7: ROADMAP row "Read fig-column over a figure's class" states the old behavior — reject, planned change: the row graduates at this merge's hygiene
- ripple #8: ROADMAP row "Warn once per cell under a context" says the context check runs before the cell check — reject, false: it still does in every format
- ripple #9: margin-meta.qmd and page-wide-meta.qmd prose says every float is in the margin or page-wide — reject, false: those fixtures' floats carry no column class of their own
- ripple #10: the `meta_fig_column_set` comment is garbled — fix now, fixed 5260ed7
- ripple #11: the README order states no Quarto version — fix now, fixed 5260ed7 (now "the order of Quarto 1.10.19")
- gate: `cairn_validate.py` all checks passed; `_extension.yml` is the one version marker (0.1.0, unchanged); `python3 tests/verify.py` on 5260ed7: all 95 renders pass, tree clean after the run; changelog slot is none; no principle changed, so `cairn_impact` is skipped.
- AC1 after the fixes: the placement check re-run on 5260ed7's snapshots passes all 40 AC1 figure-format checks and the new fig-page-asis-margin; fig-page-panel, outside AC1's list, keeps its normal layout as a subfigure panel.
- snapshot: tests/_snapshots/column-order*.{pdf,typst}.txt — 8 new files; AC1 and AC3 call for them, and column-order-page's two also hold the fix-now cases fig-page-asis-margin (`is in the margin`) and fig-page-panel (`is a subfigure panel`)
- AC3: `python3 tests/verify.py` on 5260ed7: all 95 renders pass. The verify workflow on PR #17 (run 40599709769) passed in 7m31s. `git diff --name-status main` before the merge listed only the 8 added column-order snapshot files under `tests/_snapshots/`.
