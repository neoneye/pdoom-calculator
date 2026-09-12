# Split every report figure into untouched and moved

**Date:** 2026-09-12
**Scope:** How the submissions reports should separate rows where the visitor left
the sliders where the quiz put them from rows where the visitor moved them, using
the data already in the table. Companion to
[storing the calibrated starting point](2026-09-12-store-calibrated-start.md), which
makes the split exact for future rows.
**Outcome:** A row's three factor midpoints are equal if and only if the quiz
calibration set them and nobody moved one. Flag those rows, give every figure with
and without them, the way the reports already handle signed repeats, and re-read the
three reports' findings in that light. Several of them shrink.

---

## 1. The proxy

The page sets the sliders after a quiz by taking the cube root of a proposed p(doom)
and writing the same value into all three factors (`applyMidpointCalibration`). A
visitor who moves any one slider breaks that equality. So, for a row with a quiz
level:

> all three `factors[i].midpoint` equal → the midpoints were not moved.

The test is exact in one direction and an upper bound in the other. A visitor who
deliberately set all three sliders to the same value by hand would be counted as
untouched; that is rare enough to ignore. The test says nothing about spread: a
visitor can widen or narrow the bands without moving a midpoint, and the row still
counts as untouched. Of the 50 untouched rows on the 10 September export, 15 also
have all three spreads equal; the rest moved a band and left the midpoints alone.

The proxy does not apply to rows without a quiz level. Those started at 50/50/50,
where equality means "left the defaults", which is a different fact. 21 of the 103
level-less rows are in that state and the reports already discuss them under the
12.5% result.

## 2. What the split shows on the 10 September export

| Quiz | Rows | Untouched | Median p(doom), untouched | Median, moved |
|---|---|---|---|---|
| Beginner | 46 | 22 (48%) | 72% | 44% |
| Medium | 62 | 23 (37%) | 92% | 36% |
| Expert | 41 | 5 (12%) | 77% | 42% |

The untouched medians are the calibration's output. The moved medians are the
closest thing the table has to what visitors think. The two differ by 28 to 56
points, and the levels' overall medians (61%, 64%, 45%) are blends of the two in
proportions that have nothing to do with belief.

## 3. Implementation

In `prepare_report_data.py`:

- `load_rows` adds `mv` (moved) per row: false when the level is a quiz and all
  three midpoints are equal, true otherwise, null for level-less rows. Once the
  `calibration` column exists, use it instead and keep the proxy as the fallback.
- `question_breakdown` carries `mv` on each person, and each cluster reports
  `nMoved` and `medianMoved` beside `n` and `median`, as it already does for
  `nDedup` and `medianDedup`.
- `medium_breakdown` computes each rank correlation three times: all rows, without
  repeats, and moved-only.
- `print_summary` prints the untouched share per level, so the number is in the
  build log every time.

In the report page:

- Untouched rows get a distinct mark. The pages already use hollow for repeats and a
  ring for verified experts; a square or a smaller dot keeps the three encodings
  apart. Legend and tooltip say which rule produced the flag.
- Each cluster strip shows a second median tick for moved-only when it differs from
  the overall by a point or more, the way dedup medians are shown now.
- The belief-chain figure gets a fourth line, quiz-takers who moved, beside the
  existing quiz-takers line.
- The delta strip carries the untouched share per level, so it is compared report
  to report.

## 4. Findings that need re-reading

Each of these appears in the 18 August, 1 September or 10 September report, and each
is at least partly the calibration reading itself back.

- **"Quiz-takers rate every link near-certain."** The quiz cohort's chain medians of
  90%, 88%, 89% against the pre-chooser cohort's 76%, 60%, 50% is the cube root. A
  proposed 70% becomes three factors at 89%. The pre-chooser cohort set each factor
  by hand. This is not a difference in belief about the chain; it is a difference
  in who set the sliders.
- **The vulnerability checklist correlation** (+0.66, +0.51, +0.41 across the three
  reports). On the medium quiz, the vulnerability share moves the proposed number
  upward within its band. For the 23 untouched rows the correlation is built in.
  It has to be recomputed on the 39 moved rows before it is called a finding.
- **"The least informed give the higher numbers."** The least informed are also the
  least likely to move a slider. Whether the pattern survives among movers is
  unknown.
- **The opinion questions "sorting" people by 36 points.** They set the band. The
  band table is what the figure shows.
- **The step at 15 of 16 vulnerabilities recognised.** Possibly a real threshold,
  possibly the point where the calibration reaches the top of the 86–100 band.
- **September's drop from 69% to 47%.** May be a change in belief, a change in
  audience, or a change in the share of visitors who moved a slider. The split
  answers which.
- **Verified experts at 31% against self-declared at 68%.** All 19 verified
  experts moved their sliders; 17 of 22 self-declared ones did, and the five who
  did not registered a median 77%. Among movers only, the gap is 31% against 44%:
  13 points, not 37. Some of the headline gap is the check selecting people who
  edit the number.

The findings that do not depend on the calibration: the double-submit fix working,
the check turning two people away, the level chooser shares, the identity results,
and the term-by-term decoy figure. Those stand.

## 5. What to say in the next report

State the mechanism in the masthead, once, in the same register as the
"unit is a submission, not a person" sentence: the quiz proposes a number, roughly
a third of visitors register it unchanged, and every figure is given with and
without them. Then let the split figures carry it. A report that discovered this
and buried it in a footnote would be the thing the exhibits' `limits` rule exists
to prevent.
