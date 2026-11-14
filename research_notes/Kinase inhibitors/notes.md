# Kinase-inhibitor pills in osteosarcoma: research notes

*Started 2026-11-14. Working notes for the report `reports/Why kinase-inhibitor pills work in osteosarcoma.md`. Context taken as read (not redone): pooled control dataset report and CSVs, trials landscape report and CSV. Every claim carries a PMID, NCT or URL. "Abstract only" = full text not read. "HYPOTHESIS" = my inference, not a finding.*

## 0. Starting point (from earlier project work, not re-verified here)
- Pooled 4-month PFS/EFS: multi-kinase pill alone 52.5% (4 arms, 145 pts) vs older single agents 12.5%; IE alone in randomized control arms 56.1% (`data/osteosarcoma_relapse_benchmarks_published.csv`).
- AOST2032 NCT05691478 SUSPENDED ("Extend the observation period for current patients", last update 2026-10-27); CabOSTar NCT06341712 terminated after 10 pts; FOSTER platform NCT07871864 (Part 2 = FOSTER-CabOS maintenance vs BSC).

## 1. Mechanism: which kinases, and is it anti-tumour, anti-vessel or immune?

### Genomic targets in human osteosarcoma (findings)
- **4q12 (KIT/KDR/PDGFRA) and 6p12-21 (VEGFA) amplicons define two largely non-overlapping subsets.** MSK-IMPACT, 66 patients: 4q12 amplification (KIT, KDR, PDGFRA) in 13/66 (20%), with strong PDGFRA IHC; 6p12-21 gain with VEGFA amplification in 14 (24%); "at least 40%" have PDGFRA or VEGFA amplification. Suehara et al., Clin Cancer Res 2019, PMID 31175097 (abstract read; full text PMC6825534 downloaded, not mined further).
- **VEGFA amplification 23% of patients** in WGS of the Sayles PDX series (alongside MYC 39%, CCNE1 33%, RAD21 38%). Sayles et al., Cancer Discov 2019, PMID 30266815, full text PMC7134333.
- **VEGF-pathway amplification first reported** by aCGH + FISH in 58 archival tumours; VEGFA amplification and high VEGFA protein associated with microvessel density and worse tumour-free survival. Yang et al., Cancer 2011, PMID 21495021 (abstract only).
- **FGFR1 amplification** (FISH, 352 samples / 288 pts): 18.5% of patients with poor histologic response to chemotherapy; none among good responders. Fernanda Amary et al., Cancer Med 2014, PMID 24861215 (abstract only).
- **Clonal evolution:** longitudinal WGS of 37 samples / 8 relapsed patients: resistant clones enriched for MYC gain (6/7) and carried amplifications of CCNE1, RAD21, VEGFA, IGF1R. Subclonal at diagnosis, selected by neoadjuvant chemo. PMID 37812025 (abstract only). Implication: relapse tumours (where TKIs are tested) may be more VEGFA-amplified than diagnostic samples — HYPOTHESIS.
- **MET:** MET was first cloned as TPR-MET from an osteosarcoma cell line; activated Met transforms osteoblasts; dominant-negative Met blocks tumorigenicity (as reviewed in CABONE, Italiano 2020, PMID 32078813, author manuscript PMC8763616 full text).
- **Single case:** 51-month partial response to sorafenib in a 7-year-old; PDGFRA D846V later found in tumour (not in relapse specimen). PMID 30318721 (abstract only).

