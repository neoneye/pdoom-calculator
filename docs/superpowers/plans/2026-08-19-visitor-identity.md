# Signed Visitor Identity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give each browser a non-extractable ECDSA P-256 identity, sign every submission with it, store the key and signature in Supabase, and verify the signatures offline when the report is built.

**Architecture:** Identity lives in IndexedDB (`pdoom-identity`), created lazily on the first successful submission. The client builds a fixed-format canonical string, signs it, and stores that exact string alongside the signature so the Python verifier never has to reconstruct it. Verification runs in `prepare_report_data.py` using `cryptography`.

**Tech Stack:** Vanilla JS + WebCrypto + IndexedDB inline in `index.html`; Python 3 + `cryptography` in `prepare_report_data.py`; Supabase Postgres.

## Global Constraints

- Identity work must never block, delay or fail a submission. Every failure path submits with the four identity columns `null`.
- No UI signal that a visitor has submitted before: status text unchanged, counter never rendered, button never disabled.
- Signed string format is exactly `pdoom/1|k=|n=|t=|m=|lo=|hi=|p10=|p90=|f=|q=|g=` with fields in that order, numbers via `String(value)`, absent values as empty string.
- The counter persists only after a successful insert.
- **Do not press "Register your prediction" while testing.** `_data/supabase.yml` holds live production credentials. Verify by calling the builder functions in the console.

## Verification setup

```bash
sed -n '/^  <script>$/,/^  <\/script>$/p' index.html | sed '1d;$d' > /tmp/pdoom-app.js && node --check /tmp/pdoom-app.js && echo "SYNTAX OK"
```

```bash
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && bundle exec jekyll build --quiet
```

Server runs detached on port 4001. This project has no automated test suite; verification is a syntax parse, a Python round-trip test with a known keypair, and a scripted browser click-through.

---

### Task 1: Identity store

**Files:**
- Modify: `index.html` — new identity section near the other storage keys (~line 1105)

**Interfaces:**
- Produces: `async function loadIdentity()` → `{ privateKey, visitorKey, submitCount }` or `null`; `async function persistSubmitCount(count)` → void; `IDENTITY_DB_NAME = 'pdoom-identity'`, `IDENTITY_STORE = 'identity'`, `IDENTITY_RECORD_KEY = 'v1'`.
- `loadIdentity()` never throws. It returns `null` when WebCrypto or IndexedDB is unavailable or errors.

- [ ] **Step 1: Add the identity module**

Insert after the `SLIDERS_CONTAINER_ID` constant (~line 1105):

