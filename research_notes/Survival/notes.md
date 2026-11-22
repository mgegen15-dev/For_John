# Survival working notes (22 November 2026)

Question: do the project's leads predict patient outcome in open TARGET-OS patient data? This is new evidence, not a literature summary. Script: `tools/survival_analysis.py`. Results table: `data/osteosarcoma_survival_results.csv`. Figures: `docs/figures/survival_*.svg`. Report: `reports/Do the leads predict survival.md`. Raw clinical downloads and the per-patient table: `data/survival_raw/` (open-access, de-identified TARGET data; kept in git for reproducibility, unlike the larger raw folders).

## 0. Order of work (anti-fishing record)

1. Read the three lead reports (ranked leads, copy number, surface targets) and the existing tools.
2. Downloaded the open GDC clinical data and counted which fields exist and how many patients have each (section 1). At this point we had looked only at the clinical fields on their own (for example, how many patients had metastasis at diagnosis), never at any marker against any outcome.
3. Wrote the analysis plan below (section 2), then wrote the script, then ran it. Any change made after seeing results is logged in section 5 with the reason.

## 1. Clinical data: what exists (GDC, retrieved 22 Nov 2026)

**Sources.**
- GDC `cases` endpoint, `project.project_id = TARGET-OS`, `expand=diagnoses,demographic,follow_ups,diagnoses.pathology_details`: 383 case records; 305 have a demographic and a diagnosis record (78 have neither, mostly cases with no clinical submission).
- Open clinical supplement files (GDC `files`, `data_category = Clinical`, all open): `TARGET_OS_ClinicalData_Discovery_20230709.xlsx` (100 patients), `TARGET_OS_ClinicalData_Validation_20230329.xlsx` (193 patients), plus a data dictionary (`TARGET_OS_CDE_20230329.xlsx`) and a percent-tumour supplement. All 88 molecular patients are in the Discovery file.

**Molecular cohort.** 89 patients have RNA-seq (88) or copy number (81); 80 have both. All 89 are in the GDC case records.

Field coverage, GDC cases endpoint (all 383 TARGET-OS records / the 89 molecular patients). Counts exclude null, "Not Reported" and "Unknown":

| Field | All | Molecular 89 |
|---|---|---|
| demographic.vital_status | 276 | 87 (57 alive, 30 dead, 2 not reported) |
| demographic.days_to_death | 106 | 30 (all 30 deaths) |
| diagnoses.days_to_last_follow_up | 277 | 87 |
| diagnoses.metastasis_at_diagnosis | 262 | 88 (23 "Metastasis, NOS", 65 "No Metastasis", 1 missing) |
| diagnoses.age_at_diagnosis (days) | 305 | 89 |
| demographic.sex_at_birth | 305 | 89 |
| diagnoses.year_of_diagnosis | 274 | 85 (2000–2012) |
| diagnoses.tissue_or_organ_of_origin | 282 | 88 (76 lower-limb long bone) |
| follow_ups.first_event + days_to_first_event | 257 / 256 | 85 / 86 (Relapse 39, None 32, Censored 11, Death 2, Second malignancy 1, Not reported 1) |
| follow_ups.days_to_progression | 126 | 39 |
| follow_ups.progression_or_recurrence_anatomic_site | 77 | 15 |
| diagnoses.pathology_details.necrosis_percent | 104 | 20 |
| diagnoses.laterality | 134 | 21 |

Clinical supplement (Discovery file), molecular patients: "Overall Survival Time in Days" 86, "Vital Status" 86, "Event Free Survival Time in Days" 86, "First Event" 85, "Disease at diagnosis" 88 (23 metastatic), "Histologic response" (necrosis grade at definitive surgery, Huvos 1/2 vs 3/4) 35, "Percent necrosis at Definitive Surgery" 21, "Protocol" 88 (AOST0331 24, P9851 18, IHRT 16, AOST06B1 15, AOST0121 8, P9754 3, other 4).

