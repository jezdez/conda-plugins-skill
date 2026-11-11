# Changelog

## Unreleased

## 26.11.1 (unreleased candidate)

- Rename the repository to `jezdez/conda-plugins-skill`. Use `conda-plugins` for the skill and installed directory, and `agent-skill-conda-plugins` for the conda package. Install the new skill before removing an existing `conda-plugin-skill` installation.
- Stop building and publishing custom skill ZIPs. Keep Skills CLI/Git installation and conda packages.
- Add lessons from reviewing conda-skills: isolated file-based discovery tests, conda-workspaces task usage, authoring versus installed state, filesystem containment, and literal terminal output. Add pinned provenance and a maintainer evaluation scenario.
- Refresh conda-skills guidance through its 0.2.2 preparation commit: safe source previews and directory opening, destination-derived unlinking, batch conflict checks, native aliases, and helper extraction based on readability and testing.
- Document shared Hatch version resolution, conda runtime requirements outside wheel metadata, installed-artifact checks, release jobs that depend on the full test workflow, and recovery using original artifacts. Add release and file-operation evaluation prompts.
- Document conda-skills discovery and linking. Automate releases from annotated calendar-version tags, require all reusable checks, attest exact artifacts, upload through a protected Anaconda.org environment, and publish the GitHub draft only after upload succeeds.
- Omit embedded conda recipes to keep absolute build-machine paths out of distributed packages.

## 26.11.0 (2026-11-02)

- Add a manually dispatched release workflow for existing tags. Reuse cross-platform checks, prepare canonical Linux assets with a manifest and checksums, and leave publication manual with GitHub release immutability. Validate workflows with actionlint and the upstream zizmor action in auditor mode with online checks.
- Add maintainer evaluation prompts in skill-creator's `evals/evals.json` format, separate from the distributed skill. Use paired skill/baseline runs and upstream grading and human-review tools without a repository Python test suite.
- Remove the repository tests directory, evaluation fixtures, pytest, Ruff, and ty. Use the upstream skill-creator workflow for behavioral evaluations in disposable workspaces, separate from package validation.
- Keep conda payload and license-identity checks in the recipe. The ZIP build checks the integrity of its actual output using Python's standard archive CLI.
- Remove the remaining validation and ZIP scripts. Use prek metadata rules, Lychee for local links, and Python's standard ZIP command through Pixi. ZIP output is no longer guaranteed byte-reproducible.
- Keep historical verification in the changelog instead of the README. The [old-name hosted run](https://github.com/jezdez/conda-plugin-skill/actions/runs/40590133508) found all 23 skills in Codex, Kilo, and Claude Code on Linux, macOS, and Windows. It did not test model invocation or the renamed skill.
- Remove PyYAML and generic optional-metadata parsing. Prek checks YAML syntax, recipe fields, and the skill's three-field header. Lychee checks local links.
- Use prek for the existing repository hooks, replacing the pre-commit runner. Run them with `pixi run --locked prek`.
- Centralize checks in Pixi tasks called by prek. Replace the custom conda build wrapper with recipe-native copying and tests, and replace the bespoke client installation harness with a documented manual smoke test.
- Rename the installed skill and archive from `conda-plugins` to `conda-plugin-skill`, and the repository to `jezdez/conda-plugin-skill`. Install and verify the new skill before removing the old installation. Historical client verification used the old skill name and does not verify the rename.
- Add `agent-skill-conda-plugin-skill`, a text-only `noarch: generic` conda package installing under `share/agent-skills/conda-plugin-skill`. Build and test it with `pixi run --locked build-conda` while retaining `pixi run --locked build` for ZIPs.
- Adopt a manual `YY.M.P` release process with UTC dates, an unpadded month, and `P` starting at `0` each month. The canonical `recipe/recipe.yaml` version is `'26.11.0'`, build number `0`, an unreleased candidate. Content changes require new versions. Packaging-only rebuilds use separate build numbers.
- Require a clean reviewed commit, passing CI, both artifacts, and checksums before an authorized release tag. GitHub release drafts require explicit authorization. No private channel is specified and no publication is automated or performed.
- Verify the renamed conda package with pixi-skills 0.1.7 through the generic `agents` and `claude` backend APIs in an isolated macOS project. Native client discovery remains untested. Required companions remain separately installed.
- Clarify read-only scope and evaluation guidance for activation, companion handling, and project defaults.
- Link to upstream Skills CLI installation and update docs.
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