```javascript
    // --- Visitor identity ------------------------------------------------
    // A non-extractable ECDSA P-256 keypair, generated lazily on the first
    // successful submission and kept in IndexedDB. The public key identifies the
    // browser across submissions; the private key signs each one so the grouping
    // in the published export can be verified by anyone who downloads it.
    //
    // localStorage cannot hold this: a non-extractable CryptoKey is not a string.
    // The counter shares the record so key and count cannot drift apart.
    const IDENTITY_DB_NAME = 'pdoom-identity';
    const IDENTITY_STORE = 'identity';
    const IDENTITY_RECORD_KEY = 'v1';

    function openIdentityDb() {
      return new Promise((resolve, reject) => {
        if (typeof indexedDB === 'undefined') {
          reject(new Error('IndexedDB unavailable'));
          return;
        }
        const request = indexedDB.open(IDENTITY_DB_NAME, 1);
        request.onupgradeneeded = () => {
          const db = request.result;
          if (!db.objectStoreNames.contains(IDENTITY_STORE)) {
            db.createObjectStore(IDENTITY_STORE);
          }
        };
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error || new Error('IndexedDB open failed'));
        request.onblocked = () => reject(new Error('IndexedDB blocked'));
      });
    }

    function identityRecord(db, mode, action) {
      return new Promise((resolve, reject) => {
        const tx = db.transaction(IDENTITY_STORE, mode);
        const store = tx.objectStore(IDENTITY_STORE);
        const request = action(store);
        tx.onabort = () => reject(tx.error || new Error('IndexedDB transaction aborted'));
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }

    function base64UrlFromBytes(bytes) {
      let binary = '';
      bytes.forEach((byte) => { binary += String.fromCharCode(byte); });
      return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    }

    function bytesFromBase64Url(value) {
      const padded = value.replace(/-/g, '+').replace(/_/g, '/');
      const binary = atob(padded + '==='.slice((padded.length + 3) % 4));
      return Uint8Array.from(binary, char => char.charCodeAt(0));
    }

    // "p256:" + base64url(x || y) taken from the public JWK. 91 characters, and
    // everything the Python verifier needs to rebuild the public key.
    function visitorKeyFromJwk(jwk) {
      const x = bytesFromBase64Url(jwk.x);
      const y = bytesFromBase64Url(jwk.y);
      const raw = new Uint8Array(x.length + y.length);
      raw.set(x, 0);
      raw.set(y, x.length);
      return 'p256:' + base64UrlFromBytes(raw);
    }

    // Returns null rather than throwing: a browser that cannot do this still
    // submits, just without an identity.
    async function loadIdentity() {
      if (typeof crypto === 'undefined' || !crypto.subtle) return null;
      let db = null;
      try {
        db = await openIdentityDb();
        const existing = await identityRecord(db, 'readonly', store => store.get(IDENTITY_RECORD_KEY));
        if (existing && existing.privateKey && existing.visitorKey) {
          return {
            privateKey: existing.privateKey,
            visitorKey: existing.visitorKey,
            submitCount: Number(existing.submitCount) || 0
          };
        }
        const pair = await crypto.subtle.generateKey(
          { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign', 'verify']);
        const jwk = await crypto.subtle.exportKey('jwk', pair.publicKey);
        const record = {
          privateKey: pair.privateKey,
          visitorKey: visitorKeyFromJwk(jwk),
          submitCount: 0
        };
        await identityRecord(db, 'readwrite', store => store.put(record, IDENTITY_RECORD_KEY));
        return { privateKey: record.privateKey, visitorKey: record.visitorKey, submitCount: 0 };
      } catch (error) {
        console.warn('Visitor identity unavailable', error);
        return null;
      } finally {
        if (db) db.close();
      }
    }

    async function persistSubmitCount(count) {
      let db = null;
      try {
        db = await openIdentityDb();
        const existing = await identityRecord(db, 'readonly', store => store.get(IDENTITY_RECORD_KEY));
        if (!existing) return;
        existing.submitCount = count;
        await identityRecord(db, 'readwrite', store => store.put(existing, IDENTITY_RECORD_KEY));
      } catch (error) {
        console.warn('Unable to persist submit count', error);
      } finally {
        if (db) db.close();
      }
    }
```

- [ ] **Step 2: Syntax check**

Run the syntax command. Expected: `SYNTAX OK`.

- [ ] **Step 3: Verify in the browser**

Rebuild, reload, then in the console:

```javascript
(async () => {
  const a = await loadIdentity();
  const b = await loadIdentity();
  return JSON.stringify({
    key: a.visitorKey.slice(0, 12),
    stable: a.visitorKey === b.visitorKey,
    count: a.submitCount,
    extractable: a.privateKey.extractable,
    type: a.privateKey.type
  });
})()
```

Expected: `key` starts `p256:`, `stable` true, `count` 0, `extractable` false, `type` `"private"`.

- [ ] **Step 4: Commit and push**

```bash
git add index.html
git commit -m "Add a non-extractable visitor identity in IndexedDB"
git push origin restructure-quiz
```

---

### Task 2: Sign the submission

**Files:**
- Modify: `index.html` — `buildSubmissionPayload` (~line 2299), `submitToSupabase` (~line 2330)
- Modify: `database.md` — columns and migration

**Interfaces:**
- Consumes: `loadIdentity()`, `persistSubmitCount()`, `buildSubmissionPayload()`.
- Produces: `buildSignedPayloadString(payload, visitorKey, submitCount)` → string; `signSubmission(payload)` → payload with `visitor_key`, `submit_count`, `signed_payload`, `signature` set (all `null` when identity is unavailable).

- [ ] **Step 1: Build the canonical string and sign it**

Add directly after `buildSubmissionPayload`:

```javascript
    // Fixed field order, plain String() numbers, empty string for absent values.
    // This exact string is stored alongside the signature, so the Python verifier
    // never reconstructs it — which is what keeps Postgres timestamp rewriting and
    // JS/Python float formatting from producing phantom invalid verdicts.
    function buildSignedPayloadString(payload, visitorKey, submitCount) {
      const factors = payload.factors
        .map(factor => `${factor.midpoint}:${factor.spread}`)
        .join(',');
      const blank = value => (value === null || value === undefined ? '' : String(value));
      return [
        'pdoom/1',
        `k=${visitorKey}`,
        `n=${submitCount}`,
        `t=${payload.submitted_at}`,
        `m=${payload.summary.midpoint}`,
        `lo=${payload.summary.lower}`,
        `hi=${payload.summary.upper}`,
        `p10=${payload.summary.p10}`,
        `p90=${payload.summary.p90}`,
        `f=${factors}`,
        `q=${blank(payload.quiz_flow_id)}`,
        `g=${blank(payload.gate_score)}`
      ].join('|');
    }

    // Attaches the identity columns. Any failure leaves all four null and the
    // submission goes ahead unchanged — identity must never cost a submission.
    async function signSubmission(payload) {
      payload.visitor_key = null;
      payload.submit_count = null;
      payload.signed_payload = null;
      payload.signature = null;
      const identity = await loadIdentity();
      if (!identity) return { payload, identity: null, nextCount: null };
      const nextCount = identity.submitCount + 1;
      try {
        const signedPayload = buildSignedPayloadString(payload, identity.visitorKey, nextCount);
        const signature = await crypto.subtle.sign(
          { name: 'ECDSA', hash: 'SHA-256' },
          identity.privateKey,
          new TextEncoder().encode(signedPayload));
        payload.visitor_key = identity.visitorKey;
        payload.submit_count = nextCount;
        payload.signed_payload = signedPayload;
        payload.signature = base64UrlFromBytes(new Uint8Array(signature));
        return { payload, identity, nextCount };
      } catch (error) {
        console.warn('Unable to sign submission', error);
        payload.visitor_key = null;
        payload.submit_count = null;
        payload.signed_payload = null;
        payload.signature = null;
        return { payload, identity: null, nextCount: null };
      }
    }
```

- [ ] **Step 2: Wire it into the submit path**

In `submitToSupabase`, replace:

```javascript
      setSubmissionStatus('Submitting...');
      if (button) button.disabled = true;
      try {
        const { error } = await supabaseClient
          .from(SUBMISSIONS_TABLE)
          .insert(payload);
        if (error) throw error;
        setSubmissionStatus('Submitted! Thanks for contributing.', 'success');
```

with:

```javascript
      setSubmissionStatus('Submitting...');
      if (button) button.disabled = true;
      try {
        const { identity, nextCount } = await signSubmission(payload);
        const { error } = await supabaseClient
          .from(SUBMISSIONS_TABLE)
          .insert(payload);
        if (error) throw error;
        // Only after the row lands, so a failed submit does not burn a number.
        // Deliberately not awaited into the status message: the visitor must see
        // no difference between their first submission and their fortieth.
        if (identity) persistSubmitCount(nextCount);
        setSubmissionStatus('Submitted! Thanks for contributing.', 'success');
```

The status string, the button re-enable in `finally`, and the error branch are unchanged.

- [ ] **Step 3: Syntax check**

Expected: `SYNTAX OK`.

- [ ] **Step 4: Verify signing in the browser, without writing to the database**

Run a quiz to the sliders, then in the console:

```javascript
(async () => {
  const payload = buildSubmissionPayload();
  const { nextCount } = await signSubmission(payload);
  const key = await crypto.subtle.importKey(
    'raw',
    (() => { const b = Uint8Array.from(atob(payload.visitor_key.slice(5).replace(/-/g,'+').replace(/_/g,'/') + '=='), c => c.charCodeAt(0));
             const raw = new Uint8Array(65); raw[0] = 4; raw.set(b, 1); return raw; })(),
    { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify(
    { name: 'ECDSA', hash: 'SHA-256' }, key,
    Uint8Array.from(atob(payload.signature.replace(/-/g,'+').replace(/_/g,'/') + '=='), c => c.charCodeAt(0)),
    new TextEncoder().encode(payload.signed_payload));
  return JSON.stringify({ nextCount, verifies: ok, signed: payload.signed_payload });
})()
```

Expected: `verifies` true, `nextCount` 1, and `signed` matching the `pdoom/1|k=p256:…` shape with every field present.

- [ ] **Step 5: Document the columns**

In `database.md`, add to the `CREATE TABLE`:

```sql
  visitor_key text,
  submit_count int,
  signed_payload text,
  signature text
```

Add to the existing "Migrating an existing table" SQL block:

```sql
ALTER TABLE submissions
  ADD COLUMN IF NOT EXISTS visitor_key text,
  ADD COLUMN IF NOT EXISTS submit_count int,
  ADD COLUMN IF NOT EXISTS signed_payload text,
  ADD COLUMN IF NOT EXISTS signature text;
```

