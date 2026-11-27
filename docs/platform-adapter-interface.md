# C2 Universal｜平台适配器接口（仅规格，不实现）

状态：DESIGN ONLY｜适用于 C2 Universal Core 0.4.7 / Skill 0.4.47 及之后的平台适配。

## 目标

平台适配器只处理不同 AI 宿主如何可靠读取素材并声明真实能力。适配器不复制业务规则、不选择商品卖点、不设计内容路径，也不替逻辑职责作语义决定。

## 分层边界

### Universal Core 负责

- 四个触发词与任务入口。
- 同一 AI 在一次语义分析和现有一次终检中完成判断；不增加模型、Agent 或语义轮次。
- 商品识别、切换、指代和来源归属；完整读取目标商品窗口并先建立完整有效信息池。
- 信息池完成后按动态顾客心理驱动钩子机制比较开头原话，不设固定类型顺序、权重或分数及必要紧邻回应，不比较完整成片或进行候选评分。
- 完整信息池完成后展示所有通过质量门槛且实质不同的开头候选，不设展示上限；用户最多选择三个，选择几个就各生成一条独立成片，每条从对应用户所选开头开始。
- 每条先完整覆盖有效卖点和必要支持，再按默认 1.2 倍速估算时长；90 秒为目标，超过 90 秒比较完整板块的增量，100 秒为可接受参考，超过 100 秒须逐条复核且不自动截断。仅可省略没有尚未覆盖的独立有效卖点、也不承担必要支持的低贡献完整板块，并说明省略项。
- 适用且合规的直接行动型或种草/推荐型促单完整保留在最后独立板块；原文没有时不编造、改写、补充或跨商品移用。
- 正式禁词只排除实际命中的完整字幕序号，不连带邻近字幕；上下文风险提示本身不触发机器删除。
- 原话来源、商品归属、重复信息增量、动态结构和固定五部分输出。摘要与缓存读取遵循 Skill 的版本化校验协议；缓存仅按平台能力提供。

### Platform Adapter 负责

- 识别宿主能否读取上传文件。
- 将 SRT 或逐条时长文本转换为统一 Source Packet。
- 向 Core 暴露实际可用能力，不虚构工具能力。
- 返回读取失败、截断、编码异常等可验证错误。
- 未来若支持视频，只提供实际读取到的音画证据；不作业务选段判断。

## Capability Contract

适配器必须显式提供能力声明：

```text
can_read_text_files: true|false
can_read_srt: true|false
can_read_video: true|false
can_asr: true|false
can_run_code: true|false
can_browse_web: true|false
can_write_files: true|false
```

Core 不得根据平台名称猜测能力；只使用适配器实际声明并可验证的能力。

## Source Packet

每条原始记录至少包含：

```text
source_type: srt | duration_text
source_name: string | null
record_id: 原始字幕编号
text: 原话
start_ms: SRT 可用时填写，否则 null
end_ms: SRT 可用时填写，否则 null
duration_ms: 逐条时长文本或可可靠计算时填写
source_order: 原始顺序号
```

要求：text 必须逐字来自输入；record_id 不得伪造；缺失字段使用 null，不用推测值补齐；解析错误必须返回具体记录位置。

## Evidence Packet（未来视频能力）

当前 0.4.7 不实现视频适配。后续若平台具备视频能力，只允许适配器返回已实际读取的证据：

```text
evidence_type: visual | audio | asr | timing
source_range: 可验证范围
content: 实际证据摘要
confidence: host-provided | adapter-derived
```

禁止：只凭文件扩展名声称视频已读取；只凭 SRT 声称原声已核实；只凭抽帧补写口播。

## 错误与降级

适配器应区分 FILE_UNREADABLE、INPUT_TRUNCATED、ENCODING_ERROR、INVALID_SRT、UNSUPPORTED_INPUT、VIDEO_UNAVAILABLE、TOOL_UNAVAILABLE。错误只影响对应能力；例如 Python 不可用不应阻止普通文本任务。

降级顺序：原生 SRT → 逐条时长文本 → 保留原始编号/时长字段的普通纯文本 → 无法可靠读取时停止受影响部分并要求可验证文本来源。当前正式支持仍为 SRT 与逐条时长文本；适配器仅报告能力，不改变 Core 的职责和全局边界。
