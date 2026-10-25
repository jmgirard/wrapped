<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M005: Wrap figures in Typst PDF output

- **Status:** review
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

- [x] AC1: `quarto render tests/fixture.qmd --to typst` with `keep-typ: true` exits with status 0 and prints no "typst output does not wrap figures yet" warning. In the kept `.typ`, each figure and image that is in a `.wrap-group` in the fixture's HTML render is inside the `box` that is the first content argument of its own `wrap-content(` call, whose `align` names the figure's side. The paragraphs of that `.wrap-group` are in the call's second content argument, and no other block is. The `.typ` imports `wrap-content` from `@preview/wrap-it:0.1.1`.
- [x] AC2: With Quarto 1.10.19, the fixture's Typst render loads wrap-it from the extension's bundled copy. With the Typst package cache emptied and a marker planted in the bundled copy, the marker shows in the PDF text from `pdftotext`. With the marker removed, it does not.
- [x] AC3: `pdftoppm` makes page images of the fixture's Typst PDF. On them, each wrapped figure whose full height fits on the page below its start sits on its side, and lines of the first paragraph of its group sit beside it on the same page. The block after each such group starts below the figure's bottom edge.
- [x] AC4: On the fixture's Typst page image, the box of `#fig-md` (`width="30%"`) measures 30% ± 2% of the text-block width. In the kept `.typ` of `tests/fixture.qmd` and `tests/defaults.qmd`, each width and gap value that the two fixtures set (among them `30%`, `3in`, `2em`, `150px`, `banana`, `wide`, `clamp(150px, 30%, 400px)`, `2VMIN`, and the added `2pc`, `1ex`, `2IN`, and `300`) becomes the Typst length this rule gives. A percent stays a percent. A px length, or a number with no unit, becomes pt at 0.75 pt per px. A `pc` length becomes pt at 12 pt per pc. A `pt`, `mm`, `cm`, `in`, or `em` length in any letter case keeps its number with the unit in lowercase. Any other value takes the default, with a warning. A `wrap-gap` value goes through the same rule and becomes that call's `column-gutter`. `tests/defaults.qmd` renders to Typst with exit status 0, and a figure there that sets neither attribute takes the `wrapped: width` and `wrapped: gap` metadata.
- [x] AC5: The fixture holds a `@citation` in the text of a wrapped group, with a bibliography. The Typst PDF text from `pdftotext` holds the rendered citation, and the page image shows it beside the figure. A Typst fixture holds a wrapped figure that starts too near the bottom of a page to fit there. It renders with exit status 0. On its page images, the figure and its caption sit whole on one page, and no text line overlaps the figure. Its `pdftotext` text holds every paragraph of the group. The README states the gap that the page images show before the figure.
- [x] AC6: A fixture with `pdf-standard: ua-1` holds a wrapped captioned figure and a wrapped uncaptioned image, each with `fig-alt`. It renders to Typst with exit status 0. For each of the two, the structure tree of the PDF holds its alt text, or it renders as a normal figure and the render prints one extension warning for that figure. The README names which of the two holds.
- [x] AC7: `tests/stop-rule.qmd` and `tests/contexts.qmd` each render to Typst with exit status 0. For each, AC1's membership check holds: each `wrap-content` call in the kept `.typ` holds in its second content argument exactly the paragraphs of the matching `.wrap-group` in the HTML render, and no float that falls back in HTML is inside a `wrap-content(` call. Each render prints the same extension warnings as the HTML render of that fixture.

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
- [x] T6: Review return 1: keep the sides physical in right-to-left Typst text, warn for a percent width of 100% or more in Typst, and fix the other fix-now findings that the Review section lists for this pass.

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
- 2026-10-25: claim audit: 60 claims read, 2 corrected — `_extensions/wrapped/wrapped.lua` (the `clean_image` height sentence was false for Typst, where an image with a height was cut off at the box edges; the code now gives a Typst image the box width and drops its height, and `#fig-height` in `tests/defaults.qmd` records `image-width=yes`, where before the fix the `.typ` had `height: 2in` and no width; the `TYPST_UNITS` comment now says em is not absolute). Both re-read against the render and the code.
- 2026-10-25: all tasks done; verify passes (27 renders); status set to review.
- 2026-10-25: review return 1: right-to-left Typst documents swap the sides (diff-bug #1), and a percent width of 100% or more squeezes or drops the text with no warning (diff-bug #2). The same pass fixes the other fix-now findings in the Review section: height warning and README line, `.typ` summary (block kinds, alt text, citations, unparsed calls, figure chunk), the `.wrapped-image` crash, a Typst metadata-default test, the research page's post-render lines, the `#fig-clamp` prose, and a LaTeX page-1 check.
- 2026-10-25: T6 added for review return 1 (minor amendment).
- 2026-10-25: T6 done. Quarto's Typst template sets `lang` and never `dir`, so the direction is read in Typst: the header now defines `wrapped-rtl`, `wrapped-side`, and `wrapped-columns` after the import, and each call is `#context wrap-content(align: top + wrapped-side(<side>), columns: wrapped-columns(<side>, <width>), …)`; in `tests/typst-rtl.qmd` (`lang: he`) `pdftotext -bbox` puts the right figure's caption at x 396 to 517 and the left figure's at x 95 to 214. A percent of 100% or more, on a figure or in the metadata, takes the default with a warning (`tests/typst-options.qmd`). A height in Typst warns. `typst_group` returns a user `.wrapped-image` div's group as it is. The `.typ` summary names each block's kind, records alt text and citations, counts unread calls, and reads a figure's image only before its `kind:` line; planted defects (a heading, a `#block[`, a broken opening) each showed in a scratch copy, and the figure-line fix changed exactly the two lines that had read a later image's width. LaTeX: `main` and the branch put Figures 1 to 17 on the same pages, and page 1 matches. verify: all 29 renders pass.
- 2026-10-25: T6 complete; status set to review.
- 2026-10-25: claim audit (T6 lines): 41 claims read, 3 corrected — `wrapped.lua` (at 100% the text runs one word to a line outside the text area; above 100% part drops), `README.md` (a metadata width of 100% or more takes the built-in 40%), `wrap-mechanisms.md` (the planned layout now says one `pre-quarto` entry and a planned docx `post-render` step). The `typst-options.qmd` height is now `2in`, so the page image shows the image about 1 in tall in its 1.5 in box. The reader confirmed the 11 right-to-left languages on Typst 0.15.1 and physical sides under `he`, `ar`, `he-IL`, and raw `#set text(dir: rtl)`. verify: all 29 renders pass.

## Decisions

## Review

Evidence gathered 2026-10-25 on branch head cb530ea, Quarto 1.10.19, `main` at bd9a291 (not moved since the cut).

- AC1: `quarto render fixture.qmd --to typst` exit 0, no "does not wrap figures yet" warning, the `#import "@preview/wrap-it:0.1.1": wrap-content` line present. A scratchpad script read the HTML `.wrap-group`s with `verify.html_summary` and the `.typ` calls with `verify.typ_summary`: 15 groups, 15 calls, each call's box holds the group's figure or image and `align` its side, and each call's second argument holds the group's paragraphs (33 blocks, none a heading, list, raw call, or code).
- AC2: user cache `~/Library/Caches/typst/packages/preview/wrap-it` moved aside and `tests/.quarto/typst` removed; with `wrap-content` wrapped to print `WRAPITMARKER`, the fixture's Typst PDF text held 15 marker lines (one per call); with the file restored and `.quarto/typst` removed again, 0. Bundled file restored to blob 3312efb, cache restored, `git status` clean.
- AC3: `pdftoppm -r 40` page images of the fixture's Typst PDF, pages 1, 2, 4 to 8 read (page 3 holds no wrapped figure): all 15 wrapped figures sit on their side with lines of the first paragraph of the group beside them on the same page, and each next block (heading, raw-HTML paragraph on page 6, Bibliography) starts below the figure. The two near-bottom groups (Figures 16, 17) start at a page top whole.
- AC4: page 1 `pdftotext -bbox-layout`: text block 90 to 522 pt (most common line end, 9 lines; US Letter less 1.25 in margins = 432 pt), text beside `#fig-md` ends at 381.4 pt (6 lines), gutter 11 pt (1em at 11 pt): box 129.6 pt = 30.00%. Snapshots `fixture.typst.txt` and `defaults.typst.txt` (verify green): `30%` → `30%`, `3in` → `3in`, `2em` gap → `2em`, `150px` → `112.5pt`, `2pc` → `24pt`, `2IN` → `2in`, `300` → `225pt`; `banana`, `wide`, `clamp(…)`, `2VMIN`, `1ex` each take the default with a warning; defaults' `#fig-defaults` takes `25%` and `22.5pt` (30px) from the metadata; `tests/defaults.qmd` exit 0.
- AC5: fixture page 1 `pdftotext` line 4 reads "Smith and J. Doe [1]", and the page image shows it in the text beside Figure 1; the Bibliography lists the entry. `typst-break.qmd` exit 0: page 1 holds the text above the figure, page 2 holds Figure 1 and its caption whole with no text over it, and `pdftotext` holds each of the group's 3 paragraphs once. README line 249 states that the rest of the page before stays blank.
- AC6: `typst-ua.qmd` (`pdf-standard: ua-1`) exit 0, no extension warning; `pdfinfo -struct` lists `Figure ["A scatter plot of ten rising points "]` and `Figure ["A small scatter plot "]`. The README's Typst section names this branch ("keeps its `fig-alt` text as its alt text"); `verify.py` renders the fixture with a snapshot.
- AC7: same script on `stop-rule.qmd` and `contexts.qmd`: both exit 0; 11 calls for 11 HTML groups and 1 call for 1 group, each matching in figure and paragraphs (13 blocks, all paragraphs); warnings identical to the HTML render (0 and 14).
- Gate: `cairn_validate.py` all checks passed; no principle changed, so no `cairn_impact`. Profile gate: the one version marker (`_extension.yml` `version: 0.1.0`) is unchanged by the branch; `python3 tests/verify.py` "all 27 renders pass"; changelog slot "none", nothing read.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: in a right-to-left Typst document (`lang: he`, or `dir: rtl`) the sides swap, because wrap-it's grid follows the text direction; README promises physical sides — fix now (floor return 1)
- diff-bug #2: a percent width of 100% or more leaves the text a sliver of a column (100%) or drops it from the PDF with no warning (120%) — fix now (floor return 1) for percents; too-wide absolute lengths go to the new candidate "Bound wide absolute widths in Typst"
- diff-bug #3: an image `height` is dropped in Typst with no warning and no README line — fix now
- diff-bug #4: the `.typ` summary records every block beside the box as "p", so a heading or block there would not change the snapshot; a figure chunk can read a later image's width; `--update` would write an empty wraps section without notice — fix now
- diff-bug #5: a user div with the internal `.wrapped-image` class crashes the Typst render (nil `open` in `typst_group`) — fix now
- diff-bug #6: Typst width warnings name the fallback in CSS units — reject, style: the LaTeX warnings use the same pattern on purpose (the value the user can write)
- diff-bug #7: alt text and the page-break move rest on manual evidence — alt text: fix now (snapshot records it); page placement: reject, planned change: AC5 names page images as its procedure, as M004 did for LaTeX
- blame-history #1: same as diff-bug #3 — fix now
- blame-history #2: the `#fig-md` paragraph edit may move M004's tuned LaTeX page-1 placement — fix-now check: re-read the LaTeX page 1 image in the return
- blame-history #3: two wrapped figures in one code cell share one Typst box with the first figure's options — follow-up: absorbed into the candidate "Handle a wrapped cell with two figures"
- blame-history #4: `wrap-lines` is silent in Typst — reject, planned change: Scope Out keeps it LaTeX only and the README says it does nothing in Typst
- blame-history #5: README's warning sentence is broader than the Typst warning text — reject, false: every value it names does print a warning
- prior-review #1: same as diff-bug #3 (M004 diff-bug #5's rule) — fix now
- prior-review #2: Typst alt text is not pinned by a snapshot (M004 diff-bug #10's rule) — fix now, with diff-bug #7
- prior-review #3: the Typst metadata-default warning has no test (M004 diff-bug #13's rule) — fix now
- prior-review #4: the README citation claim has no snapshot check — fix now: the `.typ` summary records citations per call
- prior-review #5: two figures in one cell — follow-up, same row as blame-history #3
- prior-review #6: Typst and LaTeX renders share output names — reject, false as a defect: no snapshot is affected, and LESSONS already records it
- ripple #1, #2, #3: `wrap-mechanisms.md` line 131 bullet, the "after the `post-render` step" Typst sketch, and the planned layout's post-render entry are stale — fix now
- ripple #4: `tests/fixture.qmd` prose at `#fig-clamp` names only LaTeX — fix now, with a LaTeX page check
- ripple #5: the Typst candidate row still asks for the citation — reject, planned change: step 9 hygiene graduates the row
- ripple #6: the W2 and W4 rows name `post-render` fallbacks — reject, false: they describe planned LaTeX and Word paths, still accurate as plans
- Fix-now items of pass 1 landed in 5c56778 and 12bd0fc (T6): diff-bug #1 to #5 and #7 (alt part), blame-history #1 and #2, prior-review #1 to #4, ripple #1 to #4.

Pass 2 evidence, 2026-10-25, head 12bd0fc, `main` at bd9a291 (unchanged).

- AC1 (pass 2): fixture Typst render exit 0, import present, no "yet" warning; 15 calls for 15 HTML groups, each matching in box content and paragraphs; `align: top + wrapped-side(<side>)` names the figure's side; the new summary names no non-paragraph block and no unread call.
- AC2 (pass 2): caches emptied as in pass 1; planted marker 15 lines, removed 0; bundled file restored to blob 3312efb, cache restored, tree clean.
- AC3 (pass 2): page images 1 to 8 are pixel-identical (md5) to pass 1 except page 6, whose `#fig-clamp` prose changed; page 6 read again, each figure beside its text and each next block below it.
- AC4 (pass 2): box 129.6 pt of 432 pt = 30.00%; the conversions in the snapshots are unchanged in value (the call form now reads `wrapped-columns(<side>, <width>)`); verify green.
- AC5 (pass 2): page 1 text line 4 "Smith and J. Doe [1]"; typst-break page 1 holds neither the caption nor the group's first paragraph, page 2 holds both; page images identical to pass 1.
- AC6 (pass 2): `pdfinfo -struct` lists both Figure alt texts.
- AC7 (pass 2): stop-rule 11 calls and contexts 1 call match their HTML groups; warnings equal to HTML (0 and 14).
- Gate (pass 2): `cairn_validate.py` all checks passed; `tests/verify.py` "all 29 renders pass" at 12bd0fc; version marker unchanged at 0.1.0; changelog "none".
- spawned: diff-bug, blame-history, prior-review, ripple
