<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M011: Finish the figure width checks

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the filter's warnings and figure widths reach every user   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m011-finish-width-checks, https://github.com/jmgirard/wrapped/pull/11   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A wrapped figure whose CSS function width is zero or below, or whose Typst width plus gap fills the text, takes the default width.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- HTML: a width written as `calc()`, `min()`, `max()`, or `clamp()` whose
  result is zero, negative, or not finite at every text width, font size,
  and window size prints a warning and takes the fallback, for a figure's
  `width` and for `wrapped: width`. A value whose result can be above zero
  at some size, or holds a `var()`, passes as now. A gap or breakpoint of
  zero stays as it is.
- PDF through Typst: the width check counts the gap. A figure whose width
  plus gap is the text width or more takes the first of the document
  default and the built-in 40% whose width plus that gap is narrower than
  the text, else 40%. When the width and the gap are both percents, the
  filter can see the sum and prints a warning; otherwise Typst checks while
  it lays out the page and prints none.
- README, DESIGN.md Known issues, code comments, and fixtures for both.

**Out:**
- Word counts the width and the gap each alone → new candidate row "Count
  the gap in Word width checks".
- A gap written as a function whose result is negative, such as
  `calc(-1em)` → new candidate row "Refuse negative gaps in CSS functions".
- A gap so wide that 40% plus the gap fills the text: the figure keeps 40%
  and the gap as written. The README states this limit.
- HTML and LaTeX widths as wide as the text → not checked now, as before.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: In HTML, each figure `width` value in a new warning section of
      `tests/css-functions.qmd` prints a warning that names the value and
      takes the document default, as `0%` does. The section holds at least
      one value for each of `calc()`, `min()`, `max()`, and `clamp()`; one
      whose result is zero, one negative, one infinite (`calc(1px / 0)`),
      and one NaN (`calc(0px / 0)`); one nested function; at least four
      values whose only unit is, in turn, a percent, an absolute unit, a
      font-relative unit, and a viewport unit; units that cancel
      (`calc(1in - 96px)`, `calc(1em - 1em)`); a negative factor
      (`calc(10% * -1)`); and a `clamp()` whose minimum is above its maximum
      (`clamp(-1px, 5%, -2px)`). Evidence: the fixture's snapshot and
      warning lines in `python3 tests/verify.py`.
- [x] AC2: In HTML, a `wrapped: width` of `calc(0%)` prints the warning and
      the built-in 40% applies, and a `wrapped: breakpoint` of `calc(0px)`
      in the same fixture stays as written with no warning. Evidence: the
      metadata fixture's snapshot in `python3 tests/verify.py`.
- [x] AC3: In HTML, each value in the "Values that pass" section of
      `tests/css-functions.qmd` reaches the style as written with no
      warning. The section gains `calc(50% - 4in)`, `calc(1em - 1rem)`,
      `calc(1em - 2ex)`, `calc(100vw - 100%)`, `calc(var(--w) - 1px)`,
      `max(0px, 10%)`, and `clamp(-1px, 10%, 1in)` as widths and a
      `wrap-gap` of `calc(0px)`. Evidence: the fixture's snapshot.
- [x] AC4: In PDF through Typst, each new `TYPST_LAYOUT` case in
      `tests/verify.py` passes, reading the image width in the Typst PDF.
      Cases (a) and (b) sit in a fixture whose document default is an
      absolute width that fits beside the text with their gap and differs
      from 40%. The cases are: (a) an absolute width narrower than the text
      whose width plus an absolute gap is not, which takes the document
      default; (b) a percent width and an `em` gap that together fill the
      text, which takes the document default; (c) an absolute width with a
      percent gap that together fill the text, which takes the document
      default; (d) a figure whose document default plus its gap also fills
      the text, which takes 40%; (e) a width plus gap narrower than the
      text, which keeps its width; (f) a `wrapped:` width and gap, at least
      one not a percent, that together fill the text, which take 40%; (g) a
      gap with which 40% also fills the text, which keeps 40%, read for the
      image width and a render with no error only.
