# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-24 (M001, used M002): In a user Lua filter, `_quarto` is not defined and a plain `walk` does not see Quarto custom nodes such as `FloatRefTarget`. Handle the custom node at the filter's top level, and use `traverse = "topdown"` to carry state from an outer div to the figure inside it.
- 2026-10-24 (M001, used M002): Typst refuses a file path outside the document's folder ("would escape the project root"), so a Typst fixture keeps its images beside the `.qmd`.
- 2026-10-24 (M001): In a blobless (`--filter=blob:none`) quarto-cli clone, `git log -S` fetches every blob and ran about 40 minutes without finishing. To date a feature, read the file at each release tag with `git show <tag>:<path>` instead.
- 2026-10-25 (M002): A `FloatRefTarget` placed inside a new `pandoc.Div` vanishes from the output. Other passes see a float as a plain Div with `__quarto_custom_type` and `__quarto_custom_id` attributes, and the float handler reads that id through `float.__quarto_custom_node`, so match on the id instead of moving the float.
- 2026-10-25 (M002): In HTML, Quarto drops the classes, style, and attributes that a filter sets on a Pandoc `Figure` (a captioned image with no `#fig-` id). Put the Figure inside a Div of your own and style the Div.
- 2026-10-25 (M002): A float has no effect inside a CSS grid or flex item list. Quarto turns the page body into a grid when the page has margin content, and gives `.cell-output-display` `overflow-x: auto`. Wrap the float and its text in one `display: flow-root` div, and set that wrapper's overflow to visible.
- 2026-10-25 (M002): Quarto finds `_extensions/` only from the document's folder up to a project root, so a fixture in `tests/` needs a `tests/_extensions` symlink. On this Mac, knitr's default SVG device for Typst needs X11 libraries, so a Typst fixture sets `fig-format: png`.
