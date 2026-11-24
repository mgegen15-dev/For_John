#!/usr/bin/env python3
"""Engine cycle 9: weaknesses that go with loss of the tumour-suppressor genes osteosarcoma loses most often.

A discovery scan, not a test. Pre-registered in research_notes/Engine/cycle-09-suppressor-scan/PREREGISTRATION.md.
Reuses the scan machinery of tools/engine_cycle08_scan.py.

  python3 tools/engine_cycle09_suppressor_scan.py fetch   mutation tables from DepMap's Figshare release; patient mutations from cBioPortal
  python3 tools/engine_cycle09_suppressor_scan.py         analyse

Outputs: data/engine/cycle09/ (loss_calls.csv, controls.csv, hits.csv, patients.csv, summary.json), docs/figures/engine09_scan.svg
"""
import collections
import csv
import json
import math
import os
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle03_9p21 as c3          # noqa: E402
import engine_cycle07_ccne1 as c7         # noqa: E402
import engine_cycle08_scan as c8          # noqa: E402

ROOT = os.path.dirname(HERE)
DEP = c8.DEP
OUT = os.path.join(ROOT, "data", "engine", "cycle09")
FIG = os.path.join(ROOT, "docs", "figures")
GENES = ["RB1", "TP53", "ATRX", "PTEN", "NF1"]
ENTREZ = {"RB1": 5925, "TP53": 7157, "ATRX": 546, "PTEN": 5728, "NF1": 4763}
EFFECT, FDR, MIN_LINES, MIN_RNAI = -0.2, 0.05, 10, 5
KNOWN = {"RB1": {"SKP2", "CDK2", "E2F3", "CCNE1", "AURKA", "AURKB", "CHEK1", "PLK1", "TTK"},
         "PTEN": {"PIK3CB", "AKT1", "AKT2", "AKT3", "PIK3R2", "MTOR"},
         "NF1": {"PTPN11", "SOS1", "KRAS", "NRAS", "RAF1", "MAP2K1", "MAPK1", "SHOC2"},
         "ATRX": {"ATR", "FANCM", "BLM", "RMI1", "RMI2", "TOP3A", "SMARCAL1", "SLX4"}, "TP53": set()}
CONTROLS = {"TP53": ["MDM2"], "RB1": ["CDK4", "CDK6", "CCND1"]}
FILES = {"OmicsSomaticMutationsMatrixDamaging.csv": 51065747, "OmicsSomaticMutationsMatrixHotspot.csv": 51065750, "OmicsSignatures.csv": 51065726}
TRUNCATING = {"Nonsense_Mutation", "Frame_Shift_Del", "Frame_Shift_Ins", "Splice_Site", "Nonstop_Mutation", "Translation_Start_Site"}


def fetch():
    for name, fid in FILES.items():
        out = os.path.join(DEP, name)
        if not (os.path.exists(out) and os.path.getsize(out) > 10000):
            subprocess.run(["curl", "-sS", "-L", "--retry", "4", "-o", out, f"https://ndownloader.figshare.com/files/{fid}"], check=True)
    os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
    out = os.path.join(OUT, "raw", "msk_mutations.json")
    if not os.path.exists(out):
        d = json.load(open(os.path.join(c3.RAW, "msk_impact_50k_2026.json")))
        muts = c3.api("/molecular-profiles/msk_impact_50k_2026_mutations/mutations/fetch?projection=DETAILED",
                      {"sampleIds": d["samples"], "entrezGeneIds": list(ENTREZ.values())})
        json.dump([{"sampleId": m["sampleId"], "gene": m["gene"]["hugoGeneSymbol"], "type": m["mutationType"],
                    "change": m.get("proteinChange", "")} for m in muts], open(out, "w"))
        print(len(muts), "mutation calls in the five genes")


