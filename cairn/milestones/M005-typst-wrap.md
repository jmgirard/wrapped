<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M005: Wrap figures in Typst PDF output

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the PDF that users get from a wrapped figure through Typst
- **Branch/PR:** m005-typst-wrap

## Goal

A document rendered to PDF through Typst with the extension installed shows body text beside each figure marked `.wrap-left` or `.wrap-right`.

## Scope

**In:**
- wrap-it 0.1.1, bundled with its license under `_extensions/wrapped/typst/packages/preview/wrap-it/0.1.1/` (D-004). The filter imports it in Typst output when a figure wraps.
- The filter puts each wrapped float, captioned image with no id, and uncaptioned image in a `wrap-content` call with the paragraphs of its group, as raw Typst blocks from the grouping pass (spike S3). Typst leaves the format fallback.
- Width and gap conversions, and the `wrapped:` metadata, for Typst. The context, next-block, and unplaced warnings print in Typst.
- A citation in wrapped text (S3, research page test plan), a figure near a page break (E10), and `pdf-standard: ua-1` (E12), in Typst.
- `.typ` snapshots that record each `wrap-content` call, and a Typst section in `README.md` that states wrap-it's limits.

**Out:**
- Word → the candidate "Wrap figures in Word output with frames".
- Typst documents with `columns:` set → the new candidate "Check wrapped figures in Typst columns".
- `wrap-lines`, which stays LaTeX only (DESIGN syntax table).
- Quarto versions other than 1.10.19 and renders of a project. DESIGN already states that 1.9.36 to 1.10.18 are not tested.

## Acceptance criteria

- [ ] AC1: `quarto render tests/fixture.qmd --to typst` with `keep-typ: true` exits with status 0 and prints no "typst output does not wrap figures yet" warning. In the kept `.typ`, each figure and image that is in a `.wrap-group` in the fixture's HTML render is inside the `box` that is the first content argument of its own `wrap-content(` call, whose `align` names the figure's side. The paragraphs of that `.wrap-group` are in the call's second content argument, and no other block is. The `.typ` imports `wrap-content` from `@preview/wrap-it:0.1.1`.
- [ ] AC2: With Quarto 1.10.19, the fixture's Typst render loads wrap-it from the extension's bundled copy. With the Typst package cache emptied and a marker planted in the bundled copy, the marker shows in the PDF text from `pdftotext`. With the marker removed, it does not.
- [ ] AC3: `pdftoppm` makes page images of the fixture's Typst PDF. On them, each wrapped figure whose full height fits on the page below its start sits on its side, and lines of the first paragraph of its group sit beside it on the same page. The block after each such group starts below the figure's bottom edge.
- [ ] AC4: On the fixture's Typst page image, the box of `#fig-md` (`width="30%"`) measures 30% ± 2% of the text-block width. In the kept `.typ` of `tests/fixture.qmd` and `tests/defaults.qmd`, each width and gap value that the two fixtures set (among them `30%`, `3in`, `2em`, `150px`, `banana`, `wide`, `clamp(150px, 30%, 400px)`, `2VMIN`, and the added `2pc`, `1ex`, `2IN`, and `300`) becomes the Typst length this rule gives. A percent stays a percent. A px length, or a number with no unit, becomes pt at 0.75 pt per px. A `pc` length becomes pt at 12 pt per pc. A `pt`, `mm`, `cm`, `in`, or `em` length in any letter case keeps its number with the unit in lowercase. Any other value takes the default, with a warning. A `wrap-gap` value goes through the same rule and becomes that call's `column-gutter`. `tests/defaults.qmd` renders to Typst with exit status 0, and a figure there that sets neither attribute takes the `wrapped: width` and `wrapped: gap` metadata.
- [ ] AC5: The fixture holds a `@citation` in the text of a wrapped group, with a bibliography. The Typst PDF text from `pdftotext` holds the rendered citation, and the page image shows it beside the figure. A Typst fixture holds a wrapped figure that starts too near the bottom of a page to fit there. It renders with exit status 0. On its page images, the figure and its caption sit whole on one page, and no text line overlaps the figure. Its `pdftotext` text holds every paragraph of the group. The README states the gap that the page images show before the figure.
- [ ] AC6: A fixture with `pdf-standard: ua-1` holds a wrapped captioned figure and a wrapped uncaptioned image, each with `fig-alt`. It renders to Typst with exit status 0. For each of the two, the structure tree of the PDF holds its alt text, or it renders as a normal figure and the render prints one extension warning for that figure. The README names which of the two holds.
- [ ] AC7: `tests/stop-rule.qmd` and `tests/contexts.qmd` each render to Typst with exit status 0. For each, AC1's membership check holds: each `wrap-content` call in the kept `.typ` holds in its second content argument exactly the paragraphs of the matching `.wrap-group` in the HTML render, and no float that falls back in HTML is inside a `wrap-content(` call. Each render prints the same extension warnings as the HTML render of that fixture.

