"""NIH funding tracker for osteosarcoma (and neuroblastoma for comparison).

Pulls every NIH project from the RePORTER API whose title, terms or abstract
mention the disease, then sorts each one into a relevance tier:

  focused     - the disease is named in the project title
  substantial - the disease is named 3+ times in the abstract/public-health text
  incidental  - mentioned 1-2 times only (often the U2OS cell line, used
                throughout general cell biology)

Search terms. Osteosarcoma is fetched twice, once for "osteosarcoma" and once
for "osteogenic sarcoma" (both words required). Records from the second search
are kept only if the phrase itself appears in the title, abstract or
public-health text, so grants that only carry the thesaurus term are not added.

De-duplication of multi-project grants. In RePORTER every subproject of a
P01/P50/U54/U2C etc. has its own appl_id and its own award amount, and the
parent award's amount already includes them. Records are therefore grouped by
(core project number, fiscal year, full project number). Within a group the
parent is the record with no subproject_id. If any subproject in the group was
returned by the search, only those subprojects are counted; otherwise the
parent is counted. The full project number is part of the key so that an
administrative supplement (e.g. "3P30CA021765-42S2"), which is a separate award
with its own number, is never dropped because a subproject of the main award
matched.

Topics. `topics()` classifies focused and substantial grants by title with the
regexes in TOPICS (one grant can fall in several topics). Run
`python3 tools/nih_funding_tracker.py --topics` to print the topic table from
the existing CSV without calling the API.

Usage:
  python3 tools/nih_funding_tracker.py [first_year] [last_year]   # fetch + write CSVs
  python3 tools/nih_funding_tracker.py --topics [first_year] [last_year]
Writes data/nih_<disease>_projects.csv and prints a JSON summary.
"""
import csv, json, re, sys, time, urllib.request
from collections import defaultdict

API = "https://api.reporter.nih.gov/v2/projects/search"
DISEASES = {
    # disease: (regex used for tiers, list of RePORTER search strings)
    "osteosarcoma": (r"osteosarcoma|osteogenic sarcoma", ["osteosarcoma", "osteogenic sarcoma"]),
    "neuroblastoma": (r"neuroblastoma", ["neuroblastoma"]),
}

# Title regexes for the topic table in reports/NIH funding for osteosarcoma.md.
# Applied case-insensitively to project titles of focused + substantial grants.
TOPICS = [
    ("Genomics and epigenetics",
     r"genom|epigen|methylat|chromatin|sequenc|transcriptom|copy number|mutation|landscape"),
    ("Drugs and targets",
     r"inhibit|target|therap|drug|treatment|agent|compound|antibod|small molecule|kinase|blockade|sensiti|resistan"),
    ("Dogs and comparative oncology", r"canine|\bdogs?\b|comparative oncology|veterinar|companion animal|\bpet\b|\bcop\b"),
    ("Immunotherapy and the immune system",
     r"immun|\bcar[- ]?t\b|\bcar\b|t[- ]cell|\bnk\b|natural killer|macrophage|vaccin|checkpoint|myeloid"),
    ("Metastasis and the lung", r"metasta|\blungs?\b|pulmonar|dissemin|coloniz|dormanc"),
    ("Germline and inherited risk",
     r"germline|inherit|predispos|heritab|susceptib|li[- ]fraumeni|familial|genetic modifier|cancer risk|\blfs\b|p53 mutant"),
    ("Laboratory models (PDX, 3D, mouse)",
     r"\bmodel|xenograft|\bpdx\b|organoid|\b3d\b|three[- ]dimensional|mouse|murine|zebrafish|bioprint"),
    ("Clinical trials and outcomes", r"\btrials?\b|outcome|survivor|late effect|quality of life"),
    ("ctDNA and liquid biopsy", r"ctdna|circulating tumou?r|liquid biops|cell[- ]free|cfdna"),
]


def fetch(term, year):
    rows, offset = [], 0
    while True:
        body = {"criteria": {"advanced_text_search": {"operator": "and",
                    "search_field": "projecttitle,terms,abstracttext", "search_text": term},
                    "fiscal_years": [year]},
                "limit": 500, "offset": offset}
        req = urllib.request.Request(API, json.dumps(body).encode(),
                                     {"Content-Type": "application/json"})
        for attempt in range(4):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=120)); break
            except Exception:
                time.sleep(3 * (attempt + 1))
        else:
            raise RuntimeError(f"RePORTER failed for {term} {year} offset {offset}")
        rows += d["results"]
        offset += 500
        if offset >= d["meta"]["total"] or offset > 14500:
            return rows
        time.sleep(1)


