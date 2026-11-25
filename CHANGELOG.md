# Skill / Plugin 0.4.39 / Core 0.4.7（2026-11-25）

- 取消合格开头候选识别与展示数量上限；展示全部达到既有质量门槛且彼此实质不同的候选，固定四项展示。
- 保留用户最多选择三个开头的限制；超出时暂停并要求重选。每个选中开头仍独立生成完整成片。
- 同步权威规则、运行契约、终检、质量标准、入口提示、便携正文、摘要、测试与双目录镜像；保留开放式观看动力优先级、前 2 秒/前 5 秒判断及所有其他业务规则。

# Plugin 0.4.38 / Core 0.4.7 / Skill 0.4.38（2026-11-25）

- 引入开放式内容板块编排：按所选开头、购买核心和观看预期逐条独立排序，板块整体连续呈现。
- 将永久增量更新治理纳入开发维护协议；增加轻量镜像同步工具，日常运行边界不变。

# Plugin 0.4.37 / Core 0.4.7 / Skill 0.4.37（2026-11-25）

- 修复 canonical Skill 与 `.agents/skills` 镜像中的 Portable 文件版本不一致，并新增镜像同步回归检查。
- 完成前 185 条字幕范围的第一阶段商品归属回归；确认旧候选中存在无法证实属于小马甲的片段，新流程必须先锁定商品再列开头。
- 仅发布镜像与验收记录修复；不改变业务规则、固定五部分、单 AI 路径或“不进入阶段二”的范围约束。

# Plugin 0.4.30 / Core 0.4.7 / Skill 0.4.30（2026-11-25）

- 建立开放式观看动力优先级：存在合格的观看动力驱动型钩子时必须从中择优，仅当不存在时才从其他有效钩子择优；类型按实际观看动力动态归类。
- 保留前 2 秒与前 5 秒连续吸引力、钩子和必要紧邻承接联合编排、1.2 倍速下 2.4/6 秒只作参考、不硬截原话；第一优先级内部不设固定顺序、权重或评分。
- 允许不同购买核心的多方案共享最佳钩子，不强制更换开头；冻结其他业务规则、卖点覆盖、促单原话、动态结构与 AI-First 架构。
- 0.4.29 的“无钩子类型优先级”规定已被本版取代；旧回归记录移入历史目录，不作为当前运行规则。

## Plugin 0.4.29 / Core 0.4.7 / Skill 0.4.29（2026-11-25，已由 0.4.30 替代）

- 将钩子原话与必要紧邻承接联合编排，综合判断前 2 秒吸引力与前 5 秒连续吸引力。
- 默认 1.2 倍速对应原素材累计 2.4 秒、6 秒作为参考；不把时间点用作硬剪辑点，不为贴合时间截断完整原话。
- 承接按素材动态延续情绪、视觉/动作期待、种草兴趣或购买收益，不设固定类型、顺序、权重或评分，不增加语义轮次或工具依赖。
- 同步权威规则、运行契约、AI-First 宪章、终检、执行摘要、测试矩阵、便携版和 `.agents/skills` 镜像；保留 Core 0.4.7、原插件 ID 和其余业务规则。

## Plugin 0.4.28 / Core 0.4.7 / Skill 0.4.28（2026-11-25）

- 将固定共情入口顺序替换为动态顾客心理驱动钩子机制：完整信息池后跨主题比较真实开头原话及必要紧邻承接，以陌生潜在买家的继续观看欲望和商品相关购买兴趣为目标，不设置固定类型优先级、权重、分数或额外语义轮次。
- 允许真实喜爱、动作展示、视觉好奇、需求收益等入口依当前商品和目标顾客动态竞争；保留真实性、商品归属、正式合规、自然语义、后文兑现、全部有效信息覆盖和原文促单。
- 更新运行契约、AI-First 宪章、终检、长文本、便携入口与跨类目回归；保留 Core 0.4.7 和原插件身份。仅凭 SRT 的视觉及情绪表现仍标为未核验。

