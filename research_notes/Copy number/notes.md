# Copy number working notes (19 November 2026)

Groundwork for lead 2 (`reports/Ranked leads and research partners.md`): do VEGFA (6p21) or KDR/PDGFRA/KIT (4q12) amplifications predict benefit from VEGFR2-blocking pills? Script: `tools/copy_number_map.py`. Raw files: `data/copy_number_raw/` (git-ignored, 274 MB). Output table: `data/osteosarcoma_copy_number_frequencies.csv`.

## 1. Data access (GDC, checked 19 Nov 2026)

- GDC files endpoint, `cases.project.project_id = TARGET-OS`, `data_category = Copy Number Variation`: 387 files in all, 189 open and 198 controlled.
- **Open:** 81 "Gene Level Copy Number" (ASCAT2, Affymetrix SNP6 genotyping arrays), 81 "Allele-specific Copy Number Segment" (ASCAT2, same arrays), 27 "Copy Number Segment" (GATK4 CNV, whole genomes).
- **Controlled:** the raw array intensities (.cel, 171 files) and the 27 GATK "Intermediate Analysis Archive" tarballs. We did not need them.
- So TARGET-OS copy number is **not** controlled-access at the processed level. No fallback to GEO or supplementary tables was needed. cBioPortal (www.cbioportal.org) did not answer from this workspace (connection refused at the proxy), so MSK numbers below come from the papers, not the portal.
- All 81 array files are paired tumour/blood-normal, one "Primary Tumor" per patient (diagnostic samples, before treatment). 24 of the 27 WGS patients are also among the 81.
- Ages (GDC open clinical fields): median 14.5 years, range 3.6–32.4; 18 of 81 aged 18 or older.
- Downloads: `GET https://api.gdc.cancer.gov/data/{file_id}`, one per file; the server sometimes dropped the connection (curl error 52), handled by retries.

## 2. Method choices

- **Ploidy.** Osteosarcomas are far from diploid: ASCAT2 ploidy (length-weighted mean copy number over autosomes) had median 3.34, range 1.54–5.36; 55 of 81 tumours had ploidy 3 or more. An absolute threshold such as "more than 4 copies" therefore calls broad whole-chromosome gains in near-tetraploid tumours "amplified". Example: ERBB2, never focally amplified here, reaches CN > 4 in 6 of 81 (7.4%) only because of ploidy.
- **Primary amplification call:** CN ≥ 2 × tumour ploidy. Closest to panel "fold change > 2" calls (MSK used fold change > 2, per Suehara 2019 methods) and to WGS log2 ≥ 1.
- **Sensitivity calls:** CN ≥ 1.5 × ploidy (lenient "gain"); CN ≥ 8 (strict); CN > 4 (Sayles 2019 threshold, for comparison only).
- **Deletions:** deep = any part of the gene at 0 copies (min_copy_number = 0); loss = CN < 0.65 × ploidy (one-copy loss in a diploid, two of 3.5 in a near-tetraploid).
- GDC leaves `copy_number` blank when a breakpoint falls inside the gene; we then use the mean of min and max.
- **Statistics:** Wilson 95% intervals; two-sided Fisher exact for co-occurrence, with Haldane-corrected odds ratios (0.5 added to each cell); Spearman rho with Fisher-z CI (variance 1.06/(n−3)) and a 10,000-shuffle permutation p (seed 1).

## 3. Results, TARGET-OS (81 patients, diagnostic primary tumours)

Primary call (CN ≥ 2 × ploidy):

