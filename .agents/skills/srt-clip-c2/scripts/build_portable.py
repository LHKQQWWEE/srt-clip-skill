#!/usr/bin/env python3
"""Build the compact single-document portable runtime."""

from __future__ import annotations

import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(
    parent for parent in SKILL_ROOT.parents
    if (parent / "VERSION").is_file() and (parent / "plugin.json").is_file()
)
SOURCES = [
    "SKILL.md",
    "references/commerce-advisory.md",
    "references/execution-summary.json",
    "references/runtime-manifest.json",
    "references/runtime-current.md",
    "references/long-context-mode.md",
    "product-knowledge-packs/womens-fashion.md",
    "product-knowledge-packs/shoes.md",
    "product-knowledge-packs/scarves.md",
]


def build() -> str:
    core_version = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    package_version = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
    plugin = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
    execution_protocol = plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]
    parts = [
        f"# SRT Clip C2 Universal · Core {core_version} · Plugin {package_version} Portable",
        "",
        "This portable file embeds the slim entry and one compiled runtime body. The commerce advisory guide, long-context rules, and product knowledge packs are included for portability and loaded only when their stated conditions apply. Developer-only update procedures, tests, and scripts are excluded; the runtime manifest and source-line map remain included for integrity and traceability.",
        "",
        "---",
        "",
        "## 执行摘要与版本校验协议（不定义高于规则源的新业务规则）",
        "",
        execution_protocol,
        "",
        "---",
    ]
    for relative in SOURCES:
        source = (SKILL_ROOT / relative).read_text(encoding="utf-8").strip()
        parts.extend(["", f"## Embedded source: {relative}", "", source])
    return "\n".join(parts).rstrip() + "\n"


if __name__ == "__main__":
    output = SKILL_ROOT / "C2-Universal-Portable.md"
    output.write_text(build(), encoding="utf-8", newline="\n")
    print(f"Rebuilt {output}")
