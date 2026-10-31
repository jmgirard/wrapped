<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M041: Wrap gt and flextable tables in Word

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the filter's Word output, which users install from `main`
- **Branch/PR:** m041-word-raw-tables

## Goal

A `#tbl-` table float whose table is raw Word XML, as gt and flextable write it, wraps the paragraphs after it in Word, with the table set to the full width of its box.

## Scope

**In:** In `wrapped.lua`, a Word table float whose content holds a raw
openxml table no longer keeps its normal layout, and its warning goes
(`raw_docx_table` and its check). In `wrapped-docx.lua`,
`floating_table` fits each raw openxml block in the box that holds a
`w:tbl`: the block's first table gets a `w:tblW` of type `dxa` equal to
the box width, in place of gt's `auto` or flextable's `pct` width, with a
`w:tblPr` added when the table has none. When that table has a
`w:tblGrid`, as flextable's fixed layout writes, its `w:gridCol` widths
scale to sum to the box width in their own proportions, and each
`w:tcW` of type `dxa` in the table scales by the same ratio. A probe on
2026-10-31 (Quarto 1.10.20, gt 1.4.0, flextable 0.10.1, a scratch copy of
the filter) showed a gt table, a flextable with a merged header, and an
autofit flextable each set at its side with text beside it in LibreOffice
and in Word. Tests, the site pages, README.md, DESIGN.md, and
`cairn/references/wrap-mechanisms.md` follow. D-025 supersedes D-023.

**Out:**
- An image in a gt or flextable cell: in a Quarto Word render, flextable
  writes the image as `r:embed="plot.png"` with no relationship or media
  part (probe), so no image shows, with or without the filter. That is
  flextable's and Quarto's to fix; no row.
- A hand-written raw openxml block that holds more than one table, or a
  table nested in a cell: only the block's first table is fitted. gt and
  flextable write one table for each block; no row, since no documented
  or common use reaches it.
- Running gt and flextable in CI: the CI setup installs knitr and
  rmarkdown only, and adding packages is a dependency change that the
  plan did not ask for. The fixture cases copy the XML that the packages
  write, and `tests/docx-raw-tables.qmd` renders the packages by hand.
- Wrapping raw LaTeX tables: the candidate row "Wrap raw LaTeX tables
  from R packages".
- Column and image sizing in Pandoc tables: the candidate row "Size
  images and columns in Word tables".

## Acceptance criteria

- [ ] AC1: In the docx of `tests/docx-tables.qmd`, each of four table floats whose table is a raw
      openxml block is a floating table (`w:tblpPr`) on its class's side, whose `w:tblW` is the box
      width that its class sets, whose inner table has a `w:tblW` of type `dxa` equal to that box
      width, and whose next paragraph comes before the clearing break that ends its wrap. The four
      are `tbl-raw`, a hand-written table with no `w:tblPr`; `tbl-gt`, in the form gt 1.4.0 writes
      (`w:tblW` `auto`, no `w:tblGrid`); `tbl-flex`, in the form flextable 0.10.1 writes by default
      with one column set wider (`w:tblLayout` `fixed`, a `w:tblGrid` of uneven widths, a header
      cell that spans two columns); and `tbl-flex-auto`, in the form flextable 0.10.1 writes with
      `layout = "autofit", width = 1` (`w:tblW` `pct` 5000, no grid).
- [ ] AC2: In the docx of `tests/docx-tables.qmd`, for `tbl-raw` and `tbl-flex`, whose source grids
      have uneven widths, the `w:gridCol` widths of the inner table sum to exactly the box width, and
      each is within 1 twip of the box width times that column's share of the grid sum in the
      fixture's source. Each `w:tcW` of type `dxa` in `tbl-raw`, whose source gives its cells
      uneven ones, is within 1 twip of its source width times the ratio of the box width to the
      source grid sum.
- [ ] AC3: The Word render of `tests/docx-tables.qmd` prints one warning, the image-height warning
      for `plot.png` that it printed at commit f207fe3, and no other.
- [x] AC4: In a LibreOffice PDF (`soffice --headless --convert-to pdf`) and in a Microsoft Word PDF
      (`tests/word-pdf.applescript`) of the Word render of `tests/docx-raw-tables.qmd`, which wraps a
      gt 1.4.0 table, a default flextable 0.10.1 table, and an autofit flextable 0.10.1 table, each
      followed by a paragraph, the `pdftohtml -xml` text boxes show, for each of the three tables,
      the paragraph's first line starting above the bottom of the lowest text box of the table's
      last row, and none of that line's text boxes overlapping the horizontal span of the table's
      cell text boxes (its caption excluded). `tests/word-pdf.applescript` also saves the Word
      render of `tests/docx-tables.qmd` as PDF with exit status 0.
