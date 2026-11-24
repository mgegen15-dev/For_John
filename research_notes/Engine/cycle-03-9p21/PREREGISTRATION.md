# Engine cycle 3: is deletion of 9p21 (CDKN2A and MTAP) more common at relapse than at diagnosis?

*Pre-registered November 24, 2026, before any study on cBioPortal was listed, downloaded or examined. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

The 9p21 region holds CDKN2A, a brake on cell division, and next to it MTAP. When a tumour deletes both copies of CDKN2A it usually takes MTAP with it. Cells without MTAP depend on an enzyme called PRMT5, and a new class of drugs (MTA-cooperative PRMT5 inhibitors, and MAT2A inhibitors) is being tested in adults whose tumours have lost MTAP (general knowledge). None has an osteosarcoma trial that this project has found.

How many osteosarcoma patients could such a drug apply to? At diagnosis, in the US TARGET-OS study, 11 of 81 tumours (13.6%, 95% CI 7.8–22.7%) had a deep deletion of CDKN2A (our calculation; `reports/Copy-number changes and the kinase-pill biomarker.md`). One hospital series reported 22% (paper, full text; PMC6825534). The patients who most need new drugs are those whose disease has come back or spread. If 9p21 deletion is more common in those tumours, the diagnosis figure understates the group a PRMT5-directed drug could reach, and the case for an osteosarcoma cohort in those trials is stronger.

## Hypotheses

- **H1 (primary):** deep (two-copy) deletion of CDKN2A is more frequent in osteosarcoma samples taken from a metastasis or a relapse than in samples taken from a primary tumour.
- **Descriptive aim, no verdict:** the share of metastatic or relapsed osteosarcomas with deep deletion of MTAP, with a confidence interval. This is the number a trial sponsor would need.

## Data

**Source:** public studies on cBioPortal (www.cbioportal.org), read through its public API after this file is committed.

**Inclusion:** any public study with (a) patients whose tumour is osteosarcoma, (b) gene-level copy-number calls that include CDKN2A, and (c) a record, for each sample, of whether it came from a primary tumour or from a metastasis or recurrence.

**Exclusion:** cell lines and xenografts; studies with no sample-type record; TARGET-OS as a test cohort (it is the source of the diagnosis figure and has almost no relapse samples), though it is shown for reference.

**Overlap:** many hospital studies on cBioPortal re-publish the same patients. Patients are matched across studies by patient identifier. Each patient is counted once, taking their record from the study with the most osteosarcoma patients.

**One sample per patient.** A patient with any metastasis or relapse sample is placed in the "metastasis or relapse" group, using that sample (the most recent if several, or the first listed if dates are absent). A patient with only primary-tumour samples is placed in the "primary" group. Patients with both kinds of sample also enter a paired secondary analysis.

**What counts as a deletion:** the study's own discrete copy-number call of −2 (deep deletion) for the gene. Samples with no copy-number profile are left out.

## Primary analysis

1. Within each study (so that the test and the calling method are the same in both groups): a 2 × 2 table of CDKN2A deep deletion by group, and the odds ratio, metastasis or relapse against primary, with 0.5 added to each cell if any cell is zero.
2. Pool the log odds ratios across studies by fixed-effect inverse-variance weighting. Random-effects (DerSimonian–Laird) and I² as sensitivity. If only one study qualifies, its odds ratio and exact (Fisher) confidence interval are the result.
3. Also report the simple pooled percentages in each group, with Wilson confidence intervals.

## Verdict rules, fixed now

Let OR be the pooled odds ratio with its 95% confidence interval.

| Verdict | Rule |
|---|---|
| **Supported** | lower 95% bound > 1.0, and OR ≥ 1.5 |
| **Refuted** | upper 95% bound < 1.5: a meaningful enrichment is ruled out |
| **Inconclusive** | anything else |

**Power, stated before looking.** If 14% of primary tumours carry the deletion, detecting a rise to 25% (an odds ratio of about 2) with 80% power at two-sided α = 0.05 needs about 200 patients per group. If the smaller group holds fewer than 100 patients, the result is reported as underpowered whatever it shows.

## The main threats, stated in advance

