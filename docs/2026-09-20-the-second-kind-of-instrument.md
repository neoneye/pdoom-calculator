# The second kind of instrument, and where to take it

**Date:** 2026-09-20
**Scope:** What the calculator is as an instrument, stated against the surveys
in [the literature note](2026-09-13-pdoom-literature.md) and
[ESPAI 2024](2026-09-15-espai-2024.md), and a reflection on the directions
that would take it further: accounts, public profiles, re-estimation over time,
cohort links, randomised variants, and reasons per link. Follows
[what the calculator is](2026-09-13-what-the-calculator-is.md) and
[the 19 September report](../reports/submissions-2026-09-19.html).
**Outcome:** A survey asks a describable population for a number. The calculator
records how each visitor arrived at theirs: which link they doubt, what they
were shown, and what they changed. In the reviewed literature nothing combines
those, and one paper says the per-link inputs had never been collected. The
next level is not a bigger sample. It is turning the per-visitor record into a
per-person record over time, without giving up the anonymity that got the rows.
Accounts can do that if they are optional and built on the keys the site already
has. Public profiles would change what is being measured, and should be tried
last, with the private number kept apart from the public one.

---

## 1. Two kinds of instrument

The first kind asks a population it can describe for a single probability.
That is every survey in the literature note: 1,580 published researchers, 89
superforecasters and 80 experts, 111 experts, 89 attendees. The output is a
distribution over people. The method's strength is the sample; its blindness is
that it learns nothing about how any one respondent reached their number.

The second kind records the reaching. The calculator has four properties that,
together, make it that kind:

1. **Per-link elicitation from the public.** Carlsmith decomposed the risk into
   six steps and assigned every probability himself. Growiec and Prettner wrote
   a four-step chain and stated that its inputs had never been elicited. The
   site has been eliciting three of them from visitors for a year.
2. **A record of what each respondent was shown.** ESPAI randomises wording and
   measures the effect between arms, which is the right method and tells you
   wording matters. It cannot say what row 143 saw. Each submission here stores
   the quiz answers, the proposed number, the check result and the page version.
3. **A record of what they changed.** Kept or moved, by how much, in which
   direction, per row. Kestin and Soares came closest with before-and-after, but
   their "before" was the person's own earlier answer, not a number the
   instrument put in front of them.
4. **Continuous collection with a signed identity.** The surveys are a fortnight
   in December. The site is a year of days, and since August each browser signs
   its rows.

Pieces of this exist elsewhere: forecasting platforms let individuals decompose
questions, Field paired a number with a familiarity questionnaire, the
persuasion tournament recorded updates over months. The combination, and
especially the third property, an instrument that hands the respondent a number
and then measures its own hand, is what the reviewed literature does not have.
The claim is that narrow. Nobody has checked the world.

## 2. What the combination has bought so far

- **The instrument caught its own error.** Three reports said recognition tracks
  p(doom). The fourth could check, per row, whether that was belief or the
  formula, and it was the formula. A survey that primes can estimate its
  priming between arms; this one subtracts it within each row.
- **A disagreement with a location.** Verified experts at 31% against ESPAI's
  10% is a gap of unknown shape. The chain gives it one: 95 / 80 / 50. Their
  whole moderation is on the last link, the one where the site's evidence is
  thinnest.
- **A within-person test of anchoring.** Five browsers took two quizzes, were
  proposed two different numbers, and landed on their own number both times,
  twice moving a proposal *up* to get there. Under pure anchoring the second
  number sits near the second proposal. Five people is a hint, but a hint no
  survey can produce, because a survey never hands one respondent two anchors.

## 3. What it lacks

A population. Three hundred visitors that nobody can describe, reached by
whatever links the site has, in a reception that
[turned around August](2026-09-20-reception-and-the-numbers.md). No per-row
record fixes that. Every level on this site should be quoted with its sample
described; the shapes are what to stand behind.

And a time axis per person. The retake finding is the most interesting thing in
the export and it rests on five accidental repeats. The site was not built to
watch a person's chain move; it was built to collect one chain per visit.

## 4. Directions

Ordered by what I think they buy against what they cost. The principle
throughout is the one the identity design already follows: nothing may cost a
submission, and anonymity stays the default.

### 4.1 Re-estimation over time, on the keys the site already has

