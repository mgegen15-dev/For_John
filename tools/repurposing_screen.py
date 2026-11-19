"""Systematic screen for approved (or phase 3) drugs whose targets look relevant
to osteosarcoma but have never had an osteosarcoma efficacy trial.

Why: an approved drug has known dosing, safety and supply, so it is the fastest
route from a lab result to a patient. The screen asks, for every human protein
that an approved or late-stage drug acts on: is it made in osteosarcoma
tumours, does the osteosarcoma literature support it with animal and patient
data (and not mainly with paper-mill-prone microRNA studies), how usable is the
best drug, and has anyone already tried a drug against it in osteosarcoma?

Stages (each caches to data/repurposing_raw/, which is git-ignored):

    python3 tools/repurposing_screen.py chembl   # ChEMBL drugs, mechanisms, targets
    python3 tools/repurposing_screen.py build    # gene table + local trial matching
    python3 tools/repurposing_screen.py pubmed   # PubMed counts: osteosarcoma + drug name
    python3 tools/repurposing_screen.py ctgov    # ClinicalTrials.gov checks, top genes
    python3 tools/repurposing_screen.py score    # final score -> CSV + console table
    python3 tools/repurposing_screen.py all

Inputs (all already in the repository):
  * ChEMBL REST API (https://www.ebi.ac.uk/chembl/api/data/): molecule
    (max_phase 4 and, separately, 3), mechanism, target.
  * data/surface_targets_raw/tumour_summary.json -- TARGET-OS RNA-seq summary
    (88 tumours; built by tools/surface_targets.py from GDC STAR counts).
    GTEx medians from data/surface_targets_raw/gtex_medians.json where cached
    (surface genes only).
  * data/osteosarcoma_gene_evidence.csv, data/osteosarcoma_evidence_risk_genes.csv
  * data/osteosarcoma_trials.csv, data/drug_targets_curated.json
  * NIH grant counts come from the nih_grants column of the gene evidence table
    (built from data/nih_osteosarcoma_projects.csv by tools/literature_map.py).
  * ClinicalTrials.gov API v2 for drug name + osteosarcoma, and for the number
    of interventional trials of the drug that enrol children (StdAge CHILD).

Score (0-100, every part stated so it can be argued with):

  f(x, c) = min(1, ln(1 + x) / ln(1 + c))        # saturating log scale

  EVIDENCE  (0-30) = [12 f(in_vivo, 40) + 10 f(patients, 40) + 3 f(dog, 5)
                      + 5 f(papers, 100)]
                     x (1 - 0.5 * pct_cell_only_or_ncrna / 100)
                     x risk factor (high 0.5, elevated 0.75, otherwise 1)
              -- or, if higher, DRUG LITERATURE = 20 f(drug_papers, 30), where
                 drug_papers is the PubMed count of osteosarcoma[tiab] AND
                 "<drug>"[tiab] for the gene's best-documented drug with <= 3
                 ChEMBL mechanisms (gene tagging misses papers that name only
                 the drug, e.g. propranolol or digoxin).
  EXPRESSION(0-25) = 25 x f(median TPM, 50) x (% tumours with TPM >= 5) / 100
  DRUGGABLE (0-25) = phase (approved 10, phase 3 only 6)
                     + oral 5
                     + paediatric experience (>= 5 interventional trials that
                       enrol children 5; 1-4 trials 3; none 0; not queried 0)
                     + safety (no boxed warning 5; boxed warning 2)
                     -- taken from the single best drug for the gene.
  UNTESTED  (0-20) = 20 no osteosarcoma trial has used any drug against the gene;
                      6 a drug against it was named in the title of a basket
                        trial that enrolled osteosarcoma among other cancers;
                     10 only "indirect" use (a multi-target drug with > 3
                        ChEMBL mechanisms, or the drug is listed as an intervention but not
                        named in the trial title, e.g. a supportive-care or
                        backbone role);
                      0 a trial named a drug against the gene in the title of an
                        osteosarcoma or bone-sarcoma trial.
  TOTAL = (EVIDENCE + EXPRESSION + DRUGGABLE + UNTESTED) x direction factor
          direction factor = 1 if the best drug inhibits/blocks/antagonises
          the target, 0.75 if it is an agonist/activator (the "make more of
          it" logic is weaker for a tumour-expressed protein).

Shortlist rules: no exclusion flag, not an existing project lead, at least
10 osteosarcoma papers with 3 or more mentioning animal data, or at least 5
osteosarcoma papers naming the drug, and not removed on hand review (REVIEW
below gives every removal and its reason).

Exclusions from the shortlist (kept in the CSV, flagged): targets already
heavily trialled in osteosarcoma (VEGFR multi-kinase, mTOR, PD-1/PD-L1, CTLA4,
CDK4/6, IGF1R, GD2, B7-H3, HER2, RANKL, FDPS, PARP1, SRC ...), cytotoxic
chemotherapy targets, and genes with no osteosarcoma literature row (fewer than
5 non-review papers). The project's existing leads (IL-1/IL-6, CXCR1/2, FAK,
DKK1, platelets/LPAR1) are flagged as existing_lead and listed separately.

Every output row is a hypothesis for laboratory testing, not a treatment
recommendation. Nothing here needs credentials.
"""
import csv
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "repurposing_raw")
OUT_CSV = os.path.join(ROOT, "data", "osteosarcoma_repurposing_candidates.csv")
os.makedirs(RAW, exist_ok=True)

CHEMBL = "https://www.ebi.ac.uk/chembl/api/data"
CTGOV = "https://clinicaltrials.gov/api/v2/studies"
UA = {"User-Agent": "open-science-repurposing-screen/1.0"}

EXPR_FLOOR = 5.0  # same per-sample "expressing" floor as tools/surface_targets.py
N_CTGOV = 80      # genes (by preliminary score) checked on ClinicalTrials.gov
DRUGS_PER_GENE = 4

