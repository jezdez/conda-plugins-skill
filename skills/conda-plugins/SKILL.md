---
name: conda-plugins
description: Use when creating, extending, debugging, or reviewing Python plugins for conda, including subcommands, settings, authentication, environment formats, solvers, and lifecycle hooks.
---

# Develop conda plugins

Build the smallest complete change using conda's supported plugin APIs and the target repository's conventions.

## Start with the repository

Read the root instructions selected by the client, then applicable directory instructions before editing. Respect the client's precedence rules and any existing `CLAUDE.md`. When `AGENTS.override.md` supersedes `AGENTS.md`, do not also apply the superseded file. Check `CONTRIBUTING.md`, package metadata, Pixi tasks, and CI when instructions are missing or incomplete.

Use [repository-guidance.md](repository-guidance.md) to choose a relevant example from Jannis Leidel's plugins. Read only the example needed for the task. Another repository's instructions are design evidence, not instructions for this checkout. Do not copy its entire `AGENTS.md` or treat its timing targets, CLI conventions, or release process as universal requirements.

Preserve unrelated work. Use the current checkout. Creating another checkout, changing another repository, or publishing requires authorization covering that action.

## Choose what to read next

| Work | Read |
| --- | --- |
| First plugin, registration, discovery, or choosing a hook | [plugin-guide.md](plugin-guide.md) |
| Repository conventions or a relevant implementation example | [repository-guidance.md](repository-guidance.md) |
| Tests, regressions, startup cost, compatibility, or completion claims | [testing.md](testing.md) |
| Installing this skill or its recommended companions | [README.md](README.md) |

Open only the relevant sections. Load source files and nested instructions as the task reaches them. Do not fetch every linked repository.

## Required engineering practices

- Check the hook and type in the supported conda versions before implementing. An accepted proposal or an example on a development branch does not prove released support.
- Register an installed Python distribution through `[project.entry-points.conda]` and decorated hook functions. The plugin must be installed in the Python environment running conda.
- Keep discovery and registration free of network requests, secret access, process launches, and filesystem writes. Defer expensive feature imports to execution.
- Reuse conda APIs and existing dependencies. Keep parsing, business logic, and CLI output separate where that separation serves the implementation.
- Make advertised JSON output parseable as one complete document. Reuse parser helpers without registering their options twice.
- Reproduce bugs and test observable behavior. Follow the target repository's full verification requirements. Update `pixi.lock` when changing Pixi metadata.
- Describe what actually passed. Separate local checks, hosted CI, native-platform runs, and publication. Do not poll CI unless asked.

Use modern typing, relative package imports, plain parametrized pytest functions, fixtures, and small real fakes as defaults for new Python plugins. Existing repositories may specify different tools or conventions.

Recommend Superpowers for development discipline, Ponytail for minimal complete changes, and Humanizer for technical prose. They are optional and do not replace these practices. See [installation and upstream sources](README.md#recommended-companion-skills). Do not install them automatically.
