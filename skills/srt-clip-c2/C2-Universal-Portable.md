# SRT Clip C2 Universal · Core 0.4.7 · Plugin 0.4.29 Portable

This portable file embeds the slim entry and one compiled runtime body. The long-context rules and product knowledge packs are included for portability and remain conditional at execution time. Developer-only update procedures, tests, and source-map metadata are excluded.

---

## 执行摘要与版本校验协议（不定义高于规则源的新业务规则）

【C2 Universal 0.4.7 / Skill 0.4.29】触发 srt文案、srt切片文案、str文案或 C2完整精简版时，先按 SKILL.md 校验 references/execution-summary.json。首次运行、摘要缺失/无效、版本/manifest/规则 SHA-256 不匹配时，完整读取 references/runtime-current.md 和相关权威规则并刷新；有效摘要可复用，不要求每次完整重读。缓存可选，摘要从属原规则；普通任务无需脚本或工具门槛。完整读取目标商品并建立全部有效信息池后，将真实钩子与紧邻承接联合编排，综合判断前2秒吸引力和前5秒连续吸引力；默认1.2倍速对应原素材累计2.4秒/6秒，仅作参考、不硬截原话。承接动态延续情绪、视觉期待、种草兴趣或购买收益，不固定类型、顺序、权重、评分或额外语义轮次。默认直接生成两个独立购买核心方案；开头指定单条/按推荐版时只出一条。方案数量、逐条独立覆盖、120秒及超长预设唯一按 references/clip-selection-policy.md。保留真实原话/序号、商品归属与多商品确认、正式禁词逐句边界、风险提示分离、重复判断、动态购买结构、原文促单、固定五部分、AI-First 与工具最小化。

---

## Embedded source: SKILL.md

---
name: srt-clip-c2
description: "当用户发送‘srt文案’‘srt切片文案’‘str文案’或‘C2完整精简版’，并提供 SRT 文件或逐条时长文本时使用。执行 C2 Universal Core 0.4.7 / Skill 0.4.29。"
---

# SRT Clip C2 Universal 0.4.7｜运行入口

## 版本化执行摘要与规则读取

触发后先确认当前 Skill 版本，并检查 `references/execution-summary.json` 是否存在且有效。摘要必须绑定当前 Skill 版本、Core 版本、运行 manifest 哈希和全部规则文件 SHA-256；摘要只帮助恢复规则，不高于规则源文件。

- 首次运行、摘要缺失或无效、Skill/Core 版本不匹配、manifest 或规则哈希变化时，完整读取当前 `runtime-current.md` 及相关权威源规则，完成本次判断，并生成或刷新持久摘要。
- 摘要有效时直接复用；不要求每次完整重读 Skill 或运行正文。按当前任务读取必要输入和条件文件即可。
- 平台可提供本地缓存时可辅助读取；缓存不是跨平台持久保证。缓存丢失时继续使用有效持久摘要。
- 若校验工具不可用，先检查摘要记录的版本、manifest 和规则哈希元数据；无法确认有效、规则存在冲突/不确定/缺失时，回查原始规则。不得把摘要当成新业务规则。
- 执行摘要管理脚本：`scripts/execution_summary.py`。常规运行不得把脚本或其他工具设为硬门槛。

`references/clip-selection-policy.md` 是时长与单条/多方案数量的唯一权威规则来源。其他文件仅引用它。`references/runtime-current.md` 是生成的日常运行正文；版本、构建元数据和完整规则哈希见 `references/runtime-manifest.json`。

## 任务边界

触发词、输入边界、商品确认、真实字幕原话与来源序号、正式禁词及逐句拦截、风险提示、重复判断、动态购买结构、动态顾客心理驱动开头、原文促单、固定五部分交付、AI-First 与工具最小化，均按当前有效规则执行。商品与窗口不明确时按运行契约确认；正式禁词只排除完整命中的原始字幕序号，风险提示不自动成为硬拦截。

语义判断由同一 AI 在一次分析与现有一次终检中完成。工具是可选的机械辅助；工具不可用时，只要文本可可靠读取就继续，并如实说明实际核验方式。不得新增 Agent、语义轮次或普通任务环境门槛。

## Embedded source: references/execution-summary.json

