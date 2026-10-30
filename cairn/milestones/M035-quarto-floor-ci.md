<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M035: Test the lowest admitted Quarto in CI

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the lowest Quarto version users can install with, and the install text in README and the site, change
- **Branch/PR:** m035-quarto-floor-ci

## Goal

CI runs `tests/verify.py` on the Quarto version that `quarto-required` names, so the floor the extension states is one the tests pass on.

## Scope

**In:** Local runs of `python3 tests/verify.py` on the stable Quarto releases from 1.9.36 to 1.10.19, as `gh api repos/quarto-dev/quarto-cli/releases` lists them (read 2026-10-30: 1.9.36, 1.9.37, 1.9.38, 1.10.18, 1.10.19), each from its macOS archive unpacked in the session scratch folder. The floor F stays 1.9.36 if the suite passes there. Otherwise F is the lowest release in that list on which the suite passes, and `quarto-required` rises to it (granted at the question set; a D-entry records the re-pin). `.github/workflows/verify.yml` runs its job on both the release channel and F. The install text in `README.md`, `docs/index.qmd`, and `docs/get-started.qmd`, DESIGN.md's Quarto version paragraph, and PROFILE.md's verify slot. Absorbs the candidate row "Test the minimum Quarto version in CI".

**Out:** Changing the filter so a release below F passes (the user chose raising the floor). Releases between F and the release channel get no CI run. `verify-prerelease.yml` and `docs.yml` keep their channels. The `_extension.yml` version, which rises at release (CLAUDE.md).

## Acceptance criteria

- [ ] AC1: `quarto-required` in `_extensions/wrapped/_extension.yml` reads `">=F"`, where F is a release of the Scope list on which `python3 tests/verify.py` exits 0 on this Mac and in the PR's CI run under F. Each release of that list below F exits 1 under the same command on this Mac or in CI, with a FAIL line or a Python traceback that the command does not print under Quarto 1.10.19.
- [ ] AC2: `.github/workflows/verify.yml` runs `python3 tests/verify.py` under Quarto's release channel and under Quarto F (quarto-actions/setup `version:`), on the triggers it has on `main` today, and both runs pass on the PR head. If the CI run fails under a release that passed on this Mac, F rises to the next release of the list, and AC1 and AC3 read that F.
- [ ] AC3: `README.md`, `docs/index.qmd`, and `docs/get-started.qmd` each say that the extension asks for Quarto F or later and is tested with Quarto F and Quarto's current release. DESIGN.md's Quarto version paragraph names F and the CI run on it, and says that releases between F and the release channel get no CI run. PROFILE.md's verify slot names both CI runs. `quarto render docs` exits 0.
- [ ] AC4: `python3 tests/verify.py` passes on the review head under Quarto 1.10.19.

## Coverage

- AC1 → T1, T2, T5
- AC2 → T3, T5
- AC3 → T4
- AC4 → T5

## Tasks

