# The osteosarcoma literature map: what 33,000 papers say, and what they don't

*Step 2 of the For John dot-connecting plan. Built on November 14, 2026 from every PubMed paper with "osteosarcoma" in its title or abstract (33,242 papers, 29,720 excluding reviews), with genes and chemicals tagged by NCBI's PubTator3 text-mining service. Each gene is linked to the 603 interventional trials in the trials report and the NIH grants in the funding report. Data: `data/osteosarcoma_gene_evidence.csv` (1,494 genes named in at least 5 papers), `data/osteosarcoma_paper_tags.csv` (one row per paper), `data/drug_targets_curated.json` (drug-to-target map). Scripts: `tools/literature_fetch.py`, `tools/literature_map.py`.*

## Summary

Three connections stand out.

1. **Trials follow available drugs, not osteosarcoma biology.** The most-trialled targets are the blood-vessel receptors hit by multi-kinase pills (VEGFR2 in 57 trials, PDGFRB in 32, KIT in 31), yet these have thin osteosarcoma literature behind them (42 to 68 papers each). Meanwhile genes with large, patient-backed literatures and drugs in clinical use elsewhere, such as MDM2, FAK (PTK2), DKK1 and cyclin E1 (CCNE1), have **no osteosarcoma trial at all**.
2. **A measurable share of the literature is unreliable.** Since 2010, **8.7% of osteosarcoma microRNA, lncRNA and circRNA papers have been retracted, against 1.0% of other papers**, a ninefold difference. These papers peaked in 2015–2019, when they made up 20% of all osteosarcoma research output. Genes whose evidence comes mostly from these papers or from single cell lines should not anchor a trial.
3. **NIH funds work on some orphan targets that never reaches a trial.** NIH currently funds osteosarcoma grants on DKK-1 and on FAK inhibition, and drugs against both exist (a FAK inhibitor was FDA-approved for ovarian cancer in 2025), but no osteosarcoma trial of either is registered.

Every finding below is a lead built from automated tagging, not a conclusion. The close reading of four targets at the end shows how a lead holds up when a reader checks the actual papers.

## How the literature has changed

| Years | Research papers | microRNA-type papers | Retracted | Cell-line-only papers |
|---|---|---|---|---|
| 2000–2004 | 2,026 | 3 | 1 | 386 |
| 2005–2009 | 2,423 | 8 | 3 | 491 |
| 2010–2014 | 3,692 | 180 | 26 | 699 |
| 2015–2019 | 5,853 | 1,196 (20%) | 244 | 1,270 |
| 2020–2024 | 7,251 | 1,282 (18%) | 139 | 1,060 |
| 2025–2026 | 2,366 | 167 | 2 | 308 |

*Earlier periods are in the data file. Retractions lag publication by years, so recent periods will rise.*

PubMed lists 455 retracted osteosarcoma papers; 418 are in this dataset, and 244 of those are microRNA-type papers. Osteosarcoma is one of the cancers most targeted by "paper mills", companies that sell formulaic, often fabricated papers. The usual template is a microRNA or long non-coding RNA that "sponges" another and controls a familiar gene in the U2OS or MG-63 cell lines. Unretracted papers of the same type are still being cited.

**Genes whose evidence rests most on weak papers** (at least 40 papers, and 60% or more either cell-line-only or microRNA-type): BCL2, BAX, CDH1, CASP9, PTEN, ANXA5, CDH2, SNAI1, LC3, CCNB1, Beclin-1, E2F1, ZEB1, MIR34A, CDK6, ROCK1, MALAT1, TWIST1, TIMP2 and HK2. **Highest retraction share** (at least 20 papers): DNMT1 (6 of 33 retracted), SOX4 (4/22), SIRT1 (5/37), ZEB1 (9/67), MIR21 (5/39), ROCK1 (6/50), MIR34A (7/59) and SOX2 (8/86).

Two of these are relevant to trials. CDK6 is a target of palbociclib, abemaciclib and trilaciclib, which have 14 osteosarcoma trials between them, and 37% of CDK6's osteosarcoma papers are microRNA-type. DNMT1, the target of decitabine and azacitidine, has the highest retraction share of any gene.

## Trials against the evidence behind them

| Target | Osteosarcoma trials | Osteosarcoma papers | With animal data | With patient data | Note |
|---|---|---|---|---|---|
| VEGFR2 (KDR) | 57 | 68 | 26 | 37 | Hit by multi-kinase pills; VEGFA itself has 432 papers |
| PDGFRB | 32 | 42 | 14 | 18 | Multi-kinase pills |
| KIT | 31 | 55 | 14 | 29 | Multi-kinase pills |
| PD-1 (PDCD1) | 29 | 125 | 50 | 85 | Checkpoint inhibitors; about 5% response |
| GD2 | 22 | 53 | 30 | 32 | Antibodies and CAR-T, borrowed from neuroblastoma |
| mTOR | 21 | 365 | 175 | 131 | Large literature; trials largely negative |
| CDK4/6 | 14 | 175 / 51 | 46 / 20 | 88 / 22 | CDK6 evidence 37% microRNA-type |
| IGF1R | 13 | 130 | 45 | 55 | Failed across sarcomas |
| B7-H3 (CD276) | 13 | 34 | 15 | 24 | Newest class, small literature |
| PARP1 | 10 | 186 | 56 | 40 | 47% of papers cell-line-only |
| Zoledronate target (FDPS) | 8 | 6 | 2 | 2 | Phase 3 OS2006 trended toward harm |

*Trial counts include basket trials and count a trial once per target, so multi-kinase pills appear under several targets.*

