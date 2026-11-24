#!/usr/bin/env python3
"""Engine cycle 3: is deep deletion of 9p21 (CDKN2A, MTAP) more common in osteosarcoma at relapse than in primary tumours?

Runs the analysis pre-registered in research_notes/Engine/cycle-03-9p21/PREREGISTRATION.md
(plan committed before any cBioPortal study was listed; study choices committed before any
copy-number call was read).

  python3 tools/engine_cycle03_9p21.py fetch    download from the public cBioPortal API into data/engine/cycle03/raw/
  python3 tools/engine_cycle03_9p21.py          analyse (default)

Outputs: data/engine/cycle03/results.csv, summary.json, patients.csv, docs/figures/engine03_9p21.svg
"""
import collections
import csv
import json
import math
import os
import re
import sys
import time
import urllib.request

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "engine", "cycle03", "raw")
OUT = os.path.join(ROOT, "data", "engine", "cycle03")
FIG = os.path.join(ROOT, "docs", "figures")
API = "https://www.cbioportal.org/api"
TEST_STUDIES = ["msk_impact_50k_2026", "pan_origimed_2020"]
ALL_STUDIES = TEST_STUDIES + ["pancan_mappyacts_2022", "os_target_gdc", "pancan_pcawg_2020"]
LABEL = {"msk_impact_50k_2026": "MSK-IMPACT (New York)", "pan_origimed_2020": "OrigiMed (China)",
         "pancan_mappyacts_2022": "MAPPYACTS (Europe, relapse trial)", "os_target_gdc": "TARGET-OS (diagnosis)",
         "pancan_pcawg_2020": "PCAWG (primary tumours)"}
GENES = {"CDKN2A": 1029, "CDKN2B": 1030, "MTAP": 4507}
RELAPSE_TYPES = {"metastasis", "local recurrence", "recurrent", "recurrence", "relapse", "metastatic"}
Z95 = 1.959964


