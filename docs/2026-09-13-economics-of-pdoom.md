# The calculator against "The Economics of p(doom)"

**Date:** 2026-09-13
**Scope:** A comparison of the calculator's belief chain with the decomposition in
Growiec and Prettner, *The Economics of p(doom): Scenarios of Existential Risk and
Economic Growth in the Age of Transformative AI*
([arXiv:2503.07341](https://arxiv.org/abs/2503.07341), v2 April 2026), and what the
paper suggests for the instrument. Follows
[experts cut the last link](2026-09-13-experts-cut-the-last-link.md).
**Outcome:** The paper builds the same chain as the calculator, one link longer,
and says the per-link estimates it needs have never been elicited. The calculator
has 197 hand-set chains. The paper's two camps, controllable tool and uncontrollable
agent, do not contain the verified experts, whose chain accepts arrival and takeover
and discounts only the final step. The one change the paper motivates is splitting
the third link into misaligned and non-corrigible, and the same caution against
overfitting applies to it.

---

## 1. Two chains

The paper is written in terms of TAI, transformative AI: an AI system capable
enough to change the trajectory of the world economy on the scale of the industrial
revolution or beyond, whether by automating most cognitive work, by driving growth
rates far above anything seen historically, or by escaping human control. It is the
economist's counterpart to what the calculator calls "powerful AI", and its
arrival is the first link in both chains. Where the paper reads "TAI arrives",
read "P(powerful AI)".

The paper decomposes extinction risk along a decision tree:

| Paper | Meaning | Calculator |
|---|---|---|
| p₁ | transformative AI arrives | P(powerful AI) |
| p₂ | it takes over, given arrival | P(dangerous \| powerful) |
| p₃ | takeover is misaligned | P(catastrophe \| dangerous), folded |
| p₄ | aligned but non-corrigible, goals locked in | P(catastrophe \| dangerous), folded |

with p(doom) = p₁p₂p₃ + p₁p₂(1−p₃)p₄. The calculator's product of three sliders is
the same object with the last two steps merged and the "TAI without takeover"
branch represented only as a low second slider.

Two definitional differences. The paper's doom is extinction; the calculator's is
"a global catastrophe", which is broader and includes the collapse and s-risk
outcomes the beginner quiz lists. And the paper's p₃ and p₄ are conditional on
takeover, where the calculator's third link is conditional on "dangerous
behaviour", a lower bar than takeover. A reader mapping one onto the other should
expect the calculator's second link to run higher than p₂ and its third link to
run lower than p₃ + (1−p₃)p₄, which is what the table shows.

## 2. They have the structure and no measurements

The paper states that no expert estimates for the individual components have been
elicited, works from illustrative scenarios for p₁ to p₄, and takes its headline
p(doom) figures from named individuals: LeCun near zero, Yudkowsky above 95%,
Hinton and Christiano around 50%, Altman, Amodei and Musk at 10 to 25%, Ord at one
in six, Metaculus at 5% with about 3 points from TAI.

The calculator's table holds per-link numbers from 253 anonymous visitors. After
this week's work the honest count of *elicited* chains is smaller: 98 pre-chooser
rows set by hand on three sliders, and 99 quiz rows where the visitor moved at
least one slider from the proposal. The 50 kept rows are the page's proposal and
do not count. That still leaves 197 chains of the kind the paper says do not
exist, with the usual caveats: self-selected, anonymous, and with the quiz priming
that the reports now separate out.

Median chain among elicited rows:

| Group | p₁ | p₂ | p₃₊₄ (calculator's third link) | p(doom) | n |
|---|---|---|---|---|---|
| Before the chooser | 0.80 | 0.60 | 0.50 | 15% | 98 |
| Beginner, moved | 0.85 | 0.83 | 0.87 | 48% | 25 |
| Medium, moved | 0.82 | 0.75 | 0.86 | 34% | 38 |
| Expert, verified, moved | 0.95 | 0.80 | 0.50 | 31% | 19 |

## 3. The two camps, and a third position

The paper describes disagreement as two camps: AI as a controllable tool, with a
low p(doom), and AI as an uncontrollable agent, with a high one. It cites Field
(2025) for the claim that experts' disagreement follows partly from varying
exposure to the key safety considerations.

The experts who cleared the site's check are the closest thing available to a
test of the exposure claim. The check is a vocabulary sanity check with decoys,
not an examination, but it does establish that these nineteen know the terms the
safety arguments are made of, so lack of exposure to the vocabulary is not what
separates them from beginners. They still sit lower, and they sit lower on one
specific link. A chain of 0.95, 0.80, 0.50 is not the controllable-tool camp: it
accepts arrival with near certainty and accepts takeover-grade behaviour at 80%.
It is a position the paper's taxonomy does not have, *uncontrollable but
survivable*, and it is held by the cohort that cleared the check.

Whether that position is a judgement or an artefact of the expert quiz never
mentioning an outcome is the open question in the previous note. The paper could
not have asked it, because it had no per-link data to ask it of. The calculator
can, at the cost of one question.

## 4. What the paper adds that the calculator lacks

The paper's contribution is the welfare side, which the calculator does not touch.
With an iso-elastic utility function and ordinary risk aversion (θ = 1.5), growth
accelerating to 30% and a 3% discount rate, a benevolent planner would accept
extinction risk from TAI only if extinction came no earlier than about 196 years
out, and the tolerable immediate misalignment probability comes out near 0.001%.
The authors conclude that current safety and alignment effort is insufficient
relative to the risk.

The implication for the calculator's readers is that the exact number on the third
link barely matters for what should be done: almost any nonzero value justifies far
more safety investment than exists. Put the other way, a product only reaches
0.001% if some link is close to zero, so the paper's threshold turns the calculator's
three sliders into the question "which link do you believe can be zeroed", taken up
in [where the zero goes](2026-09-13-where-the-zero-goes.md). The site shows a number and stops. It could
link the paper from the About page as the argument for why a small number is not
a reassuring one, which is a different message from the reading list it has now.

## 5. What the paper suggests for the instrument

**Split the third link.** The paper's distinction between misaligned doom (p₃) and
aligned-but-non-corrigible doom (p₄) is the one the calculator's third slider
collapses, and it is plausibly the distinction verified experts are reasoning about
when they cut that slider: "dangerous behaviour happens, and then it is caught"
versus "the system's goals lock in and nobody can change them". Asking the third
link as two questions would make the calculator's chain the paper's chain and let
the two be compared directly.

**The same caution applies.** The previous note argued against redesigning the
expert quiz around nineteen rows. Splitting a slider is a bigger change than adding
a question, it changes every future chain's shape, and it would make rows before
and after incomparable on the third link. If it is done, it should be done because
the chain is judged better with four links, not because the experts' 0.50 needs
explaining. The stored proposal and the page version pin the switch date, so the
report can split the cohorts either way.

**Cite the decomposition.** The About page has no explanation of the chain. The
paper is a peer-reviewed statement of the same decomposition with the reasoning
spelled out, and would serve better than any of the current links as the answer to
"why three sliders".

## 6. What not to take from it

- Not the headline figures. The paper's p(doom) list is quotes from public
  figures, not elicited estimates, and the paper says so.
- Not the two-camp model as a description of this site's visitors. The verified
  experts are in neither camp, and the pre-chooser cohort discounts every link
  roughly equally, which is not a camp either.
- Not the welfare numbers as findings. They are outputs of a utility function
  whose form the authors say is not known, and they present them that way.

Source: [Growiec and Prettner, The Economics of p(doom), arXiv:2503.07341](https://arxiv.org/abs/2503.07341).
