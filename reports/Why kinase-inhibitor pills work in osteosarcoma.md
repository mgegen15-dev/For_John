# Why VEGFR-blocking kinase-inhibitor pills work in osteosarcoma, and why they are not yet standard

*Built from trial papers (full text where open access), ClinicalTrials.gov records and preclinical studies. Last revised November 14, 2026, after an independent audit; updated November 19, 2026 (MYC, CabOSTar results, new resected-relapse benchmark; see the change log). Working notes with every source: `research_notes/Kinase inhibitors/notes.md`. Uses the same figures as the pooled control dataset (`reports/Osteosarcoma pooled control dataset.md`) and the trials landscape report.*

## Summary

Oral kinase inhibitors that block VEGFR2, the main receptor for the blood-vessel growth signal VEGF, are the most consistently active drugs in relapsed osteosarcoma, with the best evidence for regorafenib, cabozantinib, sorafenib, apatinib and lenvatinib; kinase inhibitors that do not block VEGFR2, such as imatinib, dasatinib and alisertib, have not worked. The effect looks mainly anti-vascular: lung metastases turn necrotic and hollow out, and PET scans dim within four weeks. The benefit is real but brief: in the cabozantinib trial CABONE, 33% of patients were free of progression at 6 months by the trial's own primary endpoint, and only 9.5% at 12 months by Kaplan–Meier estimate. No randomized trial has shown longer survival, and no test can yet say who will benefit. About 40% of tumours carry extra copies of VEGF-pathway genes, but no clinical study we found has checked whether those patients respond better. That check can be done with samples that already exist, and it is the single most useful next step.

**How to read the labels.** After each key number we say where it comes from:

- **(registry)**: read from the ClinicalTrials.gov record.
- **(paper, full text)**: read in the full published paper.
- **(paper, abstract only)**: read only in the abstract.
- **(press release only)**: reported by a company or the media, not in a peer-reviewed paper.
- **(our calculation)**: counted or computed by this project from the files above.
- **(preprint, abstract only)**: read only in the abstract of a preprint, which has not been peer-reviewed.

## The evidence in one table

Relapsed, measurable osteosarcoma. "PFS" means progression-free survival; "OS" means overall survival; "IE" means ifosfamide plus etoposide, the usual relapse chemotherapy.

**VEGFR-blocking pills:**

| Drug | Trial | Patients | Key result | Source |
|---|---|---|---|---|
| Regorafenib vs placebo | SARC024 (randomized) | 42 | Median PFS 3.6 vs 1.7 months, HR 0.42 (paper, abstract only); no OS difference shown, with crossover allowed | PMID 31013172 |
| Regorafenib vs placebo | REGOBONE (randomized 2:1) | 38 | Non-progressive at 8 weeks: 65% (17 of 26) vs 0% (0 of 12) (paper, abstract only) | PMID 30477937 |
| Cabozantinib | CABONE | 42 | Primary endpoint: 33% (14 of 42) free of progression at 6 months (paper, abstract only; same in registry). Kaplan–Meier PFS 71% at 4 months, 52% at 6 and **9.5% at 12**. Median OS 10.6 months; 12% (5 of 42) partial responses (paper, full text) | PMID 32078813; PMC8763616 |
| Cabozantinib, ages 2–30 | COG ADVL1622 | 29 | Response or disease control over six cycles 35%; PFS at 1 year 14.7%; OS at 1 year 35.9% (registry). We found no peer-reviewed paper | NCT02867592 |
| Apatinib | Peking University phase 2, ages 16 and older, one centre | 37 | 4-month PFS 57%; response rate 43%, investigator-assessed and including unconfirmed responses; median PFS 4.5 months (paper, abstract only) | PMID 30559126 |
| Sorafenib | Italian Sarcoma Group | 35 | 4-month PFS 46%; median PFS 4 months (paper, abstract only) | PMID 21527590 |
| Lenvatinib | ITCC-050 | 31 | 4-month PFS 29% by simple count, 38% by Kaplan–Meier (paper, full text); 32% in 28 patients in the registry; median PFS 3.0 months | PMID 34562750 |
| Anlotinib | Chinese bone-tumour trial, osteosarcoma subgroup | 29 | 3-month PFS 76%; median PFS 4.8 months (paper, full text) | PMID 35692789 |
| Lenvatinib + IE vs IE | OLIE (randomized) | 81 | PFS 6.5 vs 5.5 months, HR 0.54, not significant. OS 11.9 vs 17.4 months (HR 1.28) at the primary analysis; HR 0.93 at the final analysis (paper, full text) | PMC11581622 |
| Apatinib + IE vs IE | OAIE (randomized 2:1, China) | 81 | PFS 5.5 vs 3.4 months, HR 0.60; OS 18.1 vs 22.9 months, HR 1.48 (paper, full text). The control arm received more chemotherapy (see below) | PMC12647724 |

