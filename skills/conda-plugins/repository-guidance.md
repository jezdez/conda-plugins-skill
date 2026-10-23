# Read repository guidance progressively

## Establish the local rules

Read the target repository's root instructions and any applicable parent instructions already supplied by the client. Before editing a nested directory, read its instructions too. Inspect `AGENTS.override.md`, `CLAUDE.md`, and other client instruction files according to that client's rules. Client loading differs, as described in [README.md](README.md#repository-instructions-in-each-client).

Then inspect:

- `pyproject.toml` or `pixi.toml` for package layout, entry points, supported Python and conda versions, environments, and tasks.
- Existing plugin registration, the implementation being changed, and nearby tests.
- CI and contribution guidance for the actual completion requirements.

Extract the commands and constraints needed for this task. For a small change, a short working note is enough. Do not create a second rules file unless the user wants one.

When a rule is unclear, inspect its use in the code and tests. Ask only when a consequential choice remains unresolved. Do not silently replace the repository's tools or test conventions.

## Choose one example

These public sources were checked on 23 October 2026. The pinned instruction links show the guidance used to prepare this skill. Inspect the target repository's current files when doing work there.

| Task | Example and focused reading |
| --- | --- |
| Small settings and request-header plugin | [conda-dev-request-headers instructions](https://github.com/jezdez/conda-dev-request-headers/blob/845fb12f994ccf33c6e61a0d70500b1a2dd66abb/AGENTS.md) and [registration](https://github.com/jezdez/conda-dev-request-headers/blob/main/conda_dev_request_headers/plugin.py). Useful for small hooks, validation, and keeping credentials out of logs. Its intended use is local development. |
| Subcommands, manifests, task execution, JSON composition | [conda-workspaces instructions](https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/AGENTS.md). Read the CLI or manifest sections needed for the change. |
| Environment exporters and deterministic format output | [conda-sboms instructions](https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/AGENTS.md) and [registration](https://github.com/conda-incubator/conda-sboms/blob/main/conda_sboms/plugin.py). |
| Environment specifiers and lockfile exporters | [conda-lockfiles registration](https://github.com/conda/conda-lockfiles/blob/main/conda_lockfiles/plugin.py). Inspect metadata, tests, and contribution guidance. No `AGENTS.md` was present in the inspected public tree. |
| Authentication handlers | [conda-auth registration](https://github.com/conda-incubator/conda-auth/blob/main/conda_auth/plugin.py) and [plugin tests](https://github.com/conda-incubator/conda-auth/blob/main/tests/test_plugin.py). No `AGENTS.md` was present in the inspected public tree. |
| Tool execution, activation, and persistent state | [conda-exec instructions](https://github.com/conda-incubator/conda-exec/blob/3346c772937ce2fcb9d1a5049ba67af5024d8db8/AGENTS.md), [conda-global instructions](https://github.com/conda-incubator/conda-global/blob/91877a723d1d704c8e44111aaf423f7f0b5d23bb/AGENTS.md), or [conda-spawn](https://github.com/conda/conda-spawn). Choose the one matching the behavior. |
| Shell completion and startup performance | [conda-completion instructions](https://github.com/conda-incubator/conda-completion/blob/01cf070bf5919096c229da51fa1abc29a482905a/AGENTS.md). |
| Solver integration | [conda-pycosat-solver registration](https://github.com/conda/conda-pycosat-solver/blob/main/conda_pycosat_solver/plugin.py). Inspect the selected conda release's solver API and capability handling. |
| Attestations, verification, and untrusted data | [conda-sigstore instructions](https://github.com/conda-incubator/conda-sigstore/blob/81b2f0170548c60da625eccbb82c13f02c1ad41f/AGENTS.md). Its package-verifier integration used a pinned development conda revision when checked. Verify availability before using that hook. |

## Shared practices and local choices

Prefer stdlib and existing dependencies. Before adding a helper, look for a conda API, then a class that owns the data. Inline one-use glue. Add an abstraction when actual callers justify it.

Keep plugin registration small. Lazy imports are useful for expensive startup paths and optional dependencies. Ordinary implementation modules should keep imports at module scope unless the repository documents a reason otherwise. Measure the effect of startup changes.

For new Python modules, use `from __future__ import annotations`, modern annotations, and relative imports within the package. Mirror implementation structure in tests. Prefer plain pytest functions, parametrized cases with readable IDs, shared fixtures, and small fakes. Some existing plugins use other testing styles. Do not rewrite unrelated tests to enforce a new style.

Select tools from the target repository. Recent projects often use Ruff, `ty`, and Pixi. Environment names vary. A task named `check` may run static checks only. Read its definition.

Keep format names, aliases, and default filenames with the module that owns the format. When an existing dependency owns a schema, reuse its public validation and conversion APIs. Avoid parallel parsers or intermediate models without a concrete need.

Apply specialized requirements only where the feature needs them:

- Workspaces' `-e` environment selection and silent acceptance of `--json` on some side-effect commands are local CLI decisions.
- A submillisecond import target needs the repository's measurement method. It is not a guarantee for every conda plugin.
- Receipt verification and signature policy belong to features that process receipts or signed evidence.
- Shell handling needs platform-specific tests. A configuration file naming Windows or macOS is not proof of a native run.
- Cross-platform solving must account for conda's target subdirectory and virtual packages. Check the existing resolver before changing those values.

For credentials, archives, or signed data, test the actual failure cases. Avoid logging secrets or sensitive paths, validate untrusted inputs, and use the owning library's verification APIs. A decoded claim alone is not verified evidence.

For documentation, separate getting started, task guides, reference material, and explanations when the project uses Diataxis. Name the exact API and behavior. Preserve supported claims when editing prose. Follow the target repository's PR template and publication rules.
