#!/usr/bin/env python3
"""
Builds the website from content/site.json and content/publications.json.

    python build.py

Pages generated: index.html, one page per research field, architected-interfaces.html,
publications.html, team.html, about.html. No external dependencies.
Styling lives in assets/css/style.css (colours at the top).
"""
import json, html, re, pathlib

ROOT = pathlib.Path(__file__).parent
S = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
P = json.loads((ROOT / "content/publications.json").read_text(encoding="utf-8"))
e = lambda s: html.escape(str(s or ""), quote=True)
m, pe = S["meta"], S["person"]
FIELDS, INTER = S["fields"], S["intersection"]
PROJECTS = S["projects"]["items"]


# ---------------- helpers ----------------
def bold_me(a):
    return re.sub(r"(M\.\s?K\.\s?Budzik)", r"<strong>\1</strong>", e(a))


def media(item, cls="", vkey="video", ikey="image", alt="image_alt"):
    if item.get(vkey):
        return (f'<video class="{cls}" src="{e(item[vkey])}" poster="{e(item.get("poster"))}" autoplay muted loop '
                f'playsinline preload="metadata" aria-label="{e(item.get(alt) or item.get("caption"))}"></video>')
    if item.get(ikey):
        return f'<img class="{cls}" src="{e(item[ikey])}" alt="{e(item.get(alt))}" loading="lazy">'
    return ""


def pub_li(p, cls=""):
    status = f' <span class="tag tag-warn">{e(p["status"])}</span>' if p.get("status") else ""
    typ = "" if p["type"] == "Journal article" else f' <span class="tag">{e(p["type"])}</span>'
    doi = f' <a class="doi" href="https://doi.org/{e(p["doi"])}" target="_blank" rel="noopener">DOI</a>' if p.get("doi") else ""
    q = e(f'{p["authors"]} {p["citation"]}'.lower())
    return (f'<li data-year="{p["year"]}" data-q="{q}"{f" class={cls}" if cls else ""}><span class="py mono">{p["year"]}</span>'
            f'<div><span class="pa">{bold_me(p["authors"])}</span><span class="pc">{e(p["citation"])}</span>{typ}{status}{doi}</div></li>')


def find_pubs(keys):
    out = [p for p in P if any(k.lower() in p["citation"].lower() for k in keys)]
    return sorted(out, key=lambda p: -p["year"])


def find_projects(keys):
    return [p for p in PROJECTS if any(k.lower() in p["name"].lower() for k in keys)]


def project_list(items):
    return "".join(f"""<li><div><strong>{e(p["name"])}</strong><span>{e(p["funder"])}</span></div>
      <div class="proj-meta"><span class="tag">{e(p["role"])}</span><span class="mono">{e(p["years"])}</span></div></li>""" for p in items)


def head(title):
    return f'<div class="sec-head reveal"><h2>{e(title)}</h2></div>'


VENN = f"""
<svg class="venn" viewBox="0 0 460 470" role="img" aria-label="Composite materials and structures, containing fibre and laminated composites, adhesive bonding and mechanical metamaterials; architected interfaces at their intersection">
  <g class="umbrella"><rect x="4" y="4" width="452" height="462" rx="22"/>
    <text class="u1" x="230" y="34">{e(S["fields_intro"]["umbrella_label"])}</text>
    <text class="u2" x="230" y="52">{e(S["fields_intro"]["umbrella_sub"])}</text></g>
  <g transform="translate(20,62)">
  <a href="{FIELDS[0]['slug']}.html" class="venn-c c1"><circle cx="150" cy="145" r="115"/><text x="100" y="104">Fibre &amp;</text><text x="100" y="123">laminated</text><text x="100" y="142">composites</text></a>
  <a href="{FIELDS[1]['slug']}.html" class="venn-c c2"><circle cx="270" cy="145" r="115"/><text x="312" y="112">Adhesive</text><text x="312" y="131">bonding</text></a>
  <a href="{FIELDS[2]['slug']}.html" class="venn-c c3"><circle cx="210" cy="250" r="115"/><text x="210" y="318">Mechanical</text><text x="210" y="337">metamaterials</text></a>
  <a href="{INTER['slug']}.html" class="venn-core"><circle class="hit" cx="210" cy="185" r="34"/><circle class="dot" cx="210" cy="172" r="6"/><text x="210" y="196">architected</text><text x="210" y="210">interfaces</text></a>
  </g>
</svg>"""

NAV = [("index.html#fields", "Research", "research"), ("publications.html", "Publications", "publications"),
       ("opportunities.html", "Opportunities", "opportunities"), ("about.html", "About", "about"), ("about.html#contact", "Contact", "contact")]


