# Blind application probes for C2 0.2.20

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

User explicitly requests two plans. One plan starts with a complete appearance compliment and the other with a quoted customer-pain question. The source also contains distinct garment-length, material, process, warmth, and two different outfit-pairing points, all clearly attributed, clear, and short enough to include in both versions. No item is flagged or uncertain.
