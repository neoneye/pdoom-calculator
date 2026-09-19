# The site's reception, and what it did to the numbers

**Date:** 2026-09-20
**Scope:** An observation by the site's author about how the calculator was
received when shared, recorded here because it bears on how the submissions
should be read and would otherwise be lost. Follows
[the 19 September report](../reports/submissions-2026-09-19.html) and
[the ESPAI comparison](2026-09-15-espai-2024.md).
**Outcome:** The tone of comments about the site turned around August 2026, from
"doomer" to accepted. The rows before March, with their zeros, come from the
first period; the rise to a 50% median among visitors who set their own number
in August comes from the second, and the page's proposed number cannot explain
that rise. Whether September's fall is the crowd settling or a quieter news
month is not answerable, because the site does not record where a visitor came
from. Storing the referrer would make it answerable.

---

## 1. The observation

Until August 2026, when the calculator was shared, the immediate response was
mostly trolling: the author was a doomer, the premise was stupid. From around
August the same places treated concern about AI as an accepted position. The
author associates the turn with the weeks when the OpenAI–Hugging Face intrusion
was everywhere on social media; a later incident, an AI system at Google
escaping its sandbox, was barely discussed. This is an impression, not a count.
There is no archive of the comments.

## 2. What the table shows beside it

- **The pre-March rows have the site's only real low tail.** 98 hand-set
  submissions before the quiz launched on 9 March: median 15%, 9% at exactly
  zero, 14% under 1%. The 190 quiz-era rows have two zeros. A troll registering
  0% to make a point and a sceptic registering 0% as a view are the same row.
- **August's rise is not all the proposal.** Among visitors who set their own
  number, repeat rows excluded, August's median is 50%. The page's proposed
  number explains the kept rows; it cannot explain movers.
- **August is three bursts, not a month.** 3–5 August (18 rows, medians near
  70%), 18 August (7 rows, median 95%) and 20–21 August (18 rows, median 33% and
  24% among movers, the day after the expert check launched). Each burst looks
  like one link posted in one place, carrying the mood of that place.
- **September is steadier and lower.** Three to fourteen rows a day, medians
  mostly 30–60%, 31% among movers.

## 3. What it cannot show

The table does not say where a visitor came from. A burst from an alarmed news
thread and a burst from a sceptical forum leave the same columns. So "the
reception changed" and "the referrers changed" are the same hypothesis from
two ends, and neither can be checked on the rows the site has.

## 4. What would make it checkable

Store `document.referrer`, or a one-tap "how did you get here", as a diagnostic
column outside the signed string, the way `page_version` is. It costs the
visitor nothing and lets the next report tie each burst to its source. Until
then, any statement about why the crowd changed is an author's impression and
should be labelled as one, as the 19 September report now does.
