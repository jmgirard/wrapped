<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M004: Wrap figures in LaTeX PDF output

- **Status:** review
- **Priority:** high
- **Depends on:** M002, M003
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the PDF that users get from a wrapped figure
- **Branch/PR:** m004-latex-wrap

## Goal

A document rendered to PDF through LaTeX with the extension installed shows body text beside each figure marked `.wrap-left` or `.wrap-right`.

## Scope

**In:**
- `_extensions/wrapped/wrapped.tex`, the `wrappedfigure` wrapper from `spikes/s2/wrapped.tex`, with a gap key added. The filter loads it and wrapfig for LaTeX output (D-002).
- The filter sets `fig-env` and `fig-pos` for each wrapped float, and wraps the uncaptioned image in raw LaTeX. LaTeX leaves M002's format fallback.
- Width, gap, and line conversions, and the `wrapped:` metadata, for LaTeX.
- The knitr cell form on the LaTeX path (D-001), the caption that ran into the footer (spike S2), and the figure near a page break (E10).
- Two-column documents (E17) and tagged PDF with `pdf-standard: ua-2` (E12). Quarto 1.10.19 ignores `ua-1` for LaTeX.
- `.tex` snapshots in `tests/verify.py`, and a LaTeX section in `README.md` that states wrapfig's limits.

**Out:**
- Typst → the candidate "Wrap figures in Typst PDF output". Word → the candidate "Wrap figures in Word output with frames".
- A full stop rule in LaTeX. DESIGN says LaTeX enforces it only in part, because wrapfig measures its own height. The README states this.

## Acceptance criteria

- [x] AC1: `quarto render tests/fixture.qmd --to pdf` with `keep-tex: true` exits with status 0. In the kept `.tex`, each captioned figure that the fixture wraps in HTML is in a `wrappedfigure` environment whose option names its side. The wrapped uncaptioned image is in one too. If the knitr form needs the `#| wrap:` cell option that D-001 names as the LaTeX fallback, the fixture's knitr figure uses it. The `.tex` holds a `\ref{fig-…}` for each `@fig-` link, and the PDF text from `pdftotext` holds no `??`.
- [x] AC2: `pdftoppm` makes page images of the fixture's LaTeX PDF. On them, each wrapped figure sits on its side. Lines of the paragraph right after it sit beside it on the same page, except for AC5's two figures, which move to the next page: lines of a later paragraph sit beside each of them on that page.
- [x] AC3: The kept `.tex` shows six conversions. A percent `width` attribute becomes the matching fraction of `\linewidth`, so `40%` becomes `0.4\linewidth`. A `px` length becomes `pt` at 0.75 pt per px. Any other absolute length stays as it is. A `wrap-gap` value sets `\columnsep` for that figure only. A `wrap-lines` value becomes `lines=<n>`. In `tests/defaults.qmd`, a figure that sets neither attribute takes the `wrapped: width` and `wrapped: gap` metadata.
- [x] AC4: The fixture places a wrapped figure with a caption of two or more lines near the bottom of a page. On the page images, the caption of each wrapped figure ends above the bottom edge of the text block. That edge is the lowest body line on a full page.
- [x] AC5: The fixture holds two wrapped figures that start too near the bottom of a page to fit there. The first sets no `wrap-lines`, and the second sets it. On the page images, no page shows narrowed lines with no figure beside them for the first. The README states that `wrap-lines` can narrow lines past a page break.
- [x] AC6: One fixture sets `classoption: twocolumn`, and one sets `classoption: [twocolumn]`. Each renders to PDF with exit status 0. In each, the wrapped figure is a `\begin{figure}` in the kept `.tex`, and the render prints one extension warning (E17). A fixture with `pdf-standard: ua-2` and `documentclass: article` holds a wrapped captioned figure and a wrapped uncaptioned image, each with its own `fig-alt` text. It renders to PDF with exit status 0. For each of the two, it is a `wrappedfigure` in the kept `.tex` and `pdfinfo -struct` lists a Figure tag with its `fig-alt` text, or it is a normal figure and the render prints one extension warning (E12). A copy of that fixture with `pdf-standard: ua-1` renders to PDF with exit status 0.
- [x] AC7: `tests/stop-rule.qmd` and `tests/contexts.qmd` each render to PDF with exit status 0. In the kept `.tex` of the contexts fixture, no float that falls back in HTML is in a `wrappedfigure` environment.

## Coverage

