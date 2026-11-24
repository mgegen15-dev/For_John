#!/usr/bin/env python3
"""Engine cycles 5 and 6: two dependency questions in osteosarcoma cell lines, from DepMap public data.

  Cycle 5  Do osteosarcoma lines without MTAP depend more on PRMT5 (or MAT2A)?
  Cycle 6  Do osteosarcoma lines with more CCNE1 depend more on PKMYT1?

Pre-registered in research_notes/Engine/cycle-05-mtap-prmt5/ and cycle-06-ccne1-pkmyt1/ (committed before
any DepMap file was downloaded).

  python3 tools/engine_cycle05_06_depmap.py fetch   download from DepMap's Figshare releases (about 2.5 GB)
  python3 tools/engine_cycle05_06_depmap.py         analyse

Outputs: data/engine/cycle05/, data/engine/cycle06/ (results.csv, summary.json, lines.csv), docs/figures/engine05_mtap_primary.svg, engine06_ccne1_pkmyt1.svg
"""
import csv
import json
import math
import os
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "engine", "depmap", "raw")
FIG = os.path.join(ROOT, "docs", "figures")
FILES = {  # DepMap 24Q4 Public (Figshare article 27993248) and DEMETER2 (article 6025238)
    "Model.csv": 51065297, "CRISPRGeneEffect.csv": 51064667, "OmicsExpressionProteinCodingGenesTPMLogp1.csv": 51065489,
    "OmicsCNGene.csv": 51065324, "D2_combined_gene_dep_scores.csv": 13515395, "D2_sample_info.csv": 11489717}
GENES = ["PRMT5", "MAT2A", "RIOK1", "WDR77", "MTAP", "CDKN2A", "PKMYT1", "WEE1", "CDK2", "CCNE1"]


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for name, fid in FILES.items():
        out = os.path.join(RAW, name)
        if not (os.path.exists(out) and os.path.getsize(out) > 10000):
            subprocess.run(["curl", "-sS", "-L", "--retry", "4", "-o", out, f"https://ndownloader.figshare.com/files/{fid}"], check=True)
        print(name, os.path.getsize(out))


# ------------------------------------------------------------------ load
def wide(name):
    """Models in rows, 'GENE (entrez)' in columns: keep only the genes needed."""
    path = os.path.join(RAW, name)
    cols = pd.read_csv(path, nrows=0).columns
    keep = [cols[0]] + [c for c in cols[1:] if c.split(" (")[0] in GENES]
    df = pd.read_csv(path, usecols=keep, index_col=0)
    df.columns = [c.split(" (")[0] for c in df.columns]
    return df.loc[:, ~df.columns.duplicated()]


def load():
    model = pd.read_csv(os.path.join(RAW, "Model.csv"), index_col=0)
    crispr, expr, cn = wide("CRISPRGeneEffect.csv"), wide("OmicsExpressionProteinCodingGenesTPMLogp1.csv"), wide("OmicsCNGene.csv")
    d2 = pd.read_csv(os.path.join(RAW, "D2_combined_gene_dep_scores.csv"), index_col=0)
    d2.index = [i.split(" (")[0] for i in d2.index]
    d2 = d2.loc[[g for g in GENES if g in d2.index]].T                   # lines in rows
    ccle = {str(v): k for k, v in model["CCLEName"].dropna().items()}
    d2.index = [ccle.get(i) for i in d2.index]
    d2 = d2[[i is not None for i in d2.index]]
    d2 = d2[~d2.index.duplicated()]
    t = pd.DataFrame(index=model.index)
    t["name"] = model["StrippedCellLineName"]
    t["lineage"], t["disease"], t["subtype"] = model["OncotreeLineage"], model["OncotreePrimaryDisease"], model["OncotreeSubtype"]
    t["primary_or_metastasis"] = model["PrimaryOrMetastasis"]
    text = (t["disease"].fillna("") + " " + t["subtype"].fillna("")).str.lower()
    t["osteosarcoma"] = text.str.contains("osteosarcoma")
    t["sarcoma_lineage"] = t["lineage"].isin(["Bone", "Soft Tissue"])
    for g in ("MTAP", "CDKN2A", "CCNE1"):
        t[f"{g}_expr"] = expr[g].reindex(t.index) if g in expr else np.nan
        t[f"{g}_cn"] = cn[g].reindex(t.index) if g in cn else np.nan
    # pre-registered MTAP rule: expression below 1 on the log2(TPM+1) scale; copy number below 0.25 if expression is missing
    t["mtap_lost"] = np.where(t["MTAP_expr"].notna(), t["MTAP_expr"] < 1.0, np.where(t["MTAP_cn"].notna(), t["MTAP_cn"] < 0.25, np.nan))
    t["mtap_lost_by_cn"] = np.where(t["MTAP_cn"].notna(), t["MTAP_cn"] < 0.25, np.nan)
    t["ccne1_amplified"] = np.where(t["CCNE1_cn"].notna(), t["CCNE1_cn"] >= 2.0, np.nan)
    for g in ("PRMT5", "MAT2A", "RIOK1", "WDR77", "PKMYT1", "WEE1", "CDK2"):
        t[f"{g}_crispr"] = crispr[g].reindex(t.index) if g in crispr else np.nan
        t[f"{g}_rnai"] = d2[g].reindex(t.index) if g in d2 else np.nan
    return t


