"""Per-gene and per-journal 'evidence risk' flags for the osteosarcoma literature.

A paper is counted as higher-risk when it matches the template most associated
with retractions in this field: a microRNA/lncRNA/circRNA paper whose
abstract reports only cell-line work (no animal, patient or dog data).
This flags a *pattern*, not misconduct by any author or paper.

Inputs: data/osteosarcoma_paper_tags.csv, data/literature/osteosarcoma_pubtator.jsonl
Outputs: data/osteosarcoma_evidence_risk_genes.csv, data/osteosarcoma_evidence_risk_journals.csv"""
import csv, json, collections as C

tags = {r["pmid"]: r for r in csv.DictReader(open("data/osteosarcoma_paper_tags.csv"))}
journal = {}
for l in open("data/literature/osteosarcoma_pubtator.jsonl"):
    d = json.loads(l); journal[d["pmid"]] = d.get("journal") or ""

P = [t for t in tags.values() if t["review"] == "False" and t["year"] and int(t["year"]) >= 2010]
T = lambda t, k: t[k] == "True"
template = lambda t: T(t, "ncrna") and not (T(t, "in_vivo") or T(t, "patients") or T(t, "dog"))
base = {"template": sum(map(template, P)) / len(P), "retracted": sum(T(t, "retracted") for t in P) / len(P)}
tmpl = [t for t in P if template(t)]
print(f"papers since 2010: {len(P)}; template papers: {len(tmpl)} ({100*base['template']:.1f}%); "
      f"retracted among template: {sum(T(t,'retracted') for t in tmpl)} ({100*sum(T(t,'retracted') for t in tmpl)/len(tmpl):.1f}%); "
      f"retracted among others: {sum(T(t,'retracted') for t in P if not template(t))} "
      f"({100*sum(T(t,'retracted') for t in P if not template(t))/(len(P)-len(tmpl)):.1f}%)")

g = C.defaultdict(C.Counter)
for t in P:
    for s in filter(None, t["genes"].split(";")):
        g[s]["papers"] += 1; g[s]["template"] += template(t); g[s]["retracted"] += T(t, "retracted")
        g[s]["independent"] += T(t, "in_vivo") or T(t, "patients") or T(t, "dog")
rows = []
for s, c in g.items():
    if c["papers"] < 15: continue
    share = c["template"] / c["papers"]
    level = "high" if share >= 0.35 or c["retracted"] / c["papers"] >= 0.08 else "elevated" if share >= 0.2 or c["retracted"] / c["papers"] >= 0.04 else "typical"
    rows.append({"gene": s, "papers_since_2010": c["papers"], "pct_template": round(100 * share),
                 "retracted": c["retracted"], "pct_retracted": round(100 * c["retracted"] / c["papers"], 1),
                 "papers_with_animal_patient_or_dog_data": c["independent"], "risk": level})
rows.sort(key=lambda r: (-{"high": 2, "elevated": 1, "typical": 0}[r["risk"]], -r["pct_template"]))
with open("data/osteosarcoma_evidence_risk_genes.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("genes:", C.Counter(r["risk"] for r in rows))

j = C.defaultdict(C.Counter)
for t in P:
    jn = journal.get(t["pmid"], "")
    j[jn]["papers"] += 1; j[jn]["template"] += template(t); j[jn]["retracted"] += T(t, "retracted")
jr = [{"journal": k, "papers_since_2010": c["papers"], "template": c["template"], "retracted": c["retracted"],
       "pct_retracted": round(100 * c["retracted"] / c["papers"], 1)} for k, c in j.items() if c["papers"] >= 30]
jr.sort(key=lambda r: -r["retracted"])
with open("data/osteosarcoma_evidence_risk_journals.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(jr[0])); w.writeheader(); w.writerows(jr)
print("top journals by retractions:", [(r["journal"], r["retracted"], r["papers_since_2010"]) for r in jr[:8]])
print("high-risk genes:", [(r["gene"], r["pct_template"], r["retracted"]) for r in rows if r["risk"] == "high"][:40])
