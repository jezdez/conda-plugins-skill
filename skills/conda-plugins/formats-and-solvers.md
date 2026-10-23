# Formats, package records, and solver targets

## Decide which data the format promises

| Input | Meaning | Use |
| --- | --- | --- |
| `Environment.requested_packages` | Requested conda specifications | User intent, manifest export, declared graph roots |
| `Environment.explicit_packages` | Exact resolved package records | Lockfiles, inventories, SBOMs |
| `Environment.external_packages` | Requirements from another package system | Preserve when supported, otherwise disclose omissions |
| `PackageRecord.depends` | Required dependencies | Package graph edges |
| `PackageRecord.constrains` | Restrictions if another package is present | Constraints, not proof of an installed dependency |

An exporter promising an exact inventory must reject missing resolved records. Do not solve, inspect a real prefix, or fetch provenance inside serialization. Those operations would change which data the caller asked to export.

Preserve requested specifications in a manifest. Preserve exact sources, versions, builds, subdirectories, filenames, and available hashes in a lockfile. Reducing a URL-pinned dependency to its package name loses source identity.

A single-platform exporter accepts a conda `Environment` and returns text. A multi-platform exporter accepts an iterable of environments and returns text. The caller owns output paths and file writes. Exporters should work through `conda export` and other clients without importing a workspace manager.

Use the same serializer for a dedicated export command and a registered exporter. Otherwise the two routes can silently preserve different fields.

## Give each format one owner

Keep format metadata, validation, conversion, and serialization in the format's module. Registration imports its metadata instead of repeating strings. This illustrative metadata declares one schema version:

```python
from __future__ import annotations

from typing import Final

FORMAT: Final = "example-json-v1"
ALIASES: Final = ("example-json",)
DEFAULT_FILENAMES: Final = ("*.example.json",)
```

The versioned name lets automation select a schema. An unversioned alias may follow a newer supported schema when that behavior is documented. Do not change the meaning of a versioned name.

Use a small framework callback that delegates to the owner when mapping, graph construction, and serialization share state, such as `Exporter(environment).export()`. Keep a simple stateless transformation as a function. Add a second format in its own module. Share a normalized graph only when real implementations need the same representation.

## Adapt an existing schema narrowly

For a format derived from a supported schema:

1. Validate the local version and required structure.
2. Select the requested environment and platform.
3. Check local rules that the shared model cannot express.
4. Adapt only the representation differences.
5. Use the dependency's public validation and conversion.
6. Restore names or metadata changed temporarily for conversion.

For example, a named-environment lockfile can reuse an upstream model that expects a `default` environment by adapting the selected environment in memory and restoring its name afterward. It still has to validate package references, channel membership, and digests. Changing the version number alone does not validate the document.

Preserve the source file. Do not rewrite it to satisfy another loader. Keep logical environment or platform names separate from the concrete subdirectory used to install packages.

When a supported dependency drops one required field, keep a compatibility extension narrow. Document the upstream fix and the version at which the extension can be removed. Test the minimum supported dependency before removing the extension. Do not copy an entire upstream parser to repair one field.

Test missing environments, missing platforms, unresolved package references, conflicting hashes for the same URL, unsupported external package records, and lost fields after round trips. Compare exact package identity, not just names and versions.

## Preserve unrelated manifest content

A dedicated output file can belong to one exporter. A shared `pyproject.toml` contains other tools' data.

Let the parser that owns the format merge its subtree into an existing document. Preserve `[project]`, `[build-system]`, and unrelated tool tables. Test that they survive the update. Avoid CLI code that reaches into parser internals and rebuilds the document.

When consolidating several platforms, lift a dependency into common configuration only when both its name and value agree for every platform. Keep target-only dependencies and differing versions or source URLs in their target tables.

## Build truthful package graphs

Parse dependency strings with `MatchSpec`. Build edges from `depends`, not `constrains`. Use requested packages as declared roots when available. If roots are inferred, label that inference and handle disconnected cycles. Include known leaves when the output schema distinguishes empty dependency sets from absent statements.

Preserve exact identity from available records. Do not infer suppliers, authors, or manufacturers from channel names. Keep historical license text as text unless it has been validated as an SPDX expression.

Sanitize distribution URLs with conda's URL handling and remove credential-bearing query strings or fragments. Do not expose local prefixes or source paths as product identifiers.

Use `unknown` when completeness cannot be established and `incomplete` when input proves omissions. Conda records alone do not prove coverage of vendored code, static libraries, the operating system, or unexamined package systems.

Use the format's official serializer. If one field needs post-processing, keep the adjustment explicit and validate the final output against the official schema. Do not replace the whole serializer to repair one omission.

For reproducible output, sort components and edges, avoid random identifiers, and define timestamps. If `SOURCE_DATE_EPOCH` is supported, reject an invalid value rather than substituting the current time.

Observable tests should prove that reordered input yields identical reproducible output, missing targets remain visible, invalid hashes fail, sanitized values appear everywhere, and the installed export command produces schema-valid output. Schema validity alone does not prove accurate or complete inventory.

## Coordinate target subdirectories and virtual packages

Cross-platform solving has two inputs that must agree:

- The solver searches the requested package subdirectory and `noarch`.
- Conda's virtual-package plugins see the requested target through conda's context.

Setting only solver subdirectories can leave host virtual packages active. Where the supported conda version and existing resolver use scoped context overrides, the operation has this shape:

```python
with conda_context._override("_subdir", platform):
    solver = solver_backend(
        str(prefix),
        list(channels),
        (platform, "noarch"),
        specs_to_add=specs,
    )
    records = list(solver.solve_final_state(prune=True))
```

This excerpt describes the scoped solve, not a standalone resolver. `_override` and `_subdir` are internal APIs. Isolate their use, test the supported versions, and preserve the target project's cleanup mechanism.

Choose the configured solver through conda's plugin manager. Keep solving separate from transaction execution when producing a lockfile.

Resolve target-specific dependency tables for each platform. A host-resolved specification list remains wrong even when sent to the correct package subdirectory.

Put virtual-package version policy on the resolved environment that owns system requirements. Respect explicit `CONDA_OVERRIDE_*` values. Document the precedence of project defaults and restore temporary environment variables and context after success or failure. Do not invent GPU, libc, or architecture capabilities to make a solve succeed.

A full reproducible solve should use an empty temporary prefix so a user's installed packages and history cannot affect it. A selective update needs the exact locked baseline and an explicit choice of which roots may change.

Scoped context and environment-variable mutations affect shared process state. Serialize those operations or isolate them in processes. Do not overlap target solves in threads without proven isolation.

Test that target subdirectories and visible context agree, host virtual packages do not leak, explicit overrides retain precedence, failed solves restore state, and each target gets its own declared requirements. A failed target must not leave a partially written lockfile. A cross-platform solve is not proof of a native install.

## Avoid registration collisions and recursive hook calls

Give each solver its stable name. Add an alias only when it does not collide with another registered provider. Use a capability check where development builds make a version cutoff unreliable.

A hook inspecting other implementations of that same hook must exclude itself. Otherwise asking for the current hook results calls it recursively. Conda's plugin manager provides `subset_hook_caller` for this targeted case.

Test alias registration with another provider present and absent. Reset any cached registration decisions between tests. Assert the registered names and actual solver behavior, including pins, channel priority, unsatisfiable input, and target virtual packages.
