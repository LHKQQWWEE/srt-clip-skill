# SRT Clip C2 Universal 0.3.12

请从 `skills/srt-clip-c2/SKILL.md` 开始。跨平台正式输入范围为 SRT 和逐条时长文本。原生 Skill 用户安装 `skills/srt-clip-c2/`；文件导入用户上传完整 ZIP；纯文本用户使用 `skills/srt-clip-c2/C2-Universal-Portable.md`。四个触发词：`srt文案`、`srt切片文案`、`str文案`、`C2完整精简版`。不依赖 Python，不支持 MP4 音画核验，不将 `切片文案` 作为 C2 触发词。

- Long Context Mode：超长文本按商品窗口确保读取覆盖；商品判断、卖点筛选与编排在同一次语义处理中完成，不另建卖点池或漏检阶段；不强制依赖Python或环境。
- AI-First Constitution：所有语义决策必须由AI完成，工具只能辅助机械读取/定位/计算。
