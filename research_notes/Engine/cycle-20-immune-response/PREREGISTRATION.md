# Engine cycle 20: do tumours with more macrophage or T-cell signal respond better to chemotherapy before surgery?

*Pre-registered November 27, 2026. Before this file was committed:*
- *For GSE289059, only the sample descriptions (sex, age, P-glycoprotein status, response) and the platform's gene list were read. No expression value was read.*
- *For the three cohorts of cycle 15 (GSE21257, GSE14827, TARGET-OS), the macrophage and T-cell genes were read for engine cycle 14, against survival, but have never been compared with chemotherapy response.*

*This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycle 14 found that a tumour macrophage gene score went with longer metastasis-free survival in the Leiden cohort where the link was first reported, but only weakly in new patients. Cycle 15 found that the share of tumour killed by chemotherapy before surgery was modestly linked to MYC. A new public cohort, GSE289059 (62 patients from the Italian ISG/OS2 trial, with response recorded), measures immune genes but not MYC, so the MYC result cannot be checked there.

This cycle asks a related question: do tumours with more immune-cell signal before treatment respond better to chemotherapy? If so, that could be one reason immune signal goes with better outcome.

## Data

| Cohort | Platform | Response | Patients |
|---|---|---|---|
| GSE289059 (ISG/OS2 trial, localized disease) | NanoString immune panel, 785 genes | "GR" (good) or "PR" (poor) | 62 (30 poor) |
| GSE21257 (Leiden) | Illumina | Huvos grade 1–2 poor, 3–4 good | 47 |
| GSE14827 | Affymetrix U133 Plus 2.0 | "good" or "poor" | 27 |
| TARGET-OS | RNA sequencing | Huvos stage 1/2 poor, 3/4 good | 35 |

- GSE289059 values are used as given in the series matrix, transformed to log2 if the largest value exceeds 100.
- The other three are processed as in cycle 15.

## Measures

- **H1, macrophage score (main):** the mean within-cohort z-score of CD163, CD14 and CD68, as in cycle 14.
- **H2, T-cell score (secondary):** the mean z-score of CD3E and CD8A.
- **Effect:** odds ratio for **poor** response per standard deviation, from a logistic model in each cohort, pooled by inverse-variance weighting (fixed effect, random effects reported). Below 1 means more immune signal, better response.

## Verdict rules, fixed now (H1 and H2, pooled across the four cohorts)

| Verdict | Rule |
|---|---|
| **Supported** | odds ratio below 1, with the whole 95% interval below 1 |
| **Refuted** | the lower end of the 95% interval is above 0.67 (a protective odds ratio of 0.67 per SD or stronger is ruled out) |
| **Inconclusive** | anything else |

## Secondary analyses (reported, not used for the verdicts)

- Each cohort alone.
- GSE289059 alone, as the one cohort not looked at before by this project.
- Each gene alone.
- In GSE289059, adjusted for P-glycoprotein status, which the dataset records and which has been studied as a marker of chemotherapy resistance (general knowledge).

## Predictions, recorded before the data

In `PREDICTIONS.md`:
- **P54:** H1 is supported (25%).
- **P55:** H2 is supported (20%).

## Deviations

Recorded November 27, 2026, after the run.

1. **Description corrected.** The header says the macrophage and T-cell genes of the three cycle 15 cohorts were read for cycle 14. In fact only GSE21257 and TARGET-OS were in cycle 14; GSE14827 was not. The method is unchanged.