## Coverage

- AC1 → T2, T5
- AC2 → T1
- AC3 → T2, T5
- AC4 → T3, T5
- AC5 → T4, T5
- AC6 → T4, T5
- AC7 → T3, T5

## Tasks

- [x] T1: Copy wrap-it 0.1.1 from the typst/packages repository to `_extensions/wrapped/typst/packages/preview/wrap-it/0.1.1/`, with its `typst.toml` and license. Import it from the filter with `quarto.doc.include_text` when a Typst figure wraps. Empty the Typst package cache, plant a marker in the bundled copy, render, and remove the marker, to show that Quarto loads the bundled copy from a filter extension. Do this first: a no changes the approach.
- [x] T2: Add Typst to `wraps()`. In the grouping pass, emit raw Typst blocks that open a `wrap-content(align: <side>, column-gutter: <gap>, box(width: <width>)[` call before the figure, `], [` after it, and `])` after the group's last paragraph, as spike S3 did. Do this for floats, captioned images with no id, and uncaptioned images (with `fig-alt` as the image's `alt`). If a percent box resolves against wrap-it's column and not the text width, convert the percent to a length of the text width.
- [x] T3: Convert width and gap for Typst by AC4's rule, with the metadata defaults, and add the `2pc`, `1ex`, `2IN`, and `300` cases to the fixtures. Make the context, next-block, and unplaced warnings print in Typst. Add a `typst` format with `keep-typ: true` and `fig-format: png` to `tests/stop-rule.qmd`, `tests/contexts.qmd`, and `tests/defaults.qmd`, and render them to Typst.
- [x] T4: Add a bibliography and a citation in wrapped text to `tests/fixture.qmd`. Add a Typst page-break fixture whose figure placement does not depend on raw LaTeX, and a `pdf-standard: ua-1` Typst fixture. Read the alt text from the PDF's structure tree with `pdfinfo -struct`. Fall back with a warning for each figure whose alt text is lost.
- [x] T5: Add the Typst renders of the fixture, defaults, stop-rule, contexts, page-break, and ua-1 fixtures to `tests/verify.py`, and record in the `.typ` snapshot each `wrap-content` call's side, width, gap, and member labels. Make page images with `pdftoppm` and read them. Write the Typst section of `README.md` with wrap-it's limits: first-line indents (wrap-it #1), tall figures (#8), page breaks, the alt-text result, and the parts of the stop rule that differ from HTML.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: not run — work named at the question set.
- 2026-10-25: question set: next work — the user chose the candidate "Wrap figures in Typst PDF output".
- 2026-10-25: question set: dependency — the user allowed bundling wrap-it 0.1.1 under `_extensions/wrapped/typst/packages/` (D-004).
- 2026-10-25: idea vet: no concern. Typst wrapping is a stated goal (DESIGN Purpose), the syntax is shared with HTML and LaTeX, and S3 showed wrap-it renders a citation and a `@fig-` link beside a figure. wrap-it's last commit is 2025-02 and issues #1, #8 stay open; the README states them as limits, as M004 did for wrapfig.
- 2026-10-25: collision check: absorbed the candidate "Wrap figures in Typst PDF output". D-002 covers only the HTML and LaTeX dependencies, so wrap-it takes D-004. M001's S3 is the evidence base. No dropped milestone or rejection overlaps.
- 2026-10-25: inbox sweep: 0 open issues, 0 open PRs on jmgirard/wrapped.
- 2026-10-25: lessons used: 2026-10-24 (M001) Typst refuses paths outside the folder; 2026-10-25 (M002) `tests/_extensions` symlink and `fig-format: png`; 2026-10-25 (M003) a `Blocks` filter runs inside cells; 2026-10-25 (M004) verify.py leaves Typst's PDF as `tests/fixture.pdf`.
- 2026-10-25: plan gate chose raw Typst blocks from the pre-quarto grouping pass over the research page's `post-render` step, because S3 showed raw blocks work and the pass already builds each group for HTML; falsified by Quarto splitting or moving the raw blocks so that the `.typ` fails to compile or a `@fig-` label leaves its content block.
- 2026-10-25: plan gate chose wrap-it over meander, because the user chose wrap-it at the question set and meander lays out whole pages; falsified by wrap-it failing on a citation, a `@fig-` link, or a page break that meander handles.
- 2026-10-25: Typst `columns:` documents went to the new candidate "Check wrapped figures in Typst columns"; the research page does not cover them.
- 2026-10-25: criteria audit (full mode, fresh Opus reader): 8 findings, all taken with the narrower wording. AC4 measures the 30% box on the page image and lists its length cases (pc and ex differ from LaTeX, units in any case, unitless as px); AC7 runs AC1's membership check on stop-rule and contexts; AC3 limits same-page wrapping to figures that fit, since the fixture's raw-LaTeX spacing does not reach Typst; AC5's page-break promise names no overlap and no lost text instead of a README record alone; AC2 empties the package cache and names Quarto 1.10.19 (project renders and other versions go to Out); AC6 counts one warning per figure and adds T5; AC1 names the `box`; T3 adds Typst formats to three fixtures.
- 2026-10-25: T1 done: the four package files are copied from the Typst cache, and each one's git blob hash equals the typst/packages copy at `packages/preview/wrap-it/0.1.1`. `manual.pdf` is left out, as wrap-it's `typst.toml` excludes it. Probe on a scratch document, with the user cache's wrap-it moved aside: a planted marker showed in the PDF text, and with it removed it did not. Quarto 1.10.19 stages the extension's packages in `.quarto/typst/packages` and passes it as `--package-cache-path`. The AC2 run on the fixture itself is left for review.
- 2026-10-25: T2 done: a percent on `box(width:)` measured against wrap-it's auto column and gave a box about a quarter of the size it should be (page image), so the width sets the grid column through wrap-it's `columns:` argument and the box takes `width: 100%`. A code cell keeps its code above the call, and its wrapped floats move into the box. The `.typ` summary in `tests/verify.py` now records each call. Its 15 calls match the 15 HTML `.wrap-group`s, figure for figure and paragraph for paragraph (an HTML comment makes no Typst block).
- 2026-10-25: T3 done: `typst_length` and `checked_typst_length` sit beside the LaTeX pair, and `tex_default` became `format_default` for both formats. The new cases (`2pc` gap, `2IN` width with a `1ex` gap, unitless `300` width) went in `tests/defaults.qmd`, not `fixture.qmd`, so the LaTeX fixture's page placement stays as it is. defaults, stop-rule, and contexts render to Typst in `tests/verify.py`: 11, 1, and 4 calls, each matching its HTML group, and contexts prints the same 14 warnings in both formats. Page images show each stop-rule stop block below its figure.
- 2026-10-25: T4 done: `tests/refs.bib` (from spike S3) and `@smith2020` in the `#fig-md` paragraph, which replaces "dolor sit amet" so the line count stays; the LaTeX page of each of Figures 10 to 16 is the same as on main (`pdftotext` per page). New fixtures `typst-break.qmd` (a raw Typst `#v(14cm)` puts the figure near the page bottom) and `typst-ua.qmd`. In the Typst break render, the whole `wrap-content` box moves to page 2 and leaves page 1 blank below the text above it, because wrap-it puts the grid in an unbreakable `box`. `pdfinfo -struct` shows both alt texts in Figure tags, so no fallback was needed.
- 2026-10-25: T5 done: `pdftotext -bbox-layout` on the fixture's Typst page 1 puts the text block at x 90 to 522 pt and the text beside `#fig-md` ending at 381.4 pt, so with the 11 pt (1em) gutter the box is 129.6 pt, 30.0% of 432 pt; the `3in` box measures 216 pt. Page images 1 to 8 show each wrapped figure beside its text and each next block below it; the two near-bottom groups move to the next page whole. README gains a "PDF through Typst" section, and the intro, stop, context, and Notes lines now name Typst; Typst keeps a margin figure in the margin (`#notefigure` in contexts.typ). DESIGN Syntax, Function Families, and Architecture passes 4, 5, 7 and the research page's W3 and E10 rows are corrected in place. The plan's T5 named wrap-it #8 as a README limit; the break fixture showed the move to the next page instead, so the README states that, and states #1 as reported and untested.

## Decisions

## Review
