# Engine cycle 5: do osteosarcoma cells without MTAP depend more on PRMT5?

*Pre-registered November 24, 2026, before any DepMap file was downloaded or examined. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Across hundreds of cancer cell lines, those that have lost MTAP are more easily killed by turning down PRMT5 or MAT2A (general knowledge; first shown in 2016 in gene-knockdown screens). That finding is the basis of the MTAP-selected drug trials. Nobody has reported whether it holds in osteosarcoma cell lines specifically. Cycle 3 found the deletion in about one in five relapsed osteosarcomas, so the question now has patients attached to it.

## Data

The Cancer Dependency Map (DepMap), public release files from its official Figshare repository:

- **Gene knockdown (RNAi):** the combined DEMETER2 gene-dependency scores. More negative means the cells suffer more when the gene is turned down.
- **Gene knockout (CRISPR):** Chronos gene-effect scores from the latest public release.
- **MTAP status:** gene expression from the same release. A line is "MTAP-lost" if MTAP RNA is below 1 on the log2(TPM+1) scale, and "MTAP-intact" otherwise. If expression is missing for a line, relative copy number below 0.25 counts as lost.
- **Osteosarcoma lines:** lines whose DepMap annotation gives osteosarcoma as the disease or subtype.

Knockout of PRMT5 kills almost every cell line, lost MTAP or not, so the knockdown screens are where the difference was first seen. Both are reported.

## Step 0: positive control (not a test)

Across all cell lines of every cancer type, compare MTAP-lost with MTAP-intact lines for four measures: PRMT5 knockdown, MAT2A knockdown, PRMT5 knockout, MAT2A knockout. If none of the four shows the known difference (MTAP-lost lines more dependent, 95% confidence interval excluding zero), the data cannot test the osteosarcoma question and the cycle stops there.

## Primary analysis

- **Primary measure:** PRMT5 knockdown (RNAi). If fewer than three MTAP-lost or fewer than three MTAP-intact osteosarcoma lines have that measure, the primary measure becomes MAT2A knockout (CRISPR), which has the most lines.
- **Effect:** mean dependency score in MTAP-lost osteosarcoma lines minus the mean in MTAP-intact osteosarcoma lines, with a 95% confidence interval (Welch's unequal-variance method). Negative means MTAP-lost lines are more dependent.
- **Reference effect:** the same difference across all cell lines (from Step 0), called D.

## Verdict rules, fixed now

| Verdict | Rule |
|---|---|
| **Supported** | the osteosarcoma difference is negative and its 95% interval excludes zero |
| **Refuted** | the whole 95% interval lies above half of D (the osteosarcoma effect is at most half the size seen across cancers) |
| **Inconclusive** | anything else |

**Power, stated before looking.** DepMap holds roughly fifteen osteosarcoma lines. With so few, only a large difference can reach "supported". If either group has fewer than four lines, the result is reported as underpowered whatever it shows.

## Secondary analyses (reported, not used for the verdict)

- All four measures in osteosarcoma lines.
- The same in all bone and soft-tissue sarcoma lines together.
- RIOK1 and WDR77 (PRMT5's partner), which follow the same pattern across cancers.
- MTAP status by copy number in place of expression.
- The list of osteosarcoma lines with their MTAP and CDKN2A status, as a resource for laboratories.

## What happens next under each verdict

- **Supported:** 9p21/MTAP loss becomes a project lead, with cycle 3's frequency and cycle 4's trial list attached.
- **Refuted or inconclusive:** recorded. A direct drug test in MTAP-lost and MTAP-intact osteosarcoma lines is proposed for a partner laboratory either way, because a gene screen is not the drug.

## Prediction, recorded before the data

P20 in `PREDICTIONS.md`: 25% that H is supported.

## Deviations

*None yet.*
