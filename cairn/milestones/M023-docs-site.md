<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M023: Build the documentation site

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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

- [x] AC1: From a clean checkout of the branch head, `quarto render docs`
      with Quarto 1.10.19 exits 0 with no `R` or `Rscript` on `PATH`,
      because code-cell results come from the committed `docs/_freeze/`.
      `.github/workflows/docs.yml` runs that command on each pull request
      that changes `docs/`, `_extensions/`, or the workflow file, and it has
      no step that installs R.
- [x] AC2: An example page is a `.qmd` file in `docs/examples/` other than
      `index.qmd`, `slides.qmd`, and `dashboard.qmd`. After
      `quarto render docs`, the HTML of each example page lists PDF, Typst,
      and MS Word links under "Other Formats", and each linked file exists
      under `docs/_site/examples/`. `pdfinfo` reports a LaTeX producer for
      the file of the PDF link and Typst for the file of the Typst link.
- [x] AC3: Every wrapped figure in the gallery wraps. The domain is each
      element that `tests/layout.js` lists as a wrapped figure in the HTML of
      each page in `docs/examples/`, the slides and dashboard pages
      included. At a 1280x900 viewport, `tests/layout.js` reports each one
      with `float` `left` or `right`. For each example page, a page image of
      its LaTeX PDF, its Typst PDF, and its Word file (as a PDF that
      LibreOffice makes) shows body text beside each of those figures.
- [x] AC4: The site carries each rule that `README.md` states at the
      branch's base commit. The domain is each block of the README as
      `quarto pandoc -t json` parses it, the opening lines included: each
      paragraph, each list item, and each code block. For each block, a site
      page states the same rule with the same meaning, or shows the same
      syntax for a code block.
- [x] AC5: `docs/reference.qmd` has one table row for each of nine names:
      the classes `.wrap-right`, `.wrap-left`, and `.wrap-clear`, the
      attributes `width`, `wrap-gap`, and `wrap-lines`, and the `wrapped:`
      keys `width`, `gap`, and `breakpoint`. Each row gives the values, the
      default, and the formats where the name works, as the topic page that
      covers the name states them.
- [x] AC6: The install does not change. In an empty folder,
      `quarto add <zip> --no-prompt`, run on a `git archive --format=zip` of
      the branch head, installs `_extensions/wrapped/` with the same file
      list as `main` and no other extension.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6, T8, T10
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

- [x] T1: Scaffold `docs/` (`_quarto.yml`, `_extensions` symlink,
      `.gitignore`, images, stub home); check that `tests/verify.py` skips
      `docs/` and `quarto add` on a `git archive` zip finds one extension.
