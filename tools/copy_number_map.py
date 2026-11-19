"""Map actionable copy-number changes in osteosarcoma from open data, as
groundwork for lead 2 of `reports/Ranked leads and research partners.md`:
does VEGFA (6p21) or KDR/PDGFRA/KIT (4q12) amplification predict benefit
from VEGFR2-blocking kinase-inhibitor pills?

Data (all open access, no credentials):

  * NCI GDC, project TARGET-OS:
      - "Gene Level Copy Number" (ASCAT2 on Affymetrix SNP6 genotyping
        arrays; integer, purity-corrected absolute copy number per gene),
        one primary tumour per patient, 81 patients at the time of writing.
      - "Allele-specific Copy Number Segment" (ASCAT2, same arrays), used
        only to estimate each tumour's ploidy (length-weighted mean copy
        number), because osteosarcomas are often far from diploid.
      - "Copy Number Segment" (GATK4 CNV on whole genomes, log2 ratios),
        used as an independent-platform check for the overlapping patients.
  * Expression: the TARGET-OS STAR gene-count files already cached by
    tools/surface_targets.py in data/surface_targets_raw/ (reused, not
    re-downloaded).

Calls (per patient, per gene; ploidy P from the allele-specific segments):

  * amplification (primary)  : copy number >= 2 x P
  * gain (lenient, sensitivity): copy number >= 1.5 x P
  * high-copy (strict, sensitivity): copy number >= 8 absolute
  * deep deletion            : min_copy_number == 0 (any part of the gene
                               homozygously lost)
  * loss                     : copy number < 0.65 x P (relative loss)

Frequencies get Wilson 95% confidence intervals; co-occurrence uses a
two-sided Fisher exact test. Expression vs copy number uses Spearman rho
with a Fisher-z 95% CI and a seeded permutation p-value. The power stage
uses Schoenfeld's formula for a Cox hazard ratio.

Raw downloads go to data/copy_number_raw/ (git-ignored). Outputs:

  data/osteosarcoma_copy_number_frequencies.csv   one row per gene x call
  data/copy_number_raw/patient_calls.csv          per-patient table
  data/copy_number_raw/summary.json               everything the report uses

Run from the repo root, stage by stage or all at once:

    python3 tools/copy_number_map.py manifest   # list open CNV files (GDC)
    python3 tools/copy_number_map.py download   # fetch /data/{file_id}
    python3 tools/copy_number_map.py call       # per-patient calls + CSV
    python3 tools/copy_number_map.py wgs        # WGS cross-check
    python3 tools/copy_number_map.py expression # CN vs RNA for VEGFA, KDR, ...
    python3 tools/copy_number_map.py power      # sample sizes for lead 2
    python3 tools/copy_number_map.py all

Only the Python standard library is needed.
"""
import csv
import glob
import json
import math
import os
import random
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "copy_number_raw")
EXPR_RAW = os.path.join(ROOT, "data", "surface_targets_raw")
OUT_CSV = os.path.join(ROOT, "data", "osteosarcoma_copy_number_frequencies.csv")
SUMMARY = os.path.join(RAW, "summary.json")

GDC_FILES = "https://api.gdc.cancer.gov/files"
GDC_DATA = "https://api.gdc.cancer.gov/data"
UA = {"User-Agent": "open-science-copy-number-map/1.0"}

# Genes, cytoband and the reason each is on the list. Cytobands are the
# standard HGNC/NCBI locations.
GENES = [
    ("VEGFA", "6p21.1", "VEGF ligand; lead 2 (6p21 amplicon)"),
    ("KDR", "4q12", "VEGFR2; lead 2 (4q12 amplicon)"),
    ("PDGFRA", "4q12", "PDGFR-alpha; lead 2 (4q12 amplicon)"),
    ("KIT", "4q12", "KIT; lead 2 (4q12 amplicon)"),
    ("FGFR1", "8p11.23", "FGFR1; target of lenvatinib, FGFR blockers"),
    ("MET", "7q31.2", "MET; cabozantinib target"),
    ("MYC", "8q24.21", "MYC; common osteosarcoma amplicon"),
    ("CCNE1", "19q12", "cyclin E1; CDK2 inhibitors"),
    ("CDK4", "12q14.1", "CDK4; CDK4/6 inhibitors"),
    ("MDM2", "12q15", "MDM2; MDM2 inhibitors"),
    ("PTK2", "8q24.3", "FAK; defactinib"),
    ("DKK1", "10q21.1", "DKK1 region; DKN-01"),
    ("CD276", "15q24.1", "B7-H3; ADCs and CAR-T"),
    ("ERBB2", "17q12", "HER2; ADCs"),
    ("RB1", "13q14.2", "tumour suppressor"),
    ("CDKN2A", "9p21.3", "tumour suppressor; CDK4/6 rationale"),
    ("TP53", "17p13.1", "tumour suppressor"),
    ("PTEN", "10q23.31", "tumour suppressor; PI3K/mTOR rationale"),
]
SYMBOLS = [g[0] for g in GENES]
AMP_GENES = SYMBOLS[:14]            # amplification is the event of interest
DEL_GENES = ["RB1", "CDKN2A", "TP53", "PTEN", "DKK1"]  # deletions reported too
VEGFR_SET = ["VEGFA", "KDR", "PDGFRA", "KIT"]
REGION_4Q12 = ["KDR", "PDGFRA", "KIT"]
PILL_TARGETS = VEGFR_SET + ["FGFR1", "MET"]

