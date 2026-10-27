<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M011: Finish the figure width checks

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the filter's warnings and figure widths reach every user   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m011-finish-width-checks   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: In HTML, each figure `width` value in a new warning section of
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
- [ ] AC2: In HTML, a `wrapped: width` of `calc(0%)` prints the warning and
      the built-in 40% applies, and a `wrapped: breakpoint` of `calc(0px)`
      in the same fixture stays as written with no warning. Evidence: the
      metadata fixture's snapshot in `python3 tests/verify.py`.
- [ ] AC3: In HTML, each value in the "Values that pass" section of
      `tests/css-functions.qmd` reaches the style as written with no
      warning. The section gains `calc(50% - 4in)`, `calc(1em - 1rem)`,
      `calc(1em - 2ex)`, `calc(100vw - 100%)`, `calc(var(--w) - 1px)`,
      `max(0px, 10%)`, and `clamp(-1px, 10%, 1in)` as widths and a
      `wrap-gap` of `calc(0px)`. Evidence: the fixture's snapshot.
- [ ] AC4: In PDF through Typst, each new `TYPST_LAYOUT` case in
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
- [ ] AC5: In PDF through Typst, a figure whose width and gap are both
      percents with a sum of 100% or more prints a warning that names the
      width and the gap; in a fixture whose document default plus that gap
      is under 100%, the document default applies. A `wrapped:` width and
      gap that are both percents with such a sum print a warning, and the
      built-in 40% applies. A width of `99%` with a `1em` gap prints no
      warning. Evidence: the kept `.typ` snapshots and their warning lines
      in `python3 tests/verify.py`.
- [ ] AC6: The README's "Width and gap" section states which function
      widths warn: those that are zero, negative, or not finite at every
      size, and never one with `var()`. The README's Typst section and
      DESIGN.md's Known issues entry on Typst widths state that the check
      counts the gap, with no console warning when a term is not a percent.
      The README states that a figure keeps 40% and its gap when 40% plus
      the gap fills the text.
- [ ] AC7: `python3 tests/verify.py` passes on macOS and in CI.

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
- [ ] T3: Give `wrapped-width` in `TYPST_HEADER` (`wrapped.lua:386`) the gap,
      and resolve each width and the gap to an absolute length in `layout`
      (a ratio as a share of `size.width`). Add the percent-sum warning in
      `typst_open` (`wrapped.lua:361`) and `read_meta`
      (`wrapped.lua:821-829`).
- [ ] T4: Add Typst fixtures for AC4 and AC5 and their `TYPST_LAYOUT` cases
      in `tests/verify.py`, with widths set from the measured text width;
      update the snapshots.
- [ ] T5: Update README "Width and gap" and the Typst section, DESIGN.md
      Known issues, and the comments on the changed functions, each against
      a render's observed output.
- [ ] T6: Run `python3 tests/verify.py` on macOS, then push and read CI.

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

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
