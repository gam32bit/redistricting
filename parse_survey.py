#!/usr/bin/env python3
"""Parse WJCC redistricting survey raw-results text into structured records."""
import json
import re
from collections import Counter, defaultdict

TEXT = open("survey_raw.txt").read()

# Question headers in order of appearance (prefix match on normalized text)
QUESTIONS = {
    "relationship": "What describes your relationship to WJCC Schools? (check all that apply):",
    "relationship_other": "What describes your relationship to WJCC Schools? (check all that apply) - Other Stakeholder - Text",
    "employee_where": "If you are an employee of WJCC Schools, where do you work?",
    "school": "If you have a child (or are a student) that attends school in WJCC Schools, what school do they attend?",
    "proud": "In a few words, please describe an area or focus where the Division does well.",
    "wish": "In a few words, please describe an area or focus for improvement in the Division.",
    "facilities": "What is your perception of the overall condition of the school facilities",
    "objectives": "What facility planning objectives are MOST important to you? (Choose 2)",
    "support_zones": "I would support adjusting attendance zones if necessary to better balance enrollment and address future growth.",
    "priorities": "Which priorities do you consider most important in the development of new school boundaries? (choose up to 2) - Selected Choice",
    "priorities_other": "Which priorities do you consider most important in the development of new school boundaries? (choose up to 2) - Other boundary priority - Text",
    "feeder_realign": "The Division should realign the middle school and high school feeder patterns",
    "critical_issue": "In a few words, please describe what you feel is the most critical issue to be addressed",
    "pos_es": "What is one positive outcome/potential benefit that you could see coming from the Elementary School scenario presented?",
    "pos_ms": "What is one positive outcome/potential benefit that you could see coming from the Middle School scenario presented?",
    "pos_hs": "What is one positive outcome/potential benefit that you could see coming from the High School scenarios presented?",
    "concern_es": "What do you see as the biggest concern for the Elementary School scenario presented?",
    "concern_ms": "What do you see as the biggest concern for the Middle School scenario presented?",
    "concern_hs": "What do you see as the biggest concern for the High School scenario presented?",
    "additional": "Do you have any additional thoughts on this topic or information you want to share?",
    "email_q": "If you'd like the Division to reach out to you directly",
}


def norm(s: str) -> str:
    """Collapse whitespace for header matching."""
    return re.sub(r"\s+", " ", s).strip()


records = []
chunks = TEXT.split(">> Recorded Date <<")
for chunk in chunks[1:]:
    lines = chunk.split("\n")
    rec = {"date": lines[0].strip() if lines else ""}
    # Walk lines; when a line starts a known question header (possibly wrapped
    # over 2-3 lines), capture following lines as the answer until next header.
    # Build normalized full text with line index mapping.
    body = "\n".join(lines[1:])
    # Find header positions: try to match each question header allowing line wraps
    positions = []  # (char_pos, key, header_end_pos)
    nbody = body
    for key, header in QUESTIONS.items():
        # Build regex: escape header, allow flexible whitespace, tolerate
        # dropped f/ff/fi ligatures in extraction
        pat = re.escape(norm(header))
        pat = pat.replace(r"\ ", r"\s+")
        # ligature tolerance: letters f may be missing
        pat = pat.replace("f", "f?")
        for m in re.finditer(pat, body, flags=re.IGNORECASE):
            positions.append((m.start(), key, m.end()))
    positions.sort()
    for i, (start, key, end) in enumerate(positions):
        nxt = positions[i + 1][0] if i + 1 < len(positions) else len(body)
        ans = body[end:nxt].strip()
        # answers may repeat question tail chars; just store
        if key not in rec:  # first match wins
            rec[key] = ans
    records.append(rec)

print(f"Parsed {len(records)} records")
missing = Counter()
for r in records:
    for k in QUESTIONS:
        if k not in r:
            missing[k] += 1
print("Fields missing (unmatched header) counts:", dict(missing))

json.dump(records, open("records.json", "w"), indent=0)