# Published frequencies for comparison (step 3 of the task). Only values we
# read are listed; the label says how we read them. "pct" is a percentage of
# tumours or patients in that study. Filled in from research_notes/Copy
# number/notes.md; see that file for quotes and PMIDs.
MSK = "Suehara 2019, MSK-IMPACT, 66 patients (paper, full text; PMC6825534)"
SAY = "Sayles 2019, whole genomes, >4 purity-adjusted copies (paper, full text; PMC7134333)"
FMI = "Bousquet 2026, Foundation Medicine panel, 653 patients aged 40 or under (paper, abstract only; PMID 42424099)"
CCAT = "Japan C-CAT panel, 204 patients, any alteration (paper, full text; PMC11785636)"
PUBLISHED = {
    ("VEGFA", "amp"): [f"24% (14 of 59 patients; 17 samples) {MSK}", f"23% {SAY}",
                       f"17% (35 of 204) {CCAT}"],
    ("KDR", "amp"): [f"15% (11 samples) {MSK}"],
    ("PDGFRA", "amp"): [f"18% (13 samples) {MSK}"],
    ("KIT", "amp"): [f"15% (11 samples) {MSK}"],
    ("4q12_amp", "amp"): [f"20% (13 of 66 patients) {MSK}"],
    ("vegfr_any_amp", "amp"): [f"at least 40% PDGFRA or VEGFA amplified {MSK}"],
    ("FGFR1", "amp"): ["9.6% (24 of 275 bone osteosarcomas) by FISH, Amary 2014 (paper, full text; PMC4303166)"],
    ("MYC", "amp"): [f"39% {SAY}", f"17% altered {FMI}"],
    ("CCNE1", "amp"): [f"33% {SAY}", f"8% (6 samples) {MSK}"],
    ("CDK4", "amp"): [f"11% {SAY}", f"14% (9 of 66) {MSK}"],
    ("MDM2", "amp"): [f"14% (9 of 66) {MSK}"],
    ("CDKN2A", "deepdel"): [f"22% (16 samples) deleted {MSK}", f"18% altered {CCAT}"],
    ("PTEN", "loss"): [f"56% loss {SAY}"],
    ("PTEN", "deepdel"): [f"3% (2 of 66) deletion or truncating mutation {MSK}"],
    ("RB1", "loss"): [f"64% deletion, SV or SNV {SAY}", f"22% altered {FMI}"],
    ("TP53", "loss"): [f"74% deletion, SV or SNV {SAY}", f"55% altered {FMI}"],
}


# ----------------------------------------------------------------- helpers
def http(url, payload=None, retries=6, timeout=300):
    """GET (or POST JSON) with backoff; GDC sometimes drops connections."""
    last = None
    for i in range(retries):
        try:
            if payload is None:
                req = urllib.request.Request(url, headers=UA)
            else:
                req = urllib.request.Request(
                    url, data=json.dumps(payload).encode(),
                    headers=dict(UA, **{"Content-Type": "application/json"}))
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - network flakiness is expected
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"request failed after {retries} tries: {url} :: {last}")