def page(fname, title, body, active="", description=None):
    nav = "".join(f'<a href="{h}"{" class=active" if k == active else ""}>{t}</a>' for h, t, k in NAV)
    links = "".join(f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["label"])}</a>' for l in S["links"])
    ld = ""
    if fname == "index.html":
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Person", "name": pe["full_name"], "jobTitle": pe["role"],
            "affiliation": {"@type": "Organization", "name": "Aarhus University"}, "email": pe["email"],
            "url": m["site_url"], "sameAs": [l["url"] for l in S["links"]]}, ensure_ascii=False) + "</script>"
    full_title = m["title"] if fname == "index.html" else f'{title} · {pe["name"]}'
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description or m["description"])}">
<link rel="canonical" href="{e(m["site_url"])}/{"" if fname == "index.html" else fname}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description or m["description"])}">
<meta property="og:image" content="{e(m["site_url"])}/assets/img/og-image.jpg">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{ld}
</head>
<body>
<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span>{e(pe["name"])}</a>
    <nav id="menu">{nav}</nav>
    <button class="menu-btn" aria-label="Menu" aria-controls="menu" aria-expanded="false"><span></span><span></span></button>
  </div>
</header>
<main>
{body}
</main>
<footer class="footer">
  <div class="wrap foot-grid">
    <div><strong>{e(pe["name"])}</strong><br><span class="muted">{e(pe["role"])}<br>{e(pe["affiliation"])}</span></div>
    <div><a href="mailto:{e(pe["email"])}">{e(pe["email"])}</a><br><span class="muted">{e(pe["address"])}</span></div>
    <div class="foot-links">{links}</div>
  </div>
  <div class="wrap foot-bottom muted"><span>© {e(pe["name"])} · {e(pe["group"])}</span><span>Updated {e(m["updated"])}</span></div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""
    (ROOT / fname).write_text(doc, encoding="utf-8")
    return fname


built = []

# ---------------- HOME ----------------
H, FI, sc = S["hero"], S["fields_intro"], S["research"]["showcase"]
_cc = S.get("cross_cutting", {"items": []})
CCHOME = (f'<div class="cc reveal"><span class="eyebrow">{e(_cc["title"])}</span>' + "".join(
    f'<div class="cc-item"><strong>{e(c["title"])}</strong><p>{e(c["text"])}</p></div>' for c in _cc["items"]) + "</div>") if _cc["items"] else ""
cards = "".join(f"""
      <a class="field-card {f["key"]} reveal" href="{f["slug"]}.html">
        <span class="field-n mono">0{i}</span>
        <h3>{e(f["title"])}</h3>
        <p>{e(f["short"])}</p>
        <span class="more">Explore <span aria-hidden="true">→</span></span>
      </a>""" for i, f in enumerate(FIELDS, 1))

home = f"""
<section class="hero">
  <div class="lattice" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="eyebrow">{e(H["eyebrow"])}</p>
      <h1>{e(H["headline"])}</h1>
      <p class="lead">{e(H["lead"])}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="{e(H["cta_primary"]["href"])}">{e(H["cta_primary"]["label"])}</a>
        <a class="btn btn-ghost" href="{e(H["cta_secondary"]["href"])}">{e(H["cta_secondary"]["label"])}</a>
      </div>
    </div>
    <figure class="hero-media">{media(H)}<figcaption>{e(H["caption"])}</figcaption></figure>
  </div>
</section>

<section class="section section-soft" id="fields">
  <div class="wrap">
    <div class="fields-top">
      <div>
        {head(FI["title"])}
        <p class="sec-intro reveal">{e(FI["text"])}</p>
      </div>
      <div class="reveal">{VENN}</div>
    </div>
    <div class="field-cards">{cards}
    </div>
    {CCHOME}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <a class="inter-band reveal" href="{INTER["slug"]}.html">
      <div class="inter-media">{media(INTER)}</div>
      <div class="inter-text">
        <p class="eyebrow">{e(INTER["eyebrow"])}</p>
        <h3>{e(INTER["title"])}</h3>
        <p>{e(INTER["short"])}</p>
        <span class="more">Read more <span aria-hidden="true">→</span></span>
      </div>
    </a>
    <div class="showcase reveal">
      <div class="showcase-text"><h3>{e(sc["title"])}</h3><p>{e(sc["text"])}</p></div>
      <div class="showcase-media">{media(sc)}</div>
    </div>
    <div class="tiles reveal">
      <a href="publications.html"><strong>Publications</strong><span>Journal articles and book chapters</span></a>
      <a href="opportunities.html"><strong>Opportunities</strong><span>Internships, theses and positions</span></a>
      <a href="about.html"><strong>About</strong><span>Background, teaching and contact</span></a>
    </div>
  </div>
</section>
"""
built.append(page("index.html", "Home", home, "research"))


