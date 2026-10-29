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

- [x] AC1: Plant 1 is a scratch copy of `docs/` in which `examples/image-figure.qmd` sets `indent: true` for LaTeX and its straddle paragraph is split in two at the first line below the figure. On its LaTeX PDF, `python3 tests/docs_layout.py --site <copy>/_site` prints a `FAIL` line for `examples/image-figure latex figure 1` with "no paragraph runs from beside the figure to below it" and without "no paragraph above the figure on its page". Evidence: this run, and the same command with the script at M027's merge commit, which prints "no paragraph above the figure on its page" in place of "no paragraph runs from beside the figure to below it".
- [x] AC2: Plant 2 is a scratch copy of `docs/` in which the LaTeX caption of `examples/image-figure.qmd` sits 60 px or more below its image. On its LaTeX PDF, with `--site <copy>/_site --debug`, the figure box that the script prints has a `bottom` at or below the caption's last line, and the figure's line prints `ok`. Evidence: this run, and the same command with the script at M027's merge commit, whose figure box ends above the caption.
- [x] AC3: Plant 3 is a site copy in which a one-line paragraph is put between the paragraph above and the figure in `examples/image-figure.html`. `--html` prints a `FAIL` line for `examples/image-figure` and exits with status 1. Evidence: this run, and the same command with the script at M027's merge commit, which prints `ok`.
- [x] AC4: On the Mac, after `quarto render docs` at the review head, `python3 tests/docs_layout.py` prints an `ok` line for each figure of each page in `CASES` outside `HTML_ONLY` for `latex`, `typst`, and `word`, and `--html` prints an `ok` line for each figure of each page in `CASES`. Evidence: two local runs.
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
- 2026-10-29: step-7 approval: m028-docs-layout-gaps approved for merge

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

