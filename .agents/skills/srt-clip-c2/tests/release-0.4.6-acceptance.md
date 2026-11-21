# C2 Universal core 0.4.6｜plugin package 0.4.23 first-round acceptance

## Scope and source baseline

- Package target: `0.4.22 → 0.4.23`; core remains `0.4.6`.
- Rule source: the local 0.4.22 plugin cache snapshot, recorded by raw-byte hashes in [`c2-p0-baseline.md`](../../../docs/acceptance/c2-p0-baseline.md). The Git checkout originally tracked 0.4.15; the cache snapshot was used so the current 0.4.22 rules were the implementation baseline.
- Worktree: `codex/c2-p0-first-round`. No plugin, GitHub, or other external publication was performed.
- Semantic rule text was preserved except for the agreed operational wiring. Full rule files remain the sole rule source; no consolidation or separate rule-map artifact is part of this candidate.

## Implemented changes

- The runtime manifest is the only required-reference list. Entry consistency and path-completeness tests protect it; the entry does not hard-code a file count or duplicate the list.
- Optional `srt_tools.py` parses SRT and numbered duration text, preserves cue text and unparsed raw blocks, reports parsed/total counts, exact line ranges and reasons, mechanical diagnostics, direct hits, compact three-column rows, and timeline support. A HIT row remains visible; selecting a direct formal-term hit fails.
- The real attached duration-text regression exposed two exact leading paste labels being treated as malformed rows. The parser now reports `srt文案` and `【字幕列表】` as recognized input metadata, excludes them from cue counts, and still leaves any other unrecognized row BLOCKED.
- A source-bound selection JSON drives structural gate, source-word assembly, continuous-group/duration-text timing, and fifth-part sequence. The same `playback_duration_display` is reused in parts 1 and 3. `manual` mode reports internal status without claiming machine validation.
- The gate passes `risk_hint` through without elevating it to a hard failure. A fixture places “特殊纤维/防静电” next to a direct “羊毛” hit and confirms the selected risk cue passes the formal-term gate.
- Candidate comparison retains complete sequence, one-sentence angle, point-to-cue support mapping, necessary evidence/conditions, six-dimension results, and source-checked jump records. Losing candidate transcripts are not expanded. AI owns all meaning and transition decisions.
- The semantic replay protocol distinguishes identical-JSON mechanical reproducibility from two-pass semantic stability and produces a support/condition/role/rule diff.
- The fixed five-part output remains. Part 1 uses one short template; ordinary omitted-content notes are capped at three one-line items; risks, facts to verify, and key limits are separate exceptions. Repairs are local.

## Verification

- Pre-change 0.4.22 baseline: 89/89 tests passed.
- Post-change full suite: `python -m unittest discover -s tests -v`, **128 tests passed, 0 failed**.
- Portable package generation succeeded; manifest/metadata, portable-embedding, schema JSON, and replay JSON integrity checks passed.
- Same selection JSON produced identical assembly and gate reports. The synthetic A/B review retained the same point pool, conditions, roles, flags, and formal-word conclusion; the generated diff explains an evidence-to-support mapping change. The adjacent special-fiber/anti-static risk case produced **0 mechanical risk-to-hard-fail false positives**.
- Real attached sample (kept outside the repository): **509/509** numbered duration rows parsed, zero structural diagnostics, zero unparsed rows, cumulative duration **789,114 ms**, and byte-identical preprocessing reports on repeat. Direct formal hits were `羊毛`: 54, 186, 188, 229; `羊绒`: 54, 186, 188, 228. A source-bound assembly smoke test on cues 73–74 reproduced the original text and computed 4,000 ms source / 3,333 ms at 1.2x. Cue 509 ends mid-phrase (“你想要面料稍”) and remains a semantic completeness warning; it was not promoted into a machine parse failure.
- A real-material independent AI replay has not been performed; the checked-in A/B records are authored synthetic expected outputs, as detailed in `semantic-replay-acceptance.md`.
- The attached sample includes multiple product windows; no single-product five-part clip was issued because the regression request did not identify a target product. Audiovisual verification, external publishing, and host reload were not performed.

## Acceptance boundary

This package is the locally tested first-round candidate. The real-source failure was an input-wrapper parsing issue and was fixed in the parser; this regression showed no unresolved rule conflict or context-limit failure requiring rule consolidation. No separate consolidation work remains in this candidate. Seconds saved and percentage estimates are not acceptance thresholds.
