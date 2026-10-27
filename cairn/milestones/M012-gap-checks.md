<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M012: Finish the gap checks

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the filter's warnings, frame widths, and gaps reach every user   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m012-gap-checks   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A wrapped figure whose Word width plus gap fills the text, or whose HTML gap is a function value below zero, takes a default with a warning.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- Word: the width check counts the gap. A figure that sets its own `width`
  or `wrap-gap`, and whose frame width plus gap in twips is the text width
  or more, prints one warning and takes the first of the document default
  and the built-in 40% whose sum with the gap is below the text width, else
  40% with the gap as written, as Typst does. A `wrapped:` width and gap
  whose sum fills the text print one warning, and the document default
  width becomes 40%.
- HTML: a gap written as `calc()`, `min()`, `max()`, or `clamp()` that the
  check can show is below zero, or not finite, at every page and font size
  prints a warning and takes the fallback, for a figure's `wrap-gap` and
  for `wrapped: gap`. It reuses the bound that M011 built for widths. A gap
  of zero at every size stays as it is.
- The check sits in `checked_length`, which LaTeX, Typst, and Word share.
  There a negative function gap keeps its fallback, and its warning now
  says the gap is below zero instead of "not a length that <format> can
  use". No fixture change.
- README, DESIGN.md, `references/wrap-mechanisms.md`, code comments, and
  fixtures for both.

**Out:**
- A gap that is below zero only at some sizes, such as `calc(1em - 20px)`:
  no warning, as for widths. The README states this limit (M011).
- A `max()` gap over two units whose terms are all below zero, such as
  `max(-2px, -1%)`: M011's bound reads it as zero or below, not as below
  zero, so it passes. A DESIGN.md Known issue and the README state it.
- A function breakpoint below zero: not checked now, as before.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: In Word, a new fixture `tests/docx-gap.qmd`, rendered with no
      reference doc (text width 9360 twips) and `wrapped: width: 4in`,
      gives these frame widths and warnings in its snapshot
      `tests/_snapshots/docx-gap.docx.txt` (frame lines and `# warnings`)
      under `python3 tests/verify.py`. One warning names the width and the
      gap for (a), (b), (c), (d), (f), and (g):
      (a) `width="5in" wrap-gap="2in"` takes 4in;
      (b) `width="95%" wrap-gap="2em"` takes 4in;
      (c) no width, `wrap-gap="3in"` takes 40%;
      (d) no width, `wrap-gap="4in"` keeps 40% and the 4in gap;
      (e) `width="6in" wrap-gap="35.95pt"` (sum 9359) keeps 6in with no
      warning;
      (f) `width="6in" wrap-gap="12.699mm"` (720 twips once rounded, sum
      9360) takes 4in;
      (g) `width="10in" wrap-gap="3in"` takes 40% with one warning in all.
- [ ] AC2: In Word, a fixture with `wrapped: {width: 5in, gap: 2in}` (7200
      plus 2880 twips, at or above 9360) prints one metadata warning, and a
      figure with no `width` and no `wrap-gap` prints no warning of its own
      and gets a 3744-twip frame. Evidence: the fixture's snapshot under
      `python3 tests/verify.py`.
- [ ] AC3: In HTML, each `wrap-gap` value in a new warning section of
      `tests/css-functions.qmd` prints a warning that names the value and
      takes the document default gap, as the snapshot's style shows. The
      values: `calc(-1em)`, `calc(-1vw)`, `calc(10% / -2)`,
      `calc(-1 * 1em)`, `min(-1px, 10%)`, `max(-2px, -1px)`,
      `clamp(-3px, -2px, -1px)`, `calc(min(0px, 1em) - 1px)`,
      `calc(1px / 0)`, and `calc(0px / 0)`. Evidence: the fixture's
      snapshot and warning lines under `python3 tests/verify.py`.
- [ ] AC4: In HTML, each gap in the "Values that pass" section of
      `tests/css-functions.qmd` reaches the style as written with no
      warning. The section keeps `calc(0px)` and gains `calc(1em - 1em)`,
      `calc(1in - 96px)`, `min(0px, 10%)`, `max(-1em, 0px)`,
      `calc(1em - 20px)`, `calc(50% - 1in)`, and `calc(var(--g) - 1px)` as
      gaps. Evidence: the fixture's snapshot.
