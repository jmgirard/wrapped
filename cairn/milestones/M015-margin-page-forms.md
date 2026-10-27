<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M015: Fall back in more margin and page forms

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes which wrapped figures the filter keeps normal and what it warns   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A wrapped figure whose caption a `.margin-caption` or `.caption-margin`
class sends to the margin of an HTML page, or that a document-level
`fig-column` or `column` key puts in the margin or a page-wide column,
keeps its normal layout with one warning, in the formats where M013's
forms of the same place do.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** in `_extensions/wrapped/wrapped.lua`, read the two caption classes
on a float, on its image, on a captioned image with no id, and on a code
cell, as M013's caption-location check does (HTML pages only, not
revealjs). Read the document's `fig-column` and `column` metadata and
apply them to a float through the existing margin and page-wide rules,
only where the float, its image, and its cell carry no `fig-column-*`
class. New cases in `tests/cap-margin.qmd` and `tests/revealjs.qmd`; new
fixtures `tests/margin-meta.qmd`, `tests/page-wide-meta.qmd`, and
`tests/column-meta.qmd`, each with its `tests/verify.py` entries and
snapshots. The README section "Where a figure keeps its normal layout",
rows E20 and E21 of `cairn/references/wrap-mechanisms.md`, and the
context-check step in `cairn/DESIGN.md`'s Architecture.

**Out:** Quarto applies neither document key to a captioned image with
no id, so such an image keeps wrapping (no row: this is Quarto's
behavior, and the fixtures pin it). Quarto puts a document's
`fig-column` before a figure's own `column-*` class, so a `.column-margin`
figure in a `fig-column: body` document sits in the body, but the
existing class check still keeps it normal with a margin warning: the
candidate row "Read fig-column over a figure's class". A document-level
`column: margin` is read by the same code but has no fixture, and the
README names `column` only for page-wide columns (same row). Dashboards
stay with the row "Check wrapped figures in dashboards".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

Snapshots are those `python3 tests/verify.py` compares. A figure with an
id **wraps** when its HTML or revealjs `# figures` line shows `wrap-right`
or `wrap-left`, the LaTeX `# tex` block has `wrappedfigure: <id>`, or the
Typst `# wraps` box field or Word `# frames` bookmark field is `<id>`. It
**keeps its normal layout** when that line is absent, its HTML `# figures`
line reads `<id>: - style=-` with no `# groups` line naming it, and the
Typst `# typ` block has `figure: <id>`. A captioned image with no id wraps
when HTML has a `(box): wrapped-image` line, LaTeX a `wrappedfigure: -`
line without `caption=false`, the Typst box field is its image file, or
the Word bookmark field is `-`; it keeps its normal layout when that line
is absent. A warning line reads `1x wrapped: the figure #<id> <reason>,
so it does not wrap.`, or `1x wrapped: a figure with no id <reason>, …`.

- [ ] AC1: In the `cap-margin` HTML snapshot, five figures added to
      `tests/cap-margin.qmd` keep their normal layout, each with one
      warning whose reason is `has its caption in the margin`:
      `fig-margincap-class` (image form, `.margin-caption`),
      `fig-capmargin-class` (image form, `.caption-margin`),
      `fig-margincap-div` (div form, `.margin-caption`), a captioned image
      with no id and `.caption-margin`, and the knitr cell
      `fig-capclass-cell` (`#| classes: wrap-right caption-margin`).
- [ ] AC2: The same five wrap in the `cap-margin` LaTeX, Typst, and Word
      snapshots, whose `# warnings` blocks stay empty. The figure
      `fig-slide-margincap` (`.margin-caption`) added to
      `tests/revealjs.qmd` wraps, and the `revealjs` `# warnings` block
      stays empty.
- [ ] AC3: In `tests/margin-meta.qmd` (document `fig-column: margin`), the
      image-form float `fig-meta-margin`, the div-form float
      `fig-meta-margin-div`, and the knitr cell `fig-meta-margin-cell`
      keep their normal layout in the HTML, LaTeX, Typst, and Word
      snapshots, each with one warning whose reason is `is in the
      margin`. The cell `fig-meta-body-cell` (`#| fig-column: body`) and
      a captioned image with no id wrap in all four.
- [ ] AC4: In `tests/page-wide-meta.qmd` (document `fig-column: page`),
      the image-form float `fig-meta-page` and the knitr cell
      `fig-meta-page-cell` keep their normal layout in the HTML and LaTeX
      snapshots, each with one warning whose reason is `is page-wide`, and
      wrap in Typst and Word. The cell `fig-meta-page-body`
      (`#| fig-column: body`) and a captioned image with no id wrap in all
      four.
