#!/usr/bin/env python3
"""Re-extract the survey PDF with the f-glyphs recovered.

The PDF's embedded Aptos subset has a broken ToUnicode table: the glyphs for
f / ff / fi / fl are present in the page content but map to junk codepoints, so
every extractor (pdftotext, PyMuPDF, pdfplumber) drops them the same way. The
mapping below was derived by scanning every 7th page of the document and
inspecting every non-ASCII / control codepoint in context; these four are the
only defective ones. Everything else non-ASCII is legitimate typography.

Output: survey_clean.txt
"""
import unicodedata

import fitz  # PyMuPDF

PDF = "Redacted-Redistricting-Survey-Raw-Results-Final-June-2026.pdf"
OUT = "survey_clean.txt"

GLYPH_FIX = {
    "\x1f": "f",       # 3,077 occurrences in the sample
    "Ư": "ff",    # 413  -- capital U+01AF standing in for the ff ligature
    "ﬁ": "fi",    # 981
    "ﬂ": "fl",    # 8
}


def repair(text: str) -> str:
    for bad, good in GLYPH_FIX.items():
        text = text.replace(bad, good)
    # NFKC would also fold the fi/fl ligatures, but we handle those explicitly
    # above so the mapping stays auditable. Normalize the rest (curly quotes and
    # dashes are left alone -- they are real).
    return unicodedata.normalize("NFC", text)


def main() -> None:
    doc = fitz.open(PDF)
    pages = [repair(doc[i].get_text()) for i in range(doc.page_count)]
    text = "\n".join(pages)
    with open(OUT, "w") as fh:
        fh.write(text)

    leftover = sorted({c for c in text if ord(c) < 32 and c not in "\n\t\r"})
    print(f"pages: {doc.page_count}")
    print(f"chars: {len(text):,}")
    print(f"records (>> Recorded Date << markers): {text.count('>> Recorded Date <<')}")
    print(f"unmapped control codepoints remaining: {[hex(ord(c)) for c in leftover]}")


if __name__ == "__main__":
    main()
