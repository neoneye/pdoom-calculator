# Quiz Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire the "Decide the right level for me" path, let visitors pick beginner or medium freely, and put the existing 30-term knowledge check in front of the expert quiz as an advisory gate whose verdict is recorded on the submission.

**Architecture:** Everything lives in the one inline `<script>` in `index.html` (lines 132–2923). The knowledge check stays exactly as written; only its position in the flow, its result screen and its bookkeeping change. The flow object `decide` becomes `expert-check`, hidden from the chooser and reachable only by choosing the expert path. A module-level `gateState` carries the score forward to the submission payload.

**Tech Stack:** Jekyll (Ruby 3.3) static site, vanilla ES2015+ JavaScript inline in `index.html`, Supabase JS v2 for submissions.

## Global Constraints

- All JavaScript changes go in the single inline `<script>` block of `index.html`. No new files, no build step, no dependencies.
- Match surrounding style: 2-space indent, `const`/`let`, no semicolonless lines, comments only where they explain *why*.
- The gate is **advisory**. Every failing branch must still offer a way into the expert quiz.
- Expert threshold is `26` out of `30`. Recommendation bands are unchanged: 0–20 beginner, 21–25 medium, 26–30 expert.
- `quiz_flow_id` keeps its existing meaning — the quiz actually taken. The gate never writes to it.
- **Do not press "Register your prediction" while testing.** `_data/supabase.yml` holds live production credentials; a test click writes a real row into the dataset the report is built from. Verify payloads by calling `buildSubmissionPayload()` in the browser console instead.

## Verification setup

Two checks are used throughout. Run both after every code step.

**Syntax check** — extracts the inline script and parses it:

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

**Browser check** — serve the site and drive it:

```bash
bundle exec jekyll serve
```

Then open `http://127.0.0.1:4000/pdoom-calculator/`. This project has no automated test suite; verification is a syntax parse plus a scripted click-through in the browser. Each task below states the exact clicks and the exact expected result.

---

### Task 1: Retire `decide`, route the expert path through the gate

**Files:**
- Modify: `index.html` — flow definitions (~line 399), `wizardHeaderDefaults` (~1162), `breadcrumbLabels` (~1170), `getBreadcrumbItems`/`getActiveBreadcrumbIndex` (~1223–1239), `validHashes` (~1272), `navigateTo` (~1281), `renderWizardFlowOptions` (~1433), `updateWizardHeader` (~2001), static chooser copy (~59)

**Interfaces:**
- Produces: flow id `expert-check` (kind `knowledge-check`, `hiddenFromChooser: true`); `navigateTo(targetId, skipHash)` redirects `expert`, `expert-check` and legacy `decide` to the gate; `getBreadcrumbItems()` returns a variable-length array whose gate crumb is present only on the expert path.

- [ ] **Step 1: Replace the `decide` flow object with the hidden `expert-check` gate**

In `index.html`, the first entry of `const quizFlows = [` (~line 399) currently reads:

```javascript
      {
        id: 'decide',
        label: 'Decide the right level for me',
        description: 'Let us place you on the right lane with a bite-sized knowledge check.',
        meta: '30 terms · ~5 minutes',
        recommended: true,
        kind: 'knowledge-check',
        questions: knowledgeCheckQuestions
      },
```

Replace it with:

```javascript
      // The expert gate. Not offered as a card — reaching it means the visitor
      // asked for the expert quiz, and the score decides which level we then
      // recommend. Advisory: the expert quiz stays available either way.
      {
        id: 'expert-check',
        label: 'Expert check',
        description: 'Spot the AI-related terms and avoid the decoys.',
        meta: '30 terms · ~5 minutes',
        hiddenFromChooser: true,
        kind: 'knowledge-check',
        questions: knowledgeCheckQuestions
      },
```

- [ ] **Step 2: Hide the gate from the chooser grid**

In `renderWizardFlowOptions` (~line 1433), change:

```javascript
      quizFlows.forEach((flow) => {
```

to:

```javascript
      quizFlows.filter(flow => !flow.hiddenFromChooser).forEach((flow) => {
```

