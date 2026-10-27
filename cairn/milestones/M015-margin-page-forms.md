<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M015: Fall back in more margin and page forms

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes which wrapped figures the filter keeps normal and what it warns   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m015-margin-page-forms   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A wrapped figure whose caption a `.margin-caption` or `.caption-margin`
class sends to the margin of an HTML page, or that a document-level
`fig-column` or `column` key puts in the margin or a page-wide column,
keeps its normal layout with one warning, in the formats where M013's
forms of the same place do.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** in `_extensions/wrapped/wrapped.lua`, read `.margin-caption` and
`.caption-margin` on a float, its image, and a code cell, and
`.margin-caption` alone on a captioned image with no id, on HTML pages
only (not revealjs). Quarto 1.10.19 keeps the caption of a no-id image
with `.caption-margin` below it (T1 render without the extension). Read
the document's `fig-column`, or else its `column`, and give its margin or
page-wide context to every figure float that no earlier check keeps
normal. Quarto 1.10.19 applies that key to a cell's float even when the
cell sets `fig-column: body` (same render). New cases in
`tests/cap-margin.qmd` and `tests/revealjs.qmd`, and new fixtures
`tests/margin-meta.qmd`, `tests/page-wide-meta.qmd`, and
`tests/column-meta.qmd`, each with its `tests/verify.py` entries and
snapshots. The README section "Where a figure keeps its normal layout",
rows E20 and E21 of `cairn/references/wrap-mechanisms.md`, and the
context-check step in `cairn/DESIGN.md`'s Architecture.

**Out:** Quarto applies neither document key to a captioned image with no
id, so such an image keeps wrapping (no row: Quarto's behavior, pinned by
the fixtures). A figure's own column class, or a cell's own `fig-column`
or `column` option, is read before the document key. Where the figure's
own class or option and the document key name different places, the
filter can keep a figure normal with the wrong reason, or in a format
where Quarto puts it in the body. No fixture sets both keys, and none sets
`column: margin`. All three go to the row "Read fig-column over a
figure's class". Dashboards stay with the row "Check wrapped figures in
dashboards".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

Snapshots are those `python3 tests/verify.py` compares. A figure with an id
**wraps** when its HTML or revealjs `# figures` line shows `wrap-right` or
`wrap-left`, the LaTeX `# tex` block has `wrappedfigure: <id>`, or the Typst
`# wraps` box field or Word `# frames` bookmark field is `<id>`. It **keeps
its normal layout** when that line is absent and its HTML `# figures` line
reads `<id>: - style=-` with no `# groups` line naming it. A captioned image
with no id wraps when HTML has a `(box): wrapped-image` line, LaTeX a
`wrappedfigure: -` line without `caption=false`, the Typst box field is its
image file, or the Word bookmark field is `-`, each with its side and width
where two such images share a snapshot. It keeps its normal layout when that
line is absent. A warning line reads
`1x wrapped: the figure #<id> <reason>, so it does not wrap.`, or
`1x wrapped: a figure with no id <reason>, so it does not wrap.`

- [ ] AC1: In the `cap-margin` HTML snapshot, five figures added to
      `tests/cap-margin.qmd` keep their normal layout, each with one warning
      whose reason is `has its caption in the margin`: `fig-margincap-class`
      (image form, `.margin-caption`), `fig-capmargin-class` (image form,
      `.caption-margin`), `fig-margincap-div` (div form, `.margin-caption`), a
      captioned image with no id and `.margin-caption` (`wrap-right`), and the
      knitr cell `fig-capclass-cell` (`#| classes: wrap-right .caption-margin`).
      A no-id image with `.caption-margin` (`wrap-left`, `width="30%"`) wraps,
      and the warning line for a figure with no id reads `1x`.
- [ ] AC2: The six figures AC1 names wrap in the `cap-margin` LaTeX, Typst, and
      Word snapshots, whose `# warnings` blocks stay empty. The figure
      `fig-slide-margincap` (`.margin-caption`) added to `tests/revealjs.qmd`
      wraps, and the `revealjs` `# warnings` block stays empty.
- [ ] AC3: In `tests/margin-meta.qmd` (document `fig-column: margin`), the
      image-form float `fig-meta-margin`, the div-form float
      `fig-meta-margin-div`, the knitr cell `fig-meta-margin-cell`, and the
      knitr cell `fig-meta-body-cell` (`#| fig-column: body`) keep their normal
      layout in the HTML, LaTeX, Typst, and Word snapshots, each with one
      warning whose reason is `is in the margin`. A captioned image with no id
      wraps in all four.
- [ ] AC4: In `tests/page-wide-meta.qmd` (document `fig-column: page`), the
      image-form float `fig-meta-page`, the knitr cell `fig-meta-page-cell`,
      and the knitr cell `fig-meta-page-body` (`#| fig-column: body`) keep
      their normal layout in the HTML, LaTeX, and Typst snapshots, each with
      one warning whose reason is `is page-wide`, and wrap in Word. A
      captioned image with no id wraps in all four.
- [ ] AC5: In the `column-meta` HTML and LaTeX snapshots (document
      `column: page`), the float `fig-col-page`, the knitr cell `fig-col-cell`
      (no column option), and the knitr cell `fig-col-body-cell`
      (`#| fig-column: body`) keep their normal layout, each with one warning
      whose reason is `is page-wide`. A no-id captioned image wraps in both.
- [ ] AC6: The README section "Where a figure keeps its normal layout" names
      the two caption classes in the margin-caption item, the document
      `fig-column` key in the margin and page-wide items, and the document
      `column` key in the page-wide item, each with the formats AC1 to AC5
      test.
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

