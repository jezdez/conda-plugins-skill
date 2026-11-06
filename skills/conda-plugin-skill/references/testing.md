# Verify a conda plugin

## Establish the environment first

Read the repository's task definitions. Find the environment containing both conda and the installed plugin. A shell function named `conda` may still invoke base even after another environment is activated.

Use the selected environment's Python explicitly:

```sh
pixi run -e test python -m conda --version
pixi run -e test python -m conda greet --help
```

These commands assume the repository has a `test` environment and the example plugin. Substitute its real environment and command. Importing from the source tree does not prove package installation or entry-point discovery.

For a missing command, inspect in order:

1. The interpreter running conda and the interpreter where the distribution is installed.
2. The installed distribution's `conda` entry-point group and import target.
3. The decorated hook and the hook objects it yields.
4. Disabled-plugin settings, import errors, and duplicate registered names.
5. A fresh installed CLI process.

Do not repair a packaging or interpreter mismatch by changing a working handler.

## Runnable discovery and CLI tests

These tests go with the complete `conda-greet` example in [plugin-guide.md](plugin-guide.md). Install that example and pytest into the intended conda runtime first. Save this as `tests/test_plugin.py` and run it with that interpreter.

The first test starts outside the source directory, reads installed metadata, and uses a real plugin manager. It also proves that discovery and parser setup do not load the command implementation.

```python
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable
from importlib.metadata import distribution
from pathlib import Path

import pytest


def check_installed_discovery() -> None:
    import argparse

    from conda.plugins.hookspec import CondaSpecs
    from conda.plugins.manager import CondaPluginManager

    entry_points = [
        entry
        for entry in distribution("conda-greet").entry_points
        if entry.group == "conda"
    ]
    assert [(entry.name, entry.value) for entry in entry_points] == [
        ("conda-greet", "conda_greet.plugin")
    ]
    manager = CondaPluginManager()
    manager.add_hookspecs(CondaSpecs)
    assert manager.load_entrypoints("conda", name="conda-greet") == 1
    commands = manager.get_hook_results("subcommands")
    assert [command.name for command in commands] == ["greet"]
    commands[0].configure_parser(argparse.ArgumentParser())
    assert "conda_greet.cli" not in sys.modules


@pytest.fixture
def cli_environment(tmp_path: Path) -> dict[str, str]:
    home = tmp_path / "home"
    home.mkdir()
    condarc = tmp_path / "condarc"
    condarc.write_text("{}\n", encoding="utf-8")
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("CONDA_") and key not in {"CONDARC", "PYTHONPATH"}
    }
    environment.update(
        HOME=str(home),
        USERPROFILE=str(home),
        XDG_CONFIG_HOME=str(home / ".config"),
        CONDARC=str(condarc),
        CONDA_NO_PLUGINS="false",
        CONDA_JSON="false",
        CONDA_AUTO_UPDATE_CONDA="false",
    )
    return environment


def test_installed_discovery_keeps_command_unloaded(
    tmp_path: Path, cli_environment: dict[str, str]
) -> None:
    subprocess.run(
        [sys.executable, str(Path(__file__).resolve())],
        cwd=tmp_path,
        env=cli_environment,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.fixture
def run_conda(
    tmp_path: Path, cli_environment: dict[str, str]
) -> Callable[..., subprocess.CompletedProcess[str]]:
    def run(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "conda", *arguments],
            cwd=tmp_path,
            env=cli_environment,
            capture_output=True,
            text=True,
            timeout=60,
        )

    return run


@pytest.mark.parametrize(
    "arguments",
    [
        ("--json", "greet", "--name", "Ada"),
        ("greet", "--name", "Ada", "--json"),
    ],
    ids=["global-json", "command-json"],
)
def test_json_is_the_complete_stdout_document(
    run_conda: Callable[..., subprocess.CompletedProcess[str]],
    arguments: tuple[str, ...],
) -> None:
    result = run_conda(*arguments)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"greeting": "Hello, Ada!"}


@pytest.mark.parametrize(
    ("arguments", "status", "message"),
    [
        (("greet", "--name", "Ada"), 0, "Hello, Ada!"),
        (("greet", "--unknown-option"), 2, "unrecognized arguments"),
    ],
    ids=["human-output", "invalid-option"],
)
def test_cli_result(
    run_conda: Callable[..., subprocess.CompletedProcess[str]],
    arguments: tuple[str, ...],
    status: int,
    message: str,
) -> None:
    result = run_conda(*arguments)
    assert result.returncode == status
    output = result.stdout if status == 0 else result.stderr
    assert message in output


if __name__ == "__main__":
    check_installed_discovery()
```

Adapt the distribution, hook, assertions, and configuration to the real plugin. The isolated manager deliberately loads only this distribution. Keep an installed CLI test too, because that exercises integration with conda's other hooks.

The fresh-process probe executes this test file rather than a program embedded in a string, so normal linting and code navigation cover it. Keep execution imports out of its top level. Test collection may already load implementation modules in the parent process; it cannot establish lazy startup. Clearing inherited settings is fixture isolation, not a rule for real child processes that should preserve the user's environment. Add back only settings required by a particular test. An isolated home and condarc do not isolate every possible system configuration source.

For a cheap-startup regression, test each relevant phase: package import, hook enumeration, parser setup, and an unrelated command. Assert that the specific expensive or optional implementation stays out of `sys.modules`. If the regression created a cache or contacted a service, use a temporary configured cache directory and fail-fast recording fakes at that operation's call site. Prove no files or calls occurred before execution. Do not infer that from elapsed time.