### Preclinical mechanism (findings)
- **Cabozantinib, direct + bone niche:** reduces OS cell proliferation/migration via ERK and AKT inhibition; in osteoblast co-culture raises osteoprotegerin and lowers RANKL; authors propose RANK expression as a predictor. Fioramonti et al., Sci Rep 2018, PMID 29520051 (abstract only).
- **Sorafenib:** pERK1/2, MCL-1 and pERM active in ~70% of OS samples; sorafenib lowers all three, induces apoptosis, blocks angiogenesis (CAM assay), reduces VEGF/MMP2, shrinks xenografts and lung metastases. Pignochino et al., Mol Cancer 2009, PMID 20003259 (abstract only).
- **Genome-matched sorafenib works in VEGFA-amplified PDX only:** sorafenib shrank a VEGFA-amplified PDX (repeated on later passage; lower VEGFA protein, pERK, pH3) but not a non-amplified PDX (OS128). VEGFA protein did not track copy number across PDX; one VEGFA-amplified PDX had very high VEGFR2 protein; authors suggest VEGFR2 may be the better biomarker and propose autocrine VEGFA–VEGFR2 signalling. Sayles 2019, PMC7134333 full text.
- **Cross-cancer analogy:** in HCC, VEGFA amplification marks sorafenib-sensitive tumours; mechanism is paracrine — tumour VEGF-A acts on stromal VEGFR, which produce HGF that drives tumour cells; VEGFA-amplified patients had markedly better survival on sorafenib (retrospective FISH). Horwitz et al., Cancer Discov 2014, PMID 24687604 (abstract only). HYPOTHESIS: the same VEGFA→stroma→HGF→MET loop would explain why a VEGFR2+MET drug (cabozantinib) is active in osteosarcoma.
- **Regorafenib in PDOX:** in two drug-resistant PDOX models, regorafenib caused regression and total necrosis; sorafenib arrested one; pazopanib, sunitinib, crizotinib only slowed growth. PMID 34479916 (abstract only; Hoffman lab, small).
- **Apatinib:** VEGFR2/STAT3/BCL-2 → autophagy and apoptosis in OS cells (PMID 28837148); lowers PD-L1 via STAT3 (PMID 29225166); VEGFR2 drives metastasis and PD-L2 via STAT3/RhoA-ROCK (PMID 33014879). Titles/abstracts only; cell-line work.
- **Adaptive FGFR–ERK signalling in lung metastases (bioRxiv 2026, PMID 42856637, not peer reviewed, abstract only):** in live ex vivo OS lung metastases, tumour-cell lysis after an MCL1 inhibitor amplified FGFR-mediated ERK signalling in neighbours; persistent ERKhigh/Fra-1high cells enriched at tumour–lung interface; FGFR inhibitor fexagratinib or pazopanib blocked this and improved MCL1-inhibitor efficacy ex vivo and in vivo.

### What the clinical data say about mechanism (findings)
- **Early metabolic response is common and predicts PFS (CABONE, osteosarcoma):** 31/42 evaluable on FDG-PET after 1 cycle; 20 (64.5%) partial metabolic response, 8 (25.8%) stable, 3 (9.7%) progressive; median PFS 7.2 vs 4.5 vs 1.8 months (p<.0001). PMC8763616 full text.
- **Necrosis/cavitation, not shrinkage:** CABONE: 12/90 pneumothorax (4 OS, 8 Ewing); all had pleural/subpleural metastases; cavitation from drug-induced tumour necrosis in 7. One PR patient had lung metastases resected with no residual tumour cells. PMC8763616. Apatinib phase 2: grade 3–4 pneumothorax 16.2%. PMID 30559126. OLIE: treatment-related pneumothorax 17.9% LEN-IE vs 0 IE (any-cause 28.2% vs 2.6%). PMC11581622 full text.
- **On-target toxicity tracks benefit (apatinib):** hypertension (HR 0.44 for PFS, p=0.07), anorexia (HR 0.35, p=0.01), pneumothorax and hypothyroidism associated with benefit. PMID 32021426 (abstract only). Interpretation (HYPOTHESIS): consistent with an on-target VEGFR effect / drug exposure, i.e. adequate vascular blockade.
- **Plasma markers (CABONE OS, exploratory, n=36):** low baseline VEGF-A → longer OS (13.2 vs 8.2 mo, p=0.014); high soluble MET → longer PFS (7.8 vs 5.4 mo, p=0.016). In Ewing, VEGFA/HGF/sVEGFR2 not associated; sMET trend only. Authors: MET inhibition "may contribute". PMC8763616.

