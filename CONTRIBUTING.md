# Contributing

This repository collects practices for colleagues developing conda plugins with Codex, Claude Code, and Kilo. Useful contributions explain a development decision, provide a worked example, or correct guidance that no longer matches the supported APIs.

Read [AGENTS.md](AGENTS.md) for repository rules and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations. If the question concerns a particular plugin's implementation, use this repository to improve the general guidance and keep implementation changes in that plugin's own project.

## Set up the repository

Use [Pixi](https://pixi.sh/) to create the locked development environment:

```sh
pixi install --locked
pixi run --locked check
```

The environment contains Python, PyYAML, pytest, Ruff, ty, and pre-commit. It does not install the skill or its companions into your agent clients. Follow the [README setup instructions](README.md#install-with-npx) when you want to use them.

## Change a skill

Start with the reader's task and the existing reference that covers it. Keep `SKILL.md` focused on discovery, essential requirements, and routing. Put substantial examples and domain guidance in the relevant reference. Preserve complete standalone skill folders, including license notices.

Verify API and tool claims against the supported version or current upstream source. Record pinned examples in the source reference. Explain which rules are general defaults and which belong to one source plugin. Apply Humanizer to prose while keeping the technical facts and the detail needed by a human reader.

Run the checks and rebuild the distribution:

```sh
pixi run --locked check
pixi run --locked build
pixi run --locked pre-commit
```

The validator checks skill metadata, supported Markdown links and anchors, standalone references, and distribution notices. It does not execute examples or prove that an agent follows the instructions. Execute changed examples and use a realistic application scenario for substantial instruction changes. Keep tests that exercise observable behavior, such as a broken link or an archive missing a notice.

Metadata checks follow the [Agent Skills specification](https://agentskills.io/specification), including name and description limits and optional-field types. This repository additionally requires ASCII kebab-case names and Apache-2.0 with bundled notices. Keep client-specific extensions out of portable frontmatter. The recommended entry-point budget of 500 lines and 5,000 tokens is an editorial guideline, not a format error. Review depth and reference loading rather than applying that budget to human-facing guides.

When changing `pixi.toml`, run `pixi lock` and include the updated lockfile. `pixi run --locked build` writes `dist/conda-plugin-skill.zip`. Generated files stay untracked and out of the repository root. Inspect the ZIP before sharing it with the intended audience.

## Test installation on Linux, macOS, and Windows

Run the [installation check workflow](https://github.com/jezdez/conda-plugin-skill/actions/workflows/setup.yml) from GitHub Actions to test the pinned copy-installation fixture in `scripts/check_setup.py`. It runs only on manual dispatch, using fresh Linux, macOS, and Windows runners. Windows uses Git Bash. The check installs from the live GitHub sources into the runner's initially empty skill directories, compares the installed files with their source revisions, checks Bash helper syntax, and asks each client to list its skills without sending a model prompt.

The fixture retains Skills CLI 1.7.4 and the former README setup procedure, with the renamed `conda-plugin-skill` selection. It does not test all versions or installation methods described by the upstream docs. It fetches skills from the source repositories' default branches, so the rename must be published there before the hosted check can pass. A successful run does not validate unpublished skill changes on your branch.

The workflow saves a verification summary as a private artifact for seven days. It records source revisions, file checks, and client discovery results. The test script requires a GitHub-hosted runner and empty client skill directories to guard against accidental local installations. Model behavior and native plugin hooks need separate checks.

The README's recorded hosted results used the old `conda-plugins` name. They do not verify native discovery of `conda-plugin-skill`. For conda packages, test pixi-skills links through its generic `agents` and `claude` backends in disposable project directories. Check the selected version's backend support, the complete installed skill, relative references, and discovery in each intended client. Keep these results separate from Skills CLI copy-installation results. Do not install into a user's global client directories for verification. Required companions must be installed separately in the isolated setup.

## Release process

Releases are manual and opt-in. The conda packaging design follows [skill-forge](https://github.com/pavelzw/skill-forge), but this private repository has no selected publication channel. No publication has been automated or performed. Adding packaging or merging a change does not authorize a tag, upload, or GitHub release.

The canonical release version is `package.version` in `recipe/recipe.yaml`, initially the quoted string `'26.11.0'`, with `build.number: 0`. This is an unreleased candidate, not an available release. The `build-conda` task runs the recipe's installed-package tests, then extracts the archive and compares the complete skill payload with the source before retaining the artifact.

Versions use `YY.MM.P`, based on the release date in UTC. `YY` is the two-digit year, `MM` is the zero-padded month, and `P` starts at `0` each month and increases for each content release that month. For example, November 2026 starts at `26.11.0`, then `26.11.1`. December starts at `26.12.0`. Tags use the exact version prefixed with `v`, such as `v26.11.0`. If the candidate is released in a later month, update its version before tagging.

Changes to distributed skill content require a new version. A packaging-only rebuild of unchanged content increments `build.number` separately and keeps `package.version` unchanged. Reset the build number to `0` for a new content version. Do not move or reuse a content release tag for a rebuild. Record the rebuild's commit, build number, and checksums separately.

1. Obtain explicit authorization to prepare the release. Review the content, recipe, and changelog, choose the version, and keep the release entry marked unreleased until publication. Use a clean, reviewed commit with no uncommitted changes.
2. Run `pixi run --locked check` and `pixi run --locked pre-commit`. CI must pass for the exact reviewed commit before tagging. Local checks do not substitute for hosted CI.
3. Build both artifacts from that commit with `pixi run --locked build` and `pixi run --locked build-conda`. The ZIP belongs at `dist/conda-plugin-skill.zip`. The text-only `noarch: generic` package is named `agent-skill-conda-plugin-skill` and belongs under `dist/conda/noarch/`. Inspect both for the complete skill, references, and license notices. Check the package version, build number, and `share/agent-skills/conda-plugin-skill` payload path.
4. Verify installation in disposable environments and client directories. Generate SHA-256 checksums for both final artifacts and retain them with the artifacts under ignored `dist/`. Record the source commit and actual verification scope. Do not claim that archive inspection proves native client discovery.
5. With explicit tag authorization, create the matching `vYY.MM.P` tag on the reviewed commit. Pushing that tag also requires authorization. Never retag a published version.
6. Create a GitHub release draft only with explicit authorization. Attach the reviewed artifacts and checksums to the draft if authorized. A draft is not publication approval. Publishing it or uploading the conda package requires separate authorization and an agreed private destination.

Do not document a package install command or channel as available before publication. Keep GitHub links pointed at `jezdez/conda-plugin-skill`. Report builds, client checks, hosted CI, tagging, and publication separately.

## Evaluate skill behavior

[tests/skill_evals.json](tests/skill_evals.json) contains a small set of trigger queries and task cases with observable assertions. Its deliberately flawed plugin snippets are text fixtures for review and planning, not an installable plugin. The pytest check only verifies that the cases and fixture paths are usable. It does not run an agent or grade its behavior.

For a skill change, choose the relevant cases and start each run with clean context and disposable files. Follow each case's setup requirements. Never remove existing skills from a user's client to simulate a missing companion. If isolation or a real companion is unavailable, record that case as untested. A description-only classification is a useful preliminary check, but activation requires observing a real client load the skill.

Compare runs with the skill against runs without it, or against the previous revision. Keep the model, prompt, fixtures, tool permissions, and companion availability unchanged. Give the runner the prompt and files without the expected output or grading assertions. Waivers belong only to cases that explicitly include them. Run each companion scenario separately so one case's waiver cannot leak into another.

Grade the output and tool trace against each assertion, citing evidence for a pass. Check whether the agent respected read-only requests, retained project tools, loaded the relevant references, and stopped when required companions were missing. Record the skill revision or diff, client and model versions, companion sources and availability, commands actually run, and any unavailable timing or token measurements. Keep results outside distributed skills. Review prose with Humanizer and a human reader rather than a banned-word test.

These cases cover instruction handling, not implementation quality. For changes to implementation guidance, also run a disposable installed-plugin task and its tests. Keep native discovery, trigger evaluations, instruction scenarios, and installed-plugin execution separate in reports. Start with a few cases and expand where observed failures justify it. The upstream guides explain [task evaluation](https://agentskills.io/skill-creation/evaluating-skills) and [trigger evaluation](https://agentskills.io/skill-creation/optimizing-descriptions).

## Propose the change

Keep changes focused and describe the problem and resulting behavior. Update [CHANGELOG.md](CHANGELOG.md) for user-visible guidance, installation, or packaging changes. Follow the PR template. Share check results separately from the PR description.

Report security concerns through the private route in [SECURITY.md](SECURITY.md). Contributions of original material use [Apache License 2.0](LICENSE). Retain the applicable licenses and attribution for adapted material.
