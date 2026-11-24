#!/usr/bin/env python3
"""Engine cycle 2: do osteosarcoma lung metastases carry more CXCR4 and less CXCL12 than primary tumours?

Runs the analysis pre-registered in research_notes/Engine/cycle-02-cxcr4/PREREGISTRATION.md
(plan committed before the dataset search; dataset choices committed before any expression value was read).

Step 1  per-dataset effect: Hedges' g, lung metastasis minus primary, one value per patient or lesion
Step 2  fixed-effect inverse-variance pooling, random-effects sensitivity, verdicts for H1 and H2
Step 3  the same after adjusting for a lung score (SFTPC, SFTPB, AGER) and an immune score (PTPRC)
Step 4  tumour cells only, in the two single-cell datasets (tie-breaker)
Step 5  secondary and sensitivity analyses

Inputs: data/engine/cycle02/raw/ (GEO downloads, not stored in git; see the report for the list)
Outputs: data/engine/cycle02/results.csv, summary.json, sample_values.csv, docs/figures/engine02_*.svg
"""
import csv
import glob
import gzip
import json
import math
import os
import re
import tarfile

import h5py
import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle02", "raw")
X = os.path.join(RAW, "x")                      # unpacked archives
OUT = os.path.join(ROOT, "data", "engine", "cycle02")
FIG = os.path.join(ROOT, "docs", "figures")

TEST = ["CXCR4", "CXCL12", "ACKR3"]
LUNG = ["SFTPC", "SFTPB", "AGER"]
IMMUNE = ["PTPRC"]
BULK_GENES = TEST + LUNG + IMMUNE
# single-cell tumour-cell rule (Deviations, point 4)
SC_ENDO = ["PECAM1", "VWF"]
SC_EPI = ["EPCAM", "SFTPC", "SFTPB", "AGER"]
SC_TUMOUR = ["COL1A1", "COL1A2", "RUNX2", "SPP1", "IBSP", "ALPL", "SOX9", "COL2A1", "ACAN"]
SC_GENES = sorted(set(TEST + LUNG + IMMUNE + SC_ENDO + SC_EPI + SC_TUMOUR + ["ACP5", "CTSK", "CD68"]))
ENSG = {"CXCR4": "ENSG00000121966", "CXCL12": "ENSG00000107562", "ACKR3": "ENSG00000144476",
        "SFTPC": "ENSG00000168484", "SFTPB": "ENSG00000168878", "AGER": "ENSG00000204305",
        "PTPRC": "ENSG00000081237"}
Z95 = 1.959964
ALIASES = {"ACKR3": ("CXCR7", "CMKOR1")}        # older names for the same gene on older annotations


# ------------------------------------------------------------------ readers
def read_matrix(path):
    """GEO series matrix: sample ids, titles, joined characteristics, {probe: values}."""
    ids, titles, chars, expr, in_table = [], [], [], {}, False
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("!Sample_geo_accession"):
                ids = [v.strip('"') for v in line.split("\t")[1:]]
                chars = ["" for _ in ids]
            elif line.startswith("!Sample_title"):
                titles = [v.strip('"') for v in line.split("\t")[1:]]
            elif line.startswith("!Sample_characteristics_ch1"):
                for i, v in enumerate(line.split("\t")[1:]):
                    chars[i] = (chars[i] + "; " + v.strip('"')).strip("; ")
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
    return ids, titles, chars, expr


def probe_map(path, sym_col, genes):
    fh = gzip.open(path, "rt", errors="replace") if path.endswith(".gz") else open(path, errors="replace")
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
        syms = [s.strip() for s in re.split(r"///|,|;", p[ix])]
        for g in genes:
            if g in syms or any(a in syms for a in ALIASES.get(g, ())):
                out[g].append(p[0])
    fh.close()
    return out


def array_values(expr, pmap, keep):
    """Pre-registered probe rule: highest mean across the samples used; log2 if not on a log scale."""
    vals, chosen = {}, {}
    scale_log = np.nanmax(np.concatenate([expr[p][keep] for ps in pmap.values() for p in ps if p in expr])) <= 100
    for g, probes in pmap.items():
        best, best_mean = None, -np.inf
        for pr in probes:
            if pr in expr:
                v = expr[pr][keep].astype(float)
                v = v if scale_log else np.log2(np.clip(v, 1, None))
                m = np.nanmean(v)
                if m > best_mean:
                    best, best_mean, bv = pr, m, v
        if best is not None:
            vals[g], chosen[g] = bv, best
    return vals, chosen


def table_values(path, sep, id_to_gene, log=True, cpm=False):
    """Bulk RNA-seq table with genes in rows. Returns columns and {gene: log2 values}."""
    df = pd.read_csv(path, sep=sep, index_col=0)
    df.columns = [str(c).strip('"') for c in df.columns]
    df.index = [str(i).strip('"').split(".")[0] for i in df.index]
    if cpm:
        df = df / df.sum(axis=0) * 1e6
    vals = {}
    for g, key in id_to_gene.items():
        if key in df.index:
            row = df.loc[key]
            row = row.iloc[0] if isinstance(row, pd.DataFrame) else row
            v = row.values.astype(float)
            vals[g] = np.log2(v + 1) if log else v
    return list(df.columns), vals