**Thin or negative evidence:**

| Drug | Trial | Patients | Key result | Source |
|---|---|---|---|---|
| Pazopanib | City of Hope lung-metastasis phase 2 | 8 | 3 of 8 met a composite 4-month endpoint; stopped early (paper, abstract only) | PMID 35075361 |
| Pazopanib + oral topotecan | PAZOTOP | 28 | 69.6% progression-free at 12 weeks (paper, abstract only); includes chemotherapy | PMID 34050255 |
| Sunitinib + nivolumab | IMMUNOSARC bone cohort | 17 | Median PFS 3.5 months; 1 of 17 partial response (paper, full text). No sunitinib-alone osteosarcoma cohort found | PMID 39540661 |
| Imatinib (does not block VEGFR2) | COG trial in Lagmay 2016; SARC basket trial | 12; 27 | 0% event-free at 4 months (paper, full text); 18.5% clinical benefit at 4 months (paper, abstract only) | PMID 27400942; PMID 19451433 |
| Dasatinib (does not block VEGFR2) | SARC009 | 46 | 10.9% progression-free at 6 months (registry) | NCT00464620 |
| Alisertib (aurora kinase inhibitor) | COG ADVL0921 | 10 | 0 of 10 responses (registry; paper, full text) | NCT01154816 |

**Pooled** (our calculation, from the pooled control dataset): VEGFR-blocking pills given alone leave about 52.5% of patients event-free or progression-free at four months across four trials (145 patients), using CABONE's Kaplan–Meier 4-month figure. Using CABONE's primary endpoint instead gives 41.4%. Arms without a VEGFR-blocking pill or IE average 14.2% (271 patients). IE chemotherapy alone, in the two randomized control arms, gave 42–66% (paper, full text). So VEGFR-blocking pills clearly beat other single agents, but in combination with IE they must be judged against IE, not against 12%.

**The two randomized pill + IE trials.** Neither was designed to measure survival, and their survival results do not point to a benefit:

- **OLIE.** Overall survival was numerically shorter with lenvatinib at the primary analysis (HR 1.28). At the final analysis, requested by the FDA, the arms were about equal (HR 0.93, 0.53–1.62) (paper, full text).
- **OAIE.** Survival favoured IE alone (HR 1.48, 0.76–2.89) (paper, full text). OAIE's arms also did not receive the same chemotherapy: the control arm received IE on days 1–5 of each cycle, while the apatinib arm received the same daily doses on days 1–3 only, about 40% less chemotherapy per cycle (paper, abstract only).

## 1. Why they work: which kinase matters

**What the tumours carry.** Osteosarcoma has few point mutations but many extra gene copies. Two of the commonly amplified regions hold the pills' targets, and they rarely occur together:

| Gene region | Genes | How often | Source |
|---|---|---|---|
| 6p21 | VEGFA (the vessel growth signal) | 24% (MSK, 66 patients) (paper, abstract only); 23% (Sayles, whole genomes) (paper, full text; the audit could not re-open it) | PMID 31175097; PMC7134333 |
| 4q12 | KDR (= VEGFR2), PDGFRA, KIT | 20% (MSK), with strong PDGFRA protein (paper, abstract only) | PMID 31175097 |
| 8p11 | FGFR1 | 18.5% of poor chemotherapy responders, none of the good responders (352 samples from 288 patients) (paper, abstract only) | PMID 24861215 |
| MET | MET receptor (cabozantinib target) | First cloned from an osteosarcoma cell line; drives bone-cell transformation in models; not often amplified | reviewed in PMC8763616 |

