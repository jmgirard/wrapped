# Wrap mechanisms by output format (cairn-init)

**Provenance.** Ingested 2026-10-24 by cairn-init from SCOPE.md, the design
scope written before cairn. SCOPE.md came from a read-only read of quarto-cli
`main` at 5b23163 (2026-10-23). It also used the typst/packages,
ntjess/wrap-it, and Vanille-N/meander.typ repositories on GitHub.
Pagination: none.
Extraction: a 2026-10-24 snapshot, and quarto-cli, wrap-it, and meander move on independently. Spikes S1 to S4 tested the claims that "Open questions" names, in M001 (verified 2026-10-24). The other claims are not tested.

**Scope.** This page records how each output format can wrap text around a
figure, and which Quarto hook each path uses. It also records the edge cases,
the test plan, and the open questions that the spikes answer. It is not a
source summary. It is a reference, not an authority. Status lives in
`ROADMAP.md`, decisions in `DECISIONS.md`, and architecture in `DESIGN.md`.

**Evidence snapshot.**

- Quarto release 1.10.19 and pre-release 1.11.6, from `gh release list -R quarto-dev/quarto-cli` (observed 2026-10-24).
- Figure renderers in `src/resources/filters/customnodes/floatreftarget.lua` at 5b23163 (observed 2026-10-24).
- LaTeX environment and position in `src/resources/filters/layout/latex.lua` (`latexFigureEnv`, `latexFigurePosition`) at 5b23163 (observed 2026-10-24).
- Typst figure output in `src/resources/filters/layout/typst.lua` (`make_typst_figure`) at 5b23163 (observed 2026-10-24).
- docx captions and frames in `src/resources/filters/layout/docx.lua` (`docxDivCaption`, `docxRowBreak`) at 5b23163 (observed 2026-10-24).
- Typst packages in extensions: `src/command/render/output-typst.ts` reads each extension's `typst/packages` folder at 5b23163 (observed 2026-10-24).
- wrap-it 0.1.1: last commit 2025-02, 77 stars, 16 open issues, from the GitHub API (observed 2026-10-24).
- meander 0.4.4: last commit 2026-08, 154 stars, from the GitHub API (observed 2026-10-24).
- Feature request quarto-cli#376, text wrapping around figures: 18 reactions, open (observed 2026-10-24).

## How each format wraps

| # | Format | Mechanism | Quarto hook | Main risk |
|---|---|---|---|---|
| W1 | HTML (html, revealjs, dashboard) | CSS `float` on `div.quarto-float`. Width and gap are CSS custom properties. A `.wrap-clear` div marks the stop point. No float below a breakpoint. | Quarto copies the float's classes to the outer `div.quarto-float`. | `quarto-figure-center` sets `text-align`. The lightbox extension wraps the image in a link. |
| W2 | PDF through LaTeX | A `wrappedfigure` environment calls `wrapfigure` from `wrapfig`. Where the text runs in columns (`\if@twocolumn`, or inside `multicols`), it does not wrap (corrected M009). It sets a figure float, or it sets the figure in place inside `multicols`, inside a box, or with no caption. The filter sets `fig-env="wrappedfigure"` and `fig-pos="side=right,width=0.4\linewidth,gap=1em"`. If `wrap-lines` is set, `fig-pos` also holds `lines=<n>`. The shipped wrapper is `_extensions/wrapped/wrapped.tex` (corrected M004). | Quarto writes `\begin{<fig-env>}[<fig-pos>]` and passes `fig-pos` unchanged. | Inside another environment, `wrapfigure` can lose its paragraph shape. |
| W3 | PDF through Typst | `wrap-content(fixed, body, align: ...)` from wrap-it, bundled under `_extensions/wrapped/typst/packages/preview/wrap-it/0.1.1/`. | Quarto renders `#figure(...)<id>`. The `pre-quarto` grouping pass puts raw Typst blocks around it and the next paragraphs, as S3 did. The blocks make one `wrap-content` call inside `layout` (corrected M010). The `post-render` step changes nothing in Typst (corrected M006). | wrap-it issue #15: a citation in the wrapped text fails. S3 did not show it with wrap-it 0.1.1 on Typst 0.15.1 (corrected M001). |
| W4 | Word (docx) | Word frames. The image paragraph and the caption paragraph get the same `w:framePr`, and Word merges them into one frame. | Quarto renders a one-cell table. Its cell `Div` has the figure ID. A `post-render` step unwraps it. | A second raw `w:pPr` on the image paragraph. S4 showed that Word accepts a frame in an extra first `w:pPr`. In M006, Word 16 read it after Pandoc's and Quarto's own `w:pPr`, the order a filter makes. The caption kept its `ImageCaption` style (corrected M006). |
| W5 | gfm, commonmark, pptx, epub, ipynb, JATS, ODT | The filter removes the wrap class and keeps a normal figure. It warns once per document. | None. | None. |

