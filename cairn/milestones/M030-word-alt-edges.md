# M030: Fix the Word alt text edge cases

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the alt text in users' Word documents
- **Branch/PR:** m030-word-alt-edges

## Goal

In Word output, a framed div float that holds more than one image gives its `fig-alt` text to no image but its first, and every framed image's alt text keeps the repeated spaces of its `fig-alt`.

## Scope

**In:** In `_extensions/wrapped/wrapped-docx.lua`, `alt_image` (called from `frame_para` on each framed paragraph) changes in two ways. First, the `alt` attribute, which Quarto 1.10.19 copies from a float's `fig-alt` onto every image of the float (scratch render with a post-render dump filter, 2026-10-29), sets the description of the frame's first image only. An image's own `fig-alt` still sets its description wherever it sits in the frame, and a later image with neither keeps its description as it was. Second, the text goes in as one string, so repeated spaces stay (today `pandoc.Inlines(alt)` makes them one space). In `_extensions/wrapped/wrapped.lua`, `wrapped_image_docx` no longer copies `fig-alt` into an uncaptioned image's caption, since `alt_image` sets it in the frame. New cases in `tests/docx-alt.qmd` and its snapshot. The alt-text sentences in `docs/formats/word.qmd` and the `wrapped-docx.lua` paragraph of `cairn/DESIGN.md`.

**Out:**
- A wrapped image inside a link, `[![](plot.png){.wrap-left}](url)`, wraps in no format (the filter warns that it "is not a figure or the only content of its paragraph"), so it has no frame. The candidate row "Wrap images inside links in all formats" holds it (the user's answer at this plan's question set).
- Figures with no wrap class, and wrapped figures that keep a normal figure in Word, keep Quarto's alt text (D-017).
- HTML, PDF through LaTeX, and PDF through Typst: unchanged. A scratch HTML render and a Typst render on 2026-10-29 kept the repeated spaces of an uncaptioned image's `fig-alt`.
- Changelog: none (`cairn/PROFILE.md` changelog slot).

## Acceptance criteria

- [x] AC1: In the docx render of `tests/docx-alt.qmd`, a framed div float that sets `fig-alt` and holds two images, each with no `fig-alt` and no description, has the float's `fig-alt` text as the first image's `descr` and an empty `descr` on the second image, as its frame line in `tests/_snapshots/docx-alt.docx.txt` records.
- [x] AC2: In the same render, a framed div float that sets `fig-alt` and holds a first image with its own `fig-alt` and a second image with a description and no `fig-alt` has the first image's own `fig-alt` as its `descr` and the second image's description as its `descr`; and a framed div float that sets `fig-alt` and holds a first image with no `fig-alt` and no description and a second image with its own `fig-alt` has the float's text as the first image's `descr` and the second image's own `fig-alt` as its `descr`; each as its frame line records.
- [x] AC3: In the same render, a framed uncaptioned image and a framed markdown image float, each with a `fig-alt` that holds two spaces in a row, have that text with both spaces as their image's `descr`, as their frame lines record.
- [x] AC4: `wrapped_image_docx` in `_extensions/wrapped/wrapped.lua` does not read `fig-alt`, and in the same render the existing uncaptioned image's frame line still records `alt='Alt for the uncaptioned image'`.
- [x] AC5: `python3 tests/verify.py` exits 0, and the branch changes `tests/_snapshots/docx-alt.docx.txt` and no other snapshot file (`git diff main --stat -- tests/_snapshots`).
- [x] AC6: `docs/formats/word.qmd` says that in a framed div float with more than one image, the float's `fig-alt` text is the alt text of its first image unless that image has its own `fig-alt`, and of no other image, and that an image with its own `fig-alt` has that text; `quarto render docs` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2
- AC5 → T2
- AC6 → T3

## Tasks

