# Why kinase-inhibitor pills work in osteosarcoma, and why they are not yet standard

*Built on November 14, 2026 from trial papers (full text where open access), ClinicalTrials.gov records and preclinical studies. Working notes with every source: `research_notes/Kinase inhibitors/notes.md`. Builds on the pooled control dataset (`reports/Osteosarcoma pooled control dataset.md`) and the trials landscape report; their numbers are not re-derived here.*

## Summary

Eight oral multi-kinase inhibitors (cabozantinib, regorafenib, sorafenib, lenvatinib, apatinib, anlotinib, pazopanib, sunitinib) are the only drug class that clearly keeps relapsed osteosarcoma in check better than older drugs. The one thing all of them share is blocking VEGFR2, the main receptor for the blood-vessel growth signal VEGF. The clinical picture points mainly to an attack on the tumour's blood supply: lung metastases turn necrotic and hollow out, sometimes collapsing a lung, and PET scans dim within four weeks. The benefit is real but brief. In the cabozantinib trial CABONE, 71% of patients were progression-free at 4 months but only 9.5% at 12 months. In the two randomized trials that added a pill to standard relapse chemotherapy, the pill delayed progression, yet overall survival was numerically *shorter* in the pill arms. No test can yet say who will benefit. Patients with lung-only disease seem to do best, and about 40% of tumours carry extra copies of VEGF-pathway genes, but no clinical study has checked whether those patients respond better. That check is the single most useful next step, and it can be done with samples that already exist.

## The evidence in one table

Relapsed, measurable osteosarcoma. "PFS" means progression-free survival.

| Drug | Trial | Patients | Key result | Source |
|---|---|---|---|---|
| Regorafenib vs placebo | SARC024 (randomized) | 42 | Median PFS 3.6 vs 1.7 months, HR 0.42; no OS difference (crossover allowed) | PMID 31013172 |
| Regorafenib vs placebo | REGOBONE (randomized 2:1) | 38 | Non-progressive at 8 weeks: 65% vs 0% | PMID 30477937 |
| Cabozantinib | CABONE | 42 | PFS 71% at 4 months, 52% at 6, **9.5% at 12**; median OS 10.6 months; 12% partial responses | PMC8763616 |
| Cabozantinib, ages 2–30 | COG ADVL1622 | 29 | Response or disease control 35%; PFS at 1 year 14.7%; OS at 1 year 35.9% (registry results, no paper found) | NCT02867592 |
| Apatinib | Peking University phase 2 | 37 | 4-month PFS 57%; response rate 43%; median PFS 4.5 months | PMID 30559126 |
| Sorafenib | Italian Sarcoma Group | 35 | 4-month PFS 46%; median PFS 4 months | PMID 21527590 |
| Lenvatinib | ITCC-050 | 31 | 4-month PFS 29–38%; median PFS 3.0 months | PMID 34562750 |
| Lenvatinib + IE vs IE | OLIE (randomized) | 81 | PFS 6.5 vs 5.5 months, HR 0.54, not significant; OS 11.9 vs 17.4 months | PMC11581622 |
| Apatinib + IE vs IE | OAIE (randomized, China) | 81 | PFS 5.5 vs 3.4 months, HR 0.60; OS 18.1 vs 22.9 months, HR 1.48 | PMC12647724 |

IE = ifosfamide plus etoposide, the usual relapse chemotherapy. Neither randomized combination trial was designed to measure survival, so the survival gap may be chance. Still, both point the same way.

## 1. Why they work: which kinase matters

**What the tumours carry.** Osteosarcoma has few point mutations but many extra gene copies. Two of the commonly amplified regions hold the pills' targets, and they rarely occur together:

| Gene region | Genes | How often | Source |
|---|---|---|---|
| 6p21 | VEGFA (the vessel growth signal) | 24% (MSK, 66 patients); 23% (Sayles, whole genomes) | PMID 31175097; PMC7134333 |
| 4q12 | KDR (= VEGFR2), PDGFRA, KIT | 20% (MSK), with strong PDGFRA protein | PMID 31175097 |
| 8p11 | FGFR1 | 18.5% of poor chemotherapy responders, none of the good responders (352 samples) | PMID 24861215 |
| MET | MET receptor (cabozantinib target) | First cloned from an osteosarcoma cell line; drives bone-cell transformation in models (not amplified often) | reviewed in PMC8763616 |

