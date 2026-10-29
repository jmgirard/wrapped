# M029: Carry fig-alt to Word alt text

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the alt text in users' Word documents
- **Branch/PR:** —

## Goal

In Word output, each captioned figure that the extension puts in a Word frame has its `fig-alt` text as its image's alt text.

## Scope

**In:** In `_extensions/wrapped/wrapped-docx.lua`, when the post-render pass frames a figure, each image in the frame whose `alt` attribute or `fig-alt` attribute is set takes that text as its description, which Pandoc writes as the image's alt text (`descr` of `wp:docPr`). Quarto sets `alt` on the image of a float from the float's `fig-alt`, and a captioned image with no id keeps its own `fig-alt` (scratch render with a dump filter at post-render, 2026-10-29). The forms covered: a markdown image float, a div float, a float with the wrap class on its inner image, a captioned image with no id, and a knitr code cell with `#| fig-alt:`. A new fixture `tests/docx-alt.qmd` rendered to docx, its snapshot, and the `tests/verify.py` entry and summary lines it needs. The sentence on alt text in `docs/formats/word.qmd`.

**Out:**
- Figures with no wrap class, and wrapped figures that keep a normal figure in Word with a warning, keep the alt text Quarto gives them. The user chose at this plan's question set that the filter changes wrapped figures only (D-017).
- HTML, PDF through LaTeX, and PDF through Typst: unchanged.
- Changelog: none (`cairn/PROFILE.md` changelog slot).

## Acceptance criteria

- [ ] AC1: In the docx render of `tests/docx-alt.qmd`, each framed figure that sets `fig-alt` (a markdown image float, a div float, a float with the wrap class on its inner image, a captioned image with no id, and a knitr code cell with `#| fig-alt:`) has its `fig-alt` text as its image's `descr` in `word/document.xml`, as its frame line in `tests/_snapshots/docx-alt.docx.txt` records.
- [ ] AC2: In the same render, a framed float with no `fig-alt` has an empty `descr`, a framed captioned image with no id and no `fig-alt` has its caption text as its `descr`, and an uncaptioned wrapped image with `fig-alt` has that text, as the snapshot records.
- [ ] AC3: In the same render, a float with no wrap class and a captioned image with no id and no wrap class, each with `fig-alt`, have the same `descr` as in a render of the fixture with the filter removed from its `filters:` (empty for the float, the caption for the image), as the snapshot records.
- [ ] AC4: `python3 tests/verify.py` exits 0, and `git diff main --stat -- tests/_snapshots` lists only `tests/_snapshots/docx-alt.docx.txt`.
- [ ] AC5: `docs/formats/word.qmd` says that a wrapped figure in a Word frame, captioned or not, has its `fig-alt` text as its alt text, and that a figure the extension does not wrap keeps the alt text Quarto gives it; `quarto render docs` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2
- AC5 → T3

## Tasks

- [ ] T1: Write `tests/docx-alt.qmd` with the five framed forms of AC1, the three framed cases of AC2, and the two unwrapped figures of AC3, each followed by a paragraph. Add `("docx-alt", "docx", True)` to the fixture list in `tests/verify.py` (about line 82). In `docx_summary` (`tests/verify.py:1402`), add a section that lists each image outside a frame with its `descr`, for fixtures named in a new set, as `MARGIN_IDS` does for HTML, so other snapshots stay as they are. Render on the unchanged filter and confirm that the five AC1 lines show `alt=''`. Render a copy with `filters:` removed and confirm the AC3 baseline.
- [ ] T2: In `wrapped-docx.lua`, in `frame_blocks` or the `Image` walk it runs, set each framed image's caption to the text of its `alt` attribute, else its `fig-alt` attribute, when one is set. Write the snapshot from the fixed render and read that the AC1, AC2, and AC3 lines match. Run `python3 tests/verify.py`.
- [ ] T3: Rewrite the alt-text sentence at `docs/formats/word.qmd:8` from the T2 render. Run `quarto render docs`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: idea vet: gap — which figures get the fix: Quarto drops `fig-alt` in Word for every captioned figure; the question set chose wrapped figures only; gap — a wrapped figure that keeps a normal figure in Word: reading taken, it is a normal figure and keeps Quarto's alt text, as DESIGN.md's goals call it a normal figure.
- 2026-10-29: question set: what to work on — "Carry fig-alt to Word alt text"; which figures — wrapped figures only.
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render; 2026-10-27 (M013) dump filter after `wrapped`; 2026-10-27 (M015) render with `filters:` removed for Quarto's own output.
- 2026-10-29: collision check: absorbs the candidate row "Carry fig-alt to Word alt text" in full (its figures outside a frame dropped at the user's answer, D-017); no D-entry or archived milestone covers alt text; inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-29: plan gate chose setting the image caption in the post-render pass over carrying `fig-alt` in a `data-` attribute from the pre-quarto pass, because the image still holds `alt` or `fig-alt` at post-render in all five forms; falsified by a framed form whose image holds neither at post-render.
- 2026-10-29: checkpoint: plan committed while the full criteria audit (fresh Opus reader) runs; its findings and dispositions follow in a later line.
