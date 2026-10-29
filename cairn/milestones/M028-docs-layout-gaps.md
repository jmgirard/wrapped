<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M028: Close gaps in the docs layout checks

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M027   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — checks over the docs site that no user of the extension relies on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The docs layout checks fail on three planted page faults that pass them at M027.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Three fixes from the M026 review. In `tests/docs_layout.py`, `blocks()` splits paragraphs at 1.25 line pitches only, so two paragraphs with a smaller gap read as one (diff-bug #3). `check()` takes a caption into the figure only within 40 px below and 30 px beside its image (diff-bug #4). In `tests/layout.js`, `straddle()` finds the paragraph above by its words and does not check that it is the last block before the figure (diff-bug #6). `paragraphLines()` also joins rects whose tops are within 3 px. It changes to join a rect whose middle is inside a line's box, as `lines()` does in the PDF reader.

**Out:** CI for the checks is M027. The Word check in CI stays out, as M027 states.

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

- [ ] AC1: Plant 1 is a scratch copy of `docs/` in which `examples/image-figure.qmd` sets `indent: true` for LaTeX and its straddle paragraph is split in two at the first line below the figure. On its LaTeX PDF, `python3 tests/docs_layout.py --site <copy>` prints a `FAIL` line for `examples/image-figure latex figure 1` with "no paragraph runs from beside the figure to below it". The script at M027's merge commit prints `ok` there. Evidence: both runs.
- [ ] AC2: Plant 2 is a scratch copy of `docs/` in which the LaTeX caption of `examples/image-figure.qmd` sits 60 px or more below its image. On its LaTeX PDF, `--debug` lists no caption line among the page's blocks, and the figure's line prints `ok`. The script at M027's merge commit lists a caption line there. Evidence: both runs.
- [ ] AC3: Plant 3 is a site copy in which a one-line paragraph is put between the paragraph above and the figure in `examples/image-figure.html`. `--html` prints a `FAIL` line for `examples/image-figure` and exits with status 1. The script at M027's merge commit prints `ok` there. Evidence: both runs.
- [ ] AC4: On the Mac, after `quarto render docs` at the review head, `python3 tests/docs_layout.py` prints an `ok` line for each figure of each page in `CASES` outside `HTML_ONLY` for `latex`, `typst`, and `word`, and `--html` prints an `ok` line for each figure of each page in `CASES`. Evidence: two local runs.
- [ ] AC5: The docs workflow's render job passes on this milestone's pull request. Evidence: the PR run.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T4
- AC2 → T2, T4
- AC3 → T3, T4
- AC4 → T1, T2, T3, T4
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Build plant 1 and see it pass the M027 script. Change `blocks()` in `tests/docs_layout.py` so that a paragraph also ends where the next line starts with an indent or where the gap passes the page's line pitch by more than a small tolerance. Choose the rule from the measured gaps of the docs pages in all three PDFs.
- [ ] T2: Build plant 2 and see the caption line in `--debug`. Change the caption rule in `check()` so that a caption is found by its place under the image and its font or lead word, not by the 40 px and 30 px limits.
- [ ] T3: Build plant 3 and see it pass. In `straddle()` in `tests/layout.js`, fail when any block (paragraph, heading, code block, or list) sits between the paragraph above and the figure. Change `paragraphLines()` to the middle-inside-box join.
- [ ] T4: Run the three plants against the M027 script and the new one, and record which line each run prints. Run AC4's local checks. Update the docstrings of both files and the header of `tests/layout.js` where the rules changed. Run `python3 tests/verify.py`.

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

- 2026-10-29: created by /milestone-plan, split from the M027 plan (candidate row "Run the docs layout checks in CI").
- 2026-10-29: tier check: milestone — named with M027's request, a CI workflow change with design choices.
- 2026-10-29: idea vet: no concern for this part. The user chose at the question set to fix the weak spots; the question listed the paragraph split, the caption reach, and the straddle() order.
- 2026-10-29: question set: fix the weak spots of the checkers — yes.
- 2026-10-29: plan chose planted page faults as the proof of each fix, over a unit test file for the readers, because the readers' input is a rendered PDF or page and M026 also proved its checks by plants; falsified by a fault that no page plant can reach.
- 2026-10-29: lessons used: 2026-10-28 (M026) LibreOffice text and frozen pages, 2026-10-28 (M025) pdftohtml splits sentences, 2026-10-26 (M007) pdftohtml image files, 2026-10-28 (M020) browser viewport.

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