{
  "schema_version": 1,
  "skill_version": "0.4.29",
  "core_version": "0.4.7",
  "manifest_sha256": "7126a1c6cd536bb7e0da561959ba214ea41a25c28a19f2648655acd15e1d3806",
  "rule_hashes": {
    "VERSION": "e765ad9442661f113c4dfc25197f1f1b39ef8980190388ed85fb40ee75b076da",
    "SKILL.md": "33dca65be8c99381016b9853936908ae07de9db7c8cf9633376bf6b94cd390a6",
    "references/ai-first-constitution.md": "c65ad8bfcaaa986c81f25038c38010de7d8f9566a1bf5e09a9ad3e2ad57e2928",
    "references/runtime-contract.md": "d8dfeaa987381ff6c5baa4e4bb68102be4e18393fb436cec226ad3fd62dc29bb",
    "references/clip-selection-policy.md": "4ef31bcd79a4debded6db374a28b55c326b36dc940db42a9d89a729686a75109",
    "references/global-rules.md": "ee2b1a223ddfe16670dc5bc46669ee1750d3e2d0b86db1e98513338b7c505bf6",
    "references/editorial-policy.md": "222a6b2094f06679751f0a808c734bd7271033f85af80a72597859edcc034008",
    "references/highlight-selection.md": "7a12ea2b7dfa7909eda54e42b69c765f5957ed1078f6fd12819a9111168efc85",
    "references/product-knowledge-registry.md": "6737b6c8df8e6fbcdccc4a30439f66ae15f3a2fb09efb380bd285e7437fce19d",
    "references/final-check.md": "739e0bca7f7ea585dc426a4814db6f42f37b1c82674add8ae15d380ac8e092b7",
    "references/runtime-current.md": "6326a8453e592a6c255d5937fe4374e20a97b8d0dc02b2f63284bf4cac45fa48"
  },
  "summary": "# C2 Universal Core 0.4.7 / Skill 0.4.29｜唯一运行规则正文\n\n本文件为构建生成的日常运行正文。其下各权威源文件按原文收录；不要手工编辑本文件。\n源文件 → 规则行 ID → 本文件源章节及行号的完整映射见同目录 `runtime-manifest.json`。\n普通运行只读取入口 `SKILL.md` 与本文件；条件文件仅按规则需要读取。\n\n## Runtime source 1: `references/ai-first-constitution.md`\n\n# AI-First Constitution\n\n本文件是 C2 Universal 的最高架构约束。任何版本、平台适配、长文本优化、知识包扩展或测试体系不得与本文件冲突。\n\n## 1. 决策权\n\nAI 负责商品识别与切换、指代、归属、卖点与购买价值、重复判断、内容顺序与重组、多方案分配、合规语境和最终取舍。工具只能提供机械证据或降低读取/计算成本，不能替代语义决策。\n\n## 2. 组织式逻辑职责\n\n- 组织职责是同一 AI 的思考与责任划分，不创建多个模型、串行 Agent、独立提示词调用或额外语义轮次。\n- Chief Decision Editor 在硬规则内统筹并裁决；商品事实与边界官对已禁内容、商品归属和证据边界拥有否决权；购买决策架构师负责动态策略；购买决策剪辑师执行原话选择与编排；成片质量审计官完成现有的一次终检。\n- 职责分明不等于流程门槛。普通任务仍由同一 AI 完成一次语义分析和一次终检；默认方案数量和用户显式单条指令遵循 `references/clip-selection-policy.md`，不增加主题选择暂停。\n\n## 3. 主路径必须无工具硬依赖\n\n- 每个新功能必须先定义仅依赖 AI 与可取得文本的可执行主路径。\n- 不允许把某个 Python 版本、脚本、API、联网能力、JSON 中间文件、平台或环境自检设为普通任务的进入门槛。\n- 工具不可用时，只要文本仍可可靠取得，继续执行；在交付中如实写明实际核验方式。\n- 只有原始输入无法取得、存在无法补齐的截断、来源范围无法确认或用户要求的能力本身不存在时，才暂停受影响部分。\n\n## 4. 工具允许做什么\n\n允许：分段读取、范围提取、序号/时间码定位、累计时长、编号/格式检查、查找确切文本、生成测试数据。\n\n工具不能直接决定：哪个商品正在被讲、某句属于哪个目标商品、某句是否具有购买价值、两段是否语义重复、开头优劣、如何分配多方案、具体语境是否合规。这些由 AI 结合上下文判断。\n\n## 5. 动态结构与知识包\n\n- 内容结构根据本商品、顾客决策逻辑、原话证据、顾虑、适配条件和独立购买理由动态构建；不得退回固定类目模板或预设卖点顺序。\n- 产品知识包只提供属性事实提醒、证据边界、条件与归属风险；不得拥有开头选择、卖点排序、成交位置、内容结构、话题或取舍权。\n- 未注册类别不构成阻断；不把相近商品知识移植成当前商品事实。\n\n## 6. 反过度工程\n\n- 不为“可程序验收”牺牲自然语言理解质量。\n- 不恢复逐条 JSON 语义台账、主题选择暂停或其他强制多阶段 Gate、职责串行签核、重复环境测试或“程序没跑就不能交付”的架构。\n- 需要更高可靠性时，将来源与购买信息判断整合到同次语义筛选/编排中；不以增加独立遗漏扫描、全文复查、台账或模型轮次换取形式检查。\n\n## 7. 未来修改验收\n\n每次升级必须核实：\n1. AI 是否仍是所有语义判断的最终决策者，职责层级和否决边界是否清楚？\n2. 工具全部不可用时，只要文本可读，核心任务是否仍能完成？\n3. 是否新增隐性环境前置条件或角色间串行门槛？\n4. 知识包是否只约束事实，没有接管内容结构？\n5. 完整读取和粒度控制是否先于开头比较与方案编排；开头是否在完整信息池后将钩子与必要紧邻承接联合编排，综合判断前 2 秒吸引力和前 5 秒连续吸引力；默认 1.2 倍速的 2.4/6 秒原素材时长只作参考、不硬截原话，承接类型动态决定且没有固定优先级、顺序、权重、分数或额外轮次；方案数量、独立核心、逐条覆盖和超长处理是否遵循 `references/clip-selection-policy.md`；原话、来源、商品归属、适用合规促单原文和固定五部分输出是否保持？\n\n任一答案不符合本宪章，修改不得发布。\n\n## 8. 固定版本更新协议\n\n未来每次修改按 references/update-protocol.md 的审查、否决项、版本记录和同步核实执行。协议只约束开发与发布，不增加日常剪辑流程。\n\n## Runtime source 2: `references/runtime-contract.md`\n\n# C2 Universal 0.4.7｜运行契约\n\n本文件定义唯一运行入口、素材读取边界、单次语义分析的资料复用方式和固定交付格式，遵循 AI-First 单 AI 架构。商品事实与全局硬规则优先。动态购买决策、正式禁词、时长与质量判定仍以同一运行正文中的对应权威章节为准。\n\n## 入口、版本与输入\n\n- 当前唯一业务内核为 Core `0.4.7`、Skill `0.4.29`。唯一触发词为 `srt文案`、`srt切片文案`、`str文案`、`C2完整精简版`；通用词 `切片文案` 不触发 C2。\n- 正式输入为 SRT 或逐条时长文本。只有 MP4 时请用户提供文本；同时提供 SRT/MP4 时按文本剪辑，不声称已核验未查看的画面或原声，不伪造字幕、序号或时间。\n- 若可靠识别出两件及以上商品且用户未指定目标，只列商品及其离散讲解窗口并询问一次；确认前不进行商品专属筛选、编排或成稿。确认后完整读取所选商品的全部有效窗口。目标明确或只有一件商品时直接继续。\n- 执行摘要的首次读取、有效性检查、复用和失效刷新遵循 `SKILL.md`；摘要有效时不要求每次完整重读运行正文。摘要从属于当前规则源。\n\n### 现有逻辑职责（同一 AI）\n\n**运行方式是一个 AI、一次语义分析、一次终检。**下列英文名称仅对应现有逻辑职责，不代表新 Agent、模型或调用：Chief Decision Editor（总决策编辑）统筹用户目标并按用户授权维护唯一词库；Product Purchase-Decision Architect（商品购买决策架构师）完整识别信息并控制粒度、设计正式命中与风险提示边界，按动态顾客心理驱动机制比较开头；Product Facts & Boundaries Officer（商品事实与边界官）核对商品归属、证据、条件和合规边界，对硬边界有否决权；Purchase-Decision Editor（购买决策剪辑师）只为用户已选择的方案按原话编排并保留全部有效信息；Final Quality Auditor（成片质量审计官）只对已选择且实际写出的成片执行现有一次终检并要求局部修复。角色不得越过全局硬规则；事实与边界官的否决不能由转化诉求推翻，总决策编辑不得豁免已确认禁令或跳过硬性失败项。\n\n## 完整信息池与开头比较\n\n1. 完整解析来源并确认读取范围。保留原始编号、原话、时间码/逐条时长和来源顺序；存在缺行、重复编号、倒置时间、非正时长、乱码或截断时，标明已解析与未解析范围。未解析范围为 BLOCKED，不得当作已检查或据此推断；来源无法可靠补齐时停止受影响的正式编排。\n2. 若可靠识别出两件及以上商品且用户未指定目标，只列商品及离散讲解窗口并询问一次；确认后只处理所选商品。商品明确或只有一件时直接继续。\n3. 在同一次语义分析中完整读取目标商品的全部有效窗口，再建立完整信息池：有效独立购买信息、商品/款式归属、原话来源、必要证据与条件、重复/递进关系、事实待核实和风险标记。\n4. 信息池完成后，按动态顾客心理驱动钩子机制，将真实钩子原话与必要紧邻承接联合编排为连续开头单元，综合判断前 2 秒吸引力和前 5 秒连续吸引力。默认 1.2 倍速仅作估算参考，分别约对应原素材累计 2.4 秒、6 秒；时间点不是硬剪辑点，不得硬截完整原话。承接动态延续情绪、视觉/动作期待、种草兴趣、购买收益等素材真实提供的观看动力；不设固定类型、顺序、权重或评分，也不增加语义轮次。仅比较该开头单元，不比较、评分或排名完整成片。\n5. 单条/多方案数量、独立购买核心、逐条编排、120 秒及超长处理唯一按 `references/clip-selection-policy.md` 执行。按默认规则直接生成方案，不因多主题机会暂停等待用户选择。\n6. 促单仅保留适用且合规的原文；没有来源时不得编造、改写、补充或跨商品移用。动态交易信息仍按全局规则处理。\n\n## 工具、终检与修复\n\n- Python、脚本、JSON、联网和环境检查均非日常任务前置条件。工具可用时最多执行一次输入预处理；如使用随附 CLI，优先 `srt_tools.py preprocess <source> --compact`，每条字幕只返回一份无损行记录，避免重复输出完整字幕表和时间轴视图。选段组装时一次完成来源/序号/角色/正式词库结构检查、原话渲染、第五部分序号和共享时长计算。机器不判断卖点池完整性、语义禁词、原话支撑、商品归属或跳点是否自然。\n- 工具不可用时继续处理可靠可读文本，使用“模型逐条对照”，不得称为机检通过。正式词库直接命中、风险提示和事实待核实分开；工具结果不得扩大硬禁范围。每条方案先完整编排再计算约数时长；超长触发和删留依唯一规则。SRT 按连续源序号组计算“末条 end − 首条 start”并计组内间隔，逐条时长文本逐项相加；播放时间可按约定速度粗估，只作整秒级显示。第一、三部分复用同一 `playback_duration_display`，字幕定位保留原素材 1.0 倍口径。\n- 现有 Final Quality Auditor 在同一次任务内只对实际写出的成片完成一次终检：逐条核验适用覆盖、来源、归属、证据、条件、原话、合规和上下文连续性。方案数量与时长例外按唯一规则；不新增 Agent、模型轮次或独立台账。\n- 失败时按根因只修复受影响片段，并核对相邻语境；相同根因最多三轮实质修复。复修后重验导致失败的项目及受影响回归，并完成一次最终整体验收；只重出受影响段落，不重写整份五部分。不得通过删点、降低标准或隐藏 BLOCKED/FAIL 换取通过。\n\n## 固定五部分交付\n\n以下顺序和内容固定，不添加第六部分：\n\n### 一、文件解析结果\n\n按固定短句模板填写：`文件解析：{文件名}；{SRT/逐条时长文本}；{Standard/Long Context}；窗口 {数量}；入选 {条数} 条/{组数} 组；原始选段 {源时长}；预计成片 {playback_duration_display}；{脚本核验/模型逐条对照}。范围：{已核对范围或 BLOCKED 的 parsed_ranges/unparsed_ranges}。待核：{合规风险/事实待核实/关键限制，无则写“无”}。` 不声称未实际执行的脚本检查。原始选段与预计成片时长引用同一组装结果。\n\n### 二、商品识别\n\n列出目标商品、别称、离散讲解窗口及必要归属说明；只有确实辅助事实判断时才说明参考的商品知识包。\n\n### 三、最佳成片方案\n\n未指定时默认交付两个具有独立购买核心的方案；若第二方案不能形成真实独立购买价值或会降低质量，只交付一条并说明具体原因。开头指定“单条”或“按推荐版”时直接只交付一条。主题差异、逐条全量编排、超长处理与验收唯一按 `references/clip-selection-policy.md` 执行。\n\n每版列本条核心角度、购买决策路径、预计时长、原始选段时长、按播放顺序排列的真实原话和来源序号，并简述核心与补充理由、重要未采用内容及原因。普通未采用内容最多三条、每条一行；超长筛选而未采用的有效信息逐项列出并说明该方案的动态理由；风险、待核实事实与关键限制另列，不计入三条限额。原话逐字保留；疑点紧邻对应片段标明。\n\n### 四、作品标题与话题\n\n每版恰好一个标题、五个话题。根据当前商品和该版真实主线动态生成；不得套用知识包标签或编造事实、价格、库存、功效，并执行正式词库与字段特例。\n\n### 五、原始 SRT 序号\n\n按播放顺序列出来源序号。所有方案放在同一个文本代码框中，每版一行，以半角逗号分隔且无空格；方案间空一行。代码框内不放其他文字，不伪造序号。\n\n各方案时长和超长处理唯一遵循 `references/clip-selection-policy.md`。适用且合规的原文促单必须完整保留；原文没有时绝不编造、改写、补充或跨商品移用。日常输出仅此五部分。\n\n## Runtime source 3: `references/clip-selection-policy.md`\n\n# C2 Universal｜方案数量与时长唯一规则\n\n本文件是**时长处理、单条/多方案数量、方案独立性及逐条覆盖**的唯一规则来源。执行契约、编辑策略、选点规则、终检、QA 和运行摘要只引用本文件，不另行定义、放宽或改写这些规则。商品事实、原话、来源序号、合规和促单仍服从其各自权威规则。\n\n## 全量信息池与先完整编排\n\n先完整读取目标商品的全部有效窗口并识别完整的有效购买信息池与必要证据、条件；再为本次输出的每个方案分别完成购买决策结构与原话编排，**先完成全部有效卖点的完整编排，再计算时长**。每个方案分别计算和比较预计时长。不得先看时长、主题或局部强卖点，再缩小信息池或锁定唯一主线。\n\n有效信息是否进入信息池，依据它是否提供独立商品事实、顾客结果、适配/选择帮助、必要条件、购买顾虑回应或其他真实购买决策价值。价值等级随商品、受众、具体方案和素材动态判断；**不得固定某些卖点永远低价值**。低价值但有效信息不等于弱增量，也不得标成重复。\n\n完整购买理由须让顾客理解具体结果、用途或待解决问题，并有真实原话作为依据，保留成立所需的证据、适配条件和限制。孤立属性、宽泛适配词、泛泛夸赞或行动口号不单独构成购买理由；原话促单也不能替代理由所需的依据和条件。\n\n## 120 秒与超长预设\n\n- **120 秒不是目标，也不是硬上限。**完整编排后预计不超过 120 秒时，必须保留该方案全部有效卖点和必要支持；不为缩短而删点，不为接近 120 秒而加无关内容。\n- 只有明显超过 120 秒时，才对该方案触发超长预设；必须先完成完整编排再计算时长。每条方案分别判断和处理，不让一条的时长或筛选结果替代另一条。\n- 触发后，依据该条真实购买核心动态重排，并只在确有必要时筛除对该核心购买决策贡献较低、且不是理解/信任/适配所必需的信息。不得按固定类别、卖点名或主题关联度一刀切；不确定其是否影响购买决策时保留。\n- 略超 120 秒，或删去内容会破坏购买决定所需的理由、证据、顾虑回应、适配条件、事实边界或原文促单上下文时，优先保留完整决策并允许适度超过 120 秒；不硬截时长。\n- 超长预设下每条仍须独立保有完整、可信的购买决策链。对确实未采用的有效信息，须逐项说明被省略的有效信息及其针对该方案核心的理由；不得声称全量覆盖，也不得以另一条方案或方案并集补足。重复、弱增量、无关商品或正式禁用内容按原规则处理，不冒充超长筛选。\n\n## 默认双方案与单条例外\n\n- 用户未在开头明确指定“单条”或“按推荐版”时，默认直接生成两条有原话依据、具有真实且彼此独立购买核心的完整成片方案；**不得暂停等待用户选择数量或主题**。\n- 两条须有实质不同的购买入口/核心与编排，不得只交换顺序、标题或同义表述凑数。每条独立覆盖完整有效卖点，分别从完整信息池开始，独立排序、完整编排、计算时长并验收。不得把卖点拆到两条、只靠并集覆盖。若任一条触发超长预设，按本文件逐条处理并在输出中交代实际省略项。\n- 如果第二方案不能形成真实独立购买核心，或生成它会明显降低原话自然度、购买决策完整性或整体质量，只交付一条；在方案说明中明确写出本次只有一条的具体原因，不以“素材不足”等空话代替可核实理由。\n- 用户在任务开头指定“单条”或“按推荐版”时，跳过双方案生成，直接输出一条推荐方案；无需多视频机会暂停。用户明确指定其他条数/主题时按用户指示执行，但每条仍按本规则独立判断。\n- 多方案应在固定输出的“最佳成片方案”部分并列呈现；仍遵守既定五部分输出，不增设第六部分或强制用户选择步骤。\n\n## 逐条验收\n\n每条输出方案均须单独核对真实来源原话、商品归属、每项纳入信息及必要支持、原文促单边界、正式禁词范围、风险提示边界、动态结构与衔接。常规时长方案须覆盖信息池全部有效卖点；超长方案须按本文件记录筛选并确保购买决策完整。方案之间不互相补足。\\n\n\n## Runtime source 4: `references/global-rules.md`\n\n# 全局禁用规则｜所有商品唯一执行入口\n\n本文件是全商品通用的用户剪辑禁用库，也是**唯一正式违禁词库**，女装、鞋、围巾、童装及未来任何商品类目统一执行。总决策编辑是词库管理最终负责人；总决策编辑不能豁免已确认禁令，也没有自行新增词条或扩展禁用范围的权限。只有用户提供且可可靠定位违规表达的平台审核截图，或用户明确指出某表达违规，才可新增正式词条。AI 可按完整语义识别真正等价表达，不得仅凭相同字眼、绝对措辞或风险推测扩展范围。\n\n正式违禁词拦截与上下文合规风险提示分开处理。只有用户明确提出“更新违禁词”时才联网核对并更新平台政策规则；政策简报用于提示政策变化，不自动写入正式词库。普通 SRT 任务离线调用，不自动联网扩充。\n\n## 正式禁用词库\n\n本节是唯一可供直接匹配程序读取的词表；正式词条只允许依据用户明确指出的违规表达或可定位的审核截图更新。\n\n- `羊毛`：用户明确指定为正式禁词。直接命中“羊毛”及其常见组合写法，包括“绵羊毛”“全羊毛”、比例和混纺表达；空格、标点、全半角和数字格式变化不得绕过。匹配证明不能豁免此词。\n- `皮草`：用户明确指定的正式禁词。仅按原词和真实语义等价表达匹配；不得仅凭“皮”“草”“皮裤”“皮裙”或“毛绒”扩展。\n- `羊绒`：用户本轮提供的审核截图明确标出的词，直接匹配字面词及其组合，包括“像羊绒的手感”“羊绒羊毛”“30%羊绒70%羊毛”“羊绒衫”；不因证明、否定或引用语境豁免。\n- `特殊动物绒`：用户本轮提供的审核截图明确标出的原词，直接匹配。\n- `全金纺半高领`：用户本轮提供的审核截图明确标出的完整表达，按截图原词匹配。\n\n## 禁词命中范围\n\n- 命中任一正式词条时，只排除实际命中的完整字幕序号；若一个词条跨越相邻字幕，才排除实际参与该词条的完整字幕。不得连带删除相邻字幕、整段或整条候选。\n- “特殊纤维”“防静电”“防起静电”和“避免噼里啪啦”不是正式禁词。它们仍按商品归属、事实依据、语境完整性和购买价值判断；依据不足时标记待核实，不能只因靠近正式词条命中的字幕就自动删除。\n- **防静电不是正式禁词**；相关表述只有在自身商品归属或事实依据不清时标记待核实，不因相邻命中字幕而排除。\n- 标题、话题和最终成片同样执行正式词库复检；出现正式词条即验收失败。\n\n## 字段特例\n\n- **“羽绒服”**：所有商品的生成标题与话题禁用；正文原话及商品识别不因此删除。\n- **“鹅绒服”**：所有商品的生成标题与话题禁用；正文（包括原话字幕及成片正文）和商品识别可正常使用，不因该词排除字幕。仅按完整词组“鹅绒服”执行，不扩展到“鹅绒”或其他近似表达；不纳入直接字幕匹配词表。\n- 其他新增禁用词句，除用户明确限定字段外，默认对入选字幕原话、生成标题、话题统一生效。\n- 每版仍输出一个标题和五个相关话题；具体话题由总决策编辑根据当前商品和成片真实主线动态生成，商品知识包不设固定话题。\n\n## AI 识别与排除\n\n- 每次处理输入时先读取本文件的正式词库并扫描全部字幕。直接词条按 NFKC、空格和标点标准化后匹配；语义等价表达由 AI 按完整语境识别，不得扩大到未授权的近似词。可运行 `scripts/prohibited_term_guard.py` 辅助直接匹配；脚本不可用时仍须由 AI 完成同一检查。\n- 绝对词本身不默认属于违禁词，也不能仅因肯定语气自动拦截；只有与一条已授权正式词目在语义上实质等价时，才按该词目处理。\n- 已确认命中时，**只排除命中的完整字幕序号**；同序号里其他正常句也不拆出。多个连续序号共同构成禁用表达时，仅排除实际参与该禁用表达的那些序号。上下文可以用于辨别语义，但不能把前后字幕当作“上下文窗口”连带删除；不连带前后字幕序号。\n- 对正式词库列出的字词或固定表达，命中后排除该完整字幕，并从标题、话题和最终文案中移除对应表达。未命中词条的邻近序号继续按自己的商品归属、事实和价值判断；一次字幕命中不能触发对整段、整条候选或整份输入的防御性淘汰。\n- 目标商品所有离散讲解窗口均执行该规则。一个目标字幕序号同时提到其他商品且其中有禁用表述，也整条排除。\n- 疑似同音/错字、但尚不能可靠确定的序号暂不入正式成片，标记待回听；平台只给笼统拒审原因又无法定位原句时询问用户，不随意把整段判为禁词。\n- 命中后优先从同一目标商品其他合规原话寻找替代，保证语义完整；不得改写、删字造句或重新加入禁用序号。\n- 标题和话题命中禁令只重新生成受影响字段。仅实际命中时在五部分交付中的例外里注明排除序号、禁用表述和原因；无命中不额外报告。\n\n## 上下文风险提示\n\n- 未入正式词库但存在合规或证据风险的表达，只结合具体商品、主张、原话和可用依据作上下文风险提示；不自动加入词库，不直接删除整条字幕或整段内容。提示要说明风险所依赖的语境或待核实依据；风险提示不等于认定违规，也不等于认定合规。风险提示本身不能触发删除，也不能延伸成对相邻序号的排除。\n- 有事实依据的商品工艺、材质描述不得因关键词或肯定语气误杀。例如，确有商品事实支持时，“亮片织进纱线里面”是工艺描述，不能仅因出现“亮片”或陈述为肯定句而拦截。依据不足时只按具体主张提示核实，不升级为正式禁词。\n- “不会掉”等性能承诺要按商品、对象、条件和上下文判断，必要时提示核实其依据；不得仅凭“不会”或“掉”单词列为正式禁词或自动删除整段。问题、否定、引用或其他非肯定语境不得当作同一性能承诺。\n\n## 维护边界\n\n- 用户上传并可定位的新违规截图，或明确指出某表达违规时，AI 按用户确认范围更新**本文件**，检查语义边界、关联冲突并做最小针对性核验；不得自行扩大同类词、绝对词或风险表达。没有成功写入和读取验证，不得声称已永久更新。\n- 只有用户明确提出“更新违禁词”才联网核对当前政策规则。政策变化可以单独形成风险提示或政策简报；未经用户提供的违规截图或对具体违规表达的明确指出，不得据此新增正式词条。\n- 截图中的非文案原因（商品/投放资质、链接等）只记录问题，不自行创造禁用词。重复词句合并，不建立多套类目禁令或复杂编号数据库。\n- 仅有一般“可能违规”、缺少证明但未被用户确认为正式禁令的表达，不因推测而强制禁用；按事实、语境和证据核验。正式词库中列出的词条直接拦截，其他未列表达不扩围。价格/库存/功效等仍按现有平台合规边界独立判断。动态交易信息的日常切片排除规则见 references/editorial-policy.md，这是素材时效管理规则，不代表平台将其认定为违规，也不把这些内容加入本禁用库。\n- 全局禁令是用户内部剪辑选择标准，不可替代平台当次审核判断；不提供规避审核的改写。\n\n## Runtime source 5: `references/editorial-policy.md`\n\n# Universal Core｜动态购买决策结构\n\n本文件规定跨类目购买决策的共通边界。购买决策路径与开头由目标顾客心理、真实原话、商品事实和决策关系共同决定，并按当前商品与素材动态构建。购买决策架构师根据本商品、目标顾客、实际证据、顾虑与独立理由动态构建路径；事实与边界官负责来源和限制；总决策编辑在硬规则内裁决。商品知识包只提供事实提醒，不规定内容结构。\n\n**不存在所有商品通用的段落成交模板、卖点顺序、成交次数或成交位置。**可复用的是顾客价值、证据、适配与决策推进的判断原则；具体路径由当前素材决定。以下购买决策关系用于判断理由是否成立，可按依赖关系重排，也可在素材不支持时省略某一环节。\n\n## 动态顾客心理驱动钩子机制\n\n默认对象是第一次刷到视频、不了解主播和直播背景的陌生潜在买家。完整读取目标商品全部有效窗口、建立全部有效卖点信息池并完成粒度判断后，才跨主题比较开头候选。\n\n把真实钩子原话与理解、延续它所需的紧邻承接联合编排为一个连续开头单元，综合判断前 2 秒能否吸引注意，以及前 5 秒能否把观看兴趣连续承接下去。默认以 1.2 倍速作估算参照：成片前 2 秒约对应原素材累计 2.4 秒，前 5 秒约对应原素材累计 6 秒。两个时间点只用于判断参考，不是选段资格线或硬剪辑点；不得为对齐时间硬截完整原话、半截句子、破坏自然语义或遗漏必要承接。完整自然表达或必要语境超出参考时长时，保留完整原话与必要承接。\n\n承接须依据当前原话动态延续或增强观看动力，例如情绪感染、视觉/动作期待、种草兴趣或具体购买收益；可体现其中一项或多项，也可由素材中的其他有效关系承担，不要求固定类型、顺序或组合。可观察情绪感染、视觉引导、好奇期待、审美种草、场景代入、共情、需求与收益、自然原生感、目标顾客相关性、事实支持及后文承接；这些只是当前素材的观察角度，不是固定检查清单。真实喜爱、动作展示、视觉好奇、具体购买收益等都可成为入口或承接点。以陌生潜在买家的继续观看欲望和与商品相关的购买兴趣作综合判断；这只是文本编排判断，不等于实际留存或成交结果。不设置固定钩子类型优先级、类型顺序、权重、分数或额外语义轮次；也不预设种草或共情优先，不把信息密度、最强卖点、理性收益、共情或种草固定为唯一决定因素。入口之后仍按现有动态购买决策结构组织内容；开头不缩小后续信息池，每条方案继续覆盖全部有效卖点并按原文保留适用且合规的促单。\n\n候选须属于目标商品，离开直播前情仍自然可理解，由同商品原话支撑并能在后文兑现。开头比较只覆盖开头本身，即钩子与必要紧邻承接构成的连续开头单元；不比较、评分或排名完整成片。\n\n真实性、商品归属、正式合规、自然语义与后文兑现是硬边界。主播设问或个人判断可保留为原文候选，但不得包装成真实顾客反馈、普遍事实或商品已存在的缺陷；反馈来源不清须标为待核实。动态价格、库存、优惠、直播过渡或链接提示不作为通用钩子。没有合格候选时，从现有可证实的商品原话中选择与目标顾客兴趣最相关且可自然理解的一段；仍无合适项就如实说明，不拼凑开头。\n\n- 颜色、搭配、材质或外观表达不按关键词禁用或排除。若原话清楚说出显气色、不沉闷、显瘦、利落等具体顾客结果，且来源可信、后文能兑现，它可以与其他候选动态比较；普通或泛泛表达不能仅凭句子完整、先出现或画面暗示自动胜出。\n- 差异性只是观察角度，不是硬门槛；普遍但具体、可信且有支撑的购买结果仍可胜出。\n- 老粉、老顾客、复购用户限定内容默认不代表陌生顾客利益；只有当前目标受众确实是该人群，或同句也给陌生顾客独立决策价值时，才按实际价值比较。\n- 不把主播回答、个人偏好、一般尺码/搭配建议冒充顾客困扰。顾客困扰须来自顾客原话或主播清楚转述；主播明确确认商品存在的负面表现，依事实与适用知识边界判断，不可反向包装成优势。\n- 问题型开头与理解它所需的紧邻回应作为一个入口比较；问题段较长时，可先压缩重复问题、停顿和无增量口头填充，再判断自然节奏，但不改写、硬截或补造原话。\n- 选定入口后，使用最少但足以解释、证明或展示其核心价值的原话。若原素材不能支撑开头，应重新比较候选；不能靠改写、跨商品拼接或虚构解释补强。开头只决定入口，不把后续内容锁进单一主题。\n\n仅凭 SRT，可以判断原话涉及的视觉或情绪吸引潜力，但不能确认实际画面，也不能确认主播的真实语气、表情或情绪表现；这些音画效果必须标为未核验。\n\n## 持续购买决策关系\n\n架构师结合本商品的真实购买问题，选择有用的内容关系，例如结果与原因、特点与使用价值、顾虑与回应、属性与场景、版型与身材效果、材质与穿着体验、适配条件与选择建议。它们是理解原话的候选关系，不是模板、固定排序或要求全覆盖的模块。\n\n每个入选片段都应承担至少一种可理解的工作：提出新购买理由、证明已有理由、回应顾虑、帮助适配/选择、降低决策阻力，或完成必要承接。没有新增或承接价值的重复夸赞、普通过渡和脱离上下文的行动口号，不因“结构完整”而保留；但适用且合规的原文促单须按下文规则完整保留。\n\n主题顺序只决定怎么排，不决定理由留不留。先以最小充分内容兑现已选入口的价值，再让其他独立理由按实际关系进入成片；不因主题不同、类别不同或暂时难衔接就删除有效理由。可重排同一目标商品的原话，但须保留对象、条件、因果和原意，不跨商品或款式混编。\n\n## 完整卖点识别与开头比较前置条件\n\n在现有一次语义分析中，先完整读取目标商品的全部上下文和有效讲解窗口，再识别其全部有效独立购买信息。识别范围不因最终开头、当前主题、首个购买理由或成片角度而缩小；完成全量识别前不生成最终候选、不锁定主线。\n\n完整识别可能涉及顾客结果、用途、顾虑回应、适配条件、搭配/场景、体验、证据、限制和选择帮助；这些只是理解线索，不是要求逐类套用的固定模板。对每项信息保留原话来源、商品归属、必要条件和与其他信息的关系。\n\n### 卖点粒度\n\n覆盖单位是**有效独立购买信息**，不是每句字幕、每个名词或每条例证。先判断内容属于独立理由，还是同一理由的证据、例子、条件、递进或重复。\n\n- 不把同一购买意义下的一组例子机械拆成多个卖点。例如多种裙装、裤装和鞋靴组合可共同说明搭配兼容性；保留足以说明范围的代表性原话即可。\n- 不把不同具体事实过度合并。例如前襟领型与后背褶皱即使都支持设计差异，也可能是独立设计信息；一句泛称“有设计感”不能自动替代全部具体内容。\n- 卖点覆盖不等于每条证明都要保留。选择足以支撑该购买信息的必要证据、条件和代表性例子；若另一个证据新增原因、体验、限制或选择帮助，它可能形成新的有效信息，不能按重复删去。\n- 粒度按当前商品和原话动态判断，不建立固定商品类目表或必填卖点模板。\n\n方案数量、默认双方案、每条独立覆盖与超长处理唯一按 `references/clip-selection-policy.md` 执行。本文件不再定义多方案暂停、主题选择或逐条覆盖例外。\n\n## 重复表达的语义与说服判断\n\n购买决策架构师判断两段表达是否真正重复，以及它们相对现有内容带来的**信息增量**和**说服增量**；购买决策剪辑师执行去留与压缩，总决策编辑结合独立购买理由和注意力/结构占用裁决，成片质量审计官在现有一次终检中核对。四项职责由同一 AI 在现有一次分析和一次终检中完成，不新增角色、轮次或工具。\n\n### 重复裁决顺序（唯一顺序）\n\n对任何疑似重复，必须按以下顺序完成一次判断，不得跳步、倒置或用词面相似度代替语义裁决：\n\n1. **先判同事实**：同时核对商品/款式、对象或部位、属性或关系、事实结论及完整语义；只有这些核心要素指向同一购买事实，才进入重复判断。\n2. **再判新增信息**：检查后一句是否增加原因、证据、体验、条件、场景、程度边界或适配/选择帮助；有新增信息时属于递进或补充，优先保留。\n3. **没有新增信息，再判说服增量**：检查重述是否在当前上下文中明显增强核心利益的记忆、可信感、情绪感染或行动确定感；只有可感知的说服收益才构成有效强调，单纯换词的近义复述不算。\n4. **最后取舍**：两类增量都不成立时，同事实的无增量近义复述默认压缩，只留最完整、自然、清楚且购买价值更高的一处；若有效强调与独立购买理由竞争，仍须判断注意力负担和结构衔接。正常时长本身不能成为删减有效信息的理由，120 秒处理唯一遵循 `references/clip-selection-policy.md`。\n\n同事实不等于必删；新增信息的递进必须保留，有明确说服增量的有效强调可以保留。默认压缩只针对同事实、无信息增量且无说服增量的近义复述。\n\n- **机械性重复**：口误、卡顿、半句重启、未完成表达后紧接完整重说，且没有新增意思、证据或表达效果。通常删除不完整/重复起句，保留完整自然的版本；不得因为字幕文本相似就连同完整句一起删掉。\n- **强调性重复**：在先判同事实、再确认没有新增信息后，重述仍能明显增强顾客记忆、确定感、感染力或说服效果，才可作为有效强调保留；不能把仅换几个词的近义复述当作说服增量，也不要求有效强调另造新事实。\n- **递进性重复**：后句增加原因、证据、体验、适用条件、使用场景、程度边界或选择帮助。它已不只是重复，应优先保留；若只能保留一个片段，选择能完整表达且对当前顾客决策帮助更大的原话。\n- **过度性重复**：相同利益已被充分表达，后续再强调没有明显信息或说服增量，节奏收益低于注意力与结构占用成本。可压缩为最有力、完整、自然的一处；不改写、不拼接句子。判断重复不能以预计秒数或 120 秒为由。\n\n以上是语义类别，不是由词面相似度自动判定的标签。必须先判同事实，再判新增信息，再判说服增量，最后取舍；同事实无增量近义复述默认压缩。不得恢复固定重复次数或“同一句只留一次”的机械规则；同一表达在不同上下文中可分别承担强调、递进或冗余作用。重复取舍还须比较被占用的时间是否会挤掉另一个独立购买理由：有效强调不是无条件优先，机械/过度重复也不能因能延长成片而获豁免。\n\n## 原文促单的保留边界\n\n- 原文存在适用且合规的促单话术时，必须保留完整原话并按原顺序完整保留；不得为开头或时长要求提前移动、拆写原话，也不得因主题、预计时长或主线角度省略、改述。\n- 适用性须核对商品/颜色/对象、条件、价格或活动说明、尺码选择、问题回应、比较关系、链接状态等本地依赖；不得只凭“拍/买/入/拿”等词判断。\n- 原文没有促单时，禁止编造、改写或补充；不得跨商品移用话术，也不得用近义句替代。不得为结尾完整或转化要求增写行动口号。\n- 动态价格、优惠、库存、限时、直播专属福利、涨价和稀缺信息仍按全局规则处理；不合规内容不因其属于促单而保留。\n\n## 原话、混合信息与动态交易边界\n\n- 原话逐字保留，只能重排同一商品的完整原话；不润色、改写、补词或拼接不连续片段。命中全局禁令时，依 global-rules.md 排除完整原始字幕序号。\n- “它/这个/那款”等指代不清时，核对必要前后文；仍不能确认商品归属则不选入正式方案或明确标待核实。疑似转写错误保留原字并标注回听，不代改。\n- 具体商品价格、优惠、赠品、直播福利、倒计时、库存/稀缺数量及其他依赖实时交易条件的信息，全片默认排除。只有用户明确要求制作有效期明确的活动素材且确认活动与发布时段仍有效，才对该任务例外；该例外不扩展全局禁令。\n- 混合字幕只有在排除动态部分后，仍能逐字保留原始连续、语法完整、语义自足且自然衔接的原话子句时才可使用。仅剩词组或残句就舍弃整条相关字幕；不改写、补词或拼接。命中全局禁令仍排除完整原始序号。\n- 购买者反馈只有在来源清楚、原话完整时才能作为候选；主播泛称“大家都喜欢”不等于真实顾客反馈。无法核实的社会证明就地标明，不扩写成普遍结论。\n- 安全风险、护理要求或明确不适用条件不能被剪掉后留下相反的无条件承诺；依据不足时按全局合规规则标待核实。\n\n## Runtime source 6: `references/highlight-selection.md`\n\n# C2 Universal 0.4.7｜购买信息价值与重复判断\n\n本文件维护购买价值和重复判断；方案数量、时长及覆盖规则唯一见 `references/clip-selection-policy.md`。开头比较见 `references/editorial-policy.md`；事实与归属边界见 `references/global-rules.md` 及适用的商品知识包。全部判断由同一 AI 在一次分析和一次终检中完成。\n\n## 购买决策价值层级\n\n价值等级按当前商品、目标顾客和具体方案动态判断，不把某类商品信息固定成高、中、低等级。有效性与价值排序是两个判断；低价值不等于无效，也不等于弱增量。低价值信息的覆盖义务和仅在超长时的处理唯一按 `references/clip-selection-policy.md`。\n\n## 重复表达：信息增量、说服增量与机会成本\n\n对疑似重复的片段，在现有一次语义分析中按唯一顺序判断，不跳步：**先判同事实→判新增信息→判说服增量→最后取舍**。只有前一步成立后才进入下一步；不把同一主题、词面相似或句式相近直接当成重复。\n\n在上述顺序中同时判断两类增量：\n\n1. **信息增量**：是否加入新的理由、解释、证据、体验、条件、程度、场景或适配/选择帮助。\n2. **说服增量**：即使事实相同，重述是否能在当前语境中明显加强顾客对核心利益的记忆、可信感、情绪感染或行动确定感。\n\n据此区分并处理：\n\n| 类型 | 识别要点 | 默认处理 |\n|---|---|---|\n| 机械性重复 | 口误、卡顿、半句重启、未完成句被完整句重说，未增加信息或说服作用 | 删除机械片段，保留完整、自然的表达；若仅前段无效，不能连完整句一起删。 |\n| 强调性重复 | 同事实且没有新增信息，但重述有可感知的记忆/感染/说服作用 | 允许保留为有效强调；必须确认不是单纯换词，并且没有挤占更重要的独立购买理由或拖慢节奏。 |\n| 递进性重复 | 后句带来原因、证据、体验、条件、程度边界或选择帮助 | 优先保留其新增部分；它不是纯重复。 |\n| 过度性重复 | 同一事实已充分表达，后续没有明显新增信息或说服作用 | 默认压缩到最有力、完整、自然的一处；不得为增加时长而保留。 |\n\n先判同事实不等于必删；同一购买事实的重复表达仍须先判断新增信息与说服增量：有新增原因、证据、体验、条件、程度边界或选择帮助的递进必须保留；没有新增信息但有明确说服增量的有效强调可以保留。只有两类增量都没有时，才在最后取舍阶段默认压缩同事实的无增量近义复述。不得按词面相似度、固定重复次数或“一条字幕只留一次”规则机械删除。判断单位是当前语境中的完整表达及其顾客决策作用，而不是相同字词；一个词面不同的句子也可能没有任何增量。\n\n**机会成本检查：**有效强调的保留价值须与它占用的注意力及可能挤掉的独立购买理由比较。强调有助于记住主利益，却不能因此吞掉尺码适配、顾虑回应或其他会改变购买决定的独立理由。重复类别按语义增量判定；超长状态下是否动态筛选有效信息，遵循 `references/clip-selection-policy.md`。\n\n## 卖点覆盖与证据选择\n\n卖点覆盖、每条方案独立编排、超长例外与省略项记录，唯一遵循 `references/clip-selection-policy.md`。证据覆盖不等于卖点覆盖：同一理由有多组支持时，可选足以成立的最好表达；新增原因、证据、体验、场景、限制或选择帮助若构成新的购买信息或必要条件，仍须纳入判断。每个入选片段应提出理由、证明理由、回应顾虑、帮助选择或完成必要承接；泛夸赞和普通过渡没有新增作用时可压缩。完整购买理由必须有原话支撑并保留必要条件；不得以行动口号替代证据。\n\n## 开头比较\n\n开头候选的范围和动态顾客心理驱动钩子机制见 `references/editorial-policy.md`。信息池后的方案数量、逐条独立编排、120 秒处理及验收唯一遵循 `references/clip-selection-policy.md`。本文件不再定义暂停等待用户选择或时长规则。\n\n## 原文促单的保留\n\n原文存在适用且合规的促单话术时，必须保留完整原话，按原顺序完整保留原句及成立所需的上下文，不删节、不拆写、不改述。先核对商品、对象、条件和交易依赖；动态交易信息仍按全局规则处理。原文没有适用且合规的促单时，禁止编造、改写、补充、从其他商品移用或用近义句替代。促单不能替代理由所需的证据和适配条件。\n## 停止条件\n\n停止条件与每条方案的覆盖判定遵循 `references/clip-selection-policy.md`；核心角度或主题顺序本身不改变有效性判断。\n\n## Runtime source 7: `references/product-knowledge-registry.md`\n\n# 商品知识包注册表\n\n## 用途与边界\n\n商品知识包是事实核对提示和边界参考，不是类目路由器、内容模块或剪辑模板。\n\n- 购买决策架构师始终根据当前商品、顾客逻辑、原话证据与独立购买理由动态构建内容。\n- 商品事实与边界官只在能帮助核对当前商品的属性、限制、证据或归属时参考一个或多个知识包。参考与否不决定任务能否开始。\n- 知识包不得规定开头、中段、成交、结尾、卖点排序、固定覆盖、话题、时长或输出格式，也不得替代全局合规和来源核对。\n- 多个商品类别同时出现时，可以分别参考适用知识包，但分别保持商品与款式事实边界；不得把一个商品的信息移给另一个商品。\n- 未注册类别仍可按 Universal Core 正常处理。没有专业依据时不套用相近类别知识，也不编造行业规则或商品事实。\n\n## 当前知识包\n\n| 文件 | 可参考的事实边界 |\n|---|---|\n| product-knowledge-packs/womens-fashion.md | 服装、箱包及相关穿搭单品的版型、材质、适用条件和商品归属风险 |\n| product-knowledge-packs/shoes.md | 鞋款、鞋底、脚型尺码、材质、场景及画面依赖风险 |\n| product-knowledge-packs/scarves.md | 围巾与颈部配饰的材质、肤感、围法、护理及款式归属风险 |\n\n## 未注册或不适用的类别\n\n首饰、美妆、童装、家居、食品、数码及其他未登记商品不需要先建立知识包才能剪辑。事实与边界官基于本次原话和可靠来源处理归属、条件与风险；需要专业事实但无依据时标为待核实，不把另一类商品知识当作替代。\n\n## 新增与维护\n\n仅当重复出现的商品事实边界确实改善核对质量时新增知识包。文件必须清楚写明适用商品、需要区分的事实、不能推断的内容、证据/归属风险；不能建立固定开头、卖点顺序、成交话术或强制类别路径。更新后同步本注册表及便携版，并由回归检查确认知识包没有取得内容结构或语义裁决权。\n\n## 话题\n\n标题和五个话题由总决策编辑根据当前商品、顾客与成片真实主线动态生成。知识包不预设固定话题；所有输出遵守全局禁令和事实边界。\n\n## Runtime source 8: `references/final-check.md`\n\n# Final Quality Auditor｜实际成片终检\n\n验收结论只允许标记为 **PASS / FAIL / BLOCKED**。PASS 表示本轮实际输出的成片已完成适用检查；FAIL 表示检查已执行并发现可修复问题；BLOCKED 表示输入、来源或外部依赖缺失，无法完成相关检查。没有成片时不产生最终成片审计结论。\n\n## 终检范围与修复\n\n只对实际写出的成片执行终检；每条均独立核对适用覆盖、必要证据与条件、原话、商品归属、正式合规边界和衔接。方案数量、逐条覆盖和超长例外唯一按 `references/clip-selection-policy.md`；方案之间不能互相补足。\n\n发现 FAIL 后，定位失败项及共同根因，只修复受影响内容；随后复查导致失败的项目、关联上下文和受影响回归，再完成实际成片终检。同一根因最多三轮实质修复。仍失败时保留 FAIL 并报告证据，不降低标准、不跳过项目或隐藏结果。新问题属于不同根因时可单独处理。\n\n## 机器判定与 AI 语义判断\n\n可选脚本按实际使用方式记录 `verification_mode: script`；只有真正运行后才能称为脚本核验。未运行或工具不可用时记为 `manual`，用“模型逐条对照”，不可声称机检通过。工具是否可用不改变语义标准，也不是五部分交付的前置条件。\n\n机器只检查可确定的结构和正式词库直接命中；机器不判断信息池完整性、原话语义支持、商品归属或条件是否充分，这些由 AI 的语义判断完成：\n\n- 记录解析块数、总块数、已解析与未解析范围、行号及诊断。无法解析的范围为 BLOCKED；不得将其描述为已完整核验。\n- 检查序号重复或倒置、时间码倒置和非正时长。SRT 按连续源序号组计算“末条 end − 首条 start”；逐条时长文本累计入选条目。\n- 对每一条实际成片的 selection JSON，仅检查序号是否来自来源且已入选、每个信息点至少有一个来源支撑、每个入选序号恰有一个允许角色、必要字段结构完整。结构检查不判断语义覆盖是否成立。\n- 逐字来源文本、选段组装、第五部分序号与时长显示引用同一实际选择记录；源 SHA-256 必须匹配。已知未加速时长仅可用于显示估算。\n- 正式禁词 gate 只扫描 `references/global-rules.md` 的直接命中。机器仅排除完整命中的原始字幕序号，不连带排除邻近内容。`risk_hint` 原样提供语义判断，不得自动升级为硬失败，也不是合规结论。\n\n以下判断由 AI 完成，不由脚本 gate 代替：\n\n1. 完整读取范围、目标商品窗口、商品/款式归属和信息池粒度是否准确；没有把不同商品混编。\n2. 每条实际成片是否按 `references/clip-selection-policy.md` 独立承载应有信息及必要证据、适用条件和限制；其他成片不能补足本条。\n3. 每段原话是否在真实上下文中支持其信息点；重排后对象、代词、条件、因果和相邻衔接是否仍成立。\n4. 是否保留适用且合规的原文促单完整表达及其必要上下文；原文没有时是否避免编造、改写、补充或跨商品移用。动态交易信息仍按全局规则处理。\n5. 正式词库之外的语义等价、事实边界和上下文风险；风险提示不自动拦截，也不构成事实核实或合规结论。\n6. 开头是否在完整信息池后把真实钩子原话与必要紧邻承接联合编排，综合判断前 2 秒吸引力及前 5 秒连续吸引力；默认按 1.2 倍速将原素材累计 2.4 秒、6 秒作为参考而非硬剪辑点，未为贴合时间硬截原话；承接按素材动态延续情绪、视觉/动作期待、种草兴趣或购买收益等动力，没有固定类型、顺序、权重或评分；主播设问没有被包装为真实顾客反馈；仅凭 SRT 时音画效果标为未核验。\n7. 实际方案数量是否符合 `references/clip-selection-policy.md`，默认双方案是否具备独立购买核心；若只交付一条，是否说明第二条不能成立或会降低质量的具体原因；若超长是否记录动态筛选与省略项。\n8. 时长是否在完整编排后计算；未明显超过 120 秒时是否保留全部有效信息，超长时是否按该方案核心动态筛选、保留完整购买决策并说明有效信息省略项。\n9. 标题、话题及固定五部分是否满足当前任务要求；序号与正文一致。\n\n## 明确失败项\n\n出现任一项，实际成片验收不通过：\n\n- 未完整读取目标商品有效窗口或未建立完整信息池，就比较开头或写方案。\n- 开头比较扩展为完整成片竞争、资格评分或多维排名，或把某类钩子固定为优先；未把钩子与紧邻承接联合判断；把 1.2 倍速对应的 2.4 秒/6 秒当成硬剪辑点并硬截原话；主播设问被写成顾客真实反馈；仅凭 SRT 声称视觉、语气、表情或情绪已验证。\n- 未按 `references/clip-selection-policy.md` 直接交付默认双方案，且未能说明第二方案不能成立或会降低质量的具体原因；或把第二方案做成仅交换顺序的重复版本。\n- 摘要有效时仍强制重新完整读取所有规则，或摘要失效/缺失/哈希不匹配时继续按摘要执行。\n- 任一实际输出方案不符合逐条覆盖与超长例外规则，或用其他方案补足本条。\n- 原话改写、补造、不连续拼接、来源编号错误、商品串用或条件/归属改变。\n- 原文存在适用且合规的促单话术却未完整保留；原文没有时编造、改写、补充或跨商品移用；或把动态交易信息错误保留。\n- 将正式禁词范围扩大到未命中的邻近字幕，或把风险提示当成机器硬失败或合规结论。\n- 把 120 秒当作目标或硬上限、未先完成完整编排就删点，或超长时按固定卖点类别删选而破坏购买决策完整性。\n- 五部分交付缺项，或声称执行了未运行的脚本、读取了未读内容、核验了未查看的音画或同步了无法读回的渠道。\n- 加入多个 AI/Agent、额外语义轮次、普通文本任务必须通过的工具或环境门槛。\n\n## 检查项\n\n1. **输入与范围**：确认来源类型、解析状态、实际已读范围、目标商品和必要上下文；未读或截断部分不能声称已检查。\n2. **读取顺序与完整信息池**：确认所有目标窗口读完后才建立完整信息池并控制粒度；未因第一条强卖点或局部方案提前锁定角度。\n3. **粒度、归属与事实边界**：有效独立购买信息未被拆得过细或合并遗漏；商品、款式、对象、限制和适用条件清楚。\n4. **开头选择**：在完整信息池后，把真实钩子原话与必要紧邻承接联合编排；综合判断前 2 秒吸引力与前 5 秒连续吸引力。默认 1.2 倍速下原素材累计 2.4 秒/6 秒仅供估算参考，不硬截完整原话；承接按素材动态延续观看动力，不固定类型、顺序、权重或评分；不将主播设问当顾客反馈，也不把未核验音画说成已验证。\n5. **方案数量与差异**：按唯一规则交付默认两条或说明单条例外；各方案核心、排序和结构实质不同。\n6. **逐条完整覆盖**：每条方案独立从完整信息池编排；未明显超 120 秒时覆盖全部有效信息，超长例外按唯一规则核对；并集不代替逐条核对。\n7. **原话与促单**：来源、序号和完整语境一致；适用且合规的促单按原话保留，没有来源时不补造；风险和动态交易信息依全局规则处理。\n8. **时长与信息密度**：每条先完成全量编排再计算时长；120 秒不是目标或硬上限。按唯一规则判断是否触发超长预设、逐条动态筛选及未采用信息说明。\n9. **脚本核验与人工边界**：脚本只支持结构及直接命中检查；语义卖点覆盖、原话支持、事实归属、限制和衔接由 AI 判断。实际未运行的工具明确标为手工对照。\n10. **交付**：终检所有实际写出的成片；输出保持固定五部分，序号与正文一致，所有待核和未验证事项如实说明。"
}

