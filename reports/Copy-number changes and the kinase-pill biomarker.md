# Copy-number changes in osteosarcoma, and how to test them as a kinase-pill biomarker

*Built from open-access NCI GDC copy-number and RNA data for the TARGET-OS project, published genomic studies and ClinicalTrials.gov records. Written November 19, 2026. Script: `tools/copy_number_map.py`. Table: `data/osteosarcoma_copy_number_frequencies.csv`. Working notes with quotes and every number: `research_notes/Copy number/notes.md`. This is groundwork for lead 2 in `reports/Ranked leads and research partners.md`.*

## Summary

We measured extra and missing gene copies in diagnostic tumours from 81 young patients in the US TARGET osteosarcoma project, using free public data. Extra copies of the genes behind VEGFR2-blocking pills (VEGFA, or the KDR/PDGFRA/KIT region) were found in about one patient in four (23.5%) by our main definition, and in nearly half (46.9%) by a lenient one. The figure of "at least 40%" quoted from a US cancer centre study sits between the two, so the answer depends on how "amplified" is defined, and any trial test must fix the definition in advance. Unlike that study, we did not find that the two gene regions exclude each other: 4 patients carried both, mostly high VEGFA with a modest 4q12 gain. Using the trials already done, about 100 pill-treated patients with tumour data would be enough to show whether amplified tumours stay controlled for twice as long, and the existing trials hold about 267 such patients. Proving that the amplification predicts benefit *from the pill* rather than just a better outlook needs roughly 400 or more patients in randomized trials, more than the four existing randomized trials have together (242).

**How to read the labels.** After key numbers we say where they come from:

- **(registry)**: an official database record, such as ClinicalTrials.gov or the NCI Genomic Data Commons.
- **(paper, full text)**: read in the full published paper.
- **(paper, abstract only)**: read only in the abstract.
- **(press release only)**: from a company announcement or the media, with no peer-reviewed paper. None are used here.
- **(our calculation)**: counted or computed by this project from the files above.
- **(preprint, abstract only)**: read only in the abstract of a preprint, which has not been peer-reviewed.

## What we used

- **Tumours.** 81 patients from TARGET-OS, one diagnostic primary tumour each, before treatment, with a matched blood sample (registry). Median age at diagnosis 14.5 years, range 3.6–32.4; 18 were 18 or older (our calculation).
- **Copy number.** GDC "Gene Level Copy Number" files from SNP arrays (ASCAT2 method), which give whole-number copy counts already corrected for normal cells in the sample. They are **open access**; only the raw array files are controlled (registry). Whole-genome copy number for 24 of the same patients was used as a check.
- **RNA.** The TARGET-OS RNA files this project had already downloaded for the surface-target report; 80 patients had both RNA and copy number.

**Why the definition matters.** Osteosarcoma cells often carry three or four copies of every chromosome instead of two. In these tumours the median was 3.3 copies, and 55 of 81 had three or more (our calculation). A fixed cut-off such as "more than 4 copies" then labels whole-chromosome gains as amplifications. As a check, ERBB2 (HER2), which no tumour here amplifies by our main call, passes "more than 4 copies" in 7.4% of tumours. So our main call is **at least twice the tumour's own average copy number**, close to what clinical sequencing panels call amplification. We also report a lenient call (1.5 times) and a strict one (8 copies or more).

## 1. The pill-target genes: how often, and do they overlap?

TARGET-OS, 81 patients (our calculation). "CI" is the 95% confidence interval.

| Gene or group | Region | Amplified (2× call) | 95% CI | Lenient (1.5×) | Strict (≥8 copies) | Published |
|---|---|---|---|---|---|---|
| VEGFA | 6p21 | 13 (16.0%) | 9.6–25.5% | 23 (28.4%) | 12 (14.8%) | 24% of 59 (MSK); 23% (whole genomes, Sayles 2019); 17% of 204 altered (Japan) (paper, full text) |
| KDR (VEGFR2) | 4q12 | 7 (8.6%) | 4.2–16.8% | 19 (23.5%) | 5 (6.2%) | 15% of samples (MSK) (paper, full text) |
| PDGFRA | 4q12 | 10 (12.3%) | 6.8–21.3% | 21 (25.9%) | 6 (7.4%) | 18% of samples (MSK) (paper, full text) |
| KIT | 4q12 | 9 (11.1%) | 6.0–19.8% | 21 (25.9%) | 6 (7.4%) | 15% of samples (MSK) (paper, full text) |
| Any 4q12 gene | 4q12 | 10 (12.3%) | 6.8–21.3% | | | 20% of 66 (MSK) (paper, full text) |
| **VEGFA or any 4q12 gene** | | **19 (23.5%)** | **15.6–33.8%** | **38 (46.9%)** | 17 (21.0%) | "at least 40%" (MSK) (paper, full text) |
| Adding FGFR1 or MET | | 23 (28.4%) | 19.7–39.0% | | | |

