#!/usr/bin/env python3
"""Development-only semantic, packaging, mirror, and version release gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = next(parent for parent in SKILL_ROOT.parents if (parent / "VERSION").is_file())
EXPECTED_CORE = "0.4.7"
EXPECTED_SKILL = "0.4.44"
ACTIVE_SURFACES = (
    "SKILL.md", "README.md", "START-HERE.md", "ENVIRONMENT.md", "agents/openai.yaml",
    "references/ai-first-constitution.md", "references/runtime-contract.md",
    "references/clip-selection-policy.md", "references/editorial-policy.md",
    "references/final-check.md", "references/global-rules.md", "references/long-context-mode.md",
    "references/highlight-selection.md", "references/product-knowledge-registry.md",
    "references/update-protocol.md", "tests/quality-rubric.md",
    "references/runtime-current.md", "references/execution-summary.json",
    "scripts/prohibited_term_guard.py", "scripts/srt_tools.py",
    "tests/prohibited-term-regression-cases.md", "tests/test_phase3_duplicate_control.py",
    "tests/test_phase3_absolute_terms.py", "C2-Universal-Portable.md",
)
PLUGIN_SURFACES = ("README.md", "START-HERE.md", "CHANGELOG.md", "plugin.json", ".codex-plugin/plugin.json")

_MULTI_HOOK_SHARE = re.compile(
    r"(?:多方案|多开头|不同方案|多个方案|多条成片).{0,70}(?:共享|共用|沿用|复用).{0,35}(?:最佳|同一|开头|钩子)"
    r"|(?:最佳|同一).{0,20}(?:开头|钩子).{0,45}(?:共享|共用|沿用).{0,25}(?:多方案|多个方案|多条成片)",
    re.IGNORECASE,
)
_CANDIDATE_CAP = re.compile(
    r"(?:候选|开头).{0,20}(?:最多|至多|上限).{0,12}(?:识别|筛选|展示|显示|输出).{0,14}(?:三个|3\s*个|三项|3\s*项)"
    r"|(?:候选|开头).{0,20}(?:识别|筛选|展示|显示|输出).{0,14}(?:最多|至多|上限).{0,12}(?:三个|3\s*个|三项|3\s*项)"
    r"|(?:最多|至多|上限).{0,12}(?:识别|筛选|展示|显示|输出).{0,14}(?:三个|3\s*个|三项|3\s*项)",
    re.IGNORECASE,
)
_AUTO_PICK = re.compile(
    r"(?:AI|模型|系统).{0,24}(?:默认|自动|推荐).{0,16}(?:选择|选定|决定开头|决定成片数量)",
    re.IGNORECASE,
)
_FIXED_BLOCK_ORDER = re.compile(
    r"(?:内容结构|板块顺序|成交结构).{0,35}(?:固定|统一|必须按|一律按|始终按).{0,30}(?:模板|顺序|结构)",
    re.IGNORECASE,
)
_NEGATION = ("不得", "禁止", "不设", "不要求", "不存在", "不能", "无需", "不应", "不按")


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def semantic_conflicts(text: str) -> list[tuple[int, str, str]]:
    """Return positive claims that revive a retired selection or structure rule."""
    conflicts = []
    for line_number, line in enumerate(text.splitlines(), 1):
        candidates = (
            ("hook_reuse", _MULTI_HOOK_SHARE),
            ("candidate_display_cap", _CANDIDATE_CAP),
            ("automatic_user_choice", _AUTO_PICK),
            ("fixed_block_order", _FIXED_BLOCK_ORDER),
        )
        for label, pattern in candidates:
            if pattern.search(line) and not any(negation in line for negation in _NEGATION):
                conflicts.append((line_number, label, line.strip()))
    return conflicts


def tracked_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}
    }


def assert_current_test_contract() -> None:
    tests = SKILL_ROOT / "tests"
    required = {
        "test_phase1_scope_boundary.py": ("deferred_block_ordering_is_absent_from_active_rules", "phase_one_keeps_dynamic_body_order_and_candidate_limit", "development_governance_stays_out_of_daily_runtime", "mirror_sync_removes_stale_files"),
        "test_opening_candidate_quantity.py": ("test_policy_explicitly_separates_uncapped_display_from_selection_cap", "test_user_selection_limit_is_three_and_selected_count_maps_to_cuts"),
        "test_confirmed_workflow.py": ("test_04_text_only_context_tracks_event_lifecycle", "test_immutable_cue_records_bind_id_text_and_exact_duration", "test_any_text_or_final_sequence_mismatch_fails"),
        "test_phase3_duplicate_control.py": ("test_differently_worded_generic_praise_competes_for_one_best_line", "test_useful_information_can_continue_past_90_seconds_without_hard_cut"),
        "test_phase3_absolute_terms.py": ("test_confirmed_product_claims_are_blocked_as_full_cues", "test_first_and_best_ordinary_language_is_allowed", "test_unconfirmed_asr_lookalikes_do_not_become_hits"),
    }
    for relative, phrases in required.items():
        path = tests / relative
        if not path.is_file():
            raise ValueError(f"required current regression test missing: {relative}")
        content = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in content:
                raise ValueError(f"required regression assertion missing: {phrase!r} in {relative}")
    stale_tokens = (
        "tests/history/", "release-acceptance-0.4.37", "dynamic-hook-regression-0.4.30",
        "opening-selection-regression-0.4.40", "run_historical_material_acceptance.py",
    )
    for path in tests.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".md", ".json"}:
            text = path.read_text(encoding="utf-8")
            if any(token in text for token in stale_tokens):
                raise ValueError(f"test references a retired historical artifact: {path.relative_to(SKILL_ROOT)}")
    opener_test = (tests / "test_opening_candidate_quantity.py").read_text(encoding="utf-8")
    for phrase in ("def render_clips", "clip[\"cues\"][0][\"id\"]", "全部有效卖点"):
        if phrase not in opener_test:
            raise ValueError(f"opening regression assertions missing: {phrase}")


def assert_no_historical_package_files() -> None:
    for path in PLUGIN_ROOT.rglob("*"):
        relative = path.relative_to(PLUGIN_ROOT)
        if any(component.casefold() in {"history", "historical", "acceptance"} for component in relative.parts):
            raise ValueError(f"historical directory/file remains in release source: {relative}")
        if path.is_file() and (path.suffix.lower() == ".zip" or re.search(r"(?:old|legacy|history|release-acceptance).*\.(?:md|txt)$", path.name, re.I)):
            raise ValueError(f"historical archive or report remains in release source: {relative}")


def assert_versions_and_generated_files() -> None:
    plugin = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
    companion = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    manifest_path = SKILL_ROOT / "references/runtime-manifest.json"
    summary_path = SKILL_ROOT / "references/execution-summary.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    core = (PLUGIN_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    skill = (SKILL_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if core != EXPECTED_CORE or manifest.get("core_version") != core:
        raise ValueError("Core version and runtime manifest disagree")
    if skill != EXPECTED_SKILL or plugin.get("version") != skill or companion.get("version") != skill:
        raise ValueError("Skill/plugin versions disagree with the release target")
    if manifest.get("skill_version") != skill or summary.get("skill_version") != skill:
        raise ValueError("Runtime manifest or execution summary has a stale Skill version")
    if summary.get("core_version") != core:
        raise ValueError("Execution summary has a stale Core version")
    if plugin.get("name") != companion.get("name") or plugin.get("skills") != companion.get("skills"):
        raise ValueError("Plugin manifests disagree on identity or entry")
    if plugin.get("extensions", {}).get("com.openai", {}).get("interface", {}).get("defaultPrompt") != companion.get("interface", {}).get("defaultPrompt"):
        raise ValueError("Plugin entry prompts disagree")

    build_check = subprocess.run([sys.executable, str(SKILL_ROOT / "scripts/build_runtime.py"), "--check"], capture_output=True, text=True)
    if build_check.returncode:
        raise ValueError("compiled runtime/manifest check failed: " + (build_check.stdout + build_check.stderr).strip())
    summary_check = subprocess.run([
        sys.executable, str(SKILL_ROOT / "scripts/execution_summary.py"), "validate",
        "--skill-root", str(SKILL_ROOT), "--summary", str(summary_path),
    ], capture_output=True, text=True)
    if summary_check.returncode:
        raise ValueError("execution summary validation failed: " + (summary_check.stdout + summary_check.stderr).strip())

    import importlib.util
    spec = importlib.util.spec_from_file_location("c2_build_portable", SKILL_ROOT / "scripts/build_portable.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    portable_path = SKILL_ROOT / "C2-Universal-Portable.md"
    if portable_path.read_text(encoding="utf-8") != module.build():
        raise ValueError("portable runtime is not generated from current sources")


def assert_prohibited_term_contract() -> None:
    sys.path.insert(0, str(SKILL_ROOT / "scripts"))
    import prohibited_term_guard as guard

    entries = guard.load_term_registry()
    by_term = {entry.term: entry for entry in entries}
    absolute = {"国家级", "最高级", "顶级", "首选", "绝无仅有", "史无前例", "第一", "最好", "全网最好"}
    if not absolute <= by_term.keys() or any(by_term[term].match_class != "contextual" for term in absolute):
        raise ValueError("absolute-term registry is incomplete or classified inconsistently")
    if by_term["不起球"].allowed_exceptions != ("不易起球",):
        raise ValueError("the confirmed pilling-expression protection changed")
    if by_term["最好"].confirmed_equivalents != ("全网没有比这件更好的",):
        raise ValueError("the confirmed best-equivalent registration changed")
    if by_term["首选"].allowed_exceptions:
        raise ValueError("首选 must not have a product-promotion whitelist")

    cues = [
        guard.Cue("1", "销量第一"),
        guard.Cue("2", "第一步先看版型"),
        guard.Cue("3", "这件是我的首选"),
        guard.Cue("4", "最好明天发货"),
        guard.Cue("5", "这件不易起球"),
        guard.Cue("6", "这件国家计级活动款"),
    ]
    report = guard.build_report(cues, entries)
    if report["contextual_block_ids"] != ["1", "3"] or report["contextual_allow_ids"] != ["2", "4"]:
        raise ValueError("contextual product claims or ordinary language failed the release sample")
    if report["excluded_full_cue_ids"] != ["1", "3"] or any(item["auto_blocked"] for item in report["asr_suspicions"]):
        raise ValueError("cue-scope or unconfirmed-ASR behavior changed")


def assert_release_conflict_residuals() -> None:
    rules = (SKILL_ROOT / "references/global-rules.md").read_text(encoding="utf-8")
    final_check = (SKILL_ROOT / "references/final-check.md").read_text(encoding="utf-8")
    if "不得设“我的首选”“首选搭配”等商品宣传白名单" not in rules:
        raise ValueError("the dictionary must explicitly prevent 首选 promo whitelists")
    if "商品语境中的“我的首选”“首选搭配”不得作为白名单" not in final_check:
        raise ValueError("final check does not enforce the 首选 rule")
    if "客观事实证明不解除拦截" not in final_check:
        raise ValueError("final check must not create a proof-based exemption")


def assert_semantic_surfaces() -> None:
    text_suffixes = {".md", ".json", ".yaml", ".yml", ".py", ".toml", ".txt"}
    # The detector's own regexes describe retired variants as patterns, not as
    # operational rules. Its behavior is separately tested by encoded fixtures.
    paths = [
        path for path in PLUGIN_ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in text_suffixes
        and "__pycache__" not in path.parts
        and ".git" not in path.parts
        and path.name != "release_gate.py"
    ]
    for path in paths:
        relative = path.relative_to(PLUGIN_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if path.name == "execution-summary.json":
            text = json.loads(text).get("summary", "")
        elif path.name == "plugin.json":
            payload = json.loads(text)
            text = json.dumps(payload.get("extensions", {}), ensure_ascii=False) + "\n" + json.dumps(payload.get("interface", {}), ensure_ascii=False)
        conflicts = semantic_conflicts(text)
        if conflicts:
            line, label, excerpt = conflicts[0]
            raise ValueError(f"semantic conflict {label} in {relative}:{line}: {excerpt}")

    for relative in ACTIVE_SURFACES:
        if not (SKILL_ROOT / relative).is_file():
            raise ValueError(f"active rule surface missing: {relative}")

    editorial = (SKILL_ROOT / "references/editorial-policy.md").read_text(encoding="utf-8")
    selection = (SKILL_ROOT / "references/clip-selection-policy.md").read_text(encoding="utf-8")
    final_check = (SKILL_ROOT / "references/final-check.md").read_text(encoding="utf-8")
    for text, phrase, source in (
        (editorial, "候选展示不设数量上限", "editorial-policy.md"),
        (editorial, "不用于给候选排出一个胜者", "editorial-policy.md"),
        (editorial, "每条成片必须以对应的用户所选开头原话开始", "editorial-policy.md"),
        (selection, "每条独立重新编排正文并动态重排", "clip-selection-policy.md"),
        (final_check, "每条成片从对应用户所选开头原话开始", "final-check.md"),
    ):
        if phrase not in text:
            raise ValueError(f"required active rule missing from {source}: {phrase}")


def assert_mirror() -> None:
    mirror = PLUGIN_ROOT / ".agents/skills/srt-clip-c2"
    if tracked_files(SKILL_ROOT) != tracked_files(mirror):
        raise ValueError("canonical Skill and .agents mirror differ")


def assert_archive(archive: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        archived = {
            name.removeprefix("skills/srt-clip-c2/"): normalized_sha256(zf.read(name))
            for name in zf.namelist()
            if name.startswith("skills/srt-clip-c2/") and not name.endswith("/")
        }
    canonical = {name: normalized_sha256(data) for name, data in tracked_files(SKILL_ROOT).items()}
    if archived != canonical:
        missing = sorted(set(canonical) - set(archived))
        extra = sorted(set(archived) - set(canonical))
        changed = sorted(name for name in set(archived) & set(canonical) if archived[name] != canonical[name])
        raise ValueError(f"Skill ZIP content mismatch: missing={missing[:5]}, extra={extra[:5]}, changed={changed[:5]}")
    if any("history" in name.casefold() or name.lower().endswith(".zip") for name in archived):
        raise ValueError("Skill ZIP contains historical material or nested archives")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    checks = [
        ("semantic surfaces", assert_semantic_surfaces),
        ("historical cleanup", assert_no_historical_package_files),
        ("current tests", assert_current_test_contract),
        ("versions and generated files", assert_versions_and_generated_files),
        ("prohibited-term regression contract", assert_prohibited_term_contract),
        ("prohibited-term conflict cleanup", assert_release_conflict_residuals),
        ("canonical/mirror parity", assert_mirror),
    ]
    if args.archive:
        checks.append(("Skill ZIP", lambda: assert_archive(args.archive.resolve())))
    for label, check in checks:
        check()
        print(f"PASS {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
