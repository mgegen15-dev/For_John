#!/usr/bin/env python3
"""Engine cycle 15: do tumours with MYC gain, CCNE1 gain or 9p21 loss respond worse to chemotherapy before surgery?

Pre-registered in research_notes/Engine/cycle-15-chemo-response/PREREGISTRATION.md (commit da4b216).
Needs engine cycle 1's GEO downloads (GSE21257, GSE14827 and the GPL570 annotation in data/engine/cycle01/raw/)
and the TARGET-OS files of tools/survival_analysis.py.

Outputs: data/engine/cycle15/results.csv, summary.json, docs/figures/engine15_response.svg
"""
import csv
import gzip
import json
import math
import os
import re
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle01_ramp1 as c1        # noqa: E402
import survival_analysis as sa           # noqa: E402

ROOT = os.path.dirname(HERE)
RAW = c1.RAW
OUT = os.path.join(ROOT, "data", "engine", "cycle15")
FIG = os.path.join(ROOT, "docs", "figures")
GENES = ["MYC", "CCNE1", "CDKN2A", "MTAP"]
TESTS = {"H1": "MYC RNA", "H2": "CCNE1 RNA", "H3": "9p21 loss score (CDKN2A, MTAP)"}


def z(v):
    v = np.asarray(v, float)
    return (v - np.nanmean(v)) / np.nanstd(v, ddof=1)


def gpl570_map(genes):
    out = {g: [] for g in genes}
    with gzip.open(os.path.join(RAW, "GPL570.annot.gz"), "rt", errors="replace") as fh:
        hdr = None
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if hdr is None:
                if p[0] == "ID":
                    hdr = p
                    ix = hdr.index("Gene symbol")
                continue
            if len(p) > ix:
                syms = [s.strip() for s in re.split(r"///|,", p[ix])]
                for g in genes:
                    if g in syms:
                        out[g].append(p[0])
    return out


def measures(vals):
    m = {"MYC RNA": z(vals["MYC"]) if vals.get("MYC") is not None else None,
         "CCNE1 RNA": z(vals["CCNE1"]) if vals.get("CCNE1") is not None else None}
    loss = [z(vals[g]) for g in ("CDKN2A", "MTAP") if vals.get(g) is not None]
    m["9p21 loss score (CDKN2A, MTAP)"] = -np.nanmean(np.vstack(loss), axis=0) if loss else None
    for g in GENES:
        if vals.get(g) is not None:
            m[f"{g} alone"] = z(vals[g])
    return m


def geo_cohort(name, path, platform, outcome):
    ids, chars, expr = c1.read_matrix(path)
    pmap = gpl570_map(GENES) if platform == "GPL570" else c1.probe_map(platform, GENES)
    vals, probes = {}, {}
    for g in GENES:
        pr, v = c1.gene_values(expr, pmap[g])
        probes[g], vals[g] = pr, v
    y = np.array([outcome(c) for c in chars], float)
    keep = ~np.isnan(y)
    m = measures({g: (v[keep] if v is not None else None) for g, v in vals.items()})
    return {"cohort": name, "y": y[keep], "measures": m, "probes": probes,
            "huvos": [c.get("huvos grade") for c, k in zip(chars, keep) if k]}


def gse21257_outcome(c):
    h = c.get("huvos grade", "")
    return 1.0 if h in ("1", "2") else 0.0 if h in ("3", "4") else np.nan


def gse14827_outcome(c):
    r = c.get("chemotherapeutic response", "")
    return 1.0 if r == "poor" else 0.0 if r == "good" else np.nan


def target_cohort():
    pts = [p for p in sa.load_patients() if p.get("good_response") is not None]
    rna = sa.rna_values(GENES)
    pts = [p for p in pts if p["case"] in rna]
    y = np.array([1.0 - p["good_response"] for p in pts])
    vals = {g: np.array([rna[p["case"]].get(g, np.nan) for p in pts]) for g in GENES}
    cn = {k: [p.get(k) for p in pts] for k in ("MYC_amp", "CCNE1_amp", "CDKN2A_deepdel")}
    return {"cohort": "TARGET-OS", "y": y, "measures": measures(vals), "probes": None, "cn": cn}


def logistic(x, y):
    ok = ~np.isnan(x)
    X = np.column_stack([np.ones(ok.sum()), x[ok]])
    yy = y[ok]
    b = np.zeros(2)
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        H = X.T @ (X * (p * (1 - p))[:, None])
        step = np.linalg.solve(H, X.T @ (yy - p))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    se = float(np.sqrt(np.linalg.inv(H)[1, 1]))
    return {"beta": float(b[1]), "se": se, "or": math.exp(b[1]), "lo": math.exp(b[1] - 1.96 * se), "hi": math.exp(b[1] + 1.96 * se),
            "p": float(2 * stats.norm.sf(abs(b[1] / se))), "n": int(ok.sum()), "poor": int(yy.sum())}


