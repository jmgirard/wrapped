# M020: Stop wraps at block shortcodes

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes which blocks wrap beside a figure in every format
- **Branch/PR:** m020-shortcode-stop

## Goal

A paragraph that holds only a block shortcode, such as `{{< video >}}`, ends the wrap of the figure before it, as `{{< pagebreak >}}` does now.

## Scope

**In:** In `wrapped.lua`, the shortcode pass records the name of each shortcode by its custom id. The stop rule then ends a group at a paragraph that holds exactly one shortcode and nothing else. Eight Quarto shortcodes are the exception and join the group: `meta`, `var`, `env`, `kbd`, `lipsum`, `placeholder`, `version`, and `brand`. Such a paragraph also does not count as a paragraph for the next-block rule. This holds in HTML, PDF through LaTeX, PDF through Typst, and Word. A new fixture covers a video, a shortcode from the document's own `shortcodes:` file, a joining shortcode, an `{{< include >}}`, and a figure followed directly by a video. README "Where wrapping stops" and DESIGN.md state the rule.

**Out:** `{{< embed >}}` needs no change. Quarto turns it into a cell div before the filter runs. A scratch HTML render on 2026-10-28 put the embedded table after the wrap group. Under this rule, an inline shortcode from another extension, such as an icon alone on its line, stops the wrap. Letting such shortcodes join is the parked candidate row "Let icon shortcodes join wrap groups". A paragraph that holds two or more shortcodes still joins. revealjs takes the same stop rule as HTML and gets no fixture of its own here.

## Acceptance criteria

- [x] AC1: In `tests/stop-shortcode.qmd`, the video case's figure is taller than the paragraph beside it plus one line. The paragraph that holds only `{{< video >}}` is outside that figure's wrap group in all four formats. In the HTML, Typst, and Word renders the group holds the figure and only the paragraph before the video, as the committed snapshots record. A `LAYOUT` case in `tests/verify.py` finds the line after that paragraph at full width below the figure in the PDF through LaTeX.
- [x] AC2: In the same fixture, one case has a paragraph that holds only a shortcode from the fixture's own `shortcodes:` Lua file, which returns a div with a class. That paragraph ends the group: in the HTML render the group holds the figure and one paragraph, with no div after them.
- [x] AC3: In the same fixture, one case has a paragraph that holds only `{{< kbd >}}`, one of the eight joining shortcodes. In the HTML render that paragraph and the paragraph after it stay in the group.
- [x] AC4: In the same fixture, one case has `{{< include >}}` of a file with two paragraphs, on its own line after the paragraph beside the figure. In the HTML render the group holds the figure and three paragraphs.
- [x] AC5: In the same fixture, one case has a wrapped figure followed directly by a paragraph that holds only `{{< video >}}`. In the HTML render that figure keeps its normal layout, in no group, and the render prints no warning for it.
- [x] AC6: README "Where wrapping stops" says that a paragraph that holds exactly one shortcode and nothing else stops wrapping, and names the eight shortcodes that join. It says that such a paragraph right after a figure leaves the figure in its normal layout. It also says that Quarto expands `{{< include >}}` before the filter runs, so the included blocks follow the rule as written. DESIGN.md's stop rule, next-block rule, and filter step 1 say the same.
- [ ] AC7: `python3 tests/verify.py` passes on the review head on macOS and in the `verify.yml` workflow.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T1, T2
- AC5 → T1, T2
- AC6 → T4
- AC7 → T2, T3, T5

## Tasks

- [x] T1: Write `tests/stop-shortcode.qmd`, its shortcode file `tests/stop-shortcode.lua` (one shortcode that returns a classed div), and the included file with two paragraphs. Put each case on its own LaTeX page, as `tests/stop-rule.qmd` does. Add the fixture to `FIXTURES` in `tests/verify.py` for html, pdf, typst, and docx, with snapshots. Add a `LAYOUT` entry for the video case that reuses `stop_case`. Render all four formats with the default branch's filter first, and see the video and the document shortcode inside their groups.
- [x] T2: In `_extensions/wrapped/wrapped.lua` (`find_page_break` and `is_page_break`, near line 1560), record the name of each shortcode by custom id. Stop a group at a paragraph that holds exactly one shortcode outside the joining set. Update the comments, the filter list entry, and the snapshots. Read the snapshot diff, and make sure that `tests/stop-rule.qmd` case 12 still passes.
- [x] T3: Measure the fixture's HTML render in the built-in browser with `tests/layout.js`. For the video and document-shortcode cases, the block after the group starts below the figure.
- [x] T4: Update README "Where wrapping stops" and DESIGN.md (stop rule, next-block rule, filter step 1) as AC6 says. Check each claim against the renders of T1.
- [x] T5: Run `python3 tests/verify.py` on macOS. The `verify.yml` workflow runs it at review.

