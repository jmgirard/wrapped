# wrapped

wrapped is a Quarto filter extension. It lets body text flow beside a
figure, to the left or right of it. The figure keeps its number, its
caption, and its `@fig-` links.

This version wraps figures in HTML output, revealjs slides included, in
PDF through LaTeX, in PDF through Typst, and in Word. In every other
format, a wrapped figure renders as a normal figure, and the render prints
one warning. Dashboards are not tested yet.

## Install

The extension asks for Quarto 1.9.36 or later, and it is tested with Quarto
1.10.19. In the folder of your project, run:

```bash
quarto add jmgirard/wrapped
```

This command puts the extension under `_extensions/`. Then add the filter
to the document's YAML header:

```yaml
filters:
  - wrapped
```

## Wrap a figure

Add the class `.wrap-right` or `.wrap-left` to a figure. The class names
the side that the figure goes to. The paragraphs after the figure flow
beside it.

A captioned figure from a markdown image:

```markdown
![Mean ratings by condition.](ratings.png){#fig-ratings .wrap-right width="40%"}
```

A captioned figure from a div:

```markdown
::: {#fig-groups .wrap-left width="35%"}
![](groups.png)

Ratings by group.
:::
```

An image with no caption:

```markdown
![](logo.png){.wrap-right width="20%" fig-alt="Lab logo"}
```

A figure from a code cell. Give the cell a `fig-` label and a `fig-cap`,
so that Quarto makes a figure. Put the class in `#| classes:`, and set the
width with `#| out-width:`:

````markdown
```{r}
#| label: fig-scatter
#| fig-cap: "A scatter plot."
#| classes: wrap-right
#| out-width: "30%"
plot(1:10)
```
````

## Width and gap

The `width` attribute sets the width of the figure box, caption included.
The image fills the box. A percent is a share of the text column. An
absolute length, such as `3in` or `250px`, sets the width directly. The
default width is 40%. A width of zero written as a number, such as `0%`,
`0in`, or `0`, prints a warning, and the document default applies.

The `wrap-gap` attribute sets the space between the figure and the text.
The default gap is `1em`. A gap of zero stays as it is. In Word, a gap of
0% prints a warning. A width plus its gap as wide as the text or wider
also prints a warning in Word (see Word below).

In HTML, a width or gap can also be a `calc()`, `min()`, `max()`, or
`clamp()` value, such as `calc(100% - 2em)` or `min(40%, 300px)`. The
extension checks the value first. A value that fails the check prints a
warning, and the document default applies. The check accepts numbers,
lengths in CSS units, percents, parentheses, `var(--name)`, and the four
functions inside one another, with these rules:

- A `+` or `-` between two values has a space on each side.
- The values of a sum are all lengths and percents, or all numbers.
- A `*` has a number on one side, and a `/` has a number on its right.
- `min()` and `max()` take one or more values, and `clamp()` takes three.
- The result is a length or a percent, not a number.

Some CSS that browsers accept also prints a warning:

- other functions, such as `round()` and `env()`
- constants, such as `pi`
- `none` in `clamp()`
- a length divided by a length
- a number with an exponent, such as `1e2px`
- an empty `var()` fallback, such as `var(--a,)`

The check also looks for a function width that is zero, negative, or not
finite at every page and font size. A width that it can show is such a
width prints a warning, and the document default applies.
Examples are `calc(0%)`, `min(0px, 10%)`, `calc(-10px)`, and
`calc(1px / 0)`. The check reads each unit other than an absolute unit as
above zero and as not related to the other units. So a width such as
`calc(50% - 4in)` or `calc(1em - 1rem)`, which can be above zero, prints no
warning. A width with `var()` never prints this warning. A gap or a
breakpoint of zero stays as it is.

