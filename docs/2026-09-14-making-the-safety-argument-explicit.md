# Making the safety argument explicit

**Date:** 2026-09-14
**Scope:** A proposal for explaining the calculator through the evidence for its
three links and the question of what keeps their product small. Follows
[where the zero goes](2026-09-13-where-the-zero-goes.md) and
[what the calculator is](2026-09-13-what-the-calculator-is.md), incorporating the
clarification that safety requires a sufficiently small probability, rather than
an exactly zero probability.
**Outcome:** Ground the safety argument in what the exhibits already document:
advanced capabilities, dangerous actions, and AI assistance that improved human
performance on a bioweapons planning task. These give the concern about
catastrophe concrete foundations. The open question is how far the danger can
escalate through AI and human actions, and whether protections can hold. A claim
that humanity is safe should explain where the substantial reduction in risk
comes from. If the first two probabilities are high, that explanation must do
most of its work at the third link. These are not mandatory stages of AI
development: a weak LLM can already behave dangerously. The scope of the product
must be explicit before it can support a claim about overall safety.

---

## 1. The proposition

The calculator should connect the capabilities and dangerous behaviour documented
in the exhibits to the question of humanity's safety. Its three links locate both
the danger and the opportunities to prevent it from escalating:

1. Capability: whether a deployable AI system or toolchain reaches strategic
   capability.
2. Behaviour: whether AI does dangerous things, including things it is not
   supposed to do.
3. Consequences: whether AI's contribution leads to an unrecoverable global
   catastrophe.

These are distinct questions. A weak LLM can behave dangerously without first
reaching strategic capability. The scale of the consequences also depends on
what people do with its outputs and what systems it can affect. Calling these
questions “links” should not imply that a model must progress through three
capability stages or that dangerous behaviour awaits the arrival of powerful AI.

Humans can be the body of the AI: a system can supply plans, instructions,
persuasion, or coordination, while people provide physical access, resources,
and execution. The chain includes autonomous actions, human actions enabled or
directed by AI, and combinations of the two. It does not require the AI to
complete every step itself or to originate the harmful objective.

The calculator currently multiplies three factors, with conditional wording on
the second and third. Conditioning a probability on powerful AI does not mean
dangerous behaviour is impossible without powerful AI. It specifies which cases
the probability refers to. The scope of that multiplication matters for any
conclusion drawn from a low result.

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

“For humanity to be safe, one of the three needs to be near zero” expresses the
intended safety argument. Applying it to the whole risk requires the product to
cover the relevant routes to catastrophe. Within the product, its numerical
meaning depends on how small the risk must be and on the other two factors.
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

### The product's scope

Let A mean powerful AI exists, B mean dangerous AI behaviour occurs, and C mean
AI causes an unrecoverable global catastrophe. A complete conditional chain is:

    P(A) × P(B | A) × P(C | A and B) = P(A and B and C)

This identity allows B to occur without A. It describes the probability of all
three events occurring; it is not a claim that A is a causal prerequisite for B.
For the result to equal the full P(C), catastrophe outside A and B must be
excluded by the definitions or accounted for separately. The current third
slider says P(C | B), so any omission of A from its conditioning also needs an
explicit justification.

A weak LLM behaving dangerously does not by itself invalidate conditional
multiplication. If a weak LLM and people can cause catastrophe without the first
condition ever being met, however, that route falls outside this product. A low
first factor would then reduce the displayed number without establishing safety
from that route. The public explanation needs to acknowledge this open modeling
question. Removing the conditional wording and multiplying three unrestricted
probabilities would not resolve it.

## 3. The evidence is different at each link

The current [exhibit collection](../_data/exhibits.yml) has an important asymmetry:

| Link | What the collection contains | What the evidence leaves open |
|---|---|---|
| Powerful AI | Reports of advanced capability demonstrated on specific tasks | How those capabilities meet the calculator's threshold of strategic capability and transfer beyond the demonstrated conditions |
| Dangerous behaviour | Reports of systems taking dangerous or out-of-scope actions | How the probability and effects vary with capability, access, human involvement, and deployment conditions, including for weak LLMs |
| Global catastrophe | Measured improvement in human bioweapons planning with AI assistance; an expert assessment of the biological mechanisms that could make mirror bacteria catastrophic | The practical barriers between planning and execution, how much AI and human actions can overcome them, and whether protections prevent irreversible global harm |

