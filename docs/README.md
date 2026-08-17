# Search the WJCC redistricting survey

A search page for the written responses to the Williamsburg–James City County Schools
redistricting survey, May–June 2026.

Everything here comes from the division's own published raw results — a 3,106-page PDF of
1,540 responses, of which 1,374 contain at least one written answer:

<https://wjccschools.org/wp-content/uploads/2026/06/Redacted-Redistricting-Survey-Raw-Results-Final-June-2026.pdf>

Response text is reproduced verbatim. Nothing is summarized, ranked or interpreted; search
is plain case-insensitive substring matching, so the same query always returns the same
responses. The page discloses its own methodology and limitations under "How this works."

## Files

| File | What it is |
|---|---|
| `index.html` | The whole page — markup, styles and script, no dependencies. |
| `data/comments.json` | The corpus the page fetches, 851 KB (247 KB gzipped). |
| `.nojekyll` | Tells GitHub Pages to serve paths as-is. |

The page's Download CSV and Download JSON buttons build their files in the browser from
whatever rows are currently filtered, so there is no CSV in this repo to keep in sync.

## Generated — don't edit by hand

`index.html` and `data/` are built by `build_pages.py` in a separate working repo, from the
source PDF. Hand-edits here are overwritten on the next build. Fix things upstream.

## Deploying

GitHub Pages, Settings → Pages → deploy from branch `main`, folder `/` (root). No build
step, no Actions workflow.

The page fetches `data/comments.json` by **relative** path, so it works both at
`<user>.github.io/<repo>/` and at a custom domain. Don't change it to an absolute `/data/...`
— that breaks the project-subpath URL.