- [x] T1: Write the fixture cases first and render each without the
      extension (`filters:` removed) to record where Quarto puts each
      figure and caption: the five caption-class cases, the slide case,
      and the three metadata fixtures. A case whose render does not put
      the figure or caption where the criteria assume is an amendment
      before T2. Add the fixtures to `tests/verify.py`'s list.
- [x] T2: In `wrapped.lua`, extend `caption_location` (about line 1117)
      and `figure_block`'s check (about line 1336) so that the two classes
      on the float, its image, or its cell read as a margin caption, on
      HTML pages only.
- [x] T3: Read `fig-column`, or else `column`, in `read_meta`, turn it
      into a context with `class_context`, and add that context to the
      float pass's checks (about line 1277), after the class and panel
      checks. A dump filter after `wrapped` (lesson 2026-10-27, M013)
      shows which classes reach the float.
- [x] T4: Run `python3 tests/verify.py --update`, read each new and
      changed snapshot against AC1 to AC5, and run it again without
      `--update`.
- [x] T5: Update the README section, rows E20 and E21 of
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
- 2026-10-27: implement started on branch m015-margin-page-forms.
- 2026-10-27: checkpoint (T1 to T3 code, T5 docs drafted, not checked off): T1's render without the extension showed a cell's own `fig-column: body` does not keep its float in the body under a document key, a no-id image moves its caption only for `.margin-caption`, and `classes: wrap-right caption-margin` writes broken attributes. A criteria amendment for AC1 to AC5 is with its second fresh reader; T4's snapshots wait for it.
- 2026-10-27: re-audit: AC1 (full) — the Scope still read `.caption-margin` on a no-id image, and no AC1 case kept wrapping; fixed with a no-id `.caption-margin` case that wraps.
- 2026-10-27: re-audit: AC3 (full) — only the no-id image wraps, through `figure_block`, not the float pass; no change (no float can stay in the body under a document key in Quarto 1.10.19).
- 2026-10-27: re-audit: AC4 (full) — same as AC3; the floats that wrap in Typst and Word are the float-pass cases that can fail.
- 2026-10-27: re-audit: AC5 (full) — no case kept wrapping and "renders to HTML and LaTeX" bound the test setup; fixed with a no-id image in `column-meta` and snapshot wording. Also fixed: "`fig-column` before `column`" dropped from Scope (untested), Scope Out widened to a cell's own option, T3 rewritten.
- 2026-10-27: re-audit: AC1 (full) — "no warning names a second figure with no id" did not fit the counted warnings block, and the lead's Typst clause applied to no figure; the user approved the narrowed wording at the stop (AC1 now reads `1x`, the Typst clause dropped, Scope limited to `fig-column: body`, the candidate row lists all three gaps).
- 2026-10-27: re-audit: AC3 (full) — nothing.
- 2026-10-27: re-audit: AC4 (full) — nothing.
- 2026-10-27: re-audit: AC5 (full) — nothing.
- 2026-10-27: substantive amendment: AC1, AC3, AC4, AC5, the lead paragraph, Scope, and T3 follow T1's render without the extension. A cell's `fig-column: body` keeps its normal layout under a document key, a no-id image is tested with `.margin-caption` (falls back) and `.caption-margin` (wraps), the cell uses `wrap-right .caption-margin`, and `column-meta` adds a no-id image. What the user gets is unchanged: a figure keeps its normal layout where Quarto moves it.
- 2026-10-27: plan's choice reversed: the document key now reaches every figure float, not only one with no `fig-column-*` class, because Quarto 1.10.19 puts a `fig-column: body` cell's float in the margin or page-wide under a document key (T1 render); falsified by a Quarto release that lets a cell's own `fig-column` win.
- 2026-10-27: plan-owned body was 154 lines after the amendment; the Acceptance criteria section was rewrapped once, and AC5 lost the redundant file name.
- 2026-10-27: T4: `python3 tests/verify.py --update` wrote the 4 `cap-margin` and the `revealjs` snapshots and 10 new ones, and no other snapshot changed; each read against AC1 to AC5; the run without `--update` passes all 86 renders. A planted bug (reading `.caption-margin` on a no-id image) turned the no-id warning to `2x` and removed the wrapping `(box)` line in the `cap-margin` HTML render.
- 2026-10-27: claim audit: 21 claims read, 5 corrected — README.md, wrapped.lua, tests/cap-margin.qmd, tests/margin-meta.qmd, tests/page-wide-meta.qmd, tests/page-wide.qmd. A cell's `.margin-caption` moved the caption but wrapped (fixed: the cell's class is carried to its float, case `fig-margincap-cell` added); the README margin item's sentence order (fixed); margin-meta's "every format" for Quarto's margin (fixed: Word has none); the `caption_location` comment called the attribute order Quarto's (fixed); Typst page-wide figures overlap the text (stop, below).
- 2026-10-27: substantive amendment: AC4 — the page-wide floats now keep their normal layout in Typst too, and wrap in Word. The user chose this at the stop: Quarto 1.10.19 sets all 16 page-wide classes wider than the text in Typst (`wideblock` or a column function), and a wrapped figure there overlapped the paragraph beside it (claim audit render). `page_context` now covers Typst, which also changes M013's `page-wide` Typst snapshot, the README page-wide item, E21, and DESIGN step 2.
- 2026-10-27: pre-existing bug found by the claim audit and checked by a render: Quarto 1.10.19 follows `cap-location` over `fig-cap-location`, but `caption_location` and the README read `fig-cap-location` first, so `fig-figcap-first` in `cap-margin` wraps while its caption sits in the margin. Recorded as the candidate row "Read cap-location before fig-cap-location", whose door is `/hotfix`.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
