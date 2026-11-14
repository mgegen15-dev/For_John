"""Find candidate cell-surface targets for antibody-drug conjugates, bispecifics
or CAR-T in osteosarcoma, using only open data.

The idea is a therapeutic-window screen. A good surface target is expressed
high and in nearly every tumour, and expressed as little as possible in the
normal tissues you cannot afford to damage. So the pipeline is:

  1. TUMOUR  -- TARGET-OS RNA-seq from the NCI GDC (open-access STAR gene
     counts, which carry a tpm_unstranded column). ~88 samples.
  2. SURFACE -- keep only genes the Human Protein Atlas annotates as
     predicted membrane proteins and/or localised to the plasma membrane.
  3. NORMAL  -- GTEx v8 median TPM per tissue (54 tissues), with a named
     subset flagged as "vital" (heart, lung, liver, kidney, brain, nerve,
     colon, artery, whole blood, ...).
  4. SCORE   -- therapeutic window = tumour median TPM vs the worst vital
     normal tissue, times the fraction of tumours expressing the gene.
  5. CONTEXT -- for the leading candidates, ClinicalTrials.gov API v2 is
     searched for any existing antibody/ADC/bispecific/CAR programme against
     that target in any cancer, and osteosarcoma literature counts are taken
     from the repo's own evidence tables.

Stages cache to data/surface_targets_raw/ (git-ignored) so the script is
re-runnable without re-downloading. Run stages individually or all at once:

    python3 tools/surface_targets.py gdc      # download + build tumour matrix
    python3 tools/surface_targets.py hpa      # surface annotation
    python3 tools/surface_targets.py gtex     # normal tissue medians
    python3 tools/surface_targets.py rank     # score + write the CSV
    python3 tools/surface_targets.py context  # trials + literature for the top
    python3 tools/surface_targets.py all

Nothing here needs credentials; every endpoint used is public.
"""
import csv
import glob
import gzip
import io
import json
import os
import re
import sys
import tarfile
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "surface_targets_raw")
OUT_CSV = os.path.join(ROOT, "data", "osteosarcoma_surface_target_candidates.csv")
os.makedirs(RAW, exist_ok=True)

GDC_FILES = "https://api.gdc.cancer.gov/files"
GDC_DATA = "https://api.gdc.cancer.gov/data"
HPA_DL = "https://www.proteinatlas.org/api/search_download.php"
HPA_GENE = "https://www.proteinatlas.org/{ensg}.json"
GTEX_GENE = "https://gtexportal.org/api/v2/reference/gene"
GTEX_MED = "https://gtexportal.org/api/v2/expression/medianGeneExpression"
CTGOV = "https://clinicaltrials.gov/api/v2/studies"

UA = {"User-Agent": "open-science-target-screen/1.0"}

# GTEx v8 tissues where on-target/off-tumour toxicity would most likely be
# dose-limiting or fatal. Used for the "max vital normal" denominator.
VITAL = [
    "Heart_Left_Ventricle", "Heart_Atrial_Appendage",
    "Lung",
    "Liver",
    "Kidney_Cortex", "Kidney_Medulla",
    "Brain_Cortex", "Brain_Cerebellum", "Brain_Hippocampus",
    "Brain_Hypothalamus", "Brain_Substantia_nigra", "Brain_Spinal_cord_cervical_c-1",
    "Brain_Frontal_Cortex_BA9", "Brain_Anterior_cingulate_cortex_BA24",
    "Brain_Amygdala", "Brain_Caudate_basal_ganglia", "Brain_Nucleus_accumbens_basal_ganglia",
    "Brain_Putamen_basal_ganglia", "Brain_Cerebellar_Hemisphere",
    "Nerve_Tibial",
    "Colon_Sigmoid", "Colon_Transverse", "Small_Intestine_Terminal_Ileum",
    "Artery_Aorta", "Artery_Coronary", "Artery_Tibial",
    "Whole_Blood",
    "Esophagus_Mucosa", "Stomach",
    "Pancreas",
    "Adrenal_Gland",
    "Muscle_Skeletal",
]

TUMOUR_TPM_FLOOR = 10.0   # a gene must reach this median TPM in tumours
EXPR_FLOOR = 5.0          # per-sample TPM counted as "expressing"

# Targets already in osteosarcoma clinical development -- excluded from the
# novel list but carried through as positive controls to sanity-check ranking.
IN_TRIALS = ["CD276", "ERBB2", "B4GALNT1", "GPNMB", "EGFR", "IL11RA", "EPHA2", "ALPL"]
CONTROLS = IN_TRIALS + ["LRRC15", "MMP14", "CDH11"]


