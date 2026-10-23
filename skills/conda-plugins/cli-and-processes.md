# CLI, processes, configuration, and credentials

Read this guide when a plugin parses commands, launches programs, manages local state, adds request headers, or authenticates channels. Apply the target repository's conventions and supported conda versions.

## Separate plugin arguments from child arguments

Choose where plugin parsing stops. For a new command runner, put the executable and its arguments in one `argparse.REMAINDER` positional. Plugin options must precede that command:

```python
parser.add_argument("command", nargs=argparse.REMAINDER, metavar="COMMAND")
```

Remove only a wrapper separator at the start of the entire command, before the executable. Preserve every argument after the executable:

```python
command = list(args.command)
if command[:1] == ["--"]:
    command = command[1:]
if not command:
    raise CondaValueError("Provide an executable to run.")

result = subprocess.run(command, env=child_env)
if os.name == "posix" and result.returncode < 0:
    return 128 - result.returncode
return result.returncode
```

The handler uses `CondaValueError` from `conda.exceptions`. With this layout, both `conda example grep -- -pattern` and `conda example -- grep -- -pattern` forward `grep`, `--`, and `-pattern`. The child needs its separator to interpret `-pattern` as data.

For `conda example -- ruff check --output-format json`, `--output-format` and `json` belong to Ruff. Preserve spaces, empty arguments, quotes, and later `--` arguments as individual strings. Do not join the list and parse it again with `shlex.split`. Do not enable `shell=True` to solve quoting problems.

When maintaining an existing runner, preserve its documented separator syntax explicitly. A separate executable positional followed by a remainder can consume a child's leading `--` during parsing, so test the actual parser's forwarding behavior.

Preserve ordinary child exit statuses. On POSIX, `subprocess` represents signal termination as a negative number. The example converts it to the conventional shell status `128 + signal` rather than passing a negative number to `sys.exit`. If the command promises conventional launcher errors, distinguish an executable that cannot be found from one that cannot be executed, commonly statuses 127 and 126.

Keep a standalone console script and the conda subcommand on the same parser and handler. Preserve established command naming. For new workspace-style management commands, use `-e` or `--environment` for the target and reserve the positional argument for the package or executable. Distinguish removing a dependency from deleting its entire environment.

## Choose an activation level

| Operation | Implementation | Limitation |
| --- | --- | --- |
| Run an executable by path | Pass its path and arguments directly | Does not activate its environment |
| Apply conda environment variables | Apply the activator's exported and unset variables | Does not execute `activate.d` scripts |
| Start an activated shell | Use shell-specific activation code and startup handling | Requires shell lifecycle and quoting tests |

Use conda's activator output rather than constructing `CONDA_PREFIX`, `CONDA_SHLVL`, or platform-specific `PATH` entries yourself:

```python
from conda.activate import CmdExeActivator, PosixActivator
from conda.common.compat import on_win

activator = (CmdExeActivator if on_win else PosixActivator)()
activation = activator.build_activate(str(prefix))

child_env = os.environ.copy()
child_env.update(
    {name: str(value) for name, value in activation.get("export_vars", {}).items()}
)
for name in activation.get("unset_vars", ()):
    child_env.pop(name, None)
```

This changes the child's environment without changing the parent process. Describe that limitation in help text. An `activate_scripts` entry does not mean those scripts have run.

Use `conda.common.path.BIN_DIRECTORY` when you need conda's platform-specific executable directory. Use conda's prefix and channel APIs to resolve environments and channels.

Reuse a supported shell implementation where practical. If the plugin implements interactive shell startup:

- Generate syntax for the selected shell. POSIX quoting is not PowerShell or `cmd.exe` quoting.
- Preserve normal startup files and user prompts.
- Prefer a shell's startup mechanism when sending commands through a pseudo-terminal could race with initialization. Fish's `-C` is one example.
- Wait for an explicit activation-ready signal before handing over interaction.
- Restore terminal signal handlers and remove temporary scripts on success, error, and interruption.
- Test interactive terminals and redirected stdin.
- Use a private marker such as `_CONDA_SPAWN` for internal coordination. Avoid inventing public-looking `CONDA_*` settings that conda may interpret.

