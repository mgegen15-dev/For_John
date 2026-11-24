#!/usr/bin/env python3
"""Render the project's Markdown documents as styled pages under docs/.

Every report, brief and front-page document becomes an HTML page that shares the
site's design system, so a reader who clicks through from the home page stays on
the site instead of landing on raw Markdown. Each page keeps a link to its source
file on GitHub.

Usage (from the repository root):

    pip install markdown-it-py mdit-py-plugins
    python3 tools/build_site.py

Markdown is parsed with markdown-it-py (CommonMark plus GitHub tables), so pages
render the way GitHub renders the same files.

Writes docs/reports/<slug>.html, docs/briefs/<slug>.html and docs/<slug>.html,
and docs/pages.json (the slug map the home page links against).
"""

import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from titlecase import titlecase

import subprocess
from urllib.parse import quote

try:
    from markdown_it import MarkdownIt
    from mdit_py_plugins.anchors import anchors_plugin
except ImportError:
    sys.exit("This script needs: pip install markdown-it-py mdit-py-plugins")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
REPO = "https://github.com/mgegen15-dev/For_John/blob/main/"
SITE = "https://mgegen15-dev.github.io/For_John/"

# (source path relative to the repo root, output path relative to docs/)
SOURCES = (
    [("SUMMARY.md", "summary.html"),
     ("HOW_THIS_WAS_MADE.md", "how-this-was-made.html"),
     ("AUDIT_GUIDE.md", "audit-guide.html"),
     ("PREDICTIONS.md", "predictions.html"),
     ("RESEARCH_QUEUE.md", "research-queue.html"),
     ("DATA_MANIFEST.md", "data-manifest.html")]
)


