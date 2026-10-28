# M019: Wrap figures in Typst columns

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the README gains claims about wrapped figures in Typst documents with `columns:` set
- **Branch/PR:** m019-typst-columns

## Goal

In PDF through Typst, a document with `columns:` set wraps each wrapped
figure inside its column, and the README says so.

## Scope

**In:** Quarto 1.10.19's Typst template sets `set page(columns: …)` from
the `columns:` option (`share/formats/typst/pandoc/quarto/page.typ:11`).
Inside a page column, `layout` gives the column's size. So the filter's
`wrapped-width` and a percent width read the column width
(`_extensions/wrapped/wrapped.lua:573`, `TYPST_HEADER`). A scratch render
on 2026-10-28 with `columns: 2` put each wrapped figure in its column, with
the text beside it. A group too tall for the rest of the first column
started the second column. So no filter change is expected. The work adds
the fixture `tests/typst-columns.qmd` and its snapshot. It adds the
fixture's `TYPST_LAYOUT` cases to `tests/verify.py`, with a reader for each
column's edges. It updates the README section "PDF through Typst" and the
Typst page-bottom entry in `cairn/DESIGN.md` Known issues. It updates row
W3 of `cairn/references/wrap-mechanisms.md` and adds an edge-case row
there. If a case shows that a figure does not wrap in a column, implement
stops for an amendment.

**Out:** LaTeX columns keep M009's fallback. For `multicols`, the
candidate row "Keep wrapped figures in multicols" holds the next step. A
moved group leaves the end of its column blank, because wrap-it's box does
not break. The Known issues entry already names this limit for pages. This
milestone extends the entry to columns and does not fix the limit. A Typst
`#columns()` call in a raw block is not tested, and the README claims only
`columns:`.

## Acceptance criteria

The fixture is `tests/typst-columns.qmd`, rendered to PDF through Typst
with `columns: 2` under `format: typst` and no `wrapped:` metadata. Its
cases are `TYPST_LAYOUT` cases of `tests/verify.py`, which read the PDF
with `pdftohtml -xml` at 1.5 px for each pt. Each column's left and right
edges come from that column's full lines on the fixture's first page. That
page holds text in both columns and no image, and the title does not count.
An image **in** a column has its left and right within that column's
edges. Four tests make a paragraph **beside** a figure. Its first line is
on the figure's page. That line overlaps the image's height. The line does
not overlap the image across. The line lies within the edges of the column
that holds the image. Each test allows `NEAR` (3 px).

- [ ] AC1: In the fixture, a captioned figure and an uncaptioned image in
      the first column, and a captioned figure in the second column, each
      have their paragraph beside them. The render prints no warning that
      starts with `wrapped:`.
- [ ] AC2: In the fixture, the image of a figure with `width="40%"` is
      124 px wide, 40% of the 311 px column. Quarto 1.10.19's default Typst
      page has 648 px of text, and the column is half of that less Typst's
      default gutter of 4%. An image with `width="1in"` is 108 px wide.
      Each width allows `NEAR`.
- [ ] AC3: In the fixture, a figure whose width plus its gap is wider than
      its column and narrower than the page's text has a 124 px image,
      within `NEAR`, and its paragraph is beside it.
- [ ] AC4: In the fixture, one wrapped figure's group does not fit in the
      rest of the first column. Its image is in the second column of the
      same page, and no text line of that column ends above the image's
      top. Its paragraph is beside it.
- [ ] AC5: The README section "PDF through Typst" states four facts for a
      document with `columns:` set, such as `columns: 2`. A wrapped figure
      wraps inside its column. A percent width, and the check of a width
      plus its gap, use the column's width. A figure with the text beside
      it that does not fit at the bottom of a column moves to the next
      column. The rest of that column stays blank. A search of the section
      for `text width` finds no sentence that leaves out the column width
      for such a document.
- [ ] AC6: `python3 tests/verify.py` exits 0 locally and in the verify
      workflow on the PR. Against `main`, `_extensions/wrapped/` is
      unchanged, and each fixture on `main` renders to the output that its
      snapshot on `main` records.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T1, T4

## Tasks

- [x] T1: Write `tests/typst-columns.qmd` with `columns: 2`,
      `keep-typ: true`, and `fig-format: png`. Its title is narrower than
      a column. Its first page holds text in both columns and no image.
      After a raw `#pagebreak()` block come the cases of AC1 to AC4. Each
      paragraph opens with marker words and leaves about 1 in of text
      beside its figure. Add the fixture to the render list in
      `tests/verify.py` with a snapshot.
