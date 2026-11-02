# srt-clip-c2 — SRT切片文案 V3.0 · C2精简文本版

这是本仓库默认使用的 Skill。精确触发词：`srt切片文案`。根目录 `SKILL.md` 与 `.agents/skills/srt-clip-c2/SKILL.md` 均为C2格式，必须输出五部分。

第三部分只展示片段功能、原SRT大致时间、源序号与主播完整原话；不展示逐句精确时间码，精确数据仅后台校验。第五部分为唯一完整可复制序号串。

运行：

```
python -S scripts/srt_fast.py scan INPUT.srt --snapshot session.json
# AI决定plan.json
python -S scripts/render_compact.py --snapshot session.json --plan plan.json --stdout
```

本地测试：`python -S tests/test_portable.py`。旧版根目录Skill内容存档在 `legacy/SRT_FAST_REFERENCE.md`，不得被 `srt切片文案` 触发。

**重要**：将代码上传GitHub，不意味着ChatGPT账号已安装；需要在客户端安装/更新Skill。Google Drive现行Runtime如未更新，仍可能执行旧第三部分格式。