def wilson(k, n, z=1.959964):
    """Wilson score 95% interval for k of n, as percentages."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (100 * max(0.0, centre - half), 100 * min(1.0, centre + half))


def fisher_two_sided(a, b, c, d):
    """Two-sided Fisher exact p for [[a, b], [c, d]] (sum of tables as or
    less likely than the observed one)."""
    r1, c1, n = a + b, a + c, a + b + c + d

    def logp(x):
        return (math.lgamma(r1 + 1) - math.lgamma(x + 1) - math.lgamma(r1 - x + 1)
                + math.lgamma(n - r1 + 1) - math.lgamma(c1 - x + 1)
                - math.lgamma(n - r1 - c1 + x + 1)
                - (math.lgamma(n + 1) - math.lgamma(c1 + 1) - math.lgamma(n - c1 + 1)))
    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    obs = logp(a)
    return min(1.0, sum(math.exp(logp(x)) for x in range(lo, hi + 1)
                        if logp(x) <= obs + 1e-9))


def ranks(v):
    """Average ranks (1-based), ties shared."""
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float("nan")


def spearman(x, y, nperm=10000, seed=1):
    """rho, Fisher-z 95% CI (Bonett-Wright variance 1.06/(n-3)), and a
    two-sided permutation p-value."""
    rx, ry = ranks(x), ranks(y)
    rho = pearson(rx, ry)
    n = len(x)
    se = math.sqrt(1.06 / (n - 3))
    z = math.atanh(max(min(rho, 0.999999), -0.999999))
    ci = (math.tanh(z - 1.959964 * se), math.tanh(z + 1.959964 * se))
    rng = random.Random(seed)
    ry2 = list(ry)
    hits = 0
    for _ in range(nperm):
        rng.shuffle(ry2)
        if abs(pearson(rx, ry2)) >= abs(rho) - 1e-12:
            hits += 1
    return rho, ci, (hits + 1) / (nperm + 1)


def median(v):
    s = sorted(v)
    n = len(s)
    if n == 0:
        return float("nan")
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def load_summary():
    return json.load(open(SUMMARY)) if os.path.exists(SUMMARY) else {}


def save_summary(key, value):
    s = load_summary()
    s[key] = value
    json.dump(s, open(SUMMARY, "w"), indent=1)


# ------------------------------------------------------------ stage: manifest
def stage_manifest():
    """All open-access copy-number files in TARGET-OS, with case and sample."""
    os.makedirs(RAW, exist_ok=True)
    payload = {
        "filters": {"op": "and", "content": [
            {"op": "in", "content": {"field": "cases.project.project_id",
                                     "value": ["TARGET-OS"]}},
            {"op": "in", "content": {"field": "data_category",
                                     "value": ["Copy Number Variation"]}},
            {"op": "in", "content": {"field": "access", "value": ["open"]}},
        ]},
        "fields": ",".join([
            "file_id", "file_name", "data_type", "analysis.workflow_type",
            "experimental_strategy", "cases.submitter_id",
            "cases.samples.submitter_id", "cases.samples.sample_type",
            "cases.samples.tissue_type"]),
        "format": "json", "size": "2000",
    }
    hits = json.loads(http(GDC_FILES, payload))["data"]["hits"]
    rows = []
    for h in hits:
        case = (h.get("cases") or [{}])[0]
        tum = [s for s in case.get("samples", []) if s.get("tissue_type") == "Tumor"]
        rows.append({
            "file_id": h["file_id"], "file_name": h["file_name"],
            "data_type": h["data_type"],
            "workflow": (h.get("analysis") or {}).get("workflow_type", ""),
            "strategy": h.get("experimental_strategy", ""),
            "case": case.get("submitter_id", ""),
            "tumour_sample": ";".join(s["submitter_id"] for s in tum),
            "tumour_type": ";".join(s["sample_type"] for s in tum),
        })
    # Also record what is controlled-access, for the limits section.
    facet = {
        "filters": {"op": "and", "content": [
            {"op": "in", "content": {"field": "cases.project.project_id",
                                     "value": ["TARGET-OS"]}},
            {"op": "in", "content": {"field": "data_category",
                                     "value": ["Copy Number Variation"]}}]},
        "facets": "data_type,access", "size": "0"}
    agg = json.loads(http(GDC_FILES, facet))["data"]["aggregations"]
    # Age at diagnosis per case (open clinical fields), to describe the cohort.
    cases = json.loads(http(GDC_FILES.replace("/files", "/cases"), {
        "filters": {"op": "in", "content": {"field": "project.project_id",
                                            "value": ["TARGET-OS"]}},
        "fields": "submitter_id,diagnoses.age_at_diagnosis", "size": "2000"}))["data"]["hits"]
    ages = {c["submitter_id"]: d["age_at_diagnosis"] / 365.25
            for c in cases for d in c.get("diagnoses", []) if d.get("age_at_diagnosis")}
    json.dump(ages, open(os.path.join(RAW, "ages.json"), "w"), indent=1)
    json.dump({"retrieved": time.strftime("%Y-%m-%d"), "files": rows,
               "facets_all_access": agg},
              open(os.path.join(RAW, "manifest.json"), "w"), indent=1)
    by = {}
    for r in rows:
        by[r["data_type"]] = by.get(r["data_type"], 0) + 1
    print(f"[manifest] {len(rows)} open CNV files: {by}")
    return rows


def manifest():
    p = os.path.join(RAW, "manifest.json")
    if not os.path.exists(p):
        stage_manifest()
    return json.load(open(p))["files"]


SUBDIR = {"Gene Level Copy Number": "gene_level",
          "Allele-specific Copy Number Segment": "ascat_segments",
          "Copy Number Segment": "wgs_segments"}


def path_for(row):
    return os.path.join(RAW, SUBDIR[row["data_type"]], row["file_id"] + ".txt")


# ------------------------------------------------------------ stage: download
def stage_download():
    rows = manifest()
    todo = [r for r in rows if not os.path.exists(path_for(r))]
    print(f"[download] {len(rows) - len(todo)} cached, {len(todo)} to fetch")
    for i, r in enumerate(todo):
        os.makedirs(os.path.dirname(path_for(r)), exist_ok=True)
        data = http(f"{GDC_DATA}/{r['file_id']}")
        tmp = path_for(r) + ".part"
        open(tmp, "wb").write(data)
        os.replace(tmp, path_for(r))
        if (i + 1) % 20 == 0:
            print(f"[download]   {i + 1}/{len(todo)}")
    print("[download] done")


# ---------------------------------------------------------------- stage: call
def ploidy_by_case(rows):
    """Length-weighted mean total copy number from ASCAT2 segments."""
    out = {}
    for r in rows:
        if r["data_type"] != "Allele-specific Copy Number Segment":
            continue
        tot = wsum = 0.0
        for rec in csv.DictReader(open(path_for(r)), delimiter="\t"):
            if rec["Chromosome"] in ("chrX", "chrY"):
                continue
            ln = int(rec["End"]) - int(rec["Start"]) + 1
            tot += ln
            wsum += ln * float(rec["Copy_Number"])
        out[r["case"]] = wsum / tot if tot else float("nan")
    return out


def gene_cn(path, wanted):
    """{symbol: (copy_number, min, max, chrom, start, end)} for wanted genes.
    copy_number is blank in the GDC file when the gene spans a breakpoint;
    we then fall back to the mean of min and max."""
    out = {}
    for rec in csv.DictReader(open(path), delimiter="\t"):
        s = rec["gene_name"]
        if s not in wanted or s in out:
            continue

        def f(k):
            return float(rec[k]) if rec[k] not in ("", "NA") else None
        cn, lo, hi = f("copy_number"), f("min_copy_number"), f("max_copy_number")
        if cn is None and lo is not None and hi is not None:
            cn = (lo + hi) / 2
        out[s] = (cn, lo, hi, rec["chromosome"], int(rec["start"]), int(rec["end"]))
    return out


def call_one(cn, lo, ploidy):
    return {
        "amp": cn is not None and cn >= 2 * ploidy,
        "gain": cn is not None and cn >= 1.5 * ploidy,
        "high8": cn is not None and cn >= 8,
        "deepdel": lo is not None and lo == 0,
        "loss": cn is not None and cn < 0.65 * ploidy,
        "gt4": cn is not None and cn > 4,
    }


EVENT_LABEL = {
    "amp": "amplification: CN >= 2 x ploidy (primary)",
    "gain": "gain: CN >= 1.5 x ploidy (lenient)",
    "high8": "high copy: CN >= 8 (strict)",
    "deepdel": "deep deletion: min CN = 0",
    "loss": "loss: CN < 0.65 x ploidy",
    "gt4": "CN > 4 absolute (Sayles 2019 threshold; comparison only)",
}


def stage_call():
    rows = manifest()
    gl = [r for r in rows if r["data_type"] == "Gene Level Copy Number"]
    ploidy = ploidy_by_case(rows)
    patients = []
    coords = {}
    seen = set()
    for r in sorted(gl, key=lambda x: x["case"]):
        if r["case"] in seen:          # one tumour per patient
            continue
        seen.add(r["case"])
        g = gene_cn(path_for(r), set(SYMBOLS))
        p = ploidy.get(r["case"], float("nan"))
        rec = {"case": r["case"], "sample": r["tumour_sample"],
               "sample_type": r["tumour_type"], "ploidy": round(p, 3)}
        for s in SYMBOLS:
            cn, lo, hi, ch, st, en = g.get(s, (None, None, None, "", 0, 0))
            coords[s] = (ch, st, en)
            rec[f"{s}_cn"] = cn
            rec[f"{s}_min"] = lo
            for ev, v in call_one(cn, lo, p).items():
                rec[f"{s}_{ev}"] = int(v)
        rec["vegfr_any_amp"] = int(any(rec[f"{s}_amp"] for s in VEGFR_SET))
        rec["4q12_amp"] = int(any(rec[f"{s}_amp"] for s in REGION_4Q12))
        rec["pill_target_any_amp"] = int(any(rec[f"{s}_amp"] for s in PILL_TARGETS))
        for ev in ("gain", "high8"):
            rec[f"vegfr_any_{ev}"] = int(any(rec[f"{s}_{ev}"] for s in VEGFR_SET))
        patients.append(rec)
    n = len(patients)
    with open(os.path.join(RAW, "patient_calls.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(patients[0].keys()))
        w.writeheader()
        w.writerows(patients)
    pl = [p["ploidy"] for p in patients]
    print(f"[call] {n} patients; ploidy median {median(pl):.2f} "
          f"(range {min(pl):.2f}-{max(pl):.2f})")

    # Frequencies
    freq = []
    for s, band, why in GENES:
        events = ["amp", "gain", "high8", "gt4"] if s in AMP_GENES else []
        if s in DEL_GENES:
            events += ["deepdel", "loss"]
        for ev in events:
            k = sum(p[f"{s}_{ev}"] for p in patients)
            lo, hi = wilson(k, n)
            freq.append({"gene": s, "cytoband": band, "why_listed": why,
                         "event": ev, "definition": EVENT_LABEL[ev],
                         "n_patients": n, "n_altered": k,
                         "pct": round(100 * k / n, 1),
                         "ci95_low": round(lo, 1), "ci95_high": round(hi, 1)})
    for key, label in (("vegfr_any_amp", "any of VEGFA, KDR, PDGFRA, KIT amplified"),
                       ("4q12_amp", "any of KDR, PDGFRA, KIT (4q12) amplified"),
                       ("pill_target_any_amp", "any of VEGFA, KDR, PDGFRA, KIT, FGFR1, MET amplified"),
                       ("vegfr_any_gain", "any of VEGFA, KDR, PDGFRA, KIT at CN >= 1.5 x ploidy"),
                       ("vegfr_any_high8", "any of VEGFA, KDR, PDGFRA, KIT at CN >= 8")):
        k = sum(p[key] for p in patients)
        lo, hi = wilson(k, n)
        freq.append({"gene": key, "cytoband": "", "why_listed": "lead 2 grouping",
                     "event": key.rsplit("_", 1)[-1], "definition": label,
                     "n_patients": n, "n_altered": k, "pct": round(100 * k / n, 1),
                     "ci95_low": round(lo, 1), "ci95_high": round(hi, 1)})
    return patients, freq, coords


def cooccurrence(patients, pairs):
    out = []
    for a, b in pairs:
        ka = a if a.endswith("_amp") or a.startswith("_") else f"{a}_amp"
        kb = b if b.endswith("_amp") or b.startswith("_") else f"{b}_amp"
        both = sum(1 for p in patients if p[ka] and p[kb])
        only_a = sum(1 for p in patients if p[ka] and not p[kb])
        only_b = sum(1 for p in patients if not p[ka] and p[kb])
        neither = len(patients) - both - only_a - only_b
        # Haldane-corrected odds ratio, so empty cells do not give 0 or inf.
        orr = ((both + .5) * (neither + .5)) / ((only_a + .5) * (only_b + .5))
        out.append({"a": a, "b": b, "both": both, "only_a": only_a,
                    "only_b": only_b, "neither": neither,
                    "odds_ratio_haldane": round(orr, 2),
                    "fisher_p": round(fisher_two_sided(both, only_a, only_b, neither), 4)})
    return out


def stage_call_all():
    patients, freq, coords = stage_call()
    n = len(patients)
    pairs = [("VEGFA", "4q12_amp"), ("VEGFA", "KDR"), ("VEGFA", "PDGFRA"),
             ("VEGFA", "KIT"), ("KDR", "PDGFRA"), ("KDR", "KIT"), ("PDGFRA", "KIT"),
             ("VEGFA", "MYC"), ("VEGFA", "FGFR1"), ("VEGFA", "CCNE1"),
             ("4q12_amp", "MYC"), ("4q12_amp", "FGFR1"), ("MYC", "PTK2"),
             ("CDK4", "MDM2"), ("FGFR1", "MYC"), ("4q12_amp", "MDM2"),
             ("4q12_amp", "CDK4"), ("MYC", "CCNE1")]
    co = cooccurrence(patients, pairs)
    for c in co:
        print(f"[call] {c['a']} x {c['b']}: both {c['both']}, only first "
              f"{c['only_a']}, only second {c['only_b']}, neither {c['neither']}, "
              f"OR {c['odds_ratio_haldane']}, Fisher p {c['fisher_p']}")
    # Same 6p21 x 4q12 question at a stricter level (CN >= 3 x ploidy), to
    # see whether co-amplification survives when borderline calls are dropped.
    for p in patients:
        pl = p["ploidy"]
        p["_v3"] = int(p["VEGFA_cn"] is not None and p["VEGFA_cn"] >= 3 * pl)
        p["_q3"] = int(any(p[f"{g}_cn"] is not None and p[f"{g}_cn"] >= 3 * pl
                           for g in REGION_4Q12))
    co3 = cooccurrence(patients, [("_v3", "_q3")])[0]
    co3.update({"a": "VEGFA CN>=3x ploidy", "b": "4q12 CN>=3x ploidy"})
    co.append(co3)
    print(f"[call] strict 3x: VEGFA {co3['both'] + co3['only_a']}, 4q12 "
          f"{co3['both'] + co3['only_b']}, both {co3['both']}, Fisher p {co3['fisher_p']}")
    # How many VEGFR-pathway genes are amplified per patient
    dist = {}
    for p in patients:
        k = sum(p[f"{s}_amp"] for s in VEGFR_SET)
        dist[k] = dist.get(k, 0) + 1
    # 4q12 pattern: do the three genes travel together?
    pat = {}
    for p in patients:
        key = "".join("1" if p[f"{s}_amp"] else "0" for s in REGION_4Q12)
        pat[key] = pat.get(key, 0) + 1
    # Published comparison columns
    for f in freq:
        pub = PUBLISHED.get((f["gene"], f["event"]), [])
        f["published_comparison"] = " | ".join(pub)
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(freq[0].keys()))
        w.writeheader()
        w.writerows(freq)
    print(f"[call] wrote {OUT_CSV} ({len(freq)} rows)")
    for f in freq:
        if f["event"] in ("amp", "deepdel", "loss") or f["why_listed"] == "lead 2 grouping":
            print(f"[call] {f['gene']:20s} {f['event']:8s} {f['n_altered']:3d}/{n} "
                  f"{f['pct']:5.1f}% ({f['ci95_low']}-{f['ci95_high']})")
    ages_p = os.path.join(RAW, "ages.json")
    ages = json.load(open(ages_p)) if os.path.exists(ages_p) else {}
    av = [ages[p["case"]] for p in patients if p["case"] in ages]
    if av:
        print(f"[call] age at diagnosis: median {median(av):.1f} y "
              f"(range {min(av):.1f}-{max(av):.1f}); {sum(a >= 18 for a in av)} aged 18+")
    save_summary("call", {
        "n_patients": n,
        "age_median": median(av) if av else None,
        "age_range": [min(av), max(av)] if av else None,
        "n_age_18_plus": sum(a >= 18 for a in av),
        "ploidy_median": median([p["ploidy"] for p in patients]),
        "ploidy_min": min(p["ploidy"] for p in patients),
        "ploidy_max": max(p["ploidy"] for p in patients),
        "n_ploidy_ge_3": sum(1 for p in patients if p["ploidy"] >= 3),
        "frequencies": freq, "cooccurrence": co,
        "vegfr_genes_amplified_per_patient": dist,
        "pattern_4q12_KDR_PDGFRA_KIT": pat,
        "coords_hg38": coords,
        "sample_types": sorted({p["sample_type"] for p in patients}),
    })


# ----------------------------------------------------------------- stage: wgs
def seg_value(path, chrom, start, end, col="Segment_Mean"):
    """Length-weighted mean of a segment column over a gene's span."""
    tot = wsum = 0.0
    for rec in csv.DictReader(open(path), delimiter="\t"):
        if rec["Chromosome"] != chrom:
            continue
        s, e = int(rec["Start"]), int(rec["End"])
        ov = min(e, end) - max(s, start) + 1
        if ov > 0:
            tot += ov
            wsum += ov * float(rec[col])
    return wsum / tot if tot else None


