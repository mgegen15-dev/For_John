#!/usr/bin/env python3
"""Engine cycle 14: does tumour macrophage signal go with a better outcome outside the study that found it?

Pre-registered in research_notes/Engine/cycle-14-macrophages/PREREGISTRATION.md (commit 8a8a7c6).
Reuses the cohorts, end points and probe rules of engine cycle 1 (tools/engine_cycle01_ramp1.py; run its downloads first)
and the TARGET-OS files of tools/survival_analysis.py.

Outputs: data/engine/cycle14/results.csv, summary.json, docs/figures/engine14_macrophages.svg
"""
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle01_ramp1 as c1        # noqa: E402
import survival_analysis as sa           # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "engine", "cycle14")
FIG = os.path.join(ROOT, "docs", "figures")
MAC = ["CD163", "CD14", "CD68"]
TC = ["CD3E", "CD8A"]
GENES = MAC + TC
c1.GENES = GENES


def z(v):
    v = np.asarray(v, float)
    return (v - np.nanmean(v)) / np.nanstd(v, ddof=1)


def score(vals, genes):
    have = [g for g in genes if vals.get(g) is not None]
    if not have:
        return None, have
    return np.nanmean(np.vstack([z(vals[g]) for g in have]), axis=0), have


def cox(x, t, e, cov=None):
    ok = ~np.isnan(x)
    return c1.cox_one(x[ok], np.asarray(t, float)[ok], np.asarray(e, float)[ok], covars=None if cov is None else cov[ok])


def geo(loader):
    name, plat, ids, expr, rows = loader()
    pmap = c1.probe_map(plat, GENES)
    vals, probes = {}, {}
    for g in GENES:
        pr, v = c1.gene_values(expr, pmap[g])
        probes[g] = pr
        vals[g] = v
    if name == "GSE21257":
        sel = [r for r in rows if r["met_dx"] == 0]
        t, e, ep = [r["mfs_t"] for r in sel], [r["mfs_e"] for r in sel], "metastasis-free survival (no metastasis at diagnosis)"
    elif name == "GSE16091":
        sel = rows
        t, e, ep = [r["os_t"] for r in sel], [r["os_e"] for r in sel], "overall survival"
    else:
        sel = rows
        t, e, ep = [r["rfs_t"] for r in sel], [r["rfs_e"] for r in sel], "recurrence-free survival"
    idx = [r["i"] for r in sel]
    out = {"cohort": name, "endpoint": ep, "probes": probes, "results": {}}
    sub = {g: (v[idx] if v is not None else None) for g, v in vals.items()}
    for lab, genes in (("macrophage score", MAC), ("T-cell score", TC)):
        s, have = score(sub, genes)
        if s is not None:
            out["results"][lab] = dict(cox(s, t, e), genes_used=have)
    for g in GENES:
        if sub[g] is not None:
            out["results"][g] = cox(sub[g], t, e)
    if name == "GSE21257":
        allidx = [r["i"] for r in rows]
        s, _ = score({g: (v[allidx] if v is not None else None) for g, v in vals.items()}, MAC)
        cov = np.array([[r["met_dx"]] for r in rows], float)
        out["os_adjusted"] = cox(s, [r["os_t"] for r in rows], [r["os_e"] for r in rows], cov)
    return out


def target():
    pts = [p for p in sa.load_patients() if p.get("efs_days") is not None and p.get("efs_event") is not None and p.get("metastatic") is not None]
    rna = sa.rna_values(GENES)
    pts = [p for p in pts if p["case"] in rna]
    t = np.array([p["efs_days"] / 30.44 for p in pts])
    e = np.array([int(p["efs_event"]) for p in pts])
    m = np.array([[p["metastatic"]] for p in pts], float)
    vals = {g: np.array([rna[p["case"]].get(g, np.nan) for p in pts]) for g in GENES}
    out = {"cohort": "TARGET-OS", "endpoint": "event-free survival, adjusted for metastasis at diagnosis", "results": {}}
    for lab, genes in (("macrophage score", MAC), ("T-cell score", TC)):
        s, have = score(vals, genes)
        out["results"][lab] = dict(cox(s, t, e, m), genes_used=have)
    for g in GENES:
        out["results"][g] = cox(vals[g], t, e, m)
    return out


def pool(effs):
    """Fixed-effect pooled hazard ratio (cycle 1's meta), flattened, with the random-effects result alongside."""
    if not effs:
        return None
    m = c1.meta(effs)
    return dict(m["fixed"], random=m["random"], I2=m["I2"], k=m["k"])


def verdict(m):
    if m["hr"] < 1 and m["hi"] < 1:
        return "Supported"
    if m["lo"] > 0.77:
        return "Refuted"
    return "Inconclusive"