def mtx_counts(mtx, features, genes):
    """10x matrix: per-cell total counts and a dense cells x genes block for the genes asked for."""
    feat = pd.read_csv(features, sep="\t", header=None)
    row_of = {}
    for i, sym in enumerate(feat[1].values):
        if sym in genes and sym not in row_of:
            row_of[sym] = i + 1                      # MatrixMarket rows are 1-based
    with gzip.open(mtx, "rt") as fh:
        line = fh.readline()
        while line.startswith("%"):
            line = fh.readline()
        n_genes, n_cells, _ = map(int, line.split())
    totals = np.zeros(n_cells + 1)
    block = np.zeros((n_cells + 1, len(genes)))
    rows_wanted = np.array(sorted(row_of.values()))
    col_of_row = {r: genes.index(s) for s, r in row_of.items()}
    for ch in pd.read_csv(mtx, sep=" ", comment="%", header=None, skiprows=1, chunksize=4_000_000,
                          names=["r", "c", "v"], dtype={"r": np.int32, "c": np.int32, "v": np.float64}):
        if ch.iloc[0]["r"] == n_genes and ch.iloc[0]["c"] == n_cells:      # the size line
            ch = ch.iloc[1:]
        totals += np.bincount(ch["c"].values, weights=ch["v"].values, minlength=n_cells + 1)
        sub = ch[np.isin(ch["r"].values, rows_wanted)]
        for r, c, v in zip(sub["r"].values, sub["c"].values, sub["v"].values):
            block[c, col_of_row[r]] += v
    return totals[1:], block[1:], [g for g in genes if g in row_of]


def sc_sample(mtx, features):
    """Pseudobulk values (all cells) and tumour-cell-only values for one single-cell sample."""
    totals, block, present = mtx_counts(mtx, features, SC_GENES)
    col = {g: SC_GENES.index(g) for g in SC_GENES}
    has = lambda g: block[:, col[g]] > 0
    immune = has("PTPRC")
    endo = has("PECAM1") | has("VWF")
    epi = has("EPCAM") | has("SFTPC") | has("SFTPB") | has("AGER")
    oclast = has("ACP5") & has("CTSK") & (has("PTPRC") | has("CD68"))
    n_markers = sum(has(g).astype(int) for g in SC_TUMOUR)
    tumour = ~immune & ~endo & ~epi & ~oclast & (n_markers >= 2)
    pb = {g: float(np.log2(block[:, col[g]].sum() / totals.sum() * 1e6 + 1)) for g in BULK_GENES}
    tc = None
    if tumour.sum() >= 50:
        tt = totals[tumour].sum()
        tc = {g: float(np.log2(block[tumour, col[g]].sum() / tt * 1e6 + 1)) for g in TEST}
        tc["frac_pos"] = {g: float((block[tumour, col[g]] > 0).mean()) for g in TEST}
    counts = {"cells": int(len(totals)), "immune": int(immune.sum()), "endothelial": int((endo & ~immune).sum()),
              "lung_epithelial": int((epi & ~immune & ~endo).sum()), "tumour": int(tumour.sum())}
    # exploratory, not pre-registered: where each gene's RNA sits
    other = ~immune & ~tumour
    counts["rna_share"] = {g: {k: float(block[m, col[g]].sum() / max(block[:, col[g]].sum(), 1))
                               for k, m in (("immune", immune), ("tumour", tumour), ("other", other))} for g in TEST}
    return pb, tc, counts


def visium_pseudobulk(path):
    with h5py.File(path, "r") as f:
        m = f["matrix"]
        data, idx = m["data"][:], m["indices"][:]
        names = [n.decode() for n in m["features"]["name"][:]]
        n_genes = int(m["shape"][0])
    sums = np.bincount(idx, weights=data, minlength=n_genes)
    total = sums.sum()
    out = {}
    for g in BULK_GENES:
        if g in names:
            out[g] = float(np.log2(sums[names.index(g)] / total * 1e6 + 1))
    return out


# ------------------------------------------------------------------ datasets
# Each loader returns a list of units: {"unit", "group" ("P" or "LM"), "pair" (or None), gene values...}
def average_units(rows):
    """Average samples within (unit, group) so each patient or lesion counts once per group."""
    out = {}
    for r in rows:
        out.setdefault((r["unit"], r["group"]), []).append(r)
    res = []
    for (u, g), rs in out.items():
        d = {"unit": u, "group": g, "pair": rs[0].get("pair"), "n_samples": len(rs)}
        for k in rs[0]:
            if k not in d and isinstance(rs[0][k], (int, float)) and not isinstance(rs[0][k], bool):
                d[k] = float(np.mean([x[k] for x in rs if k in x]))
        res.append(d)
    return res


