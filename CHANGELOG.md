# Changelog

## 0.3.2
- Changed content-density policy: within the 1.2x 120-second hard cap, maximize coverage of distinct product selling points and useful highlights.
- Same selling point may retain up to two different original excerpts when the second adds reinforcement, evidence, conditions, emotion, or better transition.
- When trimming for duration, remove unrelated content first, then the second reinforcement of repeated selling points, then low-priority secondary highlights; core selling points are last to cut.
- Synced runtime default prompt to the current Universal version instead of stale 0.2.26 wording.

## 0.3.2
- Rebuilt as C2 Universal with an AI-first, platform-independent core.
- Formal cross-platform input scope is SRT and line-by-line duration text; MP4 is deferred.
- Preserved the 1.2x, 120-second hard cap, original wording/source IDs, product attribution, offline compliance baseline and five-part output.
- Removed generic trigger `切片文案`; retained exactly four C2 triggers.
- Removed mandatory per-cue JSON ledgers, multi-stage workflow gates and repeated Python checks.
- Added category auto-detection and a separate women's-fashion module.
- Added one-pass final review with reverse coverage check.
- Added anonymized benchmark scenarios; raw historical SRTs are not included in the repository or release package.