# ------------------------------------------------------------------ loss calls
def loss_calls(lines):
    dam = c8.read_cols("OmicsSomaticMutationsMatrixDamaging.csv", set(GENES)).reindex(lines)
    hot = c8.read_cols("OmicsSomaticMutationsMatrixHotspot.csv", set(GENES)).reindex(lines)
    cn = c8.read_cols("OmicsCNGene.csv", set(GENES)).reindex(lines)
    ex = c8.read_cols("OmicsExpressionProteinCodingGenesTPMLogp1.csv", set(GENES)).reindex(lines)
    calls = pd.DataFrame(index=lines)
    for g in GENES:
        d = dam[g] if g in dam else pd.Series(np.nan, index=lines)
        c = cn[g] if g in cn else pd.Series(np.nan, index=lines)
        if g == "TP53":
            h = hot[g] if g in hot else pd.Series(np.nan, index=lines)
            parts = [d > 0, h > 0, c < 0.25]
            avail = d.notna() & h.notna() & c.notna()
        else:
            e = ex[g] if g in ex else pd.Series(np.nan, index=lines)
            parts = [d > 0, c < 0.25, e < 1.0]
            avail = d.notna() & c.notna() & e.notna()
        lost = parts[0] | parts[1] | parts[2]
        calls[g] = np.where(lost, 1.0, np.where(avail, 0.0, np.nan))      # any route to loss counts; intact needs all measures
        calls[f"{g}_routes"] = ["+".join(n for n, p in zip(("mutation", "hotspot" if g == "TP53" else "deletion", "deletion" if g == "TP53" else "low RNA"), ps) if p)
                                for ps in zip(*[p.fillna(False).values for p in parts])]
    return calls


# ------------------------------------------------------------------ patients
def patient_frequency():
    units, _ = c3.one_per_patient(c7.load("msk_impact_50k_2026"))
    muts = json.load(open(os.path.join(OUT, "raw", "msk_mutations.json")))
    by = collections.defaultdict(lambda: collections.defaultdict(set))
    for m in muts:
        if m["type"] in TRUNCATING or (m["gene"] == "TP53" and m["type"] == "Missense_Mutation"):
            by[m["sampleId"]][m["gene"]].add(m["type"])
    rows, out = [], {}
    for g in GENES:
        us = [u for u in units if u["genes_on_panel"] is None or g in u["genes_on_panel"]]
        dele = sum(g in u["dels"] for u in us)
        mut = sum(bool(by[u["sample"]].get(g)) for u in us)
        either = sum((g in u["dels"]) or bool(by[u["sample"]].get(g)) for u in us)
        out[g] = {"patients": len(us), "deep_deletion": dele, "truncating_or_hotspot_mutation": mut, "either": either, "share": either / len(us)}
        rows.append([g, len(us), dele, mut, either, round(either / len(us), 3)])
    with open(os.path.join(OUT, "patients.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gene", "patients_tested", "deep_deletion", "truncating_or_TP53_missense_mutation", "either", "share"])
        w.writerows(rows)
    return out


