"""Do the project's leads predict patient outcome? A pre-specified survival
analysis of open TARGET-OS data (NCI GDC).

The analysis plan was written before any marker was compared with any
outcome; it is in research_notes/Survival/notes.md (section 2) and this
script implements it as written.

Data (all open access, no credentials):

  * Clinical: GDC `cases` endpoint for project TARGET-OS, expanded with
    diagnoses, demographic, follow_ups and pathology details; plus the open
    clinical supplement workbooks (Discovery and Validation XLSX files).
  * Copy number: per-patient calls already made by tools/copy_number_map.py
    (data/copy_number_raw/patient_calls.csv) and the ASCAT2 allele-specific
    segments in data/copy_number_raw/ascat_segments/ (for genome-instability
    measures). Run `python3 tools/copy_number_map.py all` first if missing.
  * RNA: STAR gene counts cached by tools/surface_targets.py in
    data/surface_targets_raw/gdc_tsv/ (run `python3 tools/surface_targets.py
    gdc` first if missing), matched to cases via gdc_samples.json.

Outcomes: overall survival (OS, primary), event-free survival (EFS) and
metastasis at diagnosis. Methods: Kaplan-Meier with log-rank for binary
markers (amplification yes/no; RNA above vs at-or-below the median), Cox
proportional hazards (Efron ties) for the continuous marker adjusted for
metastasis at diagnosis, Fisher exact or Mann-Whitney for metastasis.
Benjamini-Hochberg within each pre-specified family and across all tests.

KM, log-rank and Cox are implemented here with numpy/scipy because the
`lifelines` package requires pandas < 3 and this repository pins pandas
3.0.5; the numbers were cross-checked against lifelines 0.30.3 in a
separate virtual environment (see the notes).

Outputs:

  data/osteosarcoma_survival_results.csv     one row per test
  data/survival_raw/patients.csv             per-patient analysis table
                                             (git-ignored, like other raw data)
  data/survival_raw/summary.json             numbers used by the report
  docs/figures/survival_*.svg                Kaplan-Meier plots

Run from the repo root, stage by stage or all at once:

    python3 tools/survival_analysis.py fetch     # GDC clinical downloads
    python3 tools/survival_analysis.py build     # per-patient table
    python3 tools/survival_analysis.py analyse   # all tests + CSV
    python3 tools/survival_analysis.py plot      # KM figures (SVG)
    python3 tools/survival_analysis.py all

Needs numpy, scipy and matplotlib (versions in requirements.txt).
"""
import csv
import glob
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "survival_raw")
CN_RAW = os.path.join(ROOT, "data", "copy_number_raw")
RNA_RAW = os.path.join(ROOT, "data", "surface_targets_raw")
OUT_CSV = os.path.join(ROOT, "data", "osteosarcoma_survival_results.csv")
SUMMARY = os.path.join(RAW, "summary.json")
FIG_DIR = os.path.join(ROOT, "docs", "figures")
SURFACE_CSV = os.path.join(ROOT, "data", "osteosarcoma_surface_target_candidates.csv")
REPURPOSING_CSV = os.path.join(ROOT, "data", "osteosarcoma_repurposing_candidates.csv")

GDC_CASES = "https://api.gdc.cancer.gov/cases"
GDC_FILES = "https://api.gdc.cancer.gov/files"
GDC_DATA = "https://api.gdc.cancer.gov/data"
UA = {"User-Agent": "open-science-survival-analysis/1.0"}
PROJECT = "TARGET-OS"
DAYS_PER_YEAR = 365.25

# EFS: these first events count as events; "None" and "Censored" are censored.
EFS_EVENTS = {"Relapse", "Progression", "Death", "Second Malignant Neoplasm"}
EFS_CENSORED = {"None", "Censored"}

# ---- pre-specified markers (research_notes/Survival/notes.md, section 2.2)
# Copy-number markers: (name, binary column in patient_calls.csv,
#   continuous definition, label). Continuous = CN relative to ploidy.
CN_MARKERS = [
    ("MYC_amp", "MYC_amp", ("rel", ["MYC_cn"]), "MYC amplification"),
    ("VEGFR_axis_amp", "vegfr_any_amp", ("rel", ["VEGFA_cn", "KDR_cn", "PDGFRA_cn", "KIT_cn"]),
     "Any VEGFA/KDR/PDGFRA/KIT amplification"),
    ("CCNE1_amp", "CCNE1_amp", ("rel", ["CCNE1_cn"]), "CCNE1 amplification"),
    ("PTK2_amp", "PTK2_amp", ("rel", ["PTK2_cn"]), "PTK2 (FAK) amplification"),
    ("CDKN2A_deepdel", "CDKN2A_deepdel", ("rel", ["CDKN2A_min"]), "CDKN2A deep deletion"),
]
GI_MARKERS = [
    ("FGA", "Fraction of genome altered"),
    ("LOH_fraction", "Fraction of genome with LOH"),
]
RNA_GENES = ["PTK2", "DKK1", "LRRC15", "PTK7", "IL6", "IL1A", "IL1B", "CXCL8",
             "IL6R", "CXCR4", "AKT1", "AKT2", "AKT3"]
# Markers whose plots go in docs/figures (the leads' headline markers).
PLOT_MARKERS = ["MYC_amp", "VEGFR_axis_amp", "PTK2_amp", "LOH_fraction",
                "RNA_DKK1", "RNA_IL6", "RNA_CXCR4", "RNA_LRRC15"]


# ----------------------------------------------------------------- helpers
def http(url, retries=6, timeout=300):
    """GET with backoff; GDC sometimes drops connections."""
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - network flakiness is expected
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"request failed after {retries} tries: {url} :: {last}")


def load_summary():
    return json.load(open(SUMMARY)) if os.path.exists(SUMMARY) else {}


def save_summary(key, value):
    s = load_summary()
    s[key] = value
    json.dump(s, open(SUMMARY, "w"), indent=1, default=float)