- [ ] AC5: `tests/column-meta.qmd` (document `column: page`) renders to
      HTML and LaTeX. In both snapshots the float `fig-col-page` and the
      knitr cell `fig-col-cell` (no column option) keep their normal
      layout, each with one warning whose reason is `is page-wide`, and
      the cell `fig-col-body-cell` (`#| fig-column: body`) wraps.
- [ ] AC6: The README section "Where a figure keeps its normal layout"
      names the two caption classes in the margin-caption item, the
      document `fig-column` key in the margin and page-wide items, and the
      document `column` key in the page-wide item, each with the formats
      AC1 to AC5 test.
- [ ] AC7: `python3 tests/verify.py` exits 0 on macOS, and the `verify`
      workflow passes on the milestone's PR.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2, T4
- AC2 → T1, T2, T4
- AC3 → T1, T3, T4
- AC4 → T1, T3, T4
- AC5 → T1, T3, T4
- AC6 → T5
- AC7 → T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [ ] T1: Write the fixture cases first and render each without the
      extension (`filters:` removed) to record where Quarto puts each
      figure and caption: the five caption-class cases, the slide case,
      and the three metadata fixtures. A case whose render does not put
      the figure or caption where the criteria assume is an amendment
      before T2. Add the fixtures to `tests/verify.py`'s list.
- [ ] T2: In `wrapped.lua`, extend `caption_location` (about line 1117)
      and `figure_block`'s check (about line 1336) so that the two classes
      on the float, its image, or its cell read as a margin caption, on
      HTML pages only.
- [ ] T3: Read `fig-column` and `column` in `read_meta` (about line
      1122), and in the float pass give the document's value to
      `margin_context` and `page_context` (about line 1256) for a float
      whose float, image, and cell carry no `fig-column-*` class, the
      document's `fig-column` before its `column`. A dump filter after
      `wrapped` (lesson 2026-10-27, M013) shows which classes reach the
      float.
- [ ] T4: Run `python3 tests/verify.py --update`, read each new and
      changed snapshot against AC1 to AC5, and run it again without
      `--update`.
- [ ] T5: Update the README section, rows E20 and E21 of
      `cairn/references/wrap-mechanisms.md`, and the context-check step of
      `cairn/DESIGN.md`'s Architecture (about line 149).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: question set: what to work on — "Fall back in more margin and page forms" (the recommended dashboards row not chosen); the dashboards question did not apply.
- 2026-10-27: idea vet: no concern. Scratch renders on Quarto 1.10.19 showed both caption classes (on a float, a div, a no-id image, and a code cell) move the caption to the margin with no warning, and a document `fig-column: margin` puts a wrapped float in the margin with no warning; Quarto applies document column keys to floats only, so the scope adds `fig-column: margin` and the `column` key to the row.
- 2026-10-27: collision check: candidate row "Fall back in more margin and page forms" absorbed (from M013's criteria audit); extends archived M013; no D-entry bears on it; inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-27: lessons used: 2026-10-27 (M013) on Quarto copying cell options and the dump filter; 2026-10-27 (M012) on checking one fixture without the full run.
- 2026-10-27: plan chose reading a document column key only where no `fig-column-*` class comes first over modeling Quarto's full four-step order, because the full order lets a document key override a figure's own margin class, which the existing class check reads first; falsified by a user report of a `.column-margin` figure under a document `fig-column` that falls back wrongly (row "Read fig-column over a figure's class").
- 2026-10-27: criteria audit (full mode, fresh Opus reader): 11 findings. Fixed: no-id naming per format and its warning text (1, 3), normal layout needs the figure's own line in HTML and Typst (2), empty warnings blocks and T1 in AC2's coverage (4), a div-form float in margin-meta (5), a plain cell and named formats for column-meta (7), README claim narrowed to `column` for page-wide only (8), Scope order contradiction narrowed with a candidate row (10). No change: AC4 (6), AC7 binds the gate as every milestone does (9), bounded promises (11).
- 2026-10-27: plan-owned body was 159 lines; the Acceptance criteria section was rewritten once to 150 or fewer, with the warning text stated once in the lead paragraph and no promise changed.
- 2026-10-27: remainder ledger: both caption classes and the document `fig-column` key are in M015, with the `column` key added; the class-order gap and `column: margin` go to the new row "Read fig-column over a figure's class"; nothing dropped.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