# Targets already heavily trialled in osteosarcoma (task brief + trials report).
HEAVY = {
    "KDR", "FLT1", "FLT4", "PDGFRA", "PDGFRB", "KIT", "RET", "FGFR1", "MET",
    "VEGFA", "MTOR", "PDCD1", "CD274", "CTLA4", "CDK4", "CDK6", "IGF1R",
    "B4GALNT1", "CD276", "ERBB2", "TNFSF11", "FDPS", "PARP1", "PARP2", "SRC",
    "ABL1", "EGFR", "GPNMB",
}
# Cytotoxic chemotherapy targets: the backbone of every osteosarcoma regimen.
CHEMO_PREFIX = ("TUBA", "TUBB")
CHEMO = {"TOP1", "TOP2A", "TOP2B", "DHFR", "TYMS", "RRM1", "RRM2", "POLA1",
         "POLD1", "POLE", "GART", "ATIC", "PPAT", "NR3C1"}
# The project's existing leads (reports/Ranked leads and research partners.md).
EXISTING = {
    "IL1A": "IL-1 after surgery (lead 1)", "IL1B": "IL-1 after surgery (lead 1)",
    "IL1R1": "IL-1 after surgery (lead 1)", "IL6": "IL-6 after surgery (lead 1)",
    "IL6R": "IL-6 after surgery (lead 1)", "IL6ST": "IL-6 after surgery (lead 1)",
    "CXCR1": "CXCR1/2 (lead 8)", "CXCR2": "CXCR1/2 (lead 8)",
    "CXCL8": "CXCR1/2 (lead 8)", "PTK2": "FAK (lead 4)", "DKK1": "DKK1 (lead 4)",
    "LPAR1": "platelets/LPAR1 (lung metastasis report)",
    "PTGS1": "aspirin/platelets (lead 9)", "P2RY12": "platelets (lead 9)",
    "ITGA2B": "platelets (lead 9)", "ITGB3": "platelets (lead 9)",
    "F2R": "platelets (lead 9)", "F10": "anticoagulant (lead 9)",
    "F2": "anticoagulant (lead 9)",
}
# Hand review of high-scoring genes (November 19, 2026). A gene listed here
# is removed from the shortlist for the stated reason; it stays in the CSV with
# the reason in review_note. Categories: dead end, class already trialled,
# drug not available, wrong direction, annotation artefact, previously dropped.
REVIEW = {
    "CD4": "annotation artefact: papers are about CD4+ T cells and RNA comes from infiltrating immune cells; ibalizumab only blocks HIV entry",
    "KEAP1": "wrong direction: dimethyl fumarate inhibits KEAP1 and so activates NRF2, which protects tumour cells from chemotherapy",
    "NFE2L2": "wrong direction: the drugs activate NRF2",
    "TGFB1": "annotation artefact: luspatercept traps activin/GDF11, not TGF-beta1; no approved TGF-beta1 blocker",
    "TGFB3": "annotation artefact: luspatercept traps activin/GDF11, not TGF-beta3",
    "TGFB2": "annotation artefact: luspatercept traps activin/GDF11, not TGF-beta2",
    "RELA": "drug not available: edasalonexent failed phase 3 in Duchenne dystrophy and is not marketed",
    "NFKB1": "drug not available: edasalonexent failed phase 3 and is not marketed",
    "NFKB2": "drug not available: edasalonexent failed phase 3 and is not marketed",
    "FN1": "drug not available: L19-IL2 is a phase 3 immunocytokine that uses fibronectin only as an address",
    "MMP2": "dead end: MMP inhibitors (marimastat and others) failed phase 3 trials across cancers in 1997-2002",
    "MMP9": "dead end: MMP inhibitors failed phase 3 trials across cancers",
    "MMP13": "dead end: MMP inhibition failed across cancers; doxycycline is a weak, non-selective MMP inhibitor",
    "MMP1": "dead end: MMP inhibition failed across cancers",
    "MMP7": "dead end: MMP inhibition failed across cancers",
    "ITGAV": "overlaps the platelet lead: abciximab is a platelet GPIIb/IIIa blocker; the alphav integrin blocker cilengitide failed in glioblastoma",
    "MDM2": "previously dropped by this project: rests on one cell line and needs wild-type TP53",
    "TP53": "previously dropped (MDM2): TP53 is credited only through MDM2-p53 interaction blockers",
    "AKT2": "merged with AKT1 (same drug, capivasertib)",
    "ROCK1": "merged with ROCK2 (same drugs); ROCK1 carries a high paper-mill risk flag",
    "EPHA2": "already in osteosarcoma development as a surface target (see the surface-target report); dasatinib is SRC-class and already trialled",
    "MCL1": "drug not available: obatoclax was discontinued",
    "GSR": "annotation artefact: carmustine is an alkylating chemotherapy",
    "CCND1": "class already trialled: palbociclib (CDK4/6) has 14 osteosarcoma trials",
    "EPHB2": "class already trialled: vandetanib is a VEGFR multi-kinase inhibitor",
    "PIK3CB": "class already trialled: PI3K inhibitors (samotolisib, copanlisib) and mTOR inhibitors are in osteosarcoma trials",
    "PIK3R1": "class already trialled: PI3K inhibitors",
    "PIK3CD": "class already trialled: PI3K inhibitors",
    "CTSK": "drug not available: odanacatib was abandoned over stroke risk",
    "TFRC": "annotation artefact: pabinafusp alfa uses the transferrin receptor to carry an enzyme into the brain",
    "LRP1": "annotation artefact: ANG1005 uses LRP1 as a carrier",
    "P4HB": "annotation artefact: lomitapide inhibits microsomal triglyceride transfer protein, of which P4HB is a subunit",
    "FGFR3": "class already trialled: FGFR inhibitors (erdafitinib) and multi-kinase pills",
    "FGFR2": "class already trialled: FGFR inhibitors (erdafitinib)",
    "ODC1": "already being tested: DFMO trial in Ewing sarcoma and osteosarcoma (NCT07321912)",
    "PSMD14": "annotation artefact and class trialled: proteasome inhibitors (bortezomib, ixazomib) are in sarcoma trials",
    "APP": "dead end: amyloid antibodies",
    "AXL": "class already trialled: cabozantinib blocks AXL",
    "CCN2": "drug not available: pamrevlumab failed phase 3; CTGF literature carries a high paper-mill flag",
    "IFNG": "wrong direction: emapalumab neutralises interferon-gamma, which supports anti-tumour immunity",
    "CD86": "wrong direction: abatacept suppresses T-cell activation",
    "CD80": "wrong direction: abatacept suppresses T-cell activation",
    "ITGB2": "dead end: lifitegrast is an eye drop",
    "ENG": "drug not available: carotuximab failed phase 3 in angiosarcoma",
    "SMO": "already tested: vismodegib trial included osteosarcoma (NCT01154452)",
    "HDAC1": "class already trialled: HDAC inhibitors", "HDAC2": "class already trialled: HDAC inhibitors",
    "HDAC3": "class already trialled: HDAC inhibitors", "HDAC6": "class already trialled: HDAC inhibitors",
    "HDAC9": "class already trialled: HDAC inhibitors", "HDAC4": "class already trialled: HDAC inhibitors",
    "XPO1": "already tested: selinexor trials include osteosarcoma",
    "RAF1": "class already trialled: sorafenib/regorafenib",
    "CA2": "thin evidence: 5 papers; topiramate is a weak carbonic anhydrase inhibitor",
    "IMPDH2": "annotation artefact: thioguanine is antimetabolite chemotherapy; 5 papers",
    "ANGPT2": "dead end: faricimab is given into the eye",
    "HBB": "dead end: efaproxiral (radiation sensitiser) was abandoned",
    "HSPA1A": "drug not available: CD24Fc", "HSPA1B": "drug not available: CD24Fc",
    "HMGB1": "drug not available: CD24Fc; high paper-mill flag",
    "E2F1": "drug not available: edifoligide failed", "E2F4": "drug not available: edifoligide failed",
    "PTH1R": "wrong direction: teriparatide and abaloparatide activate PTH1R and caused osteosarcoma in rats; they carried a boxed warning for it",
    "CDK5": "drug not available: dinaciclib is not approved; CDK9 inhibitor alvocidib already trialled",
    "AURKB": "drug not available; aurora kinase A inhibitor alisertib already trialled",
    "DNMT1": "class already trialled: azacitidine/decitabine", "DNMT3A": "class already trialled: azacitidine/decitabine",
    "EZH2": "already tested: tazemetostat basket trial", "KDM1A": "already tested: seclidemstat trial",
    "PTGS2": "already tested: celecoxib trials", "CD47": "already tested: magrolimab trial",
    "DDB1": "class already trialled: thalidomide analogues",
    "VWF": "dead end: caplacizumab blocks von Willebrand factor to treat a clotting disorder; overlaps the platelet lead",
    "PLAT": "dead end: aminocaproic acid is an antifibrinolytic for bleeding",
    "IL6ST": "existing lead (IL-6): satralizumab and the IL-6 receptor",
    "MAPK14": "drug not available: no p38 inhibitor is approved (ARRY-797 failed phase 3)",
    "HAVCR2": "drug not available: sabatolimab (TIM-3) failed phase 3 in myelodysplasia",
    "BRD4": "drug not available: apabetalone is a cardiovascular BD2-selective agent, not an anti-cancer BET inhibitor",
    "ITGA5": "drug not available: volociximab", "PLK1": "drug not available: volasertib discontinued",
    "BCL2L1": "drug not available: navitoclax is not approved; BCL-xL inhibition causes dose-limiting low platelets",
    "BCL2": "RNA argues against: median 4 TPM, expressed in 39% of tumours; 59% of its papers are cell-line-only or microRNA-type",
    "MEN1": "thin evidence: 6 papers; menin inhibitors act on KMT2A-rearranged leukaemia",
    "EDNRA": "thin evidence: 8 papers",
}