### Synthesis (my reading, HYPOTHESIS-labelled where needed)
- The common denominator of all 8 active drugs is VEGFR2 (KDR) inhibition; MET (cabozantinib), FGFR (lenvatinib, anlotinib), PDGFR/KIT (most), RAF (sorafenib, regorafenib) vary. Apatinib is the most VEGFR2-selective and is at least as active (ORR 43% in its phase 2, PMID 30559126) → VEGFR2 blockade alone is sufficient for the main effect. (Inference from cross-trial comparison; not a head-to-head finding.)
- The clinical picture (necrosis, cavitation, pneumothorax, PET drop within 4 weeks, hypertension as marker, lung lesions respond better than bone) fits a predominantly **anti-vascular** effect on lung metastases, with possible direct tumour-cell VEGFA→VEGFR2 autocrine signalling in the VEGFA/KDR-amplified subset. Immune effect is unproven: PD-1 add-on gave no clear increment (APFAO, see §4).

## 2. Who responds: candidate predictors (all exploratory, none validated)

| Candidate | Evidence | Source |
|---|---|---|
| Lung-only disease (vs bone lesions) | APFAO (apatinib + camrelizumab, n=41 efficacy): median PFS musculoskeletal-only 2.1 mo (95% CI 1.8–5.7), lung-only 6.9 (4.8–8.1), both 5.7 (3.5–7.5); lesion location was the only factor significant on multivariate Cox (p=0.004). Lung-only share 73% (27/37) in apatinib phase 2 vs 42% (18/41) in APFAO, offered by authors as one reason for differing results. | PMC7223462 full text |
| Lung-only (supporting) | OAIE authors: TKIs "often exhibit limited and short-lived efficacy in controlling musculoskeletal lesions besides other metastasis outside the lung". In fruquintinib-based retrospective series (124 sarcoma pts, 56 OS), target lesions outside lung and bone → HR 1.79 for progression. | PMC12647724 full text; PMID 39030807 abstract |
| Early FDG-PET metabolic response | CABONE OS: PMR 64.5% after cycle 1; median PFS 7.2 / 4.5 / 1.8 mo for PMR / SMD / PMD (p<.0001). Sorafenib phase 2: PET responses and tumour density reduction seen among stable-disease patients. | PMC8763616; PMID 21527590 (abstract) |
| Plasma VEGF-A (low) and soluble MET (high) | CABONE OS, n=36: low VEGF-A → OS 13.2 vs 8.2 mo (p=0.014); high sMET → PFS 7.8 vs 5.4 (p=0.016). Not corrected for multiple testing. | PMC8763616 |
| Tumour PD-L1 ≥5% (combo with PD-1) | APFAO: PD-L1 evaluable in 28/41; 6 (21.4%) positive; PFS differed by PD-L1 (p=0.004), ORR not (p=0.11). | PMC7223462 |
| On-target toxicity | Apatinib: hypertension (HR 0.44, p=0.07), anorexia (HR 0.35, p=0.01), pneumothorax and hypothyroidism linked with benefit. | PMID 32021426 (abstract) |
| Germline VEGFR2 −906T>C | Retrospective apatinib, n=105: TT genotype longer PFS 5.0 vs 3.1 mo (p=0.011) and OS 9.8 vs 7.6 (p=0.032). | PMID 32215805 (abstract) |
| Coagulation | APFAO: hypercoagulability (shortened PT/APTT, 78%) and thrombocythaemia (85%) associated with shorter PFS on univariate analysis (HRs 3.61, 5.85, 4.88). | PMC7223462 |
| Tumour VEGFA amplification | Only preclinical: matched PDX response to sorafenib (Sayles PMC7134333); HCC analogy PMID 24687604. **No clinical osteosarcoma study linking VEGFA/KDR/PDGFRA/FGFR1/MET copy number to TKI response was found** (PubMed searches run 2026-11-14). | — |
| PDGFRA mutation | Single case, 51-month sorafenib PR (PDGFRA D846V). | PMID 30318721 (abstract) |
| Age, line, drug | CanSaRCC real-world (39 OS): age, line of therapy, regorafenib vs cabozantinib and time from diagnosis NOT associated with PFS. | PMID 37724607 (abstract) |
| Prior ifosfamide / earlier line | OLIE exploratory: LEN-IE vs IE median PFS 8.2 vs 6.0 mo without prior ifosfamide; 6.9 vs 5.5 with 1 prior line. | PMC11581622 full text |

