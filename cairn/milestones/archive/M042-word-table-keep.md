# M042: Keep short Word table boxes on one page

**Status:** dropped (2026-10-31, at the user's choice in the re-plan's question set)

**Goal:** In Word, a wrapped table box that the filter estimates at no more than half the page's text height stays whole on one page.

**Reason dropped:** every box form that keeps rows together hides rows in LibreOffice 26.8 near a page's bottom, and no form tried keeps the caption with the first rows in LibreOffice, so the user kept today's splittable box, which loses no rows in either app.

**Outcome:** implement (branch `m042-word-table-keep`, 5 commits, kept unpushed on the user's Mac) built a height estimate (`blocks_height` in `wrapped-docx.lua`), a page reader (`read_docx_page` in `wrapped.lua`) that adds the text height and font size to the frame string, a `w:cantSplit` on the box row of an estimated short box, the probe `tests/docx-page-probe.qmd`, and fixtures. Word 16.114 moved a short box whole and kept all 69 rows of a tall one. LibreOffice 26.8 hid rows 7 and 8 of the probe's `near` box, which stayed on its page; `w:tblOverlap` never, a `w:tblpY`, and `w:keepLines` on the next paragraph each left it clipped. The user stopped implement for a re-plan.

**Re-plan probe:** one 8-row box at 14 positions near a page's bottom, six box forms, PDFs from Word 16.114 and LibreOffice 26.8. Today's one-row box lost no rows in either app and left the caption and header row alone at 2 positions in each. "Keep with next" on the caption or on the first inner rows, and a caption in its own unsplittable box row, changed neither app. `w:cantSplit` on the one row kept the box whole at all 14 positions in Word and hid rows at 2 positions in LibreOffice. An unsplittable first row holding the caption, header, and 2 rows, over a splittable row with the rest, worked in Word and hid rows at 2 positions in LibreOffice. LibreOffice anchors the box as a frame that can break across pages, on the paragraph beside it, and clips an unsplittable row that does not fit there.

**Decisions:** none. The parked row "Keep Word table boxes on one page" holds the idea, with its promotion condition.