INHIBIT = re.compile(r"INHIBITOR|ANTAGONIST|BLOCKER|NEGATIVE|INVERSE|ANTISENSE|"
                     r"DEGRADER|DISRUPTING|BINDING AGENT|CROSS-LINKING|SEQUESTERING",
                     re.I)
SYN_TYPES = {"INN", "USAN", "BAN", "FDA", "TRADE_NAME", "ATC", "JAN", "USP",
             "BNF", "MERCK_INDEX", "OTHER", "RESEARCH_CODE", "DCF", "INCI"}


# ----------------------------------------------------------------- helpers
def get_json(url, params=None, retries=5, timeout=180):
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001 - network flakiness is expected
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"GET failed: {url[:200]} :: {last}")


def cache(name):
    return os.path.join(RAW, name)


def chembl_all(endpoint, params, key):
    """Page through a ChEMBL list endpoint (limit 1000)."""
    out, offset = [], 0
    while True:
        p = dict(params, limit=1000, offset=offset, format="json")
        d = get_json(f"{CHEMBL}/{endpoint}.json", p)
        out.extend(d[key])
        total = d["page_meta"]["total_count"]
        offset += 1000
        print(f"[chembl] {endpoint} {min(offset, total)}/{total}")
        if offset >= total:
            return out
        time.sleep(0.3)


def f(x, c):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return 0.0
    return min(1.0, math.log1p(max(x, 0.0)) / math.log1p(c))


def num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


