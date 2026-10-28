<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M021: Stop wraps at more shortcode forms

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes where wrapping stops in every format the filter supports
- **Branch/PR:** m021-shortcode-stop-forms

## Goal

A paragraph that holds one shortcode outside D-011's eight joining names ends the wrap of the figure before it also when HTML comments, spaces, soft breaks, or one span surround the shortcode, and a lone `{{< meta >}}` ends it when its value holds a block other than a paragraph.

## Scope

**In:**
- `is_block_shortcode` in `_extensions/wrapped/wrapped.lua` (lines 1575–1582) skips HTML comments (the existing `is_comment` test on a raw HTML inline), `Space`, and `SoftBreak`, and looks inside one span that holds only those and the shortcode. The one shortcode found decides: a name outside D-011's eight stops, one of the eight joins.
- A paragraph that holds exactly one `{{< meta key >}}` and nothing else (Quarto's block context, `block_handler`) stops when the key's value, read from the document metadata as Quarto's `parseOption` reads it (dots split keys), holds a block other than `Para` or `Plain`. A value of paragraphs only joins (the user's answer at the question set), and so does a missing key, which Quarto renders as inline text.
- The next-block rule follows the new stop forms: a wrapped figure right before such a paragraph keeps its normal layout with no warning.
- New cases 7 to 13 in `tests/stop-shortcode.qmd`, a new expectation for case 6, the snapshots, and `LAYOUT` cases in `tests/verify.py`.
- README "Where wrapping stops" and its next-block paragraph, the DESIGN.md stop and next-block rules, the comment above `JOINING_SHORTCODES`, and a D-entry that annotates D-011.
- PDF through LaTeX shares the grouping path (`group_blocks`) with the other formats, and its snapshot lists no group members, so joining there is not checked on its own.

**Out:**
- A `meta` shortcode beside a comment, inside a span, or beside other text: Quarto renders it inline (`processValue` flattens blocks to inlines), so it joins as it does now. No work owed.
- `var`: Quarto 1.10.19 always renders it inline, so it keeps joining. No work owed.
- Nested spans, a shortcode inside emphasis, a link, or other inline markup, and a shortcode nested in another shortcode's argument: not planned; the README's `wrap-clear` advice covers them.
- Inline extension shortcodes that stop a wrap: the `[parked]` row "Let icon shortcodes join wrap groups".

## Acceptance criteria

- [ ] AC1: In `tests/stop-shortcode.qmd`, these paragraphs each stop the wrap: a comment, a space, one `{{< video >}}` shortcode, a soft break, and a comment (new case 7); and a span with a class that holds a comment, a space, and one `{{< video >}}` shortcode (new case 8). In the rendered HTML and Typst, each case's group holds only the paragraph before the shortcode, and the Word frame holds one `p` before `clear` (all recorded in the snapshots). A `LAYOUT` case of `tests/verify.py` for each passes in PDF through LaTeX: the text after the shortcode starts below the figure at full width. A wrapped figure right before case 7's form (new case 13) keeps its normal layout with no warning in all four formats.
- [ ] AC2: A paragraph that holds only `{{< meta stoplist >}}`, whose value is a Markdown list (case 6), and one that holds only `{{< meta >}}` of a dotted key whose value is a paragraph and a code block (new case 12), each stop the wrap: in the rendered HTML and Typst the group holds only the paragraph before the shortcode, and the Word frame holds one `p` before `clear`. A `LAYOUT` case for case 6 passes in PDF through LaTeX: the first list item starts below the figure. A paragraph that holds only `{{< meta >}}` of a key whose value is two paragraphs (new case 9) joins: in the same three formats the group holds the paragraph before it, both meta paragraphs, and the paragraph after it, and a `LAYOUT` case shows the first meta paragraph beside the figure in PDF through LaTeX.
- [ ] AC3: Two shapes still join the group: a `{{< kbd >}}` shortcode followed by an HTML comment (new case 10), and `{{< meta stoplist >}}` followed by an HTML comment (new case 11). In the rendered HTML, Typst, and Word, the shortcode's paragraph is in each case's group.
- [ ] AC4: In each of the four `stop-shortcode` snapshots, every line that names `fig-sc-video`, `fig-sc-box`, `fig-sc-kbd`, `fig-sc-include`, or `fig-sc-next` is the same as at commit 093e4ef, and the `# warnings` section is empty.
- [ ] AC5: README "Where wrapping stops" and the DESIGN.md stop rule state: a lone shortcode outside the eight joining names, with comments, spaces, soft breaks, or one span around it, stops; one of the eight with a comment beside it joins; a lone `meta` whose value holds a block other than a paragraph stops; a lone `meta` whose value is paragraphs joins; a `meta` with a comment beside it joins. The README's next-block paragraph and the DESIGN.md next-block rule say the rule applies to these stop forms. Neither the README, the DESIGN.md stop rule, nor the comment above `JOINING_SHORTCODES` says a lone block-valued `meta` joins or needs a `wrap-clear` div.
- [ ] AC6: `python3 tests/verify.py` exits 0 on macOS, and the PR's `verify` check passes.