The check also looks for a function gap that is negative or not finite at
every page and font size. A negative gap pulls the text over the figure.
A gap that the check can show is such a gap prints a warning, and the
document default applies. Examples are `calc(-1em)`, `min(-1px, 10%)`, and
`calc(1px / 0)`. A gap that is zero at every size, such as
`calc(1em - 1em)`, stays as it is. A gap that can be zero or above, such
as `calc(1em - 20px)`, prints no warning. The check cannot show that a
`max()` or `clamp()` over two units is below zero. So such a gap, as
`max(-2px, -1%)` or `clamp(-3px, -2%, -1px)`, also prints no warning. LaTeX,
Typst, and Word take no function gap, so such a gap prints a warning
there in any case. For a gap that the check shows is below zero, that
warning says so.

```markdown
![Mean ratings by condition.](ratings.png){#fig-ratings .wrap-left width="3in" wrap-gap="2em"}
```

A `fig-align` attribute does not move the box. The class sets the side.

## Document defaults

The `wrapped` key in the YAML header sets the defaults for a document. A
figure's own `width` or `wrap-gap` attribute comes first.

```yaml
wrapped:
  width: 25%
  gap: 30px
  breakpoint: 800px
```

In a window as wide as `breakpoint` or narrower, figures stop floating and
take the full width of the text column. The default breakpoint is `576px`.

The keys follow the rules of the attributes. A `width` of zero prints a
warning, and the built-in 40% applies. A `gap` or `breakpoint` of zero stays
as it is. A function `gap` that is negative or not finite at every size
prints a warning, and the built-in `1em` applies. In Word, a `gap` of 0%
prints a warning, and the built-in `1em` applies. In Word, a `width` that
with the `gap` is as wide as the text or wider prints a warning, and the
built-in 40% applies. With only a `gap` set, the width is already 40%, and
40% plus that gap can leave no room with no warning. A `width`, `gap`, or
`breakpoint` can be a `calc()`, `min()`, `max()`, or `clamp()` value,
checked as above. A media query takes no percent and no `var()`. So a `breakpoint` with a percent or a `var()`, such
as `calc(50%)`, prints a warning, and `576px` applies.

Quarto reads the YAML values as Markdown. In a function value, put a space
on each side of `*` and `/`, as in `calc(2 * 1em)`. Without the spaces,
Markdown can read the stars as emphasis and drop them.

## Where wrapping stops

The figure wraps the paragraphs that follow it. Wrapping stops at the first
block that is not a paragraph, and that block starts below the figure.
Examples are a heading, a list, a table, a code block, a callout, another
figure, and a horizontal rule. An image with no caption and no wrap class
counts as a paragraph.

To stop wrapping earlier, put an empty `wrap-clear` div after the last
paragraph that you want beside the figure:

```markdown
::: {.wrap-clear}
:::
```

A wrapped figure with no paragraph right after it keeps its normal layout.
An example is a figure right before a heading. In HTML, LaTeX, Typst, and
Word the render prints no warning for such a figure. The places in the
lists of the next section are the exception: a figure there prints its
warning with or without a paragraph after it. Of two wrapped figures in a
row, the first keeps its normal layout, and the second wraps the paragraphs
after it. This does not hold for the figures of one code cell, which the
next section covers.

In PDF through LaTeX, in PDF through Typst, and in Word, wrapping stops as
in HTML, and a `wrap-clear` div works.

## Where a figure keeps its normal layout

In HTML, PDF through LaTeX, PDF through Typst, and Word, a wrapped figure
in one of the places in this first list does not wrap. It keeps
its normal layout, and the render prints one warning for it. The warning
names the figure's id. If the figure has no id, the warning names its image
file or says that the figure has no id.

- The margin: a figure with the `.column-margin` class, a figure in a
  `.column-margin` or `.aside` div, or a code cell with `#| column: margin`
  or `#| fig-column: margin`. The figure stays in the margin. In PDF
  through LaTeX, Quarto puts a captioned image that has the
  `.column-margin` class and no `#fig-` id in the body instead. Word has
  no margin column, so there the figure is in the body. This item also
  covers `fig-column: margin` and `column: margin` in the document
  metadata. That value applies to every figure with a `#fig-` id and every
  code cell figure, even a cell with `#| fig-column: body`. The paragraph
  after this list gives the order. It does not apply to a
  captioned image with no id, which stays in the body.
