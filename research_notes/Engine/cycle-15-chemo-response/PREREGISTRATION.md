# Engine cycle 15: do tumours with MYC gain, CCNE1 gain or 9p21 loss respond worse to chemotherapy before surgery?

*Pre-registered November 26, 2026. Before this file was committed, only the response annotations were counted in each cohort: GSE21257 Huvos grades, GSE14827 good or poor labels, and the number of TARGET-OS patients with a recorded response. No expression value of the genes below has been read from these cohorts. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

The share of tumour killed by chemotherapy before surgery is one of the strongest known predictors of outcome in osteosarcoma (general knowledge). Cycles 3 and 7 measured how often three gene changes occur in patients:
- 9p21 loss, the region holding CDKN2A and MTAP;
- CCNE1 gain;
- MYC gain, listed in cycle 7 and the subject of prediction P2.

Targeted drugs exist or are in trials for the first two. If any of these changes goes with a poor response to standard chemotherapy, patients with it are both higher-risk and candidates for a matched drug. That would matter for trial design.

## Data

Three cohorts with pre-treatment tumour RNA and a recorded response:

| Cohort | Platform | Response measure | Patients with a known response |
|---|---|---|---|
| GSE21257 (Leiden) | Illumina | Huvos grade 1–4 | 47 (6 unknown excluded) |
| GSE14827 | Affymetrix U133 Plus 2.0 | "good" or "poor" | 27 |
| TARGET-OS | RNA sequencing | Huvos stage 1/2 or 3/4 (open clinical spreadsheet) | 35 |

**Outcome:** poor response, meaning Huvos grade 1 or 2 (less than 90% of the tumour killed), or labelled "poor".

## Measures

Copy number is not available in the two GEO cohorts, so RNA stands in for each gene change. For CCNE1, MYC and the 9p21 genes, more copies usually mean more RNA, and loss means less (general knowledge). In TARGET-OS, copy-number calls are also used as a secondary check.

- **H1:** MYC RNA, per standard deviation. More MYC, poorer response.
- **H2:** CCNE1 RNA, per standard deviation. More CCNE1, poorer response.
- **H3:** 9p21 loss score, the negative of the mean z-score of CDKN2A and MTAP RNA. Higher means more loss, poorer response.

Probes are chosen by cycle 1's rule. GSE14827 uses the GPL570 annotation.

**Effect:** the odds ratio for poor response per standard deviation, from a logistic model in each cohort, pooled by inverse-variance weighting of log odds ratios (fixed effect, with random effects reported).

## Verdict rules, fixed now (each of H1, H2 and H3, pooled)

| Verdict | Rule |
|---|---|
| **Supported** | odds ratio above 1, with the whole 95% interval above 1 |
| **Refuted** | the upper end of the 95% interval is below 1.5 |
| **Inconclusive** | anything else |

**Power, stated before looking.**
- About 109 patients, 64 with a poor response, across three small cohorts.
- Only an odds ratio of about 1.7 per standard deviation or more could be detected reliably.
- No known RNA marker of chemotherapy response is solid enough to serve as a built-in check, so none is used. This is stated as a weakness.

## Secondary analyses (reported, not used for the verdicts)

- Each cohort alone.
- **TARGET-OS copy-number calls** (amplified or deep-deleted, as in `reports/Copy-number changes and the kinase-pill biomarker.md`) against response, by Fisher's exact test. With about 35 patients this is descriptive only.
- **GSE21257, with Huvos grade as an ordered outcome** (1 to 4), by Spearman correlation.

## Predictions, recorded before the data

In `PREDICTIONS.md`:
- **P43:** H1 (MYC) is supported (20%).
- **P44:** none of H1, H2 and H3 is supported (65%).

## Deviations

Recorded November 28, 2026, after an independent check.

1. **Scale of the 9p21 score.** The script averaged the two genes' z-scores without rescaling, so the 9p21 result is per unit of the score, not per standard deviation. Per SD: 1.29 (0.85–1.97); verdict unchanged.
