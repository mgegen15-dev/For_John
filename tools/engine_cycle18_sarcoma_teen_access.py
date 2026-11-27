#!/usr/bin/env python3
"""Engine cycle 18: do trials for Ewing sarcoma, rhabdomyosarcoma and other sarcomas take teenagers, and who leaves them out?

Pre-registered in research_notes/Engine/cycle-18-sarcoma-teen-access/PREREGISTRATION.md (commit ec7d1b6).

  python3 tools/engine_cycle18_sarcoma_teen_access.py fetch   # ClinicalTrials.gov; raw to data/engine/cycle18/raw/ (not in git)
  python3 tools/engine_cycle18_sarcoma_teen_access.py         # counts

Outputs: data/engine/cycle18/trials.csv, results.json
"""
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle12_teen_access as c12     # noqa: E402

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle18", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle18")
SEARCHES = {"ewing": "Ewing sarcoma", "rhabdo": "rhabdomyosarcoma", "sarcoma": "sarcoma"}


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for key, cond in SEARCHES.items():
        studies, token = [], None
        while True:
            q = {"query.cond": cond, "filter.overallStatus": "RECRUITING,NOT_YET_RECRUITING",
                 "filter.advanced": "AREA[StudyType]INTERVENTIONAL", "pageSize": "1000", "format": "json"}
            if token:
                q["pageToken"] = token
            d = json.load(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(q), timeout=180))
            studies += d.get("studies", [])
            token = d.get("nextPageToken")
            if not token:
                break
            time.sleep(0.3)
        json.dump({"searched": time.strftime("%Y-%m-%d"), "condition": cond, "studies": studies}, open(os.path.join(RAW, f"{key}.json"), "w"))
        print(key, len(studies))


def text_of(s):
    p = s["protocolSection"]
    ident, cond, elig = p["identificationModule"], p.get("conditionsModule", {}), p.get("eligibilityModule", {})
    return " ".join([ident.get("briefTitle", ""), ident.get("officialTitle", ""), " ".join(cond.get("conditions", [])),
                     " ".join(cond.get("keywords", [])), elig.get("eligibilityCriteria", "")]).lower(), cond.get("conditions", [])


def odds(rows):
    a = sum(r["accepts_teenagers"] for r in rows if r["sponsor_class"] == "Industry")
    b = sum(not r["accepts_teenagers"] for r in rows if r["sponsor_class"] == "Industry")
    c = sum(r["accepts_teenagers"] for r in rows if r["sponsor_class"] != "Industry")
    d = sum(not r["accepts_teenagers"] for r in rows if r["sponsor_class"] != "Industry")
    aa, bb, cc, dd = (a + .5, b + .5, c + .5, d + .5) if 0 in (a, b, c, d) else (a, b, c, d)
    o = aa * dd / (bb * cc)
    se = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    return {"industry": {"teen": a, "n": a + b}, "other": {"teen": c, "n": c + d}, "odds_ratio": o,
            "lo": math.exp(math.log(o) - 1.96 * se), "hi": math.exp(math.log(o) + 1.96 * se),
            "fisher_p": float(stats.fisher_exact([[a, b], [c, d]])[1])}


def verdict(m):
    if m["odds_ratio"] < 1 and m["hi"] < 1:
        return "Supported"
    if m["lo"] > 0.67:
        return "Refuted"
    return "Inconclusive"


def main():
    os.makedirs(OUT, exist_ok=True)
    sets = {}
    for key in SEARCHES:
        d = json.load(open(os.path.join(RAW, f"{key}.json")))
        keep = []
        for s in d["studies"]:
            r = c12.record(s)
            if not (c12.DRUG_TYPES & set(r["intervention_types"])):
                continue
            txt, conds = text_of(s)
            if key == "ewing" and "ewing" not in txt:
                continue
            if key == "rhabdo" and "rhabdomyosarcoma" not in txt:
                continue
            if key == "sarcoma":
                if not any("sarcoma" in c.lower() for c in conds):
                    continue
                if any(w in txt for w in ("osteosarcoma", "ewing", "rhabdomyosarcoma", "kaposi")):
                    continue
            keep.append(r)
        sets[key] = keep
    S = {"preregistration_commit": "ec7d1b6", "sets": {}}
    for key, rows in sets.items():
        k = sum(r["accepts_teenagers"] for r in rows)
        p, lo, hi = c12.wilson(k, len(rows))
        teen = [r for r in rows if r["accepts_teenagers"]]
        S["sets"][key] = {"n": len(rows), "teen": k, "share": p, "lo": lo, "hi": hi,
                          "teen_with_us_site": sum(r["us_site"] for r in teen),
                          "industry_share": sum(r["sponsor_class"] == "Industry" for r in rows) / len(rows) if rows else float("nan"),
                          "odds_industry_vs_other": odds(rows)}
    combined = {r["nct"]: r for rows in sets.values() for r in rows}
    S["combined_n"] = len(combined)
    S["H1"] = odds(list(combined.values()))
    S["verdict_H1"] = verdict(S["H1"])
    S["P49"] = "right" if S["sets"]["ewing"]["share"] >= 0.6 else "wrong"
    S["P50"] = "right" if S["sets"]["sarcoma"]["share"] < 0.4 else "wrong"
    S["P51"] = "right" if S["verdict_H1"] == "Supported" else "wrong"
    json.dump(S, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    rows = []
    for key, rs in sets.items():
        for r in rs:
            rows.append(dict(r, set=key))
    cols = ["set", "nct", "title", "status", "phase", "conditions", "min_age", "max_age", "accepts_teenagers", "sponsor_class", "us_site", "countries"]
    c12.write(sorted(rows, key=lambda r: (r["set"], r["nct"])), os.path.join(OUT, "trials.csv"), cols)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
