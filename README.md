# Conda plugin skill

Agent instructions and worked examples for developing conda plugins with Codex, Kilo, or Claude Code. This repository is private and shared with colleagues.

The [conda-plugin-skill](skills/conda-plugin-skill/SKILL.md) helps an agent work through decisions such as which hook to use, how to keep plugin discovery cheap, and how to test the installed plugin. It also covers documentation and terminal demos. The guidance comes from Jannis Leidel's recent conda plugins and their `AGENTS.md` files. Instructions and examples are included in the skill, with [source links](skills/conda-plugin-skill/references/sources.md) for readers who want to trace a recommendation.

The agent reads the references needed for your task and follows your repository's own rules. The skill uses the portable [Agent Skills format](https://agentskills.io/specification), without depending on client-specific tool names, shell-injection features, or lifecycle hooks.

Install it with the three [required companions](#required-companion-skills): Superpowers, Humanizer, and Ponytail.

## Install with npx

Install the skill and choose your client when prompted:

```sh
npx skills add jezdez/conda-plugin-skill
```

Install the required companions from the sources below. The [Skills CLI docs](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) cover client selection, project or global scope, and copy or symlink options.

| Source | Skills to select |
| --- | --- |
| `jezdez/conda-plugin-skill` | `conda-plugin-skill` |
| `obra/superpowers/skills` | All skills |
| `blader/humanizer` | `humanizer` |
| `DietrichGebert/ponytail/skills` | All skills |

You need read access to this repository. Follow the CLI's [private-repository instructions](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#private-repositories) for Git credentials, GitHub CLI, or SSH authentication. Review its [privacy settings](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry) before installing.

Keep complete skill folders, including references and helper scripts. Superpowers and Ponytail refer to files in sibling skills, so install their full collections. On Windows, preserve LF line endings in companion Bash scripts. Review existing installations before replacing them, and only commit private skills and installation lockfiles where their intended audience has access.

### Migrate from conda-plugins

The skill was renamed from `conda-plugins` to `conda-plugin-skill`. Install the new name first and confirm that your client can load it and its references. Then remove the old `conda-plugins` installation in each scope you use to avoid duplicate guidance. Preserve any local edits before removing it. The GitHub repository is now `jezdez/conda-plugin-skill` too.

The renamed skill has not yet been verified through native client discovery. Historical installation results in the [changelog](CHANGELOG.md) apply to the old name.

## Use it

Start a new session in the conda plugin repository you want to work on.

- Codex: enter `$conda-plugin-skill`, followed by your task.
- Claude Code: enter `/conda-plugin-skill`, followed by your task.
- Kilo: ask it to use the `conda-plugin-skill` skill, or choose it from the `/` menu. Use `/reload` after adding or updating skills in an existing session.

For example, in any client:

> Use the conda-plugin-skill to add a conda subcommand in this repository. Read the applicable repository instructions first, identify the development environment and supported conda versions, then implement and test the smallest complete change.

To check that installation worked, ask the client to identify `conda-plugin-skill` and all three required companions, then open the references needed for a sample task. The skill follows the project's `AGENTS.md` and existing client instructions.

## Where the skill goes

Each `conda-plugin-skill` installation contains `SKILL.md`, the complete `references/` directory, `LICENSE`, and `THIRD_PARTY_NOTICES.md`. The parent directories below were checked with Skills CLI 1.7.4 under the old skill name. The renamed destinations still need verification. Its [installer shares the `.agents/skills` directory](https://github.com/vercel-labs/skills/blob/v1.7.4/src/installer.ts#L156-L183) between Codex and Kilo. Consult the CLI's [supported-agent reference](https://github.com/vercel-labs/skills/blob/main/docs/agents.md#supported-agents) for current paths:

| Client | `--agent` value | User installation with `--global` | Project installation |
| --- | --- | --- | --- |
| Codex | `codex` | `~/.agents/skills/conda-plugin-skill/` | `.agents/skills/conda-plugin-skill/` |
| Claude Code | `claude-code` | `~/.claude/skills/conda-plugin-skill/` | `.claude/skills/conda-plugin-skill/` |
| Kilo Code and Kilo CLI | `kilo` | `~/.agents/skills/conda-plugin-skill/` | `.agents/skills/conda-plugin-skill/` |

With copy installation, Codex and Kilo share one copy under `.agents/skills`, while Claude Code has another under `.claude/skills`. Keep both copies updated. Symlink installations share files instead, as described in the CLI's installation docs.

On Windows, `~` means your user profile directory. Custom client home settings can change their configured paths. Current Kilo also supports `.kilo/skills`. Older Kilo extensions used `.kilocode/skills`, so check the documentation for an older installation.

Global installation paths and client discovery were checked on 28 October 2026 with the old `conda-plugins` name. See [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Kilo skills](https://kilo.ai/docs/customize/skills), and [Claude Code skills](https://code.claude.com/docs/en/skills) for client-specific behavior.

## Repository instructions in each client

The skill tells the agent to read applicable instructions explicitly. That remains necessary when working below the directory where the session started.

- Codex discovers instructions along the directory chain to its starting directory. `AGENTS.override.md` takes precedence over `AGENTS.md` at the same level. Read deeper instructions before editing their files. See [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Kilo supports root `AGENTS.md` and loads nested guidance while reading files in those directories. See [Kilo AGENTS.md](https://kilo.ai/docs/customize/agents-md).
- Claude Code 2.1.277 and later can load `AGENTS.md` automatically. By default, this applies when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or above. It does not recognize `AGENTS.override.md`. For older versions, or when a `CLAUDE.md` is already in use, add `@AGENTS.md` to that file with the correct relative path. Preserve its existing instructions. See [Claude Code AGENTS.md support](https://code.claude.com/docs/en/memory#agentsmd).

Do not replace existing instruction files during skill installation. Root instructions should hold shared project rules. Put specialized instructions near their code, and link detailed guides from the relevant instruction file. Review referenced rules when the task reaches that area.

## Inspect and update

Use the CLI's [list](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-list), [check](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-check), and [update](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-update) instructions to inspect installations and apply updates in the intended scope. Include the required companions when reviewing updates. Refresh manual copies yourself.

## Manual installation

If you prefer to copy files yourself, clone the repository or download its ZIP from GitHub:

```sh
gh repo clone jezdez/conda-plugin-skill
cd conda-plugin-skill
mkdir -p "$HOME/.agents/skills"
cp -R skills/conda-plugin-skill "$HOME/.agents/skills/"
mkdir -p "$HOME/.claude/skills"
cp -R skills/conda-plugin-skill "$HOME/.claude/skills/"
```

These are first-install commands. Compare or back up an existing skill before replacing it. The `.agents` copy serves Codex and current Kilo, and the `.claude` copy serves Claude Code. On Windows, copy the whole `skills/conda-plugin-skill/` folder into those directories with Explorer or PowerShell. Keep its reference files together because their links are relative, and update each copy together.

These manual commands copy only `conda-plugin-skill`. Install the three required companions using their upstream instructions below before using the workflow.

## Conda package

The packaging follows [skill-forge](https://github.com/pavelzw/skill-forge): a text-only `noarch: generic` conda package named `agent-skill-conda-plugin-skill`. It installs the complete skill under `share/agent-skills/conda-plugin-skill` in the environment prefix, with no runtime dependencies or activation hooks.

Build it with `pixi run --locked build-conda`, with output under `dist/conda/noarch/`. The ZIP build remains `pixi run --locked build`. Both distributions include the skill's references and license notices. Neither bundles Superpowers, Humanizer, or Ponytail. Install those required companions separately.

[pixi-skills](https://github.com/pavelzw/pixi-skills) links packaged skills into client directories. Use its generic `agents` backend for `.agents/skills/` and its `claude` backend for `.claude/skills/`. With pixi-skills 0.1.7 and Pixi 0.83.0 on macOS arm64, a disposable installation discovered the renamed skill and both backend APIs created relative links exposing all 11 files byte for byte. CLI list/status and link removal also passed. Native Codex, Kilo, and Claude Code discovery through these links has not been tested.

No package has been published, and the private channel is not yet specified. The skill-forge channel is an upstream example, not a publication destination for this repository. Package installation commands will be documented once an authorized channel and tested artifacts exist.

The first release candidate is `26.11.0`, build number `0`, and is not released. The canonical version is `package.version` in `recipe/recipe.yaml`. Releases use UTC calendar versions and tags of the form `vYY.M.P`, with no leading zero on the month. See the [release procedure](CONTRIBUTING.md#release-process) for version rules and the manual approval steps.

## Required companion skills

Superpowers, Humanizer, and Ponytail are required in Codex, Kilo, and Claude Code. Install them through the [Skills CLI](#install-with-npx) or follow their own installation instructions below.

Before plugin work, the agent must confirm that all three companions are available. If one is missing or cannot be loaded, it must report the problem and stop unless you explicitly waive that prerequisite for the task. The agent performs this check because the [Agent Skills format](https://agentskills.io/specification) has no standard field for automatically installing dependencies.

| Skill | Use it for | Installation instructions |
| --- | --- | --- |
| Superpowers | Planning substantial changes, reproducing bugs, useful tests, code review, and evidence before completion claims | [obra/superpowers](https://github.com/obra/superpowers#readme) |
| Humanizer | Documentation, explanations, and review prose that preserve technical facts and read naturally | [blader/humanizer](https://github.com/blader/humanizer#readme) |
| Ponytail | The smallest complete change, reuse of existing APIs, and removal of unnecessary machinery | [DietrichGebert/ponytail installation guide](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md) |

Skills CLI installs portable skills. For native plugin features such as lifecycle hooks, follow each upstream's current instructions for your client. For Claude Code, Superpowers documents `/plugin install superpowers@claude-plugins-official`. Codex users can install Superpowers through the app's Plugins interface or the CLI's `/plugins` interface. Humanizer and Ponytail document their own marketplace or skill-installation options. If you already use a native plugin, check its available skills before installing duplicate copies.

For Kilo, standard skill folders can be placed in its supported skills directory. Preserve each skill's referenced files and confirm that the agent can load them. Copying a skill folder does not enable the source plugin's lifecycle hooks or client-specific tools. Ponytail also documents a native Kilo plugin installation. Superpowers' current README does not document equivalent Kilo lifecycle integration.

Keep companion workflows within your requested scope and repository rules. Small changes still need appropriate checks, and prose edits must preserve technical facts without inventing evidence. Use only the Superpowers workflows the task needs and the client supports.

## Optional Codex Security review

[Codex Security](https://learn.chatgpt.com/docs/security/plugin) can supplement security tests with source review and finding validation. It is optional and does not affect the three companion prerequisites. Use it when available in Codex and a security review is in scope, especially for changes to credentials, request scoping, archive extraction, subprocess execution, or signed evidence.

The [testing guide](skills/conda-plugin-skill/references/testing.md#optional-security-review) explains which scan fits a change and how to report results. Kilo and Claude Code users can follow the same security test cases and review criteria without Codex Security.

## Skill references

Start with [SKILL.md](skills/conda-plugin-skill/SKILL.md), or open a guide for the topic you're working on:

- [Plugin guide](skills/conda-plugin-skill/references/plugin-guide.md) for hook selection, registration, and a complete small plugin.
- [Architecture](skills/conda-plugin-skill/references/architecture.md) for import cost, code ownership, models, dependencies, and errors.
- [CLI and processes](skills/conda-plugin-skill/references/cli-and-processes.md) for arguments, activation, JSON, settings, state writes, and credentials.
- [Formats and solvers](skills/conda-plugin-skill/references/formats-and-solvers.md) for manifests, exporters, package graphs, schema reuse, and target solving.
- [Verification](skills/conda-plugin-skill/references/verification.md) for signed evidence, artifact binding, authorization, offline behavior, and verified caches.
- [Documentation and demos](skills/conda-plugin-skill/references/documentation.md) for worked examples, editing with Humanizer, organizing a site with Diátaxis, building it with Sphinx, MyST, and sphinx-design, and recording VHS GIFs.
- [Testing](skills/conda-plugin-skill/references/testing.md) for runnable discovery tests, regression cases, and startup checks.
- [Sources](skills/conda-plugin-skill/references/sources.md) for optional provenance and pinned source examples.

## Contributing and building an archive

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the editing workflow and [AGENTS.md](AGENTS.md) for repository guidance. The repository uses Pixi for its locked development tools:

```sh
pixi install --locked
pixi run --locked check
pixi run --locked build
```

The build validates the skill and writes `dist/conda-plugin-skill.zip`, including references and license notices. Keep generated archives under `dist/`, where Git ignores them. The archive contains only `conda-plugin-skill`. Install its companions separately using the setup above.

See [CHANGELOG.md](CHANGELOG.md) for changes, [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations, and [SECURITY.md](SECURITY.md) for private reporting.

## Layout

```text
README.md
AGENTS.md
CONTRIBUTING.md
LICENSE
pixi.toml
pixi.lock
recipe/recipe.yaml
evals/evals.json             # maintainer evaluation prompts, not packaged
skills/conda-plugin-skill/
  SKILL.md
  LICENSE
  THIRD_PARTY_NOTICES.md
  references/
    plugin-guide.md
    architecture.md
    cli-and-processes.md
    formats-and-solvers.md
    verification.md
    documentation.md
    testing.md
    sources.md
dist/                       # generated and ignored
```

## License

Copyright 2026 Jannis Leidel. Original material in this repository is licensed under [Apache License 2.0](LICENSE). Applicable upstream licenses and attribution for adapted material are preserved in [THIRD_PARTY_NOTICES.md](skills/conda-plugin-skill/THIRD_PARTY_NOTICES.md) and included in standalone skill distributions.
