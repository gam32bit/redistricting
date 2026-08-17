#!/usr/bin/env python3
"""Inline site/comments.json into site/explorer.html -> site/explorer.build.html.

The standalone build is what gets published (a hosted artifact can't fetch a
sibling file). For the Astro site, ship explorer.html as-is and let it load
comments.json over the network -- see site/README.md.
"""
import json

TEMPLATE = "site/explorer.html"
DATA = "site/comments.json"
OUT = "site/explorer.build.html"

html = open(TEMPLATE, encoding="utf-8").read()
corpus = open(DATA, encoding="utf-8").read()

# The JSON lives inside <script type="application/json">, which is raw text: an
# unescaped "</script" anywhere in the data would end the element early.
corpus = corpus.replace("<", "\\u003c")

assert "__CORPUS__" in html, "template placeholder missing"
out = html.replace("__CORPUS__", corpus)
open(OUT, "w", encoding="utf-8").write(out)

print(f"{OUT}: {len(out)/1024:.0f} KB")
json.loads(corpus.replace("\\u003c", "<"))  # sanity: still valid JSON
print("corpus re-parses cleanly")
