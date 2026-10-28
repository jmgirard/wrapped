# M025: Stop text overlap with small wrap-lines

- **Status:** in-progress
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

- [ ] AC1: In PDF through LaTeX, in body text outside boxes such as callouts, a `wrap-lines` value N can be smaller than the count that wrapfig takes from the figure's height. Its N narrowed lines can then end on the figure's page above the figure's bottom. In that case, the heading or the wrapped figure that stops the wrap starts below the figure. A stop heading also sits at most one line lower, measured from the figure's bottom, than the stop heading of the existing case of the same form and side without `wrap-lines`. New layout cases in `tests/stop-latex.qmd` show this, and `python3 tests/verify.py` checks them. In case (a), a right-side image with an id and a caption has `wrap-lines="4"` and one paragraph of exactly 4 lines, then a heading. In case (b), a left-side image with no caption has a count that ends inside its first paragraph, then a short second paragraph, then a heading. In case (c), a right-side image with an id and a caption has a count that ends inside its second paragraph, and the next wrapped figure stops the wrap. Each of the three cases fails on `main` at the plan commit.
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
- [ ] T4: Run `python3 tests/verify.py` in full.

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

## Decisions

## Review
