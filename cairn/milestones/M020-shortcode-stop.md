# M020: Stop wraps at block shortcodes

- **Status:** in-progress
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

- [ ] AC1: In `tests/stop-shortcode.qmd`, the video case's figure is taller than the paragraph beside it plus one line. The paragraph that holds only `{{< video >}}` is outside that figure's wrap group in all four formats. In the HTML, Typst, and Word renders the group holds the figure and only the paragraph before the video, as the committed snapshots record. A `LAYOUT` case in `tests/verify.py` finds the line after that paragraph at full width below the figure in the PDF through LaTeX.
- [ ] AC2: In the same fixture, one case has a paragraph that holds only a shortcode from the fixture's own `shortcodes:` Lua file, which returns a div with a class. That paragraph ends the group: in the HTML render the group holds the figure and one paragraph, with no div after them.
- [ ] AC3: In the same fixture, one case has a paragraph that holds only `{{< kbd >}}`, one of the eight joining shortcodes. In the HTML render that paragraph and the paragraph after it stay in the group.
- [ ] AC4: In the same fixture, one case has `{{< include >}}` of a file with two paragraphs, on its own line after the paragraph beside the figure. In the HTML render the group holds the figure and three paragraphs.
- [ ] AC5: In the same fixture, one case has a wrapped figure followed directly by a paragraph that holds only `{{< video >}}`. In the HTML render that figure keeps its normal layout, in no group, and the render prints no warning for it.
- [ ] AC6: README "Where wrapping stops" says that a paragraph that holds exactly one shortcode and nothing else stops wrapping, and names the eight shortcodes that join. It says that such a paragraph right after a figure leaves the figure in its normal layout. It also says that Quarto expands `{{< include >}}` before the filter runs, so the included blocks follow the rule as written. DESIGN.md's stop rule, next-block rule, and filter step 1 say the same.
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
- [ ] T5: Run `python3 tests/verify.py` on macOS. The `verify.yml` workflow runs it at review.

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
