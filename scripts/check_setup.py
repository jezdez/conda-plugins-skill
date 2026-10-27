"""Exercise the README setup on GitHub-hosted Linux, macOS, and Windows runners.

This intentionally refuses local execution. Only summary.json is retained.
Client discovery never submits a model prompt or enables plugin hooks.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

SOURCES = {
    "jezdez/conda-plugin-skills": "skills",
    "obra/superpowers": "skills",
    "blader/humanizer": "",
    "DietrichGebert/ponytail": "skills",
}
CLIENT_PACKAGES = (
    "@openai/codex@0.165.0",
    "@kilocode/cli@7.8.18",
    "@anthropic-ai/claude-agent-sdk@0.3.312",
)
IGNORED_DIRS = {".git", "__pycache__", "__pypackages__"}


class SetupFailure(Exception):
    """A controlled diagnostic that is safe to include in the summary."""


class NoRedirect(HTTPRedirectHandler):
    """Never forward the GitHub API authorization header to another URL."""

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


def github(path: str, token: str) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if path.startswith("jezdez/conda-plugin-skills/"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(
        f"https://api.github.com/repos/{path}",
        headers=headers,
    )
    try:
        with build_opener(NoRedirect()).open(request, timeout=45) as response:
            return json.load(response)
    except HTTPError as error:
        raise SetupFailure(f"GitHub API returned HTTP {error.code}") from None


def source_inventory(
    token: str,
) -> tuple[dict[str, str], dict[str, dict[str, tuple[str, str]]]]:
    heads = {}
    skills = {}
    for repository, container in SOURCES.items():
        head = github(f"{repository}/commits/HEAD", token)["sha"]
        heads[repository] = head
        tree = github(f"{repository}/git/trees/{head}?recursive=1", token)
        if tree.get("truncated"):
            raise SetupFailure(f"Source tree is truncated: {repository}")
        blobs = [entry for entry in tree["tree"] if entry["type"] == "blob"]
        if container:
            roots = [
                entry["path"].removesuffix("SKILL.md")
                for entry in blobs
                if entry["path"].startswith(f"{container}/")
                and entry["path"].count("/") == 2
                and entry["path"].endswith("/SKILL.md")
            ]
        else:
            roots = [""]
        if not roots:
            raise SetupFailure(f"No skill roots found: {repository}")
        for root in roots:
            name = root.rstrip("/").split("/")[-1] if root else "humanizer"
            if name in skills:
                raise SetupFailure(f"Duplicate source skill name: {name}")
            files = {}
            for entry in blobs:
                if not entry["path"].startswith(root):
                    continue
                relative = entry["path"][len(root) :]
                parts = relative.split("/")
                if IGNORED_DIRS.intersection(parts) or parts[-1] == "metadata.json":
                    continue
                if entry["mode"] not in {"100644", "100755"}:
                    raise SetupFailure(f"Unsupported source file mode: {name}")
                files[relative] = (entry["sha"], entry["mode"])
            if "SKILL.md" not in files:
                raise SetupFailure(f"Source skill lacks SKILL.md: {name}")
            skills[name] = files
    return heads, skills


def git_blob_hash(content: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(content)).encode("ascii") + b"\0" + content,
        usedforsecurity=False,
    ).hexdigest()


def installer_results(stdout: bytes, expected: set[str]) -> list[dict[str, Any]]:
    text = stdout.decode("utf-8")
    groups = []
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        group, end = decoder.raw_decode(text)
        if not isinstance(group, list):
            raise SetupFailure("Installer output is not an array of skill results")
        groups.append(group)
        text = text[end:]
    if len(groups) != len(SOURCES):
        raise SetupFailure("Installer did not report all four sources")
    results = [item for group in groups for item in group]
    if len(results) != len(expected) or {item["name"] for item in results} != expected:
        raise SetupFailure("Installer skill inventory differs from source inventory")
    for item in results:
        if (
            item.get("status") != "installed"
            or item.get("scope") != "global"
            or item.get("mode") != "copy"
            or set(item.get("agents", [])) != {"Codex", "Claude Code", "Kilo Code"}
        ):
            raise SetupFailure("Installer did not succeed for every selected client")
    return [
        {key: item[key] for key in ("name", "status", "hash", "scope", "mode")}
        for item in results
    ]


def check_bash_script(path: Path) -> None:
    """Check line endings and Bash syntax without executing the helper."""
    if b"\r\n" in path.read_bytes():
        raise SetupFailure(f"Executable Bash helper contains CRLF: {path.name}")
    bash = shutil.which("bash")
    if not bash:
        raise SetupFailure("Bash is required to check installed helper syntax")
    result = subprocess.run(
        [bash, "-n", path.as_posix()], capture_output=True, timeout=20
    )
    if result.returncode:
        raise SetupFailure(f"Executable Bash helper has invalid syntax: {path.name}")


def verify_files(
    home: Path, skills: dict[str, dict[str, tuple[str, str]]]
) -> list[dict[str, Any]]:
    results = []
    for relative_root in (".agents/skills", ".claude/skills"):
        root = home / relative_root
        expected = {
            f"{name}/{relative}": info
            for name, files in skills.items()
            for relative, info in files.items()
        }
        actual = {
            path.relative_to(root).as_posix(): path
            for path in root.rglob("*")
            if path.is_file() or path.is_symlink()
        }
        if actual.keys() != expected.keys():
            raise SetupFailure(f"Installed file inventory differs: {relative_root}")
        normalized = 0
        bash_scripts_checked = 0
        for relative, path in actual.items():
            if path.is_symlink():
                raise SetupFailure(f"Copy installation contains a symlink: {relative}")
            content = path.read_bytes()
            source_hash, mode = expected[relative]
            if mode == "100755" and re.match(
                rb"^#![^\r\n]*(?:/|\s)bash(?:\s|$)", content
            ):
                check_bash_script(path)
                bash_scripts_checked += 1
            if git_blob_hash(content) != source_hash:
                if (
                    os.name == "nt"
                    and b"\r\n" in content
                    and git_blob_hash(content.replace(b"\r\n", b"\n")) == source_hash
                ):
                    normalized += 1
                else:
                    raise SetupFailure(f"Installed bytes differ: {relative}")
            if os.name != "nt" and bool(path.stat().st_mode & 0o111) != (
                mode == "100755"
            ):
                raise SetupFailure(f"Installed executable mode differs: {relative}")
        for relative in (
            "executing-plans/scripts/../../subagent-driven-development/scripts/task-brief",
            "subagent-driven-development/references/../../requesting-code-review/code-reviewer.md",
        ):
            target = (root / relative).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                raise SetupFailure("Superpowers sibling resource does not resolve")
            if not os.access(target, os.R_OK):
                raise SetupFailure("Superpowers sibling resource is not readable")
        helper = root / "subagent-driven-development/scripts/task-brief"
        if os.name != "nt" and not os.access(helper, os.X_OK):
            raise SetupFailure("Superpowers sibling helper is not executable")
        results.append(
            {
                "directory": relative_root,
                "skills": len(skills),
                "files": len(actual),
                "exactBytes": len(actual) - normalized,
                "crlfNormalizedFiles": normalized,
                "executableModesChecked": os.name != "nt",
                "countBashScriptsChecked": bash_scripts_checked,
                "siblingResourcesResolved": True,
            }
        )
    return results


def client_environment() -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if "TOKEN" not in key.upper()
        and "SECRET" not in key.upper()
        and not key.upper().endswith("API_KEY")
        and not key.startswith("GIT_CONFIG_")
        and key not in {"GIT_ASKPASS", "SSH_ASKPASS"}
    }
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    env["DISABLE_TELEMETRY"] = "1"
    env["KILO_DISABLE_AUTOUPDATE"] = "1"
    env["KILO_DISABLE_MODELS_FETCH"] = "1"
    if os.name == "nt":
        bash = shutil.which("bash")
        if not bash:
            raise SetupFailure("Git Bash is unavailable for the Windows probes")
        env["CLAUDE_CODE_GIT_BASH_PATH"] = str(Path(bash).resolve())
    return env


def command(
    args: list[str], cwd: Path, env: dict[str, str], timeout: int = 60
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, timeout=timeout
    )
    if result.returncode:
        label = Path(args[1]).name
        raise SetupFailure(f"{label} exited with status {result.returncode}")
    return result


def codex_discovery(
    args: list[str], cwd: Path, env: dict[str, str], home: Path, expected: set[str]
) -> dict[str, Any]:
    proc = subprocess.Popen(
        [*args, "app-server"],
        cwd=cwd,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
    )
    assert proc.stdin is not None and proc.stdout is not None
    output = proc.stdout
    messages: queue.Queue[dict[str, Any]] = queue.Queue()

    def receive() -> None:
        try:
            for line in output:
                messages.put(json.loads(line))
        finally:
            messages.put({"eof": True})

    threading.Thread(target=receive, daemon=True).start()

    def request(message: dict[str, Any]) -> dict[str, Any]:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps(message) + "\n")
        proc.stdin.flush()
        if "id" not in message:
            return {}
        while True:
            result = messages.get(timeout=45)
            if result.get("eof"):
                raise SetupFailure("Codex closed before returning its skill catalog")
            if result.get("id") == message["id"]:
                if "error" in result:
                    raise SetupFailure("Codex returned a discovery protocol error")
                return result

    try:
        request(
            {
                "id": 1,
                "method": "initialize",
                "params": {
                    "clientInfo": {"name": "readme-setup-check", "version": "1.0"},
                    "capabilities": {},
                },
            }
        )
        request({"method": "initialized"})
        result = request(
            {
                "id": 2,
                "method": "skills/list",
                "params": {"cwds": [str(cwd)], "forceReload": True},
            }
        )
        entries = result["result"]["data"]
        if any(entry["errors"] for entry in entries):
            raise SetupFailure("Codex reported skill loading errors")
        installed_root = (home / ".agents/skills").resolve()
        names = {
            Path(skill["path"]).parent.name
            for entry in entries
            for skill in entry["skills"]
            if skill.get("enabled", True)
            and Path(skill["path"]).resolve().parent.parent == installed_root
        }
        if names != expected:
            raise SetupFailure("Codex did not discover every installed skill")
        return {"client": "Codex", "version": "0.165.0", "found": len(names)}
    finally:
        proc.stdin.close()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait(timeout=5)


def discover_clients(
    workspace: Path, home: Path, expected: set[str]
) -> list[dict[str, Any]]:
    env = client_environment()
    node = shutil.which("node")
    npm = shutil.which("npm")
    if not node or not npm:
        raise SetupFailure("Node.js and npm must be installed before this check")
    node_path = Path(node).resolve()
    npm_candidates = (
        node_path.parent / "node_modules/npm/bin/npm-cli.js",
        node_path.parent.parent / "lib/node_modules/npm/bin/npm-cli.js",
        Path(npm).resolve(),
    )
    npm_cli = next(
        (path for path in npm_candidates if path.is_file() and path.suffix != ".cmd"),
        None,
    )
    if npm_cli is None:
        raise SetupFailure("Could not locate npm's JavaScript entry point")
    clients = workspace / "clients"
    clients.mkdir()
    command(
        [
            node,
            str(npm_cli),
            "install",
            "--prefix",
            str(clients),
            "--no-save",
            "--no-package-lock",
            "--no-audit",
            "--no-fund",
            *CLIENT_PACKAGES,
        ],
        workspace,
        env,
        timeout=240,
    )
    modules = clients / "node_modules"
    results = [
        codex_discovery(
            [node, str(modules / "@openai/codex/bin/codex.js")],
            workspace,
            env,
            home,
            expected,
        )
    ]
    kilo = command(
        [node, str(modules / "@kilocode/cli/bin/kilo"), "debug", "skill"],
        workspace,
        env,
    )
    catalog = json.loads(kilo.stdout)
    names = {
        skill["name"]
        for skill in catalog
        if Path(skill["location"]).resolve().parent.parent
        in {(home / ".agents/skills").resolve(), (home / ".claude/skills").resolve()}
    }
    if names != expected:
        raise SetupFailure("Kilo did not discover every installed skill")
    results.append({"client": "Kilo", "version": "7.8.18", "found": len(names)})
    sdk = (modules / "@anthropic-ai/claude-agent-sdk/sdk.mjs").as_uri()
    probe = clients / "discover.mjs"
    probe.write_text(
        f"import {{query}} from {json.dumps(sdk)}\n"
        "let release\n"
        "const gate = new Promise(resolve => { release = resolve })\n"
        "async function* input() { await gate }\n"
        "const q = query({prompt: input(), options: {"
        f"cwd: {json.dumps(str(workspace))}, "
        "settingSources: ['user', 'project'], persistSession: false}})\n"
        "try { console.log(JSON.stringify(await q.supportedCommands())) }\n"
        "finally { release(); q.close() }\n",
        encoding="utf-8",
    )
    claude = command([node, str(probe)], workspace, env)
    names = {item["name"] for item in json.loads(claude.stdout)}
    if not expected.issubset(names):
        raise SetupFailure("Claude Code did not discover every installed skill")
    results.append(
        {"client": "Claude Code", "sdkVersion": "0.3.312", "found": len(expected)}
    )
    return results


def main() -> int:
    if (
        os.environ.get("GITHUB_ACTIONS") != "true"
        or os.environ.get("RUNNER_ENVIRONMENT") != "github-hosted"
    ):
        print("This check only runs on disposable GitHub-hosted runners.")
        return 1
    output_arg = (
        sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SKILLS_TEST_OUTPUT")
    )
    if not output_arg:
        print("Set SKILLS_TEST_OUTPUT or pass an evidence directory.")
        return 1
    output = Path(output_arg).resolve()
    output.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "status": "failed",
        "platform": sys.platform,
        "osRelease": platform.release(),
        "osVersion": platform.mac_ver()[0] or platform.win32_ver()[1],
        "architecture": platform.machine(),
    }
    stage = "preflight"
    try:
        home = Path.home()
        for directory in (
            ".agents/skills",
            ".claude/skills",
            ".codex/skills",
            ".kilo/skills",
        ):
            if (home / directory).exists() or (home / directory).is_symlink():
                raise SetupFailure("A skill destination already exists on this runner")
        token = os.environ.get("SKILLS_TEST_GITHUB_TOKEN")
        if not token:
            raise SetupFailure("SKILLS_TEST_GITHUB_TOKEN is required")
        bash = shutil.which("bash")
        if not bash:
            raise SetupFailure("Bash is required for the README setup command")
        node = shutil.which("node")
        if not node:
            raise SetupFailure("Node.js is required for the README setup command")
        node_info = json.loads(
            command(
                [
                    node,
                    "-e",
                    "console.log(JSON.stringify({home: require('node:os').homedir(), "
                    "version: process.version}))",
                ],
                Path.cwd(),
                os.environ.copy(),
            ).stdout
        )
        if Path(node_info["home"]).resolve() != home.resolve():
            raise SetupFailure("Node.js and Python resolve different user homes")
        summary["nodeVersion"] = node_info["version"]
        summary["nodeAndPythonHomesMatch"] = True
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_bytes()
        block = re.search(rb"(?ms)^```sh\r?\n(.*?)^```\r?$", readme)
        if not block:
            raise SetupFailure("README does not contain its setup shell block")
        setup = block[1]
        summary["setupSha256"] = hashlib.sha256(setup).hexdigest()
        summary["initialSkillDirectoriesAbsent"] = True
        stage = "source inventories"
        heads, skills = source_inventory(token)
        summary["sourceHeads"] = heads
        summary["expectedSkills"] = sorted(skills)
        summary["expectedFilesPerDestination"] = sum(map(len, skills.values()))
        with tempfile.TemporaryDirectory(prefix="readme-setup-") as temporary:
            workspace = Path(temporary).resolve()
            env = os.environ.copy()
            env.update(
                {
                    "GIT_TERMINAL_PROMPT": "0",
                    "GIT_CONFIG_COUNT": "3",
                    "GIT_CONFIG_KEY_0": "credential.helper",
                    "GIT_CONFIG_VALUE_0": "",
                    "GIT_CONFIG_KEY_1": (
                        "credential.https://github.com/jezdez/"
                        "conda-plugin-skills.git.helper"
                    ),
                    "GIT_CONFIG_VALUE_1": (
                        '!f() { if [ "$1" = get ]; then '
                        "printf '%s\\n' 'username=x-access-token'; "
                        'printf "password=%s\\n" "$SKILLS_TEST_GITHUB_TOKEN"; '
                        "fi; }; f"
                    ),
                    "GIT_CONFIG_KEY_2": "credential.useHttpPath",
                    "GIT_CONFIG_VALUE_2": "true",
                }
            )
            stage = "README setup"
            installed = subprocess.run(
                [bash, "--noprofile", "--norc"],
                input=setup,
                cwd=workspace,
                env=env,
                capture_output=True,
                timeout=300,
            )
            summary["setupExitCode"] = installed.returncode
            summary["installerStdoutSha256"] = hashlib.sha256(
                installed.stdout
            ).hexdigest()
            summary["installerStderrSha256"] = hashlib.sha256(
                installed.stderr
            ).hexdigest()
            if installed.returncode:
                raise SetupFailure("README setup command failed")
            summary["installerResults"] = installer_results(
                installed.stdout, set(skills)
            )
            stage = "installed file verification"
            summary["destinations"] = verify_files(home, skills)
            stage = "source revision recheck"
            after = {
                repository: github(f"{repository}/commits/HEAD", token)["sha"]
                for repository in SOURCES
            }
            if after != heads:
                raise SetupFailure("An upstream source changed during the setup check")
            summary["sourceHeadsUnchangedDuringTest"] = True
            stage = "native client discovery"
            summary["clients"] = discover_clients(workspace, home, set(skills))
            summary["modelPromptSubmitted"] = False
            summary["pluginHooksTested"] = False
        summary["status"] = "passed"
    except SetupFailure as error:
        summary.update(stage=stage, error=str(error))
    except Exception as error:
        summary.update(stage=stage, error=f"Check failed with {type(error).__name__}")
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary))
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