| Gene | n | % | 95% CI | lenient (≥1.5×) | strict (≥8) |
|---|---|---|---|---|---|
| VEGFA | 13 | 16.0 | 9.6–25.5 | 23 (28.4%) | 12 (14.8%) |
| KDR | 7 | 8.6 | 4.2–16.8 | 19 (23.5%) | 5 (6.2%) |
| PDGFRA | 10 | 12.3 | 6.8–21.3 | 21 (25.9%) | 6 (7.4%) |
| KIT | 9 | 11.1 | 6.0–19.8 | 21 (25.9%) | 6 (7.4%) |
| any 4q12 | 10 | 12.3 | 6.8–21.3 | | |
| any VEGFA/KDR/PDGFRA/KIT | 19 | 23.5 | 15.6–33.8 | 38 (46.9%) | 17 (21.0%) |
| + FGFR1 or MET | 23 | 28.4 | 19.7–39.0 | | |
| FGFR1 | 5 | 6.2 | 2.7–13.6 | 10 (12.3%) | 2 (2.5%) |
| MET | 0 | 0 | 0–4.5 | 3 (3.7%) | 0 |
| MYC | 26 | 32.1 | 22.9–42.9 | 45 (55.6%) | 23 (28.4%) |
| CCNE1 | 15 | 18.5 | 11.6–28.3 | 27 (33.3%) | 12 (14.8%) |
| CDK4 | 3 | 3.7 | 1.3–10.3 | 8 (9.9%) | 3 (3.7%) |
| MDM2 | 2 | 2.5 | 0.7–8.6 | 4 (4.9%) | 1 (1.2%) |
| PTK2 (FAK) | 9 | 11.1 | 6.0–19.8 | 27 (33.3%) | 4 (4.9%) |
| DKK1 | 2 | 2.5 | 0.7–8.6 | 5 (6.2%) | 1 (1.2%) |
| CD276 (B7-H3) | 0 | 0 | 0–4.5 | 4 (4.9%) | 1 (1.2%) |
| ERBB2 | 0 | 0 | 0–4.5 | 0 | 0 |

Deletions:

| Gene | deep deletion (any 0 copies) | relative loss (<0.65 × ploidy) |
|---|---|---|
| RB1 | 8 (9.9%, 5.1–18.3) | 52 (64.2%, 53.3–73.8) |
| CDKN2A | 11 (13.6%, 7.8–22.7) | 39 (48.1%, 37.6–58.9) |
| TP53 | 6 (7.4%, 3.4–15.2) | 51 (63.0%, 52.1–72.7) |
| PTEN | 2 (2.5%, 0.7–8.6) | 42 (51.9%, 41.1–62.4) |
| DKK1 | 0 (0%, 0–4.5) | 37 (45.7%, 35.3–56.5) |

Co-occurrence (primary call; both / first only / second only / neither; Haldane OR; Fisher p):

- VEGFA × any 4q12: 4 / 9 / 6 / 62; OR 4.55; p = 0.0496. **Not mutually exclusive here.**
- VEGFA × KIT 4/9/5/63, p = 0.033; VEGFA × PDGFRA 4/9/6/62, p = 0.0496; VEGFA × KDR 3/10/4/64, p = 0.078.
- 4q12 genes travel together: pattern KDR-PDGFRA-KIT 111 in 7, 011 (PDGFRA+KIT) in 2, 010 (PDGFRA only) in 1; KDR never amplified alone.
- Number of VEGFR-set genes amplified per patient: 0 in 62, 1 in 10, 2 in 1, 3 in 5, 4 in 3.
- MYC × PTK2 (both 8q24): 8/18/1/54, p = 0.0003. Expected, same arm.
- 4q12 × MDM2 0/10/2/69 and 4q12 × CDK4 0/10/3/68 (p = 1.0): none co-amplified, but too few MDM2/CDK4 cases to test.
- VEGFA × MYC, VEGFA × CCNE1, MYC × CCNE1, 4q12 × MYC: no association (p ≥ 0.65).

WGS cross-check (24 patients with both; GATK log2 ≥ 1 vs array CN ≥ 2 × ploidy): VEGFA 24/24 agree (4 amplified on both), r = 0.98 for log2 values; KDR and PDGFRA 24/24 agree (none amplified in this subset), KIT 23/24 (one WGS-only call); MYC 22/24 (2 array-only); CCNE1 24/24; CDK4 24/24; MDM2 23/24; FGFR1 24/24. The 4q12 check is weak because no 4q12-amplified tumour is among the 24.

