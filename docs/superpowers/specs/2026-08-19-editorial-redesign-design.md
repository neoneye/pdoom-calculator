# Editorial redesign

Date: 2026-08-19
Branch: `restructure-quiz`

## Problem

The stylesheets carry **145 hard-coded `rgba()` literals across two files and exactly one
CSS custom property** (`--border-color-primary`). Every colour is spelled out at its use
site, so a dozen near-identical greys and blues have drifted apart. Type is
`"Helvetica Neue", Arial` with sizes picked ad hoc per component -- there is no scale.

The result is not ugly so much as unconsidered, and it cannot be changed cheaply:
adjusting one colour means finding every literal that meant the same thing.

## Chosen direction

Three directions were rendered on the real page and reviewed (see
`docs/superpowers/specs/assets` note below). Direction **B, editorial**, was chosen:
light paper, Newsreader serif headings, hairline rules instead of boxes, oxblood accent,
the three quiz tiles becoming a list.

The reasoning: this page asks people to read 30 terms and three probability questions.
Light backgrounds win on long-form reading, and the serif gives the page a point of view
the current UI lacks entirely.

The comparison page lives at
`https://claude.ai/code/artifact/4f5ae3b3-7ca3-4068-9a85-99c225c43bfd`.

## Design

### Foundation: the token layer

Custom properties on `:root` in `main.css`, referenced by every rule in both stylesheets.

| Group | Tokens |
|---|---|
| Ground | `--paper #faf9f6`, `--surface #ffffff`, `--surface-sunken #f3f1ea` |
| Line | `--line #e2ded4`, `--line-strong #c9c3b5` |
| Ink | `--ink #1c1a17`, `--ink-2 #55504a`, `--ink-3 #6f6a61` |
| Accent | `--accent #9a3412`, `--accent-ink #ffffff`, `--accent-soft #fbf1ef` |
| Semantic | `--ok #4a7c59`, `--ok-soft #f0f5f0`, `--ok-ink #2c4a34`, `--bad #b04a3d`, `--bad-soft #fbf1ef`, `--bad-ink #7a2e24`, `--warn #9a6a1c` |
| Type | `--font-serif`, `--font-sans`, scale `--text-xs .8125rem` through `--text-3xl 2.5rem` |
| Space | `--space-1 .25rem` through `--space-8 4rem` |
| Radius | `--radius-sm 4px`, `--radius 6px` |

The semantic group does not exist today in any form. The knowledge check's
correct/incorrect/missed states, the quiz result success/warning states and the sticky
P(doom) chip are all currently tuned for a dark background and would be unreadable on
paper. Retuning them is required work, not polish.

### Typography

Newsreader, self-hosted from `assets/fonts/`, upright only:

- `newsreader-latin.woff2` (131KB) and `newsreader-latin-ext.woff2` (86KB), each declared
  with the `unicode-range` Google publishes, so a browser fetches latin-ext only if a page
  actually needs it. Most visitors download one file.
- `font-display: swap`, Georgia then Times fallback.
- The italic cut is deliberately **not** shipped. It served only the Hawking quote in the
  footer, and 63KB for one line is poor value; the quote runs in serif regular.

Body text, controls and all numeric data stay on the system sans stack. No second webfont.
Serif is reserved for `h1`, section headings, card titles and the footer quote.

Running prose is capped near 65 characters. Numeric readouts get
`font-variant-numeric: tabular-nums`, which they lack today.

### The canvas is not CSS

The bell curves are painted in JavaScript with five hard-coded dark-theme colours at
`index.html:2759-2800`, including a `rgba(255, 255, 255, 0.9)` drag handle and near-white
gridlines. On a light ground these disappear.

The fix: read the values from the token layer at draw time via
`getComputedStyle(document.documentElement).getPropertyValue(...)`, resolved once per
`recalc()` rather than per frame. Four new tokens back this: `--curve-fill`,
`--curve-stroke`, `--curve-grid`, `--curve-handle`.

This keeps one source of truth and means a later dark mode fixes the canvas for free.

### Components

- **Nav** -- uppercase text links, accent underline for the current page, no pills.
- **`main`** -- loses its card chrome for a plain 780px column on paper.
- **`h1`** -- serif, centred, hairline rule beneath.
- **Flow cards** -- list rows separated by hairlines; hover tints the row.
- **Quiz questions** -- numbered rows, hairline separated, checkbox and radio rows with
  tap targets at 44px or more, correct/incorrect states from the semantic tokens.
- **Buttons** -- 4px radius; primary is filled accent, secondary is outlined.
- **Sliders** -- light track, accent thumb, canvas reading tokens.
- **Metric cards** -- light surfaces, tabular numerals.
- **Sticky P(doom) chip** -- accent-soft ground with accent ink, replacing the red-on-dark.

### Accessibility

Measured contrast against `--paper`, not assumed:

| Token | Ratio | |
|---|---|---|
| `--ink` | 16.49 | AAA |
| `--ink-2` | 7.58 | AAA |
| `--ink-3` | 5.10 | AA |
| `--accent` | 6.94 | AAA |
| `--ok-ink` on `--ok-soft` | 8.91 | AAA |
| `--bad-ink` on `--bad-soft` | 8.44 | AAA |
| `--accent-ink` on `--accent` | 7.31 | AAA |

`--ink-3` was first set to `#8a837a`, which measured 3.56:1 and fails AA for normal text
-- it carries the card meta, the footer quote and the slider notes. It was darkened to
`#6f6a61` after measurement. `--warn` (4.48:1) is used only as a border, where the
threshold is 3:1 for non-text UI, so it is unchanged.

Focus states are a 2px accent outline with 2px offset, applied to every interactive
element rather than the subset that has one today.

## Scope

`main.css` is shared, so `index.html`, `about.html`, `stats.html` and `embed.html` change
together. That is forced by the file structure, not a choice.

## Out of scope

- The pages under `reports/`. They carry their own embedded styles and stay dark; they
  will look like a separate artifact until they follow.
- Chart colours in `prepare_report_data.py`.
- **Dark mode.** Deferred deliberately. The tokens are structured so a
  `prefers-color-scheme: dark` block is a small follow-up; doing both now would double the
  visual QA on a change that already touches every component.
