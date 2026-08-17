#!/usr/bin/env python3
"""Build the public comment corpus from records_clean.json.

Publishes only the fields that are safe and non-duplicative:

  EXCLUDED  email_q          108 non-blank, but this is the field that solicited
                             contact info; the redaction leaves visible gaps
                             ("we are planning to move from .") that are
                             location-identifying. Editorial call -- flip
                             INCLUDE_EMAIL_Q to publish it.
  EXCLUDED  employee_where   1 non-blank, and it names an individual staff
                             member's school.
  EXCLUDED  relationship_other / priorities_other
                             byte-for-byte identical to their parent field in
                             1540/1540 records -- an export artifact, not data.

The export repeats a single answer across question groups: the Elementary /
Middle / High answers are identical in 1539/1540 records, and the "does well" and
"wish for the Division" answers are identical in 1015/1018. Each group therefore
collapses to one field; where the copies genuinely differ (three records, where
the redaction clipped different spans), all distinct values are kept.

Outputs: site/comments.json (explorer payload), site/comments.csv (download).
"""
import csv
import json
import re
from datetime import datetime

INCLUDE_EMAIL_Q = False

SRC = "records_clean.json"
OUT_JSON = "site/comments.json"
OUT_CSV = "site/comments.csv"

TEXT_FIELDS = [
    ("opinion", "What the Division does well, and what should improve"),
    ("critical", "Most critical issue for the boundary scenarios"),
    ("positive", "One positive outcome of the scenario presented"),
    ("concern", "Biggest concern about the scenario presented"),
    ("additional", "Additional thoughts / questions for the Division"),
]

SUPPORT = ["Strongly agree", "Somewhat agree", "Somewhat disagree", "Strongly disagree"]
FACILITIES = ["Excellent", "Good", "Fair", "Poor", "Unsatisfactory"]

# Multi-select fields comma-join their options, and option labels contain commas
# of their own ("Minimize time on bus, logical safe stops..."), so split only on
# a comma that begins a new option (i.e. followed by a capital).
SPLIT_OPTS = re.compile(r",(?=[A-Z])")


def opts(value: str) -> list:
    return [p.strip() for p in SPLIT_OPTS.split(value) if p.strip()]


def short(label: str) -> str:
    """Trim an option label to its name, dropping the explanatory tail."""
    return re.split(r"\s*[-–]\s", label, maxsplit=1)[0].strip().rstrip("-–").strip()


def iso(stamp: str) -> str:
    for fmt in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(stamp, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def main() -> None:
    records = json.load(open(SRC))

    vocab = {"role": [], "school": [], "priority": [], "objective": []}

    def idx(kind: str, label: str) -> int:
        if label not in vocab[kind]:
            vocab[kind].append(label)
        return vocab[kind].index(label)

    rows = []
    for n, rec in enumerate(records, start=1):
        text = {}
        for key, src in [
            ("opinion", ["proud", "wish"]),
            ("critical", ["critical_issue"]),
            ("positive", ["pos_es", "pos_ms", "pos_hs"]),
            ("concern", ["concern_es", "concern_ms", "concern_hs"]),
            ("additional", ["additional"]),
        ]:
            seen, vals = set(), []
            for f in src:
                v = rec[f].strip()
                if v and v not in seen:
                    seen.add(v)
                    vals.append(v)
            if vals:
                text[key] = " / ".join(vals)
        if INCLUDE_EMAIL_Q and rec["email_q"].strip():
            text["email_q"] = rec["email_q"].strip()

        row = {
            "id": f"r{n:04d}",
            "d": iso(rec["date"]),
            "r": [idx("role", o) for o in opts(rec["relationship"])],
            "s": [idx("school", o) for o in opts(rec["school"])],
            "z": SUPPORT.index(rec["support_zones"]) if rec["support_zones"] in SUPPORT else -1,
            "f": FACILITIES.index(rec["facilities"]) if rec["facilities"] in FACILITIES else -1,
            "p": sorted({idx("priority", short(o)) for o in opts(rec["priorities"])}),
            "o": sorted({idx("objective", short(o)) for o in opts(rec["objectives"])}),
            "t": text,
        }
        rows.append(row)

    payload = {
        "meta": {
            "n": len(rows),
            "source": "Redacted Redistricting Survey Raw Results, WJCC Schools, June 2026",
            "window": "2026-05-13 to 2026-06-08",
            "excluded_fields": ["email_q", "employee_where", "relationship_other", "priorities_other"],
            "note": "The export repeats one answer across question groups "
                    "(Elementary/Middle/High identical in 1539/1540 records; "
                    "does-well/wish identical in 1015/1018). Each group is collapsed.",
        },
        "vocab": vocab,
        "support": SUPPORT,
        "facilities": FACILITIES,
        "fields": [{"key": k, "label": l} for k, l in TEXT_FIELDS],
        "rows": rows,
    }

    import os
    os.makedirs("site", exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"), ensure_ascii=False)

    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "date", "roles", "schools", "support", "facilities",
                    "priorities", "objectives"] + [k for k, _ in TEXT_FIELDS])
        for row in rows:
            w.writerow([
                row["id"], row["d"],
                "; ".join(vocab["role"][i] for i in row["r"]),
                "; ".join(vocab["school"][i] for i in row["s"]),
                SUPPORT[row["z"]] if row["z"] >= 0 else "",
                FACILITIES[row["f"]] if row["f"] >= 0 else "",
                "; ".join(vocab["priority"][i] for i in row["p"]),
                "; ".join(vocab["objective"][i] for i in row["o"]),
            ] + [row["t"].get(k, "") for k, _ in TEXT_FIELDS])

    size = os.path.getsize(OUT_JSON)
    with_text = sum(1 for r in rows if r["t"])
    chars = sum(len(v) for r in rows for v in r["t"].values())
    print(f"rows: {len(rows)}  ({with_text} have at least one comment)")
    print(f"comment text: {chars:,} chars")
    print(f"{OUT_JSON}: {size/1024:.0f} KB")
    for kind, items in vocab.items():
        print(f"  {kind}: {len(items)} -> {items[:4]}{'...' if len(items) > 4 else ''}")


if __name__ == "__main__":
    main()
