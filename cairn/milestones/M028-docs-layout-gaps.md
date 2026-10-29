<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M028: Close gaps in the docs layout checks

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M027   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — checks over the docs site that no user of the extension relies on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m028-docs-layout-gaps   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The docs layout checks give the right result on three planted page faults that they misread at M027.

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

- [ ] AC1: Plant 1 is a scratch copy of `docs/` in which `examples/image-figure.qmd` sets `indent: true` for LaTeX and its straddle paragraph is split in two at the first line below the figure. On its LaTeX PDF, `python3 tests/docs_layout.py --site <copy>/_site` prints a `FAIL` line for `examples/image-figure latex figure 1` with "no paragraph runs from beside the figure to below it" and without "no paragraph above the figure on its page". Evidence: this run, and the same command with the script at M027's merge commit, which prints "no paragraph above the figure on its page" in place of "no paragraph runs from beside the figure to below it".
- [ ] AC2: Plant 2 is a scratch copy of `docs/` in which the LaTeX caption of `examples/image-figure.qmd` sits 60 px or more below its image. On its LaTeX PDF, with `--site <copy>/_site --debug`, the figure box that the script prints has a `bottom` at or below the caption's last line, and the figure's line prints `ok`. Evidence: this run, and the same command with the script at M027's merge commit, whose figure box ends above the caption.
- [ ] AC3: Plant 3 is a site copy in which a one-line paragraph is put between the paragraph above and the figure in `examples/image-figure.html`. `--html` prints a `FAIL` line for `examples/image-figure` and exits with status 1. Evidence: this run, and the same command with the script at M027's merge commit, which prints `ok`.
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

