# SRT Clip C2 Universal 0.3.4

AI-first, cross-platform commerce video clipping skill.

- Formal input scope: SRT and line-by-line duration text.
- Universal commerce core with category-specific modules loaded on demand.
- No mandatory Python, no mandatory JSON ledgers, no repeated workflow gates.
- 1.2x estimated final duration hard cap: 120 seconds.
- Fixed five-part output with original wording and source cue IDs.
- MP4/video/audio validation is deferred to future platform-specific adapters.

Start with `skills/srt-clip-c2/SKILL.md` (plugin package) or `.agents/skills/srt-clip-c2/SKILL.md` (GitHub/Codex repository).

- Long Context Mode：超长文本采用全局扫描→窗口地图→目标精读→单一卖点池→反向漏检→一次分析多方案；不强制依赖Python或环境。
- AI-First Constitution：所有语义决策必须由AI完成，工具只能辅助机械读取/定位/计算。
