# Sources for the synthesized practices

This is optional provenance. The bundled guides contain the development guidance and work without following these links. Another repository's instructions explain the examples used here but do not govern the target checkout.

These public sources were checked on 23 October 2026. Each GitHub file link pins the audited commit. These snapshots establish the source of a practice, not the current availability of every API or dependency version.

## Architecture, formats and solvers

| Bundled guide and practice | Source of the synthesis |
| --- | --- |
| [architecture.md](architecture.md): registration separate from execution, model ownership, helper decision order and deliberate lazy imports | [Workspaces instructions][ws-rules] state the dependency-first, owning-class, shared-function and one-use-glue decisions. [SBOM instructions][sbom-rules] distinguish cohesive stateful objects from stateless wrappers and delay shared models until real exporters need them. |
| [formats-and-solvers.md](formats-and-solvers.md): requested specifications versus exact records, format-owned metadata and generic exporter callbacks | [SBOM instructions][sbom-rules], [registration][sbom-plugin] and [CycloneDX implementation][sbom-code] show versioned format metadata, exact-record requirements and a callback that delegates to its exporter object. |
| [formats-and-solvers.md](formats-and-solvers.md): one serializer shared by command and exporter entry points | [Workspaces export.py][ws-export] delegates lock composition to `CondaLockLoader.compose`. [Lock rendering][ws-lock] uses the same export implementation after solving. |
| [formats-and-solvers.md](formats-and-solvers.md): local validation, narrow schema adapters and upstream conversion | [The workspace loader][ws-lock] validates selected references, channels and digests, adapts the environment name and schema version, then calls the [conda-lockfiles v6 model and converter][lock-v6]. Its [compatibility model extension][ws-compat] preserves `build_number` with older supported dependencies. |
| [formats-and-solvers.md](formats-and-solvers.md): preserving shared manifest tables and platform-specific requirements | [ManifestParser][ws-parser] owns export, merge behavior and dependency intersection by both name and value. Its documented `PyprojectTomlParser` override preserves peer tables when updating `[tool.conda]`. |
| [formats-and-solvers.md](formats-and-solvers.md) and [testing.md](testing.md): truthful graphs, deterministic output and preservation tests | [CycloneDX implementation][sbom-code] and [tests][sbom-tests] cover exact records, requested or inferred roots, disconnected cycles, missing edges, sanitization and reproducibility. [Lockfile tests][lock-tests] cover build-number preservation through conversion. |
| [formats-and-solvers.md](formats-and-solvers.md): solver subdirectories, virtual packages, override precedence and temporary prefixes | [ResolvedEnvironment][ws-resolver] owns `solve_for_platform`, `virtual_package_overrides` and `scoped_virtual_packages`. [Lock rendering][ws-lock] resolves each target and distinguishes empty-prefix full solves from updates seeded with a locked baseline. The caution about overlapping threaded solves follows from mutation of shared conda context and `os.environ`. |
| [formats-and-solvers.md](formats-and-solvers.md): capability checks, alias collisions and recursive hook invocation | [Pycosat registration][solver-plugin] conditionally registers `classic` by inspecting other providers through `subset_hook_caller`. Its [tests][solver-tests] cover provider presence, absence and caching. |

## CLI, authentication and operational practices

| Bundled practice | Source of the synthesis |
| --- | --- |
| Subcommand organization, JSON composition and parser helpers | [Workspaces instructions][ws-rules] supply the CLI examples. Its environment-selection flags and silent JSON acceptance on some commands remain local choices. |
| Small settings hooks, scoped headers, validation and secret handling | [Request-header instructions][headers-rules], [registration][headers-plugin] and [selector implementation][headers-code]. This plugin is intended for development use. |
| Authentication handlers and startup regression tests | [Auth registration][auth-plugin] and [plugin tests][auth-tests] show delayed implementation imports and a fresh-process check for eagerly loaded CLI, storage and keyring modules. The [handler][auth-handler] checks transport before cached credentials, and [credential models][auth-credentials] define safe status fields. |
| Tool execution, activation and persistent state | [Exec instructions][exec-rules], [Global instructions][global-rules] and [Spawn registration][spawn-plugin] supply distinct examples of command execution, conda API reuse, state writes and compatible subcommand aliases. |
| Shell completion, lifecycle hooks and startup cost | [Completion instructions][completion-rules] document lazy registration, shell coverage and failure-tolerant completion regeneration. The [manifest writer][completion-manifest] uses atomic file replacement and bounded reads. Its import-time target is a project measurement requirement, not a universal conda guarantee. |
| [verification.md](verification.md) and [testing.md](testing.md): attestations, bounded input, hermetic tests and publication rules | [Sigstore instructions][sigstore-rules]. Its package-verifier integration used a pinned development conda revision at this audit. Accepted standards did not establish released hook availability. |

