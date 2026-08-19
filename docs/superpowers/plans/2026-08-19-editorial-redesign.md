# Editorial Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the ad-hoc dark styling with a token-driven editorial design — light paper, self-hosted Newsreader headings, hairline rules, oxblood accent — across the calculator, about, stats and embed pages.

**Architecture:** A token layer on `:root` in `main.css` is the foundation; every rule in both stylesheets references tokens instead of literals. The bell-curve canvas reads four of those tokens at draw time so its colours stop being hard-coded. Work proceeds foundation → shared chrome → quiz → sliders, so each task leaves the site coherent.

**Tech Stack:** Jekyll static site, hand-written CSS in `assets/css/main.css` and `assets/css/quiz.css`, vanilla JS canvas in `index.html`, self-hosted woff2.

## Global Constraints

- Palette, verbatim: `--paper #faf9f6`, `--surface #ffffff`, `--surface-sunken #f3f1ea`, `--line #e2ded4`, `--line-strong #c9c3b5`, `--ink #1c1a17`, `--ink-2 #55504a`, `--ink-3 #8a837a`, `--accent #9a3412`, `--accent-ink #ffffff`, `--accent-soft #fbf1ef`, `--ok #4a7c59`, `--ok-soft #f0f5f0`, `--ok-ink #2c4a34`, `--bad #b04a3d`, `--bad-soft #fbf1ef`, `--bad-ink #7a2e24`, `--warn #9a6a1c`.
- Serif is for `h1`, section headings, card titles and the footer quote only. Everything else is the system sans stack.
- No italic cut of Newsreader ships. The footer quote runs in serif regular.
- Tap targets on interactive rows are at least 44px tall.
- Focus is a 2px `--accent` outline at 2px offset on every interactive element.
- Numeric readouts get `font-variant-numeric: tabular-nums`.
- No colour literal may remain outside the `:root` token block, except inside `reports/`.
- Dark mode is out of scope; do not add `prefers-color-scheme` blocks.

## Verification setup

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

```bash
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && bundle exec jekyll build --quiet
```

Server runs detached on port 4001. No automated test suite exists; verification is a CSS/JS parse plus a scripted browser sweep at 1280x800 and 375x812. **Never press "Register your prediction" while testing** — `_data/supabase.yml` holds live credentials.

Count remaining literals at any point with:

```bash
grep -ohE "#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)" assets/css/main.css assets/css/quiz.css | sort -u | wc -l
```

---

### Task 1: Token layer and page chrome

**Files:**
- Create: `assets/css/tokens.css`
- Modify: `assets/css/main.css` — `:root` (1-8), `body` (20-30), `.site-nav__links a` (48-75), `main` (80-88), `h1`, `.footer-note`
- Modify: `_layouts/default.html` — stylesheet order
- Assets already downloaded: `assets/fonts/newsreader-latin.woff2`, `assets/fonts/newsreader-latin-ext.woff2`

**Interfaces:**
- Produces: every token named in Global Constraints, plus `--font-serif`, `--font-sans`, `--text-xs` … `--text-3xl`, `--space-1` … `--space-8`, `--radius-sm`, `--radius`, `--curve-fill`, `--curve-stroke`, `--curve-grid`, `--curve-handle`, `--measure`.

- [ ] **Step 1: Create the token sheet with the two `@font-face` rules**

`assets/css/tokens.css`, with the `unicode-range` values copied from Google's own stylesheet so latin-ext is fetched only when a page needs it:

```css
/* Newsreader, self-hosted. Upright only -- the italic cut cost 63KB and served
   one line of footer quote. unicode-range mirrors Google's subsetting so most
   visitors fetch newsreader-latin.woff2 and nothing else. */
@font-face {
  font-family: 'Newsreader';
  font-style: normal;
  font-weight: 400 600;
  font-display: swap;
  src: url('/pdoom-calculator/assets/fonts/newsreader-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC,
    U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215,
    U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Newsreader';
  font-style: normal;
  font-weight: 400 600;
  font-display: swap;
  src: url('/pdoom-calculator/assets/fonts/newsreader-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304,
    U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0,
    U+2113, U+2C60-2C7F, U+A720-A7FF;
}

:root {
  --paper: #faf9f6;
  --surface: #ffffff;
  --surface-sunken: #f3f1ea;
  --line: #e2ded4;
  --line-strong: #c9c3b5;

  --ink: #1c1a17;
  --ink-2: #55504a;
  --ink-3: #8a837a;

  --accent: #9a3412;
  --accent-ink: #ffffff;
  --accent-soft: #fbf1ef;

  --ok: #4a7c59;
  --ok-soft: #f0f5f0;
  --ok-ink: #2c4a34;
  --bad: #b04a3d;
  --bad-soft: #fbf1ef;
  --bad-ink: #7a2e24;
  --warn: #9a6a1c;

  /* Read by the bell-curve canvas at draw time, so its colours live here rather
     than hard-coded in the drawing code. */
  --curve-fill: rgba(154, 52, 18, 0.10);
  --curve-stroke: #9a3412;
  --curve-grid: #d8d3c8;
  --curve-handle: #1c1a17;

  --font-serif: 'Newsreader', Georgia, 'Times New Roman', serif;
  --font-sans: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;

  --text-xs: 0.8125rem;
  --text-sm: 0.9rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.375rem;
  --text-2xl: 1.75rem;
  --text-3xl: 2.5rem;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.5rem;
  --space-6: 2rem;
  --space-7: 3rem;
  --space-8: 4rem;

  --radius-sm: 4px;
  --radius: 6px;

  --measure: 65ch;
}
```

- [ ] **Step 2: Load the token sheet before everything else**

In `_layouts/default.html`, the `main.css` link must be preceded by tokens. Check the current head with:

```bash
grep -n "stylesheet" _layouts/default.html
```

Add immediately above the `main.css` line:

```html
<link rel="stylesheet" href="{{ '/assets/css/tokens.css' | relative_url }}">
```

- [ ] **Step 3: Rewrite the `main.css` root and body**

Replace the existing `:root` block (lines 1-8) and `body` block with:

```css
:root {
  color-scheme: light;
  font-family: var(--font-sans);
  line-height: 1.6;
  background: var(--paper);
  color: var(--ink);
}

body {
  margin: 0;
  padding: var(--space-7) var(--space-4) var(--space-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-5);
  background: var(--paper);
  overflow-x: hidden;
  overscroll-behavior-x: none;
}
```

Note `color-scheme` drops to `light` only: the page no longer has a dark treatment, and leaving `light dark` makes form controls render dark-on-light.

- [ ] **Step 4: Restyle the nav as text links**

Replace the `.site-nav__links a` rules:

```css
.site-nav__links a {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: 0;
  color: var(--ink-2);
  text-decoration: none;
  font-weight: 500;
  font-size: var(--text-xs);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border: none;
  background: none;
  transition: color 0.15s ease, box-shadow 0.15s ease;
}

.site-nav__links a:hover,
.site-nav__links a:focus {
  color: var(--ink);
  background: none;
  border-color: transparent;
}

.site-nav__links a[aria-current="page"] {
  color: var(--accent);
  background: none;
  border-color: transparent;
  box-shadow: inset 0 -2px 0 var(--accent);
}

.site-nav__links a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

- [ ] **Step 5: Strip the card chrome from `main`, restyle `h1` and the footer**

```css
main {
  width: min(780px, 100%);
  background: none;
  border: none;
  border-radius: 0;
  padding: 0;
}

h1 {
  margin: 0 0 var(--space-6);
  font-family: var(--font-serif);
  font-size: clamp(1.9rem, 4vw, var(--text-3xl));
  font-weight: 500;
  letter-spacing: -0.02em;
  line-height: 1.15;
  text-align: center;
  text-wrap: balance;
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--line);
}