# ---------------- FIELD PAGES ----------------
def field_page(f, is_inter=False):
    others = [x for x in FIELDS if x is not f]
    pubs = find_pubs(f["papers"])
    CC = S.get("cross_cutting", {"items": []})
    projs = find_projects(f["projects"])
    projs += [x for x in find_projects([k for c in CC["items"] for k in c["projects"]]) if x not in projs]
    bys = {x["slug"]: x for x in FIELDS + [INTER]}
    cross = "".join(f"""<div class="cross reveal {bys[c["with"]].get("key", "ci")}"><h3>{e(c["title"])} <a href="{c["with"]}.html">→</a></h3><p>{e(c["text"])}</p>
      <ol class="pubs">{"".join(pub_li(p) for p in find_pubs(c["papers"]))}</ol></div>""" for c in f.get("crossroads", []))
    cc = "".join(f'<div class="cc-item"><strong>{e(c["title"])}</strong><p>{e(c["text"])}</p></div>' for c in CC["items"])
    topics = "".join(f"<li>{e(t)}</li>" for t in f["topics"])
    second = f'<figure class="fig reveal">{media(f, ikey="image2", alt="image2_alt")}</figure>' if f.get("image2") else ""
    nxt = "".join(f'<a class="field-card {x.get("key", "ci")}" href="{x["slug"]}.html"><h3>{e(x["title"])}</h3><p>{e(x["short"])}</p><span class="more">Explore →</span></a>'
                  for x in (FIELDS if is_inter else others + [INTER]))
    body = f"""
<section class="page-hero field-hero {f.get("key", "ci")}">
  <div class="wrap">
    <p class="crumb mono"><a href="index.html#fields">Research</a> / {e(f["title"])}</p>
    <h1>{e(f["title"])}</h1>
    <p class="lead">{e(f["short"])}</p>
  </div>
</section>
<section class="section">
  <div class="wrap field-grid">
    <div class="field-text reveal">
      {"".join(f"<p>{e(p)}</p>" for p in f["paragraphs"])}
      <h3 class="sub">Topics</h3>
      <ul class="ticks">{topics}</ul>
    </div>
    <div>
      <figure class="fig reveal">{media(f)}</figure>
      {second}
    </div>
  </div>
</section>
{f'''<section class="section" style="padding-top:0"><div class="wrap"><h3 class="sub" style="margin-top:0">Crossroads</h3>{cross}</div></section>''' if cross else ""}
<section class="section section-soft">
  <div class="wrap">
    {f'<div class="cc reveal"><span class="eyebrow">{e(CC.get("title"))}</span>{cc}</div>' if cc else ""}
    {f'<h3 class="sub">Related projects</h3><ul class="projects reveal">{project_list(projs)}</ul>' if projs else ""}
    <h3 class="sub">Key papers</h3>
    <ol class="pubs reveal">{"".join(pub_li(p) for p in pubs)}</ol>
    <p class="reveal" style="margin-top:20px"><a href="publications.html">All publications →</a></p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h3 class="sub" style="margin-top:0">{"The three fields" if is_inter else "Related"}</h3>
    <div class="field-cards">{nxt}</div>
  </div>
</section>
"""
    return page(f'{f["slug"]}.html', f["title"], body, "research", f["short"])


for f in FIELDS:
    built.append(field_page(f))
built.append(field_page(INTER, True))

# ---------------- PUBLICATIONS ----------------
PB = S["publications"]
years = sorted({p["year"] for p in P}, reverse=True)
selected = find_pubs(PB["selected_keywords"])
chips = '<button class="chip on" data-y="all">All</button>' + "".join(
    f'<button class="chip" data-y="{y}">{y}</button>' for y in years if y >= 2017) + '<button class="chip" data-y="old">Before 2017</button>'
pubs_body = f"""
<section class="page-hero"><div class="wrap"><h1>{e(PB["title"])}</h1><p class="lead">{e(PB["intro"])}</p></div></section>
<section class="section">
  <div class="wrap">
    <h3 class="sub" style="margin-top:0">Selected</h3>
    <ol class="pubs pubs-sel reveal">{"".join(pub_li(p, "sel") for p in selected)}</ol>
    <h3 class="sub">All publications <span class="mono muted">({len(P)})</span></h3>
    <div class="pub-tools">
      <input type="search" id="pubq" placeholder="Search title, author, journal…" aria-label="Search publications">
      <div class="chips">{chips}</div>
    </div>
    <ol class="pubs" id="publist">{"".join(pub_li(p) for p in sorted(P, key=lambda p: -p["year"]))}</ol>
    <p class="muted small" id="pubempty" hidden>No matching publications.</p>
  </div>
</section>
"""
built.append(page("publications.html", "Publications", pubs_body, "publications"))

