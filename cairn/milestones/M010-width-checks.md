<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M010: Check figure widths before use

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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

- [x] AC1: `tests/verify.py` renders two new fixtures to HTML, PDF through LaTeX, and PDF through Typst. The first holds the `wrapped:` values `width: 0%`, `gap: 0`, and `breakpoint: 0px`, and a figure with no width. In each format, the metadata width prints a warning that names it. That figure takes the built-in width, 40%, with a zero gap and no gap warning. In HTML, the media query uses `0px`. The second fixture holds `wrapped: width: 25%` and figures with the widths `0%`, `0in`, `0IN`, `0`, `0.0px`, and `.0`. In each format, each of those widths prints a warning that names it, and its figure takes 25%. Its figures with `wrap-gap="0pt"` and `wrap-gap="0"` keep a zero gap with no warning.
- [x] AC2: `tests/verify.py` renders a new fixture to HTML, with no `wrapped:` metadata. Each value below is a figure's `width`. The values `min(40%, 300px)` and `calc(1px + 2)` are also a figure's `wrap-gap`. These values reach the figure's style as written, with no warning: `calc(100% - 2em)`, `min(40%, 300px)`, `max(20%, 10em)`, `clamp(10em, 30%, 400px)`, `calc((100% - 2em) / 3)`, `max(calc(20% + 1em), 8em)`, `calc(var(--w) * 0.5)`, `CALC(2 * 10px)`. These values print a warning that names them, and the figure takes the default: `calc(banana)`, `calc(100%-2em)`, `calc(1px + 2)`, `calc(1px * 2px)`, `calc(10px / 2px)`, `calc(5)`, `min()`, `clamp(1px, 2px)`, `calc(1px + 2px`, `calc(foo(30%))`, `min(40%, 2)`, `calc(var(w) * 2)`, `calc(round(30%, 1px))`, `calc(10px * 2em / 1em)`.
- [x] AC3: `tests/verify.py` renders two new fixtures to HTML. The first holds the `wrapped:` values `breakpoint: calc(50%)` and `width: calc(1px + 2)`. Each prints a warning that names it. The media query uses `576px`, and a figure with no width takes 40%. The second holds `breakpoint: calc(30em + 100px)` and `width: min(40%, 300px)`, with no warning. The media query uses that breakpoint, and a figure with no width takes `min(40%, 300px)`.
- [x] AC4: `tests/verify.py` renders a new fixture to PDF through Typst. It holds `wrapped: width: 10in`, a figure with no width, figures with `width="10in"` and `width="60em"`, a figure with `width="40%"`, and a figure with `width="2in"`. A check in `tests/verify.py` reads the PDF with `pdftohtml -xml`. The figure with no width and the figures at 10in and 60em each have an image width within 3 px of the 40% figure's. The first word of each of their paragraphs sits on a line beside the figure. The 2in figure's image width is within 3 px of 216 px, at pdftohtml's 1.5 px per pt.
- [x] AC5: The README's Width and gap section states the zero-width rule, its zero-gap exception, and the function rules of AC2. Its Document defaults section states the zero and function rules for the metadata `width` and `breakpoint`. Its PDF through LaTeX and PDF through Typst sections state the zero-width rule. Its Typst section states the rule of AC4 and says that this rule prints no warning. Its Word section states the zero rule for every zero width, not only 0%.
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
- [x] T4: Typst guard. Make `typst_open` (:196) put the `wrap-content` call inside `layout(size => ...)`. Add a helper to `TYPST_HEADER` (:213) that uses the document default when the absolute width is `size.width` or more, and 40% when the default is too wide as well. Update `typ_summary`'s call patterns for the new form, so that a call it cannot read is still counted. Confirm first that the 10in figure breaks its text one word per line on `main`.
- [x] T5: Typst layout check. Add the AC4 fixture to `RENDERS` for typst. Run the layout check on its Typst PDF, with the AC4 cases. Give the fixture's first page full text lines, or make `text_edges` handle a page with an image.
- [x] T6: README. Write the AC5 rules in the Width and gap, Document defaults, PDF through LaTeX, PDF through Typst, and Word sections, from the renders of T1 to T5.
- [x] T7: Run `python3 tests/verify.py --update`, read each snapshot diff, then run `python3 tests/verify.py` and confirm it exits 0.

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
- 2026-10-26: T4 done. Each Typst call is now `#layout(wrapped-size => wrap-content(...))`, closed by `]))`; `layout` gives the context that wrapped-side needs, so `#context` went. Choice: `wrapped-width(size, ..widths)` takes the figure width, the document default, and 40%, and returns the first that is a percent or narrower than `size.width`. typ_summary reads the new form; the Typst snapshot diffs change only that argument, and none reports an unread call.
- 2026-10-26: T5 done. New fixture typst-wide.qmd; `layout_check` takes a case table, and TYPST_LAYOUT runs it after a Typst render. Choice: the Typst cases check that the first line sits beside the image and inside the text edges, not `check_beside`'s edge distance, because page 1's widest line runs 7 px past the right margin. On main's filter, the no-width, 10in, and 60em cases fail ("0 lines hold 'Marker none'"): pdftohtml shows each paragraph one word per line, "Marker" alone at x=1232 past the edge at 790. `python3 tests/verify.py --update` passed all 49 renders and every layout case.
- 2026-10-26: T6 done. README states the zero rule and zero-gap exception and the function rules (Width and gap), the metadata rules (Document defaults), the zero rule (LaTeX, Typst), the Typst wide-width rule with no warning, and Word's zero rule. DESIGN.md Architecture steps 5 and 7 name the `layout` call and `wrapped-width` (corrected M010).
- 2026-10-26: checkpoint, T7 in progress: `python3 tests/verify.py` passed all 49 renders on 4306181. The verify.py docstring and PROFILE.md's verify slot now name TYPST_LAYOUT. Paused at the user's request (low battery); the claim audit and the hand-off to review are left.
- 2026-10-26: resumed after the pause; origin/main has not moved since the cut. PROFILE.md's verify sentence split in two. T7 done: `python3 tests/verify.py` passed all 49 renders and every layout and log case; `cairn_validate` passed.
- 2026-10-26: claim audit: 41 claims read, 4 corrected — README.md (zero gap and metadata zero gap: Word warns on a 0% gap), tests/verify.py (find_words docstring: double spaces only in some lines), tests/typst-wide.qmd (the 2in figure does not match 40%). The reader re-read the four corrections once and found each holds. `python3 tests/verify.py` passed all 49 renders after them.
- 2026-10-26: implement done; status set to review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->

