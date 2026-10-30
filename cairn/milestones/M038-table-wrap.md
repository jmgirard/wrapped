<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M038: Wrap table floats in HTML and Typst

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — users put the wrap class on tables and see the layout   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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
- A document `fig-column` or `column` read for a table float: candidate
  row "Read table keys for document columns".
- A table whose content is wider than its box spills into the text in
  Typst. The site states this limit. No fix is planned.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: A new fixture `tests/tables.qmd` holds a wrapped table float in
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
- [ ] AC2: In PDF through Typst, each float of AC1 is in a `wrap-content`
      call with the paragraphs after it in the `.typ` file. The PDF is read
      as `pdftohtml -xml` text boxes. The first line of the paragraph after
      each table starts above the bottom of the table's last row. For a
      `.wrap-right` table, that line ends left of every text box of the
      table and its caption. For a `.wrap-left` table, it starts right of
      every such box.
- [ ] AC3: `tests/tables.qmd` shows five figure rules that hold for a table
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
- [ ] AC4: In PDF through LaTeX and in Word, each float of AC1 keeps its
      normal layout. The `.tex` file has no `wrappedfigure` around it, and
      the docx has no `w:framePr` on its paragraphs. The render prints one
      warning for each of the five floats. The warning names the table by
      its id and says that a table wraps only in HTML and Typst.
- [ ] AC5: In EPUB, a render of `tests/tables.qmd` prints the one format
      warning that a format which cannot wrap prints, and no table warning.
- [ ] AC6: The site states that a `#tbl-` table float wraps in HTML and
      Typst and keeps its normal layout with a warning in LaTeX and Word,
      wherever it says which elements take a wrap class. The pages are
      `docs/normal-layout.qmd` (Tables), `docs/reference.qmd`,
      `docs/get-started.qmd`, the four pages under `docs/formats/`, and
      `README.md`. One site page shows the syntax with an example and says
      which forms carry a width and a gap. `docs/formats/typst.qmd` states
      the spill limit of Scope Out. `quarto render docs` exits 0.
- [ ] AC7: `python3 tests/verify.py` passes every render. No snapshot line
      for a figure or for an element other than a table changes on the
      branch, as `git diff main -- tests/_snapshots` shows.

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

- [ ] T1: Write `tests/tables.qmd` with the cases of AC1 to AC5 and one
      table whose content is wider than its box. Add it to `RENDERS` in
      `tests/verify.py` for HTML, Typst, LaTeX, Word, and EPUB. Extend the
      table summary and the PDF checks for the wrap and the beside test.
      Extend `tests/layout.js` to measure a float that holds a table, not
      an image (`imageFillsBox`, tests/layout.js:80). Run it red first.
- [ ] T2: In `float_target` in `wrapped.lua` (line 1409), let a table
      float wrap in HTML and Typst. Set `found_wrap` for it. Read
      `tbl-cap-location` and `tbl-column` where step 2 and
      `column_context` read the figure keys. Keep its normal layout in
      LaTeX and Word with the new warning.
- [ ] T3: Make the grouping pass and `wrapped.css` place a table float in
      HTML and Typst as they place a figure float. Fit the table to the
      float box's width in both formats.
- [ ] T4: Re-snapshot the table cases that now wrap: `tbl-caption-block`,
      `tbl-cell-block`, `tbl-cell-both`, `tbl-striped`, and `tbl-cars` in
      `tests/fixture.qmd`, and `tbl-wrapped` in `tests/contexts.qmd`. Run
      the full `tests/verify.py`.
- [ ] T5: Update the pages of AC6 and add the example. Update
      `cairn/DESIGN.md` (the non-goal, steps 2, 4, and 6, and a Known
      issues entry for the Typst spill) and row E5 of
      `cairn/references/wrap-mechanisms.md`.

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

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