def ds_gse14359():
    ids, titles, chars, expr = read_matrix(os.path.join(RAW, "GSE14359_series_matrix.txt.gz"))
    keep = [i for i, c in enumerate(chars) if "osteosarcoma" in c.lower() and "osteoblast" not in c.lower()]
    pmap = probe_map(os.path.join(RAW, "GPL96.annot.gz"), "Gene symbol", BULK_GENES)
    vals, chosen = array_values(expr, pmap, keep)
    rows = []
    for j, i in enumerate(keep):
        grp = "LM" if "lung metastasis" in chars[i].lower() else "P"
        rows.append(dict({"unit": chars[i], "group": grp, "pair": None}, **{g: float(v[j]) for g, v in vals.items()}))
    return {"name": "GSE14359", "type": "array", "units": average_units(rows), "probes": chosen}


def ds_gse220538(paired_only=False):
    cols, vals = table_values(os.path.join(RAW, "GSE220538_tpm.txt.gz"), ",", ENSG)
    rows = []
    for j, c in enumerate(cols):
        pat = re.match(r"(OS-\d+)-", c).group(1)
        grp = "LM" if re.search(r"-LM\d*$", c) else "P"
        rows.append(dict({"unit": pat, "group": grp, "pair": pat}, **{g: float(v[j]) for g, v in vals.items()}))
    units = average_units(rows)
    both = {u["unit"] for u in units if u["group"] == "LM"} & {u["unit"] for u in units if u["group"] == "P"}
    if paired_only:
        units = [u for u in units if u["unit"] in both]
        return {"name": "GSE220538 (4 matched pairs)", "type": "bulk RNA-seq", "units": units, "paired": True}
    units = [u for u in units if not (u["unit"] in both and u["group"] == "P")]     # matched patients give LM only
    for u in units:
        u["pair"] = None
    return {"name": "GSE220538", "type": "bulk RNA-seq", "units": units, "matched_patients": sorted(both)}


def ds_gse140131():
    cols, vals = table_values(os.path.join(RAW, "GSE140131_norm.tsv.gz"), "\t", ENSG)
    rows = []
    for j, c in enumerate(cols):
        if c.endswith("_TMR"):
            grp = "P"
        elif c in ("S53", "S54"):                    # lung metastases; S51 is a scapula metastasis
            grp = "LM"
        else:
            continue
        rows.append(dict({"unit": c, "group": grp, "pair": None}, **{g: float(v[j]) for g, v in vals.items()}))
    return {"name": "GSE140131", "type": "bulk RNA-seq", "units": rows}


VISIUM_LUNG = ["MR1", "MR10A", "MR10B", "MR11A", "MR11B", "MR12", "MR13", "MR15", "MR18", "MR2", "MR3", "MR4"]


def ds_gse293065():
    rows = []
    for path in sorted(glob.glob(os.path.join(X, "GSM*_filtered_feature_bc_matrix.h5"))):
        tag = re.search(r"GSM\d+_([A-Z]+\d+[AB]?)_", os.path.basename(path)).group(1)
        if tag.startswith("PT"):
            grp, unit = "P", tag
        elif tag in VISIUM_LUNG:
            grp, unit = "LM", re.sub(r"[AB]$", "", tag)      # sections A and B of one lesion are averaged
        else:
            continue
        rows.append(dict({"unit": unit, "group": grp, "pair": None}, **visium_pseudobulk(path)))
    return {"name": "GSE293065", "type": "spatial, pseudobulk", "units": average_units(rows)}


SC152048 = {"BC2": "P", "BC3": "P", "BC5": "P", "BC6": "P", "BC16": "P", "BC21": "P", "BC22": "P", "BC10": "LM", "BC17": "LM"}


def ds_gse152048():
    rows, tc_rows, cells = [], [], {}
    for s, grp in SC152048.items():
        d = os.path.join(X, s)
        pb, tc, counts = sc_sample(os.path.join(d, "matrix.mtx.gz"), os.path.join(d, "features.tsv.gz"))
        rows.append(dict({"unit": s, "group": grp, "pair": None}, **pb))
        cells[s] = counts
        if tc:
            tc_rows.append(dict({"unit": s, "group": grp, "pair": None, "frac_pos": tc.pop("frac_pos")}, **tc))
    return {"name": "GSE152048", "type": "single-cell, pseudobulk", "units": rows, "tumour_units": tc_rows, "cells": cells}


def ds_gse318840():
    rows, tc_rows, cells = [], [], {}
    for mtx in sorted(glob.glob(os.path.join(X, "GSM*_Fixed_RNA_Osteosarcoma_*_matrix.mtx.gz"))):
        tag = re.search(r"Osteosarcoma_([A-Za-z]+\d)_matrix", mtx).group(1)
        if tag.startswith(("Naive", "Treated")):
            grp = "P"
        elif tag.startswith("Metastasis"):
            grp = "LM"
        else:
            continue                                  # soft-tissue recurrences
        pb, tc, counts = sc_sample(mtx, mtx.replace("_matrix.mtx.gz", "_features.tsv.gz"))
        rows.append(dict({"unit": tag, "group": grp, "pair": None}, **pb))
        cells[tag] = counts
        if tc:
            tc_rows.append(dict({"unit": tag, "group": grp, "pair": None, "frac_pos": tc.pop("frac_pos")}, **tc))
    return {"name": "GSE318840", "type": "single-cell, pseudobulk", "units": rows, "tumour_units": tc_rows, "cells": cells}