# --------------------------------------------------------------- stage: fetch
def stage_fetch():
    """Download GDC case records and the open clinical supplement workbooks."""
    os.makedirs(RAW, exist_ok=True)
    flt = json.dumps({"op": "=", "content": {"field": "project.project_id", "value": PROJECT}})
    q = urllib.parse.urlencode({
        "filters": flt, "size": "5000", "format": "json",
        "expand": "diagnoses,demographic,follow_ups,diagnoses.pathology_details"})
    data = json.loads(http(f"{GDC_CASES}?{q}"))
    hits = data["data"]["hits"]
    json.dump({"retrieved": time.strftime("%Y-%m-%d"), "hits": hits},
              open(os.path.join(RAW, "gdc_cases.json"), "w"))
    print(f"[fetch] {len(hits)} case records")
    flt = json.dumps({"op": "and", "content": [
        {"op": "=", "content": {"field": "cases.project.project_id", "value": PROJECT}},
        {"op": "=", "content": {"field": "data_category", "value": "Clinical"}},
        {"op": "=", "content": {"field": "access", "value": "open"}}]})
    q = urllib.parse.urlencode({"filters": flt, "size": "100",
                                "fields": "file_id,file_name,data_format,updated_datetime"})
    files = json.loads(http(f"{GDC_FILES}?{q}"))["data"]["hits"]
    keep = []
    for f in files:
        if not re.match(r"TARGET_OS_ClinicalData_(Discovery|Validation)_\d+\.xlsx$", f["file_name"]):
            continue
        open(os.path.join(RAW, f["file_name"]), "wb").write(http(f"{GDC_DATA}/{f['file_id']}"))
        keep.append(f)
        print(f"[fetch] {f['file_name']}")
    json.dump(keep, open(os.path.join(RAW, "clinical_files.json"), "w"), indent=1)


# ------------------------------------------------- minimal XLSX (stdlib only)
_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def _col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_xlsx_sheet(path, sheet_name):
    """Rows (lists) of one worksheet, values as str/float. Avoids openpyxl."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", _NS):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{_NS['m']}}}t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = None
    for s in wb.find("m:sheets", _NS):
        if s.get("name") == sheet_name:
            rid = s.get(f"{{{_NS['r']}}}id")
            for rel in rels:
                if rel.get("Id") == rid:
                    target = rel.get("Target").lstrip("/")
    if target is None:
        raise KeyError(sheet_name)
    if not target.startswith("xl/"):
        target = "xl/" + target
    rows = []
    for row in ET.fromstring(z.read(target)).iter(f"{{{_NS['m']}}}row"):
        vals = {}
        for c in row.findall("m:c", _NS):
            t, v = c.get("t"), c.find("m:v", _NS)
            if t == "s" and v is not None:
                val = shared[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(f"{{{_NS['m']}}}t"))
            elif v is not None:
                try:
                    val = float(v.text)
                except ValueError:
                    val = v.text
            else:
                val = None
            vals[_col_index(c.get("r"))] = val
        if vals:
            rows.append([vals.get(i) for i in range(max(vals) + 1)])
    return rows


def supplement():
    """{USI: row dict} from the Discovery and Validation workbooks
    (Discovery wins if a patient is in both)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(RAW, "TARGET_OS_ClinicalData_*.xlsx")),
                       key=lambda p: "Discovery" not in p, reverse=True):
        rows = read_xlsx_sheet(path, "Clinical Data")
        hdr = [str(h).strip() if h is not None else "" for h in rows[0]]
        for r in rows[1:]:
            d = dict(zip(hdr, r + [None] * (len(hdr) - len(r))))
            if d.get("TARGET USI"):
                d["_file"] = os.path.basename(path)
                out[str(d["TARGET USI"]).strip()] = d
    return out


