# The p(doom) literature, and the calculator beside it

**Date:** 2026-09-13
**Scope:** Fifteen papers and reports that estimate, decompose, argue for, or
criticise P(doom), each with its method and its arithmetic where it has any, and
what each says to this site's design. The list is Codex's, with one addition
(Kestin and Soares) and the definitional caveat it opened with. Follows
[the calculator against The Economics of p(doom)](2026-09-13-economics-of-pdoom.md)
and [where the zero goes](2026-09-13-where-the-zero-goes.md).
**Outcome:** Four of the papers build a chain and the calculator's is the shortest.
The survival-story taxonomy is the formal version of "each link is a strategy", and
Dung's objection to it, that a world of many AI systems is a survival route, is one
the three sliders cannot express. The calculator's sample is the weakest in the
list and its per-respondent record the richest. Its numbers line up with the
literature where definitions allow, and the one published before-and-after study
shows the calculator's kept-and-moved result from a different instrument.

---

## 0. Read the question before the number

"P(doom)" is not one quantity. Across this list it is human extinction, or
permanent disempowerment, or existential catastrophe, or any global catastrophe;
by 2100, or by 2070, or with no horizon; unconditional, or conditional on advanced
AI existing. The calculator asks for "a global catastrophe", with no date, and its
beginner quiz lists collapse and s-risks under that heading. That is the broadest
definition in the set, so its numbers should run higher than everyone else's before
any other difference is considered, and they do. Every comparison below is made
with that in mind.

## 1. Summary

| Source | Kind | Population | What it measures | Headline |
|---|---|---|---|---|
| Carlsmith 2022 | decomposition | one author | existential catastrophe by 2070 via power-seeking AI | ~5%, later >10% |
| Grace et al. 2024 | survey | 2,778 AI authors | extinction or severe disempowerment | median 5%, mean ~16% |
| Karger et al. 2025 | forecasting tournament | 89 superforecasters, 80 experts | extinction by 2100 | 0.4% vs 3%, no convergence |
| Field 2025 | survey | 111 AI experts | p(doom) plus familiarity | two camps; exposure explains part |
| Kestin & Soares 2026 | before/after | 89 event attendees | extinction or severe disempowerment | 50% → 70%; newcomers up, experts not |
| Cappelen et al. 2025 | taxonomy | — | survival routes | four stories, each negates a premise |
| Dung 2025 (PhAI) | method | — | bounds on p(doom) | survival stories give an upper bound |
| Dung 2025 (AI & Society) | argument | — | disempowerment by 2100 | premise-by-premise case |
| Lohn 2026 | method | — | uncertainty without probability | belief and plausibility intervals |
| Growiec & Prettner 2026 | economic model | — | extinction, four-step chain | tolerable risk near 0.001% |
| Turner et al. 2021 | theorem | — | power-seeking in optimal policies | formal, not empirical |
| Cohen, Hutter & Osborne 2022 | argument | — | reward intervention | formal, "catastrophic" |
| Ngo, Chan & Mindermann 2024 | mechanism | — | alignment failure in deep learning | goal misgeneralisation, deception |
| Hendrycks et al. 2023 | taxonomy | — | catastrophic risks | four categories |
| Kovarik et al. 2024 | epistemics | — | testability of extinction hypotheses | may be invisible to science |
| **Calculator** | **instrument** | **253 anonymous visitors** | **global catastrophe, no horizon** | **15% pre-quiz; 31–48% moved; 72–92% kept** |

## 2. The papers

