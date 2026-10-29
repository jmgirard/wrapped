# M031: Wrap images inside links in all formats

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes how linked images render in users' documents in all four formats
- **Branch/PR:** m031-linked-images

## Goal

In HTML, PDF through LaTeX, PDF through Typst, and Word, a wrapped image that is the only content of a link, which is the only content of its paragraph, wraps with its link and alt text as an unlinked image does, and in Word a framed captioned figure with a linked image keeps its paragraph style.

## Scope

**In:** In `_extensions/wrapped/wrapped.lua`, `lone_wrapped_image` (about line 1503) also accepts a paragraph whose only inline, spaces aside, is a `Link` whose only inline, spaces aside, is an image with a wrap class. The four `wrapped_image_*` builders and the next-block rule (`no_text_blocks`) then treat that image as they treat an uncaptioned image, and the box holds the link with the image inside it. In `_extensions/wrapped/wrapped-docx.lua`, `has_image` also finds an image inside a link, so the image paragraph of a framed captioned figure whose image is linked takes the figure's paragraph style. New and changed cases in `tests/fixture.qmd` and `tests/docx-alt.qmd`, image copies for them, their snapshots, and summary fields in `tests/verify.py` that record a wrapped image's link target. The linked-image sentences in `docs/normal-layout.qmd`, `docs/get-started.qmd`, and the Syntax section of `cairn/DESIGN.md`.

**Out:**
- A wrap class on the link instead of the image, `[![](plot.png)](url){.wrap-left}`, wraps in no format and prints no warning (scratch renders, 2026-10-29). The new candidate row "Warn for a wrap class on a link" holds it.
- A captioned linked image, `[![Caption](plot.png){.wrap-left}](url)` with or without a `#fig-` id, already wraps in all four formats, because Quarto 1.10.19 makes it a Figure or a float (scratch renders with and without the filter, 2026-10-29). Only its Word paragraph style changes here. In PDF through LaTeX, Quarto drops the link of the no-id form with or without the filter; that is Quarto's behavior and stays.
- HTML alt text: Quarto writes an image's `fig-alt` as its `alt` itself, and the filter does not touch it (the HTML summary records no alt text).
- Changelog: none (`cairn/PROFILE.md` changelog slot).

## Acceptance criteria

- [ ] AC1: In the HTML, PDF through LaTeX, PDF through Typst, and docx renders of `tests/fixture.qmd`, its "An image inside a link" case, a paragraph that holds only `[![](link.png){.wrap-left width="20%" wrap-gap="2em" fig-alt="A linked plot"}](https://example.com)` followed by two paragraphs, is a wrapped image: it sits in the box the filter makes for an uncaptioned image (an HTML `.wrapped-image` div, a LaTeX `wrappedfigure` with `caption=false`, a Typst `wrap-content` call, a Word frame) with a requested width of 20% and a 2em gap, both paragraphs after it join its group, and the render prints no warning that names `link.png`; as the four `fixture` snapshots record.
- [ ] AC2: In the same four renders, the AC1 image stays inside its link with the target `https://example.com`: an HTML `<a href>` around the `<img>`, a LaTeX `\href` around the `\includegraphics`, a Typst `#link` around the `image(` call, and a Word `w:hyperlink` whose relationship target is that URL around the drawing; as the four `fixture` snapshots record.
- [ ] AC3: In the PDF through LaTeX, PDF through Typst, and docx renders of `tests/fixture.qmd`, the AC1 image's alt text is "A linked plot", as the `fixture.pdf`, `fixture.typst`, and `fixture.docx` snapshots record.
- [ ] AC4: In the same four renders of `tests/fixture.qmd`, each under its own heading and with its own image files: three cases keep normal images in no wrap box, and the render prints the "is not a figure or the only content of its paragraph" warning for each of their images (a link that holds a wrapped image and a word, a link that holds two wrapped images, and a paragraph with a word beside a link that holds a wrapped image); a linked wrapped image followed by a heading keeps a normal image with no warning that names its file; and a wrapped float followed directly by a linked wrapped image and then a paragraph keeps a normal figure, while the linked image wraps (D-003); as the four `fixture` snapshots record.
- [ ] AC5: In the docx render of `tests/docx-alt.qmd`, a wrapped markdown float with a `#fig-` id and a wrapped captioned image with no id, each with its image as the only content of a link, give their image paragraph the same last `w:pStyle` (the style Word applies) as the same figure with no link in that render (`Compact` for the float, `CaptionedFigure` for the no-id image), as `tests/_snapshots/docx-alt.docx.txt` records.
- [ ] AC6: `docs/normal-layout.qmd` says that an image beside other content in its paragraph or in its link does not wrap and no longer says that an image inside a link does not wrap; `docs/get-started.qmd`'s "An image with no caption" section says that an image that is the only content of a link wraps and keeps its link, with the wrap class on the image; `quarto render docs` exits 0.
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

