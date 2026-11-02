# Changelog

## Unreleased

## 26.11.0 (unreleased candidate)

- Rename the installed skill and archive from `conda-plugins` to `conda-plugin-skill`, and the repository to `jezdez/conda-plugin-skill`. Install and verify the new skill before removing the old installation. Historical client verification used the old skill name and does not verify the rename.
- Add `agent-skill-conda-plugin-skill`, a text-only `noarch: generic` conda package installing under `share/agent-skills/conda-plugin-skill`. Build and test it with `pixi run --locked build-conda` while retaining `pixi run --locked build` for ZIPs.
- Adopt a manual `YY.MM.P` release process with UTC dates, a zero-padded month, and `P` starting at `0` each month. The canonical `recipe/recipe.yaml` version is `'26.11.0'`, build number `0`, an unreleased candidate. Content changes require new versions. Packaging-only rebuilds use separate build numbers.
- Require a clean reviewed commit, passing CI, both artifacts, and checksums before an authorized release tag. GitHub release drafts require explicit authorization. No private channel is specified and no publication is automated or performed.
- Verify the renamed conda package with pixi-skills 0.1.7 through the generic `agents` and `claude` backend APIs in an isolated macOS project. Native client discovery remains untested. Required companions remain separately installed.
- Validate portable metadata limits and optional fields. Clarify read-only scope and add skill evaluation cases for activation, companion handling, and project defaults.
- Link to upstream Skills CLI installation and update docs. Keep the previously tested installer command as an internal CI fixture.
- Simplify the README introduction, put usage after installation, and clarify which sources the hosted setup check tests.
- Preserve LF endings in companion Bash helpers when installing on Windows.
- Add a manual setup check on fresh Linux, macOS, and Windows runners, covering installed files, Bash helper syntax, and native client discovery.
- Correct Kilo's shared installation path and document a clean setup test with native discovery in Codex, Claude Code, and Kilo.
- Add Apache License 2.0 for original material and preserve upstream notices in standalone skill distributions.
- Add repository guidance, contribution and reporting instructions, locked development tools, validation, and CI.
- Build skill archives under `dist/` and keep generated ZIPs out of the repository root.

## Initial skill collection, 23 October 2026

- Synthesize conda plugin architecture, CLI, format, solver, verification, and testing practices into progressively loaded references.
- Require Superpowers, Humanizer, and Ponytail, with one setup command for Codex, Claude Code, and Kilo.
- Add substantial human-facing documentation guidance for Diátaxis, Sphinx, MyST, sphinx-design, and reproducible VHS demos.
- Document optional Codex Security review without making it an installation prerequisite.