- Children: ITCC-050 (2–25 y), CABONE (≥12), ADVL1622 (2–30 y), REGOBONE (≥10, but published cohort adults), SARC024 adults only (median age 37). Paediatric/AYA real-world (Japan NCC, 31 pts median 17 y): median PFS 51 d sorafenib, 101 d sorafenib+everolimus, 167 d regorafenib. PMID 37073613 (abstract). Pediatric regorafenib case series (6 pts, 12–18 y): 4/6 SD ≥8 wk, longest PFS >12 mo. PMID 42527100 (abstract).
- European sampling paper (2024) states plainly: "despite responses in up to 40% of patients, there are as yet no validated predicted biomarkers and the TKI mechanism of action remains obscure"; FOSTER-CabOS and AOST2032 include biomarker sampling timepoints. PMC11334773 full text.
- SARC024 and REGOBONE subgroup analyses: not read (SARC024 PMC7799443 body not returned by PMC efetch; REGOBONE abstract only). No subgroup finding reported here from them.

## 3. Why benefit is short and survival rarely improves

### Durability (findings)
- **CABONE OS:** 4-, 6-, 12-, 24-month PFS 71.4%, 52.4%, **9.5%**, 9.5%; median PFS 6.7 mo; OS 10.6 mo; 12- and 24-mo OS 37.9% and 23.3%. PMC8763616.
- **COG ADVL1622 (cabozantinib, ages 2–30), osteosarcoma stratum n=29, registry posted results:** response + disease-control rate 35.2% (20.2–48.3); 1-year PFS **14.7%** (4.7–30.2); 1-year time-to-progression-free 21.3%; 1-year OS 35.9%; grade ≥3 attributable AE 69.0%. https://clinicaltrials.gov/study/NCT02867592 (posted results; no paper found).
- **Sorafenib:** 4-mo PFS 46%, median PFS 4 mo, OS 7 mo; PR/SD ≥6 mo in 6/35 (17%). PMID 21527590. Sorafenib + everolimus: 6-mo PFS 45% (target ≥50% missed). PMID 25498219.
- **Apatinib:** median PFS 4.5 mo, OS 9.9 mo, despite ORR 43%. PMID 30559126.
- **Lenvatinib alone:** median PFS 3.0 mo; ORR 6.7%. PMID 34562750 (from project CSV).

### Overall survival in randomized trials (findings)
- **SARC024:** PFS HR 0.42 (0.21–0.85); OS not significant "in the context of the crossover design" (10 placebo crossed over). PMID 31013172 (abstract).
- **REGOBONE:** 10/12 placebo patients crossed over. PMID 30477937 (abstract).
- **OLIE (LEN-IE vs IE):** PFS HR 0.54 (0.27–1.08), missed significance (1-sided p=.04 vs threshold .025). **OS numerically worse with lenvatinib**: median 11.9 vs 17.4 mo, HR 1.28 (0.60–2.70); 12-mo OS 49.2% vs 72.1%; at final FDA-requested analysis HR 0.93 (0.53–1.62). Authors attribute partly to more surgery/subsequent therapy/crossover in IE arm. PMC11581622 full text.
- **OAIE (apatinib + IE vs IE):** PFS HR 0.60 (0.37–0.98) investigator; **OS numerically worse with apatinib**: median 18.1 vs 22.9 mo, HR 1.48 (0.76–2.89), p=0.25. 30.2% of Apa+IE vs 18.9% of IE had no further treatment. PMC12647724 full text.
- So in both randomized TKI+IE trials, the TKI arm had longer PFS but numerically shorter OS. Neither was powered for OS. HYPOTHESIS: (a) post-progression disease is more aggressive after VEGFR withdrawal ("rebound"), (b) TKI arm patients used up options/were less fit for later therapy (OAIE: more got no further treatment), or (c) chance. Testable in pooled individual-patient data.

