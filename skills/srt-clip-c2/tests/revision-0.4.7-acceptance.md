# C2 Universal 0.4.7 / Skill 0.4.27 regression acceptance

Status: executed on 2026-11-22. This is test evidence, not runtime policy.

## Baseline observed before rule changes

Three fresh-context samples were run against the 0.4.26 rules before changes:

- Multi-video: the sample recommended two themes, then asked the user to choose and paused.
- Duration: for a 132-second complete draft, the sample retained all four points because duration “does not participate in acceptance, deleting points, or splitting.”
- Summary reuse: the sample required rereading SKILL.md and runtime-current.md despite an exact-version summary with matching rule hashes.

These are before-change observations, not results for 0.4.27.

## Post-change evidence

The following semantic scenarios were independently reviewed against Core 0.4.7 / Skill 0.4.27:

1. **Normal duration (51.6 seconds):** default dual plan proceeds without pause. Two distinct purchase cores were identified: color/daily use and styling/fit. Each separately covers candidate points P1–P10. Ambiguous ASR fragments remain flagged and are not treated as verified facts.
2. **Clearly over 120 seconds:** a 154.8-second derived stress scenario drafts each full arrangement first, then evaluates each plan against its own purchase core. Two materially different plans have cue sets, plan-specific omissions and reasons; neither relies on union coverage.
3. **Slight overrun:** the 123.84-second derived scenario does not trigger automatic deletion. Necessary information can remain and a necessary plan may exceed 120 seconds.
4. **Single-plan instruction:** “按推荐版” directly returns one recommended plan with no dual-plan pause; this does not imply that a second core is invalid.
5. **Second plan invalid:** scoped only to source cues 1–4, one independent color-choice core exists. A second plan would repeat or fragment that reason, so the simulated result gives one plan and explains why. This does not claim the full transcript lacks another valid core.
6. **Summary lifecycle:** automated tests cover first generation, valid reuse, invalidation on Skill/rule hash change, and continued use of a valid persistent summary when optional cache is absent.
7. **Protected behavior:** the full unit suite exercises source cue integrity, product attribution and confirmation, prohibited-term boundaries, risk versus hard block, repetition, purchase structure, opening priorities, source-only CTA, fixed output structure, AI-first behavior and minimal tool use.
8. **Real-source mechanics:** the current parser returned 34 cues, IDs 1–34, 51.6-second span, 0 structural diagnostics and 0 unparsed ranges. Formal prohibited-term scan completed with 0 direct hits and 0 excluded cues.

## Validation and limitations

- Full unit suite, rerun after report edits: 145 tests passed (8.605 seconds).
- Runtime manifest/source check: passed; runtime bundle and source map are current.
- Persisted summary validation: state=valid for Skill 0.4.27/Core 0.4.7, requires_full_read=false.
- An initial fresh-context long-form response was rejected because cue 30 was both retained and omitted and the duration arithmetic did not reconcile. It was rerun in a clean context; only the consistent rerun is counted.
- Derived duration scenarios are rule stress checks, not measured edits or model-performance data. No audio/video, ASR accuracy, report/product fact, actual export or platform outcome was checked. No cross-model consistency or end-to-end editing claim is made.
