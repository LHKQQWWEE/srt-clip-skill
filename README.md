# 直播切片文案｜C2 0.2.0

本仓库同步当前唯一执行规则 **C2 0.2.0**。对应插件包版本为 **0.1.19**。

- Skill 主文件：[`.agents/skills/srt-clip-c2/SKILL.md`](.agents/skills/srt-clip-c2/SKILL.md)
- 输入：SRT、逐条时长文本、MP4+SRT；MP4-only 仅在当前宿主能实际读取口播和画面时处理。
- 固定五部分交付；统一按1.2倍速预计成片45–90秒，质量允许时尽量接近70秒。
- MP4判断只报告当前环境实际读取的音画证据。仓库脚本只解析SRT和逐条时长文本，不解码或转写MP4。
- 旧的独立SRT规则目录已移除，所有触发词与输入模式统一到同一份Skill。

## 目录

`.agents/skills/srt-clip-c2/` 包含当前 Skill、执行说明、SRT解析与渲染脚本及合成数据测试。

## 本地使用

将 `.agents/skills/srt-clip-c2/` 放入支持 agents skills 的项目中。需要核验随包文本脚本时，可在该目录运行：

```bash
python -S tests/test_portable.py
```

测试只使用合成数据，不含用户素材。
