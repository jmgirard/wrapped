# M025: Stop text overlap with small wrap-lines

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes where text lands in users' PDFs
- **Branch/PR:** m025-small-wrap-lines

## Goal

In PDF through LaTeX, the block that stops a wrap starts below the figure also after a small `wrap-lines` value ends the narrowed lines early.

## Scope

**In:** A measured skip in `\wrapped@endwrap` of `_extensions/wrapped/wrapped.tex` for a wrap whose narrowed lines ended above the figure's bottom on the figure's page. The paragraphs beside the figure keep the `wrap-lines` count, as wrapfig documents. New layout cases in `tests/stop-latex.qmd` and `tests/verify.py`. The `wrap-lines` text of `docs/formats/latex.qmd` and `cairn/DESIGN.md`, and a D-entry that annotates D-007.

**Out:** Wraps inside callouts and other boxes go to the new candidate row "Check small wrap-lines in callouts". The extra gap that paragraph spacing adds below a figure stays in the row "Trim the LaTeX stop gap at page tops". Text inside the paragraphs past the count keeps running at full width, as wrapfig documents.

## Acceptance criteria

- [x] AC1: In PDF through LaTeX, with Quarto's default line and paragraph spacing, in body text outside boxes such as callouts, a `wrap-lines` value N can set fewer lines than wrapfig narrows when `wrap-lines` is unset. In each of the cases below, the N lines end above the figure's bottom, and the paragraph that holds the figure follows a heading at the top of a page, with no footnote beside the figure. In each case, the block that stops the wrap starts below the figure: a heading in cases (a) and (b), and the next wrapped figure in case (c). In cases (a) and (b), the stop heading also sits at most one line lower, measured from the figure's bottom, than the stop heading of the "form A right" and "form C left" cases of the same fixture, which set no `wrap-lines`. `python3 tests/verify.py` checks these cases in `tests/stop-latex.qmd`. In case (a), a right-side image with an id and a caption has `wrap-lines="4"` and one paragraph of exactly 4 lines, then a heading. In case (b), a left-side image with no caption has a count that ends inside its first paragraph, then a short second paragraph, then a heading. In case (c), a right-side image with an id and a caption has a count that ends inside its second paragraph, and the next wrapped figure stops the wrap.
- [ ] AC2: The fix adds no space where the text already clears the figure. In case (d), the count ends early, but full-width text runs past the figure's bottom before a stop heading. The gap between that paragraph's last line and the heading is within 2 px of the same gap in a twin paragraph and heading with no figure. In case (e), the stop heading falls on the next page, and its top is within one line of the top text edge of that page.
- [ ] AC3: The paragraphs beside the figure keep the `wrap-lines` count. In case (b), the first N lines of the first paragraph start right of the figure. Its line N+1 and the first line of the second paragraph start at the left edge of the text block.
- [ ] AC4: Every layout that a case on `main` at the plan commit checks still holds, and no such case is removed or loosened. `python3 tests/verify.py` exits 0.
- [ ] AC5: The "Lines beside the figure" section of `docs/formats/latex.qmd` says what a `wrap-lines` value smaller than the figure needs does. LaTeX narrows that many lines. The text after them runs at full width, also beside the figure. The block that stops the wrap starts below the figure. The first bullet of the Limits section also covers that skip. Each of these statements matches a case of AC1, AC2, or AC3.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1
- AC4 → T2, T4
- AC5 → T3

## Tasks

- [x] T1: Add cases (a) to (e) and the twin of case (d) to `tests/stop-latex.qmd`, and add their checks to `stop_latex_cases` in `tests/verify.py`. Compare the heading gaps of (a) and (b) with the existing "form A right" and "form C left" cases, as `lines_case` does. Make sure that (a), (b), and (c) fail on `main`.
- [x] T2: In `_extensions/wrapped/wrapped.tex`, record the page and the `\pagetotal` where the wrap starts, in the `\WF@startwrapping` hook. If the narrowed lines ended on that page above the figure's bottom, make `\wrapped@endwrap` skip to below the figure. Keep the line-count skip for a wrap whose narrowed lines still run. Update the file's comments.
- [x] T3: Update the `wrap-lines` text of `docs/formats/latex.qmd` (AC5) and the `wrap-lines` row of `cairn/DESIGN.md`. Append a D-entry that annotates D-007: the stop block also skips below the figure after a smaller count ends. Refresh the `stop-latex` snapshot.
- [x] T4: Run `python3 tests/verify.py` in full.