Details by row:

- W2: `wrapfigure` cannot take `fig-env` directly. Its first optional
  argument is a line count, and two required arguments follow it. The wrapper
  defines key-value options (`side`, `width`, `lines`) with
  `\NewDocumentEnvironment` and `l3keys`. If the wrapper fails, a
  `post-render` step replaces the raw `\begin{figure}` and `\end{figure}`
  blocks instead.
- W2 limits: `wrapfig` fails inside lists. If a page break falls in the
  wrapped area, the first lines on the next page stay narrowed with no
  figure beside them (corrected M004). On its own it narrows a heading that
  comes before the figure's bottom edge, and two wrapped figures in a row
  break it. The extension's `\wrappedstop` ends the wrap at the stop block
  (corrected M007). It does not work in `twocolumn` documents.
- W3: typst#553 is closed. It moved to float placement, not text wrap. The
  Typst label stays inside a content block (`[...]`), so `@fig-` links work.
  Lists break in wrap-it issues #12, #19, and #3. First-line indents change
  in #1. In #8, a figure taller than the rest of the page breaks the margin.
  meander handles page breaks, but it lays out whole pages. The wrap-it
  license is Unlicense and the meander license is MIT, so the extension can
  bundle either one.
- W4: Pandoc writes every image as `wp:inline`. Raw OpenXML cannot embed an
  image, because Pandoc assigns the relationship IDs. Quarto already puts a
  raw `<w:pPr>` at the start of caption paragraphs. It also uses `w:framePr`
  in `docxRowBreak`. The stop point is
  `<w:br w:type="textWrapping" w:clear="all"/>`. The width converts to twips
  from the page width, which is 6.5 in by default.
- W4 schema order: `w:framePr` comes after `w:pStyle` and before `w:spacing`
  and `w:jc`. Quarto's own `w:pPr` is not in schema order, and Word accepts
  it.

## Code sketches

These sketches come from SCOPE.md. S2 ran the LaTeX sketch, and it did not compile as written. The working form is `spikes/s2/wrapped.tex`. No spike ran the other sketches as written (corrected M001). The working HTML stylesheet is `_extensions/wrapped/wrapped.css`, and the filter writes the breakpoint rule (corrected 2026-10-25, M002 review).

HTML stylesheet (W1):

```css
.quarto-float.wrap-right { float: right; width: var(--wrap-width); margin: 0 0 1em var(--wrap-gap); }
.quarto-float.wrap-left  { float: left;  width: var(--wrap-width); margin: 0 var(--wrap-gap) 1em 0; }
.quarto-float.wrap-right img, .quarto-float.wrap-left img { width: 100%; height: auto; }
.wrap-clear { clear: both; }
@media (max-width: 576px) { .quarto-float.wrap-right, .quarto-float.wrap-left { float: none; width: auto; margin: 1em 0; } }
```

LaTeX wrapper (W2). The filter adds `wrapfig` with
`quarto.doc.use_latex_package("wrapfig")`:

```latex
\ExplSyntaxOn
\keys_define:nn { wrapped }
  { side .tl_set:N = \l_wrapped_side_tl, side .initial:n = r,
    width .tl_set:N = \l_wrapped_width_tl, width .initial:n = 0.4\linewidth,
    lines .tl_set:N = \l_wrapped_lines_tl, lines .initial:n = }
\NewDocumentEnvironment{wrappedfigure}{O{}}
  { \keys_set:nn { wrapped } {#1}
    \tl_if_empty:NTF \l_wrapped_lines_tl
      { \exp_args:NVV \wrapfigure \l_wrapped_side_tl \l_wrapped_width_tl }
      { ... }  % with [lines]
  }
  { \endwrapfigure }
\ExplSyntaxOff
```

Typst output (W3), as the filter writes it from the `pre-quarto` pass (corrected M005, corrected M010, corrected M011). The `wrapped-side` and `wrapped-columns` helpers keep the side physical in right-to-left text. `layout` gives the text width. `wrapped-width` takes the gap, then the figure width, the document default, and 40%. It returns the first width that fits the text with the gap. When none fits, it returns 40%:

```typst
#layout(wrapped-size => wrap-content(align: top + wrapped-side(right), columns: wrapped-columns(right, wrapped-width(wrapped-size, 1em, 40%, 40%, 40%)), column-gutter: 1em, box(width: 100%)[
#figure(...)<fig-id>
], [
Paragraph one.

Paragraph two.
]))
```

Word frame (W4), on the image paragraph and the caption paragraph (corrected M012). `w:hSpace` holds the gap. The frame sits at the margin. The text beside it has the text width less the frame width and the gap. If a figure sets its own width or gap, and the frame width plus the gap fills the text width, the filter warns. The frame then takes the document default or 40%, the first that leaves room, else 40%:

```xml
<w:framePr w:w="<twips>" w:wrap="around" w:hSpace="<twips>" w:vAnchor="text" w:hAnchor="margin" w:xAlign="right"/>
```

## Planned layout

```
_extensions/wrapped/
  _extension.yml        # contributes: filters (pre-quarto and post-render entries)
  wrapped.lua           # shared parsing: classes, width, stop rule, warnings
  wrapped-docx.lua      # post-render: Word frames
  wrapped.css           # HTML layout
  wrapped.tex           # LaTeX wrapper environment
  typst/packages/preview/wrap-it/0.1.1/
```

The filter has two entry points (corrected M006):

- `pre-quarto` runs after Quarto creates `FloatRefTarget` nodes. It
  normalizes the attributes and sets `fig-env` and `fig-pos` for LaTeX. It
  also applies the stop rule, inserts clear points, writes a raw
  `\wrappedstop` after each LaTeX group (corrected M007), and writes the
  Typst `wrap-content` call. In Word it marks each group with its frame in
  `data-wrap-frame`.
- `post-render` runs `wrapped-docx.lua`, which builds the docx frames after
  Quarto renders figures. It changes nothing in other formats.

## Edge cases

