"""Build reproducible skill ZIP files in the repository's dist directory."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from check import check_repository, skill_files


def build_archives(root: Path) -> list[Path]:
    """Validate, then package each complete skill with stable order and metadata."""
    root = root.resolve()
    errors = check_repository(root)
    if errors:
        raise ValueError("\n".join(errors))
    output = root / "dist"
    if output.is_symlink():
        raise ValueError("dist/ must be a real directory inside the repository")
    output.mkdir(exist_ok=True)
    archives = []
    for entrypoint in sorted((root / "skills").glob("*/SKILL.md")):
        skill = entrypoint.parent
        archive = output / f"{skill.name}.zip"
        if archive.is_symlink():
            raise ValueError("archive destinations must not be symlinks")
        with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
            for path in skill_files(skill):
                info = ZipInfo(str(path.relative_to(skill.parent)).replace("\\", "/"))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = ZIP_DEFLATED
                bundle.writestr(info, path.read_bytes(), compresslevel=9)
        archives.append(archive)
    return archives


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[1]
    try:
        for archive in build_archives(repository):
            print(archive.relative_to(repository))
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