- **Tumour content.** A deep deletion is easier to call in a sample that is mostly tumour. If metastasis samples are purer than primary samples, deletions will look more common in them for a technical reason. Where the study records tumour purity, the analysis is repeated adjusted for purity (logistic regression), and purity is compared between groups.
- **Who gets sequenced.** Hospital sequencing is offered mostly to patients with advanced disease, so the "primary" group is not the same as "all patients at diagnosis". The TARGET-OS diagnosis figure is shown alongside for that reason.
- **A check on the method.** The same comparison is run for every gene on the panel with a deep-deletion rate above 3%, to see whether CDKN2A stands out or whether deletions of all kinds are called more often in one group. If deep deletions in general are more frequent in metastasis samples, an apparent CDKN2A difference is not specific and is reported as such.

## Secondary analyses (reported, not used for the verdict)

- MTAP and CDKN2B deep deletion, the same way, where the test covers them; and how often CDKN2A deletion comes with MTAP deletion.
- Distant metastasis and local recurrence separately; lung metastases alone.
- Patients with both a primary and a later sample: how many gained or lost the deletion.
- The analysis repeated counting every sample instead of one per patient.

## What happens next under each verdict

- **Supported:** 9p21 deletion becomes a project lead, with the relapse-stage frequency as its headline number. Next: check MTAP protein loss data and PRMT5-inhibitor sensitivity in osteosarcoma cell lines without MTAP, and write to the sponsors of MTAP-selected trials about including osteosarcoma.
- **Refuted:** recorded. The descriptive MTAP-deletion share at relapse is still reported, because a steady 10 to 20% would itself be a usable number.
- **Inconclusive:** recorded with the cohort size that would decide it.

## Deviations

Recorded November 24, 2026, after listing the 553 public studies on cBioPortal and reading only their sample descriptions (tumour type, sample type, patient identifiers, which gene panel was used). No copy-number call had been read.

### 1. Studies found

**Used for the verdict (sample type recorded, copy-number calls present):**

| Study | Where | Osteosarcoma patients | Samples by type |
|---|---|---|---|
| `msk_impact_50k_2026` | Memorial Sloan Kettering, New York; hospital gene-panel test | 197 | 130 primary, 122 metastasis, 6 local recurrence |
| `pan_origimed_2020` | OrigiMed, China; commercial gene-panel test | 144 | 121 primary, 14 metastasis, 9 recurrent |

**Used for the descriptive aim only:** `pancan_mappyacts_2022` (European trial for children and young adults whose cancer had relapsed or resisted treatment; 79 osteosarcoma patients, 49 with copy-number calls). It records no sample type, so it cannot enter the comparison, but every patient had relapsed or refractory disease, so it adds to the estimate of how common the deletion is at that stage.

**Shown for reference (primary tumours only):** `os_target_gdc` and `pancan_pcawg_2020`.

**Not used:** five smaller Memorial Sloan Kettering studies (`msk_impact_2017`, `sarcoma_mskcc_2022`, `mixed_kunga_msk_2022`, `mycf_msk_2026`, `sarcoma_msk_2023`). Of their 220 distinct patient identifiers, 197 are in the large study above. The 23 others are spread over strata of two to eleven patients, too few for a within-study comparison, and eleven of them carry a different style of identifier, so they may be patients already counted. `pediatric_dkfz_2017`, `sarcoma_msk_2022`, `msk_ch_ped_2021`, `mixed_pipseq_2017`, `sarcoma_ucla_2024` and `metastatic_solid_tumors_mich_2017` have no copy-number calls. `pog570_bcgsc_2020` has five osteosarcoma samples and no primaries.

### 2. Choosing one sample per patient

Neither study gives sample dates. Memorial Sloan Kettering numbers a patient's samples in the order they were tested (T01, T02 and so on), so the highest-numbered metastasis or recurrence sample is taken as the most recent. "Local recurrence" and "recurrent" samples count as relapse.

### 3. MTAP coverage

At Memorial Sloan Kettering only the newest version of the test (505 genes) covers MTAP; the three earlier versions do not. The MTAP figures therefore use only samples run on that version, or on any test that reports MTAP. CDKN2A and CDKN2B are on every version.

### 4. Tumour purity

Both studies record the pathologist's estimate of tumour content (`TUMOR_PURITY`; spelled `TUMOR_PURTITY` in the OrigiMed study). That field is used for the purity adjustment. Samples without it are left out of the adjusted analysis only.

### 5. Prediction recorded before the data

P18 in `PREDICTIONS.md`: 30% that H1 is supported.
