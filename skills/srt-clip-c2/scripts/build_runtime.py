#!/usr/bin/env python3
"""Compile the active C2 runtime once from its authoritative source files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(parent for parent in SKILL_ROOT.parents if (parent / "VERSION").is_file())
MANIFEST_PATH = SKILL_ROOT / "references" / "runtime-manifest.json"
RUNTIME_PATH = SKILL_ROOT / "references" / "runtime-current.md"
SKILL_VERSION_PATH = SKILL_ROOT / "VERSION"
SOURCE_FILES = [
    "references/ai-first-constitution.md",
    "references/runtime-contract.md",
    "references/clip-selection-policy.md",
    "references/global-rules.md",
    "references/editorial-policy.md",
    "references/highlight-selection.md",
    "references/product-knowledge-registry.md",
    "references/final-check.md",
]


def sha256(data: bytes) -> str:
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def expand_files(entries: list[str], *, optional: bool = False) -> list[str]:
    expanded: list[str] = []
    for relative in entries:
        if any(char in relative for char in "*?["):
            matches = sorted(path.relative_to(SKILL_ROOT).as_posix() for path in SKILL_ROOT.glob(relative) if path.is_file())
            if not matches and not optional:
                raise ValueError(f"manifest file pattern matched nothing: {relative}")
            expanded.extend(matches)
        elif (SKILL_ROOT / relative).is_file():
            expanded.append(relative)
        elif not optional:
            raise ValueError(f"manifest file is missing: {relative}")
    return list(dict.fromkeys(expanded))


def compile_bundle() -> tuple[str, dict[str, object]]:
    core_version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    skill_version = SKILL_VERSION_PATH.read_text(encoding="utf-8").strip()
    parts = [
        f"# C2 Universal Core {core_version} / Skill {skill_version}｜唯一运行规则正文",
        "",
        "本文件为构建生成的日常运行正文。其下各权威源文件按原文收录；不要手工编辑本文件。",
        "源文件 → 规则行 ID → 本文件源章节及行号的完整映射见同目录 `runtime-manifest.json`。",
        "普通运行先按入口 `SKILL.md` 校验版本化执行摘要；摘要有效时复用，缺失或失效时读取本完整正文。条件文件仅按规则需要读取。",
        "",
    ]
    source_hashes: dict[str, str] = {}
    source_map: list[dict[str, object]] = []

    for index, relative in enumerate(SOURCE_FILES, start=1):
        path = SKILL_ROOT / relative
        raw = path.read_bytes()
        source_hashes[relative] = sha256(raw)
        source_text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        source_text = source_text.rstrip("\n")
        if not source_text.strip():
            raise ValueError(f"empty runtime source: {relative}")

        parts.extend([f"## Runtime source {index}: `{relative}`", "", source_text, ""])
        runtime_start = sum(part.count("\n") + 1 for part in parts[:-2]) + 1
        for source_line, line in enumerate(source_text.splitlines(), start=1):
            if not line.strip():
                continue
            source_map.append({
                "rule_id": f"SRC{index:02d}.L{source_line:04d}",
                "source": relative,
                "source_line": source_line,
                "runtime_section": f"Runtime source {index}: {relative}",
                "runtime_line": runtime_start + source_line - 1,
            })

    runtime = "\n".join(parts).rstrip() + "\n"
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("source_files") != SOURCE_FILES:
        raise ValueError("runtime manifest source_files do not match compiler sources")
    manifest["core_version"] = core_version
    manifest["skill_version"] = skill_version
    integrity_files = expand_files(manifest.get("summary_files", []))
    integrity_files.extend(expand_files(manifest.get("optional_summary_files", []), optional=True))
    for relative in integrity_files:
        source_hashes[relative] = sha256((SKILL_ROOT / relative).read_bytes())
    manifest["source_hashes"] = source_hashes
    manifest["runtime_sha256"] = sha256(runtime.encode("utf-8"))
    manifest["source_map"] = source_map
    return runtime, manifest


def build(check: bool = False) -> bool:
    runtime, manifest = compile_bundle()
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if check:
        runtime_ok = RUNTIME_PATH.is_file() and RUNTIME_PATH.read_text(encoding="utf-8") == runtime
        manifest_ok = MANIFEST_PATH.read_text(encoding="utf-8") == manifest_text
        if not runtime_ok or not manifest_ok:
            print("runtime bundle is stale; run scripts/build_runtime.py")
            return False
        print("runtime bundle and source map are current")
        return True

    RUNTIME_PATH.write_text(runtime, encoding="utf-8", newline="\n")
    MANIFEST_PATH.write_text(manifest_text, encoding="utf-8", newline="\n")
    print(f"built {RUNTIME_PATH} ({len(runtime)} characters)")
    print(f"mapped {len(manifest['source_map'])} non-empty source lines")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated runtime files are stale")
    args = parser.parse_args()
    raise SystemExit(0 if build(check=args.check) else 1)
