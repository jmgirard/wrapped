# Toolchain profile: quarto-extension

<!-- A cairn toolchain profile: the toolchain slots that the operational
     skills read, made from cairn's quarto-extension profile. The validation
     doctrine is not a slot. It applies to every toolchain and lives in
     cairn's skills/shared/validation-doctrine.md. All seven `## <slot>`
     sections are present. cairn_validate fails on a missing or empty slot. -->

The Quarto extension toolchain. This repo's deliverable is the `wrapped`
filter under `_extensions/wrapped/`, installed with
`quarto add jmgirard/wrapped`. Quarto 1.10 installs from the branch named
`main`, which is this repo's default branch, so a merge reaches users at once.
A `v<version>` tag and a GitHub release mark the version for
`quarto add jmgirard/wrapped@v<version>` and the releases page.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite). From the
repository root, run:

```
python3 tests/verify.py
```

It renders the fixtures under `tests/` to HTML, revealjs, PDF through
LaTeX, PDF through Typst, and docx, and the book project under `tests/book/`
to HTML. It compares the parts that the filter changes with
the snapshots in `tests/_snapshots/`. It exits with status 1 on a failed
render or a difference. It needs Quarto, R with knitr, and TinyTeX. After an
intended output change, run it with `--update` and review the snapshot diff.
Layout is not in this command. Measure it in a browser with
`tests/layout.js`, as its header says.

## consistency-gate
Toolchain tests that `/milestone-review` runs *in addition to* the universal
cairn-file tests (`cairn_validate`, coverage completeness, `cairn_impact`):
- Every version marker that `release-walk` names holds the same version.
- The verify command passes on the review head: every fixture renders with
  no errors, and every snapshot matches.
- The changelog slot says "none", so the gate reads no changelog entry.

## test-doctrine
Test expectations layered on the universal "What gets a test" rules in
tracking-rules. An extension is tested by rendering, not by calling functions:
- A filter change is tested by rendering a fixture document that uses it and
  reading the output in each format the change touches. The test is a string
  in the HTML, or a snapshot of the kept `.tex`, the kept `.typ`, or the docx's
  `word/document.xml`.
- A bug fix gets a fixture document that renders wrong before the fix.
- A change to `wrapped.css` keeps the version as it is until release (see
  `release-walk`), because the version rises at release.

## release-walk
The release procedure `/cairn-release` follows. The version marker is
`version:` in `_extensions/wrapped/_extension.yml`. The filter's
`add_html_dependency` call carries no version, so it is not a marker. A later
change can add the version to another file. If it does, that change names the
file here. Every named marker holds the same version. The version rises at release (CLAUDE.md), so the
release-time arm is the usual path.
Before step 1 of `/cairn-release`,
run `git fetch --tags <base>` and read the remote default branch's tip:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_versions.py" _extensions/wrapped/_extension.yml --at <base>/<default-branch>`.
If `CLAUDE_PLUGIN_ROOT` is unset, use the cairn plugin's install directory.
The script refuses a shallow clone. It prints the tip's
version, the first commit of that version's unbroken run of first-parent
commits (`start`), and whether a `v<version>` tag exists.
- **Tag-only arm.** With no tag, the tip's version is unreleased:
  merged work raised it, or it was never tagged. Raise nothing and make no
  prep commit. First make sure that every other named marker holds the version
  at `start` (`git show <start>:<file>`). Then step 1 asks the user to accept
  the version and `start` (its subject) instead of choosing a bump. Step 2
  makes no edit. Tag the run's start:
  `git tag -a v<version> <start> -m "v<version>"`, pushed at the user's
  approval.
- **Stops.** A marker mismatch or a refused version ends the run with
  the reason and no tag. A marker mismatch at `start` cannot be fixed for this
  version: only a merge that raises the version again clears it, and this
  version then stays untagged.
- **Release-time arm.** With the tag present, run the generic walk. With
  changelog "none", decide the bump (patch/minor/major) from git history and
  skip the consolidation. Raise every named marker and commit the release prep
  to the default branch. Tag that commit `v<version>`, pushed at the user's
  approval.
- **Release notes.** With changelog "none", the notes are the commit subjects
  on the default branch since the previous `v*` tag:
  `git log --first-parent --format='- %s' <previous tag>..<tagged commit>`.
  The previous tag is
  `git describe --first-parent --tags --abbrev=0 --match 'v*' <tagged commit>^`.
  For a first release, with no previous `v*` tag, drop `<previous tag>..`.
  Where the `origin` remote is GitHub and `gh` is available, the handoff
  provides a `gh release create` command with these notes. cairn never runs
  it (the universal step 4). No registry step: the tag is the release.

## init-detection
Recognized by `cairn-init` from `_extensions/*/_extension.yml` or
`_extensions/*/_extension.yaml`. The repo must also have no `DESCRIPTION`, no
`pyproject.toml`/`setup.py`/`setup.cfg`, and no
`.claude-plugin/plugin.json`/`.claude-plugin/marketplace.json`. It ranks ahead
of docker-image and generic. This repo had no marker at init (2026-10-24), so
the user chose the profile. The repo now holds
`_extensions/wrapped/_extension.yml`, so detection finds the profile.

## greenfield-openers
Answered at init on 2026-10-24. The extension type is a filter. The version
rises at release, not at each merge (CLAUDE.md). Distribution is public, with
`v<version>` tags and GitHub releases (DESIGN Purpose & Scope).

## changelog
none. This repo keeps no changelog file. Release notes go on GitHub releases.
`/hotfix` skips the changelog entry. The release-walk skips consolidation and
writes its release notes from git history.