Evidence pass 1, 2026-10-26, head ac92bfc. `python3 tests/verify.py` exit 0, "all 49 renders pass".

- AC1: zero-meta (html, pdf, typst) each warn once, `width "0%" on the wrapped metadata is zero, so it is 40%.`; the figure is 40% (`--wrap-width: 40%`, `width=0.4\linewidth`, `wrapped-width(wrapped-size, 40%, 40%, 40%)`) with gap 0 (`0px`, `gap=0pt`, `column-gutter: 0pt`) and no gap warning; HTML breakpoint `0px`. zero-width (html, pdf, typst) each warn 6 times, one per width `0%`, `0in`, `0IN`, `0`, `0.0px`, `.0`, each "is zero, so it is 25%", and those six figures are 25%; fig-gap-zero-pt and fig-gap-zero keep gap 0 (`0pt`/`0px`, `gap=0pt`, `column-gutter: 0pt`) with no gap warning.
- AC2: css-functions.html snapshot: fig-valid-1 to 8 keep each listed width as written (`calc(100% - 2em)` … `CALC(2 * 10px)`) and fig-valid-9 keeps gap `min(40%, 300px)`, with no warning for any. 15 warnings: fig-invalid-1 to 14 each name their listed width (`calc(banana)` … `calc(10px * 2em / 1em)`) and take `--wrap-width: 40%`; fig-invalid-15 names gap `calc(1px + 2)` and takes `1em`. No `wrapped:` metadata in the fixture.
- AC3: meta-calc-bad.html: warnings `breakpoint "calc(50%)" … is not a length, so it is 576px.` and `width "calc(1px + 2)" … so it is 40%.`; breakpoint `576px`; the figure with no width is `--wrap-width: 40%`. meta-calc-good.html: no warnings; breakpoint `calc(30em + 100px)`; the figure with no width is `--wrap-width: min(40%, 300px)`.
- AC4: the verify run prints `ok layout typst-wide` for 40%, no width, 10in, 60em, and 2in. `typst_width_case` reads typst-wide.pdf with `pdftohtml -xml`; each of the no-width, 10in, and 60em images is within 3 px of the 40% image (259 px each in the T4 render), each paragraph's first line sits beside its image inside the text edges, and the 2in image is within 3 px of 216 px. On main's filter the three wide cases fail (T5 work log).
- AC5: README.md Width and gap: zero-width rule (line 76), zero-gap exception (line 80), function rules (lines 83-97). Document defaults: zero and function rules for metadata `width` and `breakpoint` (lines 121-128). PDF through LaTeX: zero rule (line 207). PDF through Typst: zero rule (line 285), wide absolute width rule and "the render prints none" (lines 291-296). Word: "a width of zero, and a gap of 0%" (line 340).
- AC6: local half: `python3 tests/verify.py` exit 0 on ac92bfc. The CI half waits for the PR at step 8.

