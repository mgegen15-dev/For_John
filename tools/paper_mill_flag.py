"""Per-gene and per-journal 'evidence risk' flags for the osteosarcoma literature.

Definition (revised November 2026). A gene is flagged by two shares of its
non-review osteosarcoma papers published since 2010:
  - the share that are microRNA / lncRNA / circRNA papers ("microRNA-type",
    the `ncrna` tag from tools/literature_map.py), and
  - the share that PubMed lists as retracted.
  High:     microRNA-type share >= 35%, or retracted share >= 8%
  Elevated: microRNA-type share >= 20%, or retracted share >= 4%
  Typical:  neither
This flags a *pattern*, not misconduct by any author or paper.

Why not the earlier "template" (microRNA-type AND no mention of animals,
patients or dogs)? An audit found it adds nothing: since 2010, template papers
were retracted at 8.6% and the other microRNA-type papers at 8.7%. Its
"patients" test is also unreliable in both directions (any abstract saying
"osteosarcoma patients" escapes it; "OS tissues" does not count as patient
data). The comparison that carries the signal is microRNA-type vs all other
papers, which this script prints.

Small numbers: with 15-40 papers per gene, one retraction can move a flag.
The output gives a 95% Wilson interval for the retracted share and a
`flag_changes_with_one_retraction_fewer` column so this is visible.

Inputs: data/osteosarcoma_paper_tags.csv, data/literature/osteosarcoma_pubtator.jsonl
Outputs: data/osteosarcoma_evidence_risk_genes.csv, data/osteosarcoma_evidence_risk_journals.csv
Run from the repository root: python3 tools/paper_mill_flag.py"""
import csv, json, math, collections as C

tags = {r["pmid"]: r for r in csv.DictReader(open("data/osteosarcoma_paper_tags.csv"))}
journal = {}
for l in open("data/literature/osteosarcoma_pubtator.jsonl"):
    d = json.loads(l); journal.setdefault(d["pmid"], d.get("journal") or "")

T = lambda t, k: t[k] == "True"


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * max(0, c - h), 1), round(100 * min(1, c + h), 1))


def level(nc, r, n):
    a, b = nc / n, r / n
    return "high" if a >= 0.35 or b >= 0.08 else "elevated" if a >= 0.20 or b >= 0.04 else "typical"


P = [t for t in tags.values() if t["review"] == "False" and t["year"] and int(t["year"]) >= 2010]


def compare(papers, label):
    nc = [t for t in papers if T(t, "ncrna")]; ot = [t for t in papers if not T(t, "ncrna")]
    a, b = sum(T(t, "retracted") for t in nc), sum(T(t, "retracted") for t in ot)
    print(f"{label}: {len(papers)} papers; microRNA-type {len(nc)} ({100*len(nc)/len(papers):.1f}%), "
          f"retracted {a} ({100*a/len(nc):.2f}%, 95% CI {wilson(a, len(nc))}); "
          f"other {len(ot)}, retracted {b} ({100*b/len(ot):.2f}%, 95% CI {wilson(b, len(ot))}); "
          f"ratio {(a/len(nc))/(b/len(ot)):.1f}-fold")
    old = [t for t in nc if not (T(t, "in_vivo") or T(t, "patients") or T(t, "dog"))]
    rest = [t for t in nc if t not in old]
    print(f"  old 'template' check: template {len(old)}, retracted {sum(T(t,'retracted') for t in old)} "
          f"({100*sum(T(t,'retracted') for t in old)/len(old):.1f}%); other microRNA-type {len(rest)}, "
          f"retracted {sum(T(t,'retracted') for t in rest)} ({100*sum(T(t,'retracted') for t in rest)/len(rest):.1f}%)")


compare(P, "since 2010")
compare([t for t in P if int(t["year"]) <= 2019], "2010-2019 (retractions have had time to happen)")

g = C.defaultdict(C.Counter)
for t in P:
    for s in filter(None, t["genes"].split(";")):
        g[s]["papers"] += 1; g[s]["ncrna"] += T(t, "ncrna"); g[s]["retracted"] += T(t, "retracted")
        g[s]["independent"] += T(t, "in_vivo") or T(t, "patients") or T(t, "dog")
rows = []
for s, c in g.items():
    n = c["papers"]
    if n < 15: continue
    lv = level(c["ncrna"], c["retracted"], n)
    fragile = c["retracted"] > 0 and level(c["ncrna"], c["retracted"] - 1, n) != lv
    lo, hi = wilson(c["retracted"], n)
    rows.append({"gene": s, "papers_since_2010": n, "pct_ncrna": round(100 * c["ncrna"] / n),
                 "retracted": c["retracted"], "pct_retracted": round(100 * c["retracted"] / n, 1),
                 "pct_retracted_ci95": f"{lo}-{hi}",
                 "papers_with_animal_patient_or_dog_data": c["independent"], "risk": lv,
                 "flag_changes_with_one_retraction_fewer": fragile})
rank = {"high": 2, "elevated": 1, "typical": 0}
rows.sort(key=lambda r: (-rank[r["risk"]], -r["pct_ncrna"], -r["pct_retracted"], r["gene"]))
with open("data/osteosarcoma_evidence_risk_genes.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("genes:", len(rows), dict(C.Counter(r["risk"] for r in rows)),
      "flags that change with one retraction fewer:", sum(r["flag_changes_with_one_retraction_fewer"] for r in rows))

j = C.defaultdict(C.Counter)
for t in P:
    jn = journal.get(t["pmid"], "")
    j[jn]["papers"] += 1; j[jn]["ncrna"] += T(t, "ncrna"); j[jn]["retracted"] += T(t, "retracted")
jr = [{"journal": k, "papers_since_2010": c["papers"], "ncrna_papers": c["ncrna"], "retracted": c["retracted"],
       "pct_retracted": round(100 * c["retracted"] / c["papers"], 1)} for k, c in j.items() if c["papers"] >= 30]
jr.sort(key=lambda r: (-r["retracted"], r["journal"]))
with open("data/osteosarcoma_evidence_risk_journals.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(jr[0])); w.writeheader(); w.writerows(jr)
print("top journals by retractions:", [(r["journal"], r["retracted"], r["papers_since_2010"]) for r in jr[:8]])
print("high-risk genes with >=3 retractions:",
      [(r["gene"], r["pct_ncrna"], r["retracted"], r["papers_since_2010"]) for r in rows if r["risk"] == "high" and r["retracted"] >= 3])