- [x] T2: Home page and getting-started page (README "Install" and "Wrap a
      figure"), each form shown live.
- [x] T3: Width-and-gap (CSS function check last), document-defaults, and
      stopping pages, with live examples of the common case.
- [x] T4: Normal-layout page with the README "Notes" placed by topic and one
      live fallback with its warning text.
- [x] T5: Format pages: HTML with slides and dashboards, LaTeX, Typst, Word.
- [x] T6: Gallery: index, eight example pages in four formats (one frozen
      code cell), `slides.qmd`, `dashboard.qmd`; commit `docs/_freeze/`.
- [x] T7: `docs/reference.qmd` with the nine-row table and topic links.
- [x] T8: `.github/workflows/docs.yml`: Quarto release with TinyTeX through
      `quarto-dev/quarto-actions/setup`, then `quarto render docs`.
- [x] T9: Review checks: render with R off `PATH`; README block ledger;
      `tests/layout.js` on the gallery (lessons M020, M022); page images
      with `pdftoppm` and LibreOffice for Word (D-005).
- [x] T10: Review return 1: `docs.yml` on every pull request that changes
      its paths and on pushes to main, PR-only cancel, re-freeze note;
      DESIGN.md and PROFILE.md lines; width-gap, reference, `.gitattributes`,
      and make-images.R fixes.

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
- 2026-10-28: T4 done: normal-layout page carries README "Where a figure keeps its normal layout" and the Notes items (no-id images, linked images, right-to-left sides, long captions, margin content; the non-length item went to width-gap). A live callout fallback shows the warning text copied from the render, `(W) wrapped: the figure #fig-callout is in a callout, so it does not wrap.`; it is the one warning in the full site render. The filter's warnings start with `(W)`, so a grep for "warn" misses them.
- 2026-10-28: T5 done: format pages for HTML (with the README's "Slides" and "Dashboards" sections), PDF through LaTeX, PDF through Typst, and Word carry the README's format sections under task headings; the HTML page adds a short lead that links to the breakpoint, CSS functions, and normal-layout pages. The site render still prints only the callout warning.
- 2026-10-28: T6 done: gallery `docs/examples/` with a table listing and ten pages (image, div, uncaptioned image, knitr code cell with `fig-format: png`, both sides, width and gap, document defaults, `wrap-clear`, slides, dashboard). The eight example pages render to HTML, LaTeX PDF, Typst PDF (`<name>-typst.pdf`), and docx; `docs/_freeze/examples/code-cell/` holds all four formats' results. In the browser at 1280x900, `tests/layout.js` (copied into `docs/_site/` to serve it same-origin) reports each of the 11 gallery figures with `float` on its side; the slides page's one group check is false because the block after the group is on a hidden slide, and a look at the slide shows the text beside the figure.
- 2026-10-28: found and fixed: knitr ran the ```` ```{r} ```` cell inside a four-backtick `markdown` fence on `formats/html.qmd`, so the page showed knitr's output; the fence now writes ```` ```{{r}} ````, which knitr prints as `{r}`, and the stray `docs/_freeze/formats/` is gone.
- 2026-10-28: T7 done: `docs/reference.qmd` has two tables, six rows for classes and attributes and three for `wrapped:` keys, each with values, default, and formats, linked to its topic page. A script over the 22 rendered pages found every internal link and anchor in `<main>` resolves.
- 2026-10-28: T8 done: `.github/workflows/docs.yml` runs `quarto render docs` with `quarto-dev/quarto-actions/setup@v2` (release, TinyTeX) on pull requests to main that change `docs/**`, `_extensions/**`, or the workflow, and by hand; no R step. A clean clone at e0eada0 rendered with a PATH of symlinked quarto, python3, LaTeX, and pandoc plus system and TeX dirs, where `command -v R` and `command -v Rscript` found nothing: exit 0, one `(W)` line (the callout).
- 2026-10-28: T9 README ledger: a script parses `README.md` at main with `quarto pandoc -t json` into 133 blocks (paragraphs, list items, code blocks, opening lines included) and finds 115 verbatim in a `docs/**/*.qmd` page. The 18 others were matched by hand: the three form lead-ins and the code-cell lead-in became get-started headings plus text; the get-started cell (`echo: fenced`) and the dashboard cell (written `{{r}}`) show the same source; "see Word below", "checked as above", "see below", "see “Slides”", "see “Dashboards”", "the next section", and "this section" became links or "this page"; "Tagged PDF:" lead-ins became headings; the stopping and shortcode paragraphs were split at their topic seams. No rule was dropped or changed.
- 2026-10-28: T9 page images (pdftoppm, 40 dpi; Word via `soffice --headless --convert-to pdf`, D-005): body text sits beside each of the 9 figures of the 8 example pages in the LaTeX PDF, the Typst PDF, and the Word file (image-figure, div-figure, uncaptioned-image, code-cell, both-sides x2, width-gap, defaults, wrap-clear); `pdfinfo` gives Producer LuaTeX-1.24.0 for each `<name>.pdf` and Creator Typst 0.15.1 for each `<name>-typst.pdf`. The width-gap source line ran past the LaTeX margin; its caption is now "Mean ratings." and the line fits.
- 2026-10-28: minor amendment: T9's per-figure ledger is in the work log above, not the Review section, which review owns; review regenerates its evidence.
- 2026-10-28: claim audit: 190 claims read, 7 corrected — docs/examples/div-figure.qmd, docs/get-started.qmd, docs/reference.qmd (two), docs/examples/uncaptioned-image.qmd, docs/index.qmd, docs/normal-layout.qmd. The div-caption claims said a div caption holds markdown an image caption cannot (a render showed both hold emphasis, links, and citations); the `wrap-gap` row omitted percents; the units note named `wrap-lines`; the alt-text claim ignored untagged PDFs; "every format" and "in every format" named four. The dashboard source card also gained its missing third paragraph. The same reader re-read the eight changes and found none still wrong.
- 2026-10-28: `python3 tests/verify.py` passes (all 103 renders) on the branch; the filter is unchanged.
- 2026-10-28: implement done; status review.
- 2026-10-28: review return 1: AC1 fails as written, since `docs.yml` limits pull requests to `branches: [main]` (diff-bug #3); the return also carries the review's fix-now items (diff-bug #1, #2, #5–#9, blame-history #1–#2, ripple #1).
- 2026-10-28: minor amendment: T10 added for review return 1, Coverage AC1 → T1, T6, T8, T10.
- 2026-10-28: T10 done: `docs.yml` now runs on every pull request that changes its paths (no branch filter), on pushes to main with the same paths, and by hand; only pull-request runs cancel; its header says to re-render with R and commit `docs/_freeze/` after editing a page with a code cell (Ruby's YAML parser reads the three triggers and the concurrency expression). DESIGN.md Conventions gained the docs-site line, PROFILE.md's verify slot names `docs.yml`, the width-gap example notes the HTML breakpoint, width-gap.qmd links the LaTeX, Typst, and Word pages, the reference `width` row names `20em` and per-format units, `.gitattributes` marks `docs/_freeze/**` generated (`git check-attr` confirms), and make-images.R names ragg. Site render: one `(W)` line; 22 pages, all links resolve.
- 2026-10-28: the T10 commit b73cdf3 broke two caps (PROFILE.md 120 lines, this file 154 plan-owned lines), caught by `cairn_validate` after the commit; PROFILE.md's new note is now one line (119) and the Tasks section was compressed in one rewrite; validate passes.
- 2026-10-28: `python3 tests/verify.py` on 9d81552: all 103 renders pass. Implement done after return 1; status review.


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

Review head 95ea977, main b7e62a3 (unmoved since the cut). Copilot round off.

- AC1: fresh clone at 95ea977, Quarto 1.10.19, PATH of symlinked quarto, python3, pdflatex, lualatex, and pandoc plus system and TeX dirs; `command -v R` and `command -v Rscript` print nothing; `quarto render docs` exit 0, one `(W)` line (fig-callout, intended). `docs.yml`: `pull_request` to main with paths `docs/**`, `_extensions/**`, `.github/workflows/docs.yml`, plus `workflow_dispatch`; its one `run:` is `quarto render docs`; no step names R, setup-r, or Rscript. Pass.
- AC2: `ls docs/examples/*.qmd` less index, slides, and dashboard gives 8 example pages (both-sides, code-cell, defaults, div-figure, image-figure, uncaptioned-image, width-gap, wrap-clear). In the clone's render each page's "Other Formats" block holds PDF → `<name>.pdf`, Typst → `<name>-typst.pdf`, MS Word → `<name>.docx`, and all 24 files exist in `docs/_site/examples/`. `pdfinfo`: each PDF-link file reports Producer LuaTeX-1.24.0 (Creator "LaTeX via pandoc"); each Typst-link file reports Creator Typst 0.15.1 and no Producer line. Pass.
- AC3: the clone's `_site` served at :8792 with `tests/layout.js` beside it; at a 1280x900 viewport `report().figures` lists 11 figures across 10 pages (image-figure fig-ratings, div-figure fig-groups, uncaptioned-image badge, code-cell fig-cars, both-sides fig-right and fig-left, width-gap fig-ratings, defaults fig-ratings, wrap-clear fig-ratings, slides fig-ratings, dashboard fig-ratings; index none), each with `float` equal to its side. Page images (pdftoppm 40 dpi; Word through `soffice --headless --convert-to pdf`) of the 8 example pages' LaTeX PDF, Typst PDF, and Word file, 26 images with both-sides' and code-cell's second LaTeX pages, show body text beside each of the 9 figures in each of the 3 formats. Pass.
- AC4: the ledger script (`quarto pandoc -t json` of `git show main:README.md`; every Para, Plain, list item, and CodeBlock, opening lines included) finds 133 blocks, 115 verbatim in `docs/**/*.qmd` at 95ea977. Each of the other 18 was found by its rule sentence or heading: stopping.qmd (4 blocks: stop rule, shortcodes, no-paragraph figure, two in a row), defaults.qmd (rules for the keys, "checked as on" link), width-gap.qmd (gap paragraph with a Word link), normal-layout.qmd (margin item, dashboard item, multi-figure cell, no-id image note), formats/latex.qmd (intro with a Columns link, Tagged PDF), formats/typst.qmd (Tagged PDF), get-started.qmd (three form headings, code-cell lead, the fenced cell's source), formats/html.qmd (dashboard cell written `{{r}}`, rendered as `{r}`). Each states the README rule with a cross-reference turned into a link or a lead-in turned into a heading; none drops or changes a rule. Pass.
- AC5: the clone's `reference.html` has a six-row table (`.wrap-right`, `.wrap-left`, `.wrap-clear` classes; `width`, `wrap-gap`, `wrap-lines` attributes) and a three-row table (`wrapped:` keys `width`, `gap`, `breakpoint`): nine rows, one per name, each with values, default, and formats. Read against the topic pages: width (percent or absolute length, CSS functions in HTML, default 40%), wrap-gap (default `1em`, percents handled on the Word and Typst pages), wrap-lines (LaTeX only, counted from the height without it), `.wrap-clear` (works in all four formats, stopping.qmd), breakpoint (HTML media query, no percent or `var()`, default `576px`); each row matches. Pass.
- AC6: `git archive --format=zip HEAD` of the clone (95ea977) and of origin/main, each run through `quarto add <zip> --no-prompt` in an empty folder: exit 0, `_extensions/` holds only `wrapped`, and `find _extensions -type f` lists the same 9 files for both. Pass.
- Gate: `cairn_validate.py` exit 0, all checks passed; no DESIGN.md principle changed, so no `cairn_impact` run. Profile gate: the one version marker (`_extensions/wrapped/_extension.yml`) reads 0.2.0 on the branch and on main; `python3 tests/verify.py` on the 95ea977 tree: all 103 renders pass, exit 0; changelog slot "none", no entry read.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: editing prose in get-started.qmd or examples/code-cell.qmd changes the freeze hash, so the R-less docs job fails, and nothing says to re-render with R and commit `_freeze` — fix now
- diff-bug #2: DESIGN.md Conventions names only verify.yml and not docs.yml, `docs/_freeze/`, or the re-freeze rule — fix now
- diff-bug #3: `docs.yml` `branches: [main]` runs only on PRs into main, so AC1's "each pull request that changes `docs/` …" fails for a PR into another branch — fix now; AC1 fails as written, so review return 1
- diff-bug #4: `version: release` floats while the docs name 1.10.19 — reject, planned change (the docs job copies verify.yml's setup, D-008)
- diff-bug #5: examples/width-gap.qmd "2.5 inches wide in every format" ignores the HTML breakpoint — fix now
- diff-bug #6: width-gap.qmd's "format pages" link goes to formats/html.qmd, which has no unit rules — fix now
- diff-bug #7: reference.qmd `width` Values cell leaves out `em` and other lengths the format pages accept — fix now
- diff-bug #8: about 9,000 lines of `docs/_freeze/site_libs` JS carry no `linguist-generated` mark, so GitHub's language bar skews — fix now
- diff-bug #9: make-images.R needs ragg and does not say so — fix now
- diff-bug #10: `docs/_extensions` is a plain file in a Windows clone without symlink support — reject, edge (a local render on such a clone, outside the documented macOS and Linux use; the effect is a render error; tests/_extensions has the same shape)
- blame-history #1: docs.yml has no push trigger, so the site is never rendered on main, against CLAUDE.md's "main must render" and verify.yml's push trigger — fix now
- blame-history #2: `cancel-in-progress: true` for every ref, where verify.yml cancels only on pull_request (M008) — fix now
- blame-history #3: docs/.gitignore lacks `*.log`, `*.aux`, `*_files/` — reject, false (after a full render `git status --ignored docs` lists only `.quarto/` and `_site/`)
- blame-history #4: ```` ```{{r}} ```` may show as `{{r}}` — reject, false (the rendered page holds one ```` ```{r} ```` and no `{{r}}`)
- blame-history #5: "tested with Quarto 1.10.19" while the docs job uses release — reject, planned change (README sentence moved verbatim under AC4; D-008)
- blame-history #6: DESIGN.md Known issues point to "The README states" while the site now holds the rules too — reject, planned change (M024 AC4)
- prior-review #1: `cancel-in-progress: true` cancels runs on main, which M008's review removed from verify.yml — fix now (same as blame-history #2)
- prior-review #2: the pages say "tested with Quarto 1.10.19" while docs.yml renders with release — reject, planned change (as blame-history #5)
- ripple #1: PROFILE.md's verify slot names verify.yml and verify-prerelease.yml only — fix now
- ripple #2: CLAUDE.md says main must render at every commit, but docs.yml runs only on PRs — fix now (as blame-history #1)
- ripple #3: DESIGN.md Conventions describes PR CI as verify.yml only — fix now (as diff-bug #2)
- ripple #4: DESIGN.md "The README states this limit" lines — reject, planned change (M024 AC4)
- ripple #5: the M002 lesson names only tests/_extensions — reject, false (it does not contradict a second symlink)
- Pass 1 fix-now items (diff-bug #1, #2, #3, #5–#9; blame-history #1, #2; prior-review #1; ripple #1–#3): fixed b73cdf3 through review return 1; caps restored 9d81552.

Pass 2, review head 9952239, main b7e62a3 (unmoved).

- AC1: fresh clone at 9952239, Quarto 1.10.19, `command -v R` and `command -v Rscript` empty; `quarto render docs` exit 0, one `(W)` line (fig-callout), `git status --porcelain` empty after. `docs.yml` triggers: `pull_request` with paths `docs/**`, `_extensions/**`, `.github/workflows/docs.yml` and no branch filter; `push` to main with the same paths; `workflow_dispatch`. One `run:`, `quarto render docs`; no R step. Pass.
- AC2: the 8 example pages each link PDF → `<name>.pdf`, Typst → `<name>-typst.pdf`, MS Word → `<name>.docx`; 24 of 24 files exist; each PDF-link file reports Producer LuaTeX-1.24.0 and each Typst-link file Creator Typst 0.15.1. Pass.
- AC3: clone's `_site` with `tests/layout.js` at 1280x900: 11 figures on 10 pages, each `float` equal to its side (same list as pass 1). 26 fresh page images (LaTeX PDF, Typst PDF, Word via LibreOffice) show body text beside each of the 9 example figures in each format, the width-gap pages with their new breakpoint sentence included. Pass.
- AC4: `readme_ledger.py` on the clone against origin/main's README: 133 blocks, 115 verbatim, the same 18 hand-matched blocks as pass 1, whose pages return 1 did not change apart from width-gap.qmd, where the gap paragraph is as before. Pass.
- AC5: reference.html: six rows (classes and attributes) and three rows (`wrapped:` keys), each with values, default, and formats; the `width` row now names `3in`, `250px`, or `20em` and per-format units, which the four format pages accept. Pass.
- AC6: `quarto add <zip> --no-prompt` on `git archive` zips of 9952239 and origin/main: exit 0, only `wrapped`, the same 9 files. `.gitattributes` does not enter the install. Pass.
- Gate: `cairn_validate.py` all checks passed; version marker 0.2.0 on branch and main; `tests/verify.py` on 9d81552 (no filter or test change since): all 103 renders pass; changelog none.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: docs.yml's "Runs on main are never cancelled" is false, since a newer queued run replaces a queued one — fix now (verify.yml's same comment is outside the diff: follow-up, row "Correct the cancel comment in verify.yml")
- diff-bug #2: the re-freeze note names the two code-cell pages by hand and goes stale when a page gains a cell — fix now
- diff-bug #3: width-gap.qmd says the values convert to each format's units and links only LaTeX, Typst, and Word, but HTML uses the CSS value as written — fix now
- diff-bug #4: examples/width-gap.qmd's breakpoint sentence is not linked, and the next sentence about narrow columns reads against it — fix now
- diff-bug #5: DESIGN.md's docs-site line omits `workflow_dispatch` — fix now
- diff-bug #6: reference.qmd's `width` row says "Each format takes its own set of units" beside a Formats cell that says the same — reject, style
- diff-bug #7: a PR touching none of docs.yml's paths would wait forever if `docs` were a required check — reject, edge (making it a required check, outside the repo's setup; the effect is a pending check)
- blame-history #1: frozen results are not re-run after a filter change, so CI could pass on stale output — reject, false (freeze keeps knitr's output; Pandoc and the filter run on every render, so a filter change shows)
- blame-history #2: docs.yml drops the main-only branch filter that verify.yml keeps — reject, planned change (AC1, return 1)
- blame-history #3: width-gap.qmd's format link leaves out HTML — fix now (as diff-bug #3)
- blame-history #4: examples/width-gap.qmd states the rule before its exception — fix now (as diff-bug #4)
- prior-review #1: DESIGN.md's "on pull requests and pushes to `main`" reads as PRs to main only — fix now (with diff-bug #5)
- ripple #1: the breakpoint sentence and the narrow-column sentence read against each other — fix now (as diff-bug #4)
- ripple #2: DESIGN.md omits the manual trigger — fix now (as diff-bug #5)
