# Restructuring the quiz: retiring "Decide for me", gating the expert path

Date: 2026-08-19
Branch: `restructure-quiz`

## Problem

Two findings from `reports/submissions-2026-08-18.html` (164 submissions, 66 of them
after the level chooser launched on 9 Mar 2026):

1. **The recommended path is not taken.** "Decide the right level for me" is listed
   first and labelled recommended. It produced 1 of 66 post-launch submissions.
2. **Self-declared experts do not clear the expert bar.** Of the 62 submissions that
   declared a level outright, 31% went straight to expert — a claim nothing in the
   expert quiz checks. 7 of 19 expert-quiz submissions recognised neither of the two
   named research organisations.

The knowledge check is the only place in the calculator where an answer can be wrong,
and almost nobody sees it. Meanwhile the one path where a wrong answer would mean
something — expert — has no check at all.

## Design

### Path chooser

`decide` is removed from `quizFlows`. The welcome grid becomes Beginner, Medium,
Expert, plus the existing Sliders card.

- Beginner and Medium open their quiz directly. No change.
- Expert opens the knowledge check first. The Expert card says so on its face
  ("Knowledge check first · 30 terms") so the friction is not a surprise.

### The gate

The existing 30-term check ("Spot the AI-related terms, beware of the decoys" —
15 AI-related terms, 15 decoys) runs unchanged as the expert gate.

Scoring is unchanged: each of the 30 terms counts independently, a ticked AI term and
an unticked decoy both scoring one. Thresholds are unchanged from `levelJumpRules`:

| Score | Recommended level |
|---|---|
| 0–20 | beginner |
| 21–25 | medium |
| 26–30 | expert |

The thresholds are deliberately not retuned. Nothing in the data justifies a
particular number, and changing them now would make old and new gate scores
incomparable. Worth recording for later: ticking nothing scores 15/30, because all
15 decoys are then correctly left alone. The effective range is 15–30, not 0–30.

After scoring, the result screen shows the score and the per-term facts as it does
today, then offers:

| Score | Buttons |
|---|---|
| 26–30 | "Start expert quiz" |
| 21–25 | "Take medium quiz" (primary), "Continue to expert anyway" (secondary) |
| 0–20 | "Take beginner quiz" (primary), "Continue to expert anyway" (secondary) |

**The gate is advisory, not binding.** Anyone can continue to the expert quiz. The
consequence of failing is not exclusion, it is being recorded as a self-declared
expert rather than a verified one.

The gate no longer pre-sets the confidence sliders. It does today, but the level quiz
that follows overwrites both spread and midpoint immediately, so that calibration
never survives. The gate scores and routes; the quiz calibrates.

### Data recorded

Three new nullable columns on `submissions`:

| Column | Type | Meaning |
|---|---|---|
| `gate_score` | int | 0–30. Null if the gate never ran. |
| `gate_recommended_level` | text | `beginner`, `medium` or `expert`. Null if the gate never ran. |
| `expert_verified` | bool | True iff `gate_score >= 26`. Null if the gate never ran. |

`quiz_flow_id` keeps its current meaning: the quiz actually taken.

This makes three previously indistinguishable cases distinguishable:

- Verified expert: `quiz_flow_id = 'expert'`, `expert_verified = true`.
- Self-declared expert: `quiz_flow_id = 'expert'`, `expert_verified = false`.
- Successfully rerouted: `quiz_flow_id = 'beginner'`, `gate_score = 18`,
  `gate_recommended_level = 'beginner'`.

The third case answers a question the report could not: whether the check ever
redirects anyone. Gate fields stay attached to the submission even when the visitor
accepts a lower level.

`decide` disappears as a flow id going forward. Historical rows keep it and
`prepare_report_data.py` keeps reading them.

## Implementation notes

- `quizFlows`, `breadcrumbLabels`, `validHashes`, `getBreadcrumbItems`: drop `decide`,
  add an `expert-check` step that appears in the breadcrumb only on the expert path.
- `#decide` and `#expert` both route to the gate. No URL reaches the expert quiz
  without passing through it.
- `runKnowledgeCheck`: drop the `applyConfidenceCalibration` call; record the outcome
  in a module-level `gateState`.
- `renderLevelRecommendationButton`: render the one- or two-button result above.
- The submission insert gains the three new fields.
- The reset button and navigating back to Start clear `gateState`, so a stale score
  cannot attach to a later submission.
- `database.md` gains the migration SQL and the new column reference. The
  `ALTER TABLE` must be run by hand in the Supabase dashboard before the new fields
  reach the database.
- The HTML comment block at the top of `index.html` describes the old flow and is
  rewritten to match.

## Out of scope

- The sliders path is unchanged.
- The three level quizzes' own questions are unchanged. No decoys are seeded into
  them, and the expert quiz's reasoning questions — 19 of 19 submissions ticked all
  four self-improvement answers — stay uninformative. Both are separate work.
- `prepare_report_data.py` and the generated report are not updated. The new columns
  produce no data until submissions arrive.