- [ ] AC5: In HTML, a `wrapped: gap` of `calc(-1em)` prints one warning,
      and the built-in `1em` gap applies to a figure with no `wrap-gap`.
      Evidence: a metadata fixture's snapshot and warning lines under
      `python3 tests/verify.py`.
- [ ] AC6: The README's "Width and gap" section states both rules,
      "Document defaults" states the metadata forms, and the Word section
      states the sum rule and the fallback order (document default, then
      40% with the gap kept). DESIGN.md's Architecture describes both
      checks and its Known issues holds the mixed-unit `max()` gap.
      `references/wrap-mechanisms.md` describes the Word sum check. The
      comments on `docx_frame`, `read_meta`, and `checked_length` describe
      the new checks.
- [ ] AC7: `python3 tests/verify.py` passes on macOS and in CI.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3
- AC5 → T4
- AC6 → T5
- AC7 → T1, T2, T3, T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Word figure check. Write `tests/docx-gap.qmd` with the seven
      AC1 cases and add it to `RENDERS` in `tests/verify.py`; render it
      before the change and see each case but (e) differ from the wanted
      widths. In `docx_frame` (`wrapped.lua:679`), when the figure sets its
      own width or gap and `w + g >= docx_text_width` (each value rounded
      to twips first), warn and take the first of `options.width` and
      `DEFAULTS.width` that fits with `g`, else 40%. A width already
      replaced by the wide-width check gets one warning, not two. Update
      the snapshot and read the diff.
- [x] T2: Word metadata check. In `read_meta`'s Word branch
      (`wrapped.lua:1021`), after `format_default`, warn once and set
      `options.width` to 40% when the metadata width plus gap fills the
      text. New fixture `tests/docx-gap-meta.qmd` with the AC2 metadata
      and one figure with no width or gap; add to `RENDERS` and snapshot.
- [x] T3: HTML gap check. In `checked_length` (`wrapped.lua:418`), warn
      for a gap (`wrap-gap` or `gap`) whose bound from `calc_length` is
      `bad` or whose upper sum is below zero at every base (each
      coefficient zero or below, one below zero); a gap whose upper sum is
      zero stays. Add the AC3 warning section and the AC4 passing gaps to
      `tests/css-functions.qmd`; update the snapshot.
- [x] T4: HTML metadata gap. New fixture `tests/meta-calc-gap.qmd` with
      `wrapped: gap: calc(-1em)` and one figure; add to `RENDERS` and
      snapshot.
- [x] T5: Docs. README "Width and gap", "Document defaults", and Word
      sections; DESIGN.md Architecture step 5 and Known issues;
      `wrap-mechanisms.md`; comments on `docx_frame`, `read_meta`, and
      `checked_length`. Run `python3 tests/verify.py` and push for CI.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: idea vet: no concern found — Word sets the gap as `w:hSpace` on the text side of a margin-anchored frame, so a width plus gap at the text width leaves no room for text; a negative CSS margin pulls text over the figure, and a plain `-1em` gap already warns.