def get(url, params=None, retries=4, timeout=180):
    """GET with urlencoded params (repeated keys allowed) and simple backoff."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params, doseq=True)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - network flakiness is expected
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"GET failed after {retries} tries: {url[:160]} :: {last}")


def get_json(url, params=None, **kw):
    return json.loads(get(url, params, **kw))


def post_json(url, payload, timeout=300, retries=3):
    body = json.dumps(payload).encode()
    hdr = dict(UA, **{"Content-Type": "application/json"})
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=hdr)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"POST failed: {url} :: {last}")


# ---------------------------------------------------------------- stage: GDC
def gdc_manifest():
    """Every open-access gene-expression file in TARGET-OS, with sample type."""
    cache = os.path.join(RAW, "gdc_manifest.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    payload = {
        "filters": {"op": "and", "content": [
            {"op": "in", "content": {"field": "cases.project.project_id",
                                     "value": ["TARGET-OS"]}},
            {"op": "in", "content": {"field": "data_type",
                                     "value": ["Gene Expression Quantification"]}},
            {"op": "in", "content": {"field": "access", "value": ["open"]}},
        ]},
        "fields": ",".join([
            "file_id", "file_name", "analysis.workflow_type",
            "cases.submitter_id", "cases.samples.sample_type",
            "cases.samples.submitter_id",
        ]),
        "format": "json", "size": "2000",
    }
    d = post_json(GDC_FILES, payload)
    hits = d["data"]["hits"]
    rows = []
    for h in hits:
        case = (h.get("cases") or [{}])[0]
        samp = (case.get("samples") or [{}])[0]
        rows.append({
            "file_id": h["file_id"],
            "file_name": h["file_name"],
            "workflow": (h.get("analysis") or {}).get("workflow_type", ""),
            "case": case.get("submitter_id", ""),
            "sample_type": samp.get("sample_type", ""),
            "sample": samp.get("submitter_id", ""),
        })
    json.dump(rows, open(cache, "w"), indent=1)
    print(f"[gdc] manifest: {len(rows)} open expression files in TARGET-OS")
    return rows


def gdc_download(rows):
    """Fetch the expression files as one tarball per chunk (fewer round trips)."""
    want = {r["file_id"] for r in rows}
    have = {os.path.basename(p).split(".")[0]
            for p in glob.glob(os.path.join(RAW, "gdc_tsv", "*.tsv"))}
    todo = sorted(want - have)
    if not todo:
        print(f"[gdc] all {len(want)} expression files already downloaded")
        return
    os.makedirs(os.path.join(RAW, "gdc_tsv"), exist_ok=True)
    print(f"[gdc] downloading {len(todo)} files")
    for i in range(0, len(todo), 20):
        chunk = todo[i:i + 20]
        body = json.dumps({"ids": chunk}).encode()
        hdr = dict(UA, **{"Content-Type": "application/json"})
        req = urllib.request.Request(GDC_DATA, data=body, headers=hdr)
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=900) as r:
                    blob = r.read()
                break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    raise
                print(f"[gdc]   retry chunk {i}: {e}")
                time.sleep(5 * (attempt + 1))
        # The bulk endpoint returns a gzipped tar whose members are
        # <file_id>/<file_name>; a single-file request returns the file itself.
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
            for m in tf.getmembers():
                if not m.isfile() or not m.name.endswith(".tsv"):
                    continue
                fid = m.name.split("/")[0]
                with open(os.path.join(RAW, "gdc_tsv", fid + ".tsv"), "wb") as fh:
                    fh.write(tf.extractfile(m).read())
        print(f"[gdc]   {min(i + 20, len(todo))}/{len(todo)}")
        time.sleep(1)


def gdc_matrix():
    """Build gene x sample TPM matrix; returns (symbols, ensg, {gene: [tpm...]})."""
    rows = gdc_manifest()
    gdc_download(rows)
    by_id = {r["file_id"]: r for r in rows}
    per_gene = {}          # gene_id -> list of TPM, one per sample
    symbol = {}            # gene_id -> symbol
    gene_order = []
    used = []
    files = sorted(glob.glob(os.path.join(RAW, "gdc_tsv", "*.tsv")))
    for n, path in enumerate(files):
        fid = os.path.basename(path)[:-4]
        meta = by_id.get(fid)
        if meta is None:
            continue
        with open(path) as fh:
            # STAR augmented files: a few '#' lines, a header, then 4 QC rows
            # (N_unmapped etc.) before the real genes.
            hdr = None
            for line in fh:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if hdr is None:
                    hdr = parts
                    ix_id = hdr.index("gene_id")
                    ix_name = hdr.index("gene_name")
                    ix_type = hdr.index("gene_type")
                    ix_tpm = hdr.index("tpm_unstranded")
                    continue
                if parts[ix_id].startswith("N_"):
                    continue
                if parts[ix_type] != "protein_coding":
                    continue
                gid = parts[ix_id]
                try:
                    tpm = float(parts[ix_tpm])
                except (ValueError, IndexError):
                    continue
                if gid not in per_gene:
                    per_gene[gid] = []
                    symbol[gid] = parts[ix_name]
                    gene_order.append(gid)
                per_gene[gid].append(tpm)
        used.append(meta)
        if (n + 1) % 20 == 0:
            print(f"[gdc] parsed {n + 1}/{len(files)}")
    # Drop genes that are not present in every sample (annotation drift).
    nsamp = len(used)
    per_gene = {g: v for g, v in per_gene.items() if len(v) == nsamp}
    print(f"[gdc] matrix: {len(per_gene)} protein-coding genes x {nsamp} samples")
    types = {}
    for m in used:
        types[m["sample_type"]] = types.get(m["sample_type"], 0) + 1
    print(f"[gdc] sample types: {types}")
    json.dump({"samples": used, "sample_types": types},
              open(os.path.join(RAW, "gdc_samples.json"), "w"), indent=1)
    return symbol, per_gene, used


def stage_gdc():
    symbol, per_gene, used = gdc_matrix()
    # Persist a compact tumour summary so later stages need no re-parse.
    out = []
    for gid, vals in per_gene.items():
        s = sorted(vals)
        n = len(s)
        med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
        out.append({
            "gene_id": gid,
            "symbol": symbol[gid],
            "ensg": gid.split(".")[0],
            "tumour_median_tpm": round(med, 3),
            "tumour_q1_tpm": round(s[int(0.25 * (n - 1))], 3),
            "tumour_q3_tpm": round(s[int(0.75 * (n - 1))], 3),
            "tumour_max_tpm": round(s[-1], 3),
            "pct_tumours_expressing": round(
                100.0 * sum(1 for v in vals if v >= EXPR_FLOOR) / n, 1),
            "n_tumours": n,
        })
    json.dump(out, open(os.path.join(RAW, "tumour_summary.json"), "w"))
    print(f"[gdc] wrote tumour summary for {len(out)} genes")


# ---------------------------------------------------------------- stage: HPA
def hpa_bulk(query, tag):
    """One HPA search_download.php query -> list of dicts, cached as TSV."""
    path = os.path.join(RAW, f"hpa_{tag}.tsv")
    if not os.path.exists(path):
        blob = get(HPA_DL, {
            "search": query, "format": "tsv", "compress": "no",
            "columns": "g,eg,pc,scl,scml,relih,relif",
        }, timeout=600)
        open(path, "wb").write(blob)
        time.sleep(1)
    txt = open(path, encoding="utf-8", errors="replace").read()
    rdr = csv.DictReader(io.StringIO(txt), delimiter="\t")
    rows = list(rdr)
    print(f"[hpa] {tag}: {len(rows)} genes")
    return rows


def stage_hpa():
    """Build the cell-surface universe and grade how good the surface call is.

    Three HPA slices are used:
      * protein_class:Predicted membrane proteins  -- the membrane proteome
      * subcell_location:Plasma membrane           -- IF-localised to the PM
      * protein_class:CD markers                   -- curated surface markers

    HPA's immunofluorescence localisation is noisy in both directions, so a
    single boolean is misleading: CD276/B7-H3, which has ADCs and CARs in the
    clinic, is annotated by HPA only to "Vesicles" and would be thrown out.
    Instead each gene gets a surface_confidence tier:

      high   predicted membrane AND plasma membrane is a *main* HPA location,
             or a curated CD marker that is also a predicted membrane protein
      medium predicted membrane AND plasma membrane appears only as a
             secondary location (so the main location is somewhere else)
      low    predicted membrane protein with no plasma-membrane IF support

    'high' is what the headline ranking uses. 'medium' and 'low' stay in the
    output table, because real surface proteins land there (MMP14 and CDH11
    both do), and because the tier is an annotation statement, not biology.
    """
    mem = hpa_bulk("protein_class:Predicted membrane proteins", "predicted_membrane")
    pm = hpa_bulk("subcell_location:Plasma membrane", "plasma_membrane")
    cd = hpa_bulk("protein_class:CD markers", "cd_markers")
    cd_set = {(r.get("Ensembl") or "").strip() for r in cd}
    surf = {}
    for rows, flag in ((mem, "predicted_membrane"), (pm, "plasma_membrane")):
        for r in rows:
            ensg = (r.get("Ensembl") or "").strip()
            if not ensg:
                continue
            e = surf.setdefault(ensg, {
                "ensg": ensg,
                "symbol": (r.get("Gene") or "").strip(),
                "predicted_membrane": False,
                "plasma_membrane": False,
                "protein_class": (r.get("Protein class") or "").strip(),
                "subcellular_location": (r.get("Subcellular location") or "").strip(),
                "subcellular_main": (r.get("Subcellular main location") or "").strip(),
                "hpa_reliability_ih": (r.get("Reliability (IH)") or "").strip(),
                "hpa_reliability_if": (r.get("Reliability (IF)") or "").strip(),
            })
            e[flag] = True
            # keep the longest annotation strings seen across the two slices
            for k, col in (("protein_class", "Protein class"),
                           ("subcellular_location", "Subcellular location"),
                           ("subcellular_main", "Subcellular main location"),
                           ("hpa_reliability_ih", "Reliability (IH)"),
                           ("hpa_reliability_if", "Reliability (IF)")):
                v = (r.get(col) or "").strip()
                if len(v) > len(e[k]):
                    e[k] = v
    for ensg in cd_set:
        if ensg and ensg in surf:
            surf[ensg]["cd_marker"] = True
    for e in surf.values():
        e.setdefault("cd_marker", False)
        pm_main = "plasma membrane" in (e["subcellular_main"] or "").lower()
        pm_any = "plasma membrane" in (e["subcellular_location"] or "").lower()
        e["pm_main_location"] = pm_main
        e["housekeeping"] = "housekeeping" in (e["protein_class"] or "").lower()
        if e["predicted_membrane"] and (pm_main or e["cd_marker"]):
            e["surface_confidence"] = "high"
        elif e["predicted_membrane"] and pm_any:
            e["surface_confidence"] = "medium"
        elif e["predicted_membrane"]:
            e["surface_confidence"] = "low"
        else:
            e["surface_confidence"] = "low"
        # "surface-supported" = any plasma-membrane evidence at all. This is
        # the tier the headline ranking uses, because restricting to "high"
        # drops LRRC15 (HPA main location "Vesicles"), which has an ADC in
        # clinical trials -- i.e. the strict tier has false negatives.
        e["surface_strong"] = e["surface_confidence"] in ("high", "medium")
    json.dump(surf, open(os.path.join(RAW, "surface_universe.json"), "w"))
    tiers = {}
    for e in surf.values():
        tiers[e["surface_confidence"]] = tiers.get(e["surface_confidence"], 0) + 1
    print(f"[hpa] surface universe: {len(surf)} genes; confidence tiers {tiers}")


# --------------------------------------------------------------- stage: GTEx
def gtex_gencode_ids(symbols):
    """Map gene symbols to GTEx's versioned GENCODE v26 IDs."""
    cache = os.path.join(RAW, "gtex_gencode_ids.json")
    known = json.load(open(cache)) if os.path.exists(cache) else {}
    todo = [s for s in symbols if s not in known]
    for i in range(0, len(todo), 150):
        chunk = todo[i:i + 150]
        d = get_json(GTEX_GENE, {"geneId": chunk, "itemsPerPage": 1000,
                                 "datasetId": "gtex_v8"})
        for rec in d.get("data", []):
            sym = rec.get("geneSymbol")
            # Only accept an exact symbol match; GTEx search also matches synonyms.
            if sym in chunk and rec.get("gencodeId"):
                known.setdefault(sym, rec["gencodeId"])
        for s in chunk:
            known.setdefault(s, None)   # remember the misses too
        json.dump(known, open(cache, "w"))
        print(f"[gtex] id lookup {min(i + 150, len(todo))}/{len(todo)}")
        time.sleep(0.4)
    hit = sum(1 for s in symbols if known.get(s))
    print(f"[gtex] gencode IDs for {hit}/{len(symbols)} symbols")
    return known


