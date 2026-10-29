# M030: Fix the Word alt text edge cases

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the alt text in users' Word documents
- **Branch/PR:** —

## Goal

In Word output, a framed figure that holds more than one image puts its `fig-alt` text on its first image only, and every framed image's alt text keeps the repeated spaces of its `fig-alt`.

## Scope

**In:** In `_extensions/wrapped/wrapped-docx.lua`, `alt_image` (called from `frame_para` on each framed paragraph) changes in two ways. First, the `alt` attribute, which Quarto 1.10.19 copies from a float's `fig-alt` onto every image of the float (scratch render with a post-render dump filter, 2026-10-29), sets the description of the frame's first image only. An image's own `fig-alt` still sets its description wherever it sits in the frame, and a later image with neither keeps its description as it was. Second, the text goes in as one string, so repeated spaces stay (today `pandoc.Inlines(alt)` makes them one space). In `_extensions/wrapped/wrapped.lua`, `wrapped_image_docx` no longer copies `fig-alt` into an uncaptioned image's caption, since `alt_image` sets it in the frame. New cases in `tests/docx-alt.qmd` and its snapshot. The alt-text sentences in `docs/formats/word.qmd` and the `wrapped-docx.lua` paragraph of `cairn/DESIGN.md`.

**Out:**
- A wrapped image inside a link, `[![](plot.png){.wrap-left}](url)`, wraps in no format (the filter warns that it "is not a figure or the only content of its paragraph"), so it has no frame. The candidate row "Wrap images inside links in all formats" holds it (the user's answer at this plan's question set).
- Figures with no wrap class, and wrapped figures that keep a normal figure in Word, keep Quarto's alt text (D-017).
- HTML, PDF through LaTeX, and PDF through Typst: unchanged. A scratch HTML render and a Typst render on 2026-10-29 kept the repeated spaces of an uncaptioned image's `fig-alt`.
- Changelog: none (`cairn/PROFILE.md` changelog slot).

## Acceptance criteria

- [ ] AC1: In the docx render of `tests/docx-alt.qmd`, a framed div float that sets `fig-alt` and holds two images, each with no `fig-alt` and no description, has the float's `fig-alt` text as the first image's `descr` and an empty `descr` on the second image, as its frame line in `tests/_snapshots/docx-alt.docx.txt` records.
- [ ] AC2: In the same render, a framed div float that sets `fig-alt` and holds a first image with its own `fig-alt` and a second image with a description and no `fig-alt` has the first image's own `fig-alt` as its `descr` and the second image's description as its `descr`, as its frame line records.
- [ ] AC3: In the same render, a framed uncaptioned image and a framed markdown image float, each with a `fig-alt` that holds two spaces in a row, have that text with both spaces as their image's `descr`, as their frame lines record.
- [ ] AC4: `wrapped_image_docx` in `_extensions/wrapped/wrapped.lua` does not read `fig-alt`, and in the same render the existing uncaptioned image's frame line still records `alt='Alt for the uncaptioned image'`.
- [ ] AC5: `python3 tests/verify.py` exits 0, and `git diff main --stat -- tests/_snapshots` lists only `tests/_snapshots/docx-alt.docx.txt`.
- [ ] AC6: `docs/formats/word.qmd` says that in a wrapped figure with more than one image, the figure's `fig-alt` text is the alt text of its first image only, and that an image with its own `fig-alt` has that text; `quarto render docs` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2
- AC5 → T2
- AC6 → T3

## Tasks

- [ ] T1: In `tests/docx-alt.qmd`, add each case of AC1, AC2, and AC3 as a wrapped figure followed by a paragraph, with unique `fig-alt` texts. Render the one fixture on the unchanged filter (the one-fixture command in `cairn/LESSONS.md`, 2026-10-27 M012) and confirm the faults: both AC1 images and the AC2 second image show the float's text, and the AC3 lines show one space.
- [ ] T2: In `wrapped-docx.lua`, make `alt_image` set the caption to one `pandoc.Str` of the text (no inlines for an empty text), and pass it whether the image is the frame's first, so `alt` applies to the first image only. The flag is set once per frame in `frame_first`, for the figure-table path and the `.wrapped-image` path. Update the comments above `alt_image` and in the file header. In `wrapped.lua`, remove the `fig-alt` copy from `wrapped_image_docx` (about line 1553) and the sentence about it in its comment. Write the snapshot from the fixed render and read that the AC1 to AC4 lines match. Run `python3 tests/verify.py`.
- [ ] T3: Add the multi-image rule to the alt-text sentences at `docs/formats/word.qmd:8`, from the T2 render, and to the `wrapped-docx.lua` paragraph of `cairn/DESIGN.md` (about line 303). Run `quarto render docs`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: idea vet: gap — a float's `fig-alt` when the frame's first image has its own `fig-alt`: reading taken, the image's own text wins and the float's text goes on no later image, as the answer gives the second image empty alt text; gap — a later image with a description of its own: reading taken, it keeps that description, its own text; gap — repeated spaces in the LaTeX and Typst copies: reading taken, Word only, as the row names `alt_image`; no flaw (the W3C images tutorial gives a group of images one text on its first image and empty alt text on the rest).
- 2026-10-29: question set: what to work on — "Fix the Word alt text edge cases"; a framed float with two images — the float's text on the first image only; a wrapped image inside a link — its own candidate row.
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render; 2026-10-29 (M029) where Quarto puts `fig-alt` and `alt` at Word post-render.
- 2026-10-29: collision check: absorbs the candidate row "Fix the Word alt text edge cases" in part; its linked-image sentence moves to the new row "Wrap images inside links in all formats" (the user's answer). D-017 holds (framed figures only). M029 shipped the rule this changes. Inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-29: plan gate chose a first-image flag per frame in the post-render pass over marking the first image in the pre-quarto pass, because at post-render every image of a float still holds Quarto's `alt` copy and the frame's walk sees the images in document order; falsified by a framed figure whose first image in `word/document.xml` is not the first image `frame_blocks` walks.
- 2026-10-29: checkpoint: plan committed while the full criteria audit (fresh Opus reader) runs; its findings and dispositions follow in a later line.

## Decisions

## Review