### Mechanisms of resistance described (mostly preclinical; findings)
- mTORC2 upregulation after sorafenib (escape) → basis for sorafenib + everolimus. PMID 23434734 (abstract). Clinically the combo did not reach its target. PMID 25498219.
- Anlotinib-resistant OS cell lines: loss of PTEN + MAPK reactivation, reversed by PI3K inhibitor (PMID 35318116); IL-6/STAT3 activation reversed by tocilizumab (PMID 37404767); METTL3-m6A → DNA-PKcs (PMID 39924638, title only); VEGFR/Ras/CDK2 (PMID 38532893). All cell-line/xenograft, Chinese single labs, abstract only.
- Regorafenib: CTDSPL2 phosphatase from multi-omics of treated lines (PMID 40352265, abstract).
- Adaptive FGFR–ERK signalling at tumour–lung interface (bioRxiv, PMID 42856637).
- Clonal: relapse clones carry MYC/CCNE1/VEGFA/IGF1R amplification and continuing HRD signature (PMID 37812025) — not TKI-specific.
- Clinical pattern: **bone lesions resist** (APFAO, OAIE commentary); progression in ITCC-050 occurred almost entirely after IE stopped (as stated by OAIE authors, PMC12647724). Responses mostly necrosis/cavitation; necrotic shell remains.
- No osteosarcoma paper found on TKI-induced vessel co-option, hypoxia-driven escape, or serial biopsy at TKI progression in patients. GAP.

## 4. Combinations: what has been tried, and results

| Combination | Trial | Result | Source |
|---|---|---|---|
| Sorafenib + everolimus (mTOR) | Italian Sarcoma Group phase 2, NCT01804374, n=38 adults | 6-mo PFS 45% (28–61), target ≥50% not met; 66% needed dose changes | PMID 25498219 (abstract) |
| Lenvatinib + IE | ITCC-050 phase 1/2 (2–25 y) | 4-mo PFS 51% (34–69), n=35 at RP2D; grade 3–4 neutropenia 77%, thrombocytopenia 71% | PMID 34416158 (abstract) |
| Lenvatinib + IE vs IE | OLIE, NCT04154189, randomized, n=81 | PFS 6.5 vs 5.5 mo, HR 0.54 (0.27–1.08), not significant; OS 11.9 vs 17.4 mo | PMC11581622 (full text) |
| Apatinib + IE vs IE | OAIE, NCT05277480, randomized 2:1, n=81 (China) | PFS 5.5 vs 3.4 mo, HR 0.60 (0.37–0.98); OS 18.1 vs 22.9 mo, HR 1.48; lower ifosfamide dose (1.8 g/m²/d), 10 cycles | PMC12647724 (full text) |
| Apatinib + camrelizumab (PD-1) | APFAO, NCT03359018, n=43 | 6-mo PFS 50.9% KM, target 60% missed; ORR 20.9%; 2 durable responders | PMC7223462 (full text) |
| Regorafenib + nivolumab | SARC038, NCT04803877, n≈48 | Active, not recruiting; no results found (registry, web search 2026-11-14) | registry |
| Cabozantinib + atezolizumab | TACOS, NCT05019703 (MDACC) | Recruiting; no results | registry |
| Cabozantinib + pembrolizumab | PEMBROCABOSARC, NCT05182164 (OS stratum) | Recruiting; no OS results found | registry |
| Cabozantinib ± ICI (retrospective, all sarcomas) | 105 pts | No PFS/OS difference with vs without ICI | PMID 43020951 (abstract) |
| Cabozantinib + topotecan/cyclophosphamide | NCT04661852, n=12 (5 OS) | Concurrent dosing too toxic (3/6 DLT); RP2D cabozantinib 25 mg/m² days 8–21 (non-concomitant); 1 PR (Ewing) | PMID 37715723 (abstract) |
| Cabozantinib + ifosfamide | NCT06156410 (CHOP), phase 1 | Recruiting | registry |
| Sunitinib + losartan (CCR2/monocyte) | NCT03900793 (Colorado), phase 1 | Recruiting; based on dogs: losartan + toceranib CBR 50% in 28 dogs with lung metastases | registry; PMID 34580111 (abstract) |
| Lenvatinib + everolimus vs everolimus | NCT07619950 (Yonsei), randomized phase 2 | Not yet recruiting | registry |
| Apatinib + tucidinostat (HDAC) | NCT06125171 | Unknown status | registry |
| Apatinib + liposomal irinotecan | NCT07479732 (PKUPH) | Recruiting | registry |
| Apatinib + gemcitabine/docetaxel after resectable lung metastases | NCT03742193 (Ruijin) | Unknown status; no results | registry |

