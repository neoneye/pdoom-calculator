# Modelling the regulation questions

**Date:** 2026-11-07
**Scope:** A visitor asked for two questions, *"Should AI innovation be well regulated?"* and
*"Would you be OK with capping model capabilities for safety?"*, to compare how non-technical
people, technical people and AI safety people answer. Working through the edge cases showed
that any short list of regulation questions has gaps, and that a gap in the answer options
makes a gap in the rules look like a sensible choice.
**Outcome:** Model the space instead of collecting opinions. Ask the same strictness scale for
every kind of AI, ask separately where the rules apply, add two belief questions about whether
rules can hold at all, and after the visitor submits, show them which kinds of AI their answers
leave without rules. Nothing is implemented yet.

---

## 1. Why the two requested questions do not work

- **"Well regulated" is a yes-trap.** Nobody is for badly regulated anything. If every group
  answers yes there is nothing to correlate.
- **"AI innovation" is too broad.** It covers a spam filter, a model on a phone and a
  frontier training run. A visitor can mean yes to one and no to another, and the answer
  cannot say which.
- **"Capping capabilities" costs nothing and names nothing.** Beginners do not know what a
  capability cap is, the question does not say which models, and yes is free when no price
  is attached.
- **The medium quiz already asks a near neighbour.** `medium-governance` asks whether
  regulation *can* keep AI safe. "Can" and "should" differ, and "should, but it can't" is a
  profile worth finding.

## 2. The central dilemma: patches look like valid choices

The first rewrite was two questions. Each objection that followed exposed a kind of AI the
options did not cover, and each fix was another question or another option:

| Objection | What the options had missed |
|---|---|
| Frontier labs versus narrow local LLMs | "Regulated AI" lumped together things with very different risk |
| An uncensored model runs on a phone | "Small programs on your own computer" assumed local means weak. Where a model runs and how capable it is are separate |
| Military AI | Not on the list at all, and excluded from most real laws |
| Claude Code, Codex, Antigravity | "Chatbots" hid AI that acts on its own and makes discoveries |
| Evil Qwen, LoRAs, removed refusals | A safety check on a downloadable model does not survive changes made afterwards |
| The EU AI Act is regional | Rules stop at borders, and downloadable AI does not |
| Orbital data centres | Physical access and the power supply, two of the three ways to switch AI off, disappear |

**Each patched version would have been published as if it were complete.** A visitor
answering it sees a finite list and reasonably treats it as the whole picture. If the list
has no row for military AI, the visitor's answers leave military AI without rules, and
nothing on the page says so. If one option reads "each country's military should decide for
itself", it sounds considered, and the visitor walks away thinking they chose a safe set of
rules. The survey has then told them something false without stating anything false.

Patching cannot fix this, because the next objection is always one news cycle away. The fix
is to model the space so that every kind of AI gets the same question, and to make any gap the
visitor's answers leave visible.

## 3. The model

Three axes, plus beliefs about whether rules can hold.

### 3.1 What: kinds of AI

Defined by what the AI is and who controls it, not by product names. The rows must not
overlap, and together they must cover everything.

| Kind | Everyday description |
|---|---|
| Big-company AI | AI run by the big companies: chatbots like ChatGPT, Claude and Gemini, and AI helpers like Claude Code, Codex and Antigravity that work on their own, write software and help make discoveries in math and physics |
| Downloadable AI | AI anyone can download and run on a phone or computer, including versions with the safety limits removed and helpers that work on their own |
| Changes to downloadable AI | Small add-on files, edits, or changes to how it runs that alter how a downloaded AI behaves, including removing its safety limits |
| AI still being built | AI inside companies before anyone outside sees it, including AI the companies use to build the next AI |
| Military AI | AI used by armed forces, including in weapons |
| Government AI | Police, surveillance, intelligence services |
| Everyday narrow AI | Spam filters, face unlock, recommendations |

Notes on the boundaries:

- **Changes are their own row** because the base model and the add-on have different makers.
  A visitor can want the base model free and the tools that strip its limits restricted, or
  the reverse.
- **Acting on its own is not a row.** Agents exist across big-company and downloadable AI;
  making it a row would split every other row. It is asked once as its own question (3.4).
