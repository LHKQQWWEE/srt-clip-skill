# Development, build, and test tools

Everything in this directory is for development, build generation, or release regression tests. Routine SRT and duration-text work never calls Python, these scripts, a CLI, or a JSON pipeline. Daily work uses the host AI's native text reading and exact source-by-source comparison.

## Development-only unified preprocessing tool

`srt_tools.py` is a development-only standard-library helper for lossless parsing, deterministic assembly, structural gate checks, and support-map diffs. It never decides product identity, selling-point meaning, evidence sufficiency, semantic equivalence, transition continuity, or candidate quality.

Examples:

```text
python scripts/srt_tools.py preprocess input.srt --output report.json
python scripts/srt_tools.py assemble input.srt selection.json --output assembly.json
python scripts/srt_tools.py check input.srt selection.json --final-text final-copy.txt
python scripts/srt_tools.py diff replay-a.json replay-b.json
```

The preprocessor includes parsed/total block counts, exact parsed and unparsed line ranges, reasons, numbering/time diagnostics, row durations, a compact three-column `id|start-end|source text` table, direct formal-term hits, confirmed-equivalent hits, contextual candidates, explicit contextual block/allow/unresolved outcomes, and review-only ASR-like near forms. It reads the structured registry from `references/global-rules.md`. Registered context examples such as product rankings/claims and allowed ordinal or schedule wording are tested against narrow patterns; unclear context and suspected ASR forms are only reported. A direct or confirmed contextual product claim is marked `HIT` in the ID cell and listed in `excluded_full_cue_ids`; only that full cue is affected. Each cue is scanned independently; neighboring cues are never combined. Unparsed ranges are `BLOCKED` and cannot be described as fully checked. Timeline rows do not assign product identity; that remains an AI judgment.

The selection object follows `selection.schema.json` and represents one actual user-selected final cut. It is not used for a pending multi-video checkpoint; that state remains in the current conversation and creates no JSON gate. `verification_mode` is `script` only when the helper is actually run; in `manual` mode the helper reports an internal status but leaves `machine_gate_status` null. Selection references must match the parsed source SHA-256. The gate checks source/selected IDs, point-to-cue structure, one allowed role for each selected cue, required flag structure, direct formal terms, explicitly registered equivalents, and contextual absolute claims covered by the registry's confirmed boundaries; it rescans final text as well. Unresolved context and ASR-like near forms set review fields but are not automatically blocked. No evidence-based exemption is implemented. The `适用促单原话` role marks source wording that must remain complete when applicable and compliant. `risk_hint` is passed through as information and never becomes a hard failure. `assemble` preserves selected source text and sequence, computes continuous-group SRT spans or summed duration-text rows, then divides the accumulated source duration by the fixed whole-clip speed of 1.2. The same speed applies to the opening attention reference. The target is 90 seconds after conversion and the 100-second acceptable reference triggers review only when exceeded before display rounding. Review can retain every selected cue. The legacy `known_unaccelerated_ms` annotation does not enter the estimate. The estimate is approximate and cannot trigger splitting or truncation; one shared `playback_duration_display` is reused in the first and third output parts.

The `diff` command compares point-pool IDs, support/evidence/condition IDs, roles, flags, selected sequence/order, angles, and supplied hard-rule outcomes. A different source SHA-256 produces `BLOCKED`. The report marks semantic review as still required; changes are evidence for review, not an automatic semantic pass/fail. AI still reviews point-pool completeness, source support, conditions, attribution, transitions, and stable hard-rule conclusions.

These commands must not be used for routine SRT execution.

## Development-only prohibited-term guard

`prohibited_term_guard.py` and `srt_tools.py` share the structured formal registry for development regression. They separate direct hits, confirmed equivalents, narrow contextual claim matches, allowed contexts, unresolved phrases, and one-edit ASR/typo suspicions. ASR suspicions never become formal hits. They enforce explicit allowed-expression protection and scan one subtitle cue at a time; they do not infer unregistered synonyms or expand the dictionary.

Example: `python scripts/prohibited_term_guard.py input.srt --selected-ids 12,18 --final-text final-copy.txt`

Exit code `0` means selected content and final copy have no confirmed direct or contextual claim hit (or the invocation is a raw scan with exclusions reported); `1` means selected content or final copy contains a confirmed hit; `2` means invalid input or an unresolved-context review is required. A scan without `--selected-ids` reports full-cue exclusions and review-only items but never edits the source. The guard does not decide product identity, unregistered semantic equivalence, product facts, or point coverage, and it never removes adjacent cues automatically.

## Canonical-to-mirror sync (development only)

Maintain skills/srt-clip-c2 as the canonical Skill tree. After rebuilding generated files, run scripts/sync_skill_mirror.py from the canonical Skill directory to replace the .agents mirror from that source. The sync ignores Python caches. Verify the two trees with the mirror regression before creating the Skill-only ZIP. This script is never part of routine SRT execution.