**Not tried in patients (registry searches 2026-11-14, ClinicalTrials.gov query.term):**
- VEGFR TKI + FAK inhibitor (defactinib): 0 osteosarcoma trials except NCI-MATCH basket NCT02465060.
- VEGFR TKI + selective MET inhibitor (capmatinib, tepotinib, savolitinib): 0. Preclinical: pazopanib + crizotinib synergy in OS cells and 143B xenografts (PMID 38423639, abstract).
- VEGFR TKI + selective FGFR inhibitor: 0 combination trials (erdafitinib only in MATCH baskets NCT03155620, NCT02465060, NCT03210714). Preclinical rationale: bioRxiv PMID 42856637.
- VEGFR TKI + PI3K or IL-6R blockade (anlotinib-resistance work, PMIDs 35318116, 37404767): 0.
- Biomarker-selected TKI trial (VEGFA- or 4q12-amplified): 0 found.
- **TKI maintenance after complete resection of relapse (resected-relapse setting):** no randomized trial found. FOSTER-CabOS and CabOSTar are after FIRST-line therapy; CabOSTar enrolled "unresectable residual osteosarcoma"; NCT04698785 (regorafenib maintenance, single arm, bone sarcomas, Léon Bérard) and NCT04055220 (regorafenib maintenance vs surveillance after first-line, randomized, 168 planned, Léon Bérard, recruiting since 2020) are the nearest. NCT05135975 (Nationwide Children's) is single-arm cabozantinib maintenance in high-risk pediatric solid tumours, 1-yr PFS endpoint.

## 5. Why not standard care

### Guideline and label status (findings)
- **NCCN Bone Cancer v3.2023**, as quoted in a CabOSTar protocol snippet surfaced by web search (protocol PDF itself blocked from this workspace, cdn.clinicaltrials.gov 403): second-line list includes high-dose ifosfamide ± etoposide, sorafenib, regorafenib; "additional recommended" includes cabozantinib and sorafenib + everolimus. Secondhand; NCCN itself needs login. https://cdn.clinicaltrials.gov/large-docs/12/NCT06341712/Prot_000.pdf
- Apatinib phase 2 paper (2019) states anti-angiogenic TKIs "have been included into new National Comprehensive Cancer Network guidelines as second-line therapy". PMID 30559126.
- **ESMO–EURACAN–GENTURIS–ERN PaedCan 2021** (PMID 34500044, doi 10.1016/j.annonc.2021.08.1995): could not read; web-search snippets say data on cabozantinib and regorafenib are given (supplementary). Grades NOT verified.
- **No regulatory approval for osteosarcoma anywhere found.** Cabozantinib FDA-approved for patients ≥12 y in differentiated thyroid cancer (2021) and pNET/epNET (March 2025; 60 mg ≥40 kg, 40 mg <40 kg). https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-cabozantinib-adults-and-pediatric-patients-12-years-age-and-older-pnet-and-epnet . Apatinib and anlotinib are Chinese-market drugs (apatinib "domestically made in China", PMID 30559126).
- Formulation: lenvatinib capsules can be dispersed in water/apple juice per US label (as summarised by drugs.com / label sites, https://drugs.com/dosage/lenvima.html). Cabozantinib: tablets; no pediatric liquid formulation found in this session. Pediatric dosing used: cabozantinib 40 mg/m²/day (ADVL1211 RP2D, PMID 29693796; CABONE children <16, PMID 32078813); regorafenib 82 mg/m² (PMID 34157616); lenvatinib 14 mg/m² (ITCC-050).
- Cost: US cash price for Cabometyx ~US$26,470 per 30 tablets (drugs.com), WebMDRx estimate ~US$47,882 uncouponed; NHS indicative £5,143 per 30 × 60 mg. https://www.drugs.com/price-guide/cabometyx ; https://www.webmdrx.com/drug-prices/cabometyx ; https://dmd-browser.nhsbsa.nhs.uk/ampp/view/156345 . Cash prices, not net prices.

### Toxicity specific to children and surgery (findings)
- **Growth plate:** COG review of 53 children on anti-angiogenic phase 1 trials: 5 (9.4%) had growth-plate abnormalities, all on sunitinib (1) or pazopanib (4); reversible off treatment. PMID 25257751 (abstract). Growth-plate dysplasia is "pathognomonic" of anti-angiogenic treatment in preclinical species (rodents, monkeys; rabbit femoral-head physis fracture). PMID 27162053 (abstract). Sorafenib case: "growth suppression" in a 7-year-old over 51 months. PMID 30318721.
- **Cabozantinib in children (ADVL1211):** DLTs at 40 mg/m² (PPE, mucositis, ALT/lipase/bilirubin) and 55 mg/m² (hypertension, PRES, proteinuria); DLTs in later cycles at all doses. PMID 29693796.
- **Wound healing/surgery:** apatinib grade 3–4 wound dehiscence 10.8% (PMID 30559126); AOST2032 skips cabozantinib in the first post-surgery consolidation cycle and has an exploratory objective on grade ≥3 port-site wound complications (registry description NCT05691478). Apatinib + AP neoadjuvant retrospective (19 vs 23 pts): more grade 3–4 mucositis 52.6% vs 17.4%, hand-foot 31.6% vs 0, proteinuria, hypertension; postoperative complications not different. PMID 38023239 (abstract).
- **Pneumothorax** is a class effect in lung-metastatic osteosarcoma (CABONE 4/45 OS; apatinib 16% grade 3–4; OLIE 17.9% related; fruquintinib series 14.5%). Sources above.
- **Chemo combination toxicity:** cabozantinib + topo/cyclo concurrent schedule not tolerable (PMID 37715723); ITCC-050 high haematological toxicity; OAIE reduced IE dose.

### Front-line and maintenance programme status (registry 2026-11-14)
| Trial | Setting | Status |
|---|---|---|
| COG AOST2032, NCT05691478 | MAP ± cabozantinib (incl. 6 cycles maintenance), newly diagnosed, ≤40 y, n=1122 planned, phase 2/3, US/Can/Aus/NZ | **SUSPENDED** — "Other - Extend the observation period for current patients"; last update 2026-10-27; feasibility closed 05/09/2025. No public explanation found (web search); site pages still say recruiting (e.g. trials.cancervic.org.au, St. Jude). |
| Ipsen CabOSTar, NCT06341712 | cabozantinib + BSC vs BSC, "unresectable residual osteosarcoma" after first line, 5–30 y | TERMINATED, 10 enrolled (5 vs 3 in safety groups), "ongoing recruitment challenges"; enrolment Nov 2024–Feb 2026; results section posted but PFS/ORR denominators 0. |
| FOSTER platform, NCT07871864 | Part 2 FOSTER-CabOS: cabozantinib 40 mg/m²/d (max 60) × 12 cycles vs BSC after first line, ≥4 y, n=530, phase 3, 8 European countries | RECRUITING, started 2026-10-07 |
| NCT04055220 (Léon Bérard) | regorafenib maintenance vs surveillance after first line, bone sarcomas | RECRUITING since 2020 |
| NCT04351308 (PKUPH) | poor responders: MAPI+camrelizumab vs API+apatinib vs MAPI | UNKNOWN (last update 2020) |
| NCT05926492 (Zhejiang) | surufatinib + chemo neoadjuvant | UNKNOWN |
- Chinese anlotinib/apatinib front-line trials: none on ClinicalTrials.gov beyond those listed; ChiCTR not searchable from here.
- Real-world France (262 metastatic OS, 2008–2018): time to next treatment on TKIs 7.6 / 6.0 / 4.8 months when used first / second / third line in metastatic setting, longer than chemotherapy after first line (TTNT 5.7, 3.7, 2.9 mo for lines 2–4). PMID 41017203 (abstract).

### Why not standard: synthesis (mine)
1. No randomized OS benefit; the two TKI+IE randomized trials show numerically worse OS (OLIE, OAIE).
2. Benefit is PFS of ~2 months; few patients progression-free at 12 months (CABONE 9.5%, ADVL1622 14.7%).
3. No predictive biomarker, so the drug cannot be targeted.
4. Front-line integration is toxic and slow: wound healing, growth plate, pneumothorax, combined myelosuppression; AOST2032 now suspended, CabOSTar failed to recruit.
5. No company holds an osteosarcoma indication or plans to file (no filing found); the drugs are expensive off-label.

## 6. Best testable idea (HYPOTHESIS)

**Hypothesis:** In relapsed osteosarcoma treated with a VEGFR2-directed multi-kinase inhibitor, tumours carrying a VEGF-axis amplification — VEGFA (6p21) or the KDR/PDGFRA/KIT amplicon (4q12), together about 40% of patients (PMID 31175097) — have substantially longer progression-free survival than tumours with neither (pre-specified: HR ≤0.5), and this group accounts for most patients still progression-free at 12 months.

**Why this one:** (1) every active drug shares VEGFR2; (2) the two amplicons are common, mutually exclusive, and measurable by standard panels, FISH, or low-pass whole-genome sequencing of plasma ctDNA; (3) matched PDX data (Sayles, PMC7134333) and the HCC precedent (PMID 24687604) both point this way; (4) no clinical test has been done; (5) it can be answered with samples that already exist, at low cost, and the answer changes how FOSTER-CabOS and any AOST2032 restart select or stratify patients.

**How to test (cheapest first):**
1. Retrospective: copy-number calls on archival tumour or banked baseline plasma from CABONE (n=42 OS, Bergonié), REGOBONE/SARC024 (randomized → can test interaction with placebo), ITCC-050/OLIE (Eisai/Gustave Roussy), OAIE (PKUPH), ADVL1622 (COG). Randomized arms (SARC024, REGOBONE, OLIE, OAIE) allow a treatment-by-biomarker interaction test, not just prognosis.
2. Institutional: MSK-IMPACT / Foundation-tested patients who later received regorafenib/cabozantinib (MSK already reported the subsets, PMID 31175097).
3. Prospective: stratify FOSTER-CabOS by amplicon status from diagnostic tissue; AOST2032 already banks ctDNA.

**What would falsify it:** HR for PFS in amplified vs non-amplified ≥0.8 in pooled ≥100 TKI-treated patients; or equal effect in randomized interaction test.

**Second-ranked ideas (HYPOTHESES):**
- Lung-only disease, not genotype, explains benefit (APFAO data). Test: per-lesion response analysis (lung vs bone lesions within the same patients) in existing CT series.
- Randomized TKI maintenance after complete surgical removal of lung relapse (where cures happen), with EFS at 12 months against the 20% (10–34%) benchmark and the 26–28% seen with dinutuximab/denosumab (project pooled-control report). Not yet tried.
- VEGFR TKI + FGFR inhibitor to block adaptive FGFR–ERK escape in lung metastases (bioRxiv PMID 42856637; FGFR1 amplified in 18.5% of poor responders, PMID 24861215).

## 7. Access log / limits
- Full text read via NCBI PMC efetch: PMC8763616 (CABONE AM), PMC7134333 (Sayles), PMC7223462 (APFAO), PMC12647724 (OAIE), PMC11581622 (OLIE), PMC11334773 (EU sampling paper). Europe PMC fullTextXML returned HTTP 500 this session.
- Blocked: cdn.clinicaltrials.gov (protocol PDFs), CT.gov history API (403). NCCN and ESMO full texts not read.
- SARC024 and REGOBONE subgroup analyses not read (no full text retrieved).
- Chinese registries/journals not searched.
