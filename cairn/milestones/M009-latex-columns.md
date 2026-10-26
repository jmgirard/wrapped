<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M009: Keep LaTeX column layouts intact

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes the PDF that users of the extension get through LaTeX   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m009-latex-columns   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In PDF through LaTeX, wrapped figures leave the document's column layout as
the document sets it up.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A check in `wrapped.tex` where each `wrappedfigure` starts. Inside
a `multicols` environment (a flag set by a hook on its begin, tested
first), the figure is set in place, since floats are lost there. Else in
two-column text (`\if@twocolumn`, set by a class default, `classoption`,
or `\twocolumn`), a captioned figure becomes a `figure` float and an
uncaptioned image is set in place. Either way the figure has the width of
its `width` key and LaTeX writes a warning from the package `wrapped`: once
per run for two-column text, once per figure in `multicols` (the DESIGN
goal's render and context rules). The gap moves from a global `\columnsep`
with a restore to a local `\columnsep` inside wrapfig's placement. Three
new fixtures with layout and log checks; README and DESIGN text. The
`classoption` check in `wrapped.lua` and its console warning stay.

**Out:**
- A warning in Quarto's console for columns set by a class, `\twocolumn`,
  or `multicols`: the check runs only while LaTeX runs. Candidate row
  "Warn in the console for LaTeX columns".
- Wrapping inside a column: the question set chose the fallback; no row.
- Typst columns: candidate row "Check wrapped figures in Typst columns".
- Column layouts from a LaTeX class or package that neither turn on
  LaTeX's two-column mode (`\if@twocolumn`) nor open a `multicols`
  environment: the README says they are not detected; no row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: In `tests/twocolumn-class.qmd`, whose class file beside it
      loads `article` with `twocolumn` and which sets no `classoption`, a
      captioned wrapped figure and an uncaptioned wrapped image render as
      normal figures: layout cases in the `LAYOUT` list of `tests/verify.py`
      find no text line of each image's column beside that image, and the
      captioned figure's caption below its image.
- [x] AC2: A wrapped figure follows a raw `\twocolumn` or `\onecolumn`
      before it. In `tests/twocolumn-switch.qmd`, layout cases find the
      paragraph after a wrapped figure before a raw `\twocolumn` beside that
      figure, no text line of its column beside a wrapped figure after that
      `\twocolumn`, and the paragraph after a wrapped figure after a later
      raw `\onecolumn` beside that figure.
- [x] AC3: In `tests/multicols.qmd`, a captioned wrapped figure and an
      uncaptioned wrapped image inside a two-column `multicols` opened and
      closed by separate `{=latex}` raw blocks are in the PDF in place. The
      text around them is long enough that each image and the paragraphs
      before and after it sit in the first column, and a layout case finds
      each image below the paragraph before it and above the paragraph
      after it, with no text line of that column beside it.
- [x] AC4: A fallback in `wrapped.tex` writes its LaTeX warning. With
      `latex-clean: false`, which keeps the `.log` beside the `.qmd`,
      `tests/verify.py` reads each fixture's log, joined across TeX's line
      breaks, and finds: one `Package wrapped Warning` for two-column text
      in `twocolumn-class` and in `twocolumn-switch`, one `multicols`
      warning naming the line of each figure's `\begin{wrappedfigure}` in
      `multicols`, and no `Package wrapped Warning` in `stop-latex`.
- [x] AC5: Wrapped figures set the gap only where wrapfig places them. In
      `tests/multicols.qmd`, a layout case finds that a `multicols` after a
      raw group that sets `\columnsep` locally around a wrapped figure has
      the column gap of a `multicols` with no wrapped figure before it,
      measured between the left edges of its two columns' text. For a
      captioned `.wrap-left` and a captioned `.wrap-right` figure whose
      `wrap-gap` differs from 1em and from `\columnsep` by more than the
      layout check's tolerance, a layout case finds the distance between
      the image's edge and its paragraph's lines equal to that gap within
      that tolerance.
- [ ] AC6: The README's "PDF through LaTeX" section says that a wrapped
      figure where the text runs in columns, set by `classoption`, a class
      default, `\twocolumn`, or `multicols`, renders as a normal figure;
      that only `classoption` gives a warning in Quarto's output and the
      others write theirs to the LaTeX log, kept with `latex-clean: false`;
      and that a column layout from a LaTeX class or package that neither
      turns on LaTeX's two-column mode nor opens a `multicols` environment
      is not detected, without naming `paracol` as such a layout. Its sentence that a class default
      such as IEEEtran is not detected is gone. Step 1 of DESIGN.md's
      Architecture names the check in `wrapped.tex`.
- [ ] AC7: `python3 tests/verify.py` passes on macOS and in the
      `verify.yml` CI workflow on the milestone's PR: every render exits
      with status 0, every snapshot matches, and every layout and log check
      passes.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T2, T3
- AC5 → T1
- AC6 → T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label. -->

- [x] T1: Gap. Write `tests/multicols.qmd` with the `\columnsep` group case
      and the two `wrap-gap` cases of AC5, add their layout cases, and see
      the `\columnsep` case fail. In `_extensions/wrapped/wrapped.tex`, keep
      each figure's gap in a global macro at the environment's end and set
      `\columnsep` to it at the start of wrapfig's `\WF@putfigmaybe`, inside
      the group of `\WF@floathand` (`wrapfig.sty` lines 94-104); remove
      `\wrapped@setcolsep`, `\wrapped@restorecolsep`, and their hooks.
- [x] T2: Columns. Add `tests/twocolumn-class.qmd` with its class file,
      `tests/twocolumn-switch.qmd`, and the `multicols` figure cases in
      `tests/multicols.qmd` to `RENDERS` and `LAYOUT`, with
      `latex-clean: false`, and see their layout cases fail. In
      `wrapped.tex`, after `\wrapped@endwrap` at the environment's start,
      test a `multicols` flag set by `\AddToHook{env/multicols/begin}`,
      then `\if@twocolumn`; in columns, set the content in a centered
      `minipage` of the `width` key, in a `figure` float or in place as
      Scope says, and write the warning. The raw environment of an
      uncaptioned image (`wrapped.lua` line 887) passes a key that says it
      has no caption.
- [x] T3: Log check and snapshots. Add the log check of AC4 to
      `tests/verify.py`, keeping each warning message short. Run
      `python3 tests/verify.py --update` and review the snapshot diff.
- [x] T4: Docs. Update the README's two-column bullet (README.md line
      212), the header comments of `wrapped.lua` (line 15) and
      `wrapped.tex`, and step 1 of DESIGN.md's Architecture.
