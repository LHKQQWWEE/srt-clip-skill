# C2 Universal｜未来平台适配器接口（仅规格，不实现）

状态：DESIGN ONLY｜适用于 C2 Universal 0.3.x 后续平台适配。

## 目标

平台适配器只解决“不同 AI 宿主如何把素材可靠地交给 Universal Core”这一层问题，不复制、不改写业务规则。业务规则继续由 Universal Core 负责，避免 ChatGPT、Claude、Gemini 等平台各维护一套不同逻辑。

## 分层边界

### Universal Core 负责
- 触发词与任务入口。
- 商品识别、商品切换和类目判断。
- 类目专项模块加载。
- 亮点盘点、开头/中段/结尾编排。
- 原话与来源约束。
- 1.2 倍速、120 秒硬上限。
- 合规风险判断。
- 固定五部分输出。

### Platform Adapter 负责
- 识别宿主能否读取上传文件。
- 将 SRT 或逐条时长文本转换为统一 Source Packet。
- 向 Core 暴露实际可用能力，不虚构工具能力。
- 返回读取失败、截断、编码异常等可验证错误。
- 未来若支持视频，只负责提供实际读取到的音画证据；不自行做业务选段判断。

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

要求：
- `text` 必须逐字来自输入，不做润色。
- `record_id` 不得伪造。
- 缺失字段使用 null，不用推测值补齐。
- 解析错误必须返回具体记录位置。

## Evidence Packet（未来视频能力）

首版 0.3.0 不实现视频适配。后续若平台具备视频能力，只允许适配器返回已实际读取的证据：

```text
evidence_type: visual | audio | asr | timing
source_range: 可验证范围
content: 实际证据摘要
confidence: host-provided | adapter-derived
```

禁止：
- 只凭文件扩展名声称视频已读取。
- 只凭 SRT 声称原声已核实。
- 只凭抽帧补写口播。

## Error Contract

适配器应区分：
- FILE_UNREADABLE
- INPUT_TRUNCATED
- ENCODING_ERROR
- INVALID_SRT
- UNSUPPORTED_INPUT
- VIDEO_UNAVAILABLE
- TOOL_UNAVAILABLE

错误只影响对应能力；例如 Python 不可用不应阻止普通 SRT 文本任务。

## 降级顺序

1. 原生 SRT 读取。
2. 逐条时长文本读取。
3. 普通纯文本读取并保留原始编号/时长字段。
4. 无法可靠读取时停止受影响部分并要求可验证文本来源。

不允许通过“猜测缺失内容”完成降级。

## 适配器实现原则

- 一个适配器只负责宿主差异，不复制 Core 业务规则。
- 任何平台特有优化都必须是可选增强，不能成为跨平台通用规则的硬依赖。
- 适配器更新不得改变四个触发词、固定五部分输出、时长上限或全局禁用规则。
- 平台特定测试与 Core 回归测试分开记录。

## 计划中的适配器

- ChatGPT Adapter
- Claude Adapter
- Gemini Adapter
- Generic File/Prompt Adapter

当前状态：均未实现。0.3.0 正式支持仍以 SRT 和逐条时长文本为准。
