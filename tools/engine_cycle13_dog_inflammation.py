#!/usr/bin/env python3
"""Engine cycle 13: in pet dogs with osteosarcoma, does tumour inflammation go with faster relapse?

Pre-registered in research_notes/Engine/cycle-13-dog-inflammation/PREREGISTRATION.md (commit 4e10b3b).

  python3 tools/engine_cycle13_dog_inflammation.py fetch   # GEO GSE180303 series matrix and GPL3738 annotation
  python3 tools/engine_cycle13_dog_inflammation.py         # analysis

Outputs: data/engine/cycle13/results.csv, summary.json, docs/figures/engine13_dogs.svg
"""
import csv
import gzip
import json
import os
import subprocess
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import survival_analysis as sa          # noqa: E402  (shared, tested Cox code)

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle13", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle13")
FIG = os.path.join(ROOT, "docs", "figures")
URLS = {"GSE180303_series_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE180nnn/GSE180303/matrix/GSE180303_series_matrix.txt.gz",
        "GPL3738.annot.gz": "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL3nnn/GPL3738/annot/GPL3738.annot.gz"}
INFL = ["IL6", "IL1B", "CXCL8"]
SYN = {"CXCL8": ("CXCL8", "IL8")}
OTHER = ["DKK1", "PTK2", "IL1A"]


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for name, url in URLS.items():
        subprocess.run(["curl", "-sS", "-f", "-L", "--retry", "3", "-o", os.path.join(RAW, name), url], check=True)
        print(name, os.path.getsize(os.path.join(RAW, name)))


def load():
    meta, rows, ids, in_table = {}, {}, None, False
    with gzip.open(os.path.join(RAW, "GSE180303_series_matrix.txt.gz"), "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p[0] == "!series_matrix_table_begin":
                in_table = True
                continue
            if p[0] == "!series_matrix_table_end":
                break
            if not in_table:
                if p[0] in ("!Sample_title", "!Sample_geo_accession"):
                    meta[p[0]] = [v.strip('"') for v in p[1:]]
                elif p[0] == "!Sample_characteristics_ch1":
                    vals = [v.strip('"') for v in p[1:]]
                    meta[vals[0].split(":")[0]] = [v.split(": ", 1)[-1] for v in vals]
            elif ids is None:
                ids = [v.strip('"') for v in p[1:]]
            else:
                try:
                    rows[p[0].strip('"')] = np.array([float(v) if v not in ("", "null") else np.nan for v in p[1:]])
                except ValueError:
                    pass
    return meta, ids, rows


def probes():
    want = {g: (SYN.get(g, (g,))) for g in INFL + OTHER}
    out = {g: [] for g in want}
    with gzip.open(os.path.join(RAW, "GPL3738.annot.gz"), "rt", encoding="utf-8", errors="replace") as f:
        header = None
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p[0] == "ID":
                header = p
                continue
            if header is None or len(p) < 3:
                continue
            syms = set(p[2].split("///")) if p[2] else set()
            for g, names in want.items():
                if syms & set(names):
                    out[g].append(p[0])
    return out


def z(v):
    v = np.asarray(v, float)
    return (v - np.nanmean(v)) / np.nanstd(v, ddof=1)


def cox(x, t, e, covars=None):
    m = ~np.isnan(x) & ~np.isnan(t)
    if covars is not None:
        m &= ~np.isnan(covars)
    X = z(x[m])[:, None]
    if covars is not None:
        X = np.column_stack([X, z(covars[m])])
    r = sa.cox(X, t[m], e[m])
    return {"hr": float(r["hr"][0]), "lo": float(r["lo"][0]), "hi": float(r["hi"][0]), "p": float(r["p"][0]),
            "n": int(m.sum()), "events": int(e[m].sum()), "converged": bool(r["converged"])}


def logistic(x, y):
    m = ~np.isnan(x)
    X = np.column_stack([np.ones(m.sum()), z(x[m])])
    yy = y[m].astype(float)
    b = np.zeros(2)
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None])
        step = np.linalg.solve(H, X.T @ (yy - p))
        b += step
        if np.max(np.abs(step)) < 1e-8:
            break
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return {"or": float(np.exp(b[1])), "lo": float(np.exp(b[1] - 1.96 * se[1])), "hi": float(np.exp(b[1] + 1.96 * se[1])),
            "p": float(2 * stats.norm.sf(abs(b[1] / se[1]))), "n": int(m.sum()), "events": int(yy.sum())}


