# C2 Universal 0.4.6 Release Acceptance

- Core version: `0.4.6`
- Plugin package version: `0.4.13`
- Acceptance: **PASS** for local rules, program tests, portable package assembly and the 296-cue real-source regression. External sync status is recorded below only after remote read-back.

## Verified changes

- `羊毛` is a direct, unconditional formal prohibited term. Unicode compatibility normalization and removal of spacing/punctuation catch variants such as `绵 羊-毛`. Matching excludes only the complete matched cue. `羊绒` is independently prohibited as of the later update; `特殊纤维`, anti-static wording, and adjacent cues remain outside the formal list.
- Every video independently covers the full valid point set and necessary evidence or conditions. A multi-video union is an extra consistency check and cannot compensate for omissions. When video count is unspecified, the skill recommends count/themes and waits for the user's selection before generating multiple cuts.
- Duration is not a task-completion condition. The 45-second reference, quality-gated short exception and no fixed upper ceiling remain.
- Acceptance states are PASS / FAIL / BLOCKED; each same-root-cause repair is capped at three substantive rounds, with the failing test and full acceptance rerun.
- The optional standard-library scanner reads only the formal list. It does not edit source, infer semantic equivalents, or replace AI fact and coverage review.

## Tests and real-source regression

- Baseline before edits: 79 existing tests passed on core 0.4.5 / plugin 0.4.12.
- Upgrade test-first state: five new tests failed against the baseline as expected.
- Focused upgrade tests after repair: 5 passed.
- Full suite after the final repair: `84 tests passed`.
- Real source: 296 rows, SHA-256 `F77115F984D262076287574BD7047C81A064EDABA7E9BE18C1F23377F24045D9`; direct hits were `106,107,111,112,171,172,179,226,227,228,231`.
- First real candidate check returned FAIL with direct hits. The candidate was repaired by removing the full matched cues. Recheck returned PASS with no selected-cue or final-text hits. The complete semantic mapping and evidence are in `real-source-regression-0.4.6.md`.
- Raw SRT was not copied into release contents.

## Final decision

Local acceptance: **PASS**. Remote publication and artifact URLs are recorded separately in the delivery report after each channel is read back.
