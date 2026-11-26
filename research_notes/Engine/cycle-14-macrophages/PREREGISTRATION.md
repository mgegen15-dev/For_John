# Engine cycle 14: does more macrophage signal in the tumour go with a better outcome, in patients outside the study that found it?

*Pre-registered November 26, 2026, before any of the genes below was read from these cohorts. The cohorts were downloaded for engine cycle 1 and for the TARGET survival analysis, which read other genes. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

A 2011 study of 53 osteosarcoma biopsies from Leiden (GEO GSE21257) reported that tumours with more macrophage genes (CD14, CD163) and more macrophages on staining had fewer metastases (paper, abstract; Buddingh et al., Clinical Cancer Research 2011). That finding is part of the rationale for macrophage-activating treatment. Mifamurtide, for example, is approved in Europe for non-metastatic osteosarcoma (registry; `reports/Osteosarcoma research landscape and gaps.md`).

Cycle 1 showed how a striking single-cohort result can fail in new patients. This cycle asks whether the macrophage signal predicts a better outcome in three cohorts that played no part in the original finding.

## Data

- **Check (reproduction, not a test):** GSE21257, the cohort the finding came from. Metastasis-free survival in patients without metastasis at diagnosis, as in cycle 1.
- **Independent test cohorts:**
  - GSE16091 (overall survival);
  - GSE39055 (recurrence-free survival);
  - TARGET-OS (event-free survival, adjusted for metastasis at diagnosis, as in cycle 1's discovery analysis).
- The end points, patient selection and probe choice are those of cycle 1 (`tools/engine_cycle01_ramp1.py`). GSE42352 is not used, because it contains the GSE21257 biopsies.

## Measures

- **H1, macrophage score (main test):** the mean of the within-cohort z-scores of CD163, CD14 and CD68. If a gene is missing from a platform, the score uses the others.
- **H2, T-cell score (secondary):** the mean z-score of CD3E and CD8A.
- **Effect:** hazard ratio per standard deviation of the score, from a Cox model in each cohort, pooled across the three independent cohorts (fixed effect, with random effects reported). Below 1 means a better outcome with more of the signal.

## Verdict rules, fixed now (pooled independent cohorts)

| Verdict | Rule |
|---|---|
| **Supported** | hazard ratio below 1, with the whole 95% interval below 1 |
| **Refuted** | the lower end of the 95% interval is above 0.77 (a protective effect of 0.77 per standard deviation or stronger, the mirror of 1.3, is ruled out) |
| **Inconclusive** | anything else |

**Power, stated before looking.** About 50 events across the independent GEO cohorts plus about 40 in TARGET-OS. That is enough to detect a hazard ratio of about 0.7 per standard deviation.

**The reproduction check** is reported first:
- If GSE21257 does not show a hazard ratio below 1, the gene score may not capture what the original study measured. The independent results are then labelled accordingly.
- It is not a gate.

## Secondary analyses (reported, not used for the verdict)

- Each gene alone.
- Overall survival in GSE21257 adjusted for metastasis at diagnosis.
- Pooling without TARGET-OS (GEO cohorts only).
- The T-cell score (H2), with the same rules.

## Caveats stated in advance

- Gene RNA from whole tumour pieces is a rough stand-in for counting macrophages on stained sections.
- A link with outcome would not show that activating macrophages helps.
- Nothing here is about any patient's treatment.

## Predictions, recorded before the data

In `PREDICTIONS.md`:
- **P41:** the GSE21257 reproduction shows a hazard ratio below 1 with the interval excluding 1 (60%).
- **P42:** H1 is supported in the pooled independent cohorts (30%).

## Deviations

*None yet.*
