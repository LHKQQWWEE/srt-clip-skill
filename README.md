# SRT文案与SRT切片文案｜C2 0.1.5

本仓库只保留一个权威 Skill，路径为 [`.agents/skills/srt-slice-copy/SKILL.md`](.agents/skills/srt-slice-copy/SKILL.md)。旧根目录副本、重复的 `srt-clip-c2` 技能副本及 V3.0/R8 历史规则包已从当前版本移除。

统一触发词：`srt文案`、`srt切片文案`、`str文案`、`C2完整精简版`。全部执行 C2 0.1.5 唯一规则。

- 完整、结构适中的短文本直接处理，不启动脚本。
- 长附件、可能截断或累计计算复杂时，采用一次扫描、一次 AI 选段、一次定稿核验。
- 未实际执行脚本时，不报告程序核验通过；逐条时长文本位置只作累计估算。
- 只处理 SRT 或逐条时长文本，不处理 MP4；视频/原声流程保持独立。

## 在 Codex 中使用

克隆本仓库后，项目级 Skill 位于 `.agents/skills/srt-slice-copy/`。个人安装时，将该目录复制到 `$CODEX_HOME/skills/srt-slice-copy/`。