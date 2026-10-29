# Design

_Seeded by `/cairn-init` on 2026-10-24 from SCOPE.md, the design scope written
before cairn. Nothing here is elicited yet. Refine it with `/design-interview`._

## Purpose & Scope

wrapped is a Quarto filter extension that lets body text flow around a figure.
One markdown syntax gives a wrapped figure in HTML, PDF through LaTeX, PDF
through Typst, and Word. It answers quarto-cli feature request #376. No
extension in the community index did this (observed 2026-10-24). Users will
install it with `quarto add jmgirard/wrapped`.

**Goals.**

- Wrap text to the left or right of one captioned figure. The figure keeps
  its number, caption, and `@fig-` links.
- Wrap text around an uncaptioned image.
- Use one width value for all formats.
- In a format or context that cannot wrap, keep a normal figure and warn
  once: once for each render in a format, once for each figure in a
  context, and once for a code cell that makes more than one figure, in a
  context or not (corrected M003, M014, M018).

**Non-goals for version 1.**

- Tables (`#tbl-` floats). LaTeX `wraptable` conflicts with `longtable`, and
  Quarto renders most tables as `longtable`.
- Subfigure panels (`layout-ncol`, `layout`).
- Code listings and callouts.
- A figure in the middle of a paragraph. The figure anchors where it appears
  in the source, which is between blocks.

**Distribution.** Public. Each version gets a `v<version>` tag and a GitHub
release with notes from commit subjects. The version lives in
`_extensions/wrapped/_extension.yml` and rises at release. The
documentation site's source is `docs/`, rendered with `quarto render docs`.
`.github/workflows/docs.yml` checks its layout and publishes it from `main` to the `gh-pages`
branch, which GitHub Pages serves at https://jmgirard.github.io/wrapped/.
`README.md` is a short page that points to the site (corrected M024).

**Quarto version.** `quarto-required: ">=1.9.36"`. Quarto 1.9.36 is the first
stable release whose source has the loader for an extension's
`typst/packages` folder (`references/wrap-mechanisms.md`, open questions).
The spikes ran only on Quarto 1.10.19, so behavior on 1.9.36 to 1.10.18 is
not tested.

### Syntax

HTML output, PDF through LaTeX, PDF through Typst, and Word implement this
syntax (corrected M006).

Captioned figure, image form:

```markdown
![Mean ratings by condition.](ratings.png){#fig-ratings .wrap-right width="40%"}

The paragraph after the figure wraps around it.
```

Captioned figure, div form:

```markdown
::: {#fig-ratings .wrap-left width="35%"}
![](ratings.png)

Mean ratings by condition.
:::
```

Uncaptioned image: `![](logo.png){.wrap-right width="20%" fig-alt="Lab logo"}`.

Figure from a code cell: `#| classes: wrap-right` beside `#| fig-cap:`. The
class lands on the cell's enclosing div, not on the figure node, and the
filter carries it to the figure (`references/wrap-mechanisms.md`, S1; D-001).

| Attribute | Values | Default | Notes |
|---|---|---|---|
| `.wrap-left`, `.wrap-right` | class | none | Turns wrapping on and picks the side. |
| `width` | percent of text width (in Typst with `columns:` set, of column width), or an absolute length | `40%` | Width of the figure box, caption included. |
| `wrap-gap` | length | `1em` | Space between the figure and the text. A gap below zero takes the default with a warning (corrected M012). |
| `wrap-lines` | integer | auto | LaTeX only. The most narrowed lines; a stop block ends the wrap earlier (changed M007, D-007). After a smaller value than the height needs, the stop block starts below the figure in body text (changed M025, D-015). |

Document or project defaults go under one metadata key:

```yaml
wrapped:
  width: 35%
  gap: 0.75em
  breakpoint: 576px   # HTML: at this width or narrower, figures stop floating
```

