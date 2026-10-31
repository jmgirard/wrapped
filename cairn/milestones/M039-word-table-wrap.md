# M039: Wrap table floats in Word

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the Word output of each document with a wrapped table float
- **Branch/PR:** m039-word-table-wrap

## Goal

A `#tbl-` table float with a wrap class wraps the paragraphs after it in Word, in a floating table that holds its caption.

## Scope

**In:** In `wrapped.lua`, a table float wraps in Word, and the table warning covers LaTeX only. In `wrapped-docx.lua`, the post-render pass replaces Quarto's one-cell outer table of a wrapped `#tbl-` float with three parts: a raw openxml open tag for a floating table (`w:tblpPr`), the cell's own blocks, and a raw close tag. The side, width, and gap come from the group's `data-wrap-frame`. The clearing break that ends a figure's wrap ends the table's wrap too. `tests/verify.py` lists floating tables in the Word snapshots. The site, the README, `cairn/DESIGN.md`, and `cairn/references/wrap-mechanisms.md` say that table floats wrap in Word. D-022 records the decision. A table float whose table is raw openxml (gt, flextable) keeps its normal layout in Word with a warning (narrowed at review pass 3, the user's choice).

A probe on 2026-10-30 showed three facts. Pandoc 3.10 passes split raw table tags through. LibreOffice sets the floating table at its side with body text beside it. The clearing break (`w:br w:clear="all"`) ends the wrap below the table.

**Out:** Table floats in PDF through LaTeX stay normal with a warning (candidate "Wrap table floats in LaTeX PDFs"). Tables with no `#tbl-` label stay normal (candidate "Wrap tables that have no tbl- label"). The format warning in Word with columns still names figures only (candidate "Name tables in the format warning"). A scripted Word layout check in `tests/verify.py` is out, because D-005 keeps LibreOffice out of the test command. A Word table example on the docs site's example pages is out, because those pages show figures. Wrapping a raw openxml table (gt, flextable) in Word is out (candidate "Wrap gt and flextable tables in Word").

## Acceptance criteria

- [x] AC1: This criterion covers the Word renders of `tests/tables.qmd`, `tests/fixture.qmd`, and `tests/contexts.qmd`. In them, eleven table floats are floating tables (`w:tblpPr`): `#tbl-div`, `#tbl-block`, `#tbl-pipe`, `#tbl-cell`, `#tbl-cell-block`, `#tbl-page`, and `#tbl-wide` in `tables.qmd`, `#tbl-caption-block`, `#tbl-cell-block`, and `#tbl-cell-both` in `fixture.qmd`, and `#tbl-wrapped` in `contexts.qmd`. Each one is on the side that its class names. Its `w:tblW` width and its text distance on the text side equal the width and gap that `docx_frame` gives a figure with the same class, width, and gap. Its one cell holds the table's caption paragraph, the table, and the `#tbl-` bookmark. A clearing break after the group's last paragraph ends its wrap. `#tbl-no-text` in `tables.qmd` and `#tbl-cars` in `fixture.qmd` keep their normal layout with no warning. `python3 tests/verify.py` passes on the Word snapshots of the three fixtures.
- [x] AC2: `grep -rn 'A table wraps only in HTML and Typst' _extensions tests/_snapshots` finds nothing. No Word snapshot `tests/_snapshots/*.docx.txt` holds a warning that starts with "wrapped: the table #" and says "does not wrap in Word". In `tables.pdf.txt`, `fixture.pdf.txt`, `contexts.pdf.txt`, and `tables-cell-columns.pdf.txt`, the table warning reads "the table #<id> does not wrap in LaTeX. A table wraps in HTML, Typst, and Word."
- [x] AC3: This criterion covers a LibreOffice PDF of `tests/tables.docx`, made with `soffice --headless --convert-to pdf`. A table's box spans across the page from the text margin on its side out to its `w:tblW` width. For each floating table, at least one line of the paragraph after it lies outside the box's span, at a height within the table's rows. The first block after the group's clearing break starts below the table's lowest text. The text of each cell of `#tbl-wide` lies inside its box's span.
- [x] AC4: The user opens `tests/tables.docx` in Microsoft Word on the Mac. The user finds each floating table at its side, with body text beside it and its caption inside its box. The user finds the text after each group's clearing break below the table.
- [x] AC5: Two searches find the candidate lines: `grep -rn -i 'table' docs --include='*.qmd'` outside `docs/_site` and `docs/_freeze`, and `grep -n -i 'table' README.md`. No paragraph that holds a found line says that a table float keeps its normal layout in Word, or that a table float wraps only in HTML and Typst. `docs/formats/word.qmd` says that a wrapped table float sits in a floating table with its caption inside it. The page also states how a table wider than its box renders, and names the app whose render shows it.
- [x] AC6: `python3 tests/verify.py` exits 0 with each render passing, and `quarto render docs` exits 0.

