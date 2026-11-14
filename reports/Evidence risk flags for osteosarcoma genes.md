# Evidence risk flags for osteosarcoma genes

*Lead 9 of the ranked leads. Built on November 14, 2026 from the literature map (18,937 non-review osteosarcoma papers published since 2010). Data: `data/osteosarcoma_evidence_risk_genes.csv` (371 genes with at least 15 papers) and `data/osteosarcoma_evidence_risk_journals.csv`. Script: `tools/paper_mill_flag.py`.*

## What this is, and what it is not

Osteosarcoma is one of the cancers most affected by "paper mills", businesses that sell formulaic, often fabricated research papers. This flag helps a researcher judge, before building on a gene, how much of its osteosarcoma literature follows the template most associated with retractions.

**It flags a pattern, not misconduct.** Many papers that fit the template are genuine. A "high" flag means "check the independent evidence before relying on this gene", not "this research is fake".

## The template

A paper fits the template when it is about a microRNA, long non-coding RNA or circular RNA **and** its abstract reports only cell-line work, with no animal, patient-tissue or dog data.

| Papers since 2010 | Count | Retracted |
|---|---|---|
| Fit the template | 1,114 (5.9%) | 96 (**8.6%**) |
| All others | 17,823 | 315 (1.8%) |

Template papers are retracted almost five times as often. Retractions also lag publication by years, so these rates will rise.

## How genes are flagged

- **High:** at least 35% of the gene's papers fit the template, or at least 8% are retracted.
- **Elevated:** at least 20% fit the template, or at least 4% are retracted.
- **Typical:** neither.

Counts: 52 genes high, 96 elevated, 223 typical.

**High-risk genes** include ROCK1 (6 retracted), ZEB1 (9), MIR34A (7), MIR21 (5), SOX2 (8), SOX4, SIRT1, DNMT1 (6 of 33), BECN1, PROM1 (7), PTK2B (7), MALAT1, HMGA2, MEG3, XIST, TUG1 and many individual microRNAs. The full list is in the data file.

## The targets that matter for trials and leads

| Target | Papers since 2010 | Template share | Retracted | With animal, patient or dog data | Flag |
|---|---|---|---|---|---|
| FAK (PTK2) | 95 | 5% | 1 | 56 | Typical |
| IL-6 | 178 | 3% | 6 | 106 | Typical |
| IL-8 (CXCL8) | 55 | 7% | 0 | 34 | Typical |
| GD2 | 39 | 0% | 0 | 32 | Typical |
| B7-H3 (CD276) | 32 | 0% | 0 | 29 | Typical |
| HER2 (ERBB2) | 76 | 0% | 1 | 67 | Typical |
| PD-L1 (CD274) | 169 | 2% | 1 | 144 | Typical |
| MDM2 | 180 | 2% | 3 | 131 | Typical |
| DKK1 | 28 | 0% | 2 | 18 | **Elevated** (2 retractions) |
| CDK6 | 43 | 19% | 2 | 27 | **Elevated** |
| mTOR | 346 | 6% | 16 | 232 | **Elevated** (16 retractions) |
| IGF1R | 89 | 9% | 5 | 67 | **Elevated** |
| Cyclin E1 (CCNE1) | 33 | 3% | 3 | 25 | **High** (3 retractions) |
| IL-6 receptor (IL6R) | 16 | 50% | 3 | 5 | **High** |
| DNMT1 | 33 | 15% | 6 | 21 | **High** |

**What this means for the ranked leads:**
- **FAK and IL-6 rest on clean literatures**, which strengthens leads 1 and 8. For IL-6, the evidence should be built on IL-6 itself, not on IL-6 receptor papers, half of which fit the template.
- **DKK1's two retractions** reinforce the close reading's caution that its evidence comes from one research lineage and needs independent replication.
- **Cyclin E1 is flagged high**, consistent with its "weak" verdict, which is why lead 10 is a cheap laboratory test, not a trial.
- **DNMT1**, the target of decitabine and azacitidine (4 osteosarcoma trials), has six retractions among 33 papers.

## Journals

Among journals with at least 30 osteosarcoma papers since 2010, the most retractions were in *Oncology Letters* (22 of 389), *BioMed Research International* (19 of 83), *Oncology Research* (16 of 77), *PLoS One* (15 of 284), *Molecular Medicine Reports* (15 of 226), *European Review for Medical and Pharmacological Sciences* (15 of 156), *OncoTargets and Therapy* (15 of 136) and *Tumor Biology* (14 of 182). Several of these journals have been the subject of large publisher-led retraction rounds, so these counts partly reflect clean-up efforts, which is a good thing.

## Limits

- Paper types are assigned by keywords in the title and abstract, so some papers are misclassified.
- Gene tags come from automated text mining.
- Retraction status is as of November 2026 and comes from PubMed.
- The thresholds are judgement calls, chosen to be easy to explain. The raw percentages are in the data file for anyone who prefers their own.
