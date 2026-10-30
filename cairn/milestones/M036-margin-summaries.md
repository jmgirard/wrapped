<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M036: List margin figures in the test summaries

- **Status:** review
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

- [x] AC1: For each `pdf` and `typst` entry of `RENDERS` in `tests/verify.py`, the summary of its rendered `.tex` or `.typ` has one `marginfigure:` line per match of `\\begin\{marginfigure\}` and one `notefigure:` line per match of `^[ \t]*#notefigure\(` in that file, in document order. Each line carries the `fig-` label inside its LaTeX environment, or the first label line after its Typst call and before the next call, or `-` when there is none.
- [x] AC2: A new fixture in `RENDERS`, rendered to Typst, holds a captioned body image with no id followed by a margin figure with a `fig-` id (the order M018 moved away from), and its snapshot holds `figure: -` followed by a `notefigure:` line with that id.
- [x] AC3: `python3 tests/verify.py` passes on the review head, and in `git diff main -- tests/_snapshots` each changed line is an added `marginfigure:` or `notefigure:` line, a line of the AC2 fixture's new snapshots, or a `figure:` line whose old label is the label of a margin figure line in the new summary.

## Coverage

- AC1 → T1, T2, T4
- AC2 → T2, T3, T4
- AC3 → T4

## Tasks

- [x] T1: Add `marginfigure` to the environment pattern of `tex_summary`, so its line uses the same label, options, image, and link parts.
- [x] T2: In `typ_summary`, split at `#figure(` and `#notefigure(` calls that start a line or follow a cell's indent, keep which call opened each chunk, and write `figure:` or `notefigure:` lines in that order. Update the function's comment.
- [x] T3: Add the AC2 fixture to `tests/` and to `RENDERS` with a `typst` entry. Before T2, render it and record in the work log that the old `typ_summary` gives the image the margin figure's label.
- [x] T4: Run `python3 tests/verify.py --update` and read the snapshot diff against AC3. With a script, count the AC1 regex matches in each `pdf` and `typst` render of `RENDERS` against the summary's lines. Run `python3 tests/verify.py`.

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
- 2026-10-30: T4 done: `--update` changed 12 snapshots by 43 added lines, all `marginfigure:` or `notefigure:`, with no `figure:` line changed, and wrote `margin-after-image.typst.txt` (`figure: -`, then `notefigure: fig-after-image-margin`). A scratch count script (not committed) read the 56 pdf and typst renders of `RENDERS`: 13 hold margin figures, and each summary's margin lines match the regex count and the labels read from the file in order; against main's `verify.py` it reports 13 of 13 mismatched. `python3 tests/verify.py`: all 106 renders pass.
- 2026-10-30: claim audit: not owed — internal tier
- 2026-10-30: status review; all four tasks checked, `python3 tests/verify.py` green on 6c2cfec.

## Review

