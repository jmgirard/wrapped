<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M040: Wrap table floats in LaTeX PDFs

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the filter's LaTeX output, which users install from `main`
- **Branch/PR:** m040-latex-table-wrap

## Goal

A `#tbl-` table float with a wrap class wraps the paragraphs after it in PDF through LaTeX, as it does in HTML, Typst, and Word.

## Scope

**In:** In `wrapped.lua`, a LaTeX table float whose content holds a Pandoc
table and no raw LaTeX wraps: the filter writes the table as a raw
`tabular` (Pandoc's `longtable` text with its head and foot parts set in
place), gives its columns shares of the box, and names a new
`wrappedtable` environment as the float's `fig-env`, with the options that
`tex_options` gives a figure. Quarto then writes the caption and the label
inside that environment. In `wrapped.tex`, `wrappedtable` runs on
wrapfig's `wraptable` and takes `wrappedfigure`'s three modes (wrap, a
`table` float in two-column text, set in place in `multicols` or in a
box), and the log warnings name the float's kind. A table float that
holds raw LaTeX, as gt, kableExtra, tinytable, and
`knitr::kable(format = "latex")` write, keeps its normal layout with a
warning. Tests, the site pages, README.md, DESIGN.md, and
`cairn/references/wrap-mechanisms.md` follow.

**Out:**
- Wrapping a raw LaTeX table from an R package: the user kept it normal at
  the plan gate; the candidate row "Wrap raw LaTeX tables from R packages"
  holds it.
- A table whose columns mix relative and default widths: LaTeX takes the
  shares that `column_shares` gives Word, and case (f) of the candidate row
  "Size images and columns in Word tables" covers that sizing.
- A wrapped table that breaks across pages: a `tabular` does not break, so
  this is a stated limit (AC6), not work.
- The format warning under `classoption: twocolumn`, which names figures
  only: the candidate row "Name tables in the format warning".
- Tables with no `#tbl-` label and callouts: their candidate rows.

## Acceptance criteria

- [ ] AC1: In the PDF through LaTeX of `tests/tables.qmd`, for each of the five tables `tbl-div`,
      `tbl-block`, `tbl-pipe`, `tbl-cell`, and `tbl-cell-block`, the first line of the paragraph
      after the table starts above the bottom of the table's last row and lies wholly on the side
      away from the table, and the heading after `tbl-div` starts below that table's last row
      (evidence: a `LAYOUT` case per table in `tests/verify.py`).
