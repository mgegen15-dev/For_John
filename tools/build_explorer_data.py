"""Build docs/data/explorer.json, the data behind the evidence explorer page
(docs/explorer.html): one compact record per gene symbol that pulls together
what the project's tables say about it.

Usage: python3 tools/build_explorer_data.py   (from the repository root)

Inputs (all in data/, already in the repository):
  osteosarcoma_gene_evidence.csv           literature counts, trials, grants
  osteosarcoma_evidence_risk_genes.csv     paper-mill risk flag
  osteosarcoma_surface_target_candidates.csv  tumour vs normal RNA, rank
  osteosarcoma_copy_number_frequencies.csv amplification / deletion frequency
  osteosarcoma_repurposing_candidates.csv  approved drugs, score, verdict
  osteosarcoma_trials.csv + drug_targets_curated.json  drugs named in trials
  reports/*.md, briefs/*.md                which reports mention the symbol

Optional inputs, included when present (re-run after they appear):
  osteosarcoma_survival_results.csv        any columns, keyed by gene/symbol
  osteosarcoma_contradictions.csv          any columns, keyed by gene/symbol

Genes kept: every gene in the literature table, the repurposing screen, the
risk table or the copy-number table, the surface-target shortlist, and the
curated leads below. Surface-table genes outside the shortlist are kept only
if they already appear elsewhere. Long lists are truncated.

The curated LEADS and NOTES below follow reports/Ranked leads and research
partners.md (lead numbers, scores) and the labels on docs/index.html. Edit
them here when the reports change.
"""
import csv, glob, json, os, re, datetime
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, "data", *p)
OUT = os.path.join(ROOT, "docs", "data", "explorer.json")

RANKED = "reports/Ranked leads and research partners.md"
LUNG = "reports/Stopping lung metastasis in osteosarcoma.md"
CN = "reports/Copy-number changes and the kinase-pill biomarker.md"
SURF = "reports/New surface targets for osteosarcoma.md"
REPO = "reports/Approved drugs worth testing in osteosarcoma.md"
BRIEF = "briefs/Brief - pet dog trial of FAK or DKK1 blockade.md"
PILLS = "reports/Why kinase-inhibitor pills work in osteosarcoma.md"
RISK = "reports/Evidence risk flags for osteosarcoma genes.md"