## Test the behavior being changed

For a bug, reproduce the reported command and add a regression case that fails for the observed reason before the fix. Prefer adding a parameter case to an existing test. Assert observable behavior.

Use plain pytest functions and fixtures for new tests unless repository guidance specifies otherwise. Use `tmp_path`, `monkeypatch`, recording closures, and small real fakes. Shared setup belongs in fixtures. Do not add tests that merely restate assignments or increase coverage without checking behavior.

| Behavior | Useful checks |
| --- | --- |
| JSON composition | Parse all stdout while nested operations emit progress, assert no extra document or styling |
| Configuration | Defaults, invalid types and ranges, conda precedence, explicit environment aliases |
| Headers and authentication | Exact host/path matches, lookalikes, redirects, missing variables, unsafe rendered values, credential redaction |
| Formats | Aliases and filename detection, exact record preservation, schema validity, deterministic output, malformed input |
| Solver targets | Target specifications, subdirectories and virtual packages, pins, channels, failure cleanup |
| Process execution | Preserved argv including empty arguments, status, cancellation, activation changes, parent state unchanged |
| State files | Previous file survives failed writes, temporary files cleaned, concurrent update policy |
| Authoring and links | Serialized metadata round-trips, generated recipe builds, installed discovery, redirected roots and parents, home-scope authorization, dangling and cyclic links on minimum/current Python, Windows cross-drive behavior |
| Optional maintenance | Failure preserves the original command's result without hiding diagnostics |

Use deterministic local responses for network and credential tests. Live-service tests should be opt-in and separately reported. Keep credentials and colleague environments out of fixtures.

Direct operation tests and installed CLI tests serve different purposes. Use both when registration or dispatch changes. A schema-valid SBOM can still invent provenance. A successful cross-platform solve does not prove a native installation.

For signed evidence, artifact binding, authorization, and offline or cache failures, use the [verification test cases](verification.md#test-rejection-stages).

## Measure startup correctly

Measure plugin import cost separately from total conda startup, in fresh processes with repeated samples. Compare the same command, interpreter, and configuration before and after the change. Keep network access and cache warming out of an import measurement.

Use module-load and side-effect assertions for correctness. Keep noisy timing benchmarks separate unless the repository defines a stable threshold and tolerance.

`CONDA_NO_PLUGINS=true` or `conda --no-plugins` can help diagnose external-plugin failures. Those modes remove other external plugins too, so they are not an exact measurement of this plugin's cost.

## Optional security review

Security tests should exercise the actual failure cases in credential handling, request scoping, archive extraction, subprocess execution, and evidence verification. Use deterministic local inputs and keep regression tests for confirmed bugs.

When a security review is requested or otherwise in the authorized scope, Codex Security can provide additional analysis if available:

- Use `security-diff-scan` for a pull request, commit, branch diff, or working-tree patch.
- Use `security-scan` for an explicitly scoped repository or directory audit without a diff. Do not turn an ordinary change into a whole-repository audit.
- Use `verify-fix` only when the user explicitly asks whether a reported security vulnerability has been fixed.

Follow the installed workflow's setup, permission, and reporting requirements. Do not install or enable a service, upload source, or widen the review merely because this skill mentions it. See the [Codex Security plugin guide](https://learn.chatgpt.com/docs/security/plugin).

Treat findings as claims to investigate. Record the affected code, reproducer or other evidence, validation result, and unresolved coverage. Passing functional tests does not disprove a vulnerability, and a scan with no findings does not establish that the code is secure. Keep scan results separate from tests actually run.

Codex Security is optional. If it is unavailable during an authorized security review, carry out the requested local tests and code review and state that limitation in the review report. Its absence does not block ordinary plugin work or waive a required security check specified by the target repository.

## Complete the required checks

Run the full test suite, lint, formatting check, and type check required by the target repository. For documentation changes, follow the [docs and demo checks](documentation.md#validate-the-readers-experience), including the declared build and representative example execution. Report failed or blocked checks clearly.

For conda-workspaces, the supplied project instructions require:

```sh
pixi run -e test pytest
pixi run -e dev lint
pixi run -e dev format-check
pixi run -e dev type-check
```

These commands describe the pinned Workspaces snapshot, not every current plugin. Confirm that a combined task includes tests. In a repository already using conda-workspaces, read `conda.toml` and use its declared environments: `conda workspace install --locked -e default` installs the lock, then `conda task run -e default check` runs a named task. Arbitrary commands use `conda workspace run -e default -- COMMAND`. Do not put `--locked` on task execution or add Pixi just to match this guide. Environment names remain project-specific.

After dependency, feature, task, or workspace metadata changes, regenerate the owning lockfile: `pixi lock` for Pixi or `conda workspace lock` for conda-workspaces. Runtime dependencies belong in shared features, with tests, docs, and artifact tooling in the environments that use them. Editable installs also need their build backend provisioned. Measure subprocess and branch coverage where required, but do not copy another project's numeric coverage threshold as a universal rule.

Exercise the minimum and current supported conda versions for API changes. Native-platform behavior needs a run on that platform. Test released conda when claiming released compatibility.

State which checks ran and what remains unverified. Keep local results, hosted CI, publication, and downstream availability distinct. After an authorized push, take at most one CI snapshot unless the user asked for monitoring.
