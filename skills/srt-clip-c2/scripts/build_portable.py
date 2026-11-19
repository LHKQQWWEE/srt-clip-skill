#!/usr/bin/env python3
"""Rebuild the portable C2 document from the active source files."""

from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "SKILL.md",
    "references/ai-first-constitution.md",
    "references/editorial-policy.md",
    "references/highlight-selection.md",
    "references/product-knowledge-registry.md",
    "references/global-rules.md",
    "references/qianchuan-offline.md",
    "references/final-check.md",
    "references/long-context-mode.md",
    "references/update-protocol.md",
    "product-knowledge-packs/womens-fashion.md",
    "product-knowledge-packs/shoes.md",
    "product-knowledge-packs/scarves.md",
    "tests/quality-rubric.md",
    "scripts/README.md",
]


def build() -> str:
    version = (SKILL_ROOT.parents[1] / "VERSION").read_text(encoding="utf-8").strip()
    parts = [
        f"# SRT Clip C2 Universal {version} Portable",
        "",
        f"This portable document embeds the current {version} entry and its active instruction sources. Source files are reproduced below; historical acceptance records and private regression transcripts are excluded.",
        "",
        "---",
    ]
    for relative in SOURCES:
        source = (SKILL_ROOT / relative).read_text(encoding="utf-8").strip()
        parts.extend(["", f"## Embedded source: {relative}", "", source])
    return "\n".join(parts).rstrip() + "\n"


if __name__ == "__main__":
    output = SKILL_ROOT / "C2-Universal-Portable.md"
    output.write_text(build(), encoding="utf-8")
    print(f"Rebuilt {output}")
