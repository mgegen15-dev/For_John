#!/usr/bin/env python3
"""Engine cycle 11: do lung metastases keep the surface targets that new drugs aim at?

Pre-registered in research_notes/Engine/cycle-11-targets-in-metastases/PREREGISTRATION.md (commit eb48e69).
Reuses the datasets and loaders of engine cycle 2 (tools/engine_cycle02_cxcr4.py; run tools/engine_cycle02_fetch.sh first).

Outputs: data/engine/cycle11/results.csv, summary.json, tumour_cells.csv, docs/figures/engine11_targets.svg
"""
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle02_cxcr4 as c2           # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "engine", "cycle11")
FIG = os.path.join(ROOT, "docs", "figures")
MAIN = ["LRRC15", "CD276"]
SECOND = ["ERBB2", "GPNMB", "B4GALNT1", "PTK7", "ADAM12", "IFITM5"]
TARGETS = MAIN + SECOND
ENSG_NEW = {"LRRC15": "ENSG00000172061", "CD276": "ENSG00000103855", "ERBB2": "ENSG00000141736", "GPNMB": "ENSG00000136235",
            "B4GALNT1": "ENSG00000135454", "PTK7": "ENSG00000112655", "ADAM12": "ENSG00000148848", "IFITM5": "ENSG00000206013"}
NAMES = {"CD276": "CD276 (B7-H3)", "ERBB2": "ERBB2 (HER2)", "B4GALNT1": "B4GALNT1 (GD2 synthase)"}
Z = c2.Z95

# point the cycle 2 loaders at the target genes
c2.TEST = TARGETS
c2.BULK_GENES = TARGETS + c2.LUNG + c2.IMMUNE
c2.SC_GENES = sorted(set(TARGETS + c2.LUNG + c2.IMMUNE + c2.SC_ENDO + c2.SC_EPI + c2.SC_TUMOUR + ["ACP5", "CTSK", "CD68"]))
c2.ENSG.update(ENSG_NEW)


def ci(e):
    if e is None:
        return None
    if "lo" in e:
        return e["g"], e["lo"], e["hi"]
    return e["g"], e["g"] - Z * e["se"], e["g"] + Z * e["se"]


def verdict(adj, tumour):
    if adj is None:
        return "No data"
    g, lo, hi = adj["g"], adj["lo"], adj["hi"]
    if lo > -0.5:
        return "Maintained"
    if g <= -0.5 and hi < 0:
        if tumour is not None and tumour["g"] >= 0:
            return "Inconclusive (explained by the surroundings)"
        return "Lower in metastases"
    return "Inconclusive"