In the same function, change the click handler from:

```javascript
        button.addEventListener('click', () => handleFlowSelection(flow.id));
```

to:

```javascript
        // navigateTo, not handleFlowSelection, so the expert card lands on the gate.
        button.addEventListener('click', () => navigateTo(flow.id));
```

- [ ] **Step 3: Flag the expert card so the check is not a surprise**

In the `expert` flow object (~line 845), change:

```javascript
        meta: '8 questions · ~10 minutes',
```

to:

```javascript
        meta: 'Knowledge check first · 8 questions · ~10 minutes',
```

- [ ] **Step 4: Route every expert entry point through the gate**

In `navigateTo` (~line 1281), replace this block:

```javascript
      if (targetId === 'decide') {
        handleFlowSelection('decide', skipHash);
        return;
      }
```

with:

```javascript
      // The expert path always opens the gate first; the gate's own buttons call
      // handleFlowSelection('expert') directly to enter the quiz. 'decide' is the
      // retired flow id, kept so old links still resolve somewhere sensible.
      if (targetId === 'expert' || targetId === 'expert-check' || targetId === 'decide') {
        handleFlowSelection('expert-check', skipHash);
        return;
      }
```

This must sit **above** the existing `if (quizFlowIds.includes(targetId))` block so `expert` is caught first.

- [ ] **Step 5: Update the hash allow-list**

At ~line 1272, change:

```javascript
    const validHashes = ['start', 'decide', 'beginner', 'medium', 'expert', 'sliders'];
```

to:

```javascript
    const validHashes = ['start', 'expert-check', 'decide', 'beginner', 'medium', 'expert', 'sliders'];
```

- [ ] **Step 6: Update the breadcrumb labels and make the gate crumb conditional**

At ~line 1170, in `breadcrumbLabels`, replace the line:

```javascript
      decide: 'Decide for me',
```

with:

```javascript
      'expert-check': 'Expert check',
```

Then replace `getBreadcrumbItems` and `getActiveBreadcrumbIndex` (~lines 1223–1239) entirely with:

```javascript
    function getBreadcrumbItems() {
      const quizId = quizFlowIds.includes(predictedQuizFlowId) ? predictedQuizFlowId : 'beginner';
      const items = [{ id: 'start', label: breadcrumbLabels.start }];
      // The gate crumb appears only once the visitor has taken the expert path,
      // and stays in the trail afterwards even if the score routed them lower.
      if (wizardState.flowId === 'expert-check' || gateState) {
        items.push({ id: 'expert-check', label: breadcrumbLabels['expert-check'] });
      }
      items.push({ id: quizId, label: breadcrumbLabels[quizId] || 'Quiz' });
      items.push({ id: 'sliders', label: breadcrumbLabels.sliders });
      return items;
    }

    function getActiveBreadcrumbIndex() {
      const items = getBreadcrumbItems();
      const flowId = wizardState.flowId;
      if (flowId === 'expert-check') {
        return items.findIndex(item => item.id === 'expert-check');
      }
      if (flowId === 'sliders') return items.length - 1;
      if (quizFlowIds.includes(flowId)) return items.length - 2;
      return 0;
    }
```

`gateState` does not exist yet — declare it now so this step parses. Immediately above `let predictedQuizFlowId = 'beginner';` (~line 1179), add:

```javascript
    // What the expert gate decided, or null if it has not run. Carried into the
    // submission so a verified expert can be told from a self-declared one.
    let gateState = null;
```

- [ ] **Step 7: Update the gate's in-quiz header copy**

In `updateWizardHeader` (~line 2001), replace:

```javascript
      if (flow.id === 'decide') {
        titleEl.textContent = 'Decide the right level';
        introEl.textContent = `Take the quick knowledge check so we can route you to beginner, medium, or expert${metaText}.`;
        return;
      }
```

with:

```javascript
      if (flow.id === 'expert-check') {
        titleEl.textContent = 'Expert check';
        introEl.textContent = `Spot the AI-related terms and avoid the decoys. Your score picks the level we recommend — the expert quiz stays open either way${metaText}.`;
        return;
      }
```

