#!/usr/bin/env python3
"""Deterministic direct-term guard for SRT and numbered duration-text inputs.

This tool checks only the exact terms listed in references/global-rules.md.
Semantic equivalents remain an AI judgment; a direct hit excludes its full
cue only. The script uses the Python standard library and is optional at
runtime: the same rule must be followed manually when it cannot be run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


SKILL_ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = SKILL_ROOT / "references" / "global-rules.md"
DURATION_LINE = re.compile(r"^\s*(\d+)\s+([0-9]+(?:\.[0-9]+)?)\s+(.+?)\s*$")
SRT_TIME = re.compile(
    r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*"
    r"\d{2}:\d{2}:\d{2}[,.]\d{3}(?:\s+.*)?$"
)


@dataclass(frozen=True)
class Cue:
    cue_id: str
    text: str


def normalize_for_match(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return "".join(
        char
        for char in normalized
        if not char.isspace()
        and unicodedata.category(char)[0] not in {"P", "Z", "C"}
    )


def load_formal_terms(path: Path = RULES_PATH) -> list[str]:
    rules = path.read_text(encoding="utf-8-sig")
    try:
        section = rules.split("## 正式禁用词库", 1)[1].split("\n## ", 1)[0]
    except IndexError as error:
        raise ValueError("formal prohibited-term section is missing") from error
    terms = re.findall(r"^\s*-\s+`([^`]+)`", section, flags=re.MULTILINE)
    if not terms:
        raise ValueError("formal prohibited-term list is empty")
    return terms


def parse_srt_blocks(text: str) -> list[Cue]:
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.strip("\ufeff\r") for line in block.splitlines()]
        if len(lines) < 3 or not lines[0].isdigit() or not SRT_TIME.match(lines[1]):
            continue
        cue_text = "\n".join(lines[2:]).strip()
        if cue_text:
            cues.append(Cue(lines[0], cue_text))
    return cues


def parse_duration_text(text: str) -> list[Cue]:
    cues = []
    for line in text.splitlines():
        match = DURATION_LINE.match(line)
        if match:
            cues.append(Cue(match.group(1), match.group(3)))
    return cues


def parse_cues(text: str) -> list[Cue]:
    cues = parse_srt_blocks(text)
    if not cues:
        cues = parse_duration_text(text)
    if not cues:
        raise ValueError("no SRT cues or numbered duration-text rows were found")
    ids = [cue.cue_id for cue in cues]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate cue IDs make selection validation ambiguous")
    return cues


def find_direct_hits(cues: Iterable[Cue], terms: Iterable[str]) -> list[dict[str, object]]:
    normalized_terms = [(term, normalize_for_match(term)) for term in terms]
    hits = []
    for cue in cues:
        normalized_text = normalize_for_match(cue.text)
        matched = [term for term, normalized_term in normalized_terms if normalized_term in normalized_text]
        if matched:
            hits.append({"cue_id": cue.cue_id, "matched_terms": matched})
    return hits


def build_report(
    cues: list[Cue],
    terms: list[str],
    selected_ids: Optional[list[str]] = None,
    final_text: Optional[str] = None,
) -> dict[str, object]:
    direct_hits = find_direct_hits(cues, terms)
    hit_ids = [str(hit["cue_id"]) for hit in direct_hits]
    selected_hit_ids = (
        [cue_id for cue_id in selected_ids if cue_id in set(hit_ids)]
        if selected_ids is not None
        else []
    )
    known_ids = {cue.cue_id for cue in cues}
    unknown_selected_ids = (
        [cue_id for cue_id in selected_ids if cue_id not in known_ids]
        if selected_ids is not None
        else []
    )
    final_text_hits = find_direct_hits([Cue("final_text", final_text)], terms) if final_text is not None else []
    validating_output = selected_ids is not None or final_text is not None
    failed = bool(selected_hit_ids or unknown_selected_ids or final_text_hits)
    return {
        "status": "FAIL" if failed else "PASS" if validating_output else "SCAN_COMPLETE",
        "source_rows": len(cues),
        "formal_terms": terms,
        "direct_hits": direct_hits,
        "excluded_full_cue_ids": hit_ids,
        "selected_hit_ids": selected_hit_ids,
        "unknown_selected_ids": unknown_selected_ids,
        "final_text_hits": final_text_hits,
    }


def parse_selected_ids(value: Optional[str]) -> Optional[list[str]]:
    if value is None:
        return None
    ids = [item.strip() for item in value.split(",") if item.strip()]
    if not ids:
        raise ValueError("--selected-ids must contain at least one cue ID")
    return ids


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="SRT file or numbered duration-text file")
    parser.add_argument("--selected-ids", help="comma-separated cue IDs used in the final clip")
    parser.add_argument("--final-text", type=Path, help="file containing the final clip, title, and hashtags")
    args = parser.parse_args(argv)

    try:
        cues = parse_cues(args.source.read_text(encoding="utf-8-sig"))
        terms = load_formal_terms()
        selected_ids = parse_selected_ids(args.selected_ids)
        final_text = args.final_text.read_text(encoding="utf-8-sig") if args.final_text else None
        report = build_report(cues, terms, selected_ids, final_text)
    except (OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
