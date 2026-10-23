# Choose and implement a conda plugin hook

## Check the installed API

Start with the [conda plugin guide](https://docs.conda.io/projects/conda/en/stable/dev-guide/plugins/index.html) and the installed version in the repository's development environment. Match the implementation to every supported version. Current online documentation can describe fields that an older installation does not have.

Inspect `conda.plugins.hookspec` and `conda.plugins.types` when a callback signature or field is unclear. Check the actual dependency revision for development builds. Avoid guessed version cutoffs and broad exception handling that conceals an unavailable hook.

| Need | Public extension to investigate | Example |
| --- | --- | --- |
| A new `conda <command>` | `conda_subcommands`, `CondaSubcommand` | conda-workspaces |
| User configuration | `conda_settings`, `CondaSetting` | conda-dev-request-headers |
| Channel authentication | `conda_auth_handlers`, `CondaAuthHandler` | conda-auth |
| Scoped HTTP headers | `conda_session_headers`, `conda_request_headers` | conda-dev-request-headers |
| Reading an environment format | `conda_environment_specifiers` | conda-lockfiles |
| Writing an environment format | `conda_environment_exporters` | conda-sboms, conda-lockfiles |
| A solver backend | `conda_solvers`, `CondaSolver` | conda-pycosat-solver |
| Checks exposed through `conda doctor` | `conda_health_checks` | conda's doctor plugins |
| Work around existing commands or transactions | The relevant pre/post command or transaction hook | conda-completion for command hooks |

See [repository-guidance.md](repository-guidance.md#choose-one-example) for source links. Choose the narrowest existing hook that owns the behavior. For an environment health check, consider `conda doctor` before adding a new top-level command. Verify availability instead of assuming every hook listed here exists in the project's minimum conda version.

## A complete small subcommand

This example adds `conda greet`. It demonstrates registration, delayed implementation imports, conda's parser helper, and JSON output. It has no network or environment mutations. The example declares conda 26.5 as its supported floor, which is not a claim about when the plugin system was introduced.

Use a fresh example directory. For an existing package, adapt its layout and build backend instead of replacing its metadata.

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "conda-greet"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["conda>=26.5"]

[project.entry-points.conda]
conda-greet = "conda_greet.plugin"

[tool.setuptools.packages.find]
where = ["src"]
```

`src/conda_greet/__init__.py`:

```python
from __future__ import annotations
```

`src/conda_greet/plugin.py`:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from conda.plugins import hookimpl

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace
    from collections.abc import Iterator

    from conda.plugins.types import CondaSubcommand


def configure_parser(parser: ArgumentParser) -> None:
    from conda.cli.helpers import add_output_and_prompt_options

    add_output_and_prompt_options(parser)
    parser.add_argument("--name", default="conda")


def run(args: Namespace) -> int:
    from .cli import execute

    return execute(args)


@hookimpl
def conda_subcommands() -> Iterator[CondaSubcommand]:
    from conda.plugins.types import CondaSubcommand

    yield CondaSubcommand(
        name="greet",
        summary="Print a greeting.",
        action=run,
        configure_parser=configure_parser,
    )
```

`src/conda_greet/cli.py`:

```python
from __future__ import annotations

import json
from argparse import Namespace

from conda.base.context import context


def execute(args: Namespace) -> int:
    result = {"greeting": f"Hello, {args.name}!"}
    if context.json:
        print(json.dumps(result))
    else:
        print(result["greeting"])
    return 0
```

With `configure_parser`, the action receives an `argparse.Namespace`. Without it, the action receives the remaining arguments as a tuple. Do not mix those callback shapes. See the [subcommand API](https://docs.conda.io/projects/conda/en/stable/dev-guide/plugins/subcommands.html).

The `add_output_and_prompt_options` helper already adds output and prompt flags, including `--json`. Do not add those flags a second time. This example uses `context.json` so conda's global flag is respected too. Only advertise structured output that the handler actually produces.

The registration module and package initializer must stay cheap to import. An unrelated `conda info` should not import `conda_greet.cli`. For a larger plugin, also avoid importing solver engines, HTTP clients, serializers, or optional packages while setting up help.

## Install and run the example

Conda discovers entry points installed in its own Python environment. Merely placing source on disk, installing into the target environment being inspected, or activating another environment does not make base conda discover the plugin.

For a standalone trial, provision conda through conda-forge, then use that same environment's interpreter:

```sh
conda create --name conda-plugin-dev --override-channels --channel conda-forge python=3.12 "conda>=26.5" pip setuptools
conda run -n conda-plugin-dev python -m pip install --no-deps --no-build-isolation -e .
conda run -n conda-plugin-dev python -m conda greet --name Ada
conda run -n conda-plugin-dev python -m conda greet --name Ada --json
conda run -n conda-plugin-dev python -m conda --json greet --name Ada
```

Run these from the example directory. The JSON commands should each emit `{"greeting": "Hello, Ada!"}` as the complete stdout document. Provisioning the dependencies first is why this editable install uses `--no-deps --no-build-isolation`. Do not use `pip install conda` as the environment bootstrap.

In an existing Pixi project, use its declared conda dependency and editable installation instead of introducing a second environment workflow. Read the task definitions before choosing an environment name.

If discovery fails, check the interpreter, installed distribution metadata, entry-point group, import target, disabled-plugin settings, and name conflicts. Reproduce through `python -m conda` in a fresh process before changing the implementation.

## Keep feature ownership clear

Use conda's settings API and configuration objects instead of parsing `.condarc` independently. Use `MatchSpec`, `Channel`, `PrefixData`, and activation or solver APIs when they own the data or operation. Prefer a public plugin interface where available. If an internal conda API is unavoidable, record the supported versions and test that dependency.

An environment exporter should serialize the supplied environment and records. It should not solve an environment or silently fetch missing provenance during serialization. Reuse the format's official library and keep output deterministic where the format allows it.

Keep authentication work in authentication or header hooks. Scope credentials to the intended host and path, and test that unrelated requests do not receive them.

Keep lifecycle hooks narrowly tied to the command or transaction they observe. A failed optional maintenance action should not accidentally prevent unrelated conda commands. Required verification failures need an explicit error policy.

Continue with [testing.md](testing.md) before claiming the plugin works.
