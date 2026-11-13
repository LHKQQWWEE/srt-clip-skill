# Blind application probes for C2 0.2.21

These are synthetic inputs for a fresh-context evaluator. Apply the installed skill to each request and return a concise decision, proposed first group/source IDs, and any required edit notes. Do not read the expected-results file while evaluating.

## A. Material word in a multi-sentence cue

User says the platform flags the exact material word “白鹅绒”.

```text
1 1.2 这件羽绒服是白鹅绒的。面料还做了三防工艺。
2 1.0 新国标九五的鹅。
3 1.0 短款显腿长。
```

## B. Material word and useful detail in one sentence

User says the platform flags the exact material word “白鹅绒”.

```text
1 1.2 新国标白鹅绒，版型穿起来还显瘦。
2 1.0 面料做了三防工艺。
3 1.0 腰线在这里。
```

## C. Appearance hook versus customer pain

```text
1 1.5 小个子买羽绒服，总担心穿起来显矮。
2 1.4 这件羽绒服穿起来真的很好看。
3 1.3 新国标九五的鹅。
4 1.2 面料是做三防的工艺。
```

## D. Direct customer comment and host response

```text
1 1.4 顾客弹幕：小个子穿这件会不会显矮？
2 1.2 衣长到这儿，腰线在上面。
3 1.1 我穿这个不会显矮。
4 1.0 里面是九五的鹅。
```

## E. Product/color statement versus customer issue

```text
1 1.3 这件是苔藓绿的M码大货。
2 1.2 对这种颜色呢，它比较怕流水印子。
3 1.2 这件穿起来很利落。
4 1.1 我们用的里料很轻。
```

## F. Color coordination alone

```text
1 1.2 这个颜色配黑裤子很好看。
2 1.2 显白。
3 1.2 这件羽绒服穿上显瘦又好看。
```

## G. Sizing advice versus product USP

```text
1 1.3 一米五八以下建议穿短款。
2 1.4 新国标九五的鹅。
3 1.2 面料是做三防的工艺。
4 1.1 衣长到臀部上面。
```

## H. Styling and product-topic order

```text
1 1.0 这件羽绒服衣长七十一。
2 1.0 腰线做得比较高。
3 1.0 里面是九五的鹅。
4 1.0 面料做了三防。
5 1.0 搭黑裤子显得利落。
6 1.0 搭直筒牛仔裤也可以。
7 1.0 裤腿不包身。
```

## I. Ending pressure and price/stock

```text
1 1.4 买过的姐妹都说穿起来好看。
2 1.5 这件真的很好看，大家赶紧拍，库存只有三件。
3 1.2 今天到手价只要五百。
4 1.1 觉得合适可以点进来看看尺码。
```

## J. Product facts conflict

```text
1 1.2 这件短款衣长七十一。
2 1.2 长款衣长九十三。
3 1.2 这件的衣长是七十一。
4 1.2 这件的衣长是九十三。
5 1.0 都属于同一个羽绒服款式系列。
```

## K. Possible transcription error in a material word

User says a prior platform note flags “白鹅绒”, but the SRT has an unclear recognition:

```text
1 1.2 这件填充是白鹅荣。
2 1.0 面料做了三防。
3 1.0 版型很利落。
```

## L. Plan count

User asks “做切片文案”, provides one clearly identified jacket, and gives no plan count. The input includes one strong appearance opening and one clear customer-pain opening, both with source-supported follow-up sections.

## M. Two requested plans with several highlights

User explicitly requests two plans. One starts with a complete appearance compliment and the other with a quoted customer-pain question. The source has shared core points plus two secondary outfit pairings that fit the runtime; reuse the core points but assign the pairings by plan focus so they do not repeat automatically in both versions. No item is flagged or uncertain.

## N. Hard duration boundary

User requests one SRT clip. A frozen plan totals 144.001 seconds at source speed (more than 120 seconds at 1.2×), while another totals exactly 144 seconds. Reject the first during rendering and allow the second on duration grounds; include any known unaccelerated time before applying the cap.

## O. User-designated forbidden phrase

User says to add “三醋酸羊绒羊毛” to their prohibited wording list.

```text
1 1.2 这件是三醋酸的羊绒、羊毛材质。穿起来很轻。
2 1.0 颜色搭配很显白。
```

The phrase-bearing sentence must be removed whole. The independent “穿起来很轻” sentence may remain if exact sentence boundaries are validated and a cut-point note is included. The phrase must not appear in selected transcript, title, or tags; if quoted for traceability, label it only as an excluded source exception and do not call it a platform finding.