# --- sensitivity only: metastasis site not recorded per sample
def ds_gse32981():
    ids, titles, chars, expr = read_matrix(os.path.join(RAW, "GSE32981_series_matrix.txt.gz"))
    keep = list(range(len(ids)))
    pmap = probe_map(os.path.join(RAW, "GPL3307.platform.txt"), "Gene_Symbol", BULK_GENES)
    vals, chosen = array_values(expr, pmap, keep)
    rows = []
    for i in keep:
        grp = "LM" if "origin: Met" in chars[i] else "P"
        rows.append(dict({"unit": titles[i], "group": grp, "pair": None},
                         **{g: float(v[i]) for g, v in vals.items() if not np.isnan(v[i])}))
    return {"name": "GSE32981 (site not recorded)", "type": "array", "units": rows, "probes": chosen}


GSE237033 = {  # sample: (patient, status), from the public GEO sample records
    "L2377": ("1598", "primary"), "L2559": ("1785", "primary"), "L2792": ("1598", "recurrence"),
    "L3309": ("1670", "recurrence"), "L3499": ("1785", "metastasis"), "L3676": ("1670", "recurrence"),
    "L4281": ("1785", "metastasis"), "L5062": ("1785", "metastasis"), "L5071": ("1670", "metastasis"),
    "L5164": ("3617", "primary"), "L5450": ("3840", "primary"), "L5465": ("3617", "metastasis"),
    "L5757": ("1785", "metastasis"), "L6052": ("3840", "metastasis"), "L6581": ("1728", "metastasis"),
    "L6621": ("4816", "primary"), "L6647": ("1785", "metastasis"), "L7039": ("4816", "metastasis"),
    "L7177": ("1598", "primary"), "L7178": ("1670", "primary"), "L7179": ("1728", "primary"),
    "L7181": ("1785", "primary"), "L7182": ("3617", "primary")}


def ds_gse237033():
    cols, vals = table_values(os.path.join(RAW, "GSE237033_raw_counts.tsv.gz"), "\t", ENSG, cpm=True)
    rows = []
    for j, c in enumerate(cols):
        pat, status = GSE237033[c]
        if status == "recurrence":
            continue
        rows.append(dict({"unit": pat, "group": "LM" if status == "metastasis" else "P", "pair": pat},
                         **{g: float(v[j]) for g, v in vals.items()}))
    units = average_units(rows)
    both = {u["unit"] for u in units if u["group"] == "LM"} & {u["unit"] for u in units if u["group"] == "P"}
    return {"name": "GSE237033 (paired; site not recorded)", "type": "bulk RNA-seq",
            "units": [u for u in units if u["unit"] in both], "paired": True}


def ds_gse87624():
    cols, vals = table_values(os.path.join(RAW, "GSE87624_Human_masked.txt.gz"), "\t", {g: g for g in BULK_GENES}, log=False)
    if "ACKR3" not in vals:
        _, alt = table_values(os.path.join(RAW, "GSE87624_Human_masked.txt.gz"), "\t", {"ACKR3": "CXCR7"}, log=False)
        vals.update(alt)
    mx = max(np.nanmax(v) for v in vals.values())
    rows = []
    for j, c in enumerate(cols):                      # suffix: M metastasis, U unknown, B normal bone, C cell line
        if re.fullmatch(r"HO\d+", c):
            grp = "P"
        elif re.fullmatch(r"HO\d+M", c):
            grp = "LM"
        else:
            continue
        rows.append(dict({"unit": c, "group": grp, "pair": None},
                         **{g: float(np.log2(v[j] + 1) if mx > 100 else v[j]) for g, v in vals.items()}))
    return {"name": "GSE87624 (site not recorded)", "type": "bulk RNA-seq", "units": rows}


# ------------------------------------------------------------------ statistics
def add_scores(units):
    """Lung score = mean z of SFTPC, SFTPB, AGER; immune score = z of PTPRC; z within dataset."""
    def z(g):
        v = np.array([u.get(g, np.nan) for u in units], float)
        sd = np.nanstd(v, ddof=1)
        return (v - np.nanmean(v)) / sd if sd > 0 else np.zeros_like(v)
    lung = [z(g) for g in LUNG if any(g in u for u in units)]
    lung = np.nanmean(np.vstack(lung), axis=0) if lung else np.full(len(units), np.nan)
    imm = z("PTPRC") if any("PTPRC" in u for u in units) else np.full(len(units), np.nan)
    for u, a, b in zip(units, lung, imm):
        u["lung_score"], u["immune_score"] = float(a), float(b)


def pooled_sd(a, b):
    return math.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))


