# M032: Warn for a wrap class on a link

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — adds a render warning that users see
- **Branch/PR:** m032-link-class-warning

## Goal

In HTML, PDF through LaTeX, PDF through Typst, and Word, a link that carries a wrap class prints a warning, since a wrap class on a link wraps nothing.

## Scope

**In:** A Link handler in the filter's last pass in `_extensions/wrapped/wrapped.lua` (beside `unplaced_image` and `unplaced_div`, about line 1908). For a link with `.wrap-left` or `.wrap-right`, it sets `found_wrap` as `unplaced_div` does and, in a format that wraps (`wraps()`), prints `wrapped: the link to <url> is not a figure, so it does not wrap. A wrap class goes on an image or a figure.`, with `<url>` the link's target. The link keeps its class, and no other output changes. Three new cases in `tests/fixture.qmd`, the four `fixture` snapshots, a line in `docs/normal-layout.qmd`, and DESIGN.md's architecture step 6.

**Out:** Making a wrap class on a link wrap its image: the request asks for a warning, and `docs/get-started.qmd` already says to put the class on the image. A wrap class on a span, heading, code, or other element that the last pass does not read: the new candidate row "Warn for a wrap class on a span". A test case for a link with a wrap class around a captioned image, which Quarto makes a Figure: the handler reads only the link, so it runs the same code as the cases below. The Word caption-style row "Keep caption style for caption images" stays a candidate row at the user's choice.

## Acceptance criteria

- [ ] AC1: After `python3 tests/verify.py`, the `fixture` snapshots for HTML, PDF through LaTeX, PDF through Typst, and Word each hold the line `1x wrapped: the link to <url> is not a figure, so it does not wrap. A wrap class goes on an image or a figure.` for each of three new `tests/fixture.qmd` links that carry a wrap class: one around an image with no wrap class, one around an image with its own wrap class, and one around text alone. Each of the three links has its own target, none of them `https://example.com`, and `<url>` is that link's target.
- [ ] AC2: In the same four snapshots, the first link's image keeps a normal layout and the second link's image wraps: in LaTeX, Typst, and Word, no `wrappedfigure`, wrap, or frame line carries `link=` with the first link's target, and one such line carries `link=` with the second link's target and the side its image's class names; in HTML, the first image's line keeps `style=width:` with the width it sets, and the second image's line has `style=-`. The fixture's existing `link.png` and `link-after.png` lines are unchanged, and no warning line names `https://example.com`.
- [ ] AC3: `docs/normal-layout.qmd` states that a wrap class on a link does not wrap and prints a warning in HTML, LaTeX, Typst, and Word, and `quarto render docs` exits 0.
- [ ] AC4: `python3 tests/verify.py` exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T2, T3

## Tasks

- [ ] T1: Add three cases to `tests/fixture.qmd` after "A float before a linked image" (about line 142), each with its own image copy (`tests/link-class*.png`) and its own target (`https://example.org/…`): an image with a width and no wrap class in a link with `.wrap-left`, an image with `.wrap-right` in a link with `.wrap-left`, and a text link with `.wrap-right` in a sentence. Render `fixture` in the four formats with the one-fixture command and confirm that no link warning prints before T2.
- [ ] T2: Add the Link handler to the last pass of `wrapped.lua`, with a comment in the style of `unplaced_div`'s, and register it in the returned filter list. Write the four `fixture` snapshots, read each diff against AC1 and AC2, and run `python3 tests/verify.py`.
- [ ] T3: Add the link rule to the "Other notes" list of `docs/normal-layout.qmd` (about line 146) and name links in step 6 of DESIGN.md's architecture. Run `quarto render docs`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: not run — work named at the question set.
- 2026-10-29: question set: which candidate to plan — "Warn for a wrap class on a link"; bundle the caption-style row — no, one row only.
- 2026-10-29: idea vet: gap — warn for any link with a wrap class or only a link around an image; took any link, since the row's title says "on a link" and `unplaced_div` warns for any div. No flaw: a warning where the filter cannot place a wrap matches DESIGN.md's goal to keep a normal figure and warn.
- 2026-10-29: lessons used: 2026-10-27 (M012) one-fixture render command; 2026-10-29 (M031) equal warnings count once, so each case gets its own image and target.
- 2026-10-29: collision check: absorbs candidate row "Warn for a wrap class on a link" (M031 plan); M031 (done) wraps an image whose class is on the image and does not cover this; no D-entry overlaps (D-003 next-block rule is unchanged). Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-29: scratch probe (Quarto 1.10.19, HTML): a link keeps its wrap class on the Link around an image, a captioned image (Quarto makes a Figure), text, and an image with its own wrap class, which still wraps; HTML writes `class="wrap-left"` on the `<a>`.
- 2026-10-29: plan gate chose to leave the class on the link over stripping it as `unplaced_div` does, because stripping changes HTML output with no layout effect (wrapped.css selects `.quarto-float` and `.wrapped-image` only); falsified by a stylesheet, Quarto's or the extension's, that selects a wrap class on an `a` element.
- 2026-10-29: criteria audit (full, fresh Opus reader): 6 findings. Fixed 4: AC1 now needs three distinct targets other than `https://example.com`, since equal warnings merge; the message's advice now fits a text link ("A wrap class goes on an image or a figure."); AC2 now names what each summary records (link targets and sides in LaTeX, Typst, Word; `style=` in HTML); the captioned-image case is named in Out as the same code path. No change: AC3 matches `wraps()`, and no rule or D-entry blocks any criterion.
- 2026-10-29: new candidate row "Warn for a wrap class on a span" for elements the last pass does not read.
- 2026-10-29: implement started on m032-link-class-warning.
- 2026-10-29: checkpoint (T1 to T3 written, unticked until `python3 tests/verify.py` finishes): three fixture cases; before `unplaced_link`, the four one-fixture renders printed no link warning; after it, the four snapshots hold the three warnings, only link-class-both wraps (right), link-class keeps `style=width:20.0%` in HTML; `quarto render docs` exit 0.
