# The osteosarcoma literature map: what 33,000 papers say, and what they don't

*Step 2 of the For John dot-connecting plan. Built November 13–14, 2026 from every PubMed paper with "osteosarcoma" in its title or abstract (33,242 papers; 29,720 excluding reviews), with genes tagged by NCBI's PubTator3 text-mining service and corrected where we found it wrong. Each gene is linked to the 603 interventional trials in the trials report and to the NIH grants in the funding report. Data: `data/osteosarcoma_gene_evidence.csv` (1,487 genes named in at least 5 non-review papers), `data/osteosarcoma_paper_tags.csv` (one row per paper), `data/osteosarcoma_literature_periods.csv` (the period table below), `data/drug_targets_curated.json` (drug-to-target map). Scripts: `tools/literature_fetch.py`, `tools/literature_map.py`.*

## Summary

We tagged every osteosarcoma paper in PubMed by the genes it names and the kind of evidence its abstract describes, then compared that with the trials and grants. The most-trialled targets are the blood-vessel receptors hit by multi-kinase pills, and those receptors are named in relatively few osteosarcoma papers. Several genes with large literatures and clinical drugs elsewhere, notably FAK, DKK1, MDM2 and cyclin E1, have no registered human osteosarcoma trial; on close reading FAK and DKK1 hold up best and MDM2 worst. About one in eleven microRNA-type osteosarcoma papers published since 2010 has been retracted, more than eight times the rate for other papers, so genes whose evidence rests mainly on such papers need checking before anyone builds on them. Everything here comes from automated tagging of abstracts and is a set of leads, not conclusions.

**How to read the labels.** Key numbers carry one of these tags:
- **(registry)**: read directly from an official registry or database: ClinicalTrials.gov, PubMed's own listings (for example, which papers are retracted), NIH RePORTER, FDA approval notices.
- **(paper, full text)**: we read the full paper.
- **(paper, abstract only)**: we read only the abstract.
- **(press release only)**: the only source is a press release or an institution's web listing, not a paper or a registry.
- **(our calculation)**: we computed it from this repository's data files with the scripts named above.

## Three findings

1. **Trials follow available drugs more than osteosarcoma biology.** The most-trialled targets are blood-vessel receptors hit by multi-kinase pills: VEGFR2 in 57 trials, PDGFRB in 32 and KIT in 31 (our calculation). Relatively few osteosarcoma papers name these receptors themselves (42 to 68 each), although the drugs have a literature of their own that a gene count does not capture. Meanwhile FAK (PTK2), DKK1, MDM2 and cyclin E1 (CCNE1), each with a substantial literature that includes animal and patient data and a drug in clinical use or testing elsewhere, have **no registered human osteosarcoma trial as of November 14, 2026** (registry).
2. **A measurable share of the literature is unreliable.** Since 2010, **244 of 2,816 microRNA, lncRNA and circRNA papers (8.7%, 95% CI 7.7–9.8%) have been retracted, against 167 of 16,121 other papers (1.0%, 95% CI 0.9–1.2%)**, an 8.4-fold difference (our calculation, retraction status from PubMed). These papers peaked in 2015–2019, when they were 20% of osteosarcoma research output.
3. **NIH funds work on two orphan targets that has not reached a human trial.** NIH funds osteosarcoma grants on FAK inhibition (Colorado State, R37) and on DKK-1 (Albert Einstein College of Medicine, R01; Texas A&M, R21) (registry). Drugs against both exist. Defactinib, a FAK inhibitor, received FDA accelerated approval on May 8, 2025, co-packaged with avutometinib, for KRAS-mutated recurrent low-grade serous ovarian cancer (registry). Colorado State lists a study giving defactinib to dogs with lung-metastatic osteosarcoma (press release only: web listing; status and results not found). We found no record of DKN-01 (sirexatamab), the anti-DKK1 antibody, being given to a dog.

## How the literature has changed

| Years | Research papers | microRNA-type papers | Retracted | Cell-line-only papers |
|---|---|---|---|---|
| 2000–2004 | 2,026 | 3 | 1 | 386 |
| 2005–2009 | 2,416 | 8 | 3 | 493 |
| 2010–2014 | 3,627 | 180 (5%) | 26 | 690 |
| 2015–2019 | 5,853 | 1,196 (20%) | 244 | 1,271 |
| 2020–2024 | 7,251 | 1,282 (18%) | 139 | 1,063 |
| 2025–2026 | 2,206 | 158 (7%) | 2 | 289 |

