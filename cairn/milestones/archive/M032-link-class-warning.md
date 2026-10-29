# M032: Warn for a wrap class on a link

**Status:** done (2026-10-29, PR #34 https://github.com/jmgirard/wrapped/pull/34)

**Goal:** In HTML, PDF through LaTeX, PDF through Typst, and Word, a link that carries a wrap class prints a warning, since a wrap class on a link wraps nothing.

**Outcome:** In `wrapped.lua`, a new `unplaced_link` in the filter's last pass (beside `unplaced_image` and `unplaced_div`) sets `found_wrap` for a link with `.wrap-left` or `.wrap-right` and, where `wraps()` holds, warns "the link to <url> is not a figure, so it does not wrap. A wrap class goes on an image or a figure." The link keeps its class; an image inside it wraps only by its own class. In Word with columns or LaTeX with `classoption: twocolumn`, the one columns warning prints instead. Tests: three `tests/fixture.qmd` cases (image link, link around an image with its own class, text link), each with its own target and image copy (`tests/link-class*.png`), in all four snapshots, and a link case in `tests/twocolumn.qmd` and `tests/docx-columns.qmd`. `docs/normal-layout.qmd` and DESIGN.md step 6 state the rule.

**Decisions:** none milestone-local. The plan gate kept the class on the link rather than stripping it as `unplaced_div` does; falsified by a stylesheet that selects a wrap class on an `a`.

**Review:** Plan criteria audit (full) returned 6 findings, 4 fixed. Claim audit read 15 claims and corrected 2 (columns warning, link alone in its paragraph). Four-lens pass, 14 findings: 4 fix-now (a test of the columns claim, proved by a planted ungated warning; the `found_wrap` comment), 9 rejected (5 planned change, 2 false, 2 edge: an empty link target, and a link-only wrap class printing a format or reference-doc warning), 1 noted. Evidence: `tests/verify.py` all 104 renders pass at a89e8bf; `quarto render docs` exit 0; `tests/docs_layout.py` 24 `ok` (`--html` not run); PR CI verify and docs render green. Hygiene graduated "Warn for a wrap class on a link", captured one lesson, marked the M012 and M031 lessons used, and evicted the 2026-10-27 (M015, used M018) Typst wideblock lesson by rank.