- [x] AC5: In PDF through Typst, a figure whose width and gap are both
      percents with a sum of 100% or more prints a warning that names the
      width and the gap; in a fixture whose document default plus that gap
      is under 100%, the document default applies. A `wrapped:` width and
      gap that are both percents with such a sum print a warning, and the
      built-in 40% applies. A width of `99%` with a `1em` gap prints no
      warning. Evidence: the kept `.typ` snapshots and their warning lines
      in `python3 tests/verify.py`.
- [x] AC6: The README's "Width and gap" section states which function
      widths warn: those that are zero, negative, or not finite at every
      size, and never one with `var()`. The README's Typst section and
      DESIGN.md's Known issues entry on Typst widths state that the check
      counts the gap, with no console warning when a term is not a percent.
      The README states that a figure keeps 40% and its gap when 40% plus
      the gap fills the text.
- [x] AC7: `python3 tests/verify.py` passes on macOS and in CI.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3, T4
- AC5 → T3, T4
- AC6 → T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Make the calc parser (`wrapped.lua:83-207`) return, beside the
      type, what it knows of the result: a sum of an absolute part in px
      and one coefficient for each relative unit, where every relative
      base is unknown and above zero, or a sign class after `min()`,
      `max()`, or `clamp()`, or unknown after `var()`. Mark division by a
      zero number as not finite. Use it in `checked_length`
      (`wrapped.lua:259`) for widths only, beside `is_zero`, with a warning
      that says zero, negative, or not finite.
- [x] T2: Add the AC1 and AC3 values to `tests/css-functions.qmd` and the
      AC2 width and breakpoint to a metadata fixture; update the snapshots
      and read the diff.
- [x] T3: Give `wrapped-width` in `TYPST_HEADER` (`wrapped.lua:386`) the gap,
      and resolve each width and the gap to an absolute length in `layout`
      (a ratio as a share of `size.width`). Add the percent-sum warning in
      `typst_open` (`wrapped.lua:361`) and `read_meta`
      (`wrapped.lua:821-829`).
- [x] T4: Add Typst fixtures for AC4 and AC5 and their `TYPST_LAYOUT` cases
      in `tests/verify.py`, with widths set from the measured text width;
      update the snapshots.
- [x] T5: Update README "Width and gap" and the Typst section, DESIGN.md
      Known issues, and the comments on the changed functions, each against
      a render's observed output.
- [x] T6: Run `python3 tests/verify.py` on macOS; CI is read on the PR at
      review's merge step.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: question set: what to work on — finish the width checks (the two M010 follow-up rows).
