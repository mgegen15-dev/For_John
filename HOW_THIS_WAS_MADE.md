# How this was made

*For John is an open, independent project. This page explains who built it, how, from what, how claims were checked, and what its limits are, so that anyone can judge how much to trust it.*

## Who

For John was started in November 2026 by John's older brother, who is not a scientist, after John died of osteosarcoma. The research was carried out with frontier AI models working as research assistants. The AI searched databases, read papers, wrote and ran analysis code, and drafted the reports. A person directed the work, chose what to pursue, and decided what to publish.

No scientist has reviewed this work yet. Getting that review is the project's next step.

## From what

Everything comes from public sources:

| Source | What we used | Size |
|---|---|---|
| PubMed, with NCBI PubTator3 annotations | Every paper with "osteosarcoma" in the title or abstract, with genes and chemicals tagged automatically | 33,242 papers |
| ClinicalTrials.gov | Every study listing osteosarcoma as a condition, plus posted results | 758 studies |
| Europe PMC and PubMed Central | Full texts of open-access papers, used to check claims | — |
| NIH RePORTER | NIH grants naming osteosarcoma or neuroblastoma, fiscal years 2015–2025 | about 2,700 osteosarcoma grant-years |
| NCI Genomic Data Commons (TARGET-OS) | Tumour RNA sequencing from 88 patients | — |
| GTEx v8 and the Human Protein Atlas | Normal-tissue expression and protein location | 54 tissues |
| NCBI Sequence Read Archive | Metadata on canine osteosarcoma genomes | 747 runs |

Nothing here uses private patient data.

## How claims were checked

1. **Primary sources first.** Numbers were taken from the original paper, registry record or database wherever possible, not from reviews or press coverage.
2. **Independent audit.** Before release, every headline claim in every report was re-checked by a separate review pass that did not see the original reasoning. It checked trial registries, PubMed and NIH records directly, and recomputed statistics from the data files. Of about 560 claims checked, roughly two-thirds were confirmed as written. The rest were wrong, overstated, out of date or unverifiable, and were corrected or labelled.
3. **Corrections are shown, not hidden.** Each report ends with a change log listing what changed and why. Several early conclusions were overturned by later checking, and the reports say so.
4. **Confidence labels.** Key numbers carry a label for where they came from:
   - **(registry):** posted on ClinicalTrials.gov.
   - **(paper, full text):** read in the full published paper.
   - **(paper, abstract only):** only the abstract could be read.
   - **(press release only):** no peer-reviewed source found.
   - **(our calculation):** computed by this project from the data files.

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

Every number can be rebuilt from public data with the scripts in `tools/`.

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

Three hand-curated files are not produced by a script:
- `data/drug_targets_curated.json`, the drug-to-target map;
- the published and basket-trial benchmark tables, `data/osteosarcoma_relapse_benchmarks_published.csv` and `data/osteosarcoma_relapse_benchmarks_basket.csv`.

Each row in the two benchmark tables records its source.

Live databases change, so a re-run will give slightly different numbers from the dates stamped in each report.

## Contact and corrections

Please [open an issue on GitHub](https://github.com/mgegen15-dev/For_John/issues). Corrections are as valuable as confirmations.
