# Store the calibrated starting point with each submission

**Date:** 2026-09-12
**Scope:** A schema and page change so that every submission records what the page
proposed as well as what the visitor registered. Companion to
[splitting the reports into untouched and moved](2026-09-12-split-untouched-moved.md).
**Outcome:** Add one `calibration` column, filled by the page from the quiz result
and left outside the signed string like the other diagnostic columns. With it, the
gap between proposed and registered becomes a per-row number, and the reports can
stop inferring it from slider equality.

---

## 1. The problem

After a quiz, the page does not hand the visitor neutral sliders. It computes a
starting p(doom) and spread from the answers and sets all three factors to the cube
root of that number (`applyMidpointCalibration`, `applyConfidenceCalibration` in
`index.html`). The rules, in the three `compute*Midpoint` functions:

| Quiz | Band chosen by | Position within band |
|---|---|---|
| Beginner | gut-reaction answer: 20–40, 40–60, 60–80 | share of boxes ticked on the three lists |
| Medium | competition + speed + governance, seven bands from 0–14 to 86–100 | vulnerability share, system-prompt level, off-the-rails level |
| Expert | funding opinion, five bands from 0–20 to 80–100 | share ticked on the seven lists |

Spread runs from ±80 at no knowledge to ±20 at full knowledge on every quiz.

So more ticks means a higher starting number, and the opinion questions choose the
range. The submission table then stores only the final slider state. Nothing in a
row says where the sliders started, so nothing in the reports can separate "the
visitor believes 72%" from "the page proposed 72% and the visitor pressed submit".

The 10 September export shows the second case is common. Taking equal factor
midpoints as the sign of untouched sliders (only the calibration produces that):

| Quiz | Rows | Midpoints untouched | Median p(doom), untouched | Median, moved |
|---|---|---|---|---|
| Beginner | 46 | 22 (48%) | 72% | 44% |
| Medium | 62 | 23 (37%) | 92% | 36% |
| Expert | 41 | 5 (12%) | 77% | 42% |

Every recognition-versus-p(doom) finding in the three reports to date is partly
this mechanism reading itself back. That is the reason to store the starting point,
not to remove the calibration. Whether the quiz should set the midpoint at all is a
separate decision; this note only makes the effect measurable.

## 2. What to store

One new jsonb column, written by the page when a quiz completes and the sliders are
set:

```json
{
  "midpoint": 72.4,
  "spread": 38.0,
  "per_factor": 89.7,
  "flow": "beginner",
  "applied_at": "2026-09-12T20:14:03.118Z"
}
```

- `midpoint` and `spread` are the values `computeXMidpoint` and `computeXSpread`
  returned, in the page's 0–100 units.
- `per_factor` is the cube root the page actually set on each slider. Storing it
  saves the report from re-deriving it and pins the "N factors" assumption.
- `flow` repeats `quiz_flow_id`, so a calibration from one quiz followed by a
  submission from another (one visitor took beginner, then medium, on 8 September)
  is visible in the row.
- `applied_at` lets the report measure how long the visitor spent between being
  shown the number and registering one.

Nothing else is needed. The formula itself is pinned by `page_version`, which every
row has carried since 2 September, so the proposed values can be recomputed from
`quiz_answers` for any row that has both. Storing them anyway is cheaper than
porting three calibration functions to Python and keeping them in step, and it
survives a formula change without a migration.

## 3. Schema

```sql
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS calibration jsonb;
```

Run before deploying the page that sends it, for the same reason as `page_version`:
PostgREST refuses an insert that names an unknown column. Rows before the change
keep `NULL`, which the report must treat as "unknown", not "untouched".

No policy change. The column is diagnostic and a script can write anything into it;
it catches what the page did, not forgery.

## 4. Page

In `buildSubmissionPayload`, alongside `page_version`:

```js
// What the quiz proposed before the visitor touched anything. Diagnostic, so
// it stays outside the signed string like page_version and gate_answers.
calibration: latestCalibration
```

`latestCalibration` is set where the calibration is applied today, in the quiz
completion handler that calls `applyConfidenceCalibration` and
`applyMidpointCalibration`, and cleared with the path state. It is not restored
across a reload: neither is `latestQuizData`, and a submission from a reloaded tab
already carries no quiz, so a proposal without its quiz would be a lie.

Keep it out of `buildSignedPayloadString`. The signed line is deliberately a short
fixed-format string, and the identity design is that a row's numbers are what is
signed, not the page's advice. If the gap is ever worth signing, add a `c=` field
in a `pdoom/2` string rather than changing `pdoom/1`.

## 5. Report

`prepare_report_data.py` gains three things:

- `load_rows` emits `cal` (the proposed midpoint, 0–1), `gap` (registered minus
  proposed) and `mv`: true when any factor midpoint differs from `per_factor` by
  more than rounding. Rows carrying the column use it; older rows get the proposal
  recomputed from `quiz_answers` with a port of the page's tables
  (`calibration_for`), and the build prints how many kept rows fail to reproduce,
  which is the check that the port still matches the page.
- Every per-question figure reports the gap as well as the registered value. A
  question whose thirds differ in registered p(doom) but not in gap is a question
  the calibration answered.
- A new figure: proposed against registered, one dot per row, with the diagonal.
  Rows on the diagonal are the untouched ones. The distance from it is the only
  number in the dataset that is unambiguously the visitor's own contribution.

## 6. What this does not fix

- Rows before the column exists rely on the recomputation, which is exact for
  the midpoint but says nothing about rows where only the spread was moved. Those
  count as kept.
- A visitor who moves a slider and puts it back is indistinguishable from one who
  never moved it. That is fine; the registered number is theirs either way.
- Storing the proposal does not stop the proposal from anchoring the visitor. A
  visitor who moves the slider from 72% to 60% may have arrived at 60% only because
  72% was in front of them. Measuring the gap is the precondition for deciding
  whether to keep the mechanism, not a substitute for the decision.