def gtex_medians(gencode_ids):
    """GTEx v8 median TPM per tissue for a list of versioned GENCODE IDs."""
    cache = os.path.join(RAW, "gtex_medians.json")
    med = json.load(open(cache)) if os.path.exists(cache) else {}
    todo = [g for g in gencode_ids if g not in med]
    for i in range(0, len(todo), 120):
        chunk = todo[i:i + 120]
        d = get_json(GTEX_MED, {"gencodeId": chunk, "datasetId": "gtex_v8",
                                "itemsPerPage": 100000}, timeout=300)
        for rec in d.get("data", []):
            med.setdefault(rec["gencodeId"], {})[rec["tissueSiteDetailId"]] = rec["median"]
        for g in chunk:
            med.setdefault(g, {})
        json.dump(med, open(cache, "w"))
        print(f"[gtex] medians {min(i + 120, len(todo))}/{len(todo)}")
        time.sleep(0.4)
    return med


def stage_gtex():
    """Pull GTEx normals for every surface gene that clears the tumour floor."""
    tum = json.load(open(os.path.join(RAW, "tumour_summary.json")))
    surf = json.load(open(os.path.join(RAW, "surface_universe.json")))
    keep = [t for t in tum
            if t["ensg"] in surf and t["tumour_median_tpm"] >= TUMOUR_TPM_FLOOR]
    syms = sorted({t["symbol"] for t in keep} | set(CONTROLS))
    print(f"[gtex] {len(keep)} surface genes clear median TPM >= {TUMOUR_TPM_FLOOR}; "
          f"{len(syms)} symbols to look up")
    ids = gtex_gencode_ids(syms)
    wanted = sorted({v for v in ids.values() if v})
    gtex_medians(wanted)


