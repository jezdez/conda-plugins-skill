# Structure a conda plugin

## Separate registration from execution

Keep the import path used by conda small:

```text
installed entry point
  -> plugin.py: hook registration and cheap callback adapters
  -> selected command or format implementation
  -> models and conda operations
  -> result returned to the caller
```

Package `__init__.py` is part of that path. A lazy import in `plugin.py` achieves nothing if the initializer already imports the CLI, HTTP client, or serializer.

Put expensive and optional imports inside the selected callback. Keep ordinary imports at module scope elsewhere. Use `TYPE_CHECKING` for annotation-only imports that would load a heavy dependency at runtime. Fix circular ownership instead of scattering local imports through unrelated functions.

Registration may import lightweight conda hook types and a lightweight parser module. Parser setup should only describe arguments. Keep command dispatch and rendering imports out of that module. Trust-root loading, credential lookup, network calls, solver construction, cache creation, and archive inspection belong to the invoked operation. Required rendering dependencies belong at module scope in the selected CLI implementation, without optional-import fallbacks.

For an optional dependency, allow unrelated commands and help to work without it. At the operation that needs it, report the missing feature and how to enable it. Catch a missing optional package narrowly. Do not reinterpret an `ImportError` inside a broken dependency as proof that the dependency is simply absent.

For a new API, inspect the installed hook and type and test every supported version. A development dependency or accepted CEP does not establish released availability. Declare an honest minimum version. Use a focused capability check when development builds make version comparison insufficient. Do not silently replace an unavailable verification hook with a different lifecycle hook.

## Assign ownership before adding files

Use these roles as the implementation grows. A small plugin may need only `plugin.py` and one implementation module.

| Responsibility | Place it |
| --- | --- |
| Entry-point metadata and hook objects | `pyproject.toml` and `plugin.py` |
| Argument parser and selected command dispatch | The CLI module |
| Reusable operation | The domain module or owning adapter |
| Input validation and derived behavior | The model that owns that data |
| One file format and its metadata | That format's module |
| Shared domain errors | The existing exceptions module |
| Presentation | CLI/output code |
| Tests | The corresponding source module's test file |

A parser converts its format into models once. Downstream operations consume those models instead of repeatedly checking which manifest syntax produced them. Use conda's `Environment`, `PackageRecord`, `MatchSpec`, and `Channel` where those types already express the data.

Keep authoring inputs separate from installed state. A skeleton writer can validate input and return a path without constructing a model that promises package ownership or an installed environment. Reuse field validation when both flows need it, but check installation-specific invariants only when loading the installed object. Interactive guides should call the same domain operations as explicit commands, not reimplement discovery, writing, or linking.

Keep reusable operations independent of `argparse.Namespace`, terminal colors, output paths selected by the CLI, and a particular caller's workspace discovery. Return data or raise a meaningful domain error. Let the command choose presentation and process status. Call `sys.exit` only at a real entry point when required by that entry point.

## Decide where a helper belongs

Check in this order:

1. Does existing code, a test fixture, conda, stdlib, or a dependency provide the operation? Use it.
2. Does an existing model or adapter own the input and derived state? Add a cohesive method.
3. Would a named function clarify its caller, reduce confusing nesting, or make substantial logic easier to test? Extract it, even with one caller.
4. Would extraction obscure the order of related steps or their shared state? Keep them together. Inline trivial forwarding unless an API requires it.

Review callers and helpers together, preserving state changes and error handling. Explain the specific readability or testing benefit. Function length, complexity scores, or a leading underscore alone do not justify extraction or inlining.

For example, if a resolved environment already holds specifications, channels, and system requirements, expose `environment.solve_for_platform(platform)`. Avoid a private helper that takes all those fields separately and forces every caller to keep them in sync.

The same rule puts evidence validation on an evidence model, cache lookup on a cache object, and format mapping on the exporter that owns the records. A framework callback can remain a module-level function. Do not add a stateless utility class merely to turn functions into methods.

Share a package graph or format-neutral model only after actual callers need the same representation. Two format names alone do not justify a new framework. Keep schema-specific fields in their format implementation.

## Keep dependencies and APIs deliberate

Use a single existing library for overlapping work when it fits, such as reading and writing the same manifest. Do not add a second HTTP, configuration, locking, cryptography, or serialization stack without a concrete missing capability.

Declare minimum supported versions. Use an upper bound for a demonstrated incompatibility, and explain why it exists. Provision conda through a conda channel in the workspace environment and record its runtime requirement in the conda recipe. Keep it out of wheel dependencies that a PyPI resolver would try to install. Declare the remaining Python runtime dependencies in `pyproject.toml` and provision them in the project's environment tool.

Use public APIs where available. If an internal conda API is necessary, isolate the dependency in the owning adapter, state the supported versions, and test the affected behavior. Do not wrap every upstream call in a private forwarding function.

## Share the resolved package version

For a project using Hatchling and hatch-vcs, resolve the version with `python -m hatchling version` in the checkout that has Git metadata. Pass that value to the conda recipe through a required project-specific environment variable. Avoid a separately maintained recipe version or a custom script that duplicates the backend's version command. Preserve a different project's chosen version scheme.

A local conda build that copies source without `.git` can set `SETUPTOOLS_SCM_PRETEND_VERSION` inside that build to the already resolved value. A release build from a published sdist uses the archive's stored version and must not apply that override. Keep generated version files out of manual edits. A fallback version supports development without Git metadata and is not evidence of a release.

On an authorized release tag, compare the backend's resolved version with the version encoded by the tag, using the repository's tag convention. Keep dated changelog notes in the manual preparation checklist. Follow the [release ordering guidance](verification.md#order-release-jobs-and-preserve-artifacts) for building and publishing the resulting artifacts.

## Keep code and prose readable

Use `from __future__ import annotations`, modern annotations, and relative imports within the package. Keep absolute package imports for installed entry points and tests. Tests should mirror the source module or behavior.

Comments explain a non-obvious constraint or tradeoff. Docstrings explain an operation's purpose and inputs. Avoid comments that narrate the next line or divide a large module into decorated sections. Split a module by responsibility when its structure becomes hard to follow.

For user-facing documentation, follow [documentation.md](documentation.md). It covers substantial explanations and worked examples, Diátaxis, the Sphinx stack, and the shared demo style. Document the exact flags, formats, supported versions, and failure behavior that exist.
