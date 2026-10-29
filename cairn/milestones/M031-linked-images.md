# M031: Wrap images inside links in all formats

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes how linked images render in users' documents in all four formats
- **Branch/PR:** —

## Goal

In HTML, PDF through LaTeX, PDF through Typst, and Word, an image with a wrap class that is the only content of a link, which is the only content of its paragraph, wraps and keeps its link.

## Scope

**In:** In `_extensions/wrapped/wrapped.lua`, `lone_wrapped_image` (about line 1503) also accepts a paragraph whose only inline, spaces aside, is a `Link` whose only inline, spaces aside, is an image with a wrap class. The four `wrapped_image_*` builders and the next-block rule (`no_text_blocks`) then treat that image as they treat an uncaptioned image, and the box holds the link with the image inside it. In `_extensions/wrapped/wrapped-docx.lua`, `has_image` also finds an image inside a link, so the image paragraph of a framed captioned figure whose image is linked takes the figure's paragraph style. New and changed cases in `tests/fixture.qmd` and `tests/docx-alt.qmd`, their snapshots, and summary fields in `tests/verify.py` that record a wrapped image's link target. The linked-image sentences in `docs/normal-layout.qmd`, `docs/get-started.qmd`, and the Syntax section of `cairn/DESIGN.md`.

**Out:**
- A wrap class on the link instead of the image, `[![](plot.png)](url){.wrap-left}`, wraps in no format and prints no warning (scratch renders, 2026-10-29). The new candidate row "Warn for a wrap class on a link" holds it.
- A captioned linked image, `[![Caption](plot.png){.wrap-left}](url)` with or without a `#fig-` id, already wraps in all four formats, because Quarto 1.10.19 makes it a Figure or a float (scratch renders with and without the filter, 2026-10-29). Only its Word paragraph style changes here. In PDF through LaTeX, Quarto drops the link of the no-id form with or without the filter; that is Quarto's behavior and stays.
- Linked images with other content beside the image in the link or the paragraph keep their normal layout and warning.
- Changelog: none (`cairn/PROFILE.md` changelog slot).

## Acceptance criteria

- [ ] AC1: In the HTML, PDF through LaTeX, PDF through Typst, and docx renders of `tests/fixture.qmd`, its "An image inside a link" case, a paragraph that holds only `[![](plot.png){.wrap-left width="20%" wrap-gap="2em" fig-alt="…"}](https://example.com)`, is a wrapped image: it sits in the box the filter makes for an uncaptioned image (an HTML `.wrapped-image` div, a LaTeX `wrappedfigure` with `caption=false`, a Typst `wrap-content` call, a Word frame) with the box width 20% of the text width and a 2em gap, the paragraphs after it join its group, and the render prints no "is not a figure or the only content of its paragraph" warning for it; as the four `fixture` snapshots record.
- [ ] AC2: In the same four renders, the AC1 image stays inside its link with the target `https://example.com`: an HTML `<a href>` around the `<img>`, a LaTeX `\href` around the `\includegraphics`, a Typst `#link` around the `image(` call, and a Word `w:hyperlink` around the drawing; as the four `fixture` snapshots record.
- [ ] AC3: In the PDF through LaTeX, PDF through Typst, and docx renders of `tests/fixture.qmd`, the AC1 image's alt text is its `fig-alt` text, as the `fixture.pdf`, `fixture.typst`, and `fixture.docx` snapshots record.
- [ ] AC4: In the same four renders of `tests/fixture.qmd`, each of three cases keeps a normal image, in no wrap box and with no link removed, and the render prints the "is not a figure or the only content of its paragraph" warning for its image: a link that holds a wrapped image and a word, a link that holds two wrapped images, and a paragraph with a word beside a link that holds a wrapped image; as the four `fixture` snapshots record.
- [ ] AC5: In the docx render of `tests/docx-alt.qmd`, a wrapped markdown float with a `#fig-` id and a wrapped captioned image with no id, each with its image as the only content of a link, give their image paragraph the same `w:pStyle` as the same figure with no link in that render (`Compact` for the float, `CaptionedFigure` for the no-id image), as `tests/_snapshots/docx-alt.docx.txt` records.
- [ ] AC6: `docs/normal-layout.qmd` says that an image beside other content in its paragraph or in its link does not wrap and no longer says that an image inside a link does not wrap; `docs/get-started.qmd`'s "An image with no caption" section says that an image that is the only content of a link wraps and keeps its link; `quarto render docs` exits 0.
- [ ] AC7: `python3 tests/verify.py` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T1, T2
- AC5 → T1, T3
- AC6 → T4
- AC7 → T2, T3, T5

