#!/usr/bin/env python3
"""Engine cycle 12: across the registry, how often can a teenager with osteosarcoma get into a drug trial?

Pre-registered in research_notes/Engine/cycle-12-teen-access/PREREGISTRATION.md (commit 56522b3).

  python3 tools/engine_cycle12_teen_access.py fetch   # search ClinicalTrials.gov; raw records to data/engine/cycle12/raw/ (not in git)
  python3 tools/engine_cycle12_teen_access.py         # classify and count

Outputs: data/engine/cycle12/set_a.csv, set_b.csv, hand_check_sample.csv, summary.json, docs/figures/engine12_ages.svg
"""
import csv
import json
import math
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "engine", "cycle12", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle12")
FIG = os.path.join(ROOT, "docs", "figures")
SEARCHES = {"A": "osteosarcoma", "B": "solid tumor"}
DRUG_TYPES = {"DRUG", "BIOLOGICAL", "GENETIC"}
EARLY = {"EARLY_PHASE1", "PHASE1", "PHASE2"}
RELAPSE = re.compile(r"relapse|relapsed|recurrent|recurrence|refractory|progressive|progression|metastatic|previously treated|prior therapy|advanced|unresectable", re.I)
SOLID = re.compile(r"solid tumou?r|solid neoplasm", re.I)


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
        json.dump({"searched": time.strftime("%Y-%m-%d"), "condition": cond, "studies": studies}, open(os.path.join(RAW, f"set_{key}.json"), "w"))
        print(key, cond, len(studies))


def age_years(s):
    m = re.match(r"(\d+)\s*(Year|Month|Week|Day)", s or "")
    return int(m.group(1)) / {"Year": 1, "Month": 12, "Week": 52, "Day": 365}[m.group(2)] if m else None


def record(s):
    p = s["protocolSection"]
    ident, status, design = p["identificationModule"], p["statusModule"], p.get("designModule", {})
    elig, cond = p.get("eligibilityModule", {}), p.get("conditionsModule", {})
    arms = p.get("armsInterventionsModule", {})
    sponsor = p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
    locs = p.get("contactsLocationsModule", {}).get("locations", [])
    countries = sorted({l.get("country", "") for l in locs if l.get("country")})
    lo, hi = age_years(elig.get("minimumAge")), age_years(elig.get("maximumAge"))
    teen = (lo is None or lo <= 17) and (hi is None or hi >= 12)
    text = " ".join([ident.get("briefTitle", ""), ident.get("officialTitle", ""), " ".join(cond.get("conditions", [])),
                     " ".join(cond.get("keywords", [])), elig.get("eligibilityCriteria", "")])
    return {"nct": ident["nctId"], "title": ident.get("briefTitle", ""), "status": status.get("overallStatus", ""),
            "phase": "/".join(design.get("phases", []) or ["NA"]), "phases": set(design.get("phases", []) or []),
            "intervention_types": sorted({i.get("type", "") for i in arms.get("interventions", [])}),
            "conditions": "; ".join(cond.get("conditions", [])), "min_age": elig.get("minimumAge", ""), "max_age": elig.get("maximumAge", ""),
            "min_years": lo, "accepts_teenagers": teen, "no_minimum_age": lo is None,
            "sponsor_class": "Industry" if sponsor.get("class") == "INDUSTRY" else "Academic or other",
            "lead_sponsor_class_raw": sponsor.get("class", ""),
            "us_site": "United States" in countries, "countries": "; ".join(countries),
            "names_osteosarcoma": "osteosarcoma" in text.lower(), "relapse_eligible": bool(RELAPSE.search(text)),
            "solid_condition": any(SOLID.search(c) for c in cond.get("conditions", []))}


def wilson(k, n):
    if n == 0:
        return (float("nan"),) * 3
    z, p = 1.96, k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return p, c - h, c + h


def share(rows, f):
    k = sum(1 for r in rows if f(r))
    p, lo, hi = wilson(k, len(rows))
    return {"k": k, "n": len(rows), "share": p, "lo": lo, "hi": hi}


def band(r):
    y = r["min_years"]
    if y is None:
        return "no minimum stated"
    return "under 12" if y < 12 else "12 to 17" if y <= 17 else "18" if y < 19 else "over 18"


def write(rows, path, cols):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: (", ".join(v) if isinstance(v, list) else v) for k, v in r.items()})


