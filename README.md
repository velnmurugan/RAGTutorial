# Setup — do this once, in order

## 1. Domain
`groundedai.com` is already taken (it's a live product). Pick a different
name before doing anything else — the rest of this doesn't depend on it,
but you'll want it settled.

## 2. Local install
```bash
npm install -g mystmd
```
Requires Node.js 18+. Check with `node -v`.

## 3. Run it locally
From this folder:
```bash
myst start
```
Opens a live-reloading preview in your browser. Edit any file in
`chapters/`, save, and the page updates automatically.

## 4. Push to GitHub
```bash
git init
git add .
git commit -m "Initial scaffold"
gh repo create groundedai-tutorial --public --source=. --push
```
(Or create the repo on github.com first and `git remote add origin <url>`.)

## 5. Connect to Netlify
- New site from Git → pick the GitHub repo
- Build command and publish directory are already set via `netlify.toml`
  in this folder, so you shouldn't need to type them in manually
- Deploy — first build takes a few minutes (it's installing mystmd fresh
  each time; that's normal)

## 6. Connect your domain
Netlify → Domain settings → Add custom domain → follow the DNS
instructions (usually a couple of CNAME/A records at your registrar).

---

## What's in here

- `myst.yml` — book config: chapter order (table of contents), and the
  `thebe_lite: true` flag that makes code cells actually runnable in the
  browser (Pyodide/WASM, no server). Without this flag the notebooks
  render as static, read-only output.
- `intro.md` — landing page
- `chapters/01-what-is-rag.ipynb` — a real, filled-in chapter you can use
  as the template for tone and structure (explanation → runnable code →
  self-check questions, no direct answers given)
- `chapters/02–08` — placeholder stubs, one per planned chapter, so the
  table of contents builds without broken links. Replace the placeholder
  text with real content as you write each one.
- `netlify.toml` — build command (`myst build --html`) and publish
  directory (`_build/html`) so Netlify's UI doesn't need manual config.

## Note on verification

I couldn't run `myst build` myself to confirm this builds clean — my
sandbox can't reach the npm registry. The `myst.yml` schema and notebook
JSON are correct per the current docs and I validated the `.ipynb` files
parse as valid JSON, but run `myst start` locally as your first real
check before pushing.
