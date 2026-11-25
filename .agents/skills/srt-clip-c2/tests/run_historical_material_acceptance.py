#!/usr/bin/env python3
"""Run the 0.4.40 acceptance scenario against an external historical subtitle file.

The source transcript is deliberately not redistributed in the skill package.
This particular historic file is duration-text, not a timecoded .srt. Its one
standalone header marker and trailing duration-unit markers are normalized
without changing cue IDs, duration values, or transcript text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import srt_tools  # noqa: E402


EXPECTED_SOURCE_SHA256 = "cd4553c25561dbe15f43bc6596cb7f087ab56437e70c91d43c3184411030c3b1"
ROW = re.compile(r"^(\s*\d+\s+[+-]?(?:\d+(?:\.\d*)?|\.\d+))s([ \t].*)$")

# Human semantic review records all distinct, source-supported openers that
# meet the current viewing-motivation threshold. This list is not a quality
# classifier; the script only verifies exact source mapping and display count.
CANDIDATES = [
    {"name": "弹力实测", "ids": ["93", "94"]},
    {"name": "耐磨不起球", "ids": ["112", "113"]},
    {"name": "裤型显利落", "ids": ["135", "136", "137"]},
    {"name": "运动休闲好搭", "ids": ["141", "142", "143"]},
    {"name": "宽胯舒适版型", "ids": ["204", "205", "206", "207"]},
    {"name": "短密绒亲肤", "ids": ["602", "603"]},
    {"name": "厚度与暖感", "ids": ["652", "653", "654", "655"]},
    {"name": "暖和不显臃肿", "ids": ["794", "795", "796", "797", "798", "799", "800"]},
    {"name": "腿根防风", "ids": ["802", "803", "804", "805"]},
    {"name": "拉链口袋收纳", "ids": ["831", "832"]},
]

# Each block is a semantic unit that can move as a whole. Every plan uses the
# same complete point pool, but the order changes with its selected opener.
BLOCKS = {
    "fabric": ["92", "783", "784", "323", "324"],
    "fleece": ["104", "106", "107", "177", "179", "180", "221", "231", "232", "233", "234", "836", "837", "951", "952"],
    "thickness": ["150", "221", "229", "230", "231", "232", "233", "234", "836", "840", "951", "952"],
    "durability": ["627", "629", "631", "632", "921", "922", "923"],
    "fit": ["133", "134", "197", "199", "201", "825", "826", "827", "828", "829", "830", "961", "962"],
    "style_size": ["148", "149", "191", "192", "193", "644", "658", "659", "664", "665", "963", "964"],
    "utility": ["96", "97", "101", "604", "605", "606", "607"],
    "cuffs": ["609", "610", "618", "619", "620", "624", "625"],
    "wind": ["189", "320", "321", "323", "324", "927", "928", "929"],
    "brand": ["195", "196"],
}

POINTS = [
    {"id": "fabric_stretch", "support_ids": ["92", "783", "784", "323", "324"]},
    {"id": "integrated_dense_fleece", "support_ids": ["104", "106", "107", "221", "231", "232", "233", "234", "836", "837", "951"]},
    {"id": "fleece_not_shedding", "support_ids": ["177", "179", "180"]},
    {"id": "warmth_thickness", "support_ids": ["150", "221", "229", "230", "231", "232", "233", "234", "836", "840", "952"]},
    {"id": "anti_pilling", "support_ids": ["627", "629", "631", "632"], "necessary_evidence_ids": ["631", "632"]},
    {"id": "color_fastness_and_first_wash_condition", "support_ids": ["921", "923"], "required_condition_ids": ["921", "922", "923"]},
    {"id": "fit_and_body_shape", "support_ids": ["134", "197", "199", "201", "825", "826", "827", "828", "829", "830", "961", "962"]},
    {"id": "style_and_unisex_range", "support_ids": ["148", "149", "191", "192", "193", "644", "963", "964"]},
    {"id": "zipped_pockets_and_waist_drawstring", "support_ids": ["96", "97", "101", "604", "605", "606", "607"]},
    {"id": "cuff_choices_and_wind_protection", "support_ids": ["609", "610", "618", "619", "620", "624", "625", "927", "928", "929"]},
    {"id": "leg_root_wind_protection", "support_ids": ["189", "320", "321", "323", "324", "927", "928", "929"]},
    {"id": "size_guidance", "support_ids": ["658", "659", "664", "665"]},
    {"id": "361_logo_classic_style", "support_ids": ["133", "195", "196"]},
]

PLANS = [
    {"candidate": "裤型显利落", "ids": ["135", "136", "137"], "core": "裤型和身形适配", "block_order": ["fit", "style_size", "fabric", "fleece", "thickness", "wind", "durability", "utility", "cuffs", "brand"]},
    {"candidate": "厚度与暖感", "ids": ["652", "653", "654", "655"], "core": "加绒保暖与冬季舒适", "block_order": ["thickness", "fleece", "fabric", "fit", "wind", "utility", "cuffs", "durability", "style_size", "brand"]},
    {"candidate": "腿根防风", "ids": ["802", "803", "804", "805"], "core": "防风包裹与冬季穿着", "block_order": ["wind", "cuffs", "fit", "fleece", "thickness", "fabric", "utility", "durability", "style_size", "brand"]},
]


def normalize_historical_duration_text(raw: str) -> tuple[str, dict[str, int]]:
    lines = raw.splitlines()
    removed_header = 0
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.strip() == "1":
            lines.pop(index)
            removed_header = 1
        break
    normalized_rows = 0
    normalized_lines = []
    for line in lines:
        match = ROW.fullmatch(line)
        if match:
            line = match.group(1) + match.group(2)
            normalized_rows += 1
        normalized_lines.append(line)
    return "\n".join(normalized_lines), {"removed_standalone_header": removed_header, "removed_duration_suffix_s": normalized_rows}


def deduplicate(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def exact_text(source: srt_tools.SourceReport, ids: list[str]) -> str:
    by_id = {cue.cue_id: cue for cue in source.cues}
    return "\n".join(by_id[cue_id].original_text for cue_id in ids)


def user_choice_gate(selected_names: list[str], available_names: set[str]) -> dict[str, object]:
    if len(selected_names) > 3:
        return {"status": "BLOCKED", "selected_count": len(selected_names), "generated_clips": 0}
    if not selected_names:
        return {"status": "AWAITING_USER_CHOICE", "selected_count": 0, "generated_clips": 0}
    if len(set(selected_names)) != len(selected_names) or any(name not in available_names for name in selected_names):
        return {"status": "BLOCKED", "selected_count": len(selected_names), "generated_clips": 0}
    return {"status": "READY", "selected_count": len(selected_names), "generated_clips": len(selected_names)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--skip-exact-hash", action="store_true", help="allow a copied source with a different SHA; still records it")
    args = parser.parse_args()
    raw_bytes = args.source.read_bytes()
    source_sha = hashlib.sha256(raw_bytes).hexdigest()
    if source_sha != EXPECTED_SOURCE_SHA256 and not args.skip_exact_hash:
        raise SystemExit(f"BLOCKED: source SHA-256 mismatch: {source_sha}")
    raw_text = raw_bytes.decode("utf-8-sig")
    normalized_text, normalization = normalize_historical_duration_text(raw_text)
    source = srt_tools.parse_source(normalized_text, source_sha256=source_sha)
    if source.status != "PASS" or len(source.cues) != 996 or source.total_blocks != 996:
        raise SystemExit(f"FAIL: parse status={source.status}, cues={len(source.cues)}, blocks={source.total_blocks}, unparsed={source.unparsed_ranges[:2]}")
    if [cue.cue_id for cue in source.cues] != [str(i) for i in range(1, 997)]:
        raise SystemExit("FAIL: cue sequence is not exactly 1..996")
    direct_hits = srt_tools.find_direct_hits(source.cues, srt_tools.load_formal_terms())
    if direct_hits:
        raise SystemExit(f"FAIL: source has formal direct-term hits: {direct_hits}")

    by_id = {cue.cue_id: cue for cue in source.cues}
    candidate_rows = []
    for candidate in CANDIDATES:
        ids = candidate["ids"]
        opening_text = exact_text(source, ids)
        raw_ms = sum((by_id[cue_id].duration_ms for cue_id in ids), start=0)
        estimated = srt_tools._display_duration(raw_ms / Decimal("1.2"))
        candidate_rows.append({"方案名称": candidate["name"], "开头正文": opening_text, "原始序号": ",".join(ids), "预计时长": estimated})
    if any(set(row) != {"方案名称", "开头正文", "原始序号", "预计时长"} for row in candidate_rows):
        raise SystemExit("FAIL: candidate display fields differ from the four-field contract")
    if len(candidate_rows) <= 3:
        raise SystemExit("FAIL: historical candidate pool does not exceed three")
    if len({"".join(row["开头正文"].split()) for row in candidate_rows}) != len(candidate_rows):
        raise SystemExit("FAIL: duplicate candidate wording in semantic audit set")

    # No choice means no clip. More than three is blocked without truncation.
    available_names = {row["方案名称"] for row in candidate_rows}
    no_choice = user_choice_gate([], available_names)
    if no_choice != {"status": "AWAITING_USER_CHOICE", "selected_count": 0, "generated_clips": 0}:
        raise SystemExit("FAIL: an empty selection must wait without generating clips")
    oversized_choice = [row["方案名称"] for row in candidate_rows[:4]]
    blocked_choice = user_choice_gate(oversized_choice, available_names)
    if blocked_choice.get("status") != "BLOCKED" or blocked_choice.get("generated_clips") != 0:
        raise SystemExit("FAIL: over-limit guard did not block without truncation")

    all_blocks = {key: value for key, value in BLOCKS.items()}
    plan_results = []
    clip_sequences = []
    rendered_clips = []
    all_candidate_ids = {cue_id for candidate in CANDIDATES for cue_id in candidate["ids"]}
    all_support_ids = {sid for point in POINTS for field in ("support_ids", "necessary_evidence_ids", "required_condition_ids") for sid in point.get(field, [])}
    for plan in PLANS:
        if plan["candidate"] not in available_names:
            raise SystemExit(f"FAIL: test selection is not in the displayed candidate set: {plan['candidate']}")
        ids = list(plan["ids"])
        opening_ids = set(ids)
        for block_name in plan["block_order"]:
            ids.extend(cue_id for cue_id in all_blocks[block_name] if cue_id not in opening_ids)
        ids = deduplicate(ids)
        if ids[:len(plan["ids"])] != plan["ids"]:
            raise SystemExit("FAIL: selected opening is not first")
        foreign_candidate_ids = (set(ids) & all_candidate_ids) - set(plan["ids"])
        if foreign_candidate_ids:
            raise SystemExit(f"FAIL: alternative hook was carried into {plan['candidate']} body: {sorted(foreign_candidate_ids)}")
        if not all_support_ids.issubset(ids):
            raise SystemExit(f"FAIL: incomplete point coverage in {plan['candidate']}: {sorted(all_support_ids-set(ids))}")
        dynamic_transaction_ids = set(range(238, 320)) | {326, 327} | set(range(572, 598)) | {663} | set(range(666, 698)) | {780, 781, 782, 787, 788, 789, 790, 791, 792, 793} | set(range(846, 853)) | set(range(859, 891)) | set(range(967, 975)) | {977, 978, 979, 980, 987, 988, 989, 990}
        if set(ids) & {str(cue_id) for cue_id in dynamic_transaction_ids}:
            raise SystemExit(f"FAIL: dynamic transaction material leaked into {plan['candidate']}")
        roles = []
        evidence = {sid for point in POINTS for sid in point.get("necessary_evidence_ids", [])}
        conditions = {sid for point in POINTS for sid in point.get("required_condition_ids", [])}
        cta = {"620"}
        bridges = {"93", "114", "115", "116", "117", "118", "119", "120", "121", "178", "804"}
        for cue_id in ids:
            if cue_id in cta:
                role = "适用促单原话"
            elif cue_id in conditions:
                role = "条件"
            elif cue_id in evidence:
                role = "证据"
            elif cue_id in bridges:
                role = "必要衔接"
            else:
                role = "独立卖点"
            roles.append({"cue_id": cue_id, "role": role})
        selection = {
            "verification_mode": "script",
            "source_sha256": source_sha,
            "selected_ids": ids,
            "selling_points": POINTS,
            "roles": roles,
            "flags": [],
        }
        assembly = srt_tools.assemble_selection(source, selection)
        if assembly.get("status") != "PASS":
            raise SystemExit(f"FAIL: assembly rejected {plan['candidate']}: {assembly.get('validation', {}).get('hard_failures', [])}")
        final = srt_tools.verify_final_output(source, selection, assembly, assembly["body_text"], assembly["fifth_part_sequence"])
        if final["status"] != "PASS":
            raise SystemExit(f"FAIL: source/sequence verification failed: {final['hard_failures']}")
        if assembly["body_text"].splitlines()[0] != by_id[plan["ids"][0]].original_text:
            raise SystemExit("FAIL: final clip does not start with exact selected opener")
        clip_sequences.append(ids)
        rendered_clips.append(assembly["body_text"])
        plan_results.append({
            "selected_opening": plan["candidate"],
            "core": plan["core"],
            "first_ids": plan["ids"],
            "first_text": exact_text(source, plan["ids"]),
            "cue_count": len(ids),
            "duration_estimate": assembly["playback_duration_display"],
            "point_coverage": len(POINTS),
            "evidence_and_conditions_included": True,
            "direct_formal_hits": 0,
            "source_map_and_fifth_part_sequence": final["status"],
            "block_order": plan["block_order"],
            "sequence": ids,
        })
    if len({tuple(plan["block_order"]) for plan in PLANS}) != len(PLANS):
        raise SystemExit("FAIL: block orders are not independently composed")

    # Release contract: exactly five sections; one title and five hashtags per plan;
    # fifth-part lines are emitted from the verified final selections.
    sections = ["一、文件解析结果", "二、商品识别", "三、最佳成片方案", "四、作品标题与话题", "五、原始 SRT 序号"]
    final_document = "\n".join([
        "# " + sections[0],
        f"文件解析：{args.source.name}；逐条时长文本；Standard；窗口 1；入选 {sum(len(p['sequence']) for p in plan_results)} 条/{len(plan_results)} 组；开发回归机械核验。",
        "# " + sections[1],
        "目标商品：361 度加绒卫裤；归属窗口：87–996。",
        "# " + sections[2],
        *[f"方案：{p['selected_opening']}；核心：{p['core']}；开头：{p['first_text']}；原始序号：{','.join(p['first_ids'])}。\n成片正文：\n{body}" for p, body in zip(plan_results, rendered_clips)],
        "# " + sections[3],
        *[f"{p['selected_opening']}：标题：361度加绒卫裤的冬季穿着体验；话题：#加绒卫裤 #冬季穿搭 #日常穿搭 #运动休闲 #裤型选择" for p in plan_results],
        "# " + sections[4],
        "```text",
        *[",".join(p["sequence"]) for p in plan_results],
        "```",
    ])
    if [line[2:] for line in final_document.splitlines() if line.startswith("# ")] != sections:
        raise SystemExit("FAIL: final delivery section count/order changed")
    for body in rendered_clips:
        if f"成片正文：\n{body}" not in final_document:
            raise SystemExit("FAIL: a complete verified clip body is absent from part three")
    if final_document.count("话题：") != 3 or any(row.count("#") != 5 for row in final_document.splitlines() if "话题：" in row):
        raise SystemExit("FAIL: title/topic cardinality is invalid")

    result = {
        "result": "PASS",
        "source_file": args.source.name,
        "source_kind": "historical numbered duration-text (not timecoded .srt)",
        "source_sha256": source_sha,
        "normalized_sha256": hashlib.sha256(normalized_text.encode("utf-8")).hexdigest(),
        "parse": {"status": source.status, "rows": len(source.cues), "unparsed": 0, "source_map_sha256": source.source_map_sha256},
        "adapter_normalization": normalization,
        "full_source_formal_direct_hits": 0,
        "semantic_candidate_audit": {"qualified_distinct_candidates": len(candidate_rows), "displayed": candidate_rows, "preselected": None, "auto_selected": False},
        "candidate_display": {"result": "PASS", "field_count": 4, "field_names": ["方案名称", "开头正文", "原始序号", "预计时长"]},
        "unselected_state": no_choice,
        "over_limit_guard": blocked_choice,
        "selected_test_case": {"selected_count": len(PLANS), "generated_clips": len(plan_results), "plans": plan_results},
        "different_dynamic_block_orders": len({tuple(p['block_order']) for p in PLANS}) == len(PLANS),
        "fixed_five_part_delivery": {"result": "PASS", "sections": sections, "complete_clip_bodies_rendered": len(rendered_clips), "title_count": 3, "hashtags_per_plan": 5, "fifth_part_ids_match_final_selections": True},
        "semantic_limit": "Candidate qualification, point semantics, product attribution, dynamic information exclusion, and board-order quality were human semantic review; the script verified IDs, exact text, duration map, formal direct terms, coverage references, and rendering structure.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