def effect(units, gene, paired=False):
    """Hedges' g, lung metastasis minus primary. Paired: mean within-patient difference on the same scale."""
    a = np.array([u[gene] for u in units if u["group"] == "LM" and gene in u], float)
    b = np.array([u[gene] for u in units if u["group"] == "P" and gene in u], float)
    if len(a) < 2 or len(b) < 2:
        return None
    sp = pooled_sd(a, b)
    if sp == 0:
        return None
    if paired:
        pa = {u["unit"]: u[gene] for u in units if u["group"] == "LM"}
        pb = {u["unit"]: u[gene] for u in units if u["group"] == "P"}
        d = np.array([pa[k] - pb[k] for k in sorted(pa)], float)
        n = len(d)
        j = 1 - 3 / (4 * (n - 1) - 1)
        g, se = j * d.mean() / sp, j * (d.std(ddof=1) / math.sqrt(n)) / sp
        return {"g": float(g), "se": float(se), "n_lm": n, "n_p": n, "diff_log2": float(d.mean()), "sp": sp, "paired": True}
    n1, n2 = len(a), len(b)
    j = 1 - 3 / (4 * (n1 + n2) - 9)
    g = j * (a.mean() - b.mean()) / sp
    se = math.sqrt((n1 + n2) / (n1 * n2) + g * g / (2 * (n1 + n2)))
    return {"g": float(g), "se": float(se), "n_lm": n1, "n_p": n2, "diff_log2": float(a.mean() - b.mean()), "sp": sp, "paired": False}


def adjusted_effect(units, gene, covars):
    """Group coefficient from a linear model with the covariates, on the same standardised scale as g."""
    us = [u for u in units if gene in u and all(not math.isnan(u[c]) for c in covars)]
    y = np.array([u[gene] for u in us], float)
    grp = np.array([1.0 if u["group"] == "LM" else 0.0 for u in us])
    Xm = np.column_stack([np.ones(len(us)), grp] + [[u[c] for u in us] for c in covars])
    df = len(us) - Xm.shape[1]
    if df < 1 or grp.sum() < 2 or (1 - grp).sum() < 2:
        return None
    sp = pooled_sd(y[grp == 1], y[grp == 0])
    beta, res, rank, _ = np.linalg.lstsq(Xm, y, rcond=None)
    if rank < Xm.shape[1] or sp == 0:
        return None
    resid = y - Xm @ beta
    cov = (resid @ resid / df) * np.linalg.inv(Xm.T @ Xm)
    return {"g": float(beta[1] / sp), "se": float(math.sqrt(cov[1, 1]) / sp), "n_lm": int(grp.sum()), "n_p": int((1 - grp).sum())}


