# 字幕亮点对照表与结构检查

仅字幕/SRT工具路径使用。人工通读、区分不同购买理由并完成逐窗记录后，建立 UTF-8 JSON，保存为 `highlights.json`。一项购买理由一条，`point` 为原话要点，`source_ids` 为快照中支持该点的原始字幕编号；按原素材写，不凭品类补造。多个相关但不同的利益应分别记录，不以同类归并。来源不明或商品指代不明，仍可记录可靠编号并标待核实，不采用无编号的虚构来源。

```json
{
  "highlights": [
    {"id":"h1","point":"轻","source_ids":["12"],"status":"入选","retained_ids":["12"]},
    {"id":"h2","point":"柔软","source_ids":["34"],"status":"未入选","reason":"该句与别款商品交叉，指代尚不能确认"},
    {"id":"h3","point":"上身轻","source_ids":["56"],"status":"合并","merged_into":"h1","retained_ids":["12"],"reason":"与h1均表达穿着轻"},
    {"id":"h4","point":"小雨防泼","source_ids":["78"],"status":"入选","retained_ids":["78"],"note":"商品归属可靠；功能和适用条件待核实"}
  ]
}
```

状态及字段：
- `入选`：`retained_ids` 非空，必须属于该条 `source_ids`，且实际存在冻结方案中。商品归属可靠但内容存疑的亮点仍为入选，在 `note` 和成片对应位置说明具体待核实事项。
- `合并`：`merged_into` 指向一条 `入选` 记录，`retained_ids` 是该目标实际入选来源；`reason` 说明为何同义。同类不同利益不可误标同义。
- `未入选`：`reason` 写具体约束及取舍，不只写“重复”“精简”“时长”“衔接”。
- `待核实`：`reason` 写清商品归属等具体事项及暂不采用的原因；不得把待核实作为已确认事实。

完成主观补漏比较和人工冻结后执行：
```text
python -S scripts/check_highlights.py --snapshot session.json --plans plans.json --ledger highlights.json
```
退出码为0表示记录结构、来源ID、状态及保留序号与快照/单方案的机械对应通过。失败时修正具体错误并复核。程序不识别遗漏的亮点，不判断含义是否相同、理由是否真实成立、窗口是否读完、商品事实、合规或音画；`HIGHLIGHT RECORD CHECK PASS` 不代表亮点齐全或成片质量通过。即使通过仍要人工逐项审阅和按源内容补漏。

短文本可以直接在工作记录列出等价表并人工核对；没有原始字幕编号的 MP4-only 不虚造编号或运行此工具，应使用实际可核验时间与工作记录手动核对。没有可靠方案时不运行空方案来伪造通过。

