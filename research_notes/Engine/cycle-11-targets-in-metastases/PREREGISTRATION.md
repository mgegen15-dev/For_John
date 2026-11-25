# Engine cycle 11: do lung metastases keep the surface targets that new drugs aim at?

*Pre-registered November 25, 2026, before any of the genes below was read from these datasets. The datasets were downloaded for engine cycle 2, which read only CXCR4, CXCL12, ACKR3 and the lung and immune marker genes. This file is committed to git before the analysis; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Several new osteosarcoma drugs home in on a protein on the tumour cell surface: radioligands and antibody–drug conjugates against LRRC15, and antibody–drug conjugates and CAR-T cells against B7-H3 (gene CD276) (registry; `reports/New surface targets for osteosarcoma.md`). These trials mostly enrol patients whose disease has relapsed, and in osteosarcoma relapse is mostly in the lungs. But the evidence for the targets comes largely from diagnostic biopsies of the primary tumour, including this project's own surface screen. If a target is weaker in lung metastases, a drug aimed at it would have less to hit in the patients who actually get it.

## Data

The six datasets of engine cycle 2, which compare lung metastases with primary tumours, and its three sensitivity datasets, loaded with the same code (`tools/engine_cycle02_cxcr4.py`). Between them, 29 lung-metastasis samples and 51 primary-tumour samples:

| Dataset | Type | Lung metastases | Primaries |
|---|---|---|---|
| GSE14359 | microarray | 4 | 5 |
| GSE220538 | bulk RNA-seq | 9 | 19 |
| GSE140131 | bulk RNA-seq | 2 | 7 |
| GSE293065 | spatial, pseudobulk | 10 | 9 |
| GSE152048 | single-cell, pseudobulk | 2 | 7 |
| GSE318840 | single-cell, pseudobulk | 2 | 4 |

## Genes

- **Main tests:** LRRC15 (H1) and CD276, the B7-H3 gene (H2). Both have drug trials that include osteosarcoma.
- **Secondary set, same rules, reported as secondary:**
  - ERBB2 (HER2);
  - GPNMB;
  - B4GALNT1 (GD2 synthase, a weak stand-in for GD2, which is a sugar, not a protein);
  - PTK7, ADAM12 and IFITM5 (leads from this project's surface screen).

## Method

As in cycle 2. Within each dataset, Hedges' g for lung metastasis minus primary. The results are pooled across the six datasets (fixed effect, with random effects reported).

The primary measure is the pooled g **adjusted for the lung score and the immune score**. Bulk samples of a lung metastasis contain normal lung and immune cells, and those can dilute or add to a gene's signal.

## Verdict rules, fixed now (each gene)

| Verdict | Rule |
|---|---|
| **Maintained** | the lower 95% bound of the adjusted pooled g is above −0.5 (a drop of half a standard deviation or more is ruled out) |
| **Lower in metastases** | the adjusted pooled g is −0.5 or lower and its whole 95% interval is below zero; but if the tumour-cell-only estimate (below) is zero or above, the verdict is **Inconclusive (explained by the surroundings)** |
| **Inconclusive** | anything else |

A gene higher in metastases meets "Maintained". If fewer than 20 lung-metastasis samples have data for a gene, its result is reported as underpowered whatever it shows. Genes missing from a dataset's platform are dropped from that dataset only.

## Secondary analyses (reported, not used for the verdicts)

- The unadjusted pooled g.
- Matched pairs of a primary tumour and a lung metastasis from the same patient (GSE220538).
- **Tumour cells only,** from the single-cell datasets. Only about four lung-metastasis samples are expected here, so this is descriptive. It also reports the share of tumour cells with any reads for each gene.
- The three sensitivity datasets from cycle 2.
- **Built-in check:** the lung score is higher in lung metastases, as cycle 2 found. This was already seen, so it confirms the loading, not the method.

## What happens next under each verdict

- **Maintained:** the target's evidence from primary tumours carries to lung metastases, at RNA level. A protein stain of matched pairs (queue row 8's kind of partner) would confirm it.
- **Lower in metastases:** this would matter for the trials that select by the target. Next would be a protein check, and whether those trials test the metastasis itself before enrolment.
- **Inconclusive:** recorded, with what it would take to decide.

## Predictions, recorded before the data

In `PREDICTIONS.md`: P33, that LRRC15 is "Maintained" (45%), and P34, that CD276 is "Maintained" (60%).

## Deviations

*None yet.*
