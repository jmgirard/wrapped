# M019: Wrap figures in Typst columns

- **Status:** review
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

- [x] AC1: In the fixture, a captioned figure and an uncaptioned image in
      the first column, and a captioned figure in the second column, each
      have their paragraph beside them. The render prints no warning that
      starts with `wrapped:`.
- [x] AC2: In the fixture, the image of a figure with `width="40%"` is
      124 px wide, 40% of the 311 px column. Quarto 1.10.19's default Typst
      page has 648 px of text, and the column is half of that less Typst's
      default gutter of 4%. An image with `width="1in"` is 108 px wide.
      Each width allows `NEAR`.
- [x] AC3: In the fixture, a figure whose width plus its gap is wider than
      its column and narrower than the page's text has a 124 px image,
      within `NEAR`, and its paragraph is beside it.
- [x] AC4: In the fixture, one wrapped figure's group does not fit in the
      rest of the first column. Its image is in the second column of the
      same page, and no text line of that column ends above the image's
      top. Its paragraph is beside it.
- [x] AC5: The README section "PDF through Typst" states four facts for a
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
- [x] T3: Update the README section "PDF through Typst" for AC5, its
      `text width` sentences included. Update the Typst page-bottom entry
      in `cairn/DESIGN.md` Known issues for columns. Update row W3 of
      `cairn/references/wrap-mechanisms.md` and add an edge-case row there
      for Typst `columns:`.
- [x] T4: Run `python3 tests/verify.py`. Compare `_extensions/wrapped/`
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
- 2026-10-28: T3 done: README "PDF through Typst" gains a columns paragraph, and both of its `text width` sentences name the column width. DESIGN's Typst page-bottom entry covers columns (corrected M019). wrap-mechanisms gains a W3 columns note and row E22.
- 2026-10-28: T4 done: `python3 tests/verify.py` exit 0, "all 98 renders pass", with the 5 typst-columns layout cases ok. Against main, `_extensions/wrapped/` is unchanged and `tests/_snapshots/` only adds `typst-columns.typst.txt`.
- 2026-10-28: claim audit: 38 claims read, 3 corrected — tests/verify.py (`column_edges`, `column_image`, and module docstrings; comment-only, re-read once and confirmed). README.md and tests/typst-columns.qmd held, with scratch renders confirming the 311 px column, 26 px gutter, column-width percents and fill check, and the moved group.
- 2026-10-28: implement complete; status review.
- 2026-10-28: review pass 1: four lenses returned 27 findings; 17 fix-now landed in 144eb1c (fixture fill case now 2.5in with a 0.5in gap, a 2.4in case with a 10% gap, a two-line blank-column check, doc fixes). The consistency gate then failed on `cairn/PROFILE.md` at 121 lines (cap 120), fixed by keeping the new clause on the slot's existing long line. Full suite rerunning on the fixed head.

## Decisions

## Review

Evidence is from `python3 tests/verify.py` on 144eb1c (fix-now pass 1 in place), exit 0, "all 98 renders pass", run 2026-10-28 after the fixes. f3e8d68 changes only `cairn/` files.

- AC1: `ok layout typst-columns 40% in column 1`, `1in image in column 1`, and `40% in column 2` (the beside tests and the column test); `ok typst-columns.typst`, whose snapshot's `# warnings` part holds no line, so the render printed no `wrapped:` warning.
- AC2: the same three cases pass their width test: 124 px (`TYPST_COL_40`) for both 40% figures and 108 px (`TYPST_1IN`) for the 1in image, within `NEAR`. Pass-1 plant: a 30% width failed "the image is 93 px wide, not 124 px".
- AC3: `ok layout typst-columns 2.5in with 0.5in gap fills the column`: 2.5in fits the column alone (207 pt), and with its 0.5in gap is wider than it and narrower than the 432 pt page text; the image is 124 px and the paragraph is beside it. Plant: a 0pt gap kept 2.5in, "the image is 270 px wide, not 124 px". Beside AC3, `2.4in with 10% gap fits the column` passes at 259 px; a 0.6in gap (10% of the page text) gave "124 px wide, not 259 px".
- AC4: `ok layout typst-columns moved to column 2`: "Marker before" is in column 1 of page 3, the moved image is in column 2 of page 3 with no column-2 line ending above it, and its paragraph is beside it. Column 1 ends at 954 px and column 2's text at 1044 px, so the end of column 1 stays blank. Plants: shorter filler ("not inside column 2"), a colbreak before the figure ("8 lines of column 2 end above the image"), about 2 more filler lines ("column 1 ends at 1019 px, less than two lines above the foot of column 2 at 1044 px").
- AC5: read at f3e8d68, README "PDF through Typst" states for `columns:` set, such as `columns: 2`: a figure "wraps inside its column"; "A percent width is a share of the column width, and Typst checks a width plus its gap against the column width"; a figure and its text that "do not fit at the bottom of a column ... move to the next column"; "The rest of that column stays blank". The section's two `text width` sentences both name the column width.
- AC6: local run above exit 0. `git diff --stat main..HEAD -- _extensions` is empty; `tests/_snapshots/` against main only adds `typst-columns.typst.txt`, so every fixture on main renders to its snapshot on main. CI on the PR is read at step 8 and recorded here before the merge.