The cheapest version of accounts is no account. A browser already holds a
signing key; the site can recognise it on return and offer, not require, a
re-estimate: "You registered 34% on 9 September. Set it again, without looking."
Store both, linked by the key. That turns the five accidental retakes into a
designed measurement: how a person's chain moves over weeks, which link moves
when the news does, and whether a second visit reproduces the first number or
the first proposal.

What it costs: nothing in anonymity, since the key is already there, and one
screen for returning visitors. What it needs: the referrer column from the
report's directions, so a return can be told from a new arrival by the same
person on another device.

### 4.2 Accounts, optional, built on the key

An account is a key that survives the browser. The honest way to add one is to
let a visitor *claim* their existing key with an email or a passkey, so their
rows on this device and their rows on the next one are one series. Nothing
about the anonymous path changes; the row still carries a key, and the account
is a table that says which keys are one person, readable only by the site.

What it buys beyond 4.1: multi-device continuity, and the ability to ask a
person something later, a follow-up question, a re-estimate by email. That is
the machinery for a panel, which is what a longitudinal study of belief needs
and what no survey in the note has.

What it costs: friction at the point where a submission could be lost, and a
sample that tilts further toward people who care. Both are manageable if the
account is offered *after* the submission is stored, the way the post-submit
survey proposal places its questions, and never on the path to the button.

What not to do: require it. The day an account is needed to submit, the site
loses the crowd that gave it its low tail and its retakes, and becomes a club.

### 4.3 Public profiles, by choice

The idea is that a visitor can publish their chain, and perhaps a line of
reasoning per link, under a name. It is attractive for two reasons: it makes
the site a place where positions are held rather than numbers dropped, and it
lets readers see chains beside each other, which is the whole point of a chain.

It is also the direction most likely to change what is being measured. A number
set in private and a number set for an audience are different numbers; the
surveys' care over anonymity exists because of that. The site's own history
says the audience was hostile until August. A public chain invites the
"doomer" comment onto the row itself.

If it is done, the design that keeps the instrument honest is: the private
number is the one the reports use, the public one is a second column set
afterwards, and the report measures the gap between them. That gap would itself
be a finding, the size of social pressure on a stated p(doom), and no survey
has it. Publishing reasons is more valuable than publishing numbers: a sentence
on why the third link is 50% is worth more than the 50%.

Try this last, after 4.1 and 4.2 have shown whether people return at all.

### 4.4 Cohort links

Half of what a survey has and the site does not is a describable population.
A cohort link, `?cohort=ml-course-autumn-2026`, tags every submission that
arrives through it. A lecturer, a lab, a reading group, a newsletter can hand
out a link and the report can describe that cohort: who they are, what they
were told, when. This gives the survey's strength on the site's instrument at
the cost of one column, and it is the same column as the referrer, used with
intent instead of read after the fact.

### 4.5 Randomised variants

Every quiz change so far has been read as before-and-after, and the reviews
were right that this cannot separate the change from the audience. The site
already randomises nothing and could randomise anything: show the proposed
number to half the visitors and neutral sliders to the other half; put the
catastrophe question in front of half the expert-quiz takers. With the
per-row record, the effect is measured on the same page in the same week. This
is the single change that would let the reports say "because" and mean it.

### 4.6 Reasons per link

The chain says where a person's doubt sits. It does not say why. One optional
free-text field per link, after submission, would give the site the thing the
literature has only from its authors: a lay account of why the third link is
small. Fifty of those from verified experts would be worth more than any median
on the page, and they are the raw material a public profile would eventually
show.

### 4.7 Evidence for and against

Lohn's two questions, how strong is the evidence for this link and how strong
against, would turn the uncertainty band from a number the quiz assigns into
one the visitor states. The 19 September report found that 19 of 20 kept rows
changed the band, so visitors do reach for it. Giving it a meaning they can
answer is a small change to the page and a large one to what the band means.

## 5. In one paragraph

The calculator is the instrument the surveys are not: it records how a number
was reached, per link, per visitor, including what the page itself did to it.
Its weakness is that it does not know who its visitors are or whether they
come back. The next level is a record per person over time, and the way to get
there without losing the crowd is to build on the keys the site already issues:
recognise returns, offer re-estimation, let a key be claimed into an account
after the row is safe, tag cohorts by link, and randomise the changes that are
meant to be measured. Public profiles come after that, with the private number
kept as the one that counts and the gap to the public one measured as a finding
of its own.
