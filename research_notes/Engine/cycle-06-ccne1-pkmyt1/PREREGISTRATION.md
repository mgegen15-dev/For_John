# Engine cycle 6: do osteosarcoma cells with more CCNE1 depend more on PKMYT1?

*Pre-registered November 24, 2026, before any DepMap file was downloaded or examined. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Tumours with extra copies of CCNE1 (cyclin E1) push cells into division too early, and such cells have been shown to depend on the enzyme PKMYT1 to survive it; a PKMYT1 inhibitor (lunresertib) is in trials for CCNE1-amplified cancers (general knowledge; paper reported in 2022). Osteosarcoma is one of the cancers where CCNE1 gain is seen (`reports/Copy-number changes and the kinase-pill biomarker.md`). Whether osteosarcoma cells with high CCNE1 share the dependency has not been checked in the public screens.

## Data

DepMap public release files from its official Figshare repository: CRISPR knockout gene-effect scores (Chronos; more negative means the cells suffer more), gene expression, relative copy number, and the cell-line annotations. Osteosarcoma lines are those whose annotation gives osteosarcoma as the disease or subtype.

## Step 0: positive control (not a test)

Across all cell lines: (a) the slope of PKMYT1 knockout score on CCNE1 expression (log2(TPM+1)), and (b) the difference in PKMYT1 score between lines with CCNE1 amplification (relative copy number of at least 2, about four or more copies in a two-copy genome) and the rest. If neither shows the known relationship (more CCNE1, more dependency, 95% interval excluding zero), the data cannot test the osteosarcoma question and the cycle stops there.

## Primary analysis

Few osteosarcoma lines are expected to be amplified, so the primary measure is continuous.

- **Effect:** the slope from a straight-line fit of PKMYT1 knockout score on CCNE1 expression across osteosarcoma lines, with its 95% confidence interval. Negative means more CCNE1, more dependency.
- **Reference effect:** the same slope across all cell lines (from Step 0), called B.

## Verdict rules, fixed now

| Verdict | Rule |
|---|---|
| **Supported** | the osteosarcoma slope is negative and its 95% interval excludes zero |
| **Refuted** | the whole 95% interval lies above half of B (the osteosarcoma relationship is at most half as steep as across cancers) |
| **Inconclusive** | anything else |

**Power, stated before looking.** With about fifteen lines only a strong relationship can reach "supported". If fewer than ten osteosarcoma lines have both measures, the result is reported as underpowered whatever it shows.

## Secondary analyses (reported, not used for the verdict)

- Spearman rank correlation in osteosarcoma lines (less sensitive to one extreme line).
- CCNE1 copy number in place of expression; amplified against not amplified, if at least two osteosarcoma lines are amplified.
- WEE1 and CDK2 knockout scores against CCNE1, which follow related biology.
- All bone and soft-tissue sarcoma lines together.
- The list of osteosarcoma lines with their CCNE1 status and PKMYT1 score, as a resource for laboratories.

## What happens next under each verdict

- **Supported:** CCNE1 gain with PKMYT1 inhibition becomes a candidate lead; next, the frequency of CCNE1 amplification at relapse (cBioPortal) and the open lunresertib trials' entry rules.
- **Refuted or inconclusive:** recorded, with the lines a laboratory could use for a direct drug test.

## Prediction, recorded before the data

P21 in `PREDICTIONS.md`: 20% that H is supported.

## Deviations

*None yet.*
