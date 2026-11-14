"""NIH funding tracker for osteosarcoma (and neuroblastoma for comparison).

Pulls every NIH project from the RePORTER API whose title, terms or abstract
mention the disease, then sorts each one into a relevance tier:

  focused     - the disease is named in the project title
  substantial - the disease is named 3+ times in the abstract/public-health text
  incidental  - mentioned 1-2 times only (often the U2OS cell line, used
                throughout general cell biology)

Dollar totals avoid double counting multi-project grants: if any
subproject of an application matches, only the matching subprojects are
counted; otherwise the whole award is counted.

Usage: python3 tools/nih_funding_tracker.py [first_year] [last_year]
Writes data/nih_<disease>_projects.csv and prints a JSON summary.
"""
import csv, json, re, sys, time, urllib.request
from collections import defaultdict

API = "https://api.reporter.nih.gov/v2/projects/search"
DISEASES = {
    "osteosarcoma": r"osteosarcoma|osteogenic sarcoma",
    "neuroblastoma": r"neuroblastoma",
}


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


def tier(r, pat):
    if re.search(pat, r.get("project_title") or "", re.I):
        return "focused"
    text = (r.get("abstract_text") or "") + " " + (r.get("phr_text") or "")
    return "substantial" if len(re.findall(pat, text, re.I)) >= 3 else "incidental"


def main(y0, y1):
    summary = {}
    for disease, pat in DISEASES.items():
        recs = []
        for y in range(y0, y1 + 1):
            recs += fetch(disease, y)
        # de-duplicate parent awards against matching subprojects
        by_appl = defaultdict(list)
        for r in recs:
            by_appl[r["appl_id"]].append(r)
        kept = []
        for rs in by_appl.values():
            subs = [r for r in rs if r.get("subproject_id")]
            kept += subs if subs else rs[:1]
        out = f"data/nih_{disease}_projects.csv"
        with open(out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["fiscal_year", "tier", "award_amount", "activity_code", "institute",
                        "project_num", "subproject_id", "title", "organization", "pi", "url"])
            for r in sorted(kept, key=lambda r: (r["fiscal_year"], -(r.get("award_amount") or 0))):
                org = (r.get("organization") or {}).get("org_name", "")
                pis = "; ".join(p.get("full_name", "") for p in r.get("principal_investigators") or [])
                w.writerow([r["fiscal_year"], tier(r, pat), r.get("award_amount") or 0,
                            r.get("activity_code"), (r.get("agency_ic_admin") or {}).get("abbreviation"),
                            r.get("project_num"), r.get("subproject_id") or "",
                            r.get("project_title"), org, pis, r.get("project_detail_url")])
        agg = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        for r in kept:
            a = agg[r["fiscal_year"]][tier(r, pat)]
            a[0] += 1; a[1] += r.get("award_amount") or 0
        summary[disease] = {y: {t: v for t, v in d.items()} for y, d in sorted(agg.items())}
        print(f"{disease}: {len(kept)} project-years -> {out}", file=sys.stderr)
    print(json.dumps(summary))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 2015, int(a[1]) if len(a) > 1 else 2025)