- [ ] **Step 8: Update the chooser copy in both places**

At ~line 1162, replace:

```javascript
    const wizardHeaderDefaults = {
      title: 'Choose your quiz path',
      intro: 'Start by selecting a path: let us decide the right level (recommended) or jump directly into the beginner, medium, or expert quiz.'
    };
```

with:

```javascript
    const wizardHeaderDefaults = {
      title: 'Choose your quiz path',
      intro: 'Pick a level. Beginner and medium start straight away; the expert quiz opens with a short knowledge check.'
    };
```

The same sentence is hard-coded in the static HTML at ~line 59. Replace:

```html
          Start by selecting a path: let us decide the right level (recommended) or jump directly into the beginner, medium, or expert quiz.
```

with:

```html
          Pick a level. Beginner and medium start straight away; the expert quiz opens with a short knowledge check.
```

- [ ] **Step 9: Run the syntax check**

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

Expected: `SYNTAX OK`

- [ ] **Step 10: Verify in the browser**

Start the server, open `http://127.0.0.1:4000/pdoom-calculator/`, and confirm all five:

1. The chooser shows exactly four cards: Beginner quiz, Medium quiz, Expert quiz, Sliders. No "Decide the right level for me", no "Recommended" badge.
2. The Expert card's meta line reads `Knowledge check first · 8 questions · ~10 minutes`.
3. Clicking **Beginner quiz** opens the beginner questions directly. Go back to Start.
4. Clicking **Expert quiz** opens the 30-term check titled "Expert check", *not* the expert questions. The breadcrumb reads `Start › Expert check › Beginner quiz › Sliders`.
5. Loading `#expert`, `#expert-check` and `#decide` directly each opens the check.

- [ ] **Step 11: Commit**

```bash
git add index.html
git commit -m "Route the expert path through the knowledge check"
```

---

### Task 2: Gate result — record the verdict, offer both doors

**Files:**
- Modify: `index.html` — `levelJumpRules` (~line 392), `renderLevelRecommendationButton` (~1618), `runKnowledgeCheck` (~1636), `handleWizardSubmit` knowledge-check branch (~2131), `handleWizardReset` (~2091), `navigateTo` start branch (~1281)

**Interfaces:**
- Consumes: `gateState` (declared in Task 1), `levelJumpRules`, `handleFlowSelection(flowId)`.
- Produces: `gateState = { score: number, recommendedLevel: 'beginner'|'medium'|'expert', expertVerified: boolean }` or `null`; `EXPERT_GATE_MIN_SCORE = 26`; `resetGateState()`; `renderGateResultActions(recommendedFlowId)`.

- [ ] **Step 1: Add the threshold constant and the reset helper**

Directly below the `let gateState = null;` declaration added in Task 1, add:

```javascript
    // A verified expert clears 26 of the 30 terms. Ticking nothing already scores
    // 15, since the 15 decoys are then correctly left alone.
    const EXPERT_GATE_MIN_SCORE = 26;

    function resetGateState() {
      gateState = null;
    }
```

- [ ] **Step 2: Drop the now-unused `label` from the routing rules**

At ~line 392, replace:

```javascript
    const levelJumpRules = [
      { min: 0, max: 20, flowId: 'beginner', label: 'Jump to beginner quiz' },
      { min: 21, max: 25, flowId: 'medium', label: 'Jump to medium quiz' },
      { min: 26, max: 30, flowId: 'expert', label: 'Jump to expert quiz' }
    ];
```

with:

```javascript
    const levelJumpRules = [
      { min: 0, max: 20, flowId: 'beginner' },
      { min: 21, max: 25, flowId: 'medium' },
      { min: 26, max: 30, flowId: 'expert' }
    ];
```

- [ ] **Step 3: Replace the single jump button with the two-door result**

Replace `renderLevelRecommendationButton` (~line 1618) entirely:

```javascript
    function renderGateResultActions(recommendedFlowId) {
      const actionsEl = document.getElementById('wizardResultActions');
      if (!actionsEl) return;
      actionsEl.innerHTML = '';
      // Clearing the bar means one door. Falling short means two: the level the
      // score suggests, and the expert quiz anyway — recorded as self-declared.
      const buttons = recommendedFlowId === 'expert'
        ? [{ flowId: 'expert', label: 'Start expert quiz', className: 'primary-button' }]
        : [
            { flowId: recommendedFlowId, label: `Take ${recommendedFlowId} quiz`, className: 'primary-button' },
            { flowId: 'expert', label: 'Continue to expert anyway', className: 'secondary-button' }
          ];
      buttons.forEach(({ flowId, label, className }) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = className;
        button.textContent = label;
        button.addEventListener('click', () => handleFlowSelection(flowId));
        actionsEl.appendChild(button);
      });
      actionsEl.hidden = false;
    }
```

- [ ] **Step 4: Record the verdict and stop calibrating the sliders**

At the end of `runKnowledgeCheck` (~line 1703), replace this block:

```javascript
      const calibratedScore = Math.max(0, score - falseSelections);
      const normalizedScore = knowledgeCheckMaxScore > 0 ? calibratedScore / knowledgeCheckMaxScore : 0;
      const boundedScore = clamp(normalizedScore, 0, 1);
      const confidenceSpread = CONFIDENCE_HIGH + (1 - boundedScore) * (CONFIDENCE_LOW - CONFIDENCE_HIGH);
      const percentCorrect = questionItemsTotal > 0 ? Math.max(0, Math.min(100, Math.round((questionsCorrect / questionItemsTotal) * 100))) : 0;
      const scoreMessage = questionItemsTotal > 0 && questionsCorrect === questionItemsTotal
        ? `You have ${questionItemsTotal} of ${questionItemsTotal} answers correct. Score 100%.`
        : `You have ${questionsCorrect} of ${questionItemsTotal} answers correct. Score ${percentCorrect}%.`;

      applyConfidenceCalibration(confidenceSpread);
      resultEl.innerHTML = `${scoreMessage}`;
      resultEl.classList.remove('quiz-result--warning');
      resultEl.classList.add('quiz-result--success');
      const recommended = levelJumpRules.find(rule => questionsCorrect >= rule.min && questionsCorrect <= rule.max);
      if (recommended) {
        setPredictedQuizFlow(recommended.flowId);
      } else {
        setPredictedQuizFlow('beginner');
      }
      renderLevelRecommendationButton(questionsCorrect);
    }
```

with:

```javascript
      // The gate no longer touches the sliders: whichever quiz follows overwrites
      // both spread and midpoint immediately, so any calibration here is dead.
      const percentCorrect = questionItemsTotal > 0 ? Math.max(0, Math.min(100, Math.round((questionsCorrect / questionItemsTotal) * 100))) : 0;
      const scoreMessage = questionItemsTotal > 0 && questionsCorrect === questionItemsTotal
        ? `You have ${questionItemsTotal} of ${questionItemsTotal} answers correct. Score 100%.`
        : `You have ${questionsCorrect} of ${questionItemsTotal} answers correct. Score ${percentCorrect}%.`;

      const recommended = levelJumpRules.find(rule => questionsCorrect >= rule.min && questionsCorrect <= rule.max);
      const recommendedFlowId = recommended ? recommended.flowId : 'beginner';
      gateState = {
        score: questionsCorrect,
        recommendedLevel: recommendedFlowId,
        expertVerified: questionsCorrect >= EXPERT_GATE_MIN_SCORE
      };

      const verdict = recommendedFlowId === 'expert'
        ? ' That clears the expert bar.'
        : ` That suggests the ${recommendedFlowId} quiz is the better fit.`;
      resultEl.innerHTML = `${scoreMessage}${verdict}`;
      resultEl.classList.remove('quiz-result--warning');
      resultEl.classList.add('quiz-result--success');
      setPredictedQuizFlow(recommendedFlowId);
      renderGateResultActions(recommendedFlowId);
    }
```