- [x] T1: Download `quarto-<v>-macos.tar.gz` for 1.9.36, then each later release of the Scope list as needed, from the quarto-cli GitHub releases into the session scratch folder, and unpack each in its own folder. Run `python3 tests/verify.py` with that release's `bin` first on `PATH`, after `quarto --version` confirms it. Go up the list from 1.9.36 and stop at the first release that passes, so every release below it has a failing run. Log one work-log line per run: the release, the exit status, and for a failure its first FAIL line or traceback and whether Quarto's output or the filter caused it.
- [x] T2: If F is not 1.9.36, set `quarto-required: ">=F"` and append a D-entry for the re-pin, citing the T1 work-log lines for the failing release.
- [x] T3: Turn the `verify` job of `.github/workflows/verify.yml` into a matrix over `release` and F with `fail-fast: false`, pass the entry to quarto-actions/setup `version:`, and name the uploaded artifact per entry, since two runs cannot upload one artifact name. Update the file's header comment.
- [ ] T4: Edit the install sentence in `README.md`, `docs/index.qmd`, and `docs/get-started.qmd`, DESIGN.md's Quarto version paragraph (and its Conventions line on the test command), and PROFILE.md's verify slot. `docs/get-started.qmd` has an R cell, so render it locally with R and commit its `docs/_freeze/` change. Run `quarto render docs`.
- [ ] T5: Run `python3 tests/verify.py` under Quarto 1.10.19. At review, read both matrix runs on the PR. If the F run fails on Ubuntu, log its first FAIL line or traceback, raise F to the next release of the list, and repeat T2 to T4 for it.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: not run — work named at the question set.
- 2026-10-30: question set: what to work on — all three normal-priority candidate rows, one milestone each, in the order M035, M036, M037; this one absorbs "Test the minimum Quarto version in CI".
- 2026-10-30: question set: if 1.9.36 fails the tests — raise `quarto-required` to the lowest release where the full suite passes, pin the CI run to it, and update README and the docs.
- 2026-10-30: question set: downloading Quarto release archives from github.com/quarto-dev into the session scratch folder for local runs — granted.
- 2026-10-30: idea vet: one gap, the outcome if 1.9.36 fails (fix the filter or raise the floor); the user chose raising the floor. The reading taken: "passes" means the full `tests/verify.py` with the current snapshots, so a Quarto output change that alters a snapshot counts as a failure. No flaw.
- 2026-10-30: lessons used: 2026-10-28 (M023), 2026-10-28 (M026), 2026-10-27 (M012).
- 2026-10-30: collision check: candidate row "Test the minimum Quarto version in CI" absorbed; M008 (done) built `verify.yml` and left this out; D-008 and D-009 name the CI tools, and a second Quarto version adds none; no D-entry on the floor. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-30: plan gate chose a matrix over release and F in the one `verify` job over a second job with copied steps, because the steps are the same and `main` has no branch protection that requires the `verify` check name; falsified by a floor run that needs steps the release run does not.
- 2026-10-30: plan gate chose running the floor on every pull request and push to `main` over a weekly run like `verify-prerelease.yml`, because a merge could break the floor unseen until the next weekly run while users install from `main`; falsified by CI time on pull requests becoming a cost the user names.
- 2026-10-30: criteria audit (full, fresh Opus reader; it ran after the plan commit 2244665, since a stop hook required a commit while the reader was still running): 5 findings, all fixed. AC1 now requires every listed release below F to fail, not only the one just below, and counts a traceback as a failure as well as a FAIL line. AC1 and AC2 require F to pass in CI as well as on the Mac, and F rises if Ubuntu fails (T5). AC3 now requires DESIGN.md to say that releases between F and the release channel get no CI run, and requires PROFILE.md's verify slot to name both runs. AC4: no finding.
- 2026-10-30: plan gate chose letting F rise at review when Ubuntu fails over a `workflow_dispatch` run of the branch before review, because pushing the branch before review is an outward step that the question set did not grant; falsified by a review that needs more than two pushes to settle F.
- 2026-10-30: T1: Quarto 1.9.36 (macOS arm64 archive, `quarto --version` 1.9.36, `tests/fixture.html` generator `quarto-1.9.36`): `python3 tests/verify.py` exit 0, "all 105 renders pass", no FAIL line. F is 1.9.36 on this Mac; no later release needed a run.
- 2026-10-30: T2: F is 1.9.36, so `quarto-required` stays `">=1.9.36"` and there is no re-pin and no D-entry.
- 2026-10-30: T3: `verify.yml`'s `verify` job is a matrix over `quarto: [release, 1.9.36]` with `fail-fast: false`, passed to quarto-actions/setup `version:`; the artifact is `rendered-outputs-<entry>`; the header comment names both runs. `verify-prerelease.yml` keeps its one `rendered-outputs` artifact. Parsed with Ruby's YAML.
