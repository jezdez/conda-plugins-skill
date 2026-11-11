# Sources for the synthesized practices

This is optional provenance. The bundled guides contain the development guidance and work without following these links. Another repository's instructions explain the examples used here but do not govern the target checkout.

These public sources were checked on 23 October 2026. Each GitHub file link pins the audited commit. These snapshots establish the source of a practice, not the current availability of every API or dependency version.

## Conda-skills follow-up

The committed conda-skills implementation was reviewed on 11 November 2026 at `40f1076d4efdde66beb1bd690f20ee6b706ca1b3`, through the 0.2.2 preparation commit. These links describe committed source and workflow behavior. They do not verify hosted CI, package publication, or native-platform execution during this review.

| Bundled practice | Source of the synthesis |
| --- | --- |
| [architecture.md](architecture.md): lightweight parser setup and helper extraction | [Registration][skills-plugin] and [parser configuration][skills-parser] keep execution imports deferred. [Instructions][skills-rules] allow one-caller extraction when it clarifies inputs, ordering, or testing, following commit `2b5105d`. |
| [architecture.md](architecture.md): distinct authoring and installed state | [Skill model][skills-model] owns loading, validation, skeleton creation, file enumeration, and bounded reads. [Quickstart][skills-quickstart] keeps authoring inputs separate from frozen installed selections. |
| [cli-and-processes.md](cli-and-processes.md): safe source previews and directory opening | [File reads][skills-model], [inspection][skills-inspect], and [directory opening][skills-open] implement commit `a5ef37d`. The 1 MiB read limit is this project's choice. Descriptor and containment checks do not prove resistance to every concurrent filesystem replacement. |
| [cli-and-processes.md](cli-and-processes.md): destination-derived removal and filesystem status | [Link operations][skills-links], [dispatch][skills-main], and [unlink tests][skills-unlink-tests] cover commit `0f4b4e4`. The destination identifies the source to verify, while forced recovery still protects files, directories, and redirected parents. |
| [cli-and-processes.md](cli-and-processes.md): literal terminal text, explicit scope, and batch preflight | [Output helpers][skills-output] and [quickstart][skills-quickstart] preserve literal data and explicit home authorization. [Batch tests][skills-quickstart-tests] cover preview, conflict detection before confirmation, and preservation of unselected links from commit `628715e`. |
| [plugin-guide.md](plugin-guide.md) and [testing.md](testing.md): native aliases and installed discovery | [Registration][skills-plugin], [plugin tests][skills-plugin-tests], and [installed round trips][skills-dispatch-tests] cover `CondaSubcommand.aliases` and commit `b436b2d`. [CLI fixtures][skills-cli-fixtures] isolate home, condarc, and inherited conda settings. The greet tests adapt the earlier file-based discovery pattern. |
| [testing.md](testing.md): artifact imports, source inventories, and generated packages | [Wheel test][skills-wheel-test] and [smoke script][skills-smoke] run outside the checkout and verify the imported location. [Build metadata][skills-project] includes shared fixtures in the sdist. [Tutorial checks][skills-tutorial-test] build, install, and discover generated packages. |
| [architecture.md](architecture.md) and [testing.md](testing.md): workspace tooling and one resolved version | [Workspace manifest][skills-workspace], [Python metadata][skills-project], and [recipe][skills-recipe] provision conda through channels, separate locked installs from named tasks, and resolve the conda version through Hatchling. Commits `23e67f1` and `8e33518` replace the duplicated recipe version and custom release script. Hatchling, Rich, environment names, and the 95% coverage threshold remain local choices. |
| [verification.md](verification.md): release dependencies and exact artifacts | [Release workflow][skills-release] depends on the complete [reusable tests][skills-tests] after commit `a333d8c`. [Conda publication][skills-publish] builds from the digest-verified published sdist, attests the stored package, and uploads through a protected environment. [Release guidance][skills-releasing] records partial-publication recovery and separate external publisher setup. |
| [documentation.md](documentation.md): user installation and isolated examples | [Installation guide][skills-installation] separates user setup from contributor tooling. [Installed-skill tutorial][skills-use] distinguishes source selection, destination scope, and trust. [Demo setup][skills-demo-setup] and [skill-forge tape][skills-demo-forge] use disposable state and an explicit temporary source prefix. |

The earlier review at `68665e9b71d0f287da71f5ec123ad76fcf8318de` reproduced a cyclic-link failure on Python 3.11.18 with conda 26.9.4, while the same probe succeeded on Python 3.14.10. Both runs were on macOS ARM64. Commit `fee7aa8` subsequently added cycle handling and regression coverage in [link operations][skills-links] and [link tests][skills-link-tests]. The recommendation to test minimum and current Python remains applicable. The old reproduction is historical evidence, not a current failure claim.