Stop rule: the figure wraps the paragraphs that follow it. Wrapping stops at
the first block that is not a paragraph: a heading, list, figure, table, code
block, callout, or horizontal rule. A paragraph that holds one shortcode
and nothing else that shows also stops it, such as `{{< pagebreak >}}` or
`{{< video >}}`, because at `pre-quarto` the shortcode is not yet rendered
and can make a block (corrected by the page-break hotfix, M020, D-011).
Spaces, soft breaks, HTML comments, and one span around the shortcode show
nothing (corrected M021, D-012). Eight shortcodes that usually make text,
an image, or paragraphs join instead, also with a comment beside them:
`meta`, `var`, `env`, `kbd`, `lipsum`, `placeholder`, `version`, and
`brand`. A `meta` shortcode that is its paragraph's one inline stops when
its value holds a block other than `Para` or `Plain`; a value of paragraphs
only joins, and in any other form Quarto renders the value as text, so it
joins (M021, D-012). Quarto expands `{{< include >}}` and `{{< embed >}}`
before the filter runs, so their blocks follow the rule as written. An empty `::: {.wrap-clear}` div stops
it earlier. HTML, LaTeX, Typst, and Word enforce the rule. In LaTeX a
`\wrappedstop` after the group skips the lines the figure's height still
needs, and puts out a figure that moved and still waits, centered with no
text beside it (corrected M007). After a `wrap-lines` value smaller than
the height needs, whose narrowed lines have ended, it skips to below the
figure on the figure's page, outside boxes (corrected M025).

Next-block rule (D-003): a wrapped figure whose next block is not a
paragraph has no text to wrap, so it keeps a normal figure with no warning.
A paragraph that stops wrapping under the stop rule, such as a lone
`{{< video >}}` with or without comments or a span around it, or a lone
`meta` whose value holds a block other than a paragraph, does not count as
a paragraph here (M020, D-011; corrected M021). Of two wrapped figures in
a row, the first keeps a normal figure and the second wraps. The figures of one code cell are the exception: a wrapped
cell that makes more than one figure without `fig-subcap` keeps all of them
normal, with one warning for the cell (D-010, M014). That warning names
the cell's context as its reason, and a cell in no context with no
paragraph after it prints none (corrected M018).

## Function Families

One filter, `_extensions/wrapped/wrapped.lua`, with the syntax above, its
Word part `wrapped-docx.lua`, its stylesheet `wrapped.css`, its LaTeX
wrapper `wrapped.tex`, and a bundled copy of the Typst package wrap-it 0.1.1
under `typst/packages/` (D-004, corrected M006). Users reach it through
`filters: - wrapped`.

## Conventions

- Numeric-results rule: off. The repo produces no statistical or scoring
  results. Its only arithmetic converts widths, for example 40% to Word twips,
  and ordinary fixture tests cover it. Decided at init on 2026-10-24.
- The version in `_extension.yml` rises at release, not at each merge
  (CLAUDE.md, `PROFILE.md` release-walk).
- Tests render fixture documents and compare the output. See `PROFILE.md`
  test-doctrine. GitHub Actions runs the same test command on each pull
  request to `main` (`.github/workflows/verify.yml`, D-008, D-009).
- The documentation site in `docs/` is a Quarto website that uses the
  extension through a `docs/_extensions` symlink. `.github/workflows/docs.yml`
  runs, with no R, on any pull request and any push to `main` that changes
  `docs/`, `_extensions/`, `tests/docs_layout.py`, `tests/layout.js`, or the
  workflow, and by hand. Its render job runs `quarto render docs` and then
  the layout checks of `tests/docs_layout.py` in LaTeX, Typst, and HTML
  (D-016). On `main` of `jmgirard/wrapped` the publish job then renders and
  publishes the site to `gh-pages`, only after the render job passes
  (corrected M024, M027). Code cells take their results from the committed
  `docs/_freeze/`, so an edit to a page with a code cell is rendered
  locally with R and its `_freeze/` changes are committed with it (M023).

## Design Principles

Not yet elicited. `/design-interview` fills this section.

### Inviolable (IP)

None yet.

### Guiding (GP)

None yet.

## Architecture