"MSK" is the Memorial Sloan Kettering study of 66 patients sequenced with the MSK-IMPACT panel (Suehara 2019, PMC6825534); children and adults, with 37 of its 71 samples from metastases or relapses.

**The 4q12 genes travel together.** KDR was never amplified without PDGFRA; all three genes were amplified together in 7 of the 10 (our calculation). Most 4q12 gains here are modest: in 8 of the 10, the highest gene was 2 to 3 times the tumour average (our calculation).

**6p21 and 4q12 are not mutually exclusive in TARGET-OS.** MSK reported that its VEGFA-amplified and 4q12-amplified tumours did not overlap, "with one exception" (paper, full text). We found:

| | 4q12 amplified | 4q12 not amplified |
|---|---|---|
| **VEGFA amplified** | 4 | 9 |
| **VEGFA not amplified** | 6 | 62 |

Odds ratio 4.55, Fisher p = 0.0496 (our calculation): if anything, they occur together *more* often than chance. At a stricter cut-off (3 times the average), only 2 tumours had 4q12 amplification, one of them with VEGFA as well, and no pattern either way can be shown (p = 0.23; our calculation). In three of the four overlapping tumours, VEGFA was high (4.3–5.2 times the average) and 4q12 was modest (2.2–3.0 times).

**What this means for lead 2.** The amplified group is about 24% by our main call and 47% by the lenient one. A trial analysis should fix the definition before seeing outcomes and report both. Because the two regions can overlap, the analysis should also count "VEGFA or 4q12" once per patient, not add the two percentages.

**Cross-check.** For the 24 patients with whole-genome data, VEGFA calls agreed in all 24 (4 amplified on both platforms), with a correlation of 0.98 between the two copy-number measures (our calculation). The 4q12 genes also agreed (23 or 24 of 24), but none of these 24 had a 4q12 amplification, so this check says little about 4q12.

## 2. Other actionable copy-number changes

TARGET-OS, 81 patients, main call (our calculation). "Published" is the closest figure we read.

| Gene | Drug class it points to | Amplified | 95% CI | Lenient (1.5×) | Published | Agreement |
|---|---|---|---|---|---|---|
| MYC (8q24) | none direct; CDK inhibitors in models | 26 (32.1%) | 22.9–42.9% | 45 (55.6%) | 39% (Sayles, >4 copies) (paper, full text); 17% altered (Foundation Medicine, 653 patients) (paper, abstract only) | Within range |
| CCNE1 (19q12) | CDK2 inhibitors | 15 (18.5%) | 11.6–28.3% | 27 (33.3%) | 33% (Sayles); 8% of samples (MSK) (paper, full text) | Between the two |
| PTK2 / FAK (8q24) | defactinib | 9 (11.1%) | 6.0–19.8% | 27 (33.3%) | none found | Mostly travels with MYC: 8 of 9 also MYC-amplified (p = 0.0003) |
| FGFR1 (8p11) | FGFR blockers; lenvatinib | 5 (6.2%) | 2.7–13.6% | 10 (12.3%) | 9.6% of 275 by FISH (Amary 2014) (paper, full text) | Consistent |
| CDK4 (12q14) | CDK4/6 inhibitors | 3 (3.7%) | 1.3–10.3% | 8 (9.9%) | 14% of 66 (MSK); 11% (Sayles) (paper, full text) | **Lower** |
| MDM2 (12q15) | MDM2 inhibitors | 2 (2.5%) | 0.7–8.6% | 4 (4.9%) | 14% of 66 (MSK) (paper, full text) | **Lower** |
| DKK1 (10q21) | DKN-01 | 2 (2.5%) | 0.7–8.6% | 5 (6.2%) | none found | — |
| MET (7q31) | cabozantinib; MET blockers | 0 | 0–4.5% | 3 (3.7%) | no frequency read | — |
| CD276 / B7-H3 (15q24) | ADCs, CAR-T | 0 | 0–4.5% | 4 (4.9%) | none found | B7-H3 is highly expressed without amplification (median 196 TPM) |
| ERBB2 / HER2 (17q12) | HER2 ADCs | 0 | 0–4.5% | 0 | none found | — |