- A subfigure panel, such as a figure div with `layout-ncol`, or a
  subfigure inside a panel.
- A panel layout: a div or a code cell with `layout-ncol`, `layout-nrow`,
  or `layout`.
- A list, a definition list included, a callout, a `.columns` layout, or a
  tabset.

A figure's own class and the document's `fig-column` or `column` can name
different places. In PDF through LaTeX and PDF through Typst, the
extension reads them in Quarto's order, and the first one set decides:

1. the figure's own `fig-column-*` class, such as `.fig-column-margin`,
2. the document's `fig-column`,
3. the figure's own `column-*` class, such as `.column-margin`,
4. the document's `column`.

For a code cell's figure, the document's `fig-column`, else its `column`,
decides over the cell's own `column` or `fig-column` option. If the
document sets `fig-column: body`, a `.column-margin` figure wraps in PDF,
because Quarto puts it in the body there. In HTML and
Word, the extension reads a margin or page-wide class on the figure or its
code cell before the document's key. A body class, such as `.column-body`,
does not override the document's key there.

A code cell that makes more than one figure without `fig-subcap` or a
layout option does not wrap either. An example is a cell that draws two
plots. Each of its figures keeps its normal layout, and the render prints one
warning that names the cell's label. If no paragraph follows the cell, its
figures keep their normal layout with no warning, as any wrapped figure
does there. To wrap a plot, give it its own cell with a paragraph after
it. A cell with `fig-subcap`
makes a subfigure panel, and a cell with `layout-ncol`, `layout-nrow`, or
`layout` makes a panel layout. The list above covers both.

A table float does not wrap either, and the render prints one warning that
names it. A `#tbl-` div or a code cell with a `tbl-` label makes a table
float.

These places keep the normal layout only in the formats named. The render
prints the same warning there, and the figure wraps in the other formats.

- A block quote: in PDF through LaTeX.
- A table cell: in Word and in PDF through LaTeX. In PDF through LaTeX, a
  captioned figure in a table cell fails to render, with or without the
  extension, so only an image with no caption renders there.
- A caption in the margin: in HTML. The extension follows where Quarto
  puts the caption. When the figure or its code cell sets `cap-location`,
  that value decides, and on a code cell `fig-cap-location` acts as
  `cap-location`. Without a `cap-location`, a `margin` value in any of
  three keys sends the caption to the margin: the figure's
  `fig-cap-location`, the document's `fig-cap-location`, and the
  document's `cap-location`. A value other than `margin` in one of these
  three does not override `margin` in another. For a captioned image with
  no id, Quarto reads only the document's `fig-cap-location`, else its
  `cap-location`. The `.margin-caption` and `.caption-margin` classes also
  send the caption to the margin. They work on the figure, on its image,
  and on its code cell, as in `#| classes: wrap-right .caption-margin`. For
  a captioned image with no id, only `.margin-caption` does this.
- A page-wide column: a page-wide class on the figure or on a div around
  it, or a code cell with `#| column: page` or `#| fig-column: page`. The
  classes are `.column-body-outset`, `.column-page-inset`, `.column-page`,
  `.column-screen-inset`, and `.column-screen`, each alone or with `-left`
  or `-right`, and `.column-screen-inset-shaded`. In HTML this covers all
  of them. In PDF through Typst it covers all of them on a div or a code
  cell. For a class on the figure itself, it covers only `.column-page`
  and `.column-screen`, each alone or with `-left` or `-right`. Quarto
  keeps the figure in the body for the others. In PDF through LaTeX
  it covers the classes that Quarto makes page-wide there: those that
  start with `.column-page` or `.column-screen` and do not end in `-left`.
  Word keeps the figure in the body, where it wraps. This item also covers
  a page-wide value of `fig-column` or `column` in the document metadata,
  such as `fig-column: page`. That value applies to every figure with a
  `#fig-` id and every code cell figure, even a cell with
  `#| fig-column: body`. The paragraph after the first list gives the
  order. In PDF through Typst it applies as a class on the
  figure itself does, except on a code cell figure. It does not apply to a
  captioned image with no id, which stays in the body.