- [x] AC5: No sentence that holds a line found by
      `grep -rn -i -E 'flextable|Word XML|openxml|raw Word' README.md docs cairn/DESIGN.md cairn/references/wrap-mechanisms.md --include='*.qmd' --include='*.md'`
      says that a gt or flextable table, or a raw Word XML or openxml table, keeps its normal
      layout in Word or makes the render warn in Word. The Tables section of
      `docs/formats/word.qmd` says that a gt or flextable table is set to the full width of its box
      and that a flextable with its default fixed layout keeps its columns' proportions.
- [ ] AC6: `python3 tests/verify.py` passes every render, snapshot, layout case, and log check;
      `quarto render docs` exits with status 0; and `python3 tests/docs_layout.py` exits with
      status 0.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T2, T3
- AC4 → T1, T4
- AC5 → T5
- AC6 → T6

## Tasks

- [x] T1: Fixtures first. In `tests/docx-tables.qmd`, rewrite `tbl-raw` with no `w:tblPr`, uneven
      grid columns (such as 1000 and 3000), and uneven `dxa` `w:tcW` cells, and change its
      after-paragraph's "keeps its normal layout" text; add `tbl-gt`, `tbl-flex` (one column set
      wider), and `tbl-flex-auto`, each a raw openxml block copied from gt 1.4.0 or flextable 0.10.1
      output (cut to three rows), with a paragraph after it. Add `tests/docx-raw-tables.qmd` with gt
      and flextable code cells, outside `verify.py`'s fixture list, its header naming the packages
      it needs. In `tests/verify.py`'s `docx_tables`, record each inner table's `w:gridCol` widths
      and `dxa` `w:tcW` widths in the snapshot.
- [x] T2: In `wrapped.lua`, remove `raw_docx_table` (about line 1732) and its check (about line
      1850). In `wrapped-docx.lua`, fit each raw openxml block that holds a `w:tbl` from
      `floating_table`'s walk: replace or add the first table's `w:tblW` in schema order (adding a
      `w:tblPr` when the table has none), and scale its first `w:tblGrid` and its `dxa` `w:tcW`
      widths by rounding the running column edges to the nearest twip, so that each column is
      within 1 twip of its share and the sum is exact. Update both files' header comments.
- [x] T3: Run `python3 tests/verify.py --update` and read the snapshot diff. Plant each defect in
      turn (no `w:tblW` change, no grid scaling, equal columns in place of scaled ones, no `w:tcW`
      scaling, the raw check restored) and see the `docx-tables` snapshot go red.
- [x] T4: Render `tests/docx-raw-tables.qmd` to Word; make its LibreOffice and Word PDFs and read
      the `pdftohtml -xml` boxes for AC4; save the docx of `tests/docx-tables.qmd` as PDF through
      Word.
- [x] T5: Docs: the Tables section of `docs/formats/word.qmd`, `docs/normal-layout.qmd`,
      `docs/get-started.qmd`, `docs/reference.qmd`, `docs/index.qmd`, README.md, DESIGN.md (the
      non-goals, the warnings list, the Word paragraph, the D-023 line near line 251), and the E5
      row of `cairn/references/wrap-mechanisms.md`; then `quarto render docs`.
- [x] T6: Run `python3 tests/verify.py`, `quarto render docs`, and `python3 tests/docs_layout.py`.

## Work log