- [x] T1: Build plant 1 and see it pass the M027 script. Change `blocks()` in `tests/docs_layout.py` so that a paragraph also ends where the next line starts with an indent or where the gap passes the page's line pitch by more than a small tolerance. Choose the rule from the measured gaps of the docs pages in all three PDFs.
- [x] T2: Build plant 2 and see the caption line in `--debug`. Change the caption rule in `check()` so that a caption is found by its place under the image and its font or lead word, not by the 40 px and 30 px limits.
- [x] T3: Build plant 3 and see it pass. In `straddle()` in `tests/layout.js`, fail when any block (paragraph, heading, code block, or list) sits between the paragraph above and the figure. Change `paragraphLines()` to the middle-inside-box join.
- [x] T4: Run the three plants against the M027 script and the new one, and record which line each run prints. Run AC4's local checks. Update the docstrings of both files and the header of `tests/layout.js` where the rules changed. Run `python3 tests/verify.py`.

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
- 2026-10-29: criteria audit (reduced mode): AC1, AC2, and AC3 each bound a property of the M027 script, which is the control, so that clause moved to Evidence; AC2's "no caption line among the blocks" read the debug printout, narrowed to the figure box's bottom; the Goal said all three plants fail, but AC2 expects `ok`, so the Goal now says the checks give the right result; `--site` takes the copy's `_site` folder. No finding on AC4 or AC5.
- 2026-10-29: M027 review moved the `paragraphLines()` middle-inside-box join into M027 to fix its red HTML check in CI, so that part of Scope In and T3 is done at M027's merge; the rest of T3 (the block between the paragraph above and the figure) stays here.
- 2026-10-29: lessons used: 2026-10-28 (M026) LibreOffice text and frozen pages, 2026-10-28 (M025) pdftohtml splits sentences, 2026-10-26 (M007) pdftohtml image files, 2026-10-28 (M020) browser viewport.
- 2026-10-29: implement started on branch m028-docs-layout-gaps, cut from main at ee47ef1. Plants live in the session scratchpad; the M027 scripts for the controls are `git show 45f7705:tests/docs_layout.py` and `:tests/layout.js`.
- 2026-10-29: Playwright for Python was not on the Mac, so `--html` runs use 1.64.0 (the docs workflow's pin, D-016) in a scratch venv outside the repo; no repo dependency change.
- 2026-10-29: T1: with `indent: true`, LaTeX indents a first line 17 px and adds no paragraph gap, so the M027 script reads the paragraph above and both halves as one block and prints `FAIL: no paragraph above the figure on its page`, not `ok`; AC1's control clause needs an amendment.
- 2026-10-29: T1: chose the split rule from `--debug` on the docs pages: lines of one paragraph sit within 1 px of the pitch in all three PDFs, paragraphs 8 px or more past it, so a block ends past pitch + TOL (2 px); a 3 pt parskip page (gap pitch + 4 px) would merge at pitch + 4.
- 2026-10-29: T1: chose to read indents in LaTeX and Typst only: LibreOffice PDFs lose letters at a line's start ("roups"), which moved Word lines right by 9 to 17 px on div-figure and width-gap, as large as LaTeX's indent.
- 2026-10-29: T1: new script on plant 1 prints only "no paragraph runs from beside the figure to below it"; the indented page without the split and the 3 pt parskip page print `ok`; the real site prints `ok` for all 24 PDF figures with the same blocks as M027.
- 2026-10-29: T2: plant 2 sets `\abovecaptionskip` to 45pt, so the caption sits 64 px under the image; M027's box ends at 781, above the caption (845 to 867). New `caption()`: the nearest text under the image with its middle in the image's span, opening with "Figure" or in a non-body font, then lines in its font within 1.5 heights, never an element that continues body text on its left. Plant 2's box ends at 867, `ok`.
- 2026-10-29: T2: the old 40 px reach took the body text ", as it does for any figure in Quarto." into plant 1's figure box (bottom 828), which made plant 1 read `ok`; on the real site the new rule shrinks two Word boxes that held body text (image-figure 676 to 617, uncaptioned-image 518 to 486), all `ok`.
- 2026-10-29: T3: plant 3 puts `<p>A planted line.</p>` before the figure in a copy of `_site`; M027 `--html` prints `ok` and exits 0. `straddle()` now fails when a p, heading, pre, list, dl, blockquote, table, or hr sits between the paragraph above and the figure, outside the figure's own `.cell`; plant 3 prints `FAIL: a p sits between the paragraph above and the figure` and exits 1, and the real site prints `ok` for all 9 figures, code-cell included.
- 2026-10-29: re-audit: AC1 (reduced) — bounded-promise and instrument: the Evidence clause's "reads the page's paragraphs as one block" stated the control's mechanism, wider than the run shows, so it dropped to what the run prints; proportionality: nothing.
- 2026-10-29: re-audit: AC1 (reduced) — bounded-promise and proportionality: nothing; instrument: the Evidence clause states the control's output, a minor finding either way; answered and kept, since the T1 run observed that output and AC2 and AC3 record their controls the same way.
- 2026-10-29: substantive amendment: AC1's M027 control prints "no paragraph above the figure on its page", not `ok`, so the Evidence clause names that output, and the new run must not print it. Wording only; the deliverable is unchanged, so no stop.
- 2026-10-29: T4: plant runs, new script then M027 script: plant 1 LaTeX `FAIL: no paragraph runs from beside the figure to below it`, then `FAIL: no paragraph above the figure on its page`; plant 2 `--debug` box bottom 867 and `ok`, then bottom 781 and `ok` (caption 845 to 867); plant 3 `--html` `FAIL: a p sits between the paragraph above and the figure` with exit 1, then `ok` with exit 0.
- 2026-10-29: T4: `python3 tests/verify.py` passes all 103 renders; after `quarto render docs` at 2a78a35, `tests/docs_layout.py` prints `ok` for all 24 LaTeX, Typst, and Word figures and `--html` for all 9 figures, both exit 0. Docstrings of both files and the `straddle()` comment name the new rules.
- 2026-10-29: claim audit: not owed — internal tier.

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
