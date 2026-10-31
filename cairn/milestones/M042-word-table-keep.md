# M042: Keep short Word table boxes on one page

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes where a wrapped table lands on the page in Word documents.
- **Branch/PR:** —

## Goal

In Word, a wrapped table box that the filter estimates at no more than half the page's text height stays whole on one page.

## Scope

**In:** a height estimate for the box of each wrapped table float in Word, in `_extensions/wrapped/wrapped-docx.lua`. A `w:cantSplit` on the box's one row when the estimate is at most half the page's text height. The page's text height from the reference doc. A committed probe document that Word and LibreOffice export to PDF. Snapshot fixtures for the new row state. The Word page of the site and the Word Known issue in `cairn/DESIGN.md`.

**Out:** a warning for a box that the filter judges too tall. The plan gate chose no warning, and no record holds it as later work. An opt-in attribute that keeps a box whole. The plan gate did not choose it, and no record holds it as later work. Word figure frames, which already move whole. Other formats. The table spacer and raw-table edge cases stay in the candidate row "Fix Word table box edge cases".

## Acceptance criteria

- [ ] AC1: In Word, `wrapped-docx.lua` writes `<w:trPr><w:cantSplit /></w:trPr>` in the one row of a box if the box's height estimate is at most half the page's text height. Otherwise that row has no `w:trPr`. The text height is the body `w:pgSz` height of the reference doc, less its `w:pgMar` top and bottom. With no readable reference doc, or a body `w:sectPr` with no `w:pgSz` height or no `w:pgMar` top and bottom, the text height is 12960 twips (9 in).
- [ ] AC2: In the PDF that Microsoft Word 16.114 writes from the committed probe document `tests/docx-page-probe.qmd`, no box whose row has `w:cantSplit` is taller than the page's text height. The probe varies each input of the estimate. It has Pandoc tables with short and long cell text, a gt table, a flextable table, a box with an image, and a caption over several lines. It also has boxes whose estimate is between 0.3 and 0.5 of the text height, at two box widths, and under a reference doc with a larger body font.
- [ ] AC3: In the docx of `tests/docx-tables.qmd`, the box rows of `tbl-after-table`, `tbl-image`, `tbl-raw`, `tbl-gt`, `tbl-flex`, and `tbl-flex-auto` cannot split. The box rows of three new cases can split: a 69-row Pandoc table, a box whose image alone is taller than half the page, and a 40-row raw openxml table.
- [ ] AC4: In a new docx fixture, one box is the same as a box of AC3 whose row cannot split. Its row can split under a reference doc with a Letter width and a shorter page height. Its row can also split under a reference doc with a Letter page whose `w:pgMar` top and bottom alone leave less than twice its estimate.
- [ ] AC5: In the PDFs that Word 16.114 and LibreOffice 26.8 write from `tests/docx-page-probe.qmd`, a short box that does not fit at a page's bottom has its caption and every row on the next page. A 69-row box in that probe shows all 69 rows.
- [ ] AC6: The Tables section of `docs/formats/word.qmd` and the Word table-width entry of the Known issues in `cairn/DESIGN.md` say two things. A box up to about half the page's text height moves whole to the next page. A taller box can break across pages. Each line about a Word table box that `grep -rnE "across pages|next page|split" README.md docs/*.qmd docs/formats/*.qmd cairn/DESIGN.md` finds agrees with that.
- [ ] AC7: `python3 tests/verify.py` passes. `quarto render docs` and `python3 tests/docs_layout.py` exit 0.

## Coverage

- AC1 → T2, T3
- AC2 → T1, T2, T4
- AC3 → T3
- AC4 → T3
- AC5 → T1, T4
- AC6 → T5
- AC7 → T6

## Tasks

- [ ] T1: Write `tests/docx-page-probe.qmd` with the boxes that AC2 and AC5 name, and a short reference doc set up in `tests/reference_narrow.py`. Export it with `tests/word-pdf.applescript` and with `soffice`. Measure each box's height in the Word PDF with `pdftohtml -xml`, and record the heights in the work log. Read Quarto's default reference doc for the body font size and line spacing that the estimate assumes.
- [ ] T2: In `wrapped-docx.lua`, estimate a box's height at the box width: each paragraph by its text lines, each table row (Pandoc or raw openxml) by its tallest cell, and each image by its own aspect ratio (`pandoc.image.size` on the mediabag item). Read the page's text height from the reference doc, beside the text-width reader in `wrapped.lua` (`read_docx_text_width`, line 639), and pass it to the post-render pass. Write the `w:trPr` of AC1 in `floating_table` (line 294). Keep the estimate at or above the T1 heights.
- [ ] T3: Add `keep=yes|no` for the box row to each line of `docx_tables` in `tests/verify.py`. Add the three cases of AC3 to `tests/docx-tables.qmd`. Add the AC4 fixture and its two reference docs to `tests/reference_narrow.py` and to the docx fixture list. Update the snapshots and review the diff.
- [ ] T4: Re-export the probe after T2, in Word and LibreOffice. Check AC2 against each box's state in the probe's docx. Check AC5 with `pdftotext` on each PDF.
- [ ] T5: Update the Tables section of `docs/formats/word.qmd`, the Word table-width Known issue and the Word mechanism paragraph in `cairn/DESIGN.md`, and every line the AC6 search finds about a Word table box.
- [ ] T6: Run `python3 tests/verify.py`, `quarto render docs`, and `python3 tests/docs_layout.py`.

## Work log

- 2026-10-31: created by /milestone-plan.
- 2026-10-31: tier check: milestone — it changes a documented Word page-break limit and needs a design choice, so it is not a hotfix.
- 2026-10-31: idea vet: flaw — a `w:cantSplit` on every box row cuts off the rows of a box taller than a page in Word 16.114 (rows 38 to 69 of 69 lost) and LibreOffice 26.8 (rows 36 to 69 lost), in a scratch probe; "keep with next" on the box's paragraphs did not keep a box whole in either app. The set chose a height estimate that keeps only boxes at most half the page's text height whole.
- 2026-10-31: plan gate chose the height estimate over an opt-in attribute because it fixes the default for every short box with no new option; falsified by a Word PDF where a box with `w:cantSplit` is taller than the page's text height, or loses rows.
- 2026-10-31: plan gate chose no warning for a box judged too tall over one warning per box, because a long table breaking across pages is normal in Word; falsified by a user report that a broken box was unexpected.
- 2026-10-31: question set: may checks open Microsoft Word through `tests/word-pdf.applescript` to export PDFs — yes (asked in the first plan run of this session, which wrote no file).
- 2026-10-31: criteria audit (full mode, Opus reader): 6 findings, all fixed. AC1 now covers a missing reference doc and a `w:pgMar` with no top or bottom. AC2 promises the Word layout over a committed probe that varies width, font, and the 0.3 to 0.5 band, and no longer binds a work-log record. AC3 names its box ids. AC4 varies page height and margins apart, at a Letter width. AC5 names the same committed probe and promises the layout, not a record. AC6 names the table-width entry and searches for "next page" and "split" too. AC7: none.
- 2026-10-31: lessons used: 2026-10-25 (M004, used M040), 2026-10-26 (M007, used M041), 2026-10-27 (M012, used M041), 2026-10-31 (M039, used M041), 2026-10-31 (M041).
- 2026-10-31: test scope: the snapshot tests of AC3 and AC4 cover the new row state in CI. Word and LibreOffice layout (AC2, AC5) is checked by hand on the Mac, because CI has no Word. No changelog entry, because `cairn/PROFILE.md` names none.

## Decisions

## Review