- 2026-10-27: question set: what to work on — "Finish the gap checks" (rows "Count the gap in Word width checks" and "Refuse negative gaps in CSS functions"); after the plan — plan and implement in this run.
- 2026-10-27: collision check: absorbs the two candidate rows, both from M011's plan; M010 and M011 (done) shipped the HTML width bound and the Typst gap sum this extends; no D-entry covers gaps (D-001 to D-009 read by heading); inbox sweep found 0 open issues and 0 open PRs; not the checker-regress shape, since the check reads user input, not repo files.
- 2026-10-27: lessons used: 2026-10-27 (M010) smart punctuation in metadata values; 2026-10-27 (M011) Lua `tonumber` integers; 2026-10-26 (M006) the default reference doc's 9360-twip text width.
- 2026-10-27: plan gate chose Word's fallback order of document default then 40%, keeping the gap, over also resetting the gap to its default, because M011's question set set that order for Typst and the README can state one rule for both; falsified by a Word render or user report where 40% with the kept gap leaves no readable text and resetting the gap would.
- 2026-10-27: plan gate chose to check only figures that set their own width or gap, with one metadata warning for the rest, over checking every figure, because a filling metadata would print one warning per figure (M011 review fixed that repeat in Typst); falsified by a figure that takes both values from the document and fills the text with no warning.
- 2026-10-27: plan gate chose a gap warning only when the gap is below zero at every size, reusing M011's bound, over a warning when it can be below zero at some size, because M011's question set chose warnings only when certain; falsified by a passing gap that puts text over the figure at the default font size in a user's document.
- 2026-10-27: criteria audit (full mode, fresh Opus reader): 11 findings, all fixed. AC1 names its snapshot file, pins its values, adds a rounding case (f) and a wide-width case (g), and no width in (d); `max(-2px, -1%)` cannot warn under M011's bound, so AC3 uses `max(-2px, -1px)` and the mixed-unit case moved to Out and a Known issue; AC3 adds viewport, percent, product, and nested probes; AC4 adds zero-at-every-size gaps; AC2 pins its metadata; Scope names the shared `checked_length` message change; AC6 names what each doc states, comments included; T1 expects no change in (e). AC5 and AC7 had none.
- 2026-10-27: implement started on branch m012-gap-checks; status in-progress.
- 2026-10-27: T1 checkpoint (not ticked): `docx_frame` counts the gap and `checked_docx_twips` reports a fallback and names a figure's gap for a too-wide width; `tests/docx-gap.qmd` gives the seven AC1 widths and warnings (before the change all but (e) differed); full verify running.
- 2026-10-27: T1 done: verify passed, 57 renders.
- 2026-10-27: T2 checkpoint (not ticked): `read_meta` warns once and sets the document default width to 40% when a `wrapped:` width or gap is set and the sum fills the text; `tests/docx-gap-meta.qmd` gave 7200 twips and no warning before, 3744 and one warning after; full verify running.
- 2026-10-27: T2 done: verify passed, 58 renders.
- 2026-10-27: T3 and T4 checkpoint (not ticked): `sum_negative` and `always_negative` make `checked_length` warn for a `wrap-gap` or metadata `gap` below zero or not finite at every size; before the change the ten AC3 gaps reached the style, after it each warns and takes 1em, and the seven AC4 gaps are unchanged; `tests/meta-calc-gap.qmd` gives one warning and a 1em gap; full verify running.
- 2026-10-27: T5 checkpoint (not ticked): DESIGN.md Architecture step 5 and a Known issue for the mixed-unit `max()` gap, and `wrap-mechanisms.md` W4 text, describe the new checks; README next.
- 2026-10-27: T5 checkpoint (not ticked): README "Width and gap", "Document defaults", and Word sections state the Word sum rule with its fallback order and the HTML negative gap rule with its limits.
- 2026-10-27: T3, T4, and T5 done: verify passed, 59 renders, on the code at f592718; later commits change only README.md and cairn/ docs, which no fixture renders (readme.qmd copies the README examples). The CI half of T5 moves to review: verify.yml runs on pull requests and pushes to main, so a branch push starts no check.
- 2026-10-27: claim audit corrections (re-read pending, verify running): README gap-only metadata note and "takes 40% and keeps the gap" wording, two comments in `checked_docx_twips` and `docx_frame`, and `fig-valid-27` (`max(-2px, -1%)` passes) in css-functions.qmd; new candidate row "Keep narrow widths when no width fits" for the widening to 40% that the plan chose.
- 2026-10-27: claim audit: 30 claims read, 4 corrected — README.md, _extensions/wrapped/wrapped.lua; one more true claim (`max(-2px, -1%)` passes) gained fixture `fig-valid-27`; the same reader re-read the five and found each true.
- 2026-10-27: verify passed, 59 renders, on the corrected code; status review.
- 2026-10-27: review: the plan-time rewrite after the criteria audit dropped the empty `## Decisions` and `## Review` sections; review restores both below.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Sync: `main` at 1d240c7, unmoved since the cut. Copilot review is off (no
`# Copilot review:` line in PROFILE.md). Open-PR cap: 0 open PRs of mine.