- [ ] AC2: The kept `.tex` of `tests/tables.qmd` sets each of the six tables `tbl-div`,
      `tbl-block`, `tbl-pipe`, `tbl-cell`, `tbl-cell-block`, and `tbl-wide`, and the kept `.tex` of
      the new fixture `tests/tables-latex.qmd` sets its table `tbl-rel`, in a `wrappedtable`
      environment whose options give the side, width, and gap that the table's class, its
      attributes, or the document's `wrapped:` keys set. Each environment holds the table's
      `\caption`, its `\label`, and one `tabular`, and no `longtable`. Each column of the six tables
      of `tests/tables.qmd`, whose columns have no widths, is a `p{}` column whose `\real{}` factor
      (the share of the box's line width less its column padding that Pandoc writes) equals that
      column's length divided by the sum of the table's column lengths, rounded to four decimals,
      where a column's length is the larger of one and the largest number of characters, spaces
      included, in the plain text (formatting removed) of a header or body cell of that column
      that spans no other column; the columns of `tbl-rel`, whose columns all have relative widths,
      have `\real{}` factors equal to each width that Pandoc's reader gives the column (its dashes'
      share of the separator line) divided by the sum of the widths, rounded to four decimals
      (evidence: both fixtures' LaTeX snapshots).
- [ ] AC3: `tests/tables-latex.qmd`, in which `tbl-rel` is the only Pandoc table and comes before
      `tbl-raw`, renders to PDF
      through LaTeX with exit status 0. Its PDF text shows `tbl-rel`'s caption numbered "Table 1"
      and the text's `@tbl-rel` link as "Table 1". Its table float `tbl-raw`, whose table
      `knitr::kable(format = "latex")` writes as raw LaTeX, has no `wrappedtable` environment in the
      kept `.tex`, and the render prints exactly one warning that names `#tbl-raw`, which says that a raw LaTeX
      table, as from gt, kableExtra, or tinytable, does not wrap.
- [ ] AC4: The PDF-through-LaTeX render of `tests/tables.qmd` prints no warning that a table does
      not wrap in LaTeX. It prints the warnings for `tbl-callout` (in a callout), `tbl-margin` (in
      the margin), and `tbl-page` (page-wide), and none for `tbl-no-text`, which has no
      `wrappedtable` environment in the `.tex` (evidence: the LaTeX snapshot).
- [ ] AC5: In `tests/multicols.qmd`, a wrapped table float inside a raw `multicols` is set in place
      in its column, between the paragraphs before and after it; in `tests/twocolumn-switch.qmd`, a
      wrapped table float after a raw `\twocolumn` has no text beside it. Both fixtures render with
      exit status 0. The LaTeX log's multicols warning for the table names a table, and its
      two-column warning names tables as well as figures.
- [ ] AC6: Of the sentences that hold a line that
      `grep -niE 'table|tbl-' README.md docs/*.qmd docs/formats/*.qmd cairn/DESIGN.md cairn/references/wrap-mechanisms.md`
      lists, each that says where a `#tbl-` table float wraps or keeps its normal layout agrees
      with the shipped behavior (it wraps in all four formats, except a raw table in Word and in
      LaTeX), and none says that a Pandoc table float does not wrap in PDF through LaTeX.
      `docs/formats/latex.qmd` states that a wrapped table does not break across pages, that
      a raw LaTeX table keeps its normal layout with a warning, and how a table wider than its box
      renders, as the `tbl-wide` render of `tests/tables.qmd` shows; `cairn/DESIGN.md` Known issues
      states the last two limits.
- [ ] AC7: `python3 tests/verify.py` passes on the review head; `quarto render docs` exits 0; `python3 tests/docs_layout.py` exits 0; the PR's CI is green
      under Quarto's release channel and Quarto 1.9.36.

## Coverage

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T2, T3
- AC5 → T1, T3
- AC6 → T4
- AC7 → T5

## Tasks

- [x] T1: In `_extensions/wrapped/wrapped.tex` (`wrappedfigure` at :193,
      warnings at :141-147), add `wrappedtable` over `\wraptable`, sharing
      the key set, the three modes (a `table` float in mode f,
      `\@captype` table in mode p), the gap record, and `\wrapped@endwrap`
      with `wrappedfigure`, so one wrap at a time holds across kinds. Make
      the multicols warning name the float's kind and the two-column
      warning name figures and tables. Update the file's header comment.
- [x] T2: In `_extensions/wrapped/wrapped.lua`, replace the LaTeX table
      return at :1630-1639 with a raw-LaTeX check (`raw_latex_table`,
      beside `raw_docx_table` at :1537) and its warning. In the
      `is_latex` branch at :1680, for a table float set `fig-env` to
      `wrappedtable` and replace the content's Pandoc table with a
      `latex_tabular` raw block: set each column's width from
      `column_shares`, `pandoc.write` the table, drop the
      `\def\LTcaptype` group, keep the first head, move the foot to the
      end, and write `tabular`. Walk `pandoc.Blocks({ content })`, since
      the content can be one Block. Make sure that a document whose only
      Pandoc table is wrapped still loads the table packages, and probe the `fig-env` path and the
      `\LTcaptype` removal under Quarto 1.9.36 (M035 lesson) before building on them.
- [x] T3: Tests: `latex_table_case` LAYOUT cases for the five forms, with
      the `tbl-div` stop below; new `tests/tables-latex.qmd` (LaTeX only:
      `tbl-rel` with relative widths and an `@tbl-rel` link, `tbl-raw`
      from `knitr::kable(format = "latex")`) in the render list; a table
      case in `multicols.qmd` and `twocolumn-switch.qmd`; snapshot
      updates with `--update`, each diff read.
- [x] T4: Docs: `docs/get-started.qmd` "Wrap a table",
      `docs/normal-layout.qmd`, `docs/reference.qmd`, `docs/index.qmd`,
      `docs/formats/latex.qmd` (Limits: no page break, raw tables, the
      wide table as rendered), README.md; `cairn/DESIGN.md` Goals,
      Non-goals, Architecture steps 4 and 7, Known issues;
      `cairn/references/wrap-mechanisms.md` E5 and the LaTeX row. Run the
      AC6 grep and fix each line it lists; render the docs and run
      `tests/docs_layout.py`.
- [ ] T5: Full `python3 tests/verify.py`; revert any `/.quarto/` lines a
      render adds to `tests/.gitignore`; open the PR at review and wait on
      CI.

## Work log

- 2026-10-31: created by /milestone-plan.
- 2026-10-31: tier check: not run — work named at the question set.
- 2026-10-31: question set: which candidate to build — "Wrap table floats in LaTeX PDFs" (absorbed in full).
- 2026-10-31: question set: what a raw LaTeX table float from an R package does in LaTeX — keep its normal layout with a warning.
- 2026-10-31: idea vet: gap — a `tabular` does not break across pages (reading: rewrite as `tabular`, as the row says; stated limit in AC6); gap — a table wider than its box (reading: columns share the box, as in Word; the render is stated in AC6); gap — raw LaTeX tables (set answer: keep normal, warn); no flaw.
- 2026-10-31: collision check: candidate "Wrap table floats in LaTeX PDFs" absorbed; D-021 and D-022 deferred LaTeX, no rejection, so D-024 supersedes their LaTeX part; M038 and M039 (done) wrap tables in the other formats; no open issues or PRs (inbox sweep 0 and 0).
- 2026-10-31: probe: a pre-quarto filter that sets a table float's `fig-env` to a `\wraptable` environment and turns its table into a raw `tabular` built with Quarto 1.10.20; the text wrapped, the caption read "Table 2: Kable cap", and `@tbl-kable` read "Table 2". Pandoc's `\def\LTcaptype{none}` group must go, or LaTeX stops with "Missing } inserted".
- 2026-10-31: plan chose rewriting Pandoc's `longtable` text over calling Quarto's `latexTabular`, because that is a global of Quarto's own filter, not an extension API; falsified by Quarto documenting it for filters.
- 2026-10-31: plan chose column shares of the box over natural `l`/`r`/`c` widths, because a natural-width table wider than its box runs into the text; falsified by a render where the shares break words in a table whose natural width fits the box.
- 2026-10-31: plan gate chose to keep raw LaTeX tables normal over rewriting them, because each package writes its own LaTeX; falsified by evidence that gt, kableExtra, and tinytable output share one form the filter can rewrite.
- 2026-10-31: lessons used: 2026-10-30 (M038) one-Block float content; 2026-10-25 (M004) LaTeX and Typst share `fixture.pdf`; 2026-10-26 (M007) pdftohtml boxes; 2026-10-27 (M012) one-fixture check; 2026-10-29 (M034) `/.quarto/` lines in `tests/.gitignore`; 2026-10-29 (M033) caption blocks after pre-quarto.
- 2026-10-31: criteria audit (full mode, fresh Opus reader): 8 findings, all taken toward the narrower promise — AC2 column widths named as Pandoc's `\real{}` factors over the line width less padding; AC3 orders `tbl-rel` first and says exactly one `#tbl-raw` warning; AC4 binds the render's warnings, not the snapshot; AC1, AC2, AC4 harness clauses made evidence pointers; AC6 narrowed to sentences that say where a table float wraps, with no sentence saying a Pandoc table does not wrap in LaTeX (the grep also lists lines on other subjects); AC7 drops "every snapshot change reviewed" (T3 reads each diff); the unprobed Quarto 1.9.36 risk became a T2 probe. No D-entry blocks any criterion.
- 2026-10-31: `tests/.gitignore` holds uncommitted `/.quarto/` lines from an earlier render (M034 lesson), left unstaged by the plan commit.
- 2026-10-31: /milestone-implement: branch m040-latex-table-wrap cut from origin/main at fca6c41; status in-progress; `tests/.gitignore`'s `/.quarto/` lines stay unstaged.
- 2026-10-31: T2 probe first: the plan's scratch probe (a `\wraptable` env named by `fig-env`, the table as raw `tabular`, the `\LTcaptype` group dropped) builds and wraps under Quarto 1.9.36 as under 1.10.20, captions "Table 1"/"Table 2" and both `@tbl-` links resolved; with every table rewritten, both versions' preambles still load `longtable,booktabs,array` and `calc`, so no package call is needed.
- 2026-10-31: T1 done: `wrapped.tex` has `\__wrapped_begin:nn`/`\__wrapped_end:n` taking the kind; `wrappedfigure` and `wrappedtable` (over `\wraptable`) share keys, modes, gap, and `\wrapped@endwrap`. Multicols warning reads "<Kind> in multicols set as normal <kind>", the two-column warning "Two-column text: figures and tables set as normal floats". `tests/verify.py`'s log check matches multicols warnings by line and kind; `multicols`, `twocolumn-switch`, `twocolumn-class` log checks pass.
- 2026-10-31: T2 in progress (checkpoint): `raw_latex_table` and `latex_tabular` added; a LaTeX table float sets `fig-env` to `wrappedtable` and `tbl-pos` (Quarto reads `<type>-pos`, in 1.9.36 and 1.10.20) to `tex_options`. `tests/tables.qmd` builds with the six tables in `wrappedtable`; two LaTeX-only `\clearpage` blocks (before `tbl-block` and before Form 4) give wrapfig room, since tables 2 and 4 otherwise fell at page ends and were set alone on the next page. No fallback branch for a longtable text `latex_tabular` cannot read: Pandoc's writer shape is fixed for a pinned Pandoc, and the fixtures run under both Quarto versions.
- 2026-10-31: the plan's falsifier for equal column shares fired: in `tbl-div` (45% box) equal shares break "Condition" as "Condi-tion", though the table's natural width fits. A scratch change giving each column a share in proportion to its longest cell text fit "Condition" on one line; it changes AC2's promised widths, so it waits for the user (stop: an amendment that changes what the user sees).
- 2026-10-31: stop answered: the user chose "Share by text length" over keeping equal shares; `text_shares` written (any set width falls back to `column_shares`, so the mixed-width Out item stands).
- 2026-10-31: re-audit: AC2 (full) — 3 findings: "in proportion" clashes with four-decimal factors (state division and rounding); character count must say spaces included and formatting removed ("Speed in mph" is 12 or 10); say header or body cells. No D-entry blocks it; bounded; binds the `.tex`. All three fixed in the wording.
- 2026-10-31: re-audit: AC2 (full) — 2 wording findings: an all-empty column has text of length 0, so say "the larger of one and"; say `tbl-rel`'s widths are the ones Pandoc's reader gives (each column's dashes' share of the separator line). The 13 factors in the scratch render match the formula. Second re-audit line on AC2, so further wording goes to the user.
- 2026-10-31: substantive amendment: AC2's column clause, from equal shares to shares by each column's longest cell text (the user's choice at the stop), in the wording below, which the user accepted with both second-reader fixes. Scope In's "gives its columns shares of the box" stands.
- 2026-10-31: T3 so far: `tex_summary` lists each `wrappedtable` (label, options, caption, tabular and longtable counts, column factors); `table_case` (renamed from `typst_table_case`) serves LaTeX too; LAYOUT gains `tables` (five forms and the `tbl-div` stop) and `tables-latex`; new `tests/tables-latex.qmd` (`tbl-rel` by dashes 0.28/0.14/0.58, `@tbl-rel` link, `tbl-raw` from `kable(format = "latex")`); tables in `multicols.qmd` (in place, log kind "table") and `twocolumn-switch.qmd` (no text beside). Plants: on main's filter the five wrap cases and `tables-latex` relative widths fail ("starts below the table's last row"); synthetic boxes turn the stop, link, and alone checks red; a log edited to name a figure fails the multicols kind check.
- 2026-10-31: T4 so far: README, `docs/` get-started, normal-layout, reference, index, stopping, formats/latex (new Tables section), html, typst; DESIGN Goals, non-goal, stop rule, steps 4 and 7, Known issues; wrap-mechanisms W2, E5, filter note.
- 2026-10-31: `python3 tests/verify.py --update`: all 125 renders pass. Snapshot diffs read: LaTeX `tables`, `fixture`, `contexts`, `tables-cell-columns` trade each "does not wrap in LaTeX" warning for a `wrappedtable` line; `multicols` and `twocolumn-switch` add their table; new `tables-latex`. `tbl-cars` in `fixture.qmd` keeps no warning, since a figure follows it (next-block rule). The fixture's one `Overfull \vbox` is page 4's `fig-unwrapped-cell` beside the `tbl-cars` longtable, the parked "Fix the overfull LaTeX fixture page" clash. `fixture.qmd`'s three table sentences that said LaTeX keeps a normal layout now say it wraps.
- 2026-10-31: observed for docs: in LaTeX a document `tbl-column` of `margin` or `page` keeps `tables-column-meta`'s table normal with the "in the margin" or "page-wide" warning (scratch renders), so normal-layout names LaTeX beside HTML and Typst.
- 2026-10-31: T2, T3, T4 done: `quarto render docs` exit 0 (only `docs/_freeze/get-started` changed); `python3 tests/docs_layout.py` exit 0 (LaTeX, Typst, Word; `--html` left to CI).
- 2026-10-31: proposed AC2 column clause for the user: "Each column of the six tables of `tests/tables.qmd`, whose columns have no widths, is a `p{}` column whose `\real{}` factor (the share of the box's line width less its column padding that Pandoc writes) equals that column's length divided by the sum of the table's column lengths, rounded to four decimals, where a column's length is the larger of one and the largest number of characters, spaces included, in the plain text (formatting removed) of a header or body cell of that column that spans no other column; the columns of `tbl-rel`, whose columns all have relative widths, have `\real{}` factors equal to each width that Pandoc's reader gives the column (its dashes' share of the separator line) divided by the sum of the widths, rounded to four decimals (evidence: both fixtures' LaTeX snapshots)."

## Decisions

## Review
