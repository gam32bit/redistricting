# Moving the comment explorer to jwcaterine.com

> **Chosen route: Option C — a separate repo on GitHub Pages, linked from the site.**
> See [OPTION-C.md](OPTION-C.md), which is built and verified. The options below are kept
> for the day the explorer should live *inside* the Astro site rather than beside it.

Target: `gam32bit/jwcaterine-site` — Astro 6, static, MDX + sitemap, deployed to GitHub
Pages by `withastro/action` on every push to `main`, custom domain via `public/CNAME`.

Three things move, in this order of difficulty: **the data** (easy), **the page** (easy),
**the CSS** (the actual work). One mandatory code change comes from a feature the site
already uses — see step 4.

---

## Step 0 — Decide the look first

This decision changes every step after it, so make it before touching a file.

|  | jwcaterine.com | explorer |
|---|---|---|
| Background | `#0f0b1e` deep purple, animated wave canvas behind everything | `#fbfaf7` cream |
| Type | Crimson Pro (Google), `line-height: 1.7` | Georgia + system sans, `1.55` |
| Theme | dark only, no toggle | light-first, with a `prefers-color-scheme: dark` palette |
| Width | `main` is `--measure: 720px` + gutters ≈ 725px | `.wrap` is `60rem` ≈ 960px |
| Links | `#7cb8d8` | `#2a78d6` |

These cannot both win on one page.

**Option A — standalone route, no `BaseLayout`.** `src/pages/redistricting-survey.astro`
emits its own `<html>`. The explorer arrives looking exactly as it does now. You add a
plain "← Joe Caterine" link at the top yourself. No nav, no waves, no frosted scrim, and
it will read as a separate tool rather than a page of your site.

**Option B — integrate.** Use `BaseLayout`, delete the explorer's light palette entirely
(the site is dark-only, so the light half is dead weight), retarget `--serif` to Crimson
Pro, and pass `scrim={false}` plus a full-bleed wrapper, because 960px does not fit inside
a 725px measure and the tables and timeline genuinely want the width.

**Recommendation: A now, B later if it bothers you.** A is an afternoon and cannot regress
the rest of the site; B is a day and touches `main`'s layout contract. A also sidesteps
step 4 almost entirely. If you ship A, note in the page that it's a tool, and move on.

Either way, **the explorer's wrapper must be opaque.** 1,374 cards of body text over a
running canvas animation is unreadable, and the canvas keeps painting behind a page people
scroll for minutes. Under Option B, set the wrapper to the site's own `#0f0b1e` so it reads
as a deliberate calm panel rather than a hole.

---

## Step 1 — The data

`comments.json` is 851 KB raw, **247 KB gzipped**, which is what actually crosses the wire
(GitHub Pages compresses JSON). That's a one-time cost per visitor and it never changes
after a rebuild.

Two ways in. Prefer the second:

```astro
---
// src/pages/redistricting-survey.astro
// Vite emits the file as a hashed asset and hands you its URL:
//   /_astro/comments.a1b2c3d4.json
import corpusUrl from '../data/comments.json?url';
---
```