def verdict(r):
    if r["lo"] > 1 and r["hr"] > 1:
        return "Supported"
    if r["hi"] < 1.3:
        return "Refuted"
    return "Inconclusive"


def forest(rows, path):
    W, top, rh, left = 860, 64, 30, 330
    H = top + rh * len(rows) + 56
    lo_ax, hi_ax = 0.25, 4.0
    X = lambda v: left + (np.log(min(max(v, lo_ax), hi_ax)) - np.log(lo_ax)) / (np.log(hi_ax) - np.log(lo_ax)) * (W - left - 170)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="13" role="img" '
         f'aria-label="Hazard ratios for faster progression in 59 pet dogs with osteosarcoma">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="26" font-weight="600" fill="#1d2430">Faster progression in 59 pet dogs: hazard ratio per standard deviation</text>',
         '<text x="16" y="44" fill="#525b6b" font-size="12">95% CI, log scale. Right of 1: faster progression with more of the measure.</text>']
    for v in (0.25, 0.5, 1, 2, 4):
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{H - 46}" stroke="{"#525b6b" if v == 1 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{H - 30}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    for i, (label, r, col) in enumerate(rows):
        y = top + rh * i + rh / 2
        s.append(f'<text x="16" y="{y + 4:.1f}" fill="#1d2430">{label}</text>')
        s.append(f'<line x1="{X(r["lo"]):.1f}" y1="{y:.1f}" x2="{X(r["hi"]):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<circle cx="{X(r["hr"]):.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
        s.append(f'<text x="{W - 10}" y="{y + 4:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{r["hr"]:.2f} ({r["lo"]:.2f}–{r["hi"]:.2f})</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    meta, ids, rows = load()
    pr = probes()
    titles = meta["!Sample_title"]
    dogs = sorted({t.split(" ")[0] for t in titles})
    col_of = {gsm: i for i, gsm in enumerate(ids)}
    gsm = meta["!Sample_geo_accession"]
    allv = np.vstack([v for v in rows.values()])
    log = np.nanmax(allv) > 100
    S = {"preregistration_commit": "4e10b3b", "arrays": len(ids), "dogs": len(dogs), "log2_applied": bool(log), "probes": {}}

    def gene_by_dog(g):
        cand = [p for p in pr[g] if p in rows]
        if not cand:
            return None
        mats = {p: (np.log2(np.clip(rows[p], 1e-3, None)) if log else rows[p]) for p in cand}
        best = max(cand, key=lambda p: np.nanmean(mats[p]))
        S["probes"][g] = {"chosen": best, "candidates": cand}
        v = mats[best]
        return np.array([np.nanmean([v[col_of[gsm[i]]] for i, t in enumerate(titles) if t.split(" ")[0] == d]) for d in dogs])

    def clin(key, cast=float):
        out = []
        for d in dogs:
            i = [k for k, t in enumerate(titles) if t.split(" ")[0] == d][0]
            try:
                out.append(cast(meta[key][i]))
            except (ValueError, KeyError):
                out.append(np.nan)
        return np.array(out, float)

    ttp, os_ = clin("time to progression (days)"), clin("overall survival (days)")
    t = np.minimum(ttp, os_)
    e = np.where((ttp == os_) & (ttp >= 365), 0, 1).astype(float)
    y1 = (ttp < 365).astype(float)
    alp = np.log(clin("alkaline phosphatase levels"))
    mono = clin("monocyte counts (1000 cells/μl)")
    S["events"], S["progressed_within_year"] = int(e.sum()), int(y1.sum())

    genes = {g: gene_by_dog(g) for g in INFL + OTHER}
    present = [g for g in INFL if genes[g] is not None]
    S["inflammation_genes_used"] = present
    infl = np.nanmean(np.vstack([z(genes[g]) for g in present]), axis=0) if len(present) >= 2 else None

    res, out = {}, []

    def add(name, kind, x, covars=None, mask=None):
        tt, ee, xx, yy = t, e, x, y1
        cv = covars
        if mask is not None:
            tt, ee, xx, yy = t[mask], e[mask], x[mask], y1[mask]
            cv = covars[mask] if covars is not None else None
        r = cox(xx, tt, ee, cv)
        lg = logistic(xx, yy)
        res[name] = {"cox": r, "one_year_logistic": lg}
        out.append([kind, name, r["n"], r["events"], f'{r["hr"]:.3f}', f'{r["lo"]:.3f}', f'{r["hi"]:.3f}', f'{r["p"]:.4f}',
                    f'{lg["or"]:.3f}', f'{lg["lo"]:.3f}', f'{lg["hi"]:.3f}'])
        return r

    chk = add("log alkaline phosphatase", "check", alp)
    add("monocyte count", "check (secondary)", mono)
    S["check_alp_hr_above_1"] = chk["hr"] > 1
    tests = {}
    if infl is not None:
        tests["H1"] = add("inflammation score (IL6, IL1B, CXCL8)", "H1", infl)
    for h, g in (("H2", "DKK1"), ("H3", "PTK2")):
        if genes[g] is not None:
            tests[h] = add(g, h, genes[g])
    for g in INFL + ["IL1A"]:
        if genes[g] is not None:
            add(g, "single gene (secondary)", genes[g])
    certain = ~((ttp == os_) & (ttp < 365))
    if infl is not None:
        add("inflammation score, excluding 9 least-certain events", "sensitivity", infl, mask=certain)
        add("inflammation score, adjusted for log ALP", "adjusted", infl, covars=alp)
    for g in ("DKK1", "PTK2"):
        if genes[g] is not None:
            add(f"{g}, adjusted for log ALP", "adjusted", genes[g], covars=alp)
    S["verdicts"] = {h: verdict(r) for h, r in tests.items()}
    S["results"] = res
    S["P38"] = "right" if (chk["hr"] > 1 and chk["lo"] > 1) else "wrong"
    S["P39"] = "right" if S["verdicts"].get("H1") == "Supported" else "wrong"
    S["P40"] = "right" if S["verdicts"].get("H2") == "Supported" else "wrong"
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kind", "measure", "dogs", "events", "hr_per_sd", "hr_lo", "hr_hi", "p", "one_year_or_per_sd", "or_lo", "or_hi"])
        w.writerows(out)
    fr = [("Check: alkaline phosphatase (log)", res["log alkaline phosphatase"]["cox"], "#6a7384"),
          ("Check: monocyte count", res["monocyte count"]["cox"], "#6a7384")]
    if "H1" in tests:
        fr.append(("H1: inflammation score", tests["H1"], "#1c5cab"))
    for h, g in (("H2", "DKK1"), ("H3", "PTK2")):
        if h in tests:
            fr.append((f"{h}: {g}", tests[h], "#1c5cab"))
    for g in INFL:
        if genes[g] is not None:
            fr.append((f"   {g} alone", res[g]["cox"], "#9aa3b2"))
    forest(fr, os.path.join(FIG, "engine13_dogs.svg"))
    for row in out:
        print(row)
    print("probes:", S["probes"])
    print("verdicts:", S["verdicts"], "events", S["events"], "1-yr", S["progressed_within_year"], "log2", log)


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
