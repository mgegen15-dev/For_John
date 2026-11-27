#!/usr/bin/env python3
"""Engine cycle 17: before and after the FDA's 2019 adolescent guidance, across trials of every status.

Pre-registered in research_notes/Engine/cycle-17-fda-guidance-all-trials/PREREGISTRATION.md (commit c2841de).

  python3 tools/engine_cycle17_fda_all_trials.py fetch   # ClinicalTrials.gov; raw to data/engine/cycle17/raw/ (not in git)
  python3 tools/engine_cycle17_fda_all_trials.py         # counts

Outputs: data/engine/cycle17/trials.csv, results.json, by_year.csv, docs/figures/engine17_years.svg
"""
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle12_teen_access as c12     # noqa: E402
import engine_cycle16_fda_guidance as c16    # noqa: E402

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle17", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle17")
FIG = os.path.join(ROOT, "docs", "figures")
PERIODS = {"before": ("2014-01-01", "2018-12-31"), "after": ("2020-01-01", "2024-12-31")}


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for key, (a, b) in PERIODS.items():
        studies, token = [], None
        while True:
            q = {"query.cond": "solid tumor", "filter.advanced": f"AREA[StudyType]INTERVENTIONAL AND AREA[StartDate]RANGE[{a},{b}]",
                 "pageSize": "1000", "format": "json"}
            if token:
                q["pageToken"] = token
            d = json.load(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(q), timeout=180))
            studies += d.get("studies", [])
            token = d.get("nextPageToken")
            if not token:
                break
            time.sleep(0.3)
        json.dump({"searched": time.strftime("%Y-%m-%d"), "period": [a, b], "studies": studies}, open(os.path.join(RAW, f"{key}.json"), "w"))
        print(key, len(studies))


def main():
    os.makedirs(OUT, exist_ok=True)
    rows, raw_n, withdrawn = [], {}, 0
    for key in PERIODS:
        d = json.load(open(os.path.join(RAW, f"{key}.json")))
        raw_n[key] = len(d["studies"])
        for s in d["studies"]:
            if s["protocolSection"]["statusModule"].get("overallStatus") == "WITHDRAWN":
                withdrawn += 1
                continue
            r = c12.record(s)
            if not (r["solid_condition"] and c12.DRUG_TYPES & set(r["intervention_types"]) and r["phases"] & c12.EARLY):
                continue
            sd = s["protocolSection"]["statusModule"].get("startDateStruct", {}).get("date", "")
            r["year"] = int(sd[:4])
            r["period"] = key
            rows.append(r)
    S = {"preregistration_commit": "c2841de", "raw_records": raw_n, "withdrawn_excluded": withdrawn, "trials": len(rows)}
    S["H1"] = c16.compare(rows)
    S["verdict_H1"] = c16.verdict(S["H1"])
    S["industry"] = c16.compare([r for r in rows if r["sponsor_class"] == "Industry"])
    S["academic_or_other"] = c16.compare([r for r in rows if r["sponsor_class"] != "Industry"])
    S["adult_type"] = c16.compare([r for r in rows if r["min_years"] is None or r["min_years"] >= 12])
    S["adult_type_industry"] = c16.compare([r for r in rows if (r["min_years"] is None or r["min_years"] >= 12) and r["sponsor_class"] == "Industry"])
    S["P47"] = "right" if S["verdict_H1"] == "Supported" else "wrong"
    S["P48"] = "right" if S["industry"]["after"]["share"] < 0.05 else "wrong"
    by = {}
    for r in rows:
        b = by.setdefault(r["year"], {"teen": 0, "n": 0, "teen_industry": 0, "n_industry": 0})
        b["teen"] += r["accepts_teenagers"]
        b["n"] += 1
        if r["sponsor_class"] == "Industry":
            b["teen_industry"] += r["accepts_teenagers"]
            b["n_industry"] += 1
    for v in by.values():
        v["share"] = v["teen"] / v["n"]
    S["by_year"] = {str(k): v for k, v in sorted(by.items())}
    json.dump(S, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    cols = ["nct", "title", "status", "phase", "year", "period", "min_age", "max_age", "accepts_teenagers", "sponsor_class", "us_site"]
    c12.write(sorted(rows, key=lambda r: r["nct"]), os.path.join(OUT, "trials.csv"), cols)
    with open(os.path.join(OUT, "by_year.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start_year", "trials", "accept_teenagers", "share", "company_led", "company_led_accepting"])
        for y, v in sorted(by.items()):
            w.writerow([y, v["n"], v["teen"], f'{v["share"]:.3f}', v["n_industry"], v["teen_industry"]])
    c16.bars(by, os.path.join(FIG, "engine17_years.svg"),
             subtitle="Early-phase &quot;solid tumour&quot; drug trials of every status, by start year (2019 left out). Dashed line: FDA guidance, March 2019.",
             guidance_after_year=2018)
    print(json.dumps({k: v for k, v in S.items() if k != "by_year"}, indent=1))
    print("by year:", {k: (v["teen"], v["n"]) for k, v in S["by_year"].items()})


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
