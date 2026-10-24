<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M002: Wrap figures in HTML output

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the first filter that users install from `main` with `quarto add jmgirard/wrapped`
- **Branch/PR:** m002-html-wrap

## Goal

A document rendered to HTML with the extension installed shows body text beside each figure marked `.wrap-left` or `.wrap-right`.

## Scope

**In:**
- `_extensions/wrapped/` with `_extension.yml` (version 0.1.0, `quarto-required: ">=1.9.36"`), `wrapped.lua`, and `wrapped.css`.
- Parsing in `wrapped.lua`. It reads the wrap class on a float, on the inner image of a div figure (E1), on an uncaptioned image, and on a code cell's enclosing div (D-001). The cell carry stays inside its own cell. It reads the `width` and `wrap-gap` attributes and the `wrapped:` metadata keys `width`, `gap`, and `breakpoint`.
- The HTML layout for the four captioned forms and the uncaptioned image, on plain pages and on pages with margin content.
- The stop rule and the `.wrap-clear` div in HTML.
- Every other format keeps a normal figure and prints one warning per render (W5).
- Fixtures under `tests/`, a verify script that compares rendered output with committed snapshots, and the `verify` slot in `cairn/PROFILE.md`.
- A `README.md` at the repository root with the install command and the syntax.

**Out:**
- Wrapping in PDF through LaTeX → M004. Until then, LaTeX keeps the normal figure from this milestone's fallback.
- Fallbacks in contexts that cannot wrap (E3 to E8), book projects (E13), and revealjs (E15) → M003.
- Typst → the candidate "Wrap figures in Typst PDF output". Word → the candidate "Wrap figures in Word output with frames". EPUB → the candidate "Use the HTML stylesheet for EPUB".
- A CI workflow → the candidate "Run the fixture renders in CI".

## Acceptance criteria

- [x] AC1: `quarto render tests/fixture.qmd --to html` exits with status 0. The fixture holds one wrapped captioned figure in each of four forms. The first two forms are a markdown image and a div figure, each with the class. The third is a div figure whose class sits on its inner image. The fourth is a knitr cell with `#| classes:`. In the HTML output, each of these figures is a `div.quarto-float` with its `wrap-left` or `wrap-right` class. Each keeps its "Figure N" caption text. Each is the target of an `<a href="#fig-…">` link in the body text.
- [x] AC2: The built-in browser opens the HTML of `tests/fixture.qmd` and `tests/margin.qmd` at a viewport 1200 px wide. `tests/margin.qmd` holds one `.column-margin` note and one wrapped figure. In both files, each wrapped figure and the wrapped uncaptioned image floats to its side, by computed `float`. The first line of the paragraph after each one sits beside it, within its vertical span. In each wrapped captioned figure, the rendered image width equals the content width of the figure box within 1 px. No `<img>` inside a wrapped float carries a wrap class or a percent inline width. The uncaptioned image takes its `width` attribute's share of the text column within 1 px. One wrapped figure sets `fig-align`. One wrapped figure has a caption of two or more lines, and that caption stays inside the box width. At a viewport 375 px wide, the computed `float` of each one is `none`.
- [x] AC3: The browser opens two fixtures at 1200 px, and each rule below holds within 1 px. `tests/fixture.qmd` sets no `wrapped:` metadata. In it, four figures show four rules. A percent `width` attribute sets the box width as that percent of the text column. An absolute-length `width` attribute sets that length. A `wrap-gap` attribute sets the computed margin of the box on its text side. A figure with neither attribute is 40% wide with a 1em margin on its text side. `tests/defaults.qmd` sets `wrapped: width`, `wrapped: gap`, and `wrapped: breakpoint: 800px`. In it, a figure with neither attribute takes the metadata width and gap. That figure has a computed `float` of `none` at a 700 px viewport and floats to its side at 1200 px.
- [x] AC4: `tests/stop-rule.qmd` holds the stop-rule cases. Each case is a wrapped figure, then a paragraph shorter than the figure, then one stop block. The first six stop blocks are an ATX heading, a bullet list, an ordered list, a blockquote, a pipe table, and a fenced code block. The other five are a knitr cell, a figure with no wrap class, a `callout-note`, a horizontal rule, and an empty `::: {.wrap-clear}` div. In the browser at 1200 px, each stop block starts at or below the bottom edge of its figure.
- [x] AC5: In `tests/fixture.qmd`, a knitr cell with `#| classes: wrap-right` makes no figure. A later markdown figure with no wrap class follows it, outside any cell. In the HTML output, the `div.quarto-float` of that later figure carries no `wrap-left` or `wrap-right` class.
- [x] AC6: `tests/fixture.qmd` renders with `--to pdf`, `--to typst`, and `--to docx`, and each render exits with status 0. The terminal output of each render holds the extension's fallback warning exactly once. The fixture wraps some captioned figures in HTML. In the kept `.tex`, each of them is Quarto's normal `\begin{figure}`. In the kept `.typ`, each of them is Quarto's normal `#figure(`.
- [x] AC7: In an empty temporary folder, `quarto add <path to this checkout> --no-prompt` installs `_extensions/wrapped/`. A document in that folder with one `.wrap-right` figure renders to HTML with `wrap-right` on its `div.quarto-float`. The repository root holds a `README.md`. Each syntax example in it appears in a fixture under `tests/`, with only ids and file names changed.