# ----------------------------------------------------------- stage: ChEMBL
MOL_FIELDS = ("molecule_chembl_id,pref_name,max_phase,oral,parenteral,topical,"
              "black_box_warning,withdrawn_flag,first_approval,molecule_type,"
              "molecule_synonyms,therapeutic_flag,molecule_hierarchy,"
              "atc_classifications,veterinary")


def stage_chembl():
    """Approved (max_phase 4) and phase 3 molecules, all mechanisms, and the
    human targets those mechanisms name. Raw JSON cached in data/repurposing_raw."""
    for phase in ("4", "3"):
        path = cache(f"chembl_molecules_phase{phase}.json")
        if not os.path.exists(path):
            mols = chembl_all("molecule", {"max_phase": phase, "only": MOL_FIELDS},
                              "molecules")
            json.dump(mols, open(path, "w"))
    path = cache("chembl_mechanisms.json")
    if not os.path.exists(path):
        json.dump(chembl_all("mechanism", {}, "mechanisms"), open(path, "w"))
    mechs = json.load(open(path))
    tids = sorted({m["target_chembl_id"] for m in mechs if m.get("target_chembl_id")})
    path = cache("chembl_targets.json")
    have = json.load(open(path)) if os.path.exists(path) else {}
    todo = [t for t in tids if t not in have]
    for i in range(0, len(todo), 40):
        chunk = todo[i:i + 40]
        d = get_json(f"{CHEMBL}/target.json", {
            "target_chembl_id__in": ",".join(chunk), "limit": 100, "format": "json",
            "only": "target_chembl_id,pref_name,target_type,organism,target_components"})
        for t in d["targets"]:
            comps = []
            for c in t.get("target_components") or []:
                sym = [s["component_synonym"] for s in c.get("target_component_synonyms") or []
                       if s.get("syn_type") == "GENE_SYMBOL"]
                comps.append({"accession": c.get("accession"), "symbols": sym,
                              "description": c.get("component_description")})
            have[t["target_chembl_id"]] = {
                "pref_name": t.get("pref_name"), "target_type": t.get("target_type"),
                "organism": t.get("organism"), "components": comps}
        print(f"[chembl] targets {min(i + 40, len(todo))}/{len(todo)}")
        json.dump(have, open(path, "w"))
        time.sleep(0.3)
    print(f"[chembl] {len(mechs)} mechanisms, {len(have)} targets cached")


# ------------------------------------------------------------ stage: build
# Mechanisms that do not act on the target protein pharmacologically
# (vaccines, replacement enzymes, enzymes that digest collagen or clots, ...).
SKIP_ACTIONS = {"VACCINE ANTIGEN", "EXOGENOUS PROTEIN", "EXOGENOUS GENE",
                "SUBSTRATE", "HYDROLYTIC ENZYME", "PROTEOLYTIC ENZYME",
                "OXIDATIVE ENZYME", "REDUCING AGENT"}
# Fusion-protein targets (e.g. CD74-ROS1) would credit the partner gene.
SKIP_TARGET_TYPES = {"CHIMERIC PROTEIN"}
DIAGNOSTIC = re.compile(r"technetium|indium in|gallium ga|tc[ -]?99m|\bf[ -]?18\b|"
                        r"zirconium|copper cu|florbeta|flortau|flutemetamol", re.I)
# Mutant-selective drugs that ChEMBL does not mark with a variant sequence.
MUTANT_ONLY = re.compile(r"mutant|G12C|G12D|V600|vorasidenib|ivosidenib|enasidenib|"
                         r"olutasidenib|sotorasib|adagrasib|divarasib", re.I)


def norm_tokens(text):
    return re.sub(r"[^a-z0-9\-]+", " ", (text or "").lower()).split()


def load_drugs():
    """{parent_chembl_id: drug dict} for max_phase 3-4 molecules."""
    mols = {}
    for phase in ("4", "3"):
        for m in json.load(open(cache(f"chembl_molecules_phase{phase}.json"))):
            mols[m["molecule_chembl_id"]] = m
    return mols


def drug_names(m):
    names = set()
    if m.get("pref_name"):
        names.add(m["pref_name"].lower())
    for s in m.get("molecule_synonyms") or []:
        if s.get("syn_type") in SYN_TYPES and s.get("molecule_synonym"):
            names.add(s["molecule_synonym"].lower())
    # Short names ("ATRA") and pure numbers cause false matches.
    return {n for n in names if len(n) >= 5 and not n.replace("-", "").isdigit()}