Together, at least 40% of patients have VEGFA or PDGFRA amplification in that cohort (paper, abstract only; PMID 31175097). In open TARGET-OS data from 81 patients at diagnosis, 23.5% carry a clear amplification of VEGFA, KDR, PDGFRA or KIT, and 47% by a looser threshold (our calculation; `reports/Copy-number changes and the kinase-pill biomarker.md`). VEGFA amplification is also enriched in the drug-resistant clones that come back at relapse, which is the setting where the pills are tested (8 patients; paper, abstract only; PMID 37812025).

**What the lab studies show.** Most of these were read as abstracts only and were not re-checked by the audit.

- **Matched tumour models.** A VEGFA-amplified patient-derived tumour shrank on sorafenib, twice; an unamplified one did not (Sayles 2019, PMC7134333). The authors note that VEGFR2 protein, not VEGFA protein, may be the better marker.
- **A liver-cancer precedent.** In liver cancer, VEGFA amplification marks tumours that are unusually sensitive to sorafenib (PMID 24687604). The mechanism runs through the surrounding tissue: tumour VEGF makes nearby cells release HGF, the signal for the MET receptor. If the same loop exists in osteosarcoma, it would explain why a drug that blocks both VEGFR2 and MET (cabozantinib) works. *This is a hypothesis; it has not been tested in osteosarcoma.*
- **Direct effects on tumour and bone cells.** Cabozantinib lowers ERK and AKT signalling in tumour cells and shifts the RANKL/osteoprotegerin balance in bone cells (PMID 29520051, abstract only). Sorafenib lowers ERK, MCL-1 and ezrin signalling and blocks vessel growth (PMID 20003259, abstract only).

**What patients' scans show.** The effect looks mainly anti-vascular:

- **Tumours die from the inside rather than shrink.** In CABONE, which treated both osteosarcoma and Ewing sarcoma, 12 of 90 patients had a collapsed lung: 4 with osteosarcoma and 8 with Ewing sarcoma. All had metastases near the lung surface, and seven showed hollowed-out (cavitated) metastases from drug-induced necrosis. One responder had lung metastases removed, and no live tumour was left (paper, full text; PMC8763616).
- **PET scans respond fast.** 65% (20 of 31) of evaluable CABONE osteosarcoma patients had a partial metabolic response after one 4-week cycle. They stayed progression-free longer: median 7.2 months, against 1.8 months for those whose PET worsened (paper, full text; PMC8763616).
- **Signs of strong VEGFR blockade go with benefit.** With apatinib, patients who got high blood pressure, poor appetite or an underactive thyroid did better (PMID 32021426, abstract only).
- **The most selective drug is among the most active.** Apatinib, the most VEGFR2-selective of these drugs, reported a 43% response rate (PMID 30559126). That figure comes from a single centre, was investigator-assessed and includes unconfirmed responses. It is not directly comparable with CABONE's centrally reviewed 12%. *Our reading: VEGFR2 blockade may be enough for most of the effect, and the extra targets (MET, FGFR, PDGFR, RAF) may add to it. This rests on cross-trial comparison, not a head-to-head test.*

**Immune effect: unproven.** Adding a PD-1 antibody to apatinib (APFAO) did not reach its 6-month target (paper, full text; PMC7223462). A retrospective series of cabozantinib with or without checkpoint inhibitors, across all sarcomas, found no difference (PMID 43020951, abstract only). Lab work shows apatinib lowers PD-L1 on osteosarcoma cells (PMID 29225166), but no clinical immune benefit has been shown.

## 2. Who responds

No marker has been validated. A 2024 European paper on tissue sampling states it plainly: "despite responses in up to 40% of patients, there are as yet no validated predicted biomarkers and the TKI mechanism of action remains obscure" (paper, full text; PMC11334773). The leads all come from small exploratory analyses:

| Lead | What was seen | Strength | Source |
|---|---|---|---|
| **Lung-only disease** | Apatinib + PD-1 antibody: median PFS 6.9 months with lung-only disease vs 2.1 months with bone or soft-tissue lesions only; lesion site was the only independent factor (paper, full text) | Moderate, consistent across reports | PMC7223462; OAIE authors' comment, PMC12647724; PMID 39030807 |
| **Early PET response** | CABONE: response after one cycle predicted PFS (p<0.0001) (paper, full text) | Moderate, but it is an early-response marker, not a selection test | PMC8763616 |
| Blood VEGF-A and soluble MET | CABONE: low VEGF-A went with longer survival (13.2 vs 8.2 months); high soluble MET went with longer PFS (7.8 vs 5.4) (paper, full text) | Weak (36 patients, many tests) | PMC8763616 |
| Tumour PD-L1 ≥5% | Longer PFS on apatinib + PD-1 antibody (p=0.004); only 6 of 28 positive (paper, full text) | Weak | PMC7223462 |
| Side effects | High blood pressure, anorexia and thyroid changes linked to benefit (paper, abstract only) | Weak, and only known after treatment starts | PMID 32021426 |
| Inherited VEGFR2 variant | One genotype linked to longer PFS (5.0 vs 3.1 months) on apatinib (paper, abstract only) | Weak, retrospective | PMID 32215805 |
| Earlier use | OLIE: larger gap in patients with no prior ifosfamide or one prior line (paper, full text). French real-world data: disease stays controlled longer when pills are used earlier, 7.6 months as first treatment for metastatic disease vs 4.8 as third (paper, abstract only) | Weak | PMC11581622; PMID 41017203 |
| Tumour VEGFA, KDR, PDGFRA, FGFR1 or MET amplification | **Not tested in patients in any study we found.** Only lab and liver-cancer evidence | None in patients | — |

**Age.** A Canadian real-world series found no link between age and benefit (PMID 37724607, abstract only). Children and young adults benefit in a similar range to adults: ITCC-050, ADVL1622, and a Japanese series in patients with a median age of 17 (PMID 37073613, abstract only).

We could not read the subgroup analyses of SARC024 or REGOBONE (no open full text), so they are not included here.

## 3. Why the benefit does not last

**The numbers.** In CABONE, progression-free survival fell from 71% at 4 months to 9.5% at 12 months by Kaplan–Meier estimate. By the trial's own primary endpoint, 33% were free of progression at 6 months (paper, full text). In COG's ADVL1622, 14.7% of children and young adults were progression-free at one year (registry). Median progression-free survival on any single pill is 3 to 7 months.

**Survival.** No randomized trial has shown that these pills help patients live longer:

- **SARC024 and REGOBONE** let placebo patients switch to the drug on progression; 10 of 20 and 10 of 12 did (paper, abstract only; the SARC024 registry participant flow records 11 crossovers). Crossover hides any survival effect.
- **OLIE.** 12-month survival was 49% with lenvatinib + IE against 72% with IE alone (registry), with HR 1.28 at the primary analysis. At the final analysis requested by the FDA, the hazard ratio was 0.93 (0.53–1.62), so no difference (paper, full text). The authors note that more patients in the IE arm went on to surgery or later treatment.
- **OAIE.** Median survival was 18.1 months with apatinib + IE against 22.9 months with IE alone (HR 1.48). In the apatinib arm, 30% received no further treatment, against 19% in the IE arm (paper, full text). The IE-alone arm also received more chemotherapy per cycle (days 1–5 against days 1–3).

*Possible explanations (hypotheses):*

- the tumour grows back faster once vessel blockade stops;
- patients who used the pill earlier have fewer good options left, or are less fit for later treatment;
- in OAIE, the control arm's extra chemotherapy;
- or chance, since neither trial was built to measure survival.

Pooling patient-level data from the two trials could tell these apart.

**What is known about resistance.**

