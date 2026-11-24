# Engine cycle 2: do lung metastases carry more CXCR4 and less CXCL12 than primary tumours?

*Pre-registered November 24, 2026, before any cohort was searched for, downloaded or examined. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Lead 14 proposes CXCR4 blockers (mavorixafor, plerixafor) against lung metastasis. The idea rests on mouse work: lung tissue is rich in CXCL12, the signal CXCR4 responds to, and blocking CXCR4 cut lung metastases in mice (PMIDs 18071913, 15701832). In patients the evidence points both ways:

- CXCR4 protein was positive in 33% of primary tumours but 67% of matched lung metastases in 30 patients (PMID 16528367, abstract only).
- In 223 untreated primary tumours, strong CXCR4 and CXCL12 staining went with a *better* outcome and fewer metastases; the authors suggested that tumour cells making CXCL12 may be held in the bone (PMID 22173290, abstract only).
- In TARGET-OS, CXCR4 RNA leaned towards worse survival but not convincingly (HR 1.21, 0.79–1.87; `reports/Do the leads predict survival.md`).

If tumour cells that reach the lung carry more CXCR4, and those that stay make less CXCL12, the lung-homing model gains support in human tissue and lead 14 is worth a mouse experiment. If lung metastases carry no more CXCR4 than primaries, the lead weakens.

## Hypotheses

- **H1 (primary):** CXCR4 RNA is higher in osteosarcoma lung metastases than in primary tumours.
- **H2 (co-primary, reported with its own verdict):** CXCL12 RNA is lower in lung metastases than in primary tumours.

## The main threat, stated in advance

A piece of lung metastasis is not pure tumour. It contains lung tissue and immune cells. Normal lung makes CXCL12, and lymphocytes make a great deal of CXCR4. A bulk-RNA difference could therefore come from what surrounds the tumour rather than from the tumour cells. The plan handles this three ways, all fixed now:

1. **Lung admixture.** A lung score is computed for every sample as the mean of standardised SFTPC, SFTPB and AGER (genes made by lung air-sac cells and not by osteosarcoma). Sensitivity analysis: CXCR4 and CXCL12 differences after adjusting for the lung score (linear model within cohort).
2. **Immune admixture.** Same, with PTPRC (CD45, on all white blood cells) as the immune score.
3. **Tumour cells only.** Where public single-cell RNA data include both primary tumours and lung metastases, CXCR4 and CXCL12 are compared in cells classed as osteosarcoma cells (not immune, not lung, not other stroma), averaged per sample. This is the cleanest test and is used as a tie-breaker (see verdict rules).

## Cohorts

**Inclusion:** any public human osteosarcoma RNA dataset (microarray, bulk RNA sequencing or single-cell RNA sequencing) with tumour samples from both (a) primary tumours and (b) lung metastases, taken from patients. Cell lines, xenografts, patient-derived xenografts and organoids are excluded (mouse lung or culture would replace the human surroundings the question depends on).

**Paired versus unpaired:** datasets where the primary and the metastasis come from the same patient are analysed as pairs. Datasets with primaries and metastases from different patients are analysed as two groups. Both kinds enter the pooled analysis; the result from paired datasets alone is also reported.

**Search:** NCBI GEO for "osteosarcoma" series containing metastasis samples, run after this file is committed. Every dataset found is listed in the results with the reason it was used or not. Candidates believed relevant before the search, not yet checked: GSE14359 (primary tumours and lung metastases, Affymetrix), GSE85537, GSE152048 (single-cell, primary, recurrent and lung-metastasis lesions).

**Overlap:** a patient is counted once per comparison.

## Primary analysis