## Slides

In revealjs slides, a wrapped figure floats beside the paragraphs after it
on the same slide, as on an HTML page:

```markdown
## Results

![Mean ratings by condition.](ratings.png){#fig-ratings .wrap-right width="40%"}

Ratings rose in both conditions.
```

Slides have no margin captions and no page-wide columns, so a figure with
a margin caption or a page-wide class still wraps on a slide.

## PDF through LaTeX

In PDF through LaTeX, the extension puts each wrapped figure in a
`wrapfigure` from the LaTeX package wrapfig. Where the text runs in
columns, it does not (see below). If your TeX distribution does
not have wrapfig, install it, for example with `tlmgr install wrapfig`.

The `width` and `wrap-gap` values change to LaTeX lengths:

- A percent is that share of the line width, so `40%` is `0.4\linewidth`.
  In one column, the line width is the text width.
- A `px` length is 0.75 `pt` for each `px`, so `200px` is `150pt`.
- A length in `pt`, `pc`, `in`, `cm`, `mm`, `em`, or `ex` stays as it is.
- Any other CSS unit, such as `vw` or `rem`, and a `calc()`, `min()`,
  `max()`, or `clamp()` value print a warning, and the document default
  applies.
- A width of zero prints a warning, and the document default applies.

The `wrap-lines` attribute sets the number of lines beside the figure. It
works only in LaTeX. Without it, wrapfig counts the lines from the height
of the figure. A block that stops the wrap ends it before that number of
lines. With a value larger than the figure needs, that block starts below
the figure, as it does without `wrap-lines`.

```markdown
![Mean ratings by condition.](ratings.png){#fig-ratings .wrap-right wrap-lines="12"}
```

A caption inside a wrapped figure is set ragged-right. An image with a
`height` keeps it in LaTeX and keeps its shape, and it fits in the box
width.

wrapfig has limits, and the extension keeps some of them:

- wrapfig narrows a number of lines that it counts from the height of the
  figure. At the block that stops the wrap, the extension skips the lines
  that the figure still needs. If the text beside the figure is shorter
  than the figure, the space beside the figure stays empty.
- A figure that does not fit at the bottom of a page moves to the start of
  a paragraph on the next page. The text before it fills the page. If its
  paragraphs all end before it is placed, it renders with no text beside
  it. It renders before the block that stops the wrap, and that block
  starts below it.
- If a page break comes while lines are still narrowed, the first lines on
  the next page are narrowed with no figure beside them. A `wrap-lines`
  value larger than the figure needs can narrow lines past a page break in
  the same way.
- Figures in a row: a figure after the paragraphs of a wrapped figure is a
  block that stops its wrap, so it starts below the wrapped figure. A
  figure that moved to the next page waits for one of its own paragraphs.
  A heading or the end of a callout does not take it.
- Where the text runs in columns, set by `classoption: twocolumn`, a class
  default, `\twocolumn`, or `multicols`, wrapped figures render as normal
  figures: they do not wrap. A percent width is a share of the column, or
  of the box that holds the figure. With `classoption: twocolumn`, the
  filter writes Quarto's normal figure, and the render prints one warning.
- In other documents, a class that sets two columns by default, such as
  IEEEtran, a
  `\twocolumn` command, and a `multicols` environment are found only while
  LaTeX runs. In two-column text, a captioned figure floats as a normal
  figure does. An image with no caption, or a figure inside a box such as
  a `minipage`, stays in place. Inside
  `multicols`, where LaTeX loses floats, each figure stays in place. After
  `\onecolumn`, figures wrap again.
