# Making the safety argument explicit

**Date:** 2026-09-14
**Scope:** A proposal for using the accessible quiz to educate visitors, help
them recognise gaps in their knowledge, and introduce the calculator's three
factors through concrete examples. Follows
[where the zero goes](2026-09-13-where-the-zero-goes.md) and
[what the calculator is](2026-09-13-what-the-calculator-is.md), incorporating the
clarification that safety requires a sufficiently small probability, rather than
an exactly zero probability.
**Outcome:** Make learning the purpose of the experience. The author's family
and friends can select quiz items but do not understand the numerical parameters.
Start with those recognisable items, introduce unfamiliar ideas, and help visitors
see what they do not yet understand. Use examples to connect that learning to
capability, behaviour, and consequences. The estimate gives visitors something
to explore; submitting it is secondary. Visitors should not need to define
capability thresholds or estimate conditional probabilities before they can learn.
Ground the teaching in what the exhibits already document:
advanced capabilities, dangerous actions, and AI assistance that improved human
performance on a bioweapons planning task. These give the concern about
catastrophe concrete foundations. The open question is how far the danger can
escalate through AI and human actions, and whether protections can hold. A claim
that humanity is safe should explain where the substantial reduction in risk
comes from. If the first two probabilities are high, that explanation must do
most of its work at the third link. Here, “powerful” should mean sufficiently
capable to enable the harm under consideration, including through people and
tools. A generally weak LLM can fully satisfy that condition. The three factors
separate capability, behaviour, and consequences; they are not mandatory stages
of AI development.

---

## 0. The quiz is an entry point for learning

The author's observation from showing the calculator to family and friends is
the design constraint: they can answer the quiz, but they are unsure what the
parameters mean. Asking them to justify three probabilities would make the
calculator harder to use. Explaining the mathematics more fully on the opening
screen would add another task before they reach the part they can already do.

The author's purpose is to educate quiz takers so they hopefully recognise gaps
in their knowledge. The recognition lists can make an unfamiliar idea visible:
a visitor encounters something they had not considered, reads what it means,
and discovers why it matters. A gap becomes a place to begin learning.

The intended sequence is to recognise familiar ideas, encounter unfamiliar ones,
read a concrete explanation, and connect it to the risk being discussed. The
calculator's estimate and parameters can then help the visitor explore the
consequences of different assumptions. Moving a slider or submitting a result
does not by itself establish that this learning happened.

The quiz should remain easy to enter. Short explanations and relevant examples
belong in the normal experience, with deeper reading available by choice. A
visitor need not master the parameters, change their estimate, or pass an
additional test to benefit. Recognising “I don't know enough about this yet” is
itself a useful outcome.

The model still needs precise definitions. Those are the responsibility of the
site's author and methodology. The explanations below establish what the model
means and what the reports can claim; they are not an entrance requirement for
quiz takers. A usable questionnaire does not, by itself, validate its numerical
mapping, so the result should be described plainly as the quiz's suggested
starting estimate.

## 1. The proposition

The calculator should connect the capabilities and dangerous behaviour documented
in the exhibits to the question of humanity's safety. Its three links locate both
the danger and the opportunities to prevent it from escalating:

1. **Capability:** Does AI exist, or become available, that is sufficiently capable
   to enable the relevant harm, including through people and tools?
2. **Behaviour:** Given that capability is available, will AI actually provide the
   harmful assistance or take the dangerous actions?
3. **Consequences:** Given those actions, will the consequences reach an
   unrecoverable global catastrophe?

“Powerful” is relative to the relevant task and the setting in which the AI's
outputs can be used. A model may be weak at general reasoning and still supply a
crucial capability for a dangerous activity. It does not need broad intelligence,
autonomy, or takeover capability to satisfy the first condition.

Under this interpretation, a generally weak LLM can max out P(powerful AI). If
the required capability has been demonstrated and is available in the relevant
setting, the probability that it exists can reasonably be at or near 100%. The
remaining uncertainty concerns whether it will be used dangerously and how far
the consequences will escalate.

