# C2 Universal 0.4.3 Validation Record

Date: 2026-11-19

Baseline confirmed from the installed Skill: C2 Universal 0.4.2. Plugin package baseline: 0.4.9.

## Changes checked

- Duration: removed the fixed 120-second ceiling; retained a general 45-second lower-bound guide with a quality-gated exception for genuinely short source material.
- Coverage: important independent purchase reasons are assessed qualitatively, with neither automatic 100% coverage nor a second full-source scan.
- Multi-cut behavior: default one best cut; proactively mention materially different, independently valid paths; create full alternatives only after the user requests them.
- Preserved dynamic structure, early purchase opportunities, repetition rules, role boundaries, AI-First operation, source wording, and five-part output.

## Real transcript fixture

粘贴的文本 (1)(5).txt — 609 numbered cues, 827.115 seconds total cue duration, target shoe product. One best 49-cue edit is 79.559 seconds source time / 66.299 seconds estimated at 1.2x. Independent alternatives were checked at 55.666 seconds (concealed height and outfit) and 50.199 seconds (wide-foot fit and autumn/winter wear). The normal output remains one best cut and only mentions the alternatives. Conflicting size advice and transaction-context-dependent lines are not detached.

The sample's best cut is under two minutes. The regression therefore checks removal of the upper-bound rule in policy and release tests; it does not claim a >120-second real cut was produced.

## Automated test results

- 62 tests passed, 0 failed across early purchase opportunity, long-context handling, product knowledge packs, purchase-reason policy, repetition semantics, role architecture, and release integrity.
- The real transcript cross-check confirmed all 125 selected cue references exist, each selected quote matches the source text exactly, and the 49/39/37-cue totals and 79.559/66.799/60.239-second source durations reproduce the prior report.
