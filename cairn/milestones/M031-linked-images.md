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

- [x] AC1: In the HTML, PDF through LaTeX, PDF through Typst, and docx renders of `tests/fixture.qmd`, its "An image inside a link" case, a paragraph that holds only `[![](link.png){.wrap-left width="20%" wrap-gap="2em" fig-alt="A linked plot"}](https://example.com)` followed by two paragraphs, is a wrapped image: it sits in the box the filter makes for an uncaptioned image (an HTML `.wrapped-image` div, a LaTeX `wrappedfigure` with `caption=false`, a Typst `wrap-content` call, a Word frame) with a requested width of 20% and a 2em gap, both paragraphs after it join its group, and the render prints no warning that names `link.png`; as the four `fixture` snapshots record.
- [x] AC2: In the same four renders, the AC1 image stays inside its link with the target `https://example.com`: an HTML `<a href>` around the `<img>`, a LaTeX `\href` around the `\includegraphics`, a Typst `#link` around the `image(` call, and a Word `w:hyperlink` whose relationship target is that URL around the drawing; as the four `fixture` snapshots record.
- [x] AC3: In the PDF through LaTeX, PDF through Typst, and docx renders of `tests/fixture.qmd`, the AC1 image's alt text is "A linked plot", as the `fixture.pdf`, `fixture.typst`, and `fixture.docx` snapshots record.
- [x] AC4: In the same four renders of `tests/fixture.qmd`, each under its own heading and with its own image files: three cases keep normal images in no wrap box, and the render prints the "is not a figure or the only content of its paragraph" warning for each of their images (a link that holds a wrapped image and a word, a link that holds two wrapped images, and a paragraph with a word beside a link that holds a wrapped image); a linked wrapped image followed by a heading keeps a normal image with no warning that names its file; and a wrapped float followed directly by a linked wrapped image and then a paragraph keeps a normal figure, while the linked image wraps (D-003); as the four `fixture` snapshots record.
- [x] AC5: In the docx render of `tests/docx-alt.qmd`, a wrapped markdown float with a `#fig-` id and a wrapped captioned image with no id, each with its image as the only content of a link, give their image paragraph the same last `w:pStyle` (the style Word applies) as the same figure with no link in that render (`Compact` for the float, `CaptionedFigure` for the no-id image), as `tests/_snapshots/docx-alt.docx.txt` records.
- [x] AC6: `docs/normal-layout.qmd` says that an image beside other content in its paragraph or in its link does not wrap and no longer says that an image inside a link does not wrap; `docs/get-started.qmd`'s "An image with no caption" section says that an image that is the only content of a link wraps and keeps its link, with the wrap class on the image; `quarto render docs` exits 0.
- [x] AC7: `python3 tests/verify.py` exits 0.

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
- 2026-10-29: correction of the T1–T5 line: a change to `link.content[1]` does write back in this Pandoc (`quarto pandoc lua` check at review, diff-bug #7); `placed_image` is kept as the one place that builds the box's inline.
- 2026-10-29: review fix-now edits: link patterns anchored to the image in `tex_summary` and `typ_summary`, `tests/verify.py` docstrings, the `normal-layout.qmd` link sentence, and the DESIGN.md next-block paragraph.
- 2026-10-29: step-7 approval: m031-linked-images approved for merge

## Decisions

## Review

- Evidence run: `python3 tests/verify.py` at 06806fa, all 104 renders pass, so each render matches its committed snapshot; the lines below are read from those snapshots.
- AC1: the `fixture` snapshots put `link.png` in a box in all four formats: HTML `(box): wrapped-image wrap-left style=--wrap-gap: 2em; --wrap-width: 20%` with group `wrapped-image, p, p`; LaTeX `wrappedfigure` `[side=left,width=0.2\linewidth,gap=2em,caption=false]`; Typst `wrap-content` with `wrapped-width(wrapped-size, 2em, 20%, …)` and `p, p`; Word frame `w=1872 gap=480` (20% of 9360 twips, 2em at 12 pt) with `p, p, clear`. No warning names `link.png` in any of the four (grep count 0).
- AC2: `link=https://example.com` on the AC1 image in all four: HTML image line `link.png: … link=https://example.com` (the `<a href>` open around the `<img>`), LaTeX `wrappedfigure` line ending `link=https://example.com` (`\href` in its body), Typst wrap line `link.png alt="A linked plot" link=https://example.com` (`#link(` in the box), Word frame part `image link.png … link=https://example.com` (a `w:hyperlink` around the drawing, its `r:id` target read from `word/_rels/document.xml.rels`).
- AC3: alt text "A linked plot": `fixture.pdf` `alt={A linked plot}`, `fixture.typst` `alt="A linked plot"`, `fixture.docx` `alt='A linked plot'`.
- AC4: each of the four `fixture` snapshots prints `1x … the image <file> is not a figure or the only content of its paragraph` for `link-text.png`, `link-two-a.png`, `link-two-b.png`, and `link-beside.png`, and none of those files is in a box (HTML image lines `wrap=- style=width:20.0%`, no LaTeX `wrappedfigure`, Typst wrap line, or Word frame names them). `link-heading.png` has no warning in any of the four and no box. `fig-before-link` keeps a normal figure (HTML `fig-before-link: - style=-`, LaTeX `figure: fig-before-link`, Typst in no wrap line, Word in no frame), and `link-after.png` wraps (HTML group `wrapped-image, p`, LaTeX `wrappedfigure … link=`, Typst wrap line `link-after.png`, Word frame `image link-after.png`).
- AC5: `docx-alt.docx.txt`: linked float `fig-md-link` image `style=Compact`, unlinked `fig-md` `style=Compact`; linked no-id image `style=CaptionedFigure`, unlinked no-id image ("Alt for the image with no id") `style=CaptionedFigure`. On the unchanged filter these two linked paragraphs were `FirstParagraph` and `BodyText` (T1 work-log line).
- AC7: `python3 tests/verify.py` at 06806fa exited 0, "all 104 renders pass".
- AC6: `docs/normal-layout.qmd:146-149` says an image beside other content in its paragraph, or beside other content in its link, does not wrap and that an image that is the only content of a link, with the link alone in its paragraph, wraps; "An image inside a link … does not wrap" is gone (`grep -n 'inside a link' docs/` finds nothing). `docs/get-started.qmd:85-87`, under "An image with no caption", says such an image wraps and keeps its link, with the wrap class on the image, not on the link. `quarto render docs` exit 0 after the review's wording fix.
- Gate: `cairn_validate.py` all checks passed; one version marker, `_extensions/wrapped/_extension.yml` 0.2.0, unchanged by the branch; verify as AC7; `tests/docs_layout.py` on the Mac 24 `ok` and no other line (`--html` not run), the docs workflow runs on the PR; changelog slot "none". No principle changed, so `cairn_impact` was skipped.
- spawned: diff-bug, blame-history, prior-review, ripple
- placement renders (scratch, 2026-10-29, for prior-review #1 and #2): a linked wrapped image at 30% with two paragraphs and a heading. LaTeX PDF image left 125 to 325 px and first line at left 342; Typst image 135 to 329, first line 346; Word through LibreOffice image 122 to 333, first line 337; each second paragraph starts below the image at full width. HTML `fixture.html` at 1280x900 in the browser pane: `link.png` box `float: left`, 160 px, image right edge 328, first line left 362 at the image's top. The LaTeX PDF and the docx keep the link; LibreOffice drops image links from its PDF with or without the filter (scratch render with `filters: []`).
- diff-bug #1: LaTeX and Typst summaries took the first link anywhere in the box, a caption link included — fix now (patterns anchored to `\href{…}{\includegraphics` and `#link("…")[#box(image(`; a planted caption `\href` gives no `link=`, an image `\href` does)
- diff-bug #2: HTML summary adds `link=` to any image inside an `<a>`, not only wrapped ones — reject, false: its comment says any image inside a link, and the AC4 lines use it; T1's "only in a wrap box" wording was looser than the code (noted)
- diff-bug #3: in Word a caption paragraph holding an image, linked or not, takes the frame's image style instead of ImageCaption (fig-two-icon shows it before this branch) — follow-up, new row "Keep caption style for caption images"
- diff-bug #4: internal links (`\hyperref`, `#link(<…>)`, `w:anchor`) are not recorded — fix now (summary comments now say external link)
- diff-bug #5: the two-image and word-in-link cases run the same code path — reject, planned change: AC4 names both cases
- diff-bug #6: the tex summary keeps LaTeX escapes in a link target — reject, style
- diff-bug #7: the work log says a Lua copy of `link.content[1]` does not write back; a `quarto pandoc lua` check shows it does — fix now (corrected in the work log; `placed_image` stays, harmless)
- diff-bug #8: the next-block changes (a float before a linked image falls back; a linked image before a heading keeps a normal image with no warning) are correct under D-003 — noted
- diff-bug #9: the warning text does not mention the link — reject, false: "is not a figure or the only content of its paragraph" is true for each image that warns, since a wrapped image is a paragraph's content only when its link is alone there
- diff-bug #10: T3's `frame_para` comment was not updated — reject, false: the comment still holds for a linked image
- diff-bug #11: `names =[` spacing and a docstring break — fix now (spacing fixed; docstring reflowed with the claim-audit edit)
- blame-history #1: the linked image's next-block classification has no D-entry or DESIGN.md line — fix now (DESIGN.md next-block paragraph names a lone wrapped image, linked or not, as no paragraph; no D-entry, since the plan's goal makes it a wrapped image and D-003 applies as written)
- blame-history #2: existing documents change layout with no changelog — reject, planned change: the changelog slot is "none"
- blame-history #3: the old "inside a link does not wrap" statements are reversed — noted (the planned change)
- blame-history #4: linked icon in a caption takes the image style — follow-up, same row as diff-bug #3
- blame-history #5: `names[-1]` read as the style Word applies — reject, false: the claim audit already changed the docstring to what wrapped-docx.lua expects
- blame-history #6: warning wording — reject, false (as diff-bug #9)
- blame-history #7: style nits — fix now (as diff-bug #11)
- prior-review #1: no Word or LibreOffice render of a framed linked image — fix now (placement renders above)
- prior-review #2: the plan's recorded falsifier (a link breaking the box layout) has no resolution — fix now (placement renders above show the image beside its text in all four formats)
- prior-review #3: caption icon styling — follow-up, same row as diff-bug #3
- ripple #1: the "Wrap images inside links in all formats" row now reads stale — fix now at hygiene (the row graduates)
- ripple #2: `tests/verify.py` module docstring lacks the link and style fields — fix now
- ripple #3: DESIGN.md next-block list does not name a lone wrapped image — fix now (as blame-history #1)
- ripple #4: `docs/index.qmd` and two examples say a wrap runs to the next block that is not a paragraph — reject, false as stale-by-this-diff: an unlinked wrapped image already stopped a wrap the same way, and `docs/stopping.qmd` states the two-figures case
- ripple #5: `docs/normal-layout.qmd` "or in its link, does not wrap" read against its next sentence — fix now (now "beside other content in its link")
- fix-now edits landed in 78e721d; `python3 tests/verify.py` on that tree: all 104 renders pass; `quarto render docs` exit 0 and `tests/docs_layout.py` 24 `ok`. Snapshot files changed by the branch (`tests/_snapshots/`, outside the skill's `_snaps` definition, listed for the record): `fixture.{html,pdf,typst,docx}.txt` and `docx-alt.docx.txt`, each change called for by AC1–AC5.
