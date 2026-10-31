<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M043: Prepare the interface and front pages for launch

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the filter's options, its warnings, and the documentation site   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m043-launch-prep   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Before the extension is advertised, its option names, its code-cell options, and its first two pages say what
a new Quarto user needs, and a misnamed document key warns instead of failing silently.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a warning for an unknown key under `wrapped:` (D-027); tests and docs for the `#| width:` and
`#| wrap-gap:` options that a knitr table cell already takes; `#| wrap-gap:` on a knitr figure cell, and a
warning for a figure cell's `#| width:`; the naming rule on the Reference page; the unknown-key rule on the
Document defaults page; a home page and a README with the demo, then a short install and one example line,
and with the limits paragraph moved to the format pages and `docs/normal-layout.qmd`.

**Out:** the v0.3.0 release, which the user declares through `/cairn-release`; Jupyter cells, which CI does
not install, so the docs name knitr (candidate row "Check and tidy code cell options"); a `width` inside a
`#| tbl-cap:` caption block, which stays ignored as the docs say; announcing the extension, which is the
user's act; the repeated four-format wording on pages other than the home page and the README.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [x] AC1: A key under `wrapped:` other than `width`, `gap`, and `breakpoint` prints one warning in each
      format's render of a file. The match is case-sensitive. The warning names the key and the three keys that
      the map takes, and for the key `wrap-gap` it also says to write `gap`. Warnings for several unknown keys
      come in byte order of the key (`Gap` before `alpha`). An unknown key changes no width, gap, or
      breakpoint. A fixture whose header has `wrap-gap`, other unknown keys including `Breakpoint: 900px`, and
      `width: 30%` shows each warning in its HTML and EPUB snapshots, and width 30% with the default gap and
      breakpoint in its HTML snapshot. The render log, read by the key-order check in `tests/verify.py`, shows
      the warnings in that order.
- [x] AC2: A knitr code cell makes one table float that Pandoc writes, as `knitr::kable` does, and that table
      wraps without cell options. With `#| width:` and `#| wrap-gap:`, it wraps at that width and that gap,
      over any `wrapped:` width and gap. The fixture's snapshots show this in HTML, PDF through LaTeX, PDF
      through Typst, and Word, for a wrap class in `#| classes:` and for one in a block at the end of
      `#| tbl-cap:`, under a document `wrapped:` width and gap.
- [x] AC3: A knitr code cell makes one figure that wraps without cell options. With `#| wrap-gap:`, it wraps at
      that gap, over any `wrapped:` gap, and its width still comes from `#| out-width:` or the default. A
      figure cell's `#| width:` changes nothing and prints one warning that names `#| out-width:`. A cell's
      `#| wrap-gap:` below zero takes the default with the warning a figure's gap below zero prints. The
      fixture's snapshots show each case in the four formats, with and without `#| out-width:`.
- [x] AC4: The Get started and Reference pages state the cell options of AC2 and AC3 and say that they are
      tested with knitr cells. No sentence on those two pages says that a code cell table takes the document
      defaults. The Reference page states the naming rule of D-027. The Document defaults page states that a
      key other than the three is ignored with a warning.
- [x] AC5: `docs/index.qmd` keeps its demo box first. Then `docs/index.qmd` and `README.md` each show the
      install command, the `filters:` YAML, and one markdown line with `.wrap-right` before any sentence that
      names a format, a place, or a table kind that does not wrap. The demo box and the Quarto version floor
      are not such sentences. Neither file holds its paragraph that today begins "This version wraps figures
      in HTML output". Each sentence of that paragraph in each file, read one by one, is stated on a page
      under `docs/formats/` or on `docs/normal-layout.qmd`.
- [ ] AC6: `python3 tests/verify.py` passes. `quarto render docs` succeeds. The `verify.yml` workflow passes on
      both CI Quarto versions, and the `docs.yml` workflow passes.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write a fixture (for example `tests/meta-unknown.qmd`) with `wrapped: wrap-gap:` and one other
      unknown key, render it to HTML and EPUB, and see that no warning prints today.
- [x] T2: In `read_meta` (`wrapped.lua`, after `local m = meta.wrapped`), warn once for each unknown key in
      sorted order, naming the three keys, with the `gap` hint for `wrap-gap`. Add the snapshots to
      `tests/verify.py`.
