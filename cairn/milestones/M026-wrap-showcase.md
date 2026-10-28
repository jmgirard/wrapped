# M026: Show text wrapping past the figure in examples

- **Status:** review
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

- [x] AC1: For each wrapped figure in the page set P, three things hold on one page. P is `docs/index.qmd` in HTML, and `docs/examples/image-figure.qmd`, `div-figure.qmd`, `uncaptioned-image.qmd`, `code-cell.qmd`, `width-gap.qmd`, `defaults.qmd`, and `both-sides.qmd` in HTML, PDF through LaTeX, PDF through Typst, and the docx as LibreOffice renders it to PDF, 29 renders in all. (a) The last body-text block before the figure (before its code cell in `code-cell.qmd`, and after the `* * *` rule for `#fig-left` in `both-sides.qmd`) is a paragraph of at least two lines, and each of its lines but the last crosses the figure's horizontal span. (b) One paragraph after the figure has a line beside the figure and a later line below the figure's bottom that crosses the figure's horizontal span. (c) A line crosses the span of a `.wrap-right` figure when its right edge is right of the figure's left edge, and of a `.wrap-left` figure when its left edge is left of the figure's right edge. The figure's bottom is the lower of its image box and its last caption line. A line-box read of each of the 29 renders shows it: `pdftohtml -xml` for the three PDFs, and the line rectangles of a DOM Range over each paragraph in a browser at 1280x900 for HTML.
- [x] AC2: For each page in P, the multiset of its figure image lines, figure-div openers, and code-cell `#|` option lines is byte-identical to `main` at the plan commit, each figure keeps the same enclosing divs, and the page's YAML header is unchanged.
- [x] AC3: Rerunning the two commands in the final comment of `docs/images/make-images.R` on the branch head reproduces `docs/images/readme-example.png` at its committed pixel size, and the image shows a paragraph above the figure, lines beside it, and lines below it that run under it. The sentence before the image in `README.md` and the image's alt text name those three parts.
- [x] AC4: With one Quarto version and a clean `docs/.quarto`, `quarto render docs` exits 0 on the branch head, and the sorted `(W) wrapped:` lines it prints equal those of the same render on `main` at the plan commit.
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
- [x] T7: Render `docs/` with no R (AC5), and run `python3 tests/verify.py`.

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
- 2026-10-28: T7: `python3 tests/verify.py` passes, all 103 renders.
- 2026-10-28: claim audit: 105 claims read, 6 corrected — tests/layout.js, tests/docs_layout.py, docs/examples/width-gap.qmd, README.md, docs/examples/uncaptioned-image.qmd, docs/examples/both-sides.qmd. The `straddle()` comment named first and last words; the body font is counted over the PDF; HTML keeps width and gap as written; the README sentence named the wrong paragraph; "a few lines" was 7 to 9; the page break left a LaTeX page with only the rule.
- 2026-10-28: both-sides fix: the page break moved into `::: {.content-hidden when-format="pdf"}`, so LaTeX has 2 pages with the rule at the top of page 2. Without any break, Typst and Word split the second figure from its text. This div is a second `::: {` line in AC2's grep, but it encloses no figure.
- 2026-10-28: T7: after the fixes, `quarto render docs` from a clean `docs/.quarto` with no `Rscript` on `PATH` and `QUARTO_R`/`R_HOME` unset exits 0 with the same sorted `(W) wrapped:` line as `main`. `tests/docs_layout.py` passes 24 of 24, `straddle()` passes 9 of 9 at 1280x900, and the four freeze hashes equal md5 08a5ee68… of `code-cell.qmd`.
- 2026-10-28: review fixes changed `code-cell.qmd`, so its freeze was rendered again with R; the hashes are now 9cefb3c3658082ecd9dfbc8201a5d45f (Review section, re-verification line).
- 2026-10-28: step-7 approval: m026-wrap-showcase approved for merge

## Decisions

## Review