**Why CDK4 and MDM2 are lower here.** TARGET-OS is mostly children and teenagers, sampled at diagnosis. MSK included adults and many relapse or metastasis samples (37 of 71), and the Foundation Medicine study found CDK4 and MDM2 amplification more often in young adults (paper, abstract only; PMID 42424099). This is our reading, not tested here.

**Lost genes.** Copy number alone undercounts these, because osteosarcoma often breaks TP53 and RB1 by rearrangement or mutation instead.

| Gene | Both copies lost (any part of gene) | One-copy or relative loss | Published |
|---|---|---|---|
| RB1 | 8 (9.9%; 5.1–18.3%) | 52 (64.2%; 53.3–73.8%) | 64% deleted, rearranged or mutated (Sayles) (paper, full text) |
| CDKN2A | 11 (13.6%; 7.8–22.7%) | 39 (48.1%; 37.6–58.9%) | 22% deleted (MSK); 18% altered (Japan) (paper, full text) |
| TP53 | 6 (7.4%; 3.4–15.2%) | 51 (63.0%; 52.1–72.7%) | 74% (Sayles) (paper, full text); 55% altered (Foundation Medicine) (paper, abstract only) |
| PTEN | 2 (2.5%; 0.7–8.6%) | 42 (51.9%; 41.1–62.4%) | 56% loss (Sayles) (paper, full text); 3% deletion or truncation (MSK) (paper, full text) |
| DKK1 | 0 | 37 (45.7%; 35.3–56.5%) | — |

All percentages in both tables are (our calculation) unless labelled otherwise. "Relative loss" means fewer than 0.65 times the tumour's average copy number.

## 3. Does extra DNA mean more RNA?

80 patients with both measures; Spearman correlation between copy number (relative to the tumour average) and RNA level (our calculation).

| Gene | Correlation | 95% CI | p | Median RNA (TPM), amplified vs not |
|---|---|---|---|---|
| VEGFA | 0.22 | −0.01 to 0.42 | 0.051 | 51.8 (13 tumours) vs 28.1 |
| KDR | 0.20 | −0.03 to 0.41 | 0.077 | 19.2 (7) vs 22.1 |
| PDGFRA | 0.55 | 0.37 to 0.69 | <0.001 | 91.5 (10) vs 44.8 |
| KIT | 0.16 | −0.07 to 0.37 | 0.17 | 4.3 (9) vs 3.8 |
| FGFR1 | 0.57 | 0.40 to 0.71 | <0.001 | 239.8 (5) vs 90.8 |
| CCNE1 | 0.51 | 0.32 to 0.66 | <0.001 | 103.2 (15) vs 19.1 |
| MYC | 0.41 | 0.21 to 0.59 | <0.001 | 81.4 (25) vs 46.5 |

- **VEGFA.** Amplified tumours make about 1.8 times more VEGFA RNA, but across all tumours the link is weak and not clearly different from zero.
- **KDR.** No link at all. In a bulk tumour sample, most KDR RNA probably comes from blood-vessel cells rather than tumour cells (our inference). So a KDR copy-number test and a KDR RNA test would measure different things.
- **PDGFRA** is the 4q12 gene whose RNA clearly follows its copy number, matching MSK's strong PDGFRA staining in 4q12-amplified tumours (paper, full text).
- More genes, including CDK4, MDM2, PTK2, MET and CD276, are in the working notes.

## 4. Design note for lead 2: how many patients, from which trials?

**The two questions.** They need very different numbers of patients.

