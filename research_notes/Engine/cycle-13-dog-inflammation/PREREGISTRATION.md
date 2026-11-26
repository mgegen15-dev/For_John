# Engine cycle 13: in pet dogs with osteosarcoma, does tumour inflammation go with faster relapse?

*Pre-registered November 26, 2026. Before this file was committed, only the dataset's sample descriptions were read: its clinical columns, and the number of dogs and of progression times under and over a year. No gene-expression value has been read. This file is committed to git before the expression data are opened; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Lead 1 of this project proposes blocking IL-1 or IL-6 in the weeks after amputation in pet dogs with osteosarcoma, to delay lung metastasis (prediction P3; `reports/Ranked leads and research partners.md`). Lead 4 proposes FAK or DKK1 blockade in dogs.

In people, this project found that tumour RNA for these genes did not predict survival in 89 TARGET patients (`reports/Do the leads predict survival.md`). Dogs are the proposed test population, and no one in this project has looked at dog tumours.

This cycle asks whether dogs whose tumours carry more of the inflammation signal relapse sooner after standard treatment. That is an **indirect** test of lead 1. The lead is about inflammation in the body after surgery, which tumour RNA does not measure, and no result here shows whether blocking IL-1 or IL-6 would help.

## Data

GEO series GSE180303: a prospective trial in pet dogs with appendicular osteosarcoma.
- **Treatment:** amputation followed by carboplatin and/or doxorubicin.
- **Samples:** pre-treatment tumour biopsies on Affymetrix Canine Genome 2.0 arrays, two per tumour, with 109 arrays from 59 dogs.
- **Clinical data per dog:** time to progression, overall survival, age, weight, serum alkaline phosphatase, monocyte count and chemotherapy doses.

## Outcome

The dataset gives days to progression and days of survival, but no censoring flag. The rules below were fixed before any gene was read.

- **Primary:** time to progression in a Cox model.
  - A dog counts as having an event at its progression time unless its progression time equals its survival time **and** is 365 days or more. Those dogs are treated as alive and progression-free at last follow-up (censored).
  - A progression time shorter than one year that equals the survival time is counted as an event: death or progression.
  - One dog whose progression time exceeds its survival time is given its survival time, with an event.
- **Secondary:** progression or death within 365 days (yes for a progression time under 365, otherwise no), in a logistic model. This needs no censoring rule beyond assuming no dog left follow-up within the first year.

## Measures

- **Expression processing:**
  - The series-matrix values are used as given, transformed to log2 if the largest value exceeds 100.
  - The two arrays per dog are averaged.
  - Probes are mapped to genes with the platform annotation (GPL3738). Where a gene has several probes, the probe with the highest mean expression is used.
- **H1, inflammation score (main test):** the mean of the z-scores of IL6, IL1B and CXCL8 (also annotated IL8). If a gene has no probe, the score uses the others; if fewer than two remain, H1 is not tested.
- **H2:** DKK1. **H3:** PTK2 (FAK). These are secondary, for lead 4.
- **Effect:** hazard ratio per standard deviation, unadjusted. A version adjusted for log alkaline phosphatase is reported as secondary.

## Built-in check

Higher serum alkaline phosphatase is a long-known sign of shorter disease-free survival in dogs with osteosarcoma (general knowledge). Expected: a hazard ratio per standard deviation of log alkaline phosphatase above 1. The check is reported first.

- If its point estimate is not above 1, the cycle reports that the data may not reflect the expected outcome pattern, and all gene results are labelled accordingly.
- It is not a gate: alkaline phosphatase is a weaker marker in some cohorts.

## Verdict rules, fixed now (H1, H2 and H3 each)

| Verdict | Rule |
|---|---|
| **Supported** | hazard ratio above 1, with the whole 95% interval above 1 |
| **Refuted** | the upper end of the 95% interval is below 1.3 (a hazard ratio of 1.3 per standard deviation or more is ruled out) |
| **Inconclusive** | anything else |

**Power, stated before looking.** About 45 events among 59 dogs. That is enough to detect a hazard ratio of about 1.5 per standard deviation, not a smaller one.

## Secondary analyses (reported, not used for the verdicts)

- The one-year logistic model for each measure.
- Each inflammation gene alone, and IL1A.
- Excluding the 9 dogs whose progression time under a year equals their survival time (the dogs whose event is least certain).
- Adjusted for log alkaline phosphatase.
- Monocyte count, a second known prognostic sign in dogs (general knowledge), as a second check.

## Predictions, recorded before the data

In `PREDICTIONS.md`:
- **P38:** the alkaline-phosphatase check has a hazard ratio above 1 with the interval excluding 1 (50%).
- **P39:** H1 is supported (15%).
- **P40:** H2 (DKK1) is supported (15%).

## Deviations

*None yet.*
