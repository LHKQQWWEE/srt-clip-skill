# SRT Clip C2 Universal｜更新记录

## Plugin 0.4.26 / C2 Universal Core 0.4.6（2026-11-22）

- 完成最终包版本统一；核心规则、插件身份和入口保持原位。
- 在 runtime manifest 中标记开发更新协议为条件读取资料，不加入日常必读运行正文。
- 恢复 0.4.24 实际安装包中的 22 项架构边界测试，并更新已过时的完整成片评分断言，继续核验单 AI、源映射、语义边界和终检约束。
- 将 0.4.24 验收记录标明为历史资料；当前业务规则以本版运行正文和验收记录为准。

## Plugin 0.4.25 / C2 Universal Core 0.4.6（2026-11-22）

- 将开头比较限定为开头及必要紧邻回应，并按共情入口、直接有证据的回应、具体可信收益、可验证商品事实的顺序比较。
- 完整信息池建立后强制检查多视频机会；需要用户选择时保存当前对话检查点并暂停，选择后恢复而不重复读取、识别或检测。
- 每条实际选定成片独立覆盖全部有效信息及必要证据/条件；取消完整成片候选竞争、资格评分和全量排名。
- 预计时长仅作约数参考，不参与验收或触发拆条；适用且合规的原文促单完整保留，原文没有时禁止补造。
- 最终终检只检查用户已选且实际写出的成片；保留固定五部分交付和 Core 0.4.6 的冻结边界。
- 同步说明更新覆盖 Portable、README、START-HERE、ENVIRONMENT、平台接口、schema、脚本契约、质量 rubric、测试和验收记录。

## Plugin 0.4.24 / C2 Universal Core 0.4.6（2026-11-21）

- Use one compiled runtime body as the only required rule load while retaining the authoritative business-rule sources and source map for builds and audits.
- Share a complete target-product information pool, rerank every valid point for each candidate angle, require each delivered candidate to cover the full pool, and keep candidate comparison and the independent final audit inside the existing one-AI workflow.
- Consolidate optional mechanical preprocessing and selection checks without transferring semantic decisions to scripts. Keep direct prohibited-term handling, original wording, product attribution, dynamic structure, duration, multi-video, six-dimension comparison, and five-part output rules unchanged.
- Preserve the 0.4.23 package and Git history for rollback. Release acceptance scope and measured limitations are recorded in `docs/acceptance/c2-exec-architecture-release-2026-11-21.md`.

## Plugin 0.4.23 / C2 Universal Core 0.4.6（2026-11-21）

- Add manifest-driven reference loading and optional lossless SRT/duration-text preprocessing with exact parsed/unparsed ranges.
- Add one selection JSON path for structural checks, source-faithful body assembly, shared duration display, fifth-part sequence generation, and replay diffs.
- Keep formal direct-term hits separate from risk hints; keep selling-point completeness, support meaning, product attribution, conditions, transitions, and candidate quality with AI.
- Compare compact complete candidate paths and expand only the selected result; cap ordinary omitted-content notes at three one-line items while listing facts, risks, and key limits separately.
- Add baseline hashes, synthetic replay fixtures, and acceptance protocol. Real-source regression adds recognition of exact leading paste labels without weakening BLOCKED handling for other malformed rows. No rule-file consolidation is included. Publication status is recorded separately.