Shell extensions that override private activator methods need version-specific tests. Do not copy those overrides into an ordinary command runner.

## Give one component ownership of stdout

Decide whether stdout carries human output, one JSON document, generated shell code, or a child program's output.

For JSON-producing commands, serialize a result object once. Put progress and diagnostics on stderr. Do not emit a heading, spinner, warning, or second JSON document on stdout.

For a composite command that invokes existing handlers:

1. Let the outer command own the final JSON object.
2. Keep nested handlers in their normal output mode.
3. Pass an injected Rich `Console` whose output goes to a buffer.
4. Capture direct Python stdout from those handlers.
5. Check nested results before emitting the outer success object.

Do not forward `--json` blindly into every nested `Namespace`. That can produce several JSON documents whose concatenation is invalid for the caller. `contextlib.redirect_stdout` captures Python writes, not child-process output. Configure subprocess stdout explicitly or call the underlying Python operation instead.

Commands that launch a child or open a shell should not advertise JSON unless they define a useful result envelope and account for the child's output. If repository conventions require accepting a global `--json` flag silently, follow those conventions without inventing a misleading payload.

Reuse conda's parser helpers once. Do not add another `--json`, `--yes`, or `--dry-run` after a helper has already registered it.

## Treat displayed data as text

Apply Rich markup only to formatting owned by the program. Escape package names, paths, URLs, exception text, and hints before interpolating them into markup:

```python
from rich.markup import escape

console.print(f"[bold red]Error:[/bold red] {escape(message)}")
```

For an unformatted message, `console.print(message, markup=False)` is simpler. Rich escaping protects markup interpretation. It is not shell quoting or a terminal-control-character filter.

Accept an optional `console` argument in reusable CLI handlers so callers can capture output without patching globals. Use words such as "Installed" and "Removed" to distinguish status, with color as additional information.

Under conda JSON or debug reporting, preserve the repository's exception handling path. Converting every exception into a friendly print can destroy structured errors and hide the requested traceback.

## Register settings through conda

Use `conda_settings`, `CondaSetting`, and conda's parameter classes for `.condarc` settings. Read effective values through `context.plugins`.

```python
from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from conda.plugins import hookimpl

if TYPE_CHECKING:
    from conda.plugins.types import CondaSetting


@hookimpl
def conda_settings() -> Iterable[CondaSetting]:
    from conda.common.configuration import PrimitiveParameter
    from conda.plugins.types import CondaSetting

    yield CondaSetting(
        name="example_enabled",
        description="Enable the example integration.",
        parameter=PrimitiveParameter(False, element_type=bool),
    )
```

Choose a type, default, and validator. A positive interval and a non-negative retention age need different validation rules.

Do not separately parse `.condarc` or guess conda's configuration precedence. If compatibility requires a direct environment-variable alias, document its precedence and parse it deliberately. `bool("false")` is true in Python and is not a configuration parser.

Keep transient process markers separate from public configuration. Put secrets in an appropriate credential backend or explicitly supplied environment variables, rather than ordinary status files.

## Make writes recoverable

For a state file, serialize and validate the complete replacement first. Create the temporary file in the destination directory, close it, then replace the destination:

```python
temporary = None
try:
    with tempfile.NamedTemporaryFile(
        dir=destination.parent, mode="wb", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
    os.replace(temporary, destination)
finally:
    if temporary is not None:
        temporary.unlink(missing_ok=True)
```

Use an existing repository writer when available. Define file permissions and symlink handling. Bound file size and collection counts before deserializing caches supplied by another process.

Atomic replacement prevents readers from observing half a file. It does not prevent concurrent read-modify-write operations from losing updates. Use the repository's locking strategy where concurrent writers are possible. If crash durability matters, also define file and directory synchronization requirements.