The methodology needs to state the threshold: what capability is sufficient for
which harm? A quiz taker should not have to invent that definition.
A prohibited response or minor rule violation does not automatically establish
capability relevant to global catastrophe. The first factor concerns the ability
to enable a relevant action; it does not require the catastrophic outcome itself
to have been demonstrated.

Humans can be the body of the AI: a system can supply plans, instructions,
persuasion, or coordination, while people provide physical access, resources,
and execution. The chain includes autonomous actions, human actions enabled or
directed by AI, and combinations of the two. It does not require the AI to
complete every step itself or to originate the harmful objective.

The calculator currently multiplies three factors, with conditional wording on
the second and third. These distinguish having a capability, acting on it, and
the resulting consequences. They do not require a model to progress through
successive levels of intelligence. Dangerous behaviour by a weak LLM can already
provide evidence about both its capability and its behaviour, while leaving the
scale of the eventual consequences unresolved.

The central question for the methodology and optional explanation is:

> What keeps the overall risk small, and which link does that protection act on?

This gives the interpretation of a low estimate something concrete to describe:
barriers to capability, prevention of dangerous behaviour, or prevention of
escalation. It also gives an interested visitor a way to investigate a high
estimate. Answering it is optional; the quiz remains usable without that analysis.

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

Let A mean the relevant AI capability is available, including through people and
tools; B mean the dangerous behaviour occurs; and C mean AI causes an
unrecoverable global catastrophe. A complete conditional chain is:

    P(A) × P(B | A) × P(C | A and B) = P(A and B and C)

With the task-relative definition of capability, a weak LLM and people enabling
the relevant harm can satisfy A. Such a route is not excluded merely because the
LLM lacks broad strategic capability. If A is already established, its factor is
one and the numerical uncertainty lies in behaviour and consequences.

For this product to equal the full P(C), the definitions of A and B must cover
the relevant routes to C. The current third slider says P(C | B). That shorthand
is justified if B explicitly refers to behaviour involving the capability in A,
so that B already implies A; otherwise the conditioning on A must be retained or
its omission justified. These are requirements for a consistent probability
model, not a requirement for an autonomous AI to pass through stages of development.

The proposal therefore resolves the weak-LLM concern by defining capability
relative to the harm it can enable. The definitions should be made explicit in
the interface before interpreting older submissions under this meaning.

## 3. The evidence is different at each link

The current [exhibit collection](../_data/exhibits.yml) has an important asymmetry:

| Link | What the collection contains | What the evidence leaves open |
|---|---|---|
| Powerful AI | Reports of capability demonstrated on specific tasks | Whether AI, together with people and tools, already supplies the capability needed for the relevant harm, and under which conditions |
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

A demonstration that meets a defined capability threshold can settle the first
question for that setting, even when the model is generally weak. That does not
by itself establish how often dangerous behaviour occurs or how likely it is to
cause catastrophe. The exhibits make the danger concrete while leaving those
probabilities to be assessed.

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

**Invite discovery through the quiz.** The opening should make the learning
purpose clear in terms the visitor already understands. Suggested copy:

> Explore what you know about AI and discover ideas you may not have encountered.
> Along the way, learn how AI could cause harm and what might prevent it.

There should be no requirement to understand the three parameters before taking
the quiz. The current recognition questions already provide an accessible way
in, according to the author's observations.

**Use unfamiliar items as invitations to learn.** Give each concept a short
explanation and, where available, a link to a concrete example or exhibit. Keep
these accessible alongside the questions or in brief feedback after answering.
The visitor should have opportunities to learn before registration. An unchecked
item is a reason to offer an explanation, not proof that the visitor knows
nothing about it. Checking a familiar name also does not demonstrate understanding.

Recognition questions should allow visitors to say what is familiar without
penalty for admitting uncertainty. Opinion questions can offer “I'm not sure”
where appropriate, with any effect on the proposed estimate documented. Decoys,
if used, should be explained after the answer so that the feedback teaches the
distinction. They should not turn the beginner experience into a barrier to entry.

