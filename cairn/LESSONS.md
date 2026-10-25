# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-24 (M001, used M003): In a user Lua filter, `_quarto` is not defined and a plain `walk` does not see Quarto custom nodes such as `FloatRefTarget`. Handle the custom node at the filter's top level, and use `traverse = "topdown"` to carry state from an outer div to the figure inside it.
- 2026-10-24 (M001, used M002): Typst refuses a file path outside the document's folder ("would escape the project root"), so a Typst fixture keeps its images beside the `.qmd`.
- 2026-10-24 (M001): In a blobless (`--filter=blob:none`) quarto-cli clone, `git log -S` fetches every blob and ran about 40 minutes without finishing. To date a feature, read the file at each release tag with `git show <tag>:<path>` instead.
- 2026-10-25 (M002, used M003): A `FloatRefTarget` placed inside a new `pandoc.Div` vanishes from the output. Other passes see a float as a plain Div with `__quarto_custom_type` and `__quarto_custom_id` attributes, and the float handler reads that id through `float.__quarto_custom_node`, so match on the id instead of moving the float.
- 2026-10-25 (M002): In HTML, Quarto drops the classes, style, and attributes that a filter sets on a Pandoc `Figure` (a captioned image with no `#fig-` id). Put the Figure inside a Div of your own and style the Div.
- 2026-10-25 (M002): A float has no effect inside a CSS grid or flex item list. Quarto turns the page body into a grid when the page has margin content, and gives `.cell-output-display` `overflow-x: auto`. Wrap the float and its text in one `display: flow-root` div, and set that wrapper's overflow to visible.
- 2026-10-25 (M002, used M003): Quarto finds `_extensions/` only from the document's folder up to a project root, so a fixture in `tests/` needs a `tests/_extensions` symlink. On this Mac, knitr's default SVG device for Typst needs X11 libraries, so a Typst fixture sets `fig-format: png`.
- 2026-10-25 (M003): At `pre-quarto`, a plain walk sees callouts, tabsets, and floats as Divs with `__quarto_custom_type`. A float's own classes are not on that Div, but an edit to a plain node inside it lasts. To act on a float by its context, mark it by `__quarto_custom_id` in an earlier `Pandoc` pass, and read the mark in the float handler.
- 2026-10-25 (M003): A `Blocks` filter also runs on the block lists inside a code cell and a float, where a figure is the last block by design. For a rule about the next block, walk top-down and return `false` at cell and float Divs.
- 2026-10-25 (M003): revealjs caps every image at `max-width: 95%` and scales the slide. `getBoundingClientRect` reads scaled screen px, and computed styles read layout px, so a layout check on a slide converts one to the other.
