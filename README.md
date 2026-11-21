# SRT Clip C2 Universal 0.4.6

C2 is an AI-led purchase-decision editor with one semantic analysis and one final audit. It reads the full target-product context, identifies every valid independent purchase point, then compares complete candidate paths without anchoring on the first strong point.

Every delivered video must independently cover the full valid point set and its necessary evidence or conditions. The union of several videos is only a secondary consistency check. When multiple differentiated videos are possible and the user has not specified a count, recommend the themes and count, then wait for the user's choice before producing them.

Direct formal prohibited terms are scanned against the single list in `skills/srt-clip-c2/references/global-rules.md`; only matching full cues are excluded. The user's newly designated `羊毛` term is unconditional. `羊绒` is independently prohibited; static-control wording and nearby cues remain outside the ban. The optional guard script performs literal matching only; AI remains responsible for semantic and factual judgment.

Duration is a planning reference, not a task completion condition. Keep the 45-second general lower-bound guidance, short-cut quality exception, and no fixed upper limit. See [START-HERE.md](START-HERE.md) and the skill references for the complete contract.
