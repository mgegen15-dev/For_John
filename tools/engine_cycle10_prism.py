#!/usr/bin/env python3
"""Engine cycle 10: do the gene-change weaknesses hold up when real drugs are used?

Pre-registered in research_notes/Engine/cycle-10-drug-screen/PREREGISTRATION.md (commit ea42023),
before any drug-response file was downloaded.

  python3 tools/engine_cycle10_prism.py fetch   # PRISM Repurposing 20Q2 files into data/engine/prism/raw/
  python3 tools/engine_cycle10_prism.py         # analysis (needs the DepMap files from engine_cycle05_06_depmap.py)

Outputs: data/engine/cycle10/results.csv, osteosarcoma_lines.csv, summary.json, docs/figures/engine10_drugs.svg
"""
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle08_scan as c8                      # noqa: E402
import engine_cycle09_suppressor_scan as c9           # noqa: E402

ROOT = os.path.dirname(HERE)
DEP = os.path.join(ROOT, "data", "engine", "depmap", "raw")
RAW = os.path.join(ROOT, "data", "engine", "prism", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle10")
FIG = os.path.join(ROOT, "docs", "figures")
FILES = {  # PRISM Repurposing 20Q2, Figshare article 20564034
    "secondary-dose-response.csv": 36794595, "secondary-treatment-info.csv": 36794619, "secondary-cell-line-info.csv": 36794589,
    "primary-logfold.csv": 36794580, "primary-treatment-info.csv": 36794583, "primary-cell-line-info.csv": 36794565}
MDM2_DRUGS = ["idasanutlin", "amg-232", "nutlin-3", "cgm097"]
CDK46_DRUGS = ["palbociclib", "ribociclib", "abemaciclib"]
PILLS = ["cabozantinib", "regorafenib", "sorafenib", "lenvatinib", "pazopanib", "sunitinib", "anlotinib", "apatinib"]
D_MIN, MIN_ALTERED = -0.2, 10


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for name, fid in FILES.items():
        out = os.path.join(RAW, name)
        if not (os.path.exists(out) and os.path.getsize(out) > 10000):
            subprocess.run(["curl", "-sS", "-L", "--retry", "4", "-o", out, f"https://ndownloader.figshare.com/files/{fid}"], check=True)
        print(name, os.path.getsize(out))


# ------------------------------------------------------------------ drug data
def secondary_auc():
    """Median AUC per (drug name, screen batch, line); lines failing STR profiling dropped."""
    use = ["depmap_id", "screen_id", "auc", "name", "passed_str_profiling"]
    df = pd.read_csv(os.path.join(RAW, "secondary-dose-response.csv"), usecols=use)
    df = df[df["passed_str_profiling"].astype(str).str.upper() == "TRUE"]
    df["name"] = df["name"].astype(str).str.lower()
    return df.groupby(["name", "screen_id", "depmap_id"])["auc"].median()


def pick(auc, drug, batch=None):
    """Preferred batch is MTS010 where the drug has it (as the dataset readme recommends), else HTS002."""
    have = auc.loc[drug].index.get_level_values(0).unique()
    b = batch or ("MTS010" if "MTS010" in have else "HTS002")
    return (auc.loc[(drug, b)] if b in have else pd.Series(dtype=float)), b


def primary_lfc(drug):
    info = pd.read_csv(os.path.join(RAW, "primary-treatment-info.csv"))
    cols = info.loc[info["name"].astype(str).str.lower() == drug, "column_name"].tolist()
    lines = pd.read_csv(os.path.join(RAW, "primary-cell-line-info.csv"))
    ok = set(lines.loc[lines["passed_str_profiling"].astype(str).str.upper() == "TRUE", "row_name"])
    df = pd.read_csv(os.path.join(RAW, "primary-logfold.csv"), usecols=lambda c: c in set(cols) or c.startswith("Unnamed") or c == "", index_col=0)
    df = df[df.index.isin(ok)]
    rn = lines.drop_duplicates("row_name").set_index("row_name")["depmap_id"]
    s = df.median(axis=1)
    s.index = rn.reindex(s.index).values
    return s[pd.notna(s.index)].groupby(level=0).median(), cols


# ------------------------------------------------------------------ gene changes (rules from cycles 5, 6 and 9)
def gene_calls(model):
    lines = model.index.tolist()
    calls = c9.loss_calls(lines)[["TP53", "RB1"]]
    cn = c8.read_cols("OmicsCNGene.csv", {"CCNE1", "MTAP"}).reindex(lines)
    ex = c8.read_cols("OmicsExpressionProteinCodingGenesTPMLogp1.csv", {"CCNE1", "MTAP"}).reindex(lines)
    calls["CCNE1"] = np.where(cn["CCNE1"].notna(), (cn["CCNE1"] >= 2.0).astype(float), np.nan)
    calls["CCNE1_rna"] = ex["CCNE1"]
    calls["MTAP"] = np.where(ex["MTAP"].notna(), (ex["MTAP"] < 1.0).astype(float),
                             np.where(cn["MTAP"].notna(), (cn["MTAP"] < 0.25).astype(float), np.nan))
    return calls


# ------------------------------------------------------------------ statistics
def adjusted(y, x, lineage, adjust=True, binary=True):
    """Lineage-adjusted effect of x on y, in standard deviations of lineage-adjusted y."""
    m = y.notna() & x.notna() & lineage.notna()
    y, x, lin = y[m].values.astype(float), x[m].values.astype(float), lineage[m].values
    if adjust:
        yr = c8.residualise(y[:, None], lin)[:, 0]
        xr = c8.residualise(x[:, None], lin)[:, 0]
        k = len(np.unique(lin))
    else:
        yr, xr, k = y - y.mean(), x - x.mean(), 1
    sxx = float(xr @ xr)
    n_alt = int(x.sum()) if binary else None
    if sxx <= 0 or len(y) - k - 1 < 3:
        return {"n": int(len(y)), "n_altered": n_alt, "d": np.nan, "lo": np.nan, "hi": np.nan, "p": np.nan}
    beta = float(xr @ yr) / sxx
    df = len(y) - k - 1
    se = float(np.sqrt(max(float(yr @ yr) - beta ** 2 * sxx, 0) / df / sxx))
    sd = float(np.sqrt((yr @ yr) / (len(y) - k)))
    tq = stats.t.ppf(0.975, df)
    return {"n": int(len(y)), "n_altered": n_alt, "d": beta / sd, "lo": (beta - tq * se) / sd, "hi": (beta + tq * se) / sd,
            "p": float(2 * stats.t.sf(abs(beta / se), df)), "raw_difference": beta}


def verdict(r):
    if np.isnan(r["d"]):
        return "No data"
    if r["d"] <= D_MIN and r["hi"] < 0:
        return "Supported"
    if r["lo"] > D_MIN:
        return "Refuted"
    return "Inconclusive"


# ------------------------------------------------------------------ figure
def forest_svg(rows, path):
    W, top, rh, left = 860, 46, 30, 330
    H = top + rh * len(rows) + 60
    lo, hi = -1.0, 2.0
    X = lambda v: left + (min(max(v, lo), hi) - lo) / (hi - lo) * (W - left - 40)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="13" role="img" '
         f'aria-label="Lineage-adjusted difference in drug response, lines with the gene change against lines without">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="16" y="24" font-weight="600" fill="#1d2430">Drug response, lines with the gene change minus lines without (standard deviations)</text>']
    for v in (-1, -0.5, 0, 0.5, 1, 1.5, 2):
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 8}" x2="{X(v):.1f}" y2="{H - 50}" stroke="{"#525b6b" if v == 0 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{H - 34}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    for i, (label, r, colour) in enumerate(rows):
        y = top + rh * i + rh / 2
        s.append(f'<text x="16" y="{y + 4:.1f}" fill="#1d2430">{label}</text>')
        if not np.isnan(r["d"]):
            s.append(f'<line x1="{X(r["lo"]):.1f}" y1="{y:.1f}" x2="{X(r["hi"]):.1f}" y2="{y:.1f}" stroke="{colour}" stroke-width="2"/>')
            s.append(f'<circle cx="{X(r["d"]):.1f}" cy="{y:.1f}" r="5" fill="{colour}"/>')
    s.append(f'<text x="{(left + W - 40) / 2:.0f}" y="{H - 12}" text-anchor="middle" fill="#525b6b" font-size="12">'
             f'Left of zero: more sensitive. Right of zero: more resistant.</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


# ------------------------------------------------------------------ main
def main():
    os.makedirs(OUT, exist_ok=True)
    model = pd.read_csv(os.path.join(DEP, "Model.csv"), index_col=0)
    model = model[model["OncotreeLineage"].apply(lambda v: isinstance(v, str))]
    lineage = model["OncotreeLineage"]
    text = (model["OncotreePrimaryDisease"].fillna("") + " " + model["OncotreeSubtype"].fillna("")).str.lower()
    osteo = text.str.contains("osteosarcoma")
    calls = gene_calls(model)
    auc = secondary_auc()
    results, S = [], {"preregistration_commit": "ea42023", "batches": {}}

    def run(kind, drug, gene, expect, y, batch, adjust=True, binary=True, x=None):
        x = calls[gene] if x is None else x
        idx = y.index.intersection(model.index)
        r = adjusted(y.reindex(idx), x.reindex(idx), lineage.reindex(idx), adjust=adjust, binary=binary)
        r.update({"kind": kind, "drug": drug, "gene_change": gene, "expected": expect, "batch": batch, "lineage_adjusted": adjust})
        results.append(r)
        return r

    # Step 0
    checkA = [run("check A", d, "TP53", "resistant", *pick(auc, d)) for d in MDM2_DRUGS]
    checkB = [run("check B", d, "RB1", "resistant", *pick(auc, d)) for d in CDK46_DRUGS]
    passA = sum(r["lo"] > 0 for r in checkA) >= 3
    passB = sum(r["lo"] > 0 for r in checkB) >= 2
    S["check_A_passes"], S["check_B_passes"] = bool(passA), bool(passB)

    # Tests
    yT1, bT1 = pick(auc, "mk-1775")
    T1 = run("T1", "adavosertib", "CCNE1", "sensitive", yT1, bT1)
    yT2, colsT2 = primary_lfc("epz015666")
    T2 = run("T2", "epz015666", "MTAP", "sensitive", yT2, "primary " + ";".join(colsT2))
    for r in (T1, T2):
        r["verdict"] = verdict(r) if passA else "Not read (check A failed)"
        r["underpowered"] = bool(r["n_altered"] is None or r["n_altered"] < MIN_ALTERED)

    # Consistency checks for T1
    other = "HTS002" if bT1 == "MTS010" else "MTS010"
    yo, _ = pick(auc, "mk-1775", other)
    if len(yo):
        run("T1 consistency", "adavosertib", "CCNE1", "sensitive", yo, other)
    yp, colsP = primary_lfc("mk-1775")
    run("T1 consistency", "adavosertib", "CCNE1", "sensitive", yp, "primary " + ";".join(colsP))
    run("T1 consistency", "adavosertib", "CCNE1_rna", "sensitive (per log2 unit of RNA)", yT1, bT1, binary=False)
    run("T1 consistency", "adavosertib", "CCNE1", "sensitive", yT1, bT1, adjust=False)

    res = pd.DataFrame(results)
    cols = ["kind", "drug", "gene_change", "expected", "batch", "lineage_adjusted", "n", "n_altered", "d", "lo", "hi", "p", "raw_difference", "verdict", "underpowered"]
    res = res.reindex(columns=cols)
    res.round(4).to_csv(os.path.join(OUT, "results.csv"), index=False)

    # Descriptive: osteosarcoma lines (exploratory)
    rows = []
    for drug in ["mk-1775"] + MDM2_DRUGS + CDK46_DRUGS + PILLS:
        if drug not in auc.index.get_level_values(0):
            continue
        y, b = pick(auc, drug)
        y = y[y.index.isin(model.index)]
        pct = y.rank(pct=True)                     # 0 = most sensitive line in the screen
        for line in y.index[osteo.reindex(y.index).fillna(False).values]:
            rows.append({"line": model.loc[line, "StrippedCellLineName"], "depmap_id": line, "drug": drug, "batch": b,
                         "auc": y[line], "percentile_among_all_lines": pct[line], "lines_with_data": len(y),
                         "TP53_altered": calls.loc[line, "TP53"], "RB1_lost": calls.loc[line, "RB1"],
                         "CCNE1_amplified": calls.loc[line, "CCNE1"], "MTAP_lost": calls.loc[line, "MTAP"]})
    ol = pd.DataFrame(rows)
    ol.round(3).to_csv(os.path.join(OUT, "osteosarcoma_lines.csv"), index=False)

    S["results"] = json.loads(res.round(4).to_json(orient="records"))
    S["osteosarcoma_lines"] = sorted(ol["line"].unique().tolist()) if len(ol) else []
    S["P29"], S["P30"] = S["check_A_passes"], S["check_B_passes"]
    S["P31"], S["P32"] = T1["verdict"], T2["verdict"]
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=str)

    blue, grey, gold = "#1c5cab", "#6a7384", "#9a6b00"
    nice = {"idasanutlin": "Idasanutlin", "amg-232": "AMG-232", "nutlin-3": "Nutlin-3", "cgm097": "CGM097",
            "palbociclib": "Palbociclib", "ribociclib": "Ribociclib", "abemaciclib": "Abemaciclib"}
    fr = [(f"Check A: {nice[d]}, TP53 altered", r, grey) for d, r in zip(MDM2_DRUGS, checkA)]
    fr += [(f"Check B: {nice[d]}, RB1 lost", r, grey) for d, r in zip(CDK46_DRUGS, checkB)]
    fr += [("T1: Adavosertib, CCNE1 amplified", T1, blue), ("T2: EPZ015666, MTAP lost", T2, gold)]
    forest_svg(fr, os.path.join(FIG, "engine10_drugs.svg"))

    pd.set_option("display.width", 220)
    print(res[["kind", "drug", "gene_change", "batch", "n", "n_altered", "d", "lo", "hi", "p", "verdict"]].round(3).to_string())
    print("check A", passA, "check B", passB)
    if len(ol):
        print(ol.pivot_table(index="drug", columns="line", values="percentile_among_all_lines").round(2).to_string())
        print(ol.drop_duplicates("line")[["line", "TP53_altered", "RB1_lost", "CCNE1_amplified", "MTAP_lost"]].to_string())


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
