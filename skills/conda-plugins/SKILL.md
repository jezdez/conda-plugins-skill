---
name: conda-plugins
description: Use when creating, extending, debugging, or reviewing Python plugins for conda, including subcommands, settings, authentication, environment formats, solvers, and lifecycle hooks.
---

# Develop conda plugins

Use these synthesized development practices when building a plugin. The bundled guides contain the implementation decisions and examples. External repositories in [sources.md](sources.md) record where the practices came from and are optional reading.

## Establish the task

Read the target repository's applicable instructions and metadata. Respect the client's instruction precedence, including `AGENTS.override.md` and existing `CLAUDE.md` files. Read nested instructions before editing their files.

Identify the behavior being changed, the hook that owns it, the supported conda versions, and the commands that validate it. Existing repository requirements take precedence over the defaults below. Preserve unrelated work and use the current checkout.

For a new plugin, start with one installed entry point and one working hook. Add modules, models, or shared infrastructure when the implementation needs them.

## Apply the shared design

1. Keep registration declarative. `plugin.py` yields conda hook objects and forwards to the selected operation. Discovery must not contact services, read credentials, initialize caches, or load expensive feature implementations.
2. Give each operation a clear owner. Normalize format input once. Put behavior on the model or adapter that owns its inputs. Keep CLI parsing and rendering outside reusable operations.
3. Reuse conda's environment, configuration, package, solver, activation, and plugin APIs. Use an existing schema's validator and serializer. Avoid a parallel configuration parser, dependency solver, or general framework.
4. Keep data claims exact. Declared requirements, resolved records, requested roots, verified evidence, and authorization are different facts. Preserve that distinction in models and output.
5. Follow standard argparse behavior for options and positionals. Give each command one output owner. JSON is one complete unstyled value on stdout. Composite commands collect child results and control their output. Process-launching commands preserve argument and exit-status semantics.
6. Verify observable behavior in the intended runtime. Cover installed discovery, errors, relevant platform behavior, and the target repository's full checks. Regenerate `pixi.lock` after Pixi metadata changes.

## Load the relevant pattern

| Current work | Bundled guide |
| --- | --- |
| First plugin, hook choice, entry point, or discovery failure | [plugin-guide.md](plugin-guide.md) |
| Module ownership, helpers, imports, dependencies, or error handling | [architecture.md](architecture.md) |
| CLI composition, settings, authentication, process execution, or caches | [cli-and-processes.md](cli-and-processes.md) |
| Manifest parsing, exporters, package graphs, lockfiles, or solver targets | [formats-and-solvers.md](formats-and-solvers.md) |
| Regression tests, startup checks, signed evidence, or completion claims | [testing.md](testing.md) |
| Installing the skill or companions | [README.md](README.md) |

Read only the guide needed for the current change. The target code and bundled patterns should be sufficient for ordinary work. Consult current upstream documentation when a supported API or standard needs verification.

## Working defaults

Use modern annotations, relative package imports, plain parametrized pytest functions, fixtures, and small real fakes. Prefer stdlib and existing dependencies. Use Ruff, `ty`, and Pixi for new Python projects unless the project has chosen other tools.

Make the smallest complete change and run its required checks. Report local results, hosted CI, native-platform runs, and publication separately. Do not poll CI unless asked. Publishing, releasing, changing another repository, or creating another checkout needs authorization covering that action.

Superpowers supports planning, debugging, and verification. Ponytail supports minimal complete implementations. Humanizer supports precise prose. They are recommended companions, and repository requirements still apply.
