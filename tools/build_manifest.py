"""Write DATA_MANIFEST.md: every data file this project uses, with size,
row count, SHA-256 checksum and the date it was first added to the repo,
including the large raw downloads that are kept out of git.

An auditor can re-run this on their own copy and compare checksums to
confirm they are analysing the same data.

Usage: python3 tools/build_manifest.py   (from the repository root)"""
import hashlib, os, subprocess, datetime

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def rows(path):
    if not path.endswith((".csv", ".jsonl", ".txt")):
        return ""
    with open(path, "rb") as f:
        n = sum(1 for _ in f)
    return str(n - 1 if path.endswith(".csv") else n)

def first_added(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--follow", "--format=%as", "--", path],
                         capture_output=True, text=True).stdout.split()
    return out[-1] if out else "not in git"

def tracked(path):
    return subprocess.run(["git", "ls-files", "--error-unmatch", path], capture_output=True).returncode == 0

RAW = {
    "data/literature/osteosarcoma_pubtator.jsonl": "PubMed + PubTator3, via tools/literature_fetch.py; retrieved 2026-11-14",
    "data/copy_number_raw": "NCI GDC, TARGET-OS open copy-number files, via tools/copy_number_map.py; retrieved 2026-11-19",
    "data/surface_targets_raw": "NCI GDC TARGET-OS RNA-seq, GTEx v8, Human Protein Atlas, via tools/surface_targets.py; retrieved 2026-11-14",
    "data/repurposing_raw": "ChEMBL, ClinicalTrials.gov and PubMed caches, via tools/repurposing_screen.py; retrieved 2026-11-19",
    "data/engine/cycle01/raw": "NCBI GEO series matrices and platform tables (engine cycles 1, 14 and 15), via tools/engine_cycle01_ramp1.py; retrieved 2026-11-24",
    "data/engine/cycle02/raw": "NCBI GEO bulk, single-cell and spatial files (engine cycle 2), via tools/engine_cycle02_fetch.sh; retrieved 2026-11-24",
    "data/engine/cycle03/raw": "cBioPortal public API (engine cycles 3, 7, 8, 9), via tools/engine_cycle03_9p21.py fetch; retrieved 2026-11-24",
    "data/engine/cycle04/raw": "ClinicalTrials.gov records (engine cycle 4), via tools/engine_cycle04_mtap_trials.py fetch; retrieved 2026-11-24; not in git because records include trial staff contact details",
    "data/engine/cycle07/raw": "cBioPortal amplification calls and ClinicalTrials.gov records (engine cycle 7), via tools/engine_cycle07_ccne1.py fetch; retrieved 2026-11-24",
    "data/engine/cycle09/raw": "cBioPortal mutation calls (engine cycle 9), via tools/engine_cycle09_suppressor_scan.py fetch; retrieved 2026-11-24",
    "data/engine/prism/raw": "PRISM Repurposing 20Q2, from Figshare article 20564034 (engine cycle 10), via tools/engine_cycle10_prism.py fetch; retrieved 2026-11-25",
    "data/engine/cycle12/raw": "ClinicalTrials.gov records (engine cycles 12 and 16), via tools/engine_cycle12_teen_access.py fetch; retrieved 2026-11-26; not in git because records include trial staff contact details",
    "data/engine/cycle13/raw": "NCBI GEO GSE180303 series matrix and GPL3738 annotation (engine cycle 13), via tools/engine_cycle13_dog_inflammation.py fetch; retrieved 2026-11-26",
    "data/engine/cycle17/raw": "ClinicalTrials.gov records (engine cycle 17), via tools/engine_cycle17_fda_all_trials.py fetch; retrieved 2026-11-26; not in git because records include trial staff contact details",
    "data/engine/cycle18/raw": "ClinicalTrials.gov records (engine cycle 18), via tools/engine_cycle18_sarcoma_teen_access.py fetch; retrieved 2026-11-26; not in git because records include trial staff contact details",
    "data/engine/cycle20/raw": "NCBI GEO GSE289059 series matrix (engine cycle 20), via tools/engine_cycle20_immune_response.py fetch; retrieved 2026-11-27",
    "data/engine/depmap/raw": "DepMap 24Q4 Public and DEMETER2, from Figshare (engine cycles 5, 6, 8, 9), via tools/engine_cycle05_06_depmap.py fetch; retrieved 2026-11-24",
}

lines = ["# Data manifest", "",
         f"*Generated {datetime.date.today().isoformat()} by `tools/build_manifest.py`. Re-run it on your copy and compare the SHA-256 checksums to confirm you have the same files.*", "",
         "Files in git are the analysed outputs. The large raw downloads are not stored in git; their checksums are listed so a re-download can be compared. Live databases change, so a fresh download will usually differ slightly: the retrieval dates below say when each was taken.", "",
         "## Files in the repository", "",
         "| File | Rows | Size (KB) | First added | SHA-256 |", "|---|---|---|---|---|"]
for root, _, files in os.walk("data"):
    for fn in sorted(files):
        p = os.path.join(root, fn)
        if not tracked(p):
            continue
        lines.append(f"| `{p}` | {rows(p)} | {os.path.getsize(p)//1024} | {first_added(p)} | `{sha256(p)}` |")
lines += ["", "## Raw downloads kept out of git", "",
          "| Location | Source | Files | Size (MB) | Combined SHA-256 of file checksums |", "|---|---|---|---|---|"]
for loc, src in RAW.items():
    if not os.path.exists(loc):
        lines.append(f"| `{loc}` | {src} | not present on this machine | | |")
        continue
    paths = [loc] if os.path.isfile(loc) else sorted(os.path.join(r, f) for r, _, fs in os.walk(loc) for f in fs)
    combo = hashlib.sha256("".join(sha256(p) for p in paths).encode()).hexdigest()
    size = sum(os.path.getsize(p) for p in paths) / 1e6
    lines.append(f"| `{loc}` | {src} | {len(paths)} | {size:.0f} | `{combo}` |")
lines += ["", "**Other retrieval dates:** ClinicalTrials.gov trial list 2026-11-14 (individual records re-checked through 2026-11-20); NIH RePORTER 2026-11-14; NCBI SRA dog genome metadata 2026-11-14; Europe PMC publication checks 2026-11-14.", "", "Per-file checksums for the raw downloads are in `data/raw_checksums.txt`.", ""]
open("DATA_MANIFEST.md", "w").write("\n".join(lines))
with open("data/raw_checksums.txt", "w") as f:
    for loc in RAW:
        if os.path.exists(loc):
            paths = [loc] if os.path.isfile(loc) else sorted(os.path.join(r, fn) for r, _, fs in os.walk(loc) for fn in fs)
            for p in paths:
                f.write(f"{sha256(p)}  {p}\n")
print("wrote DATA_MANIFEST.md and data/raw_checksums.txt")
