#!/usr/bin/env python3
"""Development and release-test helpers for C2 SRT and duration-text workflows."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable, Optional

from prohibited_term_guard import Cue as GuardCue
from prohibited_term_guard import TermEntry, classify_contextual_hit, find_asr_suspicions, load_term_registry, normalize_for_match


SKILL_ROOT = Path(__file__).resolve().parents[1]
TIMECODE = r"\d{2,}:\d{2}:\d{2}[,.]\d{3}"
SRT_TIME_LINE = re.compile(rf"^\s*({TIMECODE})\s*-->\s*({TIMECODE})(?:[ \t]+.*)?\s*$")
DURATION_ROW = re.compile(r"^\s*(?P<cue_id>\S+)\s+(?P<duration>\S+)[ \t](?P<text>.*)$")
DURATION_VALUE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")


@dataclass(frozen=True)
class Cue:
    cue_id: str
    cue_number: int
    source_order: int
    line_start: int
    line_end: int
    original_text: str
    start_ms: Decimal
    end_ms: Decimal
    duration_ms: Decimal
    timeline_known: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.cue_id,
            "source_order": self.source_order,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "original_text": self.original_text,
            "start_ms": _number_value(self.start_ms) if self.timeline_known else None,
            "end_ms": _number_value(self.end_ms) if self.timeline_known else None,
            "duration_ms": _number_value(self.duration_ms),
            "start_ms_exact": _decimal_string(self.start_ms) if self.timeline_known else None,
            "end_ms_exact": _decimal_string(self.end_ms) if self.timeline_known else None,
            "duration_ms_exact": _decimal_string(self.duration_ms),
            "timeline_known": self.timeline_known,
        }


@dataclass
class SourceReport:
    source_type: str
    cues: list[Cue] | tuple[Cue, ...] = field(default_factory=list)
    parsed_ranges: list[dict[str, object]] = field(default_factory=list)
    unparsed_ranges: list[dict[str, object]] = field(default_factory=list)
    diagnostics: list[dict[str, object]] = field(default_factory=list)
    recognized_header_lines: list[dict[str, object]] = field(default_factory=list)
    total_blocks: int = 0
    status: str = "BLOCKED"
    source_sha256: str = ""
    source_map_sha256: str = ""


FULL_CLIP_SPEED = Decimal("1.2")


def _source_map_records(cues: Iterable[Cue]) -> list[dict[str, object]]:
    return [
        {
            "id": cue.cue_id,
            "source_order": cue.source_order,
            "original_text": cue.original_text,
            "start_ms_exact": _decimal_string(cue.start_ms) if cue.timeline_known else None,
            "end_ms_exact": _decimal_string(cue.end_ms) if cue.timeline_known else None,
            "duration_ms_exact": _decimal_string(cue.duration_ms),
            "timeline_known": cue.timeline_known,
        }
        for cue in cues
    ]


def _source_map_digest(cues: Iterable[Cue]) -> str:
    payload = json.dumps(_source_map_records(cues), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _split_srt_blocks(text: str) -> list[tuple[int, int, int, list[str]]]:
    blocks: list[tuple[int, int, int, list[str]]] = []
    current: list[str] = []
    start_line = 0
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line
        if line_number == 1:
            line = line.removeprefix("\ufeff")
        if not line.strip():
            if current:
                blocks.append((len(blocks), start_line, line_number - 1, current))
                current = []
            continue
        if not current:
            start_line = line_number
        current.append(line)
    if current:
        blocks.append((len(blocks), start_line, len(text.splitlines()), current))
    return blocks


def _timecode_ms(value: str) -> int:
    match = re.fullmatch(r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})", value)
    if not match:
        raise ValueError("invalid SRT timecode")
    hours, minutes, seconds, millis = (int(part) for part in match.groups())
    if minutes >= 60 or seconds >= 60:
        raise ValueError("minutes and seconds must be below 60")
    return (((hours * 60 + minutes) * 60 + seconds) * 1000) + millis


def _parse_srt(text: str) -> SourceReport:
    blocks = _split_srt_blocks(text)
    report = SourceReport(source_type="srt", total_blocks=len(blocks))
    for block_order, line_start, line_end, lines in blocks:
        cue_id = lines[0].strip()
        reason = None
        if not re.fullmatch(r"\d+", cue_id):
            reason = "missing numeric cue ID"
        elif len(lines) < 2:
            reason = "missing SRT timecode line"
        else:
            timing = SRT_TIME_LINE.fullmatch(lines[1])
            if not timing:
                reason = "invalid SRT timecode line"
            elif len(lines) < 3 or not "\n".join(lines[2:]).strip():
                reason = "missing subtitle text"

        if reason:
            report.unparsed_ranges.append({
                "start_line": line_start,
                "end_line": line_end,
                "reason": reason,
                "source_text": "\n".join(lines),
            })
            continue

        assert timing is not None
        try:
            start_ms = _timecode_ms(timing.group(1))
            end_ms = _timecode_ms(timing.group(2))
        except ValueError as error:
            report.unparsed_ranges.append({
                "start_line": line_start,
                "end_line": line_end,
                "reason": str(error),
                "source_text": "\n".join(lines),
            })
            continue
        cue = Cue(
            cue_id=cue_id,
            cue_number=int(cue_id),
            source_order=block_order,
            line_start=line_start,
            line_end=line_end,
            original_text="\n".join(lines[2:]),
            start_ms=Decimal(start_ms),
            end_ms=Decimal(end_ms),
            duration_ms=Decimal(end_ms - start_ms),
        )
        report.cues.append(cue)
        report.parsed_ranges.append({
            "start_line": line_start,
            "end_line": line_end,
            "cue_ids": [cue_id],
        })

    _validate_cues(report, check_time_order=True)
    return _finish_report(report)


def _parse_duration_text(text: str) -> SourceReport:
    lines = [(number, value) for number, value in enumerate(text.splitlines(), 1) if value.strip()]
    header_labels = {"srt文案", "【字幕列表】"}
    recognized_header_lines = []
    while lines and lines[0][1].strip() in header_labels:
        line_number, line = lines.pop(0)
        recognized_header_lines.append({"line": line_number, "text": line})
    report = SourceReport(source_type="duration_text", total_blocks=len(lines))
    report.recognized_header_lines = recognized_header_lines
    cursor_ms = Decimal(0)
    timeline_known = True
    for source_order, (line_number, line) in enumerate(lines):
        match = DURATION_ROW.fullmatch(line)
        reason = None
        if not match or not re.fullmatch(r"\d+", match.group("cue_id")):
            reason = "expected numbered duration row: ID duration_seconds original_text"
        elif not DURATION_VALUE.fullmatch(match.group("duration")):
            reason = "duration must be a decimal number of seconds"
        elif not match.group("text").strip():
            reason = "missing subtitle text"

        if reason:
            report.unparsed_ranges.append({
                "start_line": line_number,
                "end_line": line_number,
                "reason": reason,
                "source_text": line,
            })
            timeline_known = False
            continue

        try:
            seconds = Decimal(match.group("duration"))
        except InvalidOperation:
            report.unparsed_ranges.append({
                "start_line": line_number,
                "end_line": line_number,
                "reason": "duration must be a decimal number of seconds",
                "source_text": line,
            })
            timeline_known = False
            continue
        duration_ms = seconds * 1000
        start_ms = cursor_ms
        end_ms = cursor_ms + duration_ms
        cue_id = match.group("cue_id")
        cue = Cue(
            cue_id=cue_id,
            cue_number=int(cue_id),
            source_order=source_order,
            line_start=line_number,
            line_end=line_number,
            original_text=match.group("text"),
            start_ms=start_ms,
            end_ms=end_ms,
            duration_ms=duration_ms,
            timeline_known=timeline_known,
        )
        report.cues.append(cue)
        report.parsed_ranges.append({
            "start_line": line_number,
            "end_line": line_number,
            "cue_ids": [cue_id],
        })
        cursor_ms = end_ms

    _validate_cues(report, check_time_order=False)
    return _finish_report(report)


def _validate_cues(report: SourceReport, check_time_order: bool) -> None:
    seen: dict[int, Cue] = {}
    previous: Optional[Cue] = None
    for cue in report.cues:
        if cue.cue_number in seen:
            first_seen = seen[cue.cue_number]
            report.diagnostics.append({
                "code": "duplicate_id",
                "cue_ids": [first_seen.cue_id, cue.cue_id],
                "line_start": first_seen.line_start,
                "line_end": cue.line_end,
                "reason": "duplicate cue ID",
            })
        else:
            seen[cue.cue_number] = cue
        adjacent = previous is not None and cue.source_order == previous.source_order + 1
        if adjacent and cue.cue_number < previous.cue_number:
            report.diagnostics.append({
                "code": "numbering_inversion",
                "cue_ids": [previous.cue_id, cue.cue_id],
                "line_start": cue.line_start,
                "line_end": cue.line_end,
                "reason": "cue IDs decrease in source order",
            })
        if cue.duration_ms <= 0:
            report.diagnostics.append({
                "code": "non_positive_duration",
                "cue_ids": [cue.cue_id],
                "line_start": cue.line_start,
                "line_end": cue.line_end,
                "reason": "cue duration must be positive",
            })
        if check_time_order and adjacent and cue.start_ms < previous.start_ms:
            report.diagnostics.append({
                "code": "timestamp_inversion",
                "cue_ids": [previous.cue_id, cue.cue_id],
                "line_start": cue.line_start,
                "line_end": cue.line_end,
                "reason": "cue start times decrease in source order",
            })
        previous = cue


def _finish_report(report: SourceReport) -> SourceReport:
    if report.total_blocks == 0:
        report.diagnostics.append({
            "code": "empty_source",
            "cue_ids": [],
            "line_start": 1,
            "line_end": 1,
            "reason": "source contains no subtitle rows",
        })
    if report.unparsed_ranges or report.total_blocks == 0:
        report.status = "BLOCKED"
    elif report.diagnostics:
        report.status = "FAIL"
    else:
        report.status = "PASS"
    report.source_map_sha256 = _source_map_digest(report.cues)
    report.cues = tuple(report.cues)
    return report


def parse_source(text: str, source_sha256: Optional[str] = None) -> SourceReport:
    """Parse every nonempty SRT block or numbered duration row without skipping failures."""
    if "-->" in text:
        report = _parse_srt(text)
    else:
        report = _parse_duration_text(text)
    report.source_sha256 = source_sha256 or hashlib.sha256(text.encode("utf-8")).hexdigest()
    return report


def find_direct_hits(cues: Iterable[Cue], terms: Iterable[str | TermEntry]) -> list[dict[str, object]]:
    """Match listed direct terms cue-by-cue; never combine neighboring subtitles."""
    entry_list = list(terms)
    direct_entries = [entry for entry in entry_list if isinstance(entry, TermEntry) and entry.match_class == "direct"]
    legacy_terms = [str(entry) for entry in entry_list if not isinstance(entry, TermEntry)]
    matched_ids: dict[str, list[str]] = {}
    for entry in direct_entries:
        matched_ids.setdefault(entry.term, [])
    for term in legacy_terms:
        matched_ids.setdefault(term, [])

    for cue in cues:
        normalized_text = normalize_for_match(cue.original_text)
        for entry in direct_entries:
            match_text = normalized_text
            for allowed in entry.allowed_exceptions:
                match_text = match_text.replace(normalize_for_match(allowed), "")
            if normalize_for_match(entry.term) in match_text:
                if cue.cue_id not in matched_ids[entry.term]:
                    matched_ids[entry.term].append(cue.cue_id)
        for term in legacy_terms:
            if normalize_for_match(term) in normalized_text and cue.cue_id not in matched_ids[term]:
                matched_ids[term].append(cue.cue_id)
    return [{"term": term, "cue_ids": cue_ids} for term, cue_ids in matched_ids.items() if cue_ids]


def _find_registry_candidates(cues: Iterable[Cue], entries: list[TermEntry], match_class: str) -> list[dict[str, object]]:
    matched_ids: dict[str, list[str]] = {
        entry.term: [] for entry in entries if entry.match_class == match_class
    }
    for cue in cues:
        normalized_text = normalize_for_match(cue.original_text)
        for entry in entries:
            if entry.match_class != match_class:
                continue
            if normalize_for_match(entry.term) in normalized_text and cue.cue_id not in matched_ids[entry.term]:
                matched_ids[entry.term].append(cue.cue_id)
    return [{"term": term, "cue_ids": cue_ids} for term, cue_ids in matched_ids.items() if cue_ids]


def _find_contextual_candidates(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    cue_list = list(cues)
    matched_ids: dict[str, list[str]] = {
        entry.term: [] for entry in entries if entry.match_class == "contextual"
    }
    for cue in cue_list:
        normalized_text = normalize_for_match(cue.original_text)
        for entry in entries:
            if entry.match_class != "contextual":
                continue
            if normalize_for_match(entry.term) in normalized_text:
                if cue.cue_id not in matched_ids[entry.term]:
                    matched_ids[entry.term].append(cue.cue_id)
    return [{"term": term, "cue_ids": cue_ids} for term, cue_ids in matched_ids.items() if cue_ids]


def _find_contextual_equivalent_hits(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    cue_list = list(cues)
    matched_ids: dict[tuple[str, str], list[str]] = {
        (entry.term, alias): []
        for entry in entries if entry.match_class == "contextual"
        for alias in entry.confirmed_equivalents
    }
    for cue in cue_list:
        normalized_text = normalize_for_match(cue.original_text)
        for term, alias in matched_ids:
            if normalize_for_match(alias) in normalized_text and cue.cue_id not in matched_ids[(term, alias)]:
                matched_ids[(term, alias)].append(cue.cue_id)
    return [
        {"term": term, "expression": alias, "cue_ids": cue_ids}
        for (term, alias), cue_ids in matched_ids.items() if cue_ids
    ]


def _classify_contextual_candidates(
    cues: Iterable[Cue], candidates: list[dict[str, object]]
) -> dict[str, list[dict[str, object]]]:
    cue_by_id = {cue.cue_id: cue for cue in cues}
    decisions: dict[str, dict[str, list[str]]] = {"block": {}, "allow": {}, "uncertain": {}}
    for candidate in candidates:
        term = str(candidate["term"])
        for cue_id_value in candidate["cue_ids"]:
            cue_id = str(cue_id_value)
            decision = classify_contextual_hit(cue_by_id[cue_id].original_text, term)
            decisions[decision].setdefault(term, []).append(cue_id)
    return {
        decision: [
            {"term": term, "cue_ids": list(dict.fromkeys(cue_ids))}
            for term, cue_ids in terms.items()
        ]
        for decision, terms in decisions.items()
    }


def _find_confirmed_equivalent_hits(cues: Iterable[Cue], entries: list[TermEntry]) -> list[dict[str, object]]:
    matched: dict[tuple[str, str], list[str]] = {}
    for entry in entries:
        if entry.match_class != "direct":
            continue
        for equivalent in entry.confirmed_equivalents:
            matched[(entry.term, equivalent)] = []
    for cue in cues:
        normalized_text = normalize_for_match(cue.original_text)
        for term, equivalent in matched:
            entry = next(item for item in entries if item.term == term)
            match_text = normalized_text
            for allowed in entry.allowed_exceptions:
                match_text = match_text.replace(normalize_for_match(allowed), "")
            if normalize_for_match(equivalent) in match_text and cue.cue_id not in matched[(term, equivalent)]:
                matched[(term, equivalent)].append(cue.cue_id)
    return [
        {"term": term, "expression": equivalent, "cue_ids": cue_ids}
        for (term, equivalent), cue_ids in matched.items()
        if cue_ids
    ]


def _decimal_string(value: Decimal) -> str:
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered or "0"


def _number_value(value: Decimal) -> int | str:
    if value == value.to_integral_value():
        return int(value)
    return _decimal_string(value)


def _format_timecode(milliseconds: Decimal | int) -> str:
    milliseconds = max(Decimal(milliseconds), Decimal(0))
    whole_milliseconds = int(milliseconds)
    submillisecond = milliseconds - whole_milliseconds
    seconds, millis = divmod(whole_milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    submillisecond_digits = _decimal_string(submillisecond).partition(".")[2]
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}{submillisecond_digits}"


def _escape_table_text(text: str) -> str:
    return text.replace("|", r"\|").replace("\r", r"\r").replace("\n", r"\n")


def _compact_parsed_ranges(source: SourceReport) -> list[dict[str, object]]:
    """Compress consecutive, successfully parsed cues without concealing gaps or bad blocks."""
    ranges: list[dict[str, object]] = []
    run: list[Cue] = []

    def flush() -> None:
        if not run:
            return
        first, last = run[0], run[-1]
        ranges.append({
            "start_line": first.line_start,
            "end_line": last.line_end,
            "cue_id_start": first.cue_id,
            "cue_id_end": last.cue_id,
            "cue_count": len(run),
        })
        run.clear()

    for cue in source.cues:
        if run:
            previous = run[-1]
            can_extend = (
                cue.source_order == previous.source_order + 1
                and cue.cue_number == previous.cue_number + 1
                and cue.line_start > previous.line_end
            )
            if not can_extend:
                flush()
        run.append(cue)
    flush()
    return ranges


def preprocess_text(
    text: str,
    formal_terms: Optional[Iterable[str]] = None,
    source_sha256: Optional[str] = None,
    compact: bool = False,
) -> dict[str, object]:
    """Return a lossless mechanical report, with an optional single-view compact schema."""
    source = parse_source(text, source_sha256=source_sha256)
    terms = list(formal_terms) if formal_terms is not None else load_term_registry()
    registry_entries = [entry for entry in terms if isinstance(entry, TermEntry)]
    direct_hits = find_direct_hits(source.cues, terms)
    equivalent_hits = _find_confirmed_equivalent_hits(source.cues, registry_entries)
    contextual_candidates = _find_contextual_candidates(source.cues, registry_entries)
    contextual_equivalent_hits = _find_contextual_equivalent_hits(source.cues, registry_entries)
    all_contextual_candidates = contextual_candidates + [
        {"term": hit["term"], "cue_ids": hit["cue_ids"]}
        for hit in contextual_equivalent_hits
    ]
    contextual_decisions = _classify_contextual_candidates(source.cues, all_contextual_candidates)
    asr_suspicions = find_asr_suspicions(
        [GuardCue(cue.cue_id, cue.original_text) for cue in source.cues], registry_entries
    )
    hit_ids = {cue_id for hit in direct_hits + equivalent_hits for cue_id in hit["cue_ids"]}
    hit_ids.update(cue_id for hit in contextual_decisions["block"] for cue_id in hit["cue_ids"])
    contextual_ids = {cue_id for hit in all_contextual_candidates for cue_id in hit["cue_ids"]}
    contextual_block_ids = {cue_id for hit in contextual_decisions["block"] for cue_id in hit["cue_ids"]}
    contextual_allow_ids = {cue_id for hit in contextual_decisions["allow"] for cue_id in hit["cue_ids"]}
    contextual_unresolved_ids = {cue_id for hit in contextual_decisions["uncertain"] for cue_id in hit["cue_ids"]}

    if compact:
        return {
            "format": "c2-preprocess-compact-v1",
            "source_type": source.source_type,
            "source_sha256": source.source_sha256,
            "source_map_sha256": source.source_map_sha256,
            "source_map": _source_map_records(source.cues),
            "status": source.status,
            "counts": {"parsed_blocks": len(source.cues), "total_blocks": source.total_blocks},
            "recognized_header_lines": source.recognized_header_lines,
            "parsed_ranges": _compact_parsed_ranges(source),
            "unparsed_ranges": source.unparsed_ranges,
            "diagnostics": source.diagnostics,
            "direct_hits": direct_hits,
            "confirmed_equivalent_hits": equivalent_hits,
            "contextual_candidates": contextual_candidates,
            "contextual_confirmed_equivalent_hits": contextual_equivalent_hits,
            "contextual_candidate_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_ids],
            "contextual_block_hits": contextual_decisions["block"],
            "contextual_allowed_hits": contextual_decisions["allow"],
            "contextual_unresolved_hits": contextual_decisions["uncertain"],
            "contextual_block_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_block_ids],
            "contextual_allow_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_allow_ids],
            "contextual_unresolved_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_unresolved_ids],
            "excluded_full_cue_ids": [cue.cue_id for cue in source.cues if cue.cue_id in hit_ids],
            "semantic_review_required": True,
            "contextual_review_required": bool(contextual_unresolved_ids or asr_suspicions),
            "asr_suspicions": asr_suspicions,
            "unresolved_expressions": contextual_decisions["uncertain"],
            "rows": [
                {
                    "id": cue.cue_id,
                    "source_order": cue.source_order,
                    "line_start": cue.line_start,
                    "line_end": cue.line_end,
                    "original_text": cue.original_text,
                    "start_ms_exact": _decimal_string(cue.start_ms) if cue.timeline_known else None,
                    "end_ms_exact": _decimal_string(cue.end_ms) if cue.timeline_known else None,
                    "duration_ms_exact": _decimal_string(cue.duration_ms),
                    "timeline_known": cue.timeline_known,
                    "mark": "HIT" if cue.cue_id in hit_ids else "",
                }
                for cue in source.cues
            ],
        }

    compact_table = []
    timeline_map = []
    previous: Optional[Cue] = None
    for cue in source.cues:
        compact_table.append({
            "id": cue.cue_id,
            "time_range": f"{_format_timecode(cue.start_ms)}-{_format_timecode(cue.end_ms)}" if cue.timeline_known else "位置未知",
            "duration_ms": _number_value(cue.duration_ms),
            "duration_ms_exact": _decimal_string(cue.duration_ms),
            "original_text": cue.original_text,
            "mark": "HIT" if cue.cue_id in hit_ids else "",
        })
        adjacent = previous is not None and cue.source_order == previous.source_order + 1
        timeline_known = cue.timeline_known and (previous is None or previous.timeline_known)
        gap = cue.start_ms - previous.end_ms if adjacent and source.source_type == "srt" and timeline_known else None
        timeline_map.append({
            "cue_id": cue.cue_id,
            "start_ms": _number_value(cue.start_ms) if cue.timeline_known else None,
            "end_ms": _number_value(cue.end_ms) if cue.timeline_known else None,
            "start_ms_exact": _decimal_string(cue.start_ms) if cue.timeline_known else None,
            "end_ms_exact": _decimal_string(cue.end_ms) if cue.timeline_known else None,
            "gap_from_previous_ms": _number_value(gap) if gap is not None else None,
            "timeline_known": cue.timeline_known,
            "line_start": cue.line_start,
            "line_end": cue.line_end,
        })
        previous = cue

    compact_lines = ["序号|起-止|原文"]
    compact_lines.extend(
        f"{row['id']}{' HIT' if row['mark'] == 'HIT' else ''}|{row['time_range']}|{_escape_table_text(row['original_text'])}"
        for row in compact_table
    )
    return {
        "source_type": source.source_type,
        "source_sha256": source.source_sha256,
        "source_map_sha256": source.source_map_sha256,
        "source_map": _source_map_records(source.cues),
        "status": source.status,
        "counts": {"parsed_blocks": len(source.cues), "total_blocks": source.total_blocks},
        "recognized_header_lines": source.recognized_header_lines,
        "parsed_ranges": source.parsed_ranges,
        "unparsed_ranges": source.unparsed_ranges,
        "diagnostics": source.diagnostics,
        "cues": [cue.to_dict() for cue in source.cues],
        "direct_hits": direct_hits,
        "confirmed_equivalent_hits": equivalent_hits,
        "contextual_candidates": contextual_candidates,
        "contextual_confirmed_equivalent_hits": contextual_equivalent_hits,
        "contextual_candidate_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_ids],
        "contextual_block_hits": contextual_decisions["block"],
        "contextual_allowed_hits": contextual_decisions["allow"],
        "contextual_unresolved_hits": contextual_decisions["uncertain"],
        "contextual_block_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_block_ids],
        "contextual_allow_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_allow_ids],
        "contextual_unresolved_ids": [cue.cue_id for cue in source.cues if cue.cue_id in contextual_unresolved_ids],
        "excluded_full_cue_ids": [cue.cue_id for cue in source.cues if cue.cue_id in hit_ids | contextual_block_ids],
        "semantic_review_required": True,
        "contextual_review_required": bool(contextual_unresolved_ids or asr_suspicions),
        "asr_suspicions": asr_suspicions,
        "unresolved_expressions": contextual_decisions["uncertain"],
        "compact_table": compact_table,
        "compact_table_text": "\n".join(compact_lines),
        "timeline_map": timeline_map,
        "window_map_support": {
            "semantic_product_assignment": "AI_REQUIRED",
            "items": timeline_map,
        },
    }


def preprocess_file(path: Path, compact: bool = False) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    report = preprocess_text(text, source_sha256=hashlib.sha256(raw).hexdigest(), compact=compact)
    report["source_file"] = path.name
    return report


VALID_ROLES = {"独立卖点", "证据", "条件", "必要衔接", "适用促单原话"}
VALID_FLAG_TYPES = {"fact_pending", "risk_hint", "key_limit"}
VALID_DYNAMIC_TRANSACTION_ITEMS = {
    "成交价", "优惠", "赠品", "直播福利", "倒计时", "库存/稀缺", "其他实时交易信息"
}


def _failure(code: str, message: str, **details: object) -> dict[str, object]:
    return {"code": code, "message": message, **details}


def _source_index(source: SourceReport) -> dict[str, Cue]:
    return {cue.cue_id: cue for cue in source.cues}


def validate_selection(
    source: SourceReport,
    selection: dict[str, object],
    formal_terms: Optional[Iterable[str]] = None,
    final_text: Optional[str] = None,
) -> dict[str, object]:
    """Check selection structure and formal direct hits without judging semantics."""
    mode = selection.get("verification_mode")
    label = "脚本核验" if mode == "script" else "模型逐条对照" if mode == "manual" else "未声明核验方式"
    failures: list[dict[str, object]] = []
    status = "BLOCKED" if source.status == "BLOCKED" else "PASS"
    blocked_refs: list[dict[str, object]] = []

    if source.status in {"FAIL", "BLOCKED"}:
        failures.extend(
            _failure(str(item["code"]), str(item["reason"]), cue_ids=item.get("cue_ids", []))
            for item in source.diagnostics
        )

    if mode not in {"script", "manual"}:
        failures.append(_failure("invalid_verification_mode", "verification_mode must be script or manual"))

    playback_speed = selection.get("full_clip_playback_speed", float(FULL_CLIP_SPEED))
    if playback_speed != float(FULL_CLIP_SPEED):
        failures.append(_failure(
            "invalid_full_clip_playback_speed",
            "full_clip_playback_speed must be 1.2 for the whole clip",
        ))

    selected_raw = selection.get("selected_ids", [])
    selected_ids = [str(item) for item in selected_raw] if isinstance(selected_raw, list) else []
    if not isinstance(selected_raw, list):
        failures.append(_failure("selected_ids_not_list", "selected_ids must be a list"))
    selected_set = set(selected_ids)
    if not selected_ids:
        failures.append(_failure("empty_selection", "at least one cue must be selected"))
    if len(selected_ids) != len(selected_set):
        failures.append(_failure("duplicate_selected_id", "selected cue IDs must not repeat"))

    source_by_id = _source_index(source)
    source_ids = set(source_by_id)
    for cue_id in selected_ids:
        if cue_id not in source_ids:
            if source.status == "BLOCKED":
                blocked_refs.append({"code": "selected_id_in_unparsed_scope", "cue_id": cue_id})
            else:
                failures.append(_failure("selected_id_not_in_source", "selected cue ID is absent from source", cue_id=cue_id))

    declared_hash = selection.get("source_sha256")
    if not source.source_sha256 or declared_hash != source.source_sha256:
        failures.append(_failure("source_hash_mismatch", "selection source_sha256 does not match the parsed source"))

    points = selection.get("selling_points", [])
    if not isinstance(points, list):
        failures.append(_failure("selling_points_not_list", "selling_points must be a list"))
        points = []
    point_ids: set[str] = set()
    support_ids_seen: set[str] = set()
    for point in points:
        if not isinstance(point, dict):
            failures.append(_failure("selling_point_not_object", "each selling point must be an object"))
            continue
        point_id = str(point.get("id", ""))
        if not point_id:
            failures.append(_failure("selling_point_id_missing", "each selling point must have an ID"))
        elif point_id in point_ids:
            failures.append(_failure("duplicate_selling_point_id", "selling point IDs must be unique", point_id=point_id))
        point_ids.add(point_id)
        supports = point.get("support_ids", [])
        if not isinstance(supports, list) or not supports:
            failures.append(_failure("selling_point_without_support", "each selling point needs at least one support cue", point_id=point_id))
            supports = []
        for field_name in ("support_ids", "necessary_evidence_ids", "required_condition_ids"):
            refs = point.get(field_name, [])
            if not isinstance(refs, list):
                failures.append(_failure("point_refs_not_list", f"{field_name} must be a list", point_id=point_id))
                continue
            for raw_id in refs:
                cue_id = str(raw_id)
                support_ids_seen.add(cue_id)
                if cue_id not in source_ids:
                    if source.status == "BLOCKED":
                        blocked_refs.append({"code": "point_reference_in_unparsed_scope", "point_id": point_id, "cue_id": cue_id, "field": field_name})
                    else:
                        failures.append(_failure("support_id_not_in_source", "selling point reference is absent from source", point_id=point_id, cue_id=cue_id, field=field_name))
                elif cue_id not in selected_set:
                    failures.append(_failure("support_id_not_selected", "selling point reference is not selected", point_id=point_id, cue_id=cue_id, field=field_name))

    role_rows = selection.get("roles", [])
    if not isinstance(role_rows, list):
        failures.append(_failure("roles_not_list", "roles must be a list"))
        role_rows = []
    role_counts: dict[str, int] = {}
    role_by_id: dict[str, object] = {}
    promotion_ids: set[str] = set()
    for role_row in role_rows:
        if not isinstance(role_row, dict):
            failures.append(_failure("role_not_object", "each role row must be an object"))
            continue
        cue_id = str(role_row.get("cue_id", ""))
        role = role_row.get("role")
        role_counts[cue_id] = role_counts.get(cue_id, 0) + 1
        role_by_id[cue_id] = role
        if cue_id not in source_ids:
            if source.status == "BLOCKED":
                blocked_refs.append({"code": "role_reference_in_unparsed_scope", "cue_id": cue_id})
            else:
                failures.append(_failure("role_id_not_in_source", "role cue ID is absent from source", cue_id=cue_id))
        if cue_id not in selected_set:
            failures.append(_failure("role_id_not_selected", "role cue ID is not selected", cue_id=cue_id))
        if role not in VALID_ROLES:
            failures.append(_failure("invalid_role", "role is not one of the five allowed roles", cue_id=cue_id, role=role))
        if role == "适用促单原话":
            promotion_ids.add(cue_id)

        transaction_info = role_row.get("transaction_info")
        if transaction_info is not None:
            if not isinstance(transaction_info, dict) or set(transaction_info) != {"dynamic_items", "sku_list_price_verified"}:
                failures.append(_failure("invalid_transaction_info", "transaction_info needs dynamic_items and sku_list_price_verified", cue_id=cue_id))
                continue
            dynamic_items = transaction_info.get("dynamic_items")
            verified_price = transaction_info.get("sku_list_price_verified")
            if not isinstance(dynamic_items, list) or any(item not in VALID_DYNAMIC_TRANSACTION_ITEMS for item in dynamic_items):
                failures.append(_failure("invalid_dynamic_transaction_info", "dynamic transaction information must use the supported list", cue_id=cue_id))
                continue
            if not isinstance(verified_price, bool):
                failures.append(_failure("invalid_sku_price_verification", "sku_list_price_verified must be a boolean", cue_id=cue_id))
                continue
            if role == "适用促单原话" and (dynamic_items or verified_price):
                failures.append(_failure("promotion_contains_dynamic_transaction_info", "closing promotion must omit every dynamic transaction item and every price", cue_id=cue_id, items=dynamic_items, verified_sku_price=verified_price))
            elif role != "适用促单原话" and dynamic_items:
                failures.append(_failure("selected_dynamic_transaction_info", "selected body cues may only retain a separately verified current-SKU list price", cue_id=cue_id, items=dynamic_items))
        elif role == "适用促单原话":
            failures.append(_failure("promotion_transaction_info_required", "promotion cues need an explicit empty dynamic-information check", cue_id=cue_id))

    for cue_id in selected_ids:
        if role_counts.get(cue_id, 0) != 1:
            failures.append(_failure("role_cardinality", "each selected cue must have exactly one role", cue_id=cue_id, count=role_counts.get(cue_id, 0)))

    for cue_id in support_ids_seen & promotion_ids:
        failures.append(_failure("promotion_in_selling_point_support", "promotion cues cannot support or rank a selling point", cue_id=cue_id))

    raw_blocks = selection.get("content_blocks")
    content_blocks: list[dict[str, object]] = []
    content_block_ids: set[str] = set()
    flattened_block_cues: list[str] = []
    if not isinstance(raw_blocks, list) or not raw_blocks:
        failures.append(_failure("content_blocks_required", "content_blocks must describe this cut's ordered boards"))
        raw_blocks = []
    for index, block in enumerate(raw_blocks):
        if not isinstance(block, dict):
            failures.append(_failure("invalid_content_block", "each content block must be an object", index=index))
            continue
        block_id = str(block.get("id", ""))
        name = str(block.get("name", ""))
        cue_ids = block.get("cue_ids")
        if not block_id or not name or not isinstance(cue_ids, list) or not cue_ids:
            failures.append(_failure("invalid_content_block", "each content block needs an ID, open name, and non-empty cue_ids", index=index))
            continue
        if block_id in content_block_ids:
            failures.append(_failure("duplicate_content_block_id", "a content block must remain one contiguous group", block_id=block_id))
        content_block_ids.add(block_id)
        normalized_cue_ids = [str(cue_id) for cue_id in cue_ids]
        flattened_block_cues.extend(normalized_cue_ids)
        content_blocks.append({"id": block_id, "name": name, "cue_ids": normalized_cue_ids})
        if any(cue_id not in selected_set for cue_id in normalized_cue_ids):
            failures.append(_failure("content_block_cue_not_selected", "content blocks may contain only cues in this cut", block_id=block_id))
    if flattened_block_cues != selected_ids:
        failures.append(_failure("content_blocks_do_not_match_selected_order", "selected cue playback order must follow complete, non-interleaved content blocks"))
    if promotion_ids:
        final_block_cues = set(content_blocks[-1]["cue_ids"]) if content_blocks else set()
        if not promotion_ids <= final_block_cues:
            failures.append(_failure("promotion_not_in_last_block", "all applicable promotion cues must be in the last block"))
        if selected_ids and selected_ids[-1] not in promotion_ids:
            failures.append(_failure("promotion_not_at_end", "the final selected cue must preserve the closing promotion"))

    duration_review = selection.get("duration_review")
    estimated_duration = selection.get("estimated_duration_seconds")
    if estimated_duration is not None and (
        isinstance(estimated_duration, bool)
        or not isinstance(estimated_duration, (int, float))
        or not Decimal(str(estimated_duration)).is_finite()
        or estimated_duration < 0
    ):
        failures.append(_failure("invalid_estimated_duration", "estimated duration must be a finite nonnegative number"))
    if duration_review is None and source.status == "PASS" and selected_set <= source_ids:
        groups = _selected_groups([source_by_id[cue_id] for cue_id in selected_ids], source.source_type)
        if _source_duration_ms(groups) > 100_000 * FULL_CLIP_SPEED:
            failures.append(_failure("duration_review_required", "a cut above the 100-second reference needs an individual review record"))

    omitted_block_ids: list[str] = []
    if duration_review is not None:
        if not isinstance(duration_review, dict) or set(duration_review) != {"outcome", "review_reason", "omitted_blocks"}:
            failures.append(_failure("invalid_duration_review", "duration_review needs outcome, review_reason, and omitted_blocks"))
        else:
            outcome = duration_review.get("outcome")
            review_reason = duration_review.get("review_reason")
            omitted_blocks = duration_review.get("omitted_blocks")
            if outcome not in {"retain_all", "omit_low_value_blocks"} or not isinstance(review_reason, str) or not review_reason.strip() or not isinstance(omitted_blocks, list):
                failures.append(_failure("invalid_duration_review", "duration review needs a supported outcome, reason, and omitted-block list"))
                omitted_blocks = []
            if outcome == "retain_all" and omitted_blocks:
                failures.append(_failure("duration_review_outcome_mismatch", "retain_all cannot list omitted blocks"))
            if outcome == "omit_low_value_blocks" and not omitted_blocks:
                failures.append(_failure("duration_review_omissions_missing", "omitting low-value content requires complete-block records"))
            for index, omitted in enumerate(omitted_blocks):
                if not isinstance(omitted, dict) or set(omitted) != {"id", "name", "cue_ids", "selling_point_ids", "reason"}:
                    failures.append(_failure("invalid_omitted_block", "each omission needs its block, source cues, selling points, and reason", index=index))
                    continue
                block_id = str(omitted.get("id", ""))
                cue_ids = omitted.get("cue_ids")
                point_refs = omitted.get("selling_point_ids")
                if not block_id or not str(omitted.get("name", "")).strip() or not isinstance(cue_ids, list) or not cue_ids or not isinstance(point_refs, list) or not str(omitted.get("reason", "")).strip():
                    failures.append(_failure("invalid_omitted_block", "omitted blocks need source cues, linked points, and an individual reason", index=index))
                    continue
                omitted_block_ids.append(block_id)
                if block_id in content_block_ids or any(str(cue_id) in selected_set for cue_id in cue_ids):
                    failures.append(_failure("omitted_block_is_selected", "an omitted board must remain absent as a whole", block_id=block_id))
                if any(str(cue_id) not in source_ids for cue_id in cue_ids):
                    failures.append(_failure("omitted_block_cue_not_in_source", "omitted board cues must trace to the source", block_id=block_id))
                if any(str(point_id) not in point_ids for point_id in point_refs):
                    failures.append(_failure("omitted_block_point_not_in_pool", "omitted board points must be recorded in the information pool", block_id=block_id))

    terms = list(formal_terms) if formal_terms is not None else load_term_registry()
    registry_entries = [entry for entry in terms if isinstance(entry, TermEntry)]
    direct_hits = find_direct_hits(source.cues, terms)
    equivalent_hits = _find_confirmed_equivalent_hits(source.cues, registry_entries)
    contextual_candidates = _find_contextual_candidates(source.cues, registry_entries)
    contextual_equivalent_hits = _find_contextual_equivalent_hits(source.cues, registry_entries)
    all_contextual_candidates = contextual_candidates + [
        {"term": hit["term"], "cue_ids": hit["cue_ids"]}
        for hit in contextual_equivalent_hits
    ]
    contextual_decisions = _classify_contextual_candidates(source.cues, all_contextual_candidates)
    asr_suspicions = find_asr_suspicions(
        [GuardCue(cue.cue_id, cue.original_text) for cue in source.cues], registry_entries
    )
    hard_hit_ids = {
        str(cue_id)
        for hit in direct_hits + equivalent_hits
        for cue_id in hit["cue_ids"]
    }
    contextual_ids = {
        str(cue_id)
        for hit in all_contextual_candidates
        for cue_id in hit["cue_ids"]
    }
    contextual_block_ids = {
        str(cue_id)
        for hit in contextual_decisions["block"]
        for cue_id in hit["cue_ids"]
    }
    contextual_unresolved_ids = {
        str(cue_id)
        for hit in contextual_decisions["uncertain"]
        for cue_id in hit["cue_ids"]
    }
    for cue_id in selected_ids:
        if cue_id in hard_hit_ids:
            failures.append(_failure("selected_direct_formal_term", "selected cue contains a direct formal prohibited-term hit", cue_id=cue_id))
        if cue_id in contextual_block_ids:
            failures.append(_failure("selected_contextual_absolute_claim", "selected cue contains a confirmed contextual absolute product claim", cue_id=cue_id))
    final_text_hits = find_direct_hits([Cue("final_text", -1, -1, 0, 0, final_text, 0, 0, 0)], terms) if final_text is not None else []
    final_equivalent_hits = _find_confirmed_equivalent_hits([Cue("final_text", -1, -1, 0, 0, final_text, 0, 0, 0)], registry_entries) if final_text is not None else []
    final_cue = [Cue("final_text", -1, -1, 0, 0, final_text, 0, 0, 0)] if final_text is not None else []
    final_contextual_candidates = _find_contextual_candidates(final_cue, registry_entries)
    final_contextual_equivalent_hits = _find_contextual_equivalent_hits(final_cue, registry_entries)
    all_final_contextual_candidates = final_contextual_candidates + [
        {"term": hit["term"], "cue_ids": hit["cue_ids"]}
        for hit in final_contextual_equivalent_hits
    ]
    final_contextual_decisions = _classify_contextual_candidates(final_cue, all_final_contextual_candidates)
    final_asr_suspicions = find_asr_suspicions(
        [GuardCue(cue.cue_id, cue.original_text) for cue in final_cue], registry_entries
    )
    if final_text_hits or final_equivalent_hits:
        failures.append(_failure("final_text_direct_formal_term", "final text contains a direct formal prohibited-term hit or confirmed equivalent", direct_hits=final_text_hits, confirmed_equivalent_hits=final_equivalent_hits))
    if final_contextual_decisions["block"]:
        failures.append(_failure("final_text_contextual_absolute_claim", "final text contains a confirmed contextual absolute product claim", contextual_hits=final_contextual_decisions["block"]))

    raw_flags = selection.get("flags")
    flags = raw_flags if isinstance(raw_flags, list) else []
    if "flags" not in selection:
        failures.append(_failure("flags_missing", "flags is required, even when empty"))
    elif not isinstance(raw_flags, list):
        failures.append(_failure("flags_not_list", "flags must be a list"))
    valid_flags = []
    for index, flag in enumerate(flags):
        if not isinstance(flag, dict):
            failures.append(_failure("invalid_flag_structure", "each flag must be an object", index=index))
            continue
        has_valid_shape = (
            set(flag) == {"type", "cue_ids", "note"}
            and isinstance(flag.get("cue_ids"), list)
            and all(isinstance(cue_id, str) for cue_id in flag.get("cue_ids", []))
            and isinstance(flag.get("note"), str)
        )
        if not has_valid_shape:
            failures.append(_failure("invalid_flag_structure", "flag must contain only type, cue_ids (string array), and note (string)", index=index))
            continue
        if flag.get("type") not in VALID_FLAG_TYPES:
            failures.append(_failure("invalid_flag_type", "flag type must be fact_pending, risk_hint, or key_limit", index=index, flag_type=flag.get("type")))
            continue
        valid_flags.append(flag)
    risk_hints = [flag for flag in valid_flags if flag.get("type") == "risk_hint"]
    passthrough_flags = raw_flags

    if failures and status != "BLOCKED":
        status = "FAIL"
    return {
        "status": status,
        "internal_status": status,
        "verification_mode": mode,
        "verification_label": label,
        "machine_gate_status": status if mode == "script" else None,
        "hard_failures": failures,
        "blocked_references": blocked_refs,
        "risk_hints": risk_hints,
        "flags": passthrough_flags,
        "source_sha256": source.source_sha256,
        "parsed_ranges": source.parsed_ranges,
        "unparsed_ranges": source.unparsed_ranges,
        "selected_ids": selected_ids,
        "selling_point_ids": sorted(point_ids),
        "support_ids": sorted(support_ids_seen),
        "promotion_ids": sorted(promotion_ids),
        "content_blocks": content_blocks,
        "duration_review": duration_review,
        "omitted_block_ids": omitted_block_ids,
        "direct_hits": direct_hits,
        "confirmed_equivalent_hits": equivalent_hits,
        "contextual_candidates": contextual_candidates,
        "contextual_confirmed_equivalent_hits": contextual_equivalent_hits,
        "contextual_block_hits": contextual_decisions["block"],
        "contextual_allowed_hits": contextual_decisions["allow"],
        "contextual_unresolved_hits": contextual_decisions["uncertain"],
        "selected_contextual_candidate_ids": [cue_id for cue_id in selected_ids if cue_id in contextual_ids],
        "selected_contextual_hit_ids": [cue_id for cue_id in selected_ids if cue_id in contextual_block_ids],
        "final_text_hits": final_text_hits,
        "final_confirmed_equivalent_hits": final_equivalent_hits,
        "final_contextual_candidates": final_contextual_candidates,
        "final_contextual_confirmed_equivalent_hits": final_contextual_equivalent_hits,
        "final_contextual_block_hits": final_contextual_decisions["block"],
        "final_contextual_allowed_hits": final_contextual_decisions["allow"],
        "final_contextual_unresolved_hits": final_contextual_decisions["uncertain"],
        "semantic_review_required": True,
        "contextual_review_required": bool(
            any(cue_id in contextual_unresolved_ids for cue_id in selected_ids)
            or final_contextual_decisions["uncertain"]
            or any(item["cue_id"] in selected_set for item in asr_suspicions)
            or final_asr_suspicions
        ),
        "asr_suspicions": asr_suspicions,
        "final_asr_suspicions": final_asr_suspicions,
        "unresolved_expressions": contextual_decisions["uncertain"],
        "final_unresolved_expressions": final_contextual_decisions["uncertain"],
        "analysis_started": True,
        "full_source_checked": source.status != "BLOCKED",
    }


def _display_duration(milliseconds: int | Decimal) -> str:
    """Show only a coarse estimate; source timings are not exported-video timings."""
    seconds = Decimal(str(max(milliseconds, 0))) / Decimal(1000)
    if seconds < 1:
        return "\u7ea6 1 \u79d2\u5185"
    rounded_seconds = int(seconds.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return f"\u7ea6 {rounded_seconds} \u79d2"


def _selected_groups(cues: list[Cue], source_type: str) -> list[dict[str, object]]:
    if not cues:
        return []
    groups: list[list[Cue]] = [[cues[0]]]
    for cue in cues[1:]:
        previous = groups[-1][-1]
        if cue.source_order == previous.source_order + 1:
            groups[-1].append(cue)
        else:
            groups.append([cue])
    result: list[dict[str, object]] = []
    for group in groups:
        duration = sum((cue.duration_ms for cue in group), Decimal(0)) if source_type == "duration_text" else group[-1].end_ms - group[0].start_ms
        result.append({
            "cue_ids": [cue.cue_id for cue in group],
            "start_ms": _number_value(group[0].start_ms) if group[0].timeline_known else None,
            "end_ms": _number_value(group[-1].end_ms) if group[-1].timeline_known else None,
            "span_ms": _number_value(duration),
            "span_ms_exact": _decimal_string(duration),
        })
    return result


def _source_duration_ms(groups: list[dict[str, object]]) -> Decimal:
    return sum((Decimal(str(group["span_ms_exact"])) for group in groups), Decimal(0))


def assemble_selection(
    source: SourceReport,
    selection: dict[str, object],
    formal_terms: Optional[Iterable[str]] = None,
) -> dict[str, object]:
    """Deterministically assemble original cue text, sequence, and shared duration values."""
    validation = validate_selection(source, selection, formal_terms=formal_terms)
    if validation["status"] != "PASS":
        return {"status": validation["status"], "validation": validation, "assembled": False}

    selected_ids = [str(item) for item in selection["selected_ids"]]
    by_id = _source_index(source)
    cues = [by_id[cue_id] for cue_id in selected_ids]
    groups = _selected_groups(cues, source.source_type)
    source_duration_exact = _source_duration_ms(groups)
    source_duration_ms = _number_value(source_duration_exact)
    playback_ms_exact = source_duration_exact / FULL_CLIP_SPEED
    playback_ms = int(playback_ms_exact.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    known_unaccelerated_ms = selection.get("known_unaccelerated_ms", 0)
    if isinstance(known_unaccelerated_ms, bool) or not isinstance(known_unaccelerated_ms, int) or known_unaccelerated_ms < 0:
        return {
            "status": "FAIL",
            "validation": {
                **validation,
                "status": "FAIL",
                "internal_status": "FAIL",
                "machine_gate_status": "FAIL" if selection.get("verification_mode") == "script" else None,
                "hard_failures": validation["hard_failures"] + [_failure("invalid_known_unaccelerated_ms", "known_unaccelerated_ms must be a nonnegative integer")],
            },
            "assembled": False,
        }
    display = _display_duration(playback_ms)
    return {
        "status": "PASS",
        "validation": validation,
        "assembled": True,
        "source_sha256": source.source_sha256,
        "source_map_sha256": source.source_map_sha256,
        "source_sequence": ",".join(selected_ids),
        "fifth_part_sequence": ",".join(selected_ids),
        "selected_ids": selected_ids,
        "segments": [
            {
                "cue_id": cue.cue_id,
                "source_order": cue.source_order,
                "original_text": cue.original_text,
                "duration_ms_exact": _decimal_string(cue.duration_ms),
            }
            for cue in cues
        ],
        "content_blocks": [
            {
                "id": block["id"],
                "name": block["name"],
                "cue_ids": block["cue_ids"],
                "text": "\n".join(by_id[str(cue_id)].original_text for cue_id in block["cue_ids"]),
            }
            for block in validation["content_blocks"]
        ],
        "body_text": "\n".join(cue.original_text for cue in cues),
        "source_groups": groups,
        "source_duration_ms": source_duration_ms,
        "source_duration_ms_exact": _decimal_string(source_duration_exact),
        "accelerated_duration_ms": playback_ms,
        "known_unaccelerated_ms": known_unaccelerated_ms,
        "playback_duration_ms": playback_ms,
        "full_clip_playback_speed": float(FULL_CLIP_SPEED),
        "source_duration_display": _display_duration(source_duration_exact),
        "playback_duration_display": display,
        "shared_duration_field": "playback_duration_display",
    }


def verify_final_output(
    source: SourceReport,
    selection: dict[str, object],
    assembly: dict[str, object],
    final_text: str,
    final_sequence: str,
    formal_terms: Optional[Iterable[str]] = None,
) -> dict[str, object]:
    """Release-test gate binding final clip text and fifth-part IDs to immutable source cues."""
    failures: list[dict[str, object]] = []
    if not isinstance(source.cues, tuple):
        failures.append(_failure("source_map_not_immutable", "parsed source cue mapping is not frozen"))
    actual_map_hash = _source_map_digest(source.cues)
    if not source.source_map_sha256 or actual_map_hash != source.source_map_sha256:
        failures.append(_failure("source_map_hash_mismatch", "original cue ID/text/duration map changed after parsing"))

    validation = validate_selection(source, selection, formal_terms=formal_terms)
    if validation["status"] != "PASS":
        failures.extend(validation["hard_failures"])
    if assembly.get("status") != "PASS" or assembly.get("assembled") is not True:
        failures.append(_failure("assembly_not_passed", "final output must be based on a passing assembly"))

    selected_ids = [str(item) for item in selection.get("selected_ids", [])] if isinstance(selection.get("selected_ids"), list) else []
    by_id = _source_index(source)
    expected_segments = [
        {
            "cue_id": cue_id,
            "source_order": by_id[cue_id].source_order,
            "original_text": by_id[cue_id].original_text,
            "duration_ms_exact": _decimal_string(by_id[cue_id].duration_ms),
        }
        for cue_id in selected_ids
        if cue_id in by_id
    ]
    expected_sequence = ",".join(selected_ids)
    expected_text = "\n".join(str(item["original_text"]) for item in expected_segments)

    if len(expected_segments) != len(selected_ids):
        failures.append(_failure("selected_source_mapping_missing", "one or more selected cue IDs have no source mapping"))
    if assembly.get("source_sha256") != source.source_sha256:
        failures.append(_failure("assembly_source_hash_mismatch", "assembly does not match the current source file"))
    if assembly.get("source_map_sha256") != source.source_map_sha256:
        failures.append(_failure("assembly_source_map_mismatch", "assembly does not match the immutable source cue mapping"))
    if assembly.get("selected_ids") != selected_ids or assembly.get("segments") != expected_segments:
        failures.append(_failure("assembled_line_mismatch", "assembled lines differ from selected source IDs/text/durations"))
    if assembly.get("body_text") != expected_text or final_text != expected_text:
        failures.append(_failure("final_text_source_mismatch", "final clip text is not an exact playback-order rendering of source cues"))
    if assembly.get("source_sequence") != expected_sequence or assembly.get("fifth_part_sequence") != expected_sequence:
        failures.append(_failure("assembly_sequence_mismatch", "assembly sequences do not match selected source cue IDs"))
    if final_sequence != expected_sequence:
        failures.append(_failure("final_sequence_source_mismatch", "fifth-part sequence differs from selected source cue IDs"))

    return {
        "status": "FAIL" if failures else "PASS",
        "hard_failures": failures,
        "source_sha256": source.source_sha256,
        "source_map_sha256": source.source_map_sha256,
        "expected_sequence": expected_sequence,
        "verified_sequence": final_sequence,
        "verified_line_count": len(expected_segments),
    }


def support_diff(first: dict[str, object], second: dict[str, object]) -> dict[str, object]:
    """Compare two semantic passes without requiring the candidate angle or sequence to match."""
    first_hash = first.get("source_sha256")
    second_hash = second.get("source_sha256")
    same_source = bool(first_hash) and first_hash == second_hash
    first_selected = [str(item) for item in first.get("selected_ids", [])]
    second_selected = [str(item) for item in second.get("selected_ids", [])]
    first_point_rows = first.get("selling_points", [])
    second_point_rows = second.get("selling_points", [])
    first_points = {str(point.get("id")): point for point in first_point_rows if isinstance(point, dict)} if isinstance(first_point_rows, list) else {}
    second_points = {str(point.get("id")): point for point in second_point_rows if isinstance(point, dict)} if isinstance(second_point_rows, list) else {}

    def cue_id_changes(field_name: str) -> list[dict[str, object]]:
        result = []
        for point_id in sorted(set(first_points) | set(second_points)):
            before_rows = first_points.get(point_id, {}).get(field_name, [])
            after_rows = second_points.get(point_id, {}).get(field_name, [])
            before = [str(item) for item in before_rows] if isinstance(before_rows, list) else []
            after = [str(item) for item in after_rows] if isinstance(after_rows, list) else []
            before_set = set(before)
            after_set = set(after)
            added = [item for item in after if item not in before_set]
            removed = [item for item in before if item not in after_set]
            if added or removed:
                result.append({"point_id": point_id, "added_ids": added, "removed_ids": removed})
        return result

    first_role_rows = first.get("roles", [])
    second_role_rows = second.get("roles", [])
    first_roles = {str(row.get("cue_id")): row.get("role") for row in first_role_rows if isinstance(row, dict)} if isinstance(first_role_rows, list) else {}
    second_roles = {str(row.get("cue_id")): row.get("role") for row in second_role_rows if isinstance(row, dict)} if isinstance(second_role_rows, list) else {}
    role_changes = [
        {"cue_id": cue_id, "first": first_roles.get(cue_id), "second": second_roles.get(cue_id)}
        for cue_id in sorted(set(first_roles) | set(second_roles))
        if first_roles.get(cue_id) != second_roles.get(cue_id)
    ]

    first_flags = first.get("flags", []) if isinstance(first.get("flags", []), list) else []
    second_flags = second.get("flags", []) if isinstance(second.get("flags", []), list) else []
    first_flag_keys = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in first_flags}
    second_flag_keys = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in second_flags}
    flags_added = [item for item in second_flags if json.dumps(item, ensure_ascii=False, sort_keys=True) not in first_flag_keys]
    flags_removed = [item for item in first_flags if json.dumps(item, ensure_ascii=False, sort_keys=True) not in second_flag_keys]
    first_rules = first.get("hard_rule_outcomes")
    second_rules = second.get("hard_rule_outcomes")
    both_have_rule_outcomes = isinstance(first_rules, list) and isinstance(second_rules, list)

    def rule_outcomes(rows: object) -> dict[str, dict[str, object]]:
        if not isinstance(rows, list):
            return {}
        outcomes = {}
        for row in rows:
            if isinstance(row, dict) and row.get("rule_id") is not None:
                outcomes[str(row["rule_id"])] = {
                    "status": row.get("status"),
                    "cue_ids": sorted(str(item) for item in row.get("cue_ids", [])),
                }
        return outcomes

    first_rule_map = rule_outcomes(first_rules)
    second_rule_map = rule_outcomes(second_rules)
    has_rule_outcomes = bool(first_rule_map or second_rule_map)
    hard_rule_outcomes_stable = first_rule_map == second_rule_map if both_have_rule_outcomes and has_rule_outcomes else None
    hard_rule_changes = [
        {"rule_id": rule_id, "first": first_rule_map.get(rule_id), "second": second_rule_map.get(rule_id)}
        for rule_id in sorted(set(first_rule_map) | set(second_rule_map))
        if first_rule_map.get(rule_id) != second_rule_map.get(rule_id)
    ]
    return {
        "status": "PASS" if same_source else "BLOCKED",
        "same_source": same_source,
        "source_sha256": first_hash if same_source else None,
        "support_changes": cue_id_changes("support_ids"),
        "evidence_changes": cue_id_changes("necessary_evidence_ids"),
        "condition_changes": cue_id_changes("required_condition_ids"),
        "point_pool_added_ids": [point_id for point_id in second_points if point_id not in first_points],
        "point_pool_removed_ids": [point_id for point_id in first_points if point_id not in second_points],
        "role_changes": role_changes,
        "flags_added": flags_added,
        "flags_removed": flags_removed,
        "hard_rule_outcomes_stable": hard_rule_outcomes_stable,
        "hard_rule_outcomes": [first_rules, second_rules],
        "hard_rule_changes": hard_rule_changes,
        "selected_sequences": [first_selected, second_selected],
        "sequence_order_changed": first_selected != second_selected,
        "selected_added_ids": [item for item in second_selected if item not in set(first_selected)],
        "selected_removed_ids": [item for item in first_selected if item not in set(second_selected)],
        "opening_choices": [first.get("opening_choice"), second.get("opening_choice")],
        "semantic_review_required": True,
    }


def _write_report(report: dict[str, object], output: Optional[Path], compact_json: bool = False) -> None:
    rendered = (
        json.dumps(report, ensure_ascii=False, separators=(",", ":"))
        if compact_json else json.dumps(report, ensure_ascii=False, indent=2)
    )
    if output:
        output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def _load_source(path: Path) -> SourceReport:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    return parse_source(text, source_sha256=hashlib.sha256(raw).hexdigest())


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _exit_code(status: object) -> int:
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 2}.get(str(status), 3)


def main(argv: Optional[list[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    preprocess = commands.add_parser("preprocess", help="parse and report an SRT or numbered duration-text source")
    preprocess.add_argument("source", type=Path)
    preprocess.add_argument("--output", type=Path, help="optional JSON report path")
    preprocess.add_argument("--compact", action="store_true", help="emit one lossless row per cue and compact JSON without duplicate table/timeline views")
    for name, help_text in (
        ("assemble", "validate and assemble a selection from original source cues"),
        ("check", "run the structural and formal-term gate for a selection"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("source", type=Path)
        command.add_argument("selection", type=Path)
        command.add_argument("--final-text", type=Path, help="optional file containing title/hashtags or final copy")
        command.add_argument("--output", type=Path, help="optional JSON report path")
    diff = commands.add_parser("diff", help="compare semantic-pass selection support maps")
    diff.add_argument("first", type=Path)
    diff.add_argument("second", type=Path)
    diff.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args(argv)
    try:
        if args.command == "preprocess":
            report = preprocess_file(args.source, compact=args.compact)
        elif args.command in {"assemble", "check"}:
            source = _load_source(args.source)
            selection = _load_json(args.selection)
            final_text = args.final_text.read_text(encoding="utf-8-sig") if args.final_text else None
            if args.command == "assemble":
                report = assemble_selection(source, selection)
            else:
                report = validate_selection(source, selection, final_text=final_text)
        elif args.command == "diff":
            report = support_diff(_load_json(args.first), _load_json(args.second))
        else:
            parser.error(f"unknown command: {args.command}")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 3
    _write_report(report, args.output, compact_json=args.command == "preprocess" and args.compact)
    return _exit_code(report.get("status"))


if __name__ == "__main__":
    raise SystemExit(main())
