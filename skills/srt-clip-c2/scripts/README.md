# Optional tools

C2 Universal does not require or bundle a Python runtime script for ordinary SRT or duration-text tasks.

Use the host AI's native file reading and calculation capabilities by default. Optional utilities may be added when they materially improve a specific mechanical task. They must never become a normal-task gate or require a JSON/workflow pipeline.

## Optional direct-term guard

`prohibited_term_guard.py` mechanically scans standard SRT cues or numbered duration-text rows against only the literal terms listed under `## 正式禁用词库` in `references/global-rules.md`. It normalizes Unicode compatibility forms and spacing/punctuation before direct matching. Use it when convenient for a complete mechanical scan; if unavailable, continue with the AI-first manual scan.

Example: `python scripts/prohibited_term_guard.py input.srt --selected-ids 12,18 --final-text final-copy.txt`

Exit code `0` means no direct hit was found in the selected cues or final text; `1` means selected content or final copy contains a direct formal term; `2` means invalid input or invocation. A scan without `--selected-ids` reports every cue hit and never edits the source. The guard does not decide semantic equivalence, product facts, context risk, or point coverage, and it never removes adjacent cues automatically.
