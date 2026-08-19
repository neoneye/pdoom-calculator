# Exhibits: show, don't tell

Date: 2026-08-20
Branch: `artifacts-exhibits`

## Problem

The calculator asks visitors for three probabilities and gives them a number back.
Nothing on the page shows *why* AI risk is more than an abstraction, so a visitor
arrives with a vague opinion and leaves with a vague opinion expressed as a
percentage. The goal is to move people from vague opinion toward calibrated
reasoning by showing concrete, sourced material.

The constraint that shapes everything: **these are exhibits, not predictions.**
Nothing here proves a catastrophe is coming. Each item shows one specific thing
that actually happened, bounded by what it does not show.

## Why the chain is the filing system

The calculator already decomposes p(doom) into three conditionals:

1. `P(powerful AI)`
2. `P(dangerous behavior | powerful AI)`
3. `P(global catastrophe | dangerous behavior)`

Filing each exhibit under the link it bears on is what separates this from a
gallery of alarming anecdotes. A jailbreak transcript is evidence about link 2 and
says nothing whatever about link 3.

The filing also produces an asymmetry that must be shown rather than hidden:
link 2 has abundant documented incidents, link 1 has capability trends and
forecasts, and link 3 has almost no direct evidence, because nothing has yet
caused a global catastrophe. A reader who notices the third group is nearly empty
has learned where the real uncertainty lives.

## Placement, and why

Exhibits appear **after a successful submission**, and on a standalone page.

Showing them before the sliders would influence every subsequent submission.
Because the available material runs almost entirely one direction -- incidents of
models misbehaving get written up, "the model refused correctly again" does not --
pre-slider exhibits would nudge p(doom) upward and then measure the result. The
164 existing submissions would stop being comparable with everything after, and
the upward drift already documented in the report (median 15% to 68%) would gain a
confound introduced by the site itself.

Post-submission placement reaches only visitors who submit, which is why the same
collection also lives at its own URL for anyone to read directly.

## No targeting

The result screen shows **all** exhibits, grouped by link, with the number that
visitor just submitted displayed beside each group heading.

Selecting which exhibits to show based on a visitor's answers would mean
systematically arguing at anyone with a low estimate while leaving a high estimate
unchallenged -- a nudge wearing the clothes of feedback. Showing everything and
letting the reader see which of their own beliefs each item bears on is
calibration they perform themselves.

## Design

### Content model

`_data/exhibits.yml`, so exhibits can be added without touching code and are kept
out of `index.html`, which is already 2,900 lines.

```yaml
- id: gpt4-taskrabbit
  link: dangerousBehavior      # powerfulAi | dangerousBehavior | globalCatastrophe
  title: ...
  date: 2023-03
  what: One or two sentences. What actually happened.
  source:
    label: "GPT-4 System Card, OpenAI"
    url: https://...
  limits: What this does not establish.
```

`limits` is **required**. An entry without one does not render. That makes
"exhibits, not predictions" a structural property rather than an intention, and it
is the half that earns the reader's trust: an eval showing a model reasoning about
deception in a scaffolded setting is not a model autonomously deceiving people in
the wild, and the page says so itself.

### Two renderings, one source

Jekyll reads the YAML once and emits it twice:

- as JSON inside `index.html`, for the result screen to render after submission
- as static HTML at `/exhibits/`, which works with JavaScript disabled

### Result screen

Below the submission status, after a successful submit: three groups in chain
order. Each group heading names the link and the value that visitor submitted --
"P(dangerous behavior | powerful AI) — you put this at 76%". Each exhibit renders
as title, `what`, a source link, and `limits` in muted text.

The `globalCatastrophe` group carries a standing note explaining that direct
evidence does not exist for this link, rather than being padded to look full.

### Standalone page

`/exhibits/`, added as a fourth nav item labelled **Exhibits**. Same content, no
personal numbers. "Exhibits" rather than "Evidence" because evidence implies proof,
which is the claim being avoided.

### Sourcing standard

Every claim is checked against a primary source -- a paper, system card, model
card, or lab publication -- not press coverage. Anything that cannot be confirmed
against such a source is dropped rather than softened or hedged. Dates state when
the thing happened, not when it was reported.

Roughly ten entries for the first version, weighted as the material actually
falls: three to four on capability trends, five to six on demonstrated model
behaviour, one to two on catastrophe pathways.

## Out of scope

- No change to the quiz, the sliders, or what is submitted. The dataset is
  untouched, and no exhibit state is recorded.
- No dark mode.
- The pages under `reports/` are not modified.
