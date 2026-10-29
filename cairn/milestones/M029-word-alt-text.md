# M029: Carry fig-alt to Word alt text

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the alt text in users' Word documents
- **Branch/PR:** m029-word-alt-text

## Goal

In Word output, each captioned figure that the extension puts in a Word frame has its `fig-alt` text as its image's alt text.

## Scope

**In:** In `_extensions/wrapped/wrapped-docx.lua`, when the post-render pass frames a figure, each image in the frame whose `alt` attribute or `fig-alt` attribute is set takes that text as its description, which Pandoc writes as the image's alt text (`descr` of `wp:docPr`). Quarto sets `alt` on the image of a float from the float's `fig-alt`, and a captioned image with no id keeps its own `fig-alt` (scratch render with a dump filter at post-render, 2026-10-29). The forms covered: a markdown image float, a div float, a float with the wrap class on its inner image, a captioned image with no id, and a knitr code cell with `#| fig-alt:`. A new fixture `tests/docx-alt.qmd` rendered to docx, its snapshot, and the `tests/verify.py` entry and summary lines it needs. The sentence on alt text in `docs/formats/word.qmd`.

**Out:**
- Figures with no wrap class, and wrapped figures that keep a normal figure in Word with a warning, keep the alt text Quarto gives them. The user chose at this plan's question set that the filter changes wrapped figures only (D-017).
- HTML, PDF through LaTeX, and PDF through Typst: unchanged.
- Changelog: none (`cairn/PROFILE.md` changelog slot).

## Acceptance criteria

- [ ] AC1: In the docx render of `tests/docx-alt.qmd`, each of these framed figures has its `fig-alt` text as its image's `descr` in `word/document.xml`: a markdown image float, a div float with `fig-alt` on the div, a float div with the wrap class and `fig-alt` on its inner image, a captioned image with no id, a captioned image with a non-`fig-` id, and a knitr code cell with `#| fig-alt:`. Each `fig-alt` text in the fixture is unique and differs from every caption.
- [ ] AC2: In the same render, a framed markdown float with no `fig-alt` has an empty `descr`; a framed knitr cell with no `fig-alt` has the `descr` that T1's dump predicts (the text of its image's `alt` attribute at post-render, else empty); a framed captioned image with no id and no `fig-alt` has its caption text; and an uncaptioned wrapped image with `fig-alt` has that text.
- [ ] AC3: In the same render, a float with no wrap class and a captioned image with no id and no wrap class, each with `fig-alt`, and a wrapped float with `fig-alt` in a callout, which warns and stays out of a frame, have the `descr` that T1 recorded from a render of the fixture with `filters:` removed.
- [ ] AC4: `python3 tests/verify.py` exits 0, and at the branch tip `git diff main...HEAD --stat -- tests/_snapshots` lists only `tests/_snapshots/docx-alt.docx.txt`.
- [ ] AC5: `docs/formats/word.qmd` says that a wrapped figure in a Word frame, captioned or not, has its `fig-alt` text as its alt text, and that a figure with no wrap class, or a wrapped figure that keeps a normal figure in Word, keeps the alt text Quarto gives it; `quarto render docs` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2
- AC5 → T3

## Tasks