- [x] T3: Add a table-cell fixture (for example `tests/cell-options.qmd`) with `wrapped:` width and gap and
      knitr table cells: class in `#| classes:` with `#| width:` and `#| wrap-gap:`, class in a `#| tbl-cap:`
      block with the same options, and one with no options. Snapshot the four formats and read that the
      summaries carry each width and gap. Extend a summary where it does not show one.
- [x] T4: Make a figure cell read `#| wrap-gap:` from its cell div in `cell_div` or `float_target`, warn on a
      figure cell's `#| width:`, and route a negative cell gap through the existing gap check. Add figure
      cells to the fixture of T3, with and without `#| out-width:`, and update the four snapshots.
- [x] T5: Update `docs/get-started.qmd` ("A figure from a code cell" and "Wrap a table"),
      `docs/reference.qmd` (lines 10 to 18 and the naming rule), and `docs/defaults.qmd` (the unknown-key
      rule). Render the pages with R, since their frozen cells re-run after a prose edit.
- [x] T6: Rewrite `docs/index.qmd` after the demo box and the top of `README.md`: install, the `filters:` YAML,
      one `.wrap-right` line, and a link to Get started. Check each sentence of each limits paragraph against
      `docs/formats/` and `docs/normal-layout.qmd`, and add any sentence that no page states.
- [x] T7: Run `python3 tests/verify.py` and `quarto render docs`, and run the docs layout checks.

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

