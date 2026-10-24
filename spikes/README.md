# Spikes

Small test documents that answer the open questions in
`cairn/references/wrap-mechanisms.md`. They are not part of the extension.
Run each command from the spike's folder. Render output is not committed.

- `s1/`: where a `pre-quarto` filter finds the wrap class.
  Run `quarto render s1-knitr.qmd --to html`. For the Jupyter file, set
  `QUARTO_PYTHON` to a Python that has `jupyter`, then run
  `quarto render s1-jupyter.qmd --to html`. The probe writes `S1` lines to
  the terminal.
- `s2/`: the LaTeX `wrappedfigure` wrapper. Run
  `quarto render s2.qmd --to pdf`, then read the pages with
  `pdftoppm -r 70 -png s2.pdf out/page`.
- `s3/`: wrap-it with citations in the wrapped text. Run
  `quarto render s3-wrapit.qmd --to typst` for Typst citations, and add
  `-M citeproc:true` for Pandoc citations. The first render downloads
  wrap-it 0.1.1 into Typst's package cache.