Together, at least 40% of patients have VEGFA or PDGFRA amplification (PMID 31175097). VEGFA amplification is also enriched in the drug-resistant clones that come back at relapse (PMID 37812025), which is the setting where the pills are tested.

**What the lab studies show.**
- A VEGFA-amplified patient-derived tumour shrank on sorafenib, twice; an unamplified one did not (Sayles 2019, PMC7134333). The authors note that VEGFR2 protein, not VEGFA protein, may be the better marker.
- In liver cancer, VEGFA amplification marks tumours that are unusually sensitive to sorafenib. The mechanism runs through the surrounding tissue: tumour VEGF makes nearby cells release HGF, the signal for the MET receptor (PMID 24687604). If the same loop exists in osteosarcoma, it would explain why a drug that blocks both VEGFR2 and MET (cabozantinib) works. *This is a hypothesis; it has not been tested in osteosarcoma.*
- Cabozantinib also acts on tumour cells directly (lower ERK and AKT signalling) and on bone cells, shifting the RANKL/osteoprotegerin balance (PMID 29520051, abstract only). Sorafenib lowers ERK, MCL-1 and ezrin signalling and blocks vessel growth (PMID 20003259, abstract only).

**What patients' scans show.** The effect looks mainly anti-vascular:
- Tumours die from the inside rather than shrink. In CABONE, 12 of 90 patients had a collapsed lung; all had metastases near the lung surface, and seven showed hollowed-out (cavitated) metastases from drug-induced necrosis. One responder had lung metastases removed and no live tumour was left (PMC8763616).
- PET scans respond fast: 65% of evaluable CABONE osteosarcoma patients had a partial metabolic response after one 4-week cycle, and they stayed progression-free longer (median 7.2 vs 1.8 months for those whose PET worsened; PMC8763616).
- With apatinib, the patients who got high blood pressure, poor appetite or underactive thyroid (classic signs of strong VEGFR blockade) did better (PMID 32021426, abstract only).
- Apatinib, the most VEGFR2-selective of the eight drugs, gave the highest response rate (43%; PMID 30559126). *Our reading: VEGFR2 blockade alone is enough for most of the effect; the extra targets (MET, FGFR, PDGFR, RAF) may add to it but are not required.*

**Immune effect: unproven.** Adding a PD-1 antibody to apatinib (APFAO) did not reach its target, and a retrospective series of cabozantinib with or without checkpoint inhibitors found no difference (PMC7223462; PMID 43020951). Lab work shows apatinib lowers PD-L1 on osteosarcoma cells (PMID 29225166), but no clinical immune benefit has been shown.

## 2. Who responds

No marker has been validated. A 2024 European paper on tissue sampling states it plainly: "despite responses in up to 40% of patients, there are as yet no validated predicted biomarkers and the TKI mechanism of action remains obscure" (PMC11334773). The leads, all from small exploratory analyses:

| Lead | What was seen | Strength | Source |
|---|---|---|---|
| **Lung-only disease** | Apatinib + PD-1 antibody: median PFS 6.9 months with lung-only disease vs 2.1 months with bone/soft-tissue lesions only; lesion site was the only independent factor | Moderate, consistent across reports | PMC7223462; OAIE authors' comment, PMC12647724; PMID 39030807 |
| **Early PET response** | CABONE: response after one cycle predicted PFS (p<0.0001) | Moderate, but it is an early-response marker, not a selection test | PMC8763616 |
| Blood VEGF-A and soluble MET | CABONE: low VEGF-A → longer survival (13.2 vs 8.2 months); high soluble MET → longer PFS (7.8 vs 5.4) | Weak (36 patients, many tests) | PMC8763616 |
| Tumour PD-L1 ≥5% | Longer PFS on apatinib + PD-1 antibody (p=0.004); only 6 of 28 positive | Weak | PMC7223462 |
| Side effects | High blood pressure, anorexia, thyroid changes linked to benefit | Weak, and only known after treatment starts | PMID 32021426 |
| Inherited VEGFR2 variant | One genotype linked to longer PFS (5.0 vs 3.1 months) on apatinib | Weak, retrospective | PMID 32215805 |
| Earlier use | OLIE: larger gap in patients with no prior ifosfamide or one prior line; French real-world data: pills keep disease controlled longer when used earlier (7.6 months first line vs 4.8 third) | Weak | PMC11581622; PMID 41017203 |
| Tumour VEGFA, KDR, PDGFRA, FGFR1 or MET amplification | **Never tested in patients.** Only lab and liver-cancer evidence | None in patients | — |

