# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-25 (M002 done: HTML core row narrowed, its started token moved to M003)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M003 | Fall back in contexts that cannot wrap | planned | M002 | high | milestones/M003-context-fallbacks.md |
| M004 | Wrap figures in LaTeX PDF output | planned | M002, M003 | high | milestones/M004-latex-wrap.md |
| M002 | Wrap figures in HTML output | done | — | high | milestones/archive/M002-html-wrap.md |
| M001 | Run the four wrap feasibility spikes | done | — | high | milestones/archive/M001-wrap-spikes.md |

## Candidates
<!-- unnumbered ideas; one line each, ordered high → normal → low → parked:
     - [high] short title: detail — added YYYY-MM-DD — links
     - short title: detail — added YYYY-MM-DD — links
     - [parked] short title: detail; promote when <condition> — added YYYY-MM-DD — links
     the opening token is `[high]`/`[low]`/`[parked]` or absent (`normal`); `[parked]` marks a row whose
     promotion condition has not held — tracking-rules "Candidate priority token";
     open each row with its short title, the words the cairn pane shows, then `: `;
     the title is one sentence with no ending period, at least 5 words and at most 40 characters,
     ending with `(#N)` for a row written for GitHub issue N, such as
     `Fix SE of skewness calculation (#100)`; `/cairn-triage` offers a new title for one
     with fewer than 5 words or more than 40 characters; tracking-rules "Candidate short title" has the whole rule -->
- Wrap figures in HTML and LaTeX output: the version 1 core. Left after M002 (W1, the fixtures, the verify command, and the cell-carry scope): the context fallbacks (E3 to E8) and W2. For W2, test a moved cell class on the LaTeX path and fix the caption that runs into the footer (S2). M003 and M004 hold this work — added 2026-10-24, narrowed 2026-10-25 by M002 review — references/wrap-mechanisms.md — started M003
- Wrap figures in Typst PDF output: W3, with wrap-it bundled under `typst/packages`. Spike S3 in M001 showed that wrap-it 0.1.1 renders wrapped text with a citation. Add a `@citation` in wrapped text to `tests/fixture.qmd`, as the research page's test plan asks (M002 review, ripple #4) — added 2026-10-24 — references/wrap-mechanisms.md
- Wrap figures in Word output with frames: W4. Spike S4 in M001 showed that Word opens the file and shows one merged frame. This work also checks how LibreOffice and Google Docs show the frame (moved from M001 on 2026-10-24), and shows Word the frame `w:pPr` in the order a filter makes, after Pandoc's own `w:pPr`, with the caption style checked (found at M001 review) — added 2026-10-24 — references/wrap-mechanisms.md
- Handle a wrapped cell with two figures: a code cell with `#| classes: wrap-right` that makes two figures floats both side by side in HTML. Decide whether such a cell wraps its first figure, falls back with a warning, or joins the subfigure fallback (E4). Found at M002 review (diff-bug #5, blame-history #3). A wrapped cell with `fig-subcap` and `layout-ncol` gets an empty `.wrap-group` with nothing floating (M002 claim audit 2) — added 2026-10-24 — milestones/M002-html-wrap.md
- Check wrapped figures in dashboards: in a Quarto dashboard the `.wrap-group` div likely gets `html-fill-container`, a flex container, where a float has no effect. Not verified. Make wrapping work there or fall back with a warning. Found at M002 review (diff-bug #9) — added 2026-10-24 — milestones/M002-html-wrap.md
- Run the fixture renders in CI: a GitHub Actions workflow that runs `tests/verify.py` against the Quarto release and pre-release channels, with TinyTeX and R with knitr installed (research page, test plan). Chosen for later at the M002 plan's question set — added 2026-10-24 — references/wrap-mechanisms.md
- [low] Use the HTML stylesheet for EPUB: EPUB is HTML-based, so the W1 stylesheet can apply there. Version 1 keeps a normal figure in EPUB (W5) — added 2026-10-24 — references/wrap-mechanisms.md
