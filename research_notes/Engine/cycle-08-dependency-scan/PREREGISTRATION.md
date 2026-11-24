# Engine cycle 8: a systematic scan for drug weaknesses that go with the gene losses and gains seen in osteosarcoma

*Pre-registered November 24, 2026, before the scan was run. The DepMap files it uses were downloaded for cycles 5 and 6, where only ten named genes were read; no genome-wide comparison has been looked at. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## What kind of cycle this is

Cycles 5 and 6 each tested one pair chosen by hand: a gene change (MTAP loss, CCNE1 gain) and a gene the cell then depends on. This cycle looks for such pairs systematically. It is a **discovery scan, not a test**: with tens of thousands of comparisons, some will look strong by chance. To keep that honest, the method, thresholds and a built-in replication step are fixed here, and anything the scan finds is a candidate for a later pre-registered test, not a finding.

## Step 1: which gene changes count as "seen in osteosarcoma"

From patients, not cell lines, using data already in this project:

- **Anchor genes:** genes on the Memorial Sloan Kettering test with a deep deletion in at least 3%, or an amplification in at least 5%, of the 197 osteosarcoma patients in `msk_impact_50k_2026` (one sample per patient, as in cycle 3).
- **Passenger genes lost alongside:** for each deleted anchor, any gene whose deep deletion in TARGET-OS (`os_target_gdc`) occurs in at least 4 patients and in at least half of the patients who have the anchor deleted. This is how a gene like MTAP, lost as a bystander next to CDKN2A, gets in. Requiring it to travel with an anchor keeps out harmless inherited deletions.

## Step 2: the scan, in all DepMap cell lines

- **Altered or not:** a line has a gene deleted if its relative copy number is below 0.25, and amplified if it is 2 or more (`OmicsCNGene`, 24Q4). A gene change is scanned only if at least 10 lines with knockout data carry it.
- **For every other gene in the knockout screen** (CRISPR, Chronos scores): fit dependency score on altered-or-not, adjusting for tissue lineage (lineage as fixed effects), because some gene changes and some dependencies both cluster in particular cancers. The effect is the adjusted difference, altered minus not; negative means altered lines depend on the gene more.
- **A hit:** adjusted difference of −0.2 or lower, with a false-discovery rate below 5% (Benjamini–Hochberg) across every pair tested in the whole scan.
- **Left out:** the altered gene itself for deletions (a deleted gene cannot be a dependency). For amplifications, the amplified gene itself is kept and labelled "self" (a tumour relying on its own amplified gene), and other hits on the same chromosome are labelled "same chromosome" because cutting amplified DNA can harm cells for reasons unrelated to the gene.
- **Blocks.** Genes lost or gained together give near-identical results. Hits are grouped by anchor, and each dependency gene is reported once per block with the member that gave the strongest result.

## Step 3: replication in a different kind of screen

Each hit is checked in the gene-knockdown screens (RNAi, DEMETER2), a separate technology run on a partly different set of lines. A hit **replicates** if the same lineage-adjusted difference in knockdown data is negative with a 95% confidence interval excluding zero, using at least 5 altered lines. Hits without enough knockdown data are marked "not testable", not failed.

## Step 4: what is reported

- All hits, with whether each replicated.
- For each replicated hit: the same difference in osteosarcoma lines and in bone and soft-tissue sarcoma lines (described, no verdict; cycles 5 and 6 showed these are too few to decide anything); whether the dependency gene has an approved or late-stage drug in this project's drug-target table (`data/osteosarcoma_repurposing_candidates.csv`); and how common the gene change is in osteosarcoma patients.
- **Calibration.** Pairs already established in the literature are expected among the hits and are listed in advance: 9p21 loss (CDKN2A, CDKN2B, MTAP) with PRMT5, MAT2A, WDR77 or RIOK1; CCNE1 gain with CDK2, PKMYT1 or CCNE1 itself; MDM2 gain with MDM2 and its partners (MDM4, PPM1D, USP7); CDK4 gain with CDK4 or CCND1; MYC gain with MYC or MAX; RB1 loss with SKP2, CDK2, E2F3 or CCNE1; PTEN loss with PIK3CB or AKT genes. Anything else is "not on the known list", which is not the same as new: it means it needs a literature check before anyone calls it new.

## Predictions, recorded before the scan

- P24 in `PREDICTIONS.md`: the scan recovers at least one of the known 9p21 pairs (PRMT5, MAT2A, WDR77 or RIOK1) as a replicated hit. Probability 90%. This is a check that the method works.
- P25: at least one replicated hit not on the known list involves a dependency gene with an approved or late-stage drug. Probability 35%.

## Limits known in advance

- Cell lines are not tumours, and a gene knockout is not a drug.
- The scan is across all cancers. A pair that holds in general may not hold in osteosarcoma, and the osteosarcoma lines are too few to check.
- Lineage adjustment reduces but does not remove confounding: a gene change can travel with other changes that are the real cause.
- Copy number alone defines the gene change. A deleted gene that is silenced by other means in "intact" lines weakens the comparison.

## Deviations

*None yet.*