**Agreement between the two sources** (molecular patients). Vital status, event type and EFS time agree for every patient with both (differences under 0.001 days are rounding). Three overall-survival times differ: TARGET-40-0A4HX8 (alive; API 3050 days, supplement 1750), TARGET-40-PAUXPZ (dead; API days_to_death 724, supplement 606, which equals the API's days_to_last_follow_up) and TARGET-40-PAMJXS (dead; API 3976, supplement 3862). TARGET-40-0A4I9K has first event "Not Reported" in the API and "None" at 2257 days in the supplement.

**No histologic response for most patients.** Necrosis grade exists for 35 of the 88 (40%), and it is measured after pre-operative chemotherapy, so it is not a baseline variable. It is used only as an extra, exploratory sanity check (good responders should live longer), not as an adjustment variable.

## 2. Pre-specified analysis plan (written 22 Nov 2026, before any marker was compared with any outcome)

### 2.1 Outcomes
- **Overall survival (OS), primary outcome.** Time from diagnosis to death from any cause; alive patients censored at last follow-up. Primary source: GDC cases endpoint (dead: `demographic.days_to_death`; alive: `diagnoses.days_to_last_follow_up`). Patients with vital status not reported are excluded. Sensitivity: the same analysis using the supplement's "Overall Survival Time in Days" (affects 3 patients).
- **Event-free survival (EFS), secondary outcome.** Time to `follow_ups.days_to_first_event`; event = first event Relapse, Progression, Death or Second Malignant Neoplasm; censored = "None" or "Censored". If the API value is missing or "Not Reported", the supplement's "First Event" and "Event Free Survival Time in Days" are used.
- **Metastasis at diagnosis**, secondary outcome (binary), from `diagnoses.metastasis_at_diagnosis` ("Metastasis, NOS" = 1, "No Metastasis" = 0), falling back to the supplement's "Disease at diagnosis".
- Time zero is diagnosis. Times are analysed in days and plotted in years (days / 365.25).

### 2.2 Markers (20 pre-specified, one value per patient, from the diagnostic primary tumour)
Copy number (81 patients; calls exactly as in `tools/copy_number_map.py`, read from `data/copy_number_raw/patient_calls.csv`; P = tumour ploidy):
1. **MYC amplification** (CN ≥ 2 × P). Continuous: MYC CN / P.
2. **Any VEGFA/KDR/PDGFRA/KIT amplification** (`vegfr_any_amp`). Continuous: the highest CN / P of the four genes.
3. **CCNE1 amplification.** Continuous: CCNE1 CN / P.
4. **PTK2 (FAK) amplification.** Continuous: PTK2 CN / P.
5. **CDKN2A deep deletion** (any part of the gene at 0 copies). Continuous: CDKN2A minimum CN / P (lower = more loss).
Genome instability (81 patients; computed here from the ASCAT2 allele-specific segments, autosomes only, length-weighted):
6. **Fraction of genome altered (FGA):** share of the autosomal genome whose total copy number differs from the tumour's ploidy rounded to the nearest whole number. Binary: above vs at-or-below the cohort median. Continuous: per 10 percentage points.
7. **LOH fraction:** share of the autosomal genome with minor-allele copy number 0 and total copy number ≥ 1 (copy-neutral and copy-loss LOH). Binary: above vs at-or-below the median. Continuous: per 10 percentage points. This is the closest open-data proxy for the genome-wide LOH found prognostic in the 2025 Cell paper (PMID 39814020); it is array-based, not whole-genome.
RNA (88 patients; STAR `tpm_unstranded` from `data/surface_targets_raw/gdc_tsv/`, matched to cases through `gdc_samples.json`; value = log2(TPM + 1)). Binary: above vs at-or-below the cohort median (pre-specified). Continuous: HR per one log2 unit (a doubling of expression):
8. PTK2 (FAK) RNA; 9. DKK1; 10. LRRC15; 11. PTK7; 12. IL6; 13. IL1A; 14. IL1B; 15. CXCL8; 16. IL6R; 17. CXCR4; 18. AKT1; 19. AKT2; 20. AKT3.

Direction expected by the leads (stated in advance, used only for interpretation, all tests two-sided): high/amplified = worse OS for MYC, VEGFR-axis, CCNE1, PTK2 (CN and RNA), DKK1, IL6, IL1A, IL1B, CXCL8, IL6R, CXCR4, AKT1–3, FGA and LOH; CDKN2A deletion = worse. LRRC15 and PTK7 are surface targets: no prognostic direction is implied, and a null result does not weaken them as targets.

### 2.3 Tests, per marker (all two-sided, alpha 0.05)
- **A. OS, Cox, continuous marker, adjusted for metastasis at diagnosis.** The primary test for every marker.
- **B. OS, Kaplan–Meier with log-rank, binary marker.** Effect size: unadjusted Cox HR for the binary marker, with 95% CI; also 5-year KM survival in each group.
- **C. EFS, Cox, continuous marker, adjusted for metastasis.**
- **D. EFS, log-rank, binary marker** (HR as in B).
- **E. Metastasis at diagnosis:** Fisher exact test with odds ratio for binary markers (CN calls); Mann–Whitney U for continuous markers (RNA, FGA, LOH), with the rank-biserial effect size and medians in each group.
- **Age** is not in the main model, to keep about 10 events per variable with ~30 deaths. **Sensitivity:** test A repeated with age at diagnosis (years) added.
- **Proportional hazards check** for test A: correlation of the marker's Schoenfeld residuals with event-time rank; reported, not used to change the model.

### 2.4 Multiple testing
Benjamini–Hochberg false-discovery rate, applied **within each family of 20** (A, B, C, D, E separately; A is the primary family), and also across all 100 pre-specified tests together. Both raw and adjusted p-values are reported. A marker "passes" only if its family-adjusted q < 0.10 for test A.

### 2.5 Positive control and power
- **Positive control:** metastasis at diagnosis against OS and EFS (log-rank and Cox HR). Expected HR about 2–4. If this fails, the data or code are wrong.
- Number of events and patients is reported for every test. Power is stated with Schoenfeld's formula: for a 50/50 binary marker and ~30 deaths, the minimum detectable HR at 80% power is about 2.8; for a 15/85 marker, about 4.
- Effect sizes (HR and 95% CI) are the main result; p-values are secondary.

### 2.6 Exploratory screen (labelled exploratory, separate BH family)
Every gene in the surface-target top 25 (`rank_shortlist` 1–25 in `data/osteosarcoma_surface_target_candidates.csv`) and the 20-gene repurposing shortlist (`shortlist_rank` 1–20 in `data/osteosarcoma_repurposing_candidates.csv`), de-duplicated (genes already in 2.2 are skipped): OS, Cox, continuous log2(TPM + 1), adjusted for metastasis. BH within this family only. Any hit is a hypothesis for an independent cohort, not a finding.

### 2.7 Also exploratory
- Histologic response (Huvos 3/4 vs 1/2) against OS in the 35 patients who have it.

### 2.8 Software
KM, log-rank and Cox (Efron ties, Newton–Raphson, Wald CIs) implemented in `tools/survival_analysis.py` with numpy and scipy. Reason: `lifelines` (0.30.3) installs, but it requires pandas < 3, and this repository pins pandas 3.0.5 for `tools/pool_relapse_benchmarks.py`. lifelines is used only to cross-check our numbers in a separate virtual environment (section 4).

## 3. Cohort as analysed

- 89 molecular patients: 81 with copy number, 88 with RNA, 80 with both. 52 male, 37 female; median age 14.5 years (range 3.6–32.4).
- OS evaluable: 87 (30 deaths). Patients alive at last contact were followed for a median of 4.7 years (57 patients).
- EFS evaluable: 85 (42 events). Excluded: TARGET-40-0A4I4E and TARGET-40-PAPFLB (no vital status or event), TARGET-40-0A4I9K (first event "Not Reported" in the API and blank in the supplement, so the planned fallback did not apply), TARGET-40-0A4I0S (no event record).
- Metastasis at diagnosis known for 88 (23 metastatic); TARGET-40-0A4I0S has none in either source, so it drops out of every metastasis-adjusted model.
- Cox models with metastasis: copy-number markers n = 79 (28 deaths); RNA markers n = 85 (29 deaths). EFS: 78 (38 events) and 84 (41 events).
- Medians used for the binary splits are stored in `data/survival_raw/summary.json` (key `medians`). FGA median 0.671; LOH fraction median 0.303.
- Treatment era: diagnosed 2000–2012 on COG and other protocols (AOST0331 24, P9851 18, IHRT 16, AOST06B1 15, AOST0121 8, other 7).

## 4. Results (run 22 Nov 2026)

### 4.1 Positive control: passed
| Test | n | Events | HR (95% CI) | p | 5-year KM, yes vs no |
|---|---|---|---|---|---|
| Metastasis at diagnosis, OS | 86 | 30 (15 in 22 metastatic) | 4.83 (2.33–9.98) | 3.0 × 10⁻⁶ | 25% vs 76% |
| Metastasis at diagnosis, EFS | 85 | 42 | 3.01 (1.62–5.61) | 0.00026 | 25% vs 61% |
| Age, per +10 years, OS, adjusted for metastasis (context) | 86 | 30 | 0.95 (0.38–2.36) | 0.91 | |
| Good histologic response (exploratory), OS | 35 | 10 | 0.25 (0.05–1.18) | 0.059 | 80% vs 52% |
| Good histologic response (exploratory), EFS | 34 | 13 | 0.28 (0.08–1.04) | 0.043 | 86% vs 53% |

Both the known prognostic factors behave as expected, so the data linkage and code are working.

### 4.2 Primary family A: OS, Cox, continuous marker, adjusted for metastasis
No marker passed (smallest q = 0.20). Raw p < 0.05 for one marker only: **AKT2 RNA, HR 0.42 per doubling (0.21–0.81), p = 0.010, q = 0.20**, in the direction opposite to the lead (more AKT2 = longer survival). The AKT2 PH check gave p = 0.086, so the effect may not be constant over time. All rows are in `data/osteosarcoma_survival_results.csv`; the forest plot is `docs/figures/survival_forest_os.svg`.

### 4.3 Secondary families
- **B (OS log-rank):** smallest raw p = 0.15 (DKK1 RNA above median: HR 1.72, 0.82–3.61; 5-year OS 55% vs 73%). All q ≥ 0.95.
- **C (EFS Cox):** AKT2 RNA HR 0.44 (0.23–0.84), p = 0.013, q = 0.26; IL6 RNA HR 0.68 (0.46–1.00), p = 0.050; DKK1 RNA HR 1.14 (0.99–1.31), p = 0.072. None pass.
- **D (EFS log-rank):** LOH above median HR 0.55 (0.28–1.05), p = 0.064 (more LOH, *fewer* events); DKK1 HR 1.72 (0.92–3.21), p = 0.086. None pass.
- **E (metastasis at diagnosis):** FGA lower in metastatic tumours (rank-biserial r = −0.38, p = 0.008, q = 0.16); VEGFA/4q12 amplification: 2 of 19 amplified vs 21 of 62 not amplified were metastatic (OR 0.23, 0.02–1.14, p = 0.079). None pass.
- Across all 100 pre-specified tests, the smallest BH q is 0.44.

### 4.4 Sensitivity
- Adding age to model A changed no conclusion (AKT2 HR 0.40, p = 0.008; every other marker p > 0.1).
- Using the supplement's OS times (3 patients differ) changed no HR by more than 0.05 (largest change: IL1A RNA, 1.89 to 1.85).
- PH check: only AKT3 RNA had p < 0.05 (p = 0.002; its HR was 0.99, so there is no average effect to misread).
- Cross-check: lifelines 0.30.3 (separate venv, pandas 2.3.3) reproduced our Cox HRs and p-values to 4 decimals for MYC, VEGFA/4q12, PTK2, LOH, AKT2 and DKK1, our log-rank p-values exactly, the metastasis HR (4.826) and the 5-year KM estimate (0.7636).

### 4.5 Exploratory screen (family F, 40 genes; hypotheses only)
OS Cox, log2 RNA, adjusted for metastasis; BH within the 40. Two genes reach q < 0.10: **SOST** (sclerostin; repurposing shortlist, verdict "wrong direction") HR 1.21 per doubling (1.08–1.36), p = 0.0015, q = 0.061; **ROBO1** (surface top 25) HR 1.80 (1.21–2.68), p = 0.004, q = 0.081. Next: IFITM5 HR 1.23 (1.04–1.47), p = 0.018, q = 0.15; BMPR2 1.81 (1.10–2.96), q = 0.15; ULBP2 0.64 (0.44–0.93), q = 0.15. These need an independent cohort before anyone acts on them; nothing in family F was pre-specified as a hypothesis.

## 5. Changes after seeing results (logged, all post hoc)

1. **MYC ≥ 8 absolute copies (post hoc).** Added after seeing that the pre-specified MYC call (CN ≥ 2 × ploidy) showed nothing, because the published result we were testing (*Cancer* 2025, PMID 41199591: 3-year OS 27% vs 74%, adjusted HR 3.4, in 105 patients) used "more than 7 copies" (16% of patients). Using `MYC_high8` from `patient_calls.csv`: 23 of 79 (29%) positive, 9 of 28 deaths; HR adjusted for metastasis 1.45 (0.65–3.23); log-rank p = 0.63; 5-year OS 60% vs 61%. Labelled "post hoc" in the CSV and not counted in any BH family. Our 29% is higher than their 16%, so the definitions still differ (purity correction, platform). Whether the *Cancer* 2025 cohort overlaps with TARGET-OS is unknown to us (abstract only); if it does, this is not independent.
2. **Figure layout.** Labels on the number-at-risk table and forest plot were moved after the first render; no numbers changed.
3. `data/survival_raw/` was committed to git by the coordinator during the work (open, de-identified data); notes and docstring wording updated to say so.

## 6. Reproduce

From the repository root: `python3 tools/survival_analysis.py all` (needs the RNA cache from `tools/surface_targets.py gdc` and the copy-number cache from `tools/copy_number_map.py all`). A second full run on 22 Nov 2026 gave a byte-identical results CSV.