**Age:** a Canadian real-world series found no link between age and benefit (PMID 37724607). Children and young adults benefit in the same range as adults (ITCC-050, ADVL1622; Japanese series in patients with a median age of 17, PMID 37073613).

We could not read the subgroup analyses of SARC024 or REGOBONE (no open full text), so they are not included here.

## 3. Why the benefit does not last

**The numbers.** In CABONE, progression-free survival fell from 71% at 4 months to 9.5% at 12 months. In COG's ADVL1622, 14.7% of children and young adults were progression-free at one year. Median progression-free survival on any single pill is 3 to 7 months.

**Survival.** No trial has shown that these pills help patients live longer:
- SARC024 and REGOBONE let placebo patients switch to the drug on progression (10 of 20 and 10 of 12 did), which hides any survival effect (PMID 31013172, 30477937).
- In OLIE, 12-month survival was 49% with lenvatinib + IE against 72% with IE alone (HR 1.28). At the final analysis requested by the FDA, the hazard ratio was 0.93 (PMC11581622). The authors note that more patients in the IE arm went on to surgery or later treatment.
- In OAIE, median survival was 18.1 months with apatinib + IE against 22.9 months with IE alone (HR 1.48). In the apatinib arm, 30% received no further treatment, against 19% in the IE arm (PMC12647724).

*Possible explanations (hypotheses):* the tumour grows back faster once vessel blockade stops; patients who used the pill earlier have fewer good options or are less fit for later treatment; or chance, since neither trial was built to measure survival. Pooling patient-level data from the two trials could tell these apart.

**What is known about resistance.**

| Mechanism | Evidence | Type |
|---|---|---|
| Bone lesions resist; lung lesions respond | APFAO, OAIE commentary | Clinical observation |
| Progression after chemotherapy stops | Almost all progressions in ITCC-050 came after IE ended (as reported by OAIE authors) | Clinical observation |
| mTORC2 switched on after sorafenib | Basis for adding everolimus, which then missed its trial target (6-month PFS 45%, target 50%) | Lab, then clinical (PMID 23434734, 25498219) |
| FGFR–ERK signalling switched on at the tumour–lung border when nearby tumour cells die | Live lung-metastasis models; blocked by an FGFR inhibitor or pazopanib | Lab, preprint (PMID 42856637) |
| PTEN loss and MAPK reactivation; IL-6/STAT3; others | Anlotinib-resistant cell lines | Lab only (PMID 35318116, 37404767, 38532893) |
| Resistant clones with MYC, CCNE1, VEGFA, IGF1R amplification | Whole genomes of relapses (8 patients) | Clinical genomics, not specific to pills (PMID 37812025) |

**Missing:** no study has biopsied osteosarcoma at the moment of progression on a pill to see what changed. This is a gap.

## 4. Combinations

**Tried, with results:**

| Combination | Result | Source |
|---|---|---|
| Sorafenib + everolimus (mTOR blocker) | 6-month PFS 45%; missed its 50% target | PMID 25498219 |
| Lenvatinib + IE (OLIE, randomized) | Small PFS gain (HR 0.54), not significant | PMC11581622 |
| Apatinib + IE (OAIE, randomized) | PFS gain (HR 0.60), significant; lower ifosfamide dose given for longer | PMC12647724 |
| Apatinib + camrelizumab (PD-1 antibody) | 6-month PFS 51%; missed its 60% target | PMC7223462 |
| Cabozantinib + topotecan/cyclophosphamide | Given at the same time, too toxic; cabozantinib only on days 8–21 tolerated | PMID 37715723 |

**Running, no results yet:** regorafenib + nivolumab (SARC038, NCT04803877, active, not recruiting); cabozantinib + atezolizumab (NCT05019703); cabozantinib + pembrolizumab (NCT05182164); cabozantinib + ifosfamide (NCT06156410); sunitinib + losartan, which blocks monocyte recruitment and gave a 50% clinical benefit rate with a similar pill in 28 pet dogs with lung metastases (NCT03900793; PMID 34580111); lenvatinib + everolimus against everolimus (NCT07619950, not yet open); several apatinib combinations in China.