def stage_wgs():
    """WGS GATK4 log2 ratios vs ASCAT2 calls for the shared patients.
    GATK log2 is relative to the sample's average copy number, so
    log2 >= 1 corresponds to the array call CN >= 2 x ploidy."""
    rows = manifest()
    s = load_summary()["call"]
    coords = s["coords_hg38"]
    calls = {p["case"]: p for p in csv.DictReader(open(os.path.join(RAW, "patient_calls.csv")))}
    wgs = [r for r in rows if r["data_type"] == "Copy Number Segment"]
    genes = VEGFR_SET + ["MYC", "CDK4", "MDM2", "CCNE1", "FGFR1"]
    res = {g: {"n": 0, "agree": 0, "array_only": 0, "wgs_only": 0, "both": 0}
           for g in genes}
    log2s = {g: [] for g in genes}
    shared = 0
    for r in wgs:
        if r["case"] not in calls:
            continue
        shared += 1
        for g in genes:
            ch, st, en = coords[g]
            v = seg_value(path_for(r), ch, st, en)
            if v is None:
                continue
            a = calls[r["case"]][f"{g}_amp"] == "1"
            w = v >= 1.0
            d = res[g]
            d["n"] += 1
            d["agree"] += int(a == w)
            d["both"] += int(a and w)
            d["array_only"] += int(a and not w)
            d["wgs_only"] += int(w and not a)
            cn = calls[r["case"]][f"{g}_cn"]
            pl = float(calls[r["case"]]["ploidy"])
            if cn not in ("", "None"):
                log2s[g].append((math.log2(max(float(cn), 0.1) / pl), v))
    for g in genes:
        x = [a for a, _ in log2s[g]]
        y = [b for _, b in log2s[g]]
        res[g]["pearson_log2_array_vs_wgs"] = round(pearson(x, y), 3) if len(x) > 3 else None
        d = res[g]
        print(f"[wgs] {g}: n={d['n']} agree={d['agree']} both={d['both']} "
              f"array-only={d['array_only']} wgs-only={d['wgs_only']} "
              f"r={d['pearson_log2_array_vs_wgs']}")
    print(f"[wgs] {len(wgs)} WGS files, {shared} patients also on arrays")
    save_summary("wgs", {"n_wgs_files": len(wgs), "n_shared": shared, "genes": res})


