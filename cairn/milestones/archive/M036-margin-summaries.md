# M036: List margin figures in the test summaries

**Status:** done (2026-10-30, PR #38 https://github.com/jmgirard/wrapped/pull/38)

**Goal:** The LaTeX and Typst summaries in `tests/verify.py` give each margin figure its own line, so no body figure's line takes a margin figure's label.

**Outcome:** `tex_summary` matches `marginfigure` beside `figure` and `wrappedfigure` and writes a `marginfigure:` line with the same label, options, image, and link parts. `typ_summary` splits at line-start `#figure(` and `#notefigure(` calls (a cell's indent allowed), keeps which call opened each chunk, and writes `figure:` or `notefigure:` lines; a body figure's content ends at its `kind:` line and a margin figure's at its `, caption:` line, either indented. New Typst fixture `tests/margin-after-image.qmd`: a captioned image with no id, then `fig-after-image-margin`, then `fig-after-image-margin-width` with `width="50%"`; its snapshot reads `figure: -`, then two `notefigure:` lines, the second with `image-width=yes`. Twelve snapshots gained 43 margin lines and no `figure:` line changed. The module docstring names `#notefigure(` calls. M018's margin-meta cell order stays as it was.

**Decisions:** none milestone-local. Implement choice: a margin figure's `image-width` reads up to its caption, since its `kind:` sits on the call's first line.

**Review:** AC1 to AC3 verified at 6146b0f and re-checked at 70ba6fc: a scratch count script matched the margin lines to the regex counts and labels in all 13 of the 56 pdf and typst renders that hold margin figures (13 of 13 mismatched with main's summaries), and all 106 renders passed. PR #38's `verify (release)` and `verify (1.9.36)` passed. Four-lens pass, 17 findings: 6 fixed in 67d082d and 70ba6fc (indented content boundaries, a positive width case, the docstring), 2 sent to the new parked row "Summarize margin panels and Typst asides" (an aside figure is `figure:` in Typst but `marginfigure:` in LaTeX; margin panels would lose their label), 9 rejected. Hygiene graduated "List margin figures in the summaries", captured one lesson, marked M011, M012, and M032 used, and evicted 2026-10-28 (M021) by rank at the 25-lesson limit.
