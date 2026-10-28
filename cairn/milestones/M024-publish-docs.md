<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M024: Publish the site and shorten the README

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M023   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the public docs site and the README   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m024-publish-docs   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

https://jmgirard.github.io/wrapped/ serves the documentation site that CI rebuilds from `main`, and the README becomes a short page that points to it.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**

- A publish job in `.github/workflows/docs.yml` with
  `quarto-dev/quarto-actions/publish` (target `gh-pages`), on pushes to
  `main` that change `docs/`, `_extensions/`, or the workflow, and by hand.
- The first publish by hand from the branch, which makes the `gh-pages`
  branch, and the switch of the Pages source from `main` `/` to `gh-pages`
  `/` (both allowed by the user at the plan's question set).
- A short `README.md`: what the filter does, install, the filter YAML, one
  example, an image of a rendered wrapped figure, and a link to the site.
- Pointers that name the README as the home of a rule move to the site:
  the "The README states" lines of DESIGN.md's Known issues, the intro of
  `tests/readme.qmd`, and DESIGN.md's Distribution and CLAUDE.md's dev
  commands, which gain the site and `quarto render docs`.

**Out:**

- The site's pages and examples → M023.
- D-013's line "the README asks the user to write the `.card` div" stays as
  history; the dashboards page carries that request from M023 on.
- A changelog entry: the profile's changelog slot says none.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: `.github/workflows/docs.yml` publishes the rendered site to the
      `gh-pages` branch with `quarto-dev/quarto-actions/publish` on each
      push to `main` that changes `docs/`, `_extensions/`, or the workflow
      file, and on a manual run. On a pull request it renders and does not
      publish.
- [ ] AC2: Before the merge, the GitHub Pages source of `jmgirard/wrapped`
      is the `gh-pages` branch at `/`. Each HTML file that
      `find docs/_site -name '*.html'` lists after a render of the branch
      head returns HTTP 200 at the same path under
      https://jmgirard.github.io/wrapped/, with the same `<title>`.
- [ ] AC3: `README.md` has 80 lines at most (`wc -l`). It holds a sentence
      on what the extension does, the `quarto add jmgirard/wrapped` command,
      the `filters:` YAML, one wrapped-figure example, an image of a rendered
      wrapped figure, and a link to https://jmgirard.github.io/wrapped/.
- [ ] AC4: Each of these pointers names a place that states its rule on
      the branch head: a site page, or the short README where it still
      holds that rule. They are the eight "The README states" or "The
      README says" lines of DESIGN.md's Known issues; the candidate rows
      "Stop text overlap with small wrap-lines", "Keep narrow widths when no
      width fits", "Wrap no-id margin images in PDF", and "Check margins in
      slidy and other slides"; the LESSONS.md line "the README asks for
      spaces around `*`"; and the "`README.md`, Width and gap" line of
      `cairn/references/w3c-css-values.md`. The intro of
      `tests/readme.qmd` states true facts about where each example lives.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T4
- AC3 → T2, T3
- AC4 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Add the publish job to `docs.yml`: `permissions: contents: write`,
      `quarto-dev/quarto-actions/publish@v2` with `target: gh-pages` and
      `path: docs`, run only on `push` to `main` and `workflow_dispatch`.
      Record the new action in a D-entry (it extends D-008's CI tools).
- [x] T2: Make the README image from an example page: render it, turn its
      first PDF page into a PNG with `pdftoppm`, and commit the PNG under
      `docs/images/` with the command in a comment of the page or the
      README source.
- [ ] T3: Rewrite `README.md` to the short form.
- [ ] T4: Publish from the branch with `quarto publish gh-pages docs
      --no-prompt --no-browser`, switch the Pages source with
      `gh api -X PUT repos/jmgirard/wrapped/pages` (branch `gh-pages`, path
      `/`), wait for the Pages build, and fetch each page path.
- [ ] T5: Update the AC4 pointers in place, each marked `corrected M024`
      where it is current knowledge, then DESIGN.md's Distribution and
      CLAUDE.md's dev commands (the site and `quarto render docs`).

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
- 2026-10-28: idea vet: one concern, that the README is long because it records every edge case, so a site moves the length rather than cutting it; the user chose to keep every rule, split by topic.
- 2026-10-28: lessons used: none.
- 2026-10-28: feature series: M023 -> M024
- 2026-10-28: question set: publishing — the user allowed adding `quarto-dev/quarto-actions/publish` to CI, making a `gh-pages` branch by a hand publish from this branch before the merge, and switching the Pages source from `main` `/` to `gh-pages` `/`.
- 2026-10-28: plan gate chose a `gh-pages` branch over a GitHub Actions Pages deploy because the branch can be published and checked live before the merge; falsified by the `gh-pages` branch breaking `quarto add` or the Pages build.
- 2026-10-28: criteria audit (full, shared with M023): AC2's live check needs a publish and a settings change before the merge, so T4 names both and the user allowed them; AC4 added for the seven DESIGN.md Known issues lines that say "The README states".
- 2026-10-28: AC4 was rewritten after the audit and sent to a fresh reader; that re-audit was still running at the plan commit, so its result lands in a follow-up tracking commit.
- 2026-10-28: AC4 re-audit (full, fresh reader): the grep domain mixed rule pointers with fixture ids, vendored file lists, and history, and T5 missed four candidate rows, one lesson, and one references line. AC4 now names a fixed list of pointers plus `tests/readme.qmd`'s intro; out of it on purpose: wrap-it's `typst.toml`, the `fig-readme-*` ids, `verify.py`'s fixture name, the M024 row, `wrap-mechanisms.md` E15 (a planning note), and the "README since M019" row (history).
- 2026-10-28: implement started on branch m024-publish-docs.
- 2026-10-28: T1 done: `docs.yml` has a `publish` job (contents: write, publish@v2, target gh-pages, path docs) that runs on a push or manual run on `main` only, so a manual run on another branch renders and does not publish; the `render` job runs on every other event. D-014 records the action.
- 2026-10-28: T2 done: `docs/images/readme-example.png` is a 144-dpi crop of page 1 of `image-figure.pdf` (LaTeX); the two commands sit at the end of `docs/images/make-images.R`, whose header said it makes every image in the folder, and the README comment points there (the simple-english hook blocked the commands in the README comment); a rerun of the command gives a byte-identical PNG.

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