# ------------------------------------------------------------------ fetch
def api(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Accept": "application/json", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=300))
        except Exception as e:                       # noqa: BLE001
            err = e
            time.sleep(4)
    raise err


def fetch():
    os.makedirs(RAW, exist_ok=True)
    for sid in ALL_STUDIES:
        out = os.path.join(RAW, f"{sid}.json")
        if os.path.exists(out):
            continue
        rows = []
        for att in ("CANCER_TYPE_DETAILED", "CANCER_TYPE"):
            rows += api(f"/studies/{sid}/clinical-data?clinicalDataType=SAMPLE&attributeId={att}&projection=SUMMARY&pageSize=10000000")
        samples = sorted({r["sampleId"] for r in rows if "osteosarcoma" in r["value"].lower()})
        patient_of = {r["sampleId"]: r["patientId"] for r in rows}
        clin = api("/clinical-data/fetch?clinicalDataType=SAMPLE&projection=SUMMARY",
                   {"identifiers": [{"entityId": s, "studyId": sid} for s in samples]})
        profiles = api(f"/studies/{sid}/molecular-profiles")
        cna = [p["molecularProfileId"] for p in profiles
               if p["molecularAlterationType"] == "COPY_NUMBER_ALTERATION" and p["datatype"] == "DISCRETE"]
        d = {"study": sid, "samples": samples, "patient_of": {s: patient_of[s] for s in samples}, "clinical": clin,
             "cna_profile": cna[0] if cna else None, "panel": [], "homdel": [], "panels": {}}
        if cna:
            d["panel"] = api(f"/molecular-profiles/{cna[0]}/gene-panel-data/fetch", {"sampleIds": samples})
            d["homdel"] = api(f"/molecular-profiles/{cna[0]}/discrete-copy-number/fetch?discreteCopyNumberEventType=HOMDEL&projection=DETAILED",
                              {"sampleIds": samples})
            for pid in sorted({x.get("genePanelId") for x in d["panel"] if x.get("genePanelId")}):
                d["panels"][pid] = [g["hugoGeneSymbol"] for g in api(f"/gene-panels/{pid}")["genes"]]
        json.dump(d, open(out, "w"))
        print(sid, len(samples), "samples;", len(d["homdel"]), "deep-deletion calls; profile", d["cna_profile"])
    # Which of the three genes does each study report at all? (Some tests do not cover MTAP.)
    for sid in ALL_STUDIES:
        out = os.path.join(RAW, f"{sid}.json")
        d = json.load(open(out))
        if "reported" not in d and d["cna_profile"]:
            r = api(f"/molecular-profiles/{d['cna_profile']}/molecular-data/fetch?projection=SUMMARY",
                    {"sampleIds": d["samples"], "entrezGeneIds": list(GENES.values())})
            ids = {x["entrezGeneId"] for x in r}
            d["reported"] = [g for g, e in GENES.items() if e in ids]
            json.dump(d, open(out, "w"))
            print(sid, "reports", d["reported"])


# ------------------------------------------------------------------ data
def load(sid):
    d = json.load(open(os.path.join(RAW, f"{sid}.json")))
    clin = collections.defaultdict(dict)
    for r in d["clinical"]:
        clin[r["sampleId"]][r["clinicalAttributeId"]] = r["value"]
    panel = {x["sampleId"]: x for x in d["panel"]}
    dels = collections.defaultdict(set)
    for e in d["homdel"]:
        dels[e["sampleId"]].add(e["gene"]["hugoGeneSymbol"])
    samples = []
    for s in d["samples"]:
        px = panel.get(s, {})
        if not px.get("profiled"):
            continue                                   # no copy-number profile
        c = clin[s]
        stype = c.get("SAMPLE_TYPE", "").strip().lower()
        pur = c.get("TUMOR_PURITY", c.get("TUMOR_PURTITY"))
        try:
            pur = float(str(pur).replace("%", ""))
        except (TypeError, ValueError):
            pur = None
        if pur is not None and pur <= 1:
            pur *= 100
        pid = px.get("genePanelId")
        samples.append({"sample": s, "patient": d["patient_of"][s], "type": stype,
                        "group": "R" if stype in RELAPSE_TYPES else ("P" if stype == "primary" else None),
                        "panel": pid, "genes_on_panel": set(d["panels"][pid]) if pid in d["panels"] else None,
                        "not_reported": set(GENES) - set(d.get("reported", GENES)),
                        "dels": dels.get(s, set()), "purity": pur, "met_site": c.get("METASTATIC_SITE", ""),
                        "fga": float(c["FRACTION_GENOME_ALTERED"]) if c.get("FRACTION_GENOME_ALTERED") not in (None, "", "NA") else None})
    return d, samples


def order_key(s):
    m = re.search(r"-T(\d+)-", s["sample"])
    return (int(m.group(1)) if m else 0, s["sample"])


def one_per_patient(samples):
    """Pre-registered rule: any metastasis or relapse sample puts the patient in group R (most recent such sample);
    otherwise group P (first primary sample)."""
    by = collections.defaultdict(list)
    for s in samples:
        if s["group"]:
            by[s["patient"]].append(s)
    out, paired = [], []
    for pid, ss in by.items():
        rel = sorted([s for s in ss if s["group"] == "R"], key=order_key)
        pri = sorted([s for s in ss if s["group"] == "P"], key=order_key)
        out.append(rel[-1] if rel else pri[0])
        if rel and pri:
            paired.append((pri[0], rel[-1]))
    return out, paired


def covered(s, gene):
    """Is the gene measured for this sample? By the panel's gene list where there is one; otherwise by
    whether the study reports the gene at all."""
    if gene in s["not_reported"]:
        return False
    return s["genes_on_panel"] is None or gene in s["genes_on_panel"]


# ------------------------------------------------------------------ statistics
def wilson(k, n):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    den = 1 + Z95 ** 2 / n
    c = (p + Z95 ** 2 / (2 * n)) / den
    h = Z95 * math.sqrt(p * (1 - p) / n + Z95 ** 2 / (4 * n * n)) / den
    return p, max(0.0, c - h), min(1.0, c + h)


def table(units, gene):
    us = [u for u in units if covered(u, gene)]
    a = sum(gene in u["dels"] for u in us if u["group"] == "R")
    b = sum(u["group"] == "R" for u in us) - a
    c = sum(gene in u["dels"] for u in us if u["group"] == "P")
    d = sum(u["group"] == "P" for u in us) - c
    return a, b, c, d


def log_or(a, b, c, d):
    if min(a + b, c + d) == 0:
        return None
    if 0 in (a, b, c, d):
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    return {"b": math.log(a * d / (b * c)), "se": math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)}