- [x] T2: In `tests/verify.py`, add a reader for each column's edges from
      page 1's full lines, with the title left out. Add
      `typst_columns_cases` to `TYPST_LAYOUT` for AC1 to AC4. A page holds
      more than one image, so find each image by the paragraph beside it.
      Join the boxes that share a line's top before a search for marker
      words. Make each new test fail once on a planted change, with the
      reason the test names, then restore the fixture. Drop a wrap class
      for the height test. Move the second-column case into the first
      column for the column test. Change a width for the width test.
      Shorten the text before AC4's figure so that its group fits. Leave
      one column of page 1 empty for the edge reader. Write the snapshot
      with `--update` and read it.
- [ ] T3: Update the README section "PDF through Typst" for AC5, its
      `text width` sentences included. Update the Typst page-bottom entry
      in `cairn/DESIGN.md` Known issues for columns. Update row W3 of
      `cairn/references/wrap-mechanisms.md` and add an edge-case row there
      for Typst `columns:`.
- [ ] T4: Run `python3 tests/verify.py`. Compare `_extensions/wrapped/`
      and `tests/_snapshots/` with `main`.

## Work log

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: not run — work named at the question set.
- 2026-10-28: question set: which work to take — "Check wrapped figures in Typst columns"; go on to implement after the plan — yes.
- 2026-10-28: idea vet: no concern. A scratch render with `columns: 2` wrapped each figure inside its column with a 40% width of the column, so wrapping is correct there, and DESIGN's goal keeps a normal figure only where a format cannot wrap. LaTeX falls back in columns because wrapfig cannot wrap there, so the formats differ by what each can do.
- 2026-10-28: collision check: absorbed the candidate row "Check wrapped figures in Typst columns" (from M005). M005 left the case out; M009 covers LaTeX columns only. The row "Keep wrapped figures in multicols" is LaTeX and stays apart. D-004 read whole, no conflict.
- 2026-10-28: inbox sweep: 0 open issues and 0 open PRs on jmgirard/wrapped.
- 2026-10-28: lessons used: 2026-10-25 (M002) fixture symlink and `fig-format: png`; 2026-10-25 (M005) wrap-it's box does not break; 2026-10-27 (M011) about 1 in of text beside a Typst figure; 2026-10-27 (M012) the one-fixture check command.
- 2026-10-28: criteria audit (full mode, fresh Opus reader with a scratch render): 8 findings, all fixed. A title across both columns broke the edge reader, so the edges come from each column's lines with the title left out. Text edges run 3 to 7 px past the true column, so AC2 and AC3 state 124 px from the 311 px column. AC5 gained the blank-column fact and the `text width` search. AC6 bound the snapshot files, an instrument, and now binds unchanged `_extensions/wrapped/` and unchanged output. T2's plants now cover each test, and the edge reader. "In a column" and "above the image" are defined. Images are found by paragraph and boxes joined by line top. AC5 names `columns: 2` as the example, since only 2 is tested.
- 2026-10-28: plan gate chose to test and document wrapping in Typst columns over a normal figure with a warning, as LaTeX does, because the scratch render wrapped each figure inside its column; falsified by a render where a figure in a Typst column overlaps text or leaves its column.
- 2026-10-28: surface tier: user-facing, because the README gains claims users rely on.
- 2026-10-28: implement started; branch m019-typst-columns cut from main at 0ddbcde.
- 2026-10-28: T1 minor amendment: the fixture uses raw `#pagebreak()` and `#colbreak()` blocks. A `{{< pagebreak >}}` after a wrapped paragraph joins the wrap group and fails the Typst render, a filter bug outside this scope, now the candidate row "Keep page breaks out of Typst wraps".
- 2026-10-28: T1 done: `tests/typst-columns.qmd` renders with no warning. Images measure 124 px (40%, 40% in column 2, 2.9in fallback, moved group) and 108 px (1in); the moved group starts column 2 of page 3. Added to RENDERS with its snapshot.
- 2026-10-28: T2 choice: `column_edges` splits page 1 at the middle of its text and lets text cross the middle only above the columns (the title); `column_of` puts a box in the column whose left edge is the last at or left of it, so a line that runs past its column's right edge still fails the edge test. Fixtures in `COLUMN_LAYOUT` take these edges in `layout_check`.
- 2026-10-28: T2 done: 5 `typst_columns_cases` pass. Plants, each red with its test's reason, then restored: no wrap class ("not beside the image"), second case in column 1 ("not inside column 2", 2 cases), 30% width ("93 px wide, not 124 px"), short filler ("not inside column 2"), page 1 in one column ("a column of page 1 has no text"), a -60pt gutter in `wrapped.lua` ("overlaps the figure", 5 cases), a colbreak before the moved figure ("8 lines of column 2 end above the image"). The restored render matches its snapshot.

## Decisions
