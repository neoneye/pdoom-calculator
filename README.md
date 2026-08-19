# pdoom-calculator

Interactive P(doom) calculator and stats pages.

## Install the dependencies

**Ruby 3.3 required.** GitHub Pages uses Ruby 3.3.4; Ruby 4.x is not yet supported by the Jekyll/github-pages ecosystem.

If Homebrew updated you to Ruby 4.x, use Ruby 3.3:

```bash
brew install ruby@3.3
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
```

Then:

```bash
bundle install
```

## Run the server on localhost

```bash
bundle exec jekyll serve
http://127.0.0.1:4000/pdoom-calculator/
```

## Run the server on all network interfaces (for mobile testing)

```bash
bundle exec jekyll serve --host 0.0.0.0
http://0.0.0.0:4000/pdoom-calculator/
```

Access from your phone using your computer's local IP address (e.g., `http://192.168.1.100:4000/pdoom-calculator/`)

## Developer mode

Append `?developer=1` to withhold submissions. The page builds and signs the payload
exactly as normal, logs it to the console, and stops short of the insert, so the live
table stays clean while working on the calculator:

```bash
http://127.0.0.1:4000/pdoom-calculator/?developer=1
```

The status line under the button says so explicitly rather than reporting success. The
per-browser submit counter is not advanced either, since no row lands.

## Build the submissions report

`prepare_report_data.py` reads `pdoom-submissions.json` and emits the data blob
the pages under `reports/` render from.

Verifying submission signatures needs `cryptography`, which macOS will not let
you install system-wide (PEP 668). Use a virtualenv:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

```bash
.venv/bin/python prepare_report_data.py --inject reports/submissions-<date>.html
```

Running it with a plain `python3` still works — every chart is built the same —
but signed submissions come back `unchecked` and the run prints a warning saying
so. It never passes off unverified rows as verified.
