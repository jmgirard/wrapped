# M017: Let slides wrap under margin settings

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes which wrapped figures wrap on revealjs slides and what the render warns
- **Branch/PR:** m017-slides-margin

## Goal

On revealjs slides, a wrapped figure that a margin class or a document
margin value names wraps, because slides have no margin column.

## Scope

**In:** On revealjs slides, `margin_context` in
`_extensions/wrapped/wrapped.lua` names no place for the `column-margin`
and `fig-column-margin` classes (`wrapped.lua:896`). The document's
`fig-column: margin` or `column: margin` reaches the same check through
`read_meta`. An `aside` still names a place, because revealjs sets a
`div.aside` at the slide's foot. Quarto's `renderDivColumn` skips slides,
and its revealjs stylesheet has no `column-margin` rule. The work adds
cases to `tests/revealjs.qmd` and two fixtures,
`tests/revealjs-margin-meta.qmd` with document `fig-column: margin` and
`tests/revealjs-column-margin.qmd` with document `column: margin`. It
updates the README section "Slides" and rows E3 and E15 of
`cairn/references/wrap-mechanisms.md`.

**Out:** A float with its own `.aside` class on a slide keeps the current
rule. No render has shown where revealjs puts it, and no row asks for it.
HTML pages keep every margin rule as it is.

## Acceptance criteria

The snapshots are those that `python3 tests/verify.py` compares. If its
revealjs `# figures` line shows `wrap-right` or `wrap-left`, a figure
**wraps**. If its line reads `<id>: - style=-`, the figure **keeps its
normal layout**. A warning line reads `1x wrapped: the figure #<id>
<reason>, so it does not wrap.`.

- [x] AC1: In the revealjs snapshots, these figures wrap, and no warning
      names them:
  - in `tests/revealjs.qmd`, a float with `.column-margin`, a float with
    `.fig-column-margin`, a float in a `.column-margin` div, a knitr cell
    with `#| column: margin`, and a knitr cell with `#| fig-column: margin`.
  - the float in `tests/revealjs-margin-meta.qmd`.
  - the float in `tests/revealjs-column-margin.qmd`.
- [x] AC2: A float in an `.aside` div, added to `tests/revealjs.qmd`, keeps
      its normal layout with one warning whose reason is `is in an aside`.
- [x] AC3: The README section "Slides" states two facts. A margin class
      or a document margin value does not stop a figure from wrapping on a
      slide. A figure in an aside div does not wrap.
- [ ] AC4: `python3 tests/verify.py` exits 0 locally and in the verify
      workflow on the PR. Against `main`, the change to `tests/_snapshots/`
      adds the snapshot files of the two new fixtures and adds lines to
      `revealjs.revealjs.txt`. It removes or changes no line that is on
      `main`, and it changes no other file.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T2, T4

## Tasks

- [x] T1: Add the cases of AC1 and AC2 to `tests/revealjs.qmd`, each
      followed by a paragraph, and write the two new fixtures. Render a bare
      copy of each and confirm in the HTML that no figure of AC1 sits in an
      element that the revealjs stylesheet moves. Write one work-log line.
- [x] T2: On revealjs, make `margin_context` return no place for
      `column-margin` and `fig-column-margin`, and keep `aside`. Add the
      `tests/verify.py` entries and write the snapshots.
- [x] T3: Update the README section "Slides" and rows E3 and E15 of
      `cairn/references/wrap-mechanisms.md`.
- [x] T4: Run `python3 tests/verify.py` and compare `tests/_snapshots/`
      with `main`.

## Work log