- AC1 → T1, T2, T3, T5
- AC2 → T1, T5
- AC3 → T2, T5
- AC4 → T3, T5
- AC5 → T3, T5
- AC6 → T4, T5
- AC7 → T5

## Tasks

- [x] T1: Copy the wrapper from `spikes/s2/wrapped.tex` to `_extensions/wrapped/wrapped.tex` and add a gap key that sets `\columnsep` inside the environment. Load it with `quarto.doc.include_file` and add wrapfig with `quarto.doc.use_latex_package`. Set `fig-env="wrappedfigure"` and `fig-pos` on each wrapped float for LaTeX. Remove LaTeX from the format fallback.
- [x] T2: Convert the width (percent to a `\linewidth` fraction, px to pt), the gap, and the line count, with the metadata defaults. Wrap the uncaptioned image in a raw `wrappedfigure` that keeps its alt text.
- [x] T3: Render the knitr cell form to PDF and confirm the moved class reaches LaTeX (D-001). Fix the caption that runs into the footer. Make the page-break figure keep its text beside it. Try wrapfig's floating placements (`R`, `L`) first.
- [x] T4: Detect `twocolumn` in `classoption`, as a string or a list, and fall back with one warning. Render the ua-2 fixture and read the alt text from the PDF's structure tree with `pdfinfo -struct`; render a ua-1 copy. Fall back with a warning where the alt text is lost.
- [x] T5: Add `.tex` snapshots for the fixtures to `tests/verify.py`. Make page images with `pdftoppm` and read them. Render the stop-rule and contexts fixtures to PDF. Write the LaTeX section of `README.md` with wrapfig's limits: lists, page breaks, figures in a row, two columns, narrowed headings, and the partial stop rule.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: question set: dependencies — wrapfig allowed as a LaTeX package that users' TeX distribution supplies. TinyTeX installs it on first use (D-002).
- 2026-10-24: criteria audit: see the M002 work log. The fixes here allow D-001's `#| wrap:` fallback, add the `\ref` and `??` checks, convert px to pt, limit the page-break promise to the planted figure, allow a ua-1 fallback, and render the stop-rule and contexts fixtures to PDF.
- 2026-10-24: the approach to the page-break figure is left to implement. wrapfig's floating placements are the first thing to try, because the S2 spike used the fixed placement and ran narrowed lines past the page break.
- 2026-10-25: started; branch m004-latex-wrap cut from main at a40abc1.
- 2026-10-25: T1–T3 land in one commit, because the wrapper, the conversions, and the page-break handling share `wrapped.tex`, `wrapped.lua`, and the fixture.
- 2026-10-25: T1: wrapfig reads `\columnsep` when it places the figure at a later paragraph start, after the environment ends, so a `\columnsep` set inside the environment does nothing. The environment sets it globally at its end, and hooks on wrapfig's `\WF@startwrapping` and `\WFclear` restore the document's value once the figure is placed or put out.
- 2026-10-25: T1: options read `side=left|right`; the wrapper maps them to wrapfig's floating placements L and R. The wrapper also loads wrapfig itself, beside the filter's `use_latex_package`.
- 2026-10-25: T1: a new wrappedfigure first ends an earlier wrap whose text is still narrowed (skips the lines left, then `\WFclear`), because wrapfig cannot place a figure during another wrap. Without this, figures two paragraphs apart floated and collided in the fixture.
- 2026-10-25: T1: a moved figure that still waits for a paragraph when the next wrappedfigure starts is put out centered with no text, in place of wrapfig's left-edge dump.
- 2026-10-25: T1: defect found and fixed: unnumbered headings have no hanging indent, so wrapfig placed a moved figure at a heading, whose group then undid the wrap and the next text ran over the figure. The wrapper turns `\WF@floathand` off inside `\@hangfrom`.
- 2026-10-25: T1: captions inside wrappedfigure use the caption package's `format=plain, justification=raggedright`, because a hanging, justified caption in a 150px box spread its words apart.
- 2026-10-25: T2: TeX reads pt, pc, in, cm, mm, em, and ex as written. Any other CSS unit or a CSS function gives the default with a warning naming LaTeX; a metadata value LaTeX cannot use falls back to the built-in default with a warning. A wrapped image's width becomes `100%` (`\linewidth` of the box) and its height goes. `wrap-lines` that is not a whole number above 0 is dropped with a warning; HTML drops the attribute silently.
- 2026-10-25: T2: the lone image's raw wrappedfigure keeps the image a Pandoc Image. Pandoc writes no `alt=` for it outside ua-1 (seen in the kept `.tex`); T4 checks ua-1.
- 2026-10-25: T2: contexts, unplaced images and divs, and empty wrapped cells now warn in LaTeX as in HTML; LaTeX no longer prints the format warning.
- 2026-10-25: T3: the knitr cell's moved class reaches LaTeX: `fig-cell` is a wrappedfigure in the kept `.tex`, so D-001's `#| wrap:` fallback is not needed.
- 2026-10-25: T3: floating placement (R, L) fixes both S2 problems: a figure that does not fit moves to the next paragraph start. Planted figures `fig-bottom` (fits, caption ends about one line above the text block's bottom), `fig-break`, and `fig-break-lines` (both move to the next page) are at the end of `tests/fixture.qmd`, placed with raw `\clearpage` and `\vspace`.
- 2026-10-25: T3: fixture change: short sections got a second paragraph, and raw `\clearpage` blocks start the clamp and logo sections on a new PDF page, so each main figure fits beside its first paragraph. Before that, the clamp figure moved and was put out with no text, and the logo figure sat beside its second paragraph.
- 2026-10-25: T5 part: `tests/verify.py` renders `defaults` to PDF, and the `.tex` snapshot now records each environment's options and reads only the document body. `verify.py` renders `fixture` to Typst after LaTeX, so the `fixture.pdf` left on disk is Typst's; page images need a separate `--to pdf` render.
- 2026-10-25: substantive amendment: AC6, Scope In, and T4 move the tagged-PDF check from `ua-1` to `ua-2` with `documentclass: article`. Quarto 1.10.19 prints "PDF standard 'ua-1' is not supported by LaTeX and will be ignored" and makes no structure tree, with or without the extension; `ua-2` with the default scrartcl fails ("\DocumentMetadata not supported!") with or without it. The extension's behavior is unchanged, so no stop.
- 2026-10-25: re-audit: AC6 (full) — first branch did not require the item to stay wrapped; the ua-1 exit-0 render was dropped; no named procedure for the structure tree; Scope and T4 still said ua-1. All four fixed in the wording above.
- 2026-10-25: re-audit: AC6 (full) — the fallback branch does not check alt text; "one extension warning" does not name the warning or the total; plant more `classoption` forms; README should say ua-1 gives no tags. Answered, no wording change (a third change would be a stop): both ua-2 items take the `wrappedfigure` branch with their alt text (`pdfinfo -struct` lists "A scatter plot of ten rising points" and "A small scatter plot"), so the fallback branch is not exercised; the snapshots pin each warning's exact text and count; plants `[a4paper, twocolumn]` and `twocolumn,10pt` each printed one two-column warning and kept `\begin{figure}`, and `onecolumn` wrapped with no warning; the README note goes in T5.
- 2026-10-25: T4: the wrapped uncaptioned image takes its `fig-alt` as its description, so Pandoc writes `alt=`; without this its tag read "plot.png", as it does with no extension, because Quarto writes `fig-alt` only for figures. Fixtures `twocolumn`, `twocolumn-list`, `pdf-ua`, `pdf-ua1`, and PDF renders of `contexts` and `stop-rule` joined `verify.py` with snapshots (21 renders pass).
- 2026-10-25: T5: README gains a "PDF through LaTeX" section (conversions, `wrap-lines`, ragged-right captions, the limits list, tagged PDF) and LaTeX mentions in the stop, context, and notes sections. Each limit was seen this session: stop-rule PDF pages show headings, lists, and quotes narrowed beside the figure and a heading narrowed after a page break; a probe with `wrap-lines="30"` ran narrowed lines onto the next page; the centered fallback showed in a fixture iteration. DESIGN's syntax note and architecture passes now name the LaTeX path.
- 2026-10-25: claim audit: 81 claims read, 1 corrected — README.md
- 2026-10-25: claim audit correction: in LaTeX, Quarto puts a captioned `.column-margin` image with no `#fig-` id in the body, with or without the extension; the README's margin bullet now says so.
- 2026-10-25: defect found by the claim auditor and fixed: in stop-rule.pdf, a moved figure was placed at the end of a callout (a group), lost its wrap, and the next figure's text ran over it. The `\@hangfrom` patch is replaced by one guard: wrapfig places a moved figure only at a paragraph on the group level where `\WF@startfloating` ran, which covers headings and callouts. Re-rendered: the fixture places all 15 figures with only the two planted ones moving; stop-rule case 9 sits beside outer text with no overlap.
- 2026-10-25: `\WFclear` is redefined to center a waiting figure, so the end-of-document dump matches the centered fallback; the ending of an earlier wrap moved from an `\aftergroup` (which fired one group early) into `\WF@startfloating`.
- 2026-10-25: second auditor finding, not fixed (the LaTeX stop rule is Out): a figure with no wrap class in the narrowed lines overlaps the wrapped figure's caption (stop-rule case 8), and a `wrap-clear` div has no effect in LaTeX. README limits now say both; candidate row "Honor wrap-clear and figures in LaTeX" added.
- 2026-10-25: all tasks done, `verify.py` 21 of 21 pass; status → review.
- 2026-10-25: amendment routed: AC2 — AC2 asks each wrapped figure to sit beside lines of the paragraph after it on the same page, but AC5's two planted figures cannot fit where that paragraph starts and wrapfig places a figure only at a paragraph start, so they sit beside later paragraphs on the next page (pages 11 and 13). The criterion conflicts with AC5; AC1 and AC3–AC7 verified and ticked. Status → in-progress for the amendment alone.
- 2026-10-25: re-audit: AC2 (full) — suggested "and no text overlaps it"; "which move to the next page" states a result, not a condition (reader: harmless, leave); the review's evidence line counts "figures 1–15" plus 16 and 17, while 15 figures wrap (PDF numbers include three unwrapped figures and the uncaptioned image has none); probes to plant (drop the clamp `\clearpage`, undo the group guard). Answered with no wording change: the overlap clause widens the promise and the audit decides toward the narrower one (no overlap shows on the fixture's 13 pages, and the README names overlap as a limit); the count is review evidence, which the re-review writes fresh; the criterion cites no plant.
- 2026-10-25: amendment return: AC2 — "Lines of the paragraph right after it sit beside it on the same page, except for AC5's two figures, which move to the next page: lines of a later paragraph sit beside each of them on that page."
- 2026-10-25: status → review.
- 2026-10-25: step-7 approval: m004-latex-wrap approved for merge

