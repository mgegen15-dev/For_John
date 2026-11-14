"""Score every gene named in the osteosarcoma literature by the kind of
evidence behind it, and link it to registered trials and NIH grants.

Inputs: data/literature/osteosarcoma_pubtator.jsonl (literature_fetch.py),
data/osteosarcoma_trials.csv, data/drug_targets_curated.json,
data/nih_osteosarcoma_projects.csv.
Outputs: data/osteosarcoma_gene_evidence.csv (one row per gene) and
data/osteosarcoma_paper_tags.csv (one row per paper), plus a JSON summary.

Paper tags (regex on title + abstract, approximate):
  cell_only  - osteosarcoma cell lines, no animal, patient or dog data
  in_vivo    - mice, rats, xenografts or other in vivo work
  patients   - human tumour samples or patient cohorts
  dog        - canine osteosarcoma
  ncrna      - microRNA / lncRNA / circRNA paper (a genre heavily affected
               by paper mills in this field)
  retracted / review - from PubMed publication types

Gene-name corrections (CORRECTIONS below). PubTator3 normalises some common
osteosarcoma abbreviations to the wrong gene. An audit of mention texts
(November 2026) found these, and they reached headline lists, so they are
corrected here by the mention text PubTator recorded, not by symbol alone:
  "protein kinase B"/"PKB" tagged PTK2B -> AKT1 ("Pyk2"/"PTK2B" stay PTK2B)
  "p21" tagged H3P16 (a histone pseudogene) -> CDKN1A
  "MET"/"Met/HGF receptor" tagged SLTM -> MET ("methionine" dropped)
  "COX-2"/"cyclooxygenase-2" tagged COX2 (mitochondrial MT-CO2) -> PTGS2
  "P-gp"/"Pgp"/"P-glycoprotein" tagged PGP (phosphoglycolate phosphatase) -> ABCB1
  "p53" tagged TRP53-PS (a mouse pseudogene) -> TP53
  "tyrosine kinase"/"TK" tagged TXK -> dropped (generic term)
  "TNM" tagged TENM1 -> dropped (tumour staging, not teneurin-1)
  "hsa"/"hsa-" tagged ALB -> dropped (microRNA species prefix)
  "BMP"/"bone morphogenetic protein" tagged BMP1 -> dropped (generic family name)
Any other mention of these symbols is kept as PubTator gave it. The map is
not exhaustive: it covers the cases found by checking mention texts of
suspicious genes, so other mis-normalisations can remain.

The animal-data regex ignores the gene name "murine double minute" (MDM2),
which otherwise tagged MDM2 papers as having in vivo data.

Run from the repository root: python3 tools/literature_map.py"""
import csv, json, re, collections as C

L = "data/literature/"
retr = set(open(L + "osteosarcoma_retracted_pmids.txt").read().split())  # unique PMIDs
rev = set(open(L + "osteosarcoma_reviews_pmids.txt").read().split())
CELL = re.compile(r"\b(u-?2 ?os|mg-?63|saos-?2|143b|hos|sjsa-?1|khos|zos|lm7|cell lines?)\b", re.I)
VIVO = re.compile(r"\b(mice|mouse|murine|xenograft|nude|in vivo|rats?|zebrafish|orthotopic)\b", re.I)
PAT = re.compile(r"\b(patients?|tumou?r (tissues?|samples?|specimens?)|cohort|biops(y|ies))\b", re.I)
DOG = re.compile(r"\b(canine|dogs?)\b", re.I)
NC = re.compile(r"\b(mi[rR]-?\d|microrna|lncrna|long non-?coding|circrna|circ_|hsa_circ|non-?coding rna|sponge)", re.I)
ALIAS = {"TRP53": "TP53", "CDKN2A": "CDKN2A", "MKI67": "MKI67"}
NOT_ANIMAL = re.compile(r"murine double minute", re.I)  # MDM2's own name, not animal work
# (PubTator symbol, regex on the lower-cased mention text) -> corrected symbol, or None to drop.
# Rules are tried in order; the first match wins. Unmatched mentions keep PubTator's symbol.
CORRECTIONS = [
    ("PTK2B", r"^(protein kinase[- ]?b|pkb)$", "AKT1"),
    ("H3P16", r"^p ?21$", "CDKN1A"),
    ("SLTM", r"^(met|met/.*|mesenchymal epithelial transition factor)$", "MET"),
    ("SLTM", r"methionine|@", None),
    ("COX2", r"cox|cyclo-?oxygenase", "PTGS2"),
    ("PGP", r"^p- ?gp$|^pgp$|^p-g[l]?y?coproteins?$", "ABCB1"),
    ("TRP53-PS", r"^p ?-?53$", "TP53"),
    ("TXK", r"tyrosine[- ]kinase|^tk$|^tyk$|^trk$", None),
    ("TENM1", r"^tnm$", None),
    ("ALB", r"^hsa-?$", None),
    ("BMP1", r"^(bmp|bone morphogen(et)?ic proteins?)$", None),
]
CORRECTIONS = [(a, re.compile(b), c) for a, b, c in CORRECTIONS]
n_corrected = C.Counter()


