#!/usr/bin/env python3
"""Aggregate stats for WJCC redistricting survey."""
import json
import re
from collections import Counter
from datetime import datetime

records = json.load(open("records.json"))
N = len(records)


def fixlig(s: str) -> str:
    """Best-effort repair of dropped f-ligatures for known words."""
    repl = {
        " o Division": " of Division", "Parent/Guardian o ": "Parent/Guardian of ",
        "Sta Member": "Staff Member", "La ayette": "Lafayette",
    }
    for a, b in repl.items():
        s = s.replace(a, b)
    return s


# --- Timeline ---
days = Counter()
for r in records:
    d = r["date"].split()[0] if r.get("date") else "?"
    days[d] += 1
print("=== Responses by day ===")
def daykey(d):
    try:
        return datetime.strptime(d, "%m/%d/%Y")
    except ValueError:
        return datetime.max
for d, c in sorted(days.items(), key=lambda x: daykey(x[0])):
    print(f"{d}: {c}")

# --- Relationship (multi-select, comma-separated) ---
ROLES = ["Parent/Guardian", "Division Staff Member", "Division Sta Member",
         "Community Member", "Division Student", "Other Stakeholder",
         "Business Owner", "Future", "Former"]
rel = Counter()
for r in records:
    t = fixlig(r.get("relationship", ""))
    found = False
    if "Parent/Guardian of Division Student" in t:
        rel["Parent/Guardian"] += 1; found = True
    if "Staff Member" in t:
        rel["Division Staff Member"] += 1; found = True
    if "Community Member" in t:
        rel["Community Member"] += 1; found = True
    if re.search(r"\bStudent\b(?! \()", t) and "Parent" not in t:
        rel["Student (self)"] += 1; found = True
    if "Other" in t:
        rel["Other Stakeholder"] += 1; found = True
    if not t.strip():
        rel["(blank)"] += 1; found = True
    if not found:
        rel["UNPARSED: " + t[:60]] += 1
print("\n=== Relationship (multi-select) ===")
for k, c in rel.most_common(15):
    print(f"{k}: {c}")

# --- School attended ---
schools = Counter()
for r in records:
    t = fixlig(r.get("school", "")).strip()
    t = re.sub(r"\s+", " ", t)
    if not t:
        schools["(blank)"] += 1
        continue
    # multiple schools may be comma separated
    schools[t[:80]] += 1
print("\n=== School attended (top 30 raw values) ===")
for k, c in schools.most_common(30):
    print(f"{k}: {c}")

# --- Likert: support adjusting zones ---
LIK = ["Strongly agree", "Somewhat agree", "Neither", "Somewhat disagree", "Strongly disagree"]
sup = Counter()
for r in records:
    t = re.sub(r"\s+", " ", r.get("support_zones", "")).strip().lower()
    matched = next((l for l in LIK if t.startswith(l.lower())), None)
    if matched is None and "neither" in t:
        matched = "Neither"
    sup[matched or ("(blank)" if not t else "UNPARSED:" + t[:40])] += 1
print("\n=== 'I would support adjusting attendance zones...' ===")
for k in LIK + ["(blank)"]:
    if sup.get(k):
        print(f"{k}: {sup[k]} ({100*sup[k]/N:.1f}%)")
for k, c in sup.items():
    if k.startswith("UNPARSED"):
        print(k, c)

# --- Likert: feeder realignment ---
fed = Counter()
for r in records:
    t = re.sub(r"\s+", " ", r.get("feeder_realign", "")).strip().lower()
    matched = next((l for l in LIK if t.startswith(l.lower())), None)
    if matched is None and "neither" in t:
        matched = "Neither"
    fed[matched or ("(blank)" if not t else "UNPARSED:" + t[:40])] += 1
print("\n=== 'Division should realign MS/HS feeder patterns...' ===")
for k in LIK + ["(blank)"]:
    if fed.get(k):
        print(f"{k}: {fed[k]} ({100*fed[k]/N:.1f}%)")
for k, c in fed.items():
    if k.startswith("UNPARSED"):
        print(k, c)

# --- Facilities perception ---
fac = Counter()
FACOPTS = ["Excellent", "Good", "Fair", "Poor", "Unsatis"]
for r in records:
    t = re.sub(r"\s+", " ", r.get("facilities", "")).strip()
    matched = next((f for f in FACOPTS if t.lower().startswith(f.lower())), None)
    fac[matched or ("(blank)" if not t else "UNPARSED:" + t[:40])] += 1
print("\n=== Facilities condition perception ===")
for k, c in fac.most_common():
    print(f"{k}: {c} ({100*c/N:.1f}%)")

