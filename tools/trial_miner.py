"""Pull every ClinicalTrials.gov study that lists osteosarcoma as a condition
and flatten it into one row per trial (data/osteosarcoma_trials.csv).

Each row records design, status, stop reason, interventions, primary
endpoints, ages, sponsor, countries, and whether results were posted.
Scope tag (see `scope_for`):
  os_only      every listed condition names osteosarcoma / osteogenic sarcoma,
               or is a generic bone-sarcoma term or a bare metastasis-site
               descriptor (e.g. "Lung Metastases"), AND at least one condition
               names osteosarcoma explicitly.
  bone_sarcoma every condition is a generic bone-sarcoma term (or a bare
               metastasis-site descriptor) but none names osteosarcoma
               (e.g. "Bone Sarcoma" alone).
  basket       anything else: osteosarcoma is one of several cancers, or a
               condition names another histology or organ cancer.
Words such as "recurrent", "refractory", "metastatic", "lung" or "neoplasm"
no longer qualify a condition on their own (they did before 2026-11-14,
which let Ewing, rhabdomyosarcoma and lung-cancer trials into os_only).
To re-tag an existing CSV without downloading: python3 tools/retag_trial_scope.py

Usage: python3 tools/trial_miner.py
"""
import csv, json, re, time, urllib.parse, urllib.request

API = "https://clinicaltrials.gov/api/v2/studies"
# A condition that names osteosarcoma itself.
OS_PAT = re.compile(r"osteosarcoma|osteogenic sarcoma|sarcoma,\s*osteogenic", re.I)
# Generic bone-sarcoma / bone-tumour terms that name no other histology.
BONE_SYN = re.compile(r"^(?:(?:primary|malignant|high[- ]grade|unresectable|metastatic|recurrent|"
                      r"refractory|relapsed|advanced|childhood|adult)\s+)*"
                      r"(?:bone (?:sarcomas?|cancer(?: tumou?r| surgery)?|tumou?rs?|neoplasms?)|"
                      r"(?:sarcoma|neoplasms?|malignant neoplasms?) of (?:the )?bone(?: and articular cartilage.*)?|"
                      r"sarcoma,\s*bone)$", re.I)
# A condition that also names another cancer type is never osteosarcoma-only,
# even when it mentions osteosarcoma (e.g. "Osteosarcoma, Chondrosarcoma").
OTHER_HIST = re.compile(r"ewing|chondrosarcoma|rhabdo|neuroblastoma|solid (tumou?r|malignan)|carcinoma|"
                        r"glioma|soft[- ]tissue|lymphoma|leuk|melanoma|wilms|germ cell|medulloblastoma", re.I)
# Bone metastases from other cancers are not bone sarcoma.
NOT_BONE = re.compile(r"bone metasta|secondary bone|metastatic bone disease|bone cancer metastatic", re.I)
# Bare metastasis-site descriptors with no histology or organ cancer named.
SITE_WORDS = {"metastasis", "metastases", "metastatic", "lung", "lungs", "pulmonary", "malignant",
              "neoplasm", "neoplasms", "in", "the", "to", "disease"}


def _is_site_descriptor(c):
    w = re.findall(r"[a-z]+", c.lower())
    return bool(w) and any(x.startswith("metasta") for x in w) and all(x in SITE_WORDS for x in w)


def _is_bone_syn(c):
    c = c.strip()
    return bool(BONE_SYN.match(c)) and not NOT_BONE.search(c)


def scope_for(conds):
    """Return 'os_only', 'bone_sarcoma' or 'basket' for a list of condition strings."""
    conds = [c.strip() for c in conds if c and c.strip()]
    if not conds:
        return "basket"
    named_os = any(OS_PAT.search(c) for c in conds)
    ok = all((OS_PAT.search(c) or _is_bone_syn(c) or _is_site_descriptor(c)) and not OTHER_HIST.search(c)
             for c in conds)
    if ok and named_os:
        return "os_only"
    if ok and any(_is_bone_syn(c) for c in conds):
        return "bone_sarcoma"
    return "basket"


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
    inter = g(p, "armsInterventionsModule", "interventions", default=[])
    prim = g(p, "outcomesModule", "primaryOutcomes", default=[])
    locs = g(p, "contactsLocationsModule", "locations", default=[])
    st = p["statusModule"]
    return {
        "nct_id": p["identificationModule"]["nctId"],
        "title": p["identificationModule"].get("briefTitle", ""),
        "scope": scope_for(conds),
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
