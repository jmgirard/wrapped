<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M036: List margin figures in the test summaries

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** internal — the LaTeX and Typst summaries of `tests/verify.py`; no rendered output changes for users
- **Branch/PR:** m036-margin-summaries

## Goal

The LaTeX and Typst summaries in `tests/verify.py` give each margin figure its own line, so no body figure's line takes a margin figure's label.

## Scope

**In:** `tex_summary` (`tests/verify.py:414`) lists each `marginfigure` environment as a `marginfigure:` line in document order, in the format of its `figure:` lines. `typ_summary` (`tests/verify.py:1339`) splits the `.typ` at each `#notefigure(` call as well as each `#figure(` call and writes a `notefigure:` line for each, so a body figure's chunk ends where a margin figure starts. A new Typst fixture with a body image with no id followed by a margin figure. The LaTeX and Typst snapshots in `tests/_snapshots/` that change. Absorbs the candidate row "List margin figures in the summaries".

**Out:** Margin content that is not a figure environment or call, such as a `\marginnote` or Typst `#note(` around an uncaptioned image, and margin tables. The order of M018's margin-meta cell stays as it is, since the new fixture covers the other order. HTML, revealjs, and Word summaries, which read classes and frames, not these calls.

## Acceptance criteria

- [ ] AC1: For each `pdf` and `typst` entry of `RENDERS` in `tests/verify.py`, the summary of its rendered `.tex` or `.typ` has one `marginfigure:` line per match of `\\begin\{marginfigure\}` and one `notefigure:` line per match of `^[ \t]*#notefigure\(` in that file, in document order. Each line carries the `fig-` label inside its LaTeX environment, or the first label line after its Typst call and before the next call, or `-` when there is none.
- [ ] AC2: A new fixture in `RENDERS`, rendered to Typst, holds a captioned body image with no id followed by a margin figure with a `fig-` id (the order M018 moved away from), and its snapshot holds `figure: -` followed by a `notefigure:` line with that id.
- [ ] AC3: `python3 tests/verify.py` passes on the review head, and in `git diff main -- tests/_snapshots` each changed line is an added `marginfigure:` or `notefigure:` line, a line of the AC2 fixture's new snapshots, or a `figure:` line whose old label is the label of a margin figure line in the new summary.

## Coverage

- AC1 → T1, T2, T4
- AC2 → T2, T3, T4
- AC3 → T4

## Tasks

- [x] T1: Add `marginfigure` to the environment pattern of `tex_summary`, so its line uses the same label, options, image, and link parts.
- [x] T2: In `typ_summary`, split at `#figure(` and `#notefigure(` calls that start a line or follow a cell's indent, keep which call opened each chunk, and write `figure:` or `notefigure:` lines in that order. Update the function's comment.
- [x] T3: Add the AC2 fixture to `tests/` and to `RENDERS` with a `typst` entry. Before T2, render it and record in the work log that the old `typ_summary` gives the image the margin figure's label.
- [ ] T4: Run `python3 tests/verify.py --update` and read the snapshot diff against AC3. With a script, count the AC1 regex matches in each `pdf` and `typst` render of `RENDERS` against the summary's lines. Run `python3 tests/verify.py`.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: not run — work named at the question set.
- 2026-10-30: question set: what to work on — all three normal-priority candidate rows, one milestone each, in the order M035, M036, M037; this one absorbs "List margin figures in the summaries".
- 2026-10-30: idea vet: no gap or flaw found.
- 2026-10-30: lessons used: 2026-10-27 (M012), 2026-10-29 (M032).
- 2026-10-30: collision check: candidate row "List margin figures in the summaries" absorbed; M018 (done) is its source and moved a cell instead of fixing the summary; no D-entry on the summaries. Checker-regress shape: no hit, since the summaries check the shipped filter's rendered output, not repo-internal records. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-30: probe (local renders on `main`): `\begin{marginfigure}` appears in six `.tex` files and `#notefigure(` in six `.typ` files (column-order, column-order-margin, column-order-fig-margin, column-order-page, contexts, margin-meta).
- 2026-10-30: criteria audit (reduced, fresh Opus reader; it ran after the plan commit 2244665): 5 findings, all fixed. A Typst label comes on the line after its `#notefigure(` call, not inside it (`tests/margin-meta.typ`), so AC1 and AC3 now read the first label line after the call. AC1 now names its regexes and its domain, the `pdf` and `typst` entries of `RENDERS`, because stale `.tex` and `.typ` files sit in `tests/`. AC2's one-off scratch run became a fixture in `RENDERS` (T3).
- 2026-10-30: status in-progress; branch m036-margin-summaries cut from main at 2f46345.
- 2026-10-30: T1 done: `tex_summary` matches `marginfigure`; on the kept renders it lists 1, 2, 8, and 6 `marginfigure:` lines for column-order, column-order-margin, contexts, and margin-meta, each with its label; no preamble holds the environment. The verify run for T1–T3 waits for T4, which updates the snapshots these tasks change on purpose.
- 2026-10-30: T3 done: new fixture `tests/margin-after-image.qmd` (Typst only) with a captioned image with no id, then `fig-after-image-margin` with `.column-margin`; added to `RENDERS` after column-order-margin. Its render holds one `#figure(` and one `#notefigure(` call at line start, and the old `typ_summary` printed `figure: fig-after-image-margin` and no other figure line.
- 2026-10-30: T2 done: `typ_summary` splits at `#figure(` and `#notefigure(` at line start with a captured kind and writes a line named for it. Choice: a margin figure's content for `image-width` ends before its `\n, caption: ` line, since its `kind:` sits on the call's first line. On the kept renders the new fixture reads `figure: -` then `notefigure: fig-after-image-margin`; margin-meta lists six `notefigure:` lines before its `figure: -`.
