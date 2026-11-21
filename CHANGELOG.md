## Plugin package 0.4.18 / C2 Universal core 0.4.6 (2026-11-21)

- Synchronized the fail-closed entry protocol across plugin manifests, the skill launcher and portable wrapper. Every trigger requires a fresh, complete read of the active SKILL.md and six required references; missing or incomplete files block formal output.
- Kept the active Skill and business rules unchanged; no core rule or SKILL.md body changed.
- Added regression checks for protocol parity and package contents. Removed superseded release-history files and obsolete 0.4.5 checks from the current distribution; Git commit history remains available for traceability.
