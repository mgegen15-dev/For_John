# Engine cycle 1: does tumour RAMP1 predict relapse in independent patients?

*Pre-registered November 24, 2026, before any independent cohort was downloaded or examined. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

In the TARGET-OS cohort (open NCI data), a genome-wide scan run during the project's hypothesis tournament found that tumour RAMP1 RNA at diagnosis was the single gene most strongly associated with event-free survival among 12,753 expressed genes, adjusted for metastasis at diagnosis: hazard ratio 2.29 per standard deviation, p = 7.4 × 10⁻⁷, 84 patients, 41 events (our calculation, recorded in the tournament's working notes and reproduced independently by one of its reviewers). A 2023 paper (PMID 37796823) reported high RAMP1 with poor prognosis using the same TARGET data and one GEO cohort.

RAMP1 is part of the CGRP receptor, which approved migraine drugs (gepants) block. If the association is real, it would mark a high-risk group and point to a drug class never tested in osteosarcoma. If it is a statistical fluke, the winner of a 12,753-gene scan, it should shrink towards nothing in new patients. Genome-wide winners usually shrink, so the bar below is set on that assumption.

## Hypothesis

Higher tumour RAMP1 RNA at diagnosis is associated with shorter time to relapse or metastasis in patients with osteosarcoma, independently of metastasis at diagnosis.

## Step 0: reproduce the discovery result (not a test)

Re-run the TARGET-OS association in this repository from the open GDC files, with the method below, so the discovery number is documented here. This is the source of the hypothesis and cannot confirm it.

## Cohorts

**Inclusion:** any public human osteosarcoma cohort with (a) tumour RNA measured before or at the start of treatment, (b) a time-to-event outcome per patient (metastasis-free, event-free, relapse-free or overall survival), and (c) no patients from TARGET-OS.

**Search:** NCBI GEO and EBI ArrayExpress for "osteosarcoma" series with survival or follow-up annotations, run on November 24, 2026. Every cohort found is listed in the results with the reason it was used or not. Candidates known before the search: GSE21257, GSE42352, GSE16091, GSE39058, GSE33382.

**Overlap:** where series share patients (GSE42352 is known to contain the GSE21257 biopsies), each patient is counted once, using the series with the more complete outcome data.

**GSE39058** was one of the two cohorts in the 2023 RAMP1 paper. It is independent of our discovery cohort but not of that published claim, so results are reported with and without it.

## Primary analysis

1. **Expression:** log2 scale as supplied (log2-transform if the series is not already log scale). Where several probes map to RAMP1, use the probe with the highest mean expression in that cohort, chosen before looking at outcome. Standardise to mean 0, SD 1 within each cohort.
2. **Model:** Cox proportional hazards per cohort, outcome = the cohort's primary time-to-event end point in this order of preference: metastasis-free, event-free, relapse-free, overall survival. Adjust for metastasis at diagnosis where it is recorded; otherwise unadjusted, flagged.
3. **Pooling:** fixed-effect inverse-variance meta-analysis of log hazard ratio per SD across independent cohorts. Random-effects (DerSimonian–Laird) as a sensitivity analysis, with I².

## Verdict rules, fixed now

Let HR be the pooled hazard ratio per SD from the primary analysis, with its 95% confidence interval.

| Verdict | Rule |
|---|---|
| **Replicated** | lower 95% bound of HR > 1.0, and HR ≥ 1.3 |
| **Refuted** | upper 95% bound of HR < 1.3: a clinically meaningful effect is ruled out |
| **Inconclusive** | anything else, including too few events to decide |

**Power, stated before looking.** With a standardised marker, about 48 events give 80% power to detect HR 1.5 per SD at two-sided α = 0.05, and about 114 events are needed for HR 1.3. If the independent cohorts hold fewer than 48 events in total, the result is reported as underpowered whatever it shows.

## Secondary analyses (reported, not used for the verdict)

- Overall survival, where the primary end point was not overall survival.
- CALCRL, the receptor partner RAMP1 needs to make a CGRP receptor, the same way. If RAMP1 tracks relapse but CALCRL shows nothing, the RAMP1 signal is less likely to be CGRP signalling.
- Two osteoblast-differentiation genes, SP7 and SOST, as a check on whether RAMP1 is acting as a proxy for tumour differentiation.
- Median-split Kaplan–Meier curves for display only.

## What happens next under each verdict

- **Replicated:** RAMP1 becomes a project lead. Next cycle: protein staining in tissue (which cells carry the receptor) and a pre-specified mouse experiment design for a gepant after primary tumour removal, written for a partner lab.
- **Refuted:** recorded as killed on the Research Queue and in the predictions log, with the numbers.
- **Inconclusive:** recorded with the events count, and with the size of cohort that would decide it.

## Deviations

Recorded November 24, 2026, after the cohort search and after reading only the clinical annotations, before any gene expression value was read or any model was run.

1. **Cohorts found.** The GEO search returned 200 series. Three meet all inclusion rules: GSE21257 (53 pre-chemotherapy biopsies, Leiden; metastasis-free and overall survival), GSE16091 (34 tumours; overall survival only) and GSE39055 (37 biopsies; recurrence-free survival). GSE33382 and GSE42352 contain the same Leiden patients as GSE21257 with only a 5-year yes/no metastasis label, so GSE21257 is used. GSE14827, GSE32981 and GSE9508 record metastasis only as yes/no without time, and GSE87624, GSE45275, GSE19276 and the other series have no outcome, so they are excluded. No ArrayExpress-only cohort with outcome was found.
2. **GSE21257 end point.** For metastasis-free survival, the 14 patients already metastatic at diagnosis are excluded rather than adjusted for, because metastasis at diagnosis cannot be a covariate for an outcome defined as time to metastasis. Overall survival in all 53, adjusted for metastasis at diagnosis, is reported as a secondary analysis.
3. **GSE39055 in the primary analysis.** The inclusion rule excludes only TARGET-OS patients, so GSE39055 is part of the primary pooled analysis. The result without it is reported alongside, as planned.
4. **Expected events.** 20 (GSE21257) + 15 (GSE16091) + 18 (GSE39055) = 53, above the 48 set for adequate power. Without GSE39055: 35, below it.
