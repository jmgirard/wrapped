<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M008: Run the fixture renders in CI

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — CI over the repo's own fixture tests, which no user of the extension runs or relies on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: `.github/workflows/verify.yml` runs `python3 tests/verify.py` from the repository root on an `ubuntu-latest` runner, after installing Quarto from its release channel with TinyTeX, R with the knitr and rmarkdown packages, and poppler's command-line tools. It runs on pull requests to `main`, on pushes to `main` that change a path outside `cairn/`, and by hand (`workflow_dispatch`).
- [ ] AC2: On the milestone PR's last head commit, `gh pr checks` reports the `verify.yml` job as passed and the log of its `python3 tests/verify.py` step ends with `all <n> renders pass`, where n is the length of `RENDERS` in `tests/verify.py` at that commit; `python3 tests/verify.py` also exits 0 on this Mac at that commit.
- [ ] AC3: `.github/workflows/verify-prerelease.yml` runs the same command after installing Quarto from its pre-release channel, on a weekly schedule and by hand, and has no `pull_request` or `push` trigger, so its result is not among a pull request's checks.
- [ ] AC4: A commit pushed to the draft PR that changes one line of `tests/_snapshots/meta-string.html.txt` makes the `verify.yml` job fail, the log of its verify step has the line `FAIL meta-string.html`, and the failed run has an artifact that holds `tests/meta-string.html`, as `gh run download` lists.

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

- [ ] T1: Write `.github/workflows/verify.yml`: `actions/checkout`,
      `quarto-dev/quarto-actions/setup` with `version: release` and
      `tinytex: true`, `apt-get install` of `r-base`, `r-cran-knitr`,
      `r-cran-rmarkdown`, and `poppler-utils`, then `python3 tests/verify.py`.
      On failure, `actions/upload-artifact` keeps the `.html`, `.pdf`,
      `.tex`, `.typ`, and `.docx` files under `tests/` (the `fixture.pdf`
      left is Typst's, per LESSONS 2026-10-25 M004). Triggers as AC1, with
      `paths-ignore: cairn/**` on the push trigger only.
- [ ] T2: Write `.github/workflows/verify-prerelease.yml` with the same
      steps and `version: pre-release`, triggered by `schedule` (weekly) and
      `workflow_dispatch`. A shared reusable workflow is allowed if it keeps
      both files short.
- [ ] T3: Run `python3 tests/verify.py` on this Mac, commit, push the
      `m008-ci-verify` branch, and open a draft PR (`gh pr create --draft`);
      record its URL in the Branch/PR header. Watch the check. Fix each
      Linux-only failure in the workflow or in `tests/verify.py` so the same
      snapshots pass on both systems, never by writing a Linux-only
      snapshot; log each fix and rerun on this Mac.
- [ ] T4: Prove the check can fail: push a commit that changes one line of
      `tests/_snapshots/meta-string.html.txt`, confirm the failed run, its `FAIL` line, and the
      artifact (`gh run download`), then push a commit that restores the
      line and see the check pass again.
- [ ] T5: Update `cairn/PROFILE.md` (the verify slot names both workflows
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

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
