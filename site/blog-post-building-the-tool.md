---
title: How I built the redistricting survey explorer
date: 2026-08-21
description: A companion piece on making a search page for the WJCC survey — what I trusted AI to handle without checking, and what I insisted on deciding myself.
tags: ['tools', 'AI', 'redistricting', 'behind-the-scenes']
draft: true
---

<!-- Target: src/content/blog/2026-08-21-how-i-built-the-redistricting-survey-explorer/index.md
     Companion to the Substack findings post and to site/blog-post-search-page.md
     (the short reader-facing announcement). This one is about the process of directing
     the build, told through what I actually asked for.
     Replace SEARCH_PAGE_URL, CHARTS_URL, SUBSTACK_POST_URL below. -->

I wrote a [separate post](SUBSTACK_POST_URL) about what 1,540 people actually said in the
WJCC redistricting survey. This one is about the tool I built to let you check my work — and
about what "built" actually meant, since I did it with AI assistance from Claude Code.

The honest answer to "how much of this did you write yourself" is: none of the code, and all
of the decisions that mattered. I want to walk through what that split actually looked like,
because I think it's a more useful thing to read than either "AI built my app" or a line-by-
line account of code I didn't write.

## Where it started: I decided reading wasn't going to work

I'd heard the survey results would be posted at the end of June, and they were — one PDF,
3,106 pages. I looked at it and did the math on how long it would take to actually read, and
decided it would be easier for me to browse if I built something to search it instead. That
was the whole brief, and it was mine: nobody suggested building a tool, I looked at an
unreadable document and decided that was the fix.

## Starting broad, then doing the actual curating myself

My first real prompt on this project was open-ended: "produce 10 charts of whatever you
think the most interesting insights are." I wanted a survey of the data before I decided
what mattered, and letting the charts get proposed first was faster than me guessing at
categories from raw text.

But picking which charts actually went where was mine, and it wasn't a small decision.
Three of the ten — support, the by-school breakdown, and facility objectives — needed to
work as static images in a Substack newsletter that strips JavaScript, so those had to stand
completely on their own. The other seven could assume a reader willing to click through to a
longer post. I also flagged early that chart 1 shouldn't be a pie chart, with the 70 who
skipped the question shown as a grey slice — I wanted that skip count visible, not folded
into a caveat below the chart. That's an editorial call about what a reader needs to see
without having to read a footnote, not something a chart-generation prompt gets right on
its own.

## The call that mattered most: comments don't get charted

Here's the decision I care most about explaining, because I think it's the one worth other
people copying.

Once I'd settled on which multiple-choice charts to use, I still had five free-text
questions — the parts of the survey where people wrote whatever they wanted. My reasoning
for not turning those into a chart too, in the words I actually used at the time: doing that
would mean "asking the AI to interpret the data which is sus."

That's the whole design principle behind the explorer. A multiple-choice answer is a fact —
someone clicked "strongly agree," and a chart of that is just counting. A paragraph someone
wrote is not a fact until something decides what it means, and I didn't want that something
to be an AI producing a tidy, confident-sounding summary of over a thousand people's words
that I'd then have no way to check.

So instead of asking for a summary, I asked for options: what else could I do to let people
interact with the open comments themselves. I reviewed what came back, and only greenlit it
once I was satisfied — "all of your suggestions sound good... proceed." The tool that came
out of that is a search box, not a summarizer. Every count it shows you is a literal
substring match, and it shows you the exact string next to the number, so you can retype it
and get the same answer back. That constraint — no paraphrasing, no ranking by relevance, no
"themes" invented by a model — was the requirement I set, and everything about how the
explorer works follows from it.

## What I never had to think about, and that's the point

In the middle of all this, two things went wrong with the underlying data pipeline that I
never had to notice: the source PDF had a font bug that silently deleted certain letters
from every extraction, and an early version of the parser occasionally glued leftover
question text onto the front of an answer. Both were caught and fixed before I ever saw
their effects.

I'm mentioning this because it's the actual shape of the division of labor here, not a
side note. The mechanical, checkable work — does this extraction reproduce every character,
does this parser split records at the right boundary — is exactly the kind of thing I was
comfortable not personally verifying, because it's the kind of thing that can be verified at
all. Somebody (or something) can check a character count against the source and know for
certain whether it's right. What I kept for myself was everything that isn't checkable that
way: what a chart should be titled so it tells the true story, what counts as too much
interpretation of a stranger's paragraph, what a reader needs to be told before they trust a
number.