.footer-note {
  font-family: var(--font-serif);
  font-size: var(--text-base);
  color: var(--ink-3);
  text-align: center;
  margin-top: var(--space-7);
  padding-top: var(--space-5);
  border-top: 1px solid var(--line);
  max-width: var(--measure);
  margin-left: auto;
  margin-right: auto;
}

.footer-note a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}
```

- [ ] **Step 6: Build and confirm the font actually loads**

```bash
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && bundle exec jekyll build --quiet
```

Then in the browser console on the served page:

```javascript
document.fonts.check('16px Newsreader')
```

Expected: `true`. If `false`, the `src:` path is wrong — compare against the built path in `_site/assets/fonts/`.

- [ ] **Step 7: Commit and push**

```bash
git add assets/css/tokens.css assets/css/main.css assets/fonts _layouts/default.html
git commit -m "Add the editorial token layer and restyle the page chrome"
git push origin restructure-quiz
```

---

### Task 2: Quiz surfaces

**Files:**
- Modify: `assets/css/quiz.css` — every rule from `.quiz-wizard` through `.quiz-result-actions`

**Interfaces:**
- Consumes: all tokens from Task 1.
- Produces: no new names; this task only re-expresses existing selectors against tokens.

- [ ] **Step 1: Convert the sticky header and P(doom) chip**

The chip is currently red-on-dark and unreadable on paper:

```css
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin: 0 0 var(--space-5);
  background: var(--paper);
  padding-top: var(--space-2);
}

.sticky-pdoom {
  display: flex;
  align-self: center;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-sm);
  background: var(--accent-soft);
  border: 1px solid var(--accent);
  flex-shrink: 0;
}

.sticky-pdoom__label {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.sticky-pdoom__value {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--accent);
  font-variant-numeric: tabular-nums;
}
```

- [ ] **Step 2: Convert the wizard header and flow list**

The three tiles become list rows, which is the defining move of this direction:

```css
.knowledge-quiz {
  margin-bottom: var(--space-6);
  padding: 0;
  border-radius: 0;
  background: none;
  border: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.wizard-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  text-align: center;
}

#wizardHeaderTitle {
  font-family: var(--font-serif);
  font-size: var(--text-2xl);
  font-weight: 500;
  letter-spacing: -0.01em;
  color: var(--ink);
}

.wizard-intro {
  margin: 0 auto;
  font-size: var(--text-base);
  color: var(--ink-2);
  max-width: 52ch;
}

.wizard-flow-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  border-top: 1px solid var(--line);
}

.wizard-flow-card {
  appearance: none;
  font: inherit;
  border: none;
  border-bottom: 1px solid var(--line);
  border-radius: 0;
  background: none;
  padding: var(--space-5) var(--space-1);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  text-align: left;
  color: inherit;
  cursor: pointer;
  transition: background 0.15s ease;
}

.wizard-flow-card:hover {
  background: var(--surface-sunken);
}

.wizard-flow-card:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.wizard-flow-card__title {
  margin: 0;
  font-family: var(--font-serif);
  font-size: var(--text-xl);
  font-weight: 500;
  color: var(--ink);
}

.wizard-flow-card__description {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--ink-2);
}

.wizard-flow-card__meta {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--ink-3);
}
```

- [ ] **Step 3: Convert buttons**

```css
.primary-button {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-sm);
  border: 1px solid var(--accent);
  background: var(--accent);
  color: var(--accent-ink);
  font-weight: 500;
  font-size: var(--text-base);
  cursor: pointer;
  transition: background 0.15s ease;
}