# lead number -> (title, score out of 12, evidence score out of 3, label, main report)
LEAD_INFO = {
    1: ("Block IL-1 or IL-6 after surgery to stop lung metastasis", 10, 2, "Hypothesis", LUNG),
    2: ("Test whether gene amplifications predict who benefits from VEGFR2-blocking pills", 10, 2,
        "Confirmed activity; who benefits is a Lead", CN),
    4: ("Pet-dog study of FAK or DKK1 blockade", 9, 3, "Lead", BRIEF),
    5: ("LRRC15 as a surface target: follow and inform the trials already running", 9, 3, "Lead", SURF),
    6: ("PTK7 as a surface target: stain patient tumours", 9, 2, "Lead", SURF),
    9: ("Block the IL-8 receptor (CXCR1/2) against lung metastasis", 8, 2, "Hypothesis", LUNG),
    10: ("Add metastasis to an existing aspirin-versus-blood-thinner trial", 8, 2, "Lead", LUNG),
    13: ("AKT blockers (capivasertib) with chemotherapy", 8, 1, "Lead (weaker: abstract-only evidence)", REPO),
    14: ("CXCR4 blockers (mavorixafor) against lung metastasis", 8, 1, "Lead (weaker: abstract-only evidence)", REPO),
}
LEADS = {
    "IL1A": 1, "IL1B": 1, "IL1R1": 1, "IL6": 1, "IL6R": 1, "IL6ST": 1,
    "VEGFA": 2, "KDR": 2, "PDGFRA": 2, "KIT": 2,
    "PTK2": 4, "DKK1": 4,
    "LRRC15": 5, "PTK7": 6,
    "CXCL8": 9, "CXCR1": 9, "CXCR2": 9,
    "PTGS1": 10, "F2": 10, "F10": 10, "F2R": 10, "P2RY12": 10, "ITGB3": 10, "ITGA2B": 10,
    "F3": 10, "LPAR1": 10, "PDPN": 10,
    "AKT1": 13, "CXCR4": 14,
}
# Short plain-language notes for main genes (leads and much-discussed non-leads).
NOTES = {
    "IL6": ("After amputation, IL-6 rose in a dog trial; blocking IL-6 with IL-8 reduced lung spread in mice. "
            "Approved IL-6 drugs exist but none has an osteosarcoma efficacy trial.", [LUNG, RANKED]),
    "IL1A": ("Lung tissue releases IL-1 alpha, which drives osteosarcoma cells to make IL-6 and IL-8 and settle in the lung (mouse work).",
             [LUNG, RANKED]),
    "IL1B": ("IL-1 blockade reduced lung metastasis in mice; anakinra and canakinumab are approved IL-1 blockers.", [LUNG, RANKED]),
    "CXCL8": ("IL-8. An anti-IL-8 antibody reduced lung metastasis in mice; oral CXCR1/2 blockers exist.", [LUNG, RANKED]),
    "CXCR4": ("Lung tissue is rich in CXCL12, the signal CXCR4 responds to. Blocking peptides cut lung metastases in mice, but "
              "blocking it can also keep killer T cells out of tumours. Mavorixafor (oral) is approved.", [REPO, RANKED]),
    "PTK2": ("FAK. Blocking it reduced lung spread in small mouse studies; defactinib exists. Dog studies are listed but unpublished. "
             "PTK2 amplification mostly travels with MYC.", [BRIEF, RANKED, CN]),
    "DKK1": ("Blocking DKK1 reduced lung spread in small mouse studies; an antibody exists. Dog programmes are planned.", [BRIEF, RANKED]),
    "AKT1": ("AKT inhibitors prolonged event-free survival in all 6 osteosarcoma xenografts tested by NCI, but shrank none. "
             "No osteosarcoma paper tests capivasertib itself. Elevated paper-mill flag.", [REPO, RANKED]),
    "MYC": ("Amplified in about a third of these tumours (8q24). No direct MYC drug.", [CN]),
    "VEGFA": ("6p21 amplicon. About a quarter of tumours carry extra copies of the VEGFR-pill target genes by a strict definition. "
              "Bevacizumab (anti-VEGF) has been tried in osteosarcoma.", [CN, PILLS, RANKED]),
    "KDR": ("VEGFR2, the main target of the kinase pills (cabozantinib, regorafenib, lenvatinib, apatinib) that are active, but briefly, in relapse.",
            [PILLS, CN, RANKED]),
    "PDGFRA": ("On 4q12 with KDR and KIT; often co-amplified. A target of several VEGFR pills.", [CN, RANKED]),
    "KIT": ("On 4q12 with KDR and PDGFRA. A target of several VEGFR pills.", [CN, RANKED]),
    "LRRC15": ("Ranked top in this project's surface-target screen. Three studies have now found the protein in patient tumours, "
               "and four registered trials target it, one in relapsed osteosarcoma.", [SURF, RANKED]),
    "PTK7": ("Ranked high as a surface target, but no series of patient tumours has been stained for it yet.", [SURF, RANKED]),
    "CD276": ("B7-H3. A B7-H3 antibody-drug conjugate beat standard chemotherapy in a randomized relapse trial (ARTEMIS-011), "
              "with heavier side effects.", [SURF, RANKED]),
    "ERBB2": ("HER2. No tumour in the open copy-number data amplifies it by the main call; HER2 drugs have been tried in osteosarcoma.", [CN, SURF]),
    "MDM2": ("Amplified in 2.5% of these mostly paediatric, diagnosis-time tumours, lower than adult and relapse series.", [CN]),
    "CCNE1": ("Cyclin E1. Amplified in about 18% of tumours (19q12); CDK2 inhibitors are the drug class. Its literature carries a high paper-mill flag.",
              [CN, RISK]),
    "GD2": ("A sugar-lipid on the cell surface, not a gene: matched in the literature by text. Anti-GD2 antibodies (dinutuximab, naxitamab) "
            "have been tried in osteosarcoma; after lung-metastasis surgery dinutuximab gave about 28% event-free at 12 months in a single-arm trial.",
            [RANKED, SURF]),
    "CDK4": ("Amplified in about 4% of these tumours (12q14), lower than adult and relapse series. CDK4/6 inhibitors have been trialled.", [CN]),
}
ALIASES = {
    "PTK2": ["FAK"], "ERBB2": ["HER2", "NEU"], "CD276": ["B7-H3", "B7H3"], "KDR": ["VEGFR2", "VEGFR-2", "FLK1"],
    "FLT1": ["VEGFR1"], "FLT4": ["VEGFR3"], "VEGFA": ["VEGF"], "CXCL8": ["IL-8", "IL8"], "IL6": ["IL-6"],
    "IL1A": ["IL-1A", "IL-1 alpha"], "IL1B": ["IL-1B", "IL-1 beta"], "IL6R": ["IL-6R"], "IL1R1": ["IL-1R"],
    "KIT": ["c-KIT", "CD117"], "MET": ["c-MET", "HGFR"], "CD274": ["PD-L1", "PDL1"], "PDCD1": ["PD-1", "PD1"],
    "CTLA4": ["CTLA-4"], "TNFSF11": ["RANKL"], "TNFRSF11A": ["RANK"], "MTOR": ["mTOR"], "PTGS1": ["COX-1", "COX1"],
    "PTGS2": ["COX-2", "COX2"], "F3": ["tissue factor"], "CCNE1": ["cyclin E1"], "PARP1": ["PARP"], "IGF1R": ["IGF-1R"],
    "CXCR2": ["IL-8 receptor"], "CXCR1": ["IL-8 receptor"], "EGFR": ["HER1"], "CD44": [], "GD2": ["disialoganglioside"],
}
# Uppercase words in the reports that collide with a gene symbol but are not about the gene.
REPORT_STOP = {"MB", "LTA", "ALB", "TXK", "TNM", "SET", "CAT", "IV", "II", "III"}
DRUG_RENAME = {"zoledron": "zoledronic acid", "mage": "MAGE-targeted therapy", "prame": "PRAME-targeted therapy",
               "nkg2d": "NKG2D-based cell therapy"}