## The line-by-line rounds, where the actual authorship is

Most of the real work, prompt to prompt, was editing — and it's where you can see what I
actually cared about, because I was specific about all of it.

**Rewriting a chart's story, not just its label.** The first chart, on support, initially
had a title that didn't land. What I actually wanted it to say was that while a majority
supports redistricting, the minority that opposes it is more intensely committed than the
majority that supports it — strong disagreement outnumbering strong agreement even as total
agreement wins. That's an argument about the data, not just a caption, and it took me saying
it in plain language before the chart said it right.

**Cutting language that assumed things I hadn't established.** I pulled a line claiming
"there is no way to answer without taking a side" and had the actual quoted survey language
bolded instead of that framing. I changed "where your kids go to school" to "your school
predicts what you think" once I realized the chart covered all respondents, not just
parents — a wording that implied something the data didn't actually show.

**Fixing a factual error across the whole tool.** At one point I caught that everything —
charts and table both — used "rezoning" when the correct word, the one the district itself
uses, is "redistricting." That's not a style note; it's the actual term of art, and getting
it wrong everywhere would have undercut the tool's credibility with the audience who knows
the difference.

**Finding an actual bug by just using the thing.** I noticed the table only showed 1,374 of
1,540 responses by default and asked why — a real discrepancy I caught by looking at the
page, not something flagged for me.

**Rejecting an explanation I didn't understand and replacing it with my own.** When a chart
note used the phrase "carry wide error bars," I said I didn't get what that meant and that
the explanation I'd been given didn't make sense either — then wrote the plain-language
version myself: put the respondent count next to each school and tell the reader to keep
that number in mind when reading the percentage next to it. That's a better explanation than
the statistical term, and it's mine.

**Replacing dropdowns with something a reader would actually use.** I asked for the filter
controls — relationship to the district, survey answer, date range — to become clickable
pills instead of dropdown menus, and asked for a completely different interaction for the
date filter: a timeline a reader could click a point on, or drag across a range. That's a
UI decision made by picturing an actual person on the page, not a default.

## Insisting on disclosure, in my own terms

When I got to the explorer's "how this works" section, I was specific about what it needed
to say: that the tool was developed with assistance from Claude Code, including some of its
text; that AI can make mistakes; and what precautions were taken to keep the numbers
accurate against the source PDF. I also asked for a claim to be reframed — instead of
implying nobody checked that respondents lived in the district, the tool now says the survey
intake form didn't require residency verification and didn't prevent someone from answering
more than once. That's a more honest, more precise claim than the one I started with, and it
came from me pushing back on wording that overstated what I actually knew.

None of that disclosure was a default the tool shipped with. I asked for it, specified what
it had to cover, and rewrote it until it said exactly what I meant.

## Deciding where this thing lives

Near the end, I asked what I should even call this interface, and where it should live.
The first idea was folding it into my personal site, built with Astro. I looked at what that
would require — style rules that would need to be kept from leaking, a client-side router
the explorer's script would have to work around — and decided against it. A search tool
isn't an article, and it didn't need to inherit a blog's plumbing to be useful. It got its
own repository and its own GitHub Pages deployment instead, linked from the site rather than
folded into it.

Even after I called it "ready for primetime," I kept coming back with small corrections —
reverting a filter style I'd changed my mind about, fixing a label, moving the download
buttons back onto their own line after a pass had knocked them out of place. That's not
scope creep; it's what actually shipping something you intend to hand to other people looks
like. The bar isn't "does it work," it's "does every part of it say exactly what I meant."

## What this adds up to

I didn't write the extraction script, the parser, or the interface code, and I'm not going
to pretend otherwise. What I did was make every decision that required actually caring what
the survey says and how a stranger reading it for the first time would understand it: which
findings to lead with, where AI-generated interpretation was and wasn't acceptable, which
words were factually wrong, which explanations didn't make sense, and what the tool owed its
readers about its own construction. The code is generated. The judgment isn't, and that's
the part I'd want anyone building something similar to actually spend their time on.

**[The search page is here →](SEARCH_PAGE_URL).** **[The ten-chart overview is here →](CHARTS_URL).**
And if you want the findings rather than the process — the actual survey results — that's
the [companion post](SUBSTACK_POST_URL).
