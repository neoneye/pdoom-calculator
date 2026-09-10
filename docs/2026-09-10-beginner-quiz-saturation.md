# Beginner quiz: it saturates, and decoys are the fix

**Date:** 2026-09-10
**Scope:** What the 10 September report says about how well each quiz separates its
respondents, and what to change on the beginner quiz. A note for later, not a plan.
**Outcome:** The beginner catastrophe and capability lists have a ceiling that most
respondents sit on. Adding more answers raises the ceiling without moving anyone off it.
Adding a few decoys creates an answer that can be wrong, which is what every quiz lacks
and the expert check has. Three or four decoys per list, scored as hits minus tripped.

---

## 1. What the report shows

The 10 September report ([reports/submissions-2026-09-10.html](../reports/submissions-2026-09-10.html))
charts every quiz question: how many ticked each answer, and the p(doom) of the
respondents split into thirds by how many they ticked.

On all 253 rows the pattern is that most recognition questions are ticked in full by
nearly everyone:

| Question | Respondents | Answers ticked by nearly all |
|---|---|---|
| Beginner catastrophes (12 options) | 46 | 4 answers at 45 of 46 |
| Beginner capabilities (8 options) | 46 | 3 answers at 44 of 46; 19 ticked all 8 |
| Expert self-improvement (4 options) | 41 | 32 ticked all 4 |
| Expert self-replication (5 options) | 41 | 27 ticked all 5 |

A question nearly everyone answers the same way cannot separate anyone. The "most
informed" third on the capability list is simply everyone who ticked all 8.

## 2. What the last fortnight shows

Restricting to the 51 rows since the 1 September export changes one thing. Every one of
the 15 new expert respondents came through the check, and the expert quiz stopped
saturating:

| Expert question (n = 15) | Ticked every option | Options ticked by all |
|---|---|---|
| Continuous learning | 4 | 0 of 3 |
| Self-improvement | 7 | 0 of 4 |
| Self-replication | 7 | 0 of 5 |

So the expert reasoning questions were not badly written. They were being answered by
the wrong people. The check fixed the expert quiz's calibration by fixing who takes it.

The beginner quiz did not improve, because nothing filters who takes it. On the 13 new
beginners, 6 of 12 catastrophe answers and 4 of 8 capability answers were ticked by all
13, and 9 of 13 ticked every capability. The film list is the only beginner question with
real spread, and it spreads because films are unevenly seen, not because there are 28.

The medium vulnerability list still works: thirds by count recognised submitted 70%, 43%
and 37% p(doom) in the new cohort, rank correlation +0.35 on 23 rows. It has 16 entries
with a long tail (side-channel attacks 9 of 23), so it has room below the ceiling.

## 3. Why more answers does not fix it

The saturation is not a lack of items. It is that every item can only be ticked
correctly. Add eight more capabilities and the same nine people tick 16. The ceiling
moves up and the crowd moves with it. The film list shows the alternative: spread comes
from items that are genuinely unevenly known, and catastrophes and AI capabilities are
common knowledge.

## 4. Why decoys do

A decoy is an answer that can be wrong. It turns "how many did you tick" into "how many
did you tick correctly", and it separates two people who both tick everything: one
recognises the list, the other ticks lists. The expert check demonstrates the mechanism
on this site's own visitors: two of 21 finishers fell below the bar, both by tripping
decoys built on keyword collisions (The Standard Model, Wire-frame model, Schrödinger's
cat). This has been the report's oldest open recommendation since August.

## 5. What to do, when there is time

- **Catastrophes:** add three or four fabricated but plausible entries. Names that sound
  like risk categories but are not, such as an invented astrophysical event or a made-up
  pandemic term. Do not use real-but-obscure risks; those punish knowledge.
- **Capabilities:** harder, because almost any capability is at least arguably real. Use
  things AI cannot do that a beginner might believe, or things that are not AI at all
  dressed in AI vocabulary. The check's keyword-collision pattern transfers.
- **Films:** leave alone. It already spreads, and invented films are easy to spot.
- **Scoring:** hits minus tripped, as the check does. Store both so the report can show
  decoy rates per item, the way the term-by-term figure does now.
- **Dose:** three decoys in twelve is enough to separate people without making an intro
  quiz feel like a trap. The check uses fifteen in thirty, which suits a gate and not a
  welcome.
- **Alternative:** leave the lists untouched and add one scored question with decoys at
  the end of each quiz. Less elegant, but every existing figure stays comparable.

## 6. Cautions

- Decoys change what the question measures, from familiarity to discrimination. The
  pre- and post-decoy cohorts are not comparable, so the report must split at the launch
  date, as it already does for the check and for late-added options via `OPTION_ADDED`
  in `prepare_report_data.py`. The `page_version` stamp pins which list a row saw.
- The new-cohort numbers above are bands of 2 to 9 people. They give direction, not size.
- The opinion questions (gut reaction, competition, governance, speed) separate people
  well and always will, because they restate the sliders. They are not evidence of
  calibration and should not be counted as such.