def bars_svg(bands_b, bands_a, path):
    order = ["under 12", "12 to 17", "no minimum stated", "18", "over 18"]
    W, left, rh = 820, 230, 26
    groups = [("Early-phase solid-tumour trials", bands_b), ("Trials naming osteosarcoma, relapse-eligible", bands_a)]
    H = 60 + sum(rh * len(order) + 34 for _ in groups) + 10
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="13" role="img" '
         f'aria-label="Minimum age to enter recruiting drug trials">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="26" font-weight="600" fill="#1d2430">Youngest age a recruiting drug trial accepts</text>',
         '<text x="16" y="44" fill="#525b6b" font-size="12">Share of trials in each age band. Blue: bands that let in a 12- to 17-year-old.</text>']
    y = 64
    for title, b in groups:
        n = sum(b.values())
        s.append(f'<text x="16" y="{y + 12}" font-weight="600" fill="#1d2430">{title} ({n} trials)</text>')
        y += 24
        for o in order:
            k = b.get(o, 0)
            w = (W - left - 110) * (k / n if n else 0)
            col = "#1c5cab" if o in ("under 12", "12 to 17", "no minimum stated") else "#6a7384"
            s.append(f'<text x="28" y="{y + 15}" fill="#1d2430">{o}</text>')
            s.append(f'<rect x="{left}" y="{y + 4}" width="{w:.1f}" height="15" fill="{col}"/>')
            s.append(f'<text x="{left + w + 6:.1f}" y="{y + 16}" fill="#525b6b" font-size="12">{k} ({100 * k / n:.0f}%)</text>' if n else "")
            y += rh
        y += 10
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    data = {k: json.load(open(os.path.join(RAW, f"set_{k}.json"))) for k in SEARCHES}
    A = [r for r in map(record, data["A"]["studies"]) if r["names_osteosarcoma"] and DRUG_TYPES & set(r["intervention_types"])]
    a_ids = {r["nct"] for r in A}
    B = [r for r in map(record, data["B"]["studies"])
         if r["solid_condition"] and DRUG_TYPES & set(r["intervention_types"]) and r["phases"] & EARLY and r["nct"] not in a_ids]
    Ar = [r for r in A if r["relapse_eligible"]]
    S = {"preregistration_commit": "56522b3", "searched": {k: data[k]["searched"] for k in data},
         "raw_records": {k: len(data[k]["studies"]) for k in data}, "set_A_all": len(A), "set_A_relapse_eligible": len(Ar), "set_B": len(B)}
    S["m1_A_relapse_teen"] = share(Ar, lambda r: r["accepts_teenagers"])
    S["m1_A_relapse_teen_US"] = share(Ar, lambda r: r["accepts_teenagers"] and r["us_site"])
    S["m1_A_relapse_US_any"] = share(Ar, lambda r: r["us_site"])
    S["m2_B_teen"] = share(B, lambda r: r["accepts_teenagers"])
    S["m2_B_teen_US"] = share(B, lambda r: r["accepts_teenagers"] and r["us_site"])
    S["m2_B_US_any"] = share(B, lambda r: r["us_site"])
    Bt = [r for r in B if r["accepts_teenagers"]]
    S["m3_industry_among_B_teen"] = share(Bt, lambda r: r["sponsor_class"] == "Industry")
    S["m3_industry_among_B_all"] = share(B, lambda r: r["sponsor_class"] == "Industry")
    S["m4_B_bands"] = {b: sum(band(r) == b for r in B) for b in ["under 12", "12 to 17", "no minimum stated", "18", "over 18"]}
    S["A_relapse_bands"] = {b: sum(band(r) == b for r in Ar) for b in ["under 12", "12 to 17", "no minimum stated", "18", "over 18"]}
    S["B_no_minimum_among_teen"] = sum(r["no_minimum_age"] for r in Bt)
    S["P35"] = "right" if S["m2_B_teen"]["share"] < 0.10 else "wrong"
    S["P36"] = "right" if S["m1_A_relapse_teen"]["share"] >= 0.5 else "wrong"
    S["P37"] = "right" if S["m3_industry_among_B_teen"]["share"] < S["m3_industry_among_B_all"]["share"] else "wrong"
    # descriptive extras
    S["A_all_teen"] = share(A, lambda r: r["accepts_teenagers"])
    S["B_industry_teen_US"] = share(B, lambda r: r["accepts_teenagers"] and r["us_site"] and r["sponsor_class"] == "Industry")
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
    cols = ["nct", "title", "status", "phase", "intervention_types", "conditions", "min_age", "max_age", "accepts_teenagers", "no_minimum_age",
            "sponsor_class", "us_site", "countries", "relapse_eligible"]
    write(sorted(A, key=lambda r: r["nct"]), os.path.join(OUT, "set_a.csv"), cols)
    write(sorted(B, key=lambda r: r["nct"]), os.path.join(OUT, "set_b.csv"), cols)
    sample = random.Random(12).sample(sorted(A, key=lambda r: r["nct"]), min(30, len(A)))
    write(sample, os.path.join(OUT, "hand_check_sample.csv"), ["nct", "title", "relapse_eligible", "conditions"])
    bars_svg(S["m4_B_bands"], S["A_relapse_bands"], os.path.join(FIG, "engine12_ages.svg"))
    print(json.dumps({k: v for k, v in S.items()}, indent=1, default=str))


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