Note this deletes the only uses of `score`, `falseSelections`, `calibratedScore` and `knowledgeCheckMaxScore`. Leave `score` and `falseSelections` where they are accumulated inside the loop — removing them is a wider edit than this task needs — but delete the now-orphaned `const knowledgeCheckMaxScore = ...` block at ~line 382 if nothing else references it. Confirm with:

```bash
grep -n "knowledgeCheckMaxScore" index.html
```

- [ ] **Step 5: Stop the gate from claiming to be a quiz answer**

In `handleWizardSubmit` (~line 2131), the knowledge-check branch contains:

```javascript
        runKnowledgeCheck();
        latestQuizData = buildQuizAnswersPayload(wizardState.flowId, flow);
```

Delete the second line. The gate is not a level quiz; letting it write `latestQuizData` would stamp a submission with `quiz_flow_id: 'expert-check'` if the visitor jumped straight to the sliders afterwards. The score survives in `gateState` instead. The line becomes:

```javascript
        runKnowledgeCheck();
```

- [ ] **Step 6: Clear the verdict when the visitor starts over**

In `navigateTo` (~line 1281), the `start` branch currently begins:

```javascript
      if (targetId === 'start') {
        wizardState.flowId = null;
        resetWizardResult();
```

Insert `resetGateState();` so it reads:

```javascript
      if (targetId === 'start') {
        wizardState.flowId = null;
        resetGateState();
        resetWizardResult();
```

In `handleWizardReset` (~line 2091), after `clearStoredWizardAnswers();` add `resetGateState();`:

```javascript
      clearStoredWizardAnswers();
      resetGateState();
      wizardState.flowId = null;
```

- [ ] **Step 7: Run the syntax check**

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

Expected: `SYNTAX OK`

- [ ] **Step 8: Verify the failing branch in the browser**

Open the site, click **Expert quiz**, tick nothing, click **Check my answers**.

Expected: score reads `15 of 30` (50%), followed by "That suggests the beginner quiz is the better fit." Two buttons appear: **Take beginner quiz** (primary) and **Continue to expert anyway** (secondary). In the console, `gateState` reads:

```javascript
{ score: 15, recommendedLevel: 'beginner', expertVerified: false }
```

Click **Continue to expert anyway** — the expert questions open and the breadcrumb reads `Start › Expert check › Expert quiz › Sliders`.

- [ ] **Step 9: Verify the passing branch in the browser**

Return to Start, click **Expert quiz**, and tick every genuinely AI-related term (the 15 with `aiRelated: true`). Click **Check my answers**.

Expected: score reads `30 of 30` (100%), followed by "That clears the expert bar." Exactly one button: **Start expert quiz**. Console:

```javascript
{ score: 30, recommendedLevel: 'expert', expertVerified: true }
```

- [ ] **Step 10: Verify the verdict is cleared on reset**

Click the **Start** breadcrumb. In the console, `gateState` is `null` and the breadcrumb has dropped the "Expert check" crumb.

- [ ] **Step 11: Commit**

```bash
git add index.html
git commit -m "Record the expert gate verdict and offer both doors"
```

---

### Task 3: Carry the verdict into the submission

**Files:**
- Modify: `index.html` — `buildSubmissionPayload` (~line 2299), the Supabase insert (~2344)
- Modify: `database.md` — migration SQL and column reference

**Interfaces:**
- Consumes: `gateState`, `latestQuizData`.
- Produces: `buildSubmissionPayload()` now returns the complete insert row, including `quiz_flow_id`, `quiz_answers`, `gate_score`, `gate_recommended_level` and `expert_verified`.

- [ ] **Step 1: Move the quiz fields into the payload builder and add the gate fields**

Replace `buildSubmissionPayload` (~line 2299) with:

```javascript
    function buildSubmissionPayload() {
      if (!latestSnapshot) return null;
      const { factors, lowerProduct, upperProduct, midpointProduct, p10, p90 } = latestSnapshot;
      return {
        submitted_at: new Date().toISOString(),
        factors: factors.map(({ key, label, lower, upper, midpoint, spread }) => ({
          key,
          label,
          lower,
          upper,
          midpoint,
          spread
        })),
        summary: {
          lower: lowerProduct,
          upper: upperProduct,
          midpoint: midpointProduct,
          p10,
          p90
        },
        quiz_flow_id: latestQuizData ? latestQuizData.flow_id : null,
        quiz_answers: latestQuizData ? latestQuizData.answers : null,
        // Null when the expert gate never ran, which is every beginner and medium
        // submission that went straight to its quiz.
        gate_score: gateState ? gateState.score : null,
        gate_recommended_level: gateState ? gateState.recommendedLevel : null,
        expert_verified: gateState ? gateState.expertVerified : null
      };
    }
```

- [ ] **Step 2: Insert the payload as-is**

At ~line 2344, replace:

```javascript
        const { error } = await supabaseClient
          .from(SUBMISSIONS_TABLE)
          .insert({
            factors: payload.factors,
            summary: payload.summary,
            submitted_at: payload.submitted_at,
            quiz_flow_id: latestQuizData ? latestQuizData.flow_id : null,
            quiz_answers: latestQuizData ? latestQuizData.answers : null
          });
```

with:

```javascript
        const { error } = await supabaseClient
          .from(SUBMISSIONS_TABLE)
          .insert(payload);
```

- [ ] **Step 3: Run the syntax check**

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

Expected: `SYNTAX OK`

- [ ] **Step 4: Verify the payload without writing to the database**

**Do not click "Register your prediction".** The anon key is live.

Run the beginner path end to end (Start › Beginner quiz › answer everything › Submit) so the sliders appear, then in the console:

```javascript
buildSubmissionPayload()
```

Expected: `quiz_flow_id: 'beginner'`, `quiz_answers` a populated array, and `gate_score`, `gate_recommended_level`, `expert_verified` all `null`.

Then return to Start, run Expert quiz › tick nothing › Check my answers › **Continue to expert anyway** › answer the expert quiz › Submit, and in the console:

```javascript
buildSubmissionPayload()
```

Expected: `quiz_flow_id: 'expert'`, `gate_score: 15`, `gate_recommended_level: 'beginner'`, `expert_verified: false`.

Finally return to Start, run Expert quiz › tick nothing › **Take beginner quiz** › answer it › Submit, and check that `buildSubmissionPayload()` gives `quiz_flow_id: 'beginner'` with `gate_score: 15` still attached — this is the rerouted case the report could not previously see.

- [ ] **Step 5: Document the migration**

In `database.md`, extend the `CREATE TABLE` in section 2 so a fresh project gets the columns:

```sql
CREATE TABLE submissions (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  submitted_at timestamptz NOT NULL DEFAULT now(),
  factors jsonb,
  summary jsonb,
  quiz_flow_id text,
  quiz_answers jsonb,
  gate_score int,
  gate_recommended_level text,
  expert_verified boolean
);
```

Then add a new section immediately after section 2, before "## 3. Grant Data API access":

```markdown
### Migrating an existing table

The expert gate columns were added on 19 Aug 2026. Existing projects need:

```sql
ALTER TABLE submissions
  ADD COLUMN IF NOT EXISTS gate_score int,
  ADD COLUMN IF NOT EXISTS gate_recommended_level text,
  ADD COLUMN IF NOT EXISTS expert_verified boolean;
```

Rows submitted before this date keep `NULL` in all three, which is also what a
beginner or medium submission that never met the gate records.
```

Extend the column reference table at the bottom with three rows, and correct the `quiz_flow_id` description, which still names the retired `decide` path:

```markdown
| `quiz_flow_id` | text | Which quiz was taken: `beginner`, `medium`, `expert`, or `null` if skipped. Historical rows may hold `decide`, the knowledge-check path retired on 19 Aug 2026. |
| `quiz_answers` | jsonb | Array of `{question_id, type, value/values}` — the user's quiz selections |
| `gate_score` | int | Expert gate score, 0–30. `null` if the gate never ran. |
| `gate_recommended_level` | text | Level the gate recommended: `beginner`, `medium` or `expert`. `null` if the gate never ran. |
| `expert_verified` | boolean | True when `gate_score >= 26`. A submission with `quiz_flow_id = 'expert'` and `expert_verified = false` is a self-declared expert. `null` if the gate never ran. |
```