## Decisions

## Review

- 2026-10-25: route (d): no PR for the branch; `main` at a40abc1, unmoved since the cut. Copilot round off. `python3 tests/verify.py` on e87bec1: 21 of 21 renders pass.
- AC1: `quarto render fixture.qmd --to pdf` exit 0 (LuaTeX). HTML snapshot has 15 wrapped boxes; the kept `.tex` body has 15 `wrappedfigure` environments in the same order with matching sides (12 captioned floats and figures, the Lab-logo and `#logo` captioned images, and the uncaptioned image). The knitr `fig-cell` is one (side=left) with no `#| wrap:` option in the fixture. All 15 `@fig-` links in the fixture have a `\ref{fig-…}`; `pdftotext` finds 0 `??`.
- AC2: not met as written. `pdftoppm -r 50` page images of the LaTeX render (13 pages): figures 1–15 each sit on their side beside lines of the paragraph right after them on the same page (pages 1–9). Figures 16 (`fig-break`) and 17 (`fig-break-lines`), which AC5 plants too near a page bottom to fit, move to pages 11 and 13 and sit beside the third and fourth paragraphs after them; the paragraph right after each stays full width on pages 10 and 12. So the criterion conflicts with AC5's planted figures: routed for amendment, not ticked.
- AC3: kept `.tex`: `30%` → `width=0.3\linewidth` (fig-md), `150px` → `width=112.5pt` (fig-bottom), `3in` stays `width=3in` (fig-div), `wrap-lines="12"` → `lines=12` (fig-break-lines). `wrap-gap="2em"` → `gap=2em`; a scratch copy of the kept `.tex` that logs `\columnsep` inside `\WF@startwrapping` shows 21.9pt at the placement of each of the two `2em` figures, 10.95pt (`1em`) at the other 13, and 10.0pt (the document value) right after every placement. `tests/defaults.qmd` (`wrapped: width: 25%, gap: 30px`) → `[side=right,width=0.25\linewidth,gap=22.5pt]` for a figure with neither attribute.
- AC4: fig-bottom (caption of five lines in a 112.5pt box) is placed on page 9 after `\vspace{0.6\textheight}`. `pdftotext -bbox`: the lowest body line on a full page (pages 10 and 12) ends at y=650.1pt; the lowest word on every page that holds a caption ends at or above 646.1pt, and fig-bottom's caption ends at 615.3pt, so each caption ends above that edge.
- AC5: fixture holds `fig-break` (no `wrap-lines`) and `fig-break-lines` (`wrap-lines="12"`), each after `\clearpage` and `\vspace{0.75\textheight}`. Both move to the next page (pages 11 and 13). Page 10, where `fig-break` started, shows no narrowed lines: its rightmost word ends at x=528.8pt, the full line width, and the page image shows full-width lines. `README.md:200-202` states that a larger `wrap-lines` value can narrow lines past a page break.
- AC6: `twocolumn.qmd` (`classoption: twocolumn`) and `twocolumn-list.qmd` (`classoption: [twocolumn]`) render with exit 0 in `verify.py`; each snapshot shows `figure: fig-two` and one warning, "LaTeX does not wrap figures in a two-column document, so wrapped figures render as normal figures." `pdf-ua.qmd` (`pdf-standard: ua-2`, `documentclass: article`) renders with exit 0; its kept `.tex` has both items as `wrappedfigure` with `alt=`, and `pdfinfo -struct` lists `Figure <ID.014> ["A scatter plot of ten rising points"]` and `Figure <ID.029> ["A small scatter plot"]`, each item's own `fig-alt`. `pdf-ua1.qmd` (`ua-1`) renders with exit 0.
- AC7: `stop-rule.pdf` and `contexts.pdf` render with exit 0 in `verify.py`. In the contexts HTML snapshot only `fig-second` keeps a wrap class; in the contexts `.tex` snapshot `fig-second` is the only `wrappedfigure`, and every float that falls back in HTML (`fig-panel-a`, `fig-sub-wrapped`, `fig-layout-cell`, `fig-list`, `fig-callout`, `fig-column`, `fig-tab`, `fig-before-heading`, `fig-first`, and three with no id) is a `figure`; `fig-margin`, `fig-aside`, and `fig-margin-cell` are `marginfigure` environments in the kept `.tex` body, which holds no other `wrappedfigure`.
- re-review after the AC2 amendment (6b4e3d2): `main` still a40abc1; `git diff e87bec1 HEAD` outside `cairn/` is empty, so the 21-render verify run and the LaTeX render above stand for the current code.
- AC2 (amended): page images of the LaTeX render (13 pages, `pdftoppm -r 50`). 15 figures wrap (AC1). The 13 that AC5 does not plant each sit on their side beside lines of the paragraph right after them on the same page: fig-md and fig-div (p1), fig-inner and fig-cell (p2), the uncaptioned image (p3), the Lab-logo image and fig-comment (p5), fig-bad-width and fig-styled (p6), fig-clamp and fig-raw (p7), `#logo` (p8), fig-bottom (p9). AC5's fig-break (left) and fig-break-lines (right) move to pages 11 and 13 and sit on their sides beside lines of later paragraphs there.
- gate: `cairn_validate.py` exit 0, all checks pass; no DESIGN principle changed, so no `cairn_impact`. Profile gate: one version marker (`_extension.yml` 0.1.0, unchanged on the branch); verify 21 of 21 pass on the review code; changelog "none", no entry read.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the filter reads only `classoption`, so a class that is two-column by default (IEEEtran rendered: a wrappedfigure in a column, no warning) is not detected — follow-up, row "Detect two-column LaTeX classes and gaps"; README now says only `classoption` is read, fixed a4a855b
- diff-bug #2: `%g` writes an exponent, so `width="0.0001%"` gives `1e-06\linewidth` and LaTeX stops — fix now: decimals with no exponent, regression `fig-bad-lines` in `tests/tex-options.qmd` (`gap=0.00001\linewidth`), fixed a4a855b
- diff-bug #3: global save and restore of `\columnsep` leaks a local value, and a `multicols` that starts while a figure waits takes the figure's gap — follow-up, row "Detect two-column LaTeX classes and gaps"
- diff-bug #4: `twocolumn=false` matched the two-column pattern (confirmed with the old pattern in `pandoc lua`) — fix now: options parsed one by one, `twocolumn`, `=true`, `=on`, `=yes` count; `tests/tex-options.qmd` sets `twocolumn=false` and wraps, fixed a4a855b
- diff-bug #5: LaTeX dropped an image's `height` with no warning — fix now: an image with a height keeps it and loses its width, giving `width=\linewidth,height=1in,keepaspectratio` (`fig-height` in `tests/tex-options.qmd`); README says so, fixed a4a855b
- diff-bug #6: the HTML lone-image path kept `wrap-lines` as `data-wrap-lines` — fix now, fixed 9989f94
- diff-bug #7: `wrapped.tex` needs a 2020-10 or newer LaTeX kernel, which Quarto's own template does not — reject, edge: a TeX distribution older than 2020 is outside Quarto 1.9's common use (it installs current TinyTeX), and the effect is a LaTeX error
- diff-bug #8: the end-of-wrap skip follows `wrap-lines`, so a large value leaves blank lines before the next figure — follow-up, absorbed into row "Honor wrap-clear and figures in LaTeX"
- diff-bug #9 (tests): `pdf-ua1` repeats `pdf-ua` — reject, planned change: AC6 names the ua-1 render
- diff-bug #10 (tests): nothing pinned the alt text — fix now: the `.tex` snapshot records each image's `\includegraphics` options, so `alt={…}` shows in `pdf-ua.pdf.txt`; kinds, labels, and environment options unchanged in all 8 changed PDF snapshots, fixed a4a855b
- diff-bug #11 (tests): `stop-rule.pdf` repeats one branch 11 times — reject, planned change: AC7 names the render, and the snapshot is the profile's test form
- diff-bug #12 (tests): no snapshot pins `wrapped.tex` behavior — reject, planned change: the profile keeps layout out of the verify command, and AC2, AC4, and AC5 check layout on page images
- diff-bug #13 (tests): the `tex_default` and `checked_lines` warnings had no test — fix now: `tests/tex-options.qmd` fires both (`50vw` metadata, `wrap-lines="banana"`), fixed a4a855b
- blame-history #1: a moved figure crosses a heading, which DESIGN's stop-rule sentence did not say — fix now: DESIGN states it, fixed 9989f94
- blame-history #2: a two-column document whose only wrapped figure precedes a heading still prints the two-column warning — reject, false: D-003 and E6 govern the per-figure warning; the one format warning follows `found_wrap`, as for Typst and Word since M003
- blame-history #3: same as diff-bug #6 — fix now, fixed 9989f94
- blame-history #4: Typst and Word floats keep the `wrap-lines` attribute — reject, false: `fixture.typ` and `word/document.xml` hold "wrap-lines" only in the fixture's heading and body text
- blame-history #5: the image-width column could not tell the box width from the author's — fix now: same change as diff-bug #10, fixed a4a855b
- blame-history #6: the AC2 amendment relaxes the paragraph-after rule for moved figures — reject, planned change: a recorded amendment return
- prior-review #1: the README `wrap-lines` example was not in `tests/readme.qmd` — fix now, fixed 9989f94
- prior-review #2: the README's general stop rule named `wrap-clear` with no LaTeX note — fix now, fixed 9989f94
- prior-review #3: "(corrected M004)" marks in DESIGN — reject, false: the tracking rules require that mark on a correction of a current-knowledge file
- prior-review #4: AC2 was reworded with no user approval — reject, false: a wording-only amendment takes no stop under the rules, and the work log records it
- prior-review #5: context warnings now print in LaTeX; ROADMAP W2 row still open — noted, no action (planned; hygiene graduates the row)
- ripple #1: README said only HTML prints no warning for a figure before a heading — fix now, fixed 9989f94
- ripple #2: research E12 row promised ua-1 tags — fix now, corrected in place, fixed 9989f94
- ripple #3: same as prior-review #1 — fix now, fixed 9989f94
- ripple #4: research W2 limits said a page break "fails" — fix now, corrected in place, fixed 9989f94
- ripple #5: research W2 row gave the spike's `fig-pos` — fix now, row corrected, fixed 9989f94; line 69 is the dated spike record and stays
- ripple #6: DESIGN Known issues says none while the overlap is documented — reject, false: the overlap has a candidate row, and Known issues holds only limitations with no planned work
- ripple #7: ROADMAP row "Wrap figures in HTML and LaTeX output" still says W2 is left — reject, planned change: step 9 hygiene graduates it
- ripple #8: DESIGN and CLAUDE.md name Typst and Word as goals — reject, false: they state scope, and the README says those formats are planned
- re-check after fixes: `python3 tests/verify.py` on a4a855b, 22 of 22 pass. The fixes leave the fixture's `.tex` environment and image options unchanged (snapshot comparison above), so the page-image evidence stands.
- snapshot: changed-snapshot list empty — the repo's snapshots live under `tests/_snapshots/`, not a `_snaps` or `__snapshots__` directory.
