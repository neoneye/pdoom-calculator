# Open items, in order

**Date:** 2026-09-20
**Scope:** Everything the notes and reports have recommended and nothing has
acted on, gathered in one place and put in the order worth doing them. Each item
links to the note that specifies it. Follows
[the second kind of instrument](2026-09-20-the-second-kind-of-instrument.md)
and [the 19 September report](../reports/submissions-2026-09-19.html).
**Outcome:** Six items are worth doing soon, in this order: the stats page,
a referrer column, randomising the proposal, decoys, the About page, and a
one-line copy fix. Four sit behind them. One is deliberately parked.

When an item ships, strike it here and say where.

---

## 1. Do soon

### 1.1 The stats page: stop averaging the page's number with the visitors'

`/stats/` is the page most visitors see and it leads with "Average P(doom)", a
mean of every submission's midpoint. Roughly a third of quiz submissions are
the quiz's own proposal registered unmoved, so that mean averages the page's
arithmetic in with people's beliefs, which is the error the September reports
were built to expose.

- **Do:** replace the headline card with the median of the moved rows and the
  share that kept the proposal; draw the histogram as two series; give the
  factor table a moved-only column. Identical repeat rows from one browser
  count once.
- **Specified in:** [stats page: kept and moved](2026-09-13-stats-page-kept-and-moved.md).
- **Cost:** JavaScript in `stats/index.html` only; the columns are already
  fetched. The classification rule is the one in `prepare_report_data.py`.
- **Mocked, 20 September:** [mockups/stats-kept-moved.html](mockups/stats-kept-moved.html)
  shows the three cards, a stacked histogram with a toggle between "whose
  number it is" (set their own / kept / pre-quiz) and "which quiz"
  (beginner / medium / expert / none), and the median table. The author's
  verdict: the cards and the table are right; the stacked histogram is not.
  Stacked bars do not read well as a histogram, and the stats page should not
  overwhelm a visitor into leaving. Keep the histogram a single series, and
  let the curious find the split in the reports. The mock is kept for the
  cards, the sentence under them, and the table.

### 1.2 Record where each visitor came from

August's submissions arrived in three bursts with medians of 70%, 95% and 33%;
September's are steadier and lower. Each burst looks like one link posted in
one place, and the table cannot say which. Without this column, "the reception
changed", "the news changed" and "the page changed" are indistinguishable.

- **Do:** store `document.referrer`, and a `?cohort=` tag when the URL carries
  one, as a diagnostic column outside the signed string, like `page_version`.
  `ALTER TABLE` first, then the page, then `scripts/export_submissions.py` and
  the stats page's export list.
- **Specified in:** [reception and the numbers](2026-09-20-reception-and-the-numbers.md),
  section 4; cohort links in [the second kind of instrument](2026-09-20-the-second-kind-of-instrument.md), 4.4.
- **Cost:** an afternoon.

### 1.3 Randomise the proposal

Every finding about the proposed number is with-and-without on the same
people, which two reviews correctly called a subgroup comparison, not a cause.
Showing neutral sliders to a random half of quiz-takers, with the assignment
stored in the row, is the one change that lets a report say "because".

- **Do:** a coin flip at quiz completion; half get the calibration, half get
  50/50/50 with the proposal stored but not applied. Store the arm. The
  report compares arms on the same page in the same weeks.
- **Specified in:** [the second kind of instrument](2026-09-20-the-second-kind-of-instrument.md), 4.5;
  the 19 September report's directions.
- **Cost:** medium. Once it exists, every later quiz change can be tested the
  same way instead of read as before-and-after.

### 1.4 Decoys in the beginner and medium lists

Open since August, and every report since has strengthened the case: the
beginner catastrophe list is ticked 60 of 62 on its top answers, and a list
that can only be answered correctly measures willingness to tick.

- **Do:** three or four fabricated but plausible entries per list, scored as
  hits minus tripped, both stored. Split the report at the launch date via
  `page_version`, as the check already does.
- **Specified in:** [beginner quiz saturation](2026-09-10-beginner-quiz-saturation.md).
- **Cost:** writing the decoys is the hard part; the scoring exists for the
  check.

### 1.5 An About page that explains the chain

The About page is a reading list. A first-time visitor reaches three sliders
with no account of why there are three.

- **Do:** one page saying: why a chain (Carlsmith), that the product is small
  only if a link is and each link is a strategy, the reference number (ESPAI
  2024: median 10%, mean 18%, with the caveat that the site asks a wider
  question), what "global catastrophe" covers here, that the chain assumes a
  single system, and what the site means by an expert.
- **Specified in:** [what the calculator is](2026-09-13-what-the-calculator-is.md), section 4;
  [the literature](2026-09-13-pdoom-literature.md), section 4;
  [where the zero goes](2026-09-13-where-the-zero-goes.md), section 4;
  [ESPAI 2024](2026-09-15-espai-2024.md); [definitions](definitions.md).
- **Cost:** writing.

### 1.6 One line of copy

The second slider is labelled "dangerous behavior" and explained as
"misaligned with human values", which are two different claims. The reports
use the label. The explanation in `index.html` should say what the label says:
given powerful AI, the chance it behaves dangerously, whether from misalignment
or from doing what someone asked.

- **Noted in:** [making the safety argument explicit](2026-09-14-making-the-safety-argument-explicit.md),
  section 5 (the only part of that draft to keep).
- **Cost:** five minutes.

## 2. Behind those

- **Re-estimation for returning keys.** Recognise a browser's key on return and
  offer "set it again without looking", storing both. Turns the five accidental
  retakes into a designed measurement. [Second kind](2026-09-20-the-second-kind-of-instrument.md), 4.1.
- **Reasons per link.** One optional free-text field per link, after
  submission. [Second kind](2026-09-20-the-second-kind-of-instrument.md), 4.6.
- **One theory exhibit per link.** Turner or Ngo for the second link, Kovarik
  as a stated limit for the third. [The literature](2026-09-13-pdoom-literature.md), section 4.
- **The post-submit survey.** Eleven to thirteen items chosen by hypothesis,
  after the button, in their own table. [Post-submit survey](2026-09-02-post-submit-survey.md).
- **Read option denominators from `page_version`.** `OPTION_ADDED` in
  `prepare_report_data.py` is still a hand-kept table of dates; the check's
  term list already resolves by version and the quiz options should too.
- **A Google sandbox-escape exhibit**, if a public source exists. The author
  mentioned it on 20 September; nothing is on file.

## 3. Parked

- **The 14 September safety-argument draft.** The author judged it wrong for
  the site: too much mathematics and too many disclaimers for visitors who can
  answer a quiz but do not know the parameters. Nothing since has changed that.
  Its one salvageable line is item 1.6.
- **Public profiles.** Attractive, and the direction most likely to change what
  is measured. After accounts, if at all, with the private number kept as the
  one that counts. [Second kind](2026-09-20-the-second-kind-of-instrument.md), 4.3.
