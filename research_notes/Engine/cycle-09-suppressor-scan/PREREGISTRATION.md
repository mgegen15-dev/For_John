# Engine cycle 9: a second scan, for weaknesses that go with the tumour-suppressor genes osteosarcoma loses most often

*Pre-registered November 24, 2026, before the DepMap mutation files were downloaded and before any comparison was run. The knockout, knockdown, copy-number and expression files were downloaded for cycles 5 to 8, where only named genes were read; none of the comparisons below has been looked at. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this cycle

Cycle 8 scanned osteosarcoma's copy-number changes but could not include RB1, TP53 or ATRX, the genes the disease most often inactivates, because cell lines mostly lose them through mutations or small deletions that a copy-number rule misses. This cycle repeats the scan for five tumour-suppressor genes, defining loss in a way that catches those routes. Like cycle 8, it is a **discovery scan, not a test**.

## Genes, fixed now

RB1, TP53, ATRX, PTEN and NF1: each is reported inactivated in a meaningful share of osteosarcomas (general knowledge; this project's cohort data in cycles 3 and 8 show deep deletion of RB1 in about 10%, TP53 in 10%, PTEN in 5% and ATRX in 4% of Memorial Sloan Kettering patients, before counting mutations).

## How a cell line counts as having lost the gene

From DepMap 24Q4 Public:

- **RB1, ATRX, PTEN, NF1:** lost if any one of (a) a damaging mutation (`OmicsSomaticMutationsMatrixDamaging`, value above 0); (b) deep deletion, relative copy number below 0.25; (c) RNA below 1 on the log2(TPM+1) scale. Intact if none of these, with all three measures available.
- **TP53:** altered if (a) a damaging mutation, (b) a hotspot mutation (`OmicsSomaticMutationsMatrixHotspot`, value above 0), or (c) deep deletion. Low RNA is not used, because mutant TP53 is often made in large amounts. Intact if none, with all measures available.
- A gene is scanned only if at least 10 lines with knockout data are lost and at least 10 intact.

## The scan, as in cycle 8

For every gene in the knockout screen (Chronos, 24Q4): dependency score on lost-or-not, with tissue lineage as fixed effects. A hit needs a lineage-adjusted difference of −0.2 or lower and a false-discovery rate below 5% across every pair in this scan. The lost gene itself is excluded. Hits are re-tested in the knockdown screens (DEMETER2) with the same loss rule; a hit replicates if the knockdown difference is negative with a 95% confidence interval excluding zero, with at least 5 lost lines.

## Positive controls (checks that the loss rules work)

- **TP53:** lines with altered TP53 should depend *less* on MDM2 (a positive difference, interval excluding zero), because MDM2 matters only when TP53 works.
- **RB1:** lines without RB1 should depend *less* on CDK4, CDK6 or CCND1 (a positive difference for at least one, interval excluding zero), because those act through RB1.

If a control fails, that gene's arm is reported as "loss rule not validated" and its hits are not interpreted.

## Known pairs, listed now

Anything else is "not on the known list", which means it needs a literature check, not that it is new.

- RB1 loss: SKP2, CDK2, E2F3, CCNE1, AURKA, AURKB, CHEK1, PLK1, TTK
- PTEN loss: PIK3CB, AKT1, AKT2, AKT3, PIK3R2, MTOR
- NF1 loss: PTPN11, SOS1, KRAS, NRAS, RAF1, MAP2K1, MAPK1, SHOC2
- ATRX loss: ATR, FANCM, BLM, RMI1, RMI2, TOP3A, SMARCAL1, SLX4
- TP53 alteration: none listed for a negative difference

## What is reported

All hits with replication status; for each replicated hit, the same difference in osteosarcoma and in bone and soft-tissue sarcoma lines (described, no verdict); whether the dependency gene has an approved or late-stage drug in `data/osteosarcoma_repurposing_candidates.csv`; and, from cBioPortal, how often each of the five genes is lost in osteosarcoma patients by deep deletion or by a truncating or hotspot mutation (Memorial Sloan Kettering cohort, one sample per patient).

## Predictions, recorded before the data

- P26 in `PREDICTIONS.md`: both positive controls pass. Probability 85%.
- P27: at least one pair on the known list for RB1, PTEN, NF1 or ATRX is a replicated hit. Probability 60%.
- P28: at least one replicated hit not on the known list has a dependency gene with an approved or late-stage drug in the project's table. Probability 20%.

## Limits known in advance

As cycle 8: cell lines are not tumours, a knockout is not a drug, these are relationships across all cancers, and lineage adjustment does not remove all confounding. In addition: a damaging mutation in one copy of a gene does not always mean the gene is lost, and low RNA can reflect cell type rather than loss.

## Deviations

*None yet.*