Consistency gate: `cairn_validate.py` all checks passed at f3e8d68 (pass 1 first failed weight caps, `cairn/PROFILE.md` 121 lines, fixed in f3e8d68). No principle changed, so no `cairn_impact`. Profile slot: the one version marker, `_extension.yml` `version: 0.1.0`, is unchanged; the verify command passes (above); changelog "none". Snapshot files: none under a `_snaps` or `__snapshots__` directory; `tests/_snapshots/typst-columns.typst.txt` is new, as T1 calls for.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: the 2.9in fill case could not show the gap is counted (2.9in alone is wider than the column) — fix now, fixed 144eb1c (2.5in with a 0.5in gap; a 0pt-gap plant keeps 270 px).
- diff-bug #2: "the rest of that column stays blank" had no test — fix now, fixed 144eb1c (the moved case checks column 1 ends two lines or more above the foot of column 2; plant red with that reason).
- diff-bug #3: the percent-gap part of the README bullet had no test — fix now, fixed 144eb1c (2.4in with a 10% gap keeps 259 px; a 0.6in plant falls to 124 px).
- diff-bug #4: the TYPST_COL_40 comment showed worked arithmetic — fix now, fixed 144eb1c (source facts only).
- diff-bug #5: a column-2 line ends exactly `NEAR` past the edge, so a first line could fail on other fonts — reject, false: that line is no case's first line, and the bound is the same `NEAR` the existing Typst width cases use.
- diff-bug #6: `lh=None` reaches the column cases — fix now, fixed 144eb1c (the COLUMN_LAYOUT comment says its cases must not read `lh`).
- diff-bug #7: README line over width, column check stated twice, limits bullet pages only — fix now, fixed 144eb1c.
- blame-history #1: a second W3 bullet in wrap-mechanisms — reject, false: the details list keys bullets by row, as "W4 schema order" already does.
- blame-history #2: DESIGN's M010 Typst known issue had no column rule — fix now, fixed 144eb1c.
- blame-history #3: "(M005, corrected M019)" overstates — fix now, fixed 144eb1c ("columns M019").
- blame-history #4: `typst_column_case` repeats `typst_width_case` checks — reject, style: duplication with no defect; the column lookup and column test differ.
- blame-history #5: the new helpers parallel `find_words`, `find_figure`, `after`, `text_edges` — reject, style: same ground as #4.
- blame-history #6: COLUMN_LAYOUT repeats the fixture's `columns: 2` — reject, style: it follows the LAYOUT, TYPST_LAYOUT, and LOGS tables.
- blame-history #7: README line 435 too long — fix now, fixed 144eb1c.
- blame-history #8: is `review` a valid status — reject, false: it is one of the seven statuses.
- prior-review #1: README limits bullet said pages only — fix now, fixed 144eb1c.
- prior-review #2: README "fills the text" lines lack a column case — reject, false: in a column the text is the column's text, and the section states the column case.
- prior-review #3: PROFILE.md verify slot did not name COLUMN_LAYOUT — fix now, fixed 144eb1c and f3e8d68.
- prior-review #4: E22 left out the 40% second fallback — fix now, fixed 144eb1c.
- ripple #1: ROADMAP candidate "Check wrapped figures in Typst columns" still open — reject, planned change: post-merge hygiene graduates it.
- ripple #2: wrap-mechanisms W3 sketch said `layout` gives the text width — fix now, fixed 144eb1c.
- ripple #3: DESIGN filter and header text stated Typst width rules against the text width — fix now, fixed 144eb1c.
- ripple #4: `wrapped.lua` Typst comments say text width — follow-up, row "Name column widths in Typst comments" (AC6 keeps `_extensions/wrapped/` unchanged).
- ripple #5: README 100% and fill rules name only "the text" — reject, false: same ground as prior-review #2.
- ripple #6: README limits bullet pages only — fix now, fixed 144eb1c (same fix as diff-bug #7).
- ripple #7: wrap-mechanisms E10 named only the page — fix now, fixed 144eb1c.
- ripple #8: DESIGN syntax table said "percent of text width" — fix now, fixed 144eb1c.

Return floor: no finding shows a criterion failing or a defect in what the extension does; the fixes are test and text gaps, so no return.
