---
name: conda-plugins
description: Use when creating, extending, debugging, reviewing, or documenting Python plugins for conda, including subcommands, settings, authentication, environment formats, solvers, and lifecycle hooks. Not for ordinary package installation or environment management unless the task concerns a plugin's implementation.
license: Apache-2.0
---

# Develop conda plugins

Use these synthesized development practices when building a plugin. The bundled guides contain the implementation decisions and examples. External repositories in [sources.md](references/sources.md) record where the practices came from and are optional reading.

## Check required companions

Before starting plugin implementation, debugging, review, or documentation work, confirm that Superpowers, Humanizer, and Ponytail are available to the current agent. Use the client's skill discovery and read each companion's entry point. Check once per session and reuse that confirmation unless availability changes. Namespaced skill names are valid.

If any companion is missing or cannot be loaded, identify it, link the [setup instructions](https://github.com/jezdez/conda-plugin-skills#required-companion-skills), and stop before starting the plugin work. Do not silently substitute general advice or install companions without authorization. The user may explicitly waive a prerequisite for the current task.

Apply the companions where their workflows fit:

- Superpowers: start with its `using-superpowers` entry point and load the relevant planning, debugging, testing, or review workflow.
- Ponytail: use its development guidance to keep the implementation small and reuse existing APIs.
- Humanizer: apply it to documentation, explanations, and review prose while preserving technical facts.

Use native skill invocation when available, otherwise follow the installed `SKILL.md` instructions. Preserve the user's scope and applicable repository rules. Required availability does not mean every task needs every Superpowers workflow.

## Establish the task

Read the target repository's applicable instructions and metadata. Respect the client's instruction precedence, including `AGENTS.override.md` and existing `CLAUDE.md` files. Read nested instructions before editing their files.

Determine whether the user wants implementation, a plan, an explanation, or review findings. A read-only request stays read-only. This skill and its companions do not authorize edits, installations, or publication beyond the user's request.

Identify the behavior being changed, the hook that owns it, the supported conda versions, and the commands that validate it. Existing repository requirements take precedence over the defaults below. Preserve unrelated work and use the current checkout.

For a new plugin, start with one installed entry point and one working hook. Add modules, models, or shared infrastructure when the implementation needs them.

## Apply the shared design

1. Keep registration declarative. `plugin.py` yields conda hook objects and forwards to the selected operation. Discovery must not contact services, read credentials, initialize caches, or load expensive feature implementations.
2. Give each operation a clear owner. Normalize format input once. Put behavior on the model or adapter that owns its inputs. Keep CLI parsing and rendering outside reusable operations.
3. Reuse conda's environment, configuration, package, solver, activation, and plugin APIs. Use an existing schema's validator and serializer. Avoid a parallel configuration parser, dependency solver, or general framework.
4. Keep data claims exact. Declared requirements, resolved records, requested roots, verified evidence, and authorization are different facts. Preserve that distinction in models and output.
5. Follow standard argparse behavior for options and positionals. Give each command one output owner. JSON is one complete unstyled value on stdout. Composite commands collect child results and control their output. Process-launching commands preserve argument and exit-status semantics.
6. Verify observable behavior in the intended runtime. Cover installed discovery, errors, relevant platform behavior, and the target repository's full checks. Regenerate `pixi.lock` after Pixi metadata changes.
7. Write substantial documentation for people learning and using the plugin. Follow Diátaxis, develop useful explanations and worked examples, and apply Humanizer. Keep the skill's compact instructions separate from the depth readers need.

## Load the relevant pattern

| Current work | Bundled guide |
| --- | --- |
| First plugin, hook choice, entry point, or discovery failure | [plugin-guide.md](references/plugin-guide.md) |
| Module ownership, helpers, imports, dependencies, or error handling | [architecture.md](references/architecture.md) |
| CLI composition, settings, authentication, process execution, or caches | [cli-and-processes.md](references/cli-and-processes.md) |
| Manifest parsing, exporters, package graphs, lockfiles, or solver targets | [formats-and-solvers.md](references/formats-and-solvers.md) |
| Signed evidence, artifact binding, authorization, or verification caches | [verification.md](references/verification.md) |
| Human-facing docs, Diátaxis, Sphinx, MyST, sphinx-design, examples, or GIF demos | [documentation.md](references/documentation.md) |
| Regression tests, startup checks, or completion claims | [testing.md](references/testing.md) |
| Installing the skill or companions | [Repository README](https://github.com/jezdez/conda-plugin-skills#readme) |

Read the sections relevant to the current change, including guidance from multiple references when needed. The target code and bundled patterns should be sufficient for ordinary work. Consult current upstream documentation when a supported API or standard needs verification.

## Working defaults

Use modern annotations, relative package imports, plain parametrized pytest functions, fixtures, and small real fakes. Prefer stdlib and existing dependencies. Use Ruff, `ty`, and Pixi for new Python projects unless the project has chosen other tools.

Make the smallest complete change and run its required checks. Report local results, hosted CI, native-platform runs, and publication separately. Do not poll CI unless asked. Publishing, releasing, changing another repository, or creating another checkout needs authorization covering that action.

Codex Security is optional. For an authorized security review, follow the [security-review guidance](references/testing.md#optional-security-review) when the tool is available. Security analysis does not replace regression tests.
