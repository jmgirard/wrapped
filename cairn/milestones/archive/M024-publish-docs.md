# M024: Publish the site and shorten the README

**Status:** done (2026-10-28, PR #26 https://github.com/jmgirard/wrapped/pull/26)

**Goal:** https://jmgirard.github.io/wrapped/ serves the documentation site that CI rebuilds from `main`, and the README becomes a short page that points to it.

feature series: M023 -> M024

**Outcome:** `.github/workflows/docs.yml` has a `publish` job: on a push or manual run on `main` of `jmgirard/wrapped` it runs `quarto-dev/quarto-actions/publish` (target `gh-pages`, path `docs`, `GITHUB_TOKEN` in `env`, `contents: write`, its three actions pinned to commit SHAs); the `render` job runs on pull requests, other refs, and forks. The `gh-pages` branch was made by an empty orphan commit (Quarto refuses to make it under `--no-prompt`) and a hand `quarto publish gh-pages docs`; Pages moved from `main` `/` to `gh-pages` `/`. The first CI publish (run 40737330987) pushed 4afe284 and Pages built it. `README.md` went from 612 to 69 lines: intro, site link, install, filter YAML, one `.wrap-right` example, `docs/images/readme-example.png` (a pdftoppm crop of `image-figure.pdf`, commands at the end of `docs/images/make-images.R`), and links to each site page. The eight DESIGN Known issues lines, four candidate rows, one lesson, and one w3c-css-values line that named the README as a rule's home now name the `docs/` page and section (`corrected M024`); `tests/readme.qmd`'s title and intro name where each example lives; DESIGN Distribution and Conventions and CLAUDE.md name the site and `quarto render docs`. D-014 records the publish action.

**Decisions:** D-014. Milestone-local: the `publish` job alone pins its actions to SHAs because it alone has write access; it runs only in `jmgirard/wrapped`.

**Review:** Claim audit 38 claims, 1 corrected (CLAUDE.md's README line). Fan-out of four lenses, 22 items: 13 fixed in 1b20351 (SHA pins, `GITHUB_TOKEN`, repository check, write-scope comment, stale DESIGN Conventions and workflow header, README image sentence, CLAUDE.md, fixture intro), 7 rejected (3 planned, 3 false, 1 style), 2 checks with no finding. AC1-AC4 verified; verify 103 renders pass; CI on PR #26: render 1m28s, verify 6m9s, publish skipped. No lesson captured, used, or retired.
