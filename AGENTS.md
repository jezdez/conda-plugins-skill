# Repository guidance

This repository maintains the portable `conda-plugins` skill for people developing conda plugins. Its deliverable is the content under `skills/conda-plugins/`, installed from Git or packaged as a text-only conda package. It is not a conda plugin or an installable Python package. Pixi tasks invoke maintained tools to validate and package that content.

## Structure and scope

- Keep installation and client setup in the root `README.md`.
- Keep each `skills/<name>/SKILL.md` short and route substantial guidance to its `references/` directory. Installed skill folders must work on their own.
- Maintain original instructions, concrete examples, and optional pinned provenance. A source link must not substitute for the guidance a colleague needs.
- Keep tool commands in `pixi.toml` and hook rules in `.pre-commit-config.yaml`. Package checks belong in the conda recipe. Do not add a tests directory or custom check or packaging scripts when maintained tools suffice.
- Maintain behavioral prompts in root `evals/evals.json` using upstream skill-creator's schema. Use its grading and human-review tools in disposable workspaces. Keep evals and generated results outside distributed skill folders.
- Generated output belongs in ignored `dist/`. Keep it out of the repository root.
- The conda package is `agent-skill-conda-plugins`, uses `noarch: generic`, and installs the complete skill under `share/agent-skills/conda-plugins`. Keep package output under `dist/conda/noarch/` and companions separate.
- Use this checkout and preserve unrelated changes. Do not create another checkout, edit source plugin repositories, or change publication destinations without authorization.
- The GitHub repository is `jezdez/conda-plugins-skill`. Keep repository URLs consistent with that name.

## Skill content

Preserve compatibility with Codex, Claude Code, and Kilo. Use relative links within each skill folder and verify the complete folder is copied by installation tools. Do not assume a local checkout path, a client-specific tool name, or native plugin hooks.

Superpowers, Humanizer, and Ponytail remain required companions for the conda plugin workflow. Codex Security remains optional and applies to an authorized security review. Changes to those requirements need an explicit task requirement.

Read the existing reference before adding another rule. Synthesize reusable decisions from actual plugin instructions and implementations. Distinguish shared defaults from a source project's local choices. Update pinned provenance when changing a sourced claim. Respect standard argparse behavior and reuse conda APIs in examples.

Write user documentation for people. Develop explanations and complete worked examples, use Diátaxis, and apply Humanizer without removing useful depth. The compact skill entry point does not impose a length limit on human-facing documentation. Keep prose direct, avoid semicolons and vague labels, and preserve upstream license text verbatim.

Original work uses Apache License 2.0. Keep the root and each distributed skill's `LICENSE` identical. Preserve applicable upstream attribution and license terms in the skill's `THIRD_PARTY_NOTICES.md`. Companion repositories are installed separately and are not bundled here.

## Tooling and checks

Use the locked Pixi environment. After changing dependencies, tasks, or platforms in `pixi.toml`, run `pixi lock` and include `pixi.lock` in the change.

```sh
pixi run --locked check
pixi run --locked build-conda
pixi run --locked prek
```

`check` runs prek with built-in metadata checks and a named Pixi task for Lychee local links and anchors. Avoid recursive hooks that invoke `check` or `prek`. The conda recipe checks its copied payload and installed files. Verify standalone references and package inventory manually before release. There is no repository Python test suite.

The conda build command is `pixi run --locked build-conda`, calling rattler-build directly with recipe-native copying and tests. Verify conda payloads and conda-skills discovery, inspection, linking, status, and unlinking through the generic `agents` and `claude` backends in disposable environments. Check pixi-skills separately when claiming its support. Package discovery does not prove native agent-client discovery. Historical client checks and earlier `agent-skill-conda-plugin-skill` package checks do not verify the current artifact.

For changed code examples or behavior claims, execute the affected examples in a disposable environment. Check documentation markup and recordings when those examples change. Prose-only corrections do not require unrelated conda, Sphinx, or platform runs. For changes to instructions, use a realistic independent application scenario when it would reveal a gap that static validation cannot find.

Do not install skills into the user's global client directories during verification. Keep temporary installation checks isolated. Report local checks, actual client invocation, hosted CI, and publication separately. After a push, take at most one CI snapshot unless asked to monitor it.

## Releases

Follow the release procedure in `CONTRIBUTING.md`. The canonical version is `recipe/recipe.yaml`'s `package.version`, currently `'26.11.1'`, with `build.number: 0`, released on 2026-11-11. Use UTC `YY.M.P` versions with an unpadded month, `P` starting at `0` each month, and `vYY.M.P` tags. Content changes require a new version. Packaging-only rebuilds increment the build number separately.

The 26.11.0 release retains the `conda-plugin-skill` skill and ZIP names and the `agent-skill-conda-plugin-skill` package name. Preserve its assets and changelog history when documenting the current names and repository URL.

Require a clean reviewed commit and passing CI before a release tag. Creating and pushing an annotated `vYY.M.P` tag is a publication action requiring explicit authorization. The tag-driven Release workflow waits for every reusable Checks job, then attests the canonical Linux conda package and manifest, creates a draft, uploads the package through the protected `anaconda` environment, and publishes the GitHub draft only after upload succeeds. Keep build provenance and CEP 27 evidence bound to the exact artifacts, workflow, commit, tag, and channel. Verify unchanged draft assets before final publication. Packaging-only rebuilds remain outside this workflow's scope.

The Anaconda.org destination is public owner `jezdez`, label `main`. Configure the environment's reviewer, release-tag deployment policy, and `ANACONDA_API_KEY` separately. Enable GitHub release immutability before publication. Omit embedded recipes with `--no-include-recipe` to exclude local build paths. Refuse overwrites and preserve original artifacts during recovery. Keep tokens private and required companions separate. Do not describe channel availability or native client support from local builds alone.

## Contributions

Follow `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`. Use concise commit subjects and the repository's PR template. Do not prefix PR titles with `[codex]` or put validation commands and output in PR descriptions. Keep review findings in the chat unless their publication is authorized. Opening an issue in another repository requires explicit approval of the proposed issue.
