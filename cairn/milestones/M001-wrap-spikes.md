<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M001: Run the four wrap feasibility spikes

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** internal — spike documents and a research page, and nothing reaches a user who installs the extension
- **Branch/PR:** m001-wrap-spikes

## Goal

Record a yes-or-no answer, with evidence, to each wrap feasibility question S1 to S4 and to the minimum Quarto version question.

## Scope

**In:** Small spike documents under `spikes/`, one folder per question. Each spike renders on this machine with Quarto 1.10.19. The answers go into the "Open questions" section of `cairn/references/wrap-mechanisms.md`. The minimum Quarto version also goes into `cairn/DESIGN.md`.

**Out:**
- Extension code under `_extensions/wrapped/`. That work goes to the candidate "Wrap figures in HTML and LaTeX output", planned from these answers.
- Bundling wrap-it or meander in the repo. The Typst candidate row decides it.
- How LibreOffice and Google Docs show the Word frame. The Word candidate row holds that check.
- The Quarto 2 question. It stays open in the research page because no spike can answer it.

## Acceptance criteria

- [x] AC1: The S1 entry in `cairn/references/wrap-mechanisms.md` "Open questions" records yes or no for four figure sources, with the date and Quarto 1.10.19. The four sources are a markdown image with `.wrap-right`, a div figure with `.wrap-left`, a knitr cell with `#| classes: wrap-right`, and a Jupyter cell with `#| classes: wrap-right`. For each source, the entry names the node and attribute field where a `pre-quarto` filter found the class, or says that it found none. If Jupyter is not installed, the Jupyter answer is "not tested" with the reason. The entry cites a spike file under `spikes/`.
- [x] AC2: The S2 entry records yes or no for one test. The test passes when a LaTeX render of a spike document with `fig-env="wrappedfigure"` and a key-value `fig-pos` builds a PDF with no LaTeX error, and the figure page shows body text beside the figure. The entry cites the spike file.
- [x] AC3: The S3 entry records yes or no for wrap-it 0.1.1 in two citation modes: Quarto's default Typst citation handling and `citeproc: true`. An answer is yes when a Typst render of a spike document builds a PDF with no error and shows wrapped text that holds a `@citation` beside the figure. If either wrap-it answer is no, the entry records the same two answers for meander 0.4.4. The entry cites the spike file.
- [x] AC4: The S4 entry records yes or no on whether Microsoft Word opens the spike docx with no repair prompt and shows the image and caption in one frame with body text beside it. The entry names the candidate row that holds the LibreOffice and Google Docs check. The entry cites the file under `spikes/` that builds the docx.
- [x] AC5: The Quarto version entry names the earliest Quarto release whose tagged source has the `typst/packages` loader in `src/command/render/output-typst.ts`, or the release that a quarto-cli changelog line names for it. The entry cites that tag or line. The "Quarto version" paragraph of `cairn/DESIGN.md` states that release, or keeps its provisional value with the reason.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: S1 spike in `spikes/s1/`. Write a probe filter at `pre-quarto` that logs the classes and attributes of each `FloatRefTarget` and of each image. Render the four figure sources to HTML. For the Jupyter cell, create a venv in the session scratchpad, install `jupyter` there, and set `QUARTO_PYTHON` for that render only. Record AC1.
- [x] T2: S2 spike in `spikes/s2/`. Put the `wrappedfigure` wrapper from the research page in a header include, and set `fig-env` and `fig-pos` on one figure. Render to PDF with `keep-tex: true`. Convert the figure page to an image with `pdftoppm` and read it. Record AC2.
- [x] T3: S3 spike in `spikes/s3/`. Add a small `.bib` file and a raw Typst block that calls `wrap-content` from `@preview/wrap-it:0.1.1` with a citation in the wrapped text. Render in both citation modes and read the figure page. If either mode fails, repeat with `@preview/meander:0.4.4`. Record AC3.
- [x] T4: S4 spike in `spikes/s4/`. Write a filter or script that puts the same `w:framePr` on the image paragraph and the caption paragraph, and build the docx. Ask the user to open it in Word and report what Word shows. Record AC4.
- [x] T5: Read the quarto-cli tags and changelog for the `typst/packages` loader in `src/command/render/output-typst.ts`. Record AC5 and update the "Quarto version" paragraph of `cairn/DESIGN.md`.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: tier check: not run — work named at the question set.
- 2026-10-24: idea vet: no concerns. The spikes answer the open questions that the research page lists, and each answer sets which fallback version 1 uses.
- 2026-10-24: collision check: absorbed the candidate "Run the four wrap feasibility spikes". No milestones, archive entries, or D-entries existed. Inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-24: lessons harvest: LESSONS.md is empty.
- 2026-10-24: added the minimum Quarto version question (research page, open question 5) to the scope, because T3 already reads Typst package loading and the answer sets `quarto-required`.
- 2026-10-24: question set: which work to plan — the four spikes.
- 2026-10-24: question set: who checks the spike docx — the user, in Word only. The LibreOffice and Google Docs check moved to the candidate "Wrap figures in Word output with frames".
- 2026-10-24: question set: Jupyter for S1 — install `jupyter` in a throwaway venv in the session scratchpad, with no change to the global Python.
- 2026-10-24: question set: Typst packages for S3 — renders may download wrap-it 0.1.1 and meander 0.4.4 from packages.typst.org into Typst's cache. Nothing is bundled in the repo.
- 2026-10-24: criteria audit (reduced mode, internal tier, fresh Opus reader) returned 5 findings, all fixed by narrowing. AC1 and AC2 drop the clauses on how the evidence was made. AC1 allows "not tested" for Jupyter. AC4 drops "from the user's look" and names the row for the other apps. AC5 reads tagged source instead of claiming release behavior.
- 2026-10-24: plan gate chose committed spike files under `spikes/` over spikes kept only in the scratchpad, because later milestones can rerun them and the fixture document can grow from them; falsified by `quarto add jmgirard/wrapped` copying or rendering `spikes/`.
- 2026-10-24: plan gate chose raw Typst blocks in the S3 spike over a `post-render` filter, because S3 asks whether wrap-it can render a citation, not how the filter builds the call; falsified by the filter's output differing from the hand-written call in a way that changes citation rendering.
- 2026-10-24: implement started on branch m001-wrap-spikes.
- 2026-10-24: T1 done. S1: the class reaches the float for markdown and div figures; for knitr and Jupyter cells it sits on the enclosing cell Div, and a top-down pass carries it. The Jupyter spike shows the existing PNG with `IPython.display.Image`, so the venv needs only `jupyter`, not matplotlib. Render output is ignored by `spikes/.gitignore`.
- 2026-10-24: T2 done. S2: yes. Both wrapped figures render beside their text in the PDF (pages read with `pdftoppm`). The research-page sketch did not compile, so the spike's `wrapped.tex` holds the working form.
- 2026-10-24: T3 done. S3: yes in both citation modes with wrap-it 0.1.1 on Typst 0.15.1, so meander was not tested. wrap-it issue #15 did not show here.
- 2026-10-24: T5 done. The `typst/packages` loader first appears at tag v1.9.18, and the first stable release with it is v1.9.36. DESIGN now states `>=1.9.36`. A `git log -S` search in a partial clone ran about 40 minutes without finishing and was stopped; reading the file at each release tag replaced it.
- 2026-10-24: T4 spike built (`spikes/s4/frame.py`). It frames two figures in two forms, one merged `w:pPr` and one extra `w:pPr`, so one Word look answers both. Waiting on the user's look in Word.
- 2026-10-24: T4 done. The user reported that Word opened the framed docx cleanly and showed one frame with wrapped text for both figures, so S4 is yes in both XML forms.
- 2026-10-24: claim audit: not owed — internal tier.
- 2026-10-24: all tasks done. The verify slot names no automated command yet (PROFILE.md), so the evidence is the recorded answers. Status set to review.

