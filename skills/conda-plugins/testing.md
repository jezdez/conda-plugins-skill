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
from pathlib import Path

import pytest


def test_installed_discovery_keeps_command_unloaded(tmp_path: Path) -> None:
    script = """
import argparse
import sys
from importlib.metadata import distribution

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
"""
    subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def run_conda(tmp_path: Path) -> Callable[..., subprocess.CompletedProcess[str]]:
    condarc = tmp_path / "condarc"
    condarc.write_text("{}\n")
    environment = {
        **os.environ,
        "CONDARC": str(condarc),
        "CONDA_NO_PLUGINS": "false",
        "CONDA_JSON": "false",
    }

    def run(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "conda", *arguments],
            cwd=tmp_path,
            env=environment,
            capture_output=True,
            text=True,
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
```

Adapt the distribution, hook, assertions, and configuration to the real plugin. The isolated manager deliberately loads only this distribution. Keep an installed CLI test too, because that exercises integration with conda's other hooks.

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
| Optional maintenance | Failure preserves the original command's result without hiding diagnostics |

Use deterministic local responses for network and credential tests. Live-service tests should be opt-in and separately reported. Keep credentials and colleague environments out of fixtures.

Direct operation tests and installed CLI tests serve different purposes. Use both when registration or dispatch changes. A schema-valid SBOM can still invent provenance. A successful cross-platform solve does not prove a native installation.

## Verify signed evidence in stages

When a plugin verifies attestations, archives, or cached evidence, give each check a distinct result. A cryptographically valid signature alone does not establish artifact identity, accepted statement content, or publisher authorization.

Apply the protocol's required checks in this order:

1. Select the expected source and enforce the configured online or offline policy.
2. Bound transport, decompression, and parser input. Check declared lengths and count actual streamed bytes. Reject oversized data before allocating or parsing the whole document.
3. If authenticated metadata advertises the evidence digest, verify that digest over the fetched bytes before interpreting them. An advertised but invalid object is an error, not a reason to accept weaker evidence.
4. Parse the bounded verification envelope and verify its cryptographic evidence with the intended trust roots and time policy.
5. Validate the authenticated statement's type and required fields, then bind its subject digest to the actual artifact being checked.
6. Apply the caller's accepted signer identities, issuer, predicate type, and authorization policy.
7. Cache only the result appropriate to those checks. Keep raw evidence storage distinct from a trusted acceptance decision.

Use the supported verification library for cryptography. Keep parsing needed for cryptographic verification inside that library. Do not act on unverified statement fields.

A generic verification helper should return verified evidence and identity. The application decides whether that evidence meets its own policy. Do not bake one caller's predicate policy into a general envelope verifier.

A content-addressed cache proves which bytes were stored, not that those bytes remain acceptable under current policy. Revalidate data after reading it, account for trust-policy changes and expiry, and write atomically. In offline mode, fail clearly when acceptable cached evidence is unavailable. Do not silently access the network.

Build failure tests around the stage that must reject the input:

| Case | Required observation |
| --- | --- |
| Oversized stream or decompressed input | Stops before unbounded allocation or statement processing |
| Digest mismatch | No statement use or trusted cache entry |
| Valid signature, wrong artifact | Artifact binding fails |
| Correct artifact, unapproved identity or predicate | Authorization fails |
| Malformed or corrupted cache | Rejected or refreshed only when online policy allows |
| Offline cache miss | No request, explicit unavailable-evidence result |
| Failed temporary write or interrupted operation | Previous cache remains usable, no partial trusted result |
| Untrusted URL or exception text | No credentials in logs and no interpreted terminal markup |

Use local fixtures and the repository's existing verifier fakes to reach each stage. A test that fails at parsing does not prove the authorization check works.

## Measure startup correctly

Measure plugin import cost separately from total conda startup, in fresh processes with repeated samples. Compare the same command, interpreter, and configuration before and after the change. Keep network access and cache warming out of an import measurement.

Use module-load and side-effect assertions for correctness. Keep noisy timing benchmarks separate unless the repository defines a stable threshold and tolerance.

`CONDA_NO_PLUGINS=true` or `conda --no-plugins` can help diagnose external-plugin failures. Those modes remove other external plugins too, so they are not an exact measurement of this plugin's cost.

## Complete the required checks

Run the full test suite, lint, formatting check, and type check required by the target repository. Run its documentation build where required. Report failed or blocked checks clearly.

For conda-workspaces, the supplied project instructions require:

```sh
pixi run -e test pytest
pixi run -e dev lint
pixi run -e dev format-check
pixi run -e dev type-check
```

Other plugins have different commands. Confirm that a combined task includes tests. After dependency, feature, task, or workspace metadata changes, regenerate `pixi.lock` with `pixi lock` and include it with the metadata change.

Exercise the minimum and current supported conda versions for API changes. Native-platform behavior needs a run on that platform. Test released conda when claiming released compatibility.

State which checks ran and what remains unverified. Keep local results, hosted CI, publication, and downstream availability distinct. After an authorized push, take at most one CI snapshot unless the user asked for monitoring.