### Carlsmith (2022), Is Power-Seeking AI an Existential Risk?
[arXiv:2206.13353](https://arxiv.org/abs/2206.13353)

**Method.** A six-step conditional chain, each step given a subjective probability
and the product taken. By 2070: (1) it will be possible and financially feasible to
build advanced, planning, strategically aware systems, 65%; (2) there will be strong
incentives to build them, 80%; (3) it will be much harder to build aligned than
misaligned ones, 40%; (4) misaligned ones will be deployed in high-impact settings,
65%; (5) they will disempower humanity, 40%; (6) that disempowerment will be an
existential catastrophe, 95%. Product about 5%. The author later revised his view
upward to more than 10%.

**Its arithmetic is the calculator's.** Multiply conditionals. The calculator's
first link covers his (1) and (2), its second his (3), (4) and (5), its third his
(6). Carlsmith puts most of the uncertainty in the middle, on alignment difficulty
and on whether misaligned systems actually disempower; the calculator's visitors who
cleared the check put theirs at the end, on whether disempowerment becomes
catastrophe, which is the step Carlsmith rates near-certain. That is a genuine
disagreement in structure, not just in numbers.

**To the calculator.** This is the paper that explains why there is a chain, and
the About page should cite it as such. It is also the argument for more links: his
six separate things the calculator's second slider blurs together.

### Grace et al. (2024), Thousands of AI Authors on the Future of AI
[arXiv:2401.02843](https://arxiv.org/abs/2401.02843)

**Method.** Survey of 2,778 researchers who had published at top AI venues, with
several differently framed questions about extinction or permanent, severe
disempowerment, answered as free-form probabilities.

**Its arithmetic.** None beyond the summary statistics, and the summary statistics
are the finding: median 5%, mean about 16%, with between a third and a half of
respondents at 10% or more depending on framing. A mean three times the median is
a long right tail, and the tail is where the disagreement lives.

**To the calculator.** The reference number. The pre-chooser cohort's 15% is in
range once "catastrophe" is allowed to be broader than extinction. Grace's framing
sensitivity, the same population giving different medians to differently worded
questions, is a warning the calculator's single wording has not had to face.

### Karger et al. (2025), Subjective-Probability Forecasts of Existential Risk
[International Journal of Forecasting](https://doi.org/10.1016/j.ijforecast.2024.11.008)

**Method.** The Existential Risk Persuasion Tournament: 89 superforecasters and 80
subject-matter experts forecast catastrophic and extinction risks by 2100, then
spent months exchanging arguments and updating, with incentives for accuracy and
for persuading the other group.

**Its arithmetic.** For AI-caused extinction by 2100, superforecasters landed near
0.4% and experts near 3%, and neither group moved the other. Disagreement survived
sustained argument between people paid to resolve it.

**To the calculator.** The strongest available evidence that informed people do
not converge, and the natural comparison for the check-clearers' 31%. An order of
magnitude separates them from the tournament's experts; definition covers some of
it and not all. It is also the caution against reading the calculator's cohort
medians as anything but where a self-selected group happens to sit.

### Field (2025), Why do Experts Disagree on Existential Risk and P(doom)?
[arXiv:2502.14870](https://arxiv.org/abs/2502.14870)

**Method.** 111 AI experts surveyed on their p(doom), their familiarity with AI
safety concepts, their objections, and their reactions to safety arguments.

**Its arithmetic.** Correlational. Familiarity with the concepts explains part of
the variance in p(doom); the population splits into a camp that sees AI as a
controllable tool and one that sees it as an uncontrollable agent.

**To the calculator.** This is the calculator's design run as a survey: a
familiarity measure beside a number. The site's version has two things Field's
does not, a check with decoys that can turn people away, and a record of which
boxes each person ticked. And the site's data answers back: the people who cleared
the check are in neither of Field's camps. Their chain accepts arrival and
takeover-grade behaviour and discounts only the end, a position best called
*uncontrollable but survivable*.

### Kestin and Soares (2026), Views on AI Existential Risk Before and After a Public Event
[arXiv:2603.27785](https://arxiv.org/abs/2603.27785)

**Method.** Identical surveys before and after a talk, conversation and Q&A at
Harvard built around *If Anyone Builds It, Everyone Dies*, 89 matched participants.
One of the authors co-wrote the book, which the paper states.

**Its arithmetic.** Median 50% before, 70% after. Among attendees with little prior
familiarity, 60% shifted upward and none downward; among self-described experts,
none shifted upward and 20% shifted downward.

**To the calculator.** This is the kept-and-moved finding from a different
instrument. Newcomers take the number they are given; people who know the field
move it down or not at all. Their 70% after the talk and the calculator's kept rows
at 72–92% are the same phenomenon: a number handed to someone who did not have
one. Any future About page that cites this should also say who wrote it.

### Cappelen, Goldstein and Hawthorne (2025), AI Survival Stories
[Philosophy of AI](https://doi.org/10.18716/ojs/phai/2025.2801)

**Method.** Doom requires two premises: AI becomes extremely powerful, and
extremely powerful AI destroys humanity. Humanity survives if either fails, and the
paper enumerates the ways: scientific barriers stop the power; research bans stop
it; the powerful systems have compatible goals; or dangerous systems are detected
and disabled before harm. P(doom) is then one minus the combined weight of the
survival stories, each of which faces its own difficulties.

**Its arithmetic.** Complement rather than product. Where Carlsmith multiplies
steps toward doom, this paper adds up routes to survival and takes what is left.
The two are the same calculation from opposite ends, and each is honest about a
different thing: the chain about what has to go wrong, the stories about what has
to go right.

**To the calculator.** It is the formal version of the table in
[where the zero goes](2026-09-13-where-the-zero-goes.md). Barriers and bans are
the first link at zero; aligned goals the second; detection and disabling the
third. The site's data on which link visitors zero, second and third but almost
never first, is a finding about which survival story the visitors believe.

### Dung (2025), Estimating the Probability of AI Existential Catastrophe
[Philosophy of AI](https://doi.org/10.18716/ojs/phai/2025.2854)

**Method.** A critique of the survival-story method and a proposal to combine it
with the chain method.

**Its arithmetic.** The survival-story enumeration misses stories, in particular
the multipolar one, where many superhuman systems exist and none dominates, so its
estimate is an upper bound on doom. The chain method, which can only count the
routes to doom it names, gives a lower bound. The truth is between them.

**To the calculator.** Two things. The bounds argument says the calculator's chain,
being a chain, is a lower-bound instrument by construction, and its visitors'
numbers should be read that way. And the multipolar story is a survival route the
three sliders cannot express: they treat "AI" as one system whose dangerous
behaviour either escalates or is contained. A world of many systems checking each
other has no slider.

### Dung (2025), The Argument for Near-Term Human Disempowerment Through AI
[AI & Society](https://doi.org/10.1007/s00146-024-01930-2)

**Method.** An explicit premise-by-premise argument that AI is likely to
permanently disempower humanity by 2100, each premise defended and the inference
made valid.

**Its arithmetic.** Logical rather than numerical: the conclusion follows if the
premises hold, and the paper's work is defending the premises.

**To the calculator.** The premises are the calculator's links stated as claims,
and a visitor who wants to know what setting a slider low commits them to denying
can read it there.

### Lohn (2026), Beyond P(doom) for AI Risk
[CSET](https://cset.georgetown.edu/publication/beyond-pdoom-for-ai-risk-quantifying-uncertainty-without-probability/)

**Method.** Argues that a single probability is the wrong output when ignorance,
not randomness, dominates, and proposes Dempster–Shafer belief and plausibility
intervals instead.

**Its arithmetic.** Ask two questions besides the probability: how strong is the
evidence for the outcome, and how strong the evidence against. Belief is the first,
plausibility one minus the second, and the gap between them is ignorance. "Without
ignorance, Belief and Plausibility become the same number, equal to probability."

**To the calculator.** The site half-answers this already. It refuses a point: every
slider carries a ± band and the reports show the p10–p90 range. But the band is a
spread around a belief, not Lohn's evidence-for and evidence-against pair, and the
quiz sets it from knowledge rather than eliciting it. Of everything in the list,
the calculator is the instrument closest to Lohn's proposal, and one step short of
it.

### Growiec and Prettner (2026), The Economics of P(doom)
[Economic Modelling](https://doi.org/10.1016/j.econmod.2026.107718); covered in
[its own note](2026-09-13-economics-of-pdoom.md)

**Its arithmetic.** p(doom) = p₁p₂p₃ + p₁p₂(1−p₃)p₄, arrival, takeover, misaligned,
non-corrigible; then an iso-elastic welfare function under which the tolerable
misalignment probability comes out near 0.001%.

**To the calculator.** The chain one link longer, and the argument that the size
of the third link hardly matters for policy, since almost any nonzero value
justifies more safety work than exists.

### Turner, Smith, Shah, Critch and Tadepalli (2021), Optimal Policies Tend to Seek Power
[NeurIPS](https://papers.nips.cc/paper/2021/hash/c26820b8a4c1b3c2aa868d6d57e14a79-Abstract.html)

**Its arithmetic.** A theorem about Markov decision processes: for most reward
functions, under environmental symmetries, optimal policies prefer states that keep
more options open, which is a formal definition of power. It says nothing about
the probability of any real system doing this.

**To the calculator.** The theoretical floor under the second link. The site has
incidents for that link and no theory; this is the theory.

### Cohen, Hutter and Osborne (2022), Advanced Artificial Agents Intervene in the Provision of Reward
[AI Magazine](https://doi.org/10.1002/aaai.12064)

**Its arithmetic.** An argument, under stated assumptions, that a sufficiently
capable agent maximising a learned reward will act to control the source of that
reward, and that the consequences of it succeeding would be catastrophic.

**To the calculator.** The quiz's "reward hacking" term on the expert check and its
"rewrite itself" option are this paper's mechanism, unsourced. This is the source.

### Ngo, Chan and Mindermann (2024), The Alignment Problem from a Deep Learning Perspective
[ICLR](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1e58b1bf9f218fcd19e4539e982752a5-Abstract-Conference.html)

**Its arithmetic.** None; it is a mechanism paper. It connects present training
methods to situational awareness, goal misgeneralisation, deceptive alignment and
power-seeking, and argues the path from here to there needs no new paradigm.

**To the calculator.** The second link's mechanism in the vocabulary the expert
quiz already uses. Continuous learning, self-improvement and self-replication are
the quiz's three mechanism questions; this paper is what they are about.

### Hendrycks, Mazeika and Woodside (2023), An Overview of Catastrophic AI Risks
[arXiv:2306.12001](https://arxiv.org/abs/2306.12001)

**Its arithmetic.** A taxonomy: malicious use, AI races, organisational failures,
rogue agents. No probabilities.

**To the calculator.** The exhibits' `link` field has three values that follow the
chain. This paper's four categories cut across it; malicious use and races are
routes through the second link that the quiz's "competition" question gestures at
and the exhibits do not yet document.

### Kovarik, van Merwijk and Mattsson (2024), Extinction Risks from AI: Invisible to Science?
[arXiv:2403.05540](https://arxiv.org/abs/2403.05540)

**Its arithmetic.** An argument that realistic extinction-level failure hypotheses
may be too complex, and too dependent on systems that do not yet exist, for present
scientific methods to confirm or refute.

**To the calculator.** The epistemic version of Lohn's point, and the reason the
exhibits' `limits` field exists: what the evidence fails to establish may be most
of what matters, and a site that shows incidents has to say so. It is also a
reason to expect the third link to stay where the evidence is thinnest.

## 3. Cross-cutting comparisons

### The decomposition

| Source | Steps | The calculator's three links |
|---|---|---|
| Carlsmith | 6 | 1 covers his first two, 2 his middle three, 3 his last |
| Growiec & Prettner | 4 | 1, 2, and 3 folds the last two |
| Cappelen et al. | 2 premises, 4 survival stories | each story is one link at zero |
| Dung (PhAI) | adds a multipolar story | no slider for it |

The calculator's chain is the shortest of the four. What it gains is that a
visitor can set it in a minute; what it loses is Carlsmith's separation of
alignment difficulty from deployment from disempowerment, Growiec and Prettner's
separation of misaligned from non-corrigible, and Dung's many-systems world.

### Who is asked, and how

| Source | Population | Elicitation |
|---|---|---|
| Grace | 2,778 published researchers | one probability, several framings |
| Karger | 89 superforecasters, 80 experts | probabilities, months of argument |
| Field | 111 experts | probability plus familiarity questionnaire |
| Kestin & Soares | 89 attendees, before and after | one probability, twice |
| Calculator | 253 anonymous, self-selected, signed since August | three links with bands, quiz answers, a decoy check, and the proposed number |

The calculator's sample is the weakest in the list and its per-respondent record
the richest. Nobody else stores what the respondent knew, what they were shown,
and what they changed. Field is the only paper that pairs a number with a
familiarity measure; his instrument is a questionnaire, the calculator's is a check
that can turn people away.

### The numbers

| Source | Result |
|---|---|
| Grace | median 5%, mean ~16% |
| Karger | superforecasters ~0.4%, experts ~3%, no convergence |
| Kestin & Soares | 50% before, 70% after; newcomers up, experts flat or down |
| Calculator, before the quiz | 15% (n = 98) |
| Calculator, moved a slider | beginner 48%, medium 34%, cleared the check 31% |
| Calculator, kept the proposal | 72% to 92% by level |

What lines up: the pre-chooser cohort with Grace, once the definition is allowed
to be broader; and Kestin and Soares with the kept-and-moved split. What does not:
the tournament's experts at 3% against the check-clearers at 31%, where definition
covers part of the gap and not all of it; and Field's two camps, which do not
contain the check-clearers' chain.

### What the calculator has that none of the fifteen do

Per-link numbers from ordinary visitors. A record of what each respondent was
shown before they set a number, and whether they moved it. A control, with decoys,
on who counts as informed. A measured priming effect, on the same visitors, in the
same table. An evidence page whose entries must state their limits.

### What it lacks that most of them have

Comparability. The site's definition is deliberate: once the chain is satisfied
the outcome is bad whatever form it takes, so "global catastrophe" covers
extinction, disempowerment and collapse together, and asking which would be a
fourth link nobody can estimate. That is a sound choice for the instrument. It
means the site's numbers answer a wider question than any survey in the list, and
cannot be set beside theirs without saying so. A time horizon. A sample anyone can describe. Any theory behind the second
link; the exhibits document incidents and cite nothing from Turner, Cohen or Ngo.

## 4. What should feed back into the instrument

- **Cite Carlsmith on the About page** as the reason there is a chain, and Grace
  as the reference number, with the definitional caveat beside both.
- **The multipolar objection is real.** Three sliders cannot express a world of
  many systems. Whether that needs a fourth slider or a sentence is a design
  question; that the chain assumes a single system should at least be said.
- **Lohn's two questions** are the smallest change that would make the ± band mean
  something elicited rather than assigned: evidence for, evidence against, per
  link. The same caution as every other proposed quiz change applies.
- **The exhibits need one theory entry per link.** Turner or Ngo for the second;
  Kovarik's argument, as a limit, for the third.
- **State the definition.** "Global catastrophe" is the site's choice, and the
  right one for a chain: the critical path satisfied is the bad outcome, whatever
  form it takes. The reports should say once, in the masthead, that this is wider
  than the extinction figures the literature reports, so nobody compares 31% to 3%
  without knowing they are different questions.