Consistency gate, 2026-10-26: `cairn_validate.py` all checks passed. No DESIGN.md principle changed, so `cairn_impact` skipped. Toolchain slot: the one version marker, `version: 0.1.0` in `_extensions/wrapped/_extension.yml`, is unchanged by the diff; the verify command passed (above); the changelog slot says "none".

Review pass 1, 2026-10-26. spawned: diff-bug, blame-history, prior-review, ripple. No finding shows a criterion failing or a load-bearing defect, so no return.

- diff-bug #1: metadata values pass through Pandoc's smart punctuation, so `--` in `var(--w)` becomes an en dash and `2*1em*1` loses its asterisks as emphasis; the README says metadata takes function values — fix now (restore `--` from an en dash in metadata; README tells users to put spaces around `*`).
- diff-bug #2: a zero inside a function (`calc(0%)`, `min(0px, 10%)`, `calc(-10px)`) passes with no warning, against README "A width of zero … prints a warning" — fix now for the README wording (a width of zero written as a number); the check itself — follow-up to row "Warn on zero widths in CSS functions".
- diff-bug #3: a breakpoint accepts `var()`, which a media query cannot use, so the narrow rule drops with no warning — fix now (a `no_percent` read also refuses `var()`; fixture meta-calc-var).
- diff-bug #4: no test covers the document default being chosen by `wrapped-width` — fix now (fixture typst-wide-meta with a 2in default).
- diff-bug #5: the wide cases compare against the 40% figure in the same PDF, so nothing states 40% independently — fix now (cases expect 259 px, 40% of the 6 in text of Quarto's Typst page).
- diff-bug #6: zero forms, function pairs, and 10in/60em run the same code paths — reject, planned change: AC1, AC2, and AC4 name each value after the plan's criteria audit asked for varied forms.
- diff-bug #7: README says `pi` and `none` in `clamp()` warn, with no test — fix now (both added to css-functions).
- diff-bug #8: exponents (`1e2px`), `env()`, an empty `var()` fallback, and non-ASCII property names now warn, and the README does not say so — fix now for the README (exponents, `env()`, empty fallback listed); non-ASCII names — reject, edge: a custom property name outside ASCII is outside documented and common use, and its effect is a warning.
- diff-bug #9: `calc(1px / 0)` passes — follow-up to row "Warn on zero widths in CSS functions".
- diff-bug #10: the media-query pattern reads one level of parentheses — fix now (pattern reads to the `) {` that ends the query).
- diff-bug #11: the Typst wide check ignores the gap — follow-up to row "Count the gap in Typst width checks".
- diff-bug #12: README calls the rule "absolute width" though it covers `em` — fix now (wording).
- diff-bug #13: D-006 covers poppler for LaTeX layout only — reject, false: poppler is already a test requirement and no dependency changes; the work log records the wider use.
- diff-bug #14: about 100k nested parentheses overflow the Lua stack — reject, edge: no document nests that deep, and the effect is a render error.
- blame-history #1: a width plus its gap can exceed the Typst text width (6.4in with 2em, or 99% with 1em) — follow-up to row "Count the gap in Typst width checks".
- blame-history #2: `UNITS` lacks valid CSS units (`dvmin`, `svmax`, `vi`, `vb`, `cap`, `ic`, `rcap`, `rch`, `rex`, `ric`, and others), so `calc(100% - 2dvmin)`, which main passed, now warns — fix now (units added from CSS Values 4).
- blame-history #3: the Typst fallback prints no warning, against the warn-once goal — reject, planned change: the user chose no warning at the question set.
- blame-history #4: `pi`, `round()`, and other newer forms now warn — reject, planned change: the user chose to warn on newer forms.
- blame-history #5: `calc(0%)` passes the zero check — same as diff-bug #2.
- blame-history #6: the media-query pattern reads one level — same as diff-bug #10.
- prior-review #1: the Typst wide width falls back silently, against M005's and M006's warn-on-fallback findings — reject, planned change: the user chose no warning, and the README says so.
- prior-review #2: `cairn/PROFILE.md` line 29 is long — reject, style: the cap counts lines.
- ripple #1, #2, #3: the three candidate rows describe the fixed bugs — reject, planned change: post-merge hygiene graduates them; #3's "lacks the started M010 tag" is false (the row ends with ` — started M010`).
- ripple #4: `cairn/references/wrap-mechanisms.md` shows the old `#context wrap-content(` call and `])` close — fix now.
- ripple #5: PROFILE.md test-doctrine names only the `LAYOUT` list — fix now.
- ripple #6: the W3 row says the blocks make one `wrap-content` call — fix now (with #4).
- ripple #7: the workflow comment names only fixture.pdf — reject, false: the comment says which render fixture.pdf holds, which stays true.