- 2026-10-27: created by /milestone-plan.
- 2026-10-27: tier check: not run — work named at the question set.
- 2026-10-27: question set: which work to take — the three margin follow-up rows; this milestone holds "Let slides wrap under margin settings".
- 2026-10-27: idea vet: no concern. Quarto 1.10.19's revealjs stylesheet has no `column-margin` rule and `renderDivColumn` skips slides, so a margin figure stays in the slide's text, and a scratch render (criteria audit) warned for each margin form on a slide.
- 2026-10-27: split from the one-milestone draft with M016 and M018. Each ships alone.
- 2026-10-27: criteria audit (full mode, on the one-milestone draft): the slide criterion covered 4 of the 7 margin forms. Fixed by adding own `.fig-column-margin`, a cell with `#| fig-column: margin`, and a document `column: margin`. A float's own `.aside` class went to Out. The note that a figure that keeps its normal layout renders as an `img` on a slide needs no change: AC2's aside case renders as a div.
- 2026-10-27: lessons used: 2026-10-27 (M015) render without filters before trusting a placement.
- 2026-10-28: started; branch m017-slides-margin cut from main at 90c287a.
- 2026-10-28: T1 bare render (Quarto 1.10.19, filters removed): every AC1 figure sits in the slide's section, `fig-slide-margin-div` in a `div.column-margin`; no file under the revealjs libs names `column-margin`; `fig-slide-aside` sits in an `aside`, which the theme sets `position:absolute; bottom:20px`.
- 2026-10-28: T2 choice: a module-level `is_revealjs` flag, also used by `has_page_layout`; `margin_context` skips the two margin classes when it is set.
- 2026-10-28: checkpoint, half-done: T1–T3 edits on disk, T1/T2 unchecked until `verify.py --update` finishes and the snapshot diff is read.
- 2026-10-28: T1–T3 done: `verify.py --update` passed all 97 renders; the revealjs snapshot gains only added lines, the five AC1 figures wrap and `fig-slide-aside` warns `is in an aside`. With main's filter all seven AC1 figures warn `is in the margin`, so the fixtures fail on main.
- 2026-10-28: claim audit: 19 claims read, 3 corrected — README.md, _extensions/wrapped/wrapped.lua, tests/revealjs.qmd (the aside sits at the slide's foot only by default: `center: true` and `.scrollable` slides place it otherwise; the reader re-read the three narrowed lines and all hold).
- 2026-10-28: T4 run 1: `python3 tests/verify.py` passed all 97 renders; against main the snapshots add revealjs-margin-meta and revealjs-column-margin (9 lines each) and 18 lines to revealjs.revealjs.txt, with no line removed. The three audit edits landed during that run, so a second run checks the final head.
- 2026-10-28: T4 run 2 at b88687f: `python3 tests/verify.py` passed all 97 renders, no FAIL line. Status set to review.

## Decisions

## Review

Evidence gathered 2026-10-28 at aaf6f5c (Quarto 1.10.19). Fresh `python3 tests/verify.py`: all 97 renders pass, no FAIL line; `revealjs.revealjs`, `revealjs-margin-meta.revealjs`, `revealjs-column-margin.revealjs` each `ok`.

- AC1: `revealjs.revealjs.txt` reads `wrap-right` for fig-slide-margin, fig-slide-figmargin, fig-slide-margin-div, fig-slide-margin-cell, fig-slide-figmargin-cell; `revealjs-margin-meta.revealjs.txt` for fig-slide-meta-margin; `revealjs-column-margin.revealjs.txt` for fig-slide-col-margin. The two new snapshots have empty `# warnings`, and the one warning in `revealjs.revealjs.txt` names fig-slide-aside only. With main's filter all seven warned `is in the margin` (work log, T1–T3). Pass.
- AC2: `revealjs.revealjs.txt` reads `fig-slide-aside: - style=-` and holds exactly one warning, `1x wrapped: the figure #fig-slide-aside is in an aside, so it does not wrap.` Pass.
- AC3: README.md section "Slides" (read at aaf6f5c) says "A margin setting does not stop a figure from wrapping on a slide either", naming the two margin classes, the margin div, both margin cell options, and `fig-column: margin` and `column: margin` in the document metadata, and says "A figure in an aside div does not wrap." Both facts stated. Pass.
- Gate: `cairn_validate.py` exit 0, all checks passed. Profile gate: the one version marker (`_extension.yml` `version: 0.1.0`) is unchanged on the branch; verify passes (above); changelog slot "none", no entry read. Pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the captioned image with no id and the bare image with `.column-margin` on a slide (own_margin and the find_contexts Image handler) changed behavior with no fixture — fix now: two cases added to `tests/revealjs.qmd`; both wrap, and main's filter warns `is in the margin` for both, fixed 372263a, 6fee163.
- diff-bug #2: README "Where a figure keeps its normal layout" says the margin item holds "In HTML" with no slide exception, while README line 7 counts slides as HTML — fix now: the margin item points to "Slides", fixed 372263a.
- diff-bug #3: with `center: true` or on a `.scrollable` slide the aside sits in the slide's text, yet a figure there still falls back with a warning — follow-up: candidate row "Let asides wrap on centered slides".
- diff-bug #4: DESIGN.md steps 2 and 4 and the wrapped.lua comments above `has_page_layout` and `find_contexts` miss the slide margin rule — fix now, fixed 372263a.
- diff-bug #5: `is_revealjs` covers revealjs only, but Quarto's `renderDivColumn` skips every HTML slide format (slidy, s5, dzslides, slideous) — follow-up: candidate row "Check margins in slidy and other slides" (predates the branch; the README claims revealjs only).
- diff-bug #6: `revealjs-column-margin.qmd` runs the same code path as `revealjs-margin-meta.qmd` on revealjs — reject (planned change): AC1 names both fixtures.
- diff-bug #7: the `.column-margin`/`.fig-column-margin` and `column`/`fig-column` margin pairs in `tests/revealjs.qmd` are near duplicates — reject (planned change): AC1 names all four.
- diff-bug #8: the two knitr cells make `tests/revealjs.qmd` need R — reject (planned change): AC1 names knitr cells in that fixture, and CI installs R (D-009).
- blame-history #1: DESIGN.md steps 2 and 4 stale for slides — fix now (same fix as diff-bug #4), fixed 372263a.
- blame-history #2: README fallback list has no slide exception for the margin item — fix now (same fix as diff-bug #2), fixed 372263a.
- blame-history #3: the comment above `has_page_layout` omits the margin column — fix now (same fix as diff-bug #4), fixed 372263a.
- blame-history #4: no D-entry for the slide margin rule — reject (false): no D-entry is owed; the change applies M013's rule that slides lack the page layout, and DESIGN and the README record the behavior.
- prior-review #1: the change reverses M013's "slide fallbacks" fix — reject (false): M013 diff-bug #2 stopped the page-wide and margin-caption fallbacks firing on slides, the same direction as this change.
- prior-review #2: the Quarto 1.10.19 stylesheet claims may lack a source — reject (false): the claim audit read the deck's CSS files and quarto.scss for both claims (work log).
- prior-review #3: E3 has been edited by two earlier fixes — reject (false): the reviewer found the text consistent with the code, and no defect is named.
- ripple #1: README fallback list's margin item contradicts "Slides" — fix now (same fix as diff-bug #2), fixed 372263a.
- ripple #2: wrap-mechanisms.md E21 says a margin value keeps the figure normal in every format where it decides, and HTML reads an own margin class first — fix now: E21 notes slides, fixed 372263a.
- ripple #3: DESIGN.md step 2 — fix now (same fix as diff-bug #4), fixed 372263a.
- ripple #4: DESIGN.md step 4 — fix now (same fix as diff-bug #4), fixed 372263a.
- ripple #5: ROADMAP row "Let slides wrap under margin settings" still states the old behavior — reject (planned change): post-merge hygiene graduates that row.
- ripple #6: the `column_context` comment says HTML reads an own margin class — reject (false): it states the read order, which holds on slides; `margin_context`'s comment states that the classes name no place there.
- ripple #7: the `find_contexts` comment says an image with its own margin class is in the margin — fix now (same fix as diff-bug #4), fixed 372263a.
- ripple #8: the file header names the margin as a context, "such as a list or the margin" — reject (false): it gives examples of contexts, and the format limits sit at `margin_context` and `page_context`, as for page-wide columns.
- ripple #9: the comment at wrapped.lua:1339 says a column class "can put the float in the margin" — reject (false): "can" holds in the formats with a margin.
- ripple #10: ROADMAP row "Warn once per cell under a context" says a document margin value prints one warning per figure — reject (false): the row covers the formats where the value names a context.
- ripple #11: `tests/margin-meta.qmd` prose says the float keeps its normal layout in every format — reject (false): that fixture renders html, pdf, typst, and docx only.
- Note: the diff-bug reviewer's render showed Quarto moves a float with its own `.aside` class into an `<aside>` after the slide's paragraphs, so the Out item's "No render has shown where revealjs puts it" is out of date; the rule it keeps (warn `is in an aside`) is the one that render supports. No change.
