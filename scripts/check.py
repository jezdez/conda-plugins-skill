"""Check this repository's skill metadata and portable Markdown references.

Supported links are inline links, full/collapsed references, defined shortcuts,
and same-line reference definitions. Destinations may use angle brackets or
balanced parentheses. Anchors use ATX headings and GitHub-style duplicate suffixes.
Fenced blocks and inline code are excluded. This is a repository convention check,
not a complete Markdown/MyST renderer or an external URL checker.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

IGNORED = {
    ".git",
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}


def skill_files(skill: Path) -> list[Path]:
    """Return distribution files, excluding generated caches."""
    return sorted(
        path
        for path in skill.rglob("*")
        if not IGNORED.intersection(path.relative_to(skill).parts)
        and path.suffix not in {".pyc", ".pyo"}
        and (path.is_file() or path.is_symlink())
    )


def visible_markdown(text: str) -> str:
    """Blank frontmatter and fenced examples while preserving line numbers."""
    result = []
    fence = ""
    frontmatter = text.startswith("---\n")
    for number, line in enumerate(text.splitlines()):
        if frontmatter:
            if number and line == "---":
                frontmatter = False
            result.append("")
            continue
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                if not marker[2].strip():
                    fence = ""
            result.append("")
        elif marker:
            fence = marker[1]
            result.append("")
        else:
            result.append(line)
    return "\n".join(result)


def heading_anchors(text: str) -> set[str]:
    """Derive anchors for plain ATX headings used by this repository."""
    anchors: set[str] = set()
    for line in visible_markdown(text).splitlines():
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$", line)
        if heading:
            base = re.sub(r"[^\w\s-]", "", heading[1].lower()).replace(" ", "-")
            anchor = base
            suffix = 0
            while anchor in anchors:
                suffix += 1
                anchor = f"{base}-{suffix}"
            anchors.add(anchor)
    return anchors


def destination(text: str) -> str:
    """Read a same-line link destination before its optional title."""
    text = text.lstrip()
    if text.startswith("<"):
        return text[1:].split(">", 1)[0]
    result = []
    depth = 0
    escaped = False
    for char in text:
        if escaped:
            result.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char.isspace() or (char == ")" and depth == 0):
            break
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        result.append(char)
    return "".join(result)


def markdown_links(text: str) -> tuple[list[tuple[int, str]], list[str]]:
    """Extract supported destinations and report undefined explicit references."""
    lines = visible_markdown(text).splitlines()
    definitions: dict[str, str] = {}
    links: list[tuple[int, str]] = []
    errors = []
    for index, line in enumerate(lines):
        definition = re.match(r"^ {0,3}\[([^]\n]+)\]:\s*(.+)$", line)
        if definition:
            target = destination(definition[2])
            definitions[" ".join(definition[1].casefold().split())] = target
            links.append((index + 1, target))
            lines[index] = ""
    for index, line in enumerate(lines):
        line = re.sub(r"(`+).*?\1", "", line)
        for match in re.finditer(r"(?<!\\)\[([^]\n]*)\](\(|\[)", line):
            rest = line[match.end() :]
            if match[2] == "(":
                links.append((index + 1, destination(rest)))
            else:
                label, closing, _ = rest.partition("]")
                if not closing:
                    continue
                label = " ".join((label or match[1]).casefold().split())
                if label not in definitions:
                    errors.append(f"line {index + 1}: undefined reference [{label}]")
        for match in re.finditer(r"(?<!\\)\[([^]\n]+)\](?![\[(])", line):
            label = " ".join(match[1].casefold().split())
            if label in definitions:
                links.append((index + 1, definitions[label]))
    return links, errors


def check_links(path: Path, scope: Path) -> list[str]:
    """Check local destinations without fetching external URLs."""
    links, errors = markdown_links(path.read_text(encoding="utf-8"))
    for number, target in links:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        resolved = (
            (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        )
        label = f"line {number}: {target!r}"
        if not resolved.is_relative_to(scope.resolve()):
            errors.append(f"{label} is outside the skill or repository")
        elif not resolved.exists():
            errors.append(f"{label} has a missing target")
        elif parsed.fragment and resolved.suffix.lower() == ".md":
            anchors = heading_anchors(resolved.read_text(encoding="utf-8"))
            if unquote(parsed.fragment) not in anchors:
                errors.append(f"{label} has a missing anchor")
    return errors


def check_repository(root: Path) -> list[str]:
    """Return actionable errors without writing files or using the network."""
    root = root.resolve()
    errors = []
    license_path = root / "LICENSE"
    license_bytes = license_path.read_bytes() if license_path.is_file() else None
    if license_bytes is None:
        errors.append("LICENSE: missing repository license")
    if any(path.suffix.lower() == ".zip" for path in root.iterdir()):
        errors.append("root ZIP archives must be moved into dist/")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("skills/: no SKILL.md files found")
    for entrypoint in skills:
        skill = entrypoint.parent
        label = str(entrypoint.relative_to(root))
        if skill.is_symlink() or entrypoint.is_symlink():
            errors.append(f"{label}: symlinks are not portable distribution files")
            continue
        text = entrypoint.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
        try:
            metadata = yaml.safe_load(frontmatter[1]) if frontmatter else None
        except yaml.YAMLError:
            metadata = None
        if not isinstance(metadata, dict):
            errors.append(f"{label}: missing or invalid YAML frontmatter")
        else:
            for field in ("name", "description", "license"):
                value = metadata.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{label}: {field} must be a nonempty string")
            if metadata.get("name") != skill.name or not re.fullmatch(
                r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name
            ):
                errors.append(
                    f"{label}: name must match its lowercase kebab-case directory"
                )
            if metadata.get("license") != "Apache-2.0":
                errors.append(f"{label}: license must be Apache-2.0")
        bundled_license = skill / "LICENSE"
        if (
            not bundled_license.is_file()
            or bundled_license.read_bytes() != license_bytes
        ):
            errors.append(f"{skill.name}/LICENSE: must match the repository LICENSE")
        if not (skill / "THIRD_PARTY_NOTICES.md").is_file():
            errors.append(
                f"{skill.name}/THIRD_PARTY_NOTICES.md: missing attribution file"
            )
        for path in skill_files(skill):
            relative = path.relative_to(root)
            if path.is_symlink():
                errors.append(
                    f"{relative}: symlinks are not portable distribution files"
                )
            elif path.suffix.lower() == ".md":
                errors.extend(
                    f"{relative}: {error}" for error in check_links(path, skill)
                )
    for path in sorted(root.glob("*.md")):
        errors.extend(f"{path.name}: {error}" for error in check_links(path, root))
    return errors


if __name__ == "__main__":
    problems = check_repository(Path(__file__).resolve().parents[1])
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print("Repository checks passed.")