- AC1 (6146b0f, renders from a fresh `python3 tests/verify.py` run): a scratch script imported `tests/verify.py` and read the 56 `pdf` and `typst` entries of `RENDERS`; 13 hold margin figures, and in each the `marginfigure:` or `notefigure:` line count equals the count of `\\begin\{marginfigure\}` or `^[ \t]*#notefigure\(` matches, with labels equal in order to those read from each environment or from the call to the next call; 0 mismatched. Against main's `verify.py`, 13 of 13 mismatch.
- AC2 (6146b0f): `("margin-after-image", "typst", True)` is in `RENDERS`; `tests/margin-after-image.qmd` holds a captioned image with no id, then `fig-after-image-margin` with `.column-margin`; `tests/_snapshots/margin-after-image.typst.txt` reads `figure: - image-width=no` then `notefigure: fig-after-image-margin image-width=no`, and the suite run compared it green.
- AC3 (6146b0f): `python3 tests/verify.py` exit 0, "all 106 renders pass". `git diff main -- tests/_snapshots`: 12 files modified, 1 added (`margin-after-image.typst.txt`), no removed line; every added line in the modified files is a `marginfigure:` or `notefigure:` line, and no `figure:` line changed.
- gate: `cairn_validate.py` all checks passed; no principle changed, so no impact report. Profile gate: the version marker is unchanged at one site; verify green (AC3); the diff touches no `docs/`, `_extensions/`, or docs checker, so the docs workflow and `tests/docs_layout.py` are not owed; changelog none.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a margin figure's content boundary `\n, caption: ` (and the body figure's `\nkind: `) assumes unindented lines, so an indented call would run to the next call and could report a later image's width — fix now (boundaries take `[ \t]*`), fixed 67d082d.
- diff-bug #2: no `notefigure:` line has `image-width=yes`, so the new boundary has no positive case — fix now (a margin figure with `width="50%"` added to the AC2 fixture; a scratch render shows Quarto keeps `width: 50.0%` inside the call), fixed 67d082d, 70ba6fc.
- diff-bug #3: the summaries disagree on `fig-aside`: LaTeX lists `marginfigure: fig-aside`, Typst lists `figure: fig-aside`, because Quarto writes `#note(` around a line-start `#figure(` — follow-up: candidate row "Summarize margin panels and Typst asides", parked, since no check reads an aside's kind; the line carries its own label, which is what the Goal asks.
- diff-bug #4: a margin figure with subfigure panels would report a panel's label in LaTeX and `notefigure: -` in Typst, as body panels already do; no render has one — follow-up: the same row, parked.
- diff-bug #5: AC1 says "the first label line" while the code takes the first `fig-` or `tbl-` label, so a margin call with no `fig-` label before a heading label would differ — reject (false): inside AC1's named domain, the `pdf` and `typst` entries of `RENDERS`, the AC1 script found every label equal; no render has the case.
- diff-bug #6: `python3 tests/verify.py` fails at three of the branch's commits — reject (false): the merge squashes the branch, so `main` gets one commit, green.
- blame-history #1: the comment's "content ends before its `kind:` line" is false for indented table-cell figures, a weakness since M013 widened the call split — fix now (same change as diff-bug #1), fixed 67d082d.
- blame-history #2: the notefigure width boundary is never exercised as a positive — fix now (same change as diff-bug #2), fixed 67d082d, 70ba6fc.
- blame-history #3: the module docstring names only `#figure(` calls for Typst — fix now (docstring names `#notefigure(` too), fixed 67d082d.
- blame-history #4: the new fixture sets no `fig-format: png` — reject (false): the option affects computed cell figures only, and the fixture has no code cell.
- prior-review #1: a `#notefigure(` with no caption line would run to the next call — reject (false): a scratch render shows Quarto writes a margin figure with no caption as a body `#figure(`, so every `#notefigure(` has a caption line.
- ripple #1: ROADMAP candidate row "List margin figures in the summaries" still describes the old behavior — reject (planned change): the plan absorbed the row, and post-merge hygiene removes it.
- ripple #2: `tests/verify.py` module docstring names only `#figure(` for Typst — fix now (same as blame-history #3), fixed 67d082d.
- ripple #3: the docstring's "each figure environment" for PDF does not name `marginfigure` — reject (false): `marginfigure` is a figure environment, so the sentence holds.
- ripple #4: `TYPST_BLOCKS` lacks `#notefigure`, so one beside a wrap box would count as "p" — reject (false): a margin figure is a block that is not a paragraph, so it ends the wrap group (`group_blocks`, `_extensions/wrapped/wrapped.lua`) and never sits in a wrap body.
- ripple #5: `cairn/references/wrap-mechanisms.md` W3 row names only `#figure(...)<id>` — reject (false): the row is about wrapped figures, which are body figures.
- ripple #6: candidate row "Wrap no-id margin images in PDF" cites `contexts` snapshots, which now also hold margin lines — reject (false): the reviewer found no conflict, and the cited no-id image lines are unchanged.
- 2026-10-30: review fix-now in progress: docstring, indented content boundaries, and a width case in the AC2 fixture committed; the snapshot update for them is running and lands in the next commit.
- 2026-10-30: review fix-now done: the update run changed only `margin-after-image.typst.txt` (added `notefigure: fig-after-image-margin-width image-width=yes`); fixes are in 67d082d and this commit.
- re-check after fix-now (70ba6fc): `python3 tests/verify.py` exit 0, all 106 renders pass; the AC1 script reads 13 renders with margin figures, 0 mismatched (the AC2 fixture now has 2 `notefigure:` lines); `git diff main -- tests/_snapshots` removes no line; the fix changed only the AC2 fixture's snapshot, by `notefigure: fig-after-image-margin-width image-width=yes`. A planted indented `#notefigure(` before a later `width:` image read `image-width=yes` before the fix and `no` after. AC1–AC3 hold on this head.
- snapshot files: none under a `_snaps` or `__snapshots__` directory; this repo's `tests/_snapshots/` changes are covered by AC3.
- 2026-10-30: step-7 approval: m036-margin-summaries approved for merge
