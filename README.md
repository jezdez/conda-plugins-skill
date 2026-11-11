# Conda plugin skill

Agent instructions and worked examples for developing conda plugins with Codex, Kilo, or Claude Code.

The [conda-plugins](skills/conda-plugins/SKILL.md) skill helps an agent work through decisions such as which hook to use, how to keep plugin discovery cheap, and how to test the installed plugin. It also covers documentation and terminal demos. The guidance comes from Jannis Leidel's recent conda plugins and their `AGENTS.md` files. Instructions and examples are included in the skill, with [source links](skills/conda-plugins/references/sources.md) for readers who want to trace a recommendation.

The agent reads the references needed for your task and follows your repository's own rules. The skill uses the portable [Agent Skills format](https://agentskills.io/specification), without depending on client-specific tool names, shell-injection features, or lifecycle hooks.

Choose either [npx](#install-with-npx) or [conda](#conda-package) to install `conda-plugins`. Both routes require the three [companion skills](#required-companion-skills): Superpowers, Humanizer, and Ponytail.

## Install with npx

Install the skill and choose your client when prompted:

```sh
npx skills add jezdez/conda-plugins-skill --skill conda-plugins
```

### Install the companions

Run these commands whether you installed `conda-plugins` through npx, Git, or conda. Choose the same client and installation scope as the main skill:

```sh
npx skills add https://github.com/obra/superpowers/tree/main/skills --skill '*'
npx skills add blader/humanizer --skill humanizer
npx skills add https://github.com/DietrichGebert/ponytail/tree/main/skills --skill '*'
```

The quoted `'*'` selects every skill in the Superpowers and Ponytail collections. Keep the quotes so your shell passes it literally. Client, project or global scope, and copy or symlink choices remain interactive. The [Skills CLI docs](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) describe these options.

Review the CLI's [privacy settings](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry) before installing.

Keep complete skill folders, including references and helper scripts. Superpowers and Ponytail refer to files in sibling skills, so install their full collections. On Windows, preserve LF line endings in companion Bash scripts. Review existing installations before replacing them.

## Use it

Start a new session in the conda plugin repository you want to work on.

- Codex: enter `$conda-plugins`, followed by your task.
- Claude Code: enter `/conda-plugins`, followed by your task.
- Kilo: ask it to use the `conda-plugins` skill, or choose it from the `/` menu. Use `/reload` after adding or updating skills in an existing session.

For example, in any client:

> Use the conda-plugins skill to add a conda subcommand in this repository. Read the applicable repository instructions first, identify the development environment and supported conda versions, then implement and test the smallest complete change.

To check that installation worked, ask the client to identify `conda-plugins` and all three required companions, then open the references needed for a sample task. The skill follows the project's `AGENTS.md` and existing client instructions.

## Where the skill goes

Each `conda-plugins` installation contains `SKILL.md`, the complete `references/` directory, `LICENSE`, and `THIRD_PARTY_NOTICES.md`. Skills CLI 1.7.4's [installer shares the `.agents/skills` directory](https://github.com/vercel-labs/skills/blob/v1.7.4/src/installer.ts#L156-L183) between Codex and Kilo. Consult the CLI's [supported-agent reference](https://github.com/vercel-labs/skills/blob/main/docs/agents.md#supported-agents) for current paths:

| Client | `--agent` value | User installation with `--global` | Project installation |
| --- | --- | --- | --- |
| Codex | `codex` | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |
| Claude Code | `claude-code` | `~/.claude/skills/conda-plugins/` | `.claude/skills/conda-plugins/` |
| Kilo Code and Kilo CLI | `kilo` | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |

With copy installation, Codex and Kilo share one copy under `.agents/skills`, while Claude Code has another under `.claude/skills`. Keep both copies updated. Symlink installations share files instead, as described in the CLI's installation docs.

On Windows, `~` means your user profile directory. Custom client home settings can change their configured paths. Current Kilo also supports `.kilo/skills`. Older Kilo extensions used `.kilocode/skills`, so check the documentation for an older installation.

Global installation paths and client discovery were checked on 28 October 2026 with an earlier `conda-plugins` revision. Those results do not verify the current content or conda package. See [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Kilo skills](https://kilo.ai/docs/customize/skills), and [Claude Code skills](https://code.claude.com/docs/en/skills) for client-specific behavior.

## Repository instructions in each client

The skill tells the agent to read applicable instructions explicitly. That remains necessary when working below the directory where the session started.

- Codex discovers instructions along the directory chain to its starting directory. `AGENTS.override.md` takes precedence over `AGENTS.md` at the same level. Read deeper instructions before editing their files. See [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Kilo supports root `AGENTS.md` and loads nested guidance while reading files in those directories. See [Kilo AGENTS.md](https://kilo.ai/docs/customize/agents-md).
- Claude Code 2.1.277 and later can load `AGENTS.md` automatically. By default, this applies when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or above. It does not recognize `AGENTS.override.md`. For older versions, or when a `CLAUDE.md` is already in use, add `@AGENTS.md` to that file with the correct relative path. Preserve its existing instructions. See [Claude Code AGENTS.md support](https://code.claude.com/docs/en/memory#agentsmd).

Do not replace existing instruction files during skill installation. Root instructions should hold shared project rules. Put specialized instructions near their code, and link detailed guides from the relevant instruction file. Review referenced rules when the task reaches that area.

## Inspect and update

Use the CLI's [list](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-list), [check](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-check), and [update](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-update) instructions to inspect installations and apply updates in the intended scope. Include the required companions when reviewing updates. Refresh manual copies yourself.

If you installed `conda-plugin-skill`, install and verify `conda-plugins` in the same client and scope before removing the old installation with its original installer. For conda-linked installations, unlink the old skill before removing the `agent-skill-conda-plugin-skill` package. Update explicit invocations to `$conda-plugins` or `/conda-plugins`. The repository is now `jezdez/conda-plugins-skill`.

## Manual installation

If you prefer to copy files yourself, clone the repository:

```sh
gh repo clone jezdez/conda-plugins-skill
cd conda-plugins-skill
mkdir -p "$HOME/.agents/skills"
cp -R skills/conda-plugins "$HOME/.agents/skills/"
mkdir -p "$HOME/.claude/skills"
cp -R skills/conda-plugins "$HOME/.claude/skills/"
```

These are first-install commands. Compare or back up an existing skill before replacing it. The `.agents` copy serves Codex and current Kilo, and the `.claude` copy serves Claude Code. On Windows, copy the whole `skills/conda-plugins/` folder into those directories with Explorer or PowerShell. Keep its reference files together because their links are relative, and update each copy together.

These manual commands copy only `conda-plugins`. Install the three required companions with the [commands above](#install-the-companions) before using the workflow.

## Conda package

The packaging follows [skill-forge](https://github.com/pavelzw/skill-forge): a text-only `noarch: generic` conda package named `agent-skill-conda-plugins`. It installs the complete skill under `share/agent-skills/conda-plugins` in the environment prefix, with no runtime dependencies or activation hooks.

The package includes the skill's references and license notices. Install the required Superpowers, Humanizer, and Ponytail companions with the [npx commands above](#install-the-companions). The conda and npx routes are alternatives for `conda-plugins`.

[conda-skills](https://github.com/jezdez/conda-skills) discovers the installed package and links it into client directories. Install that plugin in the environment running conda, following its installation instructions. Install the skill package from the public `jezdez` channel's `main` label into your active source environment:

```sh
conda install jezdez::agent-skill-conda-plugins
```

Then run from your project directory:

```sh
conda skill list
conda skill inspect conda-plugins
conda skill link conda-plugins
conda skill status
```

These commands use the active source environment and the project's `.agents/skills/` destination. Use `-n NAME` or `-p PREFIX` on `conda install` and on `conda skill list`, `inspect`, and `link` to select another source environment. Use `--backend claude` for `.claude/skills/`, or explicit `--global` for home destinations. `conda skill unlink conda-plugins` removes the project link without deleting the installed package. Required companions still need separate installation.

[pixi-skills](https://github.com/pavelzw/pixi-skills) also supports this package layout through its `agents` and `claude` backends. Native Codex, Kilo, and Claude Code discovery through these links has not been tested.

Version [26.11.1](https://github.com/jezdez/conda-plugins-skill/releases/tag/v26.11.1), build number `0`, was released on 2026-11-11. The package is available from [jezdez on Anaconda.org](https://anaconda.org/jezdez/agent-skill-conda-plugins).

Version [26.11.0](https://github.com/jezdez/conda-plugins-skill/releases/tag/v26.11.0) is released. Its ZIP and installed skill retain the `conda-plugin-skill` name, and its conda package is `agent-skill-conda-plugin-skill`. Those artifacts do not provide the current `conda-plugins` identifier.

The canonical version is `package.version` in `recipe/recipe.yaml`. Releases use UTC calendar versions and tags of the form `vYY.M.P`, with no leading zero on the month. An authorized release tag triggers cross-platform checks, artifact signing, a protected Anaconda.org upload, and GitHub publication after that upload succeeds. See the [release procedure](CONTRIBUTING.md#release-process) for setup and approval steps.

## Required companion skills

Superpowers, Humanizer, and Ponytail are required in Codex, Kilo, and Claude Code. Install them with the [companion commands above](#install-the-companions) or follow their own installation instructions below.

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

The [testing guide](skills/conda-plugins/references/testing.md#optional-security-review) explains which scan fits a change and how to report results. Kilo and Claude Code users can follow the same security test cases and review criteria without Codex Security.

## Skill references

Start with [SKILL.md](skills/conda-plugins/SKILL.md), or open a guide for the topic you're working on:

- [Plugin guide](skills/conda-plugins/references/plugin-guide.md) for hook selection, registration, and a complete small plugin.
- [Architecture](skills/conda-plugins/references/architecture.md) for import cost, code ownership, models, dependencies, and errors.
- [CLI and processes](skills/conda-plugins/references/cli-and-processes.md) for arguments, activation, JSON, settings, state writes, and credentials.
- [Formats and solvers](skills/conda-plugins/references/formats-and-solvers.md) for manifests, exporters, package graphs, schema reuse, and target solving.
- [Verification](skills/conda-plugins/references/verification.md) for signed evidence, artifact binding, authorization, offline behavior, and verified caches.
- [Documentation and demos](skills/conda-plugins/references/documentation.md) for worked examples, editing with Humanizer, organizing a site with Diátaxis, building it with Sphinx, MyST, and sphinx-design, and recording VHS GIFs.
- [Testing](skills/conda-plugins/references/testing.md) for runnable discovery tests, regression cases, and startup checks.
- [Sources](skills/conda-plugins/references/sources.md) for optional provenance and pinned source examples.

## Contributing and building a conda package

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the editing workflow and [AGENTS.md](AGENTS.md) for repository guidance. The repository uses Pixi for its locked development tools:

```sh
pixi install --locked
pixi run --locked check
pixi run --locked build-conda
```

The build validates the skill, creates the conda package under `dist/conda/noarch/`, and tests its installed payload. Keep generated files under `dist/`, where Git ignores them.

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
skills/conda-plugins/
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

Copyright 2026 Jannis Leidel. Original material in this repository is licensed under [Apache License 2.0](LICENSE). Applicable upstream licenses and attribution for adapted material are preserved in [THIRD_PARTY_NOTICES.md](skills/conda-plugins/THIRD_PARTY_NOTICES.md) and included in standalone skill distributions.
