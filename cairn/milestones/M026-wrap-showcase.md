# M026: Show text wrapping past the figure in examples

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the published site's example pages and the README image
- **Branch/PR:** m026-wrap-showcase

## Goal

The site's example pages and the README image show body text above a wrapped figure, beside it, and continuing below it in one paragraph, a layout that columns or a table cannot give.

## Scope

**In:** New prose in the Result sections of `docs/examples/image-figure.qmd`, `div-figure.qmd`, `uncaptioned-image.qmd`, `code-cell.qmd`, `width-gap.qmd`, `defaults.qmd`, and `both-sides.qmd`, and in the `.demo` div of `docs/index.qmd`: a full-width paragraph before each figure and a long paragraph that starts beside it and runs below it. Re-frozen results for `code-cell.qmd`. A new crop of `docs/images/readme-example.png` and its README sentence and alt text. Line-box readers for these pages in `tests/`.

**Out:** `docs/examples/slides.qmd`, `dashboard.qmd`, and `wrap-clear.qmd` stay as they are, since their point is a small space or an early stop. The guide pages (`get-started.qmd`, `width-gap.qmd`, `defaults.qmd`, `stopping.qmd`, and the others) stay as they are, at the user's choice. No filter code changes.

## Acceptance criteria

- [ ] AC1: For each wrapped figure in the page set P, three things hold on one page. P is `docs/index.qmd` in HTML, and `docs/examples/image-figure.qmd`, `div-figure.qmd`, `uncaptioned-image.qmd`, `code-cell.qmd`, `width-gap.qmd`, `defaults.qmd`, and `both-sides.qmd` in HTML, PDF through LaTeX, PDF through Typst, and the docx as LibreOffice renders it to PDF, 29 renders in all. (a) The last body-text block before the figure (before its code cell in `code-cell.qmd`, and after the `* * *` rule for `#fig-left` in `both-sides.qmd`) is a paragraph of at least two lines, and each of its lines but the last crosses the figure's horizontal span. (b) One paragraph after the figure has a line beside the figure and a later line below the figure's bottom that crosses the figure's horizontal span. (c) A line crosses the span of a `.wrap-right` figure when its right edge is right of the figure's left edge, and of a `.wrap-left` figure when its left edge is left of the figure's right edge. The figure's bottom is the lower of its image box and its last caption line. A line-box read of each of the 29 renders shows it: `pdftohtml -xml` for the three PDFs, and the line rectangles of a DOM Range over each paragraph in a browser at 1280x900 for HTML.
- [ ] AC2: For each page in P, the multiset of its figure image lines, figure-div openers, and code-cell `#|` option lines is byte-identical to `main` at the plan commit, each figure keeps the same enclosing divs, and the page's YAML header is unchanged.
- [ ] AC3: Rerunning the two commands in the final comment of `docs/images/make-images.R` on the branch head reproduces `docs/images/readme-example.png` at its committed pixel size, and the image shows a paragraph above the figure, lines beside it, and lines below it that run under it. The sentence before the image in `README.md` and the image's alt text name those three parts.
- [ ] AC4: With one Quarto version and a clean `docs/.quarto`, `quarto render docs` exits 0 on the branch head, and the sorted `(W) wrapped:` lines it prints equal those of the same render on `main` at the plan commit.
- [ ] AC5: The four files in `docs/_freeze/examples/code-cell/execute-results/` are committed from a local render with R, their `hash` equals the md5 of the branch's `code-cell.qmd`, and `quarto render docs` with no `Rscript` on `PATH` and `QUARTO_R` and `R_HOME` unset exits 0. The docs CI render job passes on the PR.

## Coverage

- AC1 → T1, T2, T3, T4, T5
- AC2 → T2, T3, T4
- AC3 → T6
- AC4 → T1, T5
- AC5 → T4, T7

## Tasks

- [x] T1: On `main`, render `docs/` from a clean `docs/.quarto` and write its sorted `(W) wrapped:` lines to the work log. Add `tests/docs_layout.py`, which reads the `pdftohtml -xml` line boxes of the LaTeX, Typst, and LibreOffice PDFs of the pages in P and checks AC1 (a) to (c) for each figure, and add a function to `tests/layout.js` that returns each paragraph's line rectangles for the same check in HTML. Make sure that both readers fail on `main`.
- [x] T2: Rewrite the Result sections of `image-figure.qmd`, `div-figure.qmd`, and `uncaptioned-image.qmd`: a paragraph of at least two lines before the figure, then a paragraph of about 8 lines that starts beside the figure and continues below it. The prose explains the example, in the site's plain style.
- [x] T3: Do the same for `width-gap.qmd`, `defaults.qmd`, and both figures of `both-sides.qmd`.
- [x] T4: Do the same for `code-cell.qmd` (the paragraph goes before the cell) and the `.demo` div of `docs/index.qmd`. Render `docs/` locally with R so that `docs/_freeze/examples/code-cell/` matches the new page.
- [x] T5: Render `docs/`, convert each docx in P to PDF with LibreOffice, and run both readers over the 29 renders. Lengthen or move text until each figure passes, with the figure and its text on one page. Compare the `(W) wrapped:` lines with T1's.
- [x] T6: Update the crop in the final comment of `docs/images/make-images.R`, rerun its commands, and rewrite the README sentence before the image and the image's alt text.
- [ ] T7: Render `docs/` with no R (AC5), and run `python3 tests/verify.py`.

