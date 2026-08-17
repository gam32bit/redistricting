#!/usr/bin/env python3
"""Corrected aggregate analysis for WJCC redistricting survey."""
import json
import re
from collections import Counter
from datetime import datetime

TEXT = open("survey_raw.txt").read()
records = json.load(open("records.json"))
N = len(records)

# --- Fix dates: pull from raw text directly ---
dates = re.findall(r">> Recorded Date <<\s*\n\s*(\d+/\d+/\d+)", TEXT)
days = Counter(dates)
print(f"=== Responses by day (n dates found: {len(dates)}) ===")
for d, c in sorted(days.items(), key=lambda x: datetime.strptime(x[0], "%m/%d/%Y")):
    print(f"{d}: {c}")

def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()

# --- Likert helpers ---
def likert(t):
    t = clean(t).lower()
    for tail in ["in the school(s) you are associated with",
                 "to align with new elementary boundaries and alleviate future and current utilization concerns at the secondary schools"]:
        if t.startswith(tail):
            t = t[len(tail):].strip()
    for l in ["strongly agree", "somewhat agree", "somewhat disagree", "strongly disagree",
              "excellent", "good", "fair", "poor", "unsatis"]:
        if t.startswith(l):
            return l
    return "(blank)" if not t else "UNPARSED:" + t[:40]

sup = Counter(likert(r.get("support_zones")) for r in records)
fed = Counter(likert(r.get("feeder_realign")) for r in records)
fac = Counter(likert(r.get("facilities")) for r in records)
LIK = ["strongly agree", "somewhat agree", "somewhat disagree", "strongly disagree", "(blank)"]
print("\n=== Support adjusting attendance zones ===")
for k in LIK:
    print(f"{k}: {sup.get(k,0)} ({100*sup.get(k,0)/N:.1f}%)")
print("agree total:", sup["strongly agree"]+sup["somewhat agree"],
      "| disagree total:", sup["strongly disagree"]+sup["somewhat disagree"])
print("\n=== Realign MS/HS feeder patterns ===")
for k in LIK:
    print(f"{k}: {fed.get(k,0)} ({100*fed.get(k,0)/N:.1f}%)")
print("agree total:", fed["strongly agree"]+fed["somewhat agree"],
      "| disagree total:", fed["strongly disagree"]+fed["somewhat disagree"])
print("\n=== Facilities perception ===")
for k in ["excellent", "good", "fair", "poor", "unsatis", "(blank)"]:
    print(f"{k}: {fac.get(k,0)} ({100*fac.get(k,0)/N:.1f}%)")

# --- Priorities (correct option list, ligature-tolerant) ---
PRI = [
    ("Transportation", "Transportation (bus time/safe stops)"),
    ("Minimize Impact", "Minimize Impact (move fewest students, long-term boundaries)"),
    ("Neighborhood Consider", "Neighborhood Considerations (keep neighborhoods together)"),
    ("Demographics", "Demographics (racial/ethnic diversity + socioeconomic)"),
    ("Natural Barriers", "Natural Barriers & Major Roads"),
    ("Capacity & Utilization", "Capacity & Utilization"),
    ("Other boundary", "Other boundary priority"),
]
pri = Counter(); pri_blank = 0
for r in records:
    t = clean(r.get("priorities"))
    if not t:
        pri_blank += 1
        continue
    for pat, label in PRI:
        if pat.lower() in t.lower():
            pri[label] += 1
answered = N - pri_blank
print(f"\n=== Boundary priorities (choose up to 2; answered={answered}) ===")
for k, c in pri.most_common():
    print(f"{k}: {c} ({100*c/answered:.1f}% of answered)")

# --- Objectives (correct option list) ---
OBJ = [("Sa ety and Security", "Safety and Security"),
       ("Safety and Security", "Safety and Security"),
       ("Enhanced Educational", "Enhanced Educational Opportunities"),
       ("Consistent Facilities", "Consistent Facilities Division-Wide"),
       ("Building Condition", "Building Condition"),
       ("Building Capacity", "Building Capacity"),
       ("Extracurr", "Improved Extracurricular Activities"),
       ("Improved Utilization", "Improved Utilization of Building Spaces")]
obj = Counter(); obj_blank = 0
for r in records:
    t = clean(r.get("objectives"))
    if not t:
        obj_blank += 1
        continue
    seen = set()
    for pat, label in OBJ:
        if pat.lower() in t.lower() and label not in seen:
            obj[label] += 1
            seen.add(label)
oanswered = N - obj_blank
print(f"\n=== Facility objectives (choose 2; answered={oanswered}) ===")
for k, c in obj.most_common():
    print(f"{k}: {c} ({100*c/oanswered:.1f}% of answered)")

# --- School mention counts (from 'what school do they attend', substring) ---
SCHOOLS = ["Matthew Whaley", "James River", "Clara Byrd Baker", "D.J. Montague",
           "J. Blaine Blayton", "Laurel Lane", "Matoaka", "Norge", "Rawls Byrd",
           "Stonehouse", "Berkeley Middle", "James Blair Middle", "Hornsby",
           "Toano Middle", "Jamestown High", "La ayette High", "Warhill High"]
sch = Counter()
for r in records:
    t = clean(r.get("school"))
    for s in SCHOOLS:
        if s.lower() in t.lower():
            sch[s.replace("La ayette", "Lafayette")] += 1
print("\n=== Respondents with a child at each school (multi) ===")
for k, c in sch.most_common():
    print(f"{k}: {c}")

# --- Cross-tab: zone support by school community ---
print("\n=== Support adjusting zones × school community (agree% / disagree% / n) ===")
for s in SCHOOLS:
    rows = [r for r in records if s.lower() in clean(r.get("school")).lower()]
    if len(rows) < 15:
        continue
    c = Counter(likert(r.get("support_zones")) for r in rows)
    n = len(rows)
    ag = c["strongly agree"] + c["somewhat agree"]
    dg = c["strongly disagree"] + c["somewhat disagree"]
    print(f"{s.replace('La ayette','Lafayette'):25s} n={n:4d}  agree {100*ag/n:4.0f}%  disagree {100*dg/n:4.0f}%  (strongly disagree {100*c['strongly disagree']/n:.0f}%)")

# --- Email/contact fix ---
tail = "to answer a specific question about your situation, please include your email below."
def email_ans(r):
    t = clean(r.get("email_q"))
    tl = t.lower()
    # strip question tail (ligature-tolerant compare)
    stripped = re.sub(r"^to answer a speci.?ic question about your situation,?\s*please include your email below\.?", "", t, flags=re.I).strip()
    return stripped
contact = sum(1 for r in records if len(email_ans(r)) > 3)
print(f"\nRespondents writing something in the contact field: {contact} ({100*contact/N:.1f}%)")

# --- Timeline by date done above; also date range ---
dts = sorted(datetime.strptime(d, "%m/%d/%Y %I:%M:%S %p")
             for d in re.findall(r">> Recorded Date <<\s*\n\s*([\d/]+ [\d:]+ [AP]M)", TEXT))
print(f"\nFirst response: {dts[0]}  Last response: {dts[-1]}")