- **Space is not a row.** Orbital data centres run big-company AI. Space changes where the
  rules apply (3.3) and whether AI can be switched off (section 6), not what kind of AI it is.
- **Government and military are kept apart** because laws often treat them differently. Worth
  testing whether visitors distinguish them.
- **Product names are examples, not definitions,** so the rows still work when the names change.

### 3.2 How strict: one scale for every row

- No rules
- Basic rules (it must be clear what it does and who is responsible)
- It must pass safety checks before it is used
- It should not be allowed

The same four steps everywhere. That gives seven ordered answers on one scale, comparable
across rows and across groups, and it fits the earlier finding that ordered scales carry
signal where tick lists do not. On a phone it is seven stacked rows of four buttons, not a grid.

### 3.3 Where: the reach of the rules

> Where should the rules for AI apply?
> - Nowhere, the companies set their own rules
> - Each country makes its own rules
> - Groups of countries together, like the EU
> - A worldwide agreement that every country signs

An earlier draft asked "who sets the rules" and mixed who makes them with how far they reach.
Reach is the thing that leaves loopholes.

### 3.4 Acting versus answering

> Should AI that does work on its own need stricter rules than AI that only answers questions?
> - No, the same rules
> - Somewhat stricter
> - Much stricter
> - AI should not be allowed to work on its own

### 3.5 Beliefs: can the rules hold at all?

Not policy questions. They measure whether the visitor knows how rules fail, which is needed
to read the policy answers correctly.

> If a downloadable AI passes a safety check, can someone change it afterwards so it behaves badly?
> - No, the check still holds
> - Yes, but it takes experts and a lot of effort
> - Yes, anyone, with a small change
> - I don't know

> If one part of the world has strict AI rules and the rest does not, what happens?
> - Companies follow the strict rules everywhere
> - The work moves to places without the rules
> - The AI is built elsewhere and still reaches everyone over the internet
> - I don't know

Without the first, "safety checks for downloadable AI" is ambiguous. It can mean "I want them
to hold" or "I don't know they can be undone in minutes". These two answers are also where
technical and non-technical visitors are most likely to split.

### 3.6 The cost of slowing down

> Would you accept the next big AI arriving years later, if that time were used to make it safe?
> - No, progress matters more
> - Only for the most powerful AI
> - Yes, even if it takes many years
> - We should stop building more powerful AI altogether

The first to drop if the set is too long. It sits closest to the p(doom) sliders and adds the
least.

## 4. The readout: show the gaps, don't grade them

After the visitor submits, read their own answers back as a set of rules, and state facts
where their answers rely on something the facts contradict. Same text for every visitor who
gives that combination. Shown after all questions, so it cannot shift later answers.

> Under your answers, these kinds of AI would have no rules: **military AI**.

> A safety check on a downloadable AI can be undone afterwards, for example with a small
> add-on file. Under your answers, those changes have no rules.

> Under your answers, rules apply only where they are made. AI built elsewhere can still be
> downloaded anywhere. AI running in space falls under the rules of the country that launched it.

> Most AI laws leave out military use. The EU AI Act, for example, does not cover AI used only
> for military or national security purposes.

This is the same move the calculator already makes: it does not tell the visitor their p(doom)
is wrong, it multiplies their own sliders. A set of rules has a gap wherever a row says "no
rules", and the readout makes that visible.

## 5. Dilemmas that remain

**Recording versus informing.** A question that warns the visitor records the site's opinion,
not theirs, and the group comparison is lost. A question that stays silent can let a gap pass
as a safe choice. The split above, neutral questions and a factual readout afterwards, is the
compromise. It informs the visitor but does not protect the data from someone who reads the
readout and then submits again; repeat rows are already flagged by visitor key.

**Completeness versus length.** Seven grid rows plus five questions is twelve answers. The
[post-submit survey note](2026-09-02-post-submit-survey.md) budgeted about ten items and a
minute. Grid answers are quick, so it may fit. If not, drop the delay question first and the
acting-versus-answering question second. The grid, the reach question and the two belief
questions are what make this a model rather than a list of opinions.

