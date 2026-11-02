from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest
import yaml
from conda_package import build_conda, package_skill


@pytest.fixture
def package_source(tmp_path: Path) -> Path:
    repository = Path(__file__).resolve().parents[1]
    root = tmp_path / "source"
    shutil.copytree(
        repository / "skills/conda-plugin-skill",
        root / "skills/conda-plugin-skill",
    )
    shutil.copyfile(repository / "LICENSE", root / "LICENSE")
    return root


def test_installed_skill_is_complete_and_standalone(
    package_source: Path, tmp_path: Path
) -> None:
    prefix = tmp_path / "prefix"
    package_skill(package_source, prefix)
    package_skill(package_source, prefix, verify=True)
    assert {path.name for path in prefix.iterdir()} == {"share"}
    with pytest.raises(FileExistsError):
        package_skill(package_source, prefix)


@pytest.mark.parametrize("change", ["missing", "changed", "extra"])
def test_rejects_changed_installed_payload(
    package_source: Path, tmp_path: Path, change: str
) -> None:
    prefix = tmp_path / "prefix"
    package_skill(package_source, prefix)
    installed = prefix / "share/agent-skills/conda-plugin-skill"
    if change == "missing":
        (installed / "LICENSE").unlink()
    elif change == "changed":
        (installed / "SKILL.md").write_text("changed\n", encoding="utf-8")
    else:
        (installed / "unexpected.txt").write_text("extra\n", encoding="utf-8")
    with pytest.raises(ValueError, match="differs"):
        package_skill(package_source, prefix, verify=True)


def test_conda_recipe_release_metadata() -> None:
    root = Path(__file__).resolve().parents[1]
    recipe = yaml.safe_load((root / "recipe/recipe.yaml").read_text(encoding="utf-8"))
    assert re.fullmatch(
        r"[0-9]{2}\.(0[1-9]|1[0-2])\.(0|[1-9][0-9]*)", recipe["package"]["version"]
    )
    assert recipe["package"]["name"] == "agent-skill-conda-plugin-skill"
    assert recipe["build"]["noarch"] == "generic"
    assert type(recipe["build"]["number"]) is int
    assert recipe["build"]["number"] >= 0
    assert not recipe["requirements"].get("run")


@pytest.mark.parametrize("mode", ["install", "verify", "build"])
def test_rejects_redirected_parent(
    package_source: Path, tmp_path: Path, mode: str
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    if mode == "build":
        parent = package_source / "dist"
        link = parent / "conda"
    else:
        parent = tmp_path / "prefix"
        link = parent / "share"
    parent.mkdir()
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("Directory symlinks unavailable for this account")
    with pytest.raises(ValueError, match="must remain inside"):
        if mode == "build":
            build_conda(package_source)
        else:
            package_skill(package_source, parent, verify=mode == "verify")
    assert list(outside.iterdir()) == []