| # | Case | Behavior |
|---|---|---|
| E1 | Wrap class on the image, not the float | The filter moves it to the float. |
| E2 | `fig-align` set | Ignored for the box position. It still aligns the image inside the box. |
| E3 | `.column-margin` or `.aside` with a wrap class, or a `fig-column: margin` cell or document | Margin wins. One warning (corrected M013). A document-level value is E21's (M015). In LaTeX and Typst, a document `fig-column` comes before a figure's own `column-*` or `.aside` class (E21, M016). Slides have no margin column. There a margin class or a document margin value names no place, and the figure wraps. An `.aside` div still keeps it normal, because revealjs sets the aside at the slide's foot (E15, M017). |
| E4 | Subfigure panel (`layout-ncol`) | Normal panel. One warning. A wrapped code cell that makes more than one figure without `fig-subcap` keeps each figure normal, with one warning for the cell (corrected M014, D-010). |
| E5 | `#tbl-` float with a wrap class | Normal table. One warning. |
| E6 | Wrapped figure is the last block before a heading | No text to wrap. Normal figure, no warning. |
| E7 | Two wrapped figures with no text between them | The first figure falls back with no warning, and the second wraps the text after it (corrected 2026-10-24, D-003). The figures of one code cell follow E4 instead (corrected M014, D-010). |
| E8 | Wrapped figure inside a list (a definition list included), callout, column layout, or tabset | Normal figure. One warning (corrected M013). |
| E9 | Text shorter than the figure | HTML and Word clear at the stop point. Typst wraps the text it has. LaTeX skips the lines that the figure's height still needs at the stop point (corrected M007). |
| E10 | Figure taller than the rest of the page | LaTeX, Typst, and Word move it to the next page. In LaTeX the text before it leaves no gap. A figure whose paragraphs all end before it is placed renders with no text beside it, before the stop block (corrected M007). In Typst the `wrap-content` box moves whole and the rest of the page stays blank (corrected M005). Word moves the frame and the paragraph after it, and the rest of the page stays blank (corrected M006). |
| E11 | Long caption | The caption wraps inside the box width in all formats. |
| E12 | `pdf-standard: ua-1` or `ua-2` | A test makes sure that alt text and tags stay. Quarto 1.10.19 ignores `ua-1` for LaTeX, so that PDF has no tags. The LaTeX test uses `ua-2` with `documentclass: article` (corrected M004). |
| E13 | Book projects and cross-chapter `@fig-` links | No change expected. The test book includes one. |
| E14 | Right-to-left documents (`dir: rtl`) | `left` and `right` stay physical in version 1. |
| E15 | revealjs | The HTML path works. If a test slide looks right, the README shows it. Quarto 1.10.19's revealjs stylesheet has no `column-margin` rule. So a figure with a margin class, setting, or document value stays in the slide's text, where it wraps. An `.aside` div sits at the slide's foot (`position: absolute; bottom: 20px`), so a figure there is normal with one warning (M017). |
| E16 | Dark mode and `_brand.yml` | The extension sets no colors, so nothing changes. |
| E17 | `classoption: twocolumn` in LaTeX | Normal figure. One warning. |
| E18 | Wrapped figure in a block quote | Normal figure with one warning in LaTeX, where wrapfig does not wrap. Wraps in HTML, Typst, and Word (M013). |
| E19 | Wrapped figure in a table cell | Normal figure with one warning in Word and LaTeX. A captioned figure in a LaTeX table cell fails to build with or without the extension. Wraps in HTML and Typst (M013). |
| E20 | Caption in the margin (`cap-location`, `fig-cap-location`, or the `.margin-caption` or `.caption-margin` class) | Normal figure with one warning on an HTML page, where no text sits beside it. Wraps in LaTeX, Typst, Word, and slides (M013). A captioned image with no id moves its caption only for `.margin-caption` (M015). |
| E21 | Page-wide column class, or a document-level `fig-column` or `column` | Normal figure with one warning on an HTML page for all 16 classes, and in LaTeX for those Quarto makes page-wide. Wraps in Word and slides (M013). In Typst, Quarto 1.10.19 sets a div or a code cell wider than the text for all 16. It sets a figure with its own class wider only for `column-page` and `column-screen`, with or without `-left` or `-right`. The figure is normal in those cases (corrected M015). In HTML and Word, a document-level value applies to every figure float, even a cell with `fig-column: body`. In LaTeX and Typst, the order below decides (corrected M016). A margin value keeps the figure normal in every format where it decides, as a margin class does. On revealjs slides neither decides, and the figure wraps (E3, M017). A captioned image with no id is no float and wraps (M015). Where a figure's own class and a document key name different places, LaTeX and Typst follow Quarto's order: own `fig-column-*`, document `fig-column`, own `column-*` or `.aside`, document `column`. A layout attribute comes before a document value, so a panel warns as a subfigure panel. A code cell's figure takes the document's value over the cell's own option. HTML reads an own margin or page-wide class first. Word reads an own margin class first. A body class does not override the document key in either (M016). |