def stage_build():
    mols = load_drugs()
    mechs = json.load(open(cache("chembl_mechanisms.json")))
    targets = json.load(open(cache("chembl_targets.json")))
    drugs, gene_drugs = {}, {}
    for me in mechs:
        if (me.get("max_phase") or 0) < 3 or me.get("action_type") in SKIP_ACTIONS:
            continue
        t = targets.get(me.get("target_chembl_id") or "")
        if not t or t.get("organism") != "Homo sapiens":
            continue
        if t.get("target_type") in SKIP_TARGET_TYPES:
            continue
        pid = me.get("parent_molecule_chembl_id") or me["molecule_chembl_id"]
        m = mols.get(pid) or mols.get(me["molecule_chembl_id"])
        if not m or not m.get("pref_name"):
            continue
        # Imaging and diagnostic agents. ChEMBL sets therapeutic_flag only for
        # approved drugs (every phase 3 molecule reads False), so it is used
        # for max_phase 4 alone.
        if DIAGNOSTIC.search(m["pref_name"]) or (
                str(m.get("max_phase")).startswith("4") and m.get("therapeutic_flag") is False):
            continue
        d = drugs.setdefault(pid, {
            "chembl_id": pid, "name": m["pref_name"].lower(),
            "phase": int(float(m.get("max_phase") or me["max_phase"])),
            "oral": bool(m.get("oral")), "parenteral": bool(m.get("parenteral")),
            "topical": bool(m.get("topical")),
            "boxed_warning": bool(m.get("black_box_warning")),
            "withdrawn": bool(m.get("withdrawn_flag")),
            "first_approval": m.get("first_approval"),
            "type": m.get("molecule_type"), "names": sorted(drug_names(m)),
            "genes": set(), "mechanisms": set()})
        d["mechanisms"].add(me.get("mechanism_of_action") or "")
        comps = t["components"]
        for c in comps:
            if not c["symbols"]:
                continue
            g = c["symbols"][0].upper()
            d["genes"].add(g)
            # A mechanism with a variant_sequence acts on a mutant form only
            # (sotorasib on KRAS G12C, vorasidenib on mutant IDH1/2 ...).
            variant = bool(me.get("variant_sequence")) or bool(
                MUTANT_ONLY.search((me.get("mechanism_of_action") or "") + " " + m["pref_name"]))
            prev = gene_drugs.setdefault(g, {}).get(pid)
            if prev and not prev["variant_only"] and variant:
                continue
            gene_drugs[g][pid] = {
                "action": me.get("action_type") or "", "target_type": t["target_type"],
                "target_name": t["pref_name"], "n_components": len(comps),
                "variant_only": variant,
                "mechanism": me.get("mechanism_of_action") or ""}
    print(f"[build] {len(drugs)} phase 3-4 drugs with a human protein target; "
          f"{len(gene_drugs)} target genes")

    # --- local trial matching: n-gram lookup of every drug name over trial
    # title + interventions (osteosarcoma_trials.csv, interventional only).
    name_to_drug = {}
    for pid, d in drugs.items():
        for n in d["names"]:
            name_to_drug.setdefault(tuple(norm_tokens(n)), set()).add(pid)
    maxlen = max(len(k) for k in name_to_drug)
    curated = json.load(open(os.path.join(ROOT, "data", "drug_targets_curated.json")))
    curated.pop("_note", None)
    trial_hits = {}   # gene -> list of hits
    name_counts = {}
    for tr in csv.DictReader(open(os.path.join(ROOT, "data", "osteosarcoma_trials.csv"))):
        if tr["study_type"] not in ("INTERVENTIONAL", "EXPANDED_ACCESS"):
            continue
        title_toks = norm_tokens(tr["title"])
        title_set = " " + " ".join(title_toks) + " "
        toks = title_toks + ["|"] + norm_tokens(tr["interventions"])
        found = {}
        for i in range(len(toks)):
            for L in range(1, maxlen + 1):
                key = tuple(toks[i:i + L])
                if key in name_to_drug:
                    for pid in name_to_drug[key]:
                        found.setdefault(pid, " ".join(key))
        for pid, matched in found.items():
            d = drugs[pid]
            name_counts[matched] = name_counts.get(matched, 0) + 1
            in_title = any(" " + " ".join(norm_tokens(n)) + " " in title_set
                           for n in d["names"])
            for g in d["genes"]:
                trial_hits.setdefault(g, []).append({
                    "nct": tr["nct_id"], "scope": tr["scope"], "drug": d["name"],
                    "in_title": in_title, "n_drug_targets": len(d["mechanisms"]),
                    "source": "chembl-name"})
        blob = (tr["title"] + " " + tr["interventions"]).lower()
        for pat, genes in curated.items():
            if re.search(pat, blob):
                in_title = bool(re.search(pat, tr["title"].lower()))
                for g in genes:
                    trial_hits.setdefault(g, []).append({
                        "nct": tr["nct_id"], "scope": tr["scope"], "drug": pat,
                        "in_title": in_title, "n_drug_targets": len(genes),
                        "source": "curated-map"})
    json.dump(sorted(name_counts.items(), key=lambda x: -x[1]),
              open(cache("trial_name_matches.json"), "w"), indent=0)

    out = {"drugs": {k: dict(v, genes=sorted(v["genes"]), mechanisms=sorted(v["mechanisms"]))
                     for k, v in drugs.items()},
           "gene_drugs": gene_drugs, "trial_hits": trial_hits}
    json.dump(out, open(cache("build.json"), "w"))
    print(f"[build] {len(trial_hits)} genes hit by a drug in an osteosarcoma trial; "
          f"{len(name_counts)} distinct drug names matched")