The extension is `_extensions/wrapped/`. `_extension.yml` holds the one
version marker, runs `wrapped.lua` at `pre-quarto`, and runs
`wrapped-docx.lua` at `post-render` (corrected M006). The filter makes eight
passes, two in step 1 (corrected M003, and by the page-break hotfix):

1. It reads the `wrapped:` metadata and checks each length. In LaTeX it
   reads `classoption`, and a two-column document keeps normal figures.
   Columns that a class, `\twocolumn`, or `multicols` sets are found only
   while LaTeX runs, by the check in `wrapped.tex` at each figure (step 7)
   (corrected M009). In a second pass, a `Shortcode` handler records the
   name of each shortcode by its custom id, so that the stop rule can tell
   a paragraph with a lone joining shortcode from one with any other
   shortcode (corrected by the page-break hotfix, M020). It also records
   each `meta` shortcode's key, which the stop rule looks up in the
   metadata that the first pass keeps (corrected M021).
2. It finds the contexts that cannot wrap: lists (definition lists
   included), callouts, column layouts, panel layouts, tabsets, asides,
   margin blocks (a `fig-column: margin` cell included), subfigure
   panels, and in a dashboard code cells outside a `.card` div (corrected
   M022). revealjs slides have no margin column, so there the margin
   classes and a document margin value name no context, and an aside still
   does (`margin_context`) (corrected M017). Some contexts depend on the
   format: a block quote in LaTeX, a
   table in LaTeX and Word, and a page-wide column class in HTML, and in
   LaTeX and Typst for the classes Quarto sets page-wide there
   (`page_context`; in Typst a float's own class counts only for the
   column-page and column-screen names without -inset) (corrected M015). In
   LaTeX and Typst, a code cell's own column class names no context when
   the document sets `fig-column` or `column`, because the document's value
   decides there (corrected M016). In a dashboard, a code cell outside a
   `.card` div is a context ("is outside a card in a dashboard"), because
   Quarto's post-render dashboard filter makes such a cell a card of its
   own; the walk tracks the `.card` divs around each
   block, and a `.card` div that is itself a context, such as one with
   `layout-ncol`, stays that context (corrected M022). It
   records each float there by its custom id, and it removes the wrap class
   from a captioned image with no id or an image there, with a warning. In
   HTML, step 4 also keeps a float whose caption goes to the margin in its
   normal layout (`caption_in_margin`), by a caption location or by the
   `margin-caption` or `caption-margin` class (corrected M013, M015). It
   reads the caption locations in Quarto's order: the figure's own
   `cap-location` decides when set, and otherwise any one of the figure's
   `fig-cap-location` and the two document keys set to `margin` sends the
   caption there (corrected by the cap-location hotfix).
3. It applies the next-block rule: it records each float with no paragraph
   after it, and removes the wrap class from such a captioned image with no
   id or image.
4. In a top-down pass, it carries a code cell's wrap class to that cell's
   floats and moves an image's class to its float. A float that step 2 or
   3 recorded, a table, a float with a margin or page-wide class or a
   layout attribute, any figure float when the document's `fig-column` or
   `column` decides its column (`column_context`, below) and names the
   margin, or a page-wide column in a format where step
   2's page-wide rule holds for it (`meta_column_context`, which reads a
   code cell's float as a cell and any other float as a float's own class),
   or a figure of a code cell with more than one float outside other
   floats keeps its normal layout (corrected M014, M015). In LaTeX and
   Typst, `column_context` reads a float's column in Quarto's order: its own
   `fig-column-*` class, the document's `fig-column`, its own `column-*` or
   `aside` class, then the document's `column`; the first one set decides.
   A code cell's own column sits on the cell, which step 2 reads only when
   the document sets neither key. A layout attribute comes before a
   document value, so a panel warns as a subfigure panel. HTML reads a
   margin or page-wide class on the float or its cell, and Word a margin
   class, then the document's value, so a body class does not override the
   document there (corrected M016). On revealjs slides a margin class or a
   document margin value keeps no float normal, by step 2's rule
   (corrected M017). In HTML,
   each other float gets its
   box width and gap as CSS custom properties, and a captioned image with
   no id gets a `.wrapped-image` box. In LaTeX, each other float and
   captioned image gets `fig-env="wrappedfigure"` and a `fig-pos` that
   holds its side, width, gap, and line count as LaTeX values (corrected
   M004), and each float is recorded for the grouping pass as in HTML
   (corrected M007). In Typst, each other float records the opening of its
   `wrap-content` call by its custom id, and a captioned image with no id
   gets a `.wrapped-image` box that holds that opening (corrected M005).
