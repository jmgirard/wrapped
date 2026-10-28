<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M023: Build the documentation site

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the documentation that users read, published by M024   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m023-docs-site   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A Quarto website in `docs/` carries all of the documentation as topic pages, with a gallery of examples rendered in HTML, PDF through LaTeX, PDF through Typst, and Word.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**

- A website project in `docs/`: `_quarto.yml` with a navbar and a sidebar,
  `filters: - wrapped`, `execute: freeze: auto` with `docs/_freeze/`
  committed, an `_extensions` symlink to `../_extensions` (as in `tests/`),
  and `docs/_site/` and `docs/.quarto/` ignored.
- Topic pages that carry every rule of `README.md` (user's choice: keep
  every rule). Each page leads with the common case: home, getting started
  (install and the four figure forms), width and gap, document defaults,
  where wrapping stops, where a figure keeps its normal layout, one page each
  for HTML (with slides and dashboards), PDF through LaTeX, PDF through
  Typst, and Word, and a reference table. A fallback case is shown on its
  topic page, never in the gallery.
- An examples gallery in `docs/examples/`: an index and one page per
  example, each rendered as HTML with "Other Formats" links to the LaTeX
  PDF, the Typst PDF (its own `output-file`, so that it does not overwrite
  the LaTeX PDF), and the Word file. One example uses a frozen knitr code
  cell. A revealjs page and a dashboard page join the gallery.
- `.github/workflows/docs.yml`: renders the site on pull requests.

**Out:**

- Publishing the site, the `gh-pages` branch, the Pages setting, and the
  short README → M024. The README stays as it is here, so nothing reaches
  users before M024.
- Examples of setups the README calls untested, such as dashboard sidebars
  → the candidate rows that hold them.
- A changelog entry: the profile's changelog slot says none.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: From a clean checkout of the branch head, `quarto render docs`
      with Quarto 1.10.19 exits 0 with no `R` or `Rscript` on `PATH`,
      because code-cell results come from the committed `docs/_freeze/`.
      `.github/workflows/docs.yml` runs that command on each pull request
      that changes `docs/`, `_extensions/`, or the workflow file, and it has
      no step that installs R.
- [ ] AC2: An example page is a `.qmd` file in `docs/examples/` other than
      `index.qmd`, `slides.qmd`, and `dashboard.qmd`. After
      `quarto render docs`, the HTML of each example page lists PDF, Typst,
      and MS Word links under "Other Formats", and each linked file exists
      under `docs/_site/examples/`. `pdfinfo` reports a LaTeX producer for
      the file of the PDF link and Typst for the file of the Typst link.
- [ ] AC3: Every wrapped figure in the gallery wraps. The domain is each
      element that `tests/layout.js` lists as a wrapped figure in the HTML of
      each page in `docs/examples/`, the slides and dashboard pages
      included. At a 1280x900 viewport, `tests/layout.js` reports each one
      with `float` `left` or `right`. For each example page, a page image of
      its LaTeX PDF, its Typst PDF, and its Word file (as a PDF that
      LibreOffice makes) shows body text beside each of those figures.
- [ ] AC4: The site carries each rule that `README.md` states at the
      branch's base commit. The domain is each block of the README as
      `quarto pandoc -t json` parses it, the opening lines included: each
      paragraph, each list item, and each code block. For each block, a site
      page states the same rule with the same meaning, or shows the same
      syntax for a code block.
- [ ] AC5: `docs/reference.qmd` has one table row for each of nine names:
      the classes `.wrap-right`, `.wrap-left`, and `.wrap-clear`, the
      attributes `width`, `wrap-gap`, and `wrap-lines`, and the `wrapped:`
      keys `width`, `gap`, and `breakpoint`. Each row gives the values, the
      default, and the formats where the name works, as the topic page that
      covers the name states them.
- [ ] AC6: The install does not change. In an empty folder,
      `quarto add <zip> --no-prompt`, run on a `git archive --format=zip` of
      the branch head, installs `_extensions/wrapped/` with the same file
      list as `main` and no other extension.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6, T8
- AC2 → T6
- AC3 → T6, T9
- AC4 → T2, T3, T4, T5, T9
- AC5 → T7
- AC6 → T1, T9

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Scaffold `docs/`: `_quarto.yml`, the `_extensions` symlink,
      `docs/.gitignore`, example images in `docs/images/`, and a stub home
      page. Render it, and confirm that `tests/verify.py` does not pick up
      `docs/` and that `quarto add` on a `git archive` zip still finds one
      extension (the `tests/_extensions` symlink is the precedent).
