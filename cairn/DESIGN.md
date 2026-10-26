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
  once: once for each render in a format, and once for each figure in a
  context (corrected M003).

**Non-goals for version 1.**

- Tables (`#tbl-` floats). LaTeX `wraptable` conflicts with `longtable`, and
  Quarto renders most tables as `longtable`.
- Subfigure panels (`layout-ncol`, `layout`).
- Code listings and callouts.
- A figure in the middle of a paragraph. The figure anchors where it appears
  in the source, which is between blocks.

**Distribution.** Public. Each version gets a `v<version>` tag and a GitHub
release with notes from commit subjects. The version lives in
`_extensions/wrapped/_extension.yml` and rises at release.

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
| `width` | percent of text width, or an absolute length | `40%` | Width of the figure box, caption included. |
| `wrap-gap` | length | `1em` | Space between the figure and the text. |
| `wrap-lines` | integer | auto | LaTeX only. The number of narrowed lines; a stop block ends the wrap earlier (corrected M007). |

Document or project defaults go under one metadata key:

```yaml
wrapped:
  width: 35%
  gap: 0.75em
  breakpoint: 576px   # HTML: at this width or narrower, figures stop floating
```

Stop rule: the figure wraps the paragraphs that follow it. Wrapping stops at
the first block that is not a paragraph: a heading, list, figure, table, code
block, callout, or horizontal rule. An empty `::: {.wrap-clear}` div stops it
earlier. HTML, LaTeX, Typst, and Word enforce the rule. In LaTeX a
`\wrappedstop` after the group skips the lines the figure's height still
needs, and puts out a figure that moved and still waits, centered with no
text beside it (corrected M007).

Next-block rule (D-003): a wrapped figure whose next block is not a
paragraph has no text to wrap, so it keeps a normal figure with no warning.
Of two wrapped figures in a row, the first keeps a normal figure and the
second wraps.

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
  test-doctrine.

## Design Principles

Not yet elicited. `/design-interview` fills this section.

### Inviolable (IP)

None yet.

### Guiding (GP)

None yet.

## Architecture

The extension is `_extensions/wrapped/`. `_extension.yml` holds the one
version marker, runs `wrapped.lua` at `pre-quarto`, and runs
`wrapped-docx.lua` at `post-render` (corrected M006). The filter makes seven
passes (corrected M003):

1. It reads the `wrapped:` metadata and checks each length. In LaTeX it
   reads `classoption`, and a two-column document keeps normal figures.
2. It finds the contexts that cannot wrap: lists, callouts, column layouts,
   panel layouts, tabsets, asides, margin blocks, and subfigure panels. It
   records each float there by its custom id, and it removes the wrap class
   from a captioned image with no id or an image there, with a warning.
3. It applies the next-block rule: it records each float with no paragraph
   after it, and removes the wrap class from such a captioned image with no
   id or image.
4. In a top-down pass, it carries a code cell's wrap class to that cell's
   floats and moves an image's class to its float. A float that step 2 or
   3 recorded, a table, or a float with a margin class or a layout
   attribute keeps its normal layout. In HTML, each other float gets its
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
   In LaTeX it finds the same groups by the stop rule but writes no div: it
   puts an image with no caption in a raw `wrappedfigure`, and a raw
   `\wrappedstop` follows each group's last paragraph (corrected M007). In Typst it writes each group as raw Typst blocks around the figure and the
   paragraphs, which make one `wrap-content(..., box(width: 100%)[figure],
   [paragraphs])` call. The width sets wrap-it's grid column. A percent of
   100% or more takes the default width with a warning. A code cell keeps
   its code above the call (corrected M005). In Word it groups as in HTML,
   and the `.wrap-group` div's `data-wrap-frame` holds the frame's side,
   width, and gap in twips. A percent is a share of the text width in the
   reference doc's `w:sectPr`, or 6.5 in when it has no page size or
   margins. Each image takes the frame width (corrected M006).
6. It warns for a wrap class on an image or a div that it cannot place.
7. In HTML it adds the stylesheet and the breakpoint rule when a figure
   wraps. In LaTeX it adds wrapfig and `wrapped.tex`, which defines
   `wrappedfigure` over wrapfig's floating placements and `\wrappedstop`,
   which ends a wrap (corrected M007). In Typst it imports
   `wrap-content` from `@preview/wrap-it:0.1.1`, which Quarto loads from the
   extension's `typst/packages` folder, and defines the helpers that turn a
   physical side into wrap-it's side in right-to-left text, read in context
   (corrected M005). Word needs nothing here. Elsewhere it prints
   one format warning.

At `post-render`, `wrapped-docx.lua` turns each Word group into a frame. It
removes Quarto's one-cell figure table, or turns a Pandoc `Figure` into its
image and caption paragraphs, and puts the same `w:framePr` in a raw
`w:pPr` on the image paragraph and each caption paragraph. Word reads the
frame after Pandoc's and Quarto's own `w:pPr`. A clearing break,
`<w:br w:type="textWrapping" w:clear="all"/>`, ends the group's last
paragraph (corrected M006).

The grouping pass finds a wrapped float by Quarto's internal
`__quarto_custom_id` attribute. `tests/verify.py` shows a change there as a
snapshot difference. The mechanism for each other format is in
`references/wrap-mechanisms.md`.

## Known issues

- PDF through Typst: a wrapped figure whose group does not fit at the bottom
  of a page moves to the next page with the text beside it, and the rest of
  the page stays blank. wrap-it puts the group in a `box`, which does not
  break across pages. The README states this limit (M005).
- Word: a frame that does not fit at the bottom of a page moves to the next
  page with the paragraph after it, and the rest of the page stays blank. A
  Word frame does not break across pages. The README states this limit
  (M006).
