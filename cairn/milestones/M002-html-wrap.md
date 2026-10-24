<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M002: Wrap figures in HTML output

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the first filter that users install from `main` with `quarto add jmgirard/wrapped`
- **Branch/PR:** —

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

- [ ] AC1: `quarto render tests/fixture.qmd --to html` exits with status 0. The fixture holds one wrapped captioned figure in each of four forms. The first two forms are a markdown image and a div figure, each with the class. The third is a div figure whose class sits on its inner image. The fourth is a knitr cell with `#| classes:`. In the HTML output, each of these figures is a `div.quarto-float` with its `wrap-left` or `wrap-right` class. Each keeps its "Figure N" caption text. Each is the target of an `<a href="#fig-…">` link in the body text.
- [ ] AC2: The built-in browser opens the HTML of `tests/fixture.qmd` and `tests/margin.qmd` at a viewport 1200 px wide. `tests/margin.qmd` holds one `.column-margin` note and one wrapped figure. In both files, each wrapped figure and the wrapped uncaptioned image floats to its side, by computed `float`. The first line of the paragraph after each one sits beside it, within its vertical span. In each wrapped captioned figure, the rendered image width equals the content width of the figure box within 1 px. No `<img>` inside a wrapped float carries a wrap class or a percent inline width. The uncaptioned image takes its `width` attribute's share of the text column within 1 px. One wrapped figure sets `fig-align`. One wrapped figure has a caption of two or more lines, and that caption stays inside the box width. At a viewport 375 px wide, the computed `float` of each one is `none`.
- [ ] AC3: The browser opens two fixtures at 1200 px, and each rule below holds within 1 px. `tests/fixture.qmd` sets no `wrapped:` metadata. In it, four figures show four rules. A percent `width` attribute sets the box width as that percent of the text column. An absolute-length `width` attribute sets that length. A `wrap-gap` attribute sets the computed margin of the box on its text side. A figure with neither attribute is 40% wide with a 1em margin on its text side. `tests/defaults.qmd` sets `wrapped: width`, `wrapped: gap`, and `wrapped: breakpoint: 800px`. In it, a figure with neither attribute takes the metadata width and gap. That figure has a computed `float` of `none` at a 700 px viewport and floats to its side at 1200 px.
- [ ] AC4: `tests/stop-rule.qmd` holds the stop-rule cases. Each case is a wrapped figure, then a paragraph shorter than the figure, then one stop block. The first six stop blocks are an ATX heading, a bullet list, an ordered list, a blockquote, a pipe table, and a fenced code block. The other five are a knitr cell, a figure with no wrap class, a `callout-note`, a horizontal rule, and an empty `::: {.wrap-clear}` div. In the browser at 1200 px, each stop block starts at or below the bottom edge of its figure.
- [ ] AC5: In `tests/fixture.qmd`, a knitr cell with `#| classes: wrap-right` makes no figure. A later markdown figure with no wrap class follows it, outside any cell. In the HTML output, the `div.quarto-float` of that later figure carries no `wrap-left` or `wrap-right` class.
- [ ] AC6: `tests/fixture.qmd` renders with `--to pdf`, `--to typst`, and `--to docx`, and each render exits with status 0. The terminal output of each render holds the extension's fallback warning exactly once. The fixture wraps some captioned figures in HTML. In the kept `.tex`, each of them is Quarto's normal `\begin{figure}`. In the kept `.typ`, each of them is Quarto's normal `#figure(`.
- [ ] AC7: In an empty temporary folder, `quarto add <path to this checkout> --no-prompt` installs `_extensions/wrapped/`. A document in that folder with one `.wrap-right` figure renders to HTML with `wrap-right` on its `div.quarto-float`. The repository root holds a `README.md`. Each syntax example in it appears in a fixture under `tests/`, with only ids and file names changed.

## Coverage

- AC1 → T1, T2, T6
- AC2 → T3, T6
- AC3 → T2, T3, T6
- AC4 → T4, T6
- AC5 → T2, T6
- AC6 → T5, T6
- AC7 → T1, T7

## Tasks

- [ ] T1: Write `_extensions/wrapped/_extension.yml` with title, author, version 0.1.0, `quarto-required: ">=1.9.36"`, and the filter at `pre-quarto`. Load `wrapped.css` with `quarto.doc.add_html_dependency`.
- [ ] T2: Parsing in `wrapped.lua`. Handle `FloatRefTarget` at the filter's top level. Carry a cell div's class in a `traverse = "topdown"` pass that scopes the carry to that cell (LESSONS, M001). Move a class from an inner image to its float (E1). Read `width` and `wrap-gap`, then the `wrapped:` metadata, then the defaults 40% and 1em. Remove the wrap class and the percent inline width from the inner image.
- [ ] T3: HTML layout in `wrapped.css` and the filter. Set width and gap as CSS custom properties on the float. Float the uncaptioned image. Emit the breakpoint media query from the `breakpoint` value, since a custom property cannot set a media query. Make the float work on a page whose margin content turns the body into a CSS grid.
- [ ] T4: The stop rule. After a wrapped figure, find the first block that is not a paragraph, and make it clear the float. Make an empty `.wrap-clear` div clear it.
- [ ] T5: The format fallback. For any format that is not HTML, remove the wrap classes, keep the normal figure, and print one warning per render that names the format.
- [ ] T6: Write `tests/fixture.qmd`, `tests/defaults.qmd`, `tests/margin.qmd`, and `tests/stop-rule.qmd`. Write `tests/verify.py` (Python standard library only). It renders each fixture and compares the wrapped-figure fragments of the HTML with committed snapshots. It exits with a non-zero status on a difference. Show it red on a planted change. Replace the `verify` slot in `cairn/PROFILE.md` with its command.
- [ ] T7: Write `README.md` with the install command, the syntax for each form, the attributes, the metadata keys, the stop rule, and the formats that keep a normal figure. Run the `quarto add` check in a scratch folder. Check the Jupyter cell form once by hand in a throwaway venv in the session scratchpad, and record the result in the work log.

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

## Decisions

## Review
