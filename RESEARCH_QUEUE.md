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

## Next

| # | Question | Why it matters | How it can be tested | Status |
|---|---|---|---|---|
| 2 | Do lung metastases carry more CXCR4 and less CXCL12 than their primary tumours? | Mouse studies say CXCR4 drives lung spread; a 223-patient study found the opposite. The answer decides whether lead 14 is worth a mouse experiment. | Public RNA from paired primary tumours and lung metastases, then tissue staining with a pathology partner | Proposed, next to run |
| 3 | Are deletions of the 9p21 region (MTAP and CDKN2A) more common at relapse than at diagnosis? | If so, a drug class that targets cells missing MTAP would apply to more relapsed patients than diagnosis data suggest. | Public relapse and metastasis genomes (MSK cohorts on cBioPortal) against TARGET-OS at diagnosis | Proposed; needs access to cBioPortal |
| 4 | Do osteosarcoma cells with extra copies of CCNE1 depend on PKMYT1? | A tested link in other cancers that has not been checked in osteosarcoma cell lines by copy number. | DepMap CRISPR screens of osteosarcoma cell lines | Proposed; DepMap blocks automated access, needs a download route |

## Needs a partner

| # | Question | What is needed |
|---|---|---|
| 5 | Do extra copies of the kinase-pill target genes predict who benefits from those pills (lead 2)? | Stored tumour samples from past pill trials |
| 6 | Does the share of dead tumour in removed lung metastases predict outcome after surgery? | Archived lung-surgery slides from a bone-tumour centre |
| 7 | Did the inhaled IL-15 dog trial fail because it delayed chemotherapy? | Individual records from NCI's Comparative Oncology Program |

## Rules the engine follows

1. A question enters testing only with a written prediction and the result that would count against it.
2. The data used to test an idea are never the data it came from.
3. Every result is published, including null and inconclusive ones.
4. Ideas that survive are handed to people who can run the experiment; the engine does not claim a treatment works.
5. Not medical advice.

## Change log

- 2026-11-24: queue started. Cycle 1 (RAMP1) tested and reported inconclusive.