Stricter 6p21 × 4q12 check (CN ≥ 3 × ploidy): VEGFA in 10, 4q12 in 2, both in 1 (Fisher p = 0.23). Most TARGET-OS 4q12 calls are low-level: in 8 of 10 4q12-amplified tumours the highest 4q12 gene sits at 2.0–3.0 × ploidy; the other two are at 3.0 × and 5.8 ×. Of the 4 tumours called for both, 3 have VEGFA at 4.3–5.2 × ploidy with 4q12 at 2.2–3.0 ×; the fourth has VEGFA at 2.4 × and 4q12 at 2.8 ×. So the co-occurrence is mostly high VEGFA with a modest 4q12 gain, much as MSK described its one exception ("4q12 amplification was higher while the 6p12 gain was borderline", reversed here).

## 4. Expression vs copy number (cached TARGET-OS STAR files, reused)

88 primary-tumour RNA samples in `data/surface_targets_raw/`; 80 patients have both RNA and copy number. Spearman of log2(TPM+1) against CN/ploidy; permutation p floor is 1/10,001 (shown as <0.001).

| Gene | rho (CN/ploidy) | 95% CI | perm p | rho (absolute CN) | median TPM, amplified vs not |
|---|---|---|---|---|---|
| VEGFA | 0.22 | −0.01 to 0.42 | 0.051 | 0.17 | 51.8 (n=13) vs 28.1 |
| KDR | 0.20 | −0.03 to 0.41 | 0.077 | 0.11 | 19.2 (n=7) vs 22.1 |
| PDGFRA | 0.55 | 0.37 to 0.69 | <0.001 | 0.57 | 91.5 (n=10) vs 44.8 |
| KIT | 0.16 | −0.07 to 0.37 | 0.17 | 0.06 | 4.3 (n=9) vs 3.8 |
| MYC | 0.41 | 0.21 to 0.59 | <0.001 | 0.23 | 81.4 (n=25) vs 46.5 |
| CDK4 | 0.61 | 0.44 to 0.73 | <0.001 | 0.32 | 387.9 (n=3) vs 72.2 |
| MDM2 | 0.44 | 0.24 to 0.61 | <0.001 | 0.28 | 182.8 (n=2) vs 10.5 |
| FGFR1 | 0.57 | 0.40 to 0.71 | <0.001 | 0.50 | 239.8 (n=5) vs 90.8 |
| CCNE1 | 0.51 | 0.32 to 0.66 | <0.001 | 0.41 | 103.2 (n=15) vs 19.1 |
| PTK2 | 0.61 | 0.44 to 0.73 | <0.001 | 0.54 | 28.8 (n=9) vs 20.3 |
| MET | 0.25 | 0.03 to 0.45 | 0.023 | 0.23 | no amplified tumours |
| CD276 | 0.40 | 0.19 to 0.57 | <0.001 | 0.31 | no amplified tumours |

Reading: VEGFA RNA is about 1.8-fold higher in amplified tumours, but the overall correlation is weak and its CI touches zero. KDR shows no copy-number effect on RNA: bulk KDR RNA is likely dominated by tumour blood vessels (endothelium), not tumour cells. That is our inference, not tested here. Of the 4q12 genes, only PDGFRA RNA tracks copy number clearly, consistent with MSK's strong PDGFRA staining in 4q12-amplified tumours.

## 5. Published frequencies (read 19 Nov 2026)

Full texts from NCBI PMC efetch; Bousquet 2026 and Marinoff 2023 only had abstract text available.

