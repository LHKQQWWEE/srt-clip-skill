#!/usr/bin/env python3
"""Validate or refresh the persistent, versioned C2 execution summary."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def current_files(root: Path, manifest: dict[str, object]) -> list[str]:
    paths = ["VERSION", "SKILL.md"]
    paths.extend(manifest.get("source_files", []))
    runtime_file = manifest.get("runtime_file")
    if isinstance(runtime_file, str):
        paths.append(runtime_file)
    return list(dict.fromkeys(str(p) for p in paths))


def validate_manifest(root: Path, manifest: dict[str, object]) -> tuple[str | None, dict[str, str]]:
    skill_version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else None
    if skill_version != manifest.get("skill_version"):
        return "manifest_stale", {}
    hashes: dict[str, str] = {}
    source_hashes = manifest.get("source_hashes", {})
    if not isinstance(source_hashes, dict):
        return "manifest_stale", {}
    for relative in current_files(root, manifest):
        path = root / relative
        if not path.is_file():
            return "manifest_stale", {}
        digest = sha256(path.read_bytes())
        hashes[relative] = digest
        if relative in source_hashes and source_hashes[relative] != digest:
            return "manifest_stale", hashes
    runtime_file = manifest.get("runtime_file")
    if not isinstance(runtime_file, str) or sha256((root / runtime_file).read_bytes()) != manifest.get("runtime_sha256"):
        return "manifest_stale", hashes
    return None, hashes


def cache_status(path: Path | None, manifest_sha: str) -> str:
    if path is None:
        return "not_provided"
    if not path.is_file():
        return "missing"
    try:
        cached = read_json(path)
    except (OSError, json.JSONDecodeError, ValueError):
        return "corrupt"
    return "valid" if cached.get("manifest_sha256") == manifest_sha else "stale"


def emit(state: str, skill_version: object, core_version: object, cache_state: str, **extra: object) -> None:
    payload = {
        "state": state,
        "skill_version": skill_version,
        "core_version": core_version,
        "requires_full_read": state != "valid",
        "cache_state": cache_state,
    }
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def do_validate(root: Path, summary_path: Path, cache_path: Path | None) -> int:
    manifest_path = root / "references" / "runtime-manifest.json"
    try:
        manifest = read_json(manifest_path)
    except (OSError, json.JSONDecodeError, ValueError):
        emit("manifest_stale", None, None, "not_provided")
        return 2
    manifest_sha = sha256(manifest_path.read_bytes())
    skill_version = manifest.get("skill_version")
    core_version = manifest.get("core_version")
    cache_state = cache_status(cache_path, manifest_sha)
    stale_state, hashes = validate_manifest(root, manifest)
    if stale_state:
        emit(stale_state, skill_version, core_version, cache_state)
        return 2
    if not summary_path.is_file():
        emit("missing", skill_version, core_version, cache_state)
        return 2
    try:
        summary = read_json(summary_path)
    except (OSError, json.JSONDecodeError, ValueError):
        emit("corrupt", skill_version, core_version, cache_state)
        return 2
    if summary.get("skill_version") != skill_version or summary.get("core_version") != core_version:
        emit("version_mismatch", skill_version, core_version, cache_state)
        return 2
    if summary.get("manifest_sha256") != manifest_sha:
        emit("manifest_stale", skill_version, core_version, cache_state)
        return 2
    if summary.get("rule_hashes") != hashes:
        emit("rule_hash_mismatch", skill_version, core_version, cache_state)
        return 2
    if not isinstance(summary.get("summary"), str) or not summary["summary"].strip():
        emit("corrupt", skill_version, core_version, cache_state)
        return 2
    emit("valid", skill_version, core_version, cache_state, summary_file=str(summary_path))
    return 0


def do_refresh(root: Path, summary_path: Path, body_path: Path) -> int:
    manifest_path = root / "references" / "runtime-manifest.json"
    try:
        manifest = read_json(manifest_path)
        stale_state, hashes = validate_manifest(root, manifest)
        if stale_state:
            emit(stale_state, manifest.get("skill_version"), manifest.get("core_version"), "not_provided")
            return 3
        body = body_path.read_text(encoding="utf-8").strip()
        if not body:
            raise ValueError("summary body is empty")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        emit("refresh_failed", None, None, "not_provided", error=str(exc))
        return 3
    payload = {
        "schema_version": 1,
        "skill_version": manifest.get("skill_version"),
        "core_version": manifest.get("core_version"),
        "manifest_sha256": sha256(manifest_path.read_bytes()),
        "rule_hashes": hashes,
        "summary": body,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    emit("refreshed", payload["skill_version"], payload["core_version"], "not_provided", summary_file=str(summary_path))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--skill-root", required=True, type=Path)
    validate.add_argument("--summary", required=True, type=Path)
    validate.add_argument("--cache", type=Path)
    refresh = commands.add_parser("refresh")
    refresh.add_argument("--skill-root", required=True, type=Path)
    refresh.add_argument("--summary", required=True, type=Path)
    refresh.add_argument("--body", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "validate":
        return do_validate(args.skill_root.resolve(), args.summary.resolve(), args.cache.resolve() if args.cache else None)
    return do_refresh(args.skill_root.resolve(), args.summary.resolve(), args.body.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