# SRT Clip C2 Universal｜更新记录

## Skill 0.4.28 / C2 Universal Core 0.4.7（2026-11-22）

- 默认直接输出两个具有不同购买核心的完整方案；每条独立覆盖完整有效信息池，第二方案无法成立或降低质量时单条交付并解释原因，显式“单条/按推荐版”直接单条。
- 先完整编排、后计算时长；120 秒不是目标或硬上限。只有完整方案明显超过 120 秒才按方案核心动态筛选并逐项说明省略项，略超时仍保留必要信息。
- 新增持久化、版本化执行摘要；摘要与清单及全部源规则校验匹配时复用，不强制每次重读，摘要失效或遇到不确定时回查原文。
- 更新运行正文、验收规则、QA 与版本清单；历史验收材料和旧发布包移出当前检索路径。
- 保护原话、字幕序号、商品归属、多商品确认、正式禁词边界、风险提示、重复识别、共情开头、原文 CTA、固定输出、AI-First 等原有规则。

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
# Plugin 0.4.37 / Core 0.4.7 / Skill 0.4.37（2026-11-25）

- 从上传包和同步渠道清除一次失败复制留下的 7 个临时文件，恢复源、插件镜像与安装缓存的精确文件一致性。
- 只涉及发布包清理；运行规则、固定五部分、序号硬门和 Core 0.4.7 不变。

# Plugin 0.4.35 / Core 0.4.7 / Skill 0.4.35（2026-11-25）

- 清除插件历史 overlay 中仅存在于旧发布包的三份 0.4.22/0.4.23 基线、计划和设计文档；当前源仓库及运行规则不变。
- 继续保持 canonical 与 `.agents` 镜像一致，并保留所有验收材料的版本归档。

# Plugin 0.4.34 / Core 0.4.7 / Skill 0.4.34（2026-11-25）

- 清除插件更新时保留在当前路径的旧验收副本（0.4.31、0.4.32、0.4.33），对应历史报告保存在归档目录。
- 本版本只修复插件 canonical 与 `.agents` 镜像的一致性；运行规则、固定五部分、序号硬门和 Core 0.4.7 均不变。

# Plugin 0.4.33 / Core 0.4.7 / Skill 0.4.33（2026-11-25）

- 仅清理私有插件 `.agents` 镜像中重复放在当前路径的 0.4.31 验收文件；历史记录仍保留在版本归档目录。
- 0.4.32 已确认的运行规则、固定五部分、序号硬门和 Core 0.4.7 均不变；本版本仅用于同步一致性。

# Plugin 0.4.32 / Core 0.4.7 / Skill 0.4.32（2026-11-25）

- 按 LF 规范化文本哈希，避免 Windows CRLF 与 LF 检出导致运行摘要误判失效。
- 完成已确认的商品选择、开头选择、独立成片、纯文本连续性和序号硬门修正；常规运行不再依赖 Python、脚本或外部工具。
- 五部分输出及有效业务规则保持；164 项自动回归通过。用户指定的 185 行 SRT 未提供，素材级语义回归仍为 BLOCKED。

# Plugin 0.4.31 / Core 0.4.7 / Skill 0.4.31（2026-11-25）

- 多商品先呈现身份与原始讲解窗口并等待用户选择；仅对选定商品生成开头候选。
- 候选最多 3 个且只显示名称、开头原话、原始序号和预估时长；不预选、不代选、不凑数。用户所选的每个开头分别生成独立完整成片。
- 增强纯文本的指代、动作/回应、前置条件与事件状态连续性跟踪，不要求视频或图片。
- 日常 SRT 执行完全移除 Python、脚本、CLI 与 JSON 流水线调用；Python 仅保留在开发、构建和发布测试。
- 将原始序号、原话、精确时长绑定到冻结映射；成片正文与第五部分序号不一致或无法核验即阻断。固定五部分、已有有效业务规则与 Core 0.4.7 保持。