def _clean(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        if v in ("", "Not Reported", "not reported", "Unknown", "NA"):
            return None
    return v


def _num(v):
    v = _clean(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------- stage: build
def clinical_table(cases, supp):
    """One clinical record per molecular patient, following notes section 2.1."""
    out = {}
    for h in cases:
        usi = h["submitter_id"]
        dm = h.get("demographic") or {}
        dg = (h.get("diagnoses") or [{}])[0]
        s = supp.get(usi, {})
        rec = {"case": usi, "case_uuid": h["case_id"]}
        # Overall survival (API primary)
        vs = _clean(dm.get("vital_status"))
        rec["os_event"] = {"Dead": 1, "Alive": 0}.get(vs)
        if vs == "Dead":
            rec["os_days"] = _num(dm.get("days_to_death"))
        elif vs == "Alive":
            rec["os_days"] = _num(dg.get("days_to_last_follow_up"))
        else:
            rec["os_days"] = None
        if rec["os_event"] is None:
            rec["os_days"] = None
        # OS from supplement (sensitivity)
        svs = _clean(s.get("Vital Status"))
        rec["os_event_supp"] = {"Dead": 1, "Alive": 0}.get(svs)
        rec["os_days_supp"] = _num(s.get("Overall Survival Time in Days"))
        if rec["os_event_supp"] is None:
            rec["os_days_supp"] = None
        # EFS: API, falling back to supplement
        fe = [f for f in h.get("follow_ups") or [] if f.get("days_to_first_event") is not None]
        ev, days, src = None, None, None
        if fe:
            ev, days, src = _clean(fe[0].get("first_event")), _num(fe[0]["days_to_first_event"]), "api"
        if ev is None or days is None:
            ev, days, src = _clean(s.get("First Event")), _num(s.get("Event Free Survival Time in Days")), "supplement"
        if ev in EFS_EVENTS:
            rec["efs_event"] = 1
        elif ev in EFS_CENSORED:
            rec["efs_event"] = 0
        else:
            rec["efs_event"] = None
        rec["efs_days"] = days if rec["efs_event"] is not None else None
        rec["first_event"] = ev
        rec["efs_source"] = src if rec["efs_event"] is not None else None
        # Metastasis at diagnosis
        m = _clean(dg.get("metastasis_at_diagnosis"))
        met = {"Metastasis, NOS": 1, "No Metastasis": 0}.get(m)
        if met is None:
            d = _clean(s.get("Disease at diagnosis"))
            if d:
                met = 0 if d.lower().startswith("non-metastatic") else (1 if d.lower().startswith("metastatic") else None)
        rec["metastatic"] = met
        a = _num(dg.get("age_at_diagnosis"))
        rec["age_years"] = a / DAYS_PER_YEAR if a is not None else None
        rec["sex"] = _clean(dm.get("sex_at_birth"))
        rec["year_of_diagnosis"] = _num(dg.get("year_of_diagnosis"))
        hr = _clean(s.get("Histologic response"))
        rec["good_response"] = None if not hr else (1 if hr.startswith("Stage 3/4") else (0 if hr.startswith("Stage 1/2") else None))
        rec["protocol"] = _clean(s.get("Protocol"))
        out[usi] = rec
    return out


def genome_instability():
    """{case: (FGA, LOH fraction, ploidy)} from ASCAT2 allele-specific segments.
    Autosomes only, length-weighted over the segmented genome.
    FGA = share where total CN != round(ploidy); LOH = minor CN 0, total >= 1."""
    man = json.load(open(os.path.join(CN_RAW, "manifest.json")))["files"]
    out = {}
    for r in man:
        if r["data_type"] != "Allele-specific Copy Number Segment":
            continue
        path = os.path.join(CN_RAW, "ascat_segments", r["file_id"] + ".txt")
        segs = []
        for rec in csv.DictReader(open(path), delimiter="\t"):
            if rec["Chromosome"] in ("chrX", "chrY"):
                continue
            ln = int(rec["End"]) - int(rec["Start"]) + 1
            segs.append((ln, float(rec["Copy_Number"]), float(rec["Minor_Copy_Number"])))
        tot = sum(s[0] for s in segs)
        ploidy = sum(s[0] * s[1] for s in segs) / tot
        base = round(ploidy)
        fga = sum(s[0] for s in segs if s[1] != base) / tot
        loh = sum(s[0] for s in segs if s[2] == 0 and s[1] >= 1) / tot
        out[r["case"]] = (fga, loh, ploidy)
    return out


def rna_values(genes):
    """{case: {gene: log2(TPM+1)}} from the cached STAR files (protein-coding)."""
    samples = json.load(open(os.path.join(RNA_RAW, "gdc_samples.json")))["samples"]
    want = set(genes)
    out = {}
    for s in samples:
        path = os.path.join(RNA_RAW, "gdc_tsv", s["file_id"] + ".tsv")
        vals, hdr = {}, None
        for line in open(path):
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if hdr is None:
                hdr = p
                ix_n, ix_t, ix_tpm = hdr.index("gene_name"), hdr.index("gene_type"), hdr.index("tpm_unstranded")
                continue
            if p[0].startswith("N_") or p[ix_n] not in want or p[ix_t] != "protein_coding":
                continue
            if p[ix_n] not in vals:            # first occurrence (PAR duplicates)
                vals[p[ix_n]] = math.log2(float(p[ix_tpm]) + 1)
        if s["case"] in out:
            raise ValueError(f"two RNA samples for {s['case']}")
        out[s["case"]] = vals
    return out


def exploratory_genes():
    surf = [r for r in csv.DictReader(open(SURFACE_CSV)) if r["rank_shortlist"]]
    surf = [r["symbol"] for r in sorted(surf, key=lambda r: int(r["rank_shortlist"]))[:25]]
    rep = [r for r in csv.DictReader(open(REPURPOSING_CSV)) if r["shortlist_rank"]]
    rep = [r["gene"] for r in sorted(rep, key=lambda r: int(r["shortlist_rank"]))]
    seen, out = set(RNA_GENES), []
    for g, src in [(g, "surface top 25") for g in surf] + [(g, "repurposing shortlist") for g in rep]:
        if g in seen:
            continue
        seen.add(g)
        out.append((g, src))
    return out


def stage_build():
    cases = json.load(open(os.path.join(RAW, "gdc_cases.json")))["hits"]
    supp = supplement()
    calls = {r["case"]: r for r in csv.DictReader(open(os.path.join(CN_RAW, "patient_calls.csv")))}
    gi = genome_instability()
    expl = exploratory_genes()
    rna = rna_values(RNA_GENES + [g for g, _ in expl])
    mol = set(calls) | set(rna)
    clin = clinical_table([h for h in cases if h["submitter_id"] in mol], supp)
    missing = mol - set(clin)
    if missing:
        raise SystemExit(f"molecular cases without GDC clinical record: {sorted(missing)}")
    rows = []
    for usi in sorted(mol):
        rec = dict(clin[usi])
        rec["has_cn"], rec["has_rna"] = int(usi in calls), int(usi in rna)
        c = calls.get(usi)
        for name, col, (kind, cols), _ in CN_MARKERS:
            if c is None:
                rec[name], rec[name + "_cont"] = None, None
                continue
            pl = float(c["ploidy"])
            rec[name] = int(c[col])
            rec[name + "_cont"] = max(float(c[k]) for k in cols) / pl
        if usi in gi:
            rec["FGA"], rec["LOH_fraction"], rec["ascat_ploidy"] = gi[usi]
        else:
            rec["FGA"] = rec["LOH_fraction"] = rec["ascat_ploidy"] = None
        for g in RNA_GENES + [g for g, _ in expl]:
            rec["RNA_" + g] = rna.get(usi, {}).get(g)
        rows.append(rec)
    keys = list(rows[0].keys())
    with open(os.path.join(RAW, "patients.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    n = len(rows)
    cov = {k: sum(1 for r in rows if r[k] is not None) for k in
           ["os_event", "os_days", "efs_event", "metastatic", "age_years", "sex",
            "good_response", "protocol", "os_event_supp"]}
    cov.update({"n_patients": n, "n_cn": sum(r["has_cn"] for r in rows),
                "n_rna": sum(r["has_rna"] for r in rows),
                "n_both": sum(r["has_cn"] and r["has_rna"] for r in rows),
                "deaths": sum(1 for r in rows if r["os_event"] == 1),
                "efs_events": sum(1 for r in rows if r["efs_event"] == 1),
                "metastatic": sum(1 for r in rows if r["metastatic"] == 1),
                "efs_from_supplement": sum(1 for r in rows if r["efs_source"] == "supplement"),
                "os_supp_differs": [r["case"] for r in rows if r["os_days"] is not None and r["os_days_supp"] is not None
                                    and abs(r["os_days"] - r["os_days_supp"]) > 0.5],
                "exploratory_genes": expl})
    save_summary("cohort", cov)
    print(f"[build] {n} patients ({cov['n_cn']} CN, {cov['n_rna']} RNA); "
          f"{cov['deaths']} deaths, {cov['efs_events']} EFS events, {cov['metastatic']} metastatic")


# ----------------------------------------------------------------- statistics
def kaplan_meier(t, e):
    """Return (times, survival, n_at_risk_before, greenwood_var) at event times."""
    t, e = np.asarray(t, float), np.asarray(e, int)
    times = np.unique(t[e == 1])
    s, var_sum, out = 1.0, 0.0, []
    for u in times:
        n = np.sum(t >= u)
        d = np.sum((t == u) & (e == 1))
        s *= 1 - d / n
        if n > d:
            var_sum += d / (n * (n - d))
        out.append((u, s, n, s * s * var_sum))
    return out


def km_at(t, e, when):
    """KM survival estimate at time `when` (days), or None if beyond follow-up."""
    if np.max(np.asarray(t, float)) < when:
        return None
    s = 1.0
    for u, su, _, _ in kaplan_meier(t, e):
        if u <= when:
            s = su
    return s


def km_median(t, e):
    for u, s, _, _ in kaplan_meier(t, e):
        if s <= 0.5:
            return u
    return None


def logrank(t, e, g):
    """Two-group log-rank test; returns (chi2, p, observed_g1, expected_g1)."""
    t, e, g = np.asarray(t, float), np.asarray(e, int), np.asarray(g, int)
    O = E = V = 0.0
    for u in np.unique(t[e == 1]):
        at = t >= u
        n, n1 = at.sum(), (at & (g == 1)).sum()
        d = ((t == u) & (e == 1)).sum()
        d1 = ((t == u) & (e == 1) & (g == 1)).sum()
        O += d1
        E += d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    chi2 = (O - E) ** 2 / V if V > 0 else float("nan")
    return chi2, float(stats.chi2.sf(chi2, 1)), O, E


def _efron_terms(X, t, e, beta):
    """Log partial likelihood, gradient and Hessian (Efron tie handling)."""
    n, p = X.shape
    xb = X @ beta
    r = np.exp(xb - xb.max())          # scaled for stability; cancels out
    ll, grad, hess = 0.0, np.zeros(p), np.zeros((p, p))
    for u in np.unique(t[e == 1]):
        R = t >= u
        D = (t == u) & (e == 1)
        d = D.sum()
        s0R, s1R = r[R].sum(), (r[R, None] * X[R]).sum(0)
        s2R = (r[R, None, None] * X[R, :, None] * X[R, None, :]).sum(0)
        s0D, s1D = r[D].sum(), (r[D, None] * X[D]).sum(0)
        s2D = (r[D, None, None] * X[D, :, None] * X[D, None, :]).sum(0)
        ll += xb[D].sum() - d * (xb.max())  # adjust for scaling below
        grad += X[D].sum(0)
        for l in range(d):
            f = l / d
            s0 = s0R - f * s0D
            s1 = s1R - f * s1D
            s2 = s2R - f * s2D
            ll -= math.log(s0)
            grad -= s1 / s0
            hess -= s2 / s0 - np.outer(s1, s1) / s0 ** 2
    return ll, grad, hess


def cox(X, t, e, max_iter=50, tol=1e-9):
    """Cox PH by Newton-Raphson with step halving. Returns dict with beta, se,
    hr, ci, p (Wald), loglik and converged flag. X: n x p array."""
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    t, e = np.asarray(t, float), np.asarray(e, int)
    beta = np.zeros(X.shape[1])
    ll, g, H = _efron_terms(X, t, e, beta)
    ll0 = ll
    converged = False
    for _ in range(max_iter):
        try:
            step = np.linalg.solve(-H, g)
        except np.linalg.LinAlgError:
            break
        k = 1.0
        while True:
            nb = beta + k * step
            nll, ng, nH = _efron_terms(X, t, e, nb)
            if nll >= ll - 1e-12 or k < 1e-4:
                break
            k /= 2
        done = abs(nll - ll) < tol
        beta, ll, g, H = nb, nll, ng, nH
        if done:
            converged = True
            break
    cov = np.linalg.inv(-H)
    se = np.sqrt(np.diag(cov))
    z = beta / se
    return {"beta": beta, "se": se, "hr": np.exp(beta),
            "lo": np.exp(beta - 1.959964 * se), "hi": np.exp(beta + 1.959964 * se),
            "p": 2 * stats.norm.sf(np.abs(z)), "loglik": ll, "loglik0": ll0,
            "converged": converged and bool(np.all(np.abs(beta) < 15))}


def schoenfeld_p(X, t, e, beta, j=0):
    """Approximate PH check for covariate j: Pearson correlation of its
    Schoenfeld residuals with event-time rank (Breslow risk-set means)."""
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    r = np.exp(X @ beta)
    res, tim = [], []
    for i in np.where(e == 1)[0]:
        R = t >= t[i]
        res.append(X[i, j] - (r[R] * X[R, j]).sum() / r[R].sum())
        tim.append(t[i])
    if len(res) < 4 or np.std(res) == 0:
        return float("nan")
    return float(stats.pearsonr(stats.rankdata(tim), res)[1])


def bh(pvals):
    """Benjamini-Hochberg adjusted p-values (NaN kept as NaN)."""
    p = np.asarray(pvals, float)
    out = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    m = ok.sum()
    if m == 0:
        return out
    idx = np.where(ok)[0][np.argsort(p[ok])]
    q = p[idx] * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out[idx] = np.minimum(q, 1)
    return out


def schoenfeld_min_hr(events, frac, power=0.8, alpha=0.05):
    """Smallest HR (>1) detectable with this many events and group share."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return math.exp(z / math.sqrt(events * frac * (1 - frac)))


# ------------------------------------------------------------- stage: analyse
def load_patients():
    rows = list(csv.DictReader(open(os.path.join(RAW, "patients.csv"))))
    for r in rows:
        for k, v in r.items():
            if v == "":
                r[k] = None
            elif k not in ("case", "case_uuid", "sex", "first_event", "efs_source", "protocol"):
                try:
                    r[k] = float(v)
                except ValueError:
                    pass
    return rows


def marker_specs(rows):
    """List of dicts: name, label, type, cont key, scale, cont unit, binary fn."""
    specs = []
    for name, _, _, label in CN_MARKERS:
        specs.append({"name": name, "label": label, "type": "copy number",
                      "cont": name + "_cont", "scale": 1.0,
                      "unit": "per +1x tumour ploidy" if name != "CDKN2A_deepdel" else "per +1x ploidy (minimum CN; higher = less loss)",
                      "bin": (lambda r, n=name: r[n]), "bin_def": "deep deletion" if name == "CDKN2A_deepdel" else "CN >= 2x ploidy"})
    for name, label in GI_MARKERS:
        specs.append({"name": name, "label": label, "type": "genome instability",
                      "cont": name, "scale": 10.0, "unit": "per +10 percentage points"})
    for g in RNA_GENES:
        specs.append({"name": "RNA_" + g, "label": f"{g} RNA", "type": "RNA",
                      "cont": "RNA_" + g, "scale": 1.0, "unit": "per doubling of TPM (log2)"})
    for s in specs:
        if "bin" not in s:
            vals = [r[s["cont"]] for r in rows if r[s["cont"]] is not None]
            med = float(np.median(vals))
            s["median"] = med
            s["bin"] = (lambda r, k=s["cont"], m=med: None if r[k] is None else int(r[k] > m))
            s["bin_def"] = f"above cohort median ({med:.3g}{'' if s['type'] == 'RNA' else ''})"
    return specs


def _arr(rows, keys):
    return np.array([[r[k] for k in keys] for r in rows], float)


def surv_tests(rows, spec, tkey, ekey, outcome, fam_cox, fam_lr, extra_sens=True):
    """Tests A/B (OS) or C/D (EFS) for one marker. Returns two result rows."""
    out = []
    cont = spec["cont"]
    # Cox, continuous marker + metastasis
    sub = [r for r in rows if r[cont] is not None and r[tkey] is not None and r[ekey] is not None and r["metastatic"] is not None]
    X = np.column_stack([np.array([r[cont] for r in sub]) * spec["scale"], [r["metastatic"] for r in sub]])
    t, e = _arr(sub, [tkey])[:, 0], _arr(sub, [ekey])[:, 0].astype(int)
    fit = cox(X, t, e)
    row = {"family": fam_cox, "marker": spec["name"], "marker_label": spec["label"],
           "marker_type": spec["type"], "outcome": outcome,
           "method": "Cox, continuous marker", "adjusted_for": "metastasis at diagnosis",
           "marker_definition": spec["unit"], "n": len(sub), "events": int(e.sum()),
           "effect_measure": "HR", "effect": fit["hr"][0], "ci_low": fit["lo"][0],
           "ci_high": fit["hi"][0], "p": fit["p"][0],
           "ph_check_p": schoenfeld_p(X, t, e, fit["beta"]),
           "converged": fit["converged"]}
    if extra_sens:
        sub2 = [r for r in sub if r["age_years"] is not None]
        X2 = np.column_stack([np.array([r[cont] for r in sub2]) * spec["scale"],
                              [r["metastatic"] for r in sub2], [r["age_years"] for r in sub2]])
        f2 = cox(X2, _arr(sub2, [tkey])[:, 0], _arr(sub2, [ekey])[:, 0].astype(int))
        row.update({"effect_age_adj": f2["hr"][0], "ci_low_age_adj": f2["lo"][0],
                    "ci_high_age_adj": f2["hi"][0], "p_age_adj": f2["p"][0]})
        if tkey == "os_days":
            sub3 = [r for r in rows if r[cont] is not None and r["os_days_supp"] is not None and r["metastatic"] is not None]
            X3 = np.column_stack([np.array([r[cont] for r in sub3]) * spec["scale"], [r["metastatic"] for r in sub3]])
            f3 = cox(X3, _arr(sub3, ["os_days_supp"])[:, 0], _arr(sub3, ["os_event_supp"])[:, 0].astype(int))
            row.update({"effect_supp_os": f3["hr"][0], "ci_low_supp_os": f3["lo"][0],
                        "ci_high_supp_os": f3["hi"][0], "p_supp_os": f3["p"][0]})
    out.append(row)
    # Log-rank, binary marker (with unadjusted Cox HR as effect size)
    sub = [r for r in rows if spec["bin"](r) is not None and r[tkey] is not None and r[ekey] is not None]
    g = np.array([spec["bin"](r) for r in sub], int)
    t, e = _arr(sub, [tkey])[:, 0], _arr(sub, [ekey])[:, 0].astype(int)
    chi2, p, O, E = logrank(t, e, g)
    fit = cox(g.astype(float), t, e)
    five = 5 * DAYS_PER_YEAR
    km_pos, km_neg = km_at(t[g == 1], e[g == 1], five), km_at(t[g == 0], e[g == 0], five)
    out.append({"family": fam_lr, "marker": spec["name"], "marker_label": spec["label"],
                "marker_type": spec["type"], "outcome": outcome,
                "method": "Kaplan-Meier, log-rank, binary marker", "adjusted_for": "none",
                "marker_definition": spec["bin_def"], "n": len(sub), "events": int(e.sum()),
                "n_marker_pos": int(g.sum()), "events_marker_pos": int(e[g == 1].sum()),
                "effect_measure": "HR (binary, unadjusted Cox)", "effect": fit["hr"][0],
                "ci_low": fit["lo"][0], "ci_high": fit["hi"][0], "p": p,
                "km5_marker_pos": km_pos, "km5_marker_neg": km_neg,
                "converged": fit["converged"]})
    return out


def met_test(rows, spec, family):
    sub = [r for r in rows if r["metastatic"] is not None and r[spec["cont"]] is not None]
    m = np.array([r["metastatic"] for r in sub], int)
    row = {"family": family, "marker": spec["name"], "marker_label": spec["label"],
           "marker_type": spec["type"], "outcome": "metastasis at diagnosis", "adjusted_for": "none",
           "n": len(sub), "events": int(m.sum())}
    if spec["type"] == "copy number":
        g = np.array([spec["bin"](r) for r in sub], int)
        a, b = int(((g == 1) & (m == 1)).sum()), int(((g == 1) & (m == 0)).sum())
        c, d = int(((g == 0) & (m == 1)).sum()), int(((g == 0) & (m == 0)).sum())
        res = stats.fisher_exact([[a, b], [c, d]])
        orr = stats.contingency.odds_ratio([[a, b], [c, d]])  # conditional MLE
        ci = orr.confidence_interval(0.95)
        row.update({"method": "Fisher exact", "marker_definition": spec["bin_def"],
                    "n_marker_pos": a + b, "events_marker_pos": a,
                    "effect_measure": "odds ratio (conditional MLE)", "effect": orr.statistic,
                    "ci_low": ci.low, "ci_high": ci.high, "p": res.pvalue})
    else:
        x = np.array([r[spec["cont"]] for r in sub]) * spec["scale"]
        u = stats.mannwhitneyu(x[m == 1], x[m == 0], alternative="two-sided")
        rbc = 2 * u.statistic / ((m == 1).sum() * (m == 0).sum()) - 1
        row.update({"method": "Mann-Whitney U", "marker_definition": spec["unit"].replace("per ", "") if spec["type"] != "RNA" else "log2(TPM+1)",
                    "effect_measure": "rank-biserial r (metastatic vs not)", "effect": rbc,
                    "median_metastatic": float(np.median(x[m == 1])) / spec["scale"],
                    "median_nonmetastatic": float(np.median(x[m == 0])) / spec["scale"],
                    "p": u.pvalue})
    return row


def control_tests(rows):
    """Positive control (metastasis) and exploratory histologic response."""
    out = []
    for tkey, ekey, outcome in [("os_days", "os_event", "OS"), ("efs_days", "efs_event", "EFS")]:
        for gkey, fam, label in [("metastatic", "positive control", "Metastasis at diagnosis"),
                                 ("good_response", "exploratory: histologic response", "Good histologic response (Huvos 3/4, >90% necrosis)")]:
            sub = [r for r in rows if r[gkey] is not None and r[tkey] is not None and r[ekey] is not None]
            g = np.array([r[gkey] for r in sub], int)
            t, e = _arr(sub, [tkey])[:, 0], _arr(sub, [ekey])[:, 0].astype(int)
            chi2, p, _, _ = logrank(t, e, g)
            fit = cox(g.astype(float), t, e)
            five = 5 * DAYS_PER_YEAR
            out.append({"family": fam, "marker": gkey, "marker_label": label, "marker_type": "clinical",
                        "outcome": outcome, "method": "Kaplan-Meier, log-rank, binary marker",
                        "adjusted_for": "none", "marker_definition": "yes vs no",
                        "n": len(sub), "events": int(e.sum()), "n_marker_pos": int(g.sum()),
                        "events_marker_pos": int(e[g == 1].sum()),
                        "effect_measure": "HR (binary, unadjusted Cox)", "effect": fit["hr"][0],
                        "ci_low": fit["lo"][0], "ci_high": fit["hi"][0], "p": p,
                        "km5_marker_pos": km_at(t[g == 1], e[g == 1], five),
                        "km5_marker_neg": km_at(t[g == 0], e[g == 0], five),
                        "converged": fit["converged"]})
    # Age (per 10 years) adjusted for metastasis, for context
    sub = [r for r in rows if r["age_years"] is not None and r["os_days"] is not None and r["metastatic"] is not None]
    X = np.column_stack([[r["age_years"] / 10 for r in sub], [r["metastatic"] for r in sub]])
    fit = cox(X, _arr(sub, ["os_days"])[:, 0], _arr(sub, ["os_event"])[:, 0].astype(int))
    out.append({"family": "context", "marker": "age_years", "marker_label": "Age at diagnosis",
                "marker_type": "clinical", "outcome": "OS", "method": "Cox, continuous marker",
                "adjusted_for": "metastasis at diagnosis", "marker_definition": "per +10 years",
                "n": len(sub), "events": int(sum(r["os_event"] for r in sub)), "effect_measure": "HR",
                "effect": fit["hr"][0], "ci_low": fit["lo"][0], "ci_high": fit["hi"][0], "p": fit["p"][0],
                "converged": fit["converged"]})
    return out


FIELDS = ["family", "test_id", "marker", "marker_label", "marker_type", "outcome", "method",
          "adjusted_for", "marker_definition", "n", "events", "n_marker_pos", "events_marker_pos",
          "effect_measure", "effect", "ci_low", "ci_high", "p", "q_family", "q_all_prespecified",
          "km5_marker_pos", "km5_marker_neg", "median_metastatic", "median_nonmetastatic",
          "ph_check_p", "effect_age_adj", "ci_low_age_adj", "ci_high_age_adj", "p_age_adj",
          "effect_supp_os", "ci_low_supp_os", "ci_high_supp_os", "p_supp_os",
          "min_detectable_hr_80pct", "converged", "source_list"]


def stage_analyse():
    rows = load_patients()
    specs = marker_specs(rows)
    results = control_tests(rows)
    pre = []
    for s in specs:
        a, b = surv_tests(rows, s, "os_days", "os_event", "OS", "A: OS Cox (primary)", "B: OS log-rank")
        c, d = surv_tests(rows, s, "efs_days", "efs_event", "EFS", "C: EFS Cox", "D: EFS log-rank")
        pre += [a, b, c, d, met_test(rows, s, "E: metastasis at diagnosis")]
    for r in pre:
        if r["family"].startswith(("B", "D")):
            frac = r["n_marker_pos"] / r["n"]
            r["min_detectable_hr_80pct"] = schoenfeld_min_hr(r["events"], frac) if 0 < frac < 1 else None
    for fam in sorted({r["family"] for r in pre}):
        grp = [r for r in pre if r["family"] == fam]
        for r, q in zip(grp, bh([r["p"] for r in grp])):
            r["q_family"] = q
    for r, q in zip(pre, bh([r["p"] for r in pre])):
        r["q_all_prespecified"] = q
    # Exploratory screen
    expl = []
    cohort = load_summary().get("cohort", {})
    for g, src in cohort.get("exploratory_genes", []):
        s = {"name": "RNA_" + g, "label": f"{g} RNA", "type": "RNA (exploratory)",
             "cont": "RNA_" + g, "unit": "per doubling of TPM (log2)"}
        if all(r["RNA_" + g] is None for r in rows):
            continue
        sub = [r for r in rows if r[s["cont"]] is not None and r["os_days"] is not None and r["metastatic"] is not None]
        X = np.column_stack([[r[s["cont"]] for r in sub], [r["metastatic"] for r in sub]])
        t, e = _arr(sub, ["os_days"])[:, 0], _arr(sub, ["os_event"])[:, 0].astype(int)
        fit = cox(X, t, e)
        expl.append({"family": "F: exploratory screen, OS Cox", "marker": s["name"], "marker_label": s["label"],
                     "marker_type": s["type"], "outcome": "OS", "method": "Cox, continuous marker",
                     "adjusted_for": "metastasis at diagnosis", "marker_definition": s["unit"],
                     "n": len(sub), "events": int(e.sum()), "effect_measure": "HR", "effect": fit["hr"][0],
                     "ci_low": fit["lo"][0], "ci_high": fit["hi"][0], "p": fit["p"][0],
                     "ph_check_p": schoenfeld_p(X, t, e, fit["beta"]), "converged": fit["converged"],
                     "source_list": src})
    for r, q in zip(expl, bh([r["p"] for r in expl])):
        r["q_family"] = q
    allrows = results + pre + expl
    for i, r in enumerate(allrows, 1):
        r["test_id"] = i
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in allrows:
            w.writerow({k: (f"{v:.4g}" if isinstance(v, (float, np.floating)) else v)
                        for k, v in ((k, r.get(k)) for k in FIELDS)})
    save_summary("medians", {s["name"]: s.get("median") for s in specs})
    print(f"[analyse] {len(allrows)} rows -> {os.path.relpath(OUT_CSV, ROOT)}")
    for r in results:
        print(f"  control {r['marker']:14s} {r['outcome']}: HR {r['effect']:.2f} "
              f"({r['ci_low']:.2f}-{r['ci_high']:.2f}) p={r['p']:.2g} n={r['n']} ev={r['events']}")
    for r in pre:
        if r["family"].startswith("A"):
            print(f"  A {r['marker']:16s} HR {r['effect']:.2f} ({r['ci_low']:.2f}-{r['ci_high']:.2f}) "
                  f"p={r['p']:.3f} q={r['q_family']:.2f} n={r['n']} ev={r['events']}")


# ---------------------------------------------------------------- stage: plot
COL_POS, COL_NEG = "#c2410c", "#1d4ed8"   # orange / blue, readable in greyscale too


def _step(t, e):
    xs, ys = [0.0], [1.0]
    for u, s, _, _ in kaplan_meier(t, e):
        xs += [u / DAYS_PER_YEAR, u / DAYS_PER_YEAR]
        ys += [ys[-1], s]
    xs.append(max(t) / DAYS_PER_YEAR)
    ys.append(ys[-1])
    return xs, ys


def km_figure(path, t, e, g, labels, title, outcome, note):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(7.2, 5.6), facecolor="white")
    ax = fig.add_axes([0.13, 0.36, 0.82, 0.55], facecolor="white")
    ticks = [0, 2, 4, 6, 8, 10]
    for grp, col, lab in [(1, COL_POS, labels[1]), (0, COL_NEG, labels[0])]:
        tt, ee = t[g == grp], e[g == grp]
        xs, ys = _step(tt, ee)
        ax.plot(xs, ys, color=col, lw=2.2, label=f"{lab} (n={len(tt)}, {int(ee.sum())} events)",
                drawstyle="default")
        cens = tt[ee == 0]
        sv = [km_at(tt, ee, c) or 0 for c in cens]
        ax.plot(cens / DAYS_PER_YEAR, sv, "|", color=col, ms=8, mew=1.4)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 1.03)
    ax.set_xticks(ticks)
    ax.set_xlabel("Years from diagnosis")
    ax.set_ylabel(f"{outcome} (probability)")
    ax.set_title(title, fontsize=12.5, loc="left", fontweight="bold")
    ax.grid(color="#e5e7eb", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower left", frameon=False, fontsize=10)
    ax.text(0.99, 0.97, note, transform=ax.transAxes, ha="right", va="top", fontsize=10,
            color="#111827", bbox=dict(facecolor="white", edgecolor="#d1d5db", boxstyle="round,pad=0.4"))
    # Number at risk
    tab = fig.add_axes([0.13, 0.06, 0.82, 0.16], facecolor="white")
    tab.set_xlim(0, 10.5)
    tab.set_ylim(-0.5, 1.6)
    tab.axis("off")
    tab.text(-0.3, 1.45, "Number at risk", fontsize=10, fontweight="bold", ha="left")
    for yrow, (grp, col, lab) in zip([0.8, 0.0], [(1, COL_POS, labels[1]), (0, COL_NEG, labels[0])]):
        tt = t[g == grp]
        for x in ticks:
            tab.text(x, yrow, str(int(np.sum(tt >= x * DAYS_PER_YEAR))), ha="center", va="center",
                     fontsize=10, color=col)
    fig.text(0.01, 0.235, labels[1], color=COL_POS, fontsize=9, ha="left")
    fig.text(0.01, 0.135, labels[0], color=COL_NEG, fontsize=9, ha="left")
    fig.savefig(path, format="svg", facecolor="white")
    plt.close(fig)


def forest_figure(path, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10.5, "svg.fonttype": "none", "font.family": "DejaVu Sans"})
    a = [r for r in res if r["family"].startswith("A")]
    n = len(a)
    fig, ax = plt.subplots(figsize=(8.6, 0.36 * n + 1.6), facecolor="white")
    fig.subplots_adjust(left=0.40, right=0.97, top=0.92, bottom=0.11)
    for i, r in enumerate(a):
        y = n - 1 - i
        hr, lo, hi = (float(r[k]) for k in ("effect", "ci_low", "ci_high"))
        ax.plot([lo, hi], [y, y], color="#374151", lw=1.5)
        ax.plot(hr, y, "s", color="#1d4ed8", ms=6)
        ax.text(1.02, y, f"q={float(r['q_family']):.2f}", transform=ax.get_yaxis_transform(),
                va="center", fontsize=9, color="#374151")
    ax.axvline(1, color="#9ca3af", lw=1, ls="--")
    ax.set_xscale("log")
    ax.set_yticks(range(n))
    ax.set_yticklabels([f"{r['marker_label']}  ({r['marker_definition'].replace('per ', '/ ')})" for r in a][::-1],
                       fontsize=9)
    ax.set_xlabel("Hazard ratio for death, adjusted for metastasis at diagnosis (log scale, 95% CI)")
    ax.set_title("Pre-specified markers and overall survival (TARGET-OS)", loc="left", fontweight="bold",
                 fontsize=11.5)
    ax.grid(axis="x", color="#e5e7eb")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(path, format="svg", facecolor="white")
    plt.close(fig)


def stage_plot():
    os.makedirs(FIG_DIR, exist_ok=True)
    rows = load_patients()
    specs = {s["name"]: s for s in marker_specs(rows)}
    res = list(csv.DictReader(open(OUT_CSV)))

    def find(marker, fam):
        return next(r for r in res if r["marker"] == marker and r["family"].startswith(fam))

    def fmt_p(p):
        p = float(p)
        return f"{p:.2g}" if p >= 0.001 else "<0.001"

    made = []
    # positive control
    sub = [r for r in rows if r["metastatic"] is not None and r["os_days"] is not None]
    r = next(x for x in res if x["marker"] == "metastatic" and x["outcome"] == "OS")
    km_figure(os.path.join(FIG_DIR, "survival_metastasis_os.svg"),
              _arr(sub, ["os_days"])[:, 0], _arr(sub, ["os_event"])[:, 0].astype(int),
              np.array([x["metastatic"] for x in sub], int), ["No metastasis", "Metastasis at diagnosis"],
              "Positive control: metastasis at diagnosis", "Overall survival",
              f"HR {float(r['effect']):.2f} (95% CI {float(r['ci_low']):.2f}–{float(r['ci_high']):.2f})\nlog-rank p = {fmt_p(r['p'])}")
    made.append("survival_metastasis_os.svg")
    for m in PLOT_MARKERS:
        s = specs[m]
        sub = [x for x in rows if s["bin"](x) is not None and x["os_days"] is not None]
        b, a = find(m, "B"), find(m, "A")
        if s["type"] == "copy number":
            labels = ["Not amplified", "Amplified"] if "amp" in m else ["No deep deletion", "Deep deletion"]
        else:
            labels = ["At or below median", "Above median"]
        note = (f"Log-rank p = {fmt_p(b['p'])} (BH q = {float(b['q_family']):.2f})\n"
                f"HR {float(b['effect']):.2f} (95% CI {float(b['ci_low']):.2f}–{float(b['ci_high']):.2f})\n"
                f"Continuous, adjusted: HR {float(a['effect']):.2f} ({float(a['ci_low']):.2f}–{float(a['ci_high']):.2f}), q = {float(a['q_family']):.2f}")
        fn = f"survival_{m.lower()}_os.svg"
        km_figure(os.path.join(FIG_DIR, fn), _arr(sub, ["os_days"])[:, 0],
                  _arr(sub, ["os_event"])[:, 0].astype(int), np.array([s["bin"](x) for x in sub], int),
                  labels, s["label"], "Overall survival", note)
        made.append(fn)
    forest_figure(os.path.join(FIG_DIR, "survival_forest_os.svg"), res)
    made.append("survival_forest_os.svg")
    print(f"[plot] wrote {len(made)} SVGs to docs/figures/: {', '.join(made)}")


# ----------------------------------------------------------------------- main
STAGES = {"fetch": stage_fetch, "build": stage_build, "analyse": stage_analyse, "plot": stage_plot}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "all":
        for name in ("fetch", "build", "analyse", "plot"):
            STAGES[name]()
    elif arg in STAGES:
        STAGES[arg]()
    else:
        raise SystemExit(f"usage: {sys.argv[0]} [{'|'.join(STAGES)}|all]")