**Rational combinations not yet tried in patients** (ClinicalTrials.gov searches, 14 November 2026):
- **Pill + selective FGFR blocker.** No trial. Supported by the FGFR–ERK escape preprint and by FGFR1 amplification in 18.5% of poor chemotherapy responders.
- **Pill + selective MET blocker** (capmatinib, tepotinib, savolitinib). No trial. Pazopanib + crizotinib was synergistic in cell and mouse models (PMID 38423639).
- **Pill + FAK blocker** (defactinib). No osteosarcoma trial outside a basket study.
- **Pill + PI3K or IL-6 receptor blockers**, from the anlotinib-resistance work. No trial.
- **Biomarker-selected pill trial** (VEGFA- or 4q12-amplified tumours). None found.
- **Pill maintenance after complete surgical removal of a relapse.** No randomized trial found. This is the setting where cures still happen, and the project's pooled controls give a ready benchmark (20% event-free at 12 months, range 10–34%; 26–28% with dinutuximab or denosumab). FOSTER-CabOS and CabOSTar test maintenance after *first-line* treatment; a French trial (NCT04055220) randomizes regorafenib maintenance against observation after first-line treatment.

## 5. Why they are not standard care

**Guidelines and labels.**
- US NCCN guidelines list regorafenib and sorafenib among second-line options for osteosarcoma, with cabozantinib and sorafenib + everolimus as "additional" options. This is from version 3.2023 as quoted in a trial protocol; we could not read the current NCCN document. The apatinib trial paper also says the class entered NCCN guidelines as second-line therapy (PMID 30559126).
- The 2021 European guideline (ESMO and partners, PMID 34500044) discusses cabozantinib and regorafenib; we could not read its exact recommendation grades.
- No regulator has approved any of these drugs for osteosarcoma. Cabozantinib is FDA-approved from age 12 for thyroid and neuroendocrine cancers, so a paediatric dose exists (40 mg under 40 kg, 60 mg above; [FDA](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-cabozantinib-adults-and-pediatric-patients-12-years-age-and-older-pnet-and-epnet)). Apatinib and anlotinib are sold mainly in China.

**Cost.** Use is off-label and expensive. Cabozantinib's US cash price is roughly US$26,000–48,000 for 30 tablets depending on the source ([drugs.com](https://www.drugs.com/price-guide/cabometyx), [WebMDRx](https://www.webmdrx.com/drug-prices/cabometyx)); the NHS indicative price is £5,143 per 30 × 60 mg ([NHSBSA](https://dmd-browser.nhsbsa.nhs.uk/ampp/view/156345)). These are list or cash prices, not what health systems actually pay.

**Children.**

