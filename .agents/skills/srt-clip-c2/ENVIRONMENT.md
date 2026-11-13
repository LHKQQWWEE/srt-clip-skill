# C2 0.2.20 environment

- Python 3.10 or newer is required for the bundled validation scripts. The package was tested with Python 3.12.
- Runtime and validation use only the Python standard library. No `pip install` step or network access is required.
- Run the bundled acceptance check from this skill directory with `python -S tests/test_portable.py`.
- The `scripts/` and `tests/` directories are included in the ZIP so parsing, source checks, rendering, and acceptance checks are available offline.
- Same-cue sentence edits require the exact `sentence_edits` source partition and matching exception ledger through `scripts/multi_plan.py`; the direct compact renderer refuses partial-sentence output without that trace.
- Video/audio decoding and speech recognition are not bundled. Video claims must be limited to media actually readable in the host environment.
