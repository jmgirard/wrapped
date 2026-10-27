<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M014: Keep two-figure cells unwrapped

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes how the filter renders a wrapped code cell and what it warns   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m014-two-figure-cells   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A code cell with a wrap class that makes more than one figure without
`fig-subcap` keeps all its figures in their normal layout in every format,
with one warning for the cell (D-010).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the check in `_extensions/wrapped/wrapped.lua` that finds such a
cell and keeps its figures normal with one warning; three new knitr cells
in `tests/contexts.qmd` and the four `contexts` snapshots; the README's
list of places that keep the normal layout; the edge-case table in
`cairn/references/wrap-mechanisms.md` and the next-block rule note in
`cairn/DESIGN.md`.

**Out:** a two-figure cell inside a list, callout, margin, or other
context keeps today's per-figure context warnings (no row: the context
rule already covers those figures). Stacking two figures on one side was
weighed and not chosen (D-010). Jupyter cells are not rendered by the
fixtures, which run knitr only (no row: the check reads the cell's floats,
not its engine).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: For the two knitr cells that this milestone adds to
      `tests/contexts.qmd`, `fig-two-plots` (`#| classes: wrap-right`, a
      `fig-cap`, two plots, no `fig-subcap`) and `fig-three-plots`
      (`#| classes: wrap-left`, a `fig-cap`, three plots, no `fig-subcap`),
      each with a paragraph after it, no figure of either cell wraps in
      HTML, PDF through LaTeX, PDF through Typst, or Word. In the four
      `contexts` snapshots that `python3 tests/verify.py` compares, no HTML
      figure line of these figures shows a wrap class or wrap style and no
      HTML `# groups` entry names them, no LaTeX line shows them as a
      `wrappedfigure`, each Typst figure line shows them with
      `image-width=no` and no `# wraps` line names them, and no Word frame
      names them.
- [ ] AC2: In each of the four formats, the render of `tests/contexts.qmd`
      prints one warning for each of those two cells. The warning names the
      cell's label (`fig-two-plots`, `fig-three-plots`) or its figures' ids
      and says that the cell makes more than one figure. Each of the four
      `contexts` snapshots lists each such warning once with the count
      `1x`, and no other line of its `# warnings` block contains the text
      `fig-two-plots` or `fig-three-plots`.
- [ ] AC3: Two shapes keep their behavior. For the knitr cell
      `fig-two-subcap` that this milestone adds to `tests/contexts.qmd`
      (`#| classes: wrap-right`, two plots, `fig-subcap`), each of the four
      `contexts` snapshots lists `wrapped: the figure #fig-two-subcap is a
      subfigure panel, so it does not wrap.` once, `wrapped: the figure
      #fig-two-subcap-1 is in a subfigure panel, so it does not wrap.` once,
      and the same line for `#fig-two-subcap-2` once, and no warning that
      the cell makes more than one figure. The one-plot cell `fig-cell` in
      `tests/fixture.qmd` still wraps: in the `fixture` snapshots its HTML
      figure line shows `wrap-left`, LaTeX shows it as a `wrappedfigure`, a
      Typst `# wraps` line names it, and a Word frame names it.
- [ ] AC4: README.md's list of places where a figure keeps its normal
      layout names a code cell that makes more than one figure without
      `fig-subcap`, and says to give each plot its own cell to wrap it.
- [ ] AC5: `python3 tests/verify.py` exits 0 on the branch head.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2, T3
- AC2 → T2, T3
- AC3 → T1, T2, T3
- AC4 → T4
- AC5 → T3, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Add the cells `fig-two-plots`, `fig-three-plots`, and
      `fig-two-subcap` to `tests/contexts.qmd`, each followed by a
      paragraph, with the file's `out-width` line for docx. Render the
      fixture with `main`'s filter and record in the work log what wraps
      and what warns (the before state; the two plain cells must wrap).
- [x] T2: In `wrapped.lua`'s `cell_div` (near line 1181), count the cell's
      figure floats that sit in no other float. `count_floats` also counts
      subfigures and tables, so the subcap cell counts 3 today. With two or
      more, keep every figure of the cell normal and print one warning in
      the style of `context_warning` (near line 946), naming the label (the
      float ids less their `-N` ending) or the ids. Leave the subcap path,
      table cells, and one-figure cells as they are.
- [ ] T3: Run `python3 tests/verify.py --update`, read the snapshot diff
      (only the new cells' lines may change), and run it again without
      `--update` until it exits 0. Show that the new check can fail: with
      the T2 change undone, the new snapshots must differ.
- [ ] T4: Add the case to the README list (near line 207), to the
      edge-case table in `cairn/references/wrap-mechanisms.md` (beside E4
      and E7), and to the next-block rule note in `cairn/DESIGN.md` (near
      line 96), citing D-010. State only what T3's renders show.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: idea vet: no concern; the work and its behavior were chosen at the question set, and a fallback with a warning matches the subfigure-panel fallback in all four formats.
- 2026-10-27: question set: next work — the "Handle a wrapped cell with two figures" candidate; behavior — both figures normal with one warning (the user's choice).
- 2026-10-27: plan gate chose all figures normal with one warning over the back-to-back rule (first normal, second wraps) and over stacking the figures on one side, because one rule holds in all four formats and LaTeX's wrapfig and Word frames hold one figure each; falsified by users asking for a two-plot cell to wrap.
- 2026-10-27: collision check: the candidate row is absorbed (started M014); D-003's back-to-back rule overlaps and is narrowed by D-010 for the figures of one cell; no planned or in-progress milestone overlaps.
- 2026-10-27: inbox sweep: no open issues and no open PRs on jmgirard/wrapped; Resolves is —, so no assignment option.
- 2026-10-27: scratch renders on main: a two-plot wrapped cell gives fig-two-1 and fig-two-2, both wrap-right side by side in HTML; a fig-subcap cell prints the panel warning and one warning per subfigure in all four formats.
- 2026-10-27: criteria audit (full mode, Opus reader): 6 findings, all fixed: AC1 now says "no figure wraps" and names the HTML groups block; D-003 overlap recorded as D-010; a second cell (three plots, wrap-left) varies count and side; AC2's "names" became a text test and allows the ids; AC3 states the subcap warnings and fig-cell's wrap lines outright, with no main-branch comparison; AC4 kept, README limited to what renders show (T4).
- 2026-10-27: lessons used: 2026-10-25 (M002) tests/_extensions symlink and Typst PNG; 2026-10-25 (M003) Blocks filter walk inside cells; 2026-10-27 (M012) one-fixture check; 2026-10-27 (M013) dump filter to see cell floats.
- 2026-10-27: T1 done: three cells added to tests/contexts.qmd. Before state with main's filter: fig-two-plots-1/-2 and fig-three-plots-1/-2/-3 wrap in HTML (wrap class and style), LaTeX (wrappedfigure each), Typst (image-width=yes, one wraps line naming the first figure), and Word (one frame naming the first figure); fig-two-subcap prints its panel warning and one per subfigure in all four formats and does not wrap.
- 2026-10-27: T2 done: a float Div inside a cell carries no type or id in a user filter (dump at pre-quarto), so cell_div counts the cell's top-level floats (count_top_floats) and float_target keeps each Figure of such a cell normal, before clean_images, with one warning at the first figure: "the code cell #<label> makes more than one figure", the label being the float id less its -N ending. Table floats keep the "is not a figure" path; context and next-block paths run first. Scratch renders of contexts.qmd show the five figures with no wrap in all four formats and each cell warning once.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