## Coverage

- AC1 → T1, T2, T4
- AC2 → T1, T3, T4
- AC3 → T1, T2, T3, T4
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks

- [x] T1: Fixture first. Add cases 7 to 13 to `tests/stop-shortcode.qmd`, each after a `\clearpage`, with a paragraph of at least 3 full lines after each stop shortcode, as case 1 has (case 9 reads a new two-paragraph key, case 12 a nested key). Add `LAYOUT` cases for cases 6, 7, 8, and 9 to `stop_shortcode_cases` in `tests/verify.py` (line 615). Render the fixture with `main`'s filter and confirm that the `LAYOUT` cases for 6, 7, and 8 fail, each with the text after the shortcode beside the figure.
- [x] T2: Comments, spaces, and spans. Change `is_block_shortcode` (wrapped.lua:1575–1582) to skip comment raw inlines, `Space`, and `SoftBreak`, and to look inside one span that holds only such content and the shortcode, so that the one shortcode found decides the result.
- [x] T3: Block meta values. Record the first positional argument of a `meta` shortcode in `find_shortcode` (wrapped.lua:1563), keep the metadata in `read_meta` (wrapped.lua:1202), and resolve the key as Quarto's `parseOption` does. Stop only for the exact lone form, as a whitelist: every block in the value is `Para` or `Plain` → join; any other block → stop.
- [ ] T4: Run the fixture with `--update`, read the snapshot diff for cases 6 to 13 and the unchanged lines for cases 1 to 5, and check cases 6 to 9 in a browser with `tests/layout.js` at 1280x900.
- [ ] T5: Write the README, DESIGN.md, and code-comment text for AC5, and append a D-entry that annotates D-011 with the new forms and the user's choice that a paragraph-only `meta` value joins.
- [ ] T6: Run `python3 tests/verify.py` in full on macOS.

