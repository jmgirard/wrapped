<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M007: Stop LaTeX wraps at every stop block

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes the layout of every wrapped figure in PDF through LaTeX   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m007-latex-stops   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In PDF through LaTeX, a wrapped figure's wrap ends at the same block as in HTML, Typst, and Word, so that block, a `wrap-clear` div included, starts below the figure.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `wrapped.lua` groups each wrapped figure with the paragraphs after it
in LaTeX too, by the stop rule the other formats use, and ends each group with
a raw LaTeX command. `wrapped.tex` defines that command: it puts out a figure
that still waits for a paragraph, with no text beside it, and where lines are
still narrowed it skips to the figure's bottom, measured from the figure's
height and not from the `wrap-lines` count, then ends the wrap. A wrapped
figure that starts while an earlier one is still narrowed uses the same end
step. A new PDF-only fixture `tests/stop-latex.qmd` holds the figure-form
cases, a `wrap-lines` pair, and a page-bottom case. `tests/verify.py` reads
word and image positions from the LaTeX PDFs with poppler (D-006). The README
and DESIGN.md's Architecture say what LaTeX now does.

**Out:** A page break while lines are still narrowed still narrows the first
lines on the next page. That is a wrapfig limit, and the README keeps it.
Two-column classes and `\columnsep` leaks stay with the candidate row "Detect
two-column LaTeX classes and gaps". Running `tests/verify.py` in CI stays
with the candidate row "Run the fixture renders in CI".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     `ACn:` labels count top-to-bottom and renumber with Coverage. -->

Terms. A figure's bottom is the lowest edge of its image and its caption
text. A line is beside a figure when it is on the page of the figure's
image, its top is at or below the image's top and above the figure's
bottom, and its words do not overlap the figure horizontally. Text is below
a figure when it is on the figure's page under its bottom, or on a later
page. Full width means that every line but a paragraph's last starts and
ends within 2 pt of the ends of a full line on a page with no figure in the
same PDF. Each criterion's evidence is the position check that
`python3 tests/verify.py` runs on the PDF through LaTeX. It reads word and
image boxes with poppler, lists each case it measured, and fails, never
skips, a case whose figure, paragraph, and first stop text are not on one
page (AC4's case excepted). Rules and frames are not read, so a table rule,
a callout frame, or a horizontal rule beside a figure is not checked.

- [ ] AC1: In the PDF through LaTeX of `tests/stop-rule.qmd`, in each of its
      11 cases, the first line of the short paragraph after the wrapped
      figure is beside the figure, and the first text after that paragraph
      is below the figure. That text is the stop block's own text, or the
      line "Text after the stop block." in case 10 (horizontal rule) and
      case 11 (`wrap-clear` div). In case 8 the plain figure's image top and
      the line "Text after the stop block." are both below the wrapped
      figure.
- [ ] AC2: In the PDF through LaTeX of `tests/stop-latex.qmd`, the same holds
      for each of these four forms, each rendered once with `.wrap-left` and
      once with `.wrap-right`, and each followed by one short paragraph, a
      heading, and a paragraph of at least three lines: a figure with a
      `#fig-` id, a captioned image with no id, an image with no caption, and
      a knitr cell figure with `#| classes:`. The heading is below the
      figure, and the paragraph after it is full width.
- [ ] AC3: In `tests/stop-latex.qmd`, a wrapped figure whose `wrap-lines` is
      at least 5 more than the line count wrapfig computes from its height,
      followed by one short paragraph and a heading, has the heading below
      it. The distance from the figure's bottom to the heading's top is
      within one line height (the distance between two lines of a paragraph
      in the same PDF) of that distance for a copy of the case with no
      `wrap-lines`.
- [ ] AC4: In `tests/stop-latex.qmd`, a case whose last paragraph after a
      wrapped figure ends on page N and whose image is on page N+1 sets that
      figure with no text beside it: on page N+1 no text other than its
      caption starts above its bottom, and the stop block's text is below
      it. The check fails when the case's precondition (paragraph on page N,
      image on page N+1) does not hold.
- [ ] AC5: The HTML, revealjs, Typst, and Word output of every fixture, and
      the book project's HTML, render as before: `python3 tests/verify.py`
      passes, and `git diff <plan commit> --stat -- tests/_snapshots/` lists
      only `.pdf.txt` files.