- 2026-10-31: created by /milestone-plan.
- 2026-10-31: tier check: milestone — a new warning and a new figure-cell option change running code, and the gap names needed a design decision.
- 2026-10-31: idea vet: gap — "let a code-cell table set its own width and gap" already works for knitr tables in all four formats (plan probe), so the reading taken is docs and tests for it; gap — figure cells have no per-cell gap, posed at the set, answered build it; gap — the gap names admit three fixes, posed at the set, answered keep names and warn; no flaw.
- 2026-10-31: plan probe (Quarto 1.10.20, knitr): `#| width: 30%` and `#| wrap-gap: 3em` reach a table cell's div and float and give 30% and 3em in HTML, LaTeX, Typst, and Word; a figure cell ignores both; a `width` in a `#| tbl-cap:` block is ignored; `read_meta` ignores unknown `wrapped:` keys silently.
- 2026-10-31: collision check: no candidate row, open milestone, or D-entry covers these items; inbox sweep found no open issue or PR.
- 2026-10-31: lessons used: 2026-10-27 (M013, used M038), 2026-10-29 (M033, used M040), 2026-10-30 (M038, used M040), 2026-10-28 (M023, used M040), 2026-10-28 (M026, used M041), 2026-10-27 (M012, used M041).
- 2026-10-31: criteria audit (full mode, fresh Opus reader): 12 findings, all accepted and narrowed into AC1 to AC5 — warning once per rendered file, sorted order, case-sensitive, breakpoint unchanged; cell options only for Pandoc tables that wrap without them; class in `#| tbl-cap:` and a document default in the fixture; figure-cell `#| width:` warning and negative gap; the review reads Get started and Reference instead of one phrase search; docs name knitr; Document defaults states the warning; "limit" defined; each file's paragraph checked on its own.
- 2026-10-31: plan gate chose keeping `gap` and warning on an unknown key over accepting both spellings or renaming the key to `wrap-gap`, because the names follow one rule once stated and no user depends on an alias; falsified by user reports of `wrap-gap` under `wrapped:` after the warning ships.
- 2026-10-31: plan gate chose the demo box first, then a short install, over a quick start above the demo, because the demo shows the result before the setup; falsified by visitor feedback that the install is hard to find.
- 2026-10-31: changelog: none (profile changelog slot is "none"; release notes come from commit subjects).
- 2026-10-31: implement started on branch m043-launch-prep, cut from main at cae0f85.
- 2026-10-31: T1-T2 done: `tests/meta-unknown.qmd` (keys `wrap-gap` and `Width`) printed no key warning before the change; `read_meta` now warns once per unknown key in sorted order with the `gap` hint for `wrap-gap`; HTML and EPUB snapshots show both warnings and the 40% and 1em defaults.
- 2026-10-31: T3 done: `tests/cell-options.qmd` (document `wrapped:` 45% and 20px) snapshots show the classes cell at 30%/3em, the caption-block cell at 35%/2em, and the no-option cell at 45%/20px in HTML, LaTeX (`wrappedtable` options), Typst (`wrapped-width` and `column-gutter`), and Word (box width and text distance); the existing summaries already carry each width and gap, so none was extended.
- 2026-10-31: T4 done: knitr puts `width` and `wrap-gap` on the cell div but not on a figure float (dump filter), so `cell_div` carries both and `float_target` takes a figure's gap from the float, then the cell, then the image; a figure cell's `width` warns once naming `out-width`. Snapshots: 2.5em at out-width 30%, 1.5em at the 45% default with no out-width, the width warning with out-width 35% kept, and `-1em` falling back to 20px with the same "not a length or a percent" warning a figure attribute of `-1em` prints, in all four formats.
- 2026-10-31: T5 done: Get started (figure cell `#| wrap-gap:` and the `#| width:` warning; table cell `#| width:` and `#| wrap-gap:`), Reference (cell options, the naming rule, the unknown-key rule), and Document defaults (unknown keys warn; cell options come before the defaults) updated, each naming knitr; `quarto render docs` exit 0 re-ran the frozen get-started cell; `docs_layout.py --no-word` and `--html` (scratch venv, playwright 1.64.0) all ok.
- 2026-10-31: T6 done: the limits paragraph left `docs/index.qmd` (now demo, Install, a "Wrap a figure" line, and links) and `README.md` (now one sentence naming the four formats and `#tbl-` tables); sentence check: slides and dashboards, `#tbl-` tables in four formats, gt and flextable in Word, raw LaTeX tables, and HTML tables tested on pages were already on `formats/html.qmd`, `formats/word.qmd`, `formats/latex.qmd`, and `normal-layout.qmd`; the figure and table sentences for other formats were on no page, so `normal-layout.qmd` gained "Formats that do not wrap" (one warning per document, per the `tables` and `meta-unknown` EPUB snapshots).
- 2026-10-31: T7 done: `python3 tests/verify.py` all 134 renders pass (run at the T4 code state; later commits touch docs only); `quarto render docs` exit 0 after the claim-audit fixes; `docs_layout.py --no-word` and `--html` all ok.
- 2026-10-31: claim audit: 41 claims read, 4 corrected — docs/defaults.qmd, docs/get-started.qmd, docs/index.qmd, README.md (cell options named per cell kind; the width warning only for a wrapped figure cell; examples show figures only; the README's table sentence now points to the site's limits); the reader re-read all 4 as holding.
- 2026-10-31: status review.
- 2026-10-31: review pass 1 merged the follow-up row "Strip code cell options from cell divs" and the plan's "Check code cell options in Jupyter" into "Check and tidy code cell options" (roadmap line cap); the Scope Out item still names the old Jupyter title.
- 2026-10-31: amendment routed: AC1 — diff-bug #3: AC1 asks the EPUB snapshot to show the default width and gap, which an EPUB snapshot never records, so AC1 as written cannot be met; the fixture now has five unknown keys beside `wrap-gap`, not one.
- 2026-10-31: status in-progress for the AC1 amendment.
- 2026-10-31: re-audit: AC1 (full) — 4 findings: the no-effect claim cannot fail while the fixture holds only unknown keys (add a known `width: 30%`); "sorted" names no order (say byte order); the snapshot sorts warnings, so name the key-order check as the order's evidence; the format domain rests on the format-independent loop, no change.
- 2026-10-31: re-audit: AC1 (full) — 2 findings on the revised wording: "one warning per rendered file" reads as per input file, though a two-format run prints each warning once per format (say "in each format's render of a file"); breakpoint has no unknown look-alike key in the fixture (add `Breakpoint: 900px`, or narrow the breakpoint clause to the fixture); byte order confirmed under both C and en_US collation.
- 2026-10-31: at the stop after the second re-audit the user chose to close both gaps; `tests/meta-unknown.qmd` gained `width: 30%` and `Breakpoint: 900px`, and its snapshots show seven key warnings, 30%, 1em, and 576px; the key-order check passes for HTML and EPUB.
- 2026-10-31: amendment return: AC1 — "A key under `wrapped:` other than `width`, `gap`, and `breakpoint` prints one warning in each format's render of a file. The match is case-sensitive. The warning names the key and the three keys that the map takes, and for the key `wrap-gap` it also says to write `gap`. Warnings for several unknown keys come in byte order of the key (`Gap` before `alpha`). An unknown key changes no width, gap, or breakpoint. A fixture whose header has `wrap-gap`, other unknown keys including `Breakpoint: 900px`, and `width: 30%` shows each warning in its HTML and EPUB snapshots, and width 30% with the default gap and breakpoint in its HTML snapshot. The render log, read by the key-order check in `tests/verify.py`, shows the warnings in that order."
- 2026-10-31: substantive amendment: Scope Out names the merged row "Check and tidy code cell options" in place of "Check code cell options in Jupyter"; wording only, the deliverable unchanged.
- 2026-10-31: status review.

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

