#!/usr/bin/env python3
"""Development-only exact mirror sync for the canonical C2 Skill tree."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
CANONICAL = SKILL_ROOT
MIRROR = REPO_ROOT / ".agents" / "skills" / SKILL_ROOT.name
IGNORE = shutil.ignore_patterns("__pycache__", "*.py[cod]", ".pytest_cache")


def sync_mirror(source: Path = CANONICAL, destination: Path = MIRROR) -> int:
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    if not source.is_dir() or source == destination or source in destination.parents:
        raise ValueError("source and mirror paths are invalid")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.sync-tmp")
    backup = destination.with_name(f".{destination.name}.sync-backup")
    for path in (temporary, backup):
        if path.exists():
            shutil.rmtree(path)
    shutil.copytree(source, temporary, ignore=IGNORE)
    if destination.exists():
        os.replace(destination, backup)
    try:
        os.replace(temporary, destination)
    except Exception:
        if backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise
    if backup.exists():
        shutil.rmtree(backup)
    return sum(path.is_file() for path in destination.rglob("*"))


if __name__ == "__main__":
    count = sync_mirror()
    print(f"synced {count} files: {CANONICAL} -> {MIRROR}")
