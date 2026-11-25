#!/usr/bin/env python3
"""Engine cycle 7: CCNE1 amplification in relapsed osteosarcoma, and the trials those patients could join.

Pre-registered in research_notes/Engine/cycle-07-ccne1-relapse-trials/PREREGISTRATION.md. Part A reuses the
cohorts and method of cycle 3 (tools/engine_cycle03_9p21.py); Part B reuses the counting rules of cycle 4.

  python3 tools/engine_cycle07_ccne1.py fetch    amplification calls from cBioPortal, trial records from ClinicalTrials.gov
  python3 tools/engine_cycle07_ccne1.py          analyse

Outputs: data/engine/cycle07/ (results.csv, summary.json (patient-level table written to raw/, not published), trials.csv, trials_classified.csv), docs/figures/engine07_ccne1.svg
"""
import collections
import csv
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle03_9p21 as c3                 # noqa: E402  cohort loading, one-sample-per-patient rule, pooling
import engine_cycle04_mtap_trials as c4          # noqa: E402  age parsing and the organisation-name rule

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle07", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle07")
FIG = os.path.join(ROOT, "docs", "figures")
GENE, ENTREZ = "CCNE1", 898
TERMS = ["PKMYT1", "MYT1", "lunresertib", "RP-6306", "CCNE1", "cyclin E1", "BLU-222", "INX-315", "PF-07104091", "tagtociclib",
         "AZD8421", "INCB123667", "BG-68501", "ARTS-021", "NKT3964", "NKT3447", "ECI830", "AVZO-021", "azenosertib", "ZN-c3",
         "Debio 0123", "ACR-2316", "SGR-3515", "APR-1051"]
OPEN = {"RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION", "ACTIVE_NOT_RECRUITING"}
Z95 = c3.Z95


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for sid in c3.ALL_STUDIES:
        out = os.path.join(RAW, f"{sid}_amp.json")
        if os.path.exists(out):
            continue
        d = json.load(open(os.path.join(c3.RAW, f"{sid}.json")))
        amp = c3.api(f"/molecular-profiles/{d['cna_profile']}/discrete-copy-number/fetch?discreteCopyNumberEventType=AMP&projection=DETAILED",
                     {"sampleIds": d["samples"]})
        rep = c3.api(f"/molecular-profiles/{d['cna_profile']}/molecular-data/fetch?projection=SUMMARY",
                     {"sampleIds": d["samples"], "entrezGeneIds": [ENTREZ]})
        json.dump({"amp": [{"sampleId": e["sampleId"], "gene": e["gene"]["hugoGeneSymbol"]} for e in amp], "ccne1_reported": bool(rep)}, open(out, "w"))
        print(sid, len(amp), "amplification calls; CCNE1 reported:", bool(rep))
    out = os.path.join(RAW, "search.json")
    if not os.path.exists(out):
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
            print(f"{t:16s} {n}")
            time.sleep(0.3)
        json.dump({"searched": time.strftime("%Y-%m-%d"), "terms": TERMS, "hits": hits, "studies": studies}, open(out, "w"))
        print("distinct trials:", len(studies))


# ------------------------------------------------------------------ Part A
def load(sid):
    d, samples = c3.load(sid)
    a = json.load(open(os.path.join(RAW, f"{sid}_amp.json")))
    amps = collections.defaultdict(set)
    for e in a["amp"]:
        amps[e["sampleId"]].add(e["gene"])
    for s in samples:
        s["amps"] = amps.get(s["sample"], set())
        s["ccne1_covered"] = a["ccne1_reported"] and (s["genes_on_panel"] is None or GENE in s["genes_on_panel"])
    return samples


def table(units, gene, sel=lambda u: True):
    us = [u for u in units if sel(u) and (u["genes_on_panel"] is None or gene in u["genes_on_panel"])]
    a = sum(gene in u["amps"] for u in us if u["group"] == "R")
    b = sum(u["group"] == "R" for u in us) - a
    c = sum(gene in u["amps"] for u in us if u["group"] == "P")
    d = sum(u["group"] == "P" for u in us) - c
    return a, b, c, d


