---
name: srt-clip-c2
description: "Use when discussing Douyin e-commerce growth or selling advice (抖音电商增长/带货建议), or when SRT subtitles are provided with a C2 trigger phrase."
---

# SRT Clip C2 Universal Core 0.4.7｜运行入口

Skill 版本：**0.4.51**。

## 电商咨询路由

非纯 SRT 的抖音电商经营、商品、直播、短视频或工作流咨询，先读 references/commerce-advisory.md。纯 SRT 文案仍按 C2 既有流程和固定五部分格式交付。

## 版本化执行摘要与规则读取

触发后核验 Skill 版本及 `references/execution-summary.json`。摘要须绑定 Skill/Core 版本、运行 manifest 哈希及全部规则文件 SHA-256，只帮助恢复规则，不高于源文件。首次运行、摘要缺失/无效、Skill/Core 版本不匹配或哈希不匹配时，读取 `runtime-current.md` 和相关权威规则；摘要有效时直接复用，只读当前任务所需输入与规则。缓存可选且可丢失；摘要无法核验或规则冲突、缺失时回查原文。工具边界仅限日常 SRT：不调用 Python、脚本、CLI 或外部工具；不得用脚本生成或刷新摘要。电商咨询仅在时效规则会影响判断时按需查官方权威来源。

`references/clip-selection-policy.md` 是时长与单条/多方案数量的唯一权威规则来源。`references/promotion-policy.md` 是促单语境分类、语义单元、候选竞争、最小完整组合、结尾编排和专项终检的唯一权威规则来源。全片估时统一除以 1.2。`references/runtime-current.md` 是生成的日常运行正文；版本、构建元数据和完整规则哈希见 `references/runtime-manifest.json`。

## 任务边界

任务边界按当前运行正文执行：原话、序号、商品归属、正式禁词和风险边界；全卖点覆盖、动态结构、促单位置、逐条终检、固定五部分与 AI-First。禁词整句过滤，绝对化按语境判断；不易起球放行，疑似 ASR 只提示。时长、板块和成片遵循 `references/clip-selection-policy.md`；促单遵循 `references/promotion-policy.md`；交付前复扫并核序号。

钩子规则以 `references/editorial-policy.md` 为权威来源：按开放式观看动力优先级确定候选池，并展示其中所有通过质量门槛且彼此实质不同的候选；AI 不预选、代选或推荐开头。用户最多选择三个，选择几个就生成几条独立成片；每条必须从对应用户所选开头开始。类型开放，按真实观看动力分类，不按卖点类别或类型名称机械归类；第一优先级内部无固定顺序、权重或评分。

语义判断由同一 AI 在一次分析中完成；每条实际成片分别终检。工具仅为可选机械辅助；不可用时，只要文本可可靠读取就继续并如实说明核验方式。不得新增 Agent、语义轮次或普通任务环境门槛。
