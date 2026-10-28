# M023: Build the documentation site

**Status:** done (2026-10-28, PR #25 https://github.com/jmgirard/wrapped/pull/25)

**Goal:** A Quarto website in `docs/` carries all of the documentation as topic pages, with a gallery of examples rendered in HTML, PDF through LaTeX, PDF through Typst, and Word.

feature series: M023 -> M024

**Outcome:** `docs/` is a Quarto website (`_quarto.yml`, navbar and docked sidebar, `docs/_extensions` symlink, `execute: freeze: auto` with committed `docs/_freeze/`, `styles.css` `.demo` frames). Topic pages carry every README rule: index, get-started, width-gap, defaults, stopping, normal-layout, formats/html (slides, dashboards), formats/latex, formats/typst, formats/word, reference (nine-row table). `docs/examples/` holds a listing, eight example pages with html, pdf, typst (`output-file: <name>-typst.pdf`), and docx formats, and revealjs and dashboard pages; one knitr cell is frozen for all four formats. Images come from `docs/images/make-images.R` (ragg). `.github/workflows/docs.yml` runs `quarto render docs` with no R on pull requests and pushes to main that change `docs/`, `_extensions/`, or the workflow, PR-only cancel. `.gitattributes` marks `docs/_freeze/**` generated. DESIGN.md Conventions and PROFILE.md's verify slot name the site. README and filter unchanged.

**Decisions:** none milestone-local. Plan choices: Quarto website over committed example outputs; CI-rendered "Other Formats" links over page images; `freeze` over R in the docs job.

**Review:** Criteria audit 7 findings, 6 taken. Claim audit 190 claims, 7 corrected (div-caption markdown, `wrap-gap` percents, `wrap-lines` units, alt text in untagged PDFs, "every format"). Pass 1 fan-out, 23 findings: 14 fixed, 9 rejected (5 planned, 3 false, 1 edge); review return 1 for AC1 (`branches: [main]` limited the PR trigger). Pass 2, 14 findings: 10 fixed, 4 rejected (1 style, 1 edge, 1 false, 1 planned); verify.yml's cancel comment went to the new row "Correct the cancel comment in verify.yml". AC1-AC6 verified at 9952239; CI on PR #25: render 1m18s, verify 7m28s, both pass. Hygiene captured one lesson (knitr fences, pdf/typst file clash, freeze hash, `(W)` warnings), evicted the 2026-10-26 (M009) LaTeX-log lesson by rank, marked the M002, M004, M020, and M022 lessons used.