- [ ] AC6: The README's "Where wrapping stops" section says that wrapping
      stops, and a `wrap-clear` div works, in PDF through LaTeX as in the
      other formats. Its "PDF through LaTeX" limits no longer say that
      wrapping stops in part, they say what AC4's figure does, and the
      "Figures in a row" limit says what the stop command now does. Each
      changed sentence matches a case that AC1 to AC4 measure.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2, T3
- AC2 → T1, T2
- AC3 → T1, T3
- AC4 → T1, T3
- AC5 → T4
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write `tests/stop-latex.qmd` (PDF only, `keep-tex`) with the AC2
      forms, the AC3 pair, and the AC4 case. Add the position check to
      `tests/verify.py`: it finds each case by its words, applies the AC1 to
      AC4 conditions, lists each case it measured, and fails on a missing
      case. Run it right after each LaTeX render, before the Typst render
      writes the same PDF path (lesson 2026-10-25, M004). Fail with a plain
      message when poppler is missing. Show each check red on a probe: the
      beside check with the wrap class removed and with the figure on the
      next page, the below check on `main`'s filter (text narrowed beside
      the figure) and with text on the figure's page above it, and the full
      width check with the wrap left on.
- [x] T2: In `wrapped.lua`, group in LaTeX as in the other formats: record
      wrapped floats and cells by custom id and cell token in LaTeX too
      (`float_target` and `cell_div`, about lines 677 to 777), put an image
      with no caption into a group (`group_blocks`, about line 1041), and
      end each group with the raw stop command.
- [x] T3: In `wrapped.tex`, define the stop command from `\wrapped@endwrap`:
      put out a waiting figure centered, skip to the figure's bottom from its
      height when lines are still narrowed, then end the wrap after the
      group as `\wrapped@afterenv` does. Use it for figures in a row. Check
      each placement with `\usepackage[verbose]{wrapfig}` (lesson 2026-10-25,
      M004).
- [x] T4: Make `tex_summary` in `tests/verify.py` record each stop command,
      run `python3 tests/verify.py --update`, and read the snapshot diff:
      only `.pdf.txt` files change, and each change is a stop command or a
      new fixture.
- [x] T5: Rewrite the README's "Where wrapping stops" paragraph about LaTeX
      and the "PDF through LaTeX" limits ("Wrapping stops only in part",
      "Figures in a row") against renders, and update passes 4, 5, and 7 of
      DESIGN.md's Architecture (`corrected M007`).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-26: created by /milestone-plan.