## Embedded source: references/runtime-manifest.json

{
  "version": 1,
  "entry_file": "SKILL.md",
  "required_files": [
    "references/runtime-current.md"
  ],
  "conditional_files": [
    {
      "path": "references/long-context-mode.md",
      "when": "Long Context Mode is needed"
    },
    {
      "path": "references/update-protocol.md",
      "when": "Updating C2 Universal rules, files, or releases"
    },
    {
      "path": "product-knowledge-packs/*.md",
      "when": "A product knowledge pack materially helps fact or attribution checks"
    }
  ],
  "schema_version": 3,
  "core_version": "0.4.7",
  "runtime_file": "references/runtime-current.md",
  "source_files": [
    "references/ai-first-constitution.md",
    "references/runtime-contract.md",
    "references/clip-selection-policy.md",
    "references/global-rules.md",
    "references/editorial-policy.md",
    "references/highlight-selection.md",
    "references/product-knowledge-registry.md",
    "references/final-check.md"
  ],
  "skill_version": "0.4.29",
  "summary_file": "references/execution-summary.json",
  "source_hashes": {
    "references/ai-first-constitution.md": "c65ad8bfcaaa986c81f25038c38010de7d8f9566a1bf5e09a9ad3e2ad57e2928",
    "references/runtime-contract.md": "d8dfeaa987381ff6c5baa4e4bb68102be4e18393fb436cec226ad3fd62dc29bb",
    "references/clip-selection-policy.md": "4ef31bcd79a4debded6db374a28b55c326b36dc940db42a9d89a729686a75109",
    "references/global-rules.md": "ee2b1a223ddfe16670dc5bc46669ee1750d3e2d0b86db1e98513338b7c505bf6",
    "references/editorial-policy.md": "222a6b2094f06679751f0a808c734bd7271033f85af80a72597859edcc034008",
    "references/highlight-selection.md": "7a12ea2b7dfa7909eda54e42b69c765f5957ed1078f6fd12819a9111168efc85",
    "references/product-knowledge-registry.md": "6737b6c8df8e6fbcdccc4a30439f66ae15f3a2fb09efb380bd285e7437fce19d",
    "references/final-check.md": "739e0bca7f7ea585dc426a4814db6f42f37b1c82674add8ae15d380ac8e092b7"
  },
  "runtime_sha256": "6326a8453e592a6c255d5937fe4374e20a97b8d0dc02b2f63284bf4cac45fa48",
  "source_map": [
    {
      "rule_id": "SRC01.L0001",
      "source": "references/ai-first-constitution.md",
      "source_line": 1,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 9
    },
    {
      "rule_id": "SRC01.L0003",
      "source": "references/ai-first-constitution.md",
      "source_line": 3,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 11
    },
    {
      "rule_id": "SRC01.L0005",
      "source": "references/ai-first-constitution.md",
      "source_line": 5,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 13
    },
    {
      "rule_id": "SRC01.L0007",
      "source": "references/ai-first-constitution.md",
      "source_line": 7,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 15
    },
    {
      "rule_id": "SRC01.L0009",
      "source": "references/ai-first-constitution.md",
      "source_line": 9,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 17
    },
    {
      "rule_id": "SRC01.L0011",
      "source": "references/ai-first-constitution.md",
      "source_line": 11,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 19
    },
    {
      "rule_id": "SRC01.L0012",
      "source": "references/ai-first-constitution.md",
      "source_line": 12,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 20
    },
    {
      "rule_id": "SRC01.L0013",
      "source": "references/ai-first-constitution.md",
      "source_line": 13,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 21
    },
    {
      "rule_id": "SRC01.L0015",
      "source": "references/ai-first-constitution.md",
      "source_line": 15,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 23
    },
    {
      "rule_id": "SRC01.L0017",
      "source": "references/ai-first-constitution.md",
      "source_line": 17,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 25
    },
    {
      "rule_id": "SRC01.L0018",
      "source": "references/ai-first-constitution.md",
      "source_line": 18,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 26
    },
    {
      "rule_id": "SRC01.L0019",
      "source": "references/ai-first-constitution.md",
      "source_line": 19,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 27
    },
    {
      "rule_id": "SRC01.L0020",
      "source": "references/ai-first-constitution.md",
      "source_line": 20,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 28
    },
    {
      "rule_id": "SRC01.L0022",
      "source": "references/ai-first-constitution.md",
      "source_line": 22,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 30
    },
    {
      "rule_id": "SRC01.L0024",
      "source": "references/ai-first-constitution.md",
      "source_line": 24,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 32
    },
    {
      "rule_id": "SRC01.L0026",
      "source": "references/ai-first-constitution.md",
      "source_line": 26,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 34
    },
    {
      "rule_id": "SRC01.L0028",
      "source": "references/ai-first-constitution.md",
      "source_line": 28,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 36
    },
    {
      "rule_id": "SRC01.L0030",
      "source": "references/ai-first-constitution.md",
      "source_line": 30,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 38
    },
    {
      "rule_id": "SRC01.L0031",
      "source": "references/ai-first-constitution.md",
      "source_line": 31,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 39
    },
    {
      "rule_id": "SRC01.L0032",
      "source": "references/ai-first-constitution.md",
      "source_line": 32,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 40
    },
    {
      "rule_id": "SRC01.L0034",
      "source": "references/ai-first-constitution.md",
      "source_line": 34,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 42
    },
    {
      "rule_id": "SRC01.L0036",
      "source": "references/ai-first-constitution.md",
      "source_line": 36,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 44
    },
    {
      "rule_id": "SRC01.L0037",
      "source": "references/ai-first-constitution.md",
      "source_line": 37,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 45
    },
    {
      "rule_id": "SRC01.L0038",
      "source": "references/ai-first-constitution.md",
      "source_line": 38,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 46
    },
    {
      "rule_id": "SRC01.L0040",
      "source": "references/ai-first-constitution.md",
      "source_line": 40,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 48
    },
    {
      "rule_id": "SRC01.L0042",
      "source": "references/ai-first-constitution.md",
      "source_line": 42,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 50
    },
    {
      "rule_id": "SRC01.L0043",
      "source": "references/ai-first-constitution.md",
      "source_line": 43,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 51
    },
    {
      "rule_id": "SRC01.L0044",
      "source": "references/ai-first-constitution.md",
      "source_line": 44,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 52
    },
    {
      "rule_id": "SRC01.L0045",
      "source": "references/ai-first-constitution.md",
      "source_line": 45,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 53
    },
    {
      "rule_id": "SRC01.L0046",
      "source": "references/ai-first-constitution.md",
      "source_line": 46,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 54
    },
    {
      "rule_id": "SRC01.L0047",
      "source": "references/ai-first-constitution.md",
      "source_line": 47,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 55
    },
    {
      "rule_id": "SRC01.L0049",
      "source": "references/ai-first-constitution.md",
      "source_line": 49,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 57
    },
    {
      "rule_id": "SRC01.L0051",
      "source": "references/ai-first-constitution.md",
      "source_line": 51,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 59
    },
    {
      "rule_id": "SRC01.L0053",
      "source": "references/ai-first-constitution.md",
      "source_line": 53,
      "runtime_section": "Runtime source 1: references/ai-first-constitution.md",
      "runtime_line": 61
    },
    {
      "rule_id": "SRC02.L0001",
      "source": "references/runtime-contract.md",
      "source_line": 1,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 65
    },
    {
      "rule_id": "SRC02.L0003",
      "source": "references/runtime-contract.md",
      "source_line": 3,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 67
    },
    {
      "rule_id": "SRC02.L0005",
      "source": "references/runtime-contract.md",
      "source_line": 5,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 69
    },
    {
      "rule_id": "SRC02.L0007",
      "source": "references/runtime-contract.md",
      "source_line": 7,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 71
    },
    {
      "rule_id": "SRC02.L0008",
      "source": "references/runtime-contract.md",
      "source_line": 8,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 72
    },
    {
      "rule_id": "SRC02.L0009",
      "source": "references/runtime-contract.md",
      "source_line": 9,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 73
    },
    {
      "rule_id": "SRC02.L0010",
      "source": "references/runtime-contract.md",
      "source_line": 10,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 74
    },
    {
      "rule_id": "SRC02.L0012",
      "source": "references/runtime-contract.md",
      "source_line": 12,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 76
    },
    {
      "rule_id": "SRC02.L0014",
      "source": "references/runtime-contract.md",
      "source_line": 14,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 78
    },
    {
      "rule_id": "SRC02.L0016",
      "source": "references/runtime-contract.md",
      "source_line": 16,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 80
    },
    {
      "rule_id": "SRC02.L0018",
      "source": "references/runtime-contract.md",
      "source_line": 18,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 82
    },
    {
      "rule_id": "SRC02.L0019",
      "source": "references/runtime-contract.md",
      "source_line": 19,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 83
    },
    {
      "rule_id": "SRC02.L0020",
      "source": "references/runtime-contract.md",
      "source_line": 20,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 84
    },
    {
      "rule_id": "SRC02.L0021",
      "source": "references/runtime-contract.md",
      "source_line": 21,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 85
    },
    {
      "rule_id": "SRC02.L0022",
      "source": "references/runtime-contract.md",
      "source_line": 22,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 86
    },
    {
      "rule_id": "SRC02.L0023",
      "source": "references/runtime-contract.md",
      "source_line": 23,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 87
    },
    {
      "rule_id": "SRC02.L0025",
      "source": "references/runtime-contract.md",
      "source_line": 25,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 89
    },
    {
      "rule_id": "SRC02.L0027",
      "source": "references/runtime-contract.md",
      "source_line": 27,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 91
    },
    {
      "rule_id": "SRC02.L0028",
      "source": "references/runtime-contract.md",
      "source_line": 28,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 92
    },
    {
      "rule_id": "SRC02.L0029",
      "source": "references/runtime-contract.md",
      "source_line": 29,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 93
    },
    {
      "rule_id": "SRC02.L0030",
      "source": "references/runtime-contract.md",
      "source_line": 30,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 94
    },
    {
      "rule_id": "SRC02.L0032",
      "source": "references/runtime-contract.md",
      "source_line": 32,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 96
    },
    {
      "rule_id": "SRC02.L0034",
      "source": "references/runtime-contract.md",
      "source_line": 34,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 98
    },
    {
      "rule_id": "SRC02.L0036",
      "source": "references/runtime-contract.md",
      "source_line": 36,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 100
    },
    {
      "rule_id": "SRC02.L0038",
      "source": "references/runtime-contract.md",
      "source_line": 38,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 102
    },
    {
      "rule_id": "SRC02.L0040",
      "source": "references/runtime-contract.md",
      "source_line": 40,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 104
    },
    {
      "rule_id": "SRC02.L0042",
      "source": "references/runtime-contract.md",
      "source_line": 42,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 106
    },
    {
      "rule_id": "SRC02.L0044",
      "source": "references/runtime-contract.md",
      "source_line": 44,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 108
    },
    {
      "rule_id": "SRC02.L0046",
      "source": "references/runtime-contract.md",
      "source_line": 46,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 110
    },
    {
      "rule_id": "SRC02.L0048",
      "source": "references/runtime-contract.md",
      "source_line": 48,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 112
    },
    {
      "rule_id": "SRC02.L0050",
      "source": "references/runtime-contract.md",
      "source_line": 50,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 114
    },
    {
      "rule_id": "SRC02.L0052",
      "source": "references/runtime-contract.md",
      "source_line": 52,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 116
    },
    {
      "rule_id": "SRC02.L0054",
      "source": "references/runtime-contract.md",
      "source_line": 54,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 118
    },
    {
      "rule_id": "SRC02.L0056",
      "source": "references/runtime-contract.md",
      "source_line": 56,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 120
    },
    {
      "rule_id": "SRC02.L0058",
      "source": "references/runtime-contract.md",
      "source_line": 58,
      "runtime_section": "Runtime source 2: references/runtime-contract.md",
      "runtime_line": 122
    },
    {
      "rule_id": "SRC03.L0001",
      "source": "references/clip-selection-policy.md",
      "source_line": 1,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 126
    },
    {
      "rule_id": "SRC03.L0003",
      "source": "references/clip-selection-policy.md",
      "source_line": 3,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 128
    },
    {
      "rule_id": "SRC03.L0005",
      "source": "references/clip-selection-policy.md",
      "source_line": 5,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 130
    },
    {
      "rule_id": "SRC03.L0007",
      "source": "references/clip-selection-policy.md",
      "source_line": 7,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 132
    },
    {
      "rule_id": "SRC03.L0009",
      "source": "references/clip-selection-policy.md",
      "source_line": 9,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 134
    },
    {
      "rule_id": "SRC03.L0011",
      "source": "references/clip-selection-policy.md",
      "source_line": 11,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 136
    },
    {
      "rule_id": "SRC03.L0013",
      "source": "references/clip-selection-policy.md",
      "source_line": 13,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 138
    },
    {
      "rule_id": "SRC03.L0015",
      "source": "references/clip-selection-policy.md",
      "source_line": 15,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 140
    },
    {
      "rule_id": "SRC03.L0016",
      "source": "references/clip-selection-policy.md",
      "source_line": 16,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 141
    },
    {
      "rule_id": "SRC03.L0017",
      "source": "references/clip-selection-policy.md",
      "source_line": 17,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 142
    },
    {
      "rule_id": "SRC03.L0018",
      "source": "references/clip-selection-policy.md",
      "source_line": 18,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 143
    },
    {
      "rule_id": "SRC03.L0019",
      "source": "references/clip-selection-policy.md",
      "source_line": 19,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 144
    },
    {
      "rule_id": "SRC03.L0021",
      "source": "references/clip-selection-policy.md",
      "source_line": 21,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 146
    },
    {
      "rule_id": "SRC03.L0023",
      "source": "references/clip-selection-policy.md",
      "source_line": 23,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 148
    },
    {
      "rule_id": "SRC03.L0024",
      "source": "references/clip-selection-policy.md",
      "source_line": 24,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 149
    },
    {
      "rule_id": "SRC03.L0025",
      "source": "references/clip-selection-policy.md",
      "source_line": 25,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 150
    },
    {
      "rule_id": "SRC03.L0026",
      "source": "references/clip-selection-policy.md",
      "source_line": 26,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 151
    },
    {
      "rule_id": "SRC03.L0027",
      "source": "references/clip-selection-policy.md",
      "source_line": 27,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 152
    },
    {
      "rule_id": "SRC03.L0029",
      "source": "references/clip-selection-policy.md",
      "source_line": 29,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 154
    },
    {
      "rule_id": "SRC03.L0031",
      "source": "references/clip-selection-policy.md",
      "source_line": 31,
      "runtime_section": "Runtime source 3: references/clip-selection-policy.md",
      "runtime_line": 156
    },
    {
      "rule_id": "SRC04.L0001",
      "source": "references/global-rules.md",
      "source_line": 1,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 160
    },
    {
      "rule_id": "SRC04.L0003",
      "source": "references/global-rules.md",
      "source_line": 3,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 162
    },
    {
      "rule_id": "SRC04.L0005",
      "source": "references/global-rules.md",
      "source_line": 5,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 164
    },
    {
      "rule_id": "SRC04.L0007",
      "source": "references/global-rules.md",
      "source_line": 7,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 166
    },
    {
      "rule_id": "SRC04.L0009",
      "source": "references/global-rules.md",
      "source_line": 9,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 168
    },
    {
      "rule_id": "SRC04.L0011",
      "source": "references/global-rules.md",
      "source_line": 11,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 170
    },
    {
      "rule_id": "SRC04.L0012",
      "source": "references/global-rules.md",
      "source_line": 12,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 171
    },
    {
      "rule_id": "SRC04.L0013",
      "source": "references/global-rules.md",
      "source_line": 13,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 172
    },
    {
      "rule_id": "SRC04.L0014",
      "source": "references/global-rules.md",
      "source_line": 14,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 173
    },
    {
      "rule_id": "SRC04.L0015",
      "source": "references/global-rules.md",
      "source_line": 15,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 174
    },
    {
      "rule_id": "SRC04.L0017",
      "source": "references/global-rules.md",
      "source_line": 17,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 176
    },
    {
      "rule_id": "SRC04.L0019",
      "source": "references/global-rules.md",
      "source_line": 19,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 178
    },
    {
      "rule_id": "SRC04.L0020",
      "source": "references/global-rules.md",
      "source_line": 20,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 179
    },
    {
      "rule_id": "SRC04.L0021",
      "source": "references/global-rules.md",
      "source_line": 21,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 180
    },
    {
      "rule_id": "SRC04.L0022",
      "source": "references/global-rules.md",
      "source_line": 22,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 181
    },
    {
      "rule_id": "SRC04.L0024",
      "source": "references/global-rules.md",
      "source_line": 24,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 183
    },
    {
      "rule_id": "SRC04.L0026",
      "source": "references/global-rules.md",
      "source_line": 26,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 185
    },
    {
      "rule_id": "SRC04.L0027",
      "source": "references/global-rules.md",
      "source_line": 27,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 186
    },
    {
      "rule_id": "SRC04.L0028",
      "source": "references/global-rules.md",
      "source_line": 28,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 187
    },
    {
      "rule_id": "SRC04.L0029",
      "source": "references/global-rules.md",
      "source_line": 29,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 188
    },
    {
      "rule_id": "SRC04.L0031",
      "source": "references/global-rules.md",
      "source_line": 31,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 190
    },
    {
      "rule_id": "SRC04.L0033",
      "source": "references/global-rules.md",
      "source_line": 33,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 192
    },
    {
      "rule_id": "SRC04.L0034",
      "source": "references/global-rules.md",
      "source_line": 34,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 193
    },
    {
      "rule_id": "SRC04.L0035",
      "source": "references/global-rules.md",
      "source_line": 35,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 194
    },
    {
      "rule_id": "SRC04.L0036",
      "source": "references/global-rules.md",
      "source_line": 36,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 195
    },
    {
      "rule_id": "SRC04.L0037",
      "source": "references/global-rules.md",
      "source_line": 37,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 196
    },
    {
      "rule_id": "SRC04.L0038",
      "source": "references/global-rules.md",
      "source_line": 38,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 197
    },
    {
      "rule_id": "SRC04.L0039",
      "source": "references/global-rules.md",
      "source_line": 39,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 198
    },
    {
      "rule_id": "SRC04.L0040",
      "source": "references/global-rules.md",
      "source_line": 40,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 199
    },
    {
      "rule_id": "SRC04.L0042",
      "source": "references/global-rules.md",
      "source_line": 42,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 201
    },
    {
      "rule_id": "SRC04.L0044",
      "source": "references/global-rules.md",
      "source_line": 44,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 203
    },
    {
      "rule_id": "SRC04.L0045",
      "source": "references/global-rules.md",
      "source_line": 45,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 204
    },
    {
      "rule_id": "SRC04.L0046",
      "source": "references/global-rules.md",
      "source_line": 46,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 205
    },
    {
      "rule_id": "SRC04.L0048",
      "source": "references/global-rules.md",
      "source_line": 48,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 207
    },
    {
      "rule_id": "SRC04.L0050",
      "source": "references/global-rules.md",
      "source_line": 50,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 209
    },
    {
      "rule_id": "SRC04.L0051",
      "source": "references/global-rules.md",
      "source_line": 51,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 210
    },
    {
      "rule_id": "SRC04.L0052",
      "source": "references/global-rules.md",
      "source_line": 52,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 211
    },
    {
      "rule_id": "SRC04.L0053",
      "source": "references/global-rules.md",
      "source_line": 53,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 212
    },
    {
      "rule_id": "SRC04.L0054",
      "source": "references/global-rules.md",
      "source_line": 54,
      "runtime_section": "Runtime source 4: references/global-rules.md",
      "runtime_line": 213
    },
    {
      "rule_id": "SRC05.L0001",
      "source": "references/editorial-policy.md",
      "source_line": 1,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 217
    },
    {
      "rule_id": "SRC05.L0003",
      "source": "references/editorial-policy.md",
      "source_line": 3,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 219
    },
    {
      "rule_id": "SRC05.L0005",
      "source": "references/editorial-policy.md",
      "source_line": 5,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 221
    },
    {
      "rule_id": "SRC05.L0007",
      "source": "references/editorial-policy.md",
      "source_line": 7,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 223
    },
    {
      "rule_id": "SRC05.L0009",
      "source": "references/editorial-policy.md",
      "source_line": 9,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 225
    },
    {
      "rule_id": "SRC05.L0011",
      "source": "references/editorial-policy.md",
      "source_line": 11,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 227
    },
    {
      "rule_id": "SRC05.L0013",
      "source": "references/editorial-policy.md",
      "source_line": 13,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 229
    },
    {
      "rule_id": "SRC05.L0015",
      "source": "references/editorial-policy.md",
      "source_line": 15,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 231
    },
    {
      "rule_id": "SRC05.L0017",
      "source": "references/editorial-policy.md",
      "source_line": 17,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 233
    },
    {
      "rule_id": "SRC05.L0019",
      "source": "references/editorial-policy.md",
      "source_line": 19,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 235
    },
    {
      "rule_id": "SRC05.L0020",
      "source": "references/editorial-policy.md",
      "source_line": 20,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 236
    },
    {
      "rule_id": "SRC05.L0021",
      "source": "references/editorial-policy.md",
      "source_line": 21,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 237
    },
    {
      "rule_id": "SRC05.L0022",
      "source": "references/editorial-policy.md",
      "source_line": 22,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 238
    },
    {
      "rule_id": "SRC05.L0023",
      "source": "references/editorial-policy.md",
      "source_line": 23,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 239
    },
    {
      "rule_id": "SRC05.L0024",
      "source": "references/editorial-policy.md",
      "source_line": 24,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 240
    },
    {
      "rule_id": "SRC05.L0026",
      "source": "references/editorial-policy.md",
      "source_line": 26,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 242
    },
    {
      "rule_id": "SRC05.L0028",
      "source": "references/editorial-policy.md",
      "source_line": 28,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 244
    },
    {
      "rule_id": "SRC05.L0030",
      "source": "references/editorial-policy.md",
      "source_line": 30,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 246
    },
    {
      "rule_id": "SRC05.L0032",
      "source": "references/editorial-policy.md",
      "source_line": 32,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 248
    },
    {
      "rule_id": "SRC05.L0034",
      "source": "references/editorial-policy.md",
      "source_line": 34,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 250
    },
    {
      "rule_id": "SRC05.L0036",
      "source": "references/editorial-policy.md",
      "source_line": 36,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 252
    },
    {
      "rule_id": "SRC05.L0038",
      "source": "references/editorial-policy.md",
      "source_line": 38,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 254
    },
    {
      "rule_id": "SRC05.L0040",
      "source": "references/editorial-policy.md",
      "source_line": 40,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 256
    },
    {
      "rule_id": "SRC05.L0042",
      "source": "references/editorial-policy.md",
      "source_line": 42,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 258
    },
    {
      "rule_id": "SRC05.L0044",
      "source": "references/editorial-policy.md",
      "source_line": 44,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 260
    },
    {
      "rule_id": "SRC05.L0046",
      "source": "references/editorial-policy.md",
      "source_line": 46,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 262
    },
    {
      "rule_id": "SRC05.L0047",
      "source": "references/editorial-policy.md",
      "source_line": 47,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 263
    },
    {
      "rule_id": "SRC05.L0048",
      "source": "references/editorial-policy.md",
      "source_line": 48,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 264
    },
    {
      "rule_id": "SRC05.L0049",
      "source": "references/editorial-policy.md",
      "source_line": 49,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 265
    },
    {
      "rule_id": "SRC05.L0051",
      "source": "references/editorial-policy.md",
      "source_line": 51,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 267
    },
    {
      "rule_id": "SRC05.L0053",
      "source": "references/editorial-policy.md",
      "source_line": 53,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 269
    },
    {
      "rule_id": "SRC05.L0055",
      "source": "references/editorial-policy.md",
      "source_line": 55,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 271
    },
    {
      "rule_id": "SRC05.L0057",
      "source": "references/editorial-policy.md",
      "source_line": 57,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 273
    },
    {
      "rule_id": "SRC05.L0059",
      "source": "references/editorial-policy.md",
      "source_line": 59,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 275
    },
    {
      "rule_id": "SRC05.L0061",
      "source": "references/editorial-policy.md",
      "source_line": 61,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 277
    },
    {
      "rule_id": "SRC05.L0062",
      "source": "references/editorial-policy.md",
      "source_line": 62,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 278
    },
    {
      "rule_id": "SRC05.L0063",
      "source": "references/editorial-policy.md",
      "source_line": 63,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 279
    },
    {
      "rule_id": "SRC05.L0064",
      "source": "references/editorial-policy.md",
      "source_line": 64,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 280
    },
    {
      "rule_id": "SRC05.L0066",
      "source": "references/editorial-policy.md",
      "source_line": 66,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 282
    },
    {
      "rule_id": "SRC05.L0068",
      "source": "references/editorial-policy.md",
      "source_line": 68,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 284
    },
    {
      "rule_id": "SRC05.L0069",
      "source": "references/editorial-policy.md",
      "source_line": 69,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 285
    },
    {
      "rule_id": "SRC05.L0070",
      "source": "references/editorial-policy.md",
      "source_line": 70,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 286
    },
    {
      "rule_id": "SRC05.L0071",
      "source": "references/editorial-policy.md",
      "source_line": 71,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 287
    },
    {
      "rule_id": "SRC05.L0073",
      "source": "references/editorial-policy.md",
      "source_line": 73,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 289
    },
    {
      "rule_id": "SRC05.L0075",
      "source": "references/editorial-policy.md",
      "source_line": 75,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 291
    },
    {
      "rule_id": "SRC05.L0077",
      "source": "references/editorial-policy.md",
      "source_line": 77,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 293
    },
    {
      "rule_id": "SRC05.L0078",
      "source": "references/editorial-policy.md",
      "source_line": 78,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 294
    },
    {
      "rule_id": "SRC05.L0079",
      "source": "references/editorial-policy.md",
      "source_line": 79,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 295
    },
    {
      "rule_id": "SRC05.L0080",
      "source": "references/editorial-policy.md",
      "source_line": 80,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 296
    },
    {
      "rule_id": "SRC05.L0082",
      "source": "references/editorial-policy.md",
      "source_line": 82,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 298
    },
    {
      "rule_id": "SRC05.L0084",
      "source": "references/editorial-policy.md",
      "source_line": 84,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 300
    },
    {
      "rule_id": "SRC05.L0085",
      "source": "references/editorial-policy.md",
      "source_line": 85,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 301
    },
    {
      "rule_id": "SRC05.L0086",
      "source": "references/editorial-policy.md",
      "source_line": 86,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 302
    },
    {
      "rule_id": "SRC05.L0087",
      "source": "references/editorial-policy.md",
      "source_line": 87,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 303
    },
    {
      "rule_id": "SRC05.L0088",
      "source": "references/editorial-policy.md",
      "source_line": 88,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 304
    },
    {
      "rule_id": "SRC05.L0089",
      "source": "references/editorial-policy.md",
      "source_line": 89,
      "runtime_section": "Runtime source 5: references/editorial-policy.md",
      "runtime_line": 305
    },
    {
      "rule_id": "SRC06.L0001",
      "source": "references/highlight-selection.md",
      "source_line": 1,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 309
    },
    {
      "rule_id": "SRC06.L0003",
      "source": "references/highlight-selection.md",
      "source_line": 3,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 311
    },
    {
      "rule_id": "SRC06.L0005",
      "source": "references/highlight-selection.md",
      "source_line": 5,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 313
    },
    {
      "rule_id": "SRC06.L0007",
      "source": "references/highlight-selection.md",
      "source_line": 7,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 315
    },
    {
      "rule_id": "SRC06.L0009",
      "source": "references/highlight-selection.md",
      "source_line": 9,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 317
    },
    {
      "rule_id": "SRC06.L0011",
      "source": "references/highlight-selection.md",
      "source_line": 11,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 319
    },
    {
      "rule_id": "SRC06.L0013",
      "source": "references/highlight-selection.md",
      "source_line": 13,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 321
    },
    {
      "rule_id": "SRC06.L0015",
      "source": "references/highlight-selection.md",
      "source_line": 15,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 323
    },
    {
      "rule_id": "SRC06.L0016",
      "source": "references/highlight-selection.md",
      "source_line": 16,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 324
    },
    {
      "rule_id": "SRC06.L0018",
      "source": "references/highlight-selection.md",
      "source_line": 18,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 326
    },
    {
      "rule_id": "SRC06.L0020",
      "source": "references/highlight-selection.md",
      "source_line": 20,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 328
    },
    {
      "rule_id": "SRC06.L0021",
      "source": "references/highlight-selection.md",
      "source_line": 21,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 329
    },
    {
      "rule_id": "SRC06.L0022",
      "source": "references/highlight-selection.md",
      "source_line": 22,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 330
    },
    {
      "rule_id": "SRC06.L0023",
      "source": "references/highlight-selection.md",
      "source_line": 23,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 331
    },
    {
      "rule_id": "SRC06.L0024",
      "source": "references/highlight-selection.md",
      "source_line": 24,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 332
    },
    {
      "rule_id": "SRC06.L0025",
      "source": "references/highlight-selection.md",
      "source_line": 25,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 333
    },
    {
      "rule_id": "SRC06.L0027",
      "source": "references/highlight-selection.md",
      "source_line": 27,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 335
    },
    {
      "rule_id": "SRC06.L0029",
      "source": "references/highlight-selection.md",
      "source_line": 29,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 337
    },
    {
      "rule_id": "SRC06.L0031",
      "source": "references/highlight-selection.md",
      "source_line": 31,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 339
    },
    {
      "rule_id": "SRC06.L0033",
      "source": "references/highlight-selection.md",
      "source_line": 33,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 341
    },
    {
      "rule_id": "SRC06.L0035",
      "source": "references/highlight-selection.md",
      "source_line": 35,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 343
    },
    {
      "rule_id": "SRC06.L0037",
      "source": "references/highlight-selection.md",
      "source_line": 37,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 345
    },
    {
      "rule_id": "SRC06.L0039",
      "source": "references/highlight-selection.md",
      "source_line": 39,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 347
    },
    {
      "rule_id": "SRC06.L0041",
      "source": "references/highlight-selection.md",
      "source_line": 41,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 349
    },
    {
      "rule_id": "SRC06.L0042",
      "source": "references/highlight-selection.md",
      "source_line": 42,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 350
    },
    {
      "rule_id": "SRC06.L0044",
      "source": "references/highlight-selection.md",
      "source_line": 44,
      "runtime_section": "Runtime source 6: references/highlight-selection.md",
      "runtime_line": 352
    },
    {
      "rule_id": "SRC07.L0001",
      "source": "references/product-knowledge-registry.md",
      "source_line": 1,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 356
    },
    {
      "rule_id": "SRC07.L0003",
      "source": "references/product-knowledge-registry.md",
      "source_line": 3,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 358
    },
    {
      "rule_id": "SRC07.L0005",
      "source": "references/product-knowledge-registry.md",
      "source_line": 5,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 360
    },
    {
      "rule_id": "SRC07.L0007",
      "source": "references/product-knowledge-registry.md",
      "source_line": 7,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 362
    },
    {
      "rule_id": "SRC07.L0008",
      "source": "references/product-knowledge-registry.md",
      "source_line": 8,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 363
    },
    {
      "rule_id": "SRC07.L0009",
      "source": "references/product-knowledge-registry.md",
      "source_line": 9,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 364
    },
    {
      "rule_id": "SRC07.L0010",
      "source": "references/product-knowledge-registry.md",
      "source_line": 10,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 365
    },
    {
      "rule_id": "SRC07.L0011",
      "source": "references/product-knowledge-registry.md",
      "source_line": 11,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 366
    },
    {
      "rule_id": "SRC07.L0013",
      "source": "references/product-knowledge-registry.md",
      "source_line": 13,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 368
    },
    {
      "rule_id": "SRC07.L0015",
      "source": "references/product-knowledge-registry.md",
      "source_line": 15,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 370
    },
    {
      "rule_id": "SRC07.L0016",
      "source": "references/product-knowledge-registry.md",
      "source_line": 16,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 371
    },
    {
      "rule_id": "SRC07.L0017",
      "source": "references/product-knowledge-registry.md",
      "source_line": 17,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 372
    },
    {
      "rule_id": "SRC07.L0018",
      "source": "references/product-knowledge-registry.md",
      "source_line": 18,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 373
    },
    {
      "rule_id": "SRC07.L0019",
      "source": "references/product-knowledge-registry.md",
      "source_line": 19,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 374
    },
    {
      "rule_id": "SRC07.L0021",
      "source": "references/product-knowledge-registry.md",
      "source_line": 21,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 376
    },
    {
      "rule_id": "SRC07.L0023",
      "source": "references/product-knowledge-registry.md",
      "source_line": 23,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 378
    },
    {
      "rule_id": "SRC07.L0025",
      "source": "references/product-knowledge-registry.md",
      "source_line": 25,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 380
    },
    {
      "rule_id": "SRC07.L0027",
      "source": "references/product-knowledge-registry.md",
      "source_line": 27,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 382
    },
    {
      "rule_id": "SRC07.L0029",
      "source": "references/product-knowledge-registry.md",
      "source_line": 29,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 384
    },
    {
      "rule_id": "SRC07.L0031",
      "source": "references/product-knowledge-registry.md",
      "source_line": 31,
      "runtime_section": "Runtime source 7: references/product-knowledge-registry.md",
      "runtime_line": 386
    },
    {
      "rule_id": "SRC08.L0001",
      "source": "references/final-check.md",
      "source_line": 1,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 390
    },
    {
      "rule_id": "SRC08.L0003",
      "source": "references/final-check.md",
      "source_line": 3,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 392
    },
    {
      "rule_id": "SRC08.L0005",
      "source": "references/final-check.md",
      "source_line": 5,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 394
    },
    {
      "rule_id": "SRC08.L0007",
      "source": "references/final-check.md",
      "source_line": 7,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 396
    },
    {
      "rule_id": "SRC08.L0009",
      "source": "references/final-check.md",
      "source_line": 9,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 398
    },
    {
      "rule_id": "SRC08.L0011",
      "source": "references/final-check.md",
      "source_line": 11,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 400
    },
    {
      "rule_id": "SRC08.L0013",
      "source": "references/final-check.md",
      "source_line": 13,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 402
    },
    {
      "rule_id": "SRC08.L0015",
      "source": "references/final-check.md",
      "source_line": 15,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 404
    },
    {
      "rule_id": "SRC08.L0017",
      "source": "references/final-check.md",
      "source_line": 17,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 406
    },
    {
      "rule_id": "SRC08.L0018",
      "source": "references/final-check.md",
      "source_line": 18,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 407
    },
    {
      "rule_id": "SRC08.L0019",
      "source": "references/final-check.md",
      "source_line": 19,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 408
    },
    {
      "rule_id": "SRC08.L0020",
      "source": "references/final-check.md",
      "source_line": 20,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 409
    },
    {
      "rule_id": "SRC08.L0021",
      "source": "references/final-check.md",
      "source_line": 21,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 410
    },
    {
      "rule_id": "SRC08.L0023",
      "source": "references/final-check.md",
      "source_line": 23,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 412
    },
    {
      "rule_id": "SRC08.L0025",
      "source": "references/final-check.md",
      "source_line": 25,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 414
    },
    {
      "rule_id": "SRC08.L0026",
      "source": "references/final-check.md",
      "source_line": 26,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 415
    },
    {
      "rule_id": "SRC08.L0027",
      "source": "references/final-check.md",
      "source_line": 27,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 416
    },
    {
      "rule_id": "SRC08.L0028",
      "source": "references/final-check.md",
      "source_line": 28,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 417
    },
    {
      "rule_id": "SRC08.L0029",
      "source": "references/final-check.md",
      "source_line": 29,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 418
    },
    {
      "rule_id": "SRC08.L0030",
      "source": "references/final-check.md",
      "source_line": 30,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 419
    },
    {
      "rule_id": "SRC08.L0031",
      "source": "references/final-check.md",
      "source_line": 31,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 420
    },
    {
      "rule_id": "SRC08.L0032",
      "source": "references/final-check.md",
      "source_line": 32,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 421
    },
    {
      "rule_id": "SRC08.L0033",
      "source": "references/final-check.md",
      "source_line": 33,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 422
    },
    {
      "rule_id": "SRC08.L0035",
      "source": "references/final-check.md",
      "source_line": 35,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 424
    },
    {
      "rule_id": "SRC08.L0037",
      "source": "references/final-check.md",
      "source_line": 37,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 426
    },
    {
      "rule_id": "SRC08.L0039",
      "source": "references/final-check.md",
      "source_line": 39,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 428
    },
    {
      "rule_id": "SRC08.L0040",
      "source": "references/final-check.md",
      "source_line": 40,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 429
    },
    {
      "rule_id": "SRC08.L0041",
      "source": "references/final-check.md",
      "source_line": 41,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 430
    },
    {
      "rule_id": "SRC08.L0042",
      "source": "references/final-check.md",
      "source_line": 42,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 431
    },
    {
      "rule_id": "SRC08.L0043",
      "source": "references/final-check.md",
      "source_line": 43,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 432
    },
    {
      "rule_id": "SRC08.L0044",
      "source": "references/final-check.md",
      "source_line": 44,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 433
    },
    {
      "rule_id": "SRC08.L0045",
      "source": "references/final-check.md",
      "source_line": 45,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 434
    },
    {
      "rule_id": "SRC08.L0046",
      "source": "references/final-check.md",
      "source_line": 46,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 435
    },
    {
      "rule_id": "SRC08.L0047",
      "source": "references/final-check.md",
      "source_line": 47,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 436
    },
    {
      "rule_id": "SRC08.L0048",
      "source": "references/final-check.md",
      "source_line": 48,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 437
    },
    {
      "rule_id": "SRC08.L0049",
      "source": "references/final-check.md",
      "source_line": 49,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 438
    },
    {
      "rule_id": "SRC08.L0051",
      "source": "references/final-check.md",
      "source_line": 51,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 440
    },
    {
      "rule_id": "SRC08.L0053",
      "source": "references/final-check.md",
      "source_line": 53,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 442
    },
    {
      "rule_id": "SRC08.L0054",
      "source": "references/final-check.md",
      "source_line": 54,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 443
    },
    {
      "rule_id": "SRC08.L0055",
      "source": "references/final-check.md",
      "source_line": 55,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 444
    },
    {
      "rule_id": "SRC08.L0056",
      "source": "references/final-check.md",
      "source_line": 56,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 445
    },
    {
      "rule_id": "SRC08.L0057",
      "source": "references/final-check.md",
      "source_line": 57,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 446
    },
    {
      "rule_id": "SRC08.L0058",
      "source": "references/final-check.md",
      "source_line": 58,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 447
    },
    {
      "rule_id": "SRC08.L0059",
      "source": "references/final-check.md",
      "source_line": 59,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 448
    },
    {
      "rule_id": "SRC08.L0060",
      "source": "references/final-check.md",
      "source_line": 60,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 449
    },
    {
      "rule_id": "SRC08.L0061",
      "source": "references/final-check.md",
      "source_line": 61,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 450
    },
    {
      "rule_id": "SRC08.L0062",
      "source": "references/final-check.md",
      "source_line": 62,
      "runtime_section": "Runtime source 8: references/final-check.md",
      "runtime_line": 451
    }
  ]
}

