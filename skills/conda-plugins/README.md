# Conda plugin development skill

A shareable Agent Skill for building and maintaining Python conda plugins. It draws on Jannis Leidel's recent plugins and their repository guidance, with a runnable starting example.

Start with [SKILL.md](SKILL.md). The agent loads the relevant reference when the task needs it:

- [repository-guidance.md](repository-guidance.md) for local instructions and source examples.
- [plugin-guide.md](plugin-guide.md) for hook selection, registration, and a small working plugin.
- [testing.md](testing.md) for discovery, compatibility, behavior, and startup checks.

The entry point uses the portable [Agent Skills format](https://agentskills.io/specification). It does not require a particular agent's tool names, shell-injection features, or lifecycle hooks.

## Install the whole folder

Clone the private [conda-plugin-skills repository](https://github.com/jezdez/conda-plugin-skills), or download its ZIP from GitHub. Colleagues need read access to the repository. The skill is in `skills/conda-plugins/` and contains these five files:

```text
conda-plugins/
  SKILL.md
  README.md
  repository-guidance.md
  plugin-guide.md
  testing.md
```

Copy the whole `skills/conda-plugins` folder. Keep all five files together because their links are relative.

Choose a user installation for your own projects, or a repository installation to share it with a team:

| Client | User installation | Repository installation |
| --- | --- | --- |
| Codex | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |
| Current Kilo Code and Kilo CLI | `~/.agents/skills/conda-plugins/` | `.agents/skills/conda-plugins/` |
| Claude Code | `~/.claude/skills/conda-plugins/` | `.claude/skills/conda-plugins/` |

Codex and current Kilo can share the same `.agents` copy. Claude Code needs a copy or supported directory symlink under `.claude/skills`. Copying works on systems where symlinks are inconvenient. If you keep two copies, update them together.

For a user installation on macOS or Linux, run these commands from the repository root:

```sh
mkdir -p "$HOME/.agents/skills"
cp -R skills/conda-plugins "$HOME/.agents/skills/"
mkdir -p "$HOME/.claude/skills"
cp -R skills/conda-plugins "$HOME/.claude/skills/"
```

Use these commands for a first installation. Compare or back up an existing skill before replacing it. On Windows, copy the folder into `.agents\skills` and `.claude\skills` under your user profile using Explorer or PowerShell.

Start a fresh agent session after installation. In Codex, invoke `$conda-plugins`. In Claude Code, invoke `/conda-plugins`. In Kilo, ask it to use the `conda-plugins` skill. A portable first prompt is:

> Use the conda-plugins skill to help me add a conda subcommand in this repository. Read the applicable repository instructions first, identify the development environment and supported conda versions, then implement and test the smallest complete change.

Check discovery by asking the client to identify the installed skill, then asking it to open the reference needed for a sample task. Installation in all three clients has not been tested end to end here.

Current paths were checked on 23 October 2026 against [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Kilo skills](https://kilo.ai/docs/customize/skills), and [Claude Code skills](https://code.claude.com/docs/en/skills). Current Kilo also supports `.kilo/skills`. Older Kilo extensions used `.kilocode/skills`, so check the documentation for an older installation.

## Repository instructions in each client

The skill tells the agent to read applicable instructions explicitly. That remains necessary when working below the directory where the session started.

- Codex discovers instructions along the directory chain to its starting directory. `AGENTS.override.md` takes precedence over `AGENTS.md` at the same level. Read deeper instructions before editing their files. See [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Kilo supports root `AGENTS.md` and loads nested guidance while reading files in those directories. See [Kilo AGENTS.md](https://kilo.ai/docs/customize/agents-md).
- Claude Code 2.1.277 and later can load `AGENTS.md` automatically. By default, this applies when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or above. It does not recognize `AGENTS.override.md`. For older versions, or when a `CLAUDE.md` is already in use, add `@AGENTS.md` to that file with the correct relative path. Preserve its existing instructions. See [Claude Code AGENTS.md support](https://code.claude.com/docs/en/memory#agentsmd).

Do not replace existing instruction files during skill installation. Root instructions should hold shared project rules. Put specialized instructions near their code, and link detailed guides from the relevant instruction file. Review referenced rules when the task reaches that area.

## Recommended companion skills

Install these when they fit your team's workflow. The conda skill works independently, and recommending a companion does not authorize an agent to install it.

| Skill | Use it for | Authoritative installation source |
| --- | --- | --- |
| Superpowers | Planning substantial changes, reproducing bugs, useful tests, code review, and evidence before completion claims | [obra/superpowers](https://github.com/obra/superpowers#readme) |
| Humanizer | Documentation, explanations, and review prose that preserve technical facts and read naturally | [blader/humanizer](https://github.com/blader/humanizer#readme) |
| Ponytail | The smallest complete change, reuse of existing APIs, and removal of unnecessary machinery | [DietrichGebert/ponytail installation guide](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md) |

Use each upstream's current instructions for your client. For Claude Code, Superpowers documents `/plugin install superpowers@claude-plugins-official`. Codex users can install Superpowers through the app's Plugins interface or the CLI's `/plugins` interface. Humanizer and Ponytail document their own marketplace or skill-installation options.

For Kilo, standard skill folders can be placed in its supported skills directory. Preserve each skill's referenced files. Copying a skill folder does not enable the source plugin's lifecycle hooks or client-specific tools. Ponytail also documents a native Kilo plugin installation. Superpowers' current README does not document equivalent Kilo lifecycle integration.

Repository rules and the user's scope still apply. Ponytail is not a reason to omit necessary checks. Humanizer must not invent evidence or weaken technical precision. Use Superpowers workflows in proportion to the task and within the client's available capabilities.