The archive-integrity distinction in [verification.md](verification.md#separate-archive-integrity-from-metadata-checks) originally came from a disposable source archive missing its final eight gzip bytes. Strict Twine metadata validation passed while a complete gzip read raised `EOFError`. The current [release workflow][skills-release] uses `gzip -t` before recording the source digest. Tests of removed custom release helpers are not evidence for their replacement.

[skills-plugin]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/plugin.py
[skills-parser]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/cli/parser.py
[skills-rules]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/AGENTS.md
[skills-model]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/skills.py
[skills-quickstart]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/cli/quickstart.py
[skills-inspect]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/cli/inspect.py
[skills-open]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/cli/open.py
[skills-links]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/links.py
[skills-main]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/cli/main.py
[skills-unlink-tests]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/tests/cli/test_unlink.py
[skills-output]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/src/conda_skill/cli/output.py
[skills-quickstart-tests]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/tests/cli/test_quickstart.py
[skills-plugin-tests]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/tests/test_plugin.py
[skills-dispatch-tests]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/tests/cli/test_dispatch.py
[skills-cli-fixtures]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/tests/cli/conftest.py
[skills-wheel-test]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/scripts/test_wheel.py
[skills-smoke]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/scripts/smoke_plugin.py
[skills-project]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/pyproject.toml
[skills-workspace]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/conda.toml
[skills-recipe]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/recipe/recipe.yaml
[skills-release]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/.github/workflows/release.yml
[skills-tests]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/.github/workflows/tests.yml
[skills-publish]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/.github/workflows/publish-conda.yml
[skills-releasing]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/RELEASING.md
[skills-link-tests]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/tests/test_links.py
[skills-tutorial-test]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/scripts/test_tutorial.py
[skills-installation]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/docs/how-to/installation.md
[skills-use]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/docs/how-to/use-an-installed-skill.md
[skills-demo-setup]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/demos/setup.sh
[skills-demo-forge]: https://github.com/jezdez/conda-skills/blob/40f1076d4efdde66beb1bd690f20ee6b706ca1b3/demos/skill-forge.tape

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

## Documentation and demos

| Practice in [documentation.md](documentation.md) | Source of the synthesis |
| --- | --- |
| Substantial tutorials with prerequisites, concepts, commands, result inspection, cleanup, and onward navigation | The [SBOM getting-started tutorial][sbom-tutorial] and [first-workspace tutorial][ws-tutorial] develop complete reader journeys. Their depth informs the examples without imposing their product-specific commands on other plugins. |
| Diátaxis navigation, Sphinx, conda-sphinx-theme, MyST, and sphinx-design | [SBOM's homepage][sbom-docs-index] and [small Sphinx configuration][sbom-docs-conf] combine the four documentation purposes with cards and toctrees. [Workspaces instructions][ws-rules] require short tab labels and restrained emphasis. Its [API index][ws-api-index] splits reference material by subject. |
| Exact page references and generated help | [Spawn's quickstart][spawn-quickstart] uses Sphinx document and section references. Its [CLI reference][spawn-cli] generates help from the installed command. Static command examples elsewhere still need separate execution checks. |
| Strict documentation builds | [SBOM project metadata][sbom-project] declares a warnings-as-errors Sphinx build with unresolved-reference checking. Other repositories use different tasks, so the guide asks agents to inspect the target's configuration. |
| VHS settings, a short visible story, fixtures, and media policy | [Shared workspace settings][ws-demo-settings], [its quickstart tape][ws-demo-quickstart], and [Exec's recording guide][exec-demos] establish the font, colors, dimensions, timing, and regeneration pattern. [Workspaces' demo guide][ws-demos] discloses an omitted image-build wait. |
| Disposable recording state and shell-specific demonstrations | [Completion's quickstart tape][completion-demo] and [demo tests][completion-demo-tests] cover temporary setup, cleanup, and unrelated files. Its [Fish recording][completion-fish-demo] adapts the shared style to another shell. |

The demo style was present in Workspaces, Exec, Global, and Completion. The inspected SBOM, Auth, Spawn, and Sigstore trees contained no `.tape` or `.gif` demo assets. The guide's reader review, accessibility checks, and representative example execution are recommendations, not claims that every source repository already automates them.

[sbom-tutorial]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/docs/tutorials/getting-started.md
[ws-tutorial]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/docs/tutorials/first-workspace.md
[sbom-docs-index]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/docs/index.md
[sbom-docs-conf]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/docs/conf.py
[ws-api-index]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/docs/reference/api.md
[spawn-quickstart]: https://github.com/conda/conda-spawn/blob/45f7b32c84079e709a5845fdf0cf982625d3b669/docs/quickstart.md
[spawn-cli]: https://github.com/conda/conda-spawn/blob/45f7b32c84079e709a5845fdf0cf982625d3b669/docs/cli.md
[sbom-project]: https://github.com/conda-incubator/conda-sboms/blob/fbfadd580a9961f28fa144c954861f108ecd3918/pyproject.toml
[ws-demo-settings]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/demos/_settings.tape
[ws-demo-quickstart]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/demos/quickstart.tape
[exec-demos]: https://github.com/conda-incubator/conda-exec/blob/3346c772937ce2fcb9d1a5049ba67af5024d8db8/demos/README.md
[ws-demos]: https://github.com/conda-incubator/conda-workspaces/blob/1eaddb9e6a0c6a516a8600ab611be96f8d9853cf/demos/README.md
[completion-demo]: https://github.com/conda-incubator/conda-completion/blob/01cf070bf5919096c229da51fa1abc29a482905a/demos/quickstart.tape
[completion-demo-tests]: https://github.com/conda-incubator/conda-completion/blob/01cf070bf5919096c229da51fa1abc29a482905a/tests/test_demos.py
[completion-fish-demo]: https://github.com/conda-incubator/conda-completion/blob/01cf070bf5919096c229da51fa1abc29a482905a/demos/fish-completion.tape

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
