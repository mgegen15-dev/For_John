# Research Queue

*The For John research engine, in public. Each question is something public data or a partner laboratory can answer. Each is written down with its success and failure rules before the data are examined, then tested on patients it was not built from. Results are posted whatever they show. Last updated November 24, 2026.*

## How a question moves through the queue

| Status | Meaning |
|---|---|
| **Proposed** | A question worth testing, with the data that could answer it. Not yet pre-registered. |
| **Pre-registered** | Hypothesis, data, analysis and verdict rules are committed to git before the data are examined. |
| **Replicated** | Held up in independent patients by the rules set in advance. Promoted to a lead and handed towards a laboratory test. |
| **Refuted** | A meaningful effect ruled out by the rules set in advance. Closed. |
| **Inconclusive** | Neither, by the rules set in advance. Recorded with what it would take to decide. |
| **Needs a partner** | Cannot be answered from public data; needs samples, records or a laboratory. |

The checks get stronger in this order: a prediction written down before looking, a test in independent patient data, then a laboratory experiment. Only the last one is proof.

## Tested

| # | Question | Result | Date |
|---|---|---|---|
| 1 | Does tumour RAMP1 RNA predict relapse in patients outside the study it was found in? | **Inconclusive.** Pooled hazard ratio 0.99 (0.74–1.32) across three independent cohorts, 53 events, against 2.30 in the discovery cohort. The large effect is ruled out; a small one is not. [Full result](reports/Engine%20cycle%201%20-%20does%20RAMP1%20predict%20relapse.md) | Nov 24, 2026 |
| 2 | Do lung metastases carry more CXCR4 and less CXCL12 than primary tumours? | **Inconclusive, both.** Across six datasets (29 lung metastases, 51 primaries) CXCR4 leaned higher in lung metastases, +0.43 standard deviations (−0.05 to +0.91), but the lean disappeared once immune cells were accounted for (+0.06). CXCL12 was not lower (−0.08, −0.55 to +0.39). Lead 14 gains no support. [Full result](reports/Engine%20cycle%202%20-%20do%20lung%20metastases%20carry%20more%20CXCR4.md) | Nov 24, 2026 |
| 3 | Are deletions of the 9p21 region (CDKN2A and MTAP) more common at relapse than in primary tumours? | **Inconclusive.** In two hospital cohorts (130 relapse-stage patients, 211 with primary samples) the odds ratio was 1.10 (0.59–2.06). About one in five relapsed osteosarcomas carries the CDKN2A deletion (35 of 179), and in 30 patients tested twice it matched between primary and later sample in 28. MTAP itself was measured in only 24 patients. [Full result](reports/Engine%20cycle%203%20-%20is%209p21%20deletion%20more%20common%20at%20relapse.md) | Nov 24, 2026 |

## Next

| # | Question | Why it matters | How it can be tested | Status |
|---|---|---|---|---|
| 4 | Do osteosarcoma cells with extra copies of CCNE1 depend on PKMYT1? | A tested link in other cancers that has not been checked in osteosarcoma cell lines by copy number. | DepMap CRISPR screens of osteosarcoma cell lines | Proposed; DepMap blocks automated access, needs a download route |
| 9 | Which drug trials that select patients by MTAP loss accept osteosarcoma, and from what age? (Follows cycle 3.) | If about one in seven relapsed patients lack MTAP, open trials they could join matter now. | ClinicalTrials.gov search, read against each trial's entry rules | Proposed, next to run |
| 10 | Do osteosarcoma cell lines without MTAP depend on PRMT5 more than those with it? | The drug idea rests on this and nobody has shown it in osteosarcoma. | DepMap screens, split by MTAP status | Proposed; DepMap blocks automated access, needs a download route |

## Needs a partner

| # | Question | What is needed |
|---|---|---|
| 5 | Do extra copies of the kinase-pill target genes predict who benefits from those pills (lead 2)? | Stored tumour samples from past pill trials |
| 6 | Does the share of dead tumour in removed lung metastases predict outcome after surgery? | Archived lung-surgery slides from a bone-tumour centre |
| 7 | Did the inhaled IL-15 dog trial fail because it delayed chemotherapy? | Individual records from NCI's Comparative Oncology Program |
| 8 | Is CXCR4 protein on tumour cells, not immune cells, higher in lung metastases than in the same patient's primary tumour? (Follows cycle 2, where whole-tissue RNA could not separate the two.) | Stained sections of matched primary tumours and lung metastases, scored on tumour cells only, from a bone-tumour pathology archive |
| 11 | What share of relapsed osteosarcomas have lost MTAP protein? (Follows cycle 3, where the gene was measured in only 24 patients.) | MTAP staining of stored relapse or primary samples, or the newer gene panel run on them, at a sarcoma centre |

## Rules the engine follows

1. A question enters testing only with a written prediction and the result that would count against it.
2. The data used to test an idea are never the data it came from.
3. Every result is published, including null and inconclusive ones.
4. Ideas that survive are handed to people who can run the experiment; the engine does not claim a treatment works.
5. Not medical advice.

## Change log

- 2026-11-24: queue started. Cycle 1 (RAMP1) tested and reported inconclusive.
- 2026-11-24: cycle 2 (CXCR4 and CXCL12 in lung metastases) tested and reported inconclusive. Question 8 added from its result. Questions 3 and 4 still wait on data access.
- 2026-11-24: cycle 3 (9p21 deletion at relapse) tested through cBioPortal and reported inconclusive. Questions 9, 10 and 11 added from its result.