## Coverage

- AC1 → T1, T2, T3, T7, T8, T9, T10
- AC2 → T1, T3
- AC3 → T2, T4, T7, T9
- AC4 → T6
- AC5 → T5
- AC6 → T6

## Tasks

- [x] T1: `wrapped.lua`: let a table float wrap in Word. In `float_target` (near line 1565), narrow the LaTeX and Word table warning to LaTeX, with the new sentence. Give a Word table float its frame through `docx_frame`, so that the grouping pass marks its group with `data-wrap-frame`. Update the comments that say a Word frame cannot hold a table.
- [x] T2: `wrapped-docx.lua`: in `frame_first`, find Quarto's one-cell table that holds a `tbl-` div, alone or in a code cell div. Replace it with the floating-table open tag, the cell's blocks, and the close tag. Fit the inner table to the box width. Keep the clearing break. Update the header comment.
- [x] T3: `tests/verify.py`: make `docx_summary` list each floating table, with its side, width, gap, bookmark, caption style, and the blocks after it up to the clearing break. Run `--update`, and read the snapshot diff for `tables`, `fixture`, `contexts`, and `tables-cell-columns`. Plant one defect for each axis and see the check fail for each: the wrong side, a dropped `w:tblpPr`, the caption moved out of the cell, a dropped bookmark, and a dropped clearing break. Cover at least one div float and one code-cell float. Fix the prose of `tests/fixture.qmd` (lines 214, 223, and 231) that says a table keeps a normal layout in Word.
- [x] T4: Convert `tests/tables.docx` to PDF with LibreOffice, and read the AC3 coordinates with `pdftotext -bbox`. If the wide table runs past its box, fix the fit. Record the coordinates in a work-log line, and keep the check script for review to rerun.
- [x] T5: Docs and README: change each paragraph that the AC5 searches find. Write the wrapped-table text and its limits in `docs/formats/word.qmd`. Update E5 and the Word mechanism text in `cairn/DESIGN.md`, and the W4 row of `cairn/references/wrap-mechanisms.md`.
- [x] T6: Run `python3 tests/verify.py` and `quarto render docs`. At review, stop once for the user's look in Word, and record the user's report in the Review section.
- [x] T7: Review return 1: a table, figure float, or callout right before a wrapped Word table float must not merge into it. Put a paragraph before the floating table, and check the case with a render and in LibreOffice.
- [x] T8: Pass-1 fix-now findings (Review section): size images outside a table float's tables to the box; record the inner table's width, the anchors, links, and citations in `docx_tables`; reword the nested-table count; render `tables-column-meta` to Word; fix the stale lines in DESIGN.md, the Lua headers, `wrap-mechanisms.md`, the `verify.py` docstrings, `docs/index.qmd`, `docs/formats/word.qmd`, and the "tested on HTML pages" sentences.
- [x] T9: Review return 2: the spacer keeps with the next paragraph, so a heading stays with its table; images in a table float's cells take their column's share of the box; the image-height warning names tables; the closing paragraph looks into a last div; the Word page's multi-column and box-contents sentences and the `docx_group` comment. Each fix gets a `tests/docx-tables.qmd` case and a plant.
- [x] T10: Narrowing at the thrash stop (the user's choice): keep a raw openxml table float normal in Word with a warning; close the cell past empty divs and after a raw block; size cell images by `fit_table`'s shares, keeping a smaller own width; restore the user's M006 height-warning wording for figures, with a table sentence of its own; the pass-3 comment and docs fixes. Each fix gets a `tests/docx-tables.qmd` case and a plant.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: not run — work named at the question set.
- 2026-10-30: question set: which work to plan — Wrap table floats in Word (candidate row absorbed, started M039).
- 2026-10-30: question set: may review stop for the user to open tests/tables.docx in Microsoft Word — yes, the user will look.
- 2026-10-30: idea vet: no flaw and no gap. Floating tables (`w:tblpPr`) are Word's own way to wrap text around a table, and the candidate row's caption-inside reading is the only one that fits it. A scratch probe confirmed the mechanism in Pandoc 3.10 and LibreOffice.
- 2026-10-30: collision check: candidate "Wrap table floats in Word documents" absorbed. D-021 kept Word tables normal as a deferral, and D-022 supersedes that part. M038 (done) shipped HTML and Typst only. No dropped milestone or rejection matches.
- 2026-10-30: inbox sweep: 0 open issues and 0 open pull requests on jmgirard/wrapped.
- 2026-10-30: plan gate chose a floating table (`w:tblpPr`) over a DrawingML text box (`wps:txbx`) that holds the table, because the floating table is Word's own table wrap and the probe showed LibreOffice and the clearing break handle it, while a text box takes a fixed height; falsified by Word showing the floating table with no text beside it, or ignoring the clearing break.
- 2026-10-30: plan gate chose split raw openxml tags around Quarto's own blocks over rewriting the zipped docx after Pandoc, because a filter cannot reach the written file and the probe showed Pandoc 3.10 keeps split tags; falsified by a Pandoc release that parses or drops unbalanced raw openxml.
- 2026-10-30: criteria audit (full mode, fresh Opus reader): 11 findings, all fixed. AC1 now names its eleven tables, states `#tbl-page` and `#tbl-cars`, defines width as `w:tblW` against `docx_frame`, and drops the snapshot line format (moved to T3). AC2's search no longer hits figure warnings that stay, and it names the four LaTeX snapshots. AC3 defines the box span and "beside". AC3 and AC4 drop their recording acts (moved to T4 and T6). AC5 reads paragraphs, not lines, and names the app. T3 plants one defect for each axis and fixes the fixture prose. D-022 supersedes the Word part of D-021.
- 2026-10-30: lessons used: 2026-10-30 (M038) on float content as one Block and cell classes, 2026-10-27 (M012) on checking one fixture, 2026-10-28 (M026) on LibreOffice PDFs that lose letters, so AC3 reads coordinates.
- 2026-10-30: no split: 6 criteria and 6 tasks. No changelog entry, since the profile keeps no changelog file.
- 2026-10-30: implement started on m039-word-table-wrap.
- 2026-10-30: checkpoint (T1, T2, T5 code and docs written; T3 summary code written, snapshots updating; T4 read done, not yet ticked). Inner tables got relative column widths (`fit_table`) after the first LibreOffice render cut off columns past the box. The floating table keeps Quarto's outer `tblStyle` and `tblLook` and closes a cell that ends in a table with an empty paragraph.
- 2026-10-30: T3: `python3 tests/verify.py --update` passed all 122 renders. The snapshot diff lists the 11 floating tables of AC1, drops every "does not wrap in Word" table warning (`#tbl-cars` and `#tbl-no-text` now print none in Word), and changes the LaTeX sentence in the four named snapshots. `docx_after` now holds the after-blocks loop that frames and tables share.
- 2026-10-30: T3 plants, each on `tests/tables.qmd` in Word, each red at `#tbl-div` (div float) and `#tbl-cell` (code-cell float): wrong side, dropped `w:tblpPr`, caption out of the cell, dropped bookmark, dropped clearing break. Script: scratchpad `plants.py`. The extension file was restored after each, and `tests/tables.docx` was rendered again and matches its snapshot.
- 2026-10-30: T4 (LibreOffice 26.8.1.1 PDF, `pdftotext -bbox`, scratchpad `ac3.py`): tables 1, 2, 3, 4, 5, 9, and 10 each have paragraph lines beside the table's text outside the box span (e.g. table 1 span x=329.4-540.0, 8 lines beside, rows y=144.2-245.8), and the next block starts below the table (table 1 next heading y=335.3). Table 9's one-line paragraph starts at y=230.9, above its caption text at 240.9, since the caption has 10 pt space before it, and overlaps the rows. `#tbl-wide` (span x=446.4-540.0) breaks across pages 3 and 4, and its 98 cell words all lie inside the span. It is the document's last group, so no block follows its clearing break.
- 2026-10-30: claim audit: 56 claims read, 4 corrected — tests/verify.py, docs/formats/word.qmd, tests/fixture.qmd; 4 stale unchanged lines fixed too (wrapped.lua header, wrapped-docx.lua header and frame_first comment, docs/normal-layout.qmd tbl-column in Word). The Word page now names LibreOffice for the wide-table behavior, since Word itself is not yet checked. Re-read pending; suite rerunning.
- 2026-10-30: claim audit re-read: 5 corrected claims hold; 2 fixed once more with no further pass (the frame_first comment now claims @fig- links only, since no snapshot records a link to a floating table; DESIGN.md's grid sum is Pandoc's 7920 twips, not the 9360-twip text width).
- 2026-10-30: T6: `python3 tests/verify.py` passed all 122 renders after the claim fixes, and `quarto render docs` exited 0 with no warning. The user's look in Word is review's stop. Status set to review.
- 2026-10-30: review return 1: a table, figure float, or callout right before a wrapped Word table float merges into it, because the raw floating table gets no paragraph between them (diff-bug #1, load-bearing). The same return carries the pass-1 fix-now findings that the Review section lists: images in a table float sized to the box, `docx_tables` recording inner width, anchor, links, and citations, the nested-count wording, a Word render of `tables-column-meta`, and the stale lines in DESIGN.md, the Lua headers, `wrap-mechanisms.md`, `verify.py` docstrings, `docs/index.qmd`, `docs/formats/word.qmd`, and the "tested on HTML pages" sentences.
- 2026-10-30: T7: a 1 pt paragraph (`w:line="20"` exact) now goes before each floating table, and the floating cell has no left or right margin. A scratch probe showed a plain table and a figure float right before wrapped tables staying apart in LaTeX-free LibreOffice output. New fixture `tests/docx-tables.qmd` (Word only) holds both cases and an image in a table float.
- 2026-10-30: T8: `docx_size` skips images in tables, so an image outside a table float's table fills the box (2377440 EMU in a 3744-twip box). `docx_tables` records anchors, the block before, image fill, the inner `w:tblW`, links, and citations; the count reads "not listed above". `tables-column-meta` renders to Word (its table warns "is in the margin"). Stale lines fixed in DESIGN.md (goals, warnings, stop rule, pass 4, post-render), the Lua headers, `wrap-mechanisms.md`, the `verify.py` docstring, `docs/formats/word.qmd`, and the three "tested on HTML pages" sentences. Two pass-1 fix-now findings turned out false on reading: ripple #6 (DESIGN.md's "a table in LaTeX and Word" is the figure-in-a-table-cell context, still true) and ripple #13 (`docs/index.qmd:26` describes how the page's demo figure is drawn).
- 2026-10-30: T7 and T8 checks: `python3 tests/verify.py --update` passed all 124 renders; the snapshot diff only adds the new fields and the two new Word snapshots. Plants on `tests/docx-tables.qmd` each turned red: dropped spacer (`before=tbl`), dropped image sizing (`image fills=no`, cx=5334000), dropped `fit_table` (`table auto 0`). AC3 reread on the new layout: all seven tables pass; `#tbl-wide` no longer breaks across pages, and `#tbl-image` in `docx-tables` shows the page break, so DESIGN.md's Known issues entry now cites it. (The T7 line's "LaTeX-free" is a slip for "LibreOffice output".) Status set to review.
- 2026-10-30: claim audit: 31 claims read, 2 corrected — tests/docx-tables.qmd, _extensions/wrapped/wrapped.lua (the fixture's opening now says the first two floats follow a table; the `docx_size` comment no longer says a table's column sizes its image). The re-read found both hold.
- 2026-10-30: `tests/.gitignore` gained `/.quarto/` from a Quarto render in `tests/`; it is not milestone work and stays unstaged.
- 2026-10-30: T4 minor amendment: T4 recorded its coordinates in the work log, not the review-owned Review section, which implement does not write.
- 2026-10-30: review return 2: the spacer paragraph before a Word floating table takes a heading's keep-with-next, so a heading near a page foot is cut off from its wrapped table (pass-2 diff-bug #1, load-bearing). The same return carries the pass-2 fix-now findings that the Review section lists: images in the inner table's cells sized to their column's share of the box, the image-height warning's wording, a closing paragraph after a last Div that ends in a table, and the Word page's multi-column and box-contents sentences and the `docx_group` comment. Defect returns so far: 2.
- 2026-10-30: T9: the spacer's `w:pPr` gains `w:keepNext`; in LibreOffice the pass-2 heading probes now put the heading on page 2 with its table. `docx_size(..., by_column)` sets each image in a table float's table to its column's equal share of the box less 216 twips of cell margin (1656 twips in a 3744-twip, two-column box). The closing paragraph looks into a div that ends the cell. The height warning now reads "in a wrapped figure or table, so the box sets the image's width" (three snapshots). `docx_tables` adds " keep" to `before=` and each cell image's width. `tests/docx-tables.qmd` gains `#tbl-cell-images` and `#tbl-nested`. `python3 tests/verify.py --update` passed all 124 renders, with only those changes. Plants each red: keepNext dropped (`before=p`), cell images unsized (`images=8400,8400`), last div not read (cell ends in `table`). AC3 reread: ok for all seven tables.
- 2026-10-30: claim audit: 24 claims read, 2 corrected — _extensions/wrapped/wrapped.lua, docs/formats/word.qmd, tests/docx-tables.qmd (cell images take an equal share per column, not their column's own width; the image in `#tbl-image` sits above its table, not beside it). The heading claim now names LibreOffice, the only app observed. DESIGN.md's Word table paragraph gains the cell-image and keep-with-next sentences.
- 2026-10-30: T9 shape: equal column shares, not each column's own width, since `fit_table` gives default-width columns equal shares; a table with explicit uneven widths can still clip a wide image in its narrow column (no fixture).
- 2026-10-30: claim audit re-read: all six corrected claims hold. It noted that the 144-twip floor in `docx_size` can make an image wider than its cell in a box under about 0.5 in for two columns; left as is, since only an asked-for box that narrow reaches it. Status set to review.
- 2026-10-31: thrash stop (a) at review pass 3: the user chose "Narrow it". A table float whose table is raw openxml (gt, flextable) keeps its normal layout in Word with a warning, and wrapping it moves to a candidate row (split from M039). The empty-div close and the pass-3 fix-now items land with the narrowing, then one review pass checks the narrowed milestone. Defect returns stay at 2; this route is the descope the rule offers, not a retry.
- 2026-10-31: question set (thrash stop): the user's look at `tests/tables.docx` and `tests/docx-tables.docx` in Microsoft Word — "Yes, looks right".
- 2026-10-31: substantive amendment: Scope In now says a table float whose table is raw openxml (gt, flextable) keeps its normal layout in Word with a warning, and Scope Out sends wrapping it to the candidate "Wrap gt and flextable tables in Word" (split from M039). No criterion's wording changed. The user chose this at the thrash stop.
- 2026-10-31: T10 checkpoint (suite update running): `raw_docx_table` keeps a raw openxml table float normal in Word with "the table #<id> is raw Word XML, as from gt or flextable, so it does not wrap in Word."; the closing paragraph looks past empty divs and also follows a raw block; `docx_size(by_column)` uses `fit_table`'s shares summed over a column span, keeps a smaller own width, and floors at half the cell; the height warning keeps the user's M006 figure wording and says "in a wrapped table, so the box or its column sets the image's width" for a table; comments and `docs/formats/word.qmd` follow. Rows: "Size Word table columns by content" and "Keep image size in unframed Word figures" merged into "[low] Size images and columns in Word tables", which also takes pass-3 diff-bug #3 and #7 and a fixture finding (a table float with no width of its own takes its box width from its first image, in every format, since M038).
- 2026-10-31: T10 checks: `python3 tests/verify.py --update` passed all 124 renders; the diff restores the M006 height-warning text in three snapshots and adds the `docx-tables` cases (`#tbl-empty-div`, `#tbl-uneven` with `images=240,2320`, `#tbl-raw`'s warning); a cell-image height then added the table warning to that snapshot. Plants on `docx-tables`, each red: raw detection off (`tbl-raw` floats with no warning), the pass-2 closing rule (`tbl-empty-div` cell ends in `table`), equal shares (`images=240,1656`), own width ignored (`images=991,2320`), table wording off (figure wording on a table image). Restored render matches.

## Decisions

## Review

- Pass 1, 2026-10-30, review head 5a7cc5c, base main 72abe16 (branch level with origin/main). Copilot round off (no header line).
- AC5 evidence: `grep -rn -i 'table' docs --include='*.qmd'` outside `_site`/`_freeze` found 56 lines, and `grep -n -i 'table' README.md` found 2. Each paragraph holding a found line that names formats for table floats names Word among the formats where they wrap (`index.qmd:38`, `README.md:10`, `get-started.qmd:120`, `normal-layout.qmd:95`, `reference.qmd:15` and the two class rows, `stopping.qmd:9`, `formats/html.qmd:14`, `formats/typst.qmd:10`). `formats/latex.qmd:73` names LaTeX only. No paragraph says a table float keeps its normal layout in Word or wraps only in HTML and Typst. `docs/formats/word.qmd` Tables says the table sits in a floating table with its caption inside it, and names LibreOffice 26.8 for the wide-table narrowing and in-word breaks.
- Gate (pass 1 head): `python3 tests/verify.py` exit 0, all 122 renders pass; `python3 tests/docs_layout.py` exit 0 (LaTeX, Typst, Word PDFs); `--html` not run on the Mac (Playwright for Python not installed), left to the docs workflow on the PR.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a table, figure float, or callout (all tables in docx) right before a wrapped table float merges into the raw floating table, since Pandoc adds no paragraph between them — fix now; load-bearing, so review return 1
- diff-bug #2: an image inside a table float keeps its own width and is clipped by the fixed box — fix now (size images outside the float's tables to the box)
- diff-bug #3: the inner table's 7920-twip grid fit is seen only in LibreOffice — noted; AC4's look in Word checks it
- diff-bug #4: `fit_table` gives default-width columns equal shares, so a long text column gets no more room than a number column — follow-up: [low] candidate "Size Word table columns by content"
- diff-bug #5: in a block quote the box sits at the page margin, not the quote's indent — reject, planned change: a Word figure frame uses the same margin anchor, and the docs say the box places as a frame does
- diff-bug #6: LibreOffice drew `#tbl-grid`'s box above its heading after the clipped image box — noted; falls with #2, rechecked after its fix
- diff-bug #7: the XML holds on every named path — noted
- diff-bug #8: `docx_tables` records no inner-table width or anchor, so dropping `fit_table` passes — fix now
- diff-bug #9: a dropped clearing break shows as "floating tables not at the top level", the wrong cause — fix now (reword to "not listed above")
- diff-bug #10: no Word render covers a document `tbl-column` — fix now (Word render of `tables-column-meta`)
- blame-history #1: DESIGN.md lines 18, 109, and 244 omit Word or say Word tables keep their normal layout — fix now
- blame-history #2: images in a table float keep their own size — fix now (same as diff-bug #2)
- blame-history #3: `#tbl-no-text` in Word now prints no warning — reject, planned change: AC1 names it, by the next-block rule
- blame-history #4: README carries a table rule against CLAUDE.md's site-page rule — reject, planned change: M038 put the sentence there, and M039 keeps it true
- blame-history #5: no Word snapshot covers the metadata `tbl-column` claim — fix now (same as diff-bug #10)
- blame-history #6: "Wrapped tables are tested on HTML pages, not in slides or dashboards" leaves out Word and Typst — fix now
- prior-review #1: Word layout seen only in LibreOffice — noted; AC4 checks it
- prior-review #2: table lines drop the links and citations that frame lines record — fix now
- prior-review #3: images in a table float are not fitted — fix now (same as diff-bug #2)
- prior-review #4: `#tbl-page` now wraps in Word — reject, planned change: a page-wide figure wraps in Word too, and AC1 names it
- prior-review #5: a Word table caption's trailing space is untested — reject, false: no caption in `tests/tables.docx` ends in a space
- prior-review #6: table floats skip the `frameable` check — reject, false: a table cell holds any block, and diff-bug #7 found valid XML on every path
- prior-review #7: the hardcoded `Table` style can be missing from a reference doc — reject, false: Quarto writes the same style on its own float tables
- prior-review #8: README table rule — reject, planned change (as blame-history #4)
- ripple #1: ROADMAP's "Wrap table floats in Word documents" row is stale — reject, planned change: hygiene removes the row at the merge
- ripple #2–#6, #8: DESIGN.md lines 17-18, 24-25, 109, 218, 244, and 345-346 — fix now
- ripple #7: the callouts candidate row says Word cannot set a box beside text — fix now (narrow the row)
- ripple #9, #10: `wrapped.lua` and `wrapped-docx.lua` header comments name frames only — fix now
- ripple #11: `wrap-mechanisms.md` lines 131 and 145-146 name frames only — fix now
- ripple #12: `tests/verify.py` docstring lines 22-23 and 39-41 omit the floating-table section — fix now
- ripple #13: `docs/index.qmd:26` names only a frame in Word — fix now
- ripple #14: `docs/formats/word.qmd:65` "Word cannot put a table in a frame" reads against the Tables section — fix now (point to Tables)
- ripple #15: a table-only document in Word with columns prints "does not wrap figures" — follow-up: existing row "Name tables in the format warning"
- Pass-1 fix-now items fixed in daaa5e6, d2dd8d5, and ddf362b. On reading, ripple #6 (DESIGN.md's "a table in LaTeX and Word" is the figure-in-a-table-cell context) and ripple #13 (`docs/index.qmd:26` describes the page's demo figure) are reject, false.
- Pass 2, 2026-10-30, review head ddf362b, base main 72abe16 (level). Gate: `python3 tests/verify.py` exit 0, all 124 renders pass; `quarto render docs` exit 0 with no warning; `python3 tests/docs_layout.py` exit 0.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the 1 pt spacer takes a heading's keep-with-next, so a heading near a page foot sits alone while its wrapped table moves to the next page (LibreOffice probe; Word keeps the same rule) — fix now (`w:keepNext` on the spacer); load-bearing, so review return 2
- diff-bug #2: images in the inner table's cells keep Pandoc's width and are clipped by the box, so a table of images now wraps broken where it kept its normal layout before — fix now (size each cell image to its column's share of the box)
- diff-bug #3: the spacer is written before every floating table and moves the paragraph beside it down 5 to 10 pt — follow-up: [parked] candidate "Write the Word table spacer only after a table", promote when a user reports the gap
- diff-bug #4: `before=` catches a dropped spacer only in `docx-tables` — reject, planned change: that fixture exists for this case, and its plant turned red
- diff-bug #5: `cites` never varies and `anchor` looks constant — reject, false: `anchor` reads `w:horzAnchor` and `w:vertAnchor` from the XML, and `cites` mirrors the frame lines that prior-review #2 asked for
- diff-bug #6: zero cell margins move caption and table text 5.4 pt toward the margin — noted; DESIGN.md records it, as a frame has no inset
- diff-bug #7: a figure float whose image is in a table has its image sized, then keeps its normal layout — follow-up: [parked] candidate "Keep image size in unframed Word figures", promote when a user reports it (it predates M039)
- diff-bug #8: the `docx_size` walk still sizes every figure image — noted
- diff-bug #9: three comment blocks are wrapped unevenly — reject, style
- blame-history #1: images in a table float's cells overflow (as diff-bug #2) — fix now
- blame-history #2: the image-height warning says the image fills the box width, false for an image in a table float — fix now
- blame-history #3: a Word table float with no paragraph after it prints no warning — reject, planned change (as pass-1 blame-history #3)
- blame-history #4: table-float images get no fig-alt from `alt_image` — reject, planned change: D-017 sets fig-alt only on figures the filter frames, and a table float's images got none before M039 either
- blame-history #5: a cell whose last block is a Div ending in a table gets no closing paragraph — fix now (look into the last Div)
- blame-history #6: a second floating table before a clearing break shows only in the unlisted count — reject, planned change: the count exists to report it
- prior-review #1: cell images overflow (as diff-bug #2) — fix now
- prior-review #2: table-float images get no fig-alt — reject (as blame-history #4)
- prior-review #3: the docs do not mention that `#tbl-page` wraps in Word — reject, false: `docs/normal-layout.qmd` says a `tbl-column` of `page` leaves a Word table in the body, where it wraps
- ripple #1: `wrap-mechanisms.md` W4 row's mechanism column describes the figure table only — reject, planned change: the row's last column states the table case (M039, D-022)
- ripple #2: `docs/formats/word.qmd:55` says a multi-column reference doc keeps normal figures, and tables keep theirs too — fix now
- ripple #3: `docs/formats/word.qmd:78` says the box holds the caption and the table, leaving out an image beside the table — fix now
- ripple #4: the Word page gives no Word behavior for a table box at a page end — noted; AC4's look covers Word, and the page names LibreOffice for its page break
- ripple #5: the `docx_group` comment says the group carries its figure's frame — fix now (figure or table)
- Pass-2 fix-now items fixed in 3dc2f09 and 1fcb0fd.
- Pass 3, 2026-10-30, review head f044ea2, base main 72abe16 (level). Gate: `python3 tests/verify.py` exit 0, all 124 renders pass; `quarto render docs` exit 0 with no warning; `python3 tests/docs_layout.py` exit 0.
- AC1 evidence (f044ea2): `tests/_snapshots/tables.docx.txt`, `fixture.docx.txt`, and `contexts.docx.txt` list the eleven named tables as floating tables, each `before=p keep`, its side from its class, `w=` and `left=`/`right=` matching `docx_frame` (4212/480 for `#tbl-div` at 45% and 2em; 3276/360 at the 35% and 1.5em defaults; 3744/240 at 40% and 1em), cell parts `<id>, caption, table pct 5000, p`, and after-blocks ending `clear`. `#tbl-no-text` and `#tbl-cars` have no table line and no warning. verify exit 0 on these snapshots.
- AC2 evidence (f044ea2): `grep -rn 'A table wraps only in HTML and Typst' _extensions tests/_snapshots` exit 1; no `*.docx.txt` holds a "wrapped: the table #… does not wrap in Word" line; `tables.pdf.txt` (7), `fixture.pdf.txt` (4), `contexts.pdf.txt` (1), and `tables-cell-columns.pdf.txt` (1) hold "does not wrap in LaTeX. A table wraps in HTML, Typst, and Word."
- AC3 evidence (f044ea2, LibreOffice 26.8.1.1 PDF of `tests/tables.docx`, scratchpad `ac3.py`): tables 1, 2, 3, 4, 5, 9, and 10 each have beside lines outside the box span within the table's text heights (table 1: span x=329.4-540.0, rows y=145.2-233.1, 7 lines beside), and the next block starts below the table (table 1: y=326.6). `#tbl-wide`: 51 cell words, none outside x=446.4-540.0.
- AC6 evidence (f044ea2): verify exit 0, all 124 renders; `quarto render docs` exit 0.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a table float whose table is raw openxml (gt, flextable) or that ends in an empty div gets no closing paragraph, so its cell ends in a table; LibreOffice sets it with no text beside, and Word may call the file damaged — load-bearing; would be defect return 3, so the thrash stop
- diff-bug #2: `by_column` enlarges small cell images, such as icons with their own width, to the column share — fix now (keep the smaller of the image's own width and the share)
- diff-bug #3: an image in a nested table or a spanning cell gets the outer table's one-column share — follow-up: [parked] candidate "Size images in nested Word table cells", promote when a user reports it
- diff-bug #4: a raw openxml table skips `fit_table`, so its grid can run past the box in Word — goes with diff-bug #1
- diff-bug #5: the reworded height warning is not true for a figure that Word then declines, a Typst cell image, or a nested-table image — fix now (restore the user's M006 wording for figures; a table sentence of its own)
- diff-bug #6: no bad keep-with-next chain found — noted
- diff-bug #7: an inline image in a table float's note paragraph is set to the full box width — follow-up: [parked] in the same candidate as #3
- diff-bug #8: `images=` floors EMU to twips — reject, style
- blame-history #1: cell images use an equal share while `fit_table` keeps uneven colspec shares — fix now (size by the same shares)
- blame-history #2: the height warning's M006 wording was the user's choice at a stop, and T9 replaced it unasked — fix now (as diff-bug #5)
- blame-history #3: an empty trailing div drops the closing paragraph — goes with diff-bug #1
- blame-history #4: the 144-twip floor overflows a cell in a box of 11 or more columns — fix now (floor at half the share)
- prior-review #1: uneven column shares (as blame-history #1) — fix now
- prior-review #2: the warning says the box sets a Typst cell image's width (as diff-bug #5) — fix now
- ripple #1: the `clean_image` comment says `docx_size` sets the width to the frame width — fix now
- ripple #2: a `wrapped.lua` comment says a multi-column reference doc keeps normal figures — fix now (figures and table floats)
- ripple #3: the multi-column Word warning names figures only — follow-up: existing row "Name tables in the format warning"
- ripple #4: `docs/formats/word.qmd` says the height warning is for a wrapped figure and the image takes the frame's width — fix now
- ripple #5: the height warning never fires for table floats — reject, false: `float_target` runs `clean_images` on every float's content
- ripple #6: a comment says a table float in a multi-figure cell wraps or warns on its own — reject, false: in a multi-column Word doc it gets the format warning
- ripple #7: the `verify.py` module docstring says table cell images report whether each fills the box — fix now (they report widths)
- ripple #8: README states Word table wrapping with no multi-column exception — reject, planned change: the figure sentence beside it has the same form
- Thrash rule (a): diff-bug #1 would be the third defect return. Stopped for the user's choice.
- AC4 evidence (2026-10-31): the user opened `tests/tables.docx` and `tests/docx-tables.docx` (rendered at f044ea2) in Microsoft Word on the Mac and reported each wrapped table at its side with body text beside it, its caption inside its box, and the text after each group below the table ("Yes, looks right").
- Thrash disposition: the user chose to narrow (descope) at the stop; routed to `/milestone-implement` for the scope amendment and the pass-3 fix-now items.
