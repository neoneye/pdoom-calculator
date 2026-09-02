# Post-submit survey: who submits?

**Date:** 2026-09-02
**Scope:** A proposal for asking visitors a short psychological survey after they register a
prediction, prompted by a psychologist's curiosity about who submits and by the
[DMIDI survey battery](https://neoneye.github.io/vibe-coding-lab/dmidi-survey/index.html)
prototype.
**Outcome:** The full battery (15 scales, roughly 250 items) is too much to ask. A ten-item
survey, offered after submission and stored in its own table, costs the visitor under a
minute and the dataset nothing. It needs about a year of collection before it can say anything.

---

## 1. Why the battery does not fit

The calculator asks four to eight quiz questions and three slider settings. The September
report shows visitors already double-submit out of impatience (six confirmed repeat rows in
two weeks), and the quiz answers themselves correlate with p(doom) at close to nothing on
cohorts of 26 to 39. Adding a research battery in front of the sliders would:

- cut completions on the thing the site exists to measure;
- produce far fewer survey completions than started surveys, biasing the sample toward the
  most patient visitors;
- collect scales nobody has a hypothesis for.

The fix is not a shorter battery. It is a survey chosen by hypothesis, placed where it cannot
cost a submission.

## 2. Pick scales by hypothesis

The question to put to the psychologist is: **what do you expect to differ between someone
who submits 5% and someone who submits 90%?** Three constructs from the battery bear on a
long-horizon catastrophe estimate, and each has a validated short form.

| Construct | Why it bears on p(doom) | Short form | Items |
|---|---|---|---|
| Consideration of Future Consequences (Strathman et al., 1994) | p(doom) is a judgement about distant outcomes; the scale measures how much distant outcomes weigh against immediate ones | The two subscales, CFC-Future and CFC-Immediate, using the highest-loading items of each | 4–6 |
| General risk attitude | Whether a high estimate goes with risk aversion or with comfort around risk | The single SOEP item, "How willing are you to take risks in general?", 0–10 (Dohmen et al., 2011). Validated against real behaviour; no scale needed | 1 |
| Need for Cognition (Cacioppo & Petty, 1982) | Whether the visitor reasoned through the chain or dragged the sliders; also a check on how seriously the quiz was taken | NCS-6 (Lins de Holanda Coelho, Hanel & Wolf, 2020) | 6 |

That is 11 to 13 items, one minute. If the psychologist wants personality breadth instead of
these three, the Ten-Item Personality Inventory (Gosling, Rentfrow & Swann, 2003) covers the
Big Five in ten items; Openness is the trait most likely to matter here. Do not run both.

The item text for every scale above is already on the DMIDI page, with its citation and
scoring rule. This document deliberately does not reproduce it.

Two scales in the battery are worth ruling out explicitly. **Social desirability** measures
impression management toward a person, and there is no person here. **Decision outcomes** is
a life-history inventory that is both long and intrusive for an anonymous visitor.

## 3. Where it goes

**After the submission, on the same card as the exhibits.** The page already shows the
exhibits once a prediction is registered (`renderExhibits` in `index.html`). The survey card
sits below them. By then the prediction is stored, so a visitor who closes the tab costs the
main dataset nothing, and the sample of survey-takers is "people who submitted", which is the
population the psychologist asked about.

Proposed copy, short enough to read in full:

> **One minute for a psychologist.** A friend who studies decision-making is curious who
> registers a prediction here. Ten quick questions, anonymous, optional. Your prediction is
> already saved either way.

Then the items, then one button: **Send answers**. No progress bar, no per-item validation, no
"are you sure" on leaving. A visitor who answers half and leaves sends nothing; partial
scales are not scoreable and a half-filled row is a cleaning problem later.

The card is shown once per browser per submission, keyed by the visitor identity the page
already keeps, and not shown again on a repeat submission from the same browser within the
same session.

## 4. Storage

A separate table, joined to submissions by visitor key. Keeping it out of `submissions`
means an unanswered survey leaves the submissions table untouched, the report's existing
queries do not change, and the two datasets can be published or withheld independently.

```sql
CREATE TABLE survey_responses (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  submitted_at timestamptz NOT NULL DEFAULT now(),
  visitor_key text,             -- joins to submissions.visitor_key; null if the browser has no key
  submit_count int,             -- which of that browser's submissions this followed
  survey_id text NOT NULL,      -- e.g. 'cfc-risk-ncs-v1'; a new set of items gets a new id
  answers jsonb NOT NULL,       -- [{item_id, value}], raw, unscored
  page_version text
);
GRANT INSERT ON survey_responses TO anon;
ALTER TABLE survey_responses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow anonymous survey inserts" ON survey_responses
  FOR INSERT TO anon WITH CHECK (survey_id IS NOT NULL);
```

Three deliberate choices:

- **Raw answers, not scores.** Scoring rules change (the CFC subscales were re-analysed after
  publication); storing item-level values means the report can rescore.
- **No SELECT grant for `anon`.** Unlike `submissions`, there is no public stats page that
  needs to read this table. Survey answers are read only by the report build, with a service
  key, and published only in aggregate.
- **`survey_id` versions the item set** the same way `page_version` versions the page. When
  an item is swapped, the id changes and old rows keep their meaning.

Signing: the row carries the visitor key so it can be joined, but it is not covered by the
submission signature. Extending the signed string would change the `pdoom/1` format and the
verifier for no gain; a forged survey row is not a threat worth a format bump.

## 5. Consent and what to say

The calculator is anonymous and the survey should stay that way. The card says what the
answers are for and who wants them. Do not add a name or email field; the moment there is a
way to identify a respondent the survey becomes something that needs a proper consent
procedure. If the psychologist intends to publish, they need their own ethics process; the
site's job is to state plainly, on the card, that answers are anonymous, optional, and may be
published in aggregate.

## 6. What to expect from it

Set expectations before building it.

| Quantity | Estimate | Basis |
|---|---|---|
| Submissions per month | 40–60 | Aug 2026 had 62, the busiest month; most months are under 20 |
| Survey uptake | 10–20% | Typical for an optional post-task survey with no incentive |
| Survey rows per month | 5–12 | The two above |
| n needed to detect r = 0.3 at 80% power | ~85 | Standard two-sided test at α = 0.05 |
| Time to that n | 8–17 months | Rows per month above |

So this is a year of collection before there is a result, and the result will be one
correlation per scale on under a hundred people. That is fine if it is understood up front. It
is not fine if the plan is a 250-item battery that yields four completions.

The site's own quiz is the caution here: 26 to 39 answers per cohort, and nothing in them
predicts p(doom) except the vulnerability checklist, at ρ ≈ +0.5. Three short scales that run
for a year will beat a full battery that nobody finishes.

## 7. Report integration

When there are rows, `prepare_report_data.py` gets one more section:

- join `survey_responses` to `submissions` on `(visitor_key, submit_count)`;
- score each scale with its published rule, from the raw items;
- report each scale's rank correlation with p(doom), with the same permutation p-value and
  leave-one-out treatment the medium quiz gets;
- report uptake: rows offered (submissions since launch) against rows answered, so the
  self-selection of survey-takers is visible rather than hidden.

The scales' medians should also be compared with their published norms, because the first
finding will almost certainly be that people who register a p(doom) are not a general
population, and that is worth knowing before reading any correlation.

## 8. Open questions for the psychologist

1. Which of the three constructs is the actual hypothesis? One scale is better than three.
2. Is the interest in the estimate, or in the uncertainty band? The p10–p90 width is arguably
   the more psychological quantity, and nobody has looked at it yet.
3. Would a single free-text question ("What made you pick that number?") be more useful than
   any scale? It is one item, and the answers are readable.
4. Is there a norm sample for the chosen scale that this population can be compared against?
