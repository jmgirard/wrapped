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