The inspected public trees for conda-lockfiles, conda-pycosat-solver, conda-auth and conda-spawn did not contain `AGENTS.md`. Their implementation, metadata and tests supplied the examples instead. Recommended test cases in the bundled guides are synthesis, not a claim that every source repository already implements every check.

[ws-rules]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/AGENTS.md
[ws-export]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/conda_workspaces/export.py
[ws-lock]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/conda_workspaces/lockfile.py
[ws-compat]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/conda_workspaces/_lockfile_compat.py
[ws-parser]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/conda_workspaces/manifests/base.py
[ws-resolver]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/conda_workspaces/resolver.py
[sbom-rules]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/AGENTS.md
[sbom-plugin]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/conda_sboms/plugin.py
[sbom-code]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/conda_sboms/cyclonedx.py
[sbom-tests]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/tests/test_cyclonedx.py
[lock-v6]: https://github.com/conda/conda-lockfiles/blob/9ff2726b1495b974e6086a0cc19cab2e8c7da0b0/conda_lockfiles/rattler_lock/v6.py
[lock-tests]: https://github.com/conda/conda-lockfiles/blob/9ff2726b1495b974e6086a0cc19cab2e8c7da0b0/tests/rattler_lock/test_v6.py
[solver-plugin]: https://github.com/conda/conda-pycosat-solver/blob/3e67ee39b82a50ba10078a459abd20f66b921934/conda_pycosat_solver/plugin.py
[solver-tests]: https://github.com/conda/conda-pycosat-solver/blob/3e67ee39b82a50ba10078a459abd20f66b921934/tests/test_plugin.py
[headers-rules]: https://github.com/jezdez/conda-dev-request-headers/blob/845fb12f994ccf33c6e61a0d70500b1a2dd66abb/AGENTS.md
[headers-plugin]: https://github.com/jezdez/conda-dev-request-headers/blob/845fb12f994ccf33c6e61a0d70500b1a2dd66abb/conda_dev_request_headers/plugin.py
[auth-plugin]: https://github.com/conda-incubator/conda-auth/blob/37742f3cec8a2a3a6c2945bcea451e204bbe9d32/conda_auth/plugin.py
[auth-tests]: https://github.com/conda-incubator/conda-auth/blob/37742f3cec8a2a3a6c2945bcea451e204bbe9d32/tests/test_plugin.py
[exec-rules]: https://github.com/conda-incubator/conda-exec/blob/3346c772937ce2fcb9d1a5049ba67af5024d8db8/AGENTS.md
[global-rules]: https://github.com/conda-incubator/conda-global/blob/91877a723d1d704c8e44111aaf423f7f0b5d23bb/AGENTS.md
[spawn-plugin]: https://github.com/conda/conda-spawn/blob/45f7b32c84079e709a5845fdf0cf982625d3b669/conda_spawn/plugin.py
[completion-rules]: https://github.com/conda-incubator/conda-completion/blob/01cf070bf5919096c229da51fa1abc29a482905a/AGENTS.md
[sigstore-rules]: https://github.com/conda-incubator/conda-sigstore/blob/81b2f0170548c60da625eccbb82c13f02c1ad41f/AGENTS.md

[headers-code]: https://github.com/jezdez/conda-dev-request-headers/blob/845fb12f994ccf33c6e61a0d70500b1a2dd66abb/conda_dev_request_headers/headers.py
[auth-handler]: https://github.com/conda-incubator/conda-auth/blob/37742f3cec8a2a3a6c2945bcea451e204bbe9d32/conda_auth/handlers/base.py
[auth-credentials]: https://github.com/conda-incubator/conda-auth/blob/37742f3cec8a2a3a6c2945bcea451e204bbe9d32/conda_auth/credentials.py
[completion-manifest]: https://github.com/conda-incubator/conda-completion/blob/01cf070bf5919096c229da51fa1abc29a482905a/conda_completion/manifest.py
