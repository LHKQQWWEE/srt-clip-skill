---
name: srt-clip-skill
description: Turn one or more raw SRT livestream subtitle files into verified, conversion-focused short-video clip scripts using SRT Clip Copy V3.0 and R8 utilities. Trigger on "srt切片文案". Strictly preserve original SRT text, timecodes and indices.
---

# SRT 切片文案 · V3.0 ACTIVE / R8

## Scope
Use for pure SRT text files only, including pasted SRT-formatted TXT. Do not claim to have validated video/audio. This is separate from the MP4-enabled "切片文案 V5.1" workflow. Never silently replace this workflow with archived R7/R6/R5 versions.

## Inputs
- One or more .srt files, or verbatim SRT text with recognizable numbered subtitle blocks and timestamps.
- Optional specified target product; otherwise identify product boundaries first. If multiple products are present and target is ambiguous, ask once for target product(s) before deep selection.
- Files are isolated by default, even if they appear continuous. Only merge with explicit user instruction.

## Authority / runtime
- Business rules: V3.0 ACTIVE. Support package: R8, located in `assets/SRT_V3.0_R8.zip`.
- Source-of-truth runtime card: Google Drive ID `1L7Q8HaW4vHSeLcKWBQnaKZ4ppvPUXnQ9wuUjAdco-aQ` (FAST-PATH 2.0). This skill embeds core operational rules so other AI agents can run without Drive access. When conflicts are detected, stop and request the authoritative rule rather than guessing.
- Confirm SHA-256 of package is `999679f9b9de47c348813ef79880ea2d230412c6741b70665ad04ffefab3edbb` before executing bundled scripts; inspect README and CLI help inside ZIP. Never execute an unverified archive blindly.

## Process
1. Read each SRT exactly once. Decode UTF-8-SIG -> UTF-8 -> GB18030. Parse and freeze per-file canonical read-only index: `source_key`, `file_id`, `filename`, `block_ordinal`, source index as text, verbatim subtitle content, `start_raw`, `end_raw`, `start_ms`, `end_ms`, file SHA-256. Do not renumber source indices.
2. Perform ONE lightweight full-file scan for product transitions, role/quote or read-comment signals, numeric risk and context boundaries. For multiple SRTs assign stable `f01`/`f02` file slots. Never concatenate source files.
3. If multiple products require user selection, pause once with product names and source ranges; keep parsed canonical state. Once confirmed, do not re-read/reparse or redo the full scan.
4. Deep-scan only the target product windows with bounded context using multi-window target slices. Use the R8 scope-once model bundle: top-level `s=f01` etc per file (single-SRT path does not add scope), row-level `c001`/`c002`. Resolve cues only with batch/file-slot/bundle/file identity and ordered canonical source keys; reject cross-file reference reuse. Long `source_key` stays in deterministic software.
5. AI interprets product meaning, buyer pain, selling points, evidence, scenario/fit, objections, trading rationale and genuine CTA. Surface `question_like` and dependency hints without automatically dropping subtitles. Reject explicit read-chat/commentary content when not suitable as the speaker's substantive pitch.
6. Compress semantically equivalent candidates without losing unique facts/price/CTA/needed context. Up to 3 complementary per cluster, up to 5 opening and 5 closing candidates ordinarily. Avoid full permutation search.
7. Opening must pass all 3 hard criteria: target buyers recognize themselves; non-target viewers can self-filter; opening promises a concrete payoff the video delivers quickly (prefer within 3 segments). Middle segments each advance the purchase decision. Price and transaction reasons generally late. If a reliable CTA exists, it must be the final segment; never fabricate claims, prices, urgency or stock conditions.
8. Target theoretical precise-cut subtitle duration strictly 45-90 seconds, ideally near 70 seconds when source supports it. Do not pad with repetitious/off-topic lines.
9. Final playback plan stores only validated `source_key` values. Run a single deterministic Final Gate to build ONE `verified_manifest` with exact original index, complete original text, raw timecode, start/end ms, file identity, source coverage, uncovered gaps, group boundaries, cumulative finished timeline and final ordered indices. No independent model arithmetic or reassembly of Part 3 and Part 5. On mismatch or duration violation, block formal delivery and repair the candidate plan, then revalidate.
10. Render five sections from that same manifest in order; keep Part 3 format fixed.

## Required output (per file)
**一、文件解析结果** — filename, parsed cue count and defects/identity.

**二、商品识别** — target product and identified segments; request confirmation first if ambiguous.

**三、最佳成片方案** — frozen format, each segment:
```text
三、最佳成片方案
主推主题：……
预计成片时长：HH:MM:SS.mmm
片段N｜片段功能｜预计成片 HH:MM:SS.mmm–HH:MM:SS.mmm｜原SRT HH:MM:SS.mmm–HH:MM:SS.mmm｜源序号 5–8｜本组未覆盖间隔 HH:MM:SS.mmm｜SRT源字幕定位
原始序号 | HH:MM:SS,mmm --> HH:MM:SS,mmm | 完整原始字幕文本
```
Do not paraphrase source subtitle lines, invert end/start, merge adjacent lines or substitute estimated timestamps. Every segment's original cue lines must be printed and source-validated.

**四、作品标题与话题** — exactly one title and three hashtags.

**五、原始SRT序号（按成片播放顺序）** — offer a copy control when UI supports it; show only the same ordered indices in a copyable code block; the absolute final line must repeat the identical plain numeric index sequence, with no text following it. Determine indices from `verified_manifest` only, including when files have repeated or out-of-order source numbering. For multiple files produce independently scoped outputs, never a combined source-number list.

## Hard fails
Fail closed when package hash disagrees, file/SHA/slot/bundle/cue resolver is inconsistent, original text or source timecodes drift, source start is later than end, any subtitles cross into another product/file, group gap/coverage is contradictory, finished length is outside 45–90 seconds, or Part 3 and Part 5 diverge. Declare what failed; do not fabricate a finished answer.

## Efficiency
Typical single-file path: 1 runtime read (or none when self-contained), 1 SRT read, 1 parse, 1 lightweight scan, 1 target deep scan, 1 Final Gate. Multi-file paths preserve per-file isolation and single-pass reads. Never claim a wall-clock speedup without measurements.

## Portable invocation
Ask an AI agent to load this SKILL.md and the R8 archive, then: “srt切片文案” with the actual subtitle file(s). Executing Python utilities requires a Python runtime; plain conversational models can follow the rules but cannot claim deterministic validation without running the Final Gate.