## Work log

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: milestone — choosing which shortcodes stop a wrap is a design decision.
- 2026-10-28: idea vet: three concerns. Embed already stops, because Quarto expands it before the filter, so the scope narrowed to block shortcodes (agent, toward the narrower scope). A video is a block only in HTML, so whether it stops in every format was asked: every format. The filter cannot see what an unknown shortcode makes, so the default was asked: stop unless one of the eight known joining shortcodes.
- 2026-10-28: question set (first run, same session): may implement and review use the built-in browser to measure HTML layout with tests/layout.js — yes.
- 2026-10-28: question set: video stops the wrap in every format or only HTML and slides — every format.
- 2026-10-28: question set: unknown shortcode alone on its line stops or joins — stops, unless one of the eight known joining shortcodes.
- 2026-10-28: plan gate chose a set of known joining shortcodes over a set of known block shortcodes (pagebreak, video, contents) because an unknown block beside a float can overlap the figure, while an early stop only leaves space; falsified by user reports of inline extension shortcodes alone on a line that stop wraps.
- 2026-10-28: criteria audit (full mode, fresh Opus reader): 7 findings, all fixed. AC1 now binds the render, not the snapshot, and needs a figure taller than one paragraph plus a line. AC2's shortcode returns a classed div. AC4 names its paragraph count. AC6 says "exactly one shortcode" and no longer calls the eight shortcodes text, since placeholder and brand return images. New AC5 covers a figure followed directly by a video (next-block rule). AC7 names verify.yml. The kbd case stands for the whole joining set, which the code names.
- 2026-10-28: collision check: the candidate row "Stop wraps at video and embed shortcodes" is absorbed. The page-break hotfix (PR #21) built the shortcode pass this extends. D-003, D-007, and D-010 read, no conflict. Inbox: 0 open issues, 0 open PRs.
- 2026-10-28: lessons used: 2026-10-27 (M013) dump filter to see what the filter sees at pre-quarto; 2026-10-25 (M004) LaTeX and Typst renders share tests/fixture.pdf; 2026-10-27 (M012) one-fixture verify run.
- 2026-10-28: T1: fixture `tests/stop-shortcode.qmd` (5 cases), `tests/stop-shortcode.lua`, `tests/_stop-shortcode-include.qmd`, four RENDERS entries and a LAYOUT case. With the default branch's filter the video and stop-box paragraphs sit in their groups in HTML (`fig-sc-video, p, div, p`), Typst, and Word, and the LAYOUT case fails: "the stop text 'https://www.youtube.com/embed/…' starts above the figure's bottom". Snapshots not yet written (checkpoint).
- 2026-10-28: T2 (checkpoint): `wrapped.lua` records every shortcode name by custom id (`find_shortcode`) and `is_block_shortcode` stops a group at a paragraph with one shortcode outside `JOINING_SHORTCODES`. Fixture renders now give groups `fig-sc-video, p` and `fig-sc-box, p` in HTML, one `p` in Typst, `p, clear` in Word, kbd and include `p, p, p`, `fig-sc-next` normal with no warning, and the LAYOUT case passes. DESIGN.md stop rule, next-block rule, and step 1 updated (T4 part). Full `verify.py --update` run in progress; snapshots not yet committed.
- 2026-10-28: T2: `python3 tests/verify.py --update` passed, "all 102 renders pass", "ok layout stop-rule case 12" and "ok layout stop-shortcode video". The only new files are the four `stop-shortcode` snapshots; no existing snapshot changed.
- 2026-10-28: T3: `tests/layout.js` `report()` in the built-in browser at 1280x900 (a 0-width hidden pane first gave float none under the breakpoint, so the size was set): all four wrapped figures float and pass, and each group's next block starts below its figure: video div at 376 px under figure bottom 359 px, stop box at 1256 px under 1239 px. `fig-sc-next` is in no group.
- 2026-10-28: T4: README "Where wrapping stops" gains the shortcode paragraph (eight joining shortcodes, extension shortcodes stop, include expanded first) and the next-block example of a lone video. `{{< pagebreak >}}` moved from the block list into that paragraph. `tests/readme.qmd` is the README fixture, so README.md itself is not rendered.
- 2026-10-28: claim audit: 20 claims read, 2 corrected — README.md, wrapped.lua. `meta` returns a block-valued key as is in block context, so "make text, an image, or paragraphs" became "usually make", with a `wrap-clear` hint; the video example now says it is a block in HTML and a link line elsewhere. DESIGN.md matched. The block-meta case predates M020 (every lone shortcode joined before), so it became the candidate row "Stop wraps at block meta values" rather than new scope.
- 2026-10-28: claim audit re-read (same reader, once): both corrected claims match Quarto 1.10.19, and the `wrap-clear` hint works (a Div ends the group); no new false claim.
- 2026-10-28: T5: `python3 tests/verify.py` (compare, no update) on macOS: "all 102 renders pass", 0 FAIL lines, "ok layout stop-rule case 12", "ok layout stop-shortcode video". The run began before the claim-audit commit, whose code change is a comment only. Status set to review.

## Review

Evidence on review head d5b29d2 (branch level with main e7c1526). `python3 tests/verify.py` on macOS: "all 102 renders pass", 0 FAIL lines, "ok stop-shortcode.html/.pdf/.typst/.docx", "ok layout stop-shortcode video", "ok layout stop-rule case 12".

- AC1: LAYOUT case "video" passes (`stop_case`: the paragraph is beside the figure, and the URL line and "Full width text after the video." start below the figure, full width). Snapshots: HTML group `fig-sc-video, p`; Typst wrap for `fig-sc-video` lists `p`; Word frame for `fig-sc-video` lists `p, clear`; the tex summary puts `wrappedstop` after `fig-sc-video`. On main the group was `fig-sc-video, p, div, p` and the LAYOUT case failed (T1 work log).
- AC2: HTML snapshot group `fig-sc-box, p` (the `stopbox` shortcode from `tests/stop-shortcode.lua` returns `div.stop-box`); on main it was `fig-sc-box, p, div, p`.
- AC3: HTML snapshot group `fig-sc-kbd, p, p, p`: the paragraph beside, the `kbd` paragraph, and "Text after the kbd."
- AC4: HTML snapshot group `fig-sc-include, p, p, p`: the paragraph beside and the two paragraphs of `tests/_stop-shortcode-include.qmd`.
- AC5: HTML snapshot lists `fig-sc-next: - style=-` (no wrap class) and no group for it; its `# warnings` section is empty. The tex summary lists `figure: fig-sc-next [-]`, a normal figure.
- AC6: README.md lines 174-185 state the lone-shortcode stop, name the eight joining shortcodes, and say Quarto expands `{{< include >}}` before the filter; the next-block paragraph names a figure right before a lone `{{< video >}}`. DESIGN.md's stop rule, next-block rule, and step 1 say the same (read on d5b29d2).
- AC7: macOS half passes (above); the `verify.yml` half runs on the PR at step 8, and the box is ticked only on its green run.

Consistency gate: `cairn_validate.py` "all checks passed". Version marker `_extension.yml` 0.2.0, unchanged on the branch (the one marker). verify passes (above). Changelog slot "none". No principle changed, so no `cairn_impact` run. Snapshot changes: four new files `tests/_snapshots/stop-shortcode.{html,pdf,typst,docx}.txt`, called for by AC1-AC5; no existing snapshot changed.

spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a block shortcode with anything else on its line (`{{< video >}} <!-- note -->`, or the shortcode in a span) still joins, so the video can sit beside the figure; pagebreak had the same gap before M020 — follow-up, row "Stop wraps at shortcodes with comments".
- diff-bug #2: the include case (AC4) passes on main too — reject, planned change: AC4 tests the README include claim the change adds.
- diff-bug #3: the video and stopbox cases run the same predicate path — reject, planned change: both are criteria, and only stopbox fails an implementation that stops at a fixed block list.
- diff-bug #4: only `kbd` of the eight joining names is tested — reject, planned change: one set lookup, accepted at the plan audit.
- diff-bug #5: a shortcode whose name is not a string (`{{< {{< meta sc >}} >}}`) now stops — reject, planned change: unknown names stop by the user's plan choice.
- diff-bug #6: DESIGN.md's "(corrected by the page-break hotfix, M020)" tag sits on the include sentence — fix now.
- diff-bug #7: long unwrapped lines in DESIGN.md and README.md — fix now, with #6 (same lines).
- blame-history #1: the stop-rule change has no D-entry, though D-003 and D-007 read "paragraph" and "stop rule" — fix now: new D-011.
- blame-history #2: `find_shortcode` reads the custom id unguarded, so a nil id would crash — reject, false: Quarto's `create_custom_node_scaffold` (share/filters/main.lua:724-742) always sets `__quarto_custom_id`.
- blame-history #3: an id missing from the table stops instead of joining — reject, planned change (unknown stops).
- blame-history #4: block-valued `meta` joins — follow-up, existing row "Stop wraps at block meta values".
- blame-history #5: the plan's rejected-alternative work-log line reads ambiguously — reject, style: history record, and the parked row states the promotion condition.
- prior-review #1: block-valued `meta` joins although a list stops a wrap — follow-up, existing row "Stop wraps at block meta values".
- prior-review #2: the README claim that a block-valued `meta` joins has no test — fix now: fixture case 6. The other untested claims it names are the eight-name set (one lookup, AC3) and DESIGN's embed sentence (a tracking record, from a scratch render) — rejected, planned change.
- prior-review #3: cases 2 and 5 have no LAYOUT check, so only the browser checked them — reject, false: the four snapshots record both cases' groups and figure kinds in every format.
- ripple #1: the candidate row "Stop wraps at video and embed shortcodes" still reads open — reject, planned change: step 9 hygiene graduates it.
- ripple #2: the comment above `group_blocks` names only "the first block that is not a paragraph" — fix now.
- ripple #3: the next-block and `no_text` comments say "not a paragraph" — fix now.
- ripple #4: README's lead sentence of "Where wrapping stops" reads as the full rule — fix now.
- ripple #5: DESIGN.md says Quarto expands `{{< embed >}}` before the filter, with no fixture — reject, false: the 2026-10-28 scratch render put the embedded table after the wrap group (Scope Out).