## Work log

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: milestone — new content for seven published example pages, the home page, and the README image.
- 2026-10-28: idea vet: no concerns. Wrapping past the figure's bottom is the filter's documented behavior in each format, and wrap-it splits a paragraph by words in Typst.
- 2026-10-28: question set: pages — the seven one-wrap example pages, the home demo, and the README image; slides, dashboard, wrap-clear, and guide pages stay.
- 2026-10-28: question set: text — real prose about each example, no placeholder text.
- 2026-10-28: question set: straddle — one paragraph per figure starts beside it and continues below it.
- 2026-10-28: lessons used: 2026-10-28 (M023) freeze hashes the whole .qmd and pdf/typst output names; 2026-10-26 (M007) pdftohtml boxes; 2026-10-28 (M025) pdftohtml splits sentences; 2026-10-28 (M020) browser pane viewport; 2026-10-28 (M022) browser pane keeps old CSS.
- 2026-10-28: collision check: extends archived M023, which built these pages. No candidate row, D-entry, or open milestone overlaps. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-28: plan gate chose rewriting the seven one-wrap example pages over rewriting only the captioned-image page, because every example otherwise still shows text only beside the figure; falsified by a format where a page's figure cannot keep its text on one page at its current width.
- 2026-10-28: plan chose committed line-box readers in `tests/` over scratch scripts, because review must re-run the AC1 reads in a fresh session; falsified by a reader that cannot tell a figure page on `main` from one on the branch.
- 2026-10-28: criteria audit (full mode, Opus reader): 13 findings. AC1's "paragraph before" was already true on `main`, "full width" and "crosses" lacked edges, caption lines could pass as text below, no one-page rule, `layout.js` reads no lines below; AC2's move exception was loose and missed the YAML key; AC3's PNG origin could not be checked and README line 45 also describes it; AC4 lacked a clean render; AC5 could not hold, since a single-file render always runs R. All fixed in the wording above; AC4 dropped `verify.py`, which reads no `docs/` file, to T7.
- 2026-10-28: started on branch m026-wrap-showcase; `tests/__pycache__/` is untracked and left unstaged.
- 2026-10-28: T1 baseline: `quarto render docs` on `main` (Quarto 1.10.19, clean `docs/.quarto`) exits 0 with one `(W) wrapped:` line, "the figure #fig-callout is in a callout, so it does not wrap."
- 2026-10-28: T1: added `tests/docs_layout.py` (pdftohtml line boxes of the LaTeX, Typst, and LibreOffice PDFs) and `straddle()` in `tests/layout.js`. On `main`'s image-figure page both fail: LaTeX and Word "paragraph above has 1 line; no later line below the figure", Typst and HTML "paragraph above has 1 line". LibreOffice's PDF loses "e" and "g" in pdftohtml, so markers match with those letters removed.
- 2026-10-28: T5: the marker reader could not match LibreOffice's garbled text (letters lost and added, "figrst"), so `tests/docs_layout.py` now finds paragraphs by line spacing and font: body font lines are paragraphs, larger lines headings, others code. Markers stay for the HTML check only. On a `main` render in a temporary worktree it fails all 24 figure checks.
- 2026-10-28: T2-T4: each page got a full-width paragraph before its figure and a straddle paragraph. Paragraph lengths were set by T5's reads: LaTeX wrapfig narrows one or two lines past the figure's bottom, so each straddle paragraph runs 3 or more lines past it. `code-cell.qmd`'s paragraph above was cut to 2 lines because the longer one pushed the figure to page 2 in LaTeX, where it waited and left no text beside it.
- 2026-10-28: T3: `both-sides.qmd` got a `{{< pagebreak >}}` after its rule, because in Typst the second figure's paragraph above fell at the bottom of page 1 and the figure on page 2. Chosen over shortening the first group, which then failed to pass its figure's bottom in LaTeX.
- 2026-10-28: T5: all 24 figure checks pass on the 21 PDF renders, and `straddle()` passes all 9 HTML figures at 1280x900 on the 8 pages. The full `quarto render docs` printed the same sorted `(W) wrapped:` line as on `main`. Figure lines, enclosing divs, and YAML headers match `main` on all 8 pages, and the four freeze `hash` values equal the md5 of `code-cell.qmd`.
- 2026-10-28: T6: the crop in `docs/images/make-images.R` is now `-H 690`, and `readme-example.png` is 940x690 with the paragraph above, the two paragraphs beside, and the lines under the chart. README's sentence and alt text name the three parts.

## Decisions

## Review