def pool(effects):
    effects = [e for e in effects if e]
    if not effects:
        return None
    b = np.array([e["b"] for e in effects])
    se = np.array([e["se"] for e in effects])
    w = 1 / se ** 2
    bf, sef = float((w * b).sum() / w.sum()), float(math.sqrt(1 / w.sum()))
    k = len(b)
    q = float((w * (b - bf) ** 2).sum())
    tau2 = max(0.0, (q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0
    wr = 1 / (se ** 2 + tau2)
    br, ser = float((wr * b).sum() / wr.sum()), float(math.sqrt(1 / wr.sum()))
    f = lambda x, s: {"or": math.exp(x), "lo": math.exp(x - Z95 * s), "hi": math.exp(x + Z95 * s),
                      "p": float(2 * stats.norm.sf(abs(x / s)))}
    return dict(f(bf, sef), random=f(br, ser), I2=max(0.0, (q - (k - 1)) / q) if q > 0 and k > 1 else 0.0, k=k)


def logistic(y, X, iters=60):
    """Plain Newton logistic regression. Returns coefficients and standard errors."""
    X = np.column_stack([np.ones(len(y)), X])
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ beta))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + 1e-8 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        beta += step
        if np.abs(step).max() < 1e-9:
            break
    return beta, np.sqrt(np.diag(np.linalg.inv(H)))


def verdict(m):
    if m["lo"] > 1.0 and m["or"] >= 1.5:
        return "Supported"
    if m["hi"] < 1.5:
        return "Refuted"
    return "Inconclusive"


def fmt_or(m):
    return f'{m["or"]:.2f} ({m["lo"]:.2f}-{m["hi"]:.2f})'