## Coverage

- AC1 → T1, T2, T6
- AC2 → T3, T6
- AC3 → T2, T3, T6
- AC4 → T4, T6
- AC5 → T2, T6
- AC6 → T5, T6
- AC7 → T1, T7

## Tasks

- [x] T1: Write `_extensions/wrapped/_extension.yml` with title, author, version 0.1.0, `quarto-required: ">=1.9.36"`, and the filter at `pre-quarto`. Load `wrapped.css` with `quarto.doc.add_html_dependency`.
- [x] T2: Parsing in `wrapped.lua`. Handle `FloatRefTarget` at the filter's top level. Carry a cell div's class in a `traverse = "topdown"` pass that scopes the carry to that cell (LESSONS, M001). Move a class from an inner image to its float (E1). Read `width` and `wrap-gap`, then the `wrapped:` metadata, then the defaults 40% and 1em. Remove the wrap class and the percent inline width from the inner image.
- [x] T3: HTML layout in `wrapped.css` and the filter. Set width and gap as CSS custom properties on the float. Float the uncaptioned image. Emit the breakpoint media query from the `breakpoint` value, since a custom property cannot set a media query. Make the float work on a page whose margin content turns the body into a CSS grid.
- [x] T4: The stop rule. After a wrapped figure, find the first block that is not a paragraph, and make it clear the float. Make an empty `.wrap-clear` div clear it.
- [x] T5: The format fallback. For any format that is not HTML, remove the wrap classes, keep the normal figure, and print one warning per render that names the format.
- [x] T6: Write `tests/fixture.qmd`, `tests/defaults.qmd`, `tests/margin.qmd`, and `tests/stop-rule.qmd`. Write `tests/verify.py` (Python standard library only). It renders each fixture and compares the wrapped-figure fragments of the HTML with committed snapshots. It exits with a non-zero status on a difference. Show it red on a planted change. Replace the `verify` slot in `cairn/PROFILE.md` with its command.
- [x] T7: Write `README.md` with the install command, the syntax for each form, the attributes, the metadata keys, the stop rule, and the formats that keep a normal figure. Run the `quarto add` check in a scratch folder. Check the Jupyter cell form once by hand in a throwaway venv in the session scratchpad, and record the result in the work log.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: tier check: not run — work named at the question set.
- 2026-10-24: idea vet: no concerns. CSS float and wrapfig are the usual wrap tools for their formats. quarto-cli#376 shows demand with 18 reactions. The syntax is DESIGN's planned interface, which spikes S1 and S2 tested.
- 2026-10-24: collision check: absorbed the candidate "Wrap figures in HTML and LaTeX output" across M002, M003, and M004. M001 (done) answered the spikes that this work builds on. D-001 governs the code-cell form. The inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-24: lessons used: the M001 lesson on handling `FloatRefTarget` at the top level with a top-down carry shapes T2.
- 2026-10-24: question set: what to plan — the HTML and LaTeX core as M002, M003, and M004.
- 2026-10-24: question set: dependencies — allowed. M004 adds wrapfig. The test command needs R with knitr and TinyTeX. The Jupyter cell form gets one check by hand (D-002).
- 2026-10-24: question set: CI — later, as the candidate "Run the fixture renders in CI".
- 2026-10-24: question set: back-to-back wrapped figures — the first falls back with no warning and the second wraps (D-003). M003 builds it.
- 2026-10-24: criteria audit (full mode): an Opus reader returned 20 findings on M002 to M004. 18 were fixed by narrowing: fixtures split by purpose, a margin-page check, the uncaptioned width, the gap read as a margin, named stop-block forms, and the carry case outside a cell. Also fixed were README examples kept in fixtures, M003's margin container and float id, M004's `\ref` and `??` checks, px to pt, and a page-break promise limited to the planted figure. The last fixes allow a ua-1 fallback and render the contexts and stop-rule fixtures to PDF.
- 2026-10-24: criteria audit: the E7 conflict went to the question set. The conflict between M002 AC6 and M004 AC1 is answered: each criterion binds its own milestone's head, and M004 replaces the PDF fallback.
- 2026-10-24: split into three milestones because the core passes the 7-criterion and 10-task tripwires. Each format is its own feature, as the roadmap already treats Typst and Word, so the three are not a feature series.
- 2026-10-24: plan gate chose a standard-library Python verify script that compares fragments with snapshots, with layout read in the built-in browser at review. It rejected a headless browser in the test command, because that adds a dependency. A layout break that the snapshots pass and review misses would falsify the choice.
- 2026-10-24: `_extension.yml` starts at version 0.1.0. The version stays unreleased until the user declares a release.
- 2026-10-24: implement started on branch m002-html-wrap.
- 2026-10-24: T1 to T3 done. Inside a user filter, a cell's figure is a Div marked `__quarto_custom_type=FloatRefTarget`, so the cell carry counts those Divs and applies only to that many floats. A float placed inside a new `pandoc.Div` vanished from the output, so the grouping pass finds a wrapped float by its `__quarto_custom_id` instead.
- 2026-10-24: chose a `.wrap-group` div with `display: flow-root` around each wrapped figure and its paragraphs. It contains the float, which also gives the stop rule, and it keeps the float working on a margin page whose body is a CSS grid. Quarto's `overflow: auto` on `.cell-output-display` trapped the cell float, so the CSS sets it to visible inside a group.
- 2026-10-24: a cell figure takes only an image width with a unit, because knitr writes the plot's pixel size as a unitless width. The README names `#| out-width:` for a cell figure's box width.
- 2026-10-24: `tests/_extensions` is a symlink to `../_extensions`, because Quarto does not find the extension from a subfolder outside a project. `tests/layout.js` holds the browser checks for AC2 to AC4. `.claude/launch.json` (ignored) serves `tests/` on port 8791.
- 2026-10-24: browser check at 1200 px: all five wrapped items in `tests/fixture.qmd` float, have text beside them, fill their box, and match their width and gap within 1 px. The margin page and the defaults fixture pass too. At 375 px nothing floats, and with `breakpoint: 800px` nothing floats at 700 px.
- 2026-10-24: T4 done. The `.wrap-group` gives the stop rule, so no clear divs are inserted. `tests/stop-rule.qmd` holds the 11 stop blocks of AC4, and at 1200 px each starts below its figure.
- 2026-10-24: T5 done. PDF, Typst, and docx renders of `tests/fixture.qmd` exit with status 0 and print one fallback warning each. Outside HTML the filter removes only the wrap class, so a figure keeps its image width. The fixture sets `fig-format: png` for Typst, because knitr's SVG device needs X11 libraries that this machine lacks.
- 2026-10-24: T6 done. `tests/verify.py` renders 7 fixture and format pairs and compares them with `tests/_snapshots/`. It sorts tag attributes, because Quarto writes a figure div's attributes in a changing order. It passed twice in a row. A planted defect (the cell carry ignoring the figure count) turned `fixture.html` red with `wrap-right` on `fig-plain`, and the revert passed. The PROFILE `verify` slot now names the script.
- 2026-10-24: T7 done. `README.md` covers install, the four forms, width and gap, document defaults, and the stop rule. A "README examples" section of `tests/fixture.qmd` holds each README example with only ids and file names changed. `quarto add <checkout> --no-prompt` in an empty scratch folder installed `_extensions/wrapped/`, and a `.wrap-right` figure there rendered with the class on its float.
- 2026-10-24: added `tests/rtl.qmd` for the README note on physical sides (E14). In the browser at 1200 px, `.wrap-right` sat on the right and `.wrap-left` on the left, each with text beside it. `#| out-width: "30%"` on a knitr cell gave a 30% box.
- 2026-10-24: Jupyter check by hand (throwaway venv, jupyter_core 5.9.1, matplotlib 3.11.2): a Jupyter cell figure with `#| classes: wrap-right` rendered with `wrap-right` on its float. A Jupyter cell with a class and no figure left the next figure without a wrap class.
- 2026-10-24: claim audit found a bug. The cell carry counted table floats, but only figures used up the carry, so a wrapped table cell passed its class to the next figure. Every float now uses up the carry, a table float loses the wrap class, and a cell starts a group only when its figure wrapped. Regression case: "A cell with a table" in `tests/fixture.qmd`. With the pre-fix filter, `fixture.html` went red with `wrap-right` on `fig-after-table`.
- 2026-10-24: claim audit: 75 claims read, 9 corrected — README.md, _extensions/wrapped/wrapped.lua, _extensions/wrapped/wrapped.css, tests/fixture.qmd, tests/verify.py, tests/layout.js
- 2026-10-24: claim audit re-read: all 9 corrections hold. The re-read found one comment above `local carry` made stale by the table fix, now corrected.
- 2026-10-24: implement done. `python3 tests/verify.py` passes all 8 renders, and `cairn_validate` passes. Status set to review.
- 2026-10-24: review checkpoint, findings not yet settled. The filter's `add_html_dependency` call no longer repeats the version, because Quarto validates only `name`. `_extension.yml` is again the one version marker, and the PROFILE release-walk says so. The diff-bug reviewer reads the branch at 49982e0, before this commit. verify has not run since this change.
- 2026-10-24: review return 1: diff-bug #1, a load-bearing defect. In HTML the filter removes the image `width` from every figure, wrapped or not. The same return carries the other fix-now items of the Review section's pass 1: diff-bug #2, #3, #4, #6, #7, #8, #12, and (c)1 to (c)5, and ripple #3, #4, #10, and #11.

