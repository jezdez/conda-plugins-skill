# Conda plugin skills

A private collection of Agent Skills for colleagues developing conda plugins with Codex, Kilo, or Claude Code.

The [conda-plugins skill](skills/conda-plugins/SKILL.md) synthesizes the development practices in Jannis Leidel's recent conda plugins and their `AGENTS.md` files. It teaches cheap hook registration, code ownership, typed settings, CLI and process behavior, format adapters, exact package inventories, solver targets, and verification through bundled instructions and examples. Its documentation guidance covers expansive writing for human readers, Diátaxis, Sphinx with MyST and sphinx-design, and the shared VHS demo style. Agents load all references relevant to the task and apply the target repository's own rules. External source links are optional provenance.

The skill uses the portable [Agent Skills format](https://agentskills.io/specification). It does not require a particular agent's tool names, shell-injection features, or lifecycle hooks.

The setup command below installs this skill and its three [required companions](#required-companion-skills) for Codex, Claude Code, and Kilo.

## Install with npx

You need read access to this repository, Git, and Node.js 22.20 or later. Authenticate with `gh auth login` if needed, or use your existing Git credentials or SSH keys. The [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#private-repositories) supports private repositories through those credentials.

Paste this single setup command into Bash, Zsh, or Git Bash on Windows. It installs `conda-plugins`, the complete Superpowers and Ponytail skill collections, and Humanizer for all three clients:

```sh
(
  export DISABLE_TELEMETRY=1
  export "GIT_CONFIG_KEY_${GIT_CONFIG_COUNT:-0}=core.autocrlf"
  export "GIT_CONFIG_VALUE_${GIT_CONFIG_COUNT:-0}=false"
  export GIT_CONFIG_COUNT="$(( ${GIT_CONFIG_COUNT:-0} + 1 ))"
  install_skills() {
    npx --yes skills@1.7.4 add "$@" \
      --global --agent codex claude-code kilo --copy --yes --json
  }
  install_skills jezdez/conda-plugin-skills --skill conda-plugins &&
    install_skills obra/superpowers/skills --skill '*' &&
    install_skills blader/humanizer --skill humanizer &&
    install_skills DietrichGebert/ponytail/skills --skill '*'
)
```

Keep only the client names you use after `--agent`. `--global` makes the skills available across your projects. `--copy` preserves complete skill directories without requiring symlinks. The command pins Skills CLI 1.7.4 and installs the current upstream skills. It reports each installation as JSON and stops if an installation fails.

The Git settings apply only while this command runs. They preserve LF line endings so companion shell scripts also work in Git Bash on Windows, and leave your existing Git configuration unchanged.

Both `--yes` flags accept installation prompts, including replacement of matching installed skills. Review existing copies first. To inspect a source before installing it, run `DISABLE_TELEMETRY=1 npx skills@1.7.4 add <source> --list` with one of the four source names above.

`DISABLE_TELEMETRY=1` disables the CLI's telemetry and security-audit requests. npm still supplies the CLI, and GitHub serves the private repository. See the [upstream privacy details](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry).

PowerShell users can run the setup command in Git Bash. For the individual `npx` commands elsewhere in this README, first run `$env:DISABLE_TELEMETRY = '1'`, then omit their `DISABLE_TELEMETRY=1` prefix.

For SSH authentication, replace `jezdez/conda-plugin-skills` with `git@github.com:jezdez/conda-plugin-skills.git`. For a project installation, run the install command from that project's root and omit `--global`. Only commit these private skill files and the generated `skills-lock.json` where their intended audience has access.

## Where the skill goes

Each `conda-plugins` installation contains `SKILL.md`, the complete `references/` directory, `LICENSE`, and `THIRD_PARTY_NOTICES.md`. Skills CLI 1.7.4 uses the following destinations. Its [installer shares the `.agents/skills` directory](https://github.com/vercel-labs/skills/blob/v1.7.4/src/installer.ts#L156-L183) between Codex and Kilo:

| Client | `--agent` value | User installation with `--global` | Project installation |
| --- | --- | --- | --- |
| Codex | `codex` | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |
| Claude Code | `claude-code` | `~/.claude/skills/conda-plugins/` | `.claude/skills/conda-plugins/` |
| Kilo Code and Kilo CLI | `kilo` | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |

The setup command creates two physical copies of each skill: one shared by Codex and Kilo under `.agents/skills`, and one for Claude Code under `.claude/skills`. Rerun the setup command to update both together. Installing for Codex alone also makes the shared copy available to current Kilo.

On Windows, `~` means your user profile directory. Custom client home settings can change their configured paths. Current Kilo also supports `.kilo/skills`. Older Kilo extensions used `.kilocode/skills`, so check the documentation for an older installation.

Global installation paths and client discovery were checked on 27 October 2026. See [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Kilo skills](https://kilo.ai/docs/customize/skills), and [Claude Code skills](https://code.claude.com/docs/en/skills) for client-specific behavior.

## Use it

Start a new session in the conda plugin repository you want to work on.

- Codex: enter `$conda-plugins`, followed by your task.
- Claude Code: enter `/conda-plugins`, followed by your task.
- Kilo: ask it to use the `conda-plugins` skill, or choose it from the `/` menu. Use `/reload` after adding or updating skills in an existing session.

For any client:

> Use the conda-plugins skill to add a conda subcommand in this repository. Read the applicable repository instructions first, identify the development environment and supported conda versions, then implement and test the smallest complete change.

Check discovery by asking the client to identify the conda skill and all three required companions, then asking it to open the references needed for a sample task. The skill works with the project's `AGENTS.md` and existing client instructions.

## Repository instructions in each client

The skill tells the agent to read applicable instructions explicitly. That remains necessary when working below the directory where the session started.

- Codex discovers instructions along the directory chain to its starting directory. `AGENTS.override.md` takes precedence over `AGENTS.md` at the same level. Read deeper instructions before editing their files. See [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Kilo supports root `AGENTS.md` and loads nested guidance while reading files in those directories. See [Kilo AGENTS.md](https://kilo.ai/docs/customize/agents-md).
- Claude Code 2.1.277 and later can load `AGENTS.md` automatically. By default, this applies when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or above. It does not recognize `AGENTS.override.md`. For older versions, or when a `CLAUDE.md` is already in use, add `@AGENTS.md` to that file with the correct relative path. Preserve its existing instructions. See [Claude Code AGENTS.md support](https://code.claude.com/docs/en/memory#agentsmd).

Do not replace existing instruction files during skill installation. Root instructions should hold shared project rules. Put specialized instructions near their code, and link detailed guides from the relevant instruction file. Review referenced rules when the task reaches that area.

## Inspect and update

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 list --global --agent codex claude-code kilo
DISABLE_TELEMETRY=1 npx skills@1.7.4 check
DISABLE_TELEMETRY=1 npx skills@1.7.4 update conda-plugins --global
```

`list` shows installed skills. `check` checks recorded installations for updates without reinstalling them. The last command updates only `conda-plugins` in user scope. Rerun the setup command to refresh this skill and all three companions together. For a project installation, run `list` without `--global` and use `update conda-plugins --project` from that project. Manual copies need to be refreshed manually.

## Manual installation

If you prefer to copy files yourself, clone the repository or download its ZIP from GitHub:

```sh
gh repo clone jezdez/conda-plugin-skills
cd conda-plugin-skills
mkdir -p "$HOME/.agents/skills"
cp -R skills/conda-plugins "$HOME/.agents/skills/"
mkdir -p "$HOME/.claude/skills"
cp -R skills/conda-plugins "$HOME/.claude/skills/"
```

These are first-install commands. Compare or back up an existing skill before replacing it. The `.agents` copy serves Codex and current Kilo, and the `.claude` copy serves Claude Code. On Windows, copy the whole `skills/conda-plugins/` folder into those directories with Explorer or PowerShell. Keep its reference files together because their links are relative, and update each copy together.

These manual commands copy only `conda-plugins`. Install the three required companions using their upstream instructions below before using the workflow.

## Required companion skills

Superpowers, Humanizer, and Ponytail are prerequisites for this workflow in Codex, Kilo, and Claude Code. The [setup command](#install-with-npx) installs all three alongside `conda-plugins`. It includes the complete Superpowers and Ponytail collections because their workflows refer to sibling skills and supporting files.

The skill instructs the agent to confirm all three companions are available before plugin work. If one is missing or cannot be loaded, the agent must report it and stop, unless you explicitly waive that prerequisite for the task. This is an instruction-level check, not an installer-enforced dependency. The [Agent Skills format](https://agentskills.io/specification) has no standard field for automatically installing dependent skills.

| Skill | Use it for | Authoritative installation source |
| --- | --- | --- |
| Superpowers | Planning substantial changes, reproducing bugs, useful tests, code review, and evidence before completion claims | [obra/superpowers](https://github.com/obra/superpowers#readme) |
| Humanizer | Documentation, explanations, and review prose that preserve technical facts and read naturally | [blader/humanizer](https://github.com/blader/humanizer#readme) |
| Ponytail | The smallest complete change, reuse of existing APIs, and removal of unnecessary machinery | [DietrichGebert/ponytail installation guide](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md) |

The setup command installs portable skills. For native plugin features such as lifecycle hooks, follow each upstream's current instructions for your client. For Claude Code, Superpowers documents `/plugin install superpowers@claude-plugins-official`. Codex users can install Superpowers through the app's Plugins interface or the CLI's `/plugins` interface. Humanizer and Ponytail document their own marketplace or skill-installation options. If you already use a native plugin, check its available skills before installing duplicate copies.

For Kilo, standard skill folders can be placed in its supported skills directory. Preserve each skill's referenced files and confirm that the agent can load them. Copying a skill folder does not enable the source plugin's lifecycle hooks or client-specific tools. Ponytail also documents a native Kilo plugin installation. Superpowers' current README does not document equivalent Kilo lifecycle integration.

Repository rules and the user's scope still apply. Ponytail is not a reason to omit necessary checks. Humanizer must not invent evidence or weaken technical precision. Use Superpowers workflows in proportion to the task and within the client's available capabilities.

## Optional Codex Security review

[Codex Security](https://learn.chatgpt.com/docs/security/plugin) can supplement security tests with source review and finding validation. It is optional and does not affect the three companion prerequisites. Use it when available in Codex and a security review is in scope, especially for changes to credentials, request scoping, archive extraction, subprocess execution, or signed evidence.

The [testing guide](skills/conda-plugins/references/testing.md#optional-security-review) explains which scan fits a change and how to report results. Kilo and Claude Code users can follow the same security test cases and review criteria without Codex Security.

## Skill references

Start with [SKILL.md](skills/conda-plugins/SKILL.md). It routes the agent to all references relevant to the task:

- [Plugin guide](skills/conda-plugins/references/plugin-guide.md) for hook selection, registration, and a complete small plugin.
- [Architecture](skills/conda-plugins/references/architecture.md) for import cost, code ownership, models, dependencies, and errors.
- [CLI and processes](skills/conda-plugins/references/cli-and-processes.md) for arguments, activation, JSON, settings, state writes, and credentials.
- [Formats and solvers](skills/conda-plugins/references/formats-and-solvers.md) for manifests, exporters, package graphs, schema reuse, and target solving.
- [Verification](skills/conda-plugins/references/verification.md) for signed evidence, artifact binding, authorization, offline behavior, and verified caches.
- [Documentation and demos](skills/conda-plugins/references/documentation.md) for human-focused writing with Humanizer, Diátaxis, Sphinx, MyST, sphinx-design, worked examples, and VHS GIFs.
- [Testing](skills/conda-plugins/references/testing.md) for runnable discovery tests, regression cases, and startup checks.
- [Sources](skills/conda-plugins/references/sources.md) for optional provenance and pinned source examples.

## Contributing and building an archive

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the editing workflow and [AGENTS.md](AGENTS.md) for repository guidance. The repository uses Pixi for its locked development tools:

```sh
pixi install --locked
pixi run --locked check
pixi run --locked build
```

The build validates the skills and writes `dist/conda-plugins.zip`, including the references and license notices. Generated archives are ignored by Git and belong under `dist/`. Keep the ZIP out of the repository root. The archive installs this skill only, so its three companions still need the setup described above.

See [CHANGELOG.md](CHANGELOG.md) for changes, [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations, and [SECURITY.md](SECURITY.md) for private reporting.

## Layout

```text
README.md
AGENTS.md
CONTRIBUTING.md
LICENSE
pixi.toml
pixi.lock
scripts/
tests/
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

## Verification scope

On 27 October 2026, the exact setup command passed in Bash in a fresh Linux ARM64 container with Node.js 22.23.4, an empty user home, and no host directories mounted. It fetched this private repository through authenticated Git and the three public companion repositories. All 23 skills installed: `conda-plugins`, Humanizer, 15 Superpowers skills, and six Ponytail skills. Each of the two installation directories contained 115 files matching the source revisions byte for byte, with executable permissions preserved. Superpowers' references to sibling skills resolved.

With container networking disconnected, Codex 0.165.0, Kilo CLI 7.8.18, and Claude Code through Agent SDK 0.3.312 each discovered all 23 installed skills. Codex lists Humanizer as `humanizer:humanizer`. The checks used Codex's `skills/list`, Kilo's `debug skill`, and Claude's `supportedCommands()` without submitting a prompt. They establish installation and native client discovery. Model invocation and native plugin hooks were not tested.

Earlier checks on 23 October 2026 covered source selection and stop-on-failure behavior in Bash, Zsh, and a POSIX shell, plus project installation from local source snapshots. The documentation examples passed a strict Sphinx build and a real VHS recording of the bundled greet plugin. Clean global installation on macOS and Windows remains untested.