- 2026-10-27: question set: CSS function values that are zero only on narrow pages — warn only when the result is zero or below at every size.
- 2026-10-27: question set: Typst gap rule — take the default when width plus gap is the text width or more, no minimum text column.
- 2026-10-27: idea vet: no concern. CSS clamps a negative width to zero and an infinite one to the largest width, so the warning names all three cases; the Typst rule fixes the one-word-per-line text that the width-only check leaves.
- 2026-10-27: collision check: absorbs candidate rows "Count the gap in Typst width checks" and "Warn on zero widths in CSS functions"; extends M010 (done); no D-entry covers widths.
- 2026-10-27: inbox sweep: no open issues or pull requests.
- 2026-10-27: lessons used: 2026-10-27 (M010) Typst `layout` and warnings; 2026-10-27 (M010) smart punctuation in metadata; 2026-10-25 (M005) wrap-it `columns:` percents; 2026-10-26 (M007) pdftohtml boxes.
- 2026-10-27: plan gate chose a linear form of an absolute part and per-unit coefficients over evaluating the value at sample text widths, because samples cannot show a value is zero or below at every width; falsified by a value the check warns on that a browser renders wider than zero.
- 2026-10-27: plan gate chose a check inside Typst's `layout` over a filter-side estimate of the text width, as M010 did, because the filter cannot know the page; falsified by a Quarto Typst template change that gives the filter the text width.
- 2026-10-27: new candidate rows "Count the gap in Word width checks" and "Refuse negative gaps in CSS functions", found at investigation.
- 2026-10-27: plan question set's third chip said HTML and LaTeX check width plus gap; neither checks wide widths, and Word checks width and gap each alone. Corrected in chat; the answer stands, since the rule extends M010's Typst check.
- 2026-10-27: checkpoint: the full criteria audit (fresh Opus reader) ran after the question set, since the work was chosen there, and is still running at this commit; its dispositions follow in a later plan commit.
- 2026-10-27: criteria audit (full mode, fresh Opus reader) returned 12 findings on AC1, AC3, AC4, AC5, AC6; all fixed by narrowing or adding cases: AC1 gains unit-kind, cancelling-unit, negative-factor, and inverted-clamp values; AC2 gains a zero breakpoint; AC3 gains clamp, em-ex, and vw-minus-percent passes; AC4 moves (a)-(c) to a fixture with a 2in-like default, adds a percent-gap case, makes the metadata case non-percent, and reads the no-room case for image width only; AC5 names its fixture condition; AC6 becomes a content check and names the 40% limit. It confirmed that the parser accepts every probe value, so the new check decides them, and that the Typst text is 6 in.
- 2026-10-27: /milestone-implement started on branch m011-finish-width-checks; T1 and T2 code and fixtures written, full suite with --update running.
- 2026-10-27: T1 done: each calc parser function also returns a bound (lower and upper sums by unit, exact, or not finite); never_positive warns on a width whose upper sum is zero or below or that is not finite, and any var() leaves no bound. A scratch harness gave the expected result on 44 probe values; all 52 renders pass.
- 2026-10-27: T2 done: css-functions.qmd gains 13 never-above-zero widths and 8 passing values; new meta-calc-zero.qmd (width calc(0%), breakpoint calc(0px)). Only those two snapshots changed. With main's wrapped.lua, meta-calc-zero prints no warning, so its snapshot fails there.
- 2026-10-27: checkpoint: T3 code (wrapped-abs, wrapped-width with the gap, percent-sum warnings) and T5 docs written; new Typst layout cases pass in targeted renders and failed 6 of 7 before T3; full suite with --update running, no box ticked yet.
- 2026-10-27: T3 done: typst_open and read_meta warn on a percent width and gap with a sum of 100% or more; wrapped-width takes the gap and returns the first width that fits with it, else 40%. Percent gaps measured 158 and 162 px against 162 px for 25% of the text, so a percent gap is a share of the text width.
- 2026-10-27: T4 done: fixtures typst-gap (default 3in), typst-gap-meta (default 5in with 1.5in gap), typst-gap-percent; 8 TYPST_LAYOUT cases and typst_image_case for the no-room case. Before T3, 7 of 8 failed (all but the case that fits). The case where the default also fills the text moved to typst-gap-meta, since with a 3in default 40% plus such a gap leaves under 1 in for the marker words. The older Typst snapshots changed only by the new gap argument (55 lines). All 55 renders pass on macOS.
- 2026-10-27: T5 done: README "Width and gap" and Typst section, DESIGN.md steps 5 and 7 and Known issues, wrap-mechanisms W3 example, each written against the renders above; the simple-english hook flags an older "would" at wrap-mechanisms.md line 164, left as is.
- 2026-10-27: claim audit: 46 claims read, 5 corrected — README.md, _extensions/wrapped/wrapped.lua, tests/typst-gap.qmd, tests/css-functions.qmd. One was a defect: a width divided by a number that is not finite, such as calc(5px - 1px / (1 / 0)), warned and took 40%; such a quotient now has no bound. The README now says the check warns on widths it can show are never above zero (it misses some min() forms); the CSS comment names NaN; two fixture intros fixed. The same reader re-read the five and found them holding, with one comment word changed after.
- 2026-10-27: kept the percent-sum warning for a figure with no width and a large percent gap (claim audit note): it says the width is 40%, which it already is, but its "no room for text" holds.
- 2026-10-27: checkpoint (review): fix-now work for blame-history #1 and #4 and diff-bug #1, #3, #4, and #6 committed; full suite with --update running for the changed and new snapshots.
- 2026-10-27: T6: all 55 renders pass on macOS after the audit fixes. CI does not run on branch pushes (verify.yml runs on pull requests and main), so CI is read at review's merge step; T6's push-and-CI half moves there (minor task edit).
- 2026-10-27: the line on line 172 is superseded by blame-history #1's fix: a figure with no width of its own no longer gets the percent-sum warning.
- 2026-10-27: step-7 approval: m011-finish-width-checks approved for merge
- 2026-10-27: PR #11 opened at pushed head 8914ccb, one check (verify) pending; review stopped before the CI wait, since this session does not poll CI; left: AC7's CI half (tick from `gh pr checks 11`), the merge marker, the squash merge, and post-merge hygiene.
- 2026-10-27: resume: verify passed on PR #11 (4m35s); merged as 1210b0a with `gh pr merge 11 --squash --delete-branch`. The delete removed the local branch with three unpushed tracking commits (PR record, CI stop, AC7 tick); this file is restored from c74a154 in the reflog.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Review head 1f66709; `python3 tests/verify.py` on macOS: all 55 renders pass, 0 FAIL lines, all 8 typst-gap layout cases ok.

