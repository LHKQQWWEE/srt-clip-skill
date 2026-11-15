# C2 Universal 0.3.4｜同步一致性补丁回归

- 业务规则与0.3.2完全一致；0.3.4不是新的剪辑策略版本。
- 目的：消除插件发布器自动递增造成的manifest/SKILL/GitHub/Drive版本号不一致。
- plugin-level defaultPrompt按账号插件更新规范原样保留；SKILL.md明确兼容字段不得覆盖当前规则。
- 必须复跑规则完整性、长文本压力、Portable一致性及活动冲突扫描。