- [x] T5: Run `python3 tests/verify.py` on macOS and see `verify.yml` pass
      on the PR.
- [x] T6: Review return 1: README states that figures in columns render
      as normal figures (AC6), and the fix-now findings listed in the
      Review section: mode p in inner mode, hypcap in mode p, width claim,
      log parser, dead caption check, README and PROFILE text, W2 row.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046). -->

- 2026-10-26: created by /milestone-plan.
- 2026-10-26: tier check: not run — work named at the question set.
- 2026-10-26: question set: work — two-column LaTeX detection (candidate "Detect two-column LaTeX classes and gaps", absorbed in full); columns — fall back to a normal figure with a warning, not wrap inside a column.
- 2026-10-26: idea vet: one concern, that wrapfig's manual says it works in two-column text; the columns answer settled it toward the fallback. `\if@twocolumn` is the kernel flag that every route to two columns sets, and floats are dropped inside `multicols` (checked in a scratch compile).
- 2026-10-26: lessons used: 2026-10-26 (M007) pdftohtml -xml boxes; 2026-10-25 (M004) \message and grep -a; 2026-10-25 (M004) wrapfig verbose log.
- 2026-10-26: collision check: candidate row absorbed; "Check wrapped figures in Typst columns" is distinct (Typst) and stays; M004 shipped the `classoption` check, which this extends; no D-entry collides.
- 2026-10-26: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-26: the candidate's waiting-figure gap leak is not reachable through markdown since M007, because every raw block after a wrap's paragraphs gets `\wrappedstop`; the local `\columnsep` removes it anyway, so AC5 tests only the local-group leak.
- 2026-10-26: plan gate chose a check in `wrapped.tex` at each figure over a list of two-column classes in `wrapped.lua` because a TeX flag covers every class and `\twocolumn` and a list goes stale; falsified by users missing the log-only warning (candidate row "Warn in the console for LaTeX columns").
- 2026-10-26: plan gate chose a local `\columnsep` inside `\WF@putfigmaybe` over the global set and restore because wrapfig reads `\columnsep` only there; falsified by a wrapfig version that reads it elsewhere.
- 2026-10-26: plan gate chose a class file in `tests/` that loads `article` with `twocolumn` over IEEEtran because it adds no TeX package to the test setup; falsified by a class whose two columns the TeX check misses. IEEEtran gets a by-hand render at implement.
- 2026-10-26: criteria audit (full mode, fresh Opus reader): 11 findings, all fixed. AC1 and AC2 narrowed to the fixtures; AC3 uses separate raw blocks, first-column text, and an uncaptioned case; AC4 became an output property checked by `verify.py` through `latex-clean: false` (confirmed to keep the `.log`), names `\begin{wrappedfigure}`, joins TeX's line breaks, and warns per the DESIGN goal's render and context rules; AC5 requires a gap apart from 1em and `\columnsep`, captioned figures, both sides; AC6 names `latex-clean: false`, drops the IEEEtran sentence, and covers DESIGN; T2 tests `multicols` first by a hook, since `\if@twocolumn` stays true inside `multicols` in two-column text. AC7 no finding.
- 2026-10-26: implement started on branch m009-latex-columns.
- 2026-10-26: T1 done. `wrapped.tex` keeps the gap in `\wrapped@gap` and sets `\columnsep` inside `\WF@putfigmaybe`; the global set and restore are gone. `tests/multicols.qmd` and 3 layout cases: the local-group case failed before the change (364 px against 341 px) and passes after; with the gap line removed from `\WF@putfigmaybe` both wide-gap cases fail (15 px against 45 px). `tests/.gitignore` ignores the `.log` and `.aux` that `latex-clean: false` keeps. verify: 37 renders pass, 24 layout cases pass, no snapshot changed but the new one.
- 2026-10-26: checkpoint, T2 to T4 in progress: column fallback in `wrapped.tex` (modes w/f/p, `multicols` hook first), `caption=false` on raw image environments, fixtures `twocolumn-class` (with `twocol.cls`), `twocolumn-switch`, and `multicols` figure cases, the `LOGS` check in `verify.py`, README and DESIGN text. Layout and log cases failed before the change and pass after; planted defects (no multicols warning, two-column warning per figure) fail the log check. By-hand IEEEtran render: both cases pass, one two-column warning. Full verify with `--update` is running; snapshots are not in this commit.
- 2026-10-26: full verify with `--update`: 39 renders pass, 31 layout cases and 4 log checks pass. Snapshot diffs: `caption=false` on raw image environments in fixture, pdf-ua, pdf-ua1, stop-latex; new cases in multicols; new snapshots twocolumn-class and twocolumn-switch.
- 2026-10-26: by-hand paracol render: paracol sets `\global\@twocolumntrue` (paracol.sty line 2021), so the check finds it and the figure is a normal figure with the two-column warning. AC6's "paracol is not detected" and the Scope Out bullet are false; amendment proposed.
- 2026-10-26: re-audit: AC6 (full) — 3 findings: a README that kept "such as paracol" would pass; the Scope Out bullet names paracol too; say "opens a multicols environment". All taken into the next wording.
- 2026-10-26: re-audit: AC6 (full) — 1 finding: Quarto's `.columns` div is a column layout that the Lua filter detects, so "a column layout that neither turns on two-column mode nor opens multicols is not detected" is false; repair "a column layout from a LaTeX class or package that ...". Second re-audit line on AC6: the wording goes to the user.
- 2026-10-26: substantive amendment: AC6's paracol clause now reads "a column layout from a LaTeX class or package that neither turns on LaTeX's two-column mode nor opens a `multicols` environment is not detected, without naming `paracol` as such a layout"; the Scope Out bullet matches. The user accepted this wording at the stop.
- 2026-10-26: T4 done: README two-column bullets, `wrapped.lua` and `wrapped.tex` header comments, DESIGN.md Architecture steps 1 and 7.
- 2026-10-26: verify on macOS on c99e972: 39 renders pass, 31 layout cases, 4 log checks, no snapshot difference. CI on the PR is left to review.
- 2026-10-26: claim audit pass (fresh Opus reader): 41 claims, 3 corrected (the verify.py log-line comment, since TinyTeX sets max_print_line 10000; the twocolumn-class page-1 sentence; "normal figure" in wrapped.tex and README, now "do not wrap"). Its edge case, a wrapped figure in `multicols` under `classoption: twocolumn`, was rendered by hand: LaTeX drops it. README now says so, and candidate row "Keep wrapped figures in multicols" holds the fix. Re-read of the corrections is running; checkpoint commit.
- 2026-10-26: claim audit: 41 claims read, 3 corrected — tests/verify.py, tests/twocolumn-class.qmd, _extensions/wrapped/wrapped.tex, README.md. The re-read found all corrections hold; its two wording nits (the log-join comment, "a figure from that document") are applied.
- 2026-10-26: T5: verify on macOS on 8ad78ab: 39 renders pass, 31 layout cases, 4 log checks, no snapshot difference. The `verify.yml` run on the PR happens at review, which opens the PR. Status set to review.
- 2026-10-26: review return 1: AC6 fails as written: the README says figures in columns "do not wrap" and no longer says that a figure in columns set by a class default, `\twocolumn`, or `multicols` renders as a normal figure. Also the review's fix-now findings: diff-bug #1 (mode p in inner mode), #2 (hypcap in mode p), #4 (width claim), #5 and #6 (log parser), #7 (dead caption check), prior-review #1 (untested README sentence), prior-review #2 and ripple #2 (PROFILE and docstring), ripple #3 (README wrapfigure sentence), ripple #4 (wrap-mechanisms W2). See the Review section.
- 2026-10-26: T6 added for review return 1 (minor amendment).
- 2026-10-26: T6 checkpoint: `wrapped.tex` sets mode p for a captioned figure in inner mode in two-column text, and turns hypcap off in mode p; verify.py reads the log with line breaks removed, fails on a missing log, deletes a stale log before the render, drops the dead caption check, and fails on the caption package's hypcap warning; new case "figure in a box" in twocolumn-class (a raw minipage). With the T5 `wrapped.tex`, the twocolumn-class render exits 1 (Float(s) lost) and the multicols log check fails on the hypcap warning; with the fix both pass. README: figures in columns "render as normal figures: they do not wrap", a percent width is a share of the column, a figure inside a box stays in place, the wrapfigure sentence names the column case, the untested classoption-multicols sentence is gone. PROFILE.md and the verify.py docstring name the log check; wrap-mechanisms W2 corrected M009. Full verify with `--update` running; snapshots not in this commit.
- 2026-10-26: T6 done: full verify with `--update`: 39 renders pass, 32 layout cases and 4 log checks pass; the one snapshot change is the new `fig-box` environment in twocolumn-class. Status set to review.
- 2026-10-26: claim audit: 24 claims read, 2 corrected — _extensions/wrapped/wrapped.tex, cairn/references/wrap-mechanisms.md (T6 delta b273058..882e1cc). The reader also named the stale `wrapped.tex` header comment on in-place cases, now corrected. Comment-only changes; no render changes.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. EXEMPT from
     the 150-line cap (D-074). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap. -->