**One wording for everyone.** Comparing groups needs identical items in every quiz, so the
wording must be beginner-readable, which on this site means no math: no percentages,
no "LoRA", no "harness", no "open weights". The cost is precision for the experts, who can
read plain words but would phrase the rows differently.

**Rows versus axes.** Every new case tempts a new row. Most are not new kinds of AI: agents
cut across rows, space is jurisdiction, bit flips are hardware security. Adding them as rows
would make the rows overlap and the answers ambiguous. The test for a new row is that it has a
different maker or controller from every existing row and that a reasonable person could want a
different rule for it.

**A moving landscape.** Evil Qwen was two weeks old when this note was written; orbital data
centres are being filed for now. Rows are defined by function so they age slowly, and the item
set gets a new `survey_id` when a row changes, so old answers keep their meaning.

**Answers that are not on the scale.** "It can't be stopped anyway" and "I don't know" are
real, common positions but not steps between yes and no. Keep them, and analyse them as their
own group rather than forcing them into the order.

**A legitimate view that looks like a gap.** "No rules for the military, strict rules for
everyone else" is held by many people, often for national-security reasons. The survey should
record it faithfully. The option is worded plainly ("No rules for military AI") so it reads as
what it is rather than as a considered compromise.

**Not feeding the calibration.** In the medium quiz the governance, competition and speed
answers set the proposed starting values for the sliders, and 55 of the 164 rows that record a
proposal never moved a slider midpoint. For those rows the quiz answers predict p(doom) because
the page computed p(doom) from them. These questions must stay unscored and sit after the
sliders, where the survey note places its own items, so they cannot steer the prediction.

**Sample size.** Cohorts are 26 to 39 per report. Three groups across four answers is a
handful of visitors per cell. Expect months before the comparison says anything.

## 6. One change to an existing question

The beginner question *"If AI starts doing dangerous things, what is your gut reaction?"*
describes its first answer as: *"Humans control the electricity, internet, and physical access
to the servers."* A solar-powered satellite removes two of the three. The description should
stop stating this as unconditional. This is the only change to the live quiz that came out of
this work.

## 7. Facts to verify before the site cites them

Check each like the exhibits ([exhibit verification](2026-08-31-exhibit-verification.md)):

- **EU AI Act:** applies to providers placing AI on the EU market wherever they are based;
  excludes AI used only for military, defence or national security; exempts free and
  open-source models from some obligations unless they carry systemic risk.
- **Council of Europe Framework Convention on AI:** signed by the US, UK and EU; national
  security is excluded.
- **Outer Space Treaty:** states are responsible for their companies' activities in space
  (Art. VI); an object stays under the jurisdiction of its state of registry (Art. VIII).
- **Evil Qwen (24 October 2026):** Lyra steered two MLP neurons in Qwen3.5-4B (layer 14,
  neuron 8949 at +1; layer 13, neuron 7956 at −1) at inference time; weights unchanged;
  reproductions say one neuron does most of the work. Sources are mostly social posts; the
  GitHub reproductions (`shmuelamar/evil-qwen`, `AbedAlrahman01/evil-qwen`) are the closest to
  primary material.
- **Refusal removal:** Arditi et al. (2024), "Refusal in language models is mediated by a
  single direction".
- **Emergent misalignment:** Betley et al. (2025), narrow fine-tuning causing broad misbehaviour.
- **Bit-flip attacks:** PrisonBreak (Coalson et al.), jailbreaking with fewer than 25 targeted
  bit flips via Rowhammer. Random flips mostly break a model rather than turn it; servers use
  ECC memory, phones mostly do not.
- **Orbital compute:** SpaceX's FCC filing for up to a million data-centre satellites
  (January 2026) and its acquisition of xAI (February 2026); Google's Project Suncatcher
  (announced November 2025; reports conflict on whether a prototype launched in October 2026);
  Blue Origin's Project Sunrise filing; Starcloud training a model in orbit.

## 8. Open items

- Whether beginners understand "AI still being built". It matters, since risk can appear
  before release.
- Whether visitors actually distinguish government AI from military AI.
- The exact readout rules: which combinations trigger which line.
- Evil Qwen and the orbital filings as candidate exhibits.