def part_a():
    S = {"studies": {}, "checks": {}}
    units, paired, everysample = {}, {}, {}
    for sid in c3.TEST_STUDIES:
        samples = [s for s in load(sid) if s["ccne1_covered"]]
        everysample[sid] = [s for s in samples if s["group"]]
        units[sid], paired[sid] = c3.one_per_patient(samples)
        S["studies"][sid] = {"patients": len(units[sid]), "group_R": sum(u["group"] == "R" for u in units[sid]),
                             "group_P": sum(u["group"] == "P" for u in units[sid])}

    def compare(gene, src=units, sel=lambda u: True):
        tabs = {sid: table(src[sid], gene, sel) for sid in c3.TEST_STUDIES}
        per = {sid: c3.log_or(*t) for sid, t in tabs.items()}
        tot = [sum(t[i] for t in tabs.values()) for i in range(4)]
        return {"tables": tabs, "per_study": {k: ({"or": math.exp(v["b"]), "lo": math.exp(v["b"] - Z95 * v["se"]), "hi": math.exp(v["b"] + Z95 * v["se"])} if v else None)
                                              for k, v in per.items()},
                "pooled": c3.pool(per.values()), "R": c3.wilson(tot[0], tot[0] + tot[1]) + (tot[0], tot[0] + tot[1]),
                "P": c3.wilson(tot[2], tot[2] + tot[3]) + (tot[2], tot[2] + tot[3])}
    prim = compare(GENE)
    S["primary"] = prim
    S["verdict"] = c3.verdict(prim["pooled"])
    S["underpowered"] = min(prim["R"][4], prim["P"][4]) < 100
    S["secondary"] = {"every_sample": compare(GENE, everysample),
                      "distant_metastasis_only": compare(GENE, sel=lambda u: u["group"] == "P" or u["type"] in ("metastasis", "metastatic"))}
    # purity
    pur = {}
    for sid in c3.TEST_STUDIES:
        us = [u for u in units[sid] if u["purity"] is not None]
        y = np.array([float(GENE in u["amps"]) for u in us])
        X = np.column_stack([[float(u["group"] == "R") for u in us], [u["purity"] / 10 for u in us]])
        if y.sum() >= 3:
            beta, se = c3.logistic(y, X)
            pur[sid] = {"b": float(beta[1]), "se": float(se[1])}
    S["checks"]["purity_adjusted"] = c3.pool(pur.values())
    # every gene amplified in more than 3%
    genes = set().union(*[u["amps"] for sid in c3.TEST_STUDIES for u in units[sid]])
    rows = []
    for g in sorted(genes):
        r = compare(g)
        k, n = r["R"][3] + r["P"][3], r["R"][4] + r["P"][4]
        if n and k / n > 0.03 and r["pooled"]:
            rows.append({"gene": g, "rate": k / n, "n": n, "or": r["pooled"]["or"], "lo": r["pooled"]["lo"], "hi": r["pooled"]["hi"],
                         "R": r["R"][3], "R_n": r["R"][4], "P": r["P"][3], "P_n": r["P"][4]})
    rows.sort(key=lambda r: -r["or"])
    S["checks"]["genes_amplified_above_3pct"] = rows
    S["checks"]["amplification_burden"] = {
        sid: {"share_with_any_amplification_R": float(np.mean([len(u["amps"]) > 0 for u in units[sid] if u["group"] == "R"])),
              "share_with_any_amplification_P": float(np.mean([len(u["amps"]) > 0 for u in units[sid] if u["group"] == "P"]))} for sid in c3.TEST_STUDIES}
    pr = {"pairs": 0, "both": 0, "neither": 0, "gained": 0, "lost": 0}
    for sid in c3.TEST_STUDIES:
        for a, b in paired[sid]:
            x, y = GENE in a["amps"], GENE in b["amps"]
            pr["pairs"] += 1
            pr["both" if x and y else "neither" if not x and not y else "gained" if y else "lost"] += 1
    S["checks"]["paired_patients"] = pr
    # relapse-stage frequency, adding the relapse-only trial if it reports CCNE1
    parts = {sid: (prim["tables"][sid][0], prim["tables"][sid][0] + prim["tables"][sid][1]) for sid in c3.TEST_STUDIES}
    m = [s for s in load("pancan_mappyacts_2022") if s["ccne1_covered"]]
    by = {}
    for s in m:
        by.setdefault(s["patient"], s)
    S["mappyacts_reports_ccne1"] = bool(by)
    if by:
        parts["pancan_mappyacts_2022"] = (sum(GENE in u["amps"] for u in by.values()), len(by))
    k, n = sum(p[0] for p in parts.values()), sum(p[1] for p in parts.values())
    S["relapse_frequency"] = {"per_study": {s: {"k": v[0], "n": v[1]} for s, v in parts.items()}, "all": dict(zip(("p", "lo", "hi"), c3.wilson(k, n)), k=k, n=n)}
    S["reference"] = {}
    for sid in ("os_target_gdc", "pancan_pcawg_2020"):
        by = {}
        for s in load(sid):
            if s["ccne1_covered"]:
                by.setdefault(s["patient"], s)
        k, n = sum(GENE in u["amps"] for u in by.values()), len(by)
        S["reference"][sid] = dict(zip(("p", "lo", "hi"), c3.wilson(k, n)), k=k, n=n)
    os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
    with open(os.path.join(OUT, "raw", "patients.csv"), "w", newline="") as f:   # patient-level: kept local, not published
        w = csv.writer(f)
        w.writerow(["study", "patient", "sample_used", "sample_type", "group", "gene_panel", "tumour_purity", "CCNE1_amplified", "genes_amplified"])
        for sid in c3.TEST_STUDIES:
            for u in units[sid]:
                w.writerow([sid, u["patient"], u["sample"], u["type"], u["group"], u["panel"] or "", u["purity"] if u["purity"] is not None else "",
                            int(GENE in u["amps"]), len(u["amps"])])
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["analysis", "study", "gene", "relapse_amplified", "relapse_n", "primary_amplified", "primary_n", "odds_ratio", "ci_low", "ci_high"])
        for lab, res in (("primary", prim), ("every sample", S["secondary"]["every_sample"]), ("distant metastasis v primary", S["secondary"]["distant_metastasis_only"])):
            for sid, t in res["tables"].items():
                o = res["per_study"][sid]
                w.writerow([lab, c3.LABEL[sid], GENE, t[0], t[0] + t[1], t[2], t[2] + t[3]] + ([f'{o[k]:.3f}' for k in ("or", "lo", "hi")] if o else ["", "", ""]))
            mm = res["pooled"]
            w.writerow([lab, "pooled (fixed)", GENE, res["R"][3], res["R"][4], res["P"][3], res["P"][4], f'{mm["or"]:.3f}', f'{mm["lo"]:.3f}', f'{mm["hi"]:.3f}'])
        for r in rows:
            w.writerow(["every gene amplified in >3%", "pooled (fixed)", r["gene"], r["R"], r["R_n"], r["P"], r["P_n"], f'{r["or"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}'])
    pc = lambda t: (100 * t[0], 100 * t[1], 100 * t[2])
    fig = [("CCNE1 amplification", None, None, None, None)]
    for sid in c3.TEST_STUDIES:
        a, b, c, d = prim["tables"][sid]
        fig.append((f"{c3.LABEL[sid]}, primary ({c}/{c + d})", *pc(c3.wilson(c, c + d)), "P"))
        fig.append((f"{c3.LABEL[sid]}, metastasis or relapse ({a}/{a + b})", *pc(c3.wilson(a, a + b)), "R"))
    if "pancan_mappyacts_2022" in parts:
        k, n = parts["pancan_mappyacts_2022"]
        fig.append((f"{c3.LABEL['pancan_mappyacts_2022']} ({k}/{n})", *pc(c3.wilson(k, n)), "R"))
    for sid in ("os_target_gdc", "pancan_pcawg_2020"):
        r = S["reference"][sid]
        fig.append((f"{c3.LABEL[sid]} ({r['k']}/{r['n']})", 100 * r["p"], 100 * r["lo"], 100 * r["hi"], "ref"))
    c3.bars_svg(fig, os.path.join(FIG, "engine07_ccne1.svg"), "CCNE1 amplification in osteosarcoma, by where the sample came from",
                ("Share of patients with the gene amplified, 95% CI. One sample per patient.",
                 "Blue: metastasis or relapse. Grey: primary tumour. Pale: reference cohorts of primary tumours."))
    print("== PART A")
    print(json.dumps(S["studies"]))
    for sid, t in prim["tables"].items():
        o = prim["per_study"][sid]
        print(f"  {c3.LABEL[sid]:24s} R {t[0]}/{t[0] + t[1]}  P {t[2]}/{t[2] + t[3]}  OR {c3.fmt_or(o) if o else 'n/a'}")
    print("  POOLED", c3.fmt_or(prim["pooled"]), "p=%.3g" % prim["pooled"]["p"], "I2=%.2f" % prim["pooled"]["I2"], "| VERDICT", S["verdict"], "| underpowered", S["underpowered"])
    print("  purity adjusted:", c3.fmt_or(S["checks"]["purity_adjusted"]) if S["checks"]["purity_adjusted"] else None)
    print("  every sample:", c3.fmt_or(S["secondary"]["every_sample"]["pooled"]), "| distant mets:", c3.fmt_or(S["secondary"]["distant_metastasis_only"]["pooled"]))
    print("  relapse frequency:", json.dumps(S["relapse_frequency"], default=lambda x: round(x, 3)))
    print("  reference:", json.dumps(S["reference"], default=lambda x: round(x, 3)))
    print("  paired:", pr, "| burden:", json.dumps(S["checks"]["amplification_burden"], default=lambda x: round(x, 2)))
    print("  genes amplified >3%:", [(r["gene"], f'{100 * r["rate"]:.0f}%', f'{r["R"]}/{r["R_n"]} v {r["P"]}/{r["P_n"]}', f'{r["or"]:.2f} ({r["lo"]:.2f}-{r["hi"]:.2f})') for r in rows])
    return S