PH_NAME = {"0.5": "Early phase 1", "1": "Phase 1", "1.5": "Phase 1/2", "2": "Phase 2", "2.5": "Phase 2/3", "3": "Phase 3", "4": "Approved"}
TRIAL_PH = {"EARLY_PHASE1": 0.5, "PHASE1": 1, "PHASE1/PHASE2": 1.5, "PHASE2": 2, "PHASE2/PHASE3": 2.5, "PHASE3": 3, "PHASE4": 4}


def rows(name):
    p = D(name)
    if not os.path.exists(p):
        return None
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v):
    if v is None or v == "":
        return None
    try:
        x = float(v)
    except ValueError:
        return None
    return int(x) if x == int(x) and abs(x) < 1e15 else round(x, 1)


def short(s, n=320):
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def phase_label(v):
    x = num(v)
    if x is None:
        return ""
    return PH_NAME.get(str(x), "Phase %s" % x)


def main():
    genes = {}

    def G(sym):
        sym = sym.strip()
        if sym not in genes:
            genes[sym] = {"gene": sym}
        return genes[sym]

    # 1. literature evidence
    for r in rows("osteosarcoma_gene_evidence.csv") or []:
        g = G(r["gene"])
        g["papers"] = num(r["papers"]); g["first_year"] = num(r["first_year"]); g["since_2021"] = num(r["since_2021"])
        g["in_vivo"] = num(r["in_vivo"]); g["patient"] = num(r["patients"]); g["dog"] = num(r["dog"])
        g["pct_ncrna"] = num(r["pct_ncrna"]); g["pct_cell_or_ncrna"] = num(r["pct_cell_only_or_ncrna"])
        g["retracted"] = num(r["retracted"]); g["trials"] = num(r["trials"]) or 0
        g["best_phase"] = phase_label(r["best_phase"]) if num(r["best_phase"]) else ""
        g["nih_grants"] = num(r["nih_grants"])
        ids = r["trial_ids"].split()
        if ids:
            g["nct"] = ids[:6]

    # 2. paper-mill risk flag
    for r in rows("osteosarcoma_evidence_risk_genes.csv") or []:
        g = G(r["gene"])
        g["risk"] = r["risk"]
        g["risk_detail"] = {"papers_since_2010": num(r["papers_since_2010"]), "pct_retracted": num(r["pct_retracted"]),
                            "pct_retracted_ci95": r["pct_retracted_ci95"], "fragile": r["flag_changes_with_one_retraction_fewer"] == "True"}

    # 3. repurposing screen (approved / late-stage drugs)
    for r in rows("osteosarcoma_repurposing_candidates.csv") or []:
        g = G(r["gene"])
        others = [d.strip() for d in r["other_drugs"].split(";") if d.strip()]
        rp = {
            "best_drug": r["best_drug"], "phase": phase_label(r["best_drug_phase"]),
            "action": r["best_drug_action"].lower().replace("_", " "), "mechanism": short(r["best_drug_mechanism"], 120),
            "oral": r["best_drug_oral"] == "True", "boxed_warning": r["best_drug_boxed_warning"] == "True",
            "first_approval": num(r["best_drug_first_approval"]), "other_drugs": others[:8], "n_drugs": num(r["n_drugs"]),
            "score": num(r["score"]), "shortlist_rank": num(r["shortlist_rank"]), "verdict": r["verdict"],
            "note": short(r["review_note"], 300), "os_trial_status": r["os_trial_status"],
            "os_trials": r["os_trials"].split()[:6] if r["os_trials"] else [], "excluded": r["excluded"],
            "target": r["chembl_target"],
        }
        g["repurposing"] = {k: v for k, v in rp.items() if v not in ("", None, [], False)}
        if r["tumour_median_tpm"] and "tpm" not in g:
            g["tpm"] = num(r["tumour_median_tpm"]); g["pct_expr"] = num(r["pct_tumours_expressing"])
        if not g.get("risk") and r["risk_flag"]:
            g["risk"] = r["risk_flag"]

    # 4. surface targets (tumour vs normal RNA)
    for r in rows("osteosarcoma_surface_target_candidates.csv") or []:
        sym = r["symbol"]
        if not r["rank_shortlist"] and sym not in genes and sym not in LEADS:
            continue
        g = G(sym)
        g["tpm"] = num(r["tumour_median_tpm"]); g["pct_expr"] = num(r["pct_tumours_expressing"])
        s = {"rank": num(r["rank_shortlist"]), "rank_overall": num(r["rank_overall"]),
             "max_vital_normal_tpm": num(r["max_vital_normal_tpm"]), "worst_vital_tissue": r["worst_vital_tissue"].replace("_", " "),
             "window_score": num(r["window_score"]), "surface_confidence": r["surface_confidence"],
             "in_os_trials": r["already_in_os_trials"] == "True", "n_tumours": num(r["n_tumours"])}
        g["surface"] = {k: v for k, v in s.items() if v not in ("", None)}

    # 5. copy number
    cn_rows = rows("osteosarcoma_copy_number_frequencies.csv") or []
    group = {"4q12_amp": ["KDR", "PDGFRA", "KIT"]}
    for r in cn_rows:
        targets = [r["gene"]] if r["gene"] in genes or re.fullmatch(r"[A-Z0-9]+", r["gene"]) else group.get(r["gene"], [])
        for sym in targets:
            g = G(sym)
            ev = {"event": r["event"], "definition": r["definition"], "pct": num(r["pct"]), "n": num(r["n_altered"]),
                  "of": num(r["n_patients"]), "ci": "%s–%s%%" % (r["ci95_low"], r["ci95_high"])}
            if sym != r["gene"]:
                ev["region"] = "4q12 (KDR, PDGFRA or KIT)"
            if r["published_comparison"]:
                ev["published"] = short(r["published_comparison"], 260)
            cn = g.setdefault("copy_number", {"cytoband": r["cytoband"], "events": []})
            cn["events"].append(ev)
            if r["event"] == "amp" and sym == r["gene"]:
                g["amp_pct"] = num(r["pct"])
            if r["event"] == "deepdel" and sym == r["gene"]:
                g["deldeep_pct"] = num(r["pct"])

    # 6. drugs named in osteosarcoma trials (curated pattern -> target map)
    dmap = json.load(open(D("drug_targets_curated.json"))); dmap.pop("_note", None)
    trial_rows = [r for r in rows("osteosarcoma_trials.csv") or [] if r["study_type"] == "INTERVENTIONAL"]
    hits = defaultdict(lambda: defaultdict(set))
    for r in trial_rows:
        iv = r["interventions"].lower() + " " + r["title"].lower()
        for pat, targets in dmap.items():
            if re.search(pat, iv):
                for t in targets:
                    hits[t][pat].add(r["nct_id"])
    for sym, pats in hits.items():
        g = G(sym)
        lst = []
        for pat, ids in sorted(pats.items(), key=lambda kv: -len(kv[1])):
            names = [p for p in pat.split("|") if re.fullmatch(r"[a-z][a-z -]{3,}", p)] or [pat.split("|")[0]]
            names = [DRUG_RENAME.get(n, n) for n in names]
            lst.append({"drug": names[0], "also": names[1:4], "trials": len(ids), "nct": sorted(ids)[:4]})
        g["trial_drugs"] = lst[:8]

    # 7. optional later analyses
    for key, fname in (("survival", "osteosarcoma_survival_results.csv"), ("contradictions", "osteosarcoma_contradictions.csv")):
        rs = rows(fname)
        if not rs:
            continue
        col = next((c for c in ("gene", "symbol", "gene_symbol", "target", "Gene") if c in rs[0]), None)
        if not col:
            print("skipped %s: no gene/symbol column" % fname); continue
        for r in rs:
            sym = (r[col] or "").strip()
            if not sym:
                continue
            g = G(sym)
            rec = {k: short(v, 300) for k, v in r.items() if k != col and v not in ("", None)}
            lst = g.setdefault(key, [])
            if len(lst) < 12:
                lst.append(rec)
        print("included %s (%d rows)" % (fname, len(rs)))

    # 8. leads and notes
    for sym, n in LEADS.items():
        title, score, ev, label, rep = LEAD_INFO[n]
        G(sym)["lead"] = {"n": n, "title": title, "score": score, "evidence": ev, "label": label}
    for sym, (text, reps) in NOTES.items():
        G(sym)["note"] = text
    for sym, al in ALIASES.items():
        if sym in genes and al:
            genes[sym]["aliases"] = al

    # 9. reports mentioning the symbol
    report_files = sorted(glob.glob(os.path.join(ROOT, "reports", "*.md")) + glob.glob(os.path.join(ROOT, "briefs", "*.md")))
    mentions = defaultdict(list)
    for f in report_files:
        rel = os.path.relpath(f, ROOT)
        text = open(f, encoding="utf-8").read()
        words = set(re.findall(r"(?<![A-Za-z0-9-])[A-Z][A-Z0-9]{1,11}(?![A-Za-z0-9-])", text))
        for w in words:
            if w in genes and w not in REPORT_STOP:
                mentions[w].append(rel)
    for sym, g in genes.items():
        reps = []
        if sym in NOTES:
            reps += NOTES[sym][1]
        if sym in LEADS:
            reps += [RANKED, LEAD_INFO[LEADS[sym]][4]]
        reps += mentions.get(sym, [])
        seen = []
        for r in reps:
            if r not in seen:
                seen.append(r)
        if seen:
            g["reports"] = seen[:8]

    # drop near-empty records: no literature, no drug, no surface rank, no lead
    def keep(g):
        return any(k in g for k in ("papers", "repurposing", "surface", "lead", "copy_number", "risk", "trial_drugs",
                                    "survival", "contradictions"))
    out = [ {k: v for k, v in g.items() if v not in (None, "", [])} for g in genes.values() if keep(g)]
    out.sort(key=lambda g: (-(g.get("papers") or 0), g["gene"]))

    manifest_date = ""
    mp = os.path.join(ROOT, "DATA_MANIFEST.md")
    if os.path.exists(mp):
        m = re.search(r"Generated (\d{4}-\d{2}-\d{2})", open(mp, encoding="utf-8").read())
        manifest_date = m.group(1) if m else ""
    meta = {"built": datetime.date.today().isoformat(), "manifest_date": manifest_date, "n_genes": len(out),
            "leads": {str(k): {"title": v[0], "score": v[1], "evidence": v[2], "label": v[3]} for k, v in LEAD_INFO.items()},
            "optional": [k for k, f in (("survival", "osteosarcoma_survival_results.csv"),
                                        ("contradictions", "osteosarcoma_contradictions.csv")) if os.path.exists(D(f))]}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "genes": out}, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote %s: %d genes, %.0f KB" % (os.path.relpath(OUT, ROOT), len(out), os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