## Tasks

- [ ] T1: Tests first. In `tests/fixture.qmd` (about line 112), give the linked case `wrap-gap="2em"` and a `fig-alt`, rewrite its sentence to say it wraps, and add the three AC4 cases, each followed by a paragraph. In `tests/docx-alt.qmd`, add the two AC5 cases and, beside them, the same two figures with no link if no case there already serves. In `tests/verify.py`, make `html_summary`, `tex_summary`, `typ_summary`, and `docx_frames` record the link target of each image in a wrap box (only where there is one, so snapshots with no linked image keep their bytes), and make `docx_frames` record the `w:pStyle` of each framed image paragraph in `docx-alt` only (as `DOCX_UNFRAMED_ALT` gates the unframed list). Render the two fixtures on the unchanged filter (the one-fixture command, `cairn/LESSONS.md` 2026-10-27 M012) and confirm the faults: the AC1 image is not wrapped and warns, and the AC5 linked image paragraphs have `BodyText`.
- [ ] T2: In `wrapped.lua`, make `lone_wrapped_image` return the image and the inline to place (the link, or the image itself), and pass that inline to `wrapped_image_div`, `wrapped_image_typst`, `wrapped_image_docx`, and `wrapped_image_tex`, which keep reading and cleaning the image itself. Check that `no_text_blocks`, `joins_group`, and `find_contexts` reach the linked image (the last two by walks that already look inside links). Update the comments of `lone_wrapped_image` and `unplaced_image`. Write the four `fixture` snapshots from the fixed renders and read that the AC1 to AC4 lines match.
- [ ] T3: In `wrapped-docx.lua`, make `has_image` find an image inside a link at the paragraph's top level, and update its comment and `frame_para`'s. Write the `docx-alt` snapshot and read that the AC5 lines match.
- [ ] T4: Edit `docs/normal-layout.qmd:146` and the "An image with no caption" section of `docs/get-started.qmd` (about line 79) from the T2 renders, and name the linked form in the Syntax section of `cairn/DESIGN.md` (uncaptioned image line). Run `quarto render docs`.
- [ ] T5: Run `python3 tests/verify.py`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: idea vet: no flaw and no gap that the question set needed. Quarto 1.10.19 already makes a captioned linked image a Figure or a float, which the filter wraps, so the request's reading is the uncaptioned form; the class-on-link form is not in the request's words and becomes a candidate row; the Word paragraph style of captioned linked figures (`BodyText` in the frame against `Compact` without the filter, scratch docx render 2026-10-29) is a linked-image defect in the row's "all formats" and joins the scope.
- 2026-10-29: question set: what to work on — "Wrap images inside links in all formats".
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render; 2026-10-27 (M015) render with `filters:` removed to see what Quarto does; 2026-10-29 (M029) where Quarto puts `fig-alt` at Word post-render.
- 2026-10-29: collision check: absorbs the candidate row "Wrap images inside links in all formats" in full. M029 and M030 shipped Word alt text for framed images, which a framed linked image now gets; D-017 holds (framed figures only). No D-entry covers linked images. Inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-29: new candidate row "Warn for a wrap class on a link" for the class-on-link form (scratch renders, all four formats, no warning).
- 2026-10-29: plan gate chose to keep the link around the image inside the wrap box over dropping the link and wrapping the bare image, because dropping it loses the user's link in every format; falsified by a format in which a link inside the wrap box breaks the box's layout (the image not beside the text in a render).
- 2026-10-29: checkpoint: plan committed while the full criteria audit (fresh Opus reader) runs; its findings and dispositions follow in a later line.

## Decisions

## Review
