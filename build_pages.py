#!/usr/bin/env python3
"""Build docs/ -- the GitHub Pages site for the comment explorer.

GitHub Pages serves this repo from main + /docs, because the repo root holds the
pipeline. That makes the live URL a project subpath, which is why the corpus fetch
below must stay relative.

Differs from build_site.py, which inlines the corpus for a hosted artifact. Here the
corpus stays a separate file the page fetches, so the browser caches 247 KB gzipped
once instead of re-downloading it inside an 890 KB document every visit.

Two edits are made to explorer.html on the way through:

  1. It is wrapped in a real HTML document (the artifact host supplied <head>).
  2. The synchronous `JSON.parse(#corpus)` becomes a fetch of a RELATIVE path.
     Relative matters: on gam32bit.github.io/<repo>/ an absolute "/data/..."
     resolves to the user root, not the project subpath, and 404s.

Run from the repo root, after build_corpus.py.
"""
import os
import re
import shutil

SRC = "site/explorer.html"
OUT = "docs"
TITLE = "Search the WJCC Redistricting Survey"
DESC = ("Search all 1,374 written responses to the Williamsburg-James City County "
        "Schools redistricting survey, taken from the division's published raw results.")
# Used only for canonical + og:url, which need absolute values. Change this if the
# site later moves to a custom subdomain; "" omits both tags rather than emit a
# wrong one.
BASE_URL = "https://gam32bit.github.io/redistricting/"
BACK_LINK = "https://jwcaterine.com/"

html = open(SRC, encoding="utf-8").read()

# ---- 1. strip the artifact-only <title>, we set a real one in <head> --------
html, n = re.subn(r"^<title>.*?</title>\n*", "", html, count=1, flags=re.S)
assert n == 1, "expected a leading <title> in explorer.html"

# ---- 2. corpus <script> out, relative fetch in ------------------------------
CORPUS_TAG = '<script id="corpus" type="application/json">__CORPUS__</script>\n'
assert CORPUS_TAG in html, "corpus placeholder tag not found -- did explorer.html change?"
html = html.replace(CORPUS_TAG, "")

OLD_INIT = '  var DATA = JSON.parse(document.getElementById("corpus").textContent);\n'
assert OLD_INIT in html, "synchronous corpus parse not found -- did explorer.html change?"
NEW_INIT = """  // Relative, not "/data/...": a project Pages site is served from a subpath.
  fetch("data/comments.json")
    .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(start)
    .catch(function () {
      document.getElementById("status").textContent =
        "The responses didn't load. Reload the page, or read the source PDF linked below.";
    });

  function start(DATA) {
"""
html = html.replace(OLD_INIT, NEW_INIT)

# start() closes where the old IIFE did; the trailing calls move inside it.
OLD_TAIL = """  render();
  jumpToHash();
  window.addEventListener("hashchange", jumpToHash);
})();"""
NEW_TAIL = """  render();
  jumpToHash();
  window.addEventListener("hashchange", jumpToHash);
  }
})();"""
assert OLD_TAIL in html, "IIFE tail not found -- did explorer.html change?"
html = html.replace(OLD_TAIL, NEW_TAIL)

# ---- 3. wrap in a document --------------------------------------------------
head = [
    '<!doctype html>',
    '<html lang="en">',
    '<head>',
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    f'<title>{TITLE}</title>',
    f'<meta name="description" content="{DESC}">',
    '<meta property="og:type" content="website">',
    f'<meta property="og:title" content="{TITLE}">',
    f'<meta property="og:description" content="{DESC}">',
    '<meta name="twitter:card" content="summary">',
]
if BASE_URL:
    head += [f'<link rel="canonical" href="{BASE_URL}">',
             f'<meta property="og:url" content="{BASE_URL}">']
head += ['</head>', '<body>']

BACK = (f'<p style="max-width:60rem;margin:0 auto;padding:1rem 1.25rem 0;font-size:.85rem">'
        f'<a href="{BACK_LINK}">← jwcaterine.com</a></p>\n')

doc = "\n".join(head) + "\n" + BACK + html + "</body>\n</html>\n"

# ---- 4. assemble the directory ---------------------------------------------
os.makedirs(f"{OUT}/data", exist_ok=True)
open(f"{OUT}/index.html", "w", encoding="utf-8").write(doc)
shutil.copyfile("site/comments.json", f"{OUT}/data/comments.json")
# comments.csv is deliberately NOT copied: nothing on the page fetches it. The
# Download CSV button builds a blob from the rows currently filtered, so shipping a
# second, full-corpus CSV would be 960 KB nobody links to. (Unlike in the artifact
# sandbox, those blob downloads do work on Pages.)
open(f"{OUT}/.nojekyll", "w").close()   # keeps Pages from filtering paths it dislikes

print(f"{OUT}/index.html      {os.path.getsize(OUT + '/index.html')/1024:.0f} KB")
print(f"{OUT}/data/comments.json {os.path.getsize(OUT + '/data/comments.json')/1024:.0f} KB")
print("wrote .nojekyll")