## Test plan

- One fixture document renders to all four formats. It has right and left
  wraps, an uncaptioned image, and a code-cell figure. It also has a
  `@citation` in the wrapped text, a figure near a page break, and a
  cross-reference to each figure.
- Committed snapshots record what the filter decides in each format's
  intermediate output: the HTML, the kept `.tex` and `.typ`, and the
  unzipped `word/document.xml`. They catch a Quarto change that alters
  those decisions, not every change to Quarto's figure renderers
  (`tests/verify.py`, corrected 2026-10-25, M002 review).
- Before each release, a person opens the docx in Word, LibreOffice, and
  Google Docs.
- CI runs the test command against the Quarto release channel on each pull
  request and push to `main`, and against the pre-release channel weekly
  (corrected M008, D-008).

## Disposition

- W1 and W2 go to the ROADMAP candidate "Wrap figures in HTML and LaTeX output".
- W3 goes to the ROADMAP candidate "Wrap figures in Typst PDF output".
- W4 goes to the ROADMAP candidate "Wrap figures in Word output with frames".
- W5 for EPUB goes to the ROADMAP candidate "Use the HTML stylesheet for EPUB". The other W5 formats stay out.
- E1 to E17 go to the acceptance criteria of the milestone for each format.
- The spikes below go to the ROADMAP candidate "Run the four wrap feasibility spikes".

## Open questions

Each spike answers one yes-or-no question. The fallback for a no follows it.

- S1: Does a `pre-quarto` filter see the wrap class on `FloatRefTarget`? This includes figures from knitr and Jupyter cells with `#| classes: wrap-right`. If no, the filter reads a `#| wrap: right` cell option instead. Answered 2026-10-24 with Quarto 1.10.19, from `spikes/s1/probe.lua` run on `spikes/s1/s1-knitr.qmd` and `spikes/s1/s1-jupyter.qmd`:
  - Markdown image with `.wrap-right`: yes. The class is in `FloatRefTarget.classes`. The `width` attribute stays in the inner `Image.attributes`, and the `Image` keeps the class too.
  - Div figure with `.wrap-left`: yes. The class is in `FloatRefTarget.classes`, and `width` is in `FloatRefTarget.attributes`.
  - knitr cell with `#| classes: wrap-right`: no. The float has no classes. The class is on the enclosing `Div` with class `cell`. That div holds the code block and a `cell-output-display` div, and the float is inside the second div.
  - Jupyter cell with `#| classes: wrap-right` (jupyter 5.9.1 core, in a throwaway venv): no. Same as knitr. The class is on the enclosing `Div` `#cell-fig-jupyter` with class `cell`.
  - Uncaptioned image: the class is in `Image.classes`, and no float exists.
  - For both cell engines, a second filter pass used `traverse = "topdown"`. It saw the cell `Div` before the nested `FloatRefTarget` and added the class to `FloatRefTarget.classes`. The HTML output then shows `wrap-right` on `div.quarto-float` for the knitr and the Jupyter figure. The LaTeX path for a moved class is not tested. The `#| wrap: right` fallback is not needed for HTML.
  - The spike's carry is a global that only a float clears. A cell with a wrap class and no figure hands its class to the next float. The real filter must scope the carry to its own cell.
- S2: Does the `wrappedfigure` wrapper around `wrapfigure` work? If no, a `post-render` step rewrites the raw blocks. Answered yes on 2026-10-24 with Quarto 1.10.19 and TinyTeX 2026 (LuaLaTeX), from `spikes/s2/s2.qmd` and its header file `spikes/s2/wrapped.tex`:
  - Quarto writes `\begin{wrappedfigure}[side=r,width=0.4\linewidth]` with the `fig-pos` string unchanged, backslash included.
  - The PDF built with no LaTeX error. On page 1, the right figure and its two-line caption sit beside the two paragraphs that follow it, and the third paragraph runs full width. The left figure with `lines=12` sits beside the paragraph that follows it.
  - The code sketch above does not compile as written. The working wrapper calls `\wrapfigure` through two small helper functions. If `lines` is set, it builds the call with `\use:e`. See `spikes/s2/wrapped.tex`.
  - Known limit seen: the left figure's 12 narrowed lines ran past the page break, so page 2 starts with narrowed text and no figure.
  - The review found a second problem on page 1. The Figure 2 caption runs into the footer band and overlaps the page number's height.
