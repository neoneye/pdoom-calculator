# pdoom-calculator

Interactive P(doom) calculator and stats pages.

## Local development

1. Install Ruby (3.x recommended) and Bundler.
2. Install dependencies: `bundle install`
3. Start the dev server: `bundle exec jekyll serve`
4. Open `http://localhost:4000/pdoom-calculator/` in your browser.

While the server runs, changes to the site files trigger an automatic rebuild. Stop the server with `Ctrl+C`.

### Testing on mobile devices (local network)

To access the site from other devices on your local network (e.g., a phone or tablet):

1. Start the server bound to all interfaces:
   ```
   bundle exec jekyll serve --host 0.0.0.0
   ```
2. Find your computer's local IP address (e.g., `192.168.1.x`):
   - **macOS**: `ipconfig getifaddr en0` (Wi-Fi) or `ipconfig getifaddr en1`
   - **Linux**: `hostname -I` or `ip addr`
3. On your mobile device, open `http://<your-local-ip>:4000/pdoom-calculator/`

Example urls:
```
192.168.1.x:4000/pdoom-calculator/
192.168.1.x:4000/pdoom-calculator/experimental_quiz2
```