## Decisions

## Review

- AC1 evidence (2026-10-24): reran `spikes/s1/s1-knitr.qmd` and `spikes/s1/s1-jupyter.qmd` on the branch head. The probe output matches the S1 entry for all four sources: class in `FloatRefTarget.classes` for the markdown image and the div figure, and on the enclosing cell `Div` for the knitr and Jupyter cells. The S1 entry in `cairn/references/wrap-mechanisms.md` carries the date, Quarto 1.10.19, the node and field for each source, and cites `spikes/s1/`.
- AC2 evidence (2026-10-24): reran `spikes/s2/s2.qmd` to PDF with no LaTeX error. Page 1, read as an image, shows both figures beside their paragraphs. The S2 entry records yes and cites `spikes/s2/s2.qmd` and `spikes/s2/wrapped.tex`.
- AC3 evidence (2026-10-24): reran `spikes/s3/s3-wrapit.qmd` to Typst PDF in both citation modes with no error. `pdftotext` shows narrowed lines holding "J. Smith and J. Doe [1]" (default) and "Smith and Doe (2020)" (citeproc) beside the figure. The S3 entry records yes for both modes, says meander was not needed, and cites the spike file.
- AC4 evidence (2026-10-24): the S4 entry records yes, from the user's answer at the Word look in this session: no repair prompt, and one frame with wrapped text for both figures. It names the candidate "Wrap figures in Word output with frames" for the LibreOffice and Google Docs check, and cites `spikes/s4/frame.py`. That row's detail in `cairn/ROADMAP.md` holds the check.
- AC5 evidence (2026-10-24): the version entry names v1.9.36 as the earliest stable release whose tagged `output-typst.ts` has the loader, and v1.9.18 as the earliest pre-release tag. It cites the tags and `collectPackageSources`. The repo uses "release" and "pre-release" as separate terms (research page, Evidence snapshot), so "the earliest Quarto release" is v1.9.36. The DESIGN "Quarto version" paragraph states `>=1.9.36`.
- Consistency gate (2026-10-24): `cairn_validate.py` exit 0, all checks passed. No principle changed, so `cairn_impact` skipped. Toolchain slot: no `_extensions/` exists, so no version marker to compare. The verify slot names no render command yet. The changelog slot is "none".