## Embedded source: references/runtime-current.md

# C2 Universal Core 0.4.7 / Skill 0.4.29｜唯一运行规则正文

本文件为构建生成的日常运行正文。其下各权威源文件按原文收录；不要手工编辑本文件。
源文件 → 规则行 ID → 本文件源章节及行号的完整映射见同目录 `runtime-manifest.json`。
普通运行只读取入口 `SKILL.md` 与本文件；条件文件仅按规则需要读取。

## Runtime source 1: `references/ai-first-constitution.md`

# AI-First Constitution

本文件是 C2 Universal 的最高架构约束。任何版本、平台适配、长文本优化、知识包扩展或测试体系不得与本文件冲突。

## 1. 决策权

AI 负责商品识别与切换、指代、归属、卖点与购买价值、重复判断、内容顺序与重组、多方案分配、合规语境和最终取舍。工具只能提供机械证据或降低读取/计算成本，不能替代语义决策。

## 2. 组织式逻辑职责

- 组织职责是同一 AI 的思考与责任划分，不创建多个模型、串行 Agent、独立提示词调用或额外语义轮次。
- Chief Decision Editor 在硬规则内统筹并裁决；商品事实与边界官对已禁内容、商品归属和证据边界拥有否决权；购买决策架构师负责动态策略；购买决策剪辑师执行原话选择与编排；成片质量审计官完成现有的一次终检。
- 职责分明不等于流程门槛。普通任务仍由同一 AI 完成一次语义分析和一次终检；默认方案数量和用户显式单条指令遵循 `references/clip-selection-policy.md`，不增加主题选择暂停。

