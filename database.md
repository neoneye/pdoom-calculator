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
  quiz_answers jsonb
);
```

## 3. Enable Row Level Security (RLS)

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
| `quiz_flow_id` | text | Which quiz path was taken: `decide`, `beginner`, `medium`, `expert`, or `null` if skipped |
| `quiz_answers` | jsonb | Array of `{question_id, type, value/values}` — the user's quiz selections |
