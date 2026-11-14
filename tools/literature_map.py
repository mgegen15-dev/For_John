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
  retracted / review - from PubMed publication types"""
import csv, json, re, collections as C

L = "data/literature/"
retr = set(open(L + "osteosarcoma_retracted_pmids.txt").read().split())
rev = set(open(L + "osteosarcoma_reviews_pmids.txt").read().split())
CELL = re.compile(r"\b(u-?2 ?os|mg-?63|saos-?2|143b|hos|sjsa-?1|khos|zos|lm7|cell lines?)\b", re.I)
VIVO = re.compile(r"\b(mice|mouse|murine|xenograft|nude|in vivo|rats?|zebrafish|orthotopic)\b", re.I)
PAT = re.compile(r"\b(patients?|tumou?r (tissues?|samples?|specimens?)|cohort|biops(y|ies))\b", re.I)
DOG = re.compile(r"\b(canine|dogs?)\b", re.I)
NC = re.compile(r"\b(mi[rR]-?\d|microrna|lncrna|long non-?coding|circrna|circ_|hsa_circ|non-?coding rna|sponge)", re.I)
ALIAS = {"TRP53": "TP53", "CDKN2A": "CDKN2A", "MKI67": "MKI67"}
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
         "ncrna": bool(NC.search(txt)), "in_vivo": bool(VIVO.search(txt)),
         "patients": bool(PAT.search(txt)), "dog": bool(DOG.search(txt))}
    t["cell_only"] = bool(CELL.search(txt)) and not (t["in_vivo"] or t["patients"] or t["dog"])
    syms = {ALIAS.get((g[2] or "").upper(), (g[2] or "").upper()) for g in d["genes"] if g[2]}
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
def grants_for(sym):
    if len(sym) < 3: return 0
    p = re.compile(rf"\b{re.escape(sym)}\b", re.I)
    return len({r["project_num"][1:12] for r in gr if p.search(r["title"])})

rows = []
for s, c in genes.items():
    if c["papers"] < 5: continue
    n = c["papers"]
    rows.append({"gene": s, "papers": n, "first_year": first.get(s, ""), "since_2021": c["since_2021"],
                 "pct_cell_only": round(100 * c["cell_only"] / n), "pct_ncrna": round(100 * c["ncrna"] / n),
                 "retracted": c["retracted"], "in_vivo": c["in_vivo"], "patients": c["patients"], "dog": c["dog"],
                 "trials": len(trials.get(s, ())), "best_phase": best.get(s, 0), "nih_grants": grants_for(s),
                 "trial_ids": " ".join(sorted(trials.get(s, ())))[:400]})
rows.sort(key=lambda r: -r["papers"])
with open("data/osteosarcoma_gene_evidence.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

P = [p for p in papers if not p["review"]]
byy = C.defaultdict(C.Counter)
for p in P:
    if p["year"]:
        b = f"{p['year']//5*5}-{p['year']//5*5+4}"
        byy[b]["papers"] += 1; byy[b]["ncrna"] += p["ncrna"]; byy[b]["retracted"] += p["retracted"]; byy[b]["cell_only"] += p["cell_only"]
print(json.dumps({"papers": len(papers), "non_review": len(P), "retracted_in_set": sum(p["retracted"] for p in papers),
                  "retracted_that_are_ncrna": sum(p["retracted"] and p["ncrna"] for p in papers),
                  "genes_scored": len(rows), "by_period": {k: dict(v) for k, v in sorted(byy.items())}}, indent=1))
