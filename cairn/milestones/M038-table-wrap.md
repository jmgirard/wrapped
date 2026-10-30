<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M038: Wrap table floats in HTML and Typst

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — users put the wrap class on tables and see the layout   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m038-table-wrap   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A `#tbl-` table float with a wrap class wraps the paragraphs after it in HTML and in PDF through Typst, and keeps its normal layout with a warning in PDF through LaTeX, Word, and EPUB.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** table floats with a wrap class (D-021). A table float is a `#tbl-`
div, a pipe table whose caption block holds `#tbl-…` first, or a code cell
with a `tbl-` label. The wrap class sits on the float, on the code cell
(`#| classes:`), or in the attribute block at the caption's end. A width or
gap reaches the float only from the div or from a pipe table's `{#tbl-…}`
block, since Quarto keeps a block inside a `#tbl-` div as caption text.
The figure rules that AC3 names, the LaTeX and Word warning, the format
warning elsewhere, the site, and DESIGN.md.

**Out:**
- Wrapping in Word: candidate row "Wrap table floats in Word documents".
- Wrapping in LaTeX: candidate row "Wrap table floats in LaTeX PDFs".
- Captioned tables with no `#tbl-` label keep M033's warning: candidate
  row "Wrap tables that have no tbl- label".
- Callouts and other boxes: candidate row "Wrap callouts and other boxed
  content".
- revealjs slides and dashboards get no table case: candidate row "Check
  wrapped tables in slides".
- A document `column` read for a table float stays as for a figure, with
  no fixture. The document `tbl-column` and `fig-column` cases moved In
  (amended 2026-10-30), so the candidate row "Read table keys for
  document columns" is covered except for `column`.
- In PDF through Typst, a table whose content is wider than its box keeps
  to the box: Typst narrows its columns and breaks its words, and in a
  narrow box the text of columns side by side can overlap. In HTML, such a
  table scrolls inside its box. The site states both. No fix is planned.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: A new fixture `tests/tables.qmd` holds a wrapped table float in
      five forms. Form 1 is a `#tbl-` div with the class, `width`, and
      `wrap-gap`. Form 2 is a `: Cap {.wrap-left}` caption block inside a
      `#tbl-` div. Form 3 is a pipe table whose caption block is
      `{#tbl-… .wrap-right width=… wrap-gap=…}`. Form 4 is a knitr cell
      with `#| classes: wrap-right` and a `tbl-` label. Form 5 is a knitr
      `tbl-cap` that ends in `{.wrap-left}`. In HTML, each float has its
      wrap class. Its width and gap custom properties equal the values that
      forms 1 and 3 set, or the fixture's `wrapped:` width and gap for
      forms 2, 4, and 5. Each float is in a `.wrap-group` div with the
      paragraphs after it. In a browser at a 1280 x 900 viewport,
      `tests/layout.js` shows each float on its side at its width. The
      first paragraph's first line lies beside the float at the float's
      gap. The table's box lies inside the float's box.
- [x] AC2: In PDF through Typst, each float of AC1 is in a `wrap-content`
      call with the paragraphs after it in the `.typ` file. The PDF is read
      as `pdftohtml -xml` text boxes. The first line of the paragraph after
      each table starts above the bottom of the table's last row. For a
      `.wrap-right` table, that line ends left of every text box of the
      table and its caption. For a `.wrap-left` table, it starts right of
      every such box.
- [x] AC3: `tests/tables.qmd` shows five figure rules that hold for a table
      float. (a) A wrapped table float whose next block is not a paragraph
      keeps its normal layout with no warning, in HTML and Typst. (b) A
      wrapped table float in a callout keeps its normal layout with one
      warning that names the table and the callout, in HTML and Typst.
      (c) A heading after the paragraphs ends the group, so the heading is
      not in the `.wrap-group` div (HTML) or the `wrap-content` call
      (Typst). (d) In HTML, a wrapped table float with
      `tbl-cap-location: margin` keeps its normal layout with one warning
      that its caption is in the margin. (e) A wrapped code cell table with
      `#| tbl-column: margin` keeps its normal layout with one warning that
      it is in the margin, in HTML and Typst.