spawned: diff-bug, blame-history, prior-review, ripple

Findings and dispositions:
- prior-review #1, blame-history #3, diff-bug #4: a gap-only `wrapped:` metadata ran the Word check and warned "so the width is 40%" with no change, against M011's Typst fix — fix now: the check needs a metadata width, as in Typst.
- blame-history #1, diff-bug #5: a metadata width that `format_default` replaced (`10in` with a `5in` gap) warned a second time — fix now: the check runs only on a metadata width that stayed as written; new fixture `docx-gap-meta-wide.qmd` shows one warning.
- diff-bug #6: a figure whose own gap fell back (`wrap-gap="abc"`) still ran the sum check and could warn twice — fix now: only a gap that Word can use counts as the figure's own.
- diff-bug #2: an unusable width with the figure's own gap now takes the gap-aware fallback (40% where the default fills), unstated and untested — fix now: README Word bullet states it; `fig-bad-width` case in docx-gap.qmd.
- prior-review #4: README "even when its own width was narrower than 40%" had no fixture — fix now: `fig-narrow` (`0.5in` with `6in`) in docx-gap.qmd.
- diff-bug #3, prior-review #2, blame-history #4, ripple #4: the negative gap check sits in the shared `checked_length`, so LaTeX, Typst, and Word change their message, with no fixture outside HTML and docs saying HTML only — fix now: `fig-negative-gap` (`calc(-1em)`) in docx-gap.qmd; README and DESIGN step 5 say the check runs in every format.
- diff-bug #9: `clamp(-3px, -2%, -1px)` passes too, while the docs name only `max()` — fix now: README and the DESIGN Known issue name `max()` and `clamp()`.
- diff-bug #10, ripple #6: wrap-mechanisms W4 said every filling frame warns, and DESIGN lacked the gap-only metadata limit — fix now: W4 names a figure with its own width or gap; new Known issue.
- ripple #3: the `docx_frame` comment said "as Typst does", while Typst warns only for percents — fix now: the comment says Typst picks its width in the same order.
- ripple #5: DESIGN's Syntax table did not say a negative gap warns — fix now.
- ripple #7: README's metadata bullet read as covering a gap-only metadata — fix now: it names a `wrapped:` width.
- diff-bug #1: `fig-below` records an 8400-twip image in an 8640-twip frame (`fills=no`) — follow-up: absorbed into the row "Fit images in wide Word frames", which predates M012.
- prior-review #3: `docx_measure` reads `9223372036854775807in` as an integer and wraps to -1440 twips — follow-up: new row "Read Word lengths as floats in twips"; M012 did not add it.
- blame-history #6: a narrow own width widens to 40% when no width fits — follow-up: row "Keep narrow widths when no width fits" (from the claim audit).
- blame-history #2, diff-bug #8: a too-wide width with its own gap now names the gap in the warning — reject, planned change: AC1 (g) asks for one warning naming the width and the gap.
- blame-history #5, diff-bug #7: the sum warning names the gap the figure ends up with, which can be the document's — reject, planned change: the plan follows Typst, whose warning does the same.
- diff-bug #11: `calc(0px / 0)` warns though CSS reads NaN as zero — reject, planned change: AC3 names it.
- diff-bug #12: a number of more than 308 digits reads as infinite and warns — reject, edge: such a number is outside documented and common use, and the effect is a warning.
- diff-bug test-rule note: pairs of AC3, AC4, and AC1 cases share a code path — reject, planned change: AC1, AC3, and AC4 name each case.
- ripple #1, #2: the ROADMAP rows "Count the gap in Word width checks" and "Refuse negative gaps in CSS functions" still describe the old behavior — reject, planned change: they end with "started M012", and post-merge hygiene removes them.
- 2026-10-27: review checkpoint: fix-now work for 11 findings committed (Word metadata check needs an unreplaced width, a fallen-back gap is not the figure's own, three docx-gap cases, fixture docx-gap-meta-wide, doc fixes); verify on it running; criteria not yet ticked.