- [x] T1: Write `tests/docx-alt.qmd` with the six framed forms of AC1, the four framed cases of AC2, and the three unframed figures of AC3, each followed by a paragraph. Add `("docx-alt", "docx", True)` to the fixture list in `tests/verify.py` (about line 82). In `docx_summary` (`tests/verify.py:1402`), add a section that lists each image outside a frame with its `descr`, for fixtures named in a new set, as `MARGIN_IDS` does for HTML, so other snapshots stay as they are. Render on the unchanged filter and confirm that the four AC1 float and cell forms show `alt=''` and the two captioned images show their captions. Dump the knitr cell's image attributes at post-render for AC2. Render a copy with `filters:` removed and write each AC3 figure's `descr` in a work-log line.
- [x] T2: In `wrapped-docx.lua`, in `frame_blocks` or the `Image` walk it runs, set each framed image's caption to the text of its `alt` attribute, else its `fig-alt` attribute, when one is set. Write the snapshot from the fixed render and read that the AC1, AC2, and AC3 lines match. Run `python3 tests/verify.py`.
- [x] T3: Rewrite the alt-text sentence at `docs/formats/word.qmd:8` from the T2 render. Run `quarto render docs`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: idea vet: gap — which figures get the fix: Quarto drops `fig-alt` in Word for every captioned figure; the question set chose wrapped figures only; gap — a wrapped figure that keeps a normal figure in Word: reading taken, it is a normal figure and keeps Quarto's alt text, as DESIGN.md's goals call it a normal figure.
- 2026-10-29: question set: what to work on — "Carry fig-alt to Word alt text"; which figures — wrapped figures only.
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render; 2026-10-27 (M013) dump filter after `wrapped`; 2026-10-27 (M015) render with `filters:` removed for Quarto's own output.
- 2026-10-29: collision check: absorbs the candidate row "Carry fig-alt to Word alt text" in full (its figures outside a frame dropped at the user's answer, D-017); no D-entry or archived milestone covers alt text; inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-29: plan gate chose setting the image caption in the post-render pass over carrying `fig-alt` in a `data-` attribute from the pre-quarto pass, because the image still holds `alt` or `fig-alt` at post-render in all five forms; falsified by a framed form whose image holds neither at post-render.
- 2026-10-29: checkpoint: plan committed while the full criteria audit (fresh Opus reader) runs; its findings and dispositions follow in a later line.
- 2026-10-29: criteria audit (full mode, fresh Opus reader) returned 9 findings, all fixed: AC1 drops the circular snapshot clause and requires unique `fig-alt` texts that differ from captions; AC1 names where `fig-alt` sits on the inner-image form and adds a captioned image with a non-`fig-` id; AC2 adds a knitr cell with no `fig-alt`; AC3 compares to T1's recorded unfiltered baseline and adds a wrapped float in a callout that falls back; AC4 diffs `main...HEAD`; AC5 names fallback figures; T1's pre-fix check now expects captions on the two captioned images; D-017 was written at plan time (e1ff7b8); finding 9 (proportion) needed no change.
- 2026-10-29: implement started on branch m029-word-alt-text, cut from main at 84c71b8.
- 2026-10-29: T1 done: `tests/docx-alt.qmd` and the `DOCX_UNFRAMED_ALT` section of `docx_summary`; on the unchanged filter the markdown, div, inner-image, and cell floats show `alt=''` and the two captioned images show their captions; the full `verify` run waits for T2, which writes the fixture's snapshot.
- 2026-10-29: T1 AC2 dump: the framed knitr cell with no `fig-alt` has no `alt` attribute at post-render, so its `descr` stays empty.
- 2026-10-29: T1 AC3 baseline (render with `filters:` removed): the plain float `''`, the plain captioned image 'A captioned image with no wrap class.', the callout float `''`.
- 2026-10-29: T2 implementation choice: `alt_image` runs in `frame_para`, because `frame_blocks`'s topdown walk stops at each paragraph and never reaches its images; it reads `alt` before `fig-alt`, since a div float holds only `alt`.
- 2026-10-29: checkpoint: T2 code and snapshot and T3's `docs/formats/word.qmd` sentence written; `quarto render docs` exited 0; the full `python3 tests/verify.py` run is in progress, so T2 and T3 stay unticked.
- 2026-10-29: T2 and T3 done: `python3 tests/verify.py` passed (all 104 renders, `ok docx-alt.docx`); `git diff main...HEAD --stat -- tests/_snapshots` lists only `docx-alt.docx.txt`.
- 2026-10-29: claim audit: 15 claims read, 1 corrected — tests/docx-alt.qmd (heading "Framed figures with no fig-alt" also held the uncaptioned image with `fig-alt`; retitled), also tests/verify.py (the unframed-image section read the first `wp:docPr` of a paragraph for each image; it now reads each `w:drawing`'s own); the same reader re-read both: hold. Files read: wrapped-docx.lua, docs/formats/word.qmd, tests/verify.py, tests/docx-alt.qmd, tests/_snapshots/docx-alt.docx.txt.
- 2026-10-29: implement complete: `python3 tests/verify.py` passed at e25c3c9 (all 104 renders); status set to review.
