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
