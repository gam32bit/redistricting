<!--
DRAFT — preview copy. Chart placement is marked with fenced `chart:` blocks.
Swap each one for whatever the Astro integration ends up being (an <iframe> of
charts.html scrolled to the card, a ported component, or the PNG). Numbers here
are pinned to the arrays in site/charts.html; if you edit a figure in one place,
edit it in both.
-->

# The WJCC redistricting survey says yes — to almost everything except the reason for redistricting

*1,540 people answered the boundary survey. A majority backed adjusting attendance zones. They also ranked the enrollment problem that started this whole process dead last among the things they care about.*

---

Williamsburg–James City County Schools ran its redistricting survey from May 13 to June 8, and in early July the division published the raw results: 3,106 pages of redacted PDF, one respondent after another, no summary tables. That release is the whole record of what the community said, and almost nobody is going to read it.

So I parsed it. Every number below comes out of that file by script — no hand-counting, no sampling, and no asking a chatbot what people "generally seemed to feel." Where I count words in the open comments, I tell you the exact string I searched for, and you can retype it yourself in the [comment explorer](https://claude.ai/code/artifact/b4a10686-be66-4bb9-b564-f74c870eea6d) and get the same number back. That's the point of this piece as much as any finding in it.

Here's the finding anyway, and it's a strange one.

The survey asked whether people would support adjusting attendance zones "if necessary to better balance enrollment and address future growth." A clear majority said yes. Then the survey asked what facility planning objectives matter most — and out of seven options, **building capacity finished sixth and improved utilization of spaces finished seventh**. The two goals that *are* the enrollment-balancing case for redistricting came in last and next-to-last. Meanwhile the boundary priority respondents ranked first, by a distance, was "keep neighborhoods together" — the exact thing critics say the draft maps break.

Read together, those results describe a community that will accept redistricting in the abstract and objects to nearly every concrete rationale for it.

---

## 1. A majority supports rezoning — and the poles are three responses apart

```chart
Chart 1 — Overall support (column chart, incl. the 70 who skipped)
```

905 respondents agree, 565 disagree. That's **62% of the 1,470 people who answered the question** — a real majority, and the number the division will lead with. Note the denominator: 70 people skipped this question entirely, so it's 62% of answerers, not of all 1,540.

(The bars above are drawn as shares of all 1,540 respondents, including that grey block of 70 skips, which is why the percentages on the chart run lower than the ones in this paragraph. Same counts, different denominator — I'd rather show you the skips than hide them.)

But look at the ends of the distribution. **351 strongly agree. 354 strongly disagree.** The most committed people on each side are three responses apart, and the majority is built almost entirely out of the soft middle — 554 "somewhat agree" against 211 "somewhat disagree."

That asymmetry has a name in survey work: intensity. **63% of the people who oppose this feel strongly about it. Only 39% of supporters do.** The opposition is smaller and much harder. If you have been to a board meeting and wondered why the room sounds nothing like a 62% majority, this chart is the answer. The room is the 354.

One design note worth flagging: the survey offered no neutral option. Agree somewhat, agree strongly, disagree somewhat, disagree strongly — that was the whole ballot. There was no way to answer this question without taking a side, which inflates both wings at the expense of the genuinely undecided.

## 2. Where your kids go to school predicts what you think

```chart
Chart 2 — Support by school community (diverging stacked bars, 17 rows)
```

This is the chart that makes the politics legible.

**James River Elementary families support the plan 85%. Matthew Whaley families, 81%.** Both are schools that would *shed* neighborhoods under the draft — schools where redistricting means relief.

At the other end: **Stonehouse Elementary at 47% and Lafayette High at 49% are the only two communities in the entire survey where opponents outnumber supporters.** Lafayette is also the single largest school group in the data, with 238 respondents. Stonehouse has 133.

Everyone else lands somewhere in between, and the ordering tracks the draft maps closely enough that you could nearly reconstruct them from this chart alone. Respondents could name more than one school, so these groups overlap, and the small ones — Bright Beginnings' 29 respondents, James River's 33 — carry wide margins of error. Don't over-read a five-point gap between two small schools. Do read the thirty-eight-point spread between the top and bottom of the list.

## 3. Nearly three-quarters of the responses landed in the last eight days

```chart
Chart 3 — Responses per day, May 13 – June 8
```

For two and a half weeks this survey was quiet — roughly 20 responses a day, with a bump on May 14 when it was announced.

Then **1,125 responses, 73% of everything collected, arrived on June 1 or later.** June 5 alone brought 419 — more than the survey's entire first two weeks combined.

That is not a community steadily making up its mind. That is organized turnout, on both sides, in the final week. Which raises the obvious question of whether the late wave says something different from the early one.

## 4. June 1 belonged to the opposition — then a bigger wave answered back

```chart
Chart 4 — Support by period (diverging stacked bars, 4 rows)
```

It does, and the swing is dramatic.

Through the quiet weeks, support ran about two to one — 65% in the opening week, 67% through the middle of the survey. Then on **June 1–2, 181 responses arrived and broke 45% agree**, the only stretch of the survey where opposition led.

And then it flipped back. **The final six days brought 905 responses — five times the opposition wave — and they leaned 63% in favor.**

Both surges look organized. The June 1–2 spike is the shape of an email going out to a list; so is June 5's 419. What matters for reading the topline is that the overall 62% is not a stable measurement that held steady all month. It is the residue of two mobilizations, and the bigger one happened to be the supportive one. Run this survey with the deadline two days earlier and the headline number is meaningfully different.

## 5. Staff back the plan four-to-one; residents without kids lean against

```chart
Chart 5 — Support by relationship to the division (diverging stacked bars, 4 rows)
```

**Staff with no child enrolled agree 79% to 21%** — the most supportive group in the survey by a wide margin. The people who work inside these buildings, and who would live with the operational consequences of new boundaries, are the least worried about them.

**Parents, who are three-quarters of everyone who responded, agree 64% to 36%** — close to the overall result, which is unsurprising since they mostly *are* the overall result.

**Community members with no child in the schools are the only group where opposition wins, 56% to 44%.**

A caveat on the bucketing, because it matters: people could check several relationships, and 98 respondents are both staff and parents. To avoid double-counting I placed each person in exactly one bucket — parent first, then staff, then community member — which means the 79% staff figure covers only staff *without* enrolled children. Counted the other way, with all 203 staff respondents included, staff agree 82% to 18%. Either way staff are the most supportive group in the survey; the exclusive framing is the conservative one.

## 6. "Keep neighborhoods together" is the boundary priority, by a distance

```chart
Chart 6 — Boundary priorities (horizontal bars, 8 options)
```

Respondents got up to two picks out of eight. **Half of them — 732 of 1,466, 50% — chose "keep neighborhoods together."** Nothing else comes close; second place is "minimize impact / move the fewest students" at 601.

Then, well down the list: **capacity and utilization, 240 picks, 16%.** Fifth of eight. The mechanical problem the boundary review exists to solve is a second-tier concern for the people being surveyed about it.

This is the chart to hold next to any claim that the community endorsed the draft maps. What the community endorsed, when asked directly, is neighborhood cohesion — and neighborhood cohesion is precisely the value the loudest objections to the draft maps invoke. Ford's Colony being split between zones is a "keep neighborhoods together" complaint. So is Kingsmill's proposed move.

(The shares sum past 100% because most people used both picks. The form also didn't enforce its own limit — 18 people got three or four selections recorded, which is why the bars total 2,942 instead of the 2,932 ceiling. Small, but I'd rather you hear it from me than find it yourself.)

## 7. Capacity — the reason for redistricting — ranks near the bottom of what people want

```chart
Chart 7 — Facility planning objectives (horizontal bars, 7 options)
```

Same story, different question, and here it's starker.

Asked which facility planning objectives matter most — two choices, 1,419 people answering — respondents picked **safety and security (855, 60%)** and **enhanced educational opportunities (793, 56%)**. Everything else is far behind.

**Building capacity: 202, 14%. Improved utilization of spaces: 155, 11%.** Sixth and seventh out of seven.

I want to be careful about what this does and doesn't show. It doesn't show that WJCC has no capacity problem — enrollment projections are a fact about buildings, not an opinion, and a community can be wrong about what it needs. What it shows is that if the division builds its case for new boundaries on capacity and utilization, it is arguing from the two objectives its own survey respondents ranked last. That's a communications problem at minimum, and it goes some way toward explaining why the process feels to so many people like an answer in search of a question.

## 8. Class and diversity run through the open comments

```chart
Chart 8 — Themes in open comments (horizontal bars, class/diversity cluster highlighted)
```

The survey's free-text fields are where the actual argument lives, and they're also where write-ups like this one usually go wrong — someone reads a sample, forms an impression, and reports the impression as a finding.

I've tried to do this so you can check it. Each bar counts **respondents whose written answers contain a literal string**, and the chart labels the exact string. Nothing is inferred. Type the same string into the [comment explorer](https://claude.ai/code/artifact/b4a10686-be66-4bb9-b564-f74c870eea6d) and you get the same number and the actual comments behind it.

Biggest single topic: **"neighborhood," 419 respondents, 27%** — consistent with chart 6.

But the highlighted cluster is the story. Combine the people who wrote **"divers" (261), "socio" (182), "equit" (103), "segregat" (72)** or **"title 1" (20)**, and you get **416 distinct respondents — 27% of everyone who took the survey.** (Coincidentally the same 27% as the neighborhoods bar; the two are separate groups of people that happen to land on nearly the same count.) More than one in four people, unprompted, brought up class or racial composition in a survey that never asked about either.

Read the comments and it's clear what they're arguing about: which neighborhoods get pulled out of high-poverty schools, and who benefits. Both sides use this vocabulary. A "diversity" mention is as likely to be someone objecting to socioeconomic balancing as someone demanding it — the count measures salience, not stance, and I'd be misleading you if I implied otherwise.

Two honest limits on these counts. Substrings catch word families, which is usually what you want ("bus" picks up busing and busses) but occasionally overshoots — three respondents matched "bus" only through *business* or *robust*. And the "together" bar, 187 respondents, is mostly "keep neighborhoods together," which overlaps the top bar rather than adding to it. I left the strings loose on purpose: a tighter regex would count better and would no longer be something you could reproduce by typing a word into a search box, and reproducibility is worth more here than a couple of percentage points.

## 9. Ford's Colony is the neighborhood on everyone's mind

```chart
Chart 9 — Neighborhoods named in comments (horizontal bars, 9 places)
```

**Ford's Colony, 115 respondents** — nearly twice as often as the next place on the list, and more than twice as often as Kingsmill. It's the neighborhood the draft plan splits between attendance zones, and splitting it collides head-on with the survey's top-ranked priority.

**Norge, 64. Kingsmill, 56.** Kingsmill's proposed move out of James River Elementary is the anchor of the socioeconomic argument in both directions, and it's worth noting that James River's own families are the most supportive group in the survey (chart 2).

Then a long tail: Wellington 33, Toano 24, Kingspoint 22, Grove 12, Powhatan 10, The Meadows 5.

Same reproducibility caveat, plus one specific to place names: Norge and Toano are schools as well as areas. 8 of Norge's 64 and 3 of Toano's 24 mention only the school, so treat those two bars as a ceiling for the neighborhood.

## 10. The buildings themselves get good marks

```chart
Chart 10 — Perceived facility condition (column chart, 5 ratings)
```

A useful control, and a quiet rebuke to a certain kind of argument.

Of the 1,437 people who rated the condition of the facilities they're associated with, **76% said excellent or good. Under 5% said poor or unsatisfactory.**

Whatever this fight is about, it is not about the buildings. It's about who attends which one.

---

## What I think this adds up to

Three things, and I'd separate them by how confident I am.

**Confident:** the survey does not deliver the mandate its topline suggests. 62% support, measured on a no-neutral-option ballot, arriving in two organized waves, from a self-selected sample — that is a soft number. The hard numbers underneath it are 354 strongly opposed against 351 strongly in favor, and a stated priority ("keep neighborhoods together") that the draft maps violate in the most-discussed case in the data.

**Fairly confident:** the division has a framing problem. Capacity and utilization finished last among facility objectives and fifth of eight among boundary priorities. If the case for redistricting is going to be made to this community, it will have to be made on safety or educational opportunity — the two things respondents actually said they want — or it will keep landing as a bureaucratic imposition regardless of how sound the enrollment math is.

**Not confident, but worth watching:** the class-and-diversity cluster at 27% is the largest unprompted theme in a survey that never raised the subject. The division's public materials talk about balance and utilization. More than a quarter of respondents are, in their own words, having a different conversation — about which schools serve which neighborhoods and whether that's going to change. That gap between the official frame and the actual one seems to me like the thing to watch as the board moves toward a vote.

---

## Method, and how to check me

Everything here comes from *Redistricting Survey Raw Results — Final* (WJCC Schools / MGT, June 2026), the 3,106-page redacted PDF the division published. Three things you should know about how it was processed:

**The PDF is booby-trapped, and I don't think that's deliberate.** Its embedded font maps the characters `f`, `ff`, `fi` and `fl` to unused codepoints. Every PDF text extractor I tried — pdftotext, PyMuPDF, all of them — silently *deletes* those characters with no warning. Straight extraction gives you "La ayette" for "Lafayette," "speci c" for "specific," "amilies" for "families." If you pull this PDF and count keywords, you will undercount every term containing an f, and nothing will tell you. The glyphs are recoverable — the character positions are intact, only the Unicode mapping is junk — and they were restored before anything was counted here. **If you cross-check my numbers against your own extraction and get different ones, this is almost certainly why.** My first pass at this analysis was wrong for exactly this reason.

**The export duplicates answers.** The published file repeats a single response across whole question groups — identical across the elementary, middle and high school scenarios in 1,539 of 1,540 records, and between "where the division does well" and "a wish for the division" in 1,015 of 1,018. That's an export artifact, not people saying the same thing three times. Comment counts here are **per respondent**, never per school level. Counting the naive way roughly triples every free-text total.

**This is not a poll.** It's a self-selected feedback survey, so it measures who showed up. Respondents could name several schools, so school communities overlap. Keyword counts are substring matches and don't capture stance. Percentages are rounded and may not sum to 100.

The [full ten-chart version is here](https://claude.ai/code/artifact/8b98e6fc-3a69-48b2-b8c7-8db20634f210), with a data table under every chart. The [comment explorer is here](https://claude.ai/code/artifact/b4a10686-be66-4bb9-b564-f74c870eea6d) — search the open comments yourself, filter by school or role, and download the whole corpus as CSV if you'd rather do your own counting. I'd genuinely rather you did.
