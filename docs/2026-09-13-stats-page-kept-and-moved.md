# Stats page: stop averaging the page's numbers with the visitors'

**Date:** 2026-09-13
**Scope:** What the live stats page at `/stats/` should show now that every
submission can be classified as *kept* (the visitor registered the number the quiz
proposed) or *moved* (the visitor set their own). Follows
[storing the calibrated starting point](2026-09-12-store-calibrated-start.md) and
[splitting the reports](2026-09-12-split-untouched-moved.md); this note is the
same split applied to the one page most visitors actually see.
**Outcome:** Replace the single "Average P(doom)" card with the median of the moved
rows and the share that kept the proposal; draw the histogram as two series; give
the factor table a moved-only column. Classification runs in the browser from the
columns the page already fetches, with no server change.

---

## 1. What the page shows today, and why it misleads

The stats page fetches every row and shows three cards, a histogram and a factor
table. The headline card is the mean of every `summary.midpoint`: 43.4% on
12 September. That number blends four populations that have nothing to do with each
other:

| Rows | What the midpoint is |
|---|---|
| 98 before the level chooser | a number set by hand on three sliders, median 15% |
| 50 quiz rows that kept the proposal | the calibration's output, median 72–92% by level |
| 99 quiz rows that moved a slider | the visitor's own number, median 34–48% by level |
| 6 with no level since March | the 50/50/50 default, 12.5% |

A mean across those is not the community's p(doom). It is mostly a measure of how
many people took the medium quiz and pressed submit. The reports now separate the
groups; the stats page, which is linked from the calculator's own navigation and
read by far more people, still does not.

The mean is also the wrong statistic for this distribution. The histogram on the
same page shows the shape: two humps, one near zero and one above 70%. A median
survives that; a mean lands between the humps where almost nobody is.

## 2. What to show instead

Three summary cards, in place of the current three:

- **Submissions** — unchanged, the row count, with the last-submission time folded
  into its subtitle rather than given its own card.
- **Median p(doom), visitors who set their own number** — median of the moved rows,
  with n. This is the closest thing the table has to what people think.
- **Kept the quiz's proposal** — share of quiz rows, with n, and the median those
  rows registered. Shown, not hidden, because it is the mechanism the site chose and
  the reader should be able to see its size.

Under the cards, one sentence, in the same register as the calculator's own copy:
"After a quiz the page proposes a starting number from the answers. Rows that
registered it unmoved are shown separately from rows where the visitor set their
own." No more than that; the figures carry the rest.

**Histogram.** Two series on the same bins: moved rows as the solid bars, kept rows
stacked above them in the lighter tint the site already uses for `--chart-bar`
against `--chart-bar-border`. A two-entry legend. The pre-chooser and no-level rows
belong to the moved series, since their numbers were set by hand; if that reads
as unfair to the quiz era, a third series for "before the quiz" is cheap and keeps
the March boundary visible.

**Factor table.** Keep the three rows. Replace the three mean columns with medians,
and add a column for the moved rows only, since the pooled medians of the quiz era
are the cube root of the proposal (0.91, 0.91, 0.91 on the kept rows) and say
nothing about how visitors weigh the links. The pre-chooser cohort's 0.76, 0.60,
0.50 and the movers' 0.89, 0.80, 0.85 are the two chains worth comparing.

**Export.** Leave the JSON export raw. Add one derived field per row, `kept`, with
the rule used, so anyone downloading it does not have to rediscover the split.

## 3. Classifying a row in the browser

The page already fetches `quiz_flow_id`, `quiz_answers` and `factors`. Add
`calibration` to the select. Then, per row:

1. No quiz level → not applicable. Counted with the moved rows in the histogram,
   excluded from the kept share.
2. `calibration.per_factor` present → kept if all three `factors[i].midpoint` are
   within 0.0005 of `per_factor / 100`. Exact; this is every row from 12 September
   on.
3. Otherwise → kept if all three midpoints are equal. This is the proxy from the
   report note. On the 10 September export it disagrees with the exact rule on one
   row in 149, a visitor who dragged all three sliders to the same spot, and it
   needs none of the calibration tables. Good enough for a live page, and the
   population it applies to stops growing the day the column is populated.

Porting the three calibration functions into the stats page, as the build script
does in Python, would make rule 3 exact. It is not worth it: the functions depend
on the quiz option lists and their add dates, which would have to be shared with
`index.html` or duplicated, and the population they would improve is fixed at 149
rows with one known disagreement.

## 4. Implementation notes

- `aggregateFactors`, `average` and the histogram builder in `stats/index.html`
  each take a row list. Give them a `kept` predicate and call them twice, or once
  with the rows tagged; the structure does not need to change.
- Add a `median` helper beside `average`. Keep `average` for the export's
  backward-compatible `average_pdoom` field, and add `median_pdoom_moved`,
  `kept_share` and `kept_count` beside it rather than renaming.
- Chart.js already renders the histogram; a second dataset with `stack: 'p'` on
  both is the whole change to the chart config.
- The CSS tokens for the second series exist: `--chart-bar` is the translucent
  fill, `--chart-bar-border` the solid; use the solid for moved and the translucent
  for kept, so the visitor's numbers read as the foreground.
- The reports list at the bottom of the page needs no change.

## 5. What this does not do

- It does not change the calculator. The quiz still proposes a number; the
  decision on that is made and this note does not reopen it.
- It does not make the moved median "the truth". Moved rows include people who
  moved one slider by a point. The gap between proposed and registered, which the
  reports now show, is the finer instrument; the stats page only needs the coarse
  split to stop reporting a blend.
- It does not fix the About page, which is a separate note if it is wanted.