- AC1 evidence (2026-10-29, head ae38255): plant 1 (scratch copy of `docs/`, `indent: true` for LaTeX, straddle paragraph split before "their text stays", the first line under the caption's bottom at 774) — new script prints `examples/image-figure latex figure 1: FAIL: no paragraph runs from beside the figure to below it`, with no "no paragraph above"; the script at 45f7705 prints `FAIL: no paragraph above the figure on its page`.
- AC2 evidence (2026-10-29, head ae38255): plant 2 (scratch copy of `docs/`, `\abovecaptionskip` 45pt) puts the caption at 845, 64 px under the image's bottom at 781, its last line ending at 867 — new script with `--debug` prints the figure box with `bottom` 867 and `examples/image-figure latex figure 1: ok`; the script at 45f7705 prints `bottom` 781, above the caption.
- AC3 evidence (2026-10-29, head ae38255): plant 3 (copy of `docs/_site` with `<p>A planted line.</p>` before the figure in `examples/image-figure.html`) — new `--html` prints `examples/image-figure html figure 1: FAIL: a p sits between the paragraph above and the figure` and exits 1; the script at 45f7705 prints `ok` and exits 0.
- AC4 evidence (2026-10-29, head ae38255): `quarto render docs` ran at 2a78a35, and `git diff 2a78a35 ae38255 -- docs _extensions tests` is empty. `python3 tests/docs_layout.py` prints 24 `ok` lines, one per figure of the 7 non-HTML_ONLY pages in `latex`, `typst`, and `word`, no other line, exit 0; `--html` (Playwright 1.64.0, scratch venv) prints 9 `ok` lines, one per figure of the 8 pages in CASES, exit 0.
- gate: `cairn_validate.py` all checks passed; the one version marker (`_extensions/wrapped/_extension.yml`) is unchanged; `python3 tests/verify.py` passed all 103 renders on the T1-T3 code; `tests/docs_layout.py` on the Mac is AC4; the docs workflow on the PR is AC5, read at step 8. No principle changed, so no `cairn_impact` run.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: an uncaptioned left image takes a heading far below it as its caption, since `under` has no lower bound (width-gap Typst with the caption removed) — fix now, fixed 540bec7 (the caption is the first line under the image that overlaps its span; text below a figure spans it).
- diff-bug #2: `continues()` drops a right-side caption when the beside text ends within half a height of it, as a 0.5em wrap gap would place it — fix now, fixed 540bec7 (guard removed; caption found at gaps of 16, 12, 10, and 8 px in the reviewer's simulation).
- diff-bug #3: with indents read, two paragraphs merge at a left figure, since the first line below at 142 is left of the narrowed lines at 375 — fix now, fixed 540bec7 (a line is indented against the line before or after it; div-figure LaTeX with `indent: true` split below the figure now prints `FAIL: no paragraph runs from beside the figure to below it`, the code at ea0b1fb printed `ok`).
- diff-bug #4: a caption line that opens with a word in another font is cut off with the rest of the caption — fix now, fixed 540bec7 (a later line joins when any element is in the caption's font).
- diff-bug #5: a short body line within 1.5 heights under a same-font caption is absorbed — follow-up, row "Harden and test the docs layout checks" (540bec7 keeps later lines inside the first caption line's span, which excludes it on width-gap Typst, but a two-line caption at a left image's edge still takes "end." in the div-figure LaTeX simulation).
- diff-bug #6: microtype protrusion can read as an indent — fix now, fixed 540bec7 (an indent is more than a quarter of the pitch; "W" protrudes 1 px on image-figure LaTeX).
- diff-bug #7: `BLOCKS` misses a normal figure or a callout between the paragraph and the figure — fix now, fixed 540bec7 (`figure` and `.callout` added; a scratch callout before the figure prints `FAIL: a div sits between the paragraph above and the figure`).
- diff-bug #8: hidden and margin blocks give false fails — fix now, fixed 540bec7 (a block needs client rects and sits outside `.column-margin`; a scratch `display: none` paragraph before the figure prints `ok`).
- diff-bug #9: the cell exclusion skips every block of the figure's cell, but the docs said only its code — fix now, fixed 540bec7 (both comments now say the cell's blocks).
- diff-bug #10: the gap rule allows 2 px, so a tall inline item such as a fraction, or a code-heavy Word page, can split a paragraph — reject, edge: inline math and code-heavy pages are outside the docs example pages, and the effect is a FAIL line, not a silent pass.
- diff-bug #11: docstrings did not match `caption()` (same-line joins in other fonts, the `continues` guard, "its own heights") — fix now, fixed 540bec7.
- diff-bug #12: `between()` never checks that the paragraph above comes before the figure — fix now, fixed 540bec7 ("paragraph above comes after the figure").
- diff-bug #13: no tests were added — reject, planned change: the plan chose scratch plants as the proof of each fix (work log).
- blame-history #1: the span test drops a later caption line whose middle lies past the image edge, and the docstring did not say later lines are tested — fix now, fixed 540bec7 (later lines are tested against the first caption line's span, as the docstring now says).
- blame-history #2: a left wrap's first beside line reads as an indent after a full-width line — fix now, fixed 540bec7 (an indent is at most two pitches; the step to a left figure's side is over 100 px).
- blame-history #3: a body line opening with "Figure" right under an uncaptioned image would be taken as its caption — reject, edge: no docs example page has such a line, and the effect is a FAIL line.
- blame-history #4: a caption label other than "Figure" in the body font is not found — reject, edge: the docs site is English, and Quarto's label there is "Figure".
- blame-history #5: the 2 px gap rule splits lines with taller inline items — reject, edge: as diff-bug #10.
- blame-history #6: `between()` skips printed output in the figure's cell while the docs said code — fix now, fixed 540bec7 (as diff-bug #9).
- blame-history #7: a bulleted item's wrapped lines read as indented, so list items split — reject, edge: no docs example page has a list beside or right above a wrapped figure, and in HTML a list before the figure fails `between()`.
- prior-review #1: the thresholds were set on Mac renders while CI renders on Ubuntu, where M027 met a 3 px inline-code offset — reject, planned change: AC5 runs the docs render job on Ubuntu on the PR, and step 8 merges only on green.
- prior-review #2: `caption()` compares tops, the error class M027 fixed — reject, false: rows group by an element's middle (540bec7), and the remaining top tests compare caption rows with each other and with the image's bottom, not inline code with its line.
- prior-review #3: the "Figure" lead word on LibreOffice text with lost letters — reject, false: every Word caption on the docs pages reads "Figure" intact and is in an italic font apart from the body font, so the font test also finds it.
- prior-review #4: the docstring said later lines join in the first font, but same-line text in any font joined — fix now, fixed 540bec7.
- prior-review #5: no committed case for the three rules, so a regression passes `tests/verify.py` — follow-up, row "Harden and test the docs layout checks".
- prior-review #6: the dated measurement in `blocks()`'s docstring will go stale — reject, false: the derived-figures rule asks a measured figure to carry its procedure and date.
- prior-review #7: the `between()` comment did not say what is left out — fix now, fixed 540bec7.
- ripple #1: the ROADMAP row "Run the docs layout checks in CI" still lists the three weak spots — reject, planned change: post-merge hygiene graduates the row this milestone took.
- ripple #2: `.github/workflows/docs.yml` lines 8-10 do not name the last-block rule — reject, false: they name which checks run, which the diff leaves as is.
- ripple #3: `cairn/PROFILE.md` lines 33 and 39 do not name the last-block rule — reject, false: as ripple #2.
- after fixes (head 540bec7): AC1 plant 1 still prints only `FAIL: no paragraph runs from beside the figure to below it`; AC2 box `bottom` 867, `ok`; AC3 `FAIL: a p sits between the paragraph above and the figure`, exit 1; AC4 24 PDF `ok` lines with the same `--debug` boxes and blocks as at ea0b1fb, and 9 HTML `ok` lines, exit 0 each; the indented page and the 3 pt parskip page print `ok`.
- snapshot files: none changed.
- gate after fixes: `python3 tests/verify.py` passed all 103 renders at 540bec7; `cairn_validate.py` all checks passed at 27543a3.