# --------------------------------------------------------------- stage: rank
def stage_rank():
    """Join tumour, surface and normal data; score the therapeutic window."""
    tum = json.load(open(os.path.join(RAW, "tumour_summary.json")))
    surf = json.load(open(os.path.join(RAW, "surface_universe.json")))
    ids = json.load(open(os.path.join(RAW, "gtex_gencode_ids.json")))
    med = json.load(open(os.path.join(RAW, "gtex_medians.json")))

    rows = []
    for t in tum:
        ann = surf.get(t["ensg"])
        is_ctrl = t["symbol"] in CONTROLS
        if ann is None and not is_ctrl:
            continue
        if t["tumour_median_tpm"] < TUMOUR_TPM_FLOOR and not is_ctrl:
            continue
        gid = ids.get(t["symbol"])
        tis = med.get(gid or "", {}) or {}
        if not tis:
            continue
        vital = {k: v for k, v in tis.items() if k in VITAL}
        if not vital:
            continue
        max_vital = max(vital.values())
        worst = max(vital, key=vital.get)
        # GTEx ships two cultured-cell "tissues". They are not tissues and
        # must not be the headline worst normal -- but fibroblasts are the
        # most useful comparator in the whole dataset for a mesenchymal
        # tumour, so they get their own columns instead of being discarded.
        CELL_LINES = ("Cells_Cultured_fibroblasts", "Cells_EBV-transformed_lymphocytes")
        fibro = tis.get("Cells_Cultured_fibroblasts")
        lymph = tis.get("Cells_EBV-transformed_lymphocytes")
        real = {k: v for k, v in tis.items() if k not in CELL_LINES}
        max_any = max(real.values())
        worst_any = max(real, key=real.get)
        # Median across all GTEx tissues: a low value here means the gene is
        # not broadly expressed, which matters for an IV-dosed agent.
        allv = sorted(real.values())
        med_norm = allv[len(allv) // 2]

        # Therapeutic-window score. log2 fold change over the worst vital
        # tissue (pseudocount 1 TPM to keep near-zero normals from exploding),
        # weighted by how consistently the tumour expresses the gene.
        import math
        window = math.log2((t["tumour_median_tpm"] + 1.0) / (max_vital + 1.0))
        score = window * (t["pct_tumours_expressing"] / 100.0)

        rows.append({
            "symbol": t["symbol"],
            "ensg": t["ensg"],
            "tumour_median_tpm": t["tumour_median_tpm"],
            "tumour_q1_tpm": t["tumour_q1_tpm"],
            "tumour_q3_tpm": t["tumour_q3_tpm"],
            "pct_tumours_expressing": t["pct_tumours_expressing"],
            "n_tumours": t["n_tumours"],
            "max_vital_normal_tpm": round(max_vital, 2),
            "worst_vital_tissue": worst,
            "max_any_normal_tpm": round(max_any, 2),
            "worst_any_tissue": worst_any,
            "median_normal_tpm": round(med_norm, 2),
            "gtex_fibroblast_tpm": round(fibro, 2) if fibro is not None else "",
            "gtex_lymphocyte_tpm": round(lymph, 2) if lymph is not None else "",
            "log2_window_vs_vital": round(window, 2),
            "window_score": round(score, 3),
            "surface_confidence": ann["surface_confidence"] if ann else "not_annotated",
            "surface_strong": bool(ann["surface_strong"]) if ann else "",
            "predicted_membrane": bool(ann["predicted_membrane"]) if ann else "",
            "plasma_membrane_localised": bool(ann["plasma_membrane"]) if ann else "",
            "pm_is_main_location": bool(ann["pm_main_location"]) if ann else "",
            "cd_marker": bool(ann["cd_marker"]) if ann else "",
            "housekeeping": bool(ann["housekeeping"]) if ann else "",
            "hpa_subcellular_main": ann["subcellular_main"] if ann else "",
            "hpa_subcellular_location": ann["subcellular_location"] if ann else "",
            "hpa_protein_class": ann["protein_class"] if ann else "",
            "hpa_reliability_ih": ann["hpa_reliability_ih"] if ann else "",
            "hpa_reliability_if": ann["hpa_reliability_if"] if ann else "",
            "already_in_os_trials": t["symbol"] in IN_TRIALS,
            "is_control": is_ctrl,
        })

    rows.sort(key=lambda r: -r["window_score"])
    for i, r in enumerate(rows, 1):
        r["rank_overall"] = i
    # Rank among novel candidates with any plasma-membrane support.
    novel = [r for r in rows
             if not r["already_in_os_trials"] and r["surface_strong"] is True]
    for i, r in enumerate(novel, 1):
        r["rank_novel_surface"] = i
    # A shortlist that also drops HPA "housekeeping" proteins. These are the
    # broadly-expressed intracellular-machinery genes (nuclear pore, Golgi,
    # lysosomal, P450) that a membrane-prediction filter lets through and that
    # nobody would put an ADC against. Dropping them is a judgement call, so it
    # is a separate column rather than a filter on the table.
    short = [r for r in novel if not r["housekeeping"]]
    for i, r in enumerate(short, 1):
        r["rank_shortlist"] = i
    for r in rows:
        r.setdefault("rank_novel_surface", "")
        r.setdefault("rank_shortlist", "")

    cols = ["rank_shortlist", "rank_novel_surface", "rank_overall", "symbol", "ensg",
            "tumour_median_tpm", "tumour_q1_tpm", "tumour_q3_tpm",
            "pct_tumours_expressing", "n_tumours",
            "max_vital_normal_tpm", "worst_vital_tissue",
            "max_any_normal_tpm", "worst_any_tissue", "median_normal_tpm",
            "gtex_fibroblast_tpm", "gtex_lymphocyte_tpm",
            "log2_window_vs_vital", "window_score",
            "surface_confidence", "predicted_membrane", "plasma_membrane_localised",
            "pm_is_main_location", "cd_marker", "housekeeping",
            "hpa_subcellular_main", "hpa_subcellular_location",
            "hpa_protein_class", "hpa_reliability_ih", "hpa_reliability_if",
            "already_in_os_trials", "is_control"]
    json.dump(rows, open(os.path.join(RAW, "ranked.json"), "w"))
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"[rank] {len(rows)} scored genes -> {OUT_CSV}")
    print(f"[rank] {len(novel)} novel surface-supported candidates; "
          f"{len(short)} after dropping housekeeping proteins")
    print("[rank] top 15 novel:")
    for r in short[:25]:
        print(f"   {r['rank_shortlist']:>3} {r['symbol']:<12} {r['surface_confidence']:<7} "
              f"tum={r['tumour_median_tpm']:>8.1f}  {r['pct_tumours_expressing']:>5.1f}%  "
              f"vital_max={r['max_vital_normal_tpm']:>8.2f} ({r['worst_vital_tissue']})  "
              f"score={r['window_score']}")
    print("[rank] controls:")
    for r in rows:
        if r["is_control"]:
            print(f"   overall#{r['rank_overall']:<5} novel#{r['rank_novel_surface'] or '-':<5} "
                  f"{r['symbol']:<10} tum={r['tumour_median_tpm']:>8.1f} "
                  f"{r['pct_tumours_expressing']:>5.1f}% "
                  f"vital_max={r['max_vital_normal_tpm']:>8.2f} score={r['window_score']}")