## 3. 主路径必须无工具硬依赖

- 每个新功能必须先定义仅依赖 AI 与可取得文本的可执行主路径。
- 不允许把某个 Python 版本、脚本、API、联网能力、JSON 中间文件、平台或环境自检设为普通任务的进入门槛。
- 工具不可用时，只要文本仍可可靠取得，继续执行；在交付中如实写明实际核验方式。
- 只有原始输入无法取得、存在无法补齐的截断、来源范围无法确认或用户要求的能力本身不存在时，才暂停受影响部分。

## 4. 工具允许做什么

允许：分段读取、范围提取、序号/时间码定位、累计时长、编号/格式检查、查找确切文本、生成测试数据。

工具不能直接决定：哪个商品正在被讲、某句属于哪个目标商品、某句是否具有购买价值、两段是否语义重复、开头优劣、如何分配多方案、具体语境是否合规。这些由 AI 结合上下文判断。

## 5. 动态结构与知识包

- 内容结构根据本商品、顾客决策逻辑、原话证据、顾虑、适配条件和独立购买理由动态构建；不得退回固定类目模板或预设卖点顺序。
- 产品知识包只提供属性事实提醒、证据边界、条件与归属风险；不得拥有开头选择、卖点排序、成交位置、内容结构、话题或取舍权。
- 未注册类别不构成阻断；不把相近商品知识移植成当前商品事实。

