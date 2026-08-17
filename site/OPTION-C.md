# Option C — GitHub Pages from this repo's `docs/`, linked from the site

**This is the chosen route.** The search page is served straight from
`github.com/gam32bit/redistricting`, and jwcaterine.com links to it.

It's the least work of the three options, not a compromise version of them. Because the page
owns its whole document and has no Astro around it:

- **Step 3 of MIGRATION.md disappears.** Nothing leaks, because there's no shared stylesheet
  to leak into. The `:root` palette, `body`, `h1`, `a`, `button`, `table` and `code` rules all
  stay exactly as written.
- **Step 4b disappears.** No `<ClientRouter />`, so no swap, so no dead "Loading…" page. Only
  the async fetch (4a) was needed, and `build_pages.py` already performs it.
- No `npm`, no build step, no Actions workflow, no Astro version to keep up with.

The cost is that it isn't *on* jwcaterine.com — it's a page you link to. Given this is a tool
rather than an article, that reads fine.

## Why `docs/` and not the repo root

Pages can serve from `main` root, from `main` + `/docs`, or from a `gh-pages` branch. This
repo holds the pipeline as well as the site, so root is out, and a separate branch adds a
moving part for nothing. `/docs` it is.

That makes the live URL a **project subpath** — `https://gam32bit.github.io/redistricting/` —
which is exactly why the corpus is fetched by a relative `data/comments.json`. An absolute
`/data/…` would resolve to the user root and 404. Don't "fix" it.

## What's built and verified

`python3 build_pages.py` (from the repo root) produces:

```
docs/
├── index.html          41 KB   the page, wrapped in a real document
├── data/
│   └── comments.json  851 KB   fetched at runtime (247 KB gzipped)
├── .nojekyll
└── README.md                   hand-written; the build leaves it alone
```

The script makes exactly three changes to `explorer.html` on the way through, each guarded by
an assertion so a future edit upstream fails loudly instead of silently producing a broken
page: it strips the artifact-only `<title>`, swaps the synchronous `JSON.parse(#corpus)` for a
`fetch("data/comments.json")` with an error path, and wraps the result in
`<!doctype html>` … `<head>` … `<body>` with title, description, canonical and OG tags.

Verified by serving the build and loading it in a browser: the corpus fetch resolves, all
1,374 responses render, `neighborhood` returns **419** (matching the figure in
`site/README.md`'s reproducibility check), phrase search and highlighting work, the sticky
filter bar behaves, all three download controls render, and the console is clean.

Note that `comments.csv` is deliberately *not* copied into `docs/` — nothing fetches it. The
Download CSV button builds a blob from the rows currently filtered. Unlike in the artifact
sandbox, those blob downloads do work on Pages.

## Turning Pages on

The repo is public and the commit is local. Remaining steps, all yours:

1. **Push** — `git push -u origin main`.
2. **Settings → Pages** → Source: *Deploy from a branch*, Branch: `main`, Folder: **`/docs`**.
   Save. The first build takes a minute or two.
3. **Check it live** at `https://gam32bit.github.io/redistricting/`. Confirm the responses
   load — that URL, not a local server, is the real test of the relative fetch path.
4. **Link it from the post**: replace `SEARCH_PAGE_URL` in `blog-post-search-page.md`.

**Optional, and worth it later: a subdomain.** `survey.jwcaterine.com` reads far better in a
newsletter than a `github.io` path.

- At your DNS host, add a `CNAME` record: `survey` → `gam32bit.github.io`.
- Settings → Pages → Custom domain → `survey.jwcaterine.com`. That writes a `CNAME` file into
  the repo, so pull afterwards.
- Wait for the certificate, then tick **Enforce HTTPS**.
- Then update `BASE_URL` in `build_pages.py` and rebuild, so `canonical` and `og:url` point at
  the new address instead of the github.io one.
- This doesn't touch the main site. A repo holds one custom domain, and `jwcaterine.com` stays
  with `jwcaterine-site`.

## Keeping it current

```sh
python3 build_corpus.py && python3 build_pages.py && git add docs && git commit && git push
```

`docs/index.html` and `docs/data/` are generated; `docs/README.md` and any `CNAME` are not, and
the build leaves them alone. The 851 KB JSON accumulates in git history on every regeneration —
negligible at a handful, worth knowing if it becomes a habit.

## Two open decisions

**The source PDF.** Currently gitignored. Committing it would give you a permanent copy of a
citation the division controls and could move; it costs 9.3 MB in git history forever, and
adding it later is easy while removing it is not. An Internet Archive snapshot gets you most of
the permanence for none of the weight, and the division's own copy stays the stronger citation
either way — so link theirs first regardless.

**The date label.** The export's recorded dates run 13 May – 8 June 2026, but the division
labels this same file "May 12-June 7." June 7 was a Sunday, matching the announced close; 19
responses carry a date one day *after* it, and none carry the announced open date. That
asymmetry is what a UTC-vs-Eastern offset looks like, but the export has no times, so it can't
be settled from this document. The masthead now says "responses recorded 13 May – 8 June 2026,"
which describes the data and can't be wrong either way. Worth a footnote in a longer piece; not
worth raising in a short one.