## Decisions

## Review

Review of 2026-10-24 on branch m002-html-wrap at 63a1db4, Quarto 1.10.19. The branch contains origin/main (231f50e), so no merge was needed.

- AC1 evidence: `quarto render tests/fixture.qmd --to html` exited 0. `fig-md`, `fig-div`, `fig-inner`, and `fig-cell` (markdown image, div, class on inner image, knitr cell) are each a `div.quarto-float` with their class (`wrap-right`, `wrap-left`, `wrap-right`, `wrap-left`). Their captions read Figure 1 to Figure 4, and each is the target of one `<a href="#fig-…">` link.
- AC5 evidence: in the same HTML, `fig-plain` (a markdown figure after a knitr cell with `#| classes: wrap-right` and no figure, outside any cell) carries no wrap class.
- AC6 evidence: `tests/fixture.qmd` rendered with `--to pdf`, `--to typst`, and `--to docx`, each exiting 0. Each log holds the line "wrapped: <format> output does not wrap figures yet…" once (latex, typst, docx). The kept `.tex` holds 10 `\begin{figure}` environments, one for each labeled figure, including the 8 wrapped ones. It holds no `wrappedfigure`. The kept `.typ` holds a `#figure(` before each of the 8 wrapped figures' labels.
- AC2 evidence: built-in browser, `tests/layout.js` `report()` at a 1200 px viewport. In `fixture.html`, all 10 wrapped items (8 captioned figures and 2 uncaptioned images) float to their side, with the paragraph's first line beside them. Each captioned image's width equals its box's content width, and each uncaptioned image is 159.8 px, 20% of the 799 px column. None of the 8 images inside a wrapped float has a wrap class or a percent inline width. `fig-md` sets `fig-align="left"` and floats right. Its caption runs 2 lines and `fig-inner`'s runs 4, both inside the box. In `margin.html` (one `.column-margin` note, parent display `grid`), `fig-margin-page` passes the same checks. At 375 px, every item in both files has `float: none`.
- AC3 evidence: same tool at 1200 px, 799 px column. In `fixture.html`, `fig-md` (`width="30%"`) is 239.7 px. `fig-div` (`width="3in"`) is 288 px. `fig-inner` (`wrap-gap="2em"`) has a 34 px margin on its text side. `fig-cell`, with neither attribute, is 319.6 px (40%) with a 17 px (1em) margin. In `defaults.html`, `fig-defaults` takes the metadata: 199.8 px (25%) and a 30 px margin. It floats right at 1200 px and has `float: none` at 700 px.
- AC4 evidence: same tool at 1200 px on `stop-rule.html`. Each of the 11 cases is a wrapped figure, a one-line paragraph, and a stop block. Each stop block starts at or below its figure's bottom edge: the heading section (359 to 402), bullet list, ordered list, blockquote, pipe table, fenced code block, knitr cell, unwrapped figure, callout, horizontal rule, and `.wrap-clear` div (5104 to 5121).
- AC7 evidence: in an empty scratch folder, `quarto add /Users/jmgirard/github/wrapped --no-prompt` exited 0 and installed `_extensions/wrapped/` (`_extension.yml`, `wrapped.css`, `wrapped.lua`). A document there with one `.wrap-right` figure rendered with exit 0 and `wrap-right` on `div#fig-a.quarto-float`. `README.md` exists at the repository root. A script took each of its 8 fenced blocks, replaced ids and `.png` file names, and searched the fixtures. The `filters:` block, the 5 figure examples, the `wrapped:` block, and the `.wrap-clear` block each appear in `tests/fixture.qmd`, `tests/defaults.qmd`, or `tests/stop-rule.qmd`. The 8th block is the install command, `quarto add jmgirard/wrapped`.