## Work log

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: milestone — a change to the LaTeX stop code with a design choice.
- 2026-10-28: idea vet: one concern. wrapfig documents a smaller count as its fix for extra vertical space, such as Quarto's default paragraph spacing, so a minimum would remove that use. The user chose to keep the count and move the stop block below the measured figure bottom.
- 2026-10-28: question set: wraps inside callouts and other boxes — body text only, a candidate row holds callouts.
- 2026-10-28: lessons used: 2026-10-26 (M007) pdftohtml boxes and \intextsep; 2026-10-25 (M004) LaTeX PDF before Typst; 2026-10-27 (M012) one-fixture check.
- 2026-10-28: collision check: absorbs the candidate row "Stop text overlap with small wrap-lines". Extends archived M007 and D-007, which skip only while lines are narrowed. The row "Trim the LaTeX stop gap at page tops" stays apart. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-28: plan gate chose a measured skip at the stop block over raising a smaller count to wrapfig's count, because a smaller count is wrapfig's fix for paragraph spacing; falsified by a render where the measured skip leaves the stop block beside the figure on its page.
- 2026-10-28: plan chose to measure only where the narrowed lines ended, over measuring every stop, because measuring every stop changes the default gap that the "Trim the LaTeX stop gap" row holds; falsified by a case where the line-count skip and the measured skip disagree by more than one line.
- 2026-10-28: criteria audit (full mode, Opus reader): claim wider than two cases, no cap on the skip, no check against added space or a next-page stop, harness wording, AC2 claim wider than its check, stale Limits bullet, no D-007 annotation. All fixed: narrowed to body text outside boxes, cases (c) to (e), a one-line cap, harness detail moved behind layout claims, AC3 checks N narrowed lines, AC5 adds the Limits bullet, T3 adds the D-entry.
- 2026-10-28: T1 done. Cases (a) to (e) and the twin of (d) are in `tests/stop-latex.qmd`, checked by `small_a_case` to `small_e_case` in `tests/verify.py`. On the unchanged filter, (a) and (b) fail with "the stop heading … starts above the figure's bottom", (c) fails with "the next wrapped figure starts above the figure's bottom", and (d) and (e) pass. Case (b) uses a 40% width so its stop heading sits clearly above the figure's bottom on `main`.
- 2026-10-28: checkpoint, T2 and T3 written, not ticked: the full `python3 tests/verify.py` run is in progress and the `stop-latex` snapshot is not refreshed. `\wrapped@skipbelow` targets the start's `\pagetotal` plus `\WF@size` less one `\baselineskip`, a choice made against the stop gaps of (a) 46 px and (b) 44 px, which sit below their reference gaps of 62 px and 55 px. Added case (f), a paragraph that ends on the next page, because (e) cannot fail without the page check. Planted defects: no page check fails (f); a skip of the full `\WF@size` fails (a), (b), and (d).
- 2026-10-28: T2 and T3 done. The full run failed only on the `stop-latex` snapshot, which lacked the seven new figures; the snapshot is refreshed. 64 layout cases passed, none failed.
- 2026-10-28: T4 done. `python3 tests/verify.py` at `1b0b521` exits 0: all 103 renders pass and 64 layout cases pass.
- 2026-10-28: claim audit: 29 claims read, 5 corrected — docs/formats/latex.qmd, _extensions/wrapped/wrapped.tex, tests/stop-latex.qmd. The corrections are text past the count "prints over the figure", the stop and Limits statements limited to body text, the skip comment matching the code, `\pagetotal` up to date in the main vertical list only, and the case (e) comment. The same reader re-read all five, and each holds. The `stop-latex` render after the edits keeps its snapshot and passes its layout cases.
- 2026-10-28: review checkpoint: evidence recorded, criteria not yet ticked, because prior-review #1 asks for same-page checks in the new cases, and the evidence is re-run after that fix. Diff-bug and blame-history reviewers still running.
- 2026-10-28: review checkpoint: fix-now work from the four lenses committed, full suite run on it in progress. The `stop-latex` fixture alone passes all 16 layout cases and keeps its snapshot.
- 2026-10-28: `python3 tests/verify.py` on the files of `6bcd808` exits 0: all 103 renders pass and 64 layout cases pass.
- 2026-10-28: amendment routed: AC1 — diff-bug #1: when TeX breaks the page just before the figure's first line, the narrowed lines end on the figure's page above its bottom, but the start's page count is stale and the stop block is not moved, so AC1's prose promises more than the code does; the case is outside AC1's named cases (a) to (c).
- 2026-10-28: re-audit: AC1 (full) — the first amended wording ("no page break between the paragraph where wrapfig places the figure and the block that stops the wrap") still covers a paragraph moved to the next page; the one-line cap is false for case (d); "existing case of the same form" and "fails on `main`" bind the test fixture; the domain is wider than Quarto's default spacing; "the count that wrapfig takes" is off by one. All taken into the second wording, which goes to a second reader.
- 2026-10-28: re-audit: AC1 (full) — the second wording reads "that block, a heading or the next wrapped figure" as if no other block stops a wrap; the cap's reference ("a figure of the same side and caption form") fixes no width or text; all three cases start after a heading at a page top, so a mid-page start is untested; a footnote beside the figure can lower the page goal and lose the skip. This is the second re-audit of AC1, so the wording goes to the user.
- 2026-10-28: proposed AC1 wording (narrow to the cases): "AC1: In PDF through LaTeX, with Quarto's default line and paragraph spacing, in body text outside boxes such as callouts, a `wrap-lines` value N can set fewer lines than wrapfig narrows when `wrap-lines` is unset. In each of the cases below, the N lines end above the figure's bottom, and the paragraph that holds the figure follows a heading at the top of a page, with no footnote beside the figure. In each case, the block that stops the wrap starts below the figure: a heading in cases (a) and (b), and the next wrapped figure in case (c). In cases (a) and (b), the stop heading also sits at most one line lower, measured from the figure's bottom, than the stop heading of the "form A right" and "form C left" cases of the same fixture, which set no `wrap-lines`. `python3 tests/verify.py` checks these cases in `tests/stop-latex.qmd`. In case (a), a right-side image with an id and a caption has `wrap-lines="4"` and one paragraph of exactly 4 lines, then a heading. In case (b), a left-side image with no caption has a count that ends inside its first paragraph, then a short second paragraph, then a heading. In case (c), a right-side image with an id and a caption has a count that ends inside its second paragraph, and the next wrapped figure stops the wrap."
- 2026-10-28: amendment return: AC1 — "In each of the cases below, the N lines end above the figure's bottom, and the paragraph that holds the figure follows a heading at the top of a page, with no footnote beside the figure. In each case, the block that stops the wrap starts below the figure: a heading in cases (a) and (b), and the next wrapped figure in case (c)." The user chose this narrowed wording at the stop, over adding a mid-page case and a 40% twin. AC1 now opens with "with Quarto's default line and paragraph spacing", names the "form A right" and "form C left" references, and drops "fails on `main`", which T1 holds. The mid-page start and the footnote case join the row "Check small wrap-lines stops in more layouts".