- AC1: css-functions snapshot holds 13 `on #fig-never-N is zero, negative, or not finite, so it is 40%` warnings, and all 13 fig-never figures carry `--wrap-width: 40%`. The section covers calc (1, 5-13), min (2), max (3), clamp with min above max (4), zero (1, 13), negative (5, 9, 12), infinite (6), NaN (7), nested (8), single-unit percent (1), absolute (5), font-relative (13), viewport (9), cancelling units (10, 11), and a negative factor (12).
- AC2: meta-calc-zero snapshot: one warning `width "calc(0%)" on the wrapped metadata is zero, negative, or not finite, so it is 40%.`, the figure has `--wrap-width: 40%`, and `# breakpoint` reads `calc(0px)` with no breakpoint warning.
- AC3: css-functions snapshot has 0 warnings naming `#fig-valid-`; fig-valid-11 to 17 carry their widths as written (`calc(50% - 4in)` … `clamp(-1px, 10%, 1in)`), and fig-valid-18 carries `--wrap-gap: calc(0px)`.
- AC4: suite lines `ok layout typst-gap` for (a) 5in with 1.5in gap → 3in, (b) 99% with 1em gap → 3in, (c) 4.5in with 25% gap → 3in, (e) 2in with 2em gap → 2in, (g) 40% with gap too wide → 259 px image only; `ok layout typst-gap-meta` for (d) default with gap too wide → 40% and (f) 5in with 1.5in metadata gap → 40%. typst-gap's default is 3in (324 px), which fits with the (a) and (b) gaps.
- AC5: typst-gap snapshot warns `width "75%" and wrap-gap "25%" on #fig-g70 leave no room for text in Typst, so the width is 3in.`, and the 75%-with-25% case measures 3in; typst-gap-percent warns `width "70%" and gap "40%" in the wrapped metadata … so the width is 40%.` and its call reads `wrapped-width(wrapped-size, 40%, 40%, 40%, 40%)`; fig-g99 (99% with 1em) has no warning.
- AC6: README.md:105-113 states that a function width the check can show is zero, negative, or not finite at every page and font size warns, and that a width with `var()` never does; README.md:306-320 states the percent-sum warning, the width-plus-gap check with no warning for other units, and that a figure keeps 40% and the gap when 40% plus the gap fills the text; DESIGN.md:221-226 Known issues states the same limit. `grep -n "calc(0%)\` prints no" README.md` prints nothing.
- AC7: macOS part above; CI part read on the PR at step 8.
- Re-verified after the fix-now commits (3d95522 plus snapshots): `python3 tests/verify.py --update` all 56 renders pass, 0 FAIL, 8 typst-gap layout cases ok; css-functions now holds 15 fig-never warnings (adds fig-never-14 and 15) and fig-valid-19 as written; typst-gap-default warns `… so the width is 40%.`. AC1 to AC6 evidence above still holds on this head.
- AC7 (CI): `gh pr checks 11` — verify pass in 4m35s on head 8914ccb (run 40462905427); with the macOS run above, AC7 holds.
- Gate: `cairn_validate.py` all checks passed; version marker `_extensions/wrapped/_extension.yml` unchanged by the diff (one marker, so all markers agree); changelog slot "none"; verify passes on the review head (above); no principle changed, so `cairn_impact` skipped.
- spawned: diff-bug, blame-history, prior-review, ripple
- ripple #1: ROADMAP row "Warn on zero widths in CSS functions" still says such widths pass with no warning — reject, planned change: post-merge hygiene graduates this started row.
- ripple #2: ROADMAP row "Count the gap in Typst width checks" still says the width is checked alone — reject, planned change: post-merge hygiene graduates this started row.
- ripple #3: the is_zero comment "A function value is not read." reads as the width rule now that never_positive reads function values — fix now, fixed 7bfbb94.
- ripple #4: tests/typst-wide.qmd:13 says a width as wide as the text leaves no room, with the width-alone framing — reject, false: the sentence still holds, and the rule it states is a case of width plus gap.
- ripple #5: tests/typst-wide-meta.qmd:13 says a width as wide as the text takes the default when the default fits — reject, false: still true for that fixture's figures.
- prior-review #1: M005 pass 2 rejected diff-bug #1 ("a 50% width with a 50% gap … not a defect: all text renders"), and M011 now replaces such a width with the default and warns — reject, planned change: the M010 follow-up row asked for it and the plan question set chose width plus gap at the text width.
- prior-review #2: M010 recorded no Typst warning for a fallback; M011 warns for a percent pair but not for mixed units that fill the text the same way — reject, planned change: AC5 sets that boundary, since Typst cannot print a warning and only the percent sum is known to the filter.
- prior-review #3: typst_image_case checks only the image width, unlike the earlier cases that check the paragraph beside the image — reject, planned change: AC4 (g) reads that case for image width only, since its text column has no room.
- blame-history #1: a metadata `gap: 60%` with no metadata width warns about the built-in 40% width the user never set, and every figure with no width of its own repeats the warning — fix now: the percent-sum warning fires only for a figure's own width (typst_open) or a metadata width (read_meta); a scratch render with `gap: 60%` and three figures printed one warning, for the figure with its own 45% width., fixed 3d95522
- blame-history #2: the gap is now checked before the width, so the order of warnings changes — reject, false as a defect: snapshots sort and count warnings, and no contract states an order.
- blame-history #3: the new warnings say "so the width is %s" where the M005 and M010 Typst warnings say "so it is %s" — reject, style: the new messages name two values, so "it" would not say which one changes.
- blame-history #4: the 4.5in with 25% gap case adds up to the 6in text width exactly, so it pins a tie — fix now: the case uses 4.6in., fixed 3d95522
- diff-bug #1: when the document default plus a figure's percent gap also fills the text, the warning names the default while Typst uses 40% (`wrapped: width: 80%` with `width="75%" wrap-gap="30%"`) — fix now: typst_open names and writes 40% where the filter sees that sum; regression fixture typst-gap-default names 80% at 7bfbb94 and 40% with the fix., fixed 3d95522
- diff-bug #2: warnings for a figure or metadata with no width of its own — fix now, the same change as blame-history #1., fixed 3d95522
- diff-bug #3: `tonumber` keeps Lua integers, so `calc(9223372036854775807px + 1px)` wraps around and gets a false warning — fix now: numbers are read as floats; regression value fig-valid-19 in css-functions.qmd., fixed 3d95522
- diff-bug #4: on a Typst page of auto width, `layout` gives an infinite width, so every figure took 40% where main kept its width — fix now: wrapped-width returns the first width when the text width is infinite; checked by hand with `quarto typst compile` on a scratch file (auto width gave 2in for a 2in figure; a letter page gave 3in for 7in with a 1.5in gap and 40% with a 4in gap), with no fixture, since the snapshot shows only the call text and the layout check reads a fixed page., fixed 3d95522
- diff-bug #5: widths that are never above zero but print no warning, such as `calc(min(1%, 1px) - min(1%, 1px))` and `calc(7mm - 0.7cm)` — reject, false as a defect: the README promises a warning only where the check can show the result.
- diff-bug #6: no fixture runs a number times a length or division by a number other than zero — fix now: fig-never-14 `calc(-1 * 10%)` and fig-never-15 `calc(10% / -2)`., fixed 3d95522
- diff-bug #7: some fixture values repeat one code path (fig-never-1, 5, 9, 13; fig-never-10 and 11; fig-valid-11 to 14; MGap and MDefault) — reject, planned change: AC1, AC3, and AC4 name each of them.
- diff-bug #8: the metadata zero warning reads "on the wrapped metadata" and the new Typst metadata warnings "in the wrapped metadata" — reject, style: the first comes from checked_length's existing wording, shared by every metadata check.
- diff-bug #9: the exact-tie case — fix now, the same change as blame-history #4., fixed 3d95522