The `?url` import matters because **GitHub Pages does not let you set response headers** —
you cannot send `Cache-Control: immutable`. A content-hashed filename gets you cache-busting
without a header: the URL changes only when the data changes. (The older advice in
`README.md` said to set that header; on Pages it isn't achievable. This supersedes it.)

The alternative is `public/data/comments.json` fetched at `/data/comments.json` — simpler to
reason about, no hash, so a rebuild can serve a stale copy from cache. Fine if you'd rather
keep the path readable.

Do **not** inline the corpus. `explorer.build.html` exists only because a hosted artifact
can't fetch a sibling file. Inlining makes an 890 KB HTML document that is re-downloaded on
every visit and can't be cached separately. Ship `explorer.html`, not `explorer.build.html`.

---

## Step 2 — The page

`explorer.html` is content-only: it opens with a bare `<title>`, then `<style>`, then the
markup. It has no `<html>`, `<head>` or `<body>`, because the artifact host adds those.

- **Option A:** paste the markup into a `.astro` page that writes its own
  `<html><head>…</head><body>` shell. Move the `<title>` text into a real `<title>`, add
  `<meta name="viewport">` and a description.
- **Option B:** drop the `<title>` line and pass it as the layout prop:
  `<BaseLayout title="Search the redistricting survey" description="…">`. `BaseLayout`
  already appends `| Joe Caterine`, sets canonical, and points OG at `/og.png`.

Two Astro mechanics to know:

- Astro doesn't parse `<script>` / `<style>` contents as JSX, so the `{` characters
  throughout the IIFE are safe. No escaping needed.
- The `<script id="corpus" type="application/json">__CORPUS__</script>` element **goes away**
  — step 4 replaces it with a fetch. Nothing else in the file references `__CORPUS__`, so
  `build_site.py` stops being part of the website path (keep it for artifacts).

The sitemap integration picks the new page up automatically. It won't appear in `rss.xml` or
`search.json` — those read the `blog` collection.

---

## Step 3 — Re-anchor the CSS

This is the part that will bite. The explorer's stylesheet was written to own the whole
document, and about a dozen of its rules are unqualified element selectors that will leak
onto every other page of the site.

**Put it in `src/styles/explorer.css` and import it from the page.** Don't use a scoped
Astro `<style>` block — scoping rewrites selectors, and `:root` in particular behaves in a
way you don't want to debug. A plain imported stylesheet has no surprises and Astro still
bundles and hashes it.

Then wrap the markup in `<div class="explorer">` and fix these, which are the rules that
currently escape:

| Rule in `explorer.html` | What it breaks site-wide |
|---|---|
| `:root { --bg … }` (25 custom properties, ×3 palettes) | move to `.explorer` |
| `body { margin: 0; background; color; font-family; font-size; line-height }` | kills the site's `padding: 2rem`, `#0f0b1e`, Crimson Pro, `1.7` |
| `h1 { … }` | overrides the site's `3rem` heading on every page |
| `a { color: var(--blue-ink) }` | overrides `#7cb8d8` everywhere |
| `button`, `button:hover` | the site doesn't style buttons; yours would become the default |
| `input[type="search"]`, `select` | same |
| `table`, `th`, `td` | restyles tables in blog posts |
| `code` | restyles inline code in blog posts |
| `mark` | harmless today, still global |
| `* { box-sizing: border-box }` | probably what you want, but know it's global |
| `@media (prefers-reduced-motion) { * { animation-duration: .01ms !important } }` | would freeze the wave canvas site-wide for those users |

Mechanically: `:root` → `.explorer`, and prefix each bare element selector with
`.explorer ` (e.g. `table` → `.explorer table`). The former `body` declarations become
`.explorer`'s own — that's where the opaque background from step 0 lives.

Two simplifications while you're in there:

- **`button.primary` is dead CSS.** Three rules, lines 169–171, and no element in the page
  ever carries the class. They're also the only rules with awkward
  `:root[data-theme]`-compound selectors. Delete them and step 3 gets noticeably easier.
- **Under Option B, delete the light palette and both dark blocks**, keeping one set of
  values on `.explorer`. The site has no theme toggle, so three palettes are maintaining
  a feature that doesn't exist.

Watch one interaction under Option B: `.controls` is `position: sticky`, and `.scrim`'s
`backdrop-filter` creates a containing block. Sticky inside a blurred panel is legal but
looks wrong — the sticky bar's opaque background sits on top of the frosted glass. Another
reason for `scrim={false}`.

---

## Step 4 — The one mandatory code change

Two changes to the IIFE, and the second one is the one that will otherwise ship broken.

**4a. Load the corpus asynchronously.** Today line 366 is synchronous:

```js
var DATA = JSON.parse(document.getElementById("corpus").textContent);
```

Rename the IIFE body to a `start(DATA)` function and drive it from a fetch. The HTML already
renders `<p class="status" id="status">Loading…</p>`, so the loading state is designed for —
you only need a failure path.

**Getting the URL into the script.** The `?url` import from step 1 lives in `.astro`
frontmatter, which runs at *build* time; Astro bundles `<script>` tags separately and they
**cannot read frontmatter variables**. Hand the URL over through the DOM — on the same
element you're already marking in 4b:

```astro
<div class="explorer" data-corpus={corpusUrl}>
```

```js
fetch(root.dataset.corpus)
  .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(start)
  .catch(function () {
    document.getElementById("status").textContent =
      "The responses didn't load. Reload the page, or read the source PDF linked below.";
  });
```

(`<script define:vars={{ corpusUrl }}>` also works, but it forces the script inline and gives
up bundling. The data attribute keeps one element as the single handle for both the URL and
the init marker.)

**4b. `BaseLayout` renders `<ClientRouter />`, and that breaks initialization.** With Astro's
client-side router, navigating from `/blog` to the explorer swaps the DOM *without* a page
load, and **`<script>` tags do not re-execute on a swap**. A visitor who arrives from
anywhere else on your site gets a page stuck on "Loading…" forever. It will work perfectly
when you test it by typing the URL directly, and fail for everyone who clicks a link. This
is the single most likely way this migration ships broken.

Drive init from `astro:page-load`, which fires on first load *and* after every swap, and
guard on the DOM rather than a flag:

```js
function init() {
  var root = document.querySelector(".explorer");
  if (!root || root.dataset.ready) return;  // absent = another page; ready = already wired
  root.dataset.ready = "1";
  fetch(root.dataset.corpus) /* … as above … */;
}

// Both registrations are required, and the dataset.ready guard makes the overlap
// harmless. Under Option A there is no ClientRouter, so astro:page-load never fires
// and the readyState half is the only thing that runs. Under Option B the readyState
// half covers the first load and astro:page-load covers every later swap.
if (document.readyState !== "loading") init();
else document.addEventListener("DOMContentLoaded", init);
document.addEventListener("astro:page-load", init);
```

The marker has to live on the element, not in a module variable: the script's closure
survives a swap but the DOM doesn't, so a boolean would skip the re-init and leave you with
the same dead page. Getting this backwards is subtle — a `booted` flag looks correct and
fails only on the second visit.

Also, inside `start()`, `hashchange` is bound to `window`, which survives swaps. Re-binding
on each init leaks listeners that close over a stale `ROWS`:

```js
if (window.__rxHash) window.removeEventListener("hashchange", window.__rxHash);
window.addEventListener("hashchange", window.__rxHash = jumpToHash);
```

Same reasoning for `bubbles()` — it appends to `#f-role` unconditionally, so a second init
on the same DOM would duplicate every role chip. The `dataset.ready` guard is what prevents
that.

**Escape hatch:** put `data-astro-reload` on any link pointing at the explorer and that
navigation becomes a full page load, sidestepping all of 4b. Under Option A the page has no
`ClientRouter` at all, and Astro should fall back to a full load when the destination hasn't
opted in — but add `data-astro-reload` to the inbound link anyway. It's one attribute and it
removes the need to trust that fallback.

---

## Step 5 — Keep it in sync

The pipeline stays here; the site repo only receives generated files. That's the right split,
but it means a copy step exists and will be forgotten.

Add a target to this repo rather than copying by hand:

```python
# deploy_to_site.py  — run after build_corpus.py
SITE = "../jwcaterine-site"
# copy site/comments.json -> {SITE}/src/data/comments.json
# copy site/comments.csv  -> {SITE}/public/data/wjcc-survey-comments.csv
```

Put a `GENERATED — do not edit; source is ~/projects/redistricting` header comment where you
can (the `.astro` page, the CSS), so future-you doesn't hand-patch a file that the next
rebuild overwrites. `comments.json` is 851 KB per revision in git history — negligible at a
handful of rebuilds, worth knowing if you start regenerating weekly.

---

## Verify before you push

- [ ] `npm run build` passes, then `npm run preview`.
- [ ] **Load the explorer by typing its URL directly.** Catches a missing
      `DOMContentLoaded`/`readyState` registration.
- [ ] **Then load it by clicking a link from `/blog`.** Catches the ClientRouter trap in 4b.
      These are two different failure modes with two different entry paths — one passing
      tells you nothing about the other.
- [ ] Leave and come back twice. Role chips should not multiply.
- [ ] Check a blog post with a table and inline code — did step 3 leak?
- [ ] Check the home page still has its background and padding.
- [ ] Search `bus`, confirm 3 tabs render, timeline drag works, `#r0001` deep link scrolls.
- [ ] Throttle to Fast 3G and watch the "Loading…" → results transition.
- [ ] Mobile: the sticky filter bar already goes static under 44rem.

---

## Afterwards, not now

**The charts.** `charts.html` has the same content-only shape and the same `:root` problem,
plus `.scroller svg { min-width: 640px }`, which will force a horizontal scroller inside a
725px measure. Port it into the post rather than iframing it — it's one dependency-free IIFE.

**The blog post.** `blog-post.md` needs frontmatter matching `src/content.config.ts`:
`title`, `date` (a real date, not a string), `description`, optional `tags[]`, and `hero`
only alongside a non-empty `heroAlt` — the schema `refine()` fails the build otherwise. It
goes at `src/content/blog/2026-08-17-slug/index.mdx` with its images beside it. The PNGs in
`site/substack/` are already at 3×.

**Archive the source PDF.** The Download PDF link now points at `wjccschools.org`. That's the
right authority, but it's a link the division can move or remove, and your whole
"check it yourself" premise rests on it. Save a snapshot to the Internet Archive and link
that as a fallback. Self-hosting the 9.3 MB PDF in the site repo is the other option — it
guarantees permanence but that weight stays in git history forever, and a copy you host is a
weaker citation than the division's own.