- [ ] **Step 6: Commit**

```bash
git add index.html database.md
git commit -m "Record the gate verdict on each submission"
```

---

### Task 4: Update the flow documentation and verify end to end

**Files:**
- Modify: `index.html` — the HTML comment block at lines 6–34

- [ ] **Step 1: Rewrite the flow description at the top of the file**

The comment at `index.html:6` describes the retired design. Replace lines 7–20 — from `Similar to a **Windows Wizard**.` through the `If the number of correct answers are 26..30 then show an **expert** quiz.` line — with:

```
Similar to a **Windows Wizard**. First page is the welcome page.
From there the visitor picks a level: **beginner**, **medium** or **expert**,
or skips to the **sliders**.

Beginner and medium open their quiz directly. Expert opens a knowledge check
first: 30 terms, 15 genuinely AI-related and 15 decoys. Each term scores
independently — a ticked AI term and an unticked decoy both count — so ticking
nothing already scores 15.

The score picks the level we recommend:
0..20 -> **beginner**, 21..25 -> **medium**, 26..30 -> **expert**.

The check is advisory. Below 26 the visitor is offered the recommended quiz and
a "continue to expert anyway" button; taking that second door records the
submission as a self-declared rather than verified expert (`expert_verified`
in the database). The check no longer pre-sets the sliders, because whichever
quiz follows overwrites both spread and midpoint anyway.
```

Leave the "I have omitted these areas" and "Gaps / potential future questions" paragraphs below untouched, except for the line reading `- Instrumental convergence / power-seeking — Only in the knowledge check (paperclip maximizer), not explored as a quiz topic.` which stays accurate as written.

- [ ] **Step 2: Run the syntax check**

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

Expected: `SYNTAX OK`

- [ ] **Step 3: Confirm the retired flow id is gone from the app**

```bash
grep -n "'decide'" index.html
```

Expected: exactly one hit, the legacy-hash branch in `navigateTo`, plus the entry in `validHashes`. No flow object, no breadcrumb label, no header branch. `prepare_report_data.py` keeps its two `decide` references — those read historical rows and must not change.

- [ ] **Step 4: Full click-through**

With the server running, walk all six paths and confirm each:

1. Beginner → quiz → sliders. Breadcrumb never shows "Expert check".
2. Medium → quiz → sliders. Same.
3. Expert → check → 30/30 → "Start expert quiz" → expert quiz → sliders.
4. Expert → check → 15/30 → "Take medium quiz" is *not* offered (15 lands in the beginner band); "Take beginner quiz" and "Continue to expert anyway" are.
5. Expert → check → score 21–25 by ticking a partial set → "Take medium quiz" and "Continue to expert anyway".
6. Sliders card → sliders directly, no quiz, `buildSubmissionPayload()` shows all five quiz and gate fields `null`.

Also confirm back/forward navigation: from the expert quiz, press the browser Back button and land on the check, not on a blank panel.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Describe the restructured quiz flow at the top of index.html"
```

---

## Self-review notes

- Spec coverage: chooser (Task 1), gate content and thresholds unchanged (Task 1 step 1, Task 2 step 2), advisory two-door result (Task 2 step 3), no slider calibration (Task 2 step 4), three new columns (Task 3), `database.md` (Task 3 step 5), comment block (Task 4). Out-of-scope items — sliders path, level quiz content, `prepare_report_data.py` — are untouched and Task 4 step 3 asserts it.
- `gateState` is declared in Task 1 (needed by `getBreadcrumbItems`) and populated in Task 2. A worker doing Task 1 alone will see it stay `null`, which is correct.
- Names used consistently throughout: `gateState`, `resetGateState`, `EXPERT_GATE_MIN_SCORE`, `renderGateResultActions`, `expert-check`, `hiddenFromChooser`, `gate_score`, `gate_recommended_level`, `expert_verified`.
