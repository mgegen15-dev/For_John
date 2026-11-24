#!/usr/bin/env python3
"""Engine cycle 4: which MTAP-selected drug trials could an osteosarcoma patient join?

Search and counting rules are pre-registered in research_notes/Engine/cycle-04-mtap-trials/PREREGISTRATION.md.

  python3 tools/engine_cycle04_mtap_trials.py fetch   search ClinicalTrials.gov, save raw records
  python3 tools/engine_cycle04_mtap_trials.py         build data/engine/cycle04/trials.csv for hand classification

The "open to osteosarcoma" column is filled by reading each record (see the report); this script
proposes a value from the text and never overrides data/engine/cycle04/classification.csv.
"""
import collections
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "engine", "cycle04", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle04")
TERMS = ["MTAP", "methylthioadenosine phosphorylase", "PRMT5", "MAT2A", "MRTX1719", "BMS-986504", "AMG 193", "TNG908", "TNG462",
         "TNG456", "AZD3470", "IDE397", "S095035", "PRT811", "PRT543", "GSK3326595", "JNJ-64619178", "PF-06939999", "AG-270",
         "SCR-6920", "SH3765", "BGB-58067", "ISM3412"]
ORG = (r"universit|hospital|cent(er|re)|institut|college|pharm|therap|bio|medicine|science|ltd|inc\\b|co\\.|llc|gmbh|"
       r"squibb|amgen|astrazeneca|bayer|gilead|janssen|servier|holdings|cancer|clinic|foundation|group|network|oncology|research|glaxo|pfizer|agios|prelude|mirati")
OPEN = {"RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION", "ACTIVE_NOT_RECRUITING"}


def fetch():
    os.makedirs(RAW, exist_ok=True)
    studies, hits = {}, {}
    for t in TERMS:
        token, n = None, 0
        while True:
            q = {"query.term": f'"{t}"', "pageSize": "200", "format": "json"}
            if token:
                q["pageToken"] = token
            d = json.load(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(q), timeout=120))
            for s in d.get("studies", []):
                nct = s["protocolSection"]["identificationModule"]["nctId"]
                studies[nct] = s
                hits.setdefault(nct, []).append(t)
                n += 1
            token = d.get("nextPageToken")
            if not token:
                break
        print(f"{t:36s} {n}")
        time.sleep(0.3)
    json.dump({"searched": time.strftime("%Y-%m-%d"), "terms": TERMS, "hits": hits, "studies": studies}, open(os.path.join(RAW, "search.json"), "w"))
    print("distinct trials:", len(studies))


def age_years(s):
    if not s:
        return None
    m = re.match(r"(\d+)\s*(Year|Month|Week|Day)", s)
    if not m:
        return None
    return int(m.group(1)) / {"Year": 1, "Month": 12, "Week": 52, "Day": 365}[m.group(2)]