# ------------------------------------------------------------------ main
def main():
    os.makedirs(OUT, exist_ok=True)
    model = pd.read_csv(os.path.join(DEP, "Model.csv"), index_col=0)
    crispr = pd.read_csv(os.path.join(DEP, "CRISPRGeneEffect.csv"), index_col=0)
    crispr.columns = [c.split(" (")[0] for c in crispr.columns]
    crispr = crispr.loc[:, ~crispr.columns.duplicated()]
    crispr = crispr.loc[:, crispr.isna().mean() <= 0.05]
    lines = [i for i in crispr.index if i in model.index and isinstance(model.loc[i, "OncotreeLineage"], str)]
    crispr = crispr.loc[lines]
    lineage = model.loc[lines, "OncotreeLineage"].values
    Y = crispr.values.astype(float)
    for lin in np.unique(lineage):
        m = lineage == lin
        sub = Y[m]
        mu = np.nanmean(sub, axis=0)
        mu = np.where(np.isnan(mu), np.nanmean(Y, axis=0), mu)
        idx = np.where(np.isnan(sub))
        sub[idx] = mu[idx[1]]
        Y[m] = sub
    dep = list(crispr.columns)
    col = {g: j for j, g in enumerate(dep)}
    calls = loss_calls(lines)
    text = (model["OncotreePrimaryDisease"].fillna("") + " " + model["OncotreeSubtype"].fillna("")).str.lower()
    is_os = text.reindex(lines).str.contains("osteosarcoma").values
    is_sarc = model.loc[lines, "OncotreeLineage"].isin(["Bone", "Soft Tissue"]).values

    # RNAi
    d2 = pd.read_csv(os.path.join(DEP, "D2_combined_gene_dep_scores.csv"), index_col=0)
    d2.index = [i.split(" (")[0] for i in d2.index]
    ccle = {str(v): k for k, v in model["CCLEName"].dropna().items()}
    d2.columns = [ccle.get(c) for c in d2.columns]
    d2 = d2.loc[:, [c is not None for c in d2.columns]]
    d2 = d2.loc[~d2.index.duplicated(), ~d2.columns.duplicated()]
    rn_lines = [l for l in d2.columns if l in model.index and isinstance(model.loc[l, "OncotreeLineage"], str)]
    rn_lineage = model.loc[rn_lines, "OncotreeLineage"].values
    rn_calls = loss_calls(rn_lines)

    def rnai(gene, dg):
        if dg not in d2.index:
            return {"rnai_effect": np.nan, "rnai_lo": np.nan, "rnai_hi": np.nan, "rnai_lost": 0}
        y = d2.loc[dg, rn_lines].values.astype(float)
        alt = rn_calls[gene].values
        ok = ~np.isnan(alt) & ~np.isnan(y)
        n = int(np.nansum(alt[ok]))
        out = {"rnai_effect": np.nan, "rnai_lo": np.nan, "rnai_hi": np.nan, "rnai_lost": n}
        if n >= MIN_RNAI:
            r = c8.scan_matrix(y[ok][:, None], [dg], rn_lineage[ok], alt[ok])
            if r is not None:
                b, se, p, df = r
                tq = stats.t.ppf(0.975, df)
                out.update(rnai_effect=float(b[0]), rnai_lo=float(b[0] - tq * se[0]), rnai_hi=float(b[0] + tq * se[0]))
        return out

    S = {"genes": {}, "controls": {}}
    results, status = [], {}
    for g in GENES:
        alt = calls[g].values
        ok = ~np.isnan(alt)
        n_lost, n_int = int(np.nansum(alt)), int((alt[ok] == 0).sum())
        routes = collections.Counter(r for r, a in zip(calls[f"{g}_routes"], alt) if a == 1)
        S["genes"][g] = {"lines_lost": n_lost, "lines_intact": n_int, "routes": dict(routes.most_common()),
                         "osteosarcoma_lines_lost": int(np.nansum(alt[is_os])), "osteosarcoma_lines_with_call": int(ok[is_os].sum())}
        if n_lost < MIN_LINES or n_int < MIN_LINES:
            S["genes"][g]["scanned"] = False
            continue
        S["genes"][g]["scanned"] = True
        r = c8.scan_matrix(Y[ok], dep, lineage[ok], alt[ok])
        beta, se, p, df = r
        status[g] = (alt, ok)
        tq = stats.t.ppf(0.975, df)
        for cg in CONTROLS.get(g, []):
            j = col.get(cg)
            if j is not None:
                S["controls"].setdefault(g, {})[cg] = {"effect": float(beta[j]), "lo": float(beta[j] - tq * se[j]), "hi": float(beta[j] + tq * se[j]),
                                                       "passes": bool(beta[j] - tq * se[j] > 0)}
        for j, dg in enumerate(dep):
            if dg != g:
                results.append((g, dg, beta[j], se[j], p[j]))
    passed = {g: any(v["passes"] for v in S["controls"].get(g, {}).values()) for g in CONTROLS if g in S["controls"]}
    S["controls_passed"] = passed
    res = pd.DataFrame(results, columns=["lost_gene", "dependency", "effect", "se", "p"])
    res["q"] = c8.bh(res["p"].values)
    hits = res[(res["effect"] <= EFFECT) & (res["q"] < FDR)].copy().reset_index(drop=True)
    drug = {r["gene"]: (r["best_drug"], r["best_drug_phase"]) for r in csv.DictReader(open(os.path.join(ROOT, "data", "osteosarcoma_repurposing_candidates.csv")))}
    extra = []
    for _, h in hits.iterrows():
        d = rnai(h["lost_gene"], h["dependency"])
        d["replicated"] = "not testable" if d["rnai_lost"] < MIN_RNAI or np.isnan(d["rnai_effect"]) else ("yes" if d["rnai_hi"] < 0 else "no")
        alt, ok = status[h["lost_gene"]]
        y = Y[:, col[h["dependency"]]]
        for lab, mask in (("os", is_os), ("sarcoma", is_sarc)):
            a_, b_ = y[mask & ok & (alt == 1)], y[mask & ok & (alt == 0)]
            d[f"{lab}_lost_lines"], d[f"{lab}_intact_lines"] = len(a_), len(b_)
            d[f"{lab}_difference"] = float(a_.mean() - b_.mean()) if len(a_) and len(b_) else np.nan
        d["known_pair"] = "yes" if h["dependency"] in KNOWN[h["lost_gene"]] else ""
        d["control_passed"] = passed.get(h["lost_gene"], "no control")
        d["drug"], d["drug_phase"] = drug.get(h["dependency"], ("", ""))
        d["mean_score_lost"], d["mean_score_intact"] = float(y[ok & (alt == 1)].mean()), float(y[ok & (alt == 0)].mean())
        extra.append(d)
    hits = pd.concat([hits, pd.DataFrame(extra)], axis=1) if len(hits) else hits
    if len(hits):
        hits = hits.sort_values(["replicated", "effect"], ascending=[False, True])
    hits.round(5).to_csv(os.path.join(OUT, "hits.csv"), index=False)
    calls.to_csv(os.path.join(OUT, "loss_calls.csv"))
    with open(os.path.join(OUT, "controls.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lost_gene", "control_dependency", "effect", "ci_low", "ci_high", "passes"])
        for g, v in S["controls"].items():
            for cg, x in v.items():
                w.writerow([g, cg, f'{x["effect"]:.3f}', f'{x["lo"]:.3f}', f'{x["hi"]:.3f}', x["passes"]])
    # exploratory, added after the scan (see the report): ATRX pairs without microsatellite-unstable lines
    sig = pd.read_csv(os.path.join(DEP, "OmicsSignatures.csv"), index_col=0)["MSIScore"].reindex(lines).values
    S["exploratory_atrx_without_msi_high"] = {}
    for dg in ("WRN", "FANCM", "SMARCAL1", "PELO", "ATR"):
        if dg not in col:
            continue
        alt, ok = status["ATRX"]
        keep = ok & ~np.isnan(sig) & (sig <= 20)
        r = c8.scan_matrix(Y[keep][:, [col[dg]]], [dg], lineage[keep], alt[keep])
        if r is not None:
            b, se_, p_, df_ = r
            tq = stats.t.ppf(0.975, df_)
            S["exploratory_atrx_without_msi_high"][dg] = {"lost_lines": int(alt[keep].sum()), "effect": float(b[0]),
                                                          "lo": float(b[0] - tq * se_[0]), "hi": float(b[0] + tq * se_[0])}
    a_, o_ = status["ATRX"]
    S["atrx_msi_high_share"] = {"lost": float(np.nanmean(sig[o_ & (a_ == 1)] > 20)), "intact": float(np.nanmean(sig[o_ & (a_ == 0)] > 20))}
    S["patients"] = patient_frequency()
    repd = hits[hits["replicated"] == "yes"] if len(hits) else hits
    S.update({"cell_lines": len(lines), "dependency_genes": len(dep), "pairs_tested": int(len(res)), "hits": int(len(hits)),
              "hits_by_replication": hits["replicated"].value_counts().to_dict() if len(hits) else {},
              "replicated": [{k: (r[k] if not isinstance(r[k], float) else round(r[k], 3)) for k in ("lost_gene", "dependency", "effect", "rnai_effect", "known_pair", "drug", "drug_phase")}
                             for _, r in repd.iterrows()],
              "P26_controls_pass": bool(passed.get("TP53") and passed.get("RB1")),
              "P27_known_replicated": bool(len(repd) and ((repd["known_pair"] == "yes") & repd["lost_gene"].isin(["RB1", "PTEN", "NF1", "ATRX"])).any()),
              "P28_unlisted_with_drug": bool(len(repd) and ((repd["known_pair"] != "yes") & (repd["drug"].fillna("") != "")).any())})
    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)

    # figure
    rows = repd.sort_values("effect").head(24) if len(repd) else repd
    if len(rows):
        W, rowh, left, top = 860, 26, 300, 92
        H = top + rowh * len(rows) + 56
        lo = min(-0.2, float(min(rows["effect"].min(), rows["rnai_effect"].min()))) - 0.1
        X = lambda v: left + (v - lo) / (0.1 - lo) * (W - left - 40)
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="13">',
             f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
             '<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">Dependencies that go with loss of five tumour-suppressor genes</text>',
             '<text x="16" y="50" fill="#525b6b">Hits that replicated, across all cancer cell lines. Further left = cells without the gene depend on it more.</text>',
             '<text x="16" y="68" fill="#525b6b">Blue: knockout screen (discovery). Gold: knockdown screen (replication).</text>']
        v = math.ceil(lo / 0.2) * 0.2
        while v <= 0.1:
            s.append(f'<line x1="{X(v):.1f}" y1="{top - 6}" x2="{X(v):.1f}" y2="{top + rowh * len(rows)}" stroke="{"#525b6b" if abs(v) < 1e-9 else "#e2e5ea"}"/>')
            s.append(f'<text x="{X(v):.1f}" y="{top + rowh * len(rows) + 18}" text-anchor="middle" fill="#525b6b" font-size="12">{v:.1f}</text>')
            v += 0.2
        for k, (_, r) in enumerate(rows.iterrows()):
            y = top + rowh * k + rowh / 2
            tag = " (known)" if r["known_pair"] == "yes" else ""
            s.append(f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" fill="#14181f" font-size="12">{r["lost_gene"]} lost → {r["dependency"]}{tag}</text>')
            s.append(f'<line x1="{X(0):.1f}" y1="{y - 4:.1f}" x2="{X(r["effect"]):.1f}" y2="{y - 4:.1f}" stroke="#1c5cab" stroke-width="6"/>')
            s.append(f'<line x1="{X(0):.1f}" y1="{y + 5:.1f}" x2="{X(r["rnai_effect"]):.1f}" y2="{y + 5:.1f}" stroke="#f7c020" stroke-width="6"/>')
        s.append(f'<text x="{(left + W - 40) / 2:.0f}" y="{H - 14}" text-anchor="middle" fill="#525b6b" font-size="12">Lineage-adjusted difference in dependency score, lost minus intact</text>')
        s.append("</svg>")
        open(os.path.join(FIG, "engine09_scan.svg"), "w").write("\n".join(s))

    print(json.dumps({k: v for k, v in S.items() if k != "replicated"}, indent=1, default=float))
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 300)
    if len(hits):
        print(hits[["lost_gene", "dependency", "known_pair", "effect", "q", "rnai_effect", "rnai_lo", "rnai_hi", "rnai_lost", "replicated", "os_lost_lines",
                    "os_difference", "sarcoma_lost_lines", "sarcoma_difference", "drug", "drug_phase"]].round(3).to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
    else:
        main()
