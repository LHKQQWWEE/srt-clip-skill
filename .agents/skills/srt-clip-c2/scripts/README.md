# Optional tools

C2 Universal does not require or bundle a Python runtime script for ordinary SRT or duration-text tasks.

Use the host AI's native file reading and calculation capabilities by default. These standard-library utilities are optional and never become a normal-task gate or require a JSON/workflow pipeline.

## Optional unified preprocessing tool

`srt_tools.py` is an optional standard-library helper for lossless parsing, deterministic assembly, structural gate checks, and support-map diffs. It never decides product identity, selling-point meaning, evidence sufficiency, semantic equivalence, transition continuity, or candidate quality.

Examples:

```text
python scripts/srt_tools.py preprocess input.srt --compact --output report.json
python scripts/srt_tools.py assemble input.srt selection.json --output assembly.json
python scripts/srt_tools.py check input.srt selection.json --final-text final-copy.txt
python scripts/srt_tools.py diff replay-a.json replay-b.json
```

By default, the preprocessor preserves the legacy JSON shape, including a compact table and a separate timeline view. Add `--compact` to return one lossless `rows` entry per cue with exact timing, source lines, original text, and a direct-hit mark; it also returns counts, diagnostics, direct hits, and coalesced consecutive parsed ranges. It omits duplicate table/timeline views and uses compact JSON serialization, so it is preferred for large sources. The compact mode preserves malformed ranges and does not merge across a malformed block or numbering gap. Both modes recognize exact leading paste labels `srt文案` and `【字幕列表】` as input metadata, report their line numbers, and exclude them from cue counts; other unrecognized text remains unparsed and BLOCKED. Duration-text rows retain decimal precision through aggregation; a malformed row makes later cumulative timeline positions explicitly unknown while preserving their parsed text. A hit is marked `HIT` on its row; hit rows remain visible, and selection validation fails if one is selected. Unparsed ranges are `BLOCKED` and cannot be described as fully checked. Timeline rows do not assign product identity; that remains an AI judgment.

The selection object follows `selection.schema.json`. `verification_mode` is `script` only when the helper is actually run; in `manual` mode the helper reports an internal status but leaves `machine_gate_status` null. Selection references must match the parsed source SHA-256. The gate checks source/selected IDs, point-to-cue structure, one allowed role for each selected cue, required flag structure, and literal terms in the formal word bank. `risk_hint` is passed through as information and never becomes a hard failure. `assemble` preserves selected source text and sequence, computes continuous-group SRT spans or summed duration-text rows, divides by 1.2 once and rounds the final playback duration once to milliseconds, then returns one `playback_duration_display` for reuse in the first and third output parts.

The `diff` command compares point-pool IDs, support/evidence/condition IDs, roles, flags, selected sequence/order, angles, and supplied hard-rule outcomes. A different source SHA-256 produces `BLOCKED`. The report marks semantic review as still required; changes are evidence for review, not an automatic semantic pass/fail. AI still reviews point-pool completeness, source support, conditions, attribution, transitions, and stable hard-rule conclusions.

If Python or the script is unavailable, continue manually when the text is reliable, report “模型逐条对照”, and do not claim a script check.

## Optional legacy direct-term guard

`prohibited_term_guard.py` is the compatibility CLI for direct formal-term scans. The unified `srt_tools.py` path is preferred when source range accounting, cross-cue direct matching, selection validation, or deterministic assembly are needed. Both use the formal term list only; neither makes semantic judgments. If unavailable, continue with the AI-first manual scan.

Example: `python scripts/prohibited_term_guard.py input.srt --selected-ids 12,18 --final-text final-copy.txt`

Exit code `0` means no direct hit was found in the selected cues or final text; `1` means selected content or final copy contains a direct formal term; `2` means invalid input or invocation. A scan without `--selected-ids` reports every cue hit and never edits the source. The guard does not decide semantic equivalence, product facts, context risk, or point coverage, and it never removes adjacent cues automatically.
