# Devlog

Residue only — what was tried and abandoned, why a road was taken, what is still open.
The diff is in `git log`; the numbers are in the scripts.

## 2026-09-02 — Per-chart PNGs + iframe embeds (charts 2, 5, 6)

Closes the DEVLOG open item "the goal is per-chart PNGs rather than a page."
`build_chart_embeds.py` slices `charts.html` into single-chart documents: a
one-line patch to `card()` (`ONLY_CHART` guard on the sole `getElementById("cards")`
append) makes the shared script render just the wanted card while the other nine
builders run harmlessly into detached sections — cheaper than forking the script.

Two outputs per chart. The `site/embeds/*.html` keep the `<details>` table and stay
responsive (for `<iframe>` on jwcaterine.com — Substack accepts no HTML/JS/iframe,
which is the whole reason for the split). The `site/substack/*.png` hide the table
and are shot at a 760 px viewport / 3× → 2160 px wide, matching the older charts 1
and 7 shots already in the post. Chart 6's note ended "...in the table below.",
which dangles once the table is gone, so for the PNG that clause is rewritten to be
the pointer ("...in the data table at the bottom of the Substack post") rather than
having a second sentence bolted on; charts 2 and 5 notes carry no table reference
so they just get the sentence appended.

Chart 6 intro text: "two picks" → "two selections", "four picks" → "four
selections", in `charts.html` itself. The note's "most respondents picked two" was
deliberately left alone — the ask was the intro.

Open: the embeds inline unqualified selectors (`h2`, `svg text`, `.wrap`…). Fine
inside an iframe; if they ever get inlined into Astro they need re-anchoring under a
wrapper class, same bite as MIGRATION.md step 4 for the explorer.

## 2026-08-31 — Chart 5 rebuilt on overlapping categories; chart 6 labels made verbatim

Chart 5 previously assigned each respondent to exactly one bucket via a priority
cascade (parent → staff → community), which produced labels like "Staff, no child
enrolled." That was an inference, not a fact: the survey never asks whether a
respondent has a child enrolled, so the bucket really meant "checked Staff but not
Parent." Abandoned the cascade. The relationship question is check-all-that-apply,
so respondents are now counted in every category they selected. Consequence to
remember: the five rows deliberately do not sum to 1,470 (1,101 + 203 + 292 + 94 +
48 = 1,738), and the 8 records that left the question blank now appear in no
category at all — the old "Other respondents" bucket had been quietly absorbing
them. `Division Student` (97 checked, 94 answered, 47% agree) had been buried in
that same catch-all despite being the lowest-agreeing group in the survey.

Chart 6's bar labels were paraphrases of the survey options, two of them
substantively wrong ("Avoid island zones" for **Island Zones**, "Keep neighborhoods
together" for **Neighborhood Considerations**). Bars now carry each option's
verbatim header and the table twin carries the full option text, which is why
`tableTwin` grew a `textCols` argument — the existing right-align-everything-but-
column-0 rule was a deliberate earlier decision and shouldn't be reverted wholesale
just because one column now holds prose.

The "18 respondents recorded three or four picks" claim was checked against the
export's known answer-duplication artifact before being printed: 11 of the 18 do
not involve the free-text `Other boundary priority` option, so duplication does not
explain them. All 18 fall on May 13–14, which reads like the form's cap was fixed
after the first two days. Not asserted on the card — only the count is.

The bold-count "styling" ask turned out to be a selector bug: `text.t-ink` could
never match the counts, because `divergingRows` renders them on a `<tspan>`.

Open: nothing in this session was verified in a browser. Chrome could not reach a
local `http.server` (200 from curl, "site can't be reached" from the extension),
and `site/charts.html` is an Artifact *fragment* — no doctype, no `<html>`/`<body>`
— so it needs wrapping before it renders standalone at all. Chart 5's label gutter
was set to 200px (matching chart 2's 196) rather than measured. Worth an eyeball.

Also open: the goal is per-chart PNGs rather than a page. Every title, caption and
note lives in HTML *outside* the `<svg>`, so none of it survives an SVG export —
that text has to move into the SVG or be dropped. `site/substack/` holds hand-made
PNGs of charts 1, 2 and 7; the chart 2 one is now stale (retitled, note trimmed).

## 2026-09-02 — Live counts on the explorer's "who answered" chips and date bars

Both readouts are facet counts, and they need *different* bases: the chip counts
apply every filter except the roles, the bar heights apply every filter except the
date range. The tempting single-pass version — count roles, then reuse that list for
the bars — leaves the bars frozen when a role chip is clicked, since that list has
already had the date filter applied and has had roles stripped. Hence two `select()`
passes per render. Excluding each control from its own counts is also what stops the
numbers collapsing to zero the moment you use it, and keeps the bars still under the
pointer mid-drag instead of rescaling every frame.

The bars rescale to the filtered peak rather than holding the unfiltered scale. Fixed
scale loses to the existing `Math.max(8, …)` floor: a query matching thirty responses
against a 356-response peak puts every bar on the floor, so the shape goes unreadable
exactly when it is most wanted. A ghost silhouette of the unfiltered shape behind the
solid bars was considered and dropped — the two scales contradict each other visually,
and the honest fix was cheaper: the peak is now printed under the label, so the y-axis
is stated rather than implied.

Resolved the last session's blocker: Chrome genuinely cannot reach `python3 -m
http.server` started through the Bash tool, because the sandbox blocks the listening
socket — curl from inside the sandbox succeeds while the browser gets a connection
error, which is what made it look like a Chrome problem. Run the server with the
sandbox disabled and the extension connects fine. That is how this session's changes
were verified against `site/explorer.build.html`.

Note that `site/explorer.build.html` served over a bare `http.server` shows mojibake:
it is a fragment with no `<meta charset>`, and the host normally supplies the head.
`docs/index.html` is the copy to eyeball if encoding matters.

## 2026-09-07 — Custom domain, and a note about the redactions

The explorer moved to `redistricting.jwcaterine.com`. `survey.` was the name penciled into
OPTION-C.md and `redistricting.` won on being descriptive; nothing else was weighed, so if it
ever reads as too long, the switch is one DNS record and a `BASE_URL` edit. The subdomain is a
plain CNAME to `gam32bit.github.io` with a `docs/CNAME` file — no Actions workflow, no move
into the Astro site, and MIGRATION.md's Options A and B stay unbuilt.

`docs/index.html` was stale on arrival: the previous session edited `site/explorer.html` and
ran only `build_site.py`, so the Pages copy lagged two changes behind. There are two builders
over one source and neither knows about the other. Worth collapsing into one entry point, or
at least a check that fails when `docs/` predates `explorer.html`.

The new method note says redactions "show up as blank spaces," which is the reader-facing
description rather than the literal one: the division's redaction leaves a single ordinary
space, so `2 years at , then having to do 1 year at` is what's actually in the payload. Nobody
scanning the page will parse that as a gap unless told, hence the note. Resisted quantifying
how many responses are affected — the obvious regex for gap-like spacing (`\S  +\S| \.| ,`)
catches `We live .7 miles away` and any ordinary `for example,`, so its 29 is not a number
worth printing.

Confirmed while answering a question about the "Other" chip: `Other Stakeholder` is a real
survey option, one of five on the relationship question, ticked by 54 of 1,540 and alone by
only 14. What those respondents meant is unrecoverable — the export duplicated the parent
field into the `relationship_other` write-in column byte-for-byte in all 1,540 records, which
is why `build_corpus.py` drops it.
