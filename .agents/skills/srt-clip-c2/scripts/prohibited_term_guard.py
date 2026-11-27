#!/usr/bin/env python3
"""Development-only scanner for the C2 prohibited-term registry.

Direct entries and their explicitly listed equivalents are mechanical hard
matches. Confirmed contextual advertising claims are also identified and
excluded cue-by-cue; ordinary language is protected and unresolved contexts
remain review-only. Daily editing remains AI-first and does not depend on this
development scanner.
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


@dataclass(frozen=True)
class TermEntry:
    term: str
    match_class: str
    category: str
    source: str
    trigger_condition: str
    allowed_exceptions: tuple[str, ...]
    confirmed_equivalents: tuple[str, ...]
    scope: str
    test_cases: tuple[str, ...]
    version_record: str


def normalize_for_match(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return "".join(
        char
        for char in normalized
        if not char.isspace()
        and unicodedata.category(char)[0] not in {"P", "Z", "C"}
    )


def _cell_values(value: str) -> tuple[str, ...]:
    if value.strip() in {"", "—", "-", "无"}:
        return ()
    return tuple(part.strip().strip("`") for part in value.split("、") if part.strip())


def load_term_registry(path: Path = RULES_PATH) -> list[TermEntry]:
    rules = path.read_text(encoding="utf-8-sig")
    try:
        section = rules.split("## 正式禁用词库", 1)[1].split("\n## ", 1)[0]
    except IndexError as error:
        raise ValueError("formal prohibited-term section is missing") from error

    entries: list[TermEntry] = []
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 10:
            raise ValueError(f"invalid prohibited-term registry row: {line}")
        term = cells[0].strip("`")
        match_class = cells[1].strip("`")
        if match_class not in {"direct", "contextual"}:
            raise ValueError(f"invalid match class for {term}: {match_class}")
        entries.append(
            TermEntry(
                term=term,
                match_class=match_class,
                category=cells[2],
                source=cells[3],
                trigger_condition=cells[4],
                allowed_exceptions=_cell_values(cells[5]),
                confirmed_equivalents=_cell_values(cells[6]),
                scope=cells[7],
                test_cases=_cell_values(cells[8]),
                version_record=cells[9],
            )
        )
    if not entries:
        raise ValueError("formal prohibited-term registry is empty")
    if len({entry.term for entry in entries}) != len(entries):
        raise ValueError("formal prohibited-term registry contains duplicate terms")
    return entries


def load_formal_terms(path: Path = RULES_PATH) -> list[str]:
    """Backward-compatible helper returning direct canonical entries only."""
    return [entry.term for entry in load_term_registry(path) if entry.match_class == "direct"]


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


def _entries(entries: Iterable[TermEntry | str]) -> list[TermEntry]:
    normalized: list[TermEntry] = []
    for entry in entries:
        if isinstance(entry, TermEntry):
            normalized.append(entry)
        else:
            normalized.append(
                TermEntry(
                    term=str(entry),
                    match_class="direct",
                    category="legacy direct term",
                    source="legacy caller",
                    trigger_condition="literal match",
                    allowed_exceptions=(),
                    confirmed_equivalents=(),
                    scope="full cue",
                    test_cases=(),
                    version_record="legacy caller",
                )
            )
    return normalized


def find_direct_hits(cues: Iterable[Cue], terms: Iterable[str]) -> list[dict[str, object]]:
    """Legacy literal matcher; only use with a direct-term list."""
    normalized_terms = [(term, normalize_for_match(term)) for term in terms]
    hits = []
    for cue in cues:
        normalized_text = normalize_for_match(cue.text)
        matched = [term for term, normalized_term in normalized_terms if normalized_term in normalized_text]
        if matched:
            hits.append({"cue_id": cue.cue_id, "matched_terms": matched})
    return hits


def _hits_for_entries(cues: Iterable[Cue], entries: list[TermEntry], match_class: str) -> list[dict[str, object]]:
    eligible = [entry for entry in entries if entry.match_class == match_class]
    hits: list[dict[str, object]] = []
    for cue in cues:
        normalized_text = normalize_for_match(cue.text)
        matched_terms = []
        for entry in eligible:
            match_text = normalized_text
            for allowed in entry.allowed_exceptions:
                match_text = match_text.replace(normalize_for_match(allowed), "")
            if normalize_for_match(entry.term) in match_text:
                matched_terms.append(entry.term)
        if matched_terms:
            hits.append({"cue_id": cue.cue_id, "matched_terms": matched_terms})
    return hits


def _confirmed_equivalent_hits(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    aliases = [
        (entry.term, alias, normalize_for_match(alias))
        for entry in entries
        if entry.match_class == "direct"
        for alias in entry.confirmed_equivalents
    ]
    hits: list[dict[str, object]] = []
    for cue in cues:
        normalized_text = normalize_for_match(cue.text)
        matched = []
        for term, alias, normalized_alias in aliases:
            entry = next(item for item in entries if item.term == term)
            match_text = normalized_text
            for allowed in entry.allowed_exceptions:
                match_text = match_text.replace(normalize_for_match(allowed), "")
            if normalized_alias in match_text:
                matched.append({"term": term, "expression": alias})
        if matched:
            hits.append({"cue_id": cue.cue_id, "matched_equivalents": matched})
    return hits


def _contextual_equivalent_hits(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    aliases = [
        (entry.term, alias, normalize_for_match(alias))
        for entry in entries
        if entry.match_class == "contextual"
        for alias in entry.confirmed_equivalents
    ]
    grouped: dict[str, dict[str, object]] = {}
    for cue in cues:
        normalized_text = normalize_for_match(cue.text)
        for term, alias, normalized_alias in aliases:
            if normalized_alias not in normalized_text:
                continue
            hit = grouped.setdefault(cue.cue_id, {"cue_id": cue.cue_id, "matched_terms": [], "matched_expressions": []})
            if term not in hit["matched_terms"]:
                hit["matched_terms"].append(term)
            if alias not in hit["matched_expressions"]:
                hit["matched_expressions"].append(alias)
    return list(grouped.values())


def classify_contextual_hit(text: str, term: str) -> str:
    """Classify only the confirmed absolute-expression boundaries in Stage 3.

    Returns ``block`` for an explicit product claim, ``allow`` for the
    confirmed ordinary ordinal/scheduling examples, and ``uncertain`` when the
    surrounding sentence does not establish either meaning. This deliberately
    avoids synonym and ASR expansion.
    """
    normalized = normalize_for_match(text)
    normalized_term = normalize_for_match(term)
    if term == "最好" and re.search(r"全网没有比.{0,16}更好的?", normalized):
        return "block"
    if normalized_term not in normalized:
        return "uncertain"

    if term == "全网最好":
        return "block"

    if term == "第一":
        if re.search(r"第一(?:件|步|条)", normalized):
            return "allow"
        ranking_patterns = (
            r"销量第一", r"全网第一", r"行业第一", r"品牌排名第一",
            r"品牌第一", r"同类产品第一", r"排名第一", r"排行第一",
            r"第一名", r"位居第一", r"稳居第一",
        )
        if any(re.search(pattern, normalized) for pattern in ranking_patterns):
            return "block"
        return "uncertain"

    if term == "最好":
        if re.search(r"最好(?:明天|今天|現在|现在|先|再|提前|尽量|下次)", normalized):
            return "allow"
        product_claim_patterns = (
            r"全网最好", r"市场上最好", r"最好的(?:面料|品质|质量|工艺|做工|款式|商品|产品)",
            r"(?:这件(?:衣服|外套|裤子|商品|产品)?|这款(?:商品|产品|衣服|款式)?|这个款式|商品|产品|面料|品质|质量|工艺|做工|款式|这)"
            r".{0,8}(?:就是|是|算|属于)?(?:全网|市场上)?最好的?",
            r"全网没有比.{0,16}更好的?",
        )
        if any(re.search(pattern, normalized) for pattern in product_claim_patterns):
            return "block"
        return "uncertain"

    if term == "首选":
        product_context_patterns = (
            r"首选搭配", r".{0,8}(?:衣服|外套|裤子|商品|产品|这件|这款|搭配|穿搭|购买|推荐|本场|种草).{0,8}首选",
            r"首选.{0,8}(?:搭配|穿搭|衣服|外套|裤子|商品|产品|购买|推荐)",
            r"我的首选", r"你们购买的首选",
        )
        if any(re.search(pattern, normalized) for pattern in product_context_patterns):
            return "block"
        return "uncertain"

    # The remaining registered absolute phrases are blocked when the phrase
    # makes a concrete product quality, material, workmanship, design, or
    # brand claim. Bare or unrelated uses remain review-only.
    product_claim_patterns = (
        r"国家级.{0,4}(?:品质|质量|面料|工艺|设计|品牌|产品|商品|标准|技术)",
        r"最高级.{0,4}(?:品质|质量|面料|工艺|设计|品牌|产品|商品|标准|技术)",
        r"顶级.{0,4}(?:品质|质量|面料|工艺|设计|品牌|产品|商品|材质)",
        r"(?:品质|质量|面料|工艺|设计|品牌|产品|商品|材质).{0,4}顶级",
        r"绝无仅有.{0,6}(?:设计|品质|质量|面料|工艺|款式|产品|商品)",
        r"史无前例.{0,6}(?:设计|品质|质量|面料|工艺|款式|产品|商品)",
        r"(?:这件|这款|商品|产品|衣服|外套|裤子).{0,6}(?:绝无仅有|史无前例)",
    )
    if any(re.search(pattern, normalized) for pattern in product_claim_patterns):
        return "block"
    return "uncertain"


def _contextual_decisions(
    cues: Iterable[Cue], candidates: list[dict[str, object]]
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    cue_by_id = {cue.cue_id: cue for cue in cues}
    groups: dict[str, dict[str, list[str]]] = {"block": {}, "allow": {}, "uncertain": {}}
    for hit in candidates:
        cue = cue_by_id[str(hit["cue_id"])]
        for term in hit["matched_terms"]:
            decision = classify_contextual_hit(cue.text, str(term))
            groups[decision].setdefault(cue.cue_id, []).append(str(term))

    def rendered(decision: str) -> list[dict[str, object]]:
        return [
            {"cue_id": cue_id, "matched_terms": terms}
            for cue_id, terms in groups[decision].items()
        ]

    return rendered("block"), rendered("allow"), rendered("uncertain")


def _edit_distance_at_most_one(left: str, right: str) -> bool:
    if abs(len(left) - len(right)) > 1:
        return False
    if left == right:
        return True
    if len(left) > len(right):
        left, right = right, left
    i = j = edits = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            i += 1
            j += 1
            continue
        edits += 1
        if edits > 1:
            return False
        if len(left) == len(right):
            i += 1
            j += 1
        else:
            j += 1
    if j < len(right) or i < len(left):
        edits += 1
    return edits <= 1


def find_asr_suspicions(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    """Flag one-edit near forms as review-only risks; never promote them to hits."""
    eligible = [entry for entry in entries if entry.match_class == "contextual" and len(normalize_for_match(entry.term)) >= 3]
    suspicions: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for cue in cues:
        normalized = normalize_for_match(cue.text)
        for entry in eligible:
            canonical = normalize_for_match(entry.term)
            aliases = [normalize_for_match(alias) for alias in entry.confirmed_equivalents]
            if canonical in normalized or any(alias in normalized for alias in aliases):
                continue
            # Same-length substitutions and one inserted character are useful
            # warning shapes; shorter substrings create noisy prefix matches.
            for length in {len(canonical), len(canonical) + 1}:
                if length <= 1:
                    continue
                for start in range(max(0, len(normalized) - length + 1)):
                    fragment = normalized[start:start + length]
                    if fragment == canonical or not _edit_distance_at_most_one(canonical, fragment):
                        continue
                    key = (cue.cue_id, entry.term)
                    if key in seen:
                        continue
                    seen.add(key)
                    suspicions.append({
                        "cue_id": cue.cue_id,
                        "registered_term": entry.term,
                        "observed_fragment": fragment,
                        "classification": "unconfirmed_possible_asr_or_typo",
                        "auto_blocked": False,
                    })
    return suspicions


def _contextual_candidates(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    return _hits_for_entries(cues, entries, "contextual")


def _cue_ids(*hit_groups: list[dict[str, object]]) -> list[str]:
    return list(dict.fromkeys(str(hit["cue_id"]) for group in hit_groups for hit in group))


def build_report(
    cues: list[Cue],
    terms: list[TermEntry] | list[str],
    selected_ids: Optional[list[str]] = None,
    final_text: Optional[str] = None,
) -> dict[str, object]:
    entries = _entries(terms)
    direct_hits = _hits_for_entries(cues, entries, "direct")
    equivalent_hits = _confirmed_equivalent_hits(cues, entries)
    contextual_candidates = _contextual_candidates(cues, entries)
    contextual_equivalent_hits = _contextual_equivalent_hits(cues, entries)
    all_contextual_candidates = contextual_candidates + contextual_equivalent_hits
    contextual_block_hits, contextual_allowed_hits, contextual_unresolved_hits = _contextual_decisions(cues, all_contextual_candidates)
    asr_suspicions = find_asr_suspicions(cues, entries)
    hard_hit_ids = set(_cue_ids(direct_hits, equivalent_hits, contextual_block_hits))
    excluded_ids = [cue.cue_id for cue in cues if cue.cue_id in hard_hit_ids]
    selected_hit_ids = (
        [cue_id for cue_id in selected_ids if cue_id in hard_hit_ids]
        if selected_ids is not None
        else []
    )
    known_ids = {cue.cue_id for cue in cues}
    unknown_selected_ids = (
        [cue_id for cue_id in selected_ids if cue_id not in known_ids]
        if selected_ids is not None
        else []
    )
    final_cues = [Cue("final_text", final_text)] if final_text is not None else []
    final_text_hits = _hits_for_entries(final_cues, entries, "direct")
    final_equivalent_hits = _confirmed_equivalent_hits(final_cues, entries)
    final_contextual_candidates = _contextual_candidates(final_cues, entries)
    final_contextual_equivalent_hits = _contextual_equivalent_hits(final_cues, entries)
    all_final_contextual_candidates = final_contextual_candidates + final_contextual_equivalent_hits
    final_contextual_block_hits, final_contextual_allowed_hits, final_contextual_unresolved_hits = _contextual_decisions(final_cues, all_final_contextual_candidates)
    final_asr_suspicions = find_asr_suspicions(final_cues, entries)
    selected_set = set(selected_ids or [])

    def attach_source_ids(hit: dict[str, object], expressions: Iterable[str]) -> None:
        normalized_expressions = [normalize_for_match(expression) for expression in expressions]
        matched_source_ids = [
            cue.cue_id
            for cue in cues
            if any(expression in normalize_for_match(cue.text) for expression in normalized_expressions)
        ]
        hit["source_cue_ids"] = matched_source_ids
        hit["selected_source_cue_ids"] = [cue_id for cue_id in matched_source_ids if cue_id in selected_set]

    for hit in final_text_hits:
        attach_source_ids(hit, hit["matched_terms"])
    for hit in final_equivalent_hits:
        attach_source_ids(hit, [item["expression"] for item in hit["matched_equivalents"]])
    for hit in all_final_contextual_candidates:
        attach_source_ids(hit, hit.get("matched_expressions", hit["matched_terms"]))
    for hit in final_contextual_block_hits + final_contextual_allowed_hits + final_contextual_unresolved_hits:
        attach_source_ids(hit, hit.get("matched_expressions", hit["matched_terms"]))
    validating_output = selected_ids is not None or final_text is not None
    selected_contextual_hit_ids = [cue_id for cue_id in selected_ids or [] if cue_id in set(_cue_ids(contextual_block_hits))]
    failed = bool(selected_hit_ids or unknown_selected_ids or final_text_hits or final_equivalent_hits or final_contextual_block_hits)
    needs_context_review = bool(contextual_unresolved_hits or final_contextual_unresolved_hits or asr_suspicions or final_asr_suspicions)
    status = "FAIL" if failed else "REVIEW_CONTEXT" if needs_context_review else "PASS" if validating_output else "SCAN_COMPLETE"
    return {
        "status": status,
        "source_rows": len(cues),
        "formal_terms": [entry.term for entry in entries if entry.match_class == "direct"],
        "contextual_terms": [entry.term for entry in entries if entry.match_class == "contextual"],
        "direct_hits": direct_hits,
        "confirmed_equivalent_hits": equivalent_hits,
        "contextual_candidates": contextual_candidates,
        "contextual_confirmed_equivalent_hits": contextual_equivalent_hits,
        "contextual_block_hits": contextual_block_hits,
        "contextual_allowed_hits": contextual_allowed_hits,
        "contextual_unresolved_hits": contextual_unresolved_hits,
        "selected_contextual_candidate_ids": [cue_id for cue_id in selected_ids or [] if cue_id in set(_cue_ids(contextual_candidates))],
        "selected_contextual_hit_ids": selected_contextual_hit_ids,
        "excluded_full_cue_ids": excluded_ids,
        "selected_hit_ids": selected_hit_ids,
        "unknown_selected_ids": unknown_selected_ids,
        "final_text_hits": final_text_hits,
        "final_confirmed_equivalent_hits": final_equivalent_hits,
        "final_contextual_candidates": final_contextual_candidates,
        "final_contextual_confirmed_equivalent_hits": final_contextual_equivalent_hits,
        "final_contextual_block_hits": final_contextual_block_hits,
        "final_contextual_allowed_hits": final_contextual_allowed_hits,
        "final_contextual_unresolved_hits": final_contextual_unresolved_hits,
        "contextual_candidate_ids": _cue_ids(contextual_candidates),
        "contextual_block_ids": _cue_ids(contextual_block_hits),
        "contextual_allow_ids": _cue_ids(contextual_allowed_hits),
        "contextual_unresolved_ids": _cue_ids(contextual_unresolved_hits),
        "contextual_review_required": needs_context_review,
        "asr_suspicions": asr_suspicions,
        "final_asr_suspicions": final_asr_suspicions,
        "unresolved_expressions": contextual_unresolved_hits,
        "final_unresolved_expressions": final_contextual_unresolved_hits,
        "validated_source_cue_ids": selected_hit_ids,
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
        registry = load_term_registry()
        selected_ids = parse_selected_ids(args.selected_ids)
        final_text = args.final_text.read_text(encoding="utf-8-sig") if args.final_text else None
        report = build_report(cues, registry, selected_ids, final_text)
    except (OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return {"FAIL": 1, "REVIEW_CONTEXT": 2}.get(str(report["status"]), 0)


if __name__ == "__main__":
    raise SystemExit(main())