- **Suehara 2019, MSK-IMPACT, Clin Cancer Res** (PMC6825534, PMID 31175097; full text). 66 patients, 71 samples (37 metastatic/recurrent), paediatric and adult. Fold change > 2 for gains. "VEGFA at 6p12 was amplified in 14 of 59 patients (24%)"; table: VEGFA 17 samples (24%), CCND3 13 (18%). "4q12 amplification ... in 13 of 66 patients (20%)"; KIT 11 (15%), KDR 11 (15%), PDGFRA 13 (18%). MDM2 9 of 66 (14%), CDK4 9 (13–14%), 6 with both. CDKN2A deletion 16 (22%). CCNE1 6 samples (8%). PTEN deletion or truncation 2 of 66 (3%). Quote: "The 17 samples with VEFGA / CCND3 amplification at 6p12–21 were mutually exclusive with the 13 samples with amplification of PDGFRA, KIT and KDR, with one exception". Also: 4q12 "mutually exclusive ... with 12q14 gene amplification involving MDM2". And "at least 40% of patients have tumors harboring PDGFRA or VEGFA amplification".
- **Sayles 2019, Cancer Discov** (PMC7134333; full text). WGS of 30 tumours from 23 patients, merged with a published 31-patient WGS set. Thresholds >4, >8, >12 purity-adjusted copies (absolute, not ploidy-relative). MYC 39%, CCNE1 33%, RAD21 38%, VEGFA 23%, AURKB 13%, CDK4 11%; TP53 74%, RB1 64%, PTEN 56% (deletions, SVs and SNVs combined). Denominator for the per-patient percentages not stated in the sentences read.
- **Bousquet 2026, Cancer** (PMC13348730, PMID 42424099; abstract only). Foundation Medicine panel, 653 patients aged 40 or under. TP53 55%, RB1 22%, MYC 17%, CCND3 16% altered; CDK4/MDM2 amplification more frequent in young adults, MYC/CCND3/CCNE1 in children and adolescents.
- **Japan C-CAT, Int J Clin Oncol 2025** (PMC11785636; full text). 204 patients. "TP53 (79 patients; 39%), followed by RB1 (42; 21%), CDKN2A (36; 18%), VEGFA (35; 17%), CDKN2B (33; 16%), and CCND3 (33; 16%)". Alteration type not split in that sentence.
- **Amary 2014, Cancer Med** (PMC4303166; full text). FGFR1 amplification by FISH in 24 of 275 bone osteosarcomas (8.7%; the text prints 9.6%, Table 4 gives 8.7%); 18.5% of poor responders.
- **Marinoff 2023, JCO Precis Oncol** (PMC10531050; abstract only). 92 patients (OncoPanel) plus 86 (MSK-IMPACT); MYC amplification linked to worse 3-year survival in both. No frequencies in the abstract.
- **Behjati 2017** (PMC5490007), **Chen 2014** (PMC4096827), **Recurrent OS 2023** (PMC10646480): no per-gene amplification percentages for our genes found by text search.

Agreements and disagreements with TARGET-OS (primary call unless stated):