# ------------------------------------------------------------ stage: context
DRUG_PAT = re.compile(
    r"\b(mab|antibody|antibodies|ADC|antibody-drug|antibody drug|bispecific|"
    r"trispecific|CAR[- ]?T|CAR[- ]?NK|chimeric antigen|immunoconjugate|"
    r"radioimmuno|nanobody|BiTE|tucatinib|-tecan|vedotin|deruxtecan|mafodotin|"
    r"govitecan|emtansine)\b", re.I)


SARC_PAT = re.compile(r"sarcoma|bone (cancer|tumou?r|neoplasm)", re.I)


def ctgov_target(symbol, aliases=()):
    """Trials that name this target, split by whether a biologic is involved.

    The target name often appears only in the brief summary, not in the title
    or the intervention name -- ABBV-085 (anti-LRRC15 ADC) is titled "A Study
    of ABBV-085 in Subjects With Advanced Solid Tumors". So the target match
    runs over title + interventions + keywords + brief summary.

    Modality language is matched separately and reported as its own count,
    rather than used as a hard filter: SOT106, an LRRC15-directed agent, is
    described to patients as "a special cancer medicine", with no modality
    word anywhere. Two counts are therefore returned -- trials naming the
    target at all, and the subset with explicit antibody/ADC/bispecific/CAR
    language -- plus a flag for whether any of them is in sarcoma.
    """
    terms = [symbol] + list(aliases)
    seen, hits = set(), []
    for term in terms:
        try:
            d = get_json(CTGOV, {
                "query.term": term, "pageSize": 300, "format": "json",
                "fields": "NCTId,BriefTitle,OverallStatus,Phase,Condition,"
                          "InterventionName,InterventionType,StudyType,"
                          "Keyword,BriefSummary",
            }, timeout=180)
        except Exception as e:  # noqa: BLE001
            print(f"[ctgov] {term}: {e}")
            continue
        for s in d.get("studies", []):
            p = s.get("protocolSection", {})
            nct = p.get("identificationModule", {}).get("nctId", "")
            if not nct or nct in seen:
                continue
            title = p.get("identificationModule", {}).get("briefTitle", "")
            arms = p.get("armsInterventionsModule", {}).get("interventions", []) or []
            inames = "; ".join(i.get("name", "") for i in arms)
            cm = p.get("conditionsModule", {})
            conds = "; ".join(cm.get("conditions", []) or [])
            kw = "; ".join(cm.get("keywords", []) or [])
            summ = p.get("descriptionModule", {}).get("briefSummary", "") or ""
            # Target match over everything the registry gives us.
            target_blob = f"{title} {inames} {kw} {summ}"
            if not re.search(rf"\b{re.escape(term)}\b", target_blob, re.I):
                continue
            # Interventional drug/biologic studies only -- drop pure imaging,
            # observational and biomarker-correlative records.
            if p.get("designModule", {}).get("studyType", "") != "INTERVENTIONAL":
                continue
            seen.add(nct)
            hits.append({
                "nct": nct, "title": title[:150],
                "status": p.get("statusModule", {}).get("overallStatus", ""),
                "phase": ";".join(p.get("designModule", {})
                                  .get("phases", []) or []),
                "conditions": conds[:120],
                "interventions": inames[:150],
                "matched_term": term,
                "biologic_language": bool(DRUG_PAT.search(f"{title} {inames} {summ}")),
                "sarcoma": bool(SARC_PAT.search(f"{conds} {kw} {title}")),
            })
        time.sleep(0.5)
    return hits