And to the column reference table:

```markdown
| `visitor_key` | text | `p256:` + base64url of the browser's ECDSA P-256 public key. `null` for unsigned rows and everything submitted before 19 Aug 2026. |
| `submit_count` | int | 1-based submission number for that `visitor_key`. |
| `signed_payload` | text | The exact string the signature covers. Stored verbatim so verification never reconstructs it. |
| `signature` | text | base64url of the raw 64-byte r‖s ECDSA signature over `signed_payload`. |
```

- [ ] **Step 6: Commit and push**

```bash
git add index.html database.md
git commit -m "Sign each submission with the visitor identity"
git push origin restructure-quiz
```

---

### Task 3: Verify signatures offline

**Files:**
- Create: `requirements.txt`
- Modify: `prepare_report_data.py` — new verification section, `main()` wiring, stderr summary

**Interfaces:**
- Consumes: `visitor_key`, `submit_count`, `signed_payload`, `signature` on each submission dict.
- Produces: `verify_submissions(submissions)` → `{"signed", "valid", "invalid", "unsigned", "visitors", "repeat", "max_per_visitor", "replays", "mismatched"}`; `print_identity_summary(identity, out)`.

- [ ] **Step 1: Declare the dependency**

Create `requirements.txt`:

```
cryptography>=42
```

Install it:

```bash
python3 -m pip install -r requirements.txt
```

- [ ] **Step 2: Write the verifier**

Add to `prepare_report_data.py`, after `duplicate_audit`:

```python
def _public_key_from_visitor_key(visitor_key):
    """Rebuild the P-256 public key from "p256:" + base64url(x || y)."""
    if not isinstance(visitor_key, str) or not visitor_key.startswith("p256:"):
        return None
    raw = base64.urlsafe_b64decode(visitor_key[5:] + "=" * (-len(visitor_key[5:]) % 4))
    if len(raw) != 64:
        return None
    numbers = ec.EllipticCurvePublicNumbers(
        int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"), ec.SECP256R1())
    return numbers.public_key()


def _signed_fields(signed_payload):
    """Parse the canonical string into its key=value fields."""
    parts = signed_payload.split("|")
    if not parts or parts[0] != "pdoom/1":
        return None
    fields = {}
    for part in parts[1:]:
        key, _, value = part.partition("=")
        fields[key] = value
    return fields


def _agrees_with_row(fields, s, tol=1e-6):
    """The signature covers the canonical string, not the jsonb. Check the two
    tell the same story, so a row edited after signing is caught."""
    def close(a, b):
        try:
            return abs(float(a) - float(b)) <= tol
        except (TypeError, ValueError):
            return False
    summary = s.get("summary") or {}
    for field, key in (("m", "midpoint"), ("lo", "lower"), ("hi", "upper"),
                       ("p10", "p10"), ("p90", "p90")):
        if not close(fields.get(field), summary.get(key)):
            return False
    factors = s.get("factors") or []
    pairs = [p for p in (fields.get("f") or "").split(",") if p]
    if len(pairs) != len(factors):
        return False
    for pair, factor in zip(pairs, factors):
        mid, _, spread = pair.partition(":")
        if not close(mid, factor.get("midpoint")) or not close(spread, factor.get("spread")):
            return False
    return fields.get("k") == (s.get("visitor_key") or "") and \
        fields.get("n") == str(s.get("submit_count"))


def verify_submissions(submissions):
    """Check every signature against its own public key.

    Rows are annotated in place with ``_identity``: signed-valid, signed-invalid
    or unsigned. Invalid rows are never dropped -- silently discarding data would
    be a worse failure than reporting a bad signature."""
    counts = Counter()
    mismatched = 0
    seen_pairs = Counter()
    per_visitor = Counter()
    for s in submissions:
        key, sig, payload = s.get("visitor_key"), s.get("signature"), s.get("signed_payload")
        if not (key and sig and payload):
            s["_identity"] = "unsigned"
            counts["unsigned"] += 1
            continue
        counts["signed"] += 1
        per_visitor[key] += 1
        seen_pairs[(key, s.get("submit_count"))] += 1
        public_key = _public_key_from_visitor_key(key)
        verdict = "signed-invalid"
        if public_key is not None:
            raw_sig = base64.urlsafe_b64decode(sig + "=" * (-len(sig) % 4))
            if len(raw_sig) == 64:
                der = encode_dss_signature(int.from_bytes(raw_sig[:32], "big"),
                                           int.from_bytes(raw_sig[32:], "big"))
                try:
                    public_key.verify(der, payload.encode("utf-8"), ec.ECDSA(hashes.SHA256()))
                    verdict = "signed-valid"
                except InvalidSignature:
                    verdict = "signed-invalid"
        if verdict == "signed-valid":
            fields = _signed_fields(payload)
            if fields is None or not _agrees_with_row(fields, s):
                mismatched += 1
        s["_identity"] = verdict
        counts[verdict] += 1
    return {
        "signed": counts["signed"],
        "valid": counts["signed-valid"],
        "invalid": counts["signed-invalid"],
        "unsigned": counts["unsigned"],
        "visitors": len(per_visitor),
        "repeat": sum(1 for n in per_visitor.values() if n > 1),
        "maxPerVisitor": max(per_visitor.values(), default=0),
        # A visitor's counter is monotonic, so a repeated (key, count) pair means
        # the same submission reached the table twice.
        "replays": sum(n - 1 for n in seen_pairs.values() if n > 1),
        "mismatched": mismatched,
    }
```

