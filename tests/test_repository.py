from __future__ import annotations

import os
import zipfile
from pathlib import Path

import pytest
from check import check_repository
from package import build_archives


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    skill = tmp_path / "skills" / "example"
    references = skill / "references"
    references.mkdir(parents=True)
    (tmp_path / "LICENSE").write_text("Apache License, Version 2.0\n", encoding="utf-8")
    (skill / "LICENSE").write_bytes((tmp_path / "LICENSE").read_bytes())
    (skill / "THIRD_PARTY_NOTICES.md").write_text(
        "# Third-party notices\n", encoding="utf-8"
    )
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: A working example.\n"
        "license: Apache-2.0\n---\n\n# Example\n\n"
        "[Guide](references/guide.md#use-the-tool)\n",
        encoding="utf-8",
    )
    (references / "guide.md").write_text(
        "# Guide\n\n## Use the `tool`\n", encoding="utf-8"
    )
    (tmp_path / "README.md").write_text(
        "[Example](skills/example/SKILL.md#example)\n", encoding="utf-8"
    )
    return tmp_path


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("[Guide](missing.md)", "missing target"),
        ("[Guide](references/guide.md#absent)", "missing anchor"),
        ("[Root](../../README.md)", "outside the skill"),
        ("[Root](%2e%2e/%2e%2e/README.md)", "outside the skill"),
        ("[Guide][missing]", "undefined reference"),
        ("[Guide][g]\n\n[g]: missing.md", "missing target"),
        ("[Guide][]\n\n[Guide]: references/guide.md#absent", "missing anchor"),
    ],
    ids=[
        "file",
        "anchor",
        "escape",
        "encoded-escape",
        "reference",
        "definition",
        "collapsed",
    ],
)
def test_rejects_broken_links(repository: Path, content: str, expected: str) -> None:
    path = repository / "skills/example/SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8") + "\n" + content + "\n", encoding="utf-8"
    )
    assert any(expected in error for error in check_repository(repository))


@pytest.mark.parametrize("fence", ["```", "~~~~"], ids=["backticks", "tildes"])
def test_ignores_examples_and_checks_real_references(
    repository: Path, fence: str
) -> None:
    path = repository / "skills/example/references/guide.md"
    path.write_text(
        "# Guide\n\n## Use the `tool`\n\n## Use the `tool`\n\n"
        "[Again](#use-the-tool-1)\n[Guide][g]\n[Guide][]\n"
        '[g]: <guide.md#use-the-tool> "Guide title"\n'
        "[Guide]: guide.md#use-the-tool\n"
        "`[literal](absent.md)`\n[External](https://example.org/unknown#absent)\n"
        f"{fence}markdown\n[Example](absent.md)\n{fence}\n",
        encoding="utf-8",
    )
    assert check_repository(repository) == []


@pytest.mark.parametrize(
    "change", ["missing", "different"], ids=["missing", "mismatch"]
)
def test_requires_distributed_license(repository: Path, change: str) -> None:
    path = repository / "skills/example/LICENSE"
    if change == "missing":
        path.unlink()
    else:
        path.write_text("Different license\n", encoding="utf-8")
    assert any("LICENSE" in error for error in check_repository(repository))


@pytest.mark.parametrize("field", ["name", "description", "license"])
def test_requires_valid_frontmatter(repository: Path, field: str) -> None:
    path = repository / "skills/example/SKILL.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line for line in lines if not line.startswith(f"{field}:")),
        encoding="utf-8",
    )
    assert any(field in error for error in check_repository(repository))


@pytest.mark.parametrize(
    "missing", ["LICENSE", "skills/example/THIRD_PARTY_NOTICES.md"]
)
def test_requires_repository_and_notice_files(repository: Path, missing: str) -> None:
    (repository / missing).unlink()
    assert check_repository(repository)


def test_rejects_root_archives_before_building(repository: Path) -> None:
    (repository / "example.zip").write_bytes(b"old archive")
    with pytest.raises(ValueError, match="root ZIP"):
        build_archives(repository)
    assert not (repository / "dist").exists()


def test_archives_are_complete_reproducible_and_scoped(repository: Path) -> None:
    skill = repository / "skills/example"
    cache = skill / "__pycache__"
    cache.mkdir()
    (cache / "discard.pyc").write_bytes(b"cached")
    (repository / "unrelated.txt").write_text("Do not distribute\n", encoding="utf-8")
    [archive] = build_archives(repository)
    first = archive.read_bytes()
    for path in skill.rglob("*"):
        os.utime(path, (1_700_000_000, 1_700_000_000))
    assert build_archives(repository) == [archive]
    assert archive.read_bytes() == first
    assert archive.parent == repository / "dist"
    with zipfile.ZipFile(archive) as bundle:
        assert set(bundle.namelist()) == {
            "example/SKILL.md",
            "example/LICENSE",
            "example/THIRD_PARTY_NOTICES.md",
            "example/references/guide.md",
        }
        assert bundle.read("example/LICENSE") == (repository / "LICENSE").read_bytes()


def test_rejects_symlinked_distribution_files(repository: Path) -> None:
    target = repository / "skills/example/references/link.md"
    try:
        target.symlink_to(repository / "README.md")
    except OSError:
        pytest.skip("Creating symlinks is unavailable for this account")
    assert any("symlink" in error for error in check_repository(repository))
    with pytest.raises(ValueError, match="symlink"):
        build_archives(repository)
