# Repurposing screen: working notes

*Started November 19, 2026. Working notes behind `reports/Approved drugs worth testing in osteosarcoma.md`. Script: `tools/repurposing_screen.py`. Output: `data/osteosarcoma_repurposing_candidates.csv`. Raw pulls cached (git-ignored) in `data/repurposing_raw/`.*

Every candidate below is a hypothesis for laboratory testing, not a treatment recommendation, and nothing here is medical advice.

## 1. Data pulled

- **ChEMBL REST API**, November 19, 2026: 4,225 molecule records with max_phase 4 and 1,892 with max_phase 3 (salts and parents counted separately), and all 7,561 mechanism-of-action records, with the 1,518 targets they name (registry). Raw JSON: `chembl_molecules_phase4.json`, `chembl_molecules_phase3.json`, `chembl_mechanisms.json`, `chembl_targets.json`.
- Kept: mechanisms with max_phase 3 or 4 acting on a human protein target. Dropped: vaccines, replacement enzymes, collagen- or clot-digesting enzymes, fusion-protein targets (ChEMBL lists repotrectinib against "CD74-ROS1", which would credit CD74), and imaging agents.
- **Caveat found while building**: ChEMBL's `therapeutic_flag` is False for every phase 3 molecule, so it can only be used to remove diagnostics among approved drugs. ChEMBL also lags recent approvals: defactinib still reads max_phase 3 although the FDA granted accelerated approval on May 8, 2025 (registry).
- Mutant-selective drugs (a mechanism with a variant sequence, or sotorasib/adagrasib/ivosidenib/vorasidenib-type names) are not credited to the wild-type gene. Osteosarcoma rarely carries those mutations.

## 2. Joins

- **Tumour RNA**: `data/surface_targets_raw/tumour_summary.json` (TARGET-OS, 88 tumour RNA-seq files from GDC, STAR `tpm_unstranded`, protein-coding genes; built by `tools/surface_targets.py gdc`). "Expressing" = TPM >= 5 in that tumour, the same floor as the surface-target screen. Bulk RNA includes stroma and immune cells, which matters for CXCR4, CSF1R and CD4 below.
- **GTEx**: only cached for the ~2,400 surface genes in `data/surface_targets_raw/gtex_medians.json`, so the GTEx columns are blank for most genes.
- **Literature**: `data/osteosarcoma_gene_evidence.csv` (papers, in vivo, patients, dog, % cell-line-only or microRNA-type, retractions, NIH grants), `data/osteosarcoma_evidence_risk_genes.csv` (risk flag).
- **Drug literature**: PubMed count of `osteosarcoma[tiab] AND "<drug>"[tiab]` for every phase 3-4 drug with a human target (salt words stripped), run November 19, 2026. Added because gene tagging misses papers that name only the drug: ADRB2 has 7 gene-tagged papers but propranolol has its own small literature; ATP1A1 has none but digoxin/ouabain have some. Endogenous substances (adenosine, estradiol, dopamine ...) get no credit because those papers are almost never about the drug.
- **Trials, local**: every drug name and ChEMBL synonym (5+ characters) looked up as an n-gram in the title + interventions of the 758 trials in `data/osteosarcoma_trials.csv` (interventional and expanded access only), plus the hand-curated map in `data/drug_targets_curated.json`. The 154 matched names are in `data/repurposing_raw/trial_name_matches.json`; I read the list and found no false matches.
- **Trials, ClinicalTrials.gov API v2**: for the top genes (by provisional score, after hand review) the four best drugs per gene were searched with `query.cond=osteosarcoma&query.intr=<drug>`; hits were kept only when the drug name appears in the intervention list or title (the API's fuzzy match otherwise pulls in unrelated drugs). The same call with `filter.advanced=AREA[StdAge]CHILD AND AREA[StudyType]INTERVENTIONAL` gives the number of interventional trials of the drug that enrol children, used as the paediatric-experience proxy.
- openFDA and DailyMed were not reachable from this environment, so label details (age limits, boxed-warning text) are not checked against labels; boxed warnings come from ChEMBL's `black_box_warning` flag.