The pattern is that drugs reach osteosarcoma trials because they exist and are approved for something else, not because osteosarcoma research pointed to them. Zoledronate reached a phase 3 trial with six papers behind it.

## Orphan targets: strong literature, a drug exists, no trial

Genes with at least 30 osteosarcoma papers, at least 10 with animal data and 10 with patient data, no more than 20% microRNA-type and 35% cell-line-only papers, and no registered osteosarcoma trial: 79 genes. Most are markers or biology without a drug (TP53, osteocalcin, vimentin). These have clinical-stage drugs in other diseases:

| Target | Osteosarcoma papers (animal / patient / dog) | Clinical-stage drugs elsewhere | Osteosarcoma or sarcoma trials | NIH osteosarcoma grants |
|---|---|---|---|---|
| MDM2 | 249 (75 / 109 / 4) | Milademetan, brigimadlin, idasanutlin, navtemadlin | None in osteosarcoma; 9 in other sarcomas | None by title; see the close reading below, which finds a weak rationale |
| FAK (PTK2) | 105 (46 / 27 / 0) | Defactinib (FDA-approved 2025, ovarian cancer) | None in osteosarcoma; 1 sarcoma trial not yet recruiting | R37, Colorado State |
| DKK1 | 36 (16 / 12 / 0) | DKN-01 (sirexatamab) | None | R01 Einstein; R21 Texas A&M |
| Cyclin E1 (CCNE1) | 34 (11 / 20 / 0) | CDK2 inhibitors (BLU-222, INX-315) | None; the one sarcoma-eligible trial was terminated | None |
| STAT3 | 308 (137 / 97 / 14) | Napabucasin, TTI-101 | None | 1 |
| IL-6 | 270 (95 / 71 / 8) | Tocilizumab, siltuximab | 1 combination trial | None |
| CXCR4 / CXCL12 | 115 / 64 | Motixafortide, mavorixafor | None | None |
| IL-8 (CXCL8) | 85 (22 / 32 / 6) | Reparixin, SX-682 | None | None |
| IGF2 | 76 (31 / 12 / 1) | Xentuzumab, dusigitumab | None | None |

*Trial searches were run on ClinicalTrials.gov by drug name on November 14, 2026. "NIH grants by title" counts focused or substantial osteosarcoma grants naming the gene in the title.*

IL-6 and IL-8 match a gap the research report already named: the IL-1, IL-6 and IL-8 axis that drives lung metastasis in mouse models, which no trial has tested.

## Close reading: do the four strongest orphan targets hold up?

A second pass read every abstract for MDM2, FAK, DKK1 and cyclin E1 (424 papers) and judged consistency, strength, retractions and whether a patient group could be selected. Full notes with PubMed IDs: `research_notes/Osteosarcoma literature map/orphan_targets_close_read.md`.

| Target | Verdict | Best evidence | Biggest problem | Key missing experiment |
|---|---|---|---|---|
| **DKK1** | Moderate; most trial-ready | Three different ways of blocking DKK1 (an antibody close to DKN-01, a morpholino, a small molecule) all reduced metastasis and protected bone in mice, including patient-derived tumours grown in bone | Nearly all from one research lineage, never independently replicated; some papers report the opposite direction; no cut-off for "high DKK1" patients | Independent replication with DKN-01 itself, ideally in dogs |
| **FAK (PTK2)** | Moderate; most immediately actionable | A clinical-stage FAK inhibitor shrank osteosarcoma xenografts when given by mouth; activated FAK is high in 62% of tumours, and a FAK-based marker panel separated chemotherapy responders | Only about 12 of 105 papers actually block FAK; eight papers contradict its role | Defactinib in osteosarcoma models, selected on activated FAK |
| **Cyclin E1 (CCNE1)** | Weak | High protein in 61% of tumours, the largest patient genomic base of the four | No CDK2 inhibitor has ever been tested in an osteosarcoma model; no abstract gives the amplification frequency a trial would need | Test a CDK2 inhibitor in cyclin-E1-high osteosarcoma models |
| **MDM2** | Contradictory | One dose of an MDM2 inhibitor caused complete regression in a xenograft | Almost all of it is one cell line (SJSA-1). MDM2 amplification is common in low-grade osteosarcoma, which surgery usually cures, but rare in the aggressive form (about 7% of 83 tumours), and it excludes the TP53 damage most patients have. The NCI pediatric testing program left osteosarcoma models out for this reason | Find the share of high-grade osteosarcoma with MDM2 amplification and intact TP53 |

**What this changes.** MDM2, which looked like the strongest orphan by paper count, is the weakest case for a trial in the patients who need one most. DKK1 and FAK, the two targets NIH already funds, have the best evidence, and **neither has been tested in dogs**, even though one of the funded groups is at a veterinary school. A pet-dog study of DKN-01 or defactinib is the cheapest high-value experiment this map points to.

**Across all four**, nobody has tested the actual clinical drug in osteosarcoma models (only close analogues, and for cyclin E1 not even that), and studies of whether blocking the target prevents metastasis, the thing that kills patients, are rare.

## Limits

- **Gene tagging is automated.** PubTator sometimes maps a generic term to one gene (for example "Akt" to AKT1), and mouse and rat genes are merged with human ones by symbol.
- **Paper tags are keyword-based.** "Animal data" means the abstract mentions mice, rats, xenografts or similar; it does not mean the target was tested in them.
- **A microRNA-type paper is not automatically unreliable**, and the 8.7% figure counts only retractions so far.
- **Trial links depend on the hand-curated drug map**, so a trial of a drug missing from the map is not counted.
- **Abstracts only.** Full texts were not read except in the close reading below.
