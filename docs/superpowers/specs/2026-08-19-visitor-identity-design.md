# Signed visitor identity

Date: 2026-08-19
Branch: `restructure-quiz`

## Problem

The export carries no visitor identifier, so the report cannot tell one person
submitting twice from two people submitting once. `duplicate_audit` in
`prepare_report_data.py` exists only to work around this: it collapses
byte-identical payloads and reports both counts, because that is the closest
approximation available. Of 164 records, 145 payloads are distinct, and most
repeats arrive within seconds of each other — which looks like double-submits
but cannot be established.

A stable per-browser identifier settles it directly.

## Threat model

`pdoom-submissions.json` is exported into a public repository, so any identifier
it carries is readable by anyone. Two distinct attacks follow, and only one of
them is addressable from a static site:

**Impersonation** — copy an identifier out of the public export and submit rows
claiming to be that visitor. A keypair defeats this: the export carries the
*public* key, and producing a valid submission requires the private key, which
is generated non-extractably in the browser and never leaves it.

**Identity reset / ballot stuffing** — clear browser storage for a fresh
identity, or generate keypairs in a loop and submit hundreds of times. A keypair
does nothing here, because the attacker legitimately holds every key they
generate. This is also already the cheaper attack: `SUPABASE_ANON_KEY` is in the
page source, so rows can be POSTed with `curl` without involving the browser.

What signing buys, therefore: nobody can claim an identity they do not hold, and
the "these three submissions are one person" grouping in the public dataset
becomes independently verifiable by anyone who downloads it. What it does not
buy: any assurance that N distinct keys means N distinct people. This is a
data-quality feature that resists vandalism, not a security boundary.

## Design

### Identity in the browser

Created lazily on the first *successful* submission, so visitors who never
submit leave no identity behind.

```js
crypto.subtle.generateKey({ name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign'])
```

`false` makes the private key non-extractable — unreadable by page script and by
devtools. That forces a deviation from "store it in localStorage": a `CryptoKey`
is not a string. The identity record lives in IndexedDB (`pdoom-identity` →
object store `identity` → key `v1`) and holds the private `CryptoKey`, the
public JWK and the submit counter in a single record, so the key and the counter
cannot drift apart if one store is cleared independently.

`visitor_key` is `"p256:" + base64url(x ‖ y)` taken from the public JWK — 91
characters, and sufficient for Python to rebuild the public key.

ECDSA P-256 is chosen over Ed25519 for browser coverage: WebCrypto P-256 has
been available for years, while WebCrypto Ed25519 requires Chrome 137+,
Safari 17+ or Firefox 130+.

### What gets signed

Reconstructing the signed string in Python from the stored row would break in
two places. Postgres rewrites the timestamp (`...628Z` in, `...628+00:00` out),
and JS and Python float formatting can disagree in the last digit. Either
produces phantom "invalid signature" verdicts.

So the client stores the exact string it signed, in a `signed_payload` column:

```
pdoom/1|k=p256:AbC…|n=3|t=2026-08-19T09:14:02.117Z|m=0.7494305|lo=0.14985|hi=1|p10=0.276848|p90=0.654273|f=0.98:0.305,0.905:0.35,0.845:0.445|q=expert|g=15
```

Field order is fixed. Numbers use plain JavaScript `String(value)`. Absent
values (`quiz_flow_id`, `gate_score`) render as the empty string. Factors appear
in `config` order as `midpoint:spread` triples.

Python verifies the signature over the stored string verbatim, so nothing is
reconstructed and nothing can disagree. Separately it checks, with a 1e-6
tolerance, that the numbers inside the string match the row's `factors` and
`summary` jsonb — which catches a row edited after signing.

`quiz_answers` is not covered by the signature. It is a large nested structure
and the attribution value is in the numbers.

### Database

| Column | Type | Meaning |
|---|---|---|
| `visitor_key` | text | `p256:…` public key. `NULL` for unsigned rows and all 164 historical rows. |
| `submit_count` | int | 1-based, per identity. |
| `signed_payload` | text | The exact string the signature covers. |
| `signature` | text | base64url of the raw 64-byte r‖s. |

`visitor_key` and `submit_count` also appear inside `signed_payload`. The
duplication is deliberate: the columns make grouping and indexing cheap, the
string makes verification exact.

The counter persists only *after* a successful insert, so a failed submit does
not burn a number and leave a gap. The tradeoff: a submit that succeeds
server-side but errors client-side and is then retried reuses its number, which
surfaces as a duplicate `(visitor_key, submit_count)` pair and is reported as a
replay rather than silently absorbed.

### Silence

No UI signal that a visitor has submitted before. The status message stays
`Submitted! Thanks for contributing.` for submission 1 and submission 40, the
counter is never rendered, the button is never disabled, and identity failures
never surface an error.

### When crypto is unavailable

Private-browsing storage blocks, a browser without WebCrypto, an IndexedDB write
failure: the submission proceeds exactly as today with all four columns `NULL`.
A submission is never blocked, delayed or failed by identity bookkeeping.

### Verification in `prepare_report_data.py`

`verify_submissions()` tags every row `signed-valid`, `signed-invalid` or
`unsigned`. A new `identity` key in the data blob carries the counts, the number
of distinct visitors, how many submitted more than once, the largest number of
submissions from one visitor, and any replayed `(key, count)` pairs. It prints
to stderr alongside the existing summaries.

Invalid rows are flagged, never dropped. Silently discarding data would be a
worse failure than reporting a bad signature.

`requirements.txt` gains `cryptography`.

`duplicate_audit` is unchanged. It exists precisely because there was no visitor
id, and the historical rows still have none, so it remains the only tool that
works on them.

## Out of scope

- The report pages under `reports/` state that the export carries no visitor
  identifier. That stays true of the current export and becomes false at the
  next one; updating the copy belongs with the next report build.
- Nothing here stops ballot stuffing. The anon key remains public and fresh
  keypairs are free. Moving inserts behind an Edge Function is the change that
  would address it, and is much larger.
