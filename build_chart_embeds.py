#!/usr/bin/env python3
"""Build per-chart deliverables from site/charts.html.

Two outputs per featured chart:

  site/embeds/chartN-slug.html   Standalone, responsive, KEEPS the collapsible
                                 <details> data table. This is what gets embedded
                                 (via <iframe>) on jwcaterine.com.

  site/substack/chartN-slug.png  The card rendered at a 760 px viewport, 3x, with
                                 the data table hidden and the footnote extended to
                                 point readers at the table printed below the
                                 Substack post. 2160 px wide to match charts 1 and 7
                                 already in site/substack/.

charts.html is an artifact *fragment* (no <!doctype>/<html>/<head>), so both
outputs wrap it in a real document. A one-line patch to card() makes the shared
script render only the requested chart; the other nine builders run harmlessly
into detached <section>s.

Run from the repo root. Needs `playwright` + its chromium for the PNG step
(`pip install playwright && playwright install chromium`); pass --no-png to skip.
"""
import os
import re
import sys

SRC = "site/charts.html"
EMBED_DIR = "site/embeds"
PNG_DIR = "site/substack"

CHARTS = {
    2: dict(slug="schools",    title="Position on Redistricting by School Affiliation"),
    5: dict(slug="roles",      title="Position on Redistricting by Respondent Category"),
    6: dict(slug="priorities",
            title="Which priorities do you consider most important in new school boundaries"),
}

# Charts 2 and 5 notes carry no table reference, so the pointer is just appended.
PNG_NOTE_APPEND = {
    2: " The data table for this chart is at the bottom of the Substack post.",
    5: " The data table for this chart is at the bottom of the Substack post.",
}
# Chart 6's note already ends "...in the table below." With the table hidden that
# dangles, so the clause is rewritten to be the pointer rather than appended to.
PNG_NOTE_REPLACE = {
    6: ("the full option text is in the table below.",
        "the full option text is in the data table at the bottom of the Substack post."),
}

html = open(SRC, encoding="utf-8").read()

style = re.search(r"<style>.*?</style>", html, re.S)
script = re.search(r"<script>.*?</script>", html, re.S)
assert style and script, "could not locate <style>/<script> in charts.html"
style, script = style.group(0), script.group(0)

# Render only the wanted chart: card() is the sole caller of getElementById("cards").
APPEND_LINE = 'document.getElementById("cards").appendChild(s);'
assert script.count(APPEND_LINE) == 1, "card() append line moved -- did charts.html change?"
script = script.replace(
    APPEND_LINE,
    'if (typeof ONLY_CHART === "undefined" || ONLY_CHART === num) ' + APPEND_LINE,
)


def doc(num, meta, *, for_png):
    extra_style = "section.card { margin: 0; }\n"
    if for_png:
        extra_style += "  details.tbl { display: none !important; }\n"
    else:
        # responsive embed: keep the scroller, just tighten the page frame
        extra_style += "  .wrap { padding: 20px; max-width: 920px; }\n"

    body_script = script
    trailer = ""
    if for_png:
        if num in PNG_NOTE_REPLACE:
            old, new = PNG_NOTE_REPLACE[num]
            assert old in body_script, f"chart {num} note clause not found"
            body_script = body_script.replace(old, new)
        elif num in PNG_NOTE_APPEND:
            add = PNG_NOTE_APPEND[num].replace("\\", "\\\\").replace('"', '\\"')
            trailer = (
                '\n<script>(function () {\n'
                '  var n = document.querySelector("#cards section.card .note");\n'
                f'  if (n) n.appendChild(document.createTextNode("{add}"));\n'
                "})();</script>"
            )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
{style}
<style>
  {extra_style}</style>
</head>
<body>
<div class="wrap">
  <div id="cards"></div>
</div>
<div id="tip" role="status" aria-live="polite"></div>
<script>window.ONLY_CHART = {num};</script>
{body_script}{trailer}
</body>
</html>
"""


os.makedirs(EMBED_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

embed_paths, png_srcs = {}, {}
for num, meta in CHARTS.items():
    ep = f"{EMBED_DIR}/chart{num}-{meta['slug']}.html"
    open(ep, "w", encoding="utf-8").write(doc(num, meta, for_png=False))
    embed_paths[num] = ep
    png_srcs[num] = doc(num, meta, for_png=True)
    print(f"wrote {ep}  ({os.path.getsize(ep) / 1024:.0f} KB)")

if "--no-png" in sys.argv:
    sys.exit(0)

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as p:
    browser = p.chromium.launch()
    for num, meta in CHARTS.items():
        page = browser.new_page(
            viewport={"width": 760, "height": 1200},
            device_scale_factor=3,
            color_scheme="light",
        )
        page.set_content(png_srcs[num], wait_until="networkidle")
        page.wait_for_selector("#cards section.card svg")
        card = page.locator("#cards section.card")
        out = f"{PNG_DIR}/chart{num}-{meta['slug']}.png"
        card.screenshot(path=out)
        box = card.bounding_box()
        print(f"wrote {out}  ({box['width'] * 3:.0f} px wide, "
              f"{os.path.getsize(out) / 1024:.0f} KB)")
        page.close()
    browser.close()