# ------------------------------------------------------------------ figure
def bars_svg(rows, path, title, sub):
    """Horizontal percentages with Wilson intervals. rows: (label, pct, lo, hi, kind) or (label, None...) for a heading."""
    W, rowh, left, right = 900, 32, 440, 130
    H = 92 + rowh * len(rows) + 40
    mx = 60.0
    Xp = lambda v: left + min(v, mx) / mx * (W - left - right)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" font-size="14">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="16" y="28" font-size="16" font-weight="600" fill="#14181f">{title}</text>',
         f'<text x="16" y="50" font-size="13" fill="#525b6b">{sub[0]}</text>',
         f'<text x="16" y="68" font-size="13" fill="#525b6b">{sub[1]}</text>']
    top = 92
    for v in (0, 20, 40, 60):
        s.append(f'<line x1="{Xp(v):.1f}" y1="{top - 6}" x2="{Xp(v):.1f}" y2="{top + rowh * len(rows)}" stroke="#e2e5ea"/>')
        s.append(f'<text x="{Xp(v):.1f}" y="{top + rowh * len(rows) + 20}" text-anchor="middle" fill="#525b6b" font-size="12">{v}%</text>')
    for k, (lab, pct, lo, hi, kind) in enumerate(rows):
        y = top + rowh * k + rowh / 2
        if pct is None:
            s.append(f'<text x="16" y="{y + 5:.1f}" fill="#14181f" font-weight="600">{lab}</text>')
            continue
        col = {"P": "#6a7384", "R": "#1c5cab", "ref": "#a8b0bd"}[kind]
        s.append(f'<text x="28" y="{y + 5:.1f}" fill="#14181f">{lab}</text>')
        s.append(f'<rect x="{Xp(0):.1f}" y="{y - 8:.1f}" width="{max(Xp(pct) - Xp(0), 1):.1f}" height="16" fill="{col}"/>')
        s.append(f'<line x1="{Xp(lo):.1f}" y1="{y:.1f}" x2="{Xp(hi):.1f}" y2="{y:.1f}" stroke="#14181f" stroke-width="1.5"/>')
        s.append(f'<text x="{W - 8}" y="{y + 5:.1f}" text-anchor="end" fill="#525b6b" font-size="12">{pct:.0f}% ({lo:.0f}-{hi:.0f}%)</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


# ------------------------------------------------------------------ main
def analyse():
    os.makedirs(FIG, exist_ok=True)
    S = {"studies": {}, "primary": {}, "secondary": {}, "checks": {}, "descriptive": {}, "reference": {}}
    rows_out, patients_out = [], []
    units, paired, all_samples = {}, {}, {}
    for sid in TEST_STUDIES:
        d, samples = load(sid)
        all_samples[sid] = [s for s in samples if s["group"]]
        units[sid], paired[sid] = one_per_patient(samples)
        S["studies"][sid] = {"cna_profile": d["cna_profile"], "osteosarcoma_samples": len(d["samples"]),
                             "samples_with_copy_number": len(samples), "patients": len(units[sid]),
                             "group_R": sum(u["group"] == "R" for u in units[sid]), "group_P": sum(u["group"] == "P" for u in units[sid]),
                             "types_R": dict(collections.Counter(u["type"] for u in units[sid] if u["group"] == "R")),
                             "panels": dict(collections.Counter(str(u["panel"]) for u in units[sid]))}
        for u in units[sid]:
            patients_out.append([sid, u["patient"], u["sample"], u["type"], u["group"], u["panel"] or "", u["purity"] if u["purity"] is not None else "",
                                 int("CDKN2A" in u["dels"]), int("CDKN2B" in u["dels"]) if covered(u, "CDKN2B") else "",
                                 int("MTAP" in u["dels"]) if covered(u, "MTAP") else "", len(u["dels"])])

    def compare(gene, sel=lambda u: True, key="units"):
        per, tabs = {}, {}
        for sid in TEST_STUDIES:
            src = units[sid] if key == "units" else all_samples[sid]
            t = table([u for u in src if sel(u)], gene)
            tabs[sid] = t
            per[sid] = log_or(*t)
        tot = [sum(t[i] for t in tabs.values()) for i in range(4)]
        return {"tables": tabs, "per_study": {k: ({"or": math.exp(v["b"]), "lo": math.exp(v["b"] - Z95 * v["se"]), "hi": math.exp(v["b"] + Z95 * v["se"])} if v else None)
                                              for k, v in per.items()},
                "pooled": pool(per.values()), "R": wilson(tot[0], tot[0] + tot[1]) + (tot[0], tot[0] + tot[1]),
                "P": wilson(tot[2], tot[2] + tot[3]) + (tot[2], tot[2] + tot[3])}

    # ---- primary
    prim = compare("CDKN2A")
    S["primary"] = prim
    S["primary"]["verdict"] = verdict(prim["pooled"])
    nR, nP = prim["R"][4], prim["P"][4]
    S["primary"]["underpowered"] = min(nR, nP) < 100

    def emit(analysis, gene, res):
        for sid, t in res["tables"].items():
            o = res["per_study"][sid]
            rows_out.append([analysis, LABEL[sid], gene, t[0], t[0] + t[1], t[2], t[2] + t[3],
                             f'{o["or"]:.3f}' if o else "", f'{o["lo"]:.3f}' if o else "", f'{o["hi"]:.3f}' if o else ""])
        m = res["pooled"]
        if m:
            rows_out.append([analysis, "pooled (fixed)", gene, res["R"][3], res["R"][4], res["P"][3], res["P"][4],
                             f'{m["or"]:.3f}', f'{m["lo"]:.3f}', f'{m["hi"]:.3f}'])
    emit("primary", "CDKN2A", prim)

    # ---- purity
    pur = {}
    for sid in TEST_STUDIES:
        us = [u for u in units[sid] if u["purity"] is not None]
        r = [u["purity"] for u in us if u["group"] == "R"]
        p = [u["purity"] for u in us if u["group"] == "P"]
        y = np.array([float("CDKN2A" in u["dels"]) for u in us])
        X = np.column_stack([[float(u["group"] == "R") for u in us], [u["purity"] / 10 for u in us]])
        adj = None
        if y.sum() >= 3 and len(r) > 2 and len(p) > 2:
            beta, se = logistic(y, X)
            adj = {"b": float(beta[1]), "se": float(se[1]), "purity_or_per_10pts": float(math.exp(beta[2]))}
        pur[sid] = {"n": len(us), "median_R": float(np.median(r)) if r else None, "median_P": float(np.median(p)) if p else None,
                    "mannwhitney_p": float(stats.mannwhitneyu(r, p).pvalue) if len(r) > 2 and len(p) > 2 else None, "adjusted": adj}
    S["checks"]["purity"] = {"per_study": pur, "pooled_adjusted": pool([v["adjusted"] for v in pur.values()])}

    # ---- every gene with a deep-deletion rate above 3% (is CDKN2A special, or are deletions called more often in one group?)
    gene_rows = []
    all_genes = set().union(*[u["dels"] for sid in TEST_STUDIES for u in units[sid]])
    for g in sorted(all_genes):
        res = compare(g)
        k, n = res["R"][3] + res["P"][3], res["R"][4] + res["P"][4]
        if n and k / n > 0.03 and res["pooled"]:
            gene_rows.append({"gene": g, "rate": k / n, "n": n, "or": res["pooled"]["or"], "lo": res["pooled"]["lo"], "hi": res["pooled"]["hi"]})
    gene_rows.sort(key=lambda r: -r["or"])
    burden = {}
    for sid in TEST_STUDIES:
        r = [len(u["dels"]) for u in units[sid] if u["group"] == "R"]
        p = [len(u["dels"]) for u in units[sid] if u["group"] == "P"]
        fr = [u["fga"] for u in units[sid] if u["group"] == "R" and u["fga"] is not None]
        fp = [u["fga"] for u in units[sid] if u["group"] == "P" and u["fga"] is not None]
        burden[sid] = {"mean_deleted_genes_R": float(np.mean(r)), "mean_deleted_genes_P": float(np.mean(p)),
                       "share_with_any_deletion_R": float(np.mean([x > 0 for x in r])), "share_with_any_deletion_P": float(np.mean([x > 0 for x in p])),
                       "mannwhitney_p": float(stats.mannwhitneyu(r, p).pvalue),
                       "median_fga_R": float(np.median(fr)) if fr else None, "median_fga_P": float(np.median(fp)) if fp else None}
    S["checks"]["genes_above_3pct"] = gene_rows
    S["checks"]["deletion_burden"] = burden

    # ---- secondary
    for g in ("CDKN2B", "MTAP"):
        S["secondary"][g] = compare(g)
        emit("secondary", g, S["secondary"][g])
    S["secondary"]["distant_metastasis_only"] = compare("CDKN2A", lambda u: u["group"] == "P" or u["type"] in ("metastasis", "metastatic"))
    emit("secondary: distant metastasis v primary", "CDKN2A", S["secondary"]["distant_metastasis_only"])
    S["secondary"]["local_recurrence_only"] = compare("CDKN2A", lambda u: u["group"] == "P" or u["type"] in ("local recurrence", "recurrent", "recurrence"))
    emit("secondary: local recurrence v primary", "CDKN2A", S["secondary"]["local_recurrence_only"])
    S["secondary"]["lung_metastasis_only"] = compare("CDKN2A", lambda u: u["group"] == "P" or "lung" in u["met_site"].lower())
    emit("secondary: lung metastasis v primary", "CDKN2A", S["secondary"]["lung_metastasis_only"])
    S["secondary"]["every_sample"] = compare("CDKN2A", key="samples")
    emit("secondary: every sample", "CDKN2A", S["secondary"]["every_sample"])
    pr = {"pairs": 0, "both": 0, "neither": 0, "gained": 0, "lost": 0}
    for sid in TEST_STUDIES:
        for a, b in paired[sid]:
            x, y = "CDKN2A" in a["dels"], "CDKN2A" in b["dels"]
            pr["pairs"] += 1
            pr["both" if x and y else "neither" if not x and not y else "gained" if y else "lost"] += 1
    S["secondary"]["paired_patients"] = pr
    co = {"cdkn2a_deleted_with_mtap_covered": 0, "of_which_mtap_deleted": 0, "mtap_deleted_without_cdkn2a": 0}
    for sid in TEST_STUDIES:
        for u in units[sid]:
            if covered(u, "MTAP"):
                if "CDKN2A" in u["dels"]:
                    co["cdkn2a_deleted_with_mtap_covered"] += 1
                    co["of_which_mtap_deleted"] += "MTAP" in u["dels"]
                elif "MTAP" in u["dels"]:
                    co["mtap_deleted_without_cdkn2a"] += 1
    S["secondary"]["co_deletion"] = co

    # ---- descriptive: share at relapse, including the relapse-only trial
    d_m, s_m = load("pancan_mappyacts_2022")
    by = {}
    for s in s_m:
        by.setdefault(s["patient"], s)
    mappy = list(by.values())
    S["studies"]["pancan_mappyacts_2022"] = {"patients_with_copy_number": len(mappy), "cna_profile": d_m["cna_profile"]}
    desc = {}
    for g in GENES:
        parts = {}
        for sid in TEST_STUDIES:
            us = [u for u in units[sid] if u["group"] == "R" and covered(u, g)]
            parts[sid] = (sum(g in u["dels"] for u in us), len(us))
        mp = [u for u in mappy if covered(u, g)]
        parts["pancan_mappyacts_2022"] = (sum(g in u["dels"] for u in mp), len(mp))
        k, n = sum(p[0] for p in parts.values()), sum(p[1] for p in parts.values())
        k2, n2 = sum(parts[s][0] for s in TEST_STUDIES), sum(parts[s][1] for s in TEST_STUDIES)
        desc[g] = {"per_study": {s: {"k": v[0], "n": v[1]} for s, v in parts.items()},
                   "relapse_all_three": dict(zip(("p", "lo", "hi"), wilson(k, n)), k=k, n=n),
                   "relapse_two_test_studies": dict(zip(("p", "lo", "hi"), wilson(k2, n2)), k=k2, n=n2)}
    S["descriptive"] = desc

    # ---- reference cohorts of primary tumours
    for sid in ("os_target_gdc", "pancan_pcawg_2020"):
        d_r, s_r = load(sid)
        by = {}
        for s in s_r:
            by.setdefault(s["patient"], s)
        us = list(by.values())
        S["reference"][sid] = {g: dict(zip(("p", "lo", "hi"), wilson(sum(g in u["dels"] for u in us), len(us))),
                                       k=sum(g in u["dels"] for u in us), n=len(us)) for g in GENES}
        S["reference"][sid]["sample_types"] = dict(collections.Counter(s["type"] for s in us))
        cd = [u for u in us if "CDKN2A" in u["dels"]]
        S["reference"][sid]["co_deletion"] = {"cdkn2a_deleted": len(cd), "of_which_mtap_deleted": sum("MTAP" in u["dels"] for u in cd)}

    json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["analysis", "study", "gene", "relapse_deleted", "relapse_n", "primary_deleted", "primary_n", "odds_ratio", "ci_low", "ci_high"])
        w.writerows(rows_out)
    with open(os.path.join(OUT, "patients.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["study", "patient", "sample_used", "sample_type", "group", "gene_panel", "tumour_purity", "CDKN2A_deep_deletion",
                    "CDKN2B_deep_deletion", "MTAP_deep_deletion", "genes_deep_deleted"])
        w.writerows(patients_out)

    pc = lambda t: (100 * t[0], 100 * t[1], 100 * t[2])
    fig = [("CDKN2A deep deletion", None, None, None, None)]
    for sid in TEST_STUDIES:
        a, b, c, d = prim["tables"][sid]
        fig.append((f"{LABEL[sid]}, primary ({c}/{c + d})", *pc(wilson(c, c + d)), "P"))
        fig.append((f"{LABEL[sid]}, metastasis or relapse ({a}/{a + b})", *pc(wilson(a, a + b)), "R"))
    k, n = desc["CDKN2A"]["per_study"]["pancan_mappyacts_2022"]["k"], desc["CDKN2A"]["per_study"]["pancan_mappyacts_2022"]["n"]
    fig.append((f"{LABEL['pancan_mappyacts_2022']} ({k}/{n})", *pc(wilson(k, n)), "R"))
    for sid in ("os_target_gdc", "pancan_pcawg_2020"):
        r = S["reference"][sid]["CDKN2A"]
        fig.append((f"{LABEL[sid]} ({r['k']}/{r['n']})", 100 * r["p"], 100 * r["lo"], 100 * r["hi"], "ref"))
    fig.append(("MTAP deep deletion (only where the test covers MTAP)", None, None, None, None))
    sec = S["secondary"]["MTAP"]
    fig.append((f"Primary ({sec['P'][3]}/{sec['P'][4]})", *pc(sec["P"]), "P"))
    fig.append((f"Metastasis or relapse ({sec['R'][3]}/{sec['R'][4]})", *pc(sec["R"]), "R"))
    for sid in ("os_target_gdc", "pancan_pcawg_2020"):
        r = S["reference"][sid]["MTAP"]
        fig.append((f"{LABEL[sid]} ({r['k']}/{r['n']})", 100 * r["p"], 100 * r["lo"], 100 * r["hi"], "ref"))
    bars_svg(fig, os.path.join(FIG, "engine03_9p21.svg"), "Deep deletion at 9p21 in osteosarcoma, by where the sample came from",
             ("Share of patients with both copies deleted, 95% CI. One sample per patient.",
              "Blue: metastasis or relapse. Grey: primary tumour. Pale: reference cohorts of primary tumours."))

    # console
    print(json.dumps(S["studies"], indent=1))
    for lab, res in (("PRIMARY CDKN2A", prim), ("CDKN2B", S["secondary"]["CDKN2B"]), ("MTAP", S["secondary"]["MTAP"]),
                     ("distant met only", S["secondary"]["distant_metastasis_only"]), ("local recurrence only", S["secondary"]["local_recurrence_only"]),
                     ("lung met only", S["secondary"]["lung_metastasis_only"]), ("every sample", S["secondary"]["every_sample"])):
        print(f"\n== {lab}")
        for sid, t in res["tables"].items():
            o = res["per_study"][sid]
            print(f"  {LABEL[sid]:24s} R {t[0]}/{t[0] + t[1]}  P {t[2]}/{t[2] + t[3]}  OR {fmt_or(o) if o else 'n/a'}")
        m = res["pooled"]
        print(f"  R {res['R'][3]}/{res['R'][4]} = {100 * res['R'][0]:.1f}% ({100 * res['R'][1]:.1f}-{100 * res['R'][2]:.1f}) | P {res['P'][3]}/{res['P'][4]} = {100 * res['P'][0]:.1f}% ({100 * res['P'][1]:.1f}-{100 * res['P'][2]:.1f})")
        if m:
            print(f"  POOLED OR {fmt_or(m)} p={m['p']:.3g} I2={m['I2']:.2f}; random {fmt_or(m['random'])}")
    print("\nVERDICT:", S["primary"]["verdict"], "| underpowered:", S["primary"]["underpowered"])
    print("purity:", json.dumps(S["checks"]["purity"], default=lambda x: round(x, 3)))
    print("burden:", json.dumps(burden, default=lambda x: round(x, 3)))
    print("genes >3%:", [(r["gene"], f'{100 * r["rate"]:.0f}%', f'{r["or"]:.2f} ({r["lo"]:.2f}-{r["hi"]:.2f})') for r in gene_rows])
    print("paired:", pr, "| co-deletion:", co)
    print("descriptive:", json.dumps(desc, default=lambda x: round(x, 3)))
    print("reference:", json.dumps(S["reference"], default=lambda x: round(x, 3)))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
    else:
        analyse()