1. **Expression:** log2 scale as supplied (log2-transform if not already log). Where several probes map to a gene, use the probe with the highest mean expression across all samples in that dataset, chosen without reference to sample type.
2. **Effect size per dataset:** difference in mean expression, lung metastasis minus primary, divided by the pooled within-group standard deviation (Hedges' g, small-sample corrected). For paired datasets, the numerator is the mean within-patient difference and the standard error comes from the paired differences, so the effect stays on the same scale while using the pairing.
3. **Pooling:** fixed-effect inverse-variance meta-analysis of g across datasets; random-effects (DerSimonian–Laird) and I² as sensitivity.
4. **Single-cell datasets** enter the primary pooling as pseudobulk (all cells per sample, summed), so they are treated like bulk data there. Their tumour-cell-only analysis is reported separately.

## Verdict rules, fixed now

A meaningful difference is set at half a standard deviation (g = 0.5), a medium effect.

For **H1 (CXCR4 higher in metastases)**, with pooled g and its 95% confidence interval:

| Verdict | Rule |
|---|---|
| **Supported** | lower 95% bound > 0 and g ≥ 0.5, **and** the direction holds (g > 0) after adjusting for the lung and immune scores |
| **Refuted** | upper 95% bound < 0.5: a meaningful increase is ruled out |
| **Inconclusive** | anything else |

For **H2 (CXCL12 lower in metastases)** the same rules apply with the sign reversed (supported: upper bound < 0 and g ≤ −0.5, direction holds after adjustment; refuted: lower bound > −0.5).

**Tie-breaker.** If a bulk result is supported but the tumour-cell-only single-cell analysis points the other way (opposite sign), the verdict is downgraded to inconclusive and reported as "explained by the surroundings, not the tumour cells".

**Power, stated before looking.** To detect g = 0.5 with 80% power at two-sided α = 0.05 needs about 64 samples per group unpaired, or about 34 pairs. Small public metastasis datasets are expected to fall short. If the pooled data hold fewer than 20 lung-metastasis samples, the result is reported as underpowered whatever it shows.

## Secondary analyses (reported, not used for the verdicts)

- ACKR3 (CXCR7), the second CXCL12 receptor, which can take over when CXCR4 is blocked.
- Lung and immune scores themselves, metastasis versus primary, to show how much admixture there is.
- Each dataset separately, paired datasets alone, and without the single-cell pseudobulk.

## What happens next under each verdict

- **H1 supported:** lead 14 gains its first human-tissue support for lung homing. Next cycle: protein staining design for a pathology partner and a pre-specified mouse experiment (oral mavorixafor after primary tumour removal in K7M2 mice, measuring lung metastases and tumour T cells).
- **H1 refuted:** lead 14 is downgraded on the leads page, with the numbers.
- **Inconclusive:** recorded with the sample size that would decide it.

## Deviations

Recorded November 24, 2026, after the dataset search and after reading only sample descriptions, series designs and the papers' methods. No expression value had been read and no model had been run.

### 1. Datasets found

Two GEO searches were run (osteosarcoma with metastasis or lung terms, 186 series; osteosarcoma with single-cell terms, 52 series).

**Primary analysis: lung metastasis confirmed per sample.**

| Dataset | Type | Primary tumours | Lung metastases | Notes |
|---|---|---|---|---|
| GSE14359 | Affymetrix U133A array | 5 patients | 4 patients | Each tumour run on two arrays; the two are averaged. Different patients. |
| GSE220538 | Bulk RNA sequencing | 19 patients | 9 patients | See point 2. |
| GSE140131 | Bulk RNA sequencing | 7 patients | 2 patients | A scapula metastasis and the circulating-tumour-cell samples are excluded. |
| GSE293065 | Spatial transcriptomics (Visium) | 9 sections | 12 sections | See point 3. Local relapses, a lymph-node and a heart metastasis are excluded. |
| GSE152048 | Single-cell RNA sequencing | 7 lesions (BC2, BC3, BC5, BC6, BC16, BC21, BC22) | 2 lesions (BC10, BC17) | Lesion types from the paper (PMID 33303760); the two recurrent lesions (BC11, BC20) are excluded. |
| GSE318840 | Single-cell RNA sequencing | 4 bone tumours (2 untreated, 2 after chemotherapy) | 2 | The two soft-tissue recurrences are excluded. |

Expected lung-metastasis patients in the primary analysis: about 29 to 31, above the 20 set for adequate power.

**Sensitivity analysis only: metastasis site not recorded per sample.** The hypothesis is about the lung, and these public records label samples "metastasis" without the site. They are reported separately and do not enter the verdicts.

- GSE32981 (array; 12 primaries, 11 metastases). The paper (PMID 22518090) says most were pulmonary but at least one was skeletal and two patients had both.
- GSE237033 (bulk RNA sequencing; 7 patients with primary, recurrence and metastasis samples).
- GSE87624 (bulk RNA sequencing; 24 primaries, 9 metastases).

**Excluded:** GSE73166 (its three non-metastatic osteosarcoma samples are one patient's recurrences, so there is no primary group); GSE85537, GSE179681, GSE234998, GSE36001 and GSE74230 RNA (cultured cells, cell lines or xenografts); GSE74230 tumour samples (chromatin data, not RNA); GSE198896 (sorted immune cells only); GSE9508, GSE162454, GSE299023 and GSE342958 (primary tumours only); GSE270231 and GSE234187 (lung metastases only); GSE237070 (primary tumours, lymph nodes and adjacent tissue).

### 2. GSE220538: repeated samples and the four matched patients

Several patients have more than one sample (biopsy, resection, and for one patient two lung metastases), and four patients (06, 07, 23, 29) have both a primary tumour and a lung metastasis. Fixed now: samples are averaged within patient and tissue type so each patient counts once per group. For the primary analysis the four matched patients contribute their lung metastasis only, so the two groups are independent people (9 lung metastases, 19 primaries). The four matched pairs are reported as a paired comparison in the secondary analyses. One sample (OS-06-R(M)) carries the tissue label "metastatic tumor, lung" but a resection code used for primary tumours, and the series design counts 28 primaries and 10 metastases, which only fits if it is a primary; it is treated as patient 06's primary tumour.

### 3. Spatial transcriptomics added as a data type

The plan listed arrays, bulk and single-cell RNA sequencing. GSE293065 is spatial transcriptomics from patient tumour sections, which is RNA from the same kind of tissue, so it is included as pseudobulk (all tissue spots per section summed), like the single-cell datasets. Sections labelled A and B from the same lesion (MR10, MR11) are averaged. It gets no tumour-only analysis: a spot holds several cells, so tumour and surrounding cells cannot be separated cleanly.

### 4. How single-cell tumour cells are identified

Fixed now, before the data are read. A cell is called immune if it has any PTPRC count; endothelial if PECAM1 or VWF; lung epithelial if EPCAM, SFTPC, SFTPB or AGER; osteoclast if both ACP5 and CTSK with PTPRC or CD68. A cell is called an osteosarcoma cell if it is none of these and has counts for at least two of COL1A1, COL1A2, RUNX2, SPP1, IBSP, ALPL, SOX9, COL2A1 and ACAN (the last three so that chondroblastic tumours are not lost). This cannot tell tumour cells from normal fibroblasts or osteoblasts, which is stated as a limit. Per sample, a gene's value is its total count in those cells per million total counts in those cells, log2(x+1). Samples with fewer than 50 such cells are dropped from the tumour-cell analysis.

### 5. Predictions recorded before the data

P16 and P17 in `PREDICTIONS.md`: 40% that H1 (CXCR4 higher) is supported, 45% that H2 (CXCL12 lower) is supported.