.primary-button:hover { background: #852d10; border-color: #852d10; }

.secondary-button {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-sm);
  border: 1px solid var(--line-strong);
  background: none;
  color: var(--ink-2);
  font-weight: 500;
  font-size: var(--text-base);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.secondary-button:hover { background: var(--surface-sunken); color: var(--ink); }

.primary-button:focus-visible,
.secondary-button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

`#852d10` is the one permitted literal outside `:root` — it is a hover shade of `--accent`. Add `--accent-hover: #852d10;` to `tokens.css` and reference it instead, so the constraint holds.

- [ ] **Step 4: Convert question rows and the answer states**

These are the states that are unreadable if skipped:

```css
.wizard-question {
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  background: none;
  border-radius: 0;
}

.wizard-checkbox,
.wizard-radio {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 44px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--ink-2);
  cursor: pointer;
}

.wizard-checkbox:hover,
.wizard-radio:hover { background: var(--surface-sunken); }

.quiz-option--correct {
  border-color: var(--ok);
  background: var(--ok-soft);
  color: var(--ok-ink);
}

.quiz-option--incorrect {
  border-color: var(--bad);
  background: var(--bad-soft);
  color: var(--bad-ink);
}

.quiz-option--missed {
  border-color: var(--warn);
  background: var(--surface-sunken);
  color: var(--ink-2);
}

.quiz-question--correct { box-shadow: inset 3px 0 0 var(--ok); }
.quiz-question--incorrect { box-shadow: inset 3px 0 0 var(--bad); }

.quiz-result--success { color: var(--ok-ink); }
.quiz-result--warning { color: var(--bad-ink); }
```

- [ ] **Step 5: Sweep the remaining literals in `quiz.css`**

```bash
grep -nE "#[0-9a-fA-F]{3,8}|rgba?\(" assets/css/quiz.css
```

Every hit must be replaced with the token that means the same thing. Expected after this step: no output.

- [ ] **Step 6: Verify in the browser**

Build, reload, then walk the chooser, a quiz, and the gate result at 1280x800. Confirm:

- Flow cards read as a list with hairline separators, not tiles.
- Ticking a wrong term after "Check my answers" produces a legible red row, and a correct one a legible green row.
- Every focusable element shows an accent outline on Tab.

- [ ] **Step 7: Commit and push**

```bash
git add assets/css/quiz.css assets/css/tokens.css
git commit -m "Restyle the quiz surfaces against the token layer"
git push origin restructure-quiz
```

---

### Task 3: Sliders and the canvas

**Files:**
- Modify: `assets/css/quiz.css` — `.factor-card`, `.slider-*`, `.metric-card`, `.driver-message`, `.submission*`
- Modify: `index.html:2759-2800` — the canvas drawing colours

**Interfaces:**
- Consumes: `--curve-fill`, `--curve-stroke`, `--curve-grid`, `--curve-handle` from Task 1.
- Produces: `readCurveColors()` returning `{ fill, stroke, grid, handle }`.

- [ ] **Step 1: Read the canvas colours from the tokens**

Add above the drawing function in `index.html`:

```javascript
    // The curve colours live in the stylesheet so the canvas cannot drift from the
    // rest of the page -- and so a later dark mode fixes the canvas for free.
    // Resolved once per recalc rather than per frame; getComputedStyle is not cheap.
    let curveColors = null;
    function readCurveColors() {
      if (curveColors) return curveColors;
      const styles = getComputedStyle(document.documentElement);
      const pick = (name, fallback) => (styles.getPropertyValue(name).trim() || fallback);
      curveColors = {
        fill: pick('--curve-fill', 'rgba(154, 52, 18, 0.10)'),
        stroke: pick('--curve-stroke', '#9a3412'),
        grid: pick('--curve-grid', '#d8d3c8'),
        handle: pick('--curve-handle', '#1c1a17')
      };
      return curveColors;
    }
```

- [ ] **Step 2: Replace the five hard-coded colours**

At `index.html:2759-2800`, substitute:

| Current | Replacement |
|---|---|
| `ctx.fillStyle = 'rgba(110, 177, 255, 0.18)';` | `ctx.fillStyle = readCurveColors().fill;` |
| `ctx.strokeStyle = 'rgba(110, 177, 255, 0.85)';` | `ctx.strokeStyle = readCurveColors().stroke;` |
| `ctx.strokeStyle = 'rgba(240, 245, 255, 0.35)';` | `ctx.strokeStyle = readCurveColors().grid;` |
| `ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';` | `ctx.strokeStyle = readCurveColors().grid;` |
| `ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';` | `ctx.fillStyle = readCurveColors().handle;` |

- [ ] **Step 3: Convert the factor cards, sliders and metrics**

```css
.factor-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: var(--space-5);
}

.slider-caption {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--ink-3);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.slider-value {
  color: var(--ink);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.slider-bellcurve {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface-sunken);
}

input[type="range"] { accent-color: var(--accent); }

.metric-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: var(--space-4);
}

.metric-value {
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--accent);
  font-variant-numeric: tabular-nums;
}

.uncertainty-note { font-size: var(--text-xs); color: var(--ink-3); }

.driver-message {
  background: var(--surface-sunken);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: var(--space-4);
  color: var(--ink-2);
}
```

- [ ] **Step 4: Verify the curves are visible**

Build, run a quiz to the sliders, and in the console:

```javascript
JSON.stringify(readCurveColors())
```

Expected: the four token values, none empty. Then confirm visually that the curve, its gridlines and the drag handle are all distinguishable against the light card, and that dragging still moves the midpoint.

- [ ] **Step 5: Commit and push**

```bash
git add assets/css/quiz.css index.html
git commit -m "Restyle the sliders and source the curve colours from tokens"
git push origin restructure-quiz
```

---

### Task 4: Companion pages and full verification

**Files:**
- Modify: `about.html`, `stats.html`, `embed.html` — only if a page-local style breaks on paper

- [ ] **Step 1: Check the three companion pages**

Serve, then open each of `/about/`, `/stats/` and `/embed.html`. They inherit `main.css`, so most of the change is automatic. Look for any inline `style=` attribute or page-local `<style>` block that still assumes a dark ground:

```bash
grep -n "style=\|<style" about.html stats.html embed.html
```

Fix any literal colour found by replacing it with the matching token.

- [ ] **Step 2: Confirm no literals survive**

```bash
grep -nE "#[0-9a-fA-F]{3,8}|rgba?\(" assets/css/main.css assets/css/quiz.css | grep -v "^assets/css/tokens.css"
```

Expected: no output outside `tokens.css`.

- [ ] **Step 3: Desktop sweep at 1280x800**

Walk beginner, medium, expert-pass, expert-fail, both back buttons and the sliders. Confirm zero horizontal overflow, no console errors, and that every text/ground pairing is legible.

- [ ] **Step 4: Mobile sweep at 375x812**

Reload after resizing. Confirm the same paths, plus: list rows remain comfortable, buttons stack rather than truncate, tap targets stay at 44px or more, and the sticky P(doom) chip is readable.

- [ ] **Step 5: Commit and push**

```bash
git add -A
git commit -m "Carry the editorial styling across the companion pages"
git push origin restructure-quiz
```

---

## Self-review notes

- Spec coverage: token layer (Task 1 step 1), typography and self-hosted font (Task 1 steps 1-2, 5), palette and semantic states (Tasks 1-2), canvas (Task 3 steps 1-2), components (Tasks 2-3), accessibility focus rings and tap targets (Tasks 1-2, verified Task 4), shared-page scope (Task 4). Dark mode and `reports/` are excluded and no task touches them.
- `--accent-hover` is introduced in Task 2 step 3 rather than Task 1, because that is where the need appears; the step says to add it to `tokens.css` so no literal escapes.
- Names used consistently: `readCurveColors()`, `--curve-fill`/`--curve-stroke`/`--curve-grid`/`--curve-handle`, `--surface-sunken`, `--line-strong`.
