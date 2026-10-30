<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M037: Say LaTeX narrows lines past figures

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — a docs-site page that users read
- **Branch/PR:** m037-latex-narrow-past

## Goal

The Limits section of `docs/formats/latex.qmd` says that wrapfig can keep lines narrow past the bottom of a wrapped figure, with the number of lines measured in the site's LaTeX example PDFs.

## Scope

**In:** One sentence in the Limits section of `docs/formats/latex.qmd`, near its first bullet on how wrapfig counts narrowed lines. The number of lines it names comes from a measurement in this milestone: in the LaTeX PDF of each example page in `docs/examples/` that renders `pdf` (both-sides, code-cell, defaults, div-figure, image-figure, uncaptioned-image, width-gap, wrap-clear), for each wrapped figure, the count of narrowed lines on its page whose top lies below the figure's bottom (the lower of its image and its last caption line, as `caption()` in `tests/docs_layout.py` finds it) and above the next figure or stop block, read with `pdftohtml -xml`. Absorbs the candidate row "Say LaTeX narrows lines past figures".

**Out:** Changing the filter or `wrapped.tex` so that wrapfig narrows no line past the figure. Typst and Word, where the M026 renders show no such lines. A check in `tests/docs_layout.py` for the count, which would need a rule for what counts as narrow on every page.

## Acceptance criteria

- [x] AC1: The Limits section of `docs/formats/latex.qmd` says that wrapfig can keep lines narrow past a wrapped figure's bottom. It gives the number or range of lines as measured in the site's example pages, and that number or range includes every nonzero count that the Scope measurement finds in the eight LaTeX PDFs. If every count is zero, the sentence is not added and the candidate row is dropped with that measurement as its reason.
- [x] AC2: `quarto render docs` exits 0, and `python3 tests/docs_layout.py` passes on the rendered site.

## Coverage

- AC1 → T1, T2
- AC2 → T3

## Tasks

- [x] T1: Run `quarto render docs`. For each of the eight LaTeX PDFs, read text lines and images with `pdftohtml -xml` into a temporary folder. Count only body-font lines that are not the last line of their paragraph (split paragraphs with `blocks()` from `tests/docs_layout.py`). Beside a right figure, a line is narrowed when its right edge lies within 3 px of the right edge of the lines beside the figure. Beside a left figure, a line is narrowed when it starts at least the figure's width plus its gap in from the column's left edge. Measure past the Scope's figure bottom and on the figure's page only, since a page break is its own Limits bullet. Log one work-log line with the eight counts and the y values behind them.
- [x] T2: Write the sentence in the Limits section from the T1 counts.
- [x] T3: Run `quarto render docs` and `python3 tests/docs_layout.py`.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: not run — work named at the question set.
- 2026-10-30: question set: what to work on — all three normal-priority candidate rows, one milestone each, in the order M035, M036, M037; this one absorbs "Say LaTeX narrows lines past figures".
- 2026-10-30: idea vet: no gap or flaw found. The row's source render (M026 review: figure bottom y=814, narrow lines at y=816 and 836) is one page, so the plan measures all eight before the docs give a count.
- 2026-10-30: lessons used: 2026-10-26 (M007), 2026-10-28 (M025), 2026-10-28 (M026).
- 2026-10-30: collision check: candidate row "Say LaTeX narrows lines past figures" absorbed; M026 (done) is its source; M007 (done) and D-007 set the stop block that skips the narrowed lines at a stop; no D-entry on documenting this limit. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-30: criteria audit (full, fresh Opus reader; it ran after the plan commit 2244665): 4 findings on AC1, all fixed. The count now leaves out a paragraph's last line, headings, and code. The rule for a narrowed line now depends on which side the figure is on. The count starts at the figure's bottom with its caption (`caption()`), and it stays on the figure's page above the next figure or stop block. The page text gives the number as measured in the site's example pages. AC2: no finding.
- 2026-10-30: implement: branch m037-latex-narrow-past cut from main at ab03bb9; working tree clean.
- 2026-10-30: T1: measured with a scratch script on the `tests/docs_layout.py` helpers, after `quarto render docs` on this branch; narrowed lines past the figure bottom (bottom px; narrowed line tops): both-sides fig 1: 1 (889; 897), fig 2 (left): 1 (473; 481); code-cell: 1 (916; 920); defaults: 1 (906; 920); div-figure (left): 1 (885; 893); image-figure: 2 (814; 816, 836); uncaptioned-image: 1 (680; 684); width-gap (left): 1 (796; 816); wrap-clear: 0 (879; its beside paragraph ends at 613, and the full-width paragraph after the wrap-clear div starts at 907). Every narrowed line is in the paragraph that ran beside its figure. Nonzero counts: 1 and 2.
- 2026-10-30: T2: two sentences added to the first Limits bullet of `docs/formats/latex.qmd`, after the one on how wrapfig counts lines; "one or two" from T1, and "a paragraph that runs on below a figure" leaves out wrap-clear, whose beside paragraph ends beside its figure.
- 2026-10-30: T3: `quarto render docs` exit 0; `python3 tests/docs_layout.py` exit 0, 24 of 24 ok (LaTeX, Typst, Word); `python3 tests/verify.py` all 106 renders pass; the sentence is in `docs/_site/formats/latex.html`.
- 2026-10-30: claim audit: 2 claims read, 1 corrected — docs/formats/latex.qmd (fresh Opus reader: "under it" could read as under the image, where the PDFs show 1 to 4 narrow lines; now "past that bottom ... below it", that bottom being the figure's and its caption's; the reader's one re-read found it true, with defaults and width-gap at 1 or 2 by how a line starting 1 to 6 px above the caption's bottom is read).
- 2026-10-30: after the claim-audit fix: `quarto render docs` exit 0, `python3 tests/docs_layout.py` exit 0 (24 ok); `tests/verify.py` not rerun, since the fix touches only `docs/formats/latex.qmd`, which it does not render (106 of 106 passed at the T2 commit). Status set to review.
- 2026-10-30: step-7 approval: m037-latex-narrow-past approved for merge

