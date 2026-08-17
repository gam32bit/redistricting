#!/usr/bin/env python3
"""Parse survey_clean.txt into per-respondent records.

Differences from the original parse_survey.py:
  * reads the f-repaired extraction, so no ligature-tolerant fuzzy matching
  * matches the FULL question text, not a truncated prefix -- the truncation is
    what left question preamble glued onto answers ("in the school(s) you are
    associated with | Unsatisfactory")
  * answers are located between question matches, so page-break artifacts
    collapse into ordinary whitespace instead of splitting a field

Output: records_clean.json
"""
import json
import re
from collections import Counter

SRC = "survey_clean.txt"
OUT = "records_clean.json"

# Exact, full question text as it appears in the export.
QUESTIONS = {
    "relationship": "What describes your relationship to WJCC Schools? (check all that apply):",
    "relationship_other": "What describes your relationship to WJCC Schools? (check all that apply) - Other Stakeholder - Text",
    "employee_where": "If you are an employee of WJCC Schools, where do you work?",
    "school": "If you have a child (or are a student) that attends school in WJCC Schools, what school do they attend?",
    "proud": "In a few words, please describe an area or focus where the Division does well. (What are you most proud of in your schools?)",
    "wish": "In a few words, please describe an area or focus for improvement in the Division. (A wish for the Division)",
    "facilities": "What is your perception of the overall condition of the school facilities in the school(s) you are associated with",
    "objectives": "What facility planning objectives are MOST important to you? (Choose 2)",
    "support_zones": "I would support adjusting attendance zones if necessary to better balance enrollment and address future growth.",
    "priorities": "Which priorities do you consider most important in the development of new school boundaries? (choose up to 2) - Selected Choice",
    "priorities_other": "Which priorities do you consider most important in the development of new school boundaries? (choose up to 2) - Other boundary priority - Text",
    "feeder_realign": "The Division should realign the middle school and high school feeder patterns to align with new elementary boundaries and alleviate future and current utilization concerns at the secondary schools",
    "critical_issue": "In a few words, please describe what you feel is the most critical issue to be addressed in the development of these boundary scenarios.",
    "pos_es": "What is one positive outcome/potential benefit that you could see coming from the Elementary School scenario presented?",
    "pos_ms": "What is one positive outcome/potential benefit that you could see coming from the Middle School scenario presented?",
    "pos_hs": "What is one positive outcome/potential benefit that you could see coming from the High School scenarios presented?",
    "concern_es": "What do you see as the biggest concern for the Elementary School scenario presented?",
    "concern_ms": "What do you see as the biggest concern for the Middle School scenario presented?",
    "concern_hs": "What do you see as the biggest concern for the High School scenario presented?",
    "additional": "Do you have any additional thoughts on this topic or information you want to share? What other questions do you need answered? Do you have any additional recommendations for the Division?",
    "email_q": "If you'd like the Division to reach out to you directly to answer a specific question about your situation, please include your email below.",
}

# Longest first: no question is a prefix of another, but matching long-to-short
# keeps that from silently mattering if the export ever changes.
ORDER = sorted(QUESTIONS, key=lambda k: -len(QUESTIONS[k]))
PATTERNS = {
    k: re.compile(re.escape(QUESTIONS[k]).replace(r"\ ", r"\s+"), re.IGNORECASE)
    for k in QUESTIONS
}


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def parse_record(chunk: str) -> dict:
    # The chunk opens with the page's trailing space, then the timestamp on its
    # own line, so take the first line that actually has content.
    lines = chunk.split("\n")
    date, body_start = "", 0
    for i, line in enumerate(lines):
        if line.strip():
            date, body_start = collapse(line), i + 1
            break
    rec = {"date": date}
    body = "\n".join(lines[body_start:])

    spans = []  # (start, end, key)
    taken = []
    for key in ORDER:
        for m in PATTERNS[key].finditer(body):
            if any(m.start() < e and s < m.end() for s, e in taken):
                continue  # overlaps an already-claimed question
            spans.append((m.start(), m.end(), key))
            taken.append((m.start(), m.end()))
            break  # first occurrence wins
    spans.sort()

    for i, (_, end, key) in enumerate(spans):
        nxt = spans[i + 1][0] if i + 1 < len(spans) else len(body)
        rec[key] = collapse(body[end:nxt])
    for key in QUESTIONS:
        rec.setdefault(key, "")
    rec["_found"] = len(spans)
    return rec


def main() -> None:
    text = open(SRC).read()
    chunks = text.split(">> Recorded Date <<")[1:]
    records = [parse_record(c) for c in chunks]

    print(f"records: {len(records)}")
    found = Counter(r["_found"] for r in records)
    print(f"questions located per record: {dict(sorted(found.items()))}")

    empty = Counter()
    for r in records:
        for k in QUESTIONS:
            if not r[k]:
                empty[k] += 1
    print("\nblank answers per field:")
    for k in QUESTIONS:
        print(f"  {k:20s} {empty[k]:5d} blank / {len(records)}")

    # How often are the ES/MS/HS answers literally identical? (export artifact)
    for a, b, c, label in [
        ("pos_es", "pos_ms", "pos_hs", "positive"),
        ("concern_es", "concern_ms", "concern_hs", "concern"),
    ]:
        same = sum(1 for r in records if r[a] == r[b] == r[c])
        nonblank = sum(1 for r in records if r[a] or r[b] or r[c])
        print(f"\n{label}: all three levels identical in {same}/{len(records)} "
              f"({nonblank} answered at least one level)")

    json.dump(records, open(OUT, "w"), indent=0)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