# ---------------------------------------------------------- stage: expression
EXPR_GENES = ["VEGFA", "KDR", "PDGFRA", "KIT", "MYC", "CDK4", "MDM2", "FGFR1",
              "MET", "CCNE1", "CD276", "PTK2"]


def stage_expression():
    """Copy number vs RNA (TPM) using the cached TARGET-OS STAR files."""
    man = json.load(open(os.path.join(EXPR_RAW, "gdc_manifest.json")))
    calls = {p["case"]: p for p in csv.DictReader(open(os.path.join(RAW, "patient_calls.csv")))}
    tpm = {}       # case -> {gene: tpm}
    types = {}
    for m in man:
        if m["sample_type"] != "Primary Tumor" or m["case"] in tpm:
            continue
        path = os.path.join(EXPR_RAW, "gdc_tsv", m["file_id"] + ".tsv")
        if not os.path.exists(path):
            continue
        vals = {}
        hdr = None
        for line in open(path):
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if hdr is None:
                hdr = parts
                ix_n, ix_t = hdr.index("gene_name"), hdr.index("tpm_unstranded")
                continue
            if parts[ix_n] in EXPR_GENES and parts[ix_n] not in vals:
                try:
                    vals[parts[ix_n]] = float(parts[ix_t])
                except ValueError:
                    pass
        tpm[m["case"]] = vals
        types[m["sample_type"]] = types.get(m["sample_type"], 0) + 1
    both = sorted(set(tpm) & set(calls))
    print(f"[expression] {len(tpm)} primary-tumour RNA samples; {len(both)} "
          f"patients with both RNA and copy number")
    out = {"n_rna": len(tpm), "n_both": len(both), "genes": {}}
    for g in EXPR_GENES:
        x, y, amp_e, non_e = [], [], [], []
        for c in both:
            cn = calls[c][f"{g}_cn"]
            if cn in ("", "None") or g not in tpm[c]:
                continue
            rel = float(cn) / float(calls[c]["ploidy"])
            e = math.log2(tpm[c][g] + 1)
            x.append(rel)
            y.append(e)
            (amp_e if calls[c][f"{g}_amp"] == "1" else non_e).append(tpm[c][g])
        if len(x) < 10:
            continue
        rho, ci, p = spearman(x, y)
        rho_abs, _, p_abs = spearman(
            [float(calls[c][f"{g}_cn"]) for c in both
             if calls[c][f"{g}_cn"] not in ("", "None") and g in tpm[c]], y)
        out["genes"][g] = {
            "n": len(x), "spearman_rho_rel_cn": round(rho, 3),
            "ci95": [round(ci[0], 3), round(ci[1], 3)], "perm_p": round(p, 4),
            "spearman_rho_abs_cn": round(rho_abs, 3), "perm_p_abs": round(p_abs, 4),
            "n_amp": len(amp_e), "median_tpm_amp": round(median(amp_e), 2) if amp_e else None,
            "median_tpm_not_amp": round(median(non_e), 2),
        }
        o = out["genes"][g]
        print(f"[expression] {g}: n={o['n']} rho(CN/ploidy)={o['spearman_rho_rel_cn']} "
              f"{o['ci95']} p={o['perm_p']}; rho(abs CN)={o['spearman_rho_abs_cn']}; "
              f"median TPM amp {o['median_tpm_amp']} (n={o['n_amp']}) vs "
              f"{o['median_tpm_not_amp']}")
    save_summary("expression", out)