Review pass 1, 2026-10-31, on `m043-launch-prep` at 67fceb1 (main not moved since cae0f85).

- AC1: `tests/_snapshots/meta-unknown.html.txt` and `.epub.txt` each hold one warning per unknown key (`Width`, `wrap-gap`), the `wrap-gap` one with "Write gap…"; the HTML figure keeps `--wrap-gap: 1em; --wrap-width: 40%` and breakpoint 576px; `read_meta` sorts the keys before warning and compares case-sensitively. Pass.
- AC2: `tests/_snapshots/cell-options.{html,pdf,typst,docx}.txt` under document `wrapped:` 45%/20px: `tbl-cell-opts` (class in `#| classes:`) at 30%/3em and `tbl-cell-cap` (class in the `#| tbl-cap:` block) at 35%/2em in HTML styles, LaTeX `wrappedtable` options, Typst `wrapped-width`/`column-gutter`, and Word box w=2808/3276 with text distance 720/480; `tbl-cell-none` at 45%/20px as the control. Pass.
- AC3: same snapshots: `fig-cell-gap` 2.5em at out-width 30%, `fig-cell-gap-only` 1.5em at the 45% default (no out-width), `fig-cell-width` one "sets width, which a figure cell does not read… out-width" warning with width 35% from out-width and gap 20px, `fig-cell-negative` falls back to 20px with the "not a length or a percent" warning that a `-1em` figure attribute gets (`checked_length`), in all four formats (Word frames w=2808/4212/3276/2808, gap 600/360/300/300). Pass.
- AC4: read `docs/get-started.qmd` and `docs/reference.qmd` whole: cell options at get-started 96-99 and 170-173 and reference 10-16, each naming knitr; the only "document defaults" sentence left (get-started 171-172) says a cell with neither option takes them; the naming rule at reference 43-48; `docs/defaults.qmd` 44-46 states that other keys are ignored with a warning. Pass.
- AC5: `docs/index.qmd`: demo box 11-33, then install (41), `filters:` (48), the `.wrap-right` line (57), and the only no-wrap sentence after it (61-63); `README.md`: install (17), `filters:` (25), example (35), and no sentence before them names a format, place, or table kind that does not wrap (line 7 points to the documented limits); neither file holds "This version wraps". Each old sentence, checked one by one per file, is on `formats/html.qmd` (slides and dashboards, tables tested on pages), `formats/word.qmd` (gt and flextable), `formats/latex.qmd` 96-98 (raw LaTeX tables), or `normal-layout.qmd` (four-format table floats; the new "Formats that do not wrap" for figures and tables elsewhere). Pass.
- AC6 (local part): `python3 tests/verify.py` all 134 renders pass at 67fceb1; `quarto render docs` exit 0 and `docs_layout.py --no-word` and `--html` all ok after the T7 fixes; CI not yet run (no PR). Not ticked.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: AC1's sorted order has no test that can fail, since `summary` sorts warnings — fix now: `tests/meta-unknown.qmd` has six unknown keys and `key_order_check` in `tests/verify.py` reads the render's own order; a planted removal of `table.sort` failed it on 3 of 3 runs.
- diff-bug #2: README line 5 names formats before the install, against AC5 if "that does not wrap" binds only "a table kind" — reject (false): the clause binds all three nouns, as the plan's criteria-audit line defines a limit, and the sentence names formats that wrap.
- diff-bug #3: AC1 asks the EPUB snapshot to show the default width and gap, which an EPUB snapshot never records — amendment routed (AC1 as written cannot be met).
- diff-bug #4: AC3's width-warning and negative-gap cases ran only with `out-width` — fix now: `fig-cell-width-only` and `fig-cell-negative-only` added; both show the warning and the 45% default in four formats.
- diff-bug #5: all evidence is Quarto 1.10.20; on 1.9.36 a figure float could get the cell's `width` — open until CI: `verify.yml` runs the same `cell-options` snapshots on 1.9.36 before merge, and AC6 is not ticked until it passes.
- diff-bug #6: the `cell_div` comment and DESIGN say a figure float gets no cell options, but a `fig-subcap` parent float gets `width` — fix now: both now say a cell's one figure float.
- diff-bug #7: an unclassed cell printing a classed markdown figure with `results: asis` ignores `#| wrap-gap:` — reject (false): the docs give `#| wrap-gap:` for figure cells whose class is in `#| classes:`, and such a markdown figure takes its own `wrap-gap` attribute.
- diff-bug #8: AC4 bars a sentence saying a code cell table takes the document defaults, and get-started 171-172 says a cell with neither option takes them — reject (false): the sentence is conditional and true (`tbl-cell-none` snapshot), while AC4 bars the unconditional claim.
- diff-bug #9: Reference said "and so does a code cell's option", which a figure cell's `#| width:` does not do — fix now: names `#| wrap-gap:`, a figure cell's `#| out-width:`, and a table cell's `#| width:`.
- diff-bug #10: a cell that makes a table and a figure warns that the figure's cell sets width, though the table used it — reject (edge): only a mixed table-and-figure cell reaches it, outside documented use (parked row "Treat mixed table and figure cells"), and the effect is a warning.
- diff-bug #11: the cell div keeps `width` and `wrap-gap` in HTML output — follow-up: parked row "Strip code cell options from cell divs" (predates M043 for table cells; no rendering effect found).
- diff-bug #12: a book with an unknown project key warns once per chapter while the docs say "the render prints a warning" — reject (edge): only a book with a misspelled project key reaches it, and the effect is repeated warnings.
- diff-bug #13: `table.sort` follows the locale, and the key prints unquoted — reject (edge, style): Quarto runs pandoc's Lua with ASCII keys in the C order the check reads, and quoting is style.
- diff-bug #14: only `wrap-gap` gets a hint, not `wrap-lines` — reject (planned change): D-027 names the `wrap-gap` hint alone.
- diff-bug #15: no test-rule violation; no fixture mixes a known and an unknown key — noted (`cell-options.qmd` shows known keys applying, and `read_meta` reads the known keys before the unknown-key loop).
- blame-history #1: a figure whose class sits in its `#| fig-cap:` block gets no cell gap — reject (false): only a table float takes a class from its caption block (`drop_caption_wrap` runs for tables).
- blame-history #2: the table path's probe ran on 1.10.20 only — open until CI, with diff-bug #5.
- blame-history #3: a cell gap now beats the image's own `wrap-gap` — reject (planned change): T4 set the order float, cell, image, and a knitr image carries no `wrap-gap` in documented use.
- blame-history #4: "the extension's tests use knitr cells" is a test note on user pages — reject (planned change): AC4 requires it.
- blame-history #5: the figure-cell width warning sentence overstates its scope — reject (false): the claim audit already narrowed it to "a wrapped figure cell".
- prior-review: no regression of a past review lesson; its notes on the first figure being named in a several-figure cell and on a cell gap counting as the figure's own in Word — noted.
- ripple #1: DESIGN's code cell paragraph omits the cell options — fix now, fixed e17962f.
- ripple #2: DESIGN's `wrapped:` block and pipeline step 1 omit the unknown-key warning — fix now, fixed e17962f.
- snapshot: tests/_snapshots/meta-unknown.html.txt, meta-unknown.epub.txt — new; four more key warnings from diff-bug #1's fix, called for by AC1.
- snapshot: tests/_snapshots/cell-options.{html,pdf,typst,docx}.txt — new; two more figure cells from diff-bug #4's fix, called for by AC3.

