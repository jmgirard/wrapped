<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M008: Run the fixture renders in CI

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — CI over the repo's own fixture tests, which no user of the extension runs or relies on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m008-ci-verify, https://github.com/jmgirard/wrapped/pull/8 (draft)   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A GitHub Actions check runs `tests/verify.py` on every pull request to `main`, so a change that breaks a fixture render fails before it merges.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a workflow `.github/workflows/verify.yml` that installs Quarto's
release channel with TinyTeX, R with knitr and rmarkdown, and poppler on an
Ubuntu runner and runs `python3 tests/verify.py`, on pull requests to
`main`, on pushes to `main` outside `cairn/`, and by hand. On failure it
keeps the rendered test outputs as a run artifact. A second workflow
`.github/workflows/verify-prerelease.yml` runs the same command against
Quarto's pre-release channel weekly and by hand, never on a pull request,
so its failure blocks no merge. Fixes to `tests/verify.py` or the
workflows that the first Linux runs need, made so the same snapshots pass
on Linux and on macOS. D-008 records the CI tools. `cairn/PROFILE.md` and
`cairn/DESIGN.md` name the workflows.

**Out:** testing the minimum Quarto version 1.9.36 in CI (candidate row
"Test the minimum Quarto version in CI"). A macOS runner (the maintainer
runs the verify command on macOS before each merge). Browser layout checks
in `tests/layout.js` and the Word and LibreOffice checks of D-005, which are
not part of the verify command. Branch protection that requires the check
(a repository setting, the user's to change).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [x] AC1: `.github/workflows/verify.yml` runs `python3 tests/verify.py` from the repository root on an `ubuntu-latest` runner, after installing Quarto from its release channel with TinyTeX, R with the knitr and rmarkdown packages, and poppler's command-line tools. It runs on pull requests to `main`, on pushes to `main` that change a path outside `cairn/`, and by hand (`workflow_dispatch`).
- [x] AC2: On the milestone PR's last head commit, `gh pr checks` reports the `verify.yml` job as passed and the log of its `python3 tests/verify.py` step ends with `all <n> renders pass`, where n is the length of `RENDERS` in `tests/verify.py` at that commit; `python3 tests/verify.py` also exits 0 on this Mac at that commit.
- [x] AC3: `.github/workflows/verify-prerelease.yml` runs the same command after installing Quarto from its pre-release channel, on a weekly schedule and by hand, and has no `pull_request` or `push` trigger, so its result is not among a pull request's checks.
- [x] AC4: A commit pushed to the draft PR that changes one line of `tests/_snapshots/meta-string.html.txt` makes the `verify.yml` job fail, the log of its verify step has the line `FAIL meta-string.html`, and the failed run has an artifact that holds `tests/meta-string.html`, as `gh run download` lists.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T3
- AC3 → T2
- AC4 → T1, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write `.github/workflows/verify.yml`: `actions/checkout`,
      `quarto-dev/quarto-actions/setup` with `version: release` and
      `tinytex: true`, `apt-get install` of `r-base`, `r-cran-knitr`,
      `r-cran-rmarkdown`, and `poppler-utils`, then `python3 tests/verify.py`.
      On failure, `actions/upload-artifact` keeps the `.html`, `.pdf`,
      `.tex`, `.typ`, and `.docx` files under `tests/` (the `fixture.pdf`
      left is Typst's, per LESSONS 2026-10-25 M004). Triggers as AC1, with
      `paths-ignore: cairn/**` on the push trigger only.
- [x] T2: Write `.github/workflows/verify-prerelease.yml` with the same
      steps and `version: pre-release`, triggered by `schedule` (weekly) and
      `workflow_dispatch`. A shared reusable workflow is allowed if it keeps
      both files short.
- [x] T3: Run `python3 tests/verify.py` on this Mac, commit, push the
      `m008-ci-verify` branch, and open a draft PR (`gh pr create --draft`);
      record its URL in the Branch/PR header. Watch the check. Fix each
      Linux-only failure in the workflow or in `tests/verify.py` so the same
      snapshots pass on both systems, never by writing a Linux-only
      snapshot; log each fix and rerun on this Mac.
- [x] T4: Prove the check can fail: push a commit that changes one line of
      `tests/_snapshots/meta-string.html.txt`, confirm the failed run, its `FAIL` line, and the
      artifact (`gh run download`), then push a commit that restores the
      line and see the check pass again.
- [x] T5: Update `cairn/PROFILE.md` (the verify slot names both workflows
      and the CI channels) and `cairn/DESIGN.md` Conventions (tests also
      run in CI).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-26: created by /milestone-plan.
- 2026-10-26: tier check: not run — work named at the question set.
- 2026-10-26: question set: which work to plan — "Run the fixture renders in CI" (candidate row absorbed; added 2026-10-24).
- 2026-10-26: question set: pre-release Quarto channel — report only, a failure blocks no merge.
- 2026-10-26: question set (second round, since the work was chosen in the first): open the PR early as a draft so the workflow runs before the merge question — allowed; implement pushes `m008-ci-verify` and runs `gh pr create --draft`, and review marks that PR ready instead of creating one (an exception to D-138's late PR open, at the user's choice).
- 2026-10-26: idea vet: none — the workflow runs the existing verify command that CLAUDE.md's main-must-render rule relies on; the untested minimum Quarto version 1.9.36 is a separate gap, recorded as a candidate row.
- 2026-10-26: lessons used: 2026-10-25 (M002) tests/_extensions symlink and png figures for Typst; 2026-10-25 (M004) the Typst render overwrites fixture.pdf.
- 2026-10-26: collision check: candidate row "Run the fixture renders in CI" absorbed; D-002, D-005, D-006 consistent (CI installs the D-002 and D-006 needs; D-005's Word checks stay out); no archive overlap; inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-26: criteria audit (reduced, internal tier, fresh Opus reader): AC1 and AC3 no finding; AC2 accuracy finding (a job log does not end with the script's last line) fixed by reading the verify step's log; AC4 bounded-promise finding ("the rendered output of that fixture" spans formats and a book folder) fixed by naming meta-string.html.
- 2026-10-26: plan gate chose a separate scheduled pre-release workflow over a pull-request job with `continue-on-error` because that job still shows a failed check in the PR, which the merge rule reads as red CI; falsified by a run where a failed `continue-on-error` job leaves `gh pr checks` exiting 0.
- 2026-10-26: plan gate chose Ubuntu packages for R, knitr, rmarkdown, and poppler over `r-lib/actions/setup-r` because apt needs no second third-party action; falsified by a CI render that fails on the Ubuntu R or knitr version.
- 2026-10-26: plan gate chose an Ubuntu runner only over adding a macOS runner because AC2 already requires a local macOS pass and macOS runner minutes cost more; falsified by a merged commit that passes CI and fails the verify command on macOS.
- 2026-10-26: implement started; branch m008-ci-verify cut from main at 2a92353.
- 2026-10-26: T1/T2 written: two full workflow files instead of a shared reusable workflow, so each check's name and steps read from one file (about 45 lines each); actions pinned to major tags checkout@v7, quarto-actions/setup@v2, upload-artifact@v7; verify.yml cancels a superseded run on the same ref. T5 text written in PROFILE.md and DESIGN.md. Checkpoint before the local verify run finishes; no task ticked yet.
- 2026-10-26: T1, T2 done: `python3 tests/verify.py` on this Mac at 1e2e843 printed `all 36 renders pass`. Branch pushed; draft PR #8 opened (question-set grant); first CI run watched in the background. This commit stays local until that run ends, since a push would cancel it.
- 2026-10-26: T3 first CI run (40309346844, at 1e2e843) failed on one render: contexts.docx, the E3 margin cell plot at cx=4620126 against the snapshot's 5334000. Cause: Linux's R PNG device writes a 96-dpi pHYs tag and the macOS quartz device writes none, so Pandoc sized the plot from different dpi values (480x384 px in both). The cairo device was tried for both systems and fails on this Mac (no X11 libraries, LESSONS 2026-10-25 M002). Fix: that cell sets `out-width` to 5in for docx only (`!expr if (knitr::pandoc_to("docx")) "5in"`), so Word's size comes from the attribute; `--update` changed one line of contexts.docx.txt (5334000 to 4572000) and no other snapshot.
- 2026-10-26: T3 done: CI run 40310313074 at f8ffcbb succeeded, its verify step printing `all 36 renders pass`; local `python3 tests/verify.py` at f8ffcbb also printed `all 36 renders pass`.
- 2026-10-26: T4 planted change (6fd85b1, meta-string.html.txt breakpoint 576px to 577px): CI run 40310746574 failed with `FAIL meta-string.html: output differs from tests/_snapshots/meta-string.html.txt`, and `gh run download` of its `rendered-outputs` artifact listed `meta-string.html`. This commit restores the line.
- 2026-10-26: paused at the user's request. Restore commit be641d8 is pushed; its CI run 40312839783 was in progress, and its watcher was stopped. On resume: read that run (`gh run view 40312839783`); on success tick T4, tick T5 (PROFILE.md and DESIGN.md text is already committed in 1e2e843), then set status review. This line's commit is local only, since a push would cancel that run.
- 2026-10-26: resumed. CI run 40312839783 at be641d8 succeeded (`all 36 renders pass`); T4 done. T5 done (text in 1e2e843). `git diff f8ffcbb HEAD -- . ':!cairn'` is empty, so the local verify pass at f8ffcbb covers the code at this head; main has not moved since the cut.
- 2026-10-26: claim audit: not owed — internal tier.
- 2026-10-26: implement complete; status review.
- 2026-10-26: cairn_validate failed weight caps after 79e118f (PROFILE.md 123 lines, cap <120, from T5's CI paragraph); the paragraph was compressed to 3 lines (118 lines), and validate passes.
- 2026-10-26: step-7 approval: m008-ci-verify approved for merge
- 2026-10-26: step 8: PR #8 marked ready and its body given the `Candidate row:` line; merge marker written; the CI wait on c650248 (run 40322532367) passed the 590 s ceiling with the check still pending, so the watcher was stopped and the review stopped before the merge. This line is committed locally only, so the PR head stays c650248.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->

Pass 1, 2026-10-26, at 51efbde (main at 2a92353, unmoved since the cut). Resume route (d): PR #8 open as a draft, no box ticked.

- AC1: `.github/workflows/verify.yml` read at 51efbde: `on:` holds `pull_request` (branches main), `push` (branches main, `paths-ignore: cairn/**`), and `workflow_dispatch`; job `verify` `runs-on: ubuntu-latest`; steps `actions/checkout@v7`, `quarto-dev/quarto-actions/setup@v2` with `version: release` and `tinytex: true`, `apt-get install` of `r-base r-cran-knitr r-cran-rmarkdown poppler-utils`, then `run: python3 tests/verify.py` (no `working-directory`, so the repository root). Pass.
- AC3: `.github/workflows/verify-prerelease.yml` read at 51efbde: `on:` holds only `schedule` (`cron: "0 6 * * 1"`, weekly) and `workflow_dispatch`, no `pull_request` or `push`; same install steps with `version: pre-release`; `run: python3 tests/verify.py`. Pass.
- AC4: run 40310746574 (pull_request, head 6fd85b1, which changed `576px` to `577px` in `tests/_snapshots/meta-string.html.txt`) read fresh: conclusion `failure`; its failed-step log holds one `FAIL meta-string.html` line; `gh run download 40310746574 -n rendered-outputs` writes `meta-string.html`. The restoring commit be641d8 ran green (run 40312839783). Pass.
- AC2: at PR #8 head c849442, `gh pr checks 8` reported `verify` passed (run 40321894448, pull_request, success); its "Run verify.py" step log holds `all 36 renders pass`, and `len(verify.RENDERS)` is 36 at that commit. `python3 tests/verify.py` on this Mac at 63a8960 exited 0 with `all 36 renders pass`, and `git diff 63a8960 c849442 -- . ':!cairn'` is empty. Commits after c849442 touch `cairn/` only; step 8 waits for green CI on the head it merges. Pass.
- Consistency gate at 51efbde: `cairn_validate` all checks passed; one version marker (`version: 0.1.0` in `_extension.yml`, untouched by the diff); `python3 tests/verify.py` exit 0, `all 36 renders pass`; changelog "none". Pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: no job timeout, and the apt step took 19 s to 12 min across runs (mirror stalls) — fix now: `timeout-minutes: 45` and `Acquire::Retries=3` in both files, fixed 63a8960
- diff-bug #2: the pre-release workflow cannot run before the merge (schedule and workflow_dispatch need the default branch) — reject, planned change: AC3 is a file check for this reason (plan audit); the close hands over a manual dispatch command
- diff-bug #3: a weekly schedule notifies only the cron line's last editor and stops after 60 idle days — reject, planned change: the user chose report-only, and that editor is the maintainer
- diff-bug #4: `cancel-in-progress: true` also cancels runs on main, so a commit there can go unchecked — fix now: cancel only for pull_request events, fixed 63a8960
- diff-bug #5: the failure artifact leaves out LaTeX `.log` files — fix now: `tests/**/*.log` added in both files, fixed 63a8960
- diff-bug #6: `ubuntu-latest` moves (now Ubuntu 26.04, R 4.5.2) — reject, planned change: AC1 names `ubuntu-latest`
- diff-bug #7: the E3 cell's Word width now comes from the fixture, not Pandoc — reject, false: E3 tests the margin warning, which stays, and other knitr cells still render unsized to docx
- diff-bug #8: no `permissions:` block — fix now: `contents: read` in both files, fixed 63a8960
- diff-bug #9: PROFILE.md omits "outside cairn/", the manual trigger, and the channel names — fix now: verify slot reworded, fixed 63a8960
- diff-bug #10: the artifact's HTML opens unstyled and takes the symlinked extension's files — reject, style: debugging aid, the files needed are present
- diff-bug #11: actions pinned to major tags, not commit hashes — reject, planned change: D-008 names the actions at major tags
- diff-bug #12: the fixture.pdf comment is in verify.yml only — fix now: copied to the pre-release file, fixed 63a8960
- blame-history #1: an unsized Word figure's size depends on the system that made the PNG (pHYs tag), recorded only in this work log — follow-up: a LESSONS line at hygiene
- blame-history #2: the candidate row "Run the fixture renders in CI" stays beside the M008 row — reject, planned change: hygiene graduates it at the merge
- blame-history #3: D-008 says the installs are D-002's and D-006's needs, but rmarkdown is named by neither — reject, false: Quarto's knitr engine needs rmarkdown, so it is part of D-002's "R with knitr"
- blame-history #4: DESIGN.md says CI runs "on each pull request" and omits pushes and manual runs — reject, false: the sentence is true and does not claim to list every trigger
- prior-review: no finding (archived Review sections of M001–M007 read; no PR review comments)
- ripple #1: `cairn/references/wrap-mechanisms.md:178` says CI runs both channels, implying both gate changes — fix now: line corrected in place, fixed 63a8960
- ripple #2: the candidate row stays open — reject, planned change: same as blame-history #2
- ripple #3: README says "tested with Quarto 1.10.19" — reject, false: a dated record that still holds
- ripple #4: `tests/verify.py:44` and `:306` give only the brew install hint — fix now: apt form added, fixed 63a8960
- conversation: PR #8 — empty (0 reviews, 0 comments, 0 review threads)
- Fix-now re-check after 63a8960: local `python3 tests/verify.py` exit 0, `all 36 renders pass`; `cairn_validate` all checks passed.