def slug(name):
    s = re.sub(r"\.md$", "", os.path.basename(name)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def discover():
    out = list(SOURCES)
    for folder in ("reports", "briefs"):
        d = os.path.join(ROOT, folder)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                out.append((f"{folder}/{f}", f"{folder}/{slug(f)}.html"))
    return out


def rewrite_links(body_html, src_rel, pagemap, depth):
    """Point Markdown links at the generated pages; send the rest to GitHub."""
    up = "../" * depth

    def repl(m):
        attr, raw = m.group(1), m.group(2)
        href = html.unescape(raw)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        from urllib.parse import unquote
        target = unquote(href.split("#")[0])
        frag = href[len(href.split("#")[0]):]
        # resolve relative to the source file's folder
        base = os.path.dirname(src_rel)
        resolved = os.path.normpath(os.path.join(base, target)).replace(os.sep, "/")
        if resolved in pagemap:
            return f'{attr}="{up}{pagemap[resolved]}{frag}"'
        if resolved.startswith("docs/"):            # figures and other site assets
            return f'{attr}="{up}{resolved[len("docs/"):]}{frag}"'
        from urllib.parse import quote
        return f'{attr}="{REPO}{quote(resolved)}{frag}"'

    return re.sub(r'(href|src)="([^"]+)"', repl, body_html)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · For John</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{out}">
<meta name="theme-color" content="#14264a">
<link rel="icon" href="{up}icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}icon-180.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="For John">
<meta property="og:title" content="{title} · For John">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{out}">
<meta property="og:image" content="{site}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{site}og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}site.css">
<link rel="stylesheet" href="{up}doc.css">
</head>
<body>
<a class="skip" href="#main">Skip to Content</a>

<header class="bar">
  <div class="bar-in">
    <a class="wordmark" href="{up}index.html">For John</a>
    <nav aria-label="Site">
      <a href="{up}index.html#findings">Findings</a>
      <a href="{up}index.html#reports">Reports</a>
      <a href="{up}research-queue.html">Research Queue</a>
      <a href="{up}explorer.html">Evidence Explorer</a>
      <a href="{up}how-this-was-made.html">Methods</a>
    </nav>
    <a class="btn btn-gold" href="{up}audit-guide.html">Review This Work</a>
  </div>
</header>

<div class="doclayout">
  <nav class="toc" id="toc" aria-label="On this page"><p class="toc-h">On This Page</p><ol>{toc}</ol></nav>
  <main id="main" class="doc">
    <p class="crumb">{kind} · Updated {updated} · {minutes} min read</p>
    <h1>{title}</h1>
{body}
    <hr>
    <p class="srcnote">Source file: <a href="{repo}{srcq}">{src}</a>. Corrections welcome as a <a href="https://github.com/mgegen15-dev/For_John/issues">GitHub issue</a>. Not medical advice.</p>
  </main>
</div>

<footer class="site">
 <div class="wrap">
  <p>For John (2026). Open research on osteosarcoma. <a href="https://github.com/mgegen15-dev/For_John">Source and data on GitHub</a></p>
  <p>Reports and data: CC BY 4.0. Code: MIT. Not medical advice. <button class="theme-toggle" type="button" id="themeToggle" aria-label="Switch light or dark theme">Dark mode</button></p>
 </div>
</footer>

<script>
(function () {{
  var btn = document.getElementById("themeToggle"), root = document.documentElement;
  try {{ var s = localStorage.getItem("forjohn-theme"); if (s) root.setAttribute("data-theme", s); }} catch (e) {{}}
  btn.addEventListener("click", function () {{
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {{ localStorage.setItem("forjohn-theme", next); }} catch (e) {{}}
    label();
  }});
  function label() {{
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    btn.textContent = dark ? "Light mode" : "Dark mode";
  }}
  label();
  var toc = document.getElementById("toc");
  if (toc && "IntersectionObserver" in window) {{
    var links = Array.prototype.slice.call(toc.querySelectorAll("a"));
    var secs = links.map(function (a) {{ return document.getElementById(a.getAttribute("href").slice(1)); }}).filter(Boolean);
    var cur = null;
    var io = new IntersectionObserver(function (es) {{
      var vis = es.filter(function (e) {{ return e.isIntersecting; }})
        .sort(function (a, b) {{ return a.boundingClientRect.top - b.boundingClientRect.top; }});
      if (!vis.length) return;
      var id = vis[0].target.id;
      if (id === cur) return;
      cur = id;
      links.forEach(function (a) {{ a.classList.toggle("active", a.getAttribute("href") === "#" + id); }});
    }}, {{ rootMargin: "-15% 0px -70% 0px" }});
    secs.forEach(function (s) {{ io.observe(s); }});
  }}
}})();
</script>
</body>
</html>
"""


MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def last_updated(src):
    """Date of the last commit that touched the source file, e.g. 'November 23, 2026'."""
    try:
        iso = subprocess.run(["git", "log", "-1", "--format=%cs", "--", src], cwd=ROOT,
                             capture_output=True, text=True, timeout=20).stdout.strip()
        if not iso:                          # not committed yet: it is being updated now
            import datetime
            iso = datetime.date.today().isoformat()
        y, m, d = iso.split("-")
        return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"
    except Exception:
        return "2026"


def clean_title(t):
    # the wordmark already says "For John"; don't repeat it at the start of page titles
    return re.sub(r"^For John:\s*", "", t).strip()


def new_parser():
    md = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
    md.use(anchors_plugin, min_level=2, max_level=4)
    return md


def link_code_paths(body, src, pagemap, depth):
    """Turn file paths written as code (`reports/X.md`, `data/y.csv`) into links."""
    up = "../" * depth
    base = os.path.dirname(src)

    def repl(m):
        pre, raw = m.group(1), m.group(2)
        if pre:                                   # code blocks stay as they are
            return m.group(0)
        path = html.unescape(raw).strip().rstrip("/")
        if " " in path and not path.endswith(".md"):
            return m.group(0)
        if not re.search(r"\.(md|csv|py|json|tsv|txt|svg|png)$|/", path):
            return m.group(0)
        for cand in (path, os.path.normpath(os.path.join(base, path)).replace(os.sep, "/")):
            if cand in pagemap:
                return f'<a href="{up}{pagemap[cand]}"><code>{raw}</code></a>'
        for cand in (path, os.path.normpath(os.path.join(base, path)).replace(os.sep, "/")):
            if os.path.exists(os.path.join(ROOT, cand)) and not cand.startswith(".."):
                kind = "tree" if os.path.isdir(os.path.join(ROOT, cand)) else "blob"
                url = REPO.replace("/blob/", f"/{kind}/") + quote(cand)
                return f'<a href="{url}"><code>{raw}</code></a>'
        return m.group(0)

    return re.sub(r"(<pre>)?<code>([^<]{2,160})</code>", repl, body)


def name_file_links(body, titles):
    """Links whose visible text is a bare file name show the page title instead."""
    def repl(m):
        href, text = m.group(1), m.group(2)
        key = html.unescape(text).strip()
        if key in titles:
            return f'<a href="{href}">{html.escape(titles[key])}</a>'
        return m.group(0)
    return re.sub(r'<a href="([^"]+)">([^<]+\.md)</a>', repl, body)


def link_ranking_rows(body):
    """In a ranking table, link each lead to its numbered section further down the page."""
    heads = {m.group(2): m.group(1) for m in re.finditer(r'<h3 id="([^"]+)">(\d+)\.\s', body)}
    if not heads:
        return body

    def table(tm):
        t = tm.group(0)
        if not re.search(r"<th[^>]*>\s*(Rank|#)\s*</th>", t):
            return t

        def row(rm):
            r = rm.group(0)
            cells = re.findall(r"<td[^>]*>.*?</td>", r, flags=re.S)
            if len(cells) < 2:
                return r
            n = re.sub(r"<[^>]+>", "", cells[0]).strip()
            if n not in heads or "<a " in cells[1]:
                return r
            inner = re.match(r"(<td[^>]*>)(.*)(</td>)", cells[1], flags=re.S)
            linked = f'{inner.group(1)}<a href="#{heads[n]}">{inner.group(2)}</a>{inner.group(3)}'
            return r.replace(cells[1], linked, 1)

        return re.sub(r"<tr>.*?</tr>", row, t, flags=re.S)

    return re.sub(r"<table>.*?</table>", table, body, flags=re.S)


def mark_numeric_cells(body):
    """Short numeric cells get a class so the table can keep them narrow and aligned."""
    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        txt = re.sub(r"<[^>]+>", "", inner).strip()
        if re.fullmatch(r"[−\-+]?[\d.,]+\s?(%|×)?|n/?a|—|–", txt) and "class=" not in attrs:
            return f'<td{attrs} class="num">{inner}</td>'
        return m.group(0)
    return re.sub(r"<td([^>]*)>(.*?)</td>", repl, body, flags=re.S)


def build():
    pages = discover()
    pagemap = {src: out for src, out in pages}

    # titles first, so links written as file names can show the page title
    titles, srcs = {}, {}
    for src, out in pages:
        path = os.path.join(ROOT, src)
        if not os.path.exists(path):
            continue
        first = open(path, encoding="utf-8").readline()
        t = clean_title(titlecase(first.lstrip("# ").strip())) if first.startswith("# ") else slug(src)
        titles[os.path.basename(src)] = t
        titles[src] = t
        srcs[src] = t

    written = []
    for src, out in pages:
        path = os.path.join(ROOT, src)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()

        # the first H1 is the page title; it is rendered by the template, not the body
        m = re.match(r"#\s+(.+?)\n", text)
        title = m.group(1).strip() if m else slug(src).replace("-", " ").capitalize()
        title = clean_title(titlecase(title))
        body_md = text[m.end():] if m else text
        # headings are title-cased on the site only; the Markdown sources are left as written
        body_md = re.sub(r"(?m)^(#{2,4}\s+)(.+)$", lambda h: h.group(1) + titlecase(h.group(2)), body_md)

        body = new_parser().render(body_md)

        # a short description from the first paragraph of real prose
        plain = re.sub(r"<[^>]+>", "", body)
        plain = re.sub(r"\s+", " ", plain).strip()
        desc = (plain[:195].rsplit(" ", 1)[0] + "…") if len(plain) > 200 else plain
        minutes = max(1, round(len(plain.split()) / 230))

        depth = out.count("/")
        body = rewrite_links(body, src, pagemap, depth)
        body = link_code_paths(body, src, pagemap, depth)
        body = name_file_links(body, titles)
        body = link_ranking_rows(body)
        body = mark_numeric_cells(body)
        body = re.sub(r"<table>", '<div class="tablewrap"><table>', body)
        body = re.sub(r"</table>", "</table></div>", body)
        body = "\n".join("    " + line for line in body.splitlines())

        toc_items = "".join(
            f'<li class="l{len(h.group(1))}"><a href="#{h.group(2)}">{h.group(3)}</a></li>'
            for h in re.finditer(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body)
        )

        kind = ("Report" if src.startswith("reports/")
                else "Research brief" if src.startswith("briefs/") else "Project document")
        page = TEMPLATE.format(
            title=html.escape(title), desc=html.escape(desc), body=body,
            toc=toc_items, up="../" * depth, out=out, site=SITE, repo=REPO,
            src=html.escape(src), srcq=quote(src), kind=kind,
            updated=last_updated(src), minutes=minutes,
        )
        dest = os.path.join(DOCS, out)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(page)
        written.append((src, out, title))

    with open(os.path.join(DOCS, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({src: out for src, out, _ in written}, f, indent=1)

    print(f"wrote {len(written)} pages into docs/")
    for src, out, title in written:
        print(f"  {out:52s} {title[:58]}")


if __name__ == "__main__":
    build()