Pass 1, on d142e36 (level with origin/main e1f0cf3). `python3 tests/verify.py`, fresh run: all 39 renders pass, every snapshot matches.

- AC1 evidence: `ok layout twocolumn-class figure` and `ok layout twocolumn-class image` (check_alone finds no text of the image's column beside each image; the figure's caption is below its image). The fixture's class file `tests/twocol.cls` loads article with twocolumn; the fixture sets no classoption.
- AC2 evidence: `ok layout twocolumn-switch before twocolumn` (paragraph beside), `in two columns` (no column text beside), `after onecolumn` (paragraph beside).
- AC3 evidence: `ok layout multicols figure in multicols` and `image in multicols` (same page as the paragraphs before and after, below the one and above the other, in their column, nothing beside). The `multicols` is opened and closed by separate `{=latex}` blocks.
- AC4 evidence: `ok log twocolumn-class`, `ok log twocolumn-switch` (one two-column warning each), `ok log multicols` (multicols warnings on the lines of the two `\begin{wrappedfigure}` inside multicols, checked against the kept .tex; the check also asserts that count is 2), `ok log stop-latex` (no wrapped warning). The fixtures set `latex-clean: false`; the check joins 79-character lines.
- AC5 evidence: `ok layout multicols local columnsep` (gap after the group equals the reference, 341 px), `wide gap left` and `wide gap right` (captioned figures, `wrap-gap="30pt"`, text 45 px from the image within 3 px; 30pt differs from 1em and from \columnsep, 10pt, by 30 px).
- AC6 evidence (README.md lines 212-225, DESIGN.md Architecture step 1, read on d142e36): the README names the four column sources, says only `classoption` warns in Quarto's output and the others write to the LaTeX log kept with `latex-clean: false`, has the not-detected sentence for a class or package layout with neither two-column mode nor `multicols`, names no paracol, and has no "IEEEtran is not detected" sentence; DESIGN step 1 names the check in `wrapped.tex`. FAIL on one clause: since the claim-audit correction, the README says wrapped figures in columns "do not wrap" and names "normal figures" only for the `classoption` case and for a captioned float in two-column text; it no longer says that a figure in columns set by a class default, `\twocolumn`, or `multicols` renders as a normal figure. Not ticked.
- AC7 evidence (macOS part): the run above, 39 renders, 31 layout cases, 4 log checks pass. The CI half needs the PR, which step 8 opens. Not ticked yet.
- Gate: `cairn_validate.py` all checks pass; one version marker (`_extension.yml` 0.1.0, unchanged by the branch); verify passes (above); changelog slot "none". No DESIGN principle changed, so no impact report.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: in two-column text a captioned wrappedfigure in inner mode (a raw minipage or tcolorbox, the optional argument of `\twocolumn[...]`) starts a `figure` float, and LaTeX stops with "Float(s) lost" (reviewer's scratch compile); wrapfig set such a figure in place before — fix now (test `\ifinner` and use mode p)
- diff-bug #2: each in-place captioned figure logs "Package caption Warning: The option `hypcap=true' will be ignored" (tests/multicols.log) — fix now (hypcap off in mode p)
- diff-bug #3: the warnings say "set as normal figure(s)" though mode p sets the figure in place — reject (false): in this project a normal figure is one that keeps its normal layout, not a wrap (DESIGN Goals), which both modes are
- diff-bug #4: README "Each keeps its width as a share of the column" holds only for a percent width; `3in` stays 3in — fix now
- diff-bug #5: the 79-character join never runs under TinyTeX (max_print_line 10000), and pdfTeX breaks by bytes — fix now (read the log with its line breaks removed, so any break width works)
- diff-bug #6: a missing `.log` raises FileNotFoundError, a stale `.log` from an earlier run can be read, and `int(n)` fails on a warning without a line — fix now
- diff-bug #7: `normal_case`'s caption-below check can never fail, since `find_figure` already requires the image above the caption — fix now (drop the dead check; `find_figure` holds the AC1 clause)
- diff-bug #8: the local `\columnsep` is set before wrapfig's `\penalty`, so an output routine fired there sees the gap — reject (false): no wrong result in one-column text, and the old global set was wider
- diff-bug (c) "before twocolumn", "image in multicols", the twocolumn-switch log count — reject (planned change): AC2, AC3, and AC4 name these cases
- blame-history #1: caption styling now runs only in mode w, and README line 189 says "a caption inside a wrapped figure is set ragged-right" — reject (false): that README line is about wrapped figures, which mode w still styles
- blame-history #2: `\AddToHook` raises the kernel floor — reject (false): `\NewDocumentEnvironment` in the kernel already needs LaTeX 2020-10, the same release
- blame-history #3: wrapfig reading `\columnsep` only in `\WF@putfigmaybe` is recorded only in the work log — reject (false): the `wrapped.tex` header comment states it
- blame-history #4: `\WFclear` is a hand copy of wrapfig's — reject (false): no defect; the branch changes only its last line
- blame-history #5: the log join joins every 79-character line — fix now (same fix as diff-bug #5)
- prior-review #1: README "LaTeX loses a figure from that document inside `multicols`" has no fixture — fix now (drop the sentence; candidate row "Keep wrapped figures in multicols" holds the case)
- prior-review #2: PROFILE.md says verify exits 1 on a failed render, difference, or layout case, and omits the log check — fix now
- prior-review #3: an uncaptioned image's alt text in mode p is not exercised in tagged PDF — reject (false): the mode changes only the wrapper; the body's `\includegraphics` and its `alt` key are the same, and the pdf-ua snapshots pin `alt`
- prior-review #4: no case has a figure waiting when `multicols` begins — reject (false): unreachable through markdown, since every raw block after a wrap's paragraphs gets `\wrappedstop` (plan work log)
- ripple #1: ROADMAP candidate row "Detect two-column LaTeX classes and gaps" now misdescribes the code — reject (planned change): post-merge hygiene removes the absorbed row
- ripple #2: PROFILE.md lines 29-30 and 46-47 and the verify.py docstring omit the log check — fix now (with prior-review #2)
- ripple #3: README lines 166-167 say the extension puts each wrapped figure in a `wrapfigure` — fix now
- ripple #4: `cairn/references/wrap-mechanisms.md` W2 says `wrappedfigure` calls `wrapfigure` — fix now (mark corrected M009)
- ripple #5: PROFILE.md line 56 "the `LAYOUT` list" names a dict — reject (style): a pre-existing word choice, "list" read as a list of fixtures