| Mechanism | Evidence | Type |
|---|---|---|
| Bone lesions resist; lung lesions respond | APFAO, OAIE commentary | Clinical observation |
| Progression after chemotherapy stops | Almost all progressions in ITCC-050 came after IE ended, as reported by the OAIE authors | Clinical observation |
| mTORC2 switched on after sorafenib | Basis for adding everolimus, which then missed its trial target (6-month PFS 45%, target 50%) | Lab, then clinical (PMID 23434734, 25498219) |
| FGFR–ERK signalling switched on at the tumour–lung border when nearby tumour cells die | Live lung-metastasis models; blocked by an FGFR inhibitor or pazopanib | Lab, preprint (bioRxiv 2026, not peer reviewed; indexed in PubMed as PMID 42856637; abstract only) |
| PTEN loss and MAPK reactivation; IL-6/STAT3; others | Anlotinib-resistant cell lines | Lab only (PMID 35318116, 37404767, 38532893) |
| Resistant clones with MYC, CCNE1, VEGFA, IGF1R amplification | Whole genomes of relapses (8 patients) | Clinical genomics, not specific to pills (PMID 37812025) |
| MYC-driven tumour cells resist cabozantinib | Cell lines from MYC-hyperactivated mouse osteosarcomas needed about 8 times more cabozantinib to be inhibited than p53-driven lines (mean IC50 5.51 against 0.65 µM; fold change our calculation). In mice, cabozantinib-containing regimens still delayed progression of MYC-driven tumours compared with no treatment | Lab, preprint (Kappa et al., bioRxiv, September 2026, [doi 10.64898/2026.09.21.753033](https://doi.org/10.64898/2026.09.21.753033); preprint, abstract only) |

**Missing:** we found no study that biopsied osteosarcoma at the moment of progression on a pill to see what changed. This is a gap.

## 4. Combinations

**Tried, with results:**

| Combination | Result | Source |
|---|---|---|
| Sorafenib + everolimus (mTOR blocker) | 6-month PFS 45%; missed its 50% target (paper, abstract only) | PMID 25498219 |
| Lenvatinib + IE (OLIE, randomized) | PFS gain (HR 0.54), not significant; no survival gain at the final analysis (HR 0.93) (paper, full text) | PMC11581622 |
| Apatinib + IE (OAIE, randomized) | PFS gain (HR 0.60); survival favoured IE alone (HR 1.48); the control arm received IE on days 1–5, the apatinib arm on days 1–3 (paper, full text and abstract) | PMC12647724; PMID 41290609 |
| Apatinib + camrelizumab (PD-1 antibody) | 6-month PFS 51%; missed its 60% target (paper, full text) | PMC7223462 |
| Sunitinib + nivolumab (IMMUNOSARC) | Median PFS 3.5 months in 17 osteosarcoma patients (paper, full text) | PMID 39540661 |
| Cabozantinib + topotecan/cyclophosphamide | Too toxic when given at the same time; cabozantinib tolerated only on days 8–21 (paper, abstract only) | PMID 37715723 |

**Running, no results yet** (registry, 14 November 2026):

- regorafenib + nivolumab (SARC038, NCT04803877, active, not recruiting);
- cabozantinib + atezolizumab (NCT05019703);
- cabozantinib + pembrolizumab (NCT05182164);
- cabozantinib + ifosfamide (NCT06156410);
- sunitinib + losartan, which blocks monocyte recruitment (NCT03900793). A similar pill with losartan gave a 50% clinical benefit rate in 28 pet dogs with lung metastases (paper, abstract only; PMID 34580111);
- lenvatinib + everolimus against everolimus (NCT07619950, not yet open);
- several apatinib combinations in China.

**Rational combinations not yet tried in patients.** Based on ClinicalTrials.gov searches on 14 November 2026; other registries were not searched.

- **Pill + selective FGFR blocker.** No trial found. Supported by the FGFR–ERK escape preprint and by FGFR1 amplification in 18.5% of poor chemotherapy responders.
- **Pill + selective MET blocker** (capmatinib, tepotinib, savolitinib). No trial found. Pazopanib + crizotinib was synergistic in cell and mouse models (PMID 38423639).
- **Pill + FAK blocker** (defactinib). No osteosarcoma trial found outside a basket study.
- **Pill + PI3K or IL-6 receptor blockers**, from the anlotinib-resistance work. No trial found.
- **Biomarker-selected pill trial** (VEGFA- or 4q12-amplified tumours). None found.
- **Pill maintenance after complete surgical removal of a relapse.** No randomized trial found. This is the setting where cures still happen, and the pooled control dataset gives ready comparators:
  - the COG AOST0221 benchmark: 20% event-free at 12 months, 95% CI 10–34%, from one 42-patient trial (paper, full text);
  - 26–28% with dinutuximab or denosumab (registry);
  - a November 2026 COG update of the AOST0221 benchmark: 22% event-free at 12 months (95% CI 15–31%) in 99 patients from three COG phase 2 trials (preprint, abstract only; doi 10.64898/2026.11.13.26368045).

  The nearest trials test maintenance after *first-line* treatment instead: FOSTER-CabOS, CabOSTar, and a French trial (NCT04055220) that randomizes regorafenib maintenance against observation.

## 5. Why they are not standard care

**Guidelines and labels.**

- **US NCCN guidelines** list regorafenib and sorafenib among second-line options for osteosarcoma, with cabozantinib and sorafenib + everolimus as "additional" options. This comes secondhand, from version 3.2023 as quoted in a trial protocol. We could not read the current NCCN document, and the audit could not verify it. The apatinib trial paper also says the class entered NCCN guidelines as second-line therapy (PMID 30559126).
- **The 2021 European guideline** (ESMO and partners, PMID 34500044) discusses cabozantinib and regorafenib. We could not read its exact recommendation grades (not verified).
- **Approvals.** We found no regulatory approval of any of these drugs for osteosarcoma. Cabozantinib is FDA-approved from age 12 for thyroid and neuroendocrine cancers, so a paediatric dose exists: 40 mg under 40 kg, 60 mg above (FDA label; [FDA](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-cabozantinib-adults-and-pediatric-patients-12-years-age-and-older-pnet-and-epnet)). Apatinib and anlotinib are sold mainly in China.

**Cost.** Use is off-label and expensive. Cabozantinib's US cash price is roughly US$26,000–48,000 for 30 tablets, depending on the source ([drugs.com](https://www.drugs.com/price-guide/cabometyx), [WebMDRx](https://www.webmdrx.com/drug-prices/cabometyx)). The NHS indicative price is £5,143 per 30 × 60 mg tablets ([NHSBSA](https://dmd-browser.nhsbsa.nhs.uk/ampp/view/156345)). These are list or cash prices taken from price sites, not re-checked by the audit, and not what health systems actually pay.

**Children.**

| Issue | Evidence | Source |
|---|---|---|
| Growth plates | 5 of 53 children (9.4%) on anti-vessel drugs in COG phase 1 trials had growth-plate widening (1 on sunitinib, 4 on pazopanib); it reversed after stopping (paper, abstract only). Growth-plate damage is a standard finding in animal studies | PMID 25257751; PMID 27162053 |
| Wound healing near surgery | Apatinib: severe wound breakdown in 11% (4 of 37) (paper, abstract only). AOST2032 leaves out cabozantinib in the first chemotherapy cycle after surgery and tracks port-site wound problems (registry) | PMID 30559126; NCT05691478 |
| Collapsed lung | Cabozantinib: grade 3–4 in 9% (4 of 45) of osteosarcoma patients; any grade 13% (12 of 90) across all CABONE patients (paper, full text). Lenvatinib + IE: 18% treatment-related, 28% from any cause (paper, full text). Apatinib: grade 3–4 in 16% (paper, abstract only) | PMC8763616; PMC11581622; PMID 30559126 |
| Blood pressure, kidney, skin | Dose-limiting in children at higher cabozantinib doses; side effects at every dose level (paper, abstract only) | PMID 29693796 |
| Formulation | Cabozantinib comes only as tablets (no liquid found); lenvatinib capsules can be dispersed in water or apple juice ([label summary](https://drugs.com/dosage/lenvima.html)) | — |

**Front-line and maintenance trials, status on 14 November 2026** (registry):

| Trial | Question | Status |
|---|---|---|
| COG AOST2032 (NCT05691478) | Cabozantinib added to MAP chemotherapy, then 6 months of cabozantinib alone, in newly diagnosed patients; 1,122 planned | **Suspended.** Reason given: "Extend the observation period for current patients" (updated 27 October 2026). The dose-finding part closed in May 2025. We found no public explanation; some hospital pages still list it as recruiting |
| Ipsen CabOSTar (NCT06341712) | Cabozantinib vs supportive care for residual disease after first-line treatment | **Terminated** after 10 patients (November 2024 – February 2026) for recruitment problems. Results posted 29 October 2026 contain **no efficacy data**: every efficacy outcome says the planned analyses "were not performed as the study was terminated early"; only adverse events are reported, for 5 patients on cabozantinib and 3 on supportive care alone (registry, 19 November 2026) |
| FOSTER-CabOS, part of the FOSTER platform (NCT07871864) | 12 cycles (about 12 months) of cabozantinib vs supportive care after first-line treatment, 8 European countries. The 530 planned patients are for the whole FOSTER platform, not FOSTER-CabOS alone | **Recruiting** since 7 October 2026 |
| Léon Bérard (NCT04055220) | Regorafenib maintenance vs observation after first-line treatment, bone sarcomas, 168 planned | Recruiting since 2020 |
| Peking University (NCT04351308) | Apatinib or PD-1 antibody added for poor responders at diagnosis | Status unknown since 2020 |

**Our summary of why the class is stuck:**

- The gain is about two months of disease control (our calculation: median PFS gains of 1.9 months in SARC024, 1.0 in OLIE and 2.1 in OAIE).
- No survival gain has been shown.
- There is no test to pick responders.
- The drugs are hard to combine with surgery and intensive chemotherapy in growing children.
- The main US front-line trial is paused, and an industry maintenance trial could not recruit.
- We found no company seeking an osteosarcoma licence.

## 6. The best testable idea

**Hypothesis.** In relapsed osteosarcoma treated with a VEGFR2-blocking pill, tumours with extra copies of VEGFA (6p21) or of the KDR/PDGFRA/KIT region (4q12) stay progression-free substantially longer than tumours with neither. Together these two groups are about 40% of patients. A fair pre-set threshold would be a hazard ratio of 0.5 or lower. If true, this group should also account for most patients still progression-free at 12 months.

**Why this idea.**

- Every consistently active drug blocks VEGFR2, and these two amplifications put more of the drug's target pathway into the tumour.
- A matched patient-derived tumour model and the liver-cancer precedent both point the same way.
- We found no study that has tested it in patients.
- It can be answered cheaply with tissue or banked blood from trials already done. Gene copy number can be read from routine sequencing panels, from FISH, or from low-coverage sequencing of tumour DNA in blood. AOST2032 already banks blood for tumour DNA.
- The answer would change how FOSTER-CabOS, and AOST2032 if it restarts, select or stratify patients.

**How to test it, cheapest first.**

1. **Use archived samples from the randomized trials** (SARC024, REGOBONE, OLIE, OAIE). Randomized trials allow the real test: does the amplification predict benefit *from the drug*, compared with placebo or chemotherapy alone, rather than just better outcomes in general? Add single-arm cohorts (CABONE, ADVL1622, ITCC-050) for the 12-month question.
2. **Use centres that routinely sequence tumours** to look back at their patients who later received regorafenib or cabozantinib. For example, MSK reported the two subsets.
3. **Stratify new trials** by amplicon status from diagnostic tissue.

**Record MYC status as well.** Any amplification test should record MYC copy number as a variable alongside VEGFA and 4q12, for three reasons. MYC (8q24) is amplified in 26 of 81 TARGET-OS tumours (32.1%; our calculation, `reports/Copy-number changes and the kinase-pill biomarker.md`). In 105 children and young adults, MYC amplification (more than 7 copies, 16% of patients) went with 3-year overall survival of 27% against 74% (adjusted HR 3.4), independent of metastatic status (paper, abstract only; *Cancer* 2025, PMID 41199591). And MYC-driven mouse osteosarcoma cells resisted cabozantinib in the laboratory (preprint, abstract only; see the resistance table). If MYC-amplified tumours do worse on a pill, or MYC amplification co-occurs with VEGFA or 4q12 amplification in some tumours, leaving it out could hide or fake a VEGFA or 4q12 effect (our inference).

**What would disprove it.** Either of these:

- among 100 or more pooled patients treated with a pill, a hazard ratio of 0.8 or above for amplified against non-amplified tumours;
- no difference in the drug-versus-control comparison in the randomized trials.

**Runner-up ideas (also hypotheses).**

- **Site, not genes, explains benefit.** Compare lung and bone lesions *within the same patients* on existing trial scans.
- **Pill maintenance after lung relapse surgery.** A randomized trial of pill maintenance after complete surgical removal of a lung relapse, judged against the resected-relapse arms in the pooled control dataset.
- **Pill plus an FGFR blocker**, to stop the FGFR–ERK escape seen at the tumour–lung border.

## Limits

- **Most biomarker findings are exploratory.** They come from single trials of 28–105 patients, with many tests and no correction for multiple comparisons.
- **Several sources were read only as abstracts.** These include REGOBONE, SARC024, the sorafenib trials and most lab studies, and each is labelled above. Most preclinical papers were not re-checked by the audit. The Europe PMC full-text service returned errors this session; full texts came from PMC where open.
- **Guideline wording is secondhand.** The NCCN and ESMO wording came from a trial-protocol quote found by web search. Protocol PDFs on cdn.clinicaltrials.gov could not be reached from this workspace.
- **AOST2032.** The reason it was suspended is only the one-line registry entry; we found no public statement.
- **Searches not done.** Chinese trial registries and Chinese-language journals were not searched, so front-line apatinib or anlotinib work registered only in China may be missing. "No trial found" statements cover ClinicalTrials.gov only.
- **Comparisons are rough.** Cross-trial comparisons mix drugs, doses, ages, endpoints and lines of therapy. Prices are cash or list prices.
- **ADVL1622.** The osteosarcoma results come from registry postings; we found no peer-reviewed paper.

## Next steps

1. **Ask the CABONE, REGOBONE, SARC024 and OLIE teams** whether baseline tumour or plasma samples exist with copy-number data. These are Institut Bergonié, the French Sarcoma Group, SARC, and Eisai/ITCC. A pooled amplicon-versus-outcome analysis is the cheapest decisive test.
2. **Ask COG** what "extend the observation period" means for AOST2032, and whether its circulating tumour DNA samples could be used for the amplicon question.
3. **Ask COG for the ADVL1622 definition of "disease control"**, so the cohort can enter the pooled 4-month table.
4. **Re-read the SARC024 and REGOBONE full texts** when access allows, for subgroup data.

## Change log

**November 19, 2026.** Updated from the new-evidence scan (`reports/Whats new in osteosarcoma research.md`).

- **MYC added to the amplification test (section 6) and to the resistance table:** 32.1% of TARGET-OS tumours amplified (our calculation, copy-number report); MYC amplification predicts poor survival (Cancer 2025, PMID 41199591; paper, abstract only); MYC-driven mouse osteosarcoma lines resisted cabozantinib in vitro (bioRxiv 2026; preprint, abstract only).
- **CabOSTar:** its posted results (29 October 2026) contain no efficacy data (registry).
- **Resected-relapse comparators:** the COG 99-patient update (22%, 95% CI 15–31%) added beside the AOST0221 benchmark, which is kept.
- **New label (preprint, abstract only):** read only in a preprint's abstract; preprints are not peer-reviewed.

**November 13–14, 2026.** The report was revised after an independent audit (`research_notes/Audit/audit_B_trials_controls_pills.md`).

- **Title and summary narrowed** from "kinase-inhibitor pills" to VEGFR2-blocking kinase inhibitors. Imatinib, dasatinib and alisertib, which do not block VEGFR2, did not work. The evidence for sunitinib (only with nivolumab) and pazopanib (8 patients, or with topotecan) is thin. Both points are now in a separate table, and the claim that eight drugs form "the only class that clearly works" was removed.
- **CABONE framing unified with the pooled report.** The trial's primary endpoint (33% free of progression at 6 months) is now stated alongside the Kaplan–Meier 71% at 4 months. The pooled pill-alone rate is given as 52.5% (Kaplan–Meier) and 41.4% (primary endpoint).
- **Survival in the randomized trials.** "Overall survival was numerically shorter in both pill arms" was corrected: OLIE's final analysis gave HR 0.93 (no difference), after HR 1.28 at the primary analysis.
- **OAIE dosing difference corrected.** The control arm received IE on days 1–5, the apatinib arm on days 1–3. The earlier text said "lower ifosfamide dose given for longer".
- **"Range 10–34%" corrected** to the 95% confidence interval of one 42-patient trial (AOST0221).
- **Apatinib's 43% response rate** is now flagged as single-centre, investigator-assessed and including unconfirmed responses, and no longer called "the highest".
- **CABONE collapsed lung.** The 12 of 90 patients are now split by disease (4 osteosarcoma, 8 Ewing sarcoma). The collapsed-lung row now separates grade 3–4 from any grade.
- **FOSTER-CabOS.** The 530 planned patients are now attributed to the whole FOSTER platform.
- **Unverified claims marked:** NCCN and ESMO guideline wording, prices, Sayles 2019 figures and preclinical papers. The FGFR–ERK source is labelled a preprint indexed in PubMed.
- **Absolute statements softened** to "we found no…" where they rest on our own searches.
- **Next step "add ADVL1622 and OLIE/OAIE survival to the pooled dataset"** replaced; that has been done.