# ------------------------------------------------------------------ statistics
def welch(a, b):
    """Mean(a) - mean(b) with a Welch 95% confidence interval. a = MTAP-lost, b = intact."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return {"n_lost": int(len(a)), "n_intact": int(len(b)), "diff": float(a.mean() - b.mean()) if len(a) and len(b) else None}
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = math.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1)) if se > 0 else 1
    tq = stats.t.ppf(0.975, df)
    d = a.mean() - b.mean()
    return {"n_lost": int(len(a)), "n_intact": int(len(b)), "diff": float(d), "lo": float(d - tq * se), "hi": float(d + tq * se),
            "p": float(2 * stats.t.sf(abs(d / se), df)) if se > 0 else None, "mean_lost": float(a.mean()), "mean_intact": float(b.mean())}


def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = ~np.isnan(x) & ~np.isnan(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return {"n": int(len(x))}
    r = stats.linregress(x, y)
    tq = stats.t.ppf(0.975, len(x) - 2)
    rho, prho = stats.spearmanr(x, y)
    return {"n": int(len(x)), "slope": float(r.slope), "lo": float(r.slope - tq * r.stderr), "hi": float(r.slope + tq * r.stderr),
            "p": float(r.pvalue), "pearson_r": float(r.rvalue), "spearman_rho": float(rho), "spearman_p": float(prho)}


def verdict(effect, lo, hi, reference):
    """Shared rule: supported if negative with the interval excluding zero; refuted if the whole interval
    lies above half the all-cancer reference effect (which is negative); otherwise inconclusive."""
    if effect is None or lo is None:
        return "Inconclusive"
    if effect < 0 and hi < 0:
        return "Supported"
    if lo > reference / 2:
        return "Refuted"
    return "Inconclusive"


# ------------------------------------------------------------------ figures
def strip_svg(groups, path, title, sub, ylabel):
    """One row per cell line, grouped. groups: [(label, [(name, value)], colour)]."""
    rowh, left, top, right = 22, 190, 92, 40
    nrows = sum(len(pts) + 1 for _, pts, _ in groups)
    W, H = 760, top + rowh * nrows + 56
    vals = [v for _, pts, _ in groups for _, v in pts]
    lo, hi = min(vals + [0]) - 0.1, max(vals + [0]) + 0.1
    X = lambda v: left + (v - lo) / (hi - lo) * (W - left - right)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="13">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">{title}</text>',
         f'<text x="16" y="50" fill="#525b6b">{sub[0]}</text>', f'<text x="16" y="68" fill="#525b6b">{sub[1]}</text>']
    bottom = top + rowh * nrows
    v = math.ceil(lo / 0.5) * 0.5
    while v <= hi:
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{bottom}" stroke="{"#525b6b" if abs(v) < 1e-9 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{bottom + 18}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
        v += 0.5
    s.append(f'<text x="{(left + W - right) / 2:.0f}" y="{bottom + 40}" text-anchor="middle" fill="#525b6b" font-size="12">{ylabel}</text>')
    k = 0
    for lab, pts, col in groups:
        y = top + rowh * k + rowh / 2
        s.append(f'<text x="16" y="{y + 5:.1f}" fill="#14181f" font-weight="600">{lab} ({len(pts)})</text>')
        if pts:
            m = float(np.mean([p[1] for p in pts]))
            s.append(f'<line x1="{X(m):.1f}" y1="{y + rowh / 2:.1f}" x2="{X(m):.1f}" y2="{y + rowh / 2 + rowh * len(pts):.1f}" stroke="{col}" stroke-width="2" stroke-dasharray="5 4"/>')
            s.append(f'<text x="{X(m):.1f}" y="{y + 5:.1f}" text-anchor="middle" fill="{col}" font-size="12">average {m:.2f}</text>')
        k += 1
        for name, val in sorted(pts, key=lambda q: q[1]):
            y = top + rowh * k + rowh / 2
            s.append(f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{name}</text>')
            s.append(f'<line x1="{X(0):.1f}" y1="{y:.1f}" x2="{X(val):.1f}" y2="{y:.1f}" stroke="{col}" stroke-opacity="0.35" stroke-width="2"/>')
            s.append(f'<circle cx="{X(val):.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
            k += 1
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def scatter_svg(pts, fit, path, title, sub, xlabel, ylabel):
    """pts: [(name, x, y, highlight)]. fit: (slope, intercept) or None."""
    W, H, left, top, bottom = 760, 440, 70, 84, 60
    xs, ys = [p[1] for p in pts], [p[2] for p in pts]
    x0, x1, y0, y1 = min(xs) - 0.3, max(xs) + 0.3, min(ys + [0]) - 0.1, max(ys + [0]) + 0.1
    X = lambda v: left + (v - x0) / (x1 - x0) * (W - left - 30)
    Y = lambda v: top + (y1 - v) / (y1 - y0) * (H - top - bottom)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="13">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">{title}</text>',
         f'<text x="16" y="50" fill="#525b6b">{sub[0]}</text>', f'<text x="16" y="68" fill="#525b6b">{sub[1]}</text>']
    v = math.ceil(y0 / 0.5) * 0.5
    while v <= y1:
        s.append(f'<line x1="{left}" y1="{Y(v):.1f}" x2="{W - 30}" y2="{Y(v):.1f}" stroke="{"#525b6b" if abs(v) < 1e-9 else "#e2e5ea"}"/>')
        s.append(f'<text x="{left - 8}" y="{Y(v) + 4:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{v:g}</text>')
        v += 0.5
    v = math.ceil(x0)
    while v <= x1:
        s.append(f'<text x="{X(v):.1f}" y="{H - bottom + 18}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
        v += 1
    if fit:
        s.append(f'<line x1="{X(x0):.1f}" y1="{Y(fit[0] * x0 + fit[1]):.1f}" x2="{X(x1):.1f}" y2="{Y(fit[0] * x1 + fit[1]):.1f}" stroke="#a3401a" stroke-dasharray="5 4"/>')
    for name, x, y, hl in pts:
        s.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5" fill="{"#f7c020" if hl else "#1c5cab"}" stroke="#14264a" stroke-width="{1.5 if hl else 0}"/>')
        s.append(f'<text x="{X(x) + 8:.1f}" y="{Y(y) + 4:.1f}" fill="#525b6b" font-size="10">{name}</text>')
    s.append(f'<text x="{(left + W - 30) / 2:.0f}" y="{H - 16}" text-anchor="middle" fill="#525b6b" font-size="12">{xlabel}</text>')
    s.append(f'<text x="18" y="{(top + H - bottom) / 2:.0f}" transform="rotate(-90 18 {(top + H - bottom) / 2:.0f})" text-anchor="middle" fill="#525b6b" font-size="12">{ylabel}</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


# ------------------------------------------------------------------ cycles
MEASURES = [("PRMT5 knockdown (RNAi)", "PRMT5_rnai"), ("MAT2A knockdown (RNAi)", "MAT2A_rnai"),
            ("PRMT5 knockout (CRISPR)", "PRMT5_crispr"), ("MAT2A knockout (CRISPR)", "MAT2A_crispr")]


def cycle5(t):
    out = os.path.join(ROOT, "data", "engine", "cycle05")
    os.makedirs(out, exist_ok=True)
    known = t[t["mtap_lost"].notna()].copy()
    known["mtap_lost"] = known["mtap_lost"].astype(bool)
    osl, sar = known[known["osteosarcoma"]], known[known["sarcoma_lineage"]]
    S = {"positive_control": {}, "osteosarcoma": {}, "sarcoma": {}, "secondary": {}}

    def cmp(df, col, flag="mtap_lost"):
        f = df[flag].astype(bool)
        return welch(df.loc[f, col], df.loc[~f, col])
    for lab, col in MEASURES:
        S["positive_control"][lab] = cmp(known, col)
        S["osteosarcoma"][lab] = cmp(osl, col)
        S["sarcoma"][lab] = cmp(sar, col)
    S["control_passed"] = any(v.get("hi") is not None and v["hi"] < 0 for v in S["positive_control"].values())
    # primary measure by the pre-registered rule
    p = S["osteosarcoma"]["PRMT5 knockdown (RNAi)"]
    primary = "PRMT5 knockdown (RNAi)" if min(p["n_lost"], p["n_intact"]) >= 3 else "MAT2A knockout (CRISPR)"
    e, ref = S["osteosarcoma"][primary], S["positive_control"][primary]["diff"]
    S["primary_measure"], S["reference_effect_D"] = primary, ref
    S["verdict"] = verdict(e.get("diff"), e.get("lo"), e.get("hi"), ref) if S["control_passed"] else "Not testable (positive control failed)"
    S["underpowered"] = min(e["n_lost"], e["n_intact"]) < 4
    for g in ("RIOK1", "WDR77"):
        for kind in ("rnai", "crispr"):
            S["secondary"][f"{g} {kind}"] = {"all_lines": cmp(known, f"{g}_{kind}"), "osteosarcoma": cmp(osl, f"{g}_{kind}")}
    bycn = t[t["mtap_lost_by_cn"].notna() & t["osteosarcoma"]].copy()
    S["secondary"]["MTAP status by copy number, osteosarcoma"] = {lab: cmp(bycn, col, "mtap_lost_by_cn") for lab, col in MEASURES}
    S["n_lines"] = {"all_with_mtap_status": int(len(known)), "all_mtap_lost": int(known["mtap_lost"].sum()),
                    "osteosarcoma": int(len(osl)), "osteosarcoma_mtap_lost": int(osl["mtap_lost"].sum())}
    json.dump(S, open(os.path.join(out, "summary.json"), "w"), indent=1, default=float)
    cols = ["name", "disease", "subtype", "primary_or_metastasis", "mtap_lost", "MTAP_expr", "MTAP_cn", "CDKN2A_expr", "CDKN2A_cn",
            "PRMT5_rnai", "MAT2A_rnai", "PRMT5_crispr", "MAT2A_crispr", "RIOK1_crispr", "WDR77_crispr"]
    t[t["osteosarcoma"]].sort_values("MTAP_expr")[cols].round(3).to_csv(os.path.join(out, "lines.csv"))
    with open(os.path.join(out, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["set", "measure", "mtap_lost_lines", "mtap_intact_lines", "mean_lost", "mean_intact", "difference", "ci_low", "ci_high", "p"])
        for setname in ("positive_control", "osteosarcoma", "sarcoma"):
            for lab, v in S[setname].items():
                w.writerow([setname, lab, v["n_lost"], v["n_intact"]] + [f"{v[k]:.3f}" if v.get(k) is not None else "" for k in ("mean_lost", "mean_intact", "diff", "lo", "hi", "p")])
    col = dict(MEASURES)[primary]
    f_ = osl["mtap_lost"]
    strip_svg([("MTAP lost", [(r["name"], r[col]) for _, r in osl[f_].iterrows() if not np.isnan(r[col])], "#1c5cab"),
               ("MTAP intact", [(r["name"], r[col]) for _, r in osl[~f_].iterrows() if not np.isnan(r[col])], "#6a7384")],
              os.path.join(FIG, "engine05_mtap_primary.svg"), f"Osteosarcoma cell lines: {primary}",
              ("Each row is one cell line. Further left means the cells suffer more when the gene is removed.", "Dashed lines are group averages."),
              "dependency score")
    print("\n===== CYCLE 5: MTAP and PRMT5 / MAT2A")
    print("lines:", S["n_lines"], "| control passed:", S["control_passed"])
    for setname in ("positive_control", "osteosarcoma", "sarcoma"):
        for lab, v in S[setname].items():
            ci = f'({v["lo"]:+.3f} to {v["hi"]:+.3f}) p={v["p"]:.3g}' if v.get("lo") is not None else ""
            print(f'  {setname:16s} {lab:26s} lost {v["n_lost"]:4d} intact {v["n_intact"]:4d} diff {v["diff"] if v["diff"] is None else round(v["diff"], 3)} {ci}')
    print("PRIMARY:", primary, "| D =", round(ref, 3), "| VERDICT:", S["verdict"], "| underpowered:", S["underpowered"])
    for k, v in S["secondary"].items():
        print("  secondary", k, json.dumps(v, default=lambda x: round(x, 3))[:400])
    print(t[t["osteosarcoma"]].sort_values("MTAP_expr")[["name", "mtap_lost", "MTAP_expr", "MTAP_cn", "CDKN2A_cn", "PRMT5_rnai", "MAT2A_rnai", "PRMT5_crispr", "MAT2A_crispr"]].round(2).to_string())


def cycle6(t):
    out = os.path.join(ROOT, "data", "engine", "cycle06")
    os.makedirs(out, exist_ok=True)
    osl, sar = t[t["osteosarcoma"]], t[t["sarcoma_lineage"]]
    S = {"positive_control": {}, "osteosarcoma": {}, "sarcoma": {}, "secondary": {}}
    S["positive_control"]["slope_on_expression"] = slope(t["CCNE1_expr"], t["PKMYT1_crispr"])
    amp = t[t["ccne1_amplified"].notna()]
    a = amp["ccne1_amplified"].astype(bool)
    S["positive_control"]["amplified_vs_not"] = welch(amp.loc[a, "PKMYT1_crispr"], amp.loc[~a, "PKMYT1_crispr"])
    pc = S["positive_control"]
    S["control_passed"] = bool((pc["slope_on_expression"].get("hi") is not None and pc["slope_on_expression"]["hi"] < 0)
                               or (pc["amplified_vs_not"].get("hi") is not None and pc["amplified_vs_not"]["hi"] < 0))
    e = slope(osl["CCNE1_expr"], osl["PKMYT1_crispr"])
    S["osteosarcoma"]["slope_on_expression"] = e
    B = pc["slope_on_expression"].get("slope")
    S["reference_slope_B"] = B
    S["verdict"] = verdict(e.get("slope"), e.get("lo"), e.get("hi"), B) if S["control_passed"] else "Not testable (positive control failed)"
    S["underpowered"] = e["n"] < 10
    S["osteosarcoma"]["slope_on_copy_number"] = slope(osl["CCNE1_cn"], osl["PKMYT1_crispr"])
    oa = osl[osl["ccne1_amplified"].notna()]
    fa = oa["ccne1_amplified"].astype(bool)
    S["osteosarcoma"]["amplified_lines"] = [str(x) for x in oa.loc[fa, "name"]]
    S["osteosarcoma"]["amplified_vs_not"] = welch(oa.loc[fa, "PKMYT1_crispr"], oa.loc[~fa, "PKMYT1_crispr"]) if fa.sum() >= 2 else {"n_amplified": int(fa.sum())}
    S["sarcoma"]["slope_on_expression"] = slope(sar["CCNE1_expr"], sar["PKMYT1_crispr"])
    for g in ("WEE1", "CDK2"):
        S["secondary"][g] = {"all_lines": slope(t["CCNE1_expr"], t[f"{g}_crispr"]), "osteosarcoma": slope(osl["CCNE1_expr"], osl[f"{g}_crispr"])}
    json.dump(S, open(os.path.join(out, "summary.json"), "w"), indent=1, default=float)
    cols = ["name", "disease", "subtype", "CCNE1_expr", "CCNE1_cn", "ccne1_amplified", "PKMYT1_crispr", "WEE1_crispr", "CDK2_crispr"]
    osl.sort_values("CCNE1_expr", ascending=False)[cols].round(3).to_csv(os.path.join(out, "lines.csv"))
    with open(os.path.join(out, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["set", "analysis", "lines", "slope", "ci_low", "ci_high", "p", "spearman_rho", "spearman_p"])
        for setname, key in (("all cell lines", pc["slope_on_expression"]), ("osteosarcoma", e), ("osteosarcoma, copy number", S["osteosarcoma"]["slope_on_copy_number"]),
                             ("bone and soft-tissue lines", S["sarcoma"]["slope_on_expression"])):
            w.writerow([setname, "PKMYT1 knockout score on CCNE1", key.get("n")] + [f"{key[k]:.4f}" if key.get(k) is not None else "" for k in ("slope", "lo", "hi", "p", "spearman_rho", "spearman_p")])
    pts = [(r["name"], r["CCNE1_expr"], r["PKMYT1_crispr"], bool(r["ccne1_amplified"]) if not pd.isna(r["ccne1_amplified"]) else False)
           for _, r in osl.iterrows() if not (np.isnan(r["CCNE1_expr"]) or np.isnan(r["PKMYT1_crispr"]))]
    fit = None
    if e.get("slope") is not None:
        xm, ym = np.mean([p[1] for p in pts]), np.mean([p[2] for p in pts])
        fit = (e["slope"], ym - e["slope"] * xm)
    scatter_svg(pts, fit, os.path.join(FIG, "engine06_ccne1_pkmyt1.svg"), "Osteosarcoma cell lines: CCNE1 level against dependence on PKMYT1",
                ("Each dot is one cell line. Lower means the cells suffer more when PKMYT1 is knocked out.", "Gold dots have CCNE1 amplification. The dashed line is the fitted trend."),
                "CCNE1 RNA, log2(TPM+1)", "PKMYT1 gene effect (Chronos)")
    print("\n===== CYCLE 6: CCNE1 and PKMYT1")
    print("control:", json.dumps(pc, default=lambda x: round(x, 4)), "passed:", S["control_passed"])
    print("osteosarcoma slope:", json.dumps(e, default=lambda x: round(x, 4)))
    print("osteosarcoma by copy number:", json.dumps(S["osteosarcoma"]["slope_on_copy_number"], default=lambda x: round(x, 4)))
    print("amplified OS lines:", S["osteosarcoma"]["amplified_lines"], json.dumps(S["osteosarcoma"]["amplified_vs_not"], default=lambda x: round(x, 4)))
    print("sarcoma lineage slope:", json.dumps(S["sarcoma"]["slope_on_expression"], default=lambda x: round(x, 4)))
    print("B =", B, "| VERDICT:", S["verdict"], "| underpowered:", S["underpowered"])
    print("secondary:", json.dumps(S["secondary"], default=lambda x: round(x, 4)))
    print(osl.sort_values("CCNE1_expr", ascending=False)[cols].round(2).to_string())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
    else:
        os.makedirs(FIG, exist_ok=True)
        table = load()
        cycle5(table)
        cycle6(table)