# ------------------------------------------------------------------ Part B
def part_b():
    d = json.load(open(os.path.join(RAW, "search.json")))
    rows = []
    for nct, s in sorted(d["studies"].items()):
        p = s["protocolSection"]
        ident, status, design = p["identificationModule"], p["statusModule"], p.get("designModule", {})
        elig, cond, arms = p.get("eligibilityModule", {}), p.get("conditionsModule", {}), p.get("armsInterventionsModule", {})
        drugs = sorted({i["name"] for i in arms.get("interventions", [])})
        text = " ".join([ident.get("briefTitle", ""), ident.get("officialTitle", ""), " ".join(cond.get("conditions", [])), " ".join(cond.get("keywords", [])),
                         elig.get("eligibilityCriteria", ""), " ".join(drugs), p.get("descriptionModule", {}).get("briefSummary", ""),
                         " ".join(a.get("label", "") + " " + a.get("description", "") for a in arms.get("armGroups", []))]).lower()
        pkmyt1 = bool(re.search(r"pkmyt1|\bmyt1\b|lunresertib|rp-6306", text))
        ccne1 = bool(re.search(r"ccne1|cyclin[ -]?e1?\b", text))
        lead = dict(p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}))
        if not re.search(c4.ORG, lead.get("name", ""), re.I):
            lead["name"] = "Investigator-sponsored (individual)"
        countries = sorted({l.get("country", "") for l in p.get("contactsLocationsModule", {}).get("locations", []) if l.get("country")})
        rows.append({"nct": nct, "title": ident.get("briefTitle", ""), "status": status.get("overallStatus", ""),
                     "candidate": status.get("overallStatus", "") in OPEN and design.get("studyType") == "INTERVENTIONAL" and (pkmyt1 or ccne1),
                     "phase": "/".join(design.get("phases", [])), "min_age": elig.get("minimumAge", ""), "min_age_years": c4.age_years(elig.get("minimumAge", "")),
                     "max_age": elig.get("maximumAge", ""), "sponsor": lead.get("name", ""), "sponsor_class": lead.get("class", ""),
                     "countries": "; ".join(countries), "us_site": "United States" in countries, "drugs": "; ".join(drugs),
                     "pkmyt1_inhibitor_text": pkmyt1, "mentions_ccne1": ccne1, "conditions": "; ".join(cond.get("conditions", [])),
                     "matched_terms": "; ".join(d["hits"][nct])})
    with open(os.path.join(OUT, "trials.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cand = [r for r in rows if r["candidate"]]
    print("\n== PART B:", len(rows), "trials found;", len(cand), "open and mention PKMYT1 or CCNE1 (candidates to read)")
    print(collections.Counter(r["status"] for r in rows))
    cpath = os.path.join(OUT, "classification.csv")
    if not os.path.exists(cpath):
        return None
    cl = {r["nct"]: r for r in csv.DictReader(open(cpath))}
    tab = [dict(r, **{k: cl[r["nct"]][k] for k in ("counts", "open_to_osteosarcoma", "ccne1_required", "drug_class", "note")}) for r in cand]
    counted = [t for t in tab if t["counts"] == "yes"]
    yes = [t for t in counted if t["open_to_osteosarcoma"].startswith("yes")]
    A = [t for t in yes if t["status"] in ("RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION")]
    B = [t for t in A if t["min_age_years"] is not None and t["min_age_years"] < 18]
    summary = {"searched": d["searched"], "trials_found": len(rows), "candidates_read": len(cand), "meeting_rules": len(counted),
               "A_recruiting_or_about_to": len(A), "A_named": [t["nct"] for t in A if t["open_to_osteosarcoma"] == "yes, named"],
               "A_pkmyt1_inhibitor": [t["nct"] for t in A if "PKMYT1" in t["drug_class"]],
               "A_by_drug_class": dict(collections.Counter(t["drug_class"] for t in A)),
               "A_requiring_ccne1": sum(t["ccne1_required"] == "yes" for t in A),
               "B_under_18": [(t["nct"], t["min_age"], t["countries"]) for t in B], "C_us_site": [t["nct"] for t in A if t["us_site"]],
               "unclear": [t["nct"] for t in counted if t["open_to_osteosarcoma"] == "unclear"],
               "closed_to_new_patients": [t["nct"] for t in yes if t["status"] == "ACTIVE_NOT_RECRUITING"]}
    with open(os.path.join(OUT, "trials_classified.csv"), "w", newline="") as f:
        cols = ["nct", "title", "status", "phase", "drugs", "sponsor", "sponsor_class", "min_age", "max_age", "countries", "us_site",
                "counts", "open_to_osteosarcoma", "ccne1_required", "drug_class", "note"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(tab, key=lambda t: (t["counts"] != "yes", not t["open_to_osteosarcoma"].startswith("yes"), t["status"], t["nct"])))
    print(json.dumps(summary, indent=1))
    for t in A:
        print(f'  {t["nct"]} | {t["status"][:5]} | {t["phase"]:14s} | {t["min_age"]:9s} | US {str(t["us_site"]):5s} | {t["drugs"][:44]:44s} | {t["sponsor"][:26]}')
    return summary


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
    else:
        os.makedirs(OUT, exist_ok=True)
        a, b = part_a(), part_b()
        json.dump({"part_a": a, "part_b": b}, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
