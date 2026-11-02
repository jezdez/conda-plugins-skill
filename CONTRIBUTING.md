# Contributing

This repository collects practices for colleagues developing conda plugins with Codex, Claude Code, and Kilo. Useful contributions explain a development decision, provide a worked example, or correct guidance that no longer matches the supported APIs.

Read [AGENTS.md](AGENTS.md) for repository rules and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations. If the question concerns a particular plugin's implementation, use this repository to improve the general guidance and keep implementation changes in that plugin's own project.

## Set up the repository

Use [Pixi](https://pixi.sh/) to create the locked development environment:

```sh
pixi install --locked
pixi run --locked check
```

The environment contains Python, Lychee, rattler-build, and [prek](https://prek.j178.dev/). Prek runs `.pre-commit-config.yaml`, using its built-in YAML and text checks with the existing license-text exclusions. It does not install the skill or its companions into your agent clients. Follow the [README setup instructions](README.md#install-with-npx) when you want to use them.

Actionlint validates workflows through `pixi run --locked workflows`. The shared Checks workflow also runs the pinned upstream `zizmorcore/zizmor-action` once, including during release preparation, with the highest-sensitivity `auditor` persona and online audits. No severity or confidence filters are set. `advanced-security: false` makes findings fail the job without requiring paid code scanning for this private repository. No zizmor ignore rules are configured. The action does not expose the CLI's strict-collection or no-ignores switches; actionlint separately checks workflow syntax. Zizmor is not installed in the Pixi environment or run in every matrix build.

The workflow uses GitHub's `$/` self-repository reference for reusable checks. Actionlint 1.7.12 does not recognize that syntax, so its Pixi task excludes only the exact format diagnostic for that reference. Remove this compatibility exception when actionlint supports the syntax. Zizmor audits the reference without suppression.

`pixi run --locked check` runs prek, including the named Pixi `links` task. CI uses the same entry point. Run `pixi run --locked links` to investigate link failures. To opt into automatic Git hooks, run `pixi run --locked install-hooks`. Hook installation is not part of environment setup.

## Change a skill

Start with the reader's task and the existing reference that covers it. Keep `SKILL.md` focused on discovery, essential requirements, and routing. Put substantial examples and domain guidance in the relevant reference. Preserve complete standalone skill folders, including license notices.

Verify API and tool claims against the supported version or current upstream source. Record pinned examples in the source reference. Explain which rules are general defaults and which belong to one source plugin. Apply Humanizer to prose while keeping the technical facts and the detail needed by a human reader.

Run the checks and rebuild the distribution:

```sh
pixi run --locked check
pixi run --locked build
pixi run --locked build-conda
```

Prek checks the skill header and recipe metadata. Lychee checks local Markdown links and anchors without fetching external URLs. Conda payload checks belong in the recipe, including license identity. The ZIP build checks archive integrity with `python -m zipfile --test`. There is no repository Python test suite. Inspect ZIP inventory, source-file hygiene, and standalone reference access manually before release. These checks do not execute examples or prove that an agent follows the instructions.

The skill uses a deliberately small frontmatter format: `name`, `description`, and `license`, in that order, each on one unquoted line. The prek rule requires the exact `conda-plugin-skill` name, Apache-2.0, and a description of at most 1,024 characters starting with a letter and containing no colons or hash characters. This is a targeted text rule, not general YAML schema validation or scalar-type checking. Optional fields and other YAML spellings need an explicit tooling change. Prek also checks YAML file syntax and the recipe's package name, calendar version, and build fields. The recommended entry-point budget of 500 lines and 5,000 tokens remains an editorial guideline, not a format error.

When changing `pixi.toml`, run `pixi lock` and include the updated lockfile. `pixi run --locked build` uses `python -m zipfile` to write `dist/conda-plugin-skill.zip`. It includes the complete skill folder and preserves source file timestamps, so byte-reproducible ZIP output is no longer guaranteed. Generate checksums from the actual release artifacts. Generated files stay untracked and out of the repository root. Inspect the ZIP before sharing it with the intended audience.

## Test installation on Linux, macOS, and Windows

Installation is a manual smoke test using upstream tools, separate from repository CI. Use a disposable project and isolated client homes, with no existing user installations. Record the OS, client and installer versions, source revision, and package checksum. Install the skill and companions using the [README instructions](README.md#install-with-npx). When testing unpublished changes, select the local source folder instead of the default branch.

Compare the installed file inventory and bytes with the source, check relative reference links and companion helper scripts, then ask each intended client to list and load the skill. On Windows, preserve LF endings for Bash helpers. Do not claim model execution or native plugin hooks were tested unless you actually exercised them. Keep results in ignored `dist/` or another private, disposable location.

The changelog's recorded hosted results used the old `conda-plugins` name. They do not verify native discovery of `conda-plugin-skill`. For conda packages, test pixi-skills links through its generic `agents` and `claude` backends in disposable project directories. Check the selected version's backend support, the complete installed skill, relative references, and discovery in each intended client. Keep these results separate from Skills CLI copy-installation results. Do not install into a user's global client directories for verification. Required companions must be installed separately in the isolated setup.

## Release process

Releases are manual and opt-in. The [Prepare release workflow](.github/workflows/release.yml) checks an existing tag, builds both distributions on three platforms, and creates a draft from the Linux artifacts. It never creates tags, publishes releases, or uploads to a conda channel. The conda packaging design follows [skill-forge](https://github.com/pavelzw/skill-forge), but this private repository has no selected channel.

The canonical release version is `package.version` in `recipe/recipe.yaml`, initially the quoted string `'26.11.0'`, with `build.number: 0`. This is an unreleased candidate, not an available release. The `build-conda` task calls rattler-build directly. The recipe compares copied files with the source during the build, enforces a strict package inventory, and checks installed files and reference counts using only Python's standard library. YAML metadata is validated by the repository checks before building. A failed build may leave an artifact under `dist/`. Only use artifacts from successful builds.

Versions use `YY.M.P`, based on the release date in UTC. `YY` is the two-digit year, `M` is the month without leading zeros, and `P` starts at `0` each month and increases for each content release that month. For example, November 2026 starts at `26.11.0`, then `26.11.1`. December starts at `26.12.0`, and January 2027 at `27.1.0`. Tags use the exact version prefixed with `v`, such as `v26.11.0`. If the candidate is released in a later month, update its version before tagging.

Changes to distributed skill content require a new version. A packaging-only rebuild of unchanged content increments `build.number` separately and keeps `package.version` unchanged. Reset the build number to `0` for a new content version. Do not move or reuse a content release tag for a rebuild. Record the rebuild's commit, build number, and checksums separately.

Before the first release, enable **Settings > General > Releases > Enable release immutability**. It applies only to future publications. Create a GitHub environment named `release` with a required maintainer reviewer and restrict it to `main`, where the dispatch runs. Disable administrator bypass, and prevent self-review when another maintainer is available. A sole maintainer must explicitly accept self-approval rather than configure an unusable gate. An environment declaration in YAML alone does not configure approval protection. If required reviewers are unavailable for this private repository's plan, restrict workflow dispatch to trusted maintainers and treat dispatch as explicit draft-creation authorization. The workflow does not change these settings or require an administrator token.

1. Review the recipe, changelog, and relevant skill evaluations. Keep the candidate marked unreleased. Use a clean, reviewed commit on `main`, with passing Checks CI for that exact SHA before tagging.
2. With explicit authorization, create and push the matching `vYY.M.P` tag at that SHA. The first content release uses `build.number: 0`. Never move a published release tag.
3. With explicit draft-creation authorization, run **Prepare release** from the Actions UI on `main`, supplying the existing tag. The workflow validates ancestry, exact recipe version, zero build number, changelog entry, and current UTC year/month. It rejects malformed tags and nonexistent tags. It runs the shared Checks workflow at the resolved commit on Linux, macOS, and Windows.
4. Review and approve the `release` environment job. Only after all checks pass does it download the Linux ZIP and conda package from this run, verify that the tag object has not changed, and create a draft. Windows and macOS builds are compatibility checks, not competing release assets. Build jobs have read-only repository permissions. The write-enabled job does not check out or execute candidate code.
5. Inspect the draft's four assets: `conda-plugin-skill-<version>.zip`, the versioned `.conda` package, `release-manifest.json`, and `SHA256SUMS`. The workflow gives the local ZIP its versioned release filename without rebuilding it or changing its internal `conda-plugin-skill/` directory. The manifest records the source SHA, tag, version, build number, workflow SHA, run URL, and attempt. Download and verify the assets and perform isolated installation checks on those exact files. Do not rebuild them after review. Release notes come from the matching version's changelog section at the tagged commit. Preparation fails if that section is absent or empty. Review these notes, including the evaluation coverage limits.
6. With explicit publication authorization, confirm repository immutability is enabled, the tag still points to the manifest's SHA, and the draft contains exactly the reviewed assets with matching checksums. Publish the draft manually. Verify it with `gh release verify v26.11.0` and verify downloaded files with `gh release verify-asset v26.11.0 <file>`, substituting the actual tag. Update the changelog's release status in a follow-up commit without moving the tag.

Immutable publication locks the tag and assets, including the attached manifest and checksums. GitHub creates a release attestation automatically. Titles and notes remain editable, so they are not a substitute for the manifest. Attestation verifies the published association, not correctness of the skill. See [GitHub's immutable-release documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

Candidate artifacts expire after seven days. Rerun the entire workflow if they expire or if an earlier job failed. Rerunning only failed jobs cannot reuse another attempt's artifacts. The workflow refuses to replace an existing draft or published release and never uses `--clobber`. If asset upload partially fails, inspect the draft and recover it manually using the original run's files and checksums. Deleting an unpublished draft for a full rebuild requires maintainer approval and another review. Never delete a published release to reuse its version.

This workflow handles content releases only. Packaging-only rebuilds with a nonzero build number are rejected until a separately reviewed tag convention and workflow exist for them. They must never append assets to an already published immutable release. Fresh build caches avoid testing an older local package with the same candidate filename.

Do not document a package install command or channel as available before publication. Keep GitHub links pointed at `jezdez/conda-plugin-skill`. Report builds, client checks, hosted CI, tagging, and publication separately.

## Evaluate skill behavior

Use the upstream [skill-creator skill](https://github.com/anthropics/skills/tree/main/skills/skill-creator) for behavioral evaluations, following the [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills). It provides paired runs, assertion grading, benchmark aggregation, and a human review viewer. Install it separately in an isolated evaluation environment. It is a maintainer tool, not another required companion for plugin users. Its Claude-specific automation does not establish Codex or Kilo behavior.

The initial integration uses upstream revision `ca45fc496a3436251f191354091d557da31c15b5`. Its `references/schemas.md` names the eval checks `expectations`, though parts of its prose call them assertions. Preserve that schema and use `text`, `passed`, and `evidence` in grading results. Its aggregator expects `eval-<id>/<configuration>/run-<number>/grading.json`. Put `eval_metadata.json` beside each run's `outputs/` for the viewer as well as at eval level for aggregation.

After grading, use upstream `eval-viewer/generate_review.py` with `--static` to create a review page without a server. The pinned aggregator substitutes zero for missing measurements and supplies placeholder model/run-count metadata. Check its output before reporting a benchmark. When timing and tokens are unavailable, omit the benchmark from the viewer and report expectation counts with that limitation instead. Do not treat zero-filled fields as observations. The viewer loads some resources from third-party CDNs, so inspect its dependencies before opening private outputs under a restrictive network policy. Open static reviews as local files and submit feedback to download `feedback.json` before closing. Keep original grades when correcting an ambiguous expectation, and distinguish rubric changes from skill improvements.

The maintained prompts are in [evals/evals.json](evals/evals.json), using skill-creator's `skill_name`, integer `id`, `prompt`, `expected_output`, `files`, and `expectations` fields. This file is outside the distributed skill. Copy it into `evals/evals.json` inside a disposable skill copy under ignored `dist/` or a temporary directory to follow the upstream layout. Keep results in that copy's sibling workspace. Do not add a custom runner or a `tests/` directory, and do not include evaluation inputs or outputs in release artifacts. Record the upstream skill-creator revision used.

The initial cases cover an installed subcommand and a read-only review retaining project tools. Both explicitly waive companions to isolate this skill's contribution. These cases do not validate companion discovery or missing-companion enforcement. Add those as separate evaluations with real isolated client configurations, not invented availability.

Start each run with clean context and disposable files. Never remove existing skills from a user's client to simulate a missing companion. If isolation or a real companion is unavailable, record that case as untested. A description-only classification is a useful preliminary check, but activation requires observing a real client load the skill.

Compare runs with the skill against runs without it, or against the previous revision. Keep the model, prompt, fixtures, tool permissions, and companion availability unchanged. Give the runner the prompt and files without the expected output or grading assertions. Waivers belong only to cases that explicitly include them. Run each companion scenario separately so one case's waiver cannot leak into another.

For an installed-plugin comparison, provide the same pinned conda and Python versions to both runners. If agents select their own runtimes, disclose the versions and treat differences as a comparison limitation. Lazy registration can distinguish designs without demonstrating a performance benefit for a tiny plugin. Do not interpret that assertion alone as improved task quality.

Grade the output and tool trace against each assertion, citing evidence for a pass. Check whether the agent respected read-only requests, retained project tools, loaded the relevant references, and stopped when required companions were missing. Record the skill revision or diff, client and model versions, companion sources and availability, commands actually run, and any unavailable timing or token measurements. Keep results outside distributed skills. Review prose with Humanizer and a human reader rather than a banned-word test.

The installed-plugin case requires actual execution, while the review case checks instruction handling. Keep native discovery, trigger evaluations, instruction scenarios, and installed-plugin execution separate in reports. A human must review the upstream viewer's outputs before accepting the evaluation. Missing token or timing measurements are unavailable, not zero-cost runs. Start with a few cases and expand where observed failures justify it. The upstream guides explain [task evaluation](https://agentskills.io/skill-creation/evaluating-skills) and [trigger evaluation](https://agentskills.io/skill-creation/optimizing-descriptions).

## Propose the change

Keep changes focused and describe the problem and resulting behavior. Update [CHANGELOG.md](CHANGELOG.md) for user-visible guidance, installation, or packaging changes. Follow the PR template. Share check results separately from the PR description.

Report security concerns through the private route in [SECURITY.md](SECURITY.md). Contributions of original material use [Apache License 2.0](LICENSE). Retain the applicable licenses and attribution for adapted material.