- S3: Does wrap-it render wrapped text that contains a citation? If no, test meander. If neither works, Typst keeps a normal figure when the wrapped text contains a citation. Answered 2026-10-24 with Quarto 1.10.19 (Typst 0.15.1) and wrap-it 0.1.1, from `spikes/s3/s3-wrapit.qmd`:
  - Quarto's default Typst citations: yes. Quarto writes `#cite(<smith2020>, form: "prose")` and `@smith2020[p.~3]` inside the `wrap-content` call. The PDF built with no error and shows both citations and the `@fig-right` link in the text beside the figure.
  - `citeproc: true`: yes. Pandoc writes the citations as plain text, and the PDF shows them in the text beside the figure.
  - meander 0.4.4 was not tested, because both wrap-it answers are yes.
  - Raw Typst blocks around the figure and the paragraphs open and close the `wrap-content` call. Quarto renders the figure and the citations itself. The planned `post-render` step that builds this call is not tested.
  - Typst refused the image path `../assets/plot.png`, outside the document's folder. Its error: "would escape the project root". The spike keeps its own copy of the image.
- S4: Does Word open a docx with a raw frame `w:pPr` on the image paragraph, and show one merged frame? How do LibreOffice and Google Docs show it? If Word fails, version 1 ships without docx wrapping. Answered yes for Word on 2026-10-24, from the user's look at a docx that `spikes/s4/frame.py` builds from `spikes/s4/s4.qmd` (Quarto 1.10.19):
  - The script removes Quarto's one-cell figure table and puts the same `w:framePr` on the image paragraph and the caption paragraph. It edits the finished docx, so the planned `post-render` filter step is not tested. The frame width comes from the image's `wp:extent`, so the conversion from a percent width to twips is not tested.
  - Word opened the file with no repair prompt.
  - Right figure, one merged `w:pPr` in schema order: Word shows the image and caption in one frame on the right, with body text beside it.
  - Left figure, the frame in an extra `w:pPr` before Quarto's own `w:pPr` elements: Word shows the same result on the left. So Word accepts a frame in an extra first `w:pPr`.
  - A filter puts raw OpenXML after Pandoc's own `w:pPr`, so its frame `w:pPr` comes second or third. That order is not tested, and neither is whether the caption keeps its `ImageCaption` style. LibreOffice and Google Docs were not checked. The candidate "Wrap figures in Word output with frames" holds these checks.
- Which Quarto version first loads Typst packages from an extension's `typst/packages` folder? The answer sets `quarto-required`. Answered 2026-10-24 from a quarto-cli clone:
  - The loader is `collectPackageSources` in `src/command/render/output-typst.ts`, which adds `join(ext.path, "typst/packages")` for each extension.
  - Tag v1.9.18 is the earliest tag whose `output-typst.ts` has `typst/packages`. It is a pre-release. The last tag of each minor release from v1.4 to v1.8 does not have it. No Typst-named file under `src` at v1.8.27 names the folder.
  - The earliest stable release with the loader is v1.9.36 (2026-03-19), the first 1.9 release that GitHub does not mark as a pre-release.
  - No changelog line names this feature. The nearest is quarto-cli#13486 in `news/changelog-1.9.md`, which bundles Typst template packages with `typst-gather`.
- How will Quarto 2 (quarto-dev/q2, a Rust rewrite in active development) treat Lua filter extensions? The Typst and docx paths depend on the shape of Quarto's rendered output, so they break first. Not yet known (observed 2026-10-24).
