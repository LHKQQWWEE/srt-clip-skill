# srt-clip-c2｜SRT切片文案 V3.0 · 文本精简Skill

已按照用户确认格式保留 **片段功能 / 约略原片时间 / 原SRT序号 / 完整原话**，不展示逐句毫秒时间码；后台通过 `srt_fast.py` 校验原始精确时间。

## 安装
- ChatGPT（支持个人Skill上传的账号/工作空间）：插件 → 技能 → 创建 → 从电脑上传ZIP，完成平台扫描后启用。
- Codex：将本Skill目录放入 `${CODEX_HOME:-$HOME/.codex}/skills/srt-clip-c2/`；或使用GitHub仓库的 `.agents/skills/srt-clip-c2/` 项目级Skill。
- 未看到对应安装入口时，使用与账号匹配的Plugin Creator能力或Codex项目级安装；ZIP/仓库提交不能自动给当前ChatGPT会话注册Skill。

## 本地使用
```
python -S scripts/srt_fast.py scan INPUT.srt --snapshot session.json
# AI按 SKILL.md 读全量扫描结果，创建包含六键的plan.json
python -S scripts/render_compact.py --snapshot session.json --plan plan.json --stdout
```

## 验证
```
python -S tests/test_portable.py
```

无外部依赖、无用户SRT或真实销售价格硬编码。本Skill不修改现有Google Drive V3.0 ACTIVE执行卡。
