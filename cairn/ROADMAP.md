# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-24 (scaffold: five candidates from SCOPE.md)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M001 | Run the four wrap feasibility spikes | planned | — | high | milestones/M001-wrap-spikes.md |

## Candidates
<!-- unnumbered ideas; one line each, ordered high → normal → low → parked:
     - [high] short title: detail — added YYYY-MM-DD — links
     - short title: detail — added YYYY-MM-DD — links
     - [parked] short title: detail; promote when <condition> — added YYYY-MM-DD — links
     the opening token is `[high]`/`[low]`/`[parked]` or absent (`normal`); `[parked]` marks a row whose
     promotion condition has not held — tracking-rules "Candidate priority token";
     open each row with its short title, the words the cairn pane shows, then `: `;
     the title is one sentence with no ending period, at least 5 words and at most 40 characters,
     ending with `(#N)` for a row written for GitHub issue N, such as
     `Fix SE of skewness calculation (#100)`; `/cairn-triage` offers a new title for one
     with fewer than 5 words or more than 40 characters; tracking-rules "Candidate short title" has the whole rule -->
- [high] Run the four wrap feasibility spikes: answer S1 to S4 (the wrap class on `FloatRefTarget`, the LaTeX `wrappedfigure` wrapper, wrap-it with a citation in the wrapped text, Word frames). Each answer sets what version 1 covers and which fallback applies — added 2026-10-24 — references/wrap-mechanisms.md — started M001
- Wrap figures in HTML and LaTeX output: the version 1 core. W1 and W2, the edge cases that apply to them, and the fixture document and snapshots that become the verify command. Needs S1 and S2 answered — added 2026-10-24 — references/wrap-mechanisms.md
- [low] Use the HTML stylesheet for EPUB: EPUB is HTML-based, so the W1 stylesheet can apply there. Version 1 keeps a normal figure in EPUB (W5) — added 2026-10-24 — references/wrap-mechanisms.md
- [parked] Wrap figures in Typst PDF output: W3, with wrap-it or meander bundled under `typst/packages`; promote when spike S3 shows that one of them renders wrapped text with a citation — added 2026-10-24 — references/wrap-mechanisms.md
- [parked] Wrap figures in Word output with frames: W4; promote when spike S4 shows that Word opens the file and shows one merged frame. This work also checks how LibreOffice and Google Docs show the frame (moved from M001 on 2026-10-24) — added 2026-10-24 — references/wrap-mechanisms.md
