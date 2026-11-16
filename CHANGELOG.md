## 0.3.10 (2026-11-16)

- Added the phrases identified in the 2026-11-16 material-proof rejection screenshot to the single global clipping prohibition library: “三股的全羊毛” and “全精纺羊毛”; “全金纺半高领” is covered only when its context makes it an animal-fiber material claim. A collar-style description alone is not prohibited.
- Updated the offline evidence reference to record the screenshot without duplicating or broadening the active prohibition rules.
- Regenerated the portable single-file skill and synchronized release metadata. Other C2 workflow rules remain unchanged from 0.3.9.
- See docs/release-0.3.10.md.

## 0.3.9 (2026-11-16)

Synchronization and cleanup only; business rules unchanged from 0.3.8. See docs/release-0.3.9.md.

# Changelog

## 0.3.8
- Simplified global banned-claim maintenance to two user-driven inputs: audit screenshots and explicitly specified phrases; no automated official-policy lookup in normal tasks.
- One shared prohibition library across all product categories. Confirmed matches exclude entire original subtitle cue IDs; continuous cross-cue matches only exclude contributing IDs.
- Incorporated identifiable historic material proof rejection wording as user clipping bans without broadening to unrelated materials.
- Reconciled main skill, womens-fashion, shoes, scarves, editorial policy, offline evidence, final check, launcher, and portable distribution. Preserved AI-First, one analysis/one final check, 1.2x/120s, original-source fidelity, five-part delivery.
- Publication status and regression results tracked by verified channel only.


## 0.3.7
- Added `categories/shoes.md` for all footwear: dynamic hooks, full core-selling-point coverage, size/foot-shape restrictions, claim classification, shoe variant attribution and video-context uncertainty.
- Added `categories/scarves.md` for scarves, fur neck warmers, silk scarves, shawls and neckwear: visual/feel/warmth/tying and layering, material attribution, care/sensitivity limits, and multi-item sales vs distinct buying reasons.
- Updated category routing to make shoes and scarves exclusive of womens-fashion editorial defaults; preserved two historical fashion hashtags for compatibility.
- Kept AI-First, tool-optional, source fidelity, same-selling-point two-excerpt cap, 1.2x 120-second hard cap, five-part output and offline compliance. No new daily tool or environment prerequisites.
- Rebuilt portable distribution and added focused route/scenario regression tests; manual real-video validation remains unverified.

## 0.3.6
- Publication-consistency patch: synchronized the complete portable single-file pack, Agent Skills launcher metadata, tests, and release ZIP with the 0.3.5 AI-First governance protocol.
- No new SRT editing semantics, tools, environment prerequisites, or daily workflow gates.
- Added explicit governance-only regression checks; historical 0.3.4/0.3.5 changelog sections remain immutable.

## 0.3.5
- Added a permanent AI-First version update protocol: six required checks, three veto rules, release records, and honest per-channel sync status.
- Governance-only update. No changes to the ordinary clipping execution flow, semantic decision ownership, 1.2x 120-second hard cap, or five-part delivery.
- Kept Python, scripts, and external environments optional for daily text tasks.

## 0.3.4
- Sync-integrity patch only; business behavior is unchanged from the fully tested 0.3.2 AI-First / Long Context release.
- Resolved plugin-publisher version auto-increment mismatch so plugin source, GitHub main, Drive current routing, and release ZIP use one active version.
- Preserved the current plugin-level defaultPrompt exactly for publisher compatibility; SKILL.md remains the authoritative active rule source.
- Cleaned stale current-version labels in archive and platform-adapter documentation.

## 0.3.3
- Transient publisher auto-increment encountered during same-business-rule resync. Superseded by 0.3.4; do not treat 0.3.3 as a distinct business-rule release.

## 0.3.2
- Added AI-First Constitution as the highest architecture constraint.
- Added Long Context Mode: global coverage scan → product window map → target-window deep read → single selling-point pool → reverse coverage check → Single Analysis, Multi Output → 120-second value packing → final check.
- Added long-text structural stress tests including a synthetic 2000-cue / 2-hour case.
- Fixed Universal topic leakage: #穿搭 and #时尚营销 belong only to the women/fashion module.

## 0.3.1
- Within the 1.2x / 120-second hard cap, maximize coverage of distinct product selling points and useful highlights.
- Same selling point may retain up to two different original excerpts when the second adds meaningful reinforcement.
- Trim order: unrelated/promo content → second reinforcement → low-priority secondary highlights → core selling points last.

## 0.3.0
- Rebuilt as C2 Universal with an AI-first, platform-independent core.
- Formal cross-platform input scope: SRT and line-by-line duration text; MP4 deferred.
- Removed generic trigger `切片文案`; retained exactly four C2 triggers.
- Removed mandatory per-cue JSON ledgers, multi-stage workflow gates, and repeated Python checks.
- Added category auto-detection, women/fashion module, five-part output, and one-pass final reverse review.