def symbol(g):
    """Corrected gene symbol for one PubTator gene annotation [id, mention, symbol]."""
    s = (g[2] or "").upper()
    s = ALIAS.get(s, s)
    m = (g[1] or "").lower().strip()
    for sym, pat, new in CORRECTIONS:
        if s == sym and pat.search(m):
            n_corrected[(sym, new)] += 1
            return new or ""
    return s
GD2 = re.compile(r"\bGD2\b")

papers, genes = [], C.defaultdict(lambda: C.Counter())
first = {}
seen = set()
for line in open(L + "osteosarcoma_pubtator.jsonl"):
    d = json.loads(line)
    if d["pmid"] in seen:  # PubTator can return a paper twice
        continue
    seen.add(d["pmid"])
    txt = d["title"] + " " + d["abstract"]
    y = int(d["year"]) if str(d["year"] or "").isdigit() else None
    t = {"pmid": d["pmid"], "year": y, "retracted": d["pmid"] in retr, "review": d["pmid"] in rev,
         "ncrna": bool(NC.search(txt)), "in_vivo": bool(VIVO.search(NOT_ANIMAL.sub(" ", txt))),
         "patients": bool(PAT.search(txt)), "dog": bool(DOG.search(txt))}
    t["cell_only"] = bool(CELL.search(txt)) and not (t["in_vivo"] or t["patients"] or t["dog"])
    syms = {symbol(g) for g in d["genes"] if g[2]}
    if GD2.search(txt): syms.add("GD2")
    syms.discard("")
    t["genes"] = ";".join(sorted(syms))
    papers.append(t)
    if t["review"]: continue
    for s in syms:
        c = genes[s]
        c["papers"] += 1
        for k in ("retracted", "ncrna", "in_vivo", "patients", "dog", "cell_only"):
            c[k] += t[k]
        c["cell_only_or_ncrna"] += t["cell_only"] or t["ncrna"]  # union, not the sum of the two shares
        if y and y >= 2021: c["since_2021"] += 1
        if y: first[s] = min(first.get(s, 9999), y)

