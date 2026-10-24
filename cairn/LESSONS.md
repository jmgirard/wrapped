# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-24 (M001): In a user Lua filter, `_quarto` is not defined and a plain `walk` does not see Quarto custom nodes such as `FloatRefTarget`. Handle the custom node at the filter's top level, and use `traverse = "topdown"` to carry state from an outer div to the figure inside it.
- 2026-10-24 (M001): Typst refuses a file path outside the document's folder ("would escape the project root"), so a Typst fixture keeps its images beside the `.qmd`.
- 2026-10-24 (M001): In a blobless (`--filter=blob:none`) quarto-cli clone, `git log -S` fetches every blob and ran about 40 minutes without finishing. To date a feature, read the file at each release tag with `git show <tag>:<path>` instead.
