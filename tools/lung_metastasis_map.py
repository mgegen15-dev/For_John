#!/usr/bin/env python3
"""Map the osteosarcoma lung-metastasis literature and cross-check it against trials.

Inputs (all local):
  data/literature/osteosarcoma_pubtator.jsonl  33k PubMed records (title, abstract, genes)
  data/literature/osteosarcoma_retracted_pmids.txt
  data/literature/osteosarcoma_reviews_pmids.txt
  data/osteosarcoma_trials.csv                 758 ClinicalTrials.gov studies

Outputs (written to data/):
  lung_metastasis_mechanisms.csv   per-mechanism paper counts
  lung_metastasis_papers.csv       one row per metastasis-focused paper
  lung_metastasis_trials.csv       trials flagged as lung/metastasis-directed

Definitions used (keyword-based, on title+abstract; see report limits section):
  metastasis-focused : matches metasta* / lung / pulmonary / "pleural"
  lung-specific      : matches lung / pulmonary / pleural
  in vivo            : mouse/mice/rat/xenograft/orthotopic/in vivo/nude/NSG ...
  in vivo metastasis : in vivo AND metastasis-focused AND an explicit metastasis-model
                       phrase (tail vein, intravenous injection, orthotopic, lung
                       nodules/colonies, metastatic burden, spontaneous metastasis ...)
  cell-only          : no in vivo and no patient/clinical term
Run:  python3 tools/lung_metastasis_map.py
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LIT = os.path.join(DATA, "literature")

# ---------------------------------------------------------------- regexes
RE_METS = re.compile(r"metasta|\blung\b|\blungs\b|pulmonary|pleural", re.I)
RE_LUNG = re.compile(r"\blung\b|\blungs\b|pulmonary|pleural", re.I)
RE_INVIVO = re.compile(
    r"\bmice\b|\bmouse\b|\brats?\b|xenograft|orthotopic|in vivo|nude mice|"
    r"\bnsg\b|\bscid\b|\bnod/|allograft|syngeneic|\bdogs?\b|\bcanine\b|zebrafish",
    re.I,
)
RE_METMODEL = re.compile(
    r"tail[- ]vein|intravenous(?:ly)? inject|i\.v\. inject|orthotopic|intratibial|"
    r"intra[- ]?tibial|paratibial|lung (?:nodul|colon|metasta|lesion|burden|foci)|"
    r"pulmonary (?:nodul|metasta|colon)|metastatic (?:burden|colonization|coloni[sz]ation)|"
    r"spontaneous(?:ly)? metasta|metastasis model|metastatic model|experimental metastasis|"
    r"number of metastas|metastatic nodul|lung metastas",
    re.I,
)
RE_PATIENT = re.compile(
    r"\bpatients?\b|\bclinical\b|cohort|\bbiops|resect|retrospective|prognos|"
    r"tissue microarray|overall survival|\btrial\b",
    re.I,
)
RE_DOG = re.compile(r"\bdogs?\b|\bcanine\b|\bcanines\b", re.I)
RE_SINGLECELL = re.compile(
    r"single[- ]cell|scRNA|snRNA|CITE-seq|spatial transcriptom|10x genomics", re.I
)

# ------------------------------------------------- mechanism dictionary
# Each entry: display name -> (regex of synonyms, mechanism family, drug if any)
MECHANISMS = [
    # --- lung niche cytokines / innate immunity
    ("IL-1 (IL1A/IL1B)", r"\bIL-?1(?:alpha|beta|a|b)?\b|interleukin-?1\b|IL1A|IL1B|inflammasome|NLRP3", "lung niche cytokine", "anakinra, canakinumab, rilonacept"),
    ("IL-6", r"\bIL-?6\b|interleukin-?6", "lung niche cytokine", "tocilizumab, siltuximab, sarilumab"),
    ("IL-8 / CXCL8", r"\bIL-?8\b|CXCL8|interleukin-?8", "lung niche cytokine", "reparixin, SX-682, ladarixin (CXCR1/2)"),
    ("IL-11", r"\bIL-?11\b|interleukin-?11", "lung niche cytokine", "none clinical"),
    ("CCL2 / CCR2", r"CCL2\b|MCP-?1\b|CCR2\b", "myeloid recruitment", "plozalizumab, CCX872 (investigational)"),
    ("CSF1R / TAM", r"CSF1R|CSF-?1R|\bCSF1\b|tumor[- ]associated macrophage|\bTAMs?\b|M2 macrophage|macrophage polari", "myeloid / macrophage", "pexidartinib, emactuzumab"),
    ("Neutrophils / NETs", r"neutrophil|\bNETs?\b|neutrophil extracellular trap|myeloid[- ]derived suppressor|\bMDSCs?\b|\bPMN-MDSC", "myeloid / neutrophil", "SX-682, DNase I (NETs), Lorlatinib n/a"),
    ("GM-CSF (CSF2)", r"GM-?CSF|CSF2\b|sargramostim", "immune stimulant", "sargramostim (inhaled, tested)"),
    ("IL-2", r"\bIL-?2\b|interleukin-?2|aldesleukin", "immune stimulant", "aldesleukin (aerosol, tested)"),
    ("IL-15", r"\bIL-?15\b|interleukin-?15", "immune stimulant", "rhIL-15, ALT-803/N-803"),
    ("NK cells", r"\bNK cells?\b|natural killer", "immune effector", "NK adoptive transfer, N-803"),
    ("Fibroblasts / CAF", r"cancer[- ]associated fibroblast|\bCAFs?\b|fibroblast activation protein|\bFAP\b|myofibroblast", "stromal niche", "FAP-directed agents (investigational)"),
    ("TGF-beta", r"TGF-?beta|TGFB1|TGF-?b1|transforming growth factor beta", "stromal niche", "galunisertib, vactosertib, AVID200"),
    # --- adhesion / cytoskeleton / motility
    ("Ezrin (VIL2/MSN family)", r"\bezrin\b|\bVIL2\b|\bMSN\b(?! )|moesin", "cytoskeleton / adhesion", "NSC305787, NSC668394 (tool compounds only)"),
    ("FAK (PTK2)", r"\bFAK\b|focal adhesion kinase|PTK2\b", "adhesion signalling", "defactinib (FDA 2025), IN10018, PF-562271"),
    ("Integrins", r"\bintegrin|ITGA\d|ITGB\d|\bITGAV\b|alpha ?v ?beta ?3|alphavbeta", "adhesion signalling", "cilengitide (failed GBM), abituzumab"),
    ("SRC", r"\bSRC\b|\bc-Src\b|SRC family kinase", "adhesion signalling", "dasatinib, saracatinib"),
    ("ROCK / RhoA", r"\bROCK1\b|\bROCK2\b|\bRhoA\b|Rho kinase", "cytoskeleton", "fasudil, netarsudil"),
    # --- chemokine homing
    ("CXCR4 / CXCL12", r"CXCR4|CXCL12|\bSDF-?1\b|stromal cell[- ]derived factor", "chemokine homing", "plerixafor, motixafortide, mavorixafor, balixafortide"),
    ("CXCR3 / CXCL9-10", r"CXCR3|CXCL9\b|CXCL10", "chemokine homing", "none approved"),
    ("CCR5", r"\bCCR5\b|CCL5\b|\bRANTES\b", "chemokine homing", "maraviroc, leronlimab"),
    # --- Wnt / bone
    ("DKK1", r"\bDKK-?1\b|dickkopf", "Wnt / bone niche", "DKN-01 (sirexatamab)"),
    ("RANKL (TNFSF11)", r"\bRANKL\b|TNFSF11|receptor activator of nuclear factor", "bone niche", "denosumab (tested, cohort 2)"),
    ("Wnt / beta-catenin", r"beta[- ]catenin|CTNNB1|\bWnt\b|Wnt signal", "Wnt / bone niche", "various investigational"),
    # --- dormancy / stemness / plasticity
    ("Dormancy", r"\bdormanc|\bdormant\b|quiescen|\bmicrometastas|latency|latent metasta|minimal residual", "dormancy", "none specific"),
    ("Autophagy", r"autophag|\bLC3\b|ATG\d|BECN1|beclin", "dormancy / stress", "hydroxychloroquine, chloroquine"),
    ("EMT", r"epithelial[- ]mesenchymal|\bEMT\b|\bSNAI1\b|\bSNAI2\b|\bTWIST1\b|\bZEB1\b", "plasticity", "none specific"),
    ("Cancer stem cells", r"cancer stem cell|\bCSCs?\b|sphere formation|tumor[- ]initiating cell|\bALDH1", "plasticity", "none specific"),
    ("NOTCH", r"\bNOTCH\d?\b|\bDLL4\b|\bJAG1\b|gamma[- ]secretase", "plasticity", "nirogacestat (DT), AL101"),
    # --- metabolism
    ("Glycolysis / HK2 / LDHA", r"glycoly|\bHK2\b|hexokinase|\bLDHA\b|Warburg|\bPKM2\b|lactate", "metabolic adaptation", "metformin (indirect), none specific"),
    ("Glutamine metabolism", r"glutamin|\bGLS\b|\bASCT2\b|SLC1A5|\bGLUL\b", "metabolic adaptation", "telaglenastat (CB-839), DRP-104"),
    ("Fatty acid / lipid metabolism", r"fatty acid oxidation|\bCPT1\b|\bFASN\b|lipid metabol|cholesterol|\bSREBP", "metabolic adaptation", "TVB-2640 (FASN), etomoxir (tool)"),
    ("Oxidative stress / ferroptosis", r"ferroptos|\bGPX4\b|\bNRF2\b|\bNFE2L2\b|reactive oxygen species|oxidative stress|\bSLC7A11\b", "metabolic adaptation", "none approved"),
    ("Hypoxia / HIF1A", r"\bHIF-?1(?:alpha|a)?\b|HIF1A\b|hypoxi", "metabolic adaptation", "belzutifan (HIF2A)"),
    # --- growth-factor / kinase axes
    ("IGF1R / IGF2", r"IGF-?1R|IGF1R\b|\bIGF-?2\b|IGF2\b|insulin[- ]like growth factor", "growth factor", "xentuzumab, ganitumab (failed unselected)"),
    ("VEGF / VEGFR", r"\bVEGF\b|VEGFA\b|\bVEGFR|\bKDR\b|angiogen", "angiogenesis", "bevacizumab, multikinase TKIs"),
    ("MET / HGF", r"\bc-Met\b|\bMET\b(?![A-Za-z])|\bHGF\b|hepatocyte growth factor", "growth factor", "cabozantinib, crizotinib, capmatinib"),
    ("mTOR / PI3K / AKT", r"\bmTOR\b|PI3K|\bAKT\b|AKT1\b|rapamycin|everolimus|sirolimus", "growth factor", "sirolimus, everolimus (dog trial negative)"),
    ("STAT3", r"\bSTAT3\b", "growth factor", "napabucasin, TTI-101"),
    ("CXCL / chemokine other", r"CXCL1\b|CXCL2\b|CXCL5\b|CXCL16", "chemokine homing", "none"),
    # --- immune checkpoints / targets in lung
    ("PD-1 / PD-L1", r"\bPD-?1\b|PDCD1\b|PD-?L1\b|CD274\b|pembrolizumab|nivolumab|camrelizumab|atezolizumab|avelumab", "checkpoint", "many approved"),
    ("GD2", r"\bGD2\b|disialoganglioside|dinutuximab|naxitamab", "surface antigen", "dinutuximab (tested AOST1421)"),
    ("B7-H3 / CD276", r"B7-?H3|CD276", "surface antigen", "ifinatamab deruxtecan, CAR-T"),
    ("HER2 / ERBB2", r"\bHER-?2\b|ERBB2\b|trastuzumab", "surface antigen", "OST-HER2 vaccine, trastuzumab deruxtecan"),
    # --- matrix / proteolysis
    ("MMPs", r"\bMMP-?\d|matrix metalloprotein", "matrix remodelling", "none (broad MMPi failed)"),
    ("uPA / PLAU", r"\bPLAU\b|urokinase|\buPAR?\b|PLAUR", "matrix remodelling", "none approved"),
    ("LOX / collagen crosslinking", r"\bLOX\b|lysyl oxidase|LOXL\d|collagen crosslink", "matrix remodelling", "simtuzumab (failed elsewhere)"),
    # --- other named leads
    ("Platelets / coagulation", r"platelet|thrombocyt|\btissue factor\b|coagulat|fibrin", "intravascular survival", "aspirin, LMWH"),
    ("Exosomes / EVs", r"exosom|extracellular vesicle|\bEVs?\b(?! )|microvesicle", "communication", "none"),
    ("Anoikis", r"anoikis", "intravascular survival", "none"),
    ("ctDNA / liquid biopsy", r"\bctDNA\b|circulating tumor DNA|liquid biopsy|cell[- ]free DNA|\bcfDNA\b|circulating tumou?r cell|\bCTCs?\b", "detection", "assay, not a drug"),
    ("Imaging surveillance", r"\bCT scan|chest CT|computed tomograph|\bPET\b|FDG|surveillance imaging|chest radiograph|chest x-?ray", "detection", "n/a"),
    ("Single-cell / spatial", r"single[- ]cell|scRNA|snRNA|spatial transcriptom|CITE-seq", "method", "n/a"),
    ("Inhaled / aerosol delivery", r"inhal|aerosol|nebuli[sz]|intratracheal|intranasal deliver|pulmonary deliver|dry powder", "delivery route", "inhaled GM-CSF, ILC, aerosol IL-2"),
    ("Radiotherapy / SBRT", r"\bSBRT\b|stereotactic body radi|stereotactic ablative|\bSABR\b|radiotherapy|radiation therapy|\bRT\b(?! )|samarium|radium-223", "local therapy", "SBRT, radium-223"),
    ("Metastasectomy / surgery", r"metastasectom|pulmonary resection|thoracotom|thoracoscop|\bVATS\b|wedge resection|lung resection", "local therapy", "surgery"),
]

TRIAL_LUNG_RE = re.compile(
    r"\blung\b|pulmonary|metasta|inhal|aerosol|nebuli|thoracotom|metastasectom|"
    r"\bSBRT\b|stereotactic|resect|pleural",
    re.I,
)


def load_pmid_set(path):
    if not os.path.exists(path):
        return set()
    return {l.strip() for l in open(path) if l.strip()}


def main():
    retracted = load_pmid_set(os.path.join(LIT, "osteosarcoma_retracted_pmids.txt"))
    reviews = load_pmid_set(os.path.join(LIT, "osteosarcoma_reviews_pmids.txt"))

    recs = {}
    for line in open(os.path.join(LIT, "osteosarcoma_pubtator.jsonl")):
        d = json.loads(line)
        recs[d["pmid"]] = d  # dedupe on pmid

    papers = []
    for pmid, d in recs.items():
        text = (d.get("title") or "") + " " + (d.get("abstract") or "")
        mets = bool(RE_METS.search(text))
        lung = bool(RE_LUNG.search(text))
        invivo = bool(RE_INVIVO.search(text))
        patient = bool(RE_PATIENT.search(text))
        metmodel = bool(RE_METMODEL.search(text))
        papers.append(
            dict(
                pmid=pmid,
                year=d.get("year") or "",
                journal=d.get("journal") or "",
                title=(d.get("title") or "").replace("\n", " "),
                text=text,
                mets=mets,
                lung=lung,
                invivo=invivo,
                patient=patient,
                invivo_mets=invivo and mets and metmodel,
                cell_only=(not invivo) and (not patient),
                dog=bool(RE_DOG.search(text)),
                sc=bool(RE_SINGLECELL.search(text)),
                retracted=pmid in retracted,
                review=pmid in reviews,
                has_abstract=bool(d.get("abstract")),
            )
        )

    tot = len(papers)
    research = [p for p in papers if not p["review"] and not p["retracted"]]
    print(f"records: {tot} unique pmids; {len(research)} non-review non-retracted")
    for key in ("mets", "lung", "invivo_mets"):
        print(f"  {key}: all={sum(p[key] for p in papers)} research={sum(p[key] for p in research)}")

    # ------------------------------------------------ per mechanism
    rows = []
    for name, pat, family, drug in MECHANISMS:
        rx = re.compile(pat, re.I)
        hits = [p for p in research if rx.search(p["text"])]
        mh = [p for p in hits if p["mets"]]
        lh = [p for p in hits if p["lung"]]
        ivm = [p for p in mh if p["invivo_mets"]]
        co = [p for p in mh if p["cell_only"]]
        pt = [p for p in mh if p["patient"]]
        dg = [p for p in hits if p["dog"]]
        rows.append(
            dict(
                mechanism=name,
                family=family,
                drug_available=drug,
                papers=len(hits),
                metastasis_papers=len(mh),
                lung_papers=len(lh),
                in_vivo_metastasis=len(ivm),
                cell_only_metastasis=len(co),
                patient_metastasis=len(pt),
                dog_papers=len(dg),
                first_year=min([p["year"] for p in hits if p["year"]], default=""),
                ivm_pmids=";".join(sorted(p["pmid"] for p in ivm)[:40]),
            )
        )
    rows.sort(key=lambda r: -r["in_vivo_metastasis"])

    out = os.path.join(DATA, "lung_metastasis_mechanisms.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", out)

    print(f"\n{'mechanism':34s} {'pap':>5s} {'mets':>5s} {'lung':>5s} {'ivm':>5s} {'cell':>5s} {'pt':>4s} {'dog':>4s}")
    for r in rows:
        print(f"{r['mechanism'][:34]:34s} {r['papers']:5d} {r['metastasis_papers']:5d} "
              f"{r['lung_papers']:5d} {r['in_vivo_metastasis']:5d} {r['cell_only_metastasis']:5d} "
              f"{r['patient_metastasis']:4d} {r['dog_papers']:4d}")

    # ------------------------------------------------ paper-level dump
    out2 = os.path.join(DATA, "lung_metastasis_papers.csv")
    with open(out2, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pmid", "year", "journal", "in_vivo_metastasis", "lung", "dog",
                    "single_cell", "patient", "title"])
        for p in sorted((p for p in research if p["mets"]), key=lambda x: x["year"]):
            w.writerow([p["pmid"], p["year"], p["journal"], p["invivo_mets"], p["lung"],
                        p["dog"], p["sc"], p["patient"], p["title"]])
    print("wrote", out2)

    # ------------------------------------------------ year trend
    yr = Counter()
    yrivm = Counter()
    for p in research:
        if not p["year"]:
            continue
        b = (int(p["year"]) // 5) * 5
        if p["mets"]:
            yr[b] += 1
        if p["invivo_mets"]:
            yrivm[b] += 1
    print("\nmetastasis-focused papers by 5-year block (research only):")
    for b in sorted(yr):
        print(f"  {b}-{b+4}: mets={yr[b]:5d} in-vivo-mets={yrivm[b]:5d}")

    # ------------------------------------------------ dog + single cell lists
    sc_mets = [p for p in research if p["sc"] and p["mets"]]
    dog_mets = [p for p in research if p["dog"] and p["mets"]]
    print(f"\nsingle-cell/spatial + metastasis papers: {len(sc_mets)}")
    print(f"dog/canine + metastasis papers: {len(dog_mets)}")

    # ------------------------------------------------ trials cross-check
    trials = list(csv.DictReader(open(os.path.join(DATA, "osteosarcoma_trials.csv"))))
    lung_trials = []
    for t in trials:
        blob = " ".join([t.get("title", ""), t.get("primary_outcomes", ""),
                         t.get("interventions", ""), t.get("conditions", ""),
                         t.get("scope", "")])
        if TRIAL_LUNG_RE.search(blob):
            lung_trials.append(t)
    print(f"\ntrials: {len(trials)} total; {len(lung_trials)} mention lung/metastasis/inhaled terms")

    strict = re.compile(r"\blung\b|pulmonary|inhal|aerosol|nebuli|thoracotom|metastasectom|"
                        r"\bSBRT\b|stereotactic|pleural", re.I)
    strict_trials = [t for t in lung_trials
                     if strict.search(" ".join([t.get("title", ""), t.get("interventions", ""),
                                                t.get("primary_outcomes", ""), t.get("conditions", "")]))]
    print(f"  of those, {len(strict_trials)} explicitly lung-directed / lung-local")
    out3 = os.path.join(DATA, "lung_metastasis_trials.csv")
    with open(out3, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(trials[0].keys()) + ["lung_directed"])
        w.writeheader()
        sset = {t["nct_id"] for t in strict_trials}
        for t in lung_trials:
            t = dict(t)
            t["lung_directed"] = t["nct_id"] in sset
            w.writerow(t)
    print("wrote", out3)
    for t in sorted(strict_trials, key=lambda x: x.get("start") or ""):
        print(f"  {t['nct_id']} {t.get('start','')[:7]:8s} {t.get('status','')[:12]:12s} "
              f"{t.get('phase','')[:8]:8s} n={t.get('enrollment','')or '?':>5s} res={t.get('has_results','')[:5]:5s} "
              f"{t['title'][:95]}")

    # ------------------------------------------------ mechanisms with drug, no trial
    trial_blob = " ".join(
        " ".join([t.get("title", ""), t.get("interventions", ""), t.get("primary_outcomes", "")])
        for t in trials
    ).lower()
    print("\nmechanism drug-name presence in the 758-trial file:")
    for r in rows:
        if r["drug_available"] in ("none", "n/a", "") or r["in_vivo_metastasis"] < 3:
            continue
        names = [d.strip().split(" (")[0].lower() for d in r["drug_available"].split(",")]
        found = [n for n in names if n and len(n) > 4 and n in trial_blob]
        print(f"  {r['mechanism'][:32]:32s} ivm={r['in_vivo_metastasis']:3d} "
              f"drugs_in_trial_file={found if found else 'NONE'}")


if __name__ == "__main__":
    main()
