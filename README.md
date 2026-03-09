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