5. In HTML it groups each wrapped figure with the paragraphs after it in a
   `.wrap-group` div. The group's `display: flow-root` gives the stop rule.
   A dashboard marks the group and a cell's `.cell` and
   `.cell-output-display` wrappers as flex fill items and containers;
   `wrapped.css` sets those cell wrappers to `display: block`, so the float
   reaches the paragraphs, and the group to `flex: 0 0 auto`, so a card
   that fills its height does not shrink it (corrected M022). These rules
   and the group's `flow-root` have the same specificity as the fill
   rules, so they win only because `wrapped.css` loads after Bootstrap.
   In LaTeX it finds the same groups by the stop rule but writes no div: it
   puts an image with no caption in a raw `wrappedfigure`, and a raw
   `\wrappedstop` follows each group's last paragraph (corrected M007). In Typst it writes each group as raw Typst blocks around the figure and the
   paragraphs, which make one `layout(wrapped-size => wrap-content(...,
   box(width: 100%)[figure], [paragraphs]))` call. The width sets wrap-it's
   grid column. A percent of 100% or more, or a percent width and gap with
   a sum of 100% or more, takes the default width with a warning. Any
   other width that with the gap is as wide as the text or wider takes the
   default in Typst, with no warning, through `wrapped-width` (corrected
   M010, corrected M011). With `columns:` set, the text is the figure's
   column (M019). A code cell keeps its code above the call (corrected M005). In Word it groups as in HTML,
   and the `.wrap-group` div's `data-wrap-frame` holds the frame's side,
   width, and gap in twips. A percent is a share of the text width in the
   reference doc's `w:sectPr`, or 6.5 in when it has no page size or
   margins. Each image takes the frame width (corrected M006). A frame
   whose width plus gap is as wide as the text or wider takes the first of
   the document default and 40% that with the gap is narrower, else 40%,
   with a warning: in `docx_frame` for a figure that sets its own width or
   gap, and in `read_meta` for the `wrapped` metadata (corrected M012).
   A function gap that is below zero or not finite at every size takes the
   default gap with a warning that says so. The check is in
   `checked_length`, so it runs in every format, but only HTML takes a
   function gap; elsewhere such a gap warns in any case (corrected M012).
6. It warns for a wrap class on an image or a div that it cannot place.
7. In HTML it adds the stylesheet and the breakpoint rule when a figure
   wraps. In LaTeX it adds wrapfig and `wrapped.tex`, which defines
   `wrappedfigure` over wrapfig's floating placements and `\wrappedstop`,
   which ends a wrap (corrected M007). Where the text runs in columns,
   inside `multicols` or where `\if@twocolumn` is true, `wrappedfigure`
   sets a normal figure and writes a warning to the LaTeX log: a `figure`
   float, or the figure in place inside `multicols`, or in two-column text
   inside a box or with no caption. It sets the
   gap as `\columnsep` only inside wrapfig's placement of the figure
   (corrected M009). In Typst it imports
   `wrap-content` from `@preview/wrap-it:0.1.1`, which Quarto loads from the
   extension's `typst/packages` folder, and defines the helpers that turn a
   physical side into wrap-it's side in right-to-left text, read in context
   (corrected M005), and `wrapped-width`, which picks the first width that
   with the gap fits the text width that `layout` gives, the column width
   with `columns:` set (corrected M010, corrected M011, corrected M019). Word needs nothing here. Elsewhere it prints
   one format warning.

