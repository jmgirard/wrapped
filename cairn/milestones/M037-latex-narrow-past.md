<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M037: Say LaTeX narrows lines past figures

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — a docs-site page that users read
- **Branch/PR:** —

## Goal

The Limits section of `docs/formats/latex.qmd` says that wrapfig can keep lines narrow past the bottom of a wrapped figure, with the number of lines measured in the site's LaTeX example PDFs.

## Scope

**In:** One sentence in the Limits section of `docs/formats/latex.qmd`, near its first bullet on how wrapfig counts narrowed lines. The number of lines it names comes from a measurement in this milestone: in the LaTeX PDF of each example page in `docs/examples/` that renders `pdf` (both-sides, code-cell, defaults, div-figure, image-figure, uncaptioned-image, width-gap, wrap-clear), the count of narrowed lines whose top lies below the bottom of the figure beside them, read with `pdftohtml -xml`. Absorbs the candidate row "Say LaTeX narrows lines past figures".

**Out:** Changing the filter or `wrapped.tex` so that wrapfig narrows no line past the figure. Typst and Word, where the M026 renders show no such lines. A check in `tests/docs_layout.py` for the count, which would need a rule for what counts as narrow on every page.

## Acceptance criteria

- [ ] AC1: The Limits section of `docs/formats/latex.qmd` says that wrapfig can keep lines narrow past a wrapped figure's bottom, and the number or range of lines it gives includes every nonzero count that the Scope measurement finds in the eight LaTeX PDFs. If every count is zero, the sentence is not added and the candidate row is dropped with that measurement as its reason.
- [ ] AC2: `quarto render docs` exits 0, and `python3 tests/docs_layout.py` passes on the rendered site.

## Coverage

- AC1 → T1, T2
- AC2 → T3

## Tasks

- [ ] T1: Run `quarto render docs`. For each of the eight LaTeX PDFs, read text lines and images with `pdftohtml -xml` into a temporary folder. A line counts as narrowed when its edge on the figure's side stops at least the figure's width short of the text column's edge, and as past the figure when its top lies below the image's bottom. Log one work-log line with the eight counts and the y values behind them.
- [ ] T2: Write the sentence in the Limits section from the T1 counts.
- [ ] T3: Run `quarto render docs` and `python3 tests/docs_layout.py`.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: not run — work named at the question set.
- 2026-10-30: question set: what to work on — all three normal-priority candidate rows, one milestone each, in the order M035, M036, M037; this one absorbs "Say LaTeX narrows lines past figures".
- 2026-10-30: idea vet: no gap or flaw found. The row's source render (M026 review: figure bottom y=814, narrow lines at y=816 and 836) is one page, so the plan measures all eight before the docs give a count.
- 2026-10-30: lessons used: 2026-10-26 (M007), 2026-10-28 (M025), 2026-10-28 (M026).
- 2026-10-30: collision check: candidate row "Say LaTeX narrows lines past figures" absorbed; M026 (done) is its source; M007 (done) and D-007 set the stop block that skips the narrowed lines at a stop; no D-entry on documenting this limit. Inbox sweep: 0 open issues, 0 open PRs.