- 2026-10-26: tier check: not run — work named at the question set.
- 2026-10-26: idea vet: no concern. Ending the wrap at each stop block matches the stop rule of HTML, Typst, and Word; a moved figure that still waits at its stop block is put out with no text beside it, which follows from the user's answer below.
- 2026-10-26: question set: what to work on — "Honor wrap-clear and figures in LaTeX" (over CI renders, width input checks, Word follow-ups).
- 2026-10-26: question set: where a LaTeX wrap ends — at every stop block, as in the other formats (over wrap-clear and unwrapped figures only).
- 2026-10-26: question set: how the tests read the PDF layout — poppler in tests/verify.py (D-006), asked in a second round because the first did not cover the new test tool.
- 2026-10-26: lessons used: 2026-10-25 (M004) verify.py leaves Typst's PDF; 2026-10-25 (M004) wrapfig places a waiting figure at a paragraph start; 2026-10-25 (M004) grep -a on poppler output; 2026-10-25 (M003) Blocks filter inside cells and floats; 2026-10-25 (M002) find a float by its custom id.
- 2026-10-26: collision check: the candidate row "Honor wrap-clear and figures in LaTeX" is absorbed in full (wrap-clear, case 8 overlap, the wrap-lines skip); D-003 (back-to-back figures) stands, as its first figure has no paragraph and never groups; no other row, milestone, or D-entry overlaps. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-26: version 0.1.0 is pre-1.0 and no option or syntax changes, so the layout change takes no deprecation cycle.
- 2026-10-26: plan gate chose ending the wrap at every stop block over wrap-clear and unwrapped figures only because the user picked parity with the other formats; falsified by a LaTeX render where the stop command loses text or puts a figure over text.
- 2026-10-26: plan chose a skip to the figure's bottom from its height over the current skip by the remaining wrap-lines count because a large wrap-lines leaves blank lines; falsified by a PDF where the height-based skip ends above the figure's bottom.
- 2026-10-26: plan chose putting a waiting figure out with no text at its stop block over letting it wait for a paragraph past the stop because that paragraph can follow a heading the figure does not belong to; falsified by a fixture where the put-out figure leaves a page with no text before it.
- 2026-10-26: plan gate chose poppler in tests/verify.py over a TeX position log and over page images at the user's answer; falsified by poppler boxes that differ from the page image.
- 2026-10-26: criteria audit (full mode, fresh Opus reader) returned 12 findings, all settled toward the narrower promise: beside now needs the image's page and top (1); one-page cases fail, never skip (2); case 8 measures the plain figure's image (3); rules and frames are named as not read (4); AC2 adds a full width paragraph after the heading (5); AC2 names its four forms, each on both sides (6); AC3's excess is at least 5 lines (7); AC4 states its page precondition and fails without it (8); T1 names a probe for each check (9); AC5 states the output property with the snapshot diff as evidence (10); AC6 adds "Figures in a row" and ties sentences to measured cases (11); D-006 lands in the plan commit (12).
- 2026-10-26: started implement on branch m007-latex-stops; status in-progress.
- 2026-10-26: T1 (checkpoint, not checked off): added tests/stop-latex.qmd (PDF only, fig-format png, a page per case) and, in tests/stop-rule.qmd, a LaTeX-only raw block with a full-width paragraph and a \clearpage before each case so that each case has its own page. The layout check in tests/verify.py reads pdftohtml -xml boxes in a temporary folder (no image files left in tests/). On main's filter all 21 cases fail the below check; probes on scratch copies made the beside check fail with the wrap class removed and with the figure moved to the next page. The full-width probe waits for T3.
- 2026-10-26: implement chose pdftohtml -xml over pdftotext -bbox because it gives image boxes as well as text lines, which an image with no caption needs; both are poppler (D-006).
- 2026-10-26: T2 done: in LaTeX, cell_div sets the cell anchor (wraps()), float_target falls through to record wrapped ids and cells, an image with no caption and a wrappedfigure Figure start groups, and group_blocks ends each LaTeX group with a raw \wrappedstop.
- 2026-10-26: T3 done: wrapped.tex records the count each wrap starts with (\wrapped@startlines, added to \WF@startwrapping), \wrapped@endwrap skips the lines the height still needs (height lines less lines already set less one, none when wrap-lines is larger), and \wrappedstop runs it. All 21 layout cases pass. Probes on scratch copies: an unwrapped figure set flush right (fig-align="right") fails the beside check, and a stop that skips 8 lines but leaves the wrap on fails the full width check on both sides.
- 2026-10-26: AC3 precondition read from a scratch compile that logs \WF@startwrapping: wrapfig counts 13 lines for the lines-plain figure and starts lines-extra at 26 (wrap-lines 25 plus 1), and the height gives 13 for both, so 25 is 12 more than the height needs.
- 2026-10-26: T4 done: tex_summary records each \wrappedstop in place; `python3 tests/verify.py --update` passed all 36 renders and 21 layout cases. The snapshot diff is 39 added `wrappedstop` lines in 7 .pdf.txt files plus the new stop-latex.pdf.txt; no other snapshot changed.
- 2026-10-26: re-audit: AC1 (full) — 6 findings on the amended beside definition (first reader): half a line height bound with a flush-right probe (2), page 1 must hold no image (4), line height as a median over same-left lines (5), the short paragraph fits on one line (6); 1 and 3 found nothing. All taken; the fixed wording goes to a second reader.
- 2026-10-26: re-audit: AC2 (full) — same reader and findings as AC1, which AC2 reads through the Terms paragraph.
- 2026-10-26: T5 done: README "Where wrapping stops" now names LaTeX with Typst and Word; the wrap-lines paragraph says a stop block ends the wrap before that count; the LaTeX limits replace "Wrapping stops only in part" with the skip, give the moved figure's place (top of the next page, centered, read from stop-latex.pdf page 13: image left 342 of edges 125 to 794), and rewrite "Figures in a row". DESIGN.md stop-rule paragraph and Architecture passes 4, 5, 7 marked corrected M007.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
