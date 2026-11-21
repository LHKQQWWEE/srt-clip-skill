# C2 P0 first-round baseline

## Baseline scope

- Rules snapshot: installed plugin cache `D:\codex\.codex\plugins\cache\created-by-me-remote\srt-clip-c2\0.4.22`.
- Core version remains 0.4.6. The plugin 0.4.22 cache is the semantic baseline; the Git source checkout began at plugin 0.4.15 and was not treated as the rule baseline.
- Baseline suite: 89/89 tests passed against the imported 0.4.22 snapshot before P0 changes.
- Hashes below were recalculated from the cache snapshot's raw bytes on 2026-11-21. SHA-256 is the reproducible identity; byte and line counts are diagnostic only.
- `references/runtime-manifest.json`, `scripts/srt_tools.py`, and `scripts/selection.schema.json` did not exist in this baseline; they are new P0 artifacts.

| Baseline file | Bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `plugin.json` | 3099 | 31 | `5f8c5dd8731a6c6215c579e972d72596016ce4a79ee56694e1e55e225fc4c571` |
| `.codex-plugin/plugin.json` | 4988 | 26 | `9827817ea75aef68186fa2d47c1f7f9f95d246bdca839697f5ba8f063f67a45e` |
| `skills/srt-clip-c2/SKILL.md` | 18633 | 121 | `cbb610d264bdbe056d4384e08bf528e669e17c12b89ac08cc046c562a32098e4` |
| `skills/srt-clip-c2/references/ai-first-constitution.md` | 4020 | 53 | `d5edb790c450c748a0a6cd79ef7c644c91f1ccc9c7a3a4f439ecb807774a37ab` |
| `skills/srt-clip-c2/references/global-rules.md` | 7887 | 54 | `ee2b1a223ddfe16670dc5bc46669ee1750d3e2d0b86db1e98513338b7c505bf6` |
| `skills/srt-clip-c2/references/editorial-policy.md` | 16438 | 121 | `4befb0b168da6872e691b65ef40be3b68d17122b5b10d996b12fa5e0b9b3fa7d` |
| `skills/srt-clip-c2/references/highlight-selection.md` | 12018 | 75 | `c61235bc69af34fe4bdd793c558c43d40e24749ae3f4b0df3193bd9d63f8843c` |
| `skills/srt-clip-c2/references/final-check.md` | 11371 | 68 | `05a119abe3a9749caba8b2ce653f21d5ec39aada50d777ddb3bd17c00d3a592b` |
| `skills/srt-clip-c2/references/product-knowledge-registry.md` | 2351 | 31 | `6737b6c8df8e6fbcdccc4a30439f66ae15f3a2fb09efb380bd285e7437fce19d` |

## Reproduce the baseline

From an unchanged 0.4.22 cache copy, run:

```text
python -m unittest discover -s tests -v
```

Expected baseline result: 89 tests passed. This records the pre-change rule and package suite only; it is not a performance threshold or semantic replay result.
