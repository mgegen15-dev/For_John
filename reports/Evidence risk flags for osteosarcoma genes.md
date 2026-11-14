# Evidence risk flags for osteosarcoma genes

*Built November 13–14, 2026 from the literature map: 18,937 non-review osteosarcoma papers published since 2010. Data: `data/osteosarcoma_evidence_risk_genes.csv` (362 genes with at least 15 papers since 2010) and `data/osteosarcoma_evidence_risk_journals.csv`. Script: `tools/paper_mill_flag.py`, which reads the paper tags written by `tools/literature_map.py`.*

## Summary

Some genes' osteosarcoma literature leans heavily on a kind of paper, the microRNA, lncRNA or circRNA study, that has been retracted far more often than the rest. This flag shows, for each gene, how much of its literature is of that kind and how much has already been retracted, so a researcher can decide how hard to check before building on it. Since 2010, 8.7% of microRNA-type osteosarcoma papers have been retracted, against 1.0% of other papers, an 8.4-fold difference. A flag is a prompt to look for independent animal, patient or dog evidence. It is not a finding of misconduct. Many genes are flagged on only two or three retractions, so a single paper can change a flag.

**How to read the labels.** Key numbers carry one of these tags:
- **(registry)**: read directly from an official registry or database: PubMed's own listings (for example, which papers are retracted), ClinicalTrials.gov, NIH RePORTER.
- **(paper, full text)**: we read the full paper.
- **(paper, abstract only)**: we read only the abstract.
- **(press release only)**: the only source is a press release or an institution's web listing.
- **(our calculation)**: we computed it from this repository's data files.

## What this is, and what it is not

Osteosarcoma's literature is heavily affected by formulaic papers of the kind associated with "paper mills", businesses that sell often fabricated research papers. This flag helps a researcher judge, before relying on a gene, how much of its osteosarcoma literature is of the type most often retracted.

**It flags a pattern, not misconduct.** Many microRNA-type papers are genuine. A "high" flag means "check the independent evidence before relying on this gene". It does not mean "this research is fake".

## The comparison that carries the signal

A paper is **microRNA-type** when its title or abstract is about a microRNA, long non-coding RNA or circular RNA (for example "miR-", "lncRNA", "circRNA", "sponge"). Retraction status comes from PubMed (registry).

| Non-review papers since 2010 | Papers | Retracted | Share retracted (95% CI) |
|---|---|---|---|
| microRNA-type | 2,816 (14.9%) | 244 | **8.7%** (7.7–9.8%) |
| All other papers | 16,121 | 167 | 1.0% (0.9–1.2%) |

*Our calculation. Ratio 8.4-fold. These 411 retracted research papers are part of the 418 retracted osteosarcoma papers PubMed lists. The other seven are 3 reviews and 4 papers from before 2010.*

Retractions lag publication by years, so these rates will rise, most of all for recent papers. Restricted to 2010–2019, the rates are 12.6% against 1.2%, a 10.5-fold difference (our calculation).

**Why we no longer use a narrower "template".** An earlier version flagged only microRNA-type papers whose abstract did not mention animals, patients or dogs. That narrowing did not help. Since 2010 those papers were retracted at 8.6% (96 of 1,115) and the other microRNA-type papers at 8.7% (148 of 1,701) (our calculation). Its "patients" test was also unreliable in both directions. Any abstract that says "osteosarcoma patients" escaped it, and papers reporting "osteosarcoma tissues" did not count as having patient data. Restricted to 2010–2019 the narrow group was retracted somewhat more often (14.7% against 11.4%), but most of the signal is "microRNA-type or not". The flag now uses that simpler definition.

## How genes are flagged

For each gene with at least 15 non-review papers since 2010:

- **High:** at least 35% of its papers are microRNA-type, or at least 8% are retracted.
- **Elevated:** at least 20% are microRNA-type, or at least 4% are retracted.
- **Typical:** neither.

Counts: **75 genes high, 100 elevated, 187 typical** (our calculation). For **52 of these genes the flag would change with one retraction fewer**, which is flagged in the data file (`flag_changes_with_one_retraction_fewer`), together with a 95% interval for each gene's retracted share. The thresholds are judgement calls, chosen to be easy to explain.

**High-risk genes with at least three retractions** include TUG1, MIR34A, MIR21, MALAT1, SOX4, ZEB1, ZEB2, ROCK1, TIMP2, SIRT1, EZH2, PTEN (10 retracted of 157), DNMT1 (6 of 33), BMI1, NOTCH1, CDH2, SMAD2, SOX2 (8 of 83), FASN, BECN1, PROM1 (7 of 73), RAC1, CCNB1, CDK1 and ANXA5 (14 of 132), plus many individual microRNAs (our calculation). The full list is in the data file.

## The targets that matter for trials and leads

| Target | Papers since 2010 | microRNA-type share | Retracted | With animal, patient or dog data | Flag |
|---|---|---|---|---|---|
| FAK (PTK2) | 95 | 7% | 1 | 56 | Typical |
| IL-6 | 178 | 8% | 6 | 106 | Typical |
| IL-8 (CXCL8) | 55 | 11% | 0 | 34 | Typical |
| GD2 | 39 | 0% | 0 | 32 | Typical |
| B7-H3 (CD276) | 32 | 9% | 0 | 29 | Typical |
| HER2 (ERBB2) | 76 | 5% | 1 | 67 | Typical |
| PD-L1 (CD274) | 169 | 5% | 1 | 144 | Typical |
| MDM2 | 180 | 6% | 3 | 125 | Typical |
| DKK1 | 28 | 14% | 2 | 18 | Elevated (2 retractions; would be typical with one fewer) |
| mTOR | 346 | 15% | 16 | 232 | Elevated |
| IGF1R | 89 | 26% | 5 | 67 | Elevated |
| CDK6 | 43 | 44% | 2 | 27 | **High** (microRNA-type share) |
| Cyclin E1 (CCNE1) | 33 | 15% | 3 | 25 | **High** (3 retractions; would be elevated with one fewer) |
| IL-6 receptor (IL6R) | 16 | 69% | 3 | 5 | **High** |
| DNMT1 | 33 | 39% | 6 | 21 | **High** |

