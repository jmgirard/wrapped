# M037: Say LaTeX narrows lines past figures

**Status:** done (2026-10-30, PR #39 https://github.com/jmgirard/wrapped/pull/39)

**Goal:** The Limits section of `docs/formats/latex.qmd` says that wrapfig can keep lines narrow past the bottom of a wrapped figure, with the number of lines measured in the site's LaTeX example PDFs.

**Outcome:** The first Limits bullet of `docs/formats/latex.qmd` now says the count wrapfig takes from the figure's height can run past the bottom of the figure and its caption, and that in the LaTeX PDFs of the linked example pages a paragraph that runs on past that bottom has one or two narrowed lines there. The stop-block sentences moved to their own bullet, which now says the extension skips the rest of the counted lines. A scratch script on the `tests/docs_layout.py` helpers (`pdftohtml -xml`, `blocks()`, `caption()`) counted narrowed non-final body lines below each figure's bottom, caption included: 1 for both-sides (both figures), code-cell, defaults, div-figure, uncaptioned-image, and width-gap; 2 for image-figure; 0 for wrap-clear, whose paragraph ends beside the figure. Measured from the image's bottom alone the count is 1 to 4, which the claim audit caught in the first wording ("under it").

**Decisions:** none.

**Review:** full four-lens fan-out; both criteria passed on fresh evidence (`quarto render docs` exit 0, `tests/docs_layout.py` 24 ok, `tests/verify.py` 106 renders pass, CI green on both Quarto versions and the docs render). 23 findings: 8 fixed on the branch (the stop-block sentence's ambiguous "lines the figure still needs", "below it", "narrow" against "narrowed", the bullet split, the example-pages link, source reflow); 15 rejected as false, chiefly the example pages', README's, and home page's "last lines run full width under the figure", which hold since those lines follow the narrowed ones. No follow-up rows. Hygiene graduated the candidate row "Say LaTeX narrows lines past figures"; the M007, M025, and M026 lessons marked used.
