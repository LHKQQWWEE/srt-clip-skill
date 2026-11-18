# SRT Clip C2 Universal 0.3.20｜开始使用

唯一执行入口是当前 `SKILL.md` 与它引用的文件。插件、原生 Skill、文件导入和纯文本便携版均使用 **0.3.20**；不要混用旧版本、旧启动提示或其他同名副本。

- 输入：SRT 或逐条时长文本；MP4 不属于跨平台正式音画核验范围。
- 触发词：`srt文案`、`srt切片文案`、`str文案`、`C2完整精简版`；通用词 `切片文案` 不是 C2 触发词。
- 功能身份：带货短视频购买决策编辑器，由 AI 比较和编排原话，服务陌生顾客的购买判断。
- 通用结构只由 Universal Core 决定；类目文件只保留商品专项判断。
- 正式成片按 1.2 倍速预计 45–120 秒；45–90 秒优先，90–120 秒只在仍有独立高决策价值内容时扩展。低于45秒且无有效内容可补时，交付短候选，不灌水。
- AI 主导一次语义分析与一次终检；普通任务不依赖 Python、JSON、联网或额外模型轮次。
- 固定五部分输出；保留原话、原始序号、商品归属和必要条件。

Plugin package path: `skills/srt-clip-c2/`. Repository source path: `.agents/skills/srt-clip-c2/`. Pure-text users may use the current `C2-Universal-Portable.md`.