**Connect one concrete example to the three factors.** Introduce the factors
through an example the visitor has just encountered, before asking them to
interpret the numbers. Use ordinary language, with formal probability labels in
the detailed explanation:

| Factor | Short explanation |
|---|---|
| Capability | Whether AI can help make the harm happen, including through people and tools |
| Behaviour | Whether AI will actually give dangerous help or take dangerous actions |
| Consequences | Whether those actions lead to a global catastrophe |

For example, a system giving harmful advice illustrates a capability and an
action. Whether people act on that advice, and how far the harm spreads, concerns
the consequences. The explanation can introduce the user's points that humans
can be the AI's body and a generally weak LLM can be capable enough for a
dangerous task. It should make the connection in a few sentences, without asking
the visitor to supply a numerical probability.

**Use the result as a prompt for reflection.** Label it “Starting estimate from
your quiz answers.” Suggested supporting copy:

> This is the starting estimate the quiz generated from your answers. Which
> ideas were new to you? You can revisit their explanations and explore how the
> three factors affect the result.

An explanation of an unfamiliar item should be as easy to reach as a slider.
The visitor can keep or adjust the result and decide whether to register it.
There is no required direction for an update: learning may increase concern,
decrease it, or leave someone recognising more uncertainty. A higher submitted
P(doom) is not a measure of educational success.

**Put the full safety argument in About and the methodology.** Explain how a
weak LLM can satisfy the capability factor, how humans can carry out its outputs,
and what evidence informs each factor. Include the near-zero arithmetic and the
scope of the product for readers seeking that detail. Define the relevant harm
and capability threshold there, consistently with the quiz's numerical mapping.
The short, concrete teaching belongs in the quiz experience. About and the
methodology provide the fuller argument for people who want to follow it.

**Make the definitions consistent across those explanations.** The current
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
its operator. The consequence question includes harm mediated by people. A
contributing LLM can be weak overall while satisfying the first factor's
task-relative capability threshold.

**Check the experience with the people it is intended to serve.** When the author
next shows it to family and friends, ask what was new to them, which explanation
helped, and what they would like to understand better. See whether they can
connect one example to capability, behaviour, or consequences in their own words.
These are useful feedback questions for improving the teaching, not an additional
test required for submission. Being able to complete the quiz still matters, but
the purpose is that a visitor leaves with a clearer idea of both the subject and
the gaps in their own understanding.

## 6. How to read the submissions under this framing

Educational engagement and probability elicitation are distinct outcomes of the
same experience. Submission counts, retained proposals, and slider movements
describe interaction with the calculator. They do not establish that someone
learned, discovered a gap in their knowledge, or now understands the parameters.
Feedback about unfamiliar ideas and explanations can help assess those outcomes.

Reports can describe where visitors place the reduction in risk and how they move
each factor relative to the quiz's proposal. Those are observations about the
submitted estimates. Explaining why a visitor lowered a factor requires asking
them or collecting other evidence.

Keep the distinction between rows that retained the proposal and rows that
changed it. Neither group establishes an independent belief by itself: retaining
a number can reflect agreement, while moving it can still leave an estimate
influenced by its starting point. The author's observations also give a concrete
reason someone might keep the proposal: the quiz is understandable but the
parameters are not. The reports should not assume which explanation applies to
an individual submission. A retained proposal is a valid completed interaction;
whether the visitor learned and what they believe remain separate questions.

When a result comes from the quiz mapping, the report should describe it as such.
It should not attribute a detailed view about capability, containment, or recovery
to a respondent who never expressed that view. Parameter changes can still be
analysed, with the same caution about what the visitor understood and intended.

This proposal concerns the explanation of the existing three-link instrument.
Its next concrete deliverables are a learning-focused quiz invitation, brief
explanations for unfamiliar concepts, a concrete example connecting the three
factors, and a result presentation that invites reflection. About and the
methodology supply deeper detail. The exhibits retain their concrete evidence
and stated limits.
