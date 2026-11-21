#!/usr/bin/env python3
"""Optional, lossless mechanical helpers for C2 SRT and duration-text work."""

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

from prohibited_term_guard import load_formal_terms, normalize_for_match


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
    cues: list[Cue] = field(default_factory=list)
    parsed_ranges: list[dict[str, object]] = field(default_factory=list)
    unparsed_ranges: list[dict[str, object]] = field(default_factory=list)
    diagnostics: list[dict[str, object]] = field(default_factory=list)
    recognized_header_lines: list[dict[str, object]] = field(default_factory=list)
    total_blocks: int = 0
    status: str = "BLOCKED"
    source_sha256: str = ""


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
    return report


def parse_source(text: str, source_sha256: Optional[str] = None) -> SourceReport:
    """Parse every nonempty SRT block or numbered duration row without skipping failures."""
    if "-->" in text:
        report = _parse_srt(text)
    else:
        report = _parse_duration_text(text)
    report.source_sha256 = source_sha256 or hashlib.sha256(text.encode("utf-8")).hexdigest()
    return report


def find_direct_hits(cues: Iterable[Cue], terms: Iterable[str]) -> list[dict[str, object]]:
    """Match only listed terms; map cross-cue matches to every participating source cue."""
    cue_list = list(cues)
    term_list = [(term, normalize_for_match(term)) for term in terms]
    matched_ids: dict[str, list[str]] = {term: [] for term, _ in term_list}
    index = 0
    while index < len(cue_list):
        group = [cue_list[index]]
        index += 1
        while index < len(cue_list) and cue_list[index].source_order == group[-1].source_order + 1:
            group.append(cue_list[index])
            index += 1
        normalized = ""
        cue_for_character: list[str] = []
        for cue in group:
            normalized_text = normalize_for_match(cue.original_text)
            normalized += normalized_text
            cue_for_character.extend([cue.cue_id] * len(normalized_text))
        for original_term, normalized_term in term_list:
            if not normalized_term:
                continue
            found = normalized.find(normalized_term)
            while found >= 0:
                participating = cue_for_character[found:found + len(normalized_term)]
                for cue_id in participating:
                    if cue_id not in matched_ids[original_term]:
                        matched_ids[original_term].append(cue_id)
                found = normalized.find(normalized_term, found + 1)
    return [
        {"term": term, "cue_ids": cue_ids}
        for term, cue_ids in matched_ids.items()
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


def preprocess_text(
    text: str,
    formal_terms: Optional[Iterable[str]] = None,
    source_sha256: Optional[str] = None,
) -> dict[str, object]:
    """Return lossless source rows, mechanical diagnostics, direct hits, and compact views."""
    source = parse_source(text, source_sha256=source_sha256)
    terms = list(formal_terms) if formal_terms is not None else load_formal_terms()
    direct_hits = find_direct_hits(source.cues, terms)
    hit_ids = {cue_id for hit in direct_hits for cue_id in hit["cue_ids"]}

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
        "status": source.status,
        "counts": {"parsed_blocks": len(source.cues), "total_blocks": source.total_blocks},
        "recognized_header_lines": source.recognized_header_lines,
        "parsed_ranges": source.parsed_ranges,
        "unparsed_ranges": source.unparsed_ranges,
        "diagnostics": source.diagnostics,
        "cues": [cue.to_dict() for cue in source.cues],
        "direct_hits": direct_hits,
        "compact_table": compact_table,
        "compact_table_text": "\n".join(compact_lines),
        "timeline_map": timeline_map,
        "window_map_support": {
            "semantic_product_assignment": "AI_REQUIRED",
            "items": timeline_map,
        },
    }