# Common alternative names so the trial search is not purely HGNC-literal.
ALIASES = {
    "CD276": ["B7-H3", "B7H3"], "ERBB2": ["HER2"], "B4GALNT1": ["GD2"],
    "GPNMB": ["osteoactivin"], "ALPL": ["alkaline phosphatase"],
    "EPHA2": ["EphA2"], "IL11RA": ["IL-11R"],
    "MMP14": ["MT1-MMP"], "LRRC15": ["LRRC15"],
    "CDH11": ["OB-cadherin"], "SDC2": ["syndecan-2"], "ITGA11": ["integrin alpha 11"],
    "TNC": ["tenascin-C"], "CD248": ["endosialin", "TEM1"],
    "PTK7": ["CCK4"], "LRP1": ["CD91"], "ENPP1": ["PC-1"],
    "ANTXR1": ["TEM8"], "COL13A1": [], "MSLN": ["mesothelin"],
    "ROR2": ["ROR2"], "FZD8": [], "PLXDC1": ["TEM7"],
}


def lit_counts():
    """Osteosarcoma literature + evidence-risk context from the repo's tables."""
    ev, risk = {}, {}
    p1 = os.path.join(ROOT, "data", "osteosarcoma_gene_evidence.csv")
    if os.path.exists(p1):
        for r in csv.DictReader(open(p1)):
            ev[r["gene"].upper()] = r
    p2 = os.path.join(ROOT, "data", "osteosarcoma_evidence_risk_genes.csv")
    if os.path.exists(p2):
        for r in csv.DictReader(open(p2)):
            risk[r["gene"].upper()] = r
    return ev, risk


