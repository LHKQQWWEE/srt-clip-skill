# C2 Universal 0.3.20｜发布验收记录

## 基准与变更文件

- 基准：本机已安装的 SRT Clip C2 Universal 0.3.19；目标正式版本 0.3.20。
- 通用结构：`.agents/skills/srt-clip-c2/SKILL.md`、`references/editorial-policy.md`、`references/highlight-selection.md`、`references/long-context-mode.md`、`references/final-check.md`。
- 入口与分发：`VERSION`、`plugin.json`、`.codex-plugin/plugin.json`、`README.md`、`START-HERE.md`、`CHANGELOG.md`、`docs/platform-adapter-interface.md`、`agents/openai.yaml`、`ENVIRONMENT.md`、`C2-Universal-Portable.md`。
- 专项与质量：`categories/womens-fashion.md`、`categories/shoes.md`、`categories/scarves.md`、`tests/quality-rubric.md`、三项现有测试文件及新增 `tests/test_decision_editor_contract.py`。
- 清理旧入口：删除当前分发中的 0.3.19 验收记录；本机旧 0.3.19 插件缓存规则与文档已清空；新入口和便携内容只指向 0.3.20。

## 规则变更

- 功能身份统一为“带货短视频购买决策编辑器”；Universal Core 成为通用结构唯一权威。
- 开头使用陌生顾客首屏价值测试，明确强结果候选可淘汰普通颜色、搭配和泛介绍；老粉限定不默认代表陌生顾客。
- 首次成交升级为“第一次购买决策闭环”：购买理由先成立，再选择自然、低阻力机会；首次成交后继续评估未利用的独立高价值理由。
- 使用动态高/中/弱决策价值层级，不设机械覆盖率；单位时间购买决策价值和每段信息密度参与取舍。
- 正式成片按 1.2 倍速预计 45–120 秒，45–90 秒优先；90–120 秒只在仍有独立高价值信息时扩展。低于 45 秒先检查有效理由，仍不足则标为短候选；禁止凑时长灌水。
- 中段优先购买决策链；多条方案走互补购买路径；长文本后段强卖点与前段候选按同一标准竞争。
- 质检增加明确失败项，质量权重转向首屏价值、独立理由覆盖、成交闭环与多路径互补；第三部分只保留核心理由、关键补充理由、重要未采用内容及原因。
- 普通任务没有增加模型轮次、Python、JSON 台账、网络或环境硬依赖。

## 测试结果

- 0.3.19 基线套件：51/51 通过。
- 0.3.20 现有与新增测试：`python -m unittest discover -v`，57/57 通过；覆盖入口版本、规则权威、类别专项、长文本压力、价值层级、成片时长、输出和工作流边界。
- `git diff --check` 通过；两份插件清单、`VERSION` 与 0.3.20 一致；便携文件完整嵌入当前引用源；0.3.19 验收文件不在当前 ZIP 或远程插件文件清单中。
- 口播文本语义回归 8/8 支持预期取舍：强结果 vs 颜色、陌生顾客 vs 老粉、过早硬 CTA vs 低阻力成交、首次成交后高价值理由、37 秒扩至 52 秒且不灌到 90 秒、34 秒短候选、单条独立理由覆盖、长文本后段强卖点公平竞争及多条路径互补。
- 没有收到真实客户 SRT；语义回归使用带字幕序号的自然口播样例，不代表真实商品事实、真实剪辑时长或转化表现。

## 发布状态

- 仓库工作副本：已更新到 0.3.20；未提交，未推送 GitHub。
- 本机 Skill：`D:\codex\.codex\skills\srt-clip-c2` 已同步，文件集合与当前 Skill 源一致；旧版验收与回归说明已清理。
- 私有插件：Plugin Creator 回执确认更新为 0.3.20，权限范围保持 PRIVATE，release ID 为 `pluginrel_6afbd01abbf881919c1df0314516bc40`。
- 本机插件磁盘缓存：已建立 0.3.20 缓存；0.3.19 缓存目录内不再有文件。应用进程内缓存是否已刷新尚未验证。
- 便携 ZIP 与纯文本 portable 文件已在本地生成并核对；未同步 Google Drive 或其他外部渠道。

## 未验证项

- 实际客户 SRT 的端到端选片、时间码及成片时长；音频、画面和商品资料核对。
- 平台审核与投放效果、购买转化提升。
- 多条方案的差异程度和价值层级保持语义判断，没有设置机械分数门槛。
