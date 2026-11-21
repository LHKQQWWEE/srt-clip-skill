# SRT Clip C2 Universal 0.4.6

插件包版本：**0.4.24**；业务内核：**0.4.6**。日常入口完整读取 `skills/srt-clip-c2/SKILL.md` 与唯一编译正文 `skills/srt-clip-c2/references/runtime-current.md`；规则源文件映射和完整性元数据由构建与测试使用，不重复加载。

C2 is an AI-led purchase-decision editor with one semantic analysis and one final audit. It reads the full target-product context, identifies every valid independent purchase point, then compares complete candidate paths without anchoring on the first strong point.

Every delivered video must independently cover the full valid point set and its necessary evidence or conditions. The union of several videos is only a secondary consistency check. When multiple differentiated videos are possible and the user has not specified a count, recommend the themes and count, then wait for the user's choice before producing them.

Opening candidates compete across the full target-product transcript, regardless of the selected content theme. Compare attention hooks with their immediate responses; numbers and host experience do not automatically outrank a concrete customer problem.

Direct formal prohibited terms are scanned against the single list in `skills/srt-clip-c2/references/global-rules.md`; only matching full cues are excluded. The user's newly designated `羊毛` term is unconditional. `羊绒` is independently prohibited; static-control wording and nearby cues remain outside the ban. The optional guard script performs literal matching only; AI remains responsible for semantic and factual judgment.

Duration is a planning reference, not a task completion condition. Keep the 45-second general lower-bound guidance, short-cut quality exception, and no fixed upper limit. Long-context rules and product knowledge packs load only when their conditions apply. See [START-HERE.md](START-HERE.md) and the compiled runtime for the complete contract.
