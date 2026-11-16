# C2 Universal 0.3.11 — purchase-value coverage and arrangement

- Baseline: 0.3.10; business update, same single C2 Universal line.
- Added a cross-category rule: any new, valid purchase-decision information remains a candidate, regardless of theme or category.
- Semantic deduplication now depends on information gain. Same-category but distinct facts remain separate.
- Multi-point arrangement may use natural fact/benefit, question/answer, attribute/use, and other source-supported relations. Real contrast receives only a light priority boost; no conflict is invented.
- Time-cap trimming now removes true duplicates, empty praise, lower-value content, and fully covered secondary details before independent valuable points.
- Kept the existing hook/middle/ending system, category-specific rules, compliance boundaries, 1.2x estimate, 120-second cap, and five-part output.
- Ordinary task architecture remains AI-First: no added model turn, Python prerequisite, JSON ledger, separate outline, or extra omission scan.
- Long-context window mapping remains for input coverage; target-window semantic selection and arrangement are integrated.

## Verification

- Static regression suite: pending at publication time.
- Synthetic scenario matrix: authored for apparel, same-category facts, duplicates, authentic/no contrast, over-cap, short/long, multi-product, non-apparel, and category specialists.
- End-to-end latency and live model generations: not measured.

## Sync status

- GitHub main: pending.
- Installed plugin/skill: pending.
- Portable package: pending.
- Drive release index and ZIP: pending.
