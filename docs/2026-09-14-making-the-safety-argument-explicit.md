# Making the safety argument explicit

**Date:** 2026-09-14
**Scope:** A proposal for explaining the calculator through the evidence for its
three links and the question of what keeps their product small. Follows
[where the zero goes](2026-09-13-where-the-zero-goes.md) and
[what the calculator is](2026-09-13-what-the-calculator-is.md), incorporating the
clarification that safety requires a sufficiently small probability, rather than
an exactly zero probability.
**Outcome:** Make the argument visible: the exhibits contain observed evidence
relevant to the first two links; the third has material about possible pathways,
but no observed transition to an unrecoverable global catastrophe. A claim that
humanity is safe should explain where the substantial reduction in risk comes
from. If the first two probabilities are high, that explanation must do most of
its work at the third link.

---

## 1. The proposition

The calculator can help a visitor articulate both a catastrophe scenario and a
reason for expecting humanity to remain safe. The same chain serves both purposes:

1. A deployable AI system or toolchain reaches strategic capability.
2. Given that capability, dangerous behaviour occurs.
3. Given the first two conditions, that behaviour leads to an unrecoverable global
   catastrophe.

For the modeled chain, the probability is the product of the three conditional
factors. A visitor setting a low overall probability should be able to explain
which factors make it low, and what supports those estimates.

The central question to put beside the sliders is:

> What keeps the overall risk small, and which link does that protection act on?

This gives a low estimate something concrete to express: barriers to capability,
prevention of dangerous behaviour, or prevention of escalation. A high estimate
should likewise explain why the visitor expects those protections to be
insufficient.

## 2. What “near zero” means

An exactly zero product requires an exactly zero factor. A sufficiently small
product does not. The earlier note's statement that “only a zero” reaches safety
should be revised accordingly.

“For humanity to be safe, one of the three needs to be near zero” is useful as a
qualitative statement about where protection comes from. Its numerical meaning
depends on how small the overall risk must be and on the other two factors.
Reductions across several links also compound: three factors of 10% produce an
overall probability of 0.1%.

For a chosen overall threshold T and positive first and second factors:

    p₁ × p₂ × p₃ ≤ T
    p₃ ≤ T / (p₁ × p₂)

For illustration, if p₁ = 95% and p₂ = 80%, a third factor of 1% produces an
overall probability of 0.76%. To bring that product down to 0.1%, the third factor
would have to be about 0.132% or lower. These are hypothetical inputs and an
illustrative threshold; they do not establish what risk humanity should accept.

When the first two factors are high, the third really does have to be near zero
to make the overall probability very small. The arithmetic identifies how strong
the protection needs to be. Evidence and argument must establish whether that
strength is credible.

## 3. The evidence is different at each link

The current [exhibit collection](../_data/exhibits.yml) has an important asymmetry:

| Link | What the collection contains | What remains to be established |
|---|---|---|
| Powerful AI | Reports of advanced capability demonstrated on specific tasks | How those capabilities meet the calculator's threshold of strategic capability and transfer beyond the demonstrated conditions |
| Dangerous behaviour | Reports of systems taking dangerous or out-of-scope actions | How often such behaviour occurs in the relevant powerful systems and deployment conditions |
| Global catastrophe | A planning-task result and an assessment of a possible biological catastrophe pathway | Whether and how dangerous AI behaviour could complete a pathway to an unrecoverable global catastrophe, despite intervention |

The first two links therefore have observed evidence of the relevant kinds of
capability and behaviour. The third lacks an observed catastrophic outcome in
the collection. Its existing entries concern parts of possible pathways: the
biorisk exhibit concerns a planning task, and the mirror-bacteria exhibit says
explicitly that no AI is implicated.

This distinction should be visible in the exhibit introductions. An incident can
establish that a behaviour is possible under particular conditions without
establishing that a corresponding slider should be near 100%. Equally, the absence
of an observed catastrophe does not establish that the third slider should be
near zero. Evidence about mechanisms and barriers can inform that estimate before
the outcome occurs.

## 4. Give the third link a concrete safety question

For someone who assigns high probabilities to the first two links, the relevant
question becomes:

> If powerful AI behaves dangerously, what prevents that behaviour from becoming
> an unrecoverable global catastrophe?

Possible answers to examine include early detection, isolation, limits on access
to resources, intervention by people or other systems, and recovery before damage
becomes irreversible. These are candidate protections, each requiring support.

A useful third-link exhibit would describe a particular pathway, identify the
barrier that interrupted it or could interrupt it, and explain the conditions
under which that barrier might fail. A contained incident provides evidence that
containment worked in that case. Extending that result to more capable systems,
repeated attempts, or wider deployment requires a further argument.

The existing requirement that every exhibit state its limits already supports
this approach. The collection can develop evidence about escalation and its
prevention without waiting for a global catastrophe to occur.

## 5. Proposed changes to the public explanation

**Explain the chain before asking visitors to choose a quiz.** A short paragraph
can establish what they will estimate and why the three factors matter. Suggested
copy:

> Estimate three links: powerful AI arrives, it behaves dangerously, and that
> behaviour causes an unrecoverable global catastrophe. Their probabilities
> multiply to give your estimate for this chain. A very small overall risk needs
> a substantial reduction somewhere along the chain. The exhibits show evidence
> of advanced capabilities and dangerous behaviour; the transition to global
> catastrophe remains unobserved in the collection. What would keep that final
> transition unlikely?

**Use the About page to explain the safety argument.** Show how each link can
reduce the product, include one numerical example, and explain that the choice of
an acceptable risk threshold is a separate judgement. The estimate concerns the
routes covered by the chain's definitions; those definitions determine what a low
product says about overall safety.

**Make the definitions consistent.** The current
[slider configuration](../index.html) labels the second link “dangerous behaviour”
but explains it as being “misaligned with human values.” The accompanying notes
sometimes interpret it as takeover. These are different events. The proposed
framing uses dangerous behaviour throughout, with misalignment as a possible
cause and takeover as a possible escalation. The third question should explicitly
carry forward the powerful-system condition from the first link.

**Describe the quiz's contribution plainly.** When the sliders appear, say that
the quiz has proposed a starting point from the answers and invite the visitor to
review each factor. The explanation should distinguish that proposal from the
visitor's own assessment of the evidence.

## 6. How to read the submissions under this framing

Reports can describe where visitors place the reduction in risk and how they move
each factor relative to the quiz's proposal. Those are observations about the
submitted estimates. Explaining why a visitor lowered a factor requires asking
them or collecting other evidence.

Keep the distinction between rows that retained the proposal and rows that
changed it. Neither group establishes an independent belief by itself: retaining
a number can reflect agreement, while moving it can still leave an estimate
influenced by its starting point. A low third-link estimate is a reason to examine
the visitor's account of containment or recovery, rather than evidence that those
protections will succeed.

This proposal concerns the explanation of the existing three-link instrument.
Its next concrete deliverables are the opening paragraph, an About-page account
of the arithmetic and definitions, and exhibit introductions that distinguish
observed capability, observed behaviour, and evidence about catastrophe pathways.