def pool(effs):
    b = np.array([e["beta"] for e in effs])
    se = np.array([e["se"] for e in effs])
    w = 1 / se ** 2
    bf, sef = float((w * b).sum() / w.sum()), float(math.sqrt(1 / w.sum()))
    q = float((w * (b - bf) ** 2).sum())
    k = len(b)
    tau2 = max(0.0, (q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0
    wr = 1 / (se ** 2 + tau2)
    br, ser = float((wr * b).sum() / wr.sum()), float(math.sqrt(1 / wr.sum()))
    return {"or": math.exp(bf), "lo": math.exp(bf - 1.96 * sef), "hi": math.exp(bf + 1.96 * sef), "p": float(2 * stats.norm.sf(abs(bf / sef))),
            "I2": max(0.0, (q - (k - 1)) / q) if q > 0 and k > 1 else 0.0, "k": k,
            "random": {"or": math.exp(br), "lo": math.exp(br - 1.96 * ser), "hi": math.exp(br + 1.96 * ser)},
            "n": int(sum(e["n"] for e in effs)), "poor": int(sum(e["poor"] for e in effs))}


def verdict(m):
    if m["or"] > 1 and m["lo"] > 1:
        return "Supported"
    if m["hi"] < 1.5:
        return "Refuted"
    return "Inconclusive"


def forest(rows, path):
    W, top, rh, left = 860, 64, 30, 330
    H = top + rh * len(rows) + 56
    lo_ax, hi_ax = 0.25, 4.0
    X = lambda v: left + (np.log(min(max(v, lo_ax), hi_ax)) - np.log(lo_ax)) / (np.log(hi_ax) - np.log(lo_ax)) * (W - left - 170)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="13" role="img" '
         f'aria-label="Odds of a poor response to chemotherapy before surgery, per standard deviation">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="26" font-weight="600" fill="#1d2430">Poor response to chemotherapy before surgery: odds ratio per standard deviation</text>',
         '<text x="16" y="44" fill="#525b6b" font-size="12">Pooled across three cohorts, 95% CI, log scale. Right of 1: poorer response.</text>']
    for v in (0.25, 0.5, 1, 2, 4):
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{H - 46}" stroke="{"#525b6b" if v == 1 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{H - 30}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    for i, (label, r, col) in enumerate(rows):
        y = top + rh * i + rh / 2
        s.append(f'<text x="16" y="{y + 4:.1f}" fill="#1d2430">{label}</text>')
        s.append(f'<line x1="{X(r["lo"]):.1f}" y1="{y:.1f}" x2="{X(r["hi"]):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<circle cx="{X(r["or"]):.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
        s.append(f'<text x="{W - 10}" y="{y + 4:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{r["or"]:.2f} ({r["lo"]:.2f}–{r["hi"]:.2f})</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    cohorts = [geo_cohort("GSE21257", os.path.join(RAW, "GSE21257_series_matrix.txt.gz"), "GPL10295", gse21257_outcome),
               geo_cohort("GSE14827", os.path.join(RAW, "GSE14827_series_matrix.txt.gz"), "GPL570", gse14827_outcome),
               target_cohort()]
    S = {"preregistration_commit": "da4b216", "cohorts": {}, "pooled": {}, "verdicts": {}}
    out = []
    labels = list(TESTS.values()) + [f"{g} alone" for g in GENES]
    per = {lab: [] for lab in labels}
    for c in cohorts:
        S["cohorts"][c["cohort"]] = {"n": int(len(c["y"])), "poor": int(c["y"].sum()), "probes": c["probes"]}
        for lab in labels:
            x = c["measures"].get(lab)
            if x is None:
                continue
            r = logistic(x, c["y"])
            per[lab].append(r)
            out.append(["cohort", c["cohort"], lab, r["n"], r["poor"], f'{r["or"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.4f}'])
    for lab in labels:
        m = pool(per[lab])
        S["pooled"][lab] = m
        out.append(["pooled", "three cohorts", lab, m["n"], m["poor"], f'{m["or"]:.3f}', f'{m["lo"]:.3f}', f'{m["hi"]:.3f}', f'{m["p"]:.4f}'])
    for h, lab in TESTS.items():
        S["verdicts"][h] = verdict(S["pooled"][lab])
    # secondary: TARGET copy-number calls (Fisher), GSE21257 ordered Huvos
    t = cohorts[2]
    S["target_copy_number"] = {}
    for k in ("MYC_amp", "CCNE1_amp", "CDKN2A_deepdel"):
        pairs = [(a, yy) for a, yy in zip(t["cn"][k], t["y"]) if a is not None]
        tab = [[sum(1 for a, yy in pairs if a and yy), sum(1 for a, yy in pairs if a and not yy)],
               [sum(1 for a, yy in pairs if not a and yy), sum(1 for a, yy in pairs if not a and not yy)]]
        S["target_copy_number"][k] = {"altered_poor_good": tab[0], "not_altered_poor_good": tab[1], "fisher_p": float(stats.fisher_exact(tab)[1])}
    g = cohorts[0]
    hv = np.array([float(h) if h in ("1", "2", "3", "4") else np.nan for h in g["huvos"]])
    S["gse21257_spearman_with_huvos"] = {lab: float(stats.spearmanr(g["measures"][lab], hv, nan_policy="omit")[0]) for lab in TESTS.values()}
    S["P43"] = "right" if S["verdicts"]["H1"] == "Supported" else "wrong"
    S["P44"] = "right" if all(v != "Supported" for v in S["verdicts"].values()) else "wrong"
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["level", "cohort", "measure", "patients", "poor_response", "odds_ratio_per_sd", "lo", "hi", "p"])
        w.writerows(out)
    forest([(f"{h}: {lab}", S["pooled"][lab], "#1c5cab") for h, lab in TESTS.items()]
           + [(f"   {g} alone", S["pooled"][f"{g} alone"], "#9aa3b2") for g in GENES], os.path.join(FIG, "engine15_response.svg"))
    for r in out:
        print(r)
    print(json.dumps({k: S[k] for k in ("cohorts", "verdicts", "target_copy_number", "gse21257_spearman_with_huvos", "P43", "P44")}, indent=1, default=float))


if __name__ == "__main__":
    main()