- **Question A (prognostic among pill-treated patients).** Among patients given a VEGFR2-blocking pill, do those with VEGFA or 4q12 amplification stay progression-free longer? Target: hazard ratio 0.5 or lower.
- **Question B (predictive).** Does amplification predict benefit *from the pill*, compared with placebo or chemotherapy alone? This is the real biomarker question. It needs randomized trials, because amplified tumours could simply do better whatever the treatment.

**Osteosarcoma patients in the existing trials:**

| Trial | Drug | Design | On the pill | Control | Crossed over onto the pill | Source |
|---|---|---|---|---|---|---|
| SARC024 | regorafenib | randomized vs placebo | 22 | 20 | 11 | NCT02048371 (registry) |
| REGOBONE | regorafenib | randomized 2:1 vs placebo | 26 | 12 | 10 | PMID 30477937 (paper, abstract only) |
| OLIE | lenvatinib + IE | randomized vs IE | 40 | 41 | — | NCT04154189 (registry) |
| OAIE | apatinib + IE | randomized 2:1 vs IE | 53 | 28 | — | PMC12647724 (paper, full text) |
| CABONE | cabozantinib | single arm | 45 enrolled, 42 evaluable | — | — | NCT02243605 (registry); paper |
| COG ADVL1622 | cabozantinib | single arm, osteosarcoma group | 29 | — | — | NCT02867592 (registry) |
| ITCC-050 | lenvatinib | single arm, osteosarcoma group | 31 | — | — | NCT02432274 (registry) |

In all: **267 patients received a pill** (174 on the pill alone, 93 with IE chemotherapy), and **242 were in the four randomized trials** (our calculation). For SARC024, the registry lists 11 placebo patients who crossed over; the trial abstract, as quoted in our kinase-pill report, says 10 of 20.

**Assumptions (our calculation).**

- Standard formula for comparing two groups by hazard ratio (Schoenfeld), two-sided 5% significance, 80% power unless stated.
- 90% of patients have progressed by the time of analysis, since progression-free survival on these pills is short (9.5% progression-free at 12 months in CABONE; paper, full text).
- Amplified share: 23.5% (our main call), with 16%, 20% and 40% as alternatives.
- Usable tumour or blood DNA for 100% of patients, or for 60%. The 60% is our guess, not a measured figure: archival diagnostic tissue usually exists, but not always, and blood tests miss some low-level gains.

**Question A: patients needed** for a hazard ratio of 0.5 (our calculation):

| Amplified share | Events needed | Patients with DNA results | Patients to approach if 60% have usable DNA |
|---|---|---|---|
| 40% | 69 | 76 | 127 |
| **23.5% (our main call)** | **91** | **101** | **169** |
| 20% | 103 | 114 | 190 |
| 16% (VEGFA alone) | 122 | 136 | 226 |

At 90% power with a 23.5% amplified share: 122 events, 136 patients with results.

**Question B: patients needed** for the pill's benefit to differ two-fold between amplified and other tumours (a ratio of hazard ratios of 0.5): 364 events with 1:1 randomization, or 409 with 2:1, at a 23.5% amplified share. That is about 404–455 randomized patients with DNA results (our calculation).

**What the existing trials can do** (chance of detecting a hazard ratio of 0.5; our calculation):

| Pool | Patients | All have DNA, 23.5% amplified | 60% have DNA, 23.5% amplified | 60% have DNA, 16% amplified |
|---|---|---|---|---|
| Everyone who got a pill | 267 | 99.5% | 94% | 86% |
| Pill alone only (no IE) | 174 | 96% | 81% | 69% |
| Randomized trials, Question B | 242 | 57% | 38% | 30% |

**Recommended design.**

