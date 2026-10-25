# M003: Fall back in contexts that cannot wrap

**Status:** done (2026-10-25, PR #3 https://github.com/jmgirard/wrapped/pull/3)

**Goal:** Wrapped figures render as the research page's edge cases E3 to E8, E13, and E15 state, with E7 as D-003 states.

**Outcome:** `wrapped.lua` gains two pre-passes before the float pass. `find_contexts` marks floats in a list, callout, column layout, panel layout (a `layout*` attribute on a div or cell), tabset, aside, margin block, or subfigure panel by `__quarto_custom_id`. It also strips the wrap class, with a warning, from a captioned image with no id or an image there, or one with its own `.column-margin`/`.aside` class. `find_no_text` applies the next-block rule (D-003): a figure whose next block, past comments, is not a joining paragraph keeps a normal figure with no warning. It skips lists inside cells and floats. The float pass falls back for marked floats, tables and other non-figure floats ("is not a figure"), a float's own margin class, and a `layout` attribute. Context warnings print in HTML only, one per float. `image_wrap` skips nested floats. A `placed` flag loads `wrapped.css` only when a figure wraps. `wrapped.css` sets `max-width: 100%` on wrapped images for revealjs. Tests: `tests/contexts.qmd`, a `tests/book/` project, and `tests/revealjs.qmd` in `tests/verify.py` (14 renders), with a no-filter margin-container comparison. README documents the contexts and slides.

**Decisions:** none milestone-local. Implement choices are in the work log: ordered lists count as lists, the outermost context names the warning, and figures with no id fall back too.

**Review:** Four-lens pass, 38 findings: 24 fixed, 3 follow-up, 11 rejected. Follow-ups: new rows "Fall back in other margin and list forms" and "Check CSS function lengths before use". Claim audit: 54 claims, 3 corrected. Hygiene narrowed "Wrap figures in HTML and LaTeX output" to W2 (M004) and narrowed "Handle a wrapped cell with two figures".
