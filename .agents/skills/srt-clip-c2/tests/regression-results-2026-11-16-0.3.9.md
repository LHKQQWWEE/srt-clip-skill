# C2 Universal 0.3.9 regression record — 2026-11-16

Business baseline: GitHub main 4aa3de2a3b7b2d870766c1417a4f0619e1e0d96a and private plugin release pluginrel_6af9d5bd6a9c8191b47d9f2895c38fef (0.3.8).

- Original plugin: 25/25 unittest checks passed.
- Original repository: 22 passed, 3 errors locating .agents/plugin.json or VERSION. This pre-existing harness layout issue was fixed by finding the manifest-owning ancestor.
- 0.3.9 repository: 25/25 passed.
- 0.3.9 complete plugin directory: 25/25 passed.
- 13 business/governance files (SKILL, all references and categories) equal both original owning sources after release-number normalization only. See docs/business-equivalence-0.3.9.json.
- Existing semantic-contract, global cue-exclusion, topic/category, 120-second, five-part, AI-First and synthetic 2000-cue/window checks retained. These are structural/mechanical checks, not independent AI behavioral evaluation.
- Publisher defaultPrompt is preserved completely at 0.3.8, not rewritten to 0.3.9. Test expectation now honors that immutable compatibility field.
- Historical audit/result bodies retained below explicit ARCHIVED_DO_NOT_EXECUTE notices. Case-colliding original paths mapped to docs/history/legacy-uppercase-audit-2026-11-15.md and legacy-lowercase-audit-2026-11-15.md.
- Untested: real transcript AI blind scoring, real audio/video, actual platform moderation, end-to-end timing, other model hosts and refreshed installed runtime.

No claim of all-channel completion is made by this static test record. See final channel readback report.
