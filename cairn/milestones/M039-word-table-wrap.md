# M039: Wrap table floats in Word

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the Word output of each document with a wrapped table float
- **Branch/PR:** —

## Goal

A `#tbl-` table float with a wrap class wraps the paragraphs after it in Word, in a floating table that holds its caption.

## Scope

**In:** In `wrapped.lua`, a table float wraps in Word, and the table warning covers LaTeX only. In `wrapped-docx.lua`, the post-render pass replaces Quarto's one-cell outer table of a wrapped `#tbl-` float with three parts: a raw openxml open tag for a floating table (`w:tblpPr`), the cell's own blocks, and a raw close tag. The side, width, and gap come from the group's `data-wrap-frame`. The clearing break that ends a figure's wrap ends the table's wrap too. `tests/verify.py` lists floating tables in the Word snapshots. The site, the README, `cairn/DESIGN.md`, and `cairn/references/wrap-mechanisms.md` say that table floats wrap in Word. D-022 records the decision.

A probe on 2026-10-30 showed three facts. Pandoc 3.10 passes split raw table tags through. LibreOffice sets the floating table at its side with body text beside it. The clearing break (`w:br w:clear="all"`) ends the wrap below the table.

**Out:** Table floats in PDF through LaTeX stay normal with a warning (candidate "Wrap table floats in LaTeX PDFs"). Tables with no `#tbl-` label stay normal (candidate "Wrap tables that have no tbl- label"). The format warning in Word with columns still names figures only (candidate "Name tables in the format warning"). A scripted Word layout check in `tests/verify.py` is out, because D-005 keeps LibreOffice out of the test command. A Word table example on the docs site's example pages is out, because those pages show figures.

## Acceptance criteria

- [ ] AC1: This criterion covers the Word renders of `tests/tables.qmd`, `tests/fixture.qmd`, and `tests/contexts.qmd`. In them, eleven table floats are floating tables (`w:tblpPr`): `#tbl-div`, `#tbl-block`, `#tbl-pipe`, `#tbl-cell`, `#tbl-cell-block`, `#tbl-page`, and `#tbl-wide` in `tables.qmd`, `#tbl-caption-block`, `#tbl-cell-block`, and `#tbl-cell-both` in `fixture.qmd`, and `#tbl-wrapped` in `contexts.qmd`. Each one is on the side that its class names. Its `w:tblW` width and its text distance on the text side equal the width and gap that `docx_frame` gives a figure with the same class, width, and gap. Its one cell holds the table's caption paragraph, the table, and the `#tbl-` bookmark. A clearing break after the group's last paragraph ends its wrap. `#tbl-no-text` in `tables.qmd` and `#tbl-cars` in `fixture.qmd` keep their normal layout with no warning. `python3 tests/verify.py` passes on the Word snapshots of the three fixtures.
- [ ] AC2: `grep -rn 'A table wraps only in HTML and Typst' _extensions tests/_snapshots` finds nothing. No Word snapshot `tests/_snapshots/*.docx.txt` holds a warning that starts with "wrapped: the table #" and says "does not wrap in Word". In `tables.pdf.txt`, `fixture.pdf.txt`, `contexts.pdf.txt`, and `tables-cell-columns.pdf.txt`, the table warning reads "the table #<id> does not wrap in LaTeX. A table wraps in HTML, Typst, and Word."
- [ ] AC3: This criterion covers a LibreOffice PDF of `tests/tables.docx`, made with `soffice --headless --convert-to pdf`. A table's box spans across the page from the text margin on its side out to its `w:tblW` width. For each floating table, at least one line of the paragraph after it lies outside the box's span, at a height within the table's rows. The first block after the group's clearing break starts below the table's lowest text. The text of each cell of `#tbl-wide` lies inside its box's span.
- [ ] AC4: The user opens `tests/tables.docx` in Microsoft Word on the Mac. The user finds each floating table at its side, with body text beside it and its caption inside its box. The user finds the text after each group's clearing break below the table.
- [ ] AC5: Two searches find the candidate lines: `grep -rn -i 'table' docs --include='*.qmd'` outside `docs/_site` and `docs/_freeze`, and `grep -n -i 'table' README.md`. No paragraph that holds a found line says that a table float keeps its normal layout in Word, or that a table float wraps only in HTML and Typst. `docs/formats/word.qmd` says that a wrapped table float sits in a floating table with its caption inside it. The page also states how a table wider than its box renders, and names the app whose render shows it.
- [ ] AC6: `python3 tests/verify.py` exits 0 with each render passing, and `quarto render docs` exits 0.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T3
- AC3 → T2, T4
- AC4 → T6
- AC5 → T5
- AC6 → T6

## Tasks

- [ ] T1: `wrapped.lua`: let a table float wrap in Word. In `float_target` (near line 1565), narrow the LaTeX and Word table warning to LaTeX, with the new sentence. Give a Word table float its frame through `docx_frame`, so that the grouping pass marks its group with `data-wrap-frame`. Update the comments that say a Word frame cannot hold a table.
- [ ] T2: `wrapped-docx.lua`: in `frame_first`, find Quarto's one-cell table that holds a `tbl-` div, alone or in a code cell div. Replace it with the floating-table open tag, the cell's blocks, and the close tag. Fit the inner table to the box width. Keep the clearing break. Update the header comment.
- [ ] T3: `tests/verify.py`: make `docx_summary` list each floating table, with its side, width, gap, bookmark, caption style, and the blocks after it up to the clearing break. Run `--update`, and read the snapshot diff for `tables`, `fixture`, `contexts`, and `tables-cell-columns`. Plant one defect for each axis and see the check fail for each: the wrong side, a dropped `w:tblpPr`, the caption moved out of the cell, a dropped bookmark, and a dropped clearing break. Cover at least one div float and one code-cell float. Fix the prose of `tests/fixture.qmd` (lines 214, 223, and 231) that says a table keeps a normal layout in Word.
- [ ] T4: Convert `tests/tables.docx` to PDF with LibreOffice, and read the AC3 coordinates with `pdftotext -bbox`. If the wide table runs past its box, fix the fit. Record the coordinates in the Review section's evidence.
- [ ] T5: Docs and README: change each paragraph that the AC5 searches find. Write the wrapped-table text and its limits in `docs/formats/word.qmd`. Update E5 and the Word mechanism text in `cairn/DESIGN.md`, and the W4 row of `cairn/references/wrap-mechanisms.md`.
- [ ] T6: Run `python3 tests/verify.py` and `quarto render docs`. At review, stop once for the user's look in Word, and record the user's report in the Review section.

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

## Decisions

## Review
