# Engine cycle 7: how common is CCNE1 amplification in relapsed osteosarcoma, and which trials could those patients join?

*Pre-registered November 24, 2026, before any amplification call was read from cBioPortal and before any search of ClinicalTrials.gov for these trials. This file is committed to git before the work; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycle 6 found that osteosarcoma cell lines with more CCNE1 lean towards depending on PKMYT1, without confirming it. Drugs that block PKMYT1, and other drugs given to patients chosen for CCNE1 amplification, are in trials. Two facts decide whether this matters for patients now: how many relapsed osteosarcomas carry the amplification, and whether those trials would take them. At diagnosis, this project found CCNE1 amplified in 15 of 81 TARGET-OS tumours (18.5%).

The cohort comparison follows cycle 3's method exactly, on the same two cohorts, whose deletion data (but not amplification data) have already been seen.

## Part A: frequency at relapse

**Hypothesis H1:** CCNE1 amplification is more frequent in osteosarcoma samples from a metastasis or relapse than in samples from a primary tumour.

**Descriptive aim:** the share of metastatic or relapsed osteosarcomas with CCNE1 amplification, with a confidence interval.

**Data and method:** the same cohorts, patient selection, one-sample-per-patient rule and pooling as cycle 3 (`msk_impact_50k_2026` and `pan_origimed_2020` for the comparison; `pancan_mappyacts_2022` added for the relapse-stage frequency if it reports CCNE1; `os_target_gdc` and `pancan_pcawg_2020` shown for reference). Amplification is the study's own discrete call of +2. CCNE1 must be on the test used for a sample to count.

**Verdict rules, as in cycle 3:** supported if the pooled odds ratio is at least 1.5 with a lower 95% bound above 1; refuted if the upper bound is below 1.5; otherwise inconclusive. Underpowered if the smaller group has fewer than 100 patients.

**Checks:** the same comparison for every gene amplified in more than 3% of patients, to see whether CCNE1 stands out; tumour purity adjustment; paired patients (gained or lost between primary and later sample).

## Part B: trials

A registry count with the same rules as cycle 4.

**Search terms, fixed now:** PKMYT1; MYT1; lunresertib; RP-6306; CCNE1; cyclin E1; and the drug names BLU-222, INX-315, PF-07104091, tagtociclib, AZD8421, INCB123667, BG-68501, ARTS-021, NKT3964, NKT3447, ECI830, AVZO-021, azenosertib, ZN-c3, Debio 0123, ACR-2316, SGR-3515, APR-1051. Further drugs of the same kinds found through the general terms are added and listed.

**Which trials count:** interventional, with status recruiting, not yet recruiting, enrolling by invitation, or active but not recruiting, that either (a) test a PKMYT1 inhibitor, or (b) require CCNE1 amplification or cyclin E1 overexpression for entry to at least one group.

**Recorded for each, from the registry record:** open to osteosarcoma (yes, named; yes, by tumour-agnostic entry; no; unclear), minimum age, phase, status, sponsor type, countries, drug, and whether CCNE1 status must be shown.

**Numbers to report:** A, trials recruiting or about to that an osteosarcoma patient with CCNE1 amplification could join; B, how many of A accept under-18s; C, how many of A have a United States site.

## Predictions, recorded before the data

- P22 in `PREDICTIONS.md`: H1 is supported. Probability 15%.
- P23: at least one trial in group A accepts patients under 18. Probability 10%.

## Limits known in advance

Those of cycles 3 and 4: hospital sequencing favours advanced disease; panel amplification calls depend on tumour content; a registry is a snapshot and "any solid tumour" can hide limits. Not medical advice.

## Deviations

*None yet.*
