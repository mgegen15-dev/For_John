#!/usr/bin/env python3
"""Engine cycle 8: a systematic scan for dependencies that go with the gene losses and gains seen in osteosarcoma.

A discovery scan, not a test. Method, thresholds and the replication step are pre-registered in
research_notes/Engine/cycle-08-dependency-scan/PREREGISTRATION.md.

  Step 1  gene changes seen in osteosarcoma patients (MSK-IMPACT anchors; TARGET-OS passengers lost alongside)
  Step 2  scan every gene in the DepMap knockout screen against each change, adjusted for lineage; FDR 5%, effect <= -0.2
  Step 3  replicate each hit in the knockdown (RNAi) screens
  Step 4  describe replicated hits in osteosarcoma and sarcoma lines; attach drugs and patient frequency

Needs the files fetched by tools/engine_cycle03_9p21.py, engine_cycle07_ccne1.py and engine_cycle05_06_depmap.py.
Outputs: data/engine/cycle08/alterations.csv, hits.csv, summary.json, docs/figures/engine08_scan.svg
"""
import collections
import csv
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle03_9p21 as c3          # noqa: E402
import engine_cycle07_ccne1 as c7         # noqa: E402

ROOT = os.path.dirname(HERE)
DEP = os.path.join(ROOT, "data", "engine", "depmap", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle08")
FIG = os.path.join(ROOT, "docs", "figures")
EFFECT, FDR, MIN_ALTERED, MIN_RNAI = -0.2, 0.05, 10, 5
KNOWN = {  # pairs established in the literature, fixed in the pre-registration
    "9p21": {"PRMT5", "MAT2A", "WDR77", "RIOK1"}, "CCNE1": {"CDK2", "PKMYT1", "CCNE1"}, "MDM2": {"MDM2", "MDM4", "PPM1D", "USP7"},
    "CDK4": {"CDK4", "CCND1"}, "MYC": {"MYC", "MAX"}, "RB1": {"SKP2", "CDK2", "E2F3", "CCNE1"}, "PTEN": {"PIK3CB", "AKT1", "AKT2", "AKT3"}}
NINE_P21 = {"CDKN2A", "CDKN2B", "MTAP"}


# ------------------------------------------------------------------ step 1
def patient_alterations():
    units, _ = c3.one_per_patient(c7.load("msk_impact_50k_2026"))
    anchors = []
    genes_del = set().union(*[u["dels"] for u in units])
    genes_amp = set().union(*[u["amps"] for u in units])
    for kind, genes, key, thr in (("deletion", genes_del, "dels", 0.03), ("amplification", genes_amp, "amps", 0.05)):
        for g in sorted(genes):
            us = [u for u in units if u["genes_on_panel"] is None or g in u["genes_on_panel"]]
            k = sum(g in u[key] for u in us)
            if us and k / len(us) >= thr:
                anchors.append({"gene": g, "kind": kind, "role": "anchor", "anchor": g, "patients_altered": k, "patients_tested": len(us),
                                "patient_rate": k / len(us), "source": "MSK-IMPACT"})
    # passengers lost alongside a deleted anchor, in TARGET-OS
    by = {}
    for s in c7.load("os_target_gdc"):
        by.setdefault(s["patient"], s)
    target = list(by.values())
    out = list(anchors)
    have = {(a["gene"], a["kind"]) for a in anchors}
    for a in [x for x in anchors if x["kind"] == "deletion"]:
        carriers = [u for u in target if a["gene"] in u["dels"]]
        if len(carriers) < 4:
            continue
        cnt = collections.Counter(g for u in carriers for g in u["dels"])
        for g, k in cnt.items():
            if g != a["gene"] and k >= 4 and k >= 0.5 * len(carriers) and (g, "deletion") not in have:
                tot = sum(g in u["dels"] for u in target)
                out.append({"gene": g, "kind": "deletion", "role": "passenger", "anchor": a["gene"], "patients_altered": tot,
                            "patients_tested": len(target), "patient_rate": tot / len(target), "source": "TARGET-OS"})
                have.add((g, "deletion"))
    return out


# ------------------------------------------------------------------ DepMap
def read_cols(name, genes):
    path = os.path.join(DEP, name)
    cols = pd.read_csv(path, nrows=0).columns
    keep = [cols[0]] + [c for c in cols[1:] if c.split(" (")[0] in genes]
    df = pd.read_csv(path, usecols=keep, index_col=0)
    df.columns = [c.split(" (")[0] for c in df.columns]
    return df.loc[:, ~df.columns.duplicated()]


def residualise(M, lineage):
    """Remove lineage means column by column (lineage as fixed effects)."""
    M = M.copy()
    for lin in np.unique(lineage):
        m = lineage == lin
        M[m] -= M[m].mean(axis=0, keepdims=True)
    return M


def scan_matrix(Y, genes, lineage, altered):
    """Lineage-adjusted difference for every column of Y (lines x genes) against one 0/1 vector."""
    xr = residualise(altered[:, None].astype(float), lineage)[:, 0]
    sxx = float(xr @ xr)
    if sxx <= 0:
        return None
    Yr = residualise(Y, lineage)
    beta = (xr @ Yr) / sxx
    df = len(xr) - len(np.unique(lineage)) - 1
    rss = (Yr ** 2).sum(axis=0) - beta ** 2 * sxx
    se = np.sqrt(np.clip(rss, 0, None) / df / sxx)
    t = beta / se
    p = 2 * stats.t.sf(np.abs(t), df)
    return beta, se, p, df


def bh(p):
    p = np.asarray(p)
    order = np.argsort(p)
    q = np.empty(len(p))
    prev, n = 1.0, len(p)
    for rank, i in enumerate(order[::-1]):
        k = n - rank
        prev = min(prev, p[i] * n / k)
        q[i] = prev
    return q


def main():
    os.makedirs(OUT, exist_ok=True)
    alts = patient_alterations()
    model = pd.read_csv(os.path.join(DEP, "Model.csv"), index_col=0)
    crispr = pd.read_csv(os.path.join(DEP, "CRISPRGeneEffect.csv"), index_col=0)
    crispr.columns = [c.split(" (")[0] for c in crispr.columns]
    crispr = crispr.loc[:, ~crispr.columns.duplicated()]
    crispr = crispr.loc[:, crispr.isna().mean() <= 0.05]
    lines = [i for i in crispr.index if i in model.index and isinstance(model.loc[i, "OncotreeLineage"], str)]
    crispr = crispr.loc[lines]
    lineage = model.loc[lines, "OncotreeLineage"].values
    Y = crispr.values.astype(float)
    for lin in np.unique(lineage):                          # the few missing scores take their lineage mean
        m = lineage == lin
        sub = Y[m]
        mu = np.nanmean(sub, axis=0)
        mu = np.where(np.isnan(mu), np.nanmean(Y, axis=0), mu)
        idx = np.where(np.isnan(sub))
        sub[idx] = mu[idx[1]]
        Y[m] = sub
    dep_genes = list(crispr.columns)
    cn = read_cols("OmicsCNGene.csv", {a["gene"] for a in alts}).reindex(lines)
    text = (model["OncotreePrimaryDisease"].fillna("") + " " + model["OncotreeSubtype"].fillna("")).str.lower()
    is_os = text.reindex(lines).str.contains("osteosarcoma").values
    is_sarc = model.loc[lines, "OncotreeLineage"].isin(["Bone", "Soft Tissue"]).values

    scanned, results = [], []
    status = {}
    for a in alts:
        g = a["gene"]
        if g not in cn:
            a["scanned"], a["lines_altered"] = False, 0
            continue
        v = cn[g].values
        alt = np.where(np.isnan(v), np.nan, (v < 0.25) if a["kind"] == "deletion" else (v >= 2.0))
        ok = ~np.isnan(alt)
        a["lines_altered"] = int(np.nansum(alt))
        a["scanned"] = a["lines_altered"] >= MIN_ALTERED
        if not a["scanned"]:
            continue
        r = scan_matrix(Y[ok], dep_genes, lineage[ok], alt[ok])
        if r is None:
            a["scanned"] = False
            continue
        beta, se, p, df = r
        key = (g, a["kind"])
        status[key] = (alt, ok)
        scanned.append(key)
        for j, dg in enumerate(dep_genes):
            if a["kind"] == "deletion" and dg == g:
                continue
            results.append((g, a["kind"], a["anchor"], dg, beta[j], se[j], p[j]))
    res = pd.DataFrame(results, columns=["altered_gene", "kind", "anchor", "dependency", "effect", "se", "p"])
    res["q"] = bh(res["p"].values)
    # exploratory look-ups, added after the scan was first run (see the report): named pairs of clinical interest
    WATCH = [("CCND3", "CDK6"), ("CCND3", "CDK4"), ("CDK4", "CDK6"), ("MCL1", "BCL2L1"), ("VEGFA", "CCND3"), ("MYC", "MAX")]
    watch = res[[(a, d) in WATCH for a, d in zip(res["altered_gene"], res["dependency"])]]
    watch.round(5).to_csv(os.path.join(OUT, "exploratory_lookups.csv"), index=False)
    hits = res[(res["effect"] <= EFFECT) & (res["q"] < FDR)].copy()
    n_tests = len(res)

    # blocks: gene changes that travel together in the cell lines
    keys = scanned
    parent = {k: k for k in keys}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if a[1] != b[1]:
                continue
            xa, oa = status[a]
            xb, ob = status[b]
            m = oa & ob
            if m.sum() > 20 and np.nanstd(xa[m]) > 0 and np.nanstd(xb[m]) > 0 and np.corrcoef(xa[m], xb[m])[0, 1] > 0.5:
                parent[find(a)] = find(b)
    anchor_of = {(a["gene"], a["kind"]): a["anchor"] for a in alts}
    members = collections.defaultdict(list)
    for k in keys:
        members[find(k)].append(k)
    block_name = {}
    for root, ms in members.items():
        anchors = sorted({anchor_of[m] for m in ms})
        name = "9p21" if NINE_P21 & {m[0] for m in ms} else "/".join(anchors[:3])
        for m in ms:
            block_name[m] = f"{name} {'loss' if m[1] == 'deletion' else 'gain'}"
    hits["block"] = [block_name[(g, k)] for g, k in zip(hits["altered_gene"], hits["kind"])]
    # one row per (block, dependency): the member with the strongest result
    hits = hits.sort_values("p").drop_duplicates(["block", "dependency"]).reset_index(drop=True)

    # co-amplified dependency genes (cutting amplified DNA can harm cells for reasons unrelated to the gene)
    cn_dep = read_cols("OmicsCNGene.csv", set(hits["dependency"])).reindex(lines)
    labels = []
    for _, h in hits.iterrows():
        lab = ""
        if h["kind"] == "amplification":
            alt, ok = status[(h["altered_gene"], h["kind"])]
            same_block = {m[0] for m in keys if block_name[m] == h["block"]}
            if h["dependency"] == h["altered_gene"] or h["dependency"] in same_block:
                lab = "self"
            elif h["dependency"] in cn_dep:
                m = ok & (alt == 1)
                if m.sum() and np.nanmean(cn_dep[h["dependency"]].values[m] >= 2.0) >= 0.5:
                    lab = "co-amplified"
        labels.append(lab)
    hits["label"] = labels

    # ---- step 3: replication in knockdown screens
    d2 = pd.read_csv(os.path.join(DEP, "D2_combined_gene_dep_scores.csv"), index_col=0)
    d2.index = [i.split(" (")[0] for i in d2.index]
    ccle = {str(v): k for k, v in model["CCLEName"].dropna().items()}
    d2.columns = [ccle.get(c) for c in d2.columns]
    d2 = d2.loc[:, [c is not None for c in d2.columns]]
    d2 = d2.loc[~d2.index.duplicated(), ~d2.columns.duplicated()]
    rn_lines = [l for l in d2.columns if l in model.index and isinstance(model.loc[l, "OncotreeLineage"], str)]
    rn_lineage = model.loc[rn_lines, "OncotreeLineage"].values
    cn_all = read_cols("OmicsCNGene.csv", set(hits["altered_gene"])).reindex(rn_lines)
    rep = []
    for _, h in hits.iterrows():
        out = {"rnai_effect": np.nan, "rnai_lo": np.nan, "rnai_hi": np.nan, "rnai_altered": 0, "replicated": "not testable"}
        if h["dependency"] in d2.index and h["altered_gene"] in cn_all:
            y = d2.loc[h["dependency"], rn_lines].values.astype(float)
            v = cn_all[h["altered_gene"]].values
            alt = np.where(np.isnan(v), np.nan, (v < 0.25) if h["kind"] == "deletion" else (v >= 2.0))
            ok = ~np.isnan(alt) & ~np.isnan(y)
            out["rnai_altered"] = int(np.nansum(alt[ok]))
            if out["rnai_altered"] >= MIN_RNAI:
                r = scan_matrix(y[ok][:, None], [h["dependency"]], rn_lineage[ok], alt[ok])
                if r is not None:
                    b, se, p, df = r
                    tq = stats.t.ppf(0.975, df)
                    out.update(rnai_effect=float(b[0]), rnai_lo=float(b[0] - tq * se[0]), rnai_hi=float(b[0] + tq * se[0]),
                               replicated="yes" if (b[0] < 0 and b[0] + tq * se[0] < 0) else "no")
        rep.append(out)
    hits = pd.concat([hits, pd.DataFrame(rep)], axis=1)

    # ---- step 4: osteosarcoma and sarcoma lines, drugs, patient frequency, known list
    col = {g: j for j, g in enumerate(dep_genes)}
    drug = {r["gene"]: (r["best_drug"], r["best_drug_phase"]) for r in csv.DictReader(open(os.path.join(ROOT, "data", "osteosarcoma_repurposing_candidates.csv")))}
    rate = {(a["gene"], a["kind"]): a for a in alts}
    extra = []
    for _, h in hits.iterrows():
        alt, ok = status[(h["altered_gene"], h["kind"])]
        y = Y[:, col[h["dependency"]]]
        d = {}
        for lab, mask in (("os", is_os), ("sarcoma", is_sarc)):
            a_ = y[mask & ok & (alt == 1)]
            b_ = y[mask & ok & (alt == 0)]
            d[f"{lab}_altered_lines"], d[f"{lab}_other_lines"] = len(a_), len(b_)
            d[f"{lab}_difference"] = float(a_.mean() - b_.mean()) if len(a_) and len(b_) else np.nan
        blk = h["block"].rsplit(" ", 1)[0]
        known = any(h["dependency"] in v for k, v in KNOWN.items() if k == blk or k in blk.split("/"))
        d["known_pair"] = "yes" if known else ""
        d["drug"], d["drug_phase"] = drug.get(h["dependency"], ("", ""))
        a = rate[(h["altered_gene"], h["kind"])]
        d["patient_rate"], d["patient_source"], d["lines_altered"] = a["patient_rate"], a["source"], a["lines_altered"]
        d["mean_score_altered"] = float(y[ok & (alt == 1)].mean())
        d["mean_score_other"] = float(y[ok & (alt == 0)].mean())
        extra.append(d)
    hits = pd.concat([hits, pd.DataFrame(extra)], axis=1)
    hits = hits.sort_values(["replicated", "effect"], ascending=[False, True])
    hits.round(5).to_csv(os.path.join(OUT, "hits.csv"), index=False)
    with open(os.path.join(OUT, "alterations.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["gene", "kind", "role", "anchor", "source", "patients_altered", "patients_tested", "patient_rate", "lines_altered", "scanned"])
        w.writeheader()
        for a in alts:
            w.writerow({k: (round(a[k], 4) if isinstance(a.get(k), float) else a.get(k, "")) for k in w.fieldnames})

    repd = hits[hits["replicated"] == "yes"]
    headline = repd[(repd["label"] == "")]
    S = {"gene_changes_listed": len(alts), "anchors": sum(a["role"] == "anchor" for a in alts), "passengers": sum(a["role"] == "passenger" for a in alts),
         "gene_changes_scanned": len(scanned), "blocks": len(set(block_name.values())), "cell_lines": len(lines), "dependency_genes": len(dep_genes),
         "pairs_tested": int(n_tests), "hits": int(len(hits)), "hits_by_replication": hits["replicated"].value_counts().to_dict(),
         "replicated_hits": int(len(repd)), "replicated_self_or_coamplified": int((repd["label"] != "").sum()),
         "replicated_known": sorted(f'{b} -> {d}' for b, d in zip(repd[repd["known_pair"] == "yes"]["block"], repd[repd["known_pair"] == "yes"]["dependency"])),
         "P24_9p21_known_pair_replicated": bool(((repd["block"] == "9p21 loss") & repd["dependency"].isin(KNOWN["9p21"])).any()),
         "replicated_not_on_known_list": [{"block": r["block"], "dependency": r["dependency"], "effect": r["effect"], "rnai_effect": r["rnai_effect"],
                                           "drug": r["drug"], "drug_phase": r["drug_phase"], "label": r["label"]}
                                          for _, r in repd[repd["known_pair"] != "yes"].iterrows()],
         "P25_replicated_unlisted_with_drug": bool(((headline["known_pair"] != "yes") & (headline["drug"].fillna("") != "")).any())}
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)

    # figure: replicated hits, knockout and knockdown effects side by side
    rows = repd.sort_values("effect").head(24)
    W, rowh, left, top = 860, 26, 330, 92
    H = top + rowh * len(rows) + 56
    lo = min(-0.2, float(min(rows["effect"].min(), rows["rnai_effect"].min()))) - 0.1 if len(rows) else -1
    X = lambda v: left + (v - lo) / (0.1 - lo) * (W - left - 40)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="13">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">Dependencies that go with osteosarcoma\'s gene changes, across all cancer cell lines</text>',
         '<text x="16" y="50" fill="#525b6b">Hits that replicated. Further left = cells with the gene change depend on the gene more.</text>',
         '<text x="16" y="68" fill="#525b6b">Blue: knockout screen (discovery). Gold: knockdown screen (replication).</text>']
    v = math.ceil(lo / 0.2) * 0.2
    while v <= 0.1:
        s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{top + rowh * len(rows)}" stroke="{"#525b6b" if abs(v) < 1e-9 else "#e2e5ea"}"/>')
        s.append(f'<text x="{X(v):.1f}" y="{top + rowh * len(rows) + 18}" text-anchor="middle" fill="#525b6b" font-size="12">{v:.1f}</text>')
        v += 0.2
    for k, (_, r) in enumerate(rows.iterrows()):
        y = top + rowh * k + rowh / 2
        tag = " (known)" if r["known_pair"] == "yes" else (f' ({r["label"]})' if r["label"] else "")
        s.append(f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" fill="#14181f" font-size="12">{r["block"]} → {r["dependency"]}{tag}</text>')
        s.append(f'<line x1="{X(0):.1f}" y1="{y - 4:.1f}" x2="{X(r["effect"]):.1f}" y2="{y - 4:.1f}" stroke="#1c5cab" stroke-width="6"/>')
        s.append(f'<line x1="{X(0):.1f}" y1="{y + 5:.1f}" x2="{X(r["rnai_effect"]):.1f}" y2="{y + 5:.1f}" stroke="#f7c020" stroke-width="6"/>')
    s.append(f'<text x="{(left + W - 40) / 2:.0f}" y="{H - 14}" text-anchor="middle" fill="#525b6b" font-size="12">Lineage-adjusted difference in dependency score, altered minus not altered</text>')
    s.append("</svg>")
    open(os.path.join(FIG, "engine08_scan.svg"), "w").write("\n".join(s))

    print(json.dumps({k: v for k, v in S.items() if k != "replicated_not_on_known_list"}, indent=1, default=float))
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 200)
    cols = ["block", "altered_gene", "dependency", "label", "known_pair", "effect", "q", "lines_altered", "rnai_effect", "rnai_altered", "replicated",
            "os_altered_lines", "os_difference", "sarcoma_altered_lines", "sarcoma_difference", "drug", "drug_phase", "patient_rate"]
    print(hits[cols].round(3).to_string(index=False))
    print("\nGene changes:")
    for a in alts:
        print(f'  {a["kind"]:13s} {a["gene"]:10s} {a["role"]:9s} anchor {a["anchor"]:8s} patients {a["patients_altered"]}/{a["patients_tested"]} lines {a.get("lines_altered", 0)} scanned {a.get("scanned")}')


if __name__ == "__main__":
    main()
