# Engine cycle 10: do the gene-change weaknesses hold up when real drugs are used?

*Pre-registered November 25, 2026, before any drug-response file was downloaded or examined. Only the screen's lists of compounds and cell lines and its readme files have been read, to check which drugs and how many osteosarcoma lines it contains. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycles 5, 6, 8 and 9 used gene-knockout screens: they ask what happens when a gene is switched off in cancer cells. Patients get drugs, not knockouts, and a drug can miss its target, hit others, or fail to reach a useful dose. The PRISM Repurposing screen (Broad Institute) treated hundreds of cancer cell lines with about 1,500 compounds at eight doses. It contains a WEE1 inhibitor (adavosertib), four MDM2 inhibitors, three CDK4/6 inhibitors, an early PRMT5 inhibitor and most of the kinase pills tested in osteosarcoma. This cycle asks whether the links between gene changes and weaknesses that the knockout screens showed also appear when real drugs are used.

## Data

- **Drug responses:** PRISM Repurposing 20Q2, secondary screen, dose-response curve parameters (Figshare article 20564034, file 36794595). Measure: area under the dose-response curve (AUC); lower means the cells were killed or slowed more. Where a compound was run in both screen batches, the MTS010 batch is used, as the dataset's readme recommends; otherwise HTS002. Where a compound has more than one curve per cell line, the median AUC is used.
- **Early PRMT5 inhibitor:** EPZ015666 is only in the primary screen (one dose, 2.5 µM; file 36794580). Measure: log2 fold change in viability; lower means more killing.
- **Gene changes:** DepMap 24Q4 Public, the same files and rules as earlier cycles:
  - **TP53 altered:** damaging or hotspot mutation, or relative copy number below 0.25 (cycle 9).
  - **RB1 lost:** damaging mutation, relative copy number below 0.25, or RNA below 1 on the log2(TPM+1) scale (cycle 9).
  - **CCNE1 amplified:** relative copy number of at least 2 (cycle 6).
  - **MTAP lost:** RNA below 1 on the log2(TPM+1) scale; copy number below 0.25 where RNA is missing (cycle 5).
- **Lines:** those with a DepMap lineage annotation. Lines that the screen marks as failing identity (STR) profiling are excluded.

## Method

For each drug and gene change, the difference in AUC between lines with the change and lines without it, adjusted for lineage (lineage as fixed effects, as in cycle 8), with a 95% confidence interval. The difference is divided by the standard deviation of that drug's lineage-adjusted AUC across all lines, so effects are on one scale: **d**, in standard deviations. Negative d means lines with the change are more sensitive.

## Step 0: built-in checks (must pass before any test is read)

- **Check A (the gate):** MDM2 inhibitors work only when TP53 is intact, one of the best-established drug–gene links. Expected: lines with altered TP53 are more resistant (d above zero). **Passes** if at least three of the four MDM2 inhibitors (idasanutlin, AMG-232, nutlin-3, CGM097) have d above zero with the interval excluding zero. **If Check A fails, the cycle stops:** the data could not detect even this link, so they cannot test the others.
- **Check B (reported, not a gate):** CDK4/6 inhibitors need RB1. Expected: RB1-lost lines are more resistant. **Passes** if at least two of the three (palbociclib, ribociclib, abemaciclib) have d above zero with the interval excluding zero. Stated in advance: these drugs mostly slow cells rather than kill them, and a five-day screen may miss that, so a failure here would not by itself show the method is broken.

## Tests

| Test | Drug | Gene change | Direction expected |
|---|---|---|---|
| **T1 (primary)** | Adavosertib (WEE1 inhibitor) | CCNE1 amplified | more sensitive (d below zero) |
| **T2** | EPZ015666 (early PRMT5 inhibitor), primary screen | MTAP lost | more sensitive (d below zero) |

**Verdict rules, fixed now, for each test:**

| Verdict | Rule |
|---|---|
| **Supported** | d is −0.2 or lower and the whole 95% interval is below zero |
| **Refuted** | the whole 95% interval is above −0.2 (an effect of 0.2 standard deviations in the expected direction is ruled out) |
| **Inconclusive** | anything else |

**Power, stated before looking.** If fewer than ten lines with the gene change have data for the drug, the result is reported as underpowered whatever it shows.

**Why T2 is included.** EPZ015666 was made before the MTAP link was understood; it is not built to work better in MTAP-lost cells, and the trials in cycle 4 use newer drugs that are. T2 checks whether that difference shows in the data. A "refuted" T2 would not count against the newer drugs.

## Consistency checks (reported, not used for the verdicts)

- T1 in the other screen batch (HTS002 or MTS010, whichever was not used) and at the single dose in the primary screen. These are the same laboratory and largely the same cell lines, so agreement is a consistency check, not independent replication.
- T1 with CCNE1 RNA (continuous) in place of amplification.
- T1 without the lineage adjustment.

## Descriptive, not tests (osteosarcoma lines)

The screen has seven osteosarcoma lines (143B, G-292, HOS, MG-63, Saos-2, SJSA-1, U-2 OS). Seven lines cannot test anything, so these are reported as a resource only, labelled exploratory:

- each osteosarcoma line's gene-change status and its rank among all lines for adavosertib, the MDM2 inhibitors and the CDK4/6 inhibitors;
- the same for the kinase pills tested in osteosarcoma trials and present in the screen (cabozantinib, regorafenib, sorafenib, lenvatinib, pazopanib, sunitinib, anlotinib, apatinib). **Stated in advance:** these drugs are thought to act largely on the blood vessels that feed a tumour, which a dish of tumour cells lacks. Weak activity here would say nothing about how they work in patients, and strong activity would not show they work better than in other cancers.

## What happens next under each verdict

- **T1 supported:** the CCNE1 trials that use WEE1 inhibitors gain lab-drug support across cancers; osteosarcoma's own amplified lines (cycle 6) remain the direct test for a laboratory partner (queue row 15).
- **T1 refuted or inconclusive:** recorded; the knockout result stands alone.
- **T2:** recorded as context for why the MTAP trials use newer drugs.

## Predictions, recorded before the data

In `PREDICTIONS.md`: P29 (Check A passes, 90%), P30 (Check B passes, 50%), P31 (T1 supported, 35%), P32 (T2 supported, 10%).

## Deviations

*None yet.*