def meta(effects):
    effects = [e for e in effects if e]
    if not effects:
        return None
    b = np.array([e["g"] for e in effects])
    se = np.array([e["se"] for e in effects])
    w = 1 / se ** 2
    bf, sef = float((w * b).sum() / w.sum()), float(math.sqrt(1 / w.sum()))
    k = len(b)
    q = float((w * (b - bf) ** 2).sum())
    tau2 = max(0.0, (q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0
    wr = 1 / (se ** 2 + tau2)
    br, ser = float((wr * b).sum() / wr.sum()), float(math.sqrt(1 / wr.sum()))
    return {"g": bf, "lo": bf - Z95 * sef, "hi": bf + Z95 * sef, "p": float(2 * stats.norm.sf(abs(bf / sef))),
            "random": {"g": br, "lo": br - Z95 * ser, "hi": br + Z95 * ser},
            "I2": max(0.0, (q - (k - 1)) / q) if q > 0 and k > 1 else 0.0, "k": k,
            "n_lm": int(sum(e["n_lm"] for e in effects)), "n_p": int(sum(e["n_p"] for e in effects))}


def verdict(m, m_adj, m_tumour, sign):
    """sign=+1 for H1 (higher in metastases), -1 for H2 (lower). Rules from the pre-registration."""
    g, lo, hi = sign * m["g"], sign * (m["lo"] if sign > 0 else m["hi"]), sign * (m["hi"] if sign > 0 else m["lo"])
    if lo > 0 and g >= 0.5 and m_adj is not None and sign * m_adj["g"] > 0:
        v = "Supported"
        if m_tumour is not None and sign * m_tumour["g"] < 0:
            v = "Inconclusive (explained by the surroundings, not the tumour cells)"
    elif hi < 0.5:
        v = "Refuted"
    else:
        v = "Inconclusive"
    return v


# ------------------------------------------------------------------ figure
def forest_svg(rows, path, title, sub):
    W, rowh, left, right = 820, 32, 330, 120
    H = 92 + rowh * len(rows) + 40
    lo_ax, hi_ax = -4.0, 4.0
    def Xp(v):
        return left + (min(max(v, lo_ax), hi_ax) - lo_ax) / (hi_ax - lo_ax) * (W - left - right)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="14">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">{title}</text>',
         f'<text x="16" y="50" font-size="13" fill="#525b6b">{sub[0]}</text>',
         f'<text x="16" y="68" font-size="13" fill="#525b6b">{sub[1]}</text>']
    top = 92
    for v in (-4, -2, 0, 2, 4):
        x = Xp(v)
        s.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{top + rowh * len(rows)}" stroke="{"#525b6b" if v == 0 else "#e2e5ea"}" stroke-width="{1.5 if v == 0 else 1}"/>')
        s.append(f'<text x="{x:.1f}" y="{top + rowh * len(rows) + 20}" text-anchor="middle" fill="#525b6b" font-size="12">{v:g}</text>')
    for bar in (0.5, -0.5):
        s.append(f'<line x1="{Xp(bar):.1f}" y1="{top - 6}" x2="{Xp(bar):.1f}" y2="{top + rowh * len(rows)}" stroke="#a3401a" stroke-dasharray="4 4"/>')
    for k, (lab, g, lo, hi, kind) in enumerate(rows):
        y = top + rowh * k + rowh / 2
        if kind == "head":
            s.append(f'<text x="16" y="{y + 5:.1f}" fill="#14181f" font-weight="600">{lab}</text>')
            continue
        col = {"dataset": "#1c5cab", "pooled": "#14264a", "sens": "#6a7384"}[kind]
        s.append(f'<text x="28" y="{y + 5:.1f}" fill="#14181f" font-weight="{600 if kind == "pooled" else 400}">{lab}</text>')
        s.append(f'<line x1="{Xp(lo):.1f}" y1="{y:.1f}" x2="{Xp(hi):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        if kind == "pooled":
            s.append(f'<path d="M{Xp(g) - 9:.1f},{y:.1f} L{Xp(g):.1f},{y - 8:.1f} L{Xp(g) + 9:.1f},{y:.1f} L{Xp(g):.1f},{y + 8:.1f} Z" fill="{col}"/>')
        else:
            s.append(f'<rect x="{Xp(g) - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="{col}"/>')
        s.append(f'<text x="{W - 8}" y="{y + 5:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{g:+.2f} ({lo:+.2f} to {hi:+.2f})</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


# ------------------------------------------------------------------ main
def main():
    os.makedirs(FIG, exist_ok=True)
    primary = [ds_gse14359(), ds_gse220538(), ds_gse140131(), ds_gse293065(), ds_gse152048(), ds_gse318840()]
    sens = [ds_gse32981(), ds_gse237033(), ds_gse87624()]
    pairs220 = ds_gse220538(paired_only=True)
    for d in primary + sens + [pairs220]:
        add_scores(d["units"])

    S = {"datasets": {}, "primary": {}, "adjusted": {}, "tumour_cells": {}, "secondary": {}, "sensitivity": {}, "verdicts": {}}
    out_rows = []

    def record(analysis, dname, gene, e):
        if e:
            out_rows.append([analysis, dname, gene, e.get("n_lm", ""), e.get("n_p", ""), f'{e["g"]:.3f}',
                             f'{e["g"] - Z95 * e["se"]:.3f}' if "se" in e else f'{e["lo"]:.3f}',
                             f'{e["g"] + Z95 * e["se"]:.3f}' if "se" in e else f'{e["hi"]:.3f}',
                             f'{e.get("diff_log2", float("nan")):.3f}' if "diff_log2" in e else ""])

    genes_all = TEST + ["lung_score", "immune_score"]
    per = {g: {} for g in genes_all}
    for d in primary:
        S["datasets"][d["name"]] = {"type": d["type"], "n_lm": sum(u["group"] == "LM" for u in d["units"]),
                                    "n_p": sum(u["group"] == "P" for u in d["units"]),
                                    "probes": d.get("probes"), "cells": d.get("cells")}
        for g in genes_all:
            per[g][d["name"]] = effect(d["units"], g)
            record("primary", d["name"], g, per[g][d["name"]])
    n_lm_total = sum(v["n_lm"] for v in S["datasets"].values())

    for g in genes_all:
        S["primary"][g] = {"per_dataset": per[g], "pooled": meta(per[g].values())}
        record("primary pooled (fixed)", "all six", g, S["primary"][g]["pooled"])
    for g in TEST:
        for lab, cov in (("lung", ["lung_score"]), ("immune", ["immune_score"]), ("lung+immune", ["lung_score", "immune_score"])):
            effs = {d["name"]: adjusted_effect(d["units"], g, cov) for d in primary}
            S["adjusted"].setdefault(g, {})[lab] = {"per_dataset": effs, "pooled": meta(effs.values())}
            record(f"adjusted for {lab}, pooled", "all usable", g, S["adjusted"][g][lab]["pooled"])
        # tumour cells only, single-cell datasets
        effs = {d["name"]: effect(d["tumour_units"], g) for d in primary if "tumour_units" in d}
        S["tumour_cells"][g] = {"per_dataset": effs, "pooled": meta(effs.values()),
                                "samples": {d["name"]: [{"unit": u["unit"], "group": u["group"], "value": u[g], "frac_pos": u["frac_pos"][g]}
                                                        for u in d["tumour_units"]] for d in primary if "tumour_units" in d}}
        for dn, e in effs.items():
            record("tumour cells only", dn, g, e)
        record("tumour cells only, pooled", "single-cell", g, S["tumour_cells"][g]["pooled"])

    for g, sign, h in (("CXCR4", 1, "H1"), ("CXCL12", -1, "H2")):
        adj = S["adjusted"][g]["lung+immune"]["pooled"]
        S["verdicts"][h] = {"gene": g, "verdict": verdict(S["primary"][g]["pooled"], adj, S["tumour_cells"][g]["pooled"], sign),
                            "underpowered": n_lm_total < 20, "n_lung_metastases": n_lm_total}

    # secondary: paired, bulk only, without single-cell and spatial pseudobulk
    for g in TEST:
        S["secondary"].setdefault("GSE220538 matched pairs", {})[g] = effect(pairs220["units"], g, paired=True)
        record("secondary: matched pairs", pairs220["name"], g, S["secondary"]["GSE220538 matched pairs"][g])
        bulk = [per[g][d["name"]] for d in primary if d["type"] in ("array", "bulk RNA-seq")]
        S["secondary"].setdefault("arrays and bulk RNA-seq only", {})[g] = meta(bulk)
        record("secondary: arrays and bulk only, pooled", "3 datasets", g, S["secondary"]["arrays and bulk RNA-seq only"][g])
        nosc = [per[g][d["name"]] for d in primary if not d["type"].startswith("single-cell")]
        S["secondary"].setdefault("without single-cell pseudobulk", {})[g] = meta(nosc)
        record("secondary: without single-cell pseudobulk, pooled", "4 datasets", g, S["secondary"]["without single-cell pseudobulk"][g])

    # sensitivity: datasets whose metastasis site is not recorded
    for g in TEST:
        effs = {d["name"]: effect(d["units"], g, paired=d.get("paired", False)) for d in sens}
        allm = meta(list(per[g].values()) + list(effs.values()))
        S["sensitivity"][g] = {"per_dataset": effs, "pooled_site_unknown": meta(effs.values()), "pooled_all_nine": allm}
        for dn, e in effs.items():
            record("sensitivity", dn, g, e)
        record("sensitivity: site-unknown datasets pooled", "3 datasets", g, S["sensitivity"][g]["pooled_site_unknown"])
        record("sensitivity: all nine pooled", "9 datasets", g, allm)

    # exploratory, not pre-registered: does each gene track the immune marker once group means are removed?
    S["exploratory"] = {"correlation_with_PTPRC_within_group": {}, "rna_share_by_cell_class": {}}
    for g in TEST:
        zs, n = [], 0
        for d in primary:
            xs, ys = [], []
            for grp in ("P", "LM"):
                us = [u for u in d["units"] if u["group"] == grp and g in u and "PTPRC" in u]
                if len(us) >= 2:
                    xs += list(np.array([u[g] for u in us]) - np.mean([u[g] for u in us]))
                    ys += list(np.array([u["PTPRC"] for u in us]) - np.mean([u["PTPRC"] for u in us]))
            if len(xs) >= 5 and np.std(xs) > 0 and np.std(ys) > 0:
                r = float(np.corrcoef(xs, ys)[0, 1])
                S["exploratory"]["correlation_with_PTPRC_within_group"].setdefault(g, {})[d["name"]] = {"r": r, "n": len(xs)}
    for d in primary:
        if d.get("cells"):
            S["exploratory"]["rna_share_by_cell_class"][d["name"]] = {k: v["rna_share"] for k, v in d["cells"].items()}

    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["analysis", "dataset", "measure", "n_lung_metastases", "n_primaries", "hedges_g", "ci_low", "ci_high", "mean_difference_log2"])
        w.writerows(out_rows)
    with open(os.path.join(OUT, "sample_values.csv"), "w", newline="") as f:
        w = csv.writer(f)
        cols = BULK_GENES + ["lung_score", "immune_score"]
        w.writerow(["set", "dataset", "unit", "group", "samples_averaged"] + cols)
        for lab, ds in (("primary", primary), ("sensitivity", sens)):
            for d in ds:
                for u in d["units"]:
                    w.writerow([lab, d["name"], u["unit"], u["group"], u.get("n_samples", 1)] + [f'{u[c]:.4f}' if c in u else "" for c in cols])

    for g, fn, ttl in (("CXCR4", "engine02_cxcr4_forest.svg", "CXCR4 RNA: lung metastases against primary tumours"),
                       ("CXCL12", "engine02_cxcl12_forest.svg", "CXCL12 RNA: lung metastases against primary tumours")):
        rows = [("Lung metastasis confirmed (verdict)", 0, 0, 0, "head")]
        for d in primary:
            e = per[g][d["name"]]
            if e:
                rows.append((f'{d["name"]}, {d["type"]} ({e["n_lm"]} v {e["n_p"]})', e["g"], e["g"] - Z95 * e["se"], e["g"] + Z95 * e["se"], "dataset"))
        m = S["primary"][g]["pooled"]
        rows.append((f'Pooled ({m["n_lm"]} metastases v {m["n_p"]} primaries)', m["g"], m["lo"], m["hi"], "pooled"))
        m = S["adjusted"][g]["immune"]["pooled"]
        rows.append(("Pooled, adjusted for immune tissue", m["g"], m["lo"], m["hi"], "pooled"))
        m = S["adjusted"][g]["lung+immune"]["pooled"]
        rows.append(("Pooled, adjusted for lung and immune tissue", m["g"], m["lo"], m["hi"], "pooled"))
        m = S["tumour_cells"][g]["pooled"]
        if m:
            rows.append(("Tumour cells only (two single-cell datasets)", m["g"], m["lo"], m["hi"], "pooled"))
        rows.append(("Metastasis site not recorded (sensitivity)", 0, 0, 0, "head"))
        for dn, e in S["sensitivity"][g]["per_dataset"].items():
            if e:
                rows.append((f'{dn.split(" (")[0]} ({e["n_lm"]} v {e["n_p"]})', e["g"], e["g"] - Z95 * e["se"], e["g"] + Z95 * e["se"], "sens"))
        forest_svg(rows, os.path.join(FIG, fn), ttl,
                   ("Difference in standard deviations (Hedges' g), 95% CI. Right of 0 = higher in lung metastases.",
                    "Dashed lines: the pre-registered bar, half a standard deviation."))

    # console summary
    print(f"lung-metastasis units in primary analysis: {n_lm_total}")
    for g in genes_all:
        print(f"\n== {g}")
        for dn, e in per[g].items():
            if e:
                print(f"  {dn:12s} LM {e['n_lm']:2d} v P {e['n_p']:2d}  g {e['g']:+.2f} ({e['g'] - Z95 * e['se']:+.2f} to {e['g'] + Z95 * e['se']:+.2f})  diff log2 {e['diff_log2']:+.2f}")
        m = S["primary"][g]["pooled"]
        print(f"  POOLED fixed g {m['g']:+.2f} ({m['lo']:+.2f} to {m['hi']:+.2f}) p={m['p']:.3g} I2={m['I2']:.2f}; random {m['random']['g']:+.2f} ({m['random']['lo']:+.2f} to {m['random']['hi']:+.2f})")
        if g in TEST:
            for lab, a in S["adjusted"][g].items():
                m = a["pooled"]
                print(f"  adjusted {lab:12s} g {m['g']:+.2f} ({m['lo']:+.2f} to {m['hi']:+.2f}) k={m['k']}")
            m = S["tumour_cells"][g]["pooled"]
            print(f"  tumour cells only: {'g %+.2f (%+.2f to %+.2f)' % (m['g'], m['lo'], m['hi']) if m else 'not estimable'}")
            for dn, ss in S["tumour_cells"][g]["samples"].items():
                print("    ", dn, [(s["unit"], s["group"], round(s["value"], 2), round(s["frac_pos"], 3)) for s in ss])
            for lab, v in S["secondary"].items():
                e = v[g]
                if e:
                    lo, hi = (e["lo"], e["hi"]) if "lo" in e else (e["g"] - Z95 * e["se"], e["g"] + Z95 * e["se"])
                    print(f"  secondary {lab}: g {e['g']:+.2f} ({lo:+.2f} to {hi:+.2f})")
            for dn, e in S["sensitivity"][g]["per_dataset"].items():
                if e:
                    print(f"  sensitivity {dn}: LM {e['n_lm']} v P {e['n_p']} g {e['g']:+.2f} ({e['g'] - Z95 * e['se']:+.2f} to {e['g'] + Z95 * e['se']:+.2f})")
            m = S["sensitivity"][g]["pooled_all_nine"]
            print(f"  sensitivity all nine pooled: g {m['g']:+.2f} ({m['lo']:+.2f} to {m['hi']:+.2f})")
    print("\nEXPLORATORY r with PTPRC within group:", json.dumps(S["exploratory"]["correlation_with_PTPRC_within_group"], default=lambda x: round(x, 2)))
    for dn, v in S["exploratory"]["rna_share_by_cell_class"].items():
        for unit, sh in v.items():
            print(f"  {dn} {unit}: " + "; ".join(f"{g} immune {sh[g]['immune']:.0%} tumour {sh[g]['tumour']:.0%}" for g in ("CXCR4", "CXCL12")))
    for g in TEST:
        for lab, a in S["adjusted"][g].items():
            print(" adj", g, lab, {k: (round(e["g"], 2), round(e["se"], 2)) if e else None for k, e in a["per_dataset"].items()})
    print("\nVERDICTS:", json.dumps(S["verdicts"], indent=1))
    for d in primary:
        if d.get("cells"):
            print(d["name"], "cells:", d["cells"])
        if d.get("probes"):
            print(d["name"], "probes:", d["probes"])


if __name__ == "__main__":
    main()