# --------------------------------------------------------------- stage: power
# Osteosarcoma patients who received a VEGFR2-blocking pill (or its control)
# in the trials named for lead 2. Numbers are as read; "label" is the
# report's confidence label. ITCC-050 is included as a single-arm source.
TRIALS = [
    # name, drug, design, pill arm, control arm, crossover onto pill, label, source
    ("SARC024", "regorafenib", "randomized vs placebo", 22, 20, 11,
     "registry", "NCT02048371 participant flow: 22 regorafenib, 9 placebo, 11 placebo then crossover"),
    ("REGOBONE", "regorafenib", "randomized 2:1 vs placebo", 26, 12, 10,
     "paper, abstract only", "PMID 30477937 (registry NCT02389244 has no posted results)"),
    ("OLIE", "lenvatinib + IE", "randomized vs IE", 40, 41, 0,
     "registry", "NCT04154189 participant flow"),
    ("OAIE", "apatinib + IE", "randomized 2:1 vs IE", 53, 28, 0,
     "paper, full text", "PMC12647724 / NCT05277480"),
    ("CABONE", "cabozantinib", "single arm", 45, 0, 0,
     "registry", "NCT02243605: 45 osteosarcoma enrolled; 42 evaluable in the paper"),
    ("ADVL1622", "cabozantinib", "single arm (osteosarcoma stratum)", 29, 0, 0,
     "registry", "NCT02867592 participant flow"),
    ("ITCC-050", "lenvatinib", "single arm (osteosarcoma expansion)", 31, 0, 0,
     "registry", "NCT02432274 cohort 2B"),
]


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


