# M002: Wrap figures in HTML output

**Status:** done (2026-10-25, PR #2 https://github.com/jmgirard/wrapped/pull/2)

**Goal:** A document rendered to HTML with the extension installed shows body text beside each figure marked `.wrap-left` or `.wrap-right`.

**Outcome:** `_extensions/wrapped/` ships `_extension.yml` (version 0.1.0, the one version marker, `quarto-required: ">=1.9.36"`, filter at `pre-quarto`), `wrapped.lua`, and `wrapped.css`. The filter wraps markdown and div figures, a class on an inner image, knitr and Jupyter cell figures (the carry counts the cell's `__quarto_custom_type=FloatRefTarget` Divs and resets at each cell), captioned images with no `#fig-` id, and images with no caption, the last two in a `.wrapped-image` box. Width and gap come from attributes, then `wrapped:` metadata, then 40% and 1em, set as `--wrap-width` and `--wrap-gap` and checked as CSS lengths. A `.wrap-group` div with `display: flow-root` holds each figure and its paragraphs, which gives the stop rule and works on margin pages whose body is a CSS grid. The breakpoint media query is written into the header. Elsewhere the filter removes only the wrap class and prints one format warning. Unplaced images and non-figure divs warn in HTML. Tests: `tests/verify.py` (11 renders, snapshots of the filter's decisions), `tests/layout.js` browser checks, and fixtures under `tests/` with a `tests/_extensions` symlink. README documents the syntax.

**Decisions:** none milestone-local. The plan recorded D-002 (dependencies) and D-003 (back-to-back figures).

**Review:** Two four-lens passes, 64 findings: 41 fixed, 11 follow-up, 10 rejected, 2 noted. Pass 1 returned the milestone once: the filter stripped `width` from every HTML figure, wrapped or not. Follow-ups: candidate rows "Handle a wrapped cell with two figures" and "Check wrapped figures in dashboards", a `@citation` fixture note on the Typst row, and items held by M003 AC1, AC2, AC3, and AC5. Two claim audits corrected 13 claims. Hygiene narrowed "Wrap figures in HTML and LaTeX output" and moved its started token to M003.
