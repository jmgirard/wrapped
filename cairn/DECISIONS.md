# Decisions

Append-only. Never renumber; supersede with a new entry. D-entries record
choices with rationale — never deferrals ("not now" is a ROADMAP fact).

### D-001: Code-cell figures keep `#| classes:`, and the filter reads the cell div

2026-10-24, M001. For a figure from a knitr or Jupyter cell, the planned
syntax `#| classes: wrap-right` stays. The filter carries the class from the
cell's enclosing div to the figure in a top-down pass. It does not switch to a
`#| wrap: right` cell option. DESIGN.md had named that option as the fallback
if `classes` did not reach the figure node. Spike S1 showed that the class
does not reach the node but does reach the enclosing cell div for both
engines. A top-down pass sees that div before the figure, and a class it
adds to the figure reaches the HTML figure div. The existing syntax
therefore works, and a second cell option gives users two ways to say one
thing. The LaTeX path for a moved class is not tested. If it fails there,
the `#| wrap:` option comes back as the fallback for that path. Evidence:
`references/wrap-mechanisms.md`, S1.

### D-002: Dependencies for the HTML and LaTeX core

2026-10-24, plan of M002 to M004. The user allowed these dependencies at the
plan's question set. The extension uses the LaTeX package wrapfig for PDF
through LaTeX. Users' TeX distribution supplies it, and TinyTeX installs it
on first use. wrapfig is the package that spike S2 tested, and LaTeX has no
built-in way to wrap text. The test command in `tests/verify.py` needs R
with knitr and TinyTeX, because the fixture renders a knitr cell and a PDF.
The Jupyter cell form stays out of the test command, because the system
Python has no Jupyter. It gets one check by hand in a throwaway environment,
as spike S1 did. Spike S1 showed the same class placement for both engines.

### D-003: Back-to-back wrapped figures: the first falls back, the second wraps

2026-10-24, plan of M003. This replaces edge case E7 in
`references/wrap-mechanisms.md`, which said that the second figure falls
back with a warning. Under the stop rule, a figure whose next block is not a
paragraph has no text to wrap. The first of two back-to-back figures is such
a figure, so it keeps a normal figure with no warning, as E6 does for a
figure before a heading. The second figure has paragraphs after it, so it
wraps them. The user chose this at the plan's question set over keeping E7
as written and over a fallback for both figures.
