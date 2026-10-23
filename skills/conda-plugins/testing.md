# Verify a conda plugin

## Establish the environment first

Read the repository's Pixi or other task definitions. Find the environment containing both conda and the installed plugin. A shell function named `conda` may still invoke base even after another environment is activated.

Use the selected environment's Python explicitly, for example:

```sh
pixi run -e test python -m conda --version
pixi run -e test python -m conda greet --help
```

These commands assume that the repository has a `test` environment and the example plugin. Substitute its real environment and command. A standalone `import` from the source tree does not test package installation or entry-point discovery.

## Test the behavior being changed

For a bug, reproduce the reported command and add a regression case that fails for the observed reason before the fix. Prefer adding a parameter case to an existing test. Assert observable behavior and explain which regression the test catches.

Use plain pytest functions and fixtures for new tests unless repository guidance specifies otherwise. Use `tmp_path`, `monkeypatch`, recording closures, and small real fakes. Do not add tests that merely restate assignments or increase coverage without checking behavior.

Match coverage to the hook:

| Hook or behavior | Useful checks |
| --- | --- |
| Entry point and subcommand | Installed metadata, fresh-process discovery, help, argument errors, exit status, no duplicate registration |
| JSON output | Parse all stdout, assert fields and types, exercise global and command-local flags, keep progress out of the document |
| Settings and authentication | Defaults, invalid values, configuration precedence, host/path scoping, redirects where relevant, secret redaction |
| Specifiers and exporters | Format detection, invalid input, deterministic records, format validation, round trips where supported |
| Solver | Unsatisfiable input, channels, pins, target platform, virtual packages, reported capabilities |
| Process and shell execution | Arguments, quoting, exit status, cancellation, relevant native platforms |
| Startup hooks | Unrelated commands still work, expected optional dependencies remain unloaded, no I/O side effects |
| Signature or archive handling | Wrong identity or artifact, malformed input, size limits, traversal, cleanup after failure |

Direct handler tests and installed CLI smoke tests check different things. Include both where the change affects registration or dispatch. For CLI tests, use a subprocess with the intended interpreter and a controlled temporary prefix. Do not inventory a colleague's real environment as a test fixture.

## Measure startup correctly

Measure plugin import cost separately from total conda startup, in fresh processes with repeated samples. Compare the same command, interpreter, and configuration before and after the change. Keep network access and cache warming out of an import measurement.

Use a targeted `sys.modules` assertion to catch accidental loading of a costly optional module when that is the regression. Do not add a brittle wall-clock threshold unless the repository defines the benchmark and tolerance.

`CONDA_NO_PLUGINS=true` or `conda --no-plugins` can help diagnose external-plugin failures. Those modes also remove other external plugins, so they are not an exact measurement of this plugin's cost.

## Complete the required checks

Run the full test suite, lint, formatting check, and type check required by the target repository. Run its documentation build for documentation changes where required. Report any failed or blocked check clearly.

For conda-workspaces, the supplied project instructions require:

```sh
pixi run -e test pytest
pixi run -e dev lint
pixi run -e dev format-check
pixi run -e dev type-check
```

Other plugins have different commands. Confirm that a combined task actually includes tests. After dependency, feature, task, or workspace metadata changes, regenerate `pixi.lock` with `pixi lock` and include it with the metadata change.

Exercise the minimum and current supported conda versions for API changes. Native-platform behavior needs a run on that platform. Test against released conda when claiming released compatibility.

State which checks ran and what remains unverified. Keep local results, hosted CI, publication, and availability to downstream users distinct. After an authorized push, take at most one CI snapshot unless the user asked for monitoring.