- In those cases the render prints no warning. LaTeX writes the warning to
  its log, and Quarto keeps the log with `latex-clean: false`. A column
  layout from a LaTeX class or package that neither turns on LaTeX's
  two-column mode nor opens a `multicols` environment is not detected.
- A figure in a list keeps its normal layout, as in HTML.

Tagged PDF: Quarto 1.10.19 ignores `pdf-standard: ua-1` in LaTeX, so that
PDF has no tags, with or without the extension. With `pdf-standard: ua-2`,
Quarto's default document class fails, so set a class such as
`documentclass: article`. In such a PDF, each wrapped figure and wrapped
image keeps its `fig-alt` text as its alt text.

## PDF through Typst

In PDF through Typst, the extension puts each wrapped figure and the
paragraphs after it in a `wrap-content` call from the Typst package wrap-it
0.1.1. The extension ships its own copy of wrap-it, so the render does not
download it. Citations and `@fig-` links in the text beside the figure
work.

The `width` and `wrap-gap` values change to Typst lengths:

- A percent is that share of the text width.
- A `px` length, or a number with no unit, is 0.75 `pt` for each `px`, so
  `200px` is `150pt`. A `pc` length is 12 `pt` for each `pc`.
- A length in `pt`, `mm`, `cm`, `in`, or `em` stays as it is, with its unit
  in lowercase.
- Any other unit, such as `ex`, `vw`, or `rem`, and a `calc()`, `min()`,
  `max()`, or `clamp()` value print a warning, and the document default
  applies.
- A width of zero prints a warning, and the document default applies.

A percent of 100% or more leaves no room for the text in Typst, so it
prints a warning. A percent width and a percent gap with a sum of 100% or
more also print a warning, for example `width="75%"` with
`wrap-gap="25%"`. A figure's own width then takes the document default.
If the document default is a percent that with the gap also fills the
text, the figure's width takes the built-in 40%. A
`wrapped: width` of 100% or more, or a `wrapped:` width and gap in
percents with such a sum, takes the built-in 40%.

A width plus its gap in other units can also fill the text. Examples are
`5in` with a `1.5in` gap, and `99%` with a `1em` gap. Such a width also
leaves no room for the text. The extension cannot know the text width, so
Typst checks the width plus the gap while it lays out the page. The
figure then takes the document default. If the document default plus the
gap is that wide too, the figure takes the built-in 40%. Typst cannot
print a warning, so the render prints none for such a width. If 40% plus
the gap is that wide too, the figure keeps 40% and the gap.

The `wrap-lines` attribute does nothing in Typst. Typst does not use an
image's `height` in a wrapped figure. The image fills the box width and
keeps its shape, and the render prints a warning.

The sides stay physical in right-to-left text. Typst sets that direction
from the document's `lang`, such as `lang: he`, or from a raw Typst
`#set text(dir: rtl)`. Quarto does not pass `dir: rtl` to Typst.

wrap-it has limits:

- wrap-it puts the figure and the text beside it in one box, and the box
  does not break across pages. If the box does not fit at the bottom of a
  page, it moves to the next page. The rest of the page before it stays
  blank.
- When the text is longer than the figure, wrap-it breaks a paragraph at
  the word where the figure ends. The rest of that paragraph starts on a
  new line below the figure and runs the full width.
- wrap-it issue #1 reports that first-line indents change in wrapped text.
  The extension does not test this case.

Tagged PDF: with `pdf-standard: ua-1`, each wrapped figure and wrapped
image keeps its `fig-alt` text as its alt text.

## Word

In Word output, the extension puts each wrapped figure in a Word frame. The
image and its caption sit in the frame on the figure's side, and the
paragraphs after the figure flow beside it. Citations and `@fig-` links in
the text beside the figure work. An uncaptioned image keeps its `fig-alt`
text as its alt text.