# ---------------- OPPORTUNITIES ----------------
O = S["opportunities"]
opp = "".join(f'<div class="opp reveal"><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></div>' for x in O["items"])
opp_body = f"""
<section class="page-hero"><div class="wrap"><h1>{e(O["title"])}</h1><p class="lead">{e(O["intro"])}</p></div></section>
<section class="section">
  <div class="wrap">
    <div class="opps">{opp}</div>
    <p class="sec-intro reveal" style="margin-top:40px">{e(O["facilities"])}</p>
    <div class="join reveal">
      <div><h3>How to get in touch</h3><p>{e(O["how"])}</p></div>
      <a class="btn btn-primary" href="{e(O["cta"]["href"])}">{e(O["cta"]["label"])}</a>
    </div>
  </div>
</section>
"""
built.append(page("opportunities.html", "Students & opportunities", opp_body, "opportunities"))
(ROOT / "team.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=opportunities.html"><link rel="canonical" href="opportunities.html"><a href="opportunities.html">Students &amp; opportunities</a>', encoding="utf-8")

# ---------------- ABOUT ----------------
ab, TE, CV, NW, C = S["about"], S["teaching"], S["cv"], S["news"], S["contact"]
timeline = "".join(f'<li><span class="mono">{e(t["years"])}</span><p>{e(t["text"])}</p></li>' for t in CV["timeline"])
courses = "".join("<li>" + (f'<span class="tag">{e(c["level"])}</span>' if c.get("level") else "") + e(c["name"]) + "</li>" for c in TE["courses"])
news = "".join(f'<li><a href="{e(n["url"])}" target="_blank" rel="noopener"><span class="mono">{e(n["date"])}</span><strong>{e(n["title"])}</strong><span class="muted">{e(n["source"])} ↗</span></a></li>' for n in NW["items"])
cvbtn = f'<p><a class="btn btn-ghost" href="{e(CV["cv_pdf"])}">Download CV (PDF)</a></p>' if CV.get("cv_pdf") else ""
links = "".join(f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["label"])} ↗</a>' for l in S["links"])
about_body = f"""
<section class="page-hero"><div class="wrap"><h1>{e(ab["title"])}</h1></div></section>
<section class="section" style="padding-top:48px">
  <div class="wrap about-grid">
    <div class="portrait reveal"><img src="{e(pe["photo"])}" alt="Portrait of {e(pe["name"])}"></div>
    <div class="about-text reveal">
      <p class="who"><strong>{e(pe["full_name"])}</strong><br>{e(pe["role"])}<br><span class="muted">{e(pe["affiliation"])}</span></p>
      {"".join(f"<p>{e(p)}</p>" for p in ab["paragraphs"])}
      <h3 class="sub">Roles</h3>
      <ul class="ticks">{"".join(f"<li>{e(h)}</li>" for h in ab["highlights"])}</ul>
      <p class="muted small">Languages: {e(ab["languages"])}</p>
    </div>
  </div>
</section>
<section class="section section-soft" id="career">
  <div class="wrap cv-grid">
    <div>{head(CV["title"])}<ol class="timeline reveal">{timeline}</ol>{cvbtn}</div>
    <div class="reveal">
      {head(TE["title"])}
      <p class="muted">{e(TE["intro"])}</p>
      <ul class="courses courses-col">{courses}</ul>
      <h3 class="sub">Recognition</h3><ul class="ticks">{"".join(f"<li>{e(a)}</li>" for a in CV["awards"])}</ul>
      <h3 class="sub">{e(NW["title"])}</h3><ul class="news">{news}</ul>
    </div>
  </div>
</section>
<section class="section contact" id="contact">
  <div class="wrap">
    {head(C["title"])}
    <p class="sec-intro reveal">{e(C["text"])}</p>
    <div class="contact-grid reveal">
      <a class="contact-mail" href="mailto:{e(pe["email"])}">{e(pe["email"])}</a>
      <div class="contact-meta"><p>{e(pe["phone"])}</p><p>{e(pe["address"])}</p></div>
      <div class="links">{links}</div>
    </div>
  </div>
</section>
"""
built.append(page("about.html", "About", about_body, "about"))

# ---------------- 404, sitemap, robots ----------------
nf_body = """
<section class="page-hero"><div class="wrap"><h1>Page not found</h1>
<p class="lead">The page you are looking for does not exist or has moved.</p>
<p><a class="btn btn-primary" href="index.html">Go to the front page</a></p></div></section>
"""
page("404.html", "Page not found", nf_body)
base = m["site_url"].rstrip("/")
urls = "".join(f"<url><loc>{base}/{'' if f == 'index.html' else f}</loc></url>" for f in built)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")

print("Built:", ", ".join(built))