def forest(rows, path):
    W, top, rh, left = 900, 70, 30, 300
    H = top + rh * len(rows) + 56
    lo_ax, hi_ax = -3.0, 3.0
    X = lambda v: left + (min(max(v, lo_ax), hi_ax) - lo_ax) / (hi_ax - lo_ax) * (W - left - 150)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="13" role="img" '
         f'aria-label="Surface-target RNA in lung metastases against primary tumours, adjusted for lung and immune tissue">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="26" font-weight="600" fill="#1d2430">Target RNA, lung metastases against primary tumours (adjusted for lung and immune tissue)</text>',
         '<text x="16" y="46" fill="#525b6b" font-size="12">Hedges\' g with 95% CI. Left of the dashed line at −0.5 would mean a meaningful drop in metastases.</text>']
    for v in (-3, -2, -1, 0, 1, 2, 3):
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{H - 46}" stroke="{"#525b6b" if v == 0 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{H - 30}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    s.append(f'<line x1="{X(-0.5):.1f}" y1="{top - 6}" x2="{X(-0.5):.1f}" y2="{H - 46}" stroke="#a3401a" stroke-dasharray="4 4"/>')
    for i, (label, g, lo, hi, main) in enumerate(rows):
        y = top + rh * i + rh / 2
        col = "#1c5cab" if main else "#6a7384"
        s.append(f'<text x="16" y="{y + 4:.1f}" fill="#1d2430" font-weight="{600 if main else 400}">{label}</text>')
        s.append(f'<line x1="{X(lo):.1f}" y1="{y:.1f}" x2="{X(hi):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<circle cx="{X(g):.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
        s.append(f'<text x="{W - 10}" y="{y + 4:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{g:+.2f} ({lo:+.2f} to {hi:+.2f})</text>')
    s.append(f'<text x="{(left + W - 150) / 2:.0f}" y="{H - 10}" text-anchor="middle" fill="#525b6b" font-size="12">Right of zero: higher in lung metastases</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    primary = [c2.ds_gse14359(), c2.ds_gse220538(), c2.ds_gse140131(), c2.ds_gse293065(), c2.ds_gse152048(), c2.ds_gse318840()]
    sens = [c2.ds_gse32981(), c2.ds_gse237033(), c2.ds_gse87624()]
    pairs = c2.ds_gse220538(paired_only=True)
    for d in primary + sens + [pairs]:
        c2.add_scores(d["units"])

    rows, S = [], {"preregistration_commit": "eb48e69", "genes": {}}

    def rec(analysis, dataset, gene, e):
        c = ci(e)
        if c:
            rows.append([analysis, dataset, gene, e.get("n_lm", ""), e.get("n_p", ""), *[f"{x:.3f}" for x in c],
                         f'{e["diff_log2"]:.3f}' if "diff_log2" in e else ""])

    # built-in check
    lung = c2.meta([c2.effect(d["units"], "lung_score") for d in primary])
    S["check_lung_score"] = lung
    rec("check: lung score, pooled", "six", "lung_score", lung)

    for g in TARGETS:
        per = {d["name"]: c2.effect(d["units"], g) for d in primary}
        for dn, e in per.items():
            rec("per dataset", dn, g, e)
        unadj = c2.meta(per.values())
        adjs = {d["name"]: c2.adjusted_effect(d["units"], g, ["lung_score", "immune_score"]) for d in primary}
        adj = c2.meta(adjs.values())
        tum = {d["name"]: c2.effect(d["tumour_units"], g) for d in primary if "tumour_units" in d}
        tum_m = c2.meta(tum.values())
        paired = c2.effect(pairs["units"], g, paired=True)
        sens_e = {d["name"]: c2.effect(d["units"], g, paired=d.get("paired", False)) for d in sens}
        n_lm = adj["n_lm"] if adj else 0
        v = verdict(adj, tum_m)
        S["genes"][g] = {"verdict": v, "underpowered": n_lm < 20, "n_lm_adjusted": n_lm, "unadjusted": unadj, "adjusted": adj,
                         "tumour_cells": tum_m, "matched_pairs": paired, "sensitivity_pooled": c2.meta(sens_e.values()),
                         "datasets_with_gene": [k for k, e in per.items() if e]}
        rec("pooled, unadjusted", "six", g, unadj)
        rec("pooled, adjusted for lung and immune (verdict)", "six", g, adj)
        for dn, e in tum.items():
            rec("tumour cells only", dn, g, e)
        rec("tumour cells only, pooled", "single-cell", g, tum_m)
        rec("matched pairs", pairs["name"], g, paired)
        rec("sensitivity, site-unknown datasets pooled", "three", g, S["genes"][g]["sensitivity_pooled"])

    # tumour-cell detail (share of tumour cells with any reads)
    with open(os.path.join(OUT, "tumour_cells.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "sample", "group"] + [f"{g}_log2cpm" for g in TARGETS] + [f"{g}_share_of_cells_with_reads" for g in TARGETS])
        for d in primary:
            for u in d.get("tumour_units", []):
                w.writerow([d["name"], u["unit"], u["group"]] + [f'{u[g]:.3f}' for g in TARGETS] + [f'{u["frac_pos"][g]:.3f}' for g in TARGETS])
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["analysis", "dataset", "gene", "n_lung_metastases", "n_primaries", "hedges_g", "ci_low", "ci_high", "mean_difference_log2"])
        w.writerows(rows)
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)


    # checks outside the plan (reported as such in the cycle 11 report): stability of the lung-tissue adjustment
    post = {"lung_score_g_per_dataset": {d["name"]: c2.effect(d["units"], "lung_score")["g"] for d in primary}, "genes": {}}
    for g in TARGETS:
        row = {}
        for lab, cov in (("immune_only", ["immune_score"]), ("lung_only", ["lung_score"])):
            m = c2.meta([c2.adjusted_effect(d["units"], g, cov) for d in primary])
            row[lab] = {k: m[k] for k in ("g", "lo", "hi")} if m else None
        loo = c2.meta([c2.adjusted_effect(d["units"], g, ["lung_score", "immune_score"]) for d in primary if d["name"] != "GSE318840"])
        row["lung_and_immune_without_GSE318840"] = {k: loo[k] for k in ("g", "lo", "hi")} if loo else None
        row["per_dataset_lung_and_immune"] = {d["name"]: (lambda e: {"g": e["g"], "se": e["se"]} if e else None)(c2.adjusted_effect(d["units"], g, ["lung_score", "immune_score"])) for d in primary}
        post["genes"][g] = row
    json.dump(post, open(os.path.join(OUT, "posthoc_checks.json"), "w"), indent=1, default=float)

    fr = []
    for g in TARGETS:
        a = S["genes"][g]["adjusted"]
        if a:
            fr.append((NAMES.get(g, g) + (" (main)" if g in MAIN else ""), a["g"], a["lo"], a["hi"], g in MAIN))
    forest(fr, os.path.join(FIG, "engine11_targets.svg"))

    print("lung score check:", {k: round(lung[k], 2) for k in ("g", "lo", "hi")})
    for g in TARGETS:
        x = S["genes"][g]
        def f(e):
            return "—" if not e else (f'{e["g"]:+.2f} ({e["lo"]:+.2f} to {e["hi"]:+.2f}) n {e["n_lm"]}v{e["n_p"]}' if "lo" in e
                                      else f'{e["g"]:+.2f} ({e["g"] - Z * e["se"]:+.2f} to {e["g"] + Z * e["se"]:+.2f}) n {e["n_lm"]}')
        print(f"\n{g}: {x['verdict']}  underpowered={x['underpowered']}  datasets={x['datasets_with_gene']}")
        print("  adjusted ", f(x["adjusted"]))
        print("  unadjust ", f(x["unadjusted"]))
        print("  tumour   ", f(x["tumour_cells"]))
        print("  pairs    ", f(x["matched_pairs"]))
        print("  sens     ", f(x["sensitivity_pooled"]))


if __name__ == "__main__":
    main()