| Item | TARGET-OS | Published | Verdict |
|---|---|---|---|
| VEGFA | 16.0% (9.6–25.5); 28.4% at 1.5× | 24% MSK, 23% Sayles, 17% C-CAT | Consistent; published values sit between our strict and lenient calls |
| 4q12 (any) | 12.3% (6.8–21.3) | 20% MSK | Lower; MSK's 20% lies just inside our CI. Our 4q12 calls are mostly low-level |
| VEGFA or 4q12 | 23.5% (15.6–33.8); 46.9% at 1.5× | "at least 40%" MSK | **Disagree at the primary call.** 40% is only reached with the lenient threshold |
| 6p21 vs 4q12 | 4 of 19 both; OR 4.55, p = 0.0496 | mutually exclusive except 1 (MSK) | **Disagree** at 2× ploidy; at 3× ploidy 1 shared case, no significant pattern either way |
| MDM2 | 2.5% (0.7–8.6) | 14% MSK | **Disagree.** Likely age and setting: MSK includes adults and 37 metastatic/recurrent samples; Bousquet finds MDM2 more often in young adults |
| CDK4 | 3.7% | 11% Sayles, 14% MSK | Lower, same likely reason |
| MYC | 32.1% (22.9–42.9) | 39% Sayles (>4 copies), 17% altered Bousquet | Within range |
| CCNE1 | 18.5% | 33% Sayles, 8% MSK | Between the two |
| FGFR1 | 6.2% (2.7–13.6) | 8.7% (24 of 275) FISH (Amary; the paper's text misprints 9.6%) | Consistent |
| CDKN2A deep deletion | 13.6% | 22% MSK, 18% C-CAT | Somewhat lower; MSK counts any deletion |
| RB1, TP53, PTEN loss | 64%, 63%, 52% relative loss | 64%, 74%, 56% Sayles (incl. SVs/SNVs) | Consistent; copy number alone misses TP53 intron-1 rearrangements |

## 6. Power for lead 2 (our calculation; `python3 tools/copy_number_map.py power`)

Trial pool (osteosarcoma patients only):

| Trial | Drug | Design | Pill arm | Control | Crossover onto pill | Source (label) |
|---|---|---|---|---|---|---|
| SARC024 | regorafenib | randomized vs placebo | 22 | 20 | 11 | NCT02048371 participant flow: 22 / 9 placebo / 11 crossover (registry). The repo's kinase notes cite 10 of 20 crossing over from the abstract; the registry flow says 11 |
| REGOBONE | regorafenib | randomized 2:1 vs placebo | 26 | 12 | 10 | PMID 30477937 (paper, abstract only): 43 randomized (29 / 14); 26 / 12 are the efficacy-evaluable patients |
| OLIE | lenvatinib + IE | randomized vs IE | 40 | 41 | 0 | NCT04154189 (registry) |
| OAIE | apatinib + IE | randomized 2:1 vs IE | 53 | 28 | 0 | PMC12647724 (paper, full text) |
| CABONE | cabozantinib | single arm | 45 (42 evaluable) | – | – | NCT02243605 (registry); 42 in paper |
| ADVL1622 | cabozantinib | single arm, osteosarcoma stratum | 29 | – | – | NCT02867592 (registry) |
| ITCC-050 | lenvatinib | single arm, osteosarcoma expansion | 31 | – | – | NCT02432274 cohort 2B (registry) |
| ITCC-050 | lenvatinib + IE | single arm, osteosarcoma combination cohorts | 42 | – | – | NCT02432274 participant flow: cohort 3A 7 + 15, cohort 3B 20 (registry); added 20 Nov 2026 after audit E |

Totals (updated 20 Nov 2026): 309 pill-exposed (141 randomized pill arms + 21 crossover + 147 single arm); 174 on a pill alone (no IE); 135 with IE; 242 in the four randomized trials (247 counting all 43 REGOBONE patients randomized). The 19 Nov version counted 267 and missed ITCC-050's combination cohorts.

Assumptions: two-sided alpha 0.05; Schoenfeld events formula; 90% of patients have a PFS event by analysis (CABONE 9.5% progression-free at 12 months); two tissue scenarios, 100% and 60% of patients with usable copy-number data (60% is our guess for archival tissue plus plasma; not measured). Amplified share p: 23.5% (our VEGFR-set call), 16.0% (VEGFA only), 40% (MSK), 20% (pessimistic).

Question A, prognostic within pill-treated patients (amplified vs not, HR 0.5), 80% power:

| p | events | patients with data | enrol at 60% yield |
|---|---|---|---|
| 0.40 | 69 | 76 | 127 |
| 0.235 | 91 | 101 | 169 |
| 0.20 | 103 | 114 | 190 |
| 0.16 | 122 | 136 | 226 |

At 90% power, p = 0.235: 122 events, 136 patients with data.

Question B, predictive (treatment × amplification interaction, ratio of HRs 0.5) in randomized trials, 80% power: 273 (p 0.40) to 487 (p 0.16) events with 1:1 allocation, more with 2:1; p = 0.235 needs 364 events (1:1) or 409 (2:1), i.e. 404–455 patients with data.

Power available from the pool at HR 0.5:

| Pool | n | p = 0.235, 100% data | p = 0.235, 60% data | p = 0.16, 60% | p = 0.40, 60% |
|---|---|---|---|---|---|
| All pill-exposed | 309 | 0.998 | 0.97 | 0.91 | 0.99 |
| Pill alone (no IE) | 174 | 0.96 | 0.81 | 0.69 | 0.91 |
| Randomized, interaction | 242 | 0.57 | 0.38 | 0.30 | 0.48 |

Conclusion: Question A (amplified vs not among pill-treated patients) is answerable from the existing trials if most samples can be found. Question B (does amplification predict benefit *from the drug* compared with control) is not adequately powered even with all four randomized trials; it would need roughly 1.7 to 3 times their combined size, or a meta-analysis that adds the next randomized trials.

## 7. Status

- `python3 tools/copy_number_map.py all` re-run end to end on 19 Nov 2026; output CSV identical (md5 ccea582e…).
- Not done: linking TARGET-OS copy number to outcome (front-line chemotherapy only, no pills); checking which trials banked tissue or plasma; cBioPortal MSK data (portal unreachable).