Z975, Z80, Z90 = 1.959964, 0.841621, 1.281552


def events_needed(hr, p, power_z=Z80, alloc=None):
    """Schoenfeld: events for a two-group Cox comparison with group share p.
    With alloc (randomized share on the pill), events for the
    treatment-by-biomarker interaction, with hr read as the ratio of HRs."""
    k = p * (1 - p) * (alloc * (1 - alloc) if alloc else 1)
    return (Z975 + power_z) ** 2 / (k * math.log(hr) ** 2)


def power_for(events, hr, p, alloc=None):
    k = p * (1 - p) * (alloc * (1 - alloc) if alloc else 1)
    return ncdf(math.sqrt(events * k) * abs(math.log(hr)) - Z975)


def stage_power():
    s = load_summary()["call"]
    f = {(x["gene"], x["event"]): x for x in s["frequencies"]}
    prev = {
        "TARGET-OS any VEGFA/KDR/PDGFRA/KIT amp (our calculation)": f[("vegfr_any_amp", "amp")]["pct"] / 100,
        "TARGET-OS VEGFA amp only (our calculation)": f[("VEGFA", "amp")]["pct"] / 100,
        "Published ~40% VEGFA or PDGFRA (paper, abstract only; PMID 31175097)": 0.40,
        "Pessimistic 20%": 0.20,
    }
    EVENT_FRAC = 0.90   # assumption: PFS on pills is short (CABONE 9.5% at 12 mo)
    YIELDS = [1.0, 0.6]  # assumption: share of patients with usable CN data
    rows = []
    for name, pv in prev.items():
        if pv <= 0:
            continue
        for pz, plab in ((Z80, 80), (Z90, 90)):
            d = events_needed(0.5, pv, pz)
            for y in YIELDS:
                rows.append({"question": "amplified vs not, among pill-treated (HR 0.5)",
                             "prevalence": name, "p": round(pv, 3), "power": plab,
                             "events": math.ceil(d), "tissue_yield": y,
                             "patients_to_enrol": math.ceil(d / EVENT_FRAC / y)})
            # interaction (predictive) test, 1:1 or 2:1 randomization
            for alloc in (0.5, 2 / 3):
                di = events_needed(0.5, pv, pz, alloc=alloc)
                for y in YIELDS:
                    rows.append({"question": f"interaction: drug benefit differs by amp (ratio of HRs 0.5), alloc {alloc:.2f}",
                                 "prevalence": name, "p": round(pv, 3), "power": plab,
                                 "events": math.ceil(di), "tissue_yield": y,
                                 "patients_to_enrol": math.ceil(di / EVENT_FRAC / y)})
    pill_rand = sum(t[3] for t in TRIALS if t[4] > 0)
    pill_cross = sum(t[5] for t in TRIALS)
    pill_single = sum(t[3] for t in TRIALS if t[4] == 0)
    pill_total = pill_rand + pill_cross + pill_single
    rand_total = sum(t[3] + t[4] for t in TRIALS if t[4] > 0)
    single_agent = sum(t[3] + t[5] for t in TRIALS if "IE" not in t[1])
    achieved = []
    for name, pv in prev.items():
        for pool_name, npool, alloc in (
                ("all pill-exposed (randomized pill arms + crossover + single arm)", pill_total, None),
                ("pill alone only (no IE)", single_agent, None),
                ("randomized trials, interaction test (pooled allocation)", rand_total,
                 pill_rand / rand_total)):
            for y in YIELDS:
                ev = npool * EVENT_FRAC * y
                achieved.append({"pool": pool_name, "n_pool": npool, "tissue_yield": y,
                                 "events": round(ev), "prevalence": name, "p": round(pv, 3),
                                 "power_hr_0.5": round(power_for(ev, 0.5, pv, alloc), 3)})
    for r in achieved:
        print(f"[power] {r['pool'][:45]:45s} n={r['n_pool']} yield={r['tissue_yield']} "
              f"p={r['p']} -> power {r['power_hr_0.5']}")
    for r in rows:
        if r["power"] == 80:
            print(f"[power] {r['question'][:60]:60s} p={r['p']} y={r['tissue_yield']} "
                  f"events={r['events']} enrol={r['patients_to_enrol']}")
    save_summary("power", {
        "assumptions": {"alpha_two_sided": 0.05, "event_fraction": EVENT_FRAC,
                        "tissue_yields": YIELDS, "target_hr": 0.5,
                        "method": "Schoenfeld (1983) events formula; interaction "
                                  "variance multiplies by allocation share"},
        "trials": [dict(zip(["trial", "drug", "design", "pill_arm", "control_arm",
                             "crossover", "label", "source"], t)) for t in TRIALS],
        "pool": {"pill_randomized_arms": pill_rand, "crossover": pill_cross,
                 "single_arm": pill_single, "pill_exposed_total": pill_total,
                 "randomized_total": rand_total, "pill_alone_total": single_agent},
        "required": rows, "achieved": achieved})


# ------------------------------------------------------------------- main
STAGES = {"manifest": stage_manifest, "download": stage_download,
          "call": stage_call_all, "wgs": stage_wgs,
          "expression": stage_expression, "power": stage_power}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    order = ["manifest", "download", "call", "wgs", "expression", "power"]
    if arg == "all":
        for st in order:
            STAGES[st]()
    elif arg in STAGES:
        STAGES[arg]()
    else:
        sys.exit(f"unknown stage {arg}; choose from {order + ['all']}")
