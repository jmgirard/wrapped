<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M043: Prepare the interface and front pages for launch

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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
not install, so the docs name knitr (candidate row "Check code cell options in Jupyter"); a `width` inside a
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

- [ ] AC1: A key under `wrapped:` other than `width`, `gap`, and `breakpoint` prints one warning per rendered
      file. The match is case-sensitive. The warning names the key and the three keys that the map takes, and
      for the key `wrap-gap` it also says to write `gap`. Warnings for several unknown keys come in sorted key
      order. An unknown key changes no width, gap, or breakpoint. A fixture with `wrap-gap` and one other
      unknown key in its header shows each warning and the default width and gap in its HTML and EPUB
      snapshots.
- [ ] AC2: A knitr code cell makes one table float that Pandoc writes, as `knitr::kable` does, and that table
      wraps without cell options. With `#| width:` and `#| wrap-gap:`, it wraps at that width and that gap,
      over any `wrapped:` width and gap. The fixture's snapshots show this in HTML, PDF through LaTeX, PDF
      through Typst, and Word, for a wrap class in `#| classes:` and for one in a block at the end of
      `#| tbl-cap:`, under a document `wrapped:` width and gap.
- [ ] AC3: A knitr code cell makes one figure that wraps without cell options. With `#| wrap-gap:`, it wraps at
      that gap, over any `wrapped:` gap, and its width still comes from `#| out-width:` or the default. A
      figure cell's `#| width:` changes nothing and prints one warning that names `#| out-width:`. A cell's
      `#| wrap-gap:` below zero takes the default with the warning a figure's gap below zero prints. The
      fixture's snapshots show each case in the four formats, with and without `#| out-width:`.
- [ ] AC4: The Get started and Reference pages state the cell options of AC2 and AC3 and say that they are
      tested with knitr cells. No sentence on those two pages says that a code cell table takes the document
      defaults. The Reference page states the naming rule of D-027. The Document defaults page states that a
      key other than the three is ignored with a warning.
- [ ] AC5: `docs/index.qmd` keeps its demo box first. Then `docs/index.qmd` and `README.md` each show the
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
- [ ] T6: Rewrite `docs/index.qmd` after the demo box and the top of `README.md`: install, the `filters:` YAML,
      one `.wrap-right` line, and a link to Get started. Check each sentence of each limits paragraph against
      `docs/formats/` and `docs/normal-layout.qmd`, and add any sentence that no page states.
- [ ] T7: Run `python3 tests/verify.py` and `quarto render docs`, and run the docs layout checks.

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