- [x] AC4: In PDF through LaTeX and in Word, each float of AC1 keeps its
      normal layout. The `.tex` file has no `wrappedfigure` around it, and
      the docx has no `w:framePr` on its paragraphs. The render prints one
      warning for each of the five floats. The warning names the table by
      its id and says that a table wraps only in HTML and Typst.
- [x] AC5: In EPUB, a render of `tests/tables.qmd` prints the one format
      warning that a format which cannot wrap prints, and no table warning.
- [x] AC6: The site states that a `#tbl-` table float wraps in HTML and
      Typst and keeps its normal layout with a warning in LaTeX and Word,
      wherever it says which elements take a wrap class. The pages are
      `docs/normal-layout.qmd` (Tables), `docs/reference.qmd`,
      `docs/get-started.qmd`, the four pages under `docs/formats/`, and
      `README.md`. One site page shows the syntax with an example and says
      which forms carry a width and a gap. `docs/formats/typst.qmd` and
      `docs/formats/html.qmd` state the wide-table behavior of Scope Out.
      `quarto render docs` exits 0.
- [ ] AC7: `python3 tests/verify.py` passes every render, on this Mac and
      on each Quarto version that `verify.yml` runs on the PR. Existing
      figure and other non-table snapshot lines are unchanged: in each
      `tests/_snapshots/` file that exists on `main`, every line that
      `git diff main...HEAD -- tests/_snapshots` adds or removes names a
      table float by its `tbl-` id, with or without `#`, or is a
      `# groups` line `cell, …` whose cell, counted in source order in its
      fixture, has a `tbl-` label.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1, T2
- AC4 → T1, T2
- AC5 → T1, T2
- AC6 → T5
- AC7 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Write `tests/tables.qmd` with the cases of AC1 to AC5 and one
      table whose content is wider than its box. Add it to `RENDERS` in
      `tests/verify.py` for HTML, Typst, LaTeX, Word, and EPUB. Extend the
      table summary and the PDF checks for the wrap and the beside test.
      Extend `tests/layout.js` to measure a float that holds a table, not
      an image (`imageFillsBox`, tests/layout.js:80). Run it red first.
- [x] T2: In `float_target` in `wrapped.lua` (line 1409), let a table
      float wrap in HTML and Typst. Set `found_wrap` for it. Read
      `tbl-cap-location` and `tbl-column` where step 2 and
      `column_context` read the figure keys. Keep its normal layout in
      LaTeX and Word with the new warning.
- [x] T3: Make the grouping pass and `wrapped.css` place a table float in
      HTML and Typst as they place a figure float. Fit the table to the
      float box's width in both formats.
- [x] T4: Re-snapshot the table cases that now wrap: `tbl-caption-block`,
      `tbl-cell-block`, `tbl-cell-both`, `tbl-striped`, and `tbl-cars` in
      `tests/fixture.qmd`, and `tbl-wrapped` in `tests/contexts.qmd`. Run
      the full `tests/verify.py`.
- [x] T5: Update the pages of AC6 and add the example. Update
      `cairn/DESIGN.md` (the non-goal, steps 2, 4, and 6, and a Known
      issues entry for the Typst spill) and row E5 of
      `cairn/references/wrap-mechanisms.md`.
- [x] T6: Review return 1. Make `fig-column-*` and `tbl-column-*` cell
      classes apply only to floats of their own type, read a table float's
      column class on a div inside it, set `found_wrap` only for figure and
      table floats, add `tests/tables-cell-columns.qmd` for the three
      cases, and make the fix-now text edits the Review section lists.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: milestone — a new user-visible feature that supersedes a design non-goal.