def forest(rows, path):
    W, top, rh, left = 860, 64, 30, 330
    H = top + rh * len(rows) + 56
    lo_ax, hi_ax = 0.25, 2.5
    X = lambda v: left + (np.log(min(max(v, lo_ax), hi_ax)) - np.log(lo_ax)) / (np.log(hi_ax) - np.log(lo_ax)) * (W - left - 170)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="13" role="img" '
         f'aria-label="Tumour macrophage gene score and outcome, discovery and independent cohorts">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="26" font-weight="600" fill="#1d2430">Tumour macrophage gene score and outcome: hazard ratio per standard deviation</text>',
         '<text x="16" y="44" fill="#525b6b" font-size="12">95% CI, log scale. Left of 1: better outcome with more macrophage signal.</text>']
    for v in (0.25, 0.5, 1, 2):
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{H - 46}" stroke="{"#525b6b" if v == 1 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{H - 30}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    for i, (label, r, col, bold) in enumerate(rows):
        y = top + rh * i + rh / 2
        s.append(f'<text x="16" y="{y + 4:.1f}" fill="#1d2430" font-weight="{600 if bold else 400}">{label}</text>')
        s.append(f'<line x1="{X(r["lo"]):.1f}" y1="{y:.1f}" x2="{X(r["hi"]):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<circle cx="{X(r["hr"]):.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
        s.append(f'<text x="{W - 10}" y="{y + 4:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{r["hr"]:.2f} ({r["lo"]:.2f}–{r["hi"]:.2f})</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    disc = geo(c1.cohort_gse21257)
    ind = [geo(c1.cohort_gse16091), geo(c1.cohort_gse39055), target()]
    S = {"preregistration_commit": "8a8a7c6", "discovery": disc, "independent": ind, "pooled": {}}
    rows = []
    for lab in ("macrophage score", "T-cell score") + tuple(GENES):
        effs = [c["results"][lab] for c in ind if lab in c["results"]]
        m = pool(effs)
        geo_only = pool([c["results"][lab] for c in ind[:2] if lab in c["results"]])
        S["pooled"][lab] = {"all_three": m, "geo_only": geo_only, "events": int(sum(e["events"] for e in effs))}
    S["verdict_H1"] = verdict(S["pooled"]["macrophage score"]["all_three"])
    S["verdict_H2"] = verdict(S["pooled"]["T-cell score"]["all_three"])
    d = disc["results"]["macrophage score"]
    S["P41"] = "right" if (d["hr"] < 1 and d["hi"] < 1) else "wrong"
    S["P42"] = "right" if S["verdict_H1"] == "Supported" else "wrong"
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["set", "cohort", "endpoint", "measure", "n", "events", "hr_per_sd", "lo", "hi", "p"])
        for c, setname in [(disc, "discovery (reproduction check)")] + [(c, "independent") for c in ind]:
            for lab, r in c["results"].items():
                w.writerow([setname, c["cohort"], c["endpoint"], lab, r["n"], r["events"], f'{r["hr"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.4f}'])
        r = disc["os_adjusted"]
        w.writerow(["discovery (secondary)", "GSE21257", "overall survival, adjusted for metastasis at diagnosis", "macrophage score", r["n"], r["events"],
                    f'{r["hr"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.4f}'])
        for lab, v in S["pooled"].items():
            for k in ("all_three", "geo_only"):
                m = v[k]
                if m:
                    w.writerow(["pooled " + k.replace("_", " "), "", "", lab, "", v["events"] if k == "all_three" else "", f'{m["hr"]:.3f}', f'{m["lo"]:.3f}', f'{m["hi"]:.3f}', f'{m["p"]:.4f}'])
    blue, grey, navy = "#1c5cab", "#6a7384", "#14264a"
    fr = [("Discovery: GSE21257 (Leiden), check", d, grey, False)]
    for c in ind:
        fr.append((f'{c["cohort"]} ({c["results"]["macrophage score"]["events"]} events)', c["results"]["macrophage score"], blue, False))
    fr.append(("Pooled, three independent cohorts", S["pooled"]["macrophage score"]["all_three"], navy, True))
    forest(fr, os.path.join(FIG, "engine14_macrophages.svg"))
    print("discovery", {k: (round(v["hr"], 2), round(v["lo"], 2), round(v["hi"], 2), v["events"]) for k, v in disc["results"].items()})
    print("probes", disc["probes"])
    for c in ind:
        print(c["cohort"], {k: (round(v["hr"], 2), round(v["lo"], 2), round(v["hi"], 2), v["n"], v["events"]) for k, v in c["results"].items()})
        print("  probes", c.get("probes"))
    for lab, v in S["pooled"].items():
        m = v["all_three"]
        print("POOLED", lab, round(m["hr"], 2), round(m["lo"], 2), round(m["hi"], 2), "I2", round(m.get("I2", 0), 2), "events", v["events"])
    print("verdicts", S["verdict_H1"], S["verdict_H2"], "P41", S["P41"], "P42", S["P42"])


if __name__ == "__main__":
    main()