## Review

- AC1 evidence (2026-10-30, branch head a27f42c, fresh `quarto render docs`): the first Limits bullet of `docs/formats/latex.qmd` says "The count can run past the bottom of the figure and its caption. In the LaTeX PDFs of this site's example pages, a paragraph that runs on past that bottom keeps one or two narrow lines below it." The T1 measurement re-run on this render gives the same counts: 1 for both-sides (both figures), code-cell, defaults, div-figure, uncaptioned-image, width-gap; 2 for image-figure; 0 for wrap-clear. Nonzero counts {1, 2} lie in "one or two". Pass.
- AC2 evidence (2026-10-30, same render): `quarto render docs` exit 0; `python3 tests/docs_layout.py` exit 0, 24 ok and 0 FAIL over LaTeX, Typst, and Word. Pass.
- gate: `cairn_validate.py` all checks passed (exit 0). Version marker unchanged (no `_extensions/` change). Changelog none. Docs workflow on the PR: runs at step 8.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: "skips the lines that the figure still needs" now reads as if it could mean only to the figure's bottom; `wrapped.tex` skips the rest of wrapfig's height count, extra lines included — fix now (now "skips the rest of the counted lines"), fixed 6d17397.
- diff-bug #2: "a paragraph that runs on past that bottom" describes less than wrapfig does, since a new paragraph inside the count is narrowed too — reject (false): the sentence before it states the general case, and this one reports what the example PDFs show.
- diff-bug #3: "below it" can read as below the paragraph — fix now (now "there"), fixed 6d17397.
- diff-bug #4: "narrow lines" breaks the page's "narrowed lines" term — fix now, fixed 6d17397.
- diff-bug #5: the first Limits bullet now has seven sentences on four topics — fix now (split into two bullets: the count and its overrun; the stop block and short text), fixed 6d17397.
- diff-bug #6: "this site's example pages" is not linked — fix now (links `../examples/index.qmd`), fixed 6d17397.
- diff-bug #7: the edit left a short source line unreflowed — fix now (reflowed with #1–#5), fixed 6d17397.
- diff-bug #8: no `cairn/DESIGN.md` Known issues entry for this limit — reject (false): LaTeX limits live in the site's Limits section (CLAUDE.md), and none of the other LaTeX limits has an entry.
- blame-history #1: the example pages, `docs/index.qmd`, and `docs/get-started.qmd` say the last lines run under the figure at full width, against the new LaTeX text — reject (false): the narrowed lines are the first ones below the bottom, and T1's past-line lists show full-width lines after them on every page; `docs/index.qmd` and `docs/get-started.qmd` render to HTML only.
- blame-history #2: defaults and width-gap reach a count only by how a line just above the caption's bottom is read — reject (false): T1 counts only line tops strictly below the bottom and still finds 1 on each (defaults 920 under 906, width-gap 816 under 796).
- blame-history #3: DECISIONS.md does not record narrowing past the figure under the default count — reject (false): this is a wrapfig limit, not a choice, and limits go on the site page.
- prior-review #1: the example pages' "last lines … to the right edge, under the figure" contradicts the new text — reject (false): same evidence as blame-history #1.
- prior-review #2: the edit left a ragged source line — fix now (same fix as diff-bug #7), fixed 6d17397.
- prior-review #3: "the lines" in the stop-block sentence can be read as the narrow lines — fix now (same fix as diff-bug #1), fixed 6d17397.
- ripple #1: README.md:44–47 says the last lines of the second paragraph run under the figure at full width — reject (false): those are the paragraph's last lines, which run full width in the image-figure LaTeX PDF (856, 877) after the narrowed 816 and 836.
- ripple #2: `_extensions/wrapped/wrapped.tex:99` says wrapfig's count "ends at about the figure's bottom" — reject (false): "about" stands, and the comment at lines 76–83 gives the end as `\WF@size`, which adds 1.5 `\baselineskip` and two `\intextsep` to the figure's depth, consistent with the new text.
- ripple #3–#7: `docs/index.qmd`, defaults, both-sides, image-figure, code-cell, div-figure, uncaptioned-image, width-gap say the last lines run full width under the figure — reject (false): same evidence as blame-history #1.
- ripple #8: `docs/get-started.qmd:40–42` says the paragraphs run full width once the text passes the figure's bottom — reject (false): the page renders to HTML only (`docs/_quarto.yml` has no other format), and the sentence describes its HTML demo.
- ripple #9: the candidate row "Say LaTeX narrows lines past figures" still reads as open — reject (false): post-merge hygiene graduates it.
- AC1 re-check after the fix (6d17397, fresh `quarto render docs`): the first Limits bullet now says "The count can run past the bottom of the figure and its caption. In the LaTeX PDFs of this site's [example pages](../examples/index.qmd), a paragraph that runs on past that bottom has one or two narrowed lines there." The T1 counts are unchanged, {1, 2} lie in "one or two". Pass.
- AC2 re-check after the fix: `quarto render docs` exit 0; `python3 tests/docs_layout.py` exit 0, 24 ok; the link renders as `../examples/index.html`. Pass.
- gate: `python3 tests/verify.py` all 106 renders pass (exit 0) on 2df8af7; the fix 6d17397 touches only `docs/formats/latex.qmd`, which the suite does not render.
- snapshot: no changed `_snaps` or `__snapshots__` file (the list is empty).