Consistency gate:
- `cairn_validate.py`: all checks passed, exit 0. `cairn_impact.py` was skipped, because no DESIGN principle changed.
- Version markers: `_extension.yml` and the `add_html_dependency` call in `wrapped.lua` both hold 0.1.0. The PROFILE release-walk did not name the second marker, as it requires for a change that adds one. It now names it (fix now, review side).
- Verify render: `python3 tests/verify.py` matched all 8 renders, exit 0.
- Changelog: the slot says "none", so no entry was read.

Independent review, pass 1, on 49982e0:
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the filter removes the image `width` from every figure in HTML, wrapped or not, because `take_from_images` runs before the no-class return. `fig-plain` and an unwrapped `out-width` cell lose their widths. — fix now, floor return (a load-bearing defect for every user of the filter)
- diff-bug #2: a captioned image with no `#fig-` id (a Pandoc Figure) keeps its wrap class on the `<img>` and does not wrap, with no warning. `![Lab logo](logo.png){.wrap-right}` is a common spelling. — fix now
- diff-bug #3: an image inside a link, two images in one paragraph, and an image in a tight list item keep the wrap class and do not wrap, with no warning. — fix now: warn for a wrap class that the filter cannot place (list items stay M003's E8)
- diff-bug #4: a wrapped cell with no figure sets `found_wrap`, so the CSS loads and docx prints the fallback warning with nothing wrapped. — fix now
- diff-bug #5: a wrapped cell with two figures floats both, side by side. — follow-up: candidate "Handle a wrapped cell with two figures"
- diff-bug #6: a raw block such as an HTML comment right after the figure ends the group, so the text starts below the figure. — fix now
- diff-bug #7: an invalid `width` such as `banana` goes into `--wrap-width` with no warning. — fix now: warn and use the default
- diff-bug #8: a user `style` attribute on the float is overwritten. — fix now: keep it
- diff-bug #9: dashboards probably do not wrap, because the group gets `html-fill-container` (flex). Not verified. — follow-up: candidate "Check wrapped figures in dashboards"
- diff-bug #10: a change to the Quarto internals that the filter reads degrades with no error, losing the group or the cell wrap. — reject, false: no defect today, and the verify snapshots show such a change
- diff-bug #11: a wrapped figure in a callout, div, or list wraps inside it, an end-of-document figure gets an empty group, and other classes are kept. — noted, no defect (contexts are M003's)
- diff-bug #12: `tests/layout.js` gives NaN caption lines when line height is `normal`, and throws on a float with no image. — fix now
- diff-bug (c)1: the PDF and Typst snapshots record Quarto's own `\includegraphics` and `#figure(` lines, which is dependency behavior. — fix now: record only the figure environments and labels
- diff-bug (c)2: the HTML snapshots hold Quarto's figure markup and the lorem text, beyond what the filter changes. — fix now: record the filter's changes (classes, style, group members, image attributes)
- diff-bug (c)3: the breakpoint style is compared byte for byte. — fix now: record the breakpoint value
- diff-bug (c)4: the stop-rule, rtl, and margin snapshots and the README examples repeat code paths in the snapshot. — fix now: render those fixtures for the browser checks without a snapshot, with the README examples in their own fixture
- diff-bug (c)5: no snapshot records the image attributes of unwrapped figures, which let #1 through. — fix now: the regression test for #1
- blame-history #1: DESIGN and CLAUDE.md name `_extension.yml` as the one version marker, and `wrapped.lua` repeated the version. — fix now, fixed 5deb75c
- blame-history #2: the first of two back-to-back wrapped figures floats alone, against D-003. — follow-up: held by M003 AC3
- blame-history #3: a cell with several figures wraps every figure. — follow-up: candidate "Handle a wrapped cell with two figures"
- prior-review #1: "(added by M002)" in PROFILE is a history note in a standing file. — fix now, fixed 5deb75c (the sentence is gone)
- prior-review #2: the README does not say a knitr cell needs R with knitr. — reject, false: the extension needs no R, and Quarto states what an R cell needs
- ripple #1: CLAUDE.md and DESIGN name one version marker, and the filter added a second. — fix now, fixed 5deb75c
- ripple #2: the PROFILE release-walk named two markers but passes one to `cairn_versions.py`. — fix now, fixed 5deb75c
- ripple #3: the ROADMAP candidate "Wrap figures in HTML and LaTeX output" still says the fixture becomes the verify command and that `quarto add` finds no extension. — fix now: narrow the row to what is left
- ripple #4: DESIGN says "Not built yet", "No code yet", and no function families. — fix now: state the HTML filter as it is
- ripple #5: PROFILE test-doctrine and the research page say the docx test reads `word/document.xml`, and the docx snapshot holds only the warning. — reject, false: that text describes the test once Word wraps, and nothing wraps in Word yet
- ripple #6: a table with a wrap class prints no warning, against E5. — follow-up: held by M003 AC1
- ripple #7: a lone wrapped figure floats in an empty group, against E6 and E7. — follow-up: held by M003 AC2 and AC3
- ripple #8: a wrapped figure in a list, callout, or column layout wraps with no warning, against E3, E4, and E8. — follow-up: held by M003 AC1
- ripple #9: M003's title overlaps the format fallback that M002 ships. — reject, false: M003's scope is contexts and M002's is formats
- ripple #10: PROFILE init-detection says `_extension.yml` "arrives with the first code milestone". — fix now
- ripple #11: the PROFILE consistency-gate line says only that the verify render finishes. — fix now: say that verify passes