## 6. 反过度工程

- 不为“可程序验收”牺牲自然语言理解质量。
- 不恢复逐条 JSON 语义台账、主题选择暂停或其他强制多阶段 Gate、职责串行签核、重复环境测试或“程序没跑就不能交付”的架构。
- 需要更高可靠性时，将来源与购买信息判断整合到同次语义筛选/编排中；不以增加独立遗漏扫描、全文复查、台账或模型轮次换取形式检查。

## 7. 未来修改验收

每次升级必须核实：
1. AI 是否仍是所有语义判断的最终决策者，职责层级和否决边界是否清楚？
2. 工具全部不可用时，只要文本可读，核心任务是否仍能完成？
3. 是否新增隐性环境前置条件或角色间串行门槛？
4. 知识包是否只约束事实，没有接管内容结构？
5. 完整读取和粒度控制是否先于开头比较与方案编排；开头是否在完整信息池后将钩子与必要紧邻承接联合编排，综合判断前 2 秒吸引力和前 5 秒连续吸引力；默认 1.2 倍速的 2.4/6 秒原素材时长只作参考、不硬截原话，承接类型动态决定且没有固定优先级、顺序、权重、分数或额外轮次；方案数量、独立核心、逐条覆盖和超长处理是否遵循 `references/clip-selection-policy.md`；原话、来源、商品归属、适用合规促单原文和固定五部分输出是否保持？

任一答案不符合本宪章，修改不得发布。

## 8. 固定版本更新协议

未来每次修改按 references/update-protocol.md 的审查、否决项、版本记录和同步核实执行。协议只约束开发与发布，不增加日常剪辑流程。

## Runtime source 2: `references/runtime-contract.md`

# C2 Universal 0.4.7｜运行契约

本文件定义唯一运行入口、素材读取边界、单次语义分析的资料复用方式和固定交付格式，遵循 AI-First 单 AI 架构。商品事实与全局硬规则优先。动态购买决策、正式禁词、时长与质量判定仍以同一运行正文中的对应权威章节为准。

## 入口、版本与输入

- 当前唯一业务内核为 Core `0.4.7`、Skill `0.4.29`。唯一触发词为 `srt文案`、`srt切片文案`、`str文案`、`C2完整精简版`；通用词 `切片文案` 不触发 C2。
- 正式输入为 SRT 或逐条时长文本。只有 MP4 时请用户提供文本；同时提供 SRT/MP4 时按文本剪辑，不声称已核验未查看的画面或原声，不伪造字幕、序号或时间。
- 若可靠识别出两件及以上商品且用户未指定目标，只列商品及其离散讲解窗口并询问一次；确认前不进行商品专属筛选、编排或成稿。确认后完整读取所选商品的全部有效窗口。目标明确或只有一件商品时直接继续。
- 执行摘要的首次读取、有效性检查、复用和失效刷新遵循 `SKILL.md`；摘要有效时不要求每次完整重读运行正文。摘要从属于当前规则源。

### 现有逻辑职责（同一 AI）

**运行方式是一个 AI、一次语义分析、一次终检。**下列英文名称仅对应现有逻辑职责，不代表新 Agent、模型或调用：Chief Decision Editor（总决策编辑）统筹用户目标并按用户授权维护唯一词库；Product Purchase-Decision Architect（商品购买决策架构师）完整识别信息并控制粒度、设计正式命中与风险提示边界，按动态顾客心理驱动机制比较开头；Product Facts & Boundaries Officer（商品事实与边界官）核对商品归属、证据、条件和合规边界，对硬边界有否决权；Purchase-Decision Editor（购买决策剪辑师）只为用户已选择的方案按原话编排并保留全部有效信息；Final Quality Auditor（成片质量审计官）只对已选择且实际写出的成片执行现有一次终检并要求局部修复。角色不得越过全局硬规则；事实与边界官的否决不能由转化诉求推翻，总决策编辑不得豁免已确认禁令或跳过硬性失败项。

## 完整信息池与开头比较

1. 完整解析来源并确认读取范围。保留原始编号、原话、时间码/逐条时长和来源顺序；存在缺行、重复编号、倒置时间、非正时长、乱码或截断时，标明已解析与未解析范围。未解析范围为 BLOCKED，不得当作已检查或据此推断；来源无法可靠补齐时停止受影响的正式编排。
2. 若可靠识别出两件及以上商品且用户未指定目标，只列商品及离散讲解窗口并询问一次；确认后只处理所选商品。商品明确或只有一件时直接继续。
3. 在同一次语义分析中完整读取目标商品的全部有效窗口，再建立完整信息池：有效独立购买信息、商品/款式归属、原话来源、必要证据与条件、重复/递进关系、事实待核实和风险标记。
4. 信息池完成后，按动态顾客心理驱动钩子机制，将真实钩子原话与必要紧邻承接联合编排为连续开头单元，综合判断前 2 秒吸引力和前 5 秒连续吸引力。默认 1.2 倍速仅作估算参考，分别约对应原素材累计 2.4 秒、6 秒；时间点不是硬剪辑点，不得硬截完整原话。承接动态延续情绪、视觉/动作期待、种草兴趣、购买收益等素材真实提供的观看动力；不设固定类型、顺序、权重或评分，也不增加语义轮次。仅比较该开头单元，不比较、评分或排名完整成片。
5. 单条/多方案数量、独立购买核心、逐条编排、120 秒及超长处理唯一按 `references/clip-selection-policy.md` 执行。按默认规则直接生成方案，不因多主题机会暂停等待用户选择。
6. 促单仅保留适用且合规的原文；没有来源时不得编造、改写、补充或跨商品移用。动态交易信息仍按全局规则处理。

## 工具、终检与修复

- Python、脚本、JSON、联网和环境检查均非日常任务前置条件。工具可用时最多执行一次输入预处理；如使用随附 CLI，优先 `srt_tools.py preprocess <source> --compact`，每条字幕只返回一份无损行记录，避免重复输出完整字幕表和时间轴视图。选段组装时一次完成来源/序号/角色/正式词库结构检查、原话渲染、第五部分序号和共享时长计算。机器不判断卖点池完整性、语义禁词、原话支撑、商品归属或跳点是否自然。
- 工具不可用时继续处理可靠可读文本，使用“模型逐条对照”，不得称为机检通过。正式词库直接命中、风险提示和事实待核实分开；工具结果不得扩大硬禁范围。每条方案先完整编排再计算约数时长；超长触发和删留依唯一规则。SRT 按连续源序号组计算“末条 end − 首条 start”并计组内间隔，逐条时长文本逐项相加；播放时间可按约定速度粗估，只作整秒级显示。第一、三部分复用同一 `playback_duration_display`，字幕定位保留原素材 1.0 倍口径。
- 现有 Final Quality Auditor 在同一次任务内只对实际写出的成片完成一次终检：逐条核验适用覆盖、来源、归属、证据、条件、原话、合规和上下文连续性。方案数量与时长例外按唯一规则；不新增 Agent、模型轮次或独立台账。
- 失败时按根因只修复受影响片段，并核对相邻语境；相同根因最多三轮实质修复。复修后重验导致失败的项目及受影响回归，并完成一次最终整体验收；只重出受影响段落，不重写整份五部分。不得通过删点、降低标准或隐藏 BLOCKED/FAIL 换取通过。

## 固定五部分交付

以下顺序和内容固定，不添加第六部分：

### 一、文件解析结果

按固定短句模板填写：`文件解析：{文件名}；{SRT/逐条时长文本}；{Standard/Long Context}；窗口 {数量}；入选 {条数} 条/{组数} 组；原始选段 {源时长}；预计成片 {playback_duration_display}；{脚本核验/模型逐条对照}。范围：{已核对范围或 BLOCKED 的 parsed_ranges/unparsed_ranges}。待核：{合规风险/事实待核实/关键限制，无则写“无”}。` 不声称未实际执行的脚本检查。原始选段与预计成片时长引用同一组装结果。

### 二、商品识别

列出目标商品、别称、离散讲解窗口及必要归属说明；只有确实辅助事实判断时才说明参考的商品知识包。

### 三、最佳成片方案

未指定时默认交付两个具有独立购买核心的方案；若第二方案不能形成真实独立购买价值或会降低质量，只交付一条并说明具体原因。开头指定“单条”或“按推荐版”时直接只交付一条。主题差异、逐条全量编排、超长处理与验收唯一按 `references/clip-selection-policy.md` 执行。

每版列本条核心角度、购买决策路径、预计时长、原始选段时长、按播放顺序排列的真实原话和来源序号，并简述核心与补充理由、重要未采用内容及原因。普通未采用内容最多三条、每条一行；超长筛选而未采用的有效信息逐项列出并说明该方案的动态理由；风险、待核实事实与关键限制另列，不计入三条限额。原话逐字保留；疑点紧邻对应片段标明。

### 四、作品标题与话题

每版恰好一个标题、五个话题。根据当前商品和该版真实主线动态生成；不得套用知识包标签或编造事实、价格、库存、功效，并执行正式词库与字段特例。

### 五、原始 SRT 序号

按播放顺序列出来源序号。所有方案放在同一个文本代码框中，每版一行，以半角逗号分隔且无空格；方案间空一行。代码框内不放其他文字，不伪造序号。

各方案时长和超长处理唯一遵循 `references/clip-selection-policy.md`。适用且合规的原文促单必须完整保留；原文没有时绝不编造、改写、补充或跨商品移用。日常输出仅此五部分。

## Runtime source 3: `references/clip-selection-policy.md`

# C2 Universal｜方案数量与时长唯一规则

本文件是**时长处理、单条/多方案数量、方案独立性及逐条覆盖**的唯一规则来源。执行契约、编辑策略、选点规则、终检、QA 和运行摘要只引用本文件，不另行定义、放宽或改写这些规则。商品事实、原话、来源序号、合规和促单仍服从其各自权威规则。

## 全量信息池与先完整编排

先完整读取目标商品的全部有效窗口并识别完整的有效购买信息池与必要证据、条件；再为本次输出的每个方案分别完成购买决策结构与原话编排，**先完成全部有效卖点的完整编排，再计算时长**。每个方案分别计算和比较预计时长。不得先看时长、主题或局部强卖点，再缩小信息池或锁定唯一主线。

有效信息是否进入信息池，依据它是否提供独立商品事实、顾客结果、适配/选择帮助、必要条件、购买顾虑回应或其他真实购买决策价值。价值等级随商品、受众、具体方案和素材动态判断；**不得固定某些卖点永远低价值**。低价值但有效信息不等于弱增量，也不得标成重复。

完整购买理由须让顾客理解具体结果、用途或待解决问题，并有真实原话作为依据，保留成立所需的证据、适配条件和限制。孤立属性、宽泛适配词、泛泛夸赞或行动口号不单独构成购买理由；原话促单也不能替代理由所需的依据和条件。

## 120 秒与超长预设

- **120 秒不是目标，也不是硬上限。**完整编排后预计不超过 120 秒时，必须保留该方案全部有效卖点和必要支持；不为缩短而删点，不为接近 120 秒而加无关内容。
- 只有明显超过 120 秒时，才对该方案触发超长预设；必须先完成完整编排再计算时长。每条方案分别判断和处理，不让一条的时长或筛选结果替代另一条。
- 触发后，依据该条真实购买核心动态重排，并只在确有必要时筛除对该核心购买决策贡献较低、且不是理解/信任/适配所必需的信息。不得按固定类别、卖点名或主题关联度一刀切；不确定其是否影响购买决策时保留。
- 略超 120 秒，或删去内容会破坏购买决定所需的理由、证据、顾虑回应、适配条件、事实边界或原文促单上下文时，优先保留完整决策并允许适度超过 120 秒；不硬截时长。
- 超长预设下每条仍须独立保有完整、可信的购买决策链。对确实未采用的有效信息，须逐项说明被省略的有效信息及其针对该方案核心的理由；不得声称全量覆盖，也不得以另一条方案或方案并集补足。重复、弱增量、无关商品或正式禁用内容按原规则处理，不冒充超长筛选。

## 默认双方案与单条例外

- 用户未在开头明确指定“单条”或“按推荐版”时，默认直接生成两条有原话依据、具有真实且彼此独立购买核心的完整成片方案；**不得暂停等待用户选择数量或主题**。
- 两条须有实质不同的购买入口/核心与编排，不得只交换顺序、标题或同义表述凑数。每条独立覆盖完整有效卖点，分别从完整信息池开始，独立排序、完整编排、计算时长并验收。不得把卖点拆到两条、只靠并集覆盖。若任一条触发超长预设，按本文件逐条处理并在输出中交代实际省略项。
- 如果第二方案不能形成真实独立购买核心，或生成它会明显降低原话自然度、购买决策完整性或整体质量，只交付一条；在方案说明中明确写出本次只有一条的具体原因，不以“素材不足”等空话代替可核实理由。
- 用户在任务开头指定“单条”或“按推荐版”时，跳过双方案生成，直接输出一条推荐方案；无需多视频机会暂停。用户明确指定其他条数/主题时按用户指示执行，但每条仍按本规则独立判断。
- 多方案应在固定输出的“最佳成片方案”部分并列呈现；仍遵守既定五部分输出，不增设第六部分或强制用户选择步骤。

## 逐条验收

每条输出方案均须单独核对真实来源原话、商品归属、每项纳入信息及必要支持、原文促单边界、正式禁词范围、风险提示边界、动态结构与衔接。常规时长方案须覆盖信息池全部有效卖点；超长方案须按本文件记录筛选并确保购买决策完整。方案之间不互相补足。\n

## Runtime source 4: `references/global-rules.md`

# 全局禁用规则｜所有商品唯一执行入口

本文件是全商品通用的用户剪辑禁用库，也是**唯一正式违禁词库**，女装、鞋、围巾、童装及未来任何商品类目统一执行。总决策编辑是词库管理最终负责人；总决策编辑不能豁免已确认禁令，也没有自行新增词条或扩展禁用范围的权限。只有用户提供且可可靠定位违规表达的平台审核截图，或用户明确指出某表达违规，才可新增正式词条。AI 可按完整语义识别真正等价表达，不得仅凭相同字眼、绝对措辞或风险推测扩展范围。

正式违禁词拦截与上下文合规风险提示分开处理。只有用户明确提出“更新违禁词”时才联网核对并更新平台政策规则；政策简报用于提示政策变化，不自动写入正式词库。普通 SRT 任务离线调用，不自动联网扩充。

## 正式禁用词库

本节是唯一可供直接匹配程序读取的词表；正式词条只允许依据用户明确指出的违规表达或可定位的审核截图更新。

- `羊毛`：用户明确指定为正式禁词。直接命中“羊毛”及其常见组合写法，包括“绵羊毛”“全羊毛”、比例和混纺表达；空格、标点、全半角和数字格式变化不得绕过。匹配证明不能豁免此词。
- `皮草`：用户明确指定的正式禁词。仅按原词和真实语义等价表达匹配；不得仅凭“皮”“草”“皮裤”“皮裙”或“毛绒”扩展。
- `羊绒`：用户本轮提供的审核截图明确标出的词，直接匹配字面词及其组合，包括“像羊绒的手感”“羊绒羊毛”“30%羊绒70%羊毛”“羊绒衫”；不因证明、否定或引用语境豁免。
- `特殊动物绒`：用户本轮提供的审核截图明确标出的原词，直接匹配。
- `全金纺半高领`：用户本轮提供的审核截图明确标出的完整表达，按截图原词匹配。

## 禁词命中范围

- 命中任一正式词条时，只排除实际命中的完整字幕序号；若一个词条跨越相邻字幕，才排除实际参与该词条的完整字幕。不得连带删除相邻字幕、整段或整条候选。
- “特殊纤维”“防静电”“防起静电”和“避免噼里啪啦”不是正式禁词。它们仍按商品归属、事实依据、语境完整性和购买价值判断；依据不足时标记待核实，不能只因靠近正式词条命中的字幕就自动删除。
- **防静电不是正式禁词**；相关表述只有在自身商品归属或事实依据不清时标记待核实，不因相邻命中字幕而排除。
- 标题、话题和最终成片同样执行正式词库复检；出现正式词条即验收失败。

## 字段特例

- **“羽绒服”**：所有商品的生成标题与话题禁用；正文原话及商品识别不因此删除。
- **“鹅绒服”**：所有商品的生成标题与话题禁用；正文（包括原话字幕及成片正文）和商品识别可正常使用，不因该词排除字幕。仅按完整词组“鹅绒服”执行，不扩展到“鹅绒”或其他近似表达；不纳入直接字幕匹配词表。
- 其他新增禁用词句，除用户明确限定字段外，默认对入选字幕原话、生成标题、话题统一生效。
- 每版仍输出一个标题和五个相关话题；具体话题由总决策编辑根据当前商品和成片真实主线动态生成，商品知识包不设固定话题。