*Non-review papers (our calculation). The 2025–2026 row includes 2 papers dated 2027 (ahead of print). Papers from before 2000 (5,786) and 555 papers with no year in PubTator are in `data/osteosarcoma_literature_periods.csv`. Retractions lag publication by years, so recent periods will rise.*

PubMed lists **418 retracted osteosarcoma papers, and all 418 are in this dataset** (registry). 244 of them are microRNA-type papers. Of the 418, 3 are reviews and 4 are research papers from before 2010, which leaves the 411 research papers since 2010 (244 microRNA-type plus 167 others) used in the comparison above and in the risk-flag report. The pattern fits what has been described as "paper mill" output, formulaic and often fabricated papers sold to authors: typically a microRNA or long non-coding RNA that "sponges" another and controls a familiar gene in the U2OS or MG-63 cell lines. A retraction rate cannot show which unretracted papers are of this kind.

**Genes whose evidence rests most on weak papers** (at least 40 papers, and at least 60% of them cell-line-only, microRNA-type, or both; each paper counted once): BAX, ANXA5, CDH2, LC3 (MAP1LC3A), CCNB1, ZEB1, MIR34A, ROCK1, MALAT1 and HK2 (our calculation). BCL2 and p21 (CDKN1A) sit just below the line at 59%.

**Highest retraction share** (at least 20 papers): DNMT1 (6 of 33) and SOX4 (4 of 22) are joint highest at 18%, followed by SIRT1 (5/37), ZEB1 (9/67), MIR21 (5/39), BMI1 (3/25), ROCK1 (6/50), MIR34A (7/59), TUG1 (3/27) and FASN (4/37) (our calculation). Among genes with fewer papers, several individual microRNAs have higher shares.

Two of these matter for trials. CDK6 is a target of palbociclib, abemaciclib and trilaciclib, which have 14 osteosarcoma trials between them (our calculation), and 37% of CDK6's osteosarcoma papers are microRNA-type (44% of those since 2010). DNMT1, the target of decitabine and azacitidine (4 osteosarcoma trials), has the joint-highest retraction share among genes with at least 20 papers.

## Trials against the evidence behind them

| Target | Osteosarcoma trials | Osteosarcoma papers naming the gene | With animal data | With patient data | Note |
|---|---|---|---|---|---|
| VEGFR2 (KDR) | 57 | 68 | 26 | 37 | Hit by multi-kinase pills; VEGFA itself has 432 papers |
| PDGFRB | 32 | 42 | 14 | 18 | Multi-kinase pills |
| KIT | 31 | 55 | 14 | 29 | Multi-kinase pills |
| PD-1 (PDCD1) | at least 29 | 125 | 50 | 85 | Checkpoint inhibitors; 1 of 22 osteosarcoma patients responded to pembrolizumab in SARC028 (paper, abstract only; PMID 28988646) |
| GD2 | 22 | 53 | 30 | 32 | Antibodies and CAR-T, borrowed from neuroblastoma |
| mTOR | 21 | 365 | 175 | 131 | Large literature; trials largely negative |
| CDK4 / CDK6 | 14 | 175 / 51 | 42 / 20 | 88 / 22 | CDK6 evidence 37% microRNA-type |
| IGF1R | 13 | 130 | 45 | 55 | Failed across sarcomas |
| B7-H3 (CD276) | 13 | 34 | 15 | 24 | Newest class, small literature |
| PARP1 | 10 | 186 | 55 | 40 | 47% of papers cell-line-only |
| Zoledronate target (FDPS) | 8 | 6 | 2 | 2 | Phase 3 OS2006 did not improve event-free survival and trended toward harm (paper, abstract only) |

*All counts are our calculation. Trial counts include basket trials and count a trial once per target, so multi-kinase pills appear under several targets. A trial is linked to a target only if its drug is in the hand-curated drug map; several PD-1 antibodies common in Chinese osteosarcoma trials (toripalimab, sintilimab, tislelizumab, penpulimab, serplulimab) are not yet mapped, so the PD-1 count is a floor. Paper counts are papers that name the gene, not papers about the drug.*

The pattern suggests that drugs reach osteosarcoma trials largely because they exist and are approved for something else. Zoledronate reached a phase 3 trial with only six osteosarcoma papers naming its molecular target, FDPS (our calculation). Papers about zoledronate itself are more numerous and are not counted here.

## Orphan targets: strong literature, a drug exists, no trial

Genes with at least 30 osteosarcoma papers, at least 10 with animal data and 10 with patient data, no more than 20% microRNA-type and 35% cell-line-only papers, and no registered osteosarcoma trial in the drug map: **73 genes** (our calculation). Most are markers or biology without a drug (TP53, osteocalcin, vimentin). These have clinical-stage drugs in other diseases:

| Target | Osteosarcoma papers (animal / patient / dog) | Clinical-stage drugs elsewhere | Osteosarcoma or sarcoma trials (registry) | NIH osteosarcoma grants (registry) |
|---|---|---|---|---|
| MDM2 | 249 (63 / 109 / 4) | Milademetan, brigimadlin, idasanutlin, navtemadlin | None in osteosarcoma; about 10 in other sarcomas, mostly dedifferentiated liposarcoma | None naming MDM2; the close reading below finds a weak rationale |
| FAK (PTK2) | 105 (46 / 27 / 0) | Defactinib (FDA accelerated approval 2025, with avutometinib, KRAS-mutated low-grade serous ovarian cancer) | No human osteosarcoma trial; 1 sarcoma trial (MPNST, NCT07743554) not yet recruiting; a canine osteosarcoma study at Colorado State (press release only) | 1: R37, Colorado State |
| DKK1 | 36 (16 / 12 / 0) | DKN-01 (sirexatamab) | None | 2: R01, Albert Einstein College of Medicine; R21, Texas A&M |
| Cyclin E1 (CCNE1) | 34 (11 / 20 / 0) | CDK2 inhibitors (BLU-222, INX-315) | None in osteosarcoma; the one sarcoma-eligible trial (BLU-222, NCT05252416) was terminated | None |
| STAT3 | 308 (137 / 97 / 14) | Napabucasin, TTI-101 | None | 1: a P01 subproject, 2015–2017, ended |
| IL-6 | 270 (95 / 71 / 8) | Tocilizumab, siltuximab | No trial tests IL-6 blockade as therapy. One immunotherapy combination trial (NCT04616248) lists tocilizumab, apparently to manage side effects | 1: K08, Nationwide Children's, 2016–2020, ended (shared with IL-8) |
| CXCR4 / CXCL12 | 115 / 64 | Motixafortide, mavorixafor, plerixafor | None as anti-tumour therapy; plerixafor's sarcoma registrations are for stem-cell collection | None |
| IL-8 (CXCL8) | 85 (22 / 32 / 6) | Reparixin, SX-682 | None | 1: the same K08 as IL-6 |
| IGF2 | 76 (31 / 12 / 1) | Xentuzumab, dusigitumab | None | None |

*Paper counts are our calculation. Trial searches were run on ClinicalTrials.gov API v2 by drug name and condition on November 14, 2026. Grant counts are focused or substantial osteosarcoma grants whose title names the gene, allowing for hyphenated or spelled-out forms such as "IL-6", "DKK-1" and "focal adhesion kinase".*

IL-6 and IL-8 match a gap the research report already named: the IL-1, IL-6 and IL-8 axis that drives lung metastasis in mouse models. We found no registered osteosarcoma trial that blocks it (registry).

## Close reading: do the four strongest orphan targets hold up?

A second pass read every abstract for MDM2, FAK, DKK1 and cyclin E1 (424 papers) and judged consistency, strength, retractions and whether a patient group could be selected. A later pass read the full text of every FAK and DKK1 paper the pet-dog brief relies on. Notes with PubMed IDs: `research_notes/Osteosarcoma literature map/orphan_targets_close_read.md` and `research_notes/Osteosarcoma literature map/fak_dkk1_full_text_check.md`.