## Decisions

## Review

Evidence, 2026-10-28, on the review head `1453ed2`, branch level with `main` (`ecba1d8`):

- AC1: `python3 tests/verify.py` at `1453ed2` prints `ok` for `small wrap-lines a`, `b`, and `c`. `stop_gap` holds each heading of (a) and (b) below the figure and within one line of its reference gap. The same fixture rendered with `main`'s extension files (`ecba1d8`, scratch folder) fails (a) and (b) with "the stop heading … starts above the figure's bottom" and (c) with "the next wrapped figure starts above the figure's bottom".
- AC2: the same run prints `ok` for `small wrap-lines d` (the heading gap is within 2 px of the twin's) and `small wrap-lines e` (the heading is on the next page, within one line of its top text edge).
- AC3: the same run prints `ok` for `small wrap-lines b`. Its first 3 lines start right of the figure, and line 4 and the second paragraph start at the left edge.
- AC4: the run exits 0. All 103 renders pass and 64 layout cases pass, none failed. `git diff ecba1d8 HEAD` deletes no line of `tests/verify.py`, `tests/stop-latex.qmd`, or `tests/_snapshots/`, so every case on `main` and its checks stand unchanged.
- AC5: `docs/formats/latex.qmd` lines 31 to 34 say that LaTeX narrows that many lines, that the text after them runs at full width, also beside the figure, where it prints over the figure, and that in body text the stop block starts below the figure. The first Limits bullet adds that the extension skips to below the figure in body text. These statements match cases (a) and (b) (the narrowed count), (b) (full width over the left figure), and (a), (b), and (c) (the stop below the figure).
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: when TeX breaks the page just before the figure's first line, the start's page count is stale, the skip is lost, and the stop block overlaps as on `main` — amendment routed for AC1, whose prose covers that case, and follow-up in the row "Check small wrap-lines stops in more layouts"
- diff-bug #2: the skip also fires after wrapfig's own count, for example with a display equation, changing layouts with no `wrap-lines` — fix now, fixed 6bcd808: the skip runs only when the start count is below the height count
- diff-bug #3: case (e) passes with a 13 px misplacement inside its one-line tolerance — fix now, fixed 6bcd808: the tolerance is 3 px (the heading sits 1 px from the top text edge)
- diff-bug #4: no case covers a wrap that starts at a page top — follow-up, row "Check small wrap-lines stops in more layouts"
- diff-bug #5: the target is tuned against heading stops only, and is untested under a larger `\parskip` or `linestretch` — follow-up, same row
- diff-bug #6: "in body text" does not name lists and block quotes, where `\ifinner` is false and the skip runs — reject, false: lists and block quotes are body text, not boxes, and the skip working there is the documented behavior
- diff-bug #7: case (c) does not check that the count ends inside the second paragraph above the figure's bottom — fix now, fixed 6bcd808: `small_c_case` asserts a full-width line of the second paragraph above the figure's bottom
- diff-bug #8: case (b) at 40% compares with "form C left" at 35% — reject, false: AC1 names the same form and side, and the gap is measured from the figure's bottom, so the height difference does not enter it
- diff-bug #9: a raw `wrapfigure` in the user's LaTeX also sets the start record — follow-up, same row
- diff-bug #10: the header comment says only narrowed text skips, and the `\pagetotal` comment is a run-on — fix now, fixed 6bcd808: both comments rewritten
- blame-history #1: `\ReadonlyShipoutCounter` adds an unguarded kernel requirement — reject, false: `\AddToHook`, already in `wrapped.tex`, needs the same 2020-10 kernel
- blame-history #2: the docs and `small_b_case` lock in text past the count printing over the figure — reject, planned change: the user chose it at the question set (D-015)
- blame-history #3: the skip is not limited to a small count — fix now, fixed 6bcd808, as diff-bug #2
- blame-history #4: `\ifwrapped@started` survives a `\WFclear` at `\clearpage` — fix now, fixed 6bcd808: `\WFclear` resets it
- blame-history #5: case (e) takes its top text edge from another page — reject, false: the top text edge is the same on every page, and that page opens with a heading at its top
- prior-review #1: `stop_gap`, `small_c_case`, and `small_d_case` can pass with the measured item on a later page, as M007 pass 2 diff-bug #7 found in case 8 — fix now, fixed 6bcd808: each asserts the figure's page
- prior-review #2: the start record is now read after the narrowed lines end, so its reset matters — fix now, fixed 6bcd808, as blame-history #4
- prior-review #3: `paragraph_lines` keeps the caption in its first line — fix now, fixed 6bcd808: `leave` applies to the first line too
- ripple #1: the Limits page-break bullet does not say the skip adds nothing after a page break — reject, false: after a page break the stop block is on a later page, so it starts below the figure
- ripple #2: the candidate row "Stop text overlap with small wrap-lines" describes the fixed defect — fix now: post-merge hygiene removes the row as M025 graduates it
- ripple #3: `cairn/DESIGN.md` lines 108 to 109 omit the new skip — fix now, fixed 6bcd808
- ripple #4: the header comment of `wrapped.tex` omits the new skip — fix now, fixed 6bcd808, as diff-bug #10
- ripple #5: `cairn/references/wrap-mechanisms.md` E9 omits the new skip — fix now, fixed 6bcd808
- ripple #6: the row "Trim the LaTeX stop gap at page tops" says no fixture covers a smaller `wrap-lines` — fix now, fixed 6bcd808: the clause is removed
- Gate: `cairn_validate.py` passes. The one version marker, `_extensions/wrapped/_extension.yml`, reads 0.2.0. The verify command passes on the review head. The changelog slot is "none". No DESIGN.md principle changed, so `cairn_impact` was skipped.

Pass 2 findings:

- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the case (c) precondition does not check that the second paragraph opens narrowed — fix now, fixed 66ee2f0: its first line must end left of the figure
- diff-bug #2: case (c) checks the next figure's image top, which sits `\intextsep` below its paragraph, so that paragraph could sit beside the first caption — fix now, fixed 66ee2f0: the paragraph beside the next figure must also start below the first figure
- diff-bug #3: cases (a) and (b) do not assert that the narrowed lines end above the figure's bottom — fix now, fixed 66ee2f0: (a) asserts its 4th line ends above the bottom, (b) that its line 4 is beside the figure
- diff-bug #4: the docs' "in body text, the block that stops the wrap starts below the figure" has no exception for a page break before the figure's paragraph or a footnote beside the figure — fix now, fixed 66ee2f0: the docs name both limits
- diff-bug #5: the two new candidate rows link different paths for the M025 file — fix now, fixed 66ee2f0: both link the archive path that hygiene writes
- diff-bug #6: case (f) is not named by any criterion — reject, false: a test that pins the page check this change adds is in scope by the test rules, and T2's work log names it
- diff-bug #7: the header comment says "the text skips" where the stop block moves — fix now, fixed 66ee2f0
- blame-history #1: the docs' "prints over the figure" conflicts with D-011's "an early stop only leaves space" — reject, planned change: D-011's line is a reason for a shortcode stop rule, not a rule on wrap-lines, and the option the user chose at the question set said that text past the count still runs at full width, as wrapfig does
- blame-history #2: a wrap that starts inside a box records a stale `\pagetotal` — reject, false: the filter writes `\wrappedstop` in the same block list as the figure, so the stop is inside the box too, where `\ifinner` skips nothing
- blame-history #3: the skip leaves out the last line's `\pagedepth`, so the stop lands about one line depth lower — reject, false: the stop still starts below the figure, and `stop_gap` holds it within one line of the reference
- prior-review #1: `\WFclear` at the start of `\wrapped@endwrap` resets the flag before a waiting figure's stop reads it — reject, false: a waiting figure never started a wrap, and its own `\begin{wrappedfigure}` already cleared the flag
- prior-review #2: the case (c) precondition skips the first line — fix now, as diff-bug #1
- ripple #1: the docs' "in body text" has no page limit — fix now, as diff-bug #4
- ripple #2: `cairn/references/wrap-mechanisms.md` E9 has no "in body text" — fix now, fixed 66ee2f0
- ripple #3: the row "Stop text overlap with small wrap-lines" still describes the defect — fix now: post-merge hygiene removes it, as pass 1 ripple #2
- ripple #4: the row "Trim the LaTeX stop gap at page tops" says no fixture covers a page-top figure, but case (a) starts at a page top — reject, false: case (a)'s figure follows a heading, while that row means a figure that wrapfig places at the very top of a page
- ripple #5: the comment "which is below the figure's bottom" gives no reason — fix now, fixed 66ee2f0: it states the `\WF@size` terms that put the point about `\intextsep` less half a line below the bottom
- ripple #6: the `\WFclear` reset has no comment — fix now, fixed 66ee2f0
- ripple #7: the header comment leaves out the box limit — fix now, fixed 66ee2f0

Pass 2 evidence, 2026-10-28, on `de4b856`, level with `main` (`ecba1d8`), after the fix-now commit `6bcd808` and the AC1 amendment:

- AC1 (amended): `python3 tests/verify.py` at `de4b856` prints `ok` for `small wrap-lines a`, `b`, and `c`. In each case the paragraph that holds the figure follows a heading at a page top, has no footnote, and the stop block starts below the figure on the figure's page (`stop_gap`, and `small_c_case`'s page and precondition checks). In (a) and (b), `stop_gap` holds the stop heading within one line of the "form A right" and "form C left" gaps.
