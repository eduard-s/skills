#!/usr/bin/env python3
"""Build the portable upload ZIP from the skill's runtime files only."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "science-research"
DESTINATION = ROOT / "dist" / "science-research.zip"


def build_package(destination=DESTINATION):
    files = sorted(path for path in SKILL.rglob("*") if path.is_file()
                   and "__pycache__" not in path.parts
                   and path.suffix not in {".pyc", ".pyo"}
                   and path.name != ".DS_Store")
    if not (SKILL / "SKILL.md").is_file():
        raise ValueError("Missing skill entry point")
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for path in files:
            if path.is_symlink():
                raise ValueError("Refusing to package a symlink: " + str(path))
            entry = ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    return destination


if __name__ == "__main__":
    print(build_package())
