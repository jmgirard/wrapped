<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M027: Run the docs layout checks in CI

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — a CI check over the docs site that no user of the extension relies on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m027-docs-layout-ci   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The docs workflow fails when a page listed in `CASES` of `tests/docs_layout.py` loses its wrap in HTML, LaTeX, or Typst.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `tests/docs_layout.py` gets three options. `--site DIR` reads a site folder other than `docs/_site/`. `--no-word` skips the Word PDFs. `--html` runs the HTML check: it serves the site folder with `tests/layout.js`, opens each page in `CASES` in headless Chromium through Playwright for Python at a 1280x900 viewport, and runs `straddle()`. The render job of `.github/workflows/docs.yml` installs poppler and Playwright with its Chromium. After `quarto render docs`, it runs the script with `--no-word` and then with `--html`. The render job runs on every event, and the publish job gets `needs: render`. The workflow's `paths` filters add `tests/docs_layout.py` and `tests/layout.js`.

**Out:** The Word check in CI. It stays a by-hand run on the Mac, because LibreOffice on Ubuntu has other fonts (question set). Fixes to the weak spots of the checkers go to M028.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: The docs workflow runs on this milestone's pull request. Its render job runs `python3 tests/docs_layout.py --no-word` on the site that it rendered. The step's log prints an `ok` line for each figure of each page in `CASES` outside `HTML_ONLY`, for `latex` and for `typst`, and no `FAIL` line. Evidence: the log of the PR run.
- [ ] AC2: In the same run, `python3 tests/docs_layout.py --html` prints an `ok` line for each figure of each page in `CASES`, `index` included, and no `FAIL` line. Evidence: the log of the PR run.
- [ ] AC3: In a site copy where the straddle paragraph of `examples/image-figure.html` is cut to one sentence, `--html` prints a `FAIL` line that names `examples/image-figure` and exits with status 1. In a site copy with no `examples/div-figure.html`, it prints a `FAIL` line that names `examples/div-figure` and exits with status 1. Evidence: two local runs with `--site`.
- [ ] AC4: In `docs.yml` at the review head, the publish job has `needs: render`. The `if` of the render job admits a push to `main` and a manual run on `main` of jmgirard/wrapped. Evidence: a read of the file.
- [ ] AC5: On the Mac, after `quarto render docs`, `python3 tests/docs_layout.py` with no option prints an `ok` line for each figure of each page in `CASES` outside `HTML_ONLY`, for `latex`, `typst`, and `word`. Evidence: one local run at the review head.
- [ ] AC6: `python3 tests/verify.py` passes at the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T1, T2
- AC4 → T3
- AC5 → T1
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Add `--site DIR` and `--no-word` to `tests/docs_layout.py` (`SITE` at line 43, `pdf_paths` at line 82). Update the docstring. Run the plain command on the Mac to show the PDF output is unchanged.
- [x] T2: Add `--html` to `tests/docs_layout.py`. Serve the site folder and `tests/layout.js` from one temporary folder, open each page with Playwright at 1280x900, run the `straddle()` call that `--js` prints, and print one line per figure in the PDF lines' form. Exit with status 1 on any `ok: false`, on a missing page, or when Playwright is missing (a plain message). Install Playwright locally to run it.
- [x] T3: Edit `.github/workflows/docs.yml`: install `poppler-utils` with the retry options of `verify.yml`, install a pinned Playwright and its Chromium, and add the two check steps after the render step. Drop the render job's `if` and give the publish job `needs: render`. Add the two test files to both `paths` filters. Rewrite the header comment to say what the render job checks and that Word is checked by hand. Write D-016 for the new CI tools.
- [ ] T4: Update the verify and consistency-gate slots of `cairn/PROFILE.md` to name the CI check and the by-hand Word check. Run `python3 tests/verify.py`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-29: created by /milestone-plan, from the candidate row "Run the docs layout checks in CI", which M027 and M028 absorb in full.
- 2026-10-29: tier check: milestone — a CI workflow change and a new CI dependency, with design choices.
- 2026-10-29: idea vet: two concerns. The Word check reads a LibreOffice PDF whose fonts differ on Ubuntu, so it can fail on a good page (answer: CI skips Word, by hand on the Mac). A check before publish means the publish job must wait for it (answer: block merge and publish).
- 2026-10-29: question set: which PDF checks CI runs — LaTeX and Typst, Word by hand.
- 2026-10-29: question set: permission for the HTML check's CI dependency — Playwright for Python and its Chromium in CI. Poppler from Ubuntu's packages was named in the same question and accepted.
- 2026-10-29: question set: what a failed check does — block merge and publish.
- 2026-10-29: question set: fix the weak spots of the checkers — yes, split to M028.
- 2026-10-29: plan gate chose Playwright for Python over a script that drives the runner's own Chrome because a maintained driver needs less custom code; falsified by a Playwright install that fails or takes more than about 2 minutes in CI.
- 2026-10-29: plan gate chose LaTeX and Typst in CI over all three formats because LibreOffice on Ubuntu breaks lines in other places than on the Mac; falsified by a CI run where the Word check passes on all pages with no retuning.
- 2026-10-29: plan chose to run the render job on every event and gate publish with `needs: render` over adding check steps to the publish job, so the job with write access gains no install steps; falsified by a publish that runs while the render job failed.
- 2026-10-29: split: M027 puts the checks in CI, and M028 (planned now, depends on M027) fixes the weak spots, since both together pass about 9 criteria. Checker-regress shape not hit: the checkers read the published docs site, not repo-internal files.
- 2026-10-29: inbox sweep: no open issues or PRs.
- 2026-10-29: criteria audit (reduced mode), first pass on the pre-split draft: AC3 claimed every problem kind and every missing page from one plant of each, narrowed to the two named plants; Goal narrowed to pages listed in `CASES`; `--html` made an option so the plain run needs no Playwright. No finding on the other criteria. A second pass on M027 and M028 as written was still running at the plan commit, and its dispositions follow in a later commit.
- 2026-10-29: criteria audit (reduced mode), second pass on M027 as written: no finding on AC1 to AC6.
- 2026-10-29: implement started on branch m027-docs-layout-ci; the status edit went through sed, not the Edit tool.
- 2026-10-29: T1 done: `--site DIR` and `--no-word` in `tests/docs_layout.py`. After `quarto render docs`, the plain run printed 24 `ok` lines and `--no-word` 16. A missing PDF still ends in pdftohtml's traceback with a nonzero exit, as before.
- 2026-10-29: T2 done: `--html` serves the site with a stdlib HTTP server on a free port, maps `/layout.js` to `tests/layout.js`, and runs `straddle()` through Playwright's sync API. Playwright pinned at 1.64.0 (released 2026-10-13), since 1.64.1 was 7 days old; installed for local runs in a scratch venv only. Local runs: 9 `ok` lines; plant with the image-figure straddle paragraph cut to one sentence printed `FAIL: no later line below the figure that crosses it`, exit 1; plant with no div-figure.html printed `examples/div-figure html: FAIL: page missing`, exit 1; with no Playwright, a plain message and exit 1.
- 2026-10-29: T3 done: `docs.yml` render job drops its `if`, installs poppler and Playwright 1.64.0 in `$RUNNER_TEMP/venv` (system pip on Ubuntu 24.04 refuses installs), and runs `--no-word` then `--html`; the HTML step also runs after a failed PDF step. Publish has `needs: render`; both `paths` filters list the two test files; header comment rewritten. D-016 written. Parsed with PyYAML: jobs render and publish, publish needs render, render has no `if`. Not yet run in CI.
- 2026-10-29: lessons used: 2026-10-28 (M020) browser viewport, 2026-10-28 (M023) Typst output-file, 2026-10-28 (M026) LibreOffice text and frozen pages, 2026-10-26 (M007) pdftohtml image files.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
