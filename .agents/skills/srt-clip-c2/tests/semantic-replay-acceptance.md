# C2 semantic replay acceptance

This protocol separates repeatable mechanical evidence from AI semantic judgment. Fixtures are synthetic; real-source findings are recorded separately in `real-source-regression-0.4.7.md`.

## Layer 1: mechanical repeatability

Run `preprocess`, `check`, and `assemble` twice on identical source bytes and the same selected-cut record. Source SHA-256, structural diagnostics, assembled original text, source sequence, and any displayed duration estimate must match. Duration is informational only and is never an acceptance threshold or split trigger.

Every parse gap remains visible. An unresolved range stays BLOCKED, and an unparsed cue cannot be treated as a confirmed source ID. Direct formal-term hits exclude only their complete source cue; neighboring cues remain independently reviewable.

## Layer 2: semantic stability on the same source

Review the A/B selection records against the same complete source and current rules. The diff compares the full valid point pool, supporting source IDs, necessary evidence/conditions, product attribution, exact-rule outcomes, opening-only choices, and each actual selected cut. Plan count, independent purchase cores and per-plan coverage are semantic checks, not script decisions.

Stable findings must include:

- the same complete pool at the same semantic granularity;
- the same required evidence, conditions, ownership, and hard-rule boundaries;
- opening candidates compared only as openings and necessary adjacent responses, with empathy first;
- default two materially distinct plans with real independent purchase cores, unless the user starts with “单条” or “按推荐版” or a second plan would lack independent purchase value or lower quality;
- every plan independently arranges the full point pool and required evidence/conditions; union coverage is invalid;
- duration is calculated after full arrangement; at or below the slight-overrun region every valid point is retained, while only a clearly over-120-second complete plan may use core-specific dynamic selection and must list omitted valid points;
- optional cache loss does not invalidate a current persistent execution summary; a missing, mismatched or stale summary requires reading source rules and refreshing it;
- applicable compliant source CTA retained verbatim; no new or rewritten CTA when the source has none;
- final audit limited to the selected cuts actually written.

An evidence/support change can be valid when the source supports it. An unexplained lost point, condition, product boundary, or changed hard-rule outcome is a failure. The support diff is a review aid and never makes semantic decisions.

## Synthetic fixture review

The checked-in A/B records use the same short synthetic source and retain the same complete point pool, condition, product attribution, flags, and formal-rule conclusion. They differ only in source support and playback ordering. The generated diff reports those changes without comparing full-cut candidates. The direct-hit cue is omitted in full, while its adjacent risk hint remains informational and does not become a mechanical hard failure.

These are authored expected outputs, not claims of multiple independent production-model runs. Real-source regression and scope limits are recorded in `real-source-regression-0.4.7.md`.
