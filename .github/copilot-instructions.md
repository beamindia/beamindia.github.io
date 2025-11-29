## Quick orientation

This repository is primarily a static website (content under `beamindia/`) with a small Netlify serverless function. There is no Node/webpack build in the repo root — editing the HTML/CSS/JS files directly is the normal workflow.

Key locations
- `beamindia/index.html` — main entry page.
- `beamindia/assets/`, `beamindia/images/` — static assets and images used by pages.
- `beamindia/netlify/functions/visit-counter.js` — serverless function that proxies a call to countapi.xyz.
- `beamindia/README.md` — project owner notes and historical context.

What matters for an AI coding agent
- Treat this as a static-site repo: changes are edits to files under `beamindia/` (HTML, images, PDFs, small JS). There is typically no transpilation step.
- Preserve existing relative paths. Many pages use relative links (e.g., `images/`, `assets/`) — moving files will break links unless you update references.
- The `Backups/` tree contains many snapshots; do not modify/remove backups unless instructed.

Developer workflows (how a human runs/tests changes)
- Quick local preview (PowerShell):

  python -m http.server 8000 --directory .\beamindia

  Then open http://localhost:8000 in a browser. This mirrors how browsers resolve relative links.

- Test Netlify function locally (if you have Node):

  node -e "(async()=>{const h=require('./beamindia/netlify/functions/visit-counter.js'); const r=await h.handler({},{}); console.log('status',r.statusCode,'body',r.body);} )()"

  Or install the Netlify CLI and run `npx netlify dev` at the repo root to emulate Netlify functions and preview the site (optional).

Project-specific patterns to follow
- Small, self-contained pages: most pages are standalone HTML files rather than a single-page app. When modifying page logic, prefer minimal, inline JS or small external JS files in `assets/`.
- PDF and datasheet assets are checked into the repo (e.g., `AT89S8252 data sheet.pdf`, `L298.pdf`). Keep filenames unchanged when possible because pages link directly to them.
- Serverless function pattern: `exports.handler = async function(event, context) { ... }`. If you add functions, follow the same export signature so Netlify can pick them up.

Integration & external dependencies
- `visit-counter.js` calls `https://api.countapi.xyz` to track visits. There are no other packaged dependencies in-repo.
- Deployments are likely handled by Netlify (presence of `netlify/functions`). Expect CI/CD to deploy on push; there are no project-level package manifests (no `package.json` present).

Examples of useful edits the agent might suggest or perform
- Fix a broken relative link in `basicbeam.html` by updating `<a href="...">` to the correct relative path under `images/` or `assets/`.
- Add a small script to `beamindia/assets/` and reference it from `index.html` — keep the script simple and self-contained.
- Add another Netlify function using the same `exports.handler` pattern and test it locally using the node snippet above or `netlify dev`.

Restrictions and safety
- Do not remove or alter files inside `Backups/` unless the maintainer asks.
- Preserve existing file encodings and filenames (case changes may break links on some servers).

If anything is ambiguous
- Ask which file(s) to change (for large edits we should open one or two pages to confirm link patterns).
- If a proposed change requires adding build tooling (webpack, npm, etc.), request explicit approval — the repo currently assumes direct edit/deploy workflows.

Next steps I can take
- Create or update a test harness for the Netlify functions.
- Sweep HTML pages for broken links and offer fixes.

Please review this instruction file and tell me any missing workflow details (local deploy tools you use, CI configuration, or conventions I should follow). I'll iterate the file accordingly.