- AC1 (2026-10-28, head e934fd7, site from the clean no-R render): `python3 tests/docs_layout.py` exits 0, 24 of 24 figure checks ok over the 21 LaTeX, Typst, and LibreOffice PDFs of the 7 example pages. `straddle()` from `tests/layout.js` in the browser pane at 1280x900 returns ok for all 9 HTML figures on the 8 pages, each in a fresh frame. On `main` the PDF reader failed all 24 (T5 work-log line).
- AC2 (2026-10-28): for each of the 8 pages, the sorted lines matching `^!\[`, `^::: \{#fig`, and `^#\| ` hash the same on `main` and the branch, and the YAML header hashes the same. The one div line change is in `both-sides.qmd`: an added `::: {.content-hidden when-format="pdf"}` and its `:::` closer, which hold only the page break, after the rule and before `#fig-left`'s paragraph above. No figure is inside it, so every figure keeps its enclosing divs.
- AC3 (2026-10-28): `quarto render docs/examples/image-figure.qmd --to pdf` exits 0, and the `pdftoppm` command in `make-images.R`'s final comment writes a 940x690 PNG that `cmp` finds identical to the committed `readme-example.png`. The image (viewed) shows the full-width paragraph above the bar chart, two paragraphs beside it, and the second one's last three lines under it. README.md line 45-47 and the alt text name the paragraph above, the two beside, and the lines under the figure.
- AC4 (2026-10-28, Quarto 1.10.19 both runs): `quarto render docs` from a removed `docs/.quarto` exits 0 on `main` at 062cc3d and on the branch at e934fd7 (the no-R render). `diff` of the sorted `(W) wrapped:` lines is empty: one line each, "the figure #fig-callout is in a callout, so it does not wrap."
- AC5 (2026-10-28, local half): the four `execute-results/*.json` files are committed in 1919114 from a render with R, each `hash` is 08a5ee6868fcce0fc00ab889962f7f33, the md5 of the branch's `code-cell.qmd`, and the no-R `quarto render docs` (PATH holding only a `quarto` link, `/usr/bin`, `/bin`; `command -v Rscript` empty; `QUARTO_R` and `R_HOME` unset) exits 0. The docs CI half waits for the PR at step 8; the box stays unticked until that check passes.
- Consistency gate (2026-10-28): `cairn_validate.py` all checks passed. Profile slot: `_extension.yml` version unchanged (no version marker moved); `python3 tests/verify.py` passes, all 103 renders (T7, run on ccb9cc5; ccb9cc5..e934fd7 changes only README.md, three docs pages, `tests/docs_layout.py`, and `tests/layout.js`, which verify.py neither renders nor runs, since layout.js is for browser checks only); changelog slot "none".
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: width-gap.qmd says LaTeX and Typst convert `2.5in` and `2em`, but `tex_length` and `typst_length` pass them through (the `.typ` holds `2.5in` and `2em`) — fix now, fixed d7c902a (Word converts, HTML, LaTeX, and Typst use them as written)
- diff-bug #2: "after the text passes the bottom, each line runs the full width" is false in LaTeX, where one or two lines past the bottom stay narrow — fix now, fixed d7c902a (8 pages now say the paragraph's last lines run under the figure); the missing note in docs/formats/latex.qmd goes to the new row "Say LaTeX narrows lines past figures"
- diff-bug #3: paragraph split at 1.25 times the median line pitch can merge paragraphs on another page and pass AC1(b) with two paragraphs — follow-up, new row "Run the docs layout checks in CI"
- diff-bug #4: a caption more than 40 px below or 30 px wider than its image is not absorbed and can merge into a beside line — follow-up, same row
- diff-bug #5: `images[n]` is taken as figure n, so an extra image checks the wrong box — fix now, fixed d7c902a (a page whose image count differs from its figure count fails)
- diff-bug #6: `straddle()` merges rects within 3 px, does not check the above paragraph is the last block, and trusts `c.side` — fix now for the side, fixed d7c902a (it fails when the figure's class names the other side); the rest follow-up, same row
- diff-bug #7: `straddle()` was not shown to fail on layout — fix now, fixed d7c902a: on image-figure in the browser, a straddle paragraph cut to one sentence fails "no later line below the figure that crosses it", a one-line paragraph above fails "paragraph above has 1 line", and a wrong side fails "figure missing or on the other side"
- diff-bug #8: the readers are outside test scope, run by hand, and read an untracked render — reject, planned change (the plan chose committed readers in `tests/`; work-log line of 2026-10-28)
- diff-bug #9: the page break div gives HTML a print page break, the comment ships in HTML, and the LaTeX premise is a layout accident — fix now for HTML, fixed d7c902a (two `content-visible` divs, Typst and docx only; both-sides.html has no `page-break`); the comment and the page-fit premise reject, planned change, since `tests/docs_layout.py` checks page fit
- diff-bug #10: a one-line page, an empty font count, or a failed `soffice` run raises a traceback, not a FAIL line — reject, edge (inputs outside the 7 pages the checker reads; the effect is an error)
- diff-bug #11: repeated "comes before the figure" sentence and a near restatement in both-sides.qmd — reject, style; the defaults.qmd sentence it also names was fixed in a7c5579 (blame-history #3)
- diff-bug #12: `html.json` `supporting` path changed — reject, false (a fresh render writes it; the no-R render passes)
- diff-bug #13: the README crop ends before the "Next" heading — reject, false: the heading now starts page 2 of the LaTeX PDF, so no crop of page 1 holds it
- blame-history #1: `pagebreak` inside a div goes against the M010 lesson on containers — reject, false (that lesson is about wrap-it's box; the Typst and docx renders pass)
- blame-history #2: the pages depend on page fit — follow-up, row "Run the docs layout checks in CI"
- blame-history #3: defaults.qmd names "a figure on this page that sets its own width", but the page has none — fix now, fixed a7c5579
- blame-history #4: "HTML uses them as written" untested for percent gaps — reject, false (the page's values are `2.5in` and `2em`; no percent)
- blame-history #5: "until the next block that is not a paragraph" leaves out the lone-shortcode stop — reject, false (docs/stopping.qmd states the rule the same way first, then the shortcode case)
- blame-history #6: README gains a four-sentence image description after M024 shortened it — reject, planned change (the README image was in scope)
- prior-review #1: "each format" claims repeat M023's "every format" topic — reject, false (each names this page's layout in the 4 formats, checked by AC1)
- prior-review #2: width-gap units sentence near M023's "wrap-gap percents" — reject, false for percents; the sentence was fixed under diff-bug #1
- prior-review #3: alt-text sentence unchanged from `main` — reject, false (no regression)
- ripple #1: PROFILE.md verify slot names no docs checker — fix now, fixed a7c5579
- ripple #2: test-doctrine's LAYOUT tables line — reject, false (it is about filter changes)
- ripple #3: the consistency gate does not run the docs check — follow-up, row "Run the docs layout checks in CI"
- ripple #4: `tests/layout.js` header names no `straddle()` — fix now, fixed a7c5579
- ripple #5, #6, #7: verify.py docstring, CLAUDE.md test line, DESIGN.md test line name no docs check — reject, false (each describes the fixture suite, which is unchanged)
- Re-verification after the fixes (2026-10-28, head d7c902a): `quarto render docs` with R, then from a removed `docs/.quarto` with no R on `PATH` and `QUARTO_R`/`R_HOME` unset, exits 0; the sorted `(W) wrapped:` lines equal `main`'s. AC1: `tests/docs_layout.py` 24 of 24, `straddle()` 9 of 9 at 1280x900. AC2: figure lines and YAML hash the same on all 8 pages; both-sides.qmd's only div lines are the two `content-visible` page-break divs and their closers, which hold no figure. AC3: the two commands in `make-images.R` (crop now `-y 555 -H 690`) give a PNG that `cmp` finds identical to the committed 940x690 image, which shows the paragraph above, two beside, and three full lines under the chart. AC5 local half: the four hashes are 9cefb3c3658082ecd9dfbc8201a5d45f, the md5 of `code-cell.qmd`.