- [x] T1: Tests first. Copy `tests/plot.png` to one file per case (`link.png` for AC1 and one name per image of each AC4 case), so each warning names its case. In `tests/fixture.qmd` (about line 112), rewrite the linked case as AC1 gives it, with two paragraphs that say it wraps, and add the five AC4 cases, each under its own heading so no case joins another's group. In `tests/docx-alt.qmd`, add the two AC5 cases and, beside them, the same two figures with no link if no case there already serves. In `tests/verify.py`, make `html_summary`, `tex_summary`, `typ_summary`, and `docx_frames` record the link target of each image in a wrap box, only where there is one, so snapshots with no linked image keep their bytes; `docx_summary` reads `word/_rels/document.xml.rels` and passes the id-to-target map to `docx_frames`. Make `docx_frames` record the last `w:pStyle` of each framed image paragraph in `docx-alt` only (as `DOCX_UNFRAMED_ALT` gates the unframed list). Render the two fixtures on the unchanged filter (the one-fixture command, `cairn/LESSONS.md` 2026-10-27 M012) and confirm the faults: the AC1 image is not wrapped and warns, and the AC5 linked image paragraphs end with `BodyText`.
- [x] T2: In `wrapped.lua`, make `lone_wrapped_image` return the image and the inline to place (the link, or the image itself), and pass that inline to `wrapped_image_div`, `wrapped_image_typst`, `wrapped_image_docx`, and `wrapped_image_tex`, which keep reading and cleaning the image itself. Check that `no_text_blocks`, `joins_group`, and `find_contexts` reach the linked image (the last two by walks that already look inside links). Update the comments of `lone_wrapped_image` and `unplaced_image`. Write the four `fixture` snapshots from the fixed renders and read that the AC1 to AC4 lines match.
- [x] T3: In `wrapped-docx.lua`, make `has_image` find an image inside a link at the paragraph's top level, and update its comment and `frame_para`'s. Write the `docx-alt` snapshot and read that the AC5 lines match.
- [x] T4: Edit `docs/normal-layout.qmd:146` and the "An image with no caption" section of `docs/get-started.qmd` (about line 79) from the T2 renders, and name the linked form in the Syntax section of `cairn/DESIGN.md` (uncaptioned image line). Run `quarto render docs`.
- [x] T5: Run `python3 tests/verify.py`.

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
- 2026-10-29: criteria audit (full, fresh Opus reader): 13 findings. Fixed: #1 each case gets its own image file and AC4 says a warning for each image; #2 AC4's "no link removed" dropped, since no summary records unframed links; #3 T1 reads the Word rels part for link targets; #4 each AC4 case under its own heading, AC1 has two paragraphs; #5 AC4 adds the next-block case (a heading after a linked image) and the back-to-back case (D-003), both behavior changes the rule makes; #6 AC5 and T1 name the last `w:pStyle`; #7 Goal covers alt text and Word style, HTML alt text put in Out with its reason; #8 AC1 says requested width and names the alt text; #11 AC6 says the class goes on the image. No action: #9, #10, #12, #13 (no problem found).
- 2026-10-29: implement started on branch m031-linked-images.
- 2026-10-29: checkpoint: T1–T4 edits made (fixture and docx-alt cases, seven image copies, link and style summary fields, `lone_wrapped_image` with `only_inline` and `placed_image`, `has_image` in links, docs and DESIGN.md); one-fixture renders match AC1–AC5 and snapshots are written; `quarto render docs` exit 0; full `tests/verify.py` still running, so no task is checked yet.
- 2026-10-29: T1–T5 done. T1 confirmed the faults on the unchanged filter: all seven linked images warned and none wrapped, and the two linked captioned figures in Word had `FirstParagraph` and `BodyText` against `Compact` and `CaptionedFigure` unlinked. T1 fix: the caption branch of `docx_frames` reused the name `styles`, so the flag became `image_styles`. Implementation choice: `lone_wrapped_image` returns the image and its link, and `placed_image` rebuilds the link's content from the cleaned image, since a Lua copy of `link.content[1]` does not write back. `python3 tests/verify.py` all 104 renders pass; only the five `fixture` and `docx-alt` snapshots changed.
- 2026-10-29: checkpoint: claim audit returned 3 corrections, applied (docs need the link alone in its paragraph, also in DESIGN.md; the Word style docstring says what wrapped-docx.lua expects; the LaTeX and Typst link comments say first link in the box); `quarto render docs` exit 0; the reader's re-read of the three is running.
- 2026-10-29: claim audit: 28 claims read, 3 corrected — docs/get-started.qmd, docs/normal-layout.qmd, tests/verify.py (re-read once by the same reader: all three correct). Noted for review: the unchanged warning text "is not a figure or the only content of its paragraph" now also covers an image beside other content in its link.
- 2026-10-29: status review; the last full `tests/verify.py` (all 104 pass) ran before the claim-audit edits, which change only comments in `tests/verify.py` and docs prose.

## Decisions

## Review
