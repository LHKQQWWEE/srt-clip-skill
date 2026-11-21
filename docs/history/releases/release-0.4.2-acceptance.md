# C2 Universal 0.4.2 Release Acceptance (Archived)

Date: 2026-11-18

Archived historical acceptance record for core 0.4.2 / plugin package 0.4.9. It is not an active rule source or the current release acceptance record.

## Acceptance scope

- Integrates attention decay, the minimum sufficient purchase unit, the earliest natural purchase opportunity, distributed reassessment, context dependencies, and the rule that the back half cannot carry first persuasion.
- Keeps the existing AI-First, single-pass role structure, five-part output, source fidelity, product attribution, independent-value coverage, repetition judgment, dynamic-information exclusions, compliance rules, and category-neutral architecture.
- Adds a nonmechanical, semantic-boundary truncation pressure test to the existing final review; it adds no fixed time/ratio, agent, model round, Python requirement, or workflow node.

## Test evidence

### Automated regression

- `python -m unittest discover -s '.agents/skills/srt-clip-c2/tests' -p 'test_*.py' -v`: **61/61 passed** (52 existing regression tests plus 9 early-opportunity/truncation-policy tests).
- The new tests cover attention decay, the threshold for a complete reason, the earliest context-valid opportunity, local dependencies of moved action lines, dynamic reassessment without CTA-density growth, back-half persuasion, cumulative semantic-prefix truncation, current versions, trade-information exclusions, and retained output/source rules.

### Real shoe transcript structural test

- Input: the supplied shoe transcript attachment, 609 numbered cues. The local attachment copy is `已粘贴的文本.txt`; this was inspected as text only.
- First complete purchase reason: cue 32 establishes the shoe; cues 35–40 establish the “心机鞋” framing and its inner-lift benefit, qualified by “六七厘米吧”. The value is understandable before the later color, sizing, or transaction sections.
- Earliest candidate purchase opportunity: cue 94 (“一会我给你上车啊”) is the first cart-action candidate after the reason. Its local setup is cues 91–93, a price comparison, so it is not moved on the keyword “上车” alone. Text-only, cue 94 still reads as a link action for the already-established shoe after cues 91–93 are removed; it may follow the completed reason, but this is conditional on the actual live-link/visual context. If that context makes the price setup necessary, discard cue 94 as an early CTA and continue to the next context-valid source line. Do not bring back the price comparison to preserve it.
- Later value coverage: cues 118–124 add a separate fit/space/comfort reason. Keep their “这个位置/这两个” referents in context; the shoe area and removable pieces require the original picture to verify. Later lining/warmth, comfort/rebound, styling, and color-choice sections remain candidates and are not dropped merely because cue 94 has appeared. Color advice must retain the color names and the “this color” referent.
- Truncation pressure uses cumulative prefixes of the proposed final order, not arbitrary cue numbers: the early prefix can pass after the first reason plus cue 94 when the local-context check above succeeds; a later prefix after the fit explanation (118–124) preserves that earlier opportunity and adds a second independent reason. The source claim at cue 39 (“7厘米”) is qualified by cue 40 (“六七厘米吧”), so a cut between them fails the source-context check. A clip beginning with unrelated clothing/promotion cues 1–17 fails the value test. Front/front-middle/middle check locations and their count vary by material; no fixed seconds, percentages, or three-point checklist.
- Excluded live/transactional cues include price comparisons (91–93), coupon (261), stock/size scarcity and urgency (282–287), live benefits/prices/link prompts (321–340 and 543–550), and warranty/return/insurance wording (551–553, 604–605), pending verification that those terms apply to this product and remain current. They are not restored to make the early CTA feel stronger.
- Size advice is inconsistent: cue 290 says regular size even for wide/high-instep feet; cues 352/439 advise sizing up; cue 448 says wide/wide-instep feet do not need to size up. Do not make a definitive size recommendation until this is reconciled. The source also alternates between a 6–7 cm estimate and 7 cm; preserve the qualified statement rather than strengthening it.

### Different-category regression: plain bangle

- Input: the user’s earlier 93-cue plain-bangle transcript, read from the prior C2 conversation as a sample; text-only.
- Cue 8 establishes a sandblasted plain bangle, but the process label and broad “不挑人” claim alone do not yet establish a complete customer reason. Cues 12–14 build a fuller reason (solid, not hollow, with the host’s daily-wear claim).
- Cues 15–17 establish the fine/coarse options and their referents. Cue 22 (“个人建议去买细的啊”) is a context-valid style-choice opportunity once those options are clear; it is not a verified ring-size recommendation. The earlier “放心大胆去冲” line is an action prompt without a complete reason and is not promoted ahead of the product evidence.
- Price, live welfare, listing, and urgency lines from cue 23 onward remain excluded. The test does not force a second CTA because the remaining sample contains no new independent purchase reason that needs another push.

## Release boundaries and residual risks

- No new agent, model pass, mandatory Python runtime, or daily workflow step was added. Python was used only to run the existing repository test suite.
- Text structure and transcript cue ordering were reviewed; video, original audio, product documentation, current inventory/offer terms, platform review, and conversion performance were not verified. The candidate CTA, fit/color referents, footwear claims, size contradiction, and exact benefit measurements need source/video confirmation before publication.