| Target | Verdict | Best evidence | Biggest problem | Key missing experiment |
|---|---|---|---|---|
| **DKK1** | Moderate; anti-metastatic mouse data | A DKK1-blocking morpholino reduced lung metastasis in a patient-derived model: 2 of 10 treated against 7 of 9 control lungs positive for human tumour DNA (paper, full text; PMID 39805917). An independent group reported the same direction with an oral compound that lowers DKK1 (paper, full text; PMID 39280613). The antibody BHQ880, a different antibody from DKN-01, gave 4 of 27 against 6 of 18; that difference was not significant as randomised (P = 0.17), and reached P = 0.03 only after three treated mice were excluded (paper, full text; PMID 27049730) | The decisive work comes from two laboratories that share one patient-derived model; one older paper points the other way (PMID 24859848); no cut-off for "high DKK1" patients | Independent replication in a model neither laboratory owns, ideally with DKN-01 itself and in dogs |
| **FAK (PTK2)** | Moderate; most immediately actionable | Defactinib itself reduced lung metastasis in mice: in an orthotopic model (143B cells engineered to overexpress LOX, injected into the shin bone), 2 of 6 treated mice developed lung metastases against 6 of 6 untreated (P = 0.03), with no change in primary tumour weight; the paper prints the dose as 50 μg/kg twice daily, which is unusually low (paper, full text; Genes & Diseases 2023, PMID 37013056). Separately, PF-562271, an oral FAK inhibitor that reached phase 1, halved growth of subcutaneous 143B xenografts (n = 6 per group), without a metastasis endpoint (paper, full text; PMID 28406574). Colorado State lists a study giving defactinib to dogs with lung-metastatic osteosarcoma (press release only: web listing; status and results not found). Activated FAK is high in 62% of tumours (33 of 53), and it predicted outcome only in the 33 patients with metastases (paper, full text; PMID 28846700) | The defactinib mouse result is small (6 mice per group), uses one engineered cell line and an unusual dose. Only about 12 of 105 papers actually block FAK. The close reading listed eight papers that seemed to contradict FAK's role; full-text reading of five found them narrow or off-topic, and none tests a FAK inhibitor and reports failure | Independent replication of the defactinib metastasis result in an unengineered model, at a standard dose and after removal of the primary tumour; the status and results of the Colorado State dog study |
| **Cyclin E1 (CCNE1)** | Weak | High protein in 61% of tumours, the largest patient genomic base of the four (paper, abstract only) | No abstract reports a CDK2 inhibitor in an osteosarcoma model; no abstract gives the amplification frequency a trial would need | Test a CDK2 inhibitor in cyclin-E1-high osteosarcoma models |
| **MDM2** | Contradictory | One oral dose of an MDM2 inhibitor (SAR405838) caused complete regression in an SJSA-1 xenograft (paper, abstract only) | Almost all of the work uses one cell line (SJSA-1). MDM2 amplification is common in low-grade osteosarcoma, which surgery usually cures, but uncommon in the aggressive form: about 7% of 83 tumours in one study (paper, abstract only), 14% of 66 patients in the MSK sequencing cohort, which includes adults and relapse samples (paper, full text; PMID 31175097), and 2.5% of 81 TARGET-OS tumours at diagnosis (our calculation, copy-number report), and the drugs need intact TP53, which most patients lack. The NCI Pediatric Preclinical Testing Program excluded its osteosarcoma models from the TP53-wild-type analysis because they expressed very little TP53 (paper, abstract only; PMID 27238606) | Find the share of high-grade osteosarcoma with MDM2 amplification and intact TP53 |

**What this changes.** MDM2, which looked like the strongest orphan by paper count, is the weakest case for a trial in the patients who need one most. FAK and DKK1, the two targets NIH already funds, have the best evidence, and they have opposite strengths. For FAK, defactinib itself reduced lung metastasis in one small mouse study (2 of 6 against 6 of 6; PMID 37013056), and Colorado State lists a study giving it to dogs, though its status and results are unconfirmed. For DKK1, there is mouse evidence against metastasis in the same implant, amputate and watch design a dog study would copy, but we found no record of a dog receiving DKN-01. The cheapest high-value steps this map points to are finding out whether the listed Colorado State defactinib study ran and what it showed, and testing DKN-01 in dogs. The pet-dog brief (`briefs/Brief - pet dog trial of FAK or DKK1 blockade.md`) sets this out.

**Across all four**: for FAK and DKK1, the only published study we found of the clinical drug itself in an osteosarcoma model is the small defactinib study above (PMID 37013056); we found none for DKN-01, whose mouse data use a different antibody, BHQ880, and a morpholino. MDM2 inhibitors, including clinical-stage ones, have been tested, but almost only in the SJSA-1 cell line. For cyclin E1, we found no report of any CDK2 inhibitor being tested. Studies of whether blocking a target prevents metastasis, the thing that kills patients, are rare for all four.

## Limits