## AI 识别与排除

- 每次处理输入时先读取本文件的正式词库并扫描全部字幕。直接词条按 NFKC、空格和标点标准化后匹配；语义等价表达由 AI 按完整语境识别，不得扩大到未授权的近似词。可运行 `scripts/prohibited_term_guard.py` 辅助直接匹配；脚本不可用时仍须由 AI 完成同一检查。
- 绝对词本身不默认属于违禁词，也不能仅因肯定语气自动拦截；只有与一条已授权正式词目在语义上实质等价时，才按该词目处理。
- 已确认命中时，**只排除命中的完整字幕序号**；同序号里其他正常句也不拆出。多个连续序号共同构成禁用表达时，仅排除实际参与该禁用表达的那些序号。上下文可以用于辨别语义，但不能把前后字幕当作“上下文窗口”连带删除；不连带前后字幕序号。
- 对正式词库列出的字词或固定表达，命中后排除该完整字幕，并从标题、话题和最终文案中移除对应表达。未命中词条的邻近序号继续按自己的商品归属、事实和价值判断；一次字幕命中不能触发对整段、整条候选或整份输入的防御性淘汰。
- 目标商品所有离散讲解窗口均执行该规则。一个目标字幕序号同时提到其他商品且其中有禁用表述，也整条排除。
- 疑似同音/错字、但尚不能可靠确定的序号暂不入正式成片，标记待回听；平台只给笼统拒审原因又无法定位原句时询问用户，不随意把整段判为禁词。
- 命中后优先从同一目标商品其他合规原话寻找替代，保证语义完整；不得改写、删字造句或重新加入禁用序号。
- 标题和话题命中禁令只重新生成受影响字段。仅实际命中时在五部分交付中的例外里注明排除序号、禁用表述和原因；无命中不额外报告。

## 上下文风险提示

- 未入正式词库但存在合规或证据风险的表达，只结合具体商品、主张、原话和可用依据作上下文风险提示；不自动加入词库，不直接删除整条字幕或整段内容。提示要说明风险所依赖的语境或待核实依据；风险提示不等于认定违规，也不等于认定合规。风险提示本身不能触发删除，也不能延伸成对相邻序号的排除。
- 有事实依据的商品工艺、材质描述不得因关键词或肯定语气误杀。例如，确有商品事实支持时，“亮片织进纱线里面”是工艺描述，不能仅因出现“亮片”或陈述为肯定句而拦截。依据不足时只按具体主张提示核实，不升级为正式禁词。
- “不会掉”等性能承诺要按商品、对象、条件和上下文判断，必要时提示核实其依据；不得仅凭“不会”或“掉”单词列为正式禁词或自动删除整段。问题、否定、引用或其他非肯定语境不得当作同一性能承诺。

## 维护边界

- 用户上传并可定位的新违规截图，或明确指出某表达违规时，AI 按用户确认范围更新**本文件**，检查语义边界、关联冲突并做最小针对性核验；不得自行扩大同类词、绝对词或风险表达。没有成功写入和读取验证，不得声称已永久更新。
- 只有用户明确提出“更新违禁词”才联网核对当前政策规则。政策变化可以单独形成风险提示或政策简报；未经用户提供的违规截图或对具体违规表达的明确指出，不得据此新增正式词条。
- 截图中的非文案原因（商品/投放资质、链接等）只记录问题，不自行创造禁用词。重复词句合并，不建立多套类目禁令或复杂编号数据库。
- 仅有一般“可能违规”、缺少证明但未被用户确认为正式禁令的表达，不因推测而强制禁用；按事实、语境和证据核验。正式词库中列出的词条直接拦截，其他未列表达不扩围。价格/库存/功效等仍按现有平台合规边界独立判断。动态交易信息的日常切片排除规则见 references/editorial-policy.md，这是素材时效管理规则，不代表平台将其认定为违规，也不把这些内容加入本禁用库。
- 全局禁令是用户内部剪辑选择标准，不可替代平台当次审核判断；不提供规避审核的改写。

## Runtime source 5: `references/editorial-policy.md`

# Universal Core｜动态购买决策结构

本文件规定跨类目购买决策的共通边界。购买决策路径与开头由目标顾客心理、真实原话、商品事实和决策关系共同决定，并按当前商品与素材动态构建。购买决策架构师根据本商品、目标顾客、实际证据、顾虑与独立理由动态构建路径；事实与边界官负责来源和限制；总决策编辑在硬规则内裁决。商品知识包只提供事实提醒，不规定内容结构。

**不存在所有商品通用的段落成交模板、卖点顺序、成交次数或成交位置。**可复用的是顾客价值、证据、适配与决策推进的判断原则；具体路径由当前素材决定。以下购买决策关系用于判断理由是否成立，可按依赖关系重排，也可在素材不支持时省略某一环节。

## 动态顾客心理驱动钩子机制

默认对象是第一次刷到视频、不了解主播和直播背景的陌生潜在买家。完整读取目标商品全部有效窗口、建立全部有效卖点信息池并完成粒度判断后，才跨主题比较开头候选。

把真实钩子原话与理解、延续它所需的紧邻承接联合编排为一个连续开头单元，综合判断前 2 秒能否吸引注意，以及前 5 秒能否把观看兴趣连续承接下去。默认以 1.2 倍速作估算参照：成片前 2 秒约对应原素材累计 2.4 秒，前 5 秒约对应原素材累计 6 秒。两个时间点只用于判断参考，不是选段资格线或硬剪辑点；不得为对齐时间硬截完整原话、半截句子、破坏自然语义或遗漏必要承接。完整自然表达或必要语境超出参考时长时，保留完整原话与必要承接。

承接须依据当前原话动态延续或增强观看动力，例如情绪感染、视觉/动作期待、种草兴趣或具体购买收益；可体现其中一项或多项，也可由素材中的其他有效关系承担，不要求固定类型、顺序或组合。可观察情绪感染、视觉引导、好奇期待、审美种草、场景代入、共情、需求与收益、自然原生感、目标顾客相关性、事实支持及后文承接；这些只是当前素材的观察角度，不是固定检查清单。真实喜爱、动作展示、视觉好奇、具体购买收益等都可成为入口或承接点。以陌生潜在买家的继续观看欲望和与商品相关的购买兴趣作综合判断；这只是文本编排判断，不等于实际留存或成交结果。不设置固定钩子类型优先级、类型顺序、权重、分数或额外语义轮次；也不预设种草或共情优先，不把信息密度、最强卖点、理性收益、共情或种草固定为唯一决定因素。入口之后仍按现有动态购买决策结构组织内容；开头不缩小后续信息池，每条方案继续覆盖全部有效卖点并按原文保留适用且合规的促单。

候选须属于目标商品，离开直播前情仍自然可理解，由同商品原话支撑并能在后文兑现。开头比较只覆盖开头本身，即钩子与必要紧邻承接构成的连续开头单元；不比较、评分或排名完整成片。

真实性、商品归属、正式合规、自然语义与后文兑现是硬边界。主播设问或个人判断可保留为原文候选，但不得包装成真实顾客反馈、普遍事实或商品已存在的缺陷；反馈来源不清须标为待核实。动态价格、库存、优惠、直播过渡或链接提示不作为通用钩子。没有合格候选时，从现有可证实的商品原话中选择与目标顾客兴趣最相关且可自然理解的一段；仍无合适项就如实说明，不拼凑开头。

- 颜色、搭配、材质或外观表达不按关键词禁用或排除。若原话清楚说出显气色、不沉闷、显瘦、利落等具体顾客结果，且来源可信、后文能兑现，它可以与其他候选动态比较；普通或泛泛表达不能仅凭句子完整、先出现或画面暗示自动胜出。
- 差异性只是观察角度，不是硬门槛；普遍但具体、可信且有支撑的购买结果仍可胜出。
- 老粉、老顾客、复购用户限定内容默认不代表陌生顾客利益；只有当前目标受众确实是该人群，或同句也给陌生顾客独立决策价值时，才按实际价值比较。
- 不把主播回答、个人偏好、一般尺码/搭配建议冒充顾客困扰。顾客困扰须来自顾客原话或主播清楚转述；主播明确确认商品存在的负面表现，依事实与适用知识边界判断，不可反向包装成优势。
- 问题型开头与理解它所需的紧邻回应作为一个入口比较；问题段较长时，可先压缩重复问题、停顿和无增量口头填充，再判断自然节奏，但不改写、硬截或补造原话。
- 选定入口后，使用最少但足以解释、证明或展示其核心价值的原话。若原素材不能支撑开头，应重新比较候选；不能靠改写、跨商品拼接或虚构解释补强。开头只决定入口，不把后续内容锁进单一主题。

仅凭 SRT，可以判断原话涉及的视觉或情绪吸引潜力，但不能确认实际画面，也不能确认主播的真实语气、表情或情绪表现；这些音画效果必须标为未核验。

## 持续购买决策关系

架构师结合本商品的真实购买问题，选择有用的内容关系，例如结果与原因、特点与使用价值、顾虑与回应、属性与场景、版型与身材效果、材质与穿着体验、适配条件与选择建议。它们是理解原话的候选关系，不是模板、固定排序或要求全覆盖的模块。

每个入选片段都应承担至少一种可理解的工作：提出新购买理由、证明已有理由、回应顾虑、帮助适配/选择、降低决策阻力，或完成必要承接。没有新增或承接价值的重复夸赞、普通过渡和脱离上下文的行动口号，不因“结构完整”而保留；但适用且合规的原文促单须按下文规则完整保留。

主题顺序只决定怎么排，不决定理由留不留。先以最小充分内容兑现已选入口的价值，再让其他独立理由按实际关系进入成片；不因主题不同、类别不同或暂时难衔接就删除有效理由。可重排同一目标商品的原话，但须保留对象、条件、因果和原意，不跨商品或款式混编。

## 完整卖点识别与开头比较前置条件

在现有一次语义分析中，先完整读取目标商品的全部上下文和有效讲解窗口，再识别其全部有效独立购买信息。识别范围不因最终开头、当前主题、首个购买理由或成片角度而缩小；完成全量识别前不生成最终候选、不锁定主线。

完整识别可能涉及顾客结果、用途、顾虑回应、适配条件、搭配/场景、体验、证据、限制和选择帮助；这些只是理解线索，不是要求逐类套用的固定模板。对每项信息保留原话来源、商品归属、必要条件和与其他信息的关系。

### 卖点粒度

覆盖单位是**有效独立购买信息**，不是每句字幕、每个名词或每条例证。先判断内容属于独立理由，还是同一理由的证据、例子、条件、递进或重复。

- 不把同一购买意义下的一组例子机械拆成多个卖点。例如多种裙装、裤装和鞋靴组合可共同说明搭配兼容性；保留足以说明范围的代表性原话即可。
- 不把不同具体事实过度合并。例如前襟领型与后背褶皱即使都支持设计差异，也可能是独立设计信息；一句泛称“有设计感”不能自动替代全部具体内容。
- 卖点覆盖不等于每条证明都要保留。选择足以支撑该购买信息的必要证据、条件和代表性例子；若另一个证据新增原因、体验、限制或选择帮助，它可能形成新的有效信息，不能按重复删去。
- 粒度按当前商品和原话动态判断，不建立固定商品类目表或必填卖点模板。

方案数量、默认双方案、每条独立覆盖与超长处理唯一按 `references/clip-selection-policy.md` 执行。本文件不再定义多方案暂停、主题选择或逐条覆盖例外。

## 重复表达的语义与说服判断

购买决策架构师判断两段表达是否真正重复，以及它们相对现有内容带来的**信息增量**和**说服增量**；购买决策剪辑师执行去留与压缩，总决策编辑结合独立购买理由和注意力/结构占用裁决，成片质量审计官在现有一次终检中核对。四项职责由同一 AI 在现有一次分析和一次终检中完成，不新增角色、轮次或工具。

### 重复裁决顺序（唯一顺序）

对任何疑似重复，必须按以下顺序完成一次判断，不得跳步、倒置或用词面相似度代替语义裁决：

1. **先判同事实**：同时核对商品/款式、对象或部位、属性或关系、事实结论及完整语义；只有这些核心要素指向同一购买事实，才进入重复判断。
2. **再判新增信息**：检查后一句是否增加原因、证据、体验、条件、场景、程度边界或适配/选择帮助；有新增信息时属于递进或补充，优先保留。
3. **没有新增信息，再判说服增量**：检查重述是否在当前上下文中明显增强核心利益的记忆、可信感、情绪感染或行动确定感；只有可感知的说服收益才构成有效强调，单纯换词的近义复述不算。
4. **最后取舍**：两类增量都不成立时，同事实的无增量近义复述默认压缩，只留最完整、自然、清楚且购买价值更高的一处；若有效强调与独立购买理由竞争，仍须判断注意力负担和结构衔接。正常时长本身不能成为删减有效信息的理由，120 秒处理唯一遵循 `references/clip-selection-policy.md`。

同事实不等于必删；新增信息的递进必须保留，有明确说服增量的有效强调可以保留。默认压缩只针对同事实、无信息增量且无说服增量的近义复述。

- **机械性重复**：口误、卡顿、半句重启、未完成表达后紧接完整重说，且没有新增意思、证据或表达效果。通常删除不完整/重复起句，保留完整自然的版本；不得因为字幕文本相似就连同完整句一起删掉。
- **强调性重复**：在先判同事实、再确认没有新增信息后，重述仍能明显增强顾客记忆、确定感、感染力或说服效果，才可作为有效强调保留；不能把仅换几个词的近义复述当作说服增量，也不要求有效强调另造新事实。
- **递进性重复**：后句增加原因、证据、体验、适用条件、使用场景、程度边界或选择帮助。它已不只是重复，应优先保留；若只能保留一个片段，选择能完整表达且对当前顾客决策帮助更大的原话。
- **过度性重复**：相同利益已被充分表达，后续再强调没有明显信息或说服增量，节奏收益低于注意力与结构占用成本。可压缩为最有力、完整、自然的一处；不改写、不拼接句子。判断重复不能以预计秒数或 120 秒为由。

以上是语义类别，不是由词面相似度自动判定的标签。必须先判同事实，再判新增信息，再判说服增量，最后取舍；同事实无增量近义复述默认压缩。不得恢复固定重复次数或“同一句只留一次”的机械规则；同一表达在不同上下文中可分别承担强调、递进或冗余作用。重复取舍还须比较被占用的时间是否会挤掉另一个独立购买理由：有效强调不是无条件优先，机械/过度重复也不能因能延长成片而获豁免。

## 原文促单的保留边界

- 原文存在适用且合规的促单话术时，必须保留完整原话并按原顺序完整保留；不得为开头或时长要求提前移动、拆写原话，也不得因主题、预计时长或主线角度省略、改述。
- 适用性须核对商品/颜色/对象、条件、价格或活动说明、尺码选择、问题回应、比较关系、链接状态等本地依赖；不得只凭“拍/买/入/拿”等词判断。
- 原文没有促单时，禁止编造、改写或补充；不得跨商品移用话术，也不得用近义句替代。不得为结尾完整或转化要求增写行动口号。
- 动态价格、优惠、库存、限时、直播专属福利、涨价和稀缺信息仍按全局规则处理；不合规内容不因其属于促单而保留。

## 原话、混合信息与动态交易边界

- 原话逐字保留，只能重排同一商品的完整原话；不润色、改写、补词或拼接不连续片段。命中全局禁令时，依 global-rules.md 排除完整原始字幕序号。
- “它/这个/那款”等指代不清时，核对必要前后文；仍不能确认商品归属则不选入正式方案或明确标待核实。疑似转写错误保留原字并标注回听，不代改。
- 具体商品价格、优惠、赠品、直播福利、倒计时、库存/稀缺数量及其他依赖实时交易条件的信息，全片默认排除。只有用户明确要求制作有效期明确的活动素材且确认活动与发布时段仍有效，才对该任务例外；该例外不扩展全局禁令。
- 混合字幕只有在排除动态部分后，仍能逐字保留原始连续、语法完整、语义自足且自然衔接的原话子句时才可使用。仅剩词组或残句就舍弃整条相关字幕；不改写、补词或拼接。命中全局禁令仍排除完整原始序号。
- 购买者反馈只有在来源清楚、原话完整时才能作为候选；主播泛称“大家都喜欢”不等于真实顾客反馈。无法核实的社会证明就地标明，不扩写成普遍结论。
- 安全风险、护理要求或明确不适用条件不能被剪掉后留下相反的无条件承诺；依据不足时按全局合规规则标待核实。

## Runtime source 6: `references/highlight-selection.md`

# C2 Universal 0.4.7｜购买信息价值与重复判断

本文件维护购买价值和重复判断；方案数量、时长及覆盖规则唯一见 `references/clip-selection-policy.md`。开头比较见 `references/editorial-policy.md`；事实与归属边界见 `references/global-rules.md` 及适用的商品知识包。全部判断由同一 AI 在一次分析和一次终检中完成。

## 购买决策价值层级

价值等级按当前商品、目标顾客和具体方案动态判断，不把某类商品信息固定成高、中、低等级。有效性与价值排序是两个判断；低价值不等于无效，也不等于弱增量。低价值信息的覆盖义务和仅在超长时的处理唯一按 `references/clip-selection-policy.md`。

## 重复表达：信息增量、说服增量与机会成本

对疑似重复的片段，在现有一次语义分析中按唯一顺序判断，不跳步：**先判同事实→判新增信息→判说服增量→最后取舍**。只有前一步成立后才进入下一步；不把同一主题、词面相似或句式相近直接当成重复。

在上述顺序中同时判断两类增量：

1. **信息增量**：是否加入新的理由、解释、证据、体验、条件、程度、场景或适配/选择帮助。
2. **说服增量**：即使事实相同，重述是否能在当前语境中明显加强顾客对核心利益的记忆、可信感、情绪感染或行动确定感。

据此区分并处理：

| 类型 | 识别要点 | 默认处理 |
|---|---|---|
| 机械性重复 | 口误、卡顿、半句重启、未完成句被完整句重说，未增加信息或说服作用 | 删除机械片段，保留完整、自然的表达；若仅前段无效，不能连完整句一起删。 |
| 强调性重复 | 同事实且没有新增信息，但重述有可感知的记忆/感染/说服作用 | 允许保留为有效强调；必须确认不是单纯换词，并且没有挤占更重要的独立购买理由或拖慢节奏。 |
| 递进性重复 | 后句带来原因、证据、体验、条件、程度边界或选择帮助 | 优先保留其新增部分；它不是纯重复。 |
| 过度性重复 | 同一事实已充分表达，后续没有明显新增信息或说服作用 | 默认压缩到最有力、完整、自然的一处；不得为增加时长而保留。 |

先判同事实不等于必删；同一购买事实的重复表达仍须先判断新增信息与说服增量：有新增原因、证据、体验、条件、程度边界或选择帮助的递进必须保留；没有新增信息但有明确说服增量的有效强调可以保留。只有两类增量都没有时，才在最后取舍阶段默认压缩同事实的无增量近义复述。不得按词面相似度、固定重复次数或“一条字幕只留一次”规则机械删除。判断单位是当前语境中的完整表达及其顾客决策作用，而不是相同字词；一个词面不同的句子也可能没有任何增量。

**机会成本检查：**有效强调的保留价值须与它占用的注意力及可能挤掉的独立购买理由比较。强调有助于记住主利益，却不能因此吞掉尺码适配、顾虑回应或其他会改变购买决定的独立理由。重复类别按语义增量判定；超长状态下是否动态筛选有效信息，遵循 `references/clip-selection-policy.md`。