| Issue | Evidence | Source |
|---|---|---|
| Growth plates | 5 of 53 children (9.4%) on anti-vessel drugs in COG phase 1 trials had growth-plate widening (sunitinib, pazopanib); reversible after stopping. Growth-plate damage is a standard finding in animal studies. | PMID 25257751; PMID 27162053 |
| Wound healing near surgery | Apatinib: severe wound breakdown in 11% (PMID 30559126). AOST2032 leaves out cabozantinib in the first chemotherapy cycle after surgery and tracks port-site wound problems. | NCT05691478 |
| Collapsed lung | 9% (cabozantinib) to 18% (lenvatinib + IE) | PMC8763616; PMC11581622 |
| Blood pressure, kidney, skin | Dose-limiting in children at higher cabozantinib doses; side effects at every dose level | PMID 29693796 |
| Formulation | Cabozantinib comes only as tablets (no liquid found); lenvatinib capsules can be dispersed in water or apple juice ([label summary](https://drugs.com/dosage/lenvima.html)) | — |

**Front-line and maintenance trials, status on 14 November 2026:**

| Trial | Question | Status |
|---|---|---|
| COG AOST2032 (NCT05691478) | Cabozantinib added to MAP chemotherapy, then 6 months of cabozantinib alone, newly diagnosed, 1,122 planned | **Suspended**, reason given "Extend the observation period for current patients" (updated 27 October 2026). The dose-finding part closed in May 2025. No public explanation found; some hospital pages still list it as recruiting. |
| Ipsen CabOSTar (NCT06341712) | Cabozantinib vs supportive care for residual disease after first-line treatment | **Terminated** after 10 patients (November 2024 – February 2026) for recruitment problems |
| FOSTER-CabOS, part of the FOSTER platform (NCT07871864) | 12 months of cabozantinib vs supportive care after first-line treatment, 530 planned, 8 European countries | **Recruiting** since 7 October 2026 |
| Léon Bérard (NCT04055220) | Regorafenib maintenance vs observation after first-line treatment | Recruiting since 2020 |
| Peking University (NCT04351308) | Apatinib or PD-1 antibody added for poor responders at diagnosis | Status unknown since 2020 |

**Our summary of why the class is stuck:** the gain is about two months of disease control, with no survival gain shown; there is no test to pick responders; the drugs are hard to combine with surgery and intensive chemotherapy in growing children; the main US front-line trial is paused and an industry maintenance trial could not recruit; and we found no company seeking an osteosarcoma licence.

## 6. The best testable idea

**Hypothesis.** In relapsed osteosarcoma treated with a VEGFR2-blocking pill, tumours with extra copies of VEGFA (6p21) or of the KDR/PDGFRA/KIT region (4q12), together about 40% of patients, stay progression-free substantially longer than tumours with neither. A fair pre-set threshold would be a hazard ratio of 0.5 or lower. If true, this group should also account for most patients still progression-free at 12 months.

**Why this idea.**
- Every active drug blocks VEGFR2, and these two amplifications put more of the drug's target pathway into the tumour.
- A matched patient-derived tumour model and the liver-cancer precedent both point the same way.
- No one has tested it in patients.
- It can be answered cheaply with tissue or banked blood from trials already done. Gene copy number can be read from routine sequencing panels, from FISH, or from low-coverage sequencing of tumour DNA in blood. AOST2032 already banks blood for tumour DNA.
- The answer would change how FOSTER-CabOS, and AOST2032 if it restarts, select or stratify patients.

**How to test it, cheapest first.**
1. Use archived samples from the randomized trials (SARC024, REGOBONE, OLIE, OAIE). Randomized trials allow the real test: does the amplification predict benefit *from the drug*, compared with placebo or chemotherapy alone, rather than just better outcomes in general? Add single-arm cohorts (CABONE, ADVL1622, ITCC-050) for the 12-month question.
2. Use centres that routinely sequence tumours (for example MSK, which reported the two subsets) to look back at their patients who later received regorafenib or cabozantinib.
3. Stratify new trials by amplicon status from diagnostic tissue.

**What would disprove it.** Among 100 or more pooled patients treated with a pill, a hazard ratio of 0.8 or above for amplified against non-amplified tumours, or no difference in the drug-versus-control comparison in the randomized trials.

**Runner-up ideas (also hypotheses).**
- Site, not genes, explains benefit: compare lung and bone lesions *within the same patients* on existing trial scans.
- A randomized trial of pill maintenance after complete surgical removal of a lung relapse, judged against the resected-relapse benchmark in the project's pooled control dataset.
- Pill plus an FGFR blocker, to stop the FGFR–ERK escape seen at the tumour–lung border.

## Limits

- **Most biomarker findings are exploratory**, from single trials of 28–105 patients, with many tests and no correction for multiple comparisons.
- **Several sources were read only as abstracts** (REGOBONE, SARC024, sorafenib trials, most lab studies); this is marked in the notes. Europe PMC full-text service returned errors this session; full texts came from PMC where open.
- The NCCN and ESMO guideline wording came secondhand (a trial-protocol quote found by web search). Protocol PDFs on cdn.clinicaltrials.gov could not be reached from this workspace.
- The reason AOST2032 was suspended is only the one-line registry entry; we found no public statement.
- Chinese trial registries and Chinese-language journals were not searched, so front-line apatinib or anlotinib work registered only in China may be missing.
- Cross-trial comparisons mix drugs, doses, ages, endpoints and lines of therapy. Prices are cash or list prices.
- The ADVL1622 osteosarcoma results come from registry postings; no peer-reviewed paper was found.

## Next steps

1. Ask the CABONE (Institut Bergonié), REGOBONE (French Sarcoma Group), SARC024 (SARC) and OLIE (Eisai / ITCC) teams whether baseline tumour or plasma samples exist with copy-number data; a pooled amplicon-versus-outcome analysis is the cheapest decisive test.
2. Ask COG what "extend the observation period" means for AOST2032, and whether its ctDNA samples could be used for the amplicon question.
3. Add the ADVL1622 osteosarcoma results and the OLIE/OAIE survival figures to the pooled control dataset.
4. Re-read the SARC024 and REGOBONE full texts when access allows, for subgroup data.