## Work log

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: not run — work named at the question set
- 2026-10-28: question set: work to plan — the two shortcode stop follow-up rows; a `meta` value of paragraphs only — joins the wrap. The set's dashboard answer (fall back with a warning) went to that candidate row.
- 2026-10-28: idea vet: no concern. The scratch render (Quarto 1.10.19, no filter) showed a video with a comment or in a span makes a block video, a two-paragraph meta makes two paragraphs, and a list meta with a comment makes inline text; Quarto's `block_handler` takes block context only for a Para or Plain with one inline, and `var` always renders inline.
- 2026-10-28: lessons used: 2026-10-25 (M004), 2026-10-27 (M012), 2026-10-27 (M015), 2026-10-28 (M020)
- 2026-10-28: collision check: absorbs candidate rows "Stop wraps at block meta values" and "Stop wraps at shortcodes with comments" (both from M020); extends done M020; D-011 gets an annotating D-entry at T5. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-28: plan gate chose to stop at a `meta` value only when it holds a non-paragraph block, over stopping at any block value, because paragraph text can wrap like typed text (user's answer); falsified by a render where a paragraph-only `meta` value beside a figure overlaps or misplaces it.
- 2026-10-28: plan chose to check a `meta` value only in the exact lone form, over checking it in every form, because Quarto flattens a `meta` in any other form to inline text; falsified by a Quarto version whose render of `{{< meta key >}} <!-- c -->` makes a block.
- 2026-10-28: plan chose to skip only HTML comments, spaces, soft breaks, and one span, over skipping any raw inline, because other raw inlines can show content; falsified by a user report of another invisible inline beside a lone shortcode.
- 2026-10-28: criteria audit (full mode, fresh Opus reader): 13 findings, all fixed. Added a soft-break and leading-comment form (case 7) and a comment inside the span (case 8); T1 states 3 full lines and `\clearpage` per case; case 6's LAYOUT property named; dotted key and mixed value tested (case 12), list unwrapping and `\.` escapes dropped from the promise; T3 states the whitelist; case 9 gets a LAYOUT and browser check; unchanged-case lines moved to AC4 and named by figure id; LaTeX joining noted in Scope as unchecked; docs criterion names the eight-name exception, the next-block rule, DESIGN.md, and the code comment; next-block case 13 added; Goal reworded to D-011's rule; criteria name rendered output and the Word `clear`.

- 2026-10-28: implement started on branch m021-shortcode-stop-forms, cut from main at ec52396.
- 2026-10-28: T1 done: cases 7 to 13 and LAYOUT cases "meta list", "video comments", "video span", "meta paragraphs". On main's filter the first three fail with the stop text above the figure's bottom (the URL line or the first list item), and "meta paragraphs" passes. Pandoc reads a comment that opens a line as a RawBlock, so case 7 holds the shortcode, a space, a comment, a soft break, and a comment; the leading comment is in case 8's span.
- 2026-10-28: re-audit: AC1 (full) — 3 findings on the first amended wording: case 13's "normal layout in all four formats" named no check (now the four snapshots' unwrapped records), case 8 covered only a comment and space before the shortcode in the span (now a soft break and comment after it in the span, and a space and comment outside it), and the Pandoc parenthetical is a reason, not a check (moved to the T1 line). Case 8 in the fixture changed to match.
- 2026-10-28: T2 and T3 done: `lone_shortcode` finds one shortcode among spaces, soft breaks, comments, and at most one span; `block_meta` reads a lone meta's key from the metadata as `parseOption` does and stops when the value holds a block other than Para or Plain. Render on the branch: cases 6, 7, 8, 12 group `p` only; cases 9, 10, 11 join; case 13 unwrapped in all four formats; warnings empty; all five LAYOUT cases pass. Choice: one shared `lone_shortcode` helper, recursive once for the span, over separate span and comment passes.
- 2026-10-28: re-audit: AC1 (full) — second reader, 5 findings: case 13 is a video, a space, and a comment, not case 7's full form; case 8's wording did not match the fixture (stale: the reader read it before the case 8 edit, and the fixture now matches); the snapshots record `p` tags, not which paragraph, so "only the paragraph before the shortcode" is more than they show; the LAYOUT wording should say the shortcode's line starts below the figure and the paragraph after it runs full width; optional, no case shows that a paragraph just outside the skip (a non-comment raw inline, a span with text) still joins. Second line for AC1, so the rewording goes to the user.
- 2026-10-28: T4: snapshots written for stop-shortcode in four formats. Lines naming exactly fig-sc-video, fig-sc-box, fig-sc-kbd, fig-sc-include, fig-sc-next match 093e4ef (9, 9, 4, 5 lines; matched by id followed by no letter or hyphen, since fig-sc-kbd-comment shares the prefix), and every `# warnings` section is empty. Browser check with `tests/layout.js` at 1280x900: every figure, group, and image entry ok; the blocks after cases 6, 7, and 8 start below their figures (gaps of 17 px), case 9's group runs to the next section, and no video sits in a wrap group.

## Decisions

## Review
