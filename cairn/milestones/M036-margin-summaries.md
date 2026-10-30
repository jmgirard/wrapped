<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M036: List margin figures in the test summaries

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** internal — the LaTeX and Typst summaries of `tests/verify.py`; no rendered output changes for users
- **Branch/PR:** —

## Goal

The LaTeX and Typst summaries in `tests/verify.py` give each margin figure its own line, so no body figure's line takes a margin figure's label.

## Scope

**In:** `tex_summary` (`tests/verify.py:414`) lists each `marginfigure` environment as a `marginfigure:` line in document order, in the format of its `figure:` lines. `typ_summary` (`tests/verify.py:1339`) splits the `.typ` at each `#notefigure(` call as well as each `#figure(` call and writes a `notefigure:` line for each, so a body figure's chunk ends where a margin figure starts. The LaTeX and Typst snapshots in `tests/_snapshots/` that change. Absorbs the candidate row "List margin figures in the summaries".

**Out:** Margin content that is not a figure environment or call, such as a `\marginnote` or Typst `#note(` around an uncaptioned image, and margin tables. The order of M018's margin-meta cell stays as it is. HTML, revealjs, and Word summaries, which read classes and frames, not these calls.

## Acceptance criteria

- [ ] AC1: For each `.tex` and `.typ` file that `python3 tests/verify.py` renders, its summary has one `marginfigure:` line per `\begin{marginfigure}` and one `notefigure:` line per `#notefigure(` that a regex count finds in that file, in document order, each carrying the `fig-` label inside its own environment or call, or `-` when it has none.
- [ ] AC2: In a scratch copy of `tests/margin-meta.qmd` whose margin cell follows the body image with no id (the order M018 moved away from), the Typst summary gives that image's line `figure: -` and gives the margin figure a `notefigure:` line with its label. The summary on `main` gives the image the margin figure's label.
- [ ] AC3: `python3 tests/verify.py` passes on the review head, and in `git diff main -- tests/_snapshots` each changed line is an added `marginfigure:` or `notefigure:` line or a `figure:` line whose old label sat inside a margin figure.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T2, T3
- AC3 → T3

## Tasks

- [ ] T1: Add `marginfigure` to the environment pattern of `tex_summary`, so its line uses the same label, options, image, and link parts.
- [ ] T2: In `typ_summary`, split at `#figure(` and `#notefigure(` calls that start a line or follow a cell's indent, keep which call opened each chunk, and write `figure:` or `notefigure:` lines in that order. Update the function's comment.
- [ ] T3: Run `python3 tests/verify.py --update` and read the snapshot diff against AC3. With a script, count the margin environments and calls in each rendered `.tex` and `.typ` against the summary's lines (AC1). Render the AC2 scratch copy with the new and the old `typ_summary`. Run `python3 tests/verify.py`.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: not run — work named at the question set.
- 2026-10-30: question set: what to work on — all three normal-priority candidate rows, one milestone each, in the order M035, M036, M037; this one absorbs "List margin figures in the summaries".
- 2026-10-30: idea vet: no gap or flaw found.
- 2026-10-30: lessons used: 2026-10-27 (M012), 2026-10-29 (M032).
- 2026-10-30: collision check: candidate row "List margin figures in the summaries" absorbed; M018 (done) is its source and moved a cell instead of fixing the summary; no D-entry on the summaries. Checker-regress shape: no hit, since the summaries check the shipped filter's rendered output, not repo-internal records. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-30: probe (local renders on `main`): `\begin{marginfigure}` appears in six `.tex` files and `#notefigure(` in six `.typ` files (column-order, column-order-margin, column-order-fig-margin, column-order-page, contexts, margin-meta).