The `width` and `wrap-gap` values change to Word lengths:

- A percent above 0% and below 100% is that share of the text width. The
  extension reads the text width from the page size and margins of the
  reference doc that the document names with `reference-doc`. With no
  reference doc, or a reference doc with no page size or margins, the text
  width is 6.5 in: Word then shows a Letter page with 1 in margins.
- A length in `in`, `cm`, `mm`, `pt`, or `pc`, in any letter case, keeps
  its size. A `px` length, or a number with no unit, is 1/96 in for each
  `px`. An `em` is 12 pt.
- Any other unit, such as `ex`, `vw`, or `rem`, a `calc()`, `min()`,
  `max()`, or `clamp()` value, a width of zero, and a gap of 0% print a
  warning, and the document default applies. A figure can set its own gap
  with which the document default leaves no room, as in the next items.
  Then the width takes 40% instead.
- A width or gap as wide as the text or wider, such as `100%` or `10in`,
  leaves no room for the text. It prints a warning, and the document
  default applies. In the cases that the next item names, a width takes
  40% instead.
- A width plus its gap as wide as the text or wider also leaves no room
  for the text. Examples are `5in` with a `2in` gap on a 6.5 in text width,
  and `95%` with a `2em` gap. Such a figure prints a warning, and it takes
  the document default width. If the document default plus the gap is
  that wide too, the figure takes the built-in 40%. If 40% plus the gap is
  that wide too, the figure takes 40% and keeps the gap. This is so even
  when its own width was narrower than 40%. The extension rounds
  each value to twips (1/20 pt) before it adds them.
- A `wrapped:` width that with the gap is as wide as the text or wider
  prints one warning, and the document default width becomes 40%. A
  `wrapped:` width that already printed its own warning prints no second
  one. A figure that sets neither its own width nor its own gap prints no
  warning of its own.

The text width is the page width less the left and right margins and the
gutter. A reference doc with more than one column keeps normal figures,
and the render prints one warning.

The image takes the width of the frame and keeps its shape. The extension
does not use an image's `height` in a wrapped figure in Word, and the
render prints a warning. The `wrap-lines` attribute does nothing in Word.

A list in a figure div goes in the frame with the image and the caption.
Word cannot put a code block, a table, a heading, a horizontal rule, or
raw content in a frame. A figure div that holds one keeps its normal
layout, and the render prints a warning.

A frame does not break across pages. If a frame does not fit at the bottom
of a page, Word moves it and the paragraph after it to the next page. The
rest of the page before it stays blank.

The extension is tested in these apps, with a test document that holds 15
wrapped figures:

- Microsoft Word 16.114 on macOS: text sits beside every wrapped figure.
- LibreOffice 26.8 on macOS: text sits beside every wrapped figure.
- Google Docs: no text sits beside the figure. The figure and its caption
  sit on the figure's side on lines of their own, and the text starts
  below them. Nothing is lost. This was checked on the first figure of the
  test document.

Right-to-left Word documents are not tested.

## Notes

- A captioned image with no `#fig-` id wraps too, unless a place in the
  section "Where a figure keeps its normal layout" applies to it, such as
  a caption in the margin. In HTML and Word it has
  no figure number. In PDF through LaTeX and Typst, Quarto numbers it.
- An image inside a link, or beside other content in its paragraph, does
  not wrap. In HTML, LaTeX, Typst, and Word the render prints a warning for
  it.
- In HTML, LaTeX, Typst, and Word, a `width` or `wrap-gap` value that is
  not a length or a percent prints a warning, and the document default
  applies.
- In HTML, LaTeX, and Typst the sides are physical. In a right-to-left
  document, `.wrap-right` still puts the figure on the right. Right-to-left
  Word documents are not tested.
- A long caption wraps inside the figure box.
- If a page has margin content, such as a `.column-margin` note, a figure
  in the body of the page still wraps.
