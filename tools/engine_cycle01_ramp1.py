#!/usr/bin/env python3
"""Engine cycle 1: does tumour RAMP1 RNA predict relapse in independent osteosarcoma cohorts?

Runs the analysis pre-registered in research_notes/Engine/cycle-01-ramp1/PREREGISTRATION.md
(committed before any independent cohort was downloaded).

Step 0  reproduce the discovery association in TARGET-OS (source of the hypothesis, not a test)
Step 1  per-cohort Cox models in independent GEO cohorts, RAMP1 per standard deviation
Step 2  fixed-effect inverse-variance meta-analysis, random-effects sensitivity, verdict
Step 3  secondary genes (CALCRL, SP7, SOST) and overall survival where available

Inputs (from the repository root):
  data/survival_raw/patients.csv, data/surface_targets_raw/  TARGET-OS (see tools/survival_analysis.py)
  data/engine/cycle01/raw/  GEO series matrices and platform tables, downloaded from
      https://ftp.ncbi.nlm.nih.gov/geo/series/... and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi
Outputs:
  data/engine/cycle01/results.csv, data/engine/cycle01/summary.json, docs/figures/engine01_*.svg
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
import survival_analysis as sa          # noqa: E402  (shared, tested Cox and KM code)

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle01", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle01")
FIG = os.path.join(ROOT, "docs", "figures")
GENES = ["RAMP1", "CALCRL", "SP7", "SOST"]


# ------------------------------------------------------------------ helpers
def zscore(v):
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std(ddof=1)


def cox_one(x, t, e, covars=None):
    X = zscore(x)[:, None]
    if covars is not None:
        X = np.column_stack([X, covars])
    r = sa.cox(X, t, e)
    return {"hr": float(r["hr"][0]), "lo": float(r["lo"][0]), "hi": float(r["hi"][0]),
            "p": float(r["p"][0]), "beta": float(r["beta"][0]), "se": float(r["se"][0]),
            "n": int(len(t)), "events": int(np.sum(e)), "converged": bool(r["converged"])}


def read_matrix(path):
    """Characteristics (list of dicts per sample), sample ids and expression {probe: [values]}."""
    chars, ids, expr, in_table = [], [], {}, False
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("!Sample_geo_accession"):
                ids = [v.strip('"') for v in line.split("\t")[1:]]
                chars = [dict() for _ in ids]
            elif line.startswith("!Sample_characteristics_ch1"):
                for i, v in enumerate(line.split("\t")[1:]):
                    v = v.strip('"')
                    if ":" in v:
                        k, val = v.split(":", 1)
                        chars[i][k.strip().lower()] = val.strip()
            elif line.startswith("!series_matrix_table_begin"):
                in_table = True
            elif line.startswith("!series_matrix_table_end"):
                break
            elif in_table and not line.startswith('"ID_REF"'):
                p = line.split("\t")
                try:
                    expr[p[0].strip('"')] = np.array([float(x) if x not in ("", "null", "NA") else np.nan for x in p[1:]])
                except ValueError:
                    continue
    return ids, chars, expr


def probe_map(platform, genes):
    """{gene: [probe ids]} from a GEO platform table or annotation file."""
    if platform == "GPL96":
        fh, sym_col = gzip.open(os.path.join(RAW, "GPL96.annot.gz"), "rt", errors="replace"), "Gene symbol"
    else:
        fh, sym_col = open(os.path.join(RAW, f"{platform}.platform.txt"), errors="replace"), "Symbol"
    out, hdr = {g: [] for g in genes}, None
    for line in fh:
        if hdr is None:
            if line.startswith("ID\t"):
                hdr = line.rstrip("\n").split("\t")
                ix = hdr.index(sym_col)
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) <= ix:
            continue
        syms = [s.strip() for s in re.split(r"///|,", p[ix])]
        for g in genes:
            if g in syms:
                out[g].append(p[0])
    fh.close()
    return out


def gene_values(expr, probes):
    """Pre-specified rule: the probe with the highest mean expression; log2 if not on log scale."""
    best, best_mean = None, -np.inf
    for pr in probes:
        if pr in expr:
            m = np.nanmean(expr[pr])
            if m > best_mean:
                best, best_mean = pr, m
    if best is None:
        return None, None
    v = expr[best].astype(float)
    if np.nanmax(v) > 100:                  # not log scale
        v = np.log2(np.clip(v, 1, None))
    return best, v


# ------------------------------------------------------------------ cohorts
def cohort_gse21257():
    ids, chars, expr = read_matrix(os.path.join(RAW, "GSE21257_series_matrix.txt.gz"))
    rows = []
    for i, c in enumerate(chars):
        g, s = c["group"], c["status"]
        follow = float(re.search(r"(\d+) months", s).group(1))
        died = s.lower().startswith("deceased")
        if g.startswith("Metastases present at diagnosis"):
            met_dx, mfs_t, mfs_e = 1, None, None
        elif g.startswith("Metastases at"):
            met_dx, mfs_t, mfs_e = 0, float(re.search(r"at (\d+) months", g).group(1)), 1
        else:
            met_dx, mfs_t, mfs_e = 0, follow, 0
        rows.append({"i": i, "met_dx": met_dx, "mfs_t": mfs_t, "mfs_e": mfs_e, "os_t": follow, "os_e": int(died)})
    return "GSE21257", "GPL10295", ids, expr, rows


def cohort_gse16091():
    ids, chars, expr = read_matrix(os.path.join(RAW, "GSE16091_series_matrix.txt.gz"))
    rows = [{"i": i, "met_dx": None, "os_t": float(c["days-followup"]) / 30.44, "os_e": int(c["alive-or-dead"] == "D")}
            for i, c in enumerate(chars)]
    return "GSE16091", "GPL96", ids, expr, rows


def cohort_gse39055():
    ids, chars, expr = read_matrix(os.path.join(RAW, "GSE39055_series_matrix.txt.gz"))
    rows = []
    for i, c in enumerate(chars):
        tkey = [k for k in c if k.startswith("time until first recurrence")][0]
        rows.append({"i": i, "met_dx": None, "rfs_t": float(c[tkey]), "rfs_e": int(c["recurrence"] == "Y"),
                     "death": int(c["death"] == "Y")})
    return "GSE39055", "GPL14951", ids, expr, rows


# ------------------------------------------------------------------ analysis
def target_discovery():
    pts = [p for p in sa.load_patients() if p.get("efs_days") is not None and p.get("efs_event") is not None]
    rna = sa.rna_values(GENES)
    pts = [p for p in pts if p["case"] in rna and "RAMP1" in rna[p["case"]] and p.get("metastatic") is not None]
    t = np.array([p["efs_days"] / 30.44 for p in pts])
    e = np.array([int(p["efs_event"]) for p in pts])
    m = np.array([p["metastatic"] for p in pts], float)
    out = {}
    for g in GENES:
        x = np.array([rna[p["case"]].get(g, np.nan) for p in pts])
        ok = ~np.isnan(x)
        out[g] = cox_one(x[ok], t[ok], e[ok], covars=m[ok][:, None])
    return out


def run_cohort(loader):
    name, plat, ids, expr, rows = loader()
    pmap = probe_map(plat, GENES)
    res = {"cohort": name, "platform": plat, "probes": {}}
    vals = {}
    for g in GENES:
        pr, v = gene_values(expr, pmap[g])
        res["probes"][g] = {"chosen": pr, "candidates": len(pmap[g])}
        vals[g] = v
    if name == "GSE21257":
        sel = [r for r in rows if r["met_dx"] == 0]
        prim = ("metastasis-free survival", [r["mfs_t"] for r in sel], [r["mfs_e"] for r in sel], None,
                "patients without metastasis at diagnosis (restriction in place of adjustment; see Deviations)")
        sec = ("overall survival", [r["os_t"] for r in rows], [r["os_e"] for r in rows],
               np.array([[r["met_dx"]] for r in rows], float), "all patients, adjusted for metastasis at diagnosis")
        sec_rows = rows
    elif name == "GSE16091":
        sel = rows
        prim = ("overall survival", [r["os_t"] for r in sel], [r["os_e"] for r in sel], None,
                "all patients; metastasis at diagnosis not recorded, unadjusted")
        sec, sec_rows = None, None
    else:
        sel = rows
        prim = ("recurrence-free survival", [r["rfs_t"] for r in sel], [r["rfs_e"] for r in sel], None,
                "all patients; metastasis at diagnosis not recorded, unadjusted")
        sec, sec_rows = None, None
    idx = [r["i"] for r in sel]
    res["endpoint"], res["population"] = prim[0], prim[4]
    res["primary"] = {}
    for g in GENES:
        if vals[g] is None:
            continue
        x = vals[g][idx]
        ok = ~np.isnan(x)
        res["primary"][g] = cox_one(x[ok], np.array(prim[1])[ok], np.array(prim[2])[ok])
    if sec:
        sidx = [r["i"] for r in sec_rows]
        x = vals["RAMP1"][sidx]
        res["secondary_os"] = cox_one(x, np.array(sec[1]), np.array(sec[2]), covars=sec[3])
        res["secondary_os"]["population"] = sec[4]
    # median split for the figure (display only)
    x = vals["RAMP1"][idx]
    res["km"] = {"t": list(map(float, prim[1])), "e": list(map(int, prim[2])), "high": list(map(bool, x > np.median(x)))}
    return res


def meta(effects):
    b = np.array([e["beta"] for e in effects])
    se = np.array([e["se"] for e in effects])
    w = 1 / se ** 2
    bf = float((w * b).sum() / w.sum())
    sef = float(math.sqrt(1 / w.sum()))
    q = float((w * (b - bf) ** 2).sum())
    k = len(b)
    tau2 = max(0.0, (q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0
    wr = 1 / (se ** 2 + tau2)
    br = float((wr * b).sum() / wr.sum())
    ser = float(math.sqrt(1 / wr.sum()))
    i2 = max(0.0, (q - (k - 1)) / q) if q > 0 and k > 1 else 0.0
    z = 1.959964
    return {"fixed": {"hr": math.exp(bf), "lo": math.exp(bf - z * sef), "hi": math.exp(bf + z * sef),
                      "p": float(2 * stats.norm.sf(abs(bf / sef)))},
            "random": {"hr": math.exp(br), "lo": math.exp(br - z * ser), "hi": math.exp(br + z * ser),
                       "p": float(2 * stats.norm.sf(abs(br / ser)))},
            "Q": q, "I2": i2, "tau2": tau2, "k": k}


def verdict(m, events):
    hr, lo, hi = m["fixed"]["hr"], m["fixed"]["lo"], m["fixed"]["hi"]
    if lo > 1.0 and hr >= 1.3:
        v = "Replicated"
    elif hi < 1.3:
        v = "Refuted"
    else:
        v = "Inconclusive"
    return v, (events < 48)


# ------------------------------------------------------------------ figures
def forest_svg(rows, path, title):
    """Plain SVG forest plot on a log axis. rows: (label, hr, lo, hi, kind)."""
    W, rowh, left, right = 760, 34, 300, 60
    H = 70 + rowh * len(rows) + 40
    lo_ax, hi_ax = 0.25, 8.0
    def X(v):
        return left + (math.log(v) - math.log(lo_ax)) / (math.log(hi_ax) - math.log(lo_ax)) * (W - left - right)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="14">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">{title}</text>',
         f'<text x="16" y="50" font-size="13" fill="#525b6b">Hazard ratio per standard deviation of tumour RAMP1 RNA, 95% CI, log scale. Right of 1 = higher RAMP1, worse outcome.</text>']
    top = 70
    for v in (0.25, 0.5, 1, 2, 4, 8):
        x = X(v)
        s.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{top + rowh * len(rows)}" stroke="{"#525b6b" if v == 1 else "#e2e5ea"}" stroke-width="{1.5 if v == 1 else 1}"/>')
        s.append(f'<text x="{x:.1f}" y="{top + rowh * len(rows) + 20}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    x13 = X(1.3)
    s.append(f'<line x1="{x13:.1f}" y1="{top - 6}" x2="{x13:.1f}" y2="{top + rowh * len(rows)}" stroke="#a3401a" stroke-dasharray="4 4"/>')
    s.append(f'<text x="{x13 + 4:.1f}" y="{top - 10}" fill="#a3401a" font-size="12">pre-registered bar, 1.3</text>')
    for k, (lab, hr, lo, hi, kind) in enumerate(rows):
        y = top + rowh * k + rowh / 2
        col = {"discovery": "#6a7384", "cohort": "#1c5cab", "pooled": "#14264a"}[kind]
        s.append(f'<text x="16" y="{y + 5:.1f}" fill="#14181f" font-weight="{600 if kind == "pooled" else 400}">{lab}</text>')
        s.append(f'<line x1="{X(max(lo, lo_ax)):.1f}" y1="{y:.1f}" x2="{X(min(hi, hi_ax)):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        if kind == "pooled":
            s.append(f'<path d="M{X(hr) - 9:.1f},{y:.1f} L{X(hr):.1f},{y - 8:.1f} L{X(hr) + 9:.1f},{y:.1f} L{X(hr):.1f},{y + 8:.1f} Z" fill="{col}"/>')
        else:
            s.append(f'<rect x="{X(hr) - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="{col}"/>')
        s.append(f'<text x="{W - 8}" y="{y + 5:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{hr:.2f} ({lo:.2f}–{hi:.2f})</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(FIG, exist_ok=True)
    disc = target_discovery()
    cohorts = [run_cohort(f) for f in (cohort_gse21257, cohort_gse16091, cohort_gse39055)]
    prim = [c["primary"]["RAMP1"] for c in cohorts]
    events_all = sum(p["events"] for p in prim)
    m_all = meta(prim)
    m_wo = meta([c["primary"]["RAMP1"] for c in cohorts if c["cohort"] != "GSE39055"])
    v_all, under_all = verdict(m_all, events_all)
    ev_wo = sum(c["primary"]["RAMP1"]["events"] for c in cohorts if c["cohort"] != "GSE39055")
    v_wo, under_wo = verdict(m_wo, ev_wo)
    sec_meta = {g: meta([c["primary"][g] for c in cohorts if g in c["primary"]]) for g in ("CALCRL", "SP7", "SOST")}

    summary = {"discovery_TARGET": disc, "cohorts": cohorts, "meta_primary": m_all, "events_primary": events_all,
               "verdict_primary": v_all, "underpowered_primary": under_all,
               "meta_without_GSE39055": m_wo, "events_without_GSE39055": ev_wo,
               "verdict_without_GSE39055": v_wo, "underpowered_without_GSE39055": under_wo,
               "secondary_genes_meta": sec_meta}
    json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)

    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["analysis", "cohort", "gene", "endpoint", "population", "n", "events", "hr_per_sd", "ci_low", "ci_high", "p", "probe"])
        for g, r in disc.items():
            w.writerow(["discovery", "TARGET-OS", g, "event-free survival", "all with RNA, adjusted for metastasis at diagnosis",
                        r["n"], r["events"], f'{r["hr"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.2e}', "STAR TPM"])
        for c in cohorts:
            for g, r in c["primary"].items():
                w.writerow(["independent", c["cohort"], g, c["endpoint"], c["population"], r["n"], r["events"],
                            f'{r["hr"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.2e}', c["probes"][g]["chosen"]])
            if "secondary_os" in c:
                r = c["secondary_os"]
                w.writerow(["secondary", c["cohort"], "RAMP1", "overall survival", r["population"], r["n"], r["events"],
                            f'{r["hr"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.2e}', c["probes"]["RAMP1"]["chosen"]])
        for lab, m in (("pooled (fixed)", m_all["fixed"]), ("pooled (random)", m_all["random"]),
                       ("pooled without GSE39055 (fixed)", m_wo["fixed"])):
            w.writerow(["meta", lab, "RAMP1", "primary end points", "", "", "", f'{m["hr"]:.3f}', f'{m["lo"]:.3f}', f'{m["hi"]:.3f}', f'{m["p"]:.2e}', ""])

    d = disc["RAMP1"]
    rows = [(f"TARGET-OS, discovery ({d['n']} pts, {d['events']} events)", d["hr"], d["lo"], d["hi"], "discovery")]
    for c in cohorts:
        r = c["primary"]["RAMP1"]
        rows.append((f"{c['cohort']} ({r['n']} pts, {r['events']} events)", r["hr"], r["lo"], r["hi"], "cohort"))
    rows.append((f"Independent cohorts pooled ({events_all} events)", m_all["fixed"]["hr"], m_all["fixed"]["lo"], m_all["fixed"]["hi"], "pooled"))
    rows.append((f"Pooled without GSE39055 ({ev_wo} events)", m_wo["fixed"]["hr"], m_wo["fixed"]["lo"], m_wo["fixed"]["hi"], "pooled"))
    forest_svg(rows, os.path.join(FIG, "engine01_ramp1_forest.svg"), "Tumour RAMP1 and relapse: discovery and independent cohorts")

    print(f"DISCOVERY TARGET-OS RAMP1: HR {d['hr']:.2f} ({d['lo']:.2f}-{d['hi']:.2f}) p={d['p']:.1e} n={d['n']} events={d['events']}")
    for c in cohorts:
        r = c["primary"]["RAMP1"]
        print(f"{c['cohort']:9s} {c['endpoint']:26s} n={r['n']:3d} ev={r['events']:2d} HR {r['hr']:.2f} ({r['lo']:.2f}-{r['hi']:.2f}) p={r['p']:.3f} probe={c['probes']['RAMP1']}")
    print(f"POOLED fixed  HR {m_all['fixed']['hr']:.2f} ({m_all['fixed']['lo']:.2f}-{m_all['fixed']['hi']:.2f}) p={m_all['fixed']['p']:.3f}  I2={m_all['I2']:.2f}  events={events_all}")
    print(f"POOLED random HR {m_all['random']['hr']:.2f} ({m_all['random']['lo']:.2f}-{m_all['random']['hi']:.2f})")
    print(f"VERDICT: {v_all}{' (underpowered)' if under_all else ''}")
    print(f"WITHOUT GSE39055: HR {m_wo['fixed']['hr']:.2f} ({m_wo['fixed']['lo']:.2f}-{m_wo['fixed']['hi']:.2f}) events={ev_wo} -> {v_wo}{' (underpowered)' if under_wo else ''}")
    for g, m in sec_meta.items():
        print(f"secondary {g:7s} pooled HR {m['fixed']['hr']:.2f} ({m['fixed']['lo']:.2f}-{m['fixed']['hi']:.2f}) p={m['fixed']['p']:.3f}")
    for c in cohorts:
        if "secondary_os" in c:
            r = c["secondary_os"]
            print(f"secondary OS {c['cohort']}: HR {r['hr']:.2f} ({r['lo']:.2f}-{r['hi']:.2f}) p={r['p']:.3f} n={r['n']} ev={r['events']}")


if __name__ == "__main__":
    main()