Do not generalize this file pattern into installing a conda environment anywhere and renaming it later. Installed packages can contain prefix-specific paths. Use conda's environment and transaction operations, and verify any relocation design separately.

Before cleanup, validate that the target belongs to the plugin's managed storage. Respect dry-run and confirmation settings. Remove partial state on failure without converting failure into success.

## Match failure handling to the operation

| Operation | Failure policy |
| --- | --- |
| Explicit install, export, configuration change, or credential operation | Report a useful error and fail |
| Direct child execution | Preserve the child's status |
| Optional completion refresh after another successful command | Keep the original command successful, with an appropriate diagnostic |
| Missing optional dependency for an explicitly requested feature | Explain the missing capability and fail that feature |
| Missing optional development header | Omit it only if that is the documented policy |
| Invalid or missing required authentication | Fail rather than silently weakening authentication |

A best-effort post-command hook may catch unexpected failures because its output is supplementary. Keep that catch local to the hook. Log permission and I/O problems clearly enough to diagnose. Do not swallow `KeyboardInterrupt` or `SystemExit` as routine refresh failures.

Load optional dependencies only when their feature is selected. A successful `find_spec` check establishes that a module can be found, not that its version or runtime integration works. Test missing and supported optional dependencies.

Keep plugin imports and registration lightweight. Do not solve, access the network, retrieve credentials, launch subprocesses, or write state merely because conda discovers the plugin. Measure startup in a fresh process instead of treating another project's timing target as proof.

## Scope request headers and credentials precisely

Use `conda_session_headers(host)` for values valid for every request to a selected host. Use `conda_request_headers(host, path)` when the path changes whether a header is allowed.

Match a normalized host exactly unless a wildcard is an intentional documented feature. For a path prefix, require a complete path component:

```python
allowed = (
    host == "packages.example.org"
    and (path == "/team" or path.startswith("/team/"))
)
```

This allows `/team` and `/team/linux-64/repodata.json`. It rejects `/team-other` and `packages.example.org.attacker.invalid`.

Keep path-specific rules out of session headers. Normalize header names case-insensitively when resolving duplicates, and document precedence between file rules and inline settings.

Validate the final rendered value before yielding `CondaRequestHeader`:

- Require a valid HTTP header name.
- Reject CR, LF, and NUL in values.
- Handle missing template variables explicitly.
- Reject forbidden transport and connection headers for a configurable header feature.
- Never log rendered header values, environment-variable contents, or tokens.

The header hooks receive host and path, not a complete transport security decision. A selector written with `https://` is insufficient if its implementation discards the scheme. For credentials, enforce allowed transport through the authentication integration and test redirects.

Register channel authentication through `conda_auth_handlers` and a `ChannelAuthBase` implementation. Resolve channel identity with `Channel`, scope credential records to their intended target and authentication type, and validate transport before returning cached credentials. Default to HTTPS. Define and test any loopback or explicit plaintext exception narrowly.

Preserve an explicit request authorization header unless the feature specifies an override. Clear credential and header-configuration caches when credentials change.

Expose credential status through an allowlist of safe fields. Do not serialize the full stored record and then attempt to redact passwords and tokens. Keep access tokens, refresh tokens, client secrets, and token templates out of status output.

## Verify observable behavior

Use parametrized tests for these cases:

- Plugin options before the executable, child options after it, a child-owned `--`, and arguments containing spaces or an empty string.
- Normal exit, nonzero exit, POSIX signal termination, missing executable, and permission failure.
- Activation variables added and unset, with the parent environment unchanged.
- JSON parsed from the complete stdout string while nested handlers emit progress.
- Rich-looking user input printed literally.
- A failed state write leaving the previous file readable.
- Optional refresh failure preserving the original command result.
- Exact host and path matches, lookalike hosts, adjacent path prefixes, and invalid header values.
- A cached credential still being rejected for an insecure transport.
- Credential status omitting every secret-bearing field.

Run shell-specific behavior on the shells and platforms the plugin claims to support.