with open("data/osteosarcoma_paper_tags.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(papers[0])); w.writeheader(); w.writerows(papers)

# trials per target
dmap = json.load(open("data/drug_targets_curated.json")); dmap.pop("_note", None)
PH = {"EARLY_PHASE1": 0.5, "PHASE1": 1, "PHASE1/PHASE2": 1.5, "PHASE2": 2, "PHASE2/PHASE3": 2.5, "PHASE3": 3, "PHASE4": 4}
trials = C.defaultdict(set); best = {}
for r in csv.DictReader(open("data/osteosarcoma_trials.csv")):
    if r["study_type"] != "INTERVENTIONAL": continue
    iv = r["interventions"].lower() + " " + r["title"].lower()
    for pat, tg in dmap.items():
        if re.search(pat, iv):
            for g in tg:
                trials[g].add(r["nct_id"]); best[g] = max(best.get(g, 0), PH.get(r["phase"], 0))

# NIH grants (focused + substantial) naming the gene in the title
gr = [r for r in csv.DictReader(open("data/nih_osteosarcoma_projects.csv")) if r["tier"] != "incidental"]
# Grant titles often hyphenate ("IL-6", "DKK-1") or spell the name out, so allow an
# optional hyphen/space between letters and digits and add a few spelled-out names.
GRANT_NAMES = {"PTK2": ["focal adhesion kinase", "FAK"], "CXCL8": ["IL-?8", "interleukin-?8"],
               "IL6": ["interleukin-?6"], "CD276": ["B7-?H3"], "ERBB2": ["HER-?2"], "GD2": ["GD2"]}
def grants_for(sym):
    if len(sym) < 3: return 0
    pats = [re.sub(r"(?<=[A-Za-z])(?=\d)", "[- ]?", re.escape(sym))] + GRANT_NAMES.get(sym, [])
    p = re.compile(r"\b(" + "|".join(pats) + r")\b", re.I)
    return len({r["project_num"][1:12] for r in gr if p.search(r["title"])})

rows = []
for s, c in genes.items():
    if c["papers"] < 5: continue
    n = c["papers"]
    rows.append({"gene": s, "papers": n, "first_year": first.get(s, ""), "since_2021": c["since_2021"],
                 "pct_cell_only": round(100 * c["cell_only"] / n), "pct_ncrna": round(100 * c["ncrna"] / n),
                 "pct_cell_only_or_ncrna": round(100 * c["cell_only_or_ncrna"] / n),
                 "retracted": c["retracted"], "in_vivo": c["in_vivo"], "patients": c["patients"], "dog": c["dog"],
                 "trials": len(trials.get(s, ())), "best_phase": best.get(s, 0), "nih_grants": grants_for(s),
                 "trial_ids": " ".join(sorted(trials.get(s, ())))[:400]})
rows.sort(key=lambda r: (-r["papers"], r["gene"]))
with open("data/osteosarcoma_gene_evidence.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

P = [p for p in papers if not p["review"]]
PERIODS = [(1900, 1999), (2000, 2004), (2005, 2009), (2010, 2014), (2015, 2019), (2020, 2024), (2025, 2027)]  # 2027 = a few papers dated ahead of print
per = []
for a, b in PERIODS:
    pp = [p for p in P if p["year"] and a <= p["year"] <= b]
    per.append({"years": f"{a}-{b}" if a > 1900 else "before 2000", "research_papers": len(pp),
                "ncrna_papers": sum(p["ncrna"] for p in pp),
                "pct_ncrna": round(100 * sum(p["ncrna"] for p in pp) / len(pp), 1) if pp else 0,
                "retracted": sum(p["retracted"] for p in pp),
                "retracted_ncrna": sum(p["retracted"] and p["ncrna"] for p in pp),
                "cell_line_only": sum(p["cell_only"] for p in pp)})
per.append({"years": "no year", "research_papers": sum(1 for p in P if not p["year"]), "ncrna_papers": "",
            "pct_ncrna": "", "retracted": sum(p["retracted"] for p in P if not p["year"]),
            "retracted_ncrna": "", "cell_line_only": ""})
with open("data/osteosarcoma_literature_periods.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(per[0])); w.writeheader(); w.writerows(per)

s10 = [p for p in P if p["year"] and p["year"] >= 2010]
nc = [p for p in s10 if p["ncrna"]]; ot = [p for p in s10 if not p["ncrna"]]
rn, ro = sum(p["retracted"] for p in nc) / len(nc), sum(p["retracted"] for p in ot) / len(ot)
G = {r["gene"]: r for r in rows}
weak = [r["gene"] for r in rows if r["papers"] >= 40 and genes[r["gene"]]["cell_only_or_ncrna"] / r["papers"] >= 0.6]
top_retr = sorted((r for r in rows if r["papers"] >= 20), key=lambda r: (-r["retracted"] / r["papers"], r["gene"]))[:10]
orph = [r["gene"] for r in rows if r["papers"] >= 30 and r["in_vivo"] >= 10 and r["patients"] >= 10
        and r["pct_ncrna"] <= 20 and r["pct_cell_only"] <= 35 and r["trials"] == 0]
print(json.dumps({"papers": len(papers), "non_review": len(P), "retracted_in_set": sum(p["retracted"] for p in papers),
                  "retracted_list_unique": len(retr),
                  "retracted_that_are_ncrna": sum(p["retracted"] and p["ncrna"] for p in papers),
                  "genes_scored": len(rows),
                  "since_2010_ncrna_vs_other": {"ncrna": [len(nc), sum(p["retracted"] for p in nc), round(100 * rn, 2)],
                                                "other": [len(ot), sum(p["retracted"] for p in ot), round(100 * ro, 2)],
                                                "fold": round(rn / ro, 1)},
                  "weak_evidence_union_ge40_ge60pct": weak,
                  "top_retraction_share_ge20": [(r["gene"], r["retracted"], r["papers"]) for r in top_retr],
                  "orphans": [len(orph), orph],
                  "corrections_applied": {f"{a}->{b or 'dropped'}": n for (a, b), n in sorted(n_corrected.items(), key=str)},
                  "by_period": per}, indent=1))