- 2026-10-30: idea vet: gap, which elements "other things" means — the question set chose tables only; gap, which formats — the set chose HTML and Typst first; gap, tables with no label — the set chose labeled only; gap, a width in a caption block inside a `#tbl-` div never reaches the float — taken as a documented limit; gap, a wide table spills in Typst — taken as a documented limit; no flaw.
- 2026-10-30: collision check: DESIGN.md lists tables as a version 1 non-goal for the LaTeX `longtable` reason, which still holds for LaTeX; D-021 records the change. D-020 dropped "Count table floats in the format warning" on a premise this plan ends, so D-021 supersedes that part. M033 and M034 shipped the table warning that this changes for `#tbl-` floats.
- 2026-10-30: inbox sweep: no open issues, no open PRs.
- 2026-10-30: lessons used: 2026-10-29 (M033) caption block applied after pre-quarto filters; 2026-10-29 (M034) trailing Space in LaTeX and Word captions; 2026-10-27 (M012) single-fixture check; 2026-10-28 (M020) browser pane viewport for `tests/layout.js`.
- 2026-10-30: probe (Quarto 1.10.19): pipe and knitr tables both render as `longtable` in LaTeX; a pipe table's `{#tbl-x .wrap-right width=…}` block reaches the filter as float classes and attributes; a block inside a `#tbl-` div stays caption text; a narrow Typst table takes auto columns and can spill out of a wrap box.
- 2026-10-30: criteria audit (full, fresh Opus reader) returned 9 findings, all fixed: named the forms that carry a width; HTML check measures beside, width, gap, and table inside box; Typst beside test made exact and a wide-table case added; goal narrowed to the tested rules, with `tbl-cap-location` and `tbl-column` rules added; LaTeX and Word warning limited to the five floats; EPUB format warning added (D-020); docs pages named instead of a grep; T4 lists `tbl-cars` and `tbl-wrapped`; slides and dashboards moved out.
- 2026-10-30: plan gate chose HTML and Typst first over planning Word and LaTeX now because neither format's mechanism is probed; falsified by a probe showing that Word floating tables or a LaTeX `tabular` rewrite need no new mechanism.
- 2026-10-30: plan gate chose `#tbl-` floats only over also wrapping unlabeled tables because an unlabeled table needs a new box form; falsified by users who wrap unlabeled tables more than labeled ones.
- 2026-10-30: decided: document Typst spill rather than shrink tables, since the filter cannot measure table content before Typst lays it out; falsified by a Typst setting that fits any table to its box.
- 2026-10-30: checkpoint (in progress): filter, CSS, tests/tables.qmd, the two tables-cap-margin fixtures, verify.py table cases, layout.js table check, docs, and DESIGN.md written; full verify and snapshots pending; no task checked off yet.
- 2026-10-30: substantive amendment: Scope Out's wide-table item and AC6's last clause changed from "spills into the text in Typst" to the observed behavior (Typst narrows columns and hyphenates, HTML scrolls in the box); a probe of an auto-width and a relative-width table showed no spill. The deliverable the user sees is unchanged, so no stop.
- re-audit: AC6 (full) — 2 findings: the wide-table behavior was documented but untested (fixed in T1: a Typst beside case for tbl-wide, and layout.js's tableInside reads the scroll container); reference.qmd, formats/html.qmd, and formats/typst.qmd stated only part of the four-format rule (fixed by adding the missing clauses, AC6 wording kept).
- 2026-10-30: implementation choice: a code cell with floats now anchors its group with or without a wrap class (cell_div), because a table float in a cell can take its class from its caption block; found when form 5 failed the HTML beside check.
- 2026-10-30: implementation choice: the tbl-cap-location: margin case moved to HTML-only fixtures tests/tables-cap-margin.qmd and tables-cap-margin-meta.qmd, because Quarto 1.10.19 fails the LaTeX build for such a table with or without the extension ("Misplaced \noalign").
- 2026-10-30: full suite with --update: 113 renders; snapshot diff limited to table lines in fixture and contexts (tbl-caption-block, tbl-cell-block, tbl-cell-both, tbl-cars, tbl-wrapped) and the new tables fixtures; the Typst wide-table case first failed on a caption renumbered by the new tbl-page case, fixed, then passed.
- 2026-10-30: observed: in HTML, Quarto copies a wrapped table float's class onto its inner table element (the `# tables` lines show `table=wrap-right`); no rule in wrapped.css selects `table.wrap-*`, so it changes no layout.
- 2026-10-30: T1 to T4 done: tables.qmd with 13 cases (5 forms, no-text, callout, margin, page-wide, wide) plus two HTML-only margin-caption fixtures; HTML layout.js report ok for all 6 wrapped tables at 1280x900; Typst beside cases ok for 6 tables, and a plant with two classes removed failed 2 of them; full suite green after --update.
- 2026-10-30: quarto render docs exit 0 (one existing #fig-callout warning); tests/docs_layout.py --no-word all ok; the get-started table demo floats right at 45% in the browser at 1280x900.
- claim audit: 60 claims read, 4 corrected — docs/reference.qmd (code cell table width), docs/normal-layout.qmd (tbl-column per format; document keys), wrapped.lua caption_in_margin comment; also tests/layout.js now walks up to the element that scrolls (a weaker-than-stated comment).
- 2026-10-30: substantive amendment: Scope Out item on document column keys narrowed; the claim audit found that a document `tbl-column: margin` put a table in the margin while the filter floated it there with no warning, and a document `fig-column: margin` kept body tables normal with a false margin warning. column_context now reads tbl-column, its own class and the document's, for table floats and not fig-column; fixtures tables-column-meta and tables-fig-column-meta (HTML and Typst) cover both. No criterion changed; the deliverable gains a fix, so no stop.
- 2026-10-30: T5 done: site pages, README, DESIGN.md, and wrap-mechanisms E5 updated; docs render exit 0.
- 2026-10-30: implement complete: python3 tests/verify.py all 117 renders pass after the tbl-column fix; quarto render docs exit 0; status set to review.
- amendment routed: AC7 — the new snapshot files of tables-cap-margin-meta, tables-column-meta, and tables-fig-column-meta add lines for their control figures, so "no snapshot line for a figure changes" fails as written although no snapshot file on main changed outside table lines; the criterion needs to bind the files that exist on main.
- re-audit: AC7 (full) — 3 findings on the first amended wording: "names the code cell" overstated what a `cell, p` groups line shows; the criterion bound the snapshot record without saying it stands for unchanged output; the list of line kinds was longer than needed. Wording fixed to the reader's suggestion and sent to a second fresh reader.
- re-audit: AC7 (full) — 4 findings on the second wording: most changed lines name the id without "#"; the `cell` clause needs the fixture source order to check; "output is unchanged" claims more than snapshot summaries record; the snapshots must pass on both Quarto versions verify.yml runs. Second re-audit line, so the wording goes to the user.
- 2026-10-30: the user chose AC7's final wording with the CI clause at the second-re-audit stop (option "Final wording + CI").
- amendment return: AC7 — "`python3 tests/verify.py` passes every render, on this Mac and on each Quarto version that `verify.yml` runs on the PR. Existing figure and other non-table snapshot lines are unchanged: in each `tests/_snapshots/` file that exists on `main`, every line that `git diff main...HEAD -- tests/_snapshots` adds or removes names a table float by its `tbl-` id, with or without `#`, or is a `# groups` line `cell, …` whose cell, counted in source order in its fixture, has a `tbl-` label."
- 2026-10-30: amendment done; status back to review. The full suite on the review head passed (all 117 renders) before the amendment, and no code changed since.
- 2026-10-30: review moved the 19 work-log lines that implement had appended below the `## Review` heading back into the Work log; their text is unchanged.
- review return 1: diff-bug #1 and #3 (load-bearing): scoped column classes (fig-column-*, tbl-column-*) must apply only to floats of their own type, and a table float must read a page-wide or margin column class on a div inside it; with them the fix-now items diff-bug #2, #5, blame-history #6, #7, #8, ripple #1, #2, #3, #4, #8, and the two follow-up rows.
- 2026-10-30: T6 added for review return 1 (minor amendment).
- 2026-10-30: T6: block_context returns a scope for a context that only a cell's fig-column-* or tbl-column-* class sets, record_floats keeps it in context_scope, and float_target drops a context of the other type; column_context drops the other type's scoped classes (own_type_classes); a table float reads a column class on a div inside it, since float.content can be one Block that a walk does not visit; found_wrap only for figure and table floats. New fixture tests/tables-cell-columns.qmd (HTML, Typst): the tbl-column figure and the fig-column table wrap, and the column: page table warns page-wide.
- 2026-10-30: T6 text fixes: TABLE_IDS comment, wrapped.lua header and the several-cell comment, DESIGN.md steps 2, 4, 5, and 7, docs/index.qmd table sentence; ROADMAP row "Read table keys for document columns" narrowed to `column`, and rows "Name tables in the format warning" and "Treat mixed table and figure cells" added, both parked.
- claim audit: 34 claims read, 3 corrected — wrapped.lua and DESIGN.md (Quarto, not knitr, moves a table cell's column class inside the float); the gate on the inner class used meta_column_set, which a document fig-column sets, so a page-wide table cell under fig-column: margin wrapped in Typst; now gated on tbl-column or column (meta_table_column_set), with a tbl-page-cell case added to tests/tables-fig-column-meta.qmd.
- 2026-10-30: T6 done: python3 tests/verify.py all 119 renders pass; quarto render docs exit 0; status set to review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->

Evidence at 733a1be (no code change since 293d595; `main` at 2029477, the branch's base).

- AC1: browser pane at 1280 x 900 on tests/tables.html, `layout.js` `report()`: tbl-div (right, 45%, 2em), tbl-block (left, 35%, 1.5em), tbl-pipe (right, 30%, 1em), tbl-cell (right, 35%, 1.5em), tbl-cell-block (left, 35%, 1.5em) each `ok` with float, beside, tableInside, width, gap, and captionInside true; tables.html snapshot shows each in a group with its paragraphs (`tbl-div, p, p`, `tbl-block, p`, `tbl-pipe, p`, `cell, p` twice).
- AC2: `python3 tests/verify.py` on the review head: `ok layout tables` for div, caption block in a div, pipe table, cell class, and cell caption block (side tests on caption and row boxes); tables.typst snapshot lists a `wrap-content` call with `p` blocks for each of the five.
- AC3: tables.{html,typst} snapshots: (a) tbl-no-text `- style=-`, no group, no warning; (b) one "the table #tbl-callout is in a callout" warning in each; (c) tbl-div's group is `p, p`, ending at the next heading, in both; (d) tables-cap-margin.html and tables-cap-margin-meta.html each print one "has its caption in the margin" warning and keep the table unwrapped; (e) one "the table #tbl-margin is in the margin" warning in each.
- AC4: tables.tex has 0 `wrappedfigure` in the body and 10 `longtable`s; tables.docx has 0 `w:framePr`; tables.pdf and tables.docx snapshots print one "does not wrap in LaTeX/Word. A table wraps only in HTML and Typst." warning for each of tbl-div, tbl-block, tbl-pipe, tbl-cell, tbl-cell-block.
- AC5: tables.epub snapshot: the one line "epub output does not wrap figures yet…" and no table warning.
- AC6: read normal-layout.qmd (Tables), reference.qmd, get-started.qmd (Wrap a table: example, the forms that carry width and gap), formats/html.qmd and typst.qmd (both halves of the rule and the wide-table behavior), formats/latex.qmd and word.qmd (their own format's limit; neither lists which elements take a wrap class), README.md (both halves); `quarto render docs` exit 0 at 293d595 code.
- AC7 (local half): all 117 renders pass on this Mac; `git diff main...HEAD -- tests/_snapshots` changes 8 files that exist on main, and each of their 44 changed lines names tbl-caption-block, tbl-cell-block, tbl-cell-both, tbl-cars, or tbl-wrapped, or is one of the two `cell, p` groups of the `tbl-cell-block` and `tbl-cell-both` cells (tests/fixture.qmd:218, :226). CI half pending: the PR's verify runs on Quarto 1.9.36 and the release channel.
- gate: `cairn_validate.py` all checks passed; no principle changed, so no `cairn_impact` run; one version marker (`_extension.yml` 0.2.0), unchanged on the branch; verify passes on the review head (AC7); `tests/docs_layout.py --no-word` all ok on the Mac (the Word check is hand-run and was not run; no example page changed); the docs workflow runs on the PR; changelog slot "none".
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a figure in a code cell with `#| tbl-column: margin` (or `page`) and a wrap class stops wrapping with a false "is in the margin" warning, where main wraps it; margin_context and page_context read the scoped class whatever the float's type — fix now (floor: load-bearing regression)
- diff-bug #2: a table float in a cell with `#| fig-column: margin` gets a false margin warning, where Quarto leaves it in the body — fix now (same cause as #1)
- diff-bug #3: a knitr table cell with `#| column: page` wraps with no warning in HTML and Typst while Quarto sets it page-wide; knitr puts `column-page` on a div inside the float, which find_contexts skips — fix now (floor: load-bearing, a documented Quarto option gives a wrong layout with no warning)
- diff-bug #4: the format warning names only figures when a table is the wrapped element (two-column LaTeX, Word with columns, EPUB) — follow-up: candidate row "Name tables in the format warning", parked, promote when a user reports it
- diff-bug #5: found_wrap is set for every float type, so a wrapped listing now raises the EPUB format warning where main printed nothing — fix now
- diff-bug #6: tables wrap in revealjs with no table context check — reject, planned change (Scope Out, row "Check wrapped tables in slides")
- diff-bug #7: the new `table=wrap-right` snapshot lines record that Quarto copies the float's class onto the inner table — reject, planned change (table_summary records wrap classes that reach a table, M034)
- blame-history #1: a wrapped table float with no paragraph after it prints no LaTeX or Word warning (tbl-cars, tbl-no-text) — reject, planned change (the next-block rule applies to tables as to figures, with no warning)
- blame-history #2: a classed cell that makes a table and a figure wraps the table and keeps the figure normal under a "makes more than one figure" warning; D-010 counts figures only — follow-up: candidate row "Treat mixed table and figure cells", parked, promote when a user reports it
- blame-history #3: tables wrap in revealjs, untested — reject, planned change (as diff-bug #6)
- blame-history #4: layout.js tableInside cannot fail for a wide table — reject, false: before the overflow rule existed, the same check failed for tbl-wide (work log, T1); without the rule `scrolls` is false and the table's own box is measured
- blame-history #5: a document `column` is read for table floats with no fixture — reject, planned change (Scope Out)
- blame-history #6: found_wrap set for every float type — fix now (as diff-bug #5)
- blame-history #7: the TABLE_IDS comment says every entry has a caption block, but tbl-div and tbl-cell have none — fix now
- blame-history #8: DESIGN.md step 4 names the cell anchor but not that unclassed cells now feed the margin-caption carry — fix now
- blame-history #9: Quarto copying tbl-cap-location from a cell to its table float is unverified — reject, false: the plan probe's dump showed `tbl-cap-location=margin` on the float, and the claim audit confirmed it with a debug filter
- prior-review #1: a figure with an image-level wrap class in an unclassed cell now anchors the whole cell — reject, false: the diff-bug reviewer rendered that case (asis output with its own wrap class) and its warnings and groups match main
- prior-review #2: the HTML docs layout check (`tests/docs_layout.py --html`) has not run for this branch — reject, false: docs.yml runs `--html` on the PR, which the gate reads before the merge
- prior-review #3: the EPUB format warning names figures for a table — follow-up: row "Name tables in the format warning" (as diff-bug #4)
- prior-review #4: the Typst overlap limit has no check — reject, planned change: the limit states Typst's own layout, seen in the tbl-wide render, and a test of it would test dependency behavior
- ripple #1: DESIGN.md step 7 says the stylesheet is added when a figure wraps; a table now adds it — fix now
- ripple #2: the parked row "Read table keys for document columns" describes fig-column behavior the diff removed — fix now (narrow the row to `column`)
- ripple #3: docs/index.qmd says the version wraps figures with no table sentence — fix now
- ripple #4: the wrapped.lua header and DESIGN.md step 5 speak of figures only where tables now float and group — fix now
- ripple #5: reference.qmd's class rows say "All four formats" — reject, false: the paragraph above the table says a table float wraps only in HTML and Typst
- ripple #6: the normal-layout page title names figures only — reject, style
- ripple #7: DESIGN.md step 2 lists "a table in LaTeX and Word" as a context — reject, false: that context is a figure inside a table cell, which still holds
- ripple #8: the comment "A table keeps its own warning" in float_target is ambiguous now that HTML and Typst tables wrap — fix now
