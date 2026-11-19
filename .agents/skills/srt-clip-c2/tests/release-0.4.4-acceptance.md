# C2 Universal 0.4.4 Release Acceptance

- **Verified baseline:** live local plugin cache `srt-clip-c2/0.4.10`, Core 0.4.3; original private plugin release `pluginrel_6afdd69fa32081919a6d61cf22dac331`, Core 0.4.3 / package 0.4.10.
- **Target:** C2 Universal Core 0.4.4; plugin package 0.4.11.
- **First formal change in this work:** exact prohibited-cue exclusion; defensive false-rejection repair; complete selling-point discovery and per-video-angle reassessment; fuller single-cut coverage; differentiated complete multi-cut combinations with overall coverage; optional CTA without forced early pressure or a 120-second ceiling.
- **Preserved:** one AI, one semantic analysis, one final check, source wording and cue IDs, product attribution and evidence boundaries, the fixed five-part output, existing 45-second general lower-bound guidance and short-material exception.

## Rule acceptance

- A registered literal term removes only the complete subtitle cue number(s) that match; neighboring cues continue to be assessed. Similar terms, contextual risk and one local hit cannot reject an entire span, candidate or input.
- The complete set of valid target-product selling points is identified before selection. Each candidate video angle independently reassesses every point; one angle's value ranking does not carry to another.
- A single video should include supported, useful selling points as fully as they fit naturally. Multiple videos should each be complete, materially differentiated, and collectively cover the valid points as fully as practical. Explicit multi-video requests receive complete plans directly.
- CTA is optional. Early-CTA and truncation-prefix requirements are removed; an included action line still must retain its original context and comply with dynamic-transaction exclusions.
- No fixed duration ceiling. The user-provided test source is below two minutes after 1.2x, so it does not establish behavior on a longer-than-120-second result.
- The original five-part delivery structure remains active.

## Real source regression

- **Source:** user-uploaded `已粘贴的文本.txt`; 572 consecutive cues, IDs 1–572, positive cue durations, 1,017.241 seconds total.
- **Target-product windowing:** the input switches among the vest, sweaters, pants, shoes, skirt and outerwear. The reviewed target is the repeatedly demonstrated coffee/black wool-texture vest; other-product windows and ambiguous switches were not imported as facts about that vest.
- **Identified target-vest selling-point dimensions:** visual silhouette (slimming / making the torso look more balanced), chest-and-abdomen shaping, indoor wear and layering use, outfit variety through layering, color and lower-garment pairing (trousers / skirt and separate outfit examples), size-selection guidance where attribution is clear, and an optional review reference. These are transcript-supported candidate points, not independent proof of product performance.
- **Filtered or bounded claims:** material-composition statements were not treated as verified because no matching proof was supplied; dynamic price, promotion, inventory, delivery timing, scarcity and sales-volume statements were not used as stable selling points. Conflicting or unclear sizing and neighboring apparel claims were not generalized to the target vest.
- **Single comprehensive plan:** 42 cues / 14 original-contiguous groups; 92.819 seconds of selected source; 77.349 seconds estimated at 1.2x. Cue order: `7–13,191,182–187,130–137,391–392,397–402,100–103,378,386–387,344,501,503,506,53`.
- **Multi plan A — chest/abdomen shape:** 27 cues / 8 groups; 54.890 seconds of selected source; 45.742 seconds at 1.2x. Cue order: `191,180–187,7–13,168–169,98–103,344,53,544`.
- **Multi plan B — indoor layering and outfit pairing:** 30 cues / 10 groups; 68.039 seconds of selected source; 56.699 seconds at 1.2x. Cue order: `136–137,130–134,191,391–402,100–103,378,386–387,501,503,506`.
- The angles were evaluated independently against the full target-product selling-point set. Plans A and B differ in purpose and selected support. Cues 501, 503 and 506 add a second outfit's coffee/black vest and light-pants pairing to the single and B plans; they were left out of A because they do not materially support its shape angle. Cue 507 was too ambiguous to use. In B, 191 supports shape concerns with a layer, 100–103 supports pants pairing, and 501/503/506 qualify the light-pants suggestion as belonging to a different outfit rather than a universal rule.
- No matching material proof was supplied. The following full cues containing target-vest material claims were excluded from these cuts: **5, 139, 148, 167, 192, 195, 259, 543**. This is an editing evidence boundary, not a finding about the product's actual composition. Ambiguous cue 253 and the wool references to loafers / another purple sweater were not expanded into target-vest bans.
- The source contains no literal `皮草` match. This sample therefore does not test a positive prohibited-term hit. Synthetic regressions 22–24 cover exact full-cue exclusion, near-term nonmatches and the distinction between material claims and hand-feel comparison.
- Sample selection and semantic judgments were reviewed against the full pasted transcript; a local validator independently checked cue continuity, all selected cue references, group counts, duration sums and literal `皮草` matches.

## Technical validation

- Source test suite: **67 tests passed, 0 failed** on the 0.4.4 / 0.4.11 candidate.
- Extracted package test suite: **67 tests passed, 0 failed** against the staged ZIP contents.
- ZIP integrity: `testzip()` returned `None`; 44 package members; manifest is 0.4.11 and the embedded Skill frontmatter was verified.
- SHA-256 is recorded in the user-facing validation and synchronization report (outside the archive to avoid a self-referential hash).
- GitHub, original plugin and writable Drive synchronization: pending final publication and read-back.

## Validation boundary

This is a transcript-based editing regression. It does not verify video imagery, audible pacing, product composition, garment appearance, size chart, platform review, or sales performance. The sample does not contain a literal positive `皮草` hit and does not test an output longer than 120 seconds.