- [x] T1: In `tests/docx-alt.qmd`, add each case of AC1, AC2, and AC3 as a wrapped figure followed by a paragraph, with unique `fig-alt` texts and each image in a paragraph of its own (`docx_summary` reads one image per paragraph). Render the one fixture on the unchanged filter (the one-fixture command in `cairn/LESSONS.md`, 2026-10-27 M012). Confirm that each two-image float's frame line shows two `image` parts, and confirm the faults: both AC1 images and the second image of AC2's first float show the float's text, and the AC3 lines show one space.
- [x] T2: In `wrapped-docx.lua`, make `alt_image` set the caption to one `pandoc.Str` of the text (no inlines for an empty text), and pass it whether the image is the frame's first, so `alt` applies to the first image only. The flag is set once per frame in `frame_first`, for the figure-table path and the `.wrapped-image` path. Update the comments above `alt_image` and in the file header. In `wrapped.lua`, remove the `fig-alt` copy from `wrapped_image_docx` (about line 1553) and the sentence about it in its comment. Write the snapshot from the fixed render and read that the AC1 to AC4 lines match. Run `python3 tests/verify.py`.
- [x] T3: Add the multi-image rule to the alt-text sentences at `docs/formats/word.qmd:8`, from the T2 render, and to the `wrapped-docx.lua` paragraph of `cairn/DESIGN.md` (about line 303). Run `quarto render docs`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: idea vet: gap — a float's `fig-alt` when the frame's first image has its own `fig-alt`: reading taken, the image's own text wins and the float's text goes on no later image, as the answer gives the second image empty alt text; gap — a later image with a description of its own: reading taken, it keeps that description, its own text; gap — repeated spaces in the LaTeX and Typst copies: reading taken, Word only, as the row names `alt_image`; no flaw (the W3C images tutorial gives a group of images one text on its first image and empty alt text on the rest).
- 2026-10-29: question set: what to work on — "Fix the Word alt text edge cases"; a framed float with two images — the float's text on the first image only; a wrapped image inside a link — its own candidate row.
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render; 2026-10-29 (M029) where Quarto puts `fig-alt` and `alt` at Word post-render.
- 2026-10-29: collision check: absorbs the candidate row "Fix the Word alt text edge cases" in part; its linked-image sentence moves to the new row "Wrap images inside links in all formats" (the user's answer). D-017 holds (framed figures only). M029 shipped the rule this changes. Inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-29: plan gate chose a first-image flag per frame in the post-render pass over marking the first image in the pre-quarto pass, because at post-render every image of a float still holds Quarto's `alt` copy and the frame's walk sees the images in document order; falsified by a framed figure whose first image in `word/document.xml` is not the first image `frame_blocks` walks.
- 2026-10-29: checkpoint: plan committed while the full criteria audit (fresh Opus reader) runs; its findings and dispositions follow in a later line.
- 2026-10-29: criteria audit (full, fresh Opus reader): 10 findings. Fixed: #1 T1 puts each image in its own paragraph and checks two `image` parts; #3 AC2 adds a later image with its own `fig-alt`; #6 AC6 says the float's text skips a first image with its own `fig-alt`, and names framed figures only; #7 AC6 and the Goal narrowed to div floats; #8 AC5 reworded as a property of the branch. Answered by a scratch render (2026-10-29, filter plus post-render dump): #2 a second image's description reaches post-render as an image paragraph and is framed, so AC2 stands; #4 a markdown float's `alt` keeps two spaces at post-render; #5 an uncaptioned image keeps `fig-alt` at post-render. #9 the DESIGN.md and code comment edits stay task items, read at the review gate. #10 no action (discrimination confirmed).
- 2026-10-29: implement: branch m030-word-alt-edges cut from origin/main at af54cb1; status in-progress.
- 2026-10-29: T1 done: five cases added to `tests/docx-alt.qmd` (fig-two, fig-two-first, fig-two-second, fig-spaced, a spaced uncaptioned image); the unchanged filter gives both fig-two images and fig-two-first's second image the float's text, and both spaced texts one space. Each two-image frame line shows two `image` parts. fig-two-first's second image, a lone captioned image, becomes a Pandoc Figure, so its description also shows as a caption paragraph, as on main. Snapshot not yet written, so `tests/verify.py` fails on this commit.
- 2026-10-29: checkpoint: T2 code and snapshot written (`alt_image` takes a per-frame `first` flag through `frame_blocks`' new `state` table, and sets one `pandoc.Str`; `wrapped_image_docx` copy removed); the one-fixture render matches AC1 to AC4. T3's doc and DESIGN.md sentences written. The full `tests/verify.py` run and `quarto render docs` are still running or not yet run, so T2 and T3 stay unticked.
- 2026-10-29: T2 and T3 done: `python3 tests/verify.py` all 104 renders pass (exit 0), with only `tests/_snapshots/docx-alt.docx.txt` changed; `quarto render docs` exit 0. Claim audit (fresh Opus reader) running.
- 2026-10-29: claim audit: 11 claims read, 2 corrected — `_extensions/wrapped/wrapped-docx.lua` (the `state.seen` comment said it was set once the first image had alt text; it is set when the walk reaches it), `docs/formats/word.qmd` ("another image keeps its description" left "description" undefined; the re-read found the first rewrite read as a general rule that a fig-two first image breaks, so the sentence now names each later image without its own `fig-alt`). `quarto render docs` exit 0 after the fix.
- 2026-10-29: implement complete; status review.
- 2026-10-29: checkpoint: review pass 1 fix-now work committed (caption-icon flag fix with the fig-two-icon regression case, D-018, wording in `docs/formats/word.qmd`, `cairn/DESIGN.md`, and `wrapped-docx.lua` comments); the suite, docs render, and docs layout rerun on this head is still running, and the Review section is not yet written.
- 2026-10-29: review pass 1: verify all 104 renders pass on c45783a, docs render and `tests/docs_layout.py` pass; 19 findings: 9 fixed in c45783a (counting ripple #1 and prior-review #4 once each), 8 rejected, 2 noted, 0 follow-up.
- 2026-10-29: correction to the line above: the Review section's 19 findings are 8 fixed in c45783a, 9 rejected, 2 noted, 0 follow-up.
- 2026-10-29: step-7 approval: m030-word-alt-edges approved for merge

## Decisions

## Review

- 2026-10-29: Review pass 1 on c45783a (main at af54cb1, not moved). Evidence from `tests/_snapshots/docx-alt.docx.txt`, which `python3 tests/verify.py` matched in a run that passed all 104 renders (exit 0).
- AC1: frame line `fig-two` records `image plot.png fills=yes alt='Alt for the two-image float'; image plot.png fills=yes alt=''` (two images, neither with `fig-alt` or a description); T1's render on the unchanged filter gave both images the float's text.
- AC2: frame line `fig-two-first` records `alt='Alt for the first image'` then `alt='The second image’s description.'` (the fixture's bracket text after Pandoc's smart quote); frame line `fig-two-second` records `alt='Alt for the float with an alt on its second image'` then `alt='Alt for the second image'`.
- AC3: frame line `fig-spaced` (markdown image float) records `alt='Alt  for the  spaced float'` and the uncaptioned image's frame line records `alt='Alt  for the  spaced image'`, each with both double spaces; T1's render on the unchanged filter gave single spaces.
- AC4: `awk '/^local function wrapped_image_docx/,/^end/' _extensions/wrapped/wrapped.lua | grep -c fig-alt` prints 0; the existing uncaptioned image's frame line still records `alt='Alt for the uncaptioned image'`.
- AC5: `python3 tests/verify.py` on c45783a: "all 104 renders pass", exit 0. `git diff main --stat -- tests/_snapshots` lists only `tests/_snapshots/docx-alt.docx.txt` (17 insertions). (The AC5 box was ticked one edit before this line landed, because the evidence edit's anchor matched twice; the tick stands on this line.)
- AC6: `docs/formats/word.qmd:8-15` says "In a framed div float with more than one image, the float's `fig-alt` text is the alt text of its first image unless that image has its own `fig-alt`, and of no other image. An image with its own `fig-alt` has that text." `quarto render docs` on c45783a exit 0.
- gate: `cairn_validate.py` all checks passed; no principle changed, so `cairn_impact` skipped. Version markers: `_extensions/wrapped/_extension.yml` holds 0.2.0, unchanged. Verify passes on the review head (AC5). `tests/docs_layout.py` on the Mac after `quarto render docs`: exit 0, 24 `ok` lines, no other line (`--html` not run). The docs workflow runs on the PR. Changelog slot says none.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: an image inside a top caption (an icon) took the first-image flag, so the float's `fig-alt` reached no image — fix now: only an image that holds Quarto's `alt` counts; regression case fig-two-icon fails on 7b73abc (icon and both images `''`) and passes, fixed c45783a
- diff-bug #2: the docs did not say that a one-image frame's `fig-alt` replaces the square-bracket text — fix now, fixed c45783a
- diff-bug #3: the file-header comment left out the own-`fig-alt` exception — fix now, fixed c45783a
- diff-bug #4: fig-two-first's described second image also shows its text as a caption paragraph — reject (false): Pandoc makes a lone captioned image a figure, and a render without the filter also shows the text twice (scratch, 2026-10-29)
- diff-bug #5: no unwrapped multi-image float in the fixture — reject (planned change): D-017 leaves unwrapped figures to Quarto, and the "Figures outside a frame" cases are the ones the change leaves alone
- blame-history #1: the first-image rule was a user choice recorded only in the work log — fix now: D-018 added, fixed c45783a
- blame-history #2: one `pandoc.Str` keeps tabs and line breaks — reject (false): Pandoc's reader turns a line break in an attribute into a space before the filter runs (scratch render gave `descr="line one line two"`)
- blame-history #3: the removed `wrapped_image_docx` copy undoes no intent — noted
- blame-history #4: the empty `fig-alt` rule and the `fig-alt`-before-`alt` order still hold — noted
- blame-history #5: LaTeX keeps its `fig-alt` copy while Word no longer does — reject (planned change): LaTeX is out of scope (Scope Out)
- prior-review #1: later images now get empty alt text where M029 gave each the float's text — reject (planned change): the user's answer, D-018
- prior-review #2: a knitr cell with more than one plot under one `fig-alt` — reject (false): D-010 keeps such a cell's figures normal, so nothing is framed
- prior-review #3: a linked first image takes the float's alt — reject (false): it is the frame's first image that holds Quarto's `alt`, the documented rule
- prior-review #4: the docs' opening alt sentence overstated the rule — fix now (same edit as ripple #1), fixed c45783a
- prior-review #5: an unframed `.wrapped-image` fallback is untested — reject (false): the box holds one `Plain` image, which `frame_first` always frames
- ripple #1: `docs/formats/word.qmd` opening sentence overstated the rule — fix now, fixed c45783a
- ripple #2: the `cairn/DESIGN.md` sentence gave every framed image the float's `alt` — fix now, fixed c45783a
- ripple #3: the ROADMAP row "Fix the Word alt text edge cases" still describes the fixed faults — reject (planned change): post-merge hygiene graduates the row
- ripple #4: the `alt_image` comment said every framed image takes the text — fix now, fixed c45783a
- snapshot: tests/_snapshots/docx-alt.docx.txt — six new frame lines (fig-two, fig-two-first, fig-two-second, fig-two-icon, fig-spaced, the spaced uncaptioned image) and their image-width lines; AC1 to AC5 call for them, and fig-two-icon is diff-bug #1's regression case — called for
- conversation: not read (no PR exists yet)