def text_of(r):
    return " ".join([r.get("project_title") or "", r.get("abstract_text") or "", r.get("phr_text") or ""])


def tier(r, pat):
    if re.search(pat, r.get("project_title") or "", re.I):
        return "focused"
    text = (r.get("abstract_text") or "") + " " + (r.get("phr_text") or "")
    return "substantial" if len(re.findall(pat, text, re.I)) >= 3 else "incidental"


def core_of(r):
    c = r.get("core_project_num")
    if c:
        return c
    m = re.match(r"^\d?([A-Z0-9]{3}[A-Z]{2}\d{6})", r.get("project_num") or "")
    return m.group(1) if m else r.get("project_num")


def dedupe(recs):
    """Group by (core project, fiscal year, project number): keep matching
    subprojects if any were returned, else the parent award."""
    groups = defaultdict(list)
    for r in recs:
        groups[(core_of(r), r["fiscal_year"], r.get("project_num"))].append(r)
    kept = []
    for rs in groups.values():
        subs = [r for r in rs if r.get("subproject_id")]
        if subs:
            kept += subs
        else:
            kept += rs  # distinct appl_ids without subprojects are separate records
    return kept


def topics(path, y0=2015, y1=2025):
    rows = [r for r in csv.DictReader(open(path))
            if r["tier"] in ("focused", "substantial") and y0 <= int(r["fiscal_year"]) <= y1]
    out = []
    for name, pat in TOPICS:
        hit = [r for r in rows if re.search(pat, r["title"], re.I)]
        out.append({"topic": name, "project_years": len(hit),
                    "funding": sum(int(r["award_amount"] or 0) for r in hit)})
    return out


def main(y0, y1):
    summary = {}
    for disease, (pat, terms) in DISEASES.items():
        by_appl = {}
        for y in range(y0, y1 + 1):
            for i, term in enumerate(terms):
                for r in fetch(term, y):
                    if i > 0 and not re.search(pat, text_of(r), re.I):
                        continue  # thesaurus-only hit from the secondary term
                    by_appl.setdefault(r["appl_id"], r)
        kept = dedupe(list(by_appl.values()))
        out = f"data/nih_{disease}_projects.csv"
        with open(out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["fiscal_year", "tier", "award_amount", "activity_code", "institute",
                        "project_num", "subproject_id", "title", "organization", "pi", "url",
                        "core_project_num", "appl_id"])
            for r in sorted(kept, key=lambda r: (r["fiscal_year"], -(r.get("award_amount") or 0))):
                org = (r.get("organization") or {}).get("org_name", "")
                pis = "; ".join(p.get("full_name", "") for p in r.get("principal_investigators") or [])
                w.writerow([r["fiscal_year"], tier(r, pat), r.get("award_amount") or 0,
                            r.get("activity_code"), (r.get("agency_ic_admin") or {}).get("abbreviation"),
                            r.get("project_num"), r.get("subproject_id") or "",
                            r.get("project_title"), org, pis, r.get("project_detail_url"),
                            core_of(r), r.get("appl_id")])
        agg = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        for r in kept:
            a = agg[r["fiscal_year"]][tier(r, pat)]
            a[0] += 1; a[1] += r.get("award_amount") or 0
        summary[disease] = {y: {t: v for t, v in d.items()} for y, d in sorted(agg.items())}
        print(f"{disease}: {len(by_appl)} records fetched, {len(kept)} kept -> {out}", file=sys.stderr)
    summary["osteosarcoma_topics"] = topics("data/nih_osteosarcoma_projects.csv", y0, y1)
    print(json.dumps(summary))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--topics":
        a = a[1:]
        y0 = int(a[0]) if a else 2015
        y1 = int(a[1]) if len(a) > 1 else 2025
        for t in topics("data/nih_osteosarcoma_projects.csv", y0, y1):
            print(f"{t['topic']}\t{t['project_years']}\t${t['funding']/1e6:.1f}M")
    else:
        main(int(a[0]) if a else 2015, int(a[1]) if len(a) > 1 else 2025)
