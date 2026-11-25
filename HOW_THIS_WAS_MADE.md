# How this was made

*For John is an open, independent project. This page explains who built it, how, from what, how claims were checked, and what its limits are, so that anyone can judge how much to trust it.*

## Who

For John was started in November 2026 by John Gegen's older brother, after John died of osteosarcoma. The research was carried out with frontier AI models working as research assistants. The AI searched databases, read papers, wrote and ran analysis code, and drafted the reports. A person directed the work, chose what to pursue, and decided what to publish.

No scientist has reviewed this work yet. Getting that review is the project's next step.

## From what

Everything comes from public sources:

| Source | What we used | Size |
|---|---|---|
| PubMed, with NCBI PubTator3 annotations | Every paper with "osteosarcoma" in the title or abstract, with genes and chemicals tagged automatically | 33,242 papers |
| ClinicalTrials.gov | Every study listing osteosarcoma as a condition, plus posted results | 758 studies |
| Europe PMC and PubMed Central | Full texts of open-access papers, used to check claims | — |
| NIH RePORTER | NIH grants naming osteosarcoma or neuroblastoma, fiscal years 2015–2025 | about 2,700 osteosarcoma grant records (most only mention osteosarcoma in passing) |
| NCI Genomic Data Commons (TARGET-OS) | Tumour RNA sequencing from 88 patients; open copy-number files (SNP-array gene-level and segment calls, with whole-genome calls as a check) from 81 patients | 189 copy-number files |
| GTEx v8 and the Human Protein Atlas | Normal-tissue expression and protein location | 54 tissues |
| NCBI Sequence Read Archive | Metadata on canine osteosarcoma genomes | 747 runs |
| ChEMBL | Approved and phase 3 drugs and their protein targets, for the repurposing screen | 2,400 drugs on 1,141 genes |
| bioRxiv, medRxiv and Research Square | Preprints from June 2025 to November 2026, for the new-evidence scan (labelled as preprints) | about 100 titles screened |

Nothing here uses private patient data.

## How claims were checked