- [x] T2: Write the home page (what the filter does, which formats wrap,
      install, one live wrapped figure) and the getting-started page (the
      README's "Install" and "Wrap a figure" sections, each form shown live).
- [x] T3: Write the pages for width and gap (the CSS function check last,
      under its own heading), document defaults, and where wrapping stops,
      each with live examples of the common case.
- [ ] T4: Write the page on where a figure keeps its normal layout, with the
      README's "Notes" placed on their topic pages. Show at least one
      fallback case live, with its warning text.
- [ ] T5: Write the format pages: HTML with slides and dashboards, PDF
      through LaTeX, PDF through Typst, and Word.
- [ ] T6: Build the gallery: `docs/examples/index.qmd`, the example pages in
      four formats (image, div, uncaptioned image, code cell with
      `freeze`, left and right sides, width and gap, document defaults,
      `wrap-clear`), `slides.qmd`, and `dashboard.qmd`. Commit
      `docs/_freeze/`.
- [ ] T7: Write `docs/reference.qmd` with the nine-row table and links to
      the topic pages.
- [ ] T8: Add `.github/workflows/docs.yml`: checkout, Quarto release with
      TinyTeX through `quarto-dev/quarto-actions/setup`, and
      `quarto render docs`, on pull requests that change `docs/`,
      `_extensions/`, or the workflow, and by hand.
- [ ] T9: Checks for review: render with R off `PATH`; build the README
      block ledger (each Pandoc block → site page and heading) in this file;
      measure the gallery's HTML with `tests/layout.js` (lessons M020, M022);
      make page images with `pdftoppm` and, for Word, LibreOffice (D-005),
      and record one line for each figure and format in the Review section.

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

- 2026-10-28: created by /milestone-plan.
- 2026-10-28: tier check: milestone — new docs site, a CI workflow, and a publish change, more than one sitting.
- 2026-10-28: idea vet: one concern, that the README is long because it records every edge case, so a site moves the length rather than cutting it; the user chose to keep every rule, split by topic. Framing note: the "pkgdown site" is GitHub Pages building README.md with Jekyll from main's root.
- 2026-10-28: lessons used: 2026-10-25 (M002) `_extensions` symlink and Typst PNG; 2026-10-25 (M004) LaTeX and Typst both write the same PDF; 2026-10-28 (M020) browser pane viewport for `tests/layout.js`; 2026-10-28 (M022) browser pane CSS cache.
- 2026-10-28: feature series: M023 -> M024
- 2026-10-28: collision check: no milestone, candidate row, or D-entry covers a docs site; no open issue or PR (inbox sweep: 0 issues, 0 PRs).
- 2026-10-28: scratch check: a Quarto 1.10.19 website page with html, pdf, typst (renamed output file), and docx renders with the filter and shows "Other Formats" links; revealjs and dashboard pages render in the site.
- 2026-10-28: question set: doc structure — site in docs/ plus a short README; detail — keep every rule; other formats — "Other Formats" download links; publishing — allowed (applies to M024).
- 2026-10-28: plan gate chose a Quarto website over a short README with committed example outputs because GitHub shows committed HTML as source; falsified by GitHub rendering committed HTML pages.
- 2026-10-28: plan gate chose CI-rendered download links over committed page images because images go stale when the filter changes; falsified by users asking to see PDF or Word pages without a download.
- 2026-10-28: plan chose `freeze: auto` with committed `docs/_freeze/` over installing R in the docs workflow, so the docs job stays short; falsified by a frozen page that renders differently from a fresh run with R.
- 2026-10-28: plan split M023 (build) from M024 (publish and README) because one milestone held about 14 tasks; M023 reaches no user, so the README stays whole until the site is live.
- 2026-10-28: criteria audit (full): 7 findings, all taken except one. AC1 narrowed to a local render with R off PATH; AC2 gained the `pdfinfo` producer check; AC3 domain moved to `tests/layout.js` figures, fallbacks kept off the gallery, ledger moved to T9; AC4 domain moved to Pandoc blocks with the opening lines, ledger moved to T9; AC5 pinned to nine names; AC6 gained `--no-prompt`. The M024 live-site finding is answered by M024's tasks and the user's publish permission; the DESIGN.md "README states" finding went to M024.
- 2026-10-28: implement started on m023-docs-site, cut from main at b7e62a3.
- 2026-10-28: T1 done: `docs/` website with navbar and docked sidebar, stub pages, `freeze: auto`, `_extensions` symlink, and three images from `docs/images/make-images.R` (ragg, 144 dpi). `quarto render docs` exits 0; `tests/verify.py` lists its fixtures by name, so it does not read `docs/`; `quarto add` on `git archive` zips of the branch and of main installs the same 13 paths. A stray `git stash -u` moved the uncommitted work off disk for one command; `git stash pop` restored it.
- 2026-10-28: T2 done: home page (what the filter does, formats, a live wrapped figure, install) and get-started page (Install and Wrap a figure, each form shown as source then as a live `.demo` result framed by `docs/styles.css`). The code-cell form runs once with `echo: fenced` and is frozen in `docs/_freeze/get-started/`. In the browser at 1280x900 all four figures float (fig-ratings, fig-groups, the badge image, fig-scatter).
- 2026-10-28: T3 done: width-gap, defaults, and stopping pages carry README sections "Width and gap", "Document defaults", and "Where wrapping stops", plus the Notes item on values that are not lengths. Shortcodes in prose are escaped as `{{{< >}}}`. The defaults page sets `wrapped: width: 25%, gap: 30px` in its own YAML, and its figure measured 186px (25% of the 744px demo column) with a 30px margin; the list and `wrap-clear` demos start below their figures.
- 2026-10-28: implement chose to edit tracking files with Edit from here on; the T2 tick went in through a python script, against the rulebook's file-edit rule.

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