Review pass 2, 2026-10-31, on `m043-launch-prep` at 41fbf4b, then 11efc14 (main not moved), after the AC1 amendment return.

- AC1: `python3 tests/verify.py` at 41fbf4b printed "ok order meta-unknown.html: 7 unknown keys in sorted order" and the same for EPUB (the key-order check reads the render log, compared in code-point order, which is byte order for these ASCII keys); `tests/_snapshots/meta-unknown.html.txt` holds each of the seven key warnings once, the `wrap-gap` one with "Write gap…", `--wrap-width: 30%` from the known key, `--wrap-gap: 1em`, and breakpoint 576px despite `Width: 25%`, `Gap: 4`, and `Breakpoint: 900px`; the EPUB snapshot holds the seven key warnings once each beside the format warning; `read_meta` compares names exactly and runs the loop before any format branch. Pass.
- AC2, AC3 (refresh): the pass-1 evidence stands at this head; the suite matched all four `cell-options` snapshots, which now also show `fig-cell-width-only` (warning, 45% default, 20px) and `fig-cell-negative-only` (20px fallback with the warning) in four formats, so each AC3 case runs with and without `#| out-width:`.
- AC4, AC5 (refresh): pass-1 evidence stands; since then only `docs/reference.qmd` 40-42 changed, now naming the cell options per cell kind.
- AC6 (local part): `python3 tests/verify.py` all 134 renders pass at 41fbf4b; `quarto render docs` exit 0 at 11efc14 plus the DESIGN wrap; `docs_layout.py --no-word` 16 ok and `--html` 9 ok. CI waits on the PR; not ticked.
- D-002 check: a by-hand Jupyter render (scratch venv, Quarto 1.10.20, HTML) gave the table cell 30% and 3em, the figure cell gap 2em at the 40% default, and the figure-cell width warning, as knitr does.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the key-order comment holds worked arithmetic (7!) and a stale-prone count — fix now: the comment now says the fixture's several keys seldom match sorted order by chance.
- diff-bug #2: the key-order check runs on EPUB too, on the same code path — reject (planned change): AC1 asks for the order in each format's render.
- diff-bug #3: `fig-cell-negative-only` runs the same fallback path as `fig-cell-negative` — reject (planned change): AC3 asks for each case with and without `#| out-width:`.
- diff-bug #4: `width: 30%` beside `Width: 25%` no longer shows by value that `Width` changes nothing under a case-blind read that prefers the exact key — noted: the snapshot's `Width` warning line still catches case-blind matching, and `Gap` and `Breakpoint` show it by value.
- diff-bug #5: DESIGN line 99 runs to 98 characters, and "sorted order" wording remained — fix now: the line is wrapped; the wording was fixed in 11efc14.
- diff-bug #6: DESIGN's code cell paragraph leaves out the subfigure parent float that the `cell_div` comment names — noted: harmless, the parent keeps its normal layout.
- blame-history #1: defaults.qmd and DESIGN state the cell options with no engine limit, while D-002 asks for one by-hand Jupyter check — fix now: the check ran (D-002 check line above) and the candidate row's Jupyter item is narrowed to the formats left unchecked.
- blame-history #2: the amendment replaced the "default width and gap" clause with `width: 30%` — noted: the user chose it at the stop, and the gap and breakpoint defaults still show.
- blame-history #3: `table.sort` follows the locale — reject (false): the second AC1 re-audit read byte order under both C and en_US, and the suite's order check passed.
- prior-review #1: no recorded plant for the key-order check — reject (false): pass 1's diff-bug #1 line records a planted removal of the sort failing 3 of 3 runs.
- prior-review #2: DESIGN's "a cell's one figure float" sentence and the comment disagree on subfigure parents — reject (false): both say a cell's one figure float gets no options, and the comment adds the parent case.
- prior-review #3: Reference names a table cell's `#| width:` as first with no new case — reject (false): `tbl-cell-opts` shows 30% over the document's 45%.
- prior-review #4: the ROADMAP merge keeps both rows' content — noted.
- ripple #1: the `tests/verify.py` docstring omitted the key-order check — fix now, fixed 11efc14.
- ripple #2: DESIGN pipeline step 1 said "sorted order" — fix now, fixed 11efc14.
- ripple #3: the `read_meta` comment said "sorted order" — fix now, fixed 11efc14.
- snapshot: list unchanged since pass 1 (meta-unknown html and epub, cell-options in four formats, all new files, called for by AC1 and AC3).
- consistency gate: `cairn_validate` all checks pass; the one version marker (`_extensions/wrapped/_extension.yml`, 0.2.0) is unchanged; verify suite green; `docs_layout.py` green on the Mac; the docs workflow runs on the PR; changelog slot "none".
