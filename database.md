# Database setup (Supabase)

The site uses [Supabase](https://supabase.com/) to store P(doom) submissions.

## 1. Create a Supabase project

1. Go to [supabase.com](https://supabase.com/) and create a free project.
2. Copy the **Project URL** and **anon public** key from **Settings > API**.
3. Paste them into `_data/supabase.yml`:

```yaml
url: "https://YOUR_PROJECT.supabase.co"
anon_key: "YOUR_ANON_KEY"
```

## 2. Create the submissions table

Open the **SQL Editor** in the Supabase dashboard and run:

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
  expert_verified boolean,
  gate_answers jsonb,
  visitor_key text,
  submit_count int,
  signed_payload text,
  signature text
);
```

### Migrating an existing table

The expert gate columns were added on 19 Aug 2026. Existing projects need:

```sql
ALTER TABLE submissions
  ADD COLUMN IF NOT EXISTS gate_score int,
  ADD COLUMN IF NOT EXISTS gate_recommended_level text,
  ADD COLUMN IF NOT EXISTS expert_verified boolean,
  ADD COLUMN IF NOT EXISTS gate_answers jsonb,
  ADD COLUMN IF NOT EXISTS visitor_key text,
  ADD COLUMN IF NOT EXISTS submit_count int,
  ADD COLUMN IF NOT EXISTS signed_payload text,
  ADD COLUMN IF NOT EXISTS signature text;
```

Rows submitted before this date keep `NULL` in all seven. The three gate columns
are also `NULL` for any beginner or medium submission that never met the gate,
and the four identity columns are `NULL` whenever the browser could not generate
a key — a submission is never blocked over identity.

`gate_score` is non-null exactly when the visitor clicked **Expert quiz**, since the
check is not reachable any other way. That makes the whole expert journey queryable:

```sql
SELECT expert_verified, quiz_flow_id, count(*)
FROM submissions WHERE gate_score IS NOT NULL GROUP BY 1, 2;
```

`expert_verified = true` cleared the bar; `false` with `quiz_flow_id = 'expert'` went on
anyway; `false` with a lower `quiz_flow_id` accepted the reroute. What no query can show
is anyone who took the check and left without submitting -- they leave no row.

Grouping repeat submissions is then a plain query:

```sql
SELECT visitor_key, count(*) FROM submissions
WHERE visitor_key IS NOT NULL GROUP BY visitor_key HAVING count(*) > 1;
```

## 3. Grant Data API access

As of May 30, 2026, new Supabase projects no longer expose `public` tables to the Data API by default. Grant access explicitly so the anon key (used by supabase-js) can reach the table:

```sql
GRANT SELECT, INSERT ON submissions TO anon;
```

Without this, PostgREST returns a `42501` error.

## 4. Enable Row Level Security (RLS)

RLS is required for the anon key to work. Enable it on the table, then add policies for anonymous insert and read access:

```sql
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- Allow anyone to submit predictions
CREATE POLICY "Allow anonymous inserts"
  ON submissions FOR INSERT TO anon
  WITH CHECK (true);

-- Allow anyone to read submissions (needed for the stats page)
CREATE POLICY "Allow anonymous reads"
  ON submissions FOR SELECT TO anon
  USING (true);
```

## Column reference

| Column | Type | Description |
|---|---|---|
| `id` | bigint | Auto-incrementing primary key |
| `submitted_at` | timestamptz | When the prediction was registered |
| `factors` | jsonb | Array of `{key, label, lower, upper, midpoint, spread}` per stage |
| `summary` | jsonb | `{lower, upper, midpoint, p10, p90}` — the combined P(doom) result |
| `quiz_flow_id` | text | Which quiz was taken: `beginner`, `medium`, `expert`, or `null` if skipped. Historical rows may hold `decide`, the knowledge-check path retired on 19 Aug 2026. |
| `quiz_answers` | jsonb | Array of `{question_id, type, value/values}` — the user's quiz selections |
| `gate_score` | int | Expert gate score, 0–30. `null` if the gate never ran. |
| `gate_recommended_level` | text | Level the gate recommended: `beginner`, `medium` or `expert`. `null` if the gate never ran. |
| `expert_verified` | boolean | True when `gate_score >= 26`. A submission with `quiz_flow_id = 'expert'` and `expert_verified = false` is a self-declared expert. `null` if the gate never ran. |
| `gate_answers` | jsonb | The term ids ticked on the expert check, so per-decoy performance can be measured. `null` if the gate never ran; `[]` means it ran and nothing was ticked. |
| `visitor_key` | text | `p256:` + base64url of the browser's ECDSA P-256 public key. `null` for unsigned rows and everything submitted before 19 Aug 2026. |
| `submit_count` | int | 1-based submission number for that `visitor_key`. |
| `signed_payload` | text | The exact string the signature covers. Stored verbatim so verification never has to reconstruct it. |
| `signature` | text | base64url of the raw 64-byte r‖s ECDSA signature over `signed_payload`. |