def stage_context(n=10):
    """Drug landscape + literature depth for the leading candidates and controls."""
    rows = json.load(open(os.path.join(RAW, "ranked.json")))
    short = sorted((r for r in rows if r.get("rank_shortlist")),
                   key=lambda r: r["rank_shortlist"])
    picks = [r["symbol"] for r in short[:n]]
    picks += [r["symbol"] for r in rows if r["is_control"]]
    ev, risk = lit_counts()
    out = {}
    for sym in dict.fromkeys(picks):
        hits = ctgov_target(sym, ALIASES.get(sym, ()))
        bio = [h for h in hits if h["biologic_language"]]
        sarc = [h for h in hits if h["sarcoma"]]
        e = ev.get(sym.upper(), {})
        rk = risk.get(sym.upper(), {})
        out[sym] = {
            "trials_naming_target": len(hits),
            "trials_with_biologic": len(bio),
            "trials_in_sarcoma": len(sarc),
            "example_trials": (bio + [h for h in hits if not h["biologic_language"]])[:8],
            "os_papers": e.get("papers", ""),
            "os_papers_since_2021": e.get("since_2021", ""),
            "os_papers_in_vivo": e.get("in_vivo", ""),
            "os_papers_patients": e.get("patients", ""),
            "os_pct_cell_only": e.get("pct_cell_only", ""),
            "os_retracted": e.get("retracted", ""),
            "os_trials_in_repo": e.get("trials", ""),
            "evidence_risk": rk.get("risk", ""),
        }
        print(f"[ctx] {sym:<10} trials={len(hits):<4} biologic={len(bio):<4} "
              f"sarcoma={len(sarc):<3} OS papers={e.get('papers','?'):<6} "
              f"risk={rk.get('risk','-')}")
    json.dump(out, open(os.path.join(RAW, "context.json"), "w"), indent=1)
    print(f"[ctx] wrote context for {len(out)} genes")


