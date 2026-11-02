"""Install and verify the skill in a disposable conda build or test prefix."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from check import check_links, check_repository, skill_files


def build_conda(root: Path) -> Path:
    """Only retain a built package after verifying its extracted skill payload."""
    dist = root / "dist"
    if dist.is_symlink() or not dist.resolve().is_relative_to(root.resolve()):
        raise ValueError("dist/ must be a real directory inside the repository")
    output_dir = dist / "conda/noarch"
    if not output_dir.resolve().is_relative_to(dist.resolve()):
        raise ValueError("Conda output must remain inside dist/")
    dist.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="conda-build-", dir=dist) as temporary:
        work = Path(temporary)
        subprocess.run(
            [
                "rattler-build",
                "build",
                "--recipe",
                str(root / "recipe/recipe.yaml"),
                "--output-dir",
                str(work / "output"),
                "--no-config",
            ],
            check=True,
        )
        [archive] = (work / "output/noarch").glob("*.conda")
        extracted = work / "extracted"
        subprocess.run(
            [
                "rattler-build",
                "package",
                "extract",
                str(archive),
                "--dest",
                str(extracted),
            ],
            check=True,
        )
        package_skill(root, extracted, verify=True)
        if {path.name for path in extracted.iterdir()} != {"share", "info"}:
            raise ValueError("Conda package contains unexpected top-level content")
        output = output_dir / archive.name
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.is_symlink():
            raise ValueError("Conda archive destination must not be a symlink")
        shutil.copyfile(archive, output)
        return output


def package_skill(root: Path, prefix: Path, *, verify: bool = False) -> None:
    errors = check_repository(root)
    if errors:
        raise ValueError("\n".join(errors))
    source = root / "skills/conda-plugin-skill"
    destination = prefix / "share/agent-skills/conda-plugin-skill"
    if not destination.resolve().is_relative_to(prefix.resolve()):
        raise ValueError("Skill destination must remain inside the prefix")
    files = {path.relative_to(source): path for path in skill_files(source)}
    if not verify:
        destination.mkdir(parents=True, exist_ok=False)
        for relative, path in files.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        return
    installed = {
        path.relative_to(destination): path
        for path in destination.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if installed.keys() != files.keys():
        raise ValueError("Installed skill inventory differs from source")
    for relative, path in installed.items():
        if path.is_symlink() or path.read_bytes() != files[relative].read_bytes():
            raise ValueError(f"Installed skill file differs: {relative}")
        if path.suffix == ".md" and (errors := check_links(path, destination)):
            raise ValueError("\n".join(errors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("install", "verify", "build"))
    args = parser.parse_args()
    if args.mode == "build":
        print(build_conda(Path(__file__).resolve().parents[1]))
    else:
        prefix = Path(
            os.environ["PREFIX" if args.mode == "install" else "CONDA_PREFIX"]
        )
        package_skill(Path.cwd(), prefix, verify=args.mode == "verify")
        print(f"Skill {args.mode} passed")
