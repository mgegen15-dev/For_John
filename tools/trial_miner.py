"""Pull every ClinicalTrials.gov study that lists osteosarcoma as a condition
and flatten it into one row per trial (data/osteosarcoma_trials.csv).

Each row records design, status, stop reason, interventions, primary
endpoints, ages, sponsor, countries, and whether results were posted.
A trial is tagged `os_only` when every listed condition is osteosarcoma or
a synonym, and `basket` when osteosarcoma is one of several cancers.

Usage: python3 tools/trial_miner.py
"""
import csv, json, re, time, urllib.parse, urllib.request

API = "https://clinicaltrials.gov/api/v2/studies"
OS_PAT = re.compile(r"osteosarcoma|osteogenic sarcoma", re.I)
BONE_OK = re.compile(r"osteosarcoma|osteogenic|bone (sarcoma|cancer|tumou?r)|metasta|recurren|"
                     r"refractory|lung|pulmonary|sarcoma, osteogenic|neoplasm", re.I)


def pages():
    token = None
    while True:
        q = {"query.cond": "osteosarcoma", "pageSize": 1000, "format": "json"}
        if token:
            q["pageToken"] = token
        d = json.load(urllib.request.urlopen(API + "?" + urllib.parse.urlencode(q), timeout=120))
        yield from d["studies"]
        token = d.get("nextPageToken")
        if not token:
            return
        time.sleep(1)


def g(d, *keys, default=""):
    for k in keys:
        d = d.get(k, {}) if isinstance(d, dict) else {}
    return d if d != {} else default


def row(s):
    p = s["protocolSection"]
    conds = g(p, "conditionsModule", "conditions", default=[])
    other = [c for c in conds if not OS_PAT.search(c) and not BONE_OK.search(c)]
    inter = g(p, "armsInterventionsModule", "interventions", default=[])
    prim = g(p, "outcomesModule", "primaryOutcomes", default=[])
    locs = g(p, "contactsLocationsModule", "locations", default=[])
    st = p["statusModule"]
    return {
        "nct_id": p["identificationModule"]["nctId"],
        "title": p["identificationModule"].get("briefTitle", ""),
        "scope": "os_only" if not other else "basket",
        "study_type": g(p, "designModule", "studyType"),
        "phase": "/".join(g(p, "designModule", "phases", default=[])) or "NA",
        "allocation": g(p, "designModule", "designInfo", "allocation"),
        "enrollment": g(p, "designModule", "enrollmentInfo", "count"),
        "enrollment_type": g(p, "designModule", "enrollmentInfo", "type"),
        "status": st.get("overallStatus", ""),
        "why_stopped": st.get("whyStopped", ""),
        "start": g(st, "startDateStruct", "date"),
        "completion": g(st, "completionDateStruct", "date"),
        "last_update": g(st, "lastUpdatePostDateStruct", "date"),
        "has_results": s.get("hasResults", False),
        "sponsor": g(p, "sponsorCollaboratorsModule", "leadSponsor", "name"),
        "sponsor_class": g(p, "sponsorCollaboratorsModule", "leadSponsor", "class"),
        "interventions": " | ".join(f"{i.get('type','')}: {i.get('name','')}" for i in inter),
        "primary_outcomes": " | ".join(f"{o.get('measure','')} [{o.get('timeFrame','')}]" for o in prim),
        "min_age": g(p, "eligibilityModule", "minimumAge"),
        "max_age": g(p, "eligibilityModule", "maximumAge"),
        "countries": "; ".join(sorted({l.get("country", "") for l in locs if l.get("country")})),
        "conditions": "; ".join(conds),
    }


def main():
    rows = [row(s) for s in pages()]
    with open("data/osteosarcoma_trials.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["nct_id"]))
    print(f"{len(rows)} trials -> data/osteosarcoma_trials.csv")


if __name__ == "__main__":
    main()