def stage_hpa_detail(n=25):
    """Per-gene HPA JSON (protein-level evidence, IHC reliability) for the top."""
    rows = json.load(open(os.path.join(RAW, "ranked.json")))
    short = sorted((r for r in rows if r.get("rank_shortlist")),
                   key=lambda r: r["rank_shortlist"])
    picks = [(r["symbol"], r["ensg"]) for r in short[:n]]
    picks += [(r["symbol"], r["ensg"]) for r in rows if r["is_control"]]
    cache = os.path.join(RAW, "hpa_detail.json")
    det = json.load(open(cache)) if os.path.exists(cache) else {}
    for sym, ensg in dict.fromkeys(picks):
        if sym in det:
            continue
        try:
            d = json.loads(get(HPA_GENE.format(ensg=ensg), timeout=120))
        except Exception as e:  # noqa: BLE001
            print(f"[hpa] {sym}: {e}")
            continue
        det[sym] = {k: d.get(k) for k in (
            "Gene", "Ensembl", "Protein class", "Evidence", "HPA evidence",
            "UniProt evidence", "RNA tissue specificity", "RNA tissue distribution",
            "Subcellular location", "Subcellular main location",
            "Reliability (IH)", "Reliability (IF)", "Antibody",
            "Protein tissue specificity", "Protein tissue distribution",
            "RNA blood cell specificity", "Disease involvement",
            "Secretome location", "Gene description")}
        json.dump(det, open(cache, "w"), indent=1)
        time.sleep(0.4)
    print(f"[hpa] detail for {len(det)} genes")


STAGES = {
    "gdc": stage_gdc, "hpa": stage_hpa, "gtex": stage_gtex,
    "rank": stage_rank, "context": stage_context, "hpadetail": stage_hpa_detail,
}

if __name__ == "__main__":
    args = sys.argv[1:] or ["all"]
    order = ["gdc", "hpa", "gtex", "rank", "hpadetail", "context"]
    todo = order if args == ["all"] else args
    for s in todo:
        if s not in STAGES:
            sys.exit(f"unknown stage {s}; choose from {sorted(STAGES)} or 'all'")
        print(f"\n===== stage: {s} =====")
        STAGES[s]()
