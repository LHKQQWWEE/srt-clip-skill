# C2 semantic replay acceptance

This replay separates exact tool reproducibility from semantic stability. The fixtures are synthetic and do not establish product facts or replace a real-source quality review.

## Layer 1: identical selection JSON

Run `preprocess`, `check`, and `assemble` twice against the same source bytes and the same selection JSON. The source SHA-256 must match. The complete gate JSON, assembled original text, `source_sequence` / `fifth_part_sequence`, source duration, playback duration, and `playback_duration_display` must be byte-for-byte identical. The first and third delivery parts reuse that one displayed duration field.

Any parse gap must remain visible in `parsed_ranges` / `unparsed_ranges`; unresolved ranges remain BLOCKED. A selection that points into an unparsed range cannot be treated as a confirmed source ID. Known parsed cues remain present and inspectable.

## Layer 2: two semantic passes on the same source

Review `runtime-replay-selection-a.json` and `runtime-replay-selection-b.json` as two independent AI passes using the same complete source and current rules. Run `srt_tools.py diff` and keep the generated support-change diff with the review notes.

The generated diff reports point-pool IDs, direct support IDs, necessary evidence/conditions, cue roles, flags, selected IDs, angles, and supplied hard-rule outcomes. These items must remain stable:

- the complete effective selling-point pool and its granularity;
- the necessary evidence, conditions, ownership, and hard-rule conclusions for each point;
- each point's source support being genuine in context;
- direct formal-term hits remain excluded, while the adjacent special-fiber / anti-static risk hint stays a hint and is never promoted to `hard_fail`;
- every discontinuity in each candidate path has a source-checked `prev_id → next_id` review for referents, object, and conditions; failed transitions disqualify that candidate.

The angle and ordered sequence may differ when both candidates remain complete and eligible. For every support change, explain which cue was added or removed and why the source supports the revised mapping. A changed support ID alone is not proof of semantic instability; an unexplained lost selling point, condition, ownership boundary, or changed hard-rule outcome is a failure.

The support diff is a review aid, not an automatic semantic pass. `risk_hint` is never a machine hard failure. A machine failure caused only by a risk hint blocks release until corrected.

## Synthetic fixture review

The checked-in A/B records use the same six-cue synthetic source. Both keep the same four-point pool, washing condition, cue roles, risk/fact flags, and formal-word conclusion. B changes the order and maps cue 2 directly as support where A lists it as necessary evidence for P1; the generated diff shows both deltas without losing the underlying cue. B has two source-order discontinuities, `3 → 1` and `2 → 4`; both were checked against the original cue text for referents, product object, and conditions. Cue 6 directly hits “羊毛” and is omitted; cue 5's neighboring anti-static claim remains a `risk_hint` and the machine gate reports no hard failure.

These are authored synthetic expected outputs reviewed against their source, not two independent runs of a production host model. A real-material semantic replay remains a separate acceptance check when suitable source material is available.