*All values are our calculation from PubMed retraction status (registry). "Papers" means papers whose abstract PubTator tags with the gene, after the gene-name corrections described in the literature map.*

**What the retractions behind these flags actually are.** A gene "has" a retraction when a retracted paper mentions it. The paper need not be about that gene, so we checked titles (registry):
- **DKK1:** the two retracted papers are a study of convallatoxin in osteosarcoma cells (PMID 35635031) and a signalling "network map" for CKAP4 across cancers (PMID 36944905). Neither is a DKK1 study, and neither comes from the laboratories behind the DKK1 metastasis work. The DKK1 flag says nothing about that evidence base. Its real weakness, two laboratories sharing one model, is described in the literature map and the pet-dog brief.
- **Cyclin E1:** the three retracted papers are about nimotuzumab and EGFR (PMID 31001861), DDX5 and TCF12 (PMID 30733679) and PAK4 (PMID 35005025). Each uses cyclin E1 only as a downstream read-out. The high flag rests on these three, and with one fewer it would be elevated. It is not independent support for the close reading's "weak" verdict, which rests on the absence of any CDK2-inhibitor experiment in osteosarcoma.
- **FAK:** the single retracted paper is a proteomics study of AURKB (PMID 31122179), not a FAK study.
- **IL-6:** of the six, two are not osteosarcoma papers (a pancreatic-cancer gene analysis, PMID 25409614, and a spinal-cord-injury microarray study, PMID 25063577). The share, 3.4%, is just under the 4% "elevated" line.
- **IL-6 receptor:** the three are one retracted paper on LINC01116 (PMID 30098545) and two corrections to it, all listed by PubMed as retracted.

**What this means for the leads:**
- **FAK and IL-6 have low retraction and low microRNA-type shares.** That is not the same as strong evidence. For FAK, the close reading found that only about 12 of 105 papers actually block FAK. For IL-6, 34% of all its osteosarcoma papers are cell-line-only (our calculation). IL-6 work should build on IL-6 itself, not on IL-6 receptor papers, 69% of which are microRNA-type.
- **DKK1's elevated flag should not count against it**, for the reasons above.
- **Cyclin E1's high flag is fragile.** The case against a cyclin E1 trial rests on the close reading, not on this flag.
- **CDK6** is now flagged high because 44% of its papers since 2010 are microRNA-type. CDK4/6 inhibitors have 14 osteosarcoma trials, so the CDK6 rationale in those trials deserves a second look.
- **DNMT1**, the target of decitabine and azacitidine (4 osteosarcoma trials), has six retractions among 33 papers (18%).

## Journals

Among journals with at least 30 osteosarcoma papers since 2010, the most retractions were in *Oncology Letters* (22 of 389), *BioMed Research International* (19 of 83), *Oncology Research* (16 of 77), *European Review for Medical and Pharmacological Sciences* (15 of 156), *Molecular Medicine Reports* (15 of 226), *OncoTargets and Therapy* (15 of 136), *PLoS One* (15 of 284) and *Tumor Biology* (14 of 182) (our calculation). High counts can partly reflect publishers' clean-up efforts, which is a good thing. Some of these journals are reported to have had large publisher-led retraction rounds, but we have not checked those reports.

## Limits

- Paper types come from keywords in the title and abstract, so some papers are misclassified, though a hand check found all 7 sampled microRNA-type tags correct.
- Gene tags come from automated text mining, corrected for the mis-normalisations we found (listed in the literature map and in `tools/literature_map.py`). An earlier version listed PTK2B among the high-risk genes. Its retracted papers were really about AKT ("protein kinase B"), which is now counted under AKT1 (elevated: 59 of 963 papers retracted, 6.1%).
- A retracted paper counts against every gene it mentions, whether or not the gene is its subject (see the examples above).
- Retraction status is as of November 14, 2026, from PubMed (registry), and retractions lag publication.
- With 15–40 papers a gene, one retraction can move a flag. Use the interval and the fragility column in the data file.
- The thresholds are judgement calls. The raw percentages are in the data file for anyone who prefers their own.

## Change log

- **November 13, 2026.** First version.
- **November 14, 2026.** Revised after an independent audit (`research_notes/Audit/audit_C_literature_risk_surface.md`):
  - The earlier "template" (microRNA-type with no mention of animals, patients or dogs) is replaced by the microRNA-type share alone. The audit showed that the narrower definition did not change the retraction rate (8.6% against 8.7%), and the earlier text had described it inaccurately as "only cell-line work".
  - The headline comparison now matches the literature map: 8.7% against 1.0%, 8.4-fold.
  - Gene-name corrections removed PTK2B from the high-risk list. Its retractions belong to AKT1.
  - Gene counts changed from 371 genes (52 high, 96 elevated, 223 typical) to 362 (75 high, 100 elevated, 187 typical). Most of this comes from the broader definition and the corrections.
  - CDK6 moves from elevated to high.
  - Confidence intervals and a one-retraction fragility flag were added.
  - The statements that DKK1's retractions "reinforce" caution and that cyclin E1's flag is "consistent with" its verdict were wrong, because those retracted papers are not about those genes. They have been rewritten.
  - "FAK and IL-6 rest on clean literatures" is softened to low retraction and microRNA-type shares.
  - Stale references to numbered leads are removed.
  - The unsupported claim about publisher retraction rounds is softened.
