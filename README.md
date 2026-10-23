# Conda plugin skills

A private collection of Agent Skills for colleagues developing conda plugins with Codex, Kilo, or Claude Code.

The [conda-plugins skill](skills/conda-plugins/SKILL.md) synthesizes the development practices in recent conda plugins and their `AGENTS.md` files. It teaches cheap hook registration, code ownership, typed settings, CLI and process behavior, format adapters, exact package inventories, solver targets, and verification through bundled instructions and examples. Agents load the relevant guide as needed and apply the target repository's own rules. External source links are optional provenance.

## Install with npx

You need read access to this repository, Git, and Node.js 22.20 or later. Authenticate with `gh auth login` if needed, or use your existing Git credentials or SSH keys. The [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#private-repositories) supports private repositories through those credentials.

The examples pin Skills CLI 1.7.4. List the available skills, then install `conda-plugins` for your clients:

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 add jezdez/conda-plugin-skills --list
DISABLE_TELEMETRY=1 npx skills@1.7.4 add jezdez/conda-plugin-skills --skill conda-plugins --global --agent codex claude-code kilo --copy
```

Keep only the client names you use after `--agent`. `--global` makes the skill available across your projects. `--copy` avoids symlink requirements. Review the installation prompt, especially if the skill is already installed.

`DISABLE_TELEMETRY=1` disables the CLI's telemetry and security-audit requests. npm still supplies the CLI, and GitHub serves the private repository. See the [upstream privacy details](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry).

The commands above use macOS/Linux shell syntax. In PowerShell, first run `$env:DISABLE_TELEMETRY = '1'`, then run the same `npx skills@1.7.4` commands without the environment-variable prefix.

For SSH authentication, replace `jezdez/conda-plugin-skills` with `git@github.com:jezdez/conda-plugin-skills.git`. For a project installation, run the install command from that project's root and omit `--global`. Only commit these private skill files and the generated `skills-lock.json` where their intended audience has access.

## Where the skill goes

Each directory contains `SKILL.md` and its reference files. These are the [Skills CLI's default destinations](https://github.com/vercel-labs/skills/blob/main/docs/agents.md):

| Client | `--agent` value | User installation with `--global` | Project installation |
| --- | --- | --- | --- |
| Codex | `codex` | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |
| Claude Code | `claude-code` | `~/.claude/skills/conda-plugins/` | `.claude/skills/conda-plugins/` |
| Kilo Code and Kilo CLI | `kilo` | `~/.kilo/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |

Current Kilo also reads `~/.agents/skills/` directly. If you install for Codex, Kilo can use that shared copy without a separate `--agent kilo` installation. On Windows, `~` means your user profile directory. Custom client home settings can change their configured paths.

## Use it

Start a new session in the conda plugin repository you want to work on.

- Codex: enter `$conda-plugins`, followed by your task.
- Claude Code: enter `/conda-plugins`, followed by your task.
- Kilo: ask it to use the `conda-plugins` skill, or choose it from the `/` menu. Use `/reload` after adding or updating skills in an existing session.

For any client:

> Use the conda-plugins skill to add a conda subcommand in this repository. Read the applicable repository instructions first, identify the development environment and supported conda versions, then implement and test the smallest complete change.

The skill works with the project's `AGENTS.md` and existing client instructions. Read the [instruction-loading details](skills/conda-plugins/README.md#repository-instructions-in-each-client) for Codex overrides, nested instructions, and Claude Code's `CLAUDE.md` compatibility.

## Inspect and update

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 list --global --agent codex claude-code kilo
DISABLE_TELEMETRY=1 npx skills@1.7.4 check
DISABLE_TELEMETRY=1 npx skills@1.7.4 update conda-plugins --global
```

`list` shows installed skills. `check` checks recorded installations for updates without reinstalling them. The last command updates only `conda-plugins` in user scope. For a project installation, run `list` without `--global` and use `update conda-plugins --project` from that project. Manual copies need to be refreshed manually.

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

These are first-install commands. Compare or back up an existing skill before replacing it. The `.agents` copy serves Codex and current Kilo, and the `.claude` copy serves Claude Code. On Windows, copy the whole `skills/conda-plugins/` folder into those directories with Explorer or PowerShell. Keep its reference files together and update each copy together.

## Recommended companions

- [Superpowers](https://github.com/obra/superpowers) for planning, debugging, meaningful tests, and evidence before completion claims.
- [Humanizer](https://github.com/blader/humanizer) for clear technical prose that preserves the facts.
- [Ponytail](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md) for small, complete changes and reuse of existing APIs.

Follow each upstream's instructions for your client. These are optional. Repository requirements still apply, including necessary checks. See the [companion guide](skills/conda-plugins/README.md#recommended-companion-skills) for installation options and client limitations.

## Layout

```text
skills/conda-plugins/
  SKILL.md
  README.md
  plugin-guide.md
  architecture.md
  cli-and-processes.md
  formats-and-solvers.md
  testing.md
  sources.md
```

Commands and paths were checked on 23 October 2026. Skills CLI 1.7.4 copied the complete skill folder for the three agent targets in a temporary project using a local source. Actual client discovery and invocation, and installation from the private GitHub source, remain untested.