At `post-render`, `wrapped-docx.lua` turns each Word group into a frame. It
removes Quarto's one-cell figure table, or turns a Pandoc `Figure` into its
image and caption paragraphs, and puts the same `w:framePr` in a raw
`w:pPr` on the image paragraph and each caption paragraph. Word reads the
frame after Pandoc's and Quarto's own `w:pPr`. Each framed image takes
its `fig-alt` text, or the `alt` that Quarto copies from a float's
`fig-alt`, as its description, which Pandoc writes as its alt text
(corrected M029). Quarto puts a float's `alt` on each of its images, so
only the frame's first image takes it; a later image keeps its own
`fig-alt` or its description. The text goes in as one `Str`, which keeps
its repeated spaces (corrected M030). A clearing break,
`<w:br w:type="textWrapping" w:clear="all"/>`, ends the group's last
paragraph (corrected M006).

The grouping pass finds a wrapped float by Quarto's internal
`__quarto_custom_id` attribute. `tests/verify.py` shows a change there as a
snapshot difference. The mechanism for each other format is in
`references/wrap-mechanisms.md`.

## Known issues

- PDF through Typst: a wrapped figure whose group does not fit at the bottom
  of a page moves to the next page with the text beside it, and the rest of
  the page stays blank. With `columns:` set, the same holds at the bottom of
  a column: the group moves to the next column. wrap-it puts the group in a
  `box`, which does not break across pages or columns. The site's
  `docs/formats/typst.qmd`, Limits, states this limit (M005, columns M019,
  corrected M024).
- Word: a frame that does not fit at the bottom of a page moves to the next
  page with the paragraph after it, and the rest of the page stays blank. A
  Word frame does not break across pages. The site's
  `docs/formats/word.qmd`, Images and frames, states this limit (M006,
  corrected M024).
- PDF through Typst: a wrapped figure whose width plus its gap is as wide
  as the text or wider, or with `columns:` set as its column or wider
  (M019), takes the default width with no console warning,
  unless the width and the gap are both percents, because Typst has no
  function that prints one. When 40% plus the gap is that wide too, the
  figure keeps 40% and the gap. The site's `docs/formats/typst.qmd`,
  Widths that leave no room, states these limits (M010, corrected M011,
  corrected M024).
- HTML: newer CSS forms that browsers accept, such as `round()`, `pi`, and
  typed arithmetic, warn and take the default, because the filter checks
  the CSS Values 3 rules and `min()`, `max()`, and `clamp()`. The site's
  `docs/width-gap.qmd`, CSS functions in HTML, lists what the check
  accepts (M010, corrected M024).
- HTML: a function width that is never above zero but that the check
  cannot show to be so prints no warning, such as
  `calc(min(1%, 1px) - min(1%, 1px))` or `calc(7mm - 0.7cm)`. The check
  keeps one term's limit for `min()` and `max()`, reads each relative unit
  as unrelated to the others, and adds in floating point. The site's
  `docs/width-gap.qmd`, Widths that are never above zero, says the check
  warns only where it can show the result (M011, corrected M024).
- HTML: a `max()` or `clamp()` gap over two units whose terms are all
  below zero, such as `max(-2px, -1%)` or `clamp(-3px, -2%, -1px)`, prints
  no warning. The check reads such a value as zero or below, not as below
  zero, and a gap of zero stays. The site's `docs/width-gap.qmd`, Gaps
  below zero, states this limit (M012, corrected M024).
- Word: with only a `wrapped:` gap set, 40% plus that gap can be as wide
  as the text, and a figure that sets neither its own width nor its own
  gap then has no room for text, with no warning. The site's
  `docs/defaults.qmd`, Rules for the keys, states this limit (M012,
  corrected M024).
- PDF through LaTeX: a captioned figure in a table cell fails the build
  ("Not in outer par mode") with or without the extension, because Quarto
  puts a figure float in a `longtable`. The extension keeps a wrapped one
  in its normal layout with a warning, so the failure is Quarto's. The
  site's `docs/normal-layout.qmd`, Places that keep the normal layout in
  some formats, states this limit (M013, corrected M024).