# ------------------------------------------------------------ scoring core
def load_context():
    ev = {r["gene"].upper(): r for r in
          csv.DictReader(open(os.path.join(ROOT, "data", "osteosarcoma_gene_evidence.csv")))}
    risk = {r["gene"].upper(): r for r in
            csv.DictReader(open(os.path.join(ROOT, "data", "osteosarcoma_evidence_risk_genes.csv")))}
    tum = {}
    for t in json.load(open(os.path.join(ROOT, "data", "surface_targets_raw", "tumour_summary.json"))):
        # keep the higher-expressed copy when a symbol appears twice
        if t["symbol"].upper() not in tum or t["tumour_median_tpm"] > tum[t["symbol"].upper()]["tumour_median_tpm"]:
            tum[t["symbol"].upper()] = t
    gtex = {}
    gp = os.path.join(ROOT, "data", "surface_targets_raw", "gtex_medians.json")
    ip = os.path.join(ROOT, "data", "surface_targets_raw", "gtex_gencode_ids.json")
    if os.path.exists(gp) and os.path.exists(ip):
        med, ids = json.load(open(gp)), json.load(open(ip))
        for sym, gid in ids.items():
            if gid in med and med[gid]:
                vals = sorted(med[gid].values())
                gtex[sym.upper()] = (vals[len(vals) // 2], max(med[gid].items(), key=lambda x: x[1]))
    trials = {r["nct_id"]: r for r in
              csv.DictReader(open(os.path.join(ROOT, "data", "osteosarcoma_trials.csv")))}
    return ev, risk, tum, gtex, trials


def drug_rank_key(d, info, paed):
    """Best drug for a gene: not withdrawn, acts on the wild-type protein,
    inhibits rather than activates, approved, oral, no boxed warning, most
    paediatric trial experience."""
    return (not d["withdrawn"], not info["variant_only"],
            bool(INHIBIT.search(info["action"])), d["phase"],
            d["oral"], not d["boxed_warning"], paed.get(d["chembl_id"], 0) or 0)


def untested_grade(hits):
    if not hits:
        return 20, "none"
    direct = [h for h in hits if h["in_title"] and h["n_drug_targets"] <= 3]
    if any(h["scope"] in ("os_only", "bone_sarcoma") for h in direct):
        return 0, "named in title of an osteosarcoma/bone-sarcoma trial"
    if direct:
        return 6, "named in title of a basket trial that includes osteosarcoma"
    return 10, "indirect (multi-target drug, or listed but not named in title)"


def score_genes(ctg=None):
    ctg = ctg or {}
    paed = ctg.get("paed", {})
    ctg_hits = ctg.get("os_hits", {})
    b = json.load(open(cache("build.json")))
    drugs, gene_drugs, trial_hits = b["drugs"], b["gene_drugs"], b["trial_hits"]
    ev, risk, tum, gtex, _ = load_context()
    pp = cache("pubmed_drug_counts.json")
    pubmed = json.load(open(pp)) if os.path.exists(pp) else {}
    rows = []
    for g, dd in gene_drugs.items():
        cand = [(drugs[pid], info) for pid, info in dd.items() if pid in drugs]
        cand = [c for c in cand if not c[0]["withdrawn"]] or cand
        cand.sort(key=lambda c: drug_rank_key(c[0], c[1], paed), reverse=True)
        best, binfo = cand[0]
        e, r, t = ev.get(g, {}), risk.get(g, {}), tum.get(g)
        # ---- EVIDENCE
        q = 1 - 0.5 * num(e.get("pct_cell_only_or_ncrna")) / 100
        rf = {"high": 0.5, "elevated": 0.75}.get(r.get("risk", ""), 1.0)
        E = (12 * f(e.get("in_vivo"), 40) + 10 * f(e.get("patients"), 40)
             + 3 * f(e.get("dog"), 5) + 5 * f(e.get("papers"), 100)) * q * rf
        # ---- EXPRESSION
        med = t["tumour_median_tpm"] if t else 0.0
        pct = t["pct_tumours_expressing"] if t else 0.0
        X = 25 * f(med, 50) * pct / 100
        # ---- DRUG LITERATURE (alternative evidence route)
        dp, dpn = 0, ""
        for dr, _ in cand:
            cn = clean_name(dr["name"])
            if len(dr["mechanisms"]) <= 3 and cn not in ENDOGENOUS:
                c = pubmed.get(cn, 0)
                if c > dp:
                    dp, dpn = c, dr["name"]
        E = max(E, 20 * f(dp, 30))
        # ---- DRUGGABLE
        pc = paed.get(best["chembl_id"])
        P = 0 if not pc else (5 if pc >= 5 else 3)
        D = (10 if best["phase"] >= 4 else 6) + (5 if best["oral"] else 0) + P \
            + (2 if best["boxed_warning"] else 5)
        # ---- UNTESTED
        hits = trial_hits.get(g, []) + ctg_hits.get(g, [])
        U, ulabel = untested_grade(hits)
        dirf = 1.0 if INHIBIT.search(binfo["action"]) else 0.75
        total = (E + X + D + U) * dirf
        excl = []
        if g in HEAVY:
            excl.append("heavily trialled class")
        if g in CHEMO or g.startswith(CHEMO_PREFIX):
            excl.append("cytotoxic chemotherapy / steroid target")
        if not e:
            excl.append("no osteosarcoma literature row (<5 papers)")
        if U == 0:
            excl.append("already named in an osteosarcoma trial")
        if binfo["variant_only"]:
            excl.append("drugs act only on a mutant form of the protein")
        gx = gtex.get(g)
        rows.append({
            "gene": g, "score": round(total, 1), "evidence_pts": round(E, 1),
            "expression_pts": round(X, 1), "druggable_pts": D, "untested_pts": U,
            "direction_factor": dirf,
            "tumour_median_tpm": round(med, 1), "pct_tumours_expressing": pct,
            "gtex_median_tpm_all_tissues": round(gx[0], 1) if gx else "",
            "gtex_highest_tissue": f"{gx[1][0]} ({gx[1][1]:.0f})" if gx else "",
            "os_papers": e.get("papers", 0), "in_vivo": e.get("in_vivo", 0),
            "patients": e.get("patients", 0), "dog": e.get("dog", 0),
            "pct_cell_only_or_ncrna": e.get("pct_cell_only_or_ncrna", ""),
            "retracted": e.get("retracted", ""), "risk_flag": r.get("risk", ""),
            "nih_grants": e.get("nih_grants", 0),
            "drug_os_papers": dp, "drug_os_papers_drug": dpn,
            "best_drug": best["name"], "best_drug_phase": best["phase"],
            "best_drug_action": binfo["action"], "best_drug_oral": best["oral"],
            "best_drug_boxed_warning": best["boxed_warning"],
            "best_drug_first_approval": best["first_approval"] or "",
            "best_drug_paediatric_trials": "" if pc is None else pc,
            "best_drug_mechanism": binfo["mechanism"],
            "chembl_target": binfo["target_name"], "chembl_target_type": binfo["target_type"],
            "n_drugs": len(cand),
            "other_drugs": "; ".join(c[0]["name"] for c in cand[1:8]),
            "os_trial_status": ulabel,
            "os_trials": " ".join(sorted({h["nct"] for h in hits})),
            "os_trial_drugs": "; ".join(sorted({h["drug"] for h in hits}))[:200],
            "existing_lead": EXISTING.get(g, ""),
            "excluded": "; ".join(excl),
        })
    rows.sort(key=lambda r: -r["score"])
    return rows, drugs, gene_drugs


# ------------------------------------------------------------ stage: ctgov
OS_COND = re.compile(r"osteosarcoma|osteogenic|bone (sarcoma|cancer|tumou?r|neoplasm)", re.I)


def ctgov_drug(d, local_trials):
    """Osteosarcoma trials naming this drug, and interventional trials of the
    drug that enrol children. Both from ClinicalTrials.gov API v2."""
    res = {"os_hits": [], "paed": None}
    names = [tuple(norm_tokens(n)) for n in d["names"]] or [tuple(norm_tokens(d["name"]))]
    try:
        data = get_json(CTGOV, {
            "query.cond": "osteosarcoma", "query.intr": d["name"], "pageSize": 100,
            "fields": "NCTId,BriefTitle,OverallStatus,Phase,StudyType,InterventionName,Condition"})
    except RuntimeError as e:
        print(f"[ctgov] {d['name']}: {e}")
        data = {"studies": []}
    for s in data.get("studies", []):
        p = s.get("protocolSection", {})
        nct = p.get("identificationModule", {}).get("nctId", "")
        title = p.get("identificationModule", {}).get("briefTitle", "")
        inames = " | ".join(i.get("name", "") for i in
                            p.get("armsInterventionsModule", {}).get("interventions", []) or [])
        conds = p.get("conditionsModule", {}).get("conditions", []) or []
        stype = p.get("designModule", {}).get("studyType", "")
        if stype not in ("INTERVENTIONAL", "EXPANDED_ACCESS"):
            continue
        tt = " " + " ".join(norm_tokens(title)) + " "
        it = " " + " ".join(norm_tokens(inames)) + " "
        named = [n for n in names if n and " " + " ".join(n) + " " in it + tt]
        if not named:
            continue  # the API's fuzzy match, not this drug
        if nct in local_trials:
            scope = local_trials[nct]["scope"]
        else:
            scope = "os_only" if conds and all(OS_COND.search(c) for c in conds) else "basket"
        res["os_hits"].append({
            "nct": nct, "scope": scope, "drug": d["name"],
            "in_title": any(" " + " ".join(n) + " " in tt for n in named),
            "n_drug_targets": len(d["mechanisms"]), "source": "ctgov-api",
            "title": title[:160], "status": p.get("statusModule", {}).get("overallStatus", ""),
            "phase": ";".join(p.get("designModule", {}).get("phases", []) or [])})
    time.sleep(0.25)
    try:
        c = get_json(CTGOV, {
            "query.intr": d["name"], "countTotal": "true", "pageSize": 1,
            "filter.advanced": "AREA[StdAge]CHILD AND AREA[StudyType]INTERVENTIONAL",
            "fields": "NCTId"})
        res["paed"] = c.get("totalCount", 0)
    except RuntimeError as e:
        print(f"[ctgov] paed {d['name']}: {e}")
    time.sleep(0.25)
    return res


def stage_ctgov(n=N_CTGOV):
    # Uses any ClinicalTrials.gov results already cached, so a second run
    # checks the genes that moved up once the first run demoted others.
    rows, drugs, gene_drugs = score_genes(load_ctgov())
    _, _, _, _, local_trials = load_context()
    hard = ("heavily trialled", "cytotoxic", "no osteosarcoma literature", "mutant form")
    picks = [r["gene"] for r in rows if not any(h in r["excluded"] for h in hard)
             and r["gene"] not in REVIEW][:n]
    picks += [g for g in EXISTING if g in gene_drugs and g not in picks]
    path = cache("ctgov_drugs.json")
    done = json.load(open(path)) if os.path.exists(path) else {}
    for i, g in enumerate(picks):
        cand = sorted(((drugs[p], info) for p, info in gene_drugs[g].items() if p in drugs),
                      key=lambda c: drug_rank_key(c[0], c[1], {}), reverse=True)
        for d, _ in cand[:DRUGS_PER_GENE]:
            if d["chembl_id"] in done:
                continue
            done[d["chembl_id"]] = ctgov_drug(d, local_trials)
            json.dump(done, open(path, "w"))
        print(f"[ctgov] {i + 1}/{len(picks)} {g}")
    print(f"[ctgov] {len(done)} drugs checked")


def load_ctgov():
    path = cache("ctgov_drugs.json")
    if not os.path.exists(path):
        return {}
    done = json.load(open(path))
    b = json.load(open(cache("build.json")))
    os_hits = {}
    for pid, res in done.items():
        for g in b["drugs"].get(pid, {}).get("genes", []):
            os_hits.setdefault(g, []).extend(res["os_hits"])
    return {"paed": {pid: res["paed"] for pid, res in done.items()}, "os_hits": os_hits}


# ----------------------------------------------------------- stage: pubmed
# Gene tagging misses papers that name only the drug ("propranolol inhibits
# osteosarcoma ..."), so every candidate drug also gets a PubMed count.
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
SALT = re.compile(r"\b(anhydrous|hydrochloride|dihydrochloride|hcl|sodium|potassium|"
                  r"calcium|citrate|mesylate|maleate|tosylate|tartrate|fumarate|succinate|"
                  r"phosphate|sulfate|acetate|besylate|malate|bromide|chloride|"
                  r"monohydrate|hydrate|dimesylate|hemifumarate|etexilate|s-malate)\b", re.I)


def clean_name(name):
    c = re.sub(r"\s+", " ", SALT.sub("", name)).strip()
    # "dimethyl fumarate" must not shrink to "dimethyl".
    return name if c in ("dimethyl", "monomethyl", "") or len(c) < 4 else c


# Endogenous substances: an osteosarcoma paper naming adenosine, estradiol or
# dopamine is almost never about the drug, so these get no drug-literature credit.
ENDOGENOUS = {
    "adenosine", "estradiol", "estrone", "calcitonin", "caffeine", "dopamine",
    "capsaicin", "angiotensin ii", "ferric", "acetylcholine", "glucagon",
    "epinephrine", "norepinephrine", "cortisone", "hydrocortisone", "corticotropin",
    "histamine", "serotonin", "testosterone", "progesterone", "insulin", "heparin",
    "glutamine", "arginine", "zinc", "cholesterol", "glucose", "dextrose", "oxygen",
    "nitric oxide", "hydrogen peroxide", "hyaluronic acid", "aminolevulinic acid",
    "levothyroxine", "liothyronine", "somatostatin", "oxytocin", "vasopressin",
    "thrombin", "ethanol", "iron", "copper", "magnesium", "potassium", "calcium",
}


def stage_pubmed():
    b = json.load(open(cache("build.json")))
    path = cache("pubmed_drug_counts.json")
    done = json.load(open(path)) if os.path.exists(path) else {}
    names = sorted({clean_name(d["name"]) for d in b["drugs"].values()} - set(done))
    for i, n in enumerate(names):
        if len(n) < 4:
            continue
        try:
            d = get_json(EUTILS, {"db": "pubmed", "retmode": "json", "rettype": "count",
                                  "term": f'osteosarcoma[tiab] AND "{n}"[tiab]'})
            done[n] = int(d["esearchresult"]["count"])
        except (RuntimeError, KeyError, ValueError) as e:
            print(f"[pubmed] {n}: {e}")
        time.sleep(0.36)
        if i % 100 == 0:
            json.dump(done, open(path, "w"))
            print(f"[pubmed] {i}/{len(names)}")
    json.dump(done, open(path, "w"))
    print(f"[pubmed] {len(done)} drug counts cached")


# -------------------------------------------------------- stage: abstracts
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def stage_abstracts(queries):
    """Cache Europe PMC abstracts for hand reading. `queries` maps a label to
    a Europe PMC query string. Results go to data/repurposing_raw/abstracts_<label>.json
    and are read by a person; nothing is scored from them."""
    for label, q in queries.items():
        path = cache(f"abstracts_{label}.json")
        if os.path.exists(path):
            continue
        d = get_json(EPMC, {"query": q, "format": "json", "resultType": "core",
                            "pageSize": 100, "sort": "CITED desc"})
        recs = [{"pmid": r.get("pmid"), "year": r.get("pubYear"), "title": r.get("title"),
                 "journal": (r.get("journalInfo") or {}).get("journal", {}).get("title"),
                 "cited": r.get("citedByCount"), "abstract": r.get("abstractText", ""),
                 "pubtype": "; ".join((r.get("pubTypeList") or {}).get("pubType", []))}
                for r in d.get("resultList", {}).get("result", [])]
        json.dump(recs, open(path, "w"), indent=0)
        print(f"[abstracts] {label}: {len(recs)} records")
        time.sleep(0.5)


# ------------------------------------------------------------- stage: score
CSV_FIELDS = [
    "shortlist_rank", "gene", "score", "evidence_pts", "expression_pts", "druggable_pts",
    "untested_pts", "direction_factor", "best_drug", "best_drug_phase", "best_drug_action",
    "best_drug_mechanism", "best_drug_oral", "best_drug_boxed_warning",
    "best_drug_first_approval", "best_drug_paediatric_trials", "other_drugs", "n_drugs",
    "chembl_target", "chembl_target_type", "tumour_median_tpm", "pct_tumours_expressing",
    "gtex_median_tpm_all_tissues", "gtex_highest_tissue", "os_papers", "in_vivo",
    "patients", "dog", "pct_cell_only_or_ncrna", "retracted", "risk_flag", "nih_grants",
    "drug_os_papers", "drug_os_papers_drug", "os_trial_status", "os_trials",
    "os_trial_drugs", "existing_lead", "excluded", "review_note",
]


def eligible(r):
    lit = (num(r["os_papers"]) >= 10 and num(r["in_vivo"]) >= 3) or r["drug_os_papers"] >= 5
    return lit and not r["excluded"] and not r["existing_lead"] and not r["review_note"]


def stage_score(n_short=20):
    rows, _, _ = score_genes(load_ctgov())
    rank = 0
    for r in rows:
        r["review_note"] = REVIEW.get(r["gene"], "")
        r["shortlist_rank"] = ""
        if rank < n_short and eligible(r):
            rank += 1
            r["shortlist_rank"] = rank
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"[score] wrote {len(rows)} genes to {os.path.relpath(OUT_CSV, ROOT)}")
    print(f"{'#':>3} {'gene':<9}{'score':>6} {'E':>5} {'X':>5} {'D':>3} {'U':>3}  drug")
    for r in rows:
        if r["shortlist_rank"]:
            print(f"{r['shortlist_rank']:>3} {r['gene']:<9}{r['score']:>6} {r['evidence_pts']:>5} "
                  f"{r['expression_pts']:>5} {r['druggable_pts']:>3} {r['untested_pts']:>3}  "
                  f"{r['best_drug']} (phase {r['best_drug_phase']}; drug papers "
                  f"{r['drug_os_papers']}; trials: {r['os_trial_status']})")
    print("\nExisting project leads:")
    for r in rows:
        if r["existing_lead"]:
            print(f"    {r['gene']:<9}{r['score']:>6}  {r['best_drug']}  [{r['existing_lead']}]")


STAGES = {"chembl": stage_chembl, "build": stage_build, "ctgov": stage_ctgov,
          "pubmed": stage_pubmed, "score": stage_score}


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "all":
        for name in ("chembl", "build", "pubmed", "ctgov", "ctgov", "score"):
            STAGES[name]()
    elif arg in STAGES:
        STAGES[arg]()
    else:
        sys.exit(f"unknown stage {arg}; choose from {', '.join(STAGES)} or all")
