# Devlog

Residue only — what was tried and abandoned, why a road was taken, what is still open.
The diff is in `git log`; the numbers are in the scripts.

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
