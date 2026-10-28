# wrapped

A Quarto filter extension that wraps body text around figures in HTML, PDF
through LaTeX, PDF through Typst, and Word. The design is in
`cairn/DESIGN.md`, and the research for each format is in
`cairn/references/wrap-mechanisms.md`.

## Conventions

- The version in `_extensions/wrapped/_extension.yml` rises at release, not
  at each merge. A change to `wrapped.css` or another shipped file keeps the
  version as it is until the next release.
- Users install from `main` (`quarto add jmgirard/wrapped`), so `main` must
  render without errors at every commit.
- Run the tests with `python3 tests/verify.py` from the repository root.
- The documentation site is in `docs/`. Render it with `quarto render docs`.
  `.github/workflows/docs.yml` publishes it to the `gh-pages` branch, which
  serves https://jmgirard.github.io/wrapped/. A push to `main` that changes
  `docs/`, `_extensions/`, or the workflow starts it. The README only points
  to the site, so a rule for users goes on a site page.

## Project tracking (cairn)

This repo uses the cairn plugin. **Before acting on any request, classify it
and route** — the tracking rulebook only loads once a cairn skill fires, so
starting work in plain conversation silently bypasses the work tiers and the
git model. Classify first:

- **Trivial** (typo, comment, tracking edit): in owner mode, commit to the
  default branch. In guest mode, leave the edit on disk (`cairn/` files only).
- **Look into a GitHub issue**: invoke `/milestone` with the issue number
  or URL.
- **User-visible bug**: invoke `/hotfix`.
- **New work, a design decision, or more than one sitting**: invoke
  `/milestone-plan`. Where a hotfix or trivial route fits, it offers that
  first. Otherwise one question set comes, and the run goes on to the merge
  question. Typed `/milestone-implement` or `/milestone-review` resumes it.
- **Status, "what's next", or unsure which tier**: invoke `/milestone`.
- **Never implement code on the default branch** outside a milestone/hotfix
  branch. Nothing reaches it without the user's explicit approval at the
  merge question, or for a trivial edit their request or the tier chip.

Whenever the request is anything but trivial, invoke the skill *first* so the
full rulebook (the plugin's `skills/shared/tracking-rules.md`) and its conduct
load — do not reconstruct the rules here from memory. All project state lives under
`cairn/` (**Architecture → DESIGN · Status → ROADMAP · Tasks → milestone
files · Decisions → DECISIONS · Lessons → LESSONS · History → archive +
git**); never record
status or TODOs in this file. Claude's persistent memory never holds project
state; `cairn/` files win any conflict.