# --- Boundary priorities (choose up to 2) ---
PRI = {
    "Transportation": "Transportation",
    "Minimize Impact": "Minimize Impact (move fewest students)",
    "Neighborhood Consider": "Neighborhood Considerations",
    "Natural Barriers": "Natural Barriers & Major Roads",
    "Other boundary": "Other boundary priority",
    "eeder": "Feeder patterns",  # ligature-safe
    "Demographic": "Demographics/Diversity",
    "Socioeconomic": "Socioeconomic balance",
    "Diversity": "Diversity",
    "Utilization": "Utilization",
    "Walk": "Walkability",
}
pri = Counter()
pri_blank = 0
for r in records:
    t = re.sub(r"\s+", " ", r.get("priorities", "")).strip()
    if not t:
        pri_blank += 1
        continue
    for pat, label in PRI.items():
        if pat.lower() in t.lower():
            pri[label] += 1
print(f"\n=== Boundary priorities (multi; blank={pri_blank}) ===")
for k, c in pri.most_common():
    print(f"{k}: {c} ({100*c/N:.1f}%)")

# --- Facility planning objectives ---
OBJ = ["Enhanced Educational Opportunities", "Consistent Facilities", "Building Condition",
       "Improved Utilization", "Safety", "Security", "Growth", "Other"]
obj = Counter()
for r in records:
    t = re.sub(r"\s+", " ", r.get("objectives", "")).strip()
    for o in OBJ:
        if o.lower() in t.lower():
            obj[o] += 1
    if not t:
        obj["(blank)"] += 1
print("\n=== Facility planning objectives (multi) ===")
for k, c in obj.most_common():
    print(f"{k}: {c} ({100*c/N:.1f}%)")

# --- Open-text keyword scan across concern/critical/additional fields ---
def opentext(r):
    return " ".join(r.get(k, "") for k in
                    ["critical_issue", "concern_es", "concern_ms", "concern_hs",
                     "additional", "pos_es", "pos_ms", "pos_hs", "email_q"]).lower()

KEYWORDS = {
    "diversity/diverse": r"divers",
    "segregat*": r"segregat",
    "socioeconomic/SES": r"socio.?econom|\bses\b",
    "poverty": r"poverty",
    "Title 1/Title I": r"title\s*[1i]",
    "equity/equitable": r"equit",
    "race/racial": r"\brace\b|racial",
    "free/reduced lunch": r"reduced lunch|ree.?/?.?reduced",
    "bus/transportation": r"\bbus\b|busses|buses|transport",
    "walk (walkability)": r"\bwalk",
    "neighborhood": r"neighborhood",
    "property value": r"property value|home value|real estate",
    "traffic": r"tra\s?ic|traffic",
    "IB program": r"\bib\b",
    "magnet": r"magnet",
    "grandfather*": r"grand\s?ather|grandfather",
    "split (city/county split)": r"split",
    "data (want data)": r"\bdata\b",
    "James River ES": r"james river",
    "Matthew Whaley ES": r"matthew whaley|\bmw\b",
    "Kings Mill": r"kings ?mill",
    "Norge": r"norge",
    "Stonehouse": r"stonehouse",
    "Laurel Lane": r"laurel lane",
    "Clara Byrd Baker": r"clara byrd|\bcbb\b",
    "D.J. Montague": r"montague",
    "J. Blaine Blayton": r"blayton",
    "Rawls Byrd": r"rawls",
    "Jamestown HS": r"jamestown",
    "Lafayette HS": r"la\s?ayette",
    "Warhill HS": r"warhill",
    "Berkeley MS": r"berkeley",
    "Toano MS": r"toano",
    "Hornsby MS": r"hornsby",
    "Lois Hornsby": r"lois",
}
kw = Counter()
for r in records:
    t = opentext(r)
    for label, pat in KEYWORDS.items():
        if re.search(pat, t):
            kw[label] += 1
print("\n=== Open-text keyword mentions (respondents mentioning ≥1x) ===")
for k, c in kw.most_common():
    print(f"{k}: {c} ({100*c/N:.1f}%)")

# --- Cross-tab: support_zones by parent vs staff vs community ---
def role_of(r):
    t = fixlig(r.get("relationship", ""))
    if "Parent/Guardian of Division Student" in t:
        return "Parent"
    if "Staff Member" in t:
        return "Staff"
    if "Community Member" in t:
        return "Community"
    return "Other/blank"

xt = {}
for r in records:
    t = re.sub(r"\s+", " ", r.get("support_zones", "")).strip().lower()
    matched = next((l for l in LIK if t.startswith(l.lower())), None)
    if matched is None and "neither" in t:
        matched = "Neither"
    xt.setdefault(role_of(r), Counter())[matched or "(blank)"] += 1
print("\n=== Support adjusting zones × primary role ===")
for role, ctr in xt.items():
    tot = sum(ctr.values())
    line = ", ".join(f"{k}: {ctr.get(k,0)}" for k in LIK)
    print(f"{role} (n={tot}): {line}")

# --- Emails requested contact ---
contact = sum(1 for r in records if len(r.get("email_q", "").strip()) > 5)
print(f"\nRespondents leaving contact/email text: {contact} ({100*contact/N:.1f}%)")
