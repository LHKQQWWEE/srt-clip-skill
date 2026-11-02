# srt-slice-copy｜SRT文案 C2 0.1.6 唯一规则版

已按照用户确认格式保留 **片段功能 / 约略定位 / 原序号 / 完整原话**，不展示逐句毫秒时间码。支持SRT和逐条时长文本。

## 快捷使用
上传 `.srt` 字幕文件，或上传/粘贴逐条时长文本，在启用本插件的聊天发送：**`srt文案`** 或 **`srt切片文案`**。
逐条文本每行格式为 `序号 秒数s 原话`，例如 `1 3.4s 有请361度当家小花旦卫衣闪亮登场`；其中1是字幕编号，3.4s是该条原话的持续时长。选段保持45–90秒，并在内容质量允许时尽量接近70秒。兼容 `str文案` 与 `C2完整精简版`。所有触发词使用同一套 C2 0.1.6 规则；旧 V3.0、FAST-LITE、R8、旧固定格式契约和 RC5 候选规则不再生效。
短文本或对话中已完整可读的字幕，直接逐条处理，不要求运行脚本；结果注明“模型逐条对照，未执行程序”。长附件、可能被截断的内容或需要大量累计时长计算时，用一次扫描和一次定稿核验分担格式、编号、累计时间及最终序号检查。商品语义和选段始终由模型判断。

## 安装
- ChatGPT（支持个人Skill上传的账号/工作空间）：插件 → 技能 → 创建 → 从电脑上传ZIP，完成平台扫描后启用。
- Codex：将本目录放入 `${CODEX_HOME:-$HOME/.codex}/skills/srt-slice-copy/`；或使用GitHub仓库的 `.agents/skills/srt-slice-copy/` 项目级Skill。该入口与 `srt-clip-c2` 使用同一规则正文。
- 未看到对应安装入口时，使用与账号匹配的Plugin Creator能力或Codex项目级安装；ZIP/仓库提交不能自动给当前ChatGPT会话注册Skill。

## 长附件处理与机器核验

短文本可直接处理。长附件或希望程序核验时，逐条时长文本可以在开头带一行 `srt文案`、`str文案` 或 `C2完整精简版`；解析器会跳过这一行和空行。

```
python -S scripts/srt_fast.py scan-text INPUT.txt --snapshot session.json
# 例如已完整读到第300条，从第301条继续；offset填首条未读记录的零基偏移：
python -S scripts/srt_fast.py page --snapshot session.json --offset 300 --limit 300
# AI完成一次语义筛选并创建六键plan.json后，只核验/渲染一次：
python -S scripts/render_compact.py --snapshot session.json --plan plan.json --stdout
```

分页的 `--offset` 从0开始，后续页增加offset。直接粘贴内容可传给 `scan-text --stdin --snapshot session.json`。程序按输入顺序累计每条时长，只生成**累计位置估算**，不伪造原视频绝对时间码。只报告脚本实际核验的范围。

## 验证
```
python -S tests/test_portable.py
```

无外部依赖、无用户SRT或真实销售价格硬编码。Google Drive 现行 Runtime、索引和记忆摘要与本版同步；日常处理不读取云盘。

