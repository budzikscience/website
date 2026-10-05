# Michal K. Budzik: personal academic website

This is a static website. It has no database, no plugins and no ongoing cost apart from the domain.

## How it is organised

| What | Where |
|---|---|
| All text, people, projects, links | `content/site.json` |
| Publications (102 entries) | `content/publications.json` |
| Colours & fonts | top of `assets/css/style.css` (the `:root` block) |
| Photos & figures | `assets/img/` |
| Animations (MP4, converted from the GIFs) | `assets/media/` |
| Research fields (front page + one page each) | `fields` and `intersection` in `content/site.json` |
| Generated pages | `*.html` (do not edit by hand) |

After any content change, run `python build.py`. This regenerates all the pages.

### Editing with Claude
Ask in plain language, for example:
- "Add a new PhD student, Anna Jensen, working on fatigue of bonded joints"
- "Add my new paper: …"
- "Change the accent colour to dark blue"
- "Replace the hero animation with Animation_5.gif"
- "Add an open postdoc position with deadline 1 March"

Claude edits the JSON or CSS, rebuilds, and saves the updated site back into this folder.

## Publishing (free) with GitHub Pages
1. Create a free account at github.com. Then create a new **public** repository, e.g. `website`.
2. On the repository page, click **Add file → Upload files**. Drag in everything inside this `site` folder and click **Commit**.
3. Go to **Settings → Pages**. Set **Source** to "Deploy from a branch", choose `main` / `root`, and save.
   After about a minute the site is live at `https://<username>.github.io/website/`.
4. **Use your own domain.** In **Settings → Pages → Custom domain**, enter your domain (e.g. `www.yourname.com`).
   Then, at the company where the domain is registered (WordPress.com → Domains → DNS records):
   - Add a `CNAME` record: `www` → `<username>.github.io`
   - Add `A` records for the root domain (`@`): `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Tick **Enforce HTTPS** in GitHub once it becomes available (this can take up to 24 hours).
5. Update `"site_url"` in `content/site.json` to your real domain and rebuild.

Netlify (netlify.com, free plan) also works. Drag the `site` folder onto its "Deploy manually" area, then add your domain under **Domain settings**.

> If your domain is registered through WordPress.com, you can keep the domain and point it to the new site as above. You can then cancel any paid WordPress hosting plan.