- **Gene tagging is automated and imperfect.** PubTator3 maps some common abbreviations to the wrong gene, and before correction these reached headline lists. We now correct the cases we found, by the mention text PubTator recorded: "protein kinase B"/"PKB" (tagged PTK2B) to AKT1; "p21" (tagged H3P16, a histone pseudogene) to CDKN1A; "MET" (tagged SLTM) to MET; "COX-2" (tagged mitochondrial COX2) to PTGS2; "P-gp" (tagged PGP) to ABCB1; "p53" (tagged the mouse pseudogene TRP53-PS) to TP53. We drop "tyrosine kinase" (tagged TXK), "TNM" staging (tagged TENM1), the microRNA prefix "hsa" (tagged ALB) and generic "BMP" (tagged BMP1). The correction table is in `tools/literature_map.py`. It is not exhaustive. Mouse and rat genes are merged with human ones by symbol.
- **Paper tags are keyword-based and miss in both directions.** "Animal data" means the abstract mentions mice, rats, xenografts or similar, not that the target was tested in them. It also fires on rat cell lines and on letters. The gene name "murine double minute" (MDM2) is now excluded. "Patient data" is triggered by any mention of "patients", including "survival of osteosarcoma patients is poor". It misses phrases such as "osteosarcoma tissues" or "clinical samples", so some papers tagged cell-line-only did use patient tissue. In the audit's 21-paper hand check, 5 of 7 cell-line-only tags and 4 of 7 animal tags were correct by their own definitions, and all 7 microRNA-type tags were correct.
- **The corpus is "papers mentioning osteosarcoma", not "osteosarcoma research".** About a quarter of non-review papers (7,360 of 29,720) do not mention osteosarcoma, OS, sarcoma or bone in the title, often because they use the U2OS cell line as a general lab tool (our calculation). This inflates paper counts and the cell-line-only share.
- **A microRNA-type paper is not automatically unreliable.** The 8.7% figure counts only retractions so far. Retraction is a lagging outcome, so recent papers look cleaner than they will. Restricted to 2010–2019, the rates are 12.6% against 1.2% (our calculation).
- **Gene-name counts are not drug literature.** The comparison of trials with papers counts papers naming the target gene, not papers about the drug.
- **Trial links depend on the hand-curated drug map**, so a trial of a drug missing from the map is not counted.
- **Abstracts only**, except in the close reading and the full-text check.

## Reproducing this

```
python3 tools/literature_fetch.py   # PubMed + PubTator3 download (slow; JSONL is git-ignored)
python3 tools/literature_map.py     # gene table, paper tags, period table, headline figures
python3 tools/paper_mill_flag.py    # evidence risk flags (see the risk-flag report)
```

## Change log

- **November 13, 2026.** First version.
- **November 14, 2026.** Revised after an independent audit (`research_notes/Audit/audit_C_literature_risk_surface.md`):
  - The retracted-paper list had duplicate PMIDs. PubMed lists 418 retracted papers, not 455, and all are in the dataset. The fetch script now de-duplicates.
  - Added the PubTator correction map. The gene table now has 1,487 genes, down from 1,494, and the orphan list has 73 genes, down from 79. The artefacts TRP53-PS, SLTM, TXK, PGP, COX2 and BMP1 are gone.
  - The animal-data tag no longer fires on "murine double minute", so MDM2 has 63 papers with animal data, down from 75.
  - Recomputed the period table from the de-duplicated data. The 2005–09, 2010–14 and 2025–26 rows had come from an earlier run.
  - The ratio is now given as 8.4-fold, with confidence intervals, in place of "ninefold".
  - The weak-evidence list now counts each paper once (cell-line-only or microRNA-type), not the two shares added together. It has 10 genes, down from 20.
  - The retraction-share list now has the correct order. SOX2 is out, and DNMT1 is "joint highest among genes with at least 20 papers".
  - Grant matching now catches "IL-6", "DKK-1" and "focal adhesion kinase", which adds the IL-6/IL-8 K08 grant.
  - The defactinib approval is now worded as an accelerated approval of the avutometinib co-pack.
  - The statement that nobody had tested the actual drugs was out of date and has been rewritten to match the full-text check, including the Colorado State canine defactinib study.
  - The PPTP MDM2 wording is corrected. The zoledronate and PD-1 counts are labelled as gene-name counts and as a floor.
  - Unsupported claims about paper mills and citation of unretracted papers are removed.
- **November 20, 2026.** Aligned with the ranked leads and the pet-dog brief after a repo-wide consistency check (`research_notes/Audit/consistency_check.md`):
  - FAK: the defactinib orthotopic mouse result (PMID 37013056; lung metastasis in 2 of 6 treated against 6 of 6 untreated mice, P = 0.03; 143B cells engineered to overexpress LOX, injected into the shin bone; dose printed as 50 μg/kg twice daily, flagged as unusual) is now the best FAK evidence. The statements that there was "no mouse evidence against metastasis" and "no published study of defactinib in an osteosarcoma model" were wrong and are removed.
  - Colorado State's canine defactinib study is now described as a web listing whose status and results are unconfirmed, not as a study that has already treated dogs.
  - MDM2: the 7% of 83 figure now sits beside MSK's 14% of 66 and TARGET-OS's 2.5% of 81, with their sources.
