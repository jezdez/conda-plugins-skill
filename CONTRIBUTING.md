# Contributing

This repository collects practices for colleagues developing conda plugins with Codex, Claude Code, and Kilo. Useful contributions explain a development decision, provide a worked example, or correct guidance that no longer matches the supported APIs.

Read [AGENTS.md](AGENTS.md) for repository rules and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations. Keep implementation changes in the plugin's own project and document reusable lessons here.

## Set up the repository

Use [Pixi](https://pixi.sh/) to create the locked development environment:

```sh
pixi install --locked
pixi run --locked check
```

The environment contains Python, Lychee, rattler-build, and [prek](https://prek.j178.dev/). Prek runs `.pre-commit-config.yaml`, using its built-in YAML and text checks with the existing license-text exclusions. It does not install the skill or its companions into your agent clients. Follow the [README setup instructions](README.md#install-with-npx) when you want to use them.

Actionlint checks workflow syntax through `pixi run --locked workflows`. The shared Checks workflow runs the pinned upstream `zizmorcore/zizmor-action` once, including during release preparation, with the highest-sensitivity `auditor` persona and online audits. It has no severity or confidence filters and no ignore rules. `advanced-security: false` makes findings fail the job without requiring a code-scanning upload. The action does not expose the CLI's strict-collection or no-ignores switches. Zizmor is not installed in the Pixi environment or run in every matrix build.

The workflow uses GitHub's `$/` self-repository reference for reusable checks. Actionlint 1.7.12 does not recognize that syntax, so its Pixi task excludes only the exact format diagnostic for that reference. Remove this compatibility exception when actionlint supports the syntax. Zizmor audits the reference without suppression.

`pixi run --locked check` runs prek, including the named Pixi `links` task. CI uses the same entry point. Run `pixi run --locked links` to investigate link failures. To opt into automatic Git hooks, run `pixi run --locked install-hooks`. Hook installation is not part of environment setup.

## Change a skill

Start with the reader's task and the existing reference that covers it. Keep `SKILL.md` focused on discovery, essential requirements, and routing. Put substantial examples and domain guidance in the relevant reference. Preserve complete standalone skill folders, including license notices.

Verify API and tool claims against the supported version or current upstream source. Record pinned examples in the source reference. Explain which rules are general defaults and which belong to one source plugin. Apply Humanizer to prose while keeping the technical facts and the detail needed by a human reader.

Run the checks and rebuild the distribution:

```sh
pixi run --locked check
pixi run --locked build-conda
```

Prek checks the skill header and recipe metadata. Lychee checks local Markdown links and anchors without fetching external URLs. Conda payload checks belong in the recipe, including license identity. There is no repository Python test suite. Inspect package inventory, source-file hygiene, and standalone reference access manually before release. These checks do not execute examples or prove that an agent follows the instructions.

The skill's frontmatter contains `name`, `description`, and `license`, in that order, each on one unquoted line. The prek rule requires the exact `conda-plugins` name, Apache-2.0, and a description of at most 1,024 characters starting with a letter and containing no colons or hash characters. This text rule does not validate a general YAML schema or check scalar types. Optional fields and other YAML spellings need an explicit tooling change. Prek also checks YAML file syntax and the recipe's package name, calendar version, and build fields. The recommended entry-point budget of 500 lines and 5,000 tokens is an editorial guideline. Exceeding it is not a format error.

When changing `pixi.toml`, run `pixi lock` and include the updated lockfile. `pixi run --locked build-conda` builds the complete skill folder into a package under `dist/conda/noarch/`. Generate checksums from the actual release artifacts. Generated files stay untracked and out of the repository root. Inspect the package before sharing it with the intended audience.

## Test installation on Linux, macOS, and Windows

Installation is a manual smoke test using upstream tools, separate from repository CI. Use a disposable project and isolated client homes, with no existing user installations. Record the OS, client and installer versions, source revision, and package checksum. Install the skill and companions using the [README instructions](README.md#install-with-npx). When testing unpublished changes, select the local source folder instead of the default branch.

Compare the installed file inventory and bytes with the source, check relative reference links and companion helper scripts, then ask each intended client to list and load the skill. On Windows, preserve LF endings for Bash helpers. Do not claim model execution or native plugin hooks were tested unless you actually exercised them. Keep results in ignored `dist/` or another private, disposable location.

The changelog records client checks of an earlier `conda-plugins` revision and package-link checks of `conda-plugin-skill`. Those results do not verify the current `agent-skill-conda-plugins` artifact. Install the conda artifact into a disposable source environment and use conda-skills to list, inspect, link, check status, and unlink through its `agents` and `claude` backends in a disposable project. Compare every installed file with the source, check relative links, and confirm that unlinking preserves the package. Check pixi-skills separately when claiming its backend support. Verify native agent-client discovery separately from package discovery and Skills CLI copying. Do not install into a user's global client directories for verification. Install required companions separately in the isolated setup.

## Release process

The [Release workflow](.github/workflows/release.yml) starts when an authorized annotated `vYY.M.P` tag is pushed. It validates the tag, runs the complete reusable Checks workflow, attests the canonical Linux artifacts, creates a GitHub draft, uploads the conda package to Anaconda.org, and publishes the GitHub release after that upload succeeds. Branch checks remain separate. Tag publication depends on all jobs in the reusable workflow, including the native matrix and workflow audit.

The canonical release version is `package.version` in `recipe/recipe.yaml`, currently the unreleased candidate `'26.11.2'`, with `build.number: 0`. Version 26.11.1 was released on 2026-11-11. Versions use UTC `YY.M.P`, with an unpadded month and `P` starting at `0` each month. For example, November 2026 starts at `26.11.0`, followed by `26.11.1`. If a candidate is released in a later month, update its version before tagging.

Changes to distributed skill content require a new version. Packaging-only rebuilds increment `build.number` separately and keep the content version unchanged. Reset the build number to `0` for new content. The release workflow currently accepts only content releases with a zero build number. Packaging-only rebuilds need a separately reviewed tag and publication procedure. Never move a published tag or replace a published artifact.

### Configure publication

Enable **Settings > General > Releases > Enable release immutability** before publication. Create an `anaconda` GitHub environment with a required maintainer reviewer and a deployment policy permitting release tags matching `v*.*.*`. Disable administrator bypass. For a sole maintainer, allow self-review so the release can be approved. The previous `release` environment is not used by the tag-driven workflow.

Store a channel-scoped upload credential as `ANACONDA_API_KEY` in the `anaconda` environment. It must permit uploading to owner `jezdez`, label `main`. The workflow exposes it only to the upload step. Keep the token out of Git, logs, and chat. A workflow's environment declaration does not configure its reviewer rules or secrets. Verify those live settings separately.

The repository must be public for the configured GitHub artifact attestations without an Enterprise plan. Public packages include the complete skill, references, license notices, and package metadata. Public attestations expose signer identity and artifact metadata. Review both before publication. Builds use `--no-include-recipe` to exclude rendered recipes containing absolute build-machine paths. The maintained recipe remains in Git, and companion skills remain separate installations.

### Prepare and release

1. Review the recipe, changelog, and relevant evaluations. Run the local checks and package integration checks. Use a clean reviewed commit on `main`, with passing Checks CI at that exact SHA before tagging.
2. With explicit release authorization, create and push the matching annotated `vYY.M.P` tag. The workflow requires a canonical calendar version in the current UTC month, an annotated tag pointing to the workflow commit on `main`, matching recipe metadata, zero build number, and a matching nonempty changelog section.
3. The full reusable Checks workflow runs on Linux, macOS, and Windows. Only after every job succeeds does the draft job use the canonical Linux conda package from that run. Other platform builds validate compatibility. No build or package code runs in the attestation and draft job.
4. The draft job signs the conda package and manifest with GitHub build provenance. It also creates CEP 27 publication evidence for `https://conda.anaconda.org/jezdez`. Verification binds that evidence to the exact bytes, repository, release workflow, commit, tag, and GitHub OIDC issuer. The draft retains both bundles and `SHA256SUMS` alongside the package and manifest.
5. Review the draft's five assets: the conda package, `release-manifest.json`, `build-provenance.sigstore.json`, the package's CEP 27 bundle, and `SHA256SUMS`. Approve the protected `anaconda` job. The publisher checks their stored checksums and the unchanged tag, inspects the package's internal name, version, build, and noarch fields, and refuses an existing or unverifiable channel release. It uploads the exact checked package without rebuilding, force overrides, or user uploader configuration.
6. After the upload succeeds, the final job checks that the tag and every draft asset still match this run's stored artifacts, then publishes the GitHub draft. Release immutability locks the tag and assets. Titles and notes remain editable, so they are not a substitute for the signed manifest.

The manifest records the repository, source commit, tag, version, build number, workflow commit, run URL, attempt, and canonical platform. Changelog notes come from the tagged commit. The uploaded files are reused throughout the pipeline.

The published 26.11.0 release retains the `conda-plugin-skill` ZIP and skill-folder names and the `agent-skill-conda-plugin-skill` package name. Keep its assets and changelog history unchanged. Release 26.11.1 uses `conda-plugins` and `agent-skill-conda-plugins`.

After publication, verify the immutable release with `gh release verify TAG` and downloaded files with `gh release verify-asset TAG FILE`, substituting the actual tag and filename. Confirm the channel package's version and digest, then exercise a disposable channel installation with conda-skills. Report hosted CI, Anaconda publication, GitHub publication, and native client discovery separately. Update the changelog's release status without moving the tag.

### Recover a partial release

Publication across services is not atomic. A failure after the Anaconda upload can leave a published channel package and a GitHub draft. Inspect the failed step and both destinations before retrying. The normal publisher refuses an existing Anaconda release and never overwrites files.

Keep the original artifacts and attestation bundles. If only GitHub finalization failed, verify the channel package and the draft's exact bytes, then finalize that draft with explicit authorization. Do not repeat the upload or rebuild packages. If the upload result is ambiguous, compare remote bytes before retrying. A failed verification step is not proof that an upload failed.

Workflow artifacts expire after seven days and their names include the run attempt. Rerunning only failed jobs cannot retrieve another attempt's artifacts. Inspect the existing draft before choosing a recovery action. The normal draft job refuses any existing release and never uses `--clobber`. Deleting an unpublished draft requires maintainer approval and another artifact review. Never delete a published release to reuse a version.

For each new release, verify publication before documenting channel availability. The publication destination is the public `jezdez` channel's `main` label on Anaconda.org.

## Evaluate skill behavior

Use the upstream [skill-creator skill](https://github.com/anthropics/skills/tree/main/skills/skill-creator) for behavioral evaluations, following the [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills). It provides paired runs, assertion grading, benchmark aggregation, and a human review viewer. Install it separately in an isolated evaluation environment. It is a maintainer tool, not another required companion for plugin users. Its Claude-specific automation does not establish Codex or Kilo behavior.

The initial integration uses upstream revision `ca45fc496a3436251f191354091d557da31c15b5`. Its `references/schemas.md` names the eval checks `expectations`, though parts of its prose call them assertions. Preserve that schema and use `text`, `passed`, and `evidence` in grading results. Its aggregator expects `eval-<id>/<configuration>/run-<number>/grading.json`. Put `eval_metadata.json` beside each run's `outputs/` for the viewer as well as at eval level for aggregation.

After grading, create a local review page with upstream `eval-viewer/generate_review.py` and `--static`. The pinned aggregator fills missing measurements with zero and uses placeholder model/run-count metadata. Check its output before reporting a benchmark. If timing and tokens are unavailable, omit the benchmark from the viewer and report expectation counts with that limitation. Do not report those zeros as measurements. The viewer loads some resources from third-party CDNs, so inspect its dependencies before opening private outputs under a restrictive network policy. Open static reviews as local files and submit feedback to download `feedback.json` before closing. Keep original grades when correcting an ambiguous expectation, and distinguish rubric changes from skill improvements.

The maintained prompts are in [evals/evals.json](evals/evals.json), using skill-creator's `skill_name`, integer `id`, `prompt`, `expected_output`, `files`, and `expectations` fields. This file is outside the distributed skill. Copy it into `evals/evals.json` inside a disposable skill copy under ignored `dist/` or a temporary directory to follow the upstream layout. Keep results in that copy's sibling workspace. Do not add a custom runner or a `tests/` directory, and do not include evaluation inputs or outputs in release artifacts. Record the upstream skill-creator revision used.

The initial cases cover an installed subcommand, which requires actual execution, and a read-only review of instruction handling and project-tool retention. Both explicitly waive companions to isolate this skill's contribution. These cases do not validate companion discovery or missing-companion enforcement. Add those as separate evaluations with real isolated client configurations, not invented availability.

Start each run with clean context and disposable files. Never remove existing skills from a user's client to simulate a missing companion. If isolation or a real companion is unavailable, record that case as untested. Description-only classification is a preliminary check. To verify activation, observe a real client loading the skill.

Compare runs with the skill against runs without it, or against the previous revision. Keep the model, prompt, fixtures, tool permissions, and companion availability unchanged. Give the runner the prompt and files without the expected output or grading assertions. Waivers belong only to cases that explicitly include them. Run each companion scenario separately so one case's waiver cannot leak into another.

For an installed-plugin comparison, give both runners the same pinned conda and Python versions. If agents select their own runtimes, report the versions and note any differences that limit the comparison. Lazy registration can distinguish designs without demonstrating a performance benefit for a tiny plugin. Do not interpret that assertion alone as improved task quality.

Grade the output and tool trace against each assertion, citing evidence for a pass. Check whether the agent respected read-only requests, retained project tools, loaded the relevant references, and stopped when required companions were missing. Record the skill revision or diff, client and model versions, companion sources and availability, commands actually run, and any unavailable timing or token measurements. Keep results outside distributed skills. Review prose with Humanizer and a human reader rather than a banned-word test.

Report native discovery, trigger evaluations, instruction scenarios, and installed-plugin execution separately. A human must review the upstream viewer's outputs before accepting the evaluation. Start with a few cases and expand where observed failures justify it. The upstream guides explain [task evaluation](https://agentskills.io/skill-creation/evaluating-skills) and [trigger evaluation](https://agentskills.io/skill-creation/optimizing-descriptions).

## Propose the change

Keep changes focused and describe the problem and resulting behavior. Update [CHANGELOG.md](CHANGELOG.md) for user-visible guidance, installation, or packaging changes. Follow the PR template. Share check results separately from the PR description.

Report security concerns through the private route in [SECURITY.md](SECURITY.md). Contributions of original material use [Apache License 2.0](LICENSE). Retain the applicable licenses and attribution for adapted material.
