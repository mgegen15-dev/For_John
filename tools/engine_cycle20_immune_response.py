#!/usr/bin/env python3
"""Engine cycle 20: do tumours with more macrophage or T-cell signal respond better to chemotherapy before surgery?

Pre-registered in research_notes/Engine/cycle-20-immune-response/PREREGISTRATION.md (commit 822196e).

  python3 tools/engine_cycle20_immune_response.py fetch   # GSE289059 series matrix into data/engine/cycle20/raw/
  python3 tools/engine_cycle20_immune_response.py         # analysis (needs cycle 1 and cycle 15 inputs)

Outputs: data/engine/cycle20/results.csv, summary.json, docs/figures/engine20_immune_response.svg
"""
import csv
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle01_ramp1 as c1             # noqa: E402
import engine_cycle15_chemo_response as c15   # noqa: E402

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle20", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle20")
FIG = os.path.join(ROOT, "docs", "figures")
MAC, TC = ["CD163", "CD14", "CD68"], ["CD3E", "CD8A"]
GENES = MAC + TC
URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE289nnn/GSE289059/matrix/GSE289059_series_matrix.txt.gz"


def fetch():
    os.makedirs(RAW, exist_ok=True)
    subprocess.run(["curl", "-sS", "-f", "-L", "-o", os.path.join(RAW, "GSE289059_series_matrix.txt.gz"), URL], check=True)


def z(v):
    v = np.asarray(v, float)
    return (v - np.nanmean(v)) / np.nanstd(v, ddof=1)


def scores(vals):
    out = {}
    for lab, genes in (("macrophage score", MAC), ("T-cell score", TC)):
        have = [g for g in genes if vals.get(g) is not None]
        out[lab] = np.nanmean(np.vstack([z(vals[g]) for g in have]), axis=0) if have else None
    for g in GENES:
        if vals.get(g) is not None:
            out[f"{g} alone"] = z(vals[g])
    return out


def isg():
    ids, chars, expr = c1.read_matrix(os.path.join(RAW, "GSE289059_series_matrix.txt.gz"))
    allv = np.vstack(list(expr.values()))
    log = np.nanmax(allv) > 100
    vals = {g: (np.log2(np.clip(expr[g], 1, None)) if log else expr[g]) if g in expr else None for g in GENES}
    y = np.array([1.0 if c.get("good response/poor response") == "PR" else 0.0 if c.get("good response/poor response") == "GR" else np.nan for c in chars])
    pgp = np.array([1.0 if c.get("pgp positive") == "Positive" else 0.0 for c in chars])
    keep = ~np.isnan(y)
    v = {g: (x[keep] if x is not None else None) for g, x in vals.items()}
    return {"cohort": "GSE289059", "y": y[keep], "m": scores(v), "pgp": pgp[keep], "log2_applied": bool(log)}


def geo(name, path, platform, outcome):
    ids, chars, expr = c1.read_matrix(path)
    pmap = c15.gpl570_map(GENES) if platform == "GPL570" else c1.probe_map(platform, GENES)
    vals = {g: c1.gene_values(expr, pmap[g])[1] for g in GENES}
    y = np.array([outcome(c) for c in chars], float)
    keep = ~np.isnan(y)
    return {"cohort": name, "y": y[keep], "m": scores({g: (v[keep] if v is not None else None) for g, v in vals.items()})}


def target():
    pts = [p for p in c15.sa.load_patients() if p.get("good_response") is not None]
    rna = c15.sa.rna_values(GENES)
    pts = [p for p in pts if p["case"] in rna]
    y = np.array([1.0 - p["good_response"] for p in pts])
    return {"cohort": "TARGET-OS", "y": y, "m": scores({g: np.array([rna[p["case"]].get(g, np.nan) for p in pts]) for g in GENES})}


def logistic_adj(x, cov, y):
    X = np.column_stack([np.ones(len(y)), x, cov])
    b = np.zeros(3)
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        H = X.T @ (X * (p * (1 - p))[:, None])
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    se = float(np.sqrt(np.linalg.inv(H)[1, 1]))
    return {"or": float(np.exp(b[1])), "lo": float(np.exp(b[1] - 1.96 * se)), "hi": float(np.exp(b[1] + 1.96 * se))}


def verdict(m):
    if m["or"] < 1 and m["hi"] < 1:
        return "Supported"
    if m["lo"] > 0.67:
        return "Refuted"
    return "Inconclusive"


def main():
    os.makedirs(OUT, exist_ok=True)
    cohorts = [isg(),
               geo("GSE21257", os.path.join(c1.RAW, "GSE21257_series_matrix.txt.gz"), "GPL10295", c15.gse21257_outcome),
               geo("GSE14827", os.path.join(c1.RAW, "GSE14827_series_matrix.txt.gz"), "GPL570", c15.gse14827_outcome),
               target()]
    labels = ["macrophage score", "T-cell score"] + [f"{g} alone" for g in GENES]
    S = {"preregistration_commit": "822196e", "cohorts": {c["cohort"]: {"n": int(len(c["y"])), "poor": int(c["y"].sum())} for c in cohorts},
         "isg_log2_applied": cohorts[0]["log2_applied"], "pooled": {}, "per_cohort": {}}
    rows = []
    for lab in labels:
        effs = []
        for c in cohorts:
            x = c["m"].get(lab)
            if x is None:
                continue
            r = c15.logistic(x, c["y"])
            effs.append(r)
            S["per_cohort"].setdefault(lab, {})[c["cohort"]] = r
            rows.append(["cohort", c["cohort"], lab, r["n"], r["poor"], f'{r["or"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.4f}'])
        m = c15.pool(effs)
        S["pooled"][lab] = m
        rows.append(["pooled", f"{len(effs)} cohorts", lab, m["n"], m["poor"], f'{m["or"]:.3f}', f'{m["lo"]:.3f}', f'{m["hi"]:.3f}', f'{m["p"]:.4f}'])
    S["verdict_H1"] = verdict(S["pooled"]["macrophage score"])
    S["verdict_H2"] = verdict(S["pooled"]["T-cell score"])
    isgc = cohorts[0]
    S["isg_adjusted_for_pgp"] = {lab: logistic_adj(isgc["m"][lab], isgc["pgp"], isgc["y"]) for lab in ("macrophage score", "T-cell score")}
    S["P54"] = "right" if S["verdict_H1"] == "Supported" else "wrong"
    S["P55"] = "right" if S["verdict_H2"] == "Supported" else "wrong"
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["level", "cohort", "measure", "patients", "poor_response", "odds_ratio_per_unit_of_z_score", "lo", "hi", "p"])
        w.writerows(rows)
    fr = []
    for lab in ("macrophage score", "T-cell score"):
        for cname, r in S["per_cohort"][lab].items():
            fr.append((f"{lab.split()[0].capitalize()}: {cname}", r, "#6a7384"))
        fr.append((f"{lab.split()[0].capitalize()}: pooled", S["pooled"][lab], "#1c5cab"))
    c15.forest(fr, os.path.join(FIG, "engine20_immune_response.svg"),
               title="Poor response to chemotherapy before surgery: odds ratio per unit of the score (average of the genes' z-scores)",
               subtitle="Each cohort and pooled across four cohorts, 95% CI, log scale. Right of 1: poorer response.")
    for r in rows:
        print(r)
    print(json.dumps({k: S[k] for k in ("cohorts", "isg_log2_applied", "verdict_H1", "verdict_H2", "isg_adjusted_for_pgp", "P54", "P55")}, indent=1, default=float))


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