def build():
    d = json.load(open(os.path.join(RAW, "search.json")))
    rows = []
    for nct, s in sorted(d["studies"].items()):
        p = s["protocolSection"]
        ident, status, design = p["identificationModule"], p["statusModule"], p.get("designModule", {})
        elig, cond = p.get("eligibilityModule", {}), p.get("conditionsModule", {})
        arms = p.get("armsInterventionsModule", {})
        drugs = sorted({i["name"] for i in arms.get("interventions", [])})
        text = " ".join([ident.get("briefTitle", ""), ident.get("officialTitle", ""), " ".join(cond.get("conditions", [])),
                         " ".join(cond.get("keywords", [])), elig.get("eligibilityCriteria", ""), " ".join(drugs),
                         p.get("descriptionModule", {}).get("briefSummary", "")])
        low = text.lower()
        mtap_sel = bool(re.search(r"mtap|methylthioadenosine phosphorylase|cdkn2a|9p21", low))
        class_drug = bool(re.search(r"prmt5|mat2a|mrtx1719|bms-986504|amg ?193|tng908|tng462|tng456|azd3470|ide397|s095035|prt811|prt543|"
                                    r"gsk3326595|jnj-64619178|pf-06939999|ag-270|scr-6920|sh3765|bgb-58067|ism3412", low))
        locs = p.get("contactsLocationsModule", {}).get("locations", [])
        countries = sorted({l.get("country", "") for l in locs if l.get("country")})
        lead = dict(p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}))
        if not re.search(ORG, lead.get("name", ""), re.I):          # an individual investigator: keep people's names out of public files
            lead["name"] = "Investigator-sponsored (individual)"
        if re.search(r"osteosarcoma|bone sarcoma|bone cancer|bone tumou?r", low):
            guess = "yes, named"
        elif re.search(r"solid tumou?rs?|solid malignanc|advanced cancer|advanced malignanc", low):
            guess = "check: solid tumours"
        else:
            guess = "check: restricted"
        rows.append({"nct": nct, "title": ident.get("briefTitle", ""), "status": status.get("overallStatus", ""),
                     "counts": status.get("overallStatus", "") in OPEN and design.get("studyType") != "OBSERVATIONAL" and (mtap_sel or class_drug),
                     "study_type": p.get("designModule", {}).get("studyType", ""), "phase": "/".join(design.get("phases", [])),
                     "min_age": elig.get("minimumAge", ""), "min_age_years": age_years(elig.get("minimumAge", "")),
                     "max_age": elig.get("maximumAge", ""), "sponsor": lead.get("name", ""), "sponsor_class": lead.get("class", ""),
                     "countries": "; ".join(countries), "us_site": "United States" in countries, "drugs": "; ".join(drugs),
                     "mentions_mtap_or_9p21": mtap_sel, "prmt5_or_mat2a_drug": class_drug, "conditions": "; ".join(cond.get("conditions", [])),
                     "auto_guess_osteosarcoma": guess, "matched_terms": "; ".join(d["hits"][nct])})
    with open(os.path.join(OUT, "trials.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    c = [r for r in rows if r["counts"]]
    print(len(rows), "trials found;", len(c), "meet the status and drug-or-selection rules")
    cpath = os.path.join(OUT, "classification.csv")
    if os.path.exists(cpath):                       # hand classification, read from each record
        cl = {r["nct"]: r for r in csv.DictReader(open(cpath))}
        tab = []
        for r in c:
            k = cl[r["nct"]]
            tab.append(dict(r, open_to_osteosarcoma=k["open_to_osteosarcoma"], mtap_required=k["mtap_or_9p21_loss_required"], note=k["note"]))
        yes = [t for t in tab if t["open_to_osteosarcoma"].startswith("yes")]
        A = [t for t in yes if t["status"] in ("RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION")]
        B = [t for t in A if t["min_age_years"] is not None and t["min_age_years"] < 18]
        Cc = [t for t in A if t["us_site"]]
        summary = {"searched": d["searched"], "trials_found": len(rows), "meeting_rules": len(c),
                   "not_relevant": [t["nct"] for t in tab if t["open_to_osteosarcoma"] == "not relevant"],
                   "open_to_osteosarcoma_any_status": len(yes), "A_recruiting_or_about_to": len(A),
                   "A_named": [t["nct"] for t in A if t["open_to_osteosarcoma"] == "yes, named"],
                   "A_requiring_mtap_loss": sum(t["mtap_required"] == "yes" for t in A),
                   "B_under_18": [(t["nct"], t["min_age"], t["countries"]) for t in B], "C_us_site": [t["nct"] for t in Cc],
                   "unclear": [t["nct"] for t in tab if t["open_to_osteosarcoma"] == "unclear"],
                   "closed_to_new_patients": [t["nct"] for t in yes if t["status"] == "ACTIVE_NOT_RECRUITING"],
                   "A_by_country": dict(collections.Counter(x for t in A for x in t["countries"].split("; ") if x))}
        json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
        with open(os.path.join(OUT, "trials_classified.csv"), "w", newline="") as f:
            cols = ["nct", "title", "status", "phase", "drugs", "sponsor", "sponsor_class", "min_age", "max_age", "countries", "us_site",
                    "open_to_osteosarcoma", "mtap_required", "note"]
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(sorted(tab, key=lambda t: (not t["open_to_osteosarcoma"].startswith("yes"), t["status"], t["nct"])))
        print(json.dumps(summary, indent=1))
        for t in A:
            print(f'  {t["nct"]} | {t["status"][:5]} | {t["phase"]:14s} | {t["min_age"]:9s} | US {str(t["us_site"]):5s} | {t["drugs"][:38]:38s} | {t["sponsor"][:28]}')
    print(collections.Counter(r["status"] for r in rows))
    print(collections.Counter(r["auto_guess_osteosarcoma"] for r in c))
    print("min ages among counted:", collections.Counter(r["min_age"] for r in c))


if __name__ == "__main__":
    fetch() if len(sys.argv) > 1 and sys.argv[1] == "fetch" else build()