1. **Primary sources first.** Numbers were taken from the original paper, registry record or database wherever possible, not from reviews or press coverage.
2. **Separate audit passes.** Before release, every headline claim in every report was re-checked by a separate review pass that did not see the original reasoning. The eleven earlier reports were audited on November 14, 2026; the three newest (approved drugs, copy number, what's new) on November 20, 2026, when a repo-wide consistency check was also run and both sets of findings were applied (`research_notes/Audit/`). The reviewers checked trial registries, PubMed and NIH records directly, and recomputed statistics from the data files. Of about 690 claims checked across both rounds, most were confirmed as written. The rest were wrong, overstated, out of date or unverifiable, and were corrected or labelled.

   **These audits were run by AI models working as independent reviewers, not by people.** They were rigorous and caught real errors, but they are not a substitute for review by independent scientists. No person outside the project has yet checked this work. A third-party audit is welcome: start with [AUDIT_GUIDE.md](AUDIT_GUIDE.md).
3. **Corrections are shown, not hidden.** Each report ends with a change log listing what changed and why. Several early conclusions were overturned by later checking, and the reports say so.
4. **Confidence labels.** Key numbers carry a label for where they came from:
   - **(registry):** posted on ClinicalTrials.gov.
   - **(paper, full text):** read in the full published paper.
   - **(paper, abstract only):** only the abstract could be read.
   - **(press release only):** no peer-reviewed source found.
   - **(our calculation):** computed by this project from the data files.
   - **(preprint, abstract only):** only the abstract of a preprint, which has not been peer-reviewed, was read.

## What the AI did well, and where it went wrong

The AI was fast at reading and cross-referencing at a scale no single person could manage, and at writing code to count things exactly. It also made real mistakes, which checking caught:
- trial IDs that did not exist;
- a benchmark applied where it did not fit;
- a paper counted twice;
- "unpublished" trials that had in fact been published;
- genes mislabelled by automated text mining;
- drug results that turned out not to be osteosarcoma data.

The lesson built into this project is that every AI-generated claim needs checking against its source, and that some errors almost certainly remain. Please report any you find.

## Limits

- **Not peer-reviewed.** Findings are leads for researchers to test, not conclusions.
- **Abstracts, not always full texts.** Many papers could be read only as abstracts, because some publishers block automated access.
- **Automated tagging is approximate.** Paper types, gene names and trial scopes were assigned by software, with known error rates documented in each report.
- **Registries are incomplete.** ClinicalTrials.gov misses trials registered only in Europe or China, and many trials never post results.
- **English-language sources.** Chinese-language databases could not be searched, although about a fifth of new osteosarcoma trials now run in China.
- **Not medical advice.** Nothing here is a recommendation about any patient's care.

## Re-running the analyses

A frozen version of everything described here is tagged `v1.1` in git (November 25, 2026); `v1.0` (November 23) is the original review without the research engine. [DATA_MANIFEST.md](DATA_MANIFEST.md) lists every data file with its checksum and retrieval date, and `requirements.txt` pins the software versions.

Most analyses can be rebuilt from public data with the scripts in `tools/`. A few counts (registry spot checks, some PubMed searches, and the new-evidence scan) were made with one-off database queries described in the report concerned.

**Requirements:** Python 3.10 or newer, internet access, and `pandas` (only for `tools/pool_relapse_benchmarks.py`). Everything else uses the Python standard library. Run every script from the repository root.

```bash
pip install pandas
```

| Script | What it builds | Network | Time |
|---|---|---|---|
| `tools/nih_funding_tracker.py` | `data/nih_*_projects.csv` (NIH funding) | NIH RePORTER | a few minutes |
| `tools/trial_miner.py` | `data/osteosarcoma_trials.csv` (all registered trials) | ClinicalTrials.gov | about a minute |
| `tools/retag_trial_scope.py` | re-tags trial scope in the trials CSV | none | seconds |
| `tools/trial_analysis.py` | stop reasons, design trends, `data/osteosarcoma_trials_flags.csv` | none | seconds |
| `tools/trial_publication_check.py` | `data/osteosarcoma_trials_publications.csv` (publication check) | Europe PMC | a few minutes |
| `tools/pooled_controls.py` | `data/osteosarcoma_posted_outcomes.csv` (posted trial results) | ClinicalTrials.gov | a few minutes |
| `tools/pool_relapse_benchmarks.py` | the drug-class comparison table (prints it) | none | seconds |
| `tools/literature_fetch.py` | `data/literature/` (33,000 PubMed records; large, not stored in git) | PubMed, PubTator3 | about 30 minutes |
| `tools/literature_map.py` | `data/osteosarcoma_gene_evidence.csv`, `data/osteosarcoma_paper_tags.csv` | none (needs the fetch above) | about a minute |
| `tools/paper_mill_flag.py` | `data/osteosarcoma_evidence_risk_*.csv` | none (needs the map above) | seconds |
| `tools/surface_targets.py` | `data/osteosarcoma_surface_target_candidates.csv` | NCI GDC, GTEx, Human Protein Atlas | about 30 minutes (downloads 370 MB) |
| `tools/lung_metastasis_map.py` | `data/lung_metastasis_*.csv` | none (needs the literature fetch) | about a minute |
| `tools/copy_number_map.py` | `data/osteosarcoma_copy_number_frequencies.csv` and the biomarker sample-size figures (`python3 tools/copy_number_map.py all`) | NCI GDC (downloads 189 open files, about 274 MB); reuses the RNA files from `tools/surface_targets.py` | several minutes |
| `tools/repurposing_screen.py` | `data/osteosarcoma_repurposing_candidates.csv` (stages `chembl`, `build`, `pubmed`, `ctgov`, `score`) | ChEMBL, PubMed, ClinicalTrials.gov; needs the RNA summary from `tools/surface_targets.py` | about an hour (the PubMed stage takes about 40 minutes) |
| `tools/survival_analysis.py` | `data/osteosarcoma_survival_results.csv` (lead markers against survival) | NCI GDC (open TARGET-OS clinical files, stored in `data/survival_raw/`); reuses copy-number and RNA files | a few minutes |
| `tools/knowledge_graph.py` | `data/osteosarcoma_knowledge_graph_edges.csv`, `_contradictions.csv`, `_hidden_links.csv` (`fetch`, `build`, `abc`) | PubTator3, ChEMBL; needs the literature fetch | about an hour first time; under a minute from cache |
| `tools/build_explorer_data.py` | `docs/data/explorer.json` (the evidence explorer) | none | seconds |
| `tools/engine_cycle01_ramp1.py` | engine cycle 1: `data/engine/cycle01/results.csv`, `summary.json` and the forest plot | NCBI GEO (three series matrices and platform tables, about 200 MB); reuses the TARGET-OS files | a few minutes |
| `tools/engine_cycle02_fetch.sh`, then `tools/engine_cycle02_cxcr4.py` | engine cycle 2: `data/engine/cycle02/results.csv`, `summary.json`, `sample_values.csv` and two forest plots | NCBI GEO (nine datasets, about 1.5 GB) | about ten minutes to download, one minute to run |
| `tools/engine_cycle03_9p21.py` (`fetch`, then no argument) | engine cycle 3: `data/engine/cycle03/results.csv`, `summary.json`, `patients.csv` and one figure | cBioPortal public API (five studies, a few megabytes) | a minute |
| `tools/engine_cycle04_mtap_trials.py` (`fetch`, then no argument) | engine cycle 4: `data/engine/cycle04/trials.csv`, `trials_classified.csv`, `summary.json`; the hand classification is `classification.csv` | ClinicalTrials.gov (results change as the registry changes) | a minute |
| `tools/engine_cycle05_06_depmap.py` (`fetch`, then no argument) | engine cycles 5 and 6: `data/engine/cycle05/` and `cycle06/` results, line tables and two figures | DepMap public releases on Figshare (six files, about 2.5 GB) | several minutes to download, under a minute to run |
| `tools/engine_cycle07_ccne1.py` (`fetch`, then no argument) | engine cycle 7: `data/engine/cycle07/` results, patient table, trial tables and one figure | cBioPortal and ClinicalTrials.gov; needs cycle 3's fetch | a minute |
| `tools/engine_cycle08_scan.py` | engine cycle 8: `data/engine/cycle08/alterations.csv`, `hits.csv`, `summary.json` and one figure | none new; needs the downloads of cycles 3, 5 and 7 | about two minutes |
| `tools/engine_cycle09_suppressor_scan.py` (`fetch`, then no argument) | engine cycle 9: `data/engine/cycle09/` loss calls, checks, hits, patient frequencies and one figure | DepMap Figshare (three files, about 150 MB) and cBioPortal; needs the downloads of cycles 3, 5 and 8 | about a minute |
| `tools/engine_cycle10_prism.py` (`fetch`, then no argument) | engine cycle 10: `data/engine/cycle10/` results, osteosarcoma line table and one figure | PRISM Repurposing 20Q2 on Figshare (six files, about 340 MB); needs the DepMap downloads of cycles 5 and 9 | a few minutes to download, about a minute to run |
| `tools/build_site.py` | the website's report pages (`docs/reports/*.html` and the other document pages) from the Markdown sources, with `markdown-it-py` | none | seconds |

Three hand-curated files are not produced by a script:
- `data/drug_targets_curated.json`, the drug-to-target map;
- the published and basket-trial benchmark tables, `data/osteosarcoma_relapse_benchmarks_published.csv` and `data/osteosarcoma_relapse_benchmarks_basket.csv`.

Each row in the two benchmark tables records its source.

Live databases change, so a re-run will give slightly different numbers from the dates stamped in each report.

## Contact and corrections

Please [open an issue on GitHub](https://github.com/mgegen15-dev/For_John/issues). Corrections are as valuable as confirmations.
