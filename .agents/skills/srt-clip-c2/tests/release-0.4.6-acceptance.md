# C2 Universal 0.4.6 Release Acceptance

- Core version: `0.4.6`
- Plugin package version: `0.4.20`
- Acceptance: **PASS** for active-source integrity, execution-entry parity, package assembly and automated regression tests.

## Execution entry

- Each trigger requires a fresh complete read of the active `SKILL.md` and the six required references. If a required source is missing or incomplete, formal output is blocked and the missing source must be reported.
- The exact protocol is aligned across the two plugin manifests, the skill launcher and the portable wrapper. The portable generator sources its protocol from `plugin.json`.
- `SKILL.md` now states the per-trigger complete-read requirement at the beginning. The matching plugin prompt is preserved; active business rules are unchanged apart from removing superseded historical narration.

## Tests and package

- `python3 -m unittest discover -s skills/srt-clip-c2/tests -q`: **87 tests passed, 0 failed** in the source tree and extracted release ZIP.
- ZIP integrity: **44 files**, no Python cache artifacts.
- Current 0.4.6 regression record remains available at `real-source-regression-0.4.6.md`; the original 296-row source was not rerun for this package update.
- Obsolete 0.4.5 active checks and duplicate acceptance records were removed from the current distribution.
