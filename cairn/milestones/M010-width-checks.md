<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M010: Check figure widths before use

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the filter's warnings and figure widths reach every user   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m010-width-checks   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A wrapped figure whose width is zero, is CSS that the filter cannot check, or is as wide as the Typst text or wider takes the default width.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The candidate rows "Warn when a figure width is zero", "Check CSS function lengths before use", and "Bound wide absolute widths in Typst". A zero width warns and takes the default in HTML, PDF through LaTeX, and PDF through Typst, as it already does in Word. A `calc()`, `min()`, `max()`, or `clamp()` value is checked against the CSS Values 3 rules before it reaches the HTML style or the breakpoint media query. A Typst absolute width as wide as the text or wider takes the default width while Typst runs, with no console warning. The README states each rule.

**Out:**
- A width under the text width that still leaves too little room, such as `6.3in` with a `1em` gap in 6.5 in of text. It stays as it is, with no row.
- Newer CSS math forms, such as `round()`, `pi`, and typed arithmetic. They print a warning by the user's choice at the question set.
- A console warning for the Typst rule. Typst has no warning function, and the user chose no estimate.
- Wide absolute widths in LaTeX. They are not in these rows.
- Typst columns. The row "Check wrapped figures in Typst columns" holds it.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: `tests/verify.py` renders two new fixtures to HTML, PDF through LaTeX, and PDF through Typst. The first holds the `wrapped:` values `width: 0%`, `gap: 0`, and `breakpoint: 0px`, and a figure with no width. In each format, the metadata width prints a warning that names it. That figure takes the built-in width, 40%, with a zero gap and no gap warning. In HTML, the media query uses `0px`. The second fixture holds `wrapped: width: 25%` and figures with the widths `0%`, `0in`, `0IN`, `0`, `0.0px`, and `.0`. In each format, each of those widths prints a warning that names it, and its figure takes 25%. Its figures with `wrap-gap="0pt"` and `wrap-gap="0"` keep a zero gap with no warning.
- [ ] AC2: `tests/verify.py` renders a new fixture to HTML, with no `wrapped:` metadata. Each value below is a figure's `width`. The values `min(40%, 300px)` and `calc(1px + 2)` are also a figure's `wrap-gap`. These values reach the figure's style as written, with no warning: `calc(100% - 2em)`, `min(40%, 300px)`, `max(20%, 10em)`, `clamp(10em, 30%, 400px)`, `calc((100% - 2em) / 3)`, `max(calc(20% + 1em), 8em)`, `calc(var(--w) * 0.5)`, `CALC(2 * 10px)`. These values print a warning that names them, and the figure takes the default: `calc(banana)`, `calc(100%-2em)`, `calc(1px + 2)`, `calc(1px * 2px)`, `calc(10px / 2px)`, `calc(5)`, `min()`, `clamp(1px, 2px)`, `calc(1px + 2px`, `calc(foo(30%))`, `min(40%, 2)`, `calc(var(w) * 2)`, `calc(round(30%, 1px))`, `calc(10px * 2em / 1em)`.
- [ ] AC3: `tests/verify.py` renders two new fixtures to HTML. The first holds the `wrapped:` values `breakpoint: calc(50%)` and `width: calc(1px + 2)`. Each prints a warning that names it. The media query uses `576px`, and a figure with no width takes 40%. The second holds `breakpoint: calc(30em + 100px)` and `width: min(40%, 300px)`, with no warning. The media query uses that breakpoint, and a figure with no width takes `min(40%, 300px)`.
- [ ] AC4: `tests/verify.py` renders a new fixture to PDF through Typst. It holds `wrapped: width: 10in`, a figure with no width, figures with `width="10in"` and `width="60em"`, a figure with `width="40%"`, and a figure with `width="2in"`. A check in `tests/verify.py` reads the PDF with `pdftohtml -xml`. The figure with no width and the figures at 10in and 60em each have an image width within 3 px of the 40% figure's. The first word of each of their paragraphs sits on a line beside the figure. The 2in figure's image width is within 3 px of 216 px, at pdftohtml's 1.5 px per pt.
- [ ] AC5: The README's Width and gap section states the zero-width rule, its zero-gap exception, and the function rules of AC2. Its Document defaults section states the zero and function rules for the metadata `width` and `breakpoint`. Its PDF through LaTeX and PDF through Typst sections state the zero-width rule. Its Typst section states the rule of AC4 and says that this rule prints no warning. Its Word section states the zero rule for every zero width, not only 0%.
- [ ] AC6: `python3 tests/verify.py` exits 0 on the branch head. The `verify.yml` CI run on the pull request passes.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T7
- AC2 → T2, T7
- AC3 → T3, T7
- AC4 → T4, T5, T7
- AC5 → T6
- AC6 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Zero widths. In `_extensions/wrapped/wrapped.lua`, make a plain number equal to zero not a width. This covers `checked_length` and its callers for a width: `style_for` (:343), `checked_tex_length` (:142), `checked_typst_length` (:172), and the metadata read (:637). A gap and a breakpoint of zero stay valid. Add the two AC1 fixtures to `RENDERS` for html, pdf, and typst. Confirm first that HTML and Typst take a zero width on `main` with no warning.
- [x] T2: CSS functions. Replace the unread pass in `css_length` (:87) with a tokenizer and a parser for `calc()`, `min()`, `max()`, and `clamp()` under the CSS Values 3 rules. Accept `var(--name)` and `var(--name, <fallback>)` terms. Function names and units are case-insensitive. With `no_percent`, a percent inside a function is not a length. Add the AC2 fixture to `RENDERS` for html. Write a source note for the CSS Values 3 calc() rules with section anchors, and its `cairn/references/INDEX.md` line.
- [x] T3: Breakpoint and metadata functions. Add the two AC3 fixtures to `RENDERS` for html. Make `html_summary`'s media-query pattern read a value that holds parentheses.
- [ ] T4: Typst guard. Make `typst_open` (:196) put the `wrap-content` call inside `layout(size => ...)`. Add a helper to `TYPST_HEADER` (:213) that uses the document default when the absolute width is `size.width` or more, and 40% when the default is too wide as well. Update `typ_summary`'s call patterns for the new form, so that a call it cannot read is still counted. Confirm first that the 10in figure breaks its text one word per line on `main`.
- [ ] T5: Typst layout check. Add the AC4 fixture to `RENDERS` for typst. Run the layout check on its Typst PDF, with the AC4 cases. Give the fixture's first page full text lines, or make `text_edges` handle a page with an image.
- [ ] T6: README. Write the AC5 rules in the Width and gap, Document defaults, PDF through LaTeX, PDF through Typst, and Word sections, from the renders of T1 to T5.
- [ ] T7: Run `python3 tests/verify.py --update`, read each snapshot diff, then run `python3 tests/verify.py` and confirm it exits 0.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-26: created by /milestone-plan.
- 2026-10-26: tier check: milestone — changes the filter's output in three formats and needs design choices.
- 2026-10-26: idea vet: two concerns. Typst has no warning function, so the Typst rule cannot warn; answered: default width with no warning, and the README says so. The CSS check would reject newer CSS that browsers accept, such as round(); answered: warn on newer forms, and the README lists what the check accepts.
- 2026-10-26: question set: the first plan run chose the width-check rows and included the Typst row; it stopped at the Typst concern, and this rerun posed both concerns.
- 2026-10-26: collision check: the three candidate rows are absorbed in full. Archived M003 (css_length) and M005 (the Typst 100% check) shipped the code this extends. No D-entry collides. GitHub has no open issues or PRs.
- 2026-10-26: criteria audit (full mode): 11 findings, all fixed. AC1 got a 25% document default to tell it from 40%, the `.0` and `0IN` forms, and metadata gap and breakpoint zero cases. Snapshot sentences were cut as instrument promises. The typ_summary and html_summary pattern updates moved to T3 and T4. round() is valid CSS Values 4, so AC2 names it as a value the filter warns on, and `calc(foo(30%))`, `min(40%, 2)`, and `calc(var(w) * 2)` were added. AC2 and AC3 gained wrap-gap and metadata locations. AC4 moved to its own fixture with a 40% reference figure and a 10in metadata width. The Goal narrowed to widths as wide as the text or wider. AC5 names the README's real sections and the Word zero wording.
- 2026-10-26: plan gate chose a Typst-side guard with no warning over a filter-side estimate from papersize and margin metadata, because the estimate can be wrong with a custom template or columns; falsified by a Typst release with a warning function, or a way for the filter to read the Typst text width.
- 2026-10-26: plan gate chose the CSS Values 3 rules over a full Values 4 parser, because the four functions and var() cover the README's forms with a small parser; falsified by users who need round(), constants, or typed arithmetic in a figure width.
- 2026-10-26: the Typst layout check in T5 uses poppler, which D-006 made a test requirement for LaTeX layout and CI already installs (D-008, D-009). No dependency changes.
- 2026-10-26: lessons used: 2026-10-25 (M005) wrap-it measures a percent in its grid column; 2026-10-26 (M007) pdftohtml boxes at 1.5 px per pt.

- 2026-10-26: implement started on m010-width-checks. On main, HTML and Typst took each zero width of the two zero fixtures as written, with no warning.
- 2026-10-26: checkpoint, T1 in progress: `checked_length` now warns on a zero width ("is zero"), and the zero fixtures are in RENDERS; their snapshots wait for the --update run. Word's zero-width warning text changed to the same wording. CSS source note written; it says "CSS Values 3" holds calc() only, so min(), max(), and clamp() come from Level 4 section 10.2.
- 2026-10-26: T1 done. `python3 tests/verify.py --update` passed all 45 renders; the six zero snapshots record each warning and width, and docx-options changed only its zero-width warning text.
- 2026-10-26: T2 done. A recursive parser above `css_length` reads calc(), min(), max(), clamp(), and var() terms; a scratch run of 38 values and the css-functions render match AC2's lists. Choice: a function value that fails prints the existing "is not a length or a percent" warning, with no new wording.
- 2026-10-26: T3 done. `html_summary`'s media-query pattern reads one level of parentheses. meta-calc-bad warns on both values and uses 576px; meta-calc-good keeps both. `python3 tests/verify.py --update` passed all 48 renders, and no earlier snapshot changed.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