- 2026-10-31: created by /milestone-plan.
- 2026-10-31: tier check: not run — work named at the question set.
- 2026-10-31: question set: what to work on — "Wrap gt and flextable tables in Word".
- 2026-10-31: idea vet: no concern found; `docs/formats/word.qmd` already says the filter sets a wrapped table to the full width of its box, which covers raw tables, and a flextable image never reaches a Quarto Word file (probe), so images are out with no row.
- 2026-10-31: lessons used: 2026-10-31 (M039), 2026-10-27 (M012), 2026-10-29 (M034).
- 2026-10-31: collision check: the candidate row "Wrap gt and flextable tables in Word" is absorbed (started M041); D-023 is superseded by D-025 in the plan commit; M039 (done) shipped the normal-layout narrowing this reverses; no checker-regress shape. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-31: plan chose rewriting the raw XML text in the post-render pass over converting it to a Pandoc table, because the conversion would drop gt's and flextable's styling; falsified by a gt or flextable release whose XML the text rewrite cannot fit (Word asks to repair the file, or no text sits beside the table).
- 2026-10-31: plan chose a `dxa` box width for the raw table's `w:tblW` over `pct` 5000 as Pandoc's inner tables take, because the probe tested `dxa`; falsified by Word or LibreOffice setting a `dxa`-width raw table wider or narrower than its box.
- 2026-10-31: plan chose fixtures that copy the packages' XML over installing gt and flextable in CI, because that is a dependency change the plan did not ask for; falsified by a gt or flextable release whose XML differs from the copied forms in `w:tblW`, `w:tblGrid`, or `w:tcW`.
- 2026-10-31: criteria audit (full mode, fresh Opus reader): 9 findings, all fixed. AC1 now states docx properties, not snapshot lines; `tbl-raw` and `tbl-flex` get uneven grids and T3 an equal-columns plant; scaling rounds running edges, so each column stays within 1 twip; AC3 names the one warning at f207fe3; D-025 lands in the plan commit; AC4 measures the lowest text box of the last row, caption excluded; AC5's grep adds `openxml|raw Word`, judges sentences, and drops its catch-all; AC5 limits proportions to the fixed-layout flextable; `tbl-raw` has no `w:tblPr` and AC4 has Word open the `docx-tables` render. AC6 passed.
- 2026-10-31: implement started on `m041-word-raw-tables`; the uncommitted `tests/.gitignore` lines (`/.quarto/`, `**/*.quarto_ipynb`, from an earlier render) are not this milestone's and stay unstaged.
- 2026-10-31: T1: `tests/docx-tables.qmd` has `tbl-raw` (no `w:tblPr`, grid and `dxa` cells 1000/3000) and `tbl-gt`, `tbl-flex` (grid 2880/1080/1080, a two-column header cell), and `tbl-flex-auto`, copied with whitespace between tags removed from gt 1.4.0 and flextable 0.10.1 output; `tests/docx-raw-tables.qmd` renders the packages by hand; `docx_tables` records `grid=` and `tcw=`. The fixture inserts went through a Python script, since the copied XML runs to 31 KB. On the current filter all four warn and stay normal.
- 2026-10-31: T2: `raw_docx_table` and its warning are gone; `fit_raw` in `wrapped-docx.lua` runs from `floating_table`'s walk. It finds the first `<w:tbl>` or `<w:tbl ...>` tag (a first pattern ran past a bare `<w:tbl>` into `<w:tblGrid>`, fixed), puts `w:tblW` after any `BEFORE_TBLW` element, scales the grid by rounded edges, and scales depth-1 `dxa` `w:tcW` by a scanner that stops at the table's end. Scratch render: `tbl-raw` grid and cells 936/2808, `tbl-flex` grid 2139/803/802, all four `dxa 3744`, one warning (image height). The new `grid=` field also shows the grid Pandoc writes for its own tables (3960 per column in a 3744 box), unchanged by this milestone.
- 2026-10-31: T3 started: `python3 tests/verify.py --update` running in the background.
- 2026-10-31: T4 (gt and flextable part): `tests/docx-raw-tables.qmd` now sets `echo: false`, since with its code shown the third box broke across pages. Rendered from a scratch folder linked to `_extensions/`; LibreOffice and Word 16.114.3 PDFs, one page each. A `pdftohtml -xml` script (scratchpad `measure.py`, matching cells by digits and short words, since LibreOffice's PDF loses letters) found, for all three tables in both PDFs, the paragraph's first line above the last row's lowest box and no overlap with the cell boxes: Word line tops 362, 567, 851 against row bottoms 487, 790, 1016; LibreOffice 328, 542, 820 against 451, 694, 984. The Word save of `docx-tables.docx` waits for the suite.
- 2026-10-31: finding outside scope: with the code shown, a box at a page's bottom broke across pages in Word 16.114 and LibreOffice, a limit the site named for LibreOffice only. `docs/formats/word.qmd` and the DESIGN.md Known issue now name Word too; candidate row "Keep Word table boxes on one page" added at normal (search-first: no row held it; the Known issue held the LibreOffice half).
- 2026-10-31: T5: README.md, `docs/index.qmd`, `docs/get-started.qmd` (two passages), `docs/reference.qmd`, `docs/normal-layout.qmd` (bullet removed), `docs/formats/word.qmd` Tables, DESIGN.md (goals, warnings, non-goals, the pass list near line 251, the Word paragraph), and the E5 row now say gt and flextable tables wrap in Word. The AC5 grep's remaining hits say they wrap, or are about other raw OpenXML. The simple-english hook flags a "would" in `wrap-mechanisms.md` that is a quoted Typst error, left as it is.
- 2026-10-31: T3: `python3 tests/verify.py --update` passed all 128 renders. Snapshot diff: `docx-tables` drops the raw-XML warning and lists `tbl-raw` `dxa 3744 grid=936,2808 tcw=936,2808`, `tbl-gt` and `tbl-flex-auto` `dxa 3744`, `tbl-flex` `dxa 3744 grid=2139,803,802`; the Pandoc tables in `docx-tables`, `contexts`, `fixture`, and `tables` gain only `grid=` with Pandoc's own widths. Plants (scratchpad `plants.py`, each file restored from git): `pct 5000` in place of `dxa` red on all four; no grid scaling red on `tbl-raw` and `tbl-flex` (1000,3000 and 2880,1080,1080); equal columns red (1872,1872 and 1248,1248,1248); no `w:tcW` scaling red (`tcw=1000,3000`); `main`'s `wrapped.lua` red (four warnings). The restored render matches the snapshot.
- 2026-10-31: T4 done: `tests/word-pdf.applescript` saved the Word render of `tests/docx-tables.qmd` as a 5-page PDF, exit 0; its text shows each raw table's paragraph beside its caption.
- 2026-10-31: T6 checkpoint: `quarto render docs` exit 0 (it refreshed `docs/_freeze/get-started`, since that page's prose changed); `python3 tests/docs_layout.py` exit 0; `python3 tests/verify.py` running in the background; the claim audit's reader is running.
- 2026-10-31: T6: `python3 tests/verify.py` passed all 128 renders on 3a15971.
- 2026-10-31: claim audit: 43 claims read, 4 corrected — _extensions/wrapped/wrapped-docx.lua, docs/formats/word.qmd, cairn/DESIGN.md. Two were code defects outside gt's and flextable's output: `element_end` missed an element with a closing tag and no attributes, so `w:tblW` went before `<w:bidiVisual></w:bidiVisual>`, and a self-closing `<w:tblPr/>` got a second `w:tblPr` and an unscaled grid. Fixed, with regression cases `tbl-raw-bidi` and `tbl-raw-empty-pr` in `tests/docx-tables.qmd` and a `tblW-before=` field in `docx_tables`; on 3a15971's filter they rendered `tblW-before=bidiVisual` and `grid=1000,2000`, and now `grid=1248,2496` with no order field. The comment now says a gridless table keeps its `w:tcW` widths, and the Word page says gt and autofit flextable columns are sized "at the width of the box", not "within" it, since no render had long unbreakable cell text.
- 2026-10-31: T6 done on a974db8: `python3 tests/verify.py` all 128 renders pass; `quarto render docs` exit 0; `python3 tests/docs_layout.py` exit 0. Status set to review.

## Decisions

## Review

Review pass 1 on d91f006 (2026-10-31).

- AC4 evidence: a fresh render of `tests/docx-raw-tables.qmd` (gt 1.4.0, flextable 0.10.1) from a scratch folder linked to `_extensions/`; LibreOffice and Word 16.114.3 PDFs, one page each. The scratchpad `measure.py` reading of `pdftohtml -xml` boxes: Word, first-line tops 362, 567, 851 against last-row bottoms 487, 790, 1016; LibreOffice 328, 542, 820 against 451, 694, 984. No first-line box overlaps the table's cell boxes in either PDF. The Word save of `docx-tables.docx` is under AC1.
- AC5 evidence: the criterion's grep finds 17 lines in README.md, `docs/`, DESIGN.md, and `wrap-mechanisms.md`. Read in their sentences, each says a gt or flextable table wraps in Word, or is about raw OpenXML in another sense (DESIGN.md:386 split tags; `wrap-mechanisms.md`:64 and :231 on images and frames); none says such a table keeps its normal layout or warns in Word. `docs/formats/word.qmd` Tables says the filter sets it to the full width of the box and that a flextable with its default fixed layout keeps its columns' proportions.
