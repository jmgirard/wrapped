# wrapped

wrapped is a Quarto filter extension. It lets body text flow beside a
figure, to the left or right of it. The figure keeps its number, its
caption, and its `@fig-` links.

This version wraps figures in HTML output. In every other format, a wrapped
figure renders as a normal figure, and the render prints one warning.
Support for PDF through LaTeX, PDF through Typst, and Word is planned.
Dashboards are not tested yet.

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
default width is 40%.

The `wrap-gap` attribute sets the space between the figure and the text.
The default gap is `1em`.

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

## Notes

- A captioned image with no `#fig-` id wraps too. It has no figure number.
- An image inside a link, or beside other content in its paragraph, does
  not wrap. In HTML the render prints a warning for it.
- In HTML, a `width` or `wrap-gap` value that is not a length or a percent
  prints a warning, and the document default applies.
- The sides are physical. In a right-to-left document, `.wrap-right` still
  puts the figure on the right.
- A long caption wraps inside the figure box.
- A page with margin content, such as `.column-margin`, still wraps.