def preprocess_file(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    report = preprocess_text(text, source_sha256=hashlib.sha256(raw).hexdigest())
    report["source_file"] = path.name
    return report


VALID_ROLES = {"独立卖点", "证据", "条件", "必要衔接", "可选行动句"}
VALID_FLAG_TYPES = {"fact_pending", "risk_hint", "key_limit"}


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
    for role_row in role_rows:
        if not isinstance(role_row, dict):
            failures.append(_failure("role_not_object", "each role row must be an object"))
            continue
        cue_id = str(role_row.get("cue_id", ""))
        role = role_row.get("role")
        role_counts[cue_id] = role_counts.get(cue_id, 0) + 1
        if cue_id not in source_ids:
            if source.status == "BLOCKED":
                blocked_refs.append({"code": "role_reference_in_unparsed_scope", "cue_id": cue_id})
            else:
                failures.append(_failure("role_id_not_in_source", "role cue ID is absent from source", cue_id=cue_id))
        if cue_id not in selected_set:
            failures.append(_failure("role_id_not_selected", "role cue ID is not selected", cue_id=cue_id))
        if role not in VALID_ROLES:
            failures.append(_failure("invalid_role", "role is not one of the five allowed roles", cue_id=cue_id, role=role))
    for cue_id in selected_ids:
        if role_counts.get(cue_id, 0) != 1:
            failures.append(_failure("role_cardinality", "each selected cue must have exactly one role", cue_id=cue_id, count=role_counts.get(cue_id, 0)))

    terms = list(formal_terms) if formal_terms is not None else load_formal_terms()
    direct_hits = find_direct_hits(source.cues, terms)
    hit_ids = {str(cue_id) for hit in direct_hits for cue_id in hit["cue_ids"]}
    for cue_id in selected_ids:
        if cue_id in hit_ids:
            failures.append(_failure("selected_direct_formal_term", "selected cue contains a direct formal prohibited-term hit", cue_id=cue_id))
    final_text_hits = find_direct_hits([Cue("final_text", -1, -1, 0, 0, final_text, 0, 0, 0)], terms) if final_text is not None else []
    if final_text_hits:
        failures.append(_failure("final_text_direct_formal_term", "final text contains a direct formal prohibited-term hit", direct_hits=final_text_hits))

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
        "direct_hits": direct_hits,
        "final_text_hits": final_text_hits,
        "semantic_review_required": True,
        "analysis_started": True,
        "full_source_checked": source.status != "BLOCKED",
    }


def _display_duration(milliseconds: int) -> str:
    seconds, millis = divmod(max(milliseconds, 0), 1000)
    return f"{seconds}.{millis:03}秒"


def _display_duration_exact(milliseconds: Decimal) -> str:
    seconds_text = _decimal_string(milliseconds / Decimal(1000))
    whole, _, fraction = seconds_text.partition(".")
    return f"{whole}.{fraction.ljust(3, '0')}秒"


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
    source_duration_exact = sum((Decimal(str(group["span_ms_exact"])) for group in groups), Decimal(0))
    source_duration_ms = _number_value(source_duration_exact)
    # 1.2x acceleration is source milliseconds / 1.2, rounded once, half up.
    accelerated_ms = int((source_duration_exact / Decimal("1.2")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
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
    playback_ms = accelerated_ms + known_unaccelerated_ms
    display = _display_duration(playback_ms)
    return {
        "status": "PASS",
        "validation": validation,
        "assembled": True,
        "source_sha256": source.source_sha256,
        "source_sequence": ",".join(selected_ids),
        "fifth_part_sequence": ",".join(selected_ids),
        "selected_ids": selected_ids,
        "segments": [{"cue_id": cue.cue_id, "original_text": cue.original_text} for cue in cues],
        "body_text": "\n".join(cue.original_text for cue in cues),
        "source_groups": groups,
        "source_duration_ms": source_duration_ms,
        "source_duration_ms_exact": _decimal_string(source_duration_exact),
        "accelerated_duration_ms": accelerated_ms,
        "known_unaccelerated_ms": known_unaccelerated_ms,
        "playback_duration_ms": playback_ms,
        "source_duration_display": _display_duration_exact(source_duration_exact),
        "playback_duration_display": display,
        "shared_duration_field": "playback_duration_display",
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
        "angles": [first.get("candidate_angle"), second.get("candidate_angle")],
        "semantic_review_required": True,
    }


def _write_report(report: dict[str, object], output: Optional[Path]) -> None:
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
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
            report = preprocess_file(args.source)
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
    _write_report(report, args.output)
    return _exit_code(report.get("status"))


if __name__ == "__main__":
    raise SystemExit(main())