## 卖点覆盖与证据选择

卖点覆盖、每条方案独立编排、超长例外与省略项记录，唯一遵循 `references/clip-selection-policy.md`。证据覆盖不等于卖点覆盖：同一理由有多组支持时，可选足以成立的最好表达；新增原因、证据、体验、场景、限制或选择帮助若构成新的购买信息或必要条件，仍须纳入判断。每个入选片段应提出理由、证明理由、回应顾虑、帮助选择或完成必要承接；泛夸赞和普通过渡没有新增作用时可压缩。完整购买理由必须有原话支撑并保留必要条件；不得以行动口号替代证据。

## 开头比较

开头候选的范围和动态顾客心理驱动钩子机制见 `references/editorial-policy.md`。信息池后的方案数量、逐条独立编排、120 秒处理及验收唯一遵循 `references/clip-selection-policy.md`。本文件不再定义暂停等待用户选择或时长规则。

## 原文促单的保留

原文存在适用且合规的促单话术时，必须保留完整原话，按原顺序完整保留原句及成立所需的上下文，不删节、不拆写、不改述。先核对商品、对象、条件和交易依赖；动态交易信息仍按全局规则处理。原文没有适用且合规的促单时，禁止编造、改写、补充、从其他商品移用或用近义句替代。促单不能替代理由所需的证据和适配条件。
## 停止条件

停止条件与每条方案的覆盖判定遵循 `references/clip-selection-policy.md`；核心角度或主题顺序本身不改变有效性判断。

## Runtime source 7: `references/product-knowledge-registry.md`

# 商品知识包注册表

## 用途与边界

商品知识包是事实核对提示和边界参考，不是类目路由器、内容模块或剪辑模板。

- 购买决策架构师始终根据当前商品、顾客逻辑、原话证据与独立购买理由动态构建内容。
- 商品事实与边界官只在能帮助核对当前商品的属性、限制、证据或归属时参考一个或多个知识包。参考与否不决定任务能否开始。
- 知识包不得规定开头、中段、成交、结尾、卖点排序、固定覆盖、话题、时长或输出格式，也不得替代全局合规和来源核对。
- 多个商品类别同时出现时，可以分别参考适用知识包，但分别保持商品与款式事实边界；不得把一个商品的信息移给另一个商品。
- 未注册类别仍可按 Universal Core 正常处理。没有专业依据时不套用相近类别知识，也不编造行业规则或商品事实。

## 当前知识包

| 文件 | 可参考的事实边界 |
|---|---|
| product-knowledge-packs/womens-fashion.md | 服装、箱包及相关穿搭单品的版型、材质、适用条件和商品归属风险 |
| product-knowledge-packs/shoes.md | 鞋款、鞋底、脚型尺码、材质、场景及画面依赖风险 |
| product-knowledge-packs/scarves.md | 围巾与颈部配饰的材质、肤感、围法、护理及款式归属风险 |

## 未注册或不适用的类别

首饰、美妆、童装、家居、食品、数码及其他未登记商品不需要先建立知识包才能剪辑。事实与边界官基于本次原话和可靠来源处理归属、条件与风险；需要专业事实但无依据时标为待核实，不把另一类商品知识当作替代。

## 新增与维护

仅当重复出现的商品事实边界确实改善核对质量时新增知识包。文件必须清楚写明适用商品、需要区分的事实、不能推断的内容、证据/归属风险；不能建立固定开头、卖点顺序、成交话术或强制类别路径。更新后同步本注册表及便携版，并由回归检查确认知识包没有取得内容结构或语义裁决权。

## 话题

标题和五个话题由总决策编辑根据当前商品、顾客与成片真实主线动态生成。知识包不预设固定话题；所有输出遵守全局禁令和事实边界。

## Runtime source 8: `references/final-check.md`

# Final Quality Auditor｜实际成片终检

验收结论只允许标记为 **PASS / FAIL / BLOCKED**。PASS 表示本轮实际输出的成片已完成适用检查；FAIL 表示检查已执行并发现可修复问题；BLOCKED 表示输入、来源或外部依赖缺失，无法完成相关检查。没有成片时不产生最终成片审计结论。

## 终检范围与修复

只对实际写出的成片执行终检；每条均独立核对适用覆盖、必要证据与条件、原话、商品归属、正式合规边界和衔接。方案数量、逐条覆盖和超长例外唯一按 `references/clip-selection-policy.md`；方案之间不能互相补足。

发现 FAIL 后，定位失败项及共同根因，只修复受影响内容；随后复查导致失败的项目、关联上下文和受影响回归，再完成实际成片终检。同一根因最多三轮实质修复。仍失败时保留 FAIL 并报告证据，不降低标准、不跳过项目或隐藏结果。新问题属于不同根因时可单独处理。

## 机器判定与 AI 语义判断

可选脚本按实际使用方式记录 `verification_mode: script`；只有真正运行后才能称为脚本核验。未运行或工具不可用时记为 `manual`，用“模型逐条对照”，不可声称机检通过。工具是否可用不改变语义标准，也不是五部分交付的前置条件。

机器只检查可确定的结构和正式词库直接命中；机器不判断信息池完整性、原话语义支持、商品归属或条件是否充分，这些由 AI 的语义判断完成：

- 记录解析块数、总块数、已解析与未解析范围、行号及诊断。无法解析的范围为 BLOCKED；不得将其描述为已完整核验。
- 检查序号重复或倒置、时间码倒置和非正时长。SRT 按连续源序号组计算“末条 end − 首条 start”；逐条时长文本累计入选条目。
- 对每一条实际成片的 selection JSON，仅检查序号是否来自来源且已入选、每个信息点至少有一个来源支撑、每个入选序号恰有一个允许角色、必要字段结构完整。结构检查不判断语义覆盖是否成立。
- 逐字来源文本、选段组装、第五部分序号与时长显示引用同一实际选择记录；源 SHA-256 必须匹配。已知未加速时长仅可用于显示估算。
- 正式禁词 gate 只扫描 `references/global-rules.md` 的直接命中。机器仅排除完整命中的原始字幕序号，不连带排除邻近内容。`risk_hint` 原样提供语义判断，不得自动升级为硬失败，也不是合规结论。

以下判断由 AI 完成，不由脚本 gate 代替：

1. 完整读取范围、目标商品窗口、商品/款式归属和信息池粒度是否准确；没有把不同商品混编。
2. 每条实际成片是否按 `references/clip-selection-policy.md` 独立承载应有信息及必要证据、适用条件和限制；其他成片不能补足本条。
3. 每段原话是否在真实上下文中支持其信息点；重排后对象、代词、条件、因果和相邻衔接是否仍成立。
4. 是否保留适用且合规的原文促单完整表达及其必要上下文；原文没有时是否避免编造、改写、补充或跨商品移用。动态交易信息仍按全局规则处理。
5. 正式词库之外的语义等价、事实边界和上下文风险；风险提示不自动拦截，也不构成事实核实或合规结论。
6. 开头是否在完整信息池后把真实钩子原话与必要紧邻承接联合编排，综合判断前 2 秒吸引力及前 5 秒连续吸引力；默认按 1.2 倍速将原素材累计 2.4 秒、6 秒作为参考而非硬剪辑点，未为贴合时间硬截原话；承接按素材动态延续情绪、视觉/动作期待、种草兴趣或购买收益等动力，没有固定类型、顺序、权重或评分；主播设问没有被包装为真实顾客反馈；仅凭 SRT 时音画效果标为未核验。
7. 实际方案数量是否符合 `references/clip-selection-policy.md`，默认双方案是否具备独立购买核心；若只交付一条，是否说明第二条不能成立或会降低质量的具体原因；若超长是否记录动态筛选与省略项。
8. 时长是否在完整编排后计算；未明显超过 120 秒时是否保留全部有效信息，超长时是否按该方案核心动态筛选、保留完整购买决策并说明有效信息省略项。
9. 标题、话题及固定五部分是否满足当前任务要求；序号与正文一致。

## 明确失败项

出现任一项，实际成片验收不通过：

- 未完整读取目标商品有效窗口或未建立完整信息池，就比较开头或写方案。
- 开头比较扩展为完整成片竞争、资格评分或多维排名，或把某类钩子固定为优先；未把钩子与紧邻承接联合判断；把 1.2 倍速对应的 2.4 秒/6 秒当成硬剪辑点并硬截原话；主播设问被写成顾客真实反馈；仅凭 SRT 声称视觉、语气、表情或情绪已验证。
- 未按 `references/clip-selection-policy.md` 直接交付默认双方案，且未能说明第二方案不能成立或会降低质量的具体原因；或把第二方案做成仅交换顺序的重复版本。
- 摘要有效时仍强制重新完整读取所有规则，或摘要失效/缺失/哈希不匹配时继续按摘要执行。
- 任一实际输出方案不符合逐条覆盖与超长例外规则，或用其他方案补足本条。
- 原话改写、补造、不连续拼接、来源编号错误、商品串用或条件/归属改变。
- 原文存在适用且合规的促单话术却未完整保留；原文没有时编造、改写、补充或跨商品移用；或把动态交易信息错误保留。
- 将正式禁词范围扩大到未命中的邻近字幕，或把风险提示当成机器硬失败或合规结论。
- 把 120 秒当作目标或硬上限、未先完成完整编排就删点，或超长时按固定卖点类别删选而破坏购买决策完整性。
- 五部分交付缺项，或声称执行了未运行的脚本、读取了未读内容、核验了未查看的音画或同步了无法读回的渠道。
- 加入多个 AI/Agent、额外语义轮次、普通文本任务必须通过的工具或环境门槛。

## 检查项

1. **输入与范围**：确认来源类型、解析状态、实际已读范围、目标商品和必要上下文；未读或截断部分不能声称已检查。
2. **读取顺序与完整信息池**：确认所有目标窗口读完后才建立完整信息池并控制粒度；未因第一条强卖点或局部方案提前锁定角度。
3. **粒度、归属与事实边界**：有效独立购买信息未被拆得过细或合并遗漏；商品、款式、对象、限制和适用条件清楚。
4. **开头选择**：在完整信息池后，把真实钩子原话与必要紧邻承接联合编排；综合判断前 2 秒吸引力与前 5 秒连续吸引力。默认 1.2 倍速下原素材累计 2.4 秒/6 秒仅供估算参考，不硬截完整原话；承接按素材动态延续观看动力，不固定类型、顺序、权重或评分；不将主播设问当顾客反馈，也不把未核验音画说成已验证。
5. **方案数量与差异**：按唯一规则交付默认两条或说明单条例外；各方案核心、排序和结构实质不同。
6. **逐条完整覆盖**：每条方案独立从完整信息池编排；未明显超 120 秒时覆盖全部有效信息，超长例外按唯一规则核对；并集不代替逐条核对。
7. **原话与促单**：来源、序号和完整语境一致；适用且合规的促单按原话保留，没有来源时不补造；风险和动态交易信息依全局规则处理。
8. **时长与信息密度**：每条先完成全量编排再计算时长；120 秒不是目标或硬上限。按唯一规则判断是否触发超长预设、逐条动态筛选及未采用信息说明。
9. **脚本核验与人工边界**：脚本只支持结构及直接命中检查；语义卖点覆盖、原话支持、事实归属、限制和衔接由 AI 判断。实际未运行的工具明确标为手工对照。
10. **交付**：终检所有实际写出的成片；输出保持固定五部分，序号与正文一致，所有待核和未验证事项如实说明。

## Embedded source: references/long-context-mode.md

# Long Context Mode｜AI-First 长文本模式

## 目标与边界

在较长、多商品或分散窗口的字幕材料中，管理可核实的读取范围和目标商品边界。商品理解、购买信息识别、开头比较与编排仍由同一 AI 在一次语义处理中完成。

## 启用与读取

- 当全文读取有截断、遗漏、上下文污染或商品反复切换风险时，按需启用长文本处理。
- 覆盖来源首尾、窗口之间的必要上下文以及目标商品全部离散片段。分段只管理读取范围；窗口地图只确认范围和商品归属，不替代信息池。
- 逐个目标窗口记录读取范围并理解归属、条件与合规边界；读完所有目标窗口后，再一次性识别完整有效信息池并控制粒度。不得边读边锁定主线、生成成片或围绕局部方案补点。
- 建立完整信息池后，按动态顾客心理驱动钩子机制跨主题比较真实原话及必要紧邻承接，不设置固定类型优先级、权重或评分。方案数量、独立购买核心、逐条覆盖及超长筛选唯一遵循 `references/clip-selection-policy.md`；默认直接生成应交付方案，不暂停等待主题选择。

## 前后位置公平

所有已读窗口都应对完整信息池和开头比较提供公平来源。后段出现的重要顾客困扰、直接回应、可信收益或独立购买信息不能因位置靠后而遗漏；但开头比较始终限于开头和必要紧邻回应，不扩展为完整成片竞争。

## 装配与降级

1. 确认来源读取范围和目标商品窗口；仅补读确实缺失的范围。
2. 所有目标窗口完整读完后，按 `references/editorial-policy.md` 建立信息池并比较开头；按 `references/clip-selection-policy.md` 确定方案数量、逐条编排和时长处理。
3. 为本次输出的每个方案分别组织原话并按 `references/final-check.md` 终检。不得在发现多主题机会后暂停等待选择。

分段读取、时间码定位和时长估算是可选机械辅助；工具不可用时，只要文本仍可靠可读就继续。只有来源无法取得、读取范围存在无法补齐的缺口或关键归属无法确认时，才说明受限。

## Embedded source: product-knowledge-packs/womens-fashion.md

# 服装与穿搭商品知识包

## 适用范围

作为事实核对参考，适用于女装、常规服装、箱包及其他穿搭单品。鞋类、围巾等知识包可在其自身事实与适配内容确实出现时分别参考。此文件不规定结构、卖点顺序、内容模板或任务路由。

## 需按原话与来源区分的事实

- 服装外观、穿着轮廓、肩线、腰线、衣长、视觉比例和搭配效果应依据字幕原话或实际可用证据；没有查看画面时不补写显瘦、显高、显气色或遮肉结论。
- 颜色和搭配的价值取决于原话实际表达的顾客结果与使用关系。颜色名称、服装名称或“什么都能搭”不证明所有人或所有搭配都适用。
- 尺码、衣长、版型和选购建议保留对象与条件；不把普通建议冒充顾客困扰，也不把主播偏好扩成普遍适配。
- 材质/成分、工艺、视觉质感、主观手感与穿着体验是不同事实。没有商品资料时不把主播表述说成已核实事实，也不从材质名推导含量、品质、功效或所有人适用。
- 顾客担忧、商品负面表现和主播回答按原话语境分别识别；确认存在的负面表现不反向包装成优点。重要护理、安全或不适用条件不能被删除后留下相反承诺。
- 顺带出现的外套、裤装、鞋包等可帮助理解穿搭关系；其独立规格、材质、功能和适配不能混入目标商品。
- 同款不同颜色可共享确实适用于各色的事实；颜色或款式专属的面料、版型、图案、搭配和外观只归对应选项。同品牌、同系列或相似款不自动视为同一商品。多件单品同时出现时，明确目标商品、款式和适用范围；不得将搭配单品的卖点或事实误归属到目标商品。多件单品同时出现时，明确目标商品、款式和适用范围；不得将搭配单品的卖点或事实误归属到目标商品。
- 试穿、版型或细节若必须看画面才能确认，应标注画面待核实；只有 SRT 时不声称已验证穿着效果。

全局禁用表达只按 references/global-rules.md 执行；本知识包不复制或扩大禁词。

## Embedded source: product-knowledge-packs/shoes.md

# 鞋类商品知识包

## 适用范围

作为事实核对参考，适用于单鞋、高跟鞋、平底鞋、皮鞋、靴子、雪地靴、运动鞋、跑鞋、休闲鞋、凉鞋、拖鞋及其他鞋型，不限性别与季节。此文件不规定结构、卖点排序、内容模板或任务路由。

## 需按原话与来源区分的事实

- 鞋类字幕可能涉及鞋型、鞋头空间、鞋面与内里、鞋底结构、重量、软硬和回弹、跟高、鞋筒、脚型尺码、材质工艺、搭配或使用场景；具体哪些事实成立取决于本次商品与原话。
- 鞋底软、前掌空间、鞋跟高度、脚背适配和裤装搭配不能一概合并成“舒服/百搭”。不同鞋款的脚感、功能、尺寸或适配建议不能互相移用。
- 保留脚宽、脚背、鞋头空间、脚长/尺码、鞋筒与腿围、鞋跟高度和试穿体验的适用条件；不推断所有宽脚、胖脚或久走人群都适配。
- 区分材质/参数事实、结构设计、主播主观体验、客观功能主张和绝对化承诺。不能从鞋型或材质推导防滑、防水、耐磨、矫姿或治疗效果。
- 缺少证明不自动等于已知虚假；没有商品资料佐证的材质、功能和效果不说成已核实。医疗/健康效果、绝对保证和用户全局禁令按更高边界处理。
- 同一商品不同颜色可共用确实适用于各色的描述；鞋面材质、外观、鞋底、尺码、鞋跟、链接/款号和适配只在来源支持时归属到具体选项。
- “你看这个鞋头”“我这样弯给你看”等依赖画面的讲解，可标画面待核实；完全依赖画面、离开视频无明确语义的碎句不作确定事实。仅有 SRT 时不得声称看过上脚画面或演示。

全局禁用表达只按 references/global-rules.md 执行；本知识包不复制或扩大禁词。

## Embedded source: product-knowledge-packs/scarves.md

# 围巾与颈部配饰知识包

## 适用范围

作为事实核对参考，适用于针织围巾、羊毛/羊绒围巾、皮草/毛绒围脖、丝巾、披肩、围领等颈部配饰，不限季节。丝巾不自动等于保暖用品；披肩作为服装销售时按实际商品事实识别。此文件不规定结构、卖点顺序、内容模板或任务路由。

## 需按原话与来源区分的事实

- 区分材质/成分事实、可描述的视觉质感、主播主观肤感、保暖体验/客观性能和绝对化承诺。材质名称不能推出含量、品质、保暖等级、一定不扎或适合敏感人群。
- 兔毛、羊绒、羊毛、皮草、龙猫毛等称谓按原话识别；不能仅凭商品俗称确定真实材质、动物来源或含量。缺少资料时标待核实，不扩展成已知虚假；用户全局禁令按 references/global-rules.md 执行。
- “绝不掉毛”“所有人都不扎”“任何气温都保暖”等泛化说法依语境和证据处理，不因主播说过就认定为普遍事实。
- 普通负面体验、敏感人群限制、护理要求（如干洗）及安全注意事项分别判断。重要限制不能被删掉后留下“所有人适合”或“完全不扎”等相反承诺。
- 不同围法只有在原话给出不同佩戴利益时才构成不同购买信息；动作不同本身不等于新信息。“这样一弄”“你们看这里”等只有画面才能解码的碎句不作确定事实。
- 分开识别与大衣、毛衣、羽绒外套等服装的搭配、颜色关系、穿搭效果及季节/出行场景；顺带提到服装时不把服装规格或独立卖点移给围巾。
- “建议买两条”“多备几个颜色”本身是行动建议，不证明存在两个不同用途。同款不同色可共享通用事实；材质、长短、双面设计、图案、围法和穿戴效果须归属正确款式。

全局禁用表达只按 references/global-rules.md 执行；本知识包不复制或扩大禁词。