The first two links have observed evidence of the relevant kinds of capability
and behaviour. For the third, the biorisk exhibit reports that participants with
model access produced better bioweapons acquisition plans, with fewer critical
failures, than participants using the internet alone. That is an observed
contribution to a dangerous activity. People provide the route from the AI's
outputs to physical action.

The trial assessed plans; it did not test weapon construction or deployment. The
mirror-bacteria assessment identifies biological reasons why creating such
organisms could have catastrophic consequences. The calculator author's view is
that AI can help humans create them, with people and laboratories providing the
physical execution. That makes mirror bacteria a concrete concern for the third
link, including if the AI is assisting human research rather than pursuing an
independent objective.

The assessment addresses the biological hazard; it does not test AI's ability to
enable or accelerate the work. The inference about AI's contribution should be
stated explicitly alongside that evidence. The absence of demonstrated AI
involvement in the assessment establishes no limit on what AI could enable.
Neither exhibit documents an unrecoverable global catastrophe. Their limits
identify what remains unresolved about the route to that outcome.

The practical question is whether the remaining barriers can withstand the
capabilities available to people and AI systems acting together. A low estimate
for the third link needs an account of why they can. A high estimate needs an
account of how they could fail. The absence of a catastrophe so far cannot, by
itself, establish the reliability of those barriers. Prevention has to be assessed
before the outcome it is meant to prevent.

Observed incidents also do not assign numerical probabilities to the first two
links. Their frequency, conditions, and relevance to strategic capability remain
part of the assessment. The exhibits make the danger concrete while leaving its
ultimate probability open.

## 4. Give the third link a concrete safety question

The safety question applies to dangerous behaviour at any capability level:

> Given the capabilities and dangerous behaviour already documented, what keeps
> AI and the people acting on its outputs from causing irreversible global harm?

Protections to examine include early detection, isolation, limits on access
to resources, intervention by people or other systems, and recovery before damage
becomes irreversible. These are candidate protections, each requiring support.

Those protections must address the human part of a pathway too. People may
knowingly pursue a harmful objective, follow advice without understanding its
consequences, or act under persuasion. Shutting down a system does not by itself
withdraw instructions already delivered or stop people acting on them. A case for
containment should explain what interrupts the resulting actions as well as what
restricts the AI's own access.

A useful third-link exhibit would start with a documented action or result,
identify the further steps that could lead to wider harm, and describe the
barriers at those steps. It should explain what supports confidence in those
barriers and what could defeat them. A contained incident provides evidence that
containment worked in that case. Extending that result to more capable systems,
repeated attempts, or wider deployment requires a further argument.

The existing requirement that every exhibit state its limits already supports
this approach. The collection should help readers assess whether protections
work at the points where dangerous capabilities reach people, resources, and
infrastructure.

## 5. Proposed changes to the public explanation

**Explain the chain before asking visitors to choose a quiz.** A short paragraph
can establish what they will estimate and why the three factors matter. Suggested
copy:

> Even a weak LLM can do things it is not supposed to do. People can carry AI's
> plans and instructions into the physical world. The exhibits document advanced
> capabilities and dangerous behaviour; the safety question is what prevents
> irreversible global harm. This calculator organises your assessment around
> capability, behaviour, and consequences. What keeps the risk small, and what
> gives you confidence that the protection will hold?

**Use the About page to explain the safety argument.** Show how each link can
reduce the product, include one numerical example, and explain that the choice of
an acceptable risk threshold is a separate judgement. The estimate concerns the
routes covered by the chain's definitions; those definitions determine what a low
product says about overall safety. Explain the conditional factors and address
routes involving weak LLMs before presenting the product as the total P(doom).

**Make the definitions consistent.** The current
[slider configuration](../index.html) labels the second link “dangerous behaviour”
but explains it as being “misaligned with human values.” Those meanings should
be reconciled in the public explanation. Takeover enters the accompanying
literature comparisons through the papers being discussed, including Growiec and
Prettner's model. It is not a requirement stated by the calculator. Comparisons
should attribute that premise to the relevant paper and preserve the distinction
between its takeover event and the calculator's broader dangerous-behaviour event.
The proposed framing uses dangerous behaviour throughout, with misalignment as a
possible cause. Dangerous behaviour also includes assisting harmful human
objectives; it need not involve the system independently wanting harm or resisting
its operator. The consequence question includes harm mediated by people and does
not presume that the contributing LLM is powerful. The numerical model must make
clear how those cases enter its estimate.

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