1. **Question A first, with all pill-treated patients.** Pool the pill arms of SARC024, REGOBONE, OLIE and OAIE with CABONE, ADVL1622 and ITCC-050, plus crossover patients from the start of their pill treatment. Analyse progression-free survival with a Cox model stratified by trial, because drugs, doses, IE backbones and ages differ. If 60% of patients have usable DNA, this has about 94% power for a hazard ratio of 0.5.
2. **If funds allow only part of this, start with the single-agent trials** (SARC024, REGOBONE, CABONE, ADVL1622, ITCC-050; 174 patients). This keeps chemotherapy out of the comparison, with about 81% power at 60% DNA yield.
3. **Question B as a pre-planned, hypothesis-generating interaction test** in the four randomized trials. The power is too low to settle it (30–57%), so report it as an estimate with its confidence interval, and plan to add FOSTER-CabOS and any restarted AOST2032 to a later pooled analysis.
4. **Fix the definition in advance**: main call at twice the tumour's average copy number, lenient call at 1.5 times as a sensitivity analysis, VEGFA and 4q12 also analysed separately. Ploidy-aware copy-number calling is needed; a fixed "more than 4 copies" rule would misclassify many tumours.
5. **Measure the right sample.** Trial patients have relapsed, but most stored tissue is from diagnosis. VEGFA amplification is enriched in the clones that return at relapse (8 patients; paper, abstract only; PMID 37812025). Where both exist, test the relapse sample or the blood taken at trial entry.
6. **Record MYC status as a variable.** MYC (8q24) is amplified in 26 of 81 TARGET-OS tumours here (32.1%, 95% CI 22.9–42.9%; our calculation, table above). In 105 children and young adults, MYC amplification (more than 7 copies, 16%) went with 3-year overall survival of 27% against 74%, adjusted HR 3.4 (paper, abstract only; *Cancer* 2025, PMID 41199591). Cell lines from MYC-driven mouse osteosarcomas were about 8 times less sensitive to cabozantinib than p53-driven lines (mean IC50 5.51 against 0.65 µM; preprint, abstract only; Kappa et al., bioRxiv 2026, doi 10.64898/2026.09.21.753033; fold change our calculation). So MYC should be measured with the same ploidy-aware call and entered in the Cox model, both as a possible confounder of a VEGFA or 4q12 effect and as a candidate marker of pill resistance in its own right (our inference).

## Limits

- **One cohort, diagnostic samples.** All 81 tumours are TARGET-OS primary tumours taken at diagnosis, mostly from children and teenagers in US cooperative-group care. Relapsed tumours, the setting where the pills are used, may differ, and adults are under-represented (18 of 81 aged 18 or older).
- **Small numbers.** With 81 patients, confidence intervals are wide: the VEGFA-or-4q12 figure could plausibly lie anywhere from 16% to 34%.
- **The 4q12 cross-check is weak.** No 4q12-amplified tumour had whole-genome data, so the 4q12 calls rest on one platform.
- **Thresholds are choices.** Published studies use different rules (fold change on panels, absolute copies on whole genomes, any alteration in registries), so the comparisons are rough. Our "relative loss" call for tumour-suppressor genes is a copy-number measure only; it misses mutations and rearrangements and includes some broad losses of no clear meaning.
- **Published sources.** cBioPortal could not be reached from this workspace, so MSK figures come from the paper, not its data portal. The Foundation Medicine and Marinoff studies were read as abstracts only. Some published percentages count samples, not patients.
- **RNA comparison.** Bulk RNA mixes tumour and normal cells; this matters most for KDR, which is expressed in blood vessels.
- **Power figures are approximate.** They assume most patients progress, that the 60% DNA yield is realistic, and that trials can be pooled. Drugs differ (regorafenib, cabozantinib, lenvatinib, apatinib), and two trials add chemotherapy. Patient counts were read from registries and papers; we have not checked which trials actually banked tumour or blood.
- **No outcomes.** We did not link copy number to survival or treatment in TARGET-OS, which used front-line chemotherapy, not pills.

## Reproduce

From the repository root: `python3 tools/copy_number_map.py all`. It downloads 189 open files (about 274 MB) into `data/copy_number_raw/` (git-ignored), reuses the RNA files in `data/surface_targets_raw/`, and writes `data/osteosarcoma_copy_number_frequencies.csv`. It uses only the Python standard library.

## Change log

- **19 November 2026.** First version. Open TARGET-OS copy number (81 patients) mapped for 18 genes; compared with five published studies; RNA correlation for 12 genes; sample-size note for lead 2.
- **19 November 2026 (later).** Recommended design step 6 added: record MYC status in the amplification test (32.1% amplified here; MYC amplification predicts poor survival, Cancer 2025, PMID 41199591; MYC-driven mouse cells resisted cabozantinib, bioRxiv 2026). New label **(preprint, abstract only)**: read only in a preprint's abstract; preprints are not peer-reviewed.