Add the imports at the top, after `import argparse`:

```python
import base64
```

and after the stdlib imports:

```python
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
```

- [ ] **Step 3: Add the stderr summary**

After `print_medium_summary`:

```python
def print_identity_summary(identity, out=sys.stderr):
    print("\n-- visitor identity --", file=out)
    print(f"signed {identity['signed']} (valid {identity['valid']}, invalid {identity['invalid']}), "
          f"unsigned {identity['unsigned']}", file=out)
    print(f"distinct visitors {identity['visitors']}, "
          f"submitted more than once {identity['repeat']}, "
          f"most from one visitor {identity['maxPerVisitor']}", file=out)
    if identity["replays"]:
        print(f"replayed (key, count) pairs: {identity['replays']}", file=out)
    if identity["mismatched"]:
        print(f"signed rows whose numbers disagree with the signed string: {identity['mismatched']}", file=out)
```

- [ ] **Step 4: Wire into `main()`**

Add before the `data = {` literal:

```python
    identity = verify_submissions(submissions)
```

Add to the `data` dict:

```python
        "identity": identity,
```

Add to the summary block, after `print_medium_summary(medium_q, prompts)`:

```python
        print_identity_summary(identity)
```

Add `"identity"` to the module docstring's blob description, after the `"dupes"` line:

```
      "identity": {"signed", "valid", "invalid", "unsigned", "visitors", "repeat",
                   "maxPerVisitor", "replays", "mismatched"},
```

- [ ] **Step 5: Round-trip test against the real browser implementation**

Generate a signed payload in the browser console (Task 2 step 4), then feed it to the verifier:

```bash
python3 - <<'EOF'
import json, sys
sys.argv = ["x"]
import prepare_report_data as p
row = json.loads(open('/tmp/signed-row.json').read())
print(p.verify_submissions([row]))
EOF
```

Expected: `valid` 1, `invalid` 0, `mismatched` 0.

Then flip one character of `signed_payload` and rerun. Expected: `invalid` 1.

- [ ] **Step 6: Run against the real export**

```bash
python3 prepare_report_data.py -o /tmp/blob.json
```

Expected: runs clean, and the identity summary reports `unsigned 164` with everything else zero — the historical export has no identities.

- [ ] **Step 7: Commit and push**

```bash
git add prepare_report_data.py requirements.txt
git commit -m "Verify submission signatures when building the report"
git push origin restructure-quiz
```

---

### Task 4: Desktop and mobile verification

**Files:** none — this task changes nothing, it confirms the branch works.

- [ ] **Step 1: Desktop sweep at 1280x800**

Walk every path: beginner, medium, expert (pass and fail), sliders, and the back button. Confirm no console errors and no layout overflow.

- [ ] **Step 2: Mobile sweep at 375x812**

Reload after resizing so any load-time device gates re-run. Confirm on the chooser, the gate, a quiz and the sliders:

- The page never scrolls horizontally (`document.documentElement.scrollWidth <= clientWidth`).
- Breadcrumbs stay readable and do not overflow their container.
- The gate's two result buttons stack rather than truncate.
- Slider bell curves render at a usable size and respond to input.

- [ ] **Step 3: Screenshot both**

Capture the chooser, the gate result and the sliders at both widths.

- [ ] **Step 4: Commit any fixes and push**

```bash
git add -A
git commit -m "<describe the fix>"
git push origin restructure-quiz
```
