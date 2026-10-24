# M001: Run the four wrap feasibility spikes

**Status:** done (2026-10-24, PR #1 https://github.com/jmgirard/wrapped/pull/1)

**Goal:** Record a yes-or-no answer, with evidence, to each wrap feasibility question S1 to S4 and to the minimum Quarto version question.

**Outcome:** Spike folders `spikes/s1` to `spikes/s4` with a README, and answers in `references/wrap-mechanisms.md` "Open questions". S1: the wrap class is in `FloatRefTarget.classes` for markdown and div figures. For knitr and Jupyter cells it is on the enclosing cell div, and a top-down pass that adds it to the float puts `wrap-right` on the HTML figure div. S2: a `wrappedfigure` wrapper (`spikes/s2/wrapped.tex`) around `wrapfigure` works, after the research-page sketch failed to compile. S3: wrap-it 0.1.1 on Typst 0.15.1 renders citations in wrapped text in both citation modes, so meander was not tested. S4: Word opens a docx whose image and caption paragraphs share one `w:framePr` (`spikes/s4/frame.py`) and shows one frame. DESIGN now states `quarto-required: ">=1.9.36"`, the first stable release with the extension `typst/packages` loader. Not tested: the LaTeX path for a moved cell class, the `post-render` filter paths, the frame `w:pPr` in a filter's order, and Quarto versions other than 1.10.19.

**Decisions:** D-001 (code-cell figures keep `#| classes:`, and the filter reads the cell div).

**Review:** Full four-lens fan-out, 32 findings: 23 fixed on the branch, 2 sent to the candidate "Wrap figures in HTML and LaTeX output", 7 rejected (AC5's release reading, style, planned graduation, false). Hygiene unparked "Wrap figures in Typst PDF output" and "Wrap figures in Word output with frames" on the branch, and graduated "Run the four wrap feasibility spikes".
