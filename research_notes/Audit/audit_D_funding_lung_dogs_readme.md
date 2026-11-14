# Audit D: NIH funding, lung metastasis, dog genomes, README

*Independent fact-check, 2026-11-14. Numbers recomputed from the repo CSVs with fresh Python; external claims re-queried against NIH RePORTER, PubMed/Europe PMC, ClinicalTrials.gov v2 and NCBI SRA/BioProject. No report was edited.*

Verdicts: CONFIRMED, WRONG, OVERSTATED, UNVERIFIABLE, INTERNALLY INCONSISTENT.


## 1. reports/NIH funding for osteosarcoma.md

Method: every table recomputed from `data/nih_osteosarcoma_projects.csv` (2,723 rows) and `data/nih_neuroblastoma_projects.csv` (2,947 rows). 10 grants (6 focused, 2 substantial, 1 ZIA genome project, 1 subproject) re-queried by appl_id on RePORTER v2: fiscal year, award amount and title matched exactly for 10/10.

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 7 | FY2025 focused: $18.0M, 30 projects | CONFIRMED | $18.0M (30) | CSV recompute |
| 7 | 4x the 2015 level ($4.5M, 12 projects) | CONFIRMED | 18.0/4.5 = 4.0 | CSV |
| 7 | "roughly a quarter of one percent of NCI's budget of about $7.2 billion" | CONFIRMED (caveat) | NCI FY2025 appropriation is about $7.2B; 18.0/7,220 = 0.25%. Fairness: numerator is NIH-wide focused tier only (excludes COG network money, SPORE parents), denominator is NCI only; the report flags both caveats (lines 70-74). Acceptable, but say "title-named grants" each time. | NCI budget fact book; CSV |
| 7 | Neuroblastoma $30.8M across 51 focused projects in FY2025 | WRONG (small) | CSV gives $30.8M/51, but $0.41M is a double count (P01CA217959 parent and its focused subproject 7274 both kept). De-duplicated: **$30.4M**. | CSV, see line 21 |
| 7 | Neuroblastoma "similar number of US cases" | CONFIRMED (loose) | ~700-800 NB vs ~1,000 OS (all ages) a year in the US; "similar order" is fair. | ACS key statistics |
| 7 | Decade: NB $228M vs OS $108M, "about twice" | CONFIRMED (minor) | $227.9M raw; $226.8M after removing the $1.03M double count. Ratio 2.1 either way. | CSV |
| 9 | A third of focused money ($36.6M) to NCI in-house labs | CONFIRMED | ZIA = $36.61M = 33.8% of $108.25M | CSV |
| 9 | One genome study = $20.4M | CONFIRMED | ZIABC011328 "Characterization of the Osteosarcoma Genome", $20.36M; RePORTER matches FY2015/2016 amounts | CSV + RePORTER |
| 9 | ctDNA/liquid biopsy $3.3M over eleven years | CONFIRMED (wording) | $3.32M, all since FY2020 (R37CA244355 + K08CA290061). "Over eleven years" implies spread; say "since 2020". | CSV |
| 9 | Clinical-trial and outcomes research $4.7M | CONFIRMED | 12 project-years, $4.7M (title regex trial/outcome/survivor) | CSV |
| 15-19 | Tier table FY2025: focused 30/$18.0M; substantial 9/$10.9M; incidental 208/$116.1M | CONFIRMED | Exact | CSV |
| 13-19 | Tier rules are sound | OVERSTATED | Focused tier is clean. The **substantial tier is dominated by multi-disease programs**: Count Me In U2C ($16.6M 2020-25, many cancers), Childhood Cancer Data Initiative ZID ($3.4M), Genetic Modifiers of Cancer Risk, Comparative Oncology Program Lab ($13.6M). "Focused + substantial" ($183.2M) is therefore an upper bound, not osteosarcoma money. Also the tool searches only the word "osteosarcoma"; grants naming only "osteogenic sarcoma" are never fetched (regex is applied after fetch). | CSV; tools/nih_funding_tracker.py l.63 |
| 21 | "Multi-project grants are not double counted: where a subproject matches, only that subproject's amount is counted" | WRONG | The code groups by `appl_id`, but in RePORTER every subproject has its own appl_id (e.g. P50AT008661-01: parent 8866008, subprojects 8866010-15), so the de-dup never fires. CSV keeps parent and subprojects for 26 OS and 28 NB parent-years. No effect on OS focused/substantial totals (no focused parent; Count Me In parent is substantial but its units are incidental), but NB focused is inflated by $624,652 (2024) and $407,872 (2025). Fix: group by (fiscal_year, project_num) or drop rows with empty subproject_id when subproject rows exist. | RePORTER API check; CSV |
| 25-38 | Year table (all 33 numbers) | CONFIRMED with 2 rounding slips | FY2018 focused+substantial = $9.47M (report $9.4M, should round to **$9.5M**); FY2024 = $25.81M (report $25.9M, should be **$25.8M**). NB 2024/2025 see line 7. Totals $108.2M / $183.2M / $227.9M match raw CSV. | CSV |
| 44 | NCI $101.3M of $108.2M (94%); rest NIGMS, OD, NIBIB, NICHD, NCATS | CONFIRMED | 101.25/108.25 = 93.5% | CSV |
| 46 | R01 $37.2M; in-house $36.6M; U01 $10.8M; R21 $4.7M; R44 $4.1M | CONFIRMED | Exact. (R37 $3.4M omitted from list; fine.) | CSV |
| 46 | "K and F grants together are under $4M" | WRONG | K01 $2.28M + K08 $1.10M + F30 $0.56M + F31 $0.56M + F32 $0.27M = **$4.77M** (focused tier). Say "under $5M". The inference "few new osteosarcoma scientists are being trained" is opinion, not shown by the data. | CSV |
| 48-60 | Topic table (9 rows) | CONFIRMED (not reproducible from repo) | I reproduced 6/6 rows tested exactly with simple title regexes (dogs 32/$28.0M, ctDNA 8/$3.3M, metastasis 83/$23.2M, genomics 47/$53.2M, trials 12/$4.7M, germline 18/$15.3M), but the classifier is **not in tools/nih_funding_tracker.py**, so the README's "scripts that rebuild every analysis" does not hold for this table. Add the regexes to the tool. | CSV; tool |
| 64 | ctDNA "has one current grant, at Dana-Farber" | OVERSTATED | FY2025 has two: R37CA244355 (focused, $814K) and K08CA290061 (substantial, $254K), both Dana-Farber. | CSV |
| 64 | Trial methodology / pooled outcome data "barely appear" | CONFIRMED (judgement) | Consistent with $4.7M trials topic. | CSV |
| 65 | "Genomics is well funded but concentrated. Most of it is one in-house NCI project." | WRONG | The genome project is $20.4M of $53.2M (**38%**). The rest is Count Me In ($16.6M, multi-cancer), Functional Genomics of Sarcoma ($12.0M, NCI in-house) and others. Correct: "Most of it is two NCI in-house projects (61%) plus the multi-cancer Count Me In program." | CSV |
| 65 | "the big genome re-analysis has already been done" | UNVERIFIABLE here | Cross-report claim; not supported by funding data. | - |
| 66 | Dog studies $28M "mainly through two U01 cooperative agreements in fiscal 2025" | WRONG | $13.6M (49%) of the $28M is NCI's **Comparative Oncology Program Laboratory** (ZIA, substantial tier, multi-cancer). The three dog U01s total $7.2M over the decade, and the two FY2025 canine U01s (Tufts, UC Davis) total $1.26M that year. | CSV |
| 71 | Sarcoma SPORE "lands in the incidental tier and is excluded" | OVERSTATED | The MD Anderson Sarcoma SPORE parent (P50CA302482, FY2025) is incidental, but its Project 3 (antibody-drug conjugates, $478K) is in the **focused** tier and counted. | CSV |
| 74 | NCI budget approximate, not from API | CONFIRMED | Honest caveat | - |
| 3 | "Built from RePORTER API on November 14, 2026" | CONFIRMED (plausible) | API returns FY2025 records matching CSV | RePORTER |

## 2. reports/Stopping lung metastasis in osteosarcoma.md

Method: all 44 cited PMIDs pulled from PubMed E-utilities (esummary + efetch XML abstracts); all exist and match the described topic. All 21 cited NCT records pulled from ClinicalTrials.gov API v2. 30 "zero trial" drug names searched three ways (`query.cond=osteosarcoma`+`query.intr`, `query.term="<drug> AND osteosarcoma"`, and the drug alone to confirm the name is indexed). Counts recomputed from `data/lung_metastasis_*.csv` and from `data/literature/osteosarcoma_pubtator.jsonl` with my own script (I did not run `tools/lung_metastasis_map.py`, because it overwrites `data/`).

### 2a. Counts and data

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 3 | 33,242 PubMed records; 758 registered studies | CONFIRMED | 33,242 unique PMIDs (35,078 lines, de-duplicated); 758 rows in trials CSV | jsonl; osteosarcoma_trials.csv |
| 3 vs 192 | "live ... Europe PMC queries run" vs "europepmc.org was not reachable through this workspace's proxy" | INTERNALLY INCONSISTENT | Say which Europe PMC endpoint worked (REST API at www.ebi.ac.uk) and that the website did not. | report |
| 13 | 29,305 non-review non-retracted; 9,130 metastasis-focused; 3,579 lung; 1,093 (12%) in vivo metastasis | CONFIRMED | 29,305 / 9,130 / 3,579 / 1,093 = 12.0% | own recompute |
| 13 | "That share has not budged in twenty years" | CONFIRMED | 12.9% (2005-09), 12.6%, 13.2%, 13.0% (2020-24) | papers CSV |
| 17-35 | Mechanism table (papers / in vivo) | CONFIRMED | All 17 rows match `lung_metastasis_mechanisms.csv` | CSV |
| 29 | Platelets / coagulation: aspirin, osteosarcoma trials **0** | INTERNALLY INCONSISTENT | Line 162 describes NCT03244020, a randomized aspirin trial with a primary-bone-tumour stratum, which the report's own `cond=osteosarcoma + intr=aspirin` search returns. Say "0 anti-metastasis trials". | CT.gov |
| 39 | "VEGF has 106 in vivo metastasis studies and 57 trials behind a literature of 68 osteosarcoma papers" | INTERNALLY INCONSISTENT | Table line 19 gives VEGF/VEGFR **867** papers. The 68 is the KDR (VEGFR2) gene count from the literature-map report. Fix the sentence. | report l.19; literature map l.38 |
| 52 | 5 of the 10 most recent ezrin-titled records are retractions or expressions of concern | CONFIRMED | 41640460, 38376414, 37477177, 36324370 (notices) + 35012433 (retracted) | jsonl |
| 58 | Dormancy: 32 in vivo metastasis papers; 14 with dormancy in the title | CONFIRMED | 14 (13 in the research set) | jsonl |
| 68 | 224 lung/metastasis/inhaled trials; 73 lung-directed | CONFIRMED | 224 rows, 73 `lung_directed=True` | trials CSV |
| 184 | Glutamine "5 in vivo metastasis papers out of 33,242" | OVERSTATED | Wrong denominator: 5 of 69 glutamine papers (from 29,305 research records). | CSV |
| 200 | 37 GM-CSF papers, zero in vivo metastasis | CONFIRMED | Good self-check | CSV |

### 2b. Cited papers (PubMed abstracts)

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 7 | Blocking the IL-1/IL-6/IL-8 circuit "stops metastasis in mice without slowing the primary tumour **at all**" | OVERSTATED | Abstracts say IL-1 disruption "significantly reduced metastatic progression" (40882022) and IL-6+CXCL8 blockade had "minimal effects on tumor cell proliferation" while inhibiting metastasis (30135299). Say "reduced metastasis in mice with little effect on tumour growth". | PMID 40882022, 30135299 |
| 7, 141-143 | IL-1, IL-6 and IL-8-receptor drugs: "not one of them has **ever** been tested in an osteosarcoma trial" | OVERSTATED | ClinicalTrials.gov only (report admits, l.194), and tocilizumab is listed in NCT04616248, which enrols bone sarcoma. Say "none has a registered osteosarcoma efficacy trial on ClinicalTrials.gov". | CT.gov v2 |
| 7 | The dog inhaled-IL-15 arm "was actually worse than doing nothing" | OVERSTATED | It was worse than a historical control that received amputation + chemotherapy, not "nothing". | PMID 41209004 |
| 7 | "the reason given in that paper is that surgery and chemotherapy themselves raise IL-6 and suppress immune killing" | OVERSTATED | The abstract reports IL-6 rose and cytotoxicity fell after surgery and chemo, and says only that "correlative assays suggest significant immunological effects". It also says plasma cytokines showed "no significant differences between disease-free and metastatic-failure patients", which cuts against Hypothesis 1 and should be quoted. | PMID 41209004 |
| 7 | "the one randomized trial in sarcoma found that cheap chest X-rays every six months did no worse than CT scans every three" | WRONG / INTERNALLY INCONSISTENT | It was a 2x2 design. X-ray was non-inferior to CT; **6-monthly was not shown non-inferior to 3-monthly** (HR 1.2, upper 90% CI 1.47), which line 122 states correctly. Also single-centre, all extremity sarcoma. | PMID 24249538 |
| 43 | 2025 Cancer Res: hypo-proliferative subpopulation, IL-6/IL-8 in response to lung-epithelial IL-1alpha; IL-1 disruption reduced progression | CONFIRMED | Abstract matches | PMID 40882022 |
| 44 | IL-6/CXCL8 higher in lung mets than matched primaries; combination inhibited metastasis; bronchial epithelial + smooth muscle feed-forward | CONFIRMED | | PMID 30135299 |
| 45 | CXCL1 from lung vessels/HPAEC -> CXCR2 -> FAK -> NF-kB -> VCAM-1; CXCL1 drove lung metastasis in vivo | CONFIRMED | Pathway includes PI3K/Akt; heading "The IL-8 signal" is really CXCL1 via the shared receptor CXCR2. | PMID 32079335, 34760697 |
| 45 | IL-8 "made by tumour-associated macrophages" promoted lung metastasis; "anti-IL-8 antibody blocked it" | OVERSTATED | IL-8 came from OS-TAM co-culture medium (source cell not isolated), and the antibody "mitigated" the effect. Say "reduced". | PMID 38302407 |
| 46 | Secretome-preconditioned lungs remodel; EFEMP1 depletion prevented lung metastasis; EFEMP1 in plasma and in biopsies with worse survival | CONFIRMED | | PMID 38031171 |
| 47 | 10 dogs pre-metastatic vs 10 cancer-free: more CD204+, CD206+ macrophages, CD11d+ BMDCs; BMDCs lower once metastases established | CONFIRMED | Measured at necropsy; using it as a "4-week pharmacodynamic readout" (l.172) in live dogs is untested. | PMID 39526499 |
| 48 | beta-glucan before tumour cells "prevented tumour cell seeding"; macrophage/NK dependent; CD40 agonist improved it | CONFIRMED | | PMID 41083282 |
| 52 | NSC305787/NSC668394 inhibited lung metastasis of ezrin-sensitive but not ezrin-resistant cells after tail-vein injection | CONFIRMED | | PMID 21706056 |
| 52 | Locking ezrin open or closed abolished metastasis; early death in lung; lactate/oxygen changes | CONFIRMED | Metabolic changes were reported for the closed form only. | PMID 22147261 |
| 52 | 2026 paper "overturns the textbook": closed ezrin is an RNA-binding protein that restores metastatic capability "in ezrin-null xenografts" | OVERSTATED | The rescue was in **zebrafish** xenografts. Drop "overturns the textbook". | PMID 41843652 |
| 56 | K7M2 intratibial: 100% lung mets at 1 week; burden 0.9% -> 40.3%; foci 36.4 vs 49.3, p=0.18; amputation at 30 min 48.9% vs 40.9%, p=0.819; quote | CONFIRMED | Exact | PMID 29601385 |
| 62 | >1 million cells, 4 model types, bone and lung; canine "the most faithful model"; lung mets more ECM signalling; FN1 -> integrin/syndecan; bioRxiv | CONFIRMED (one word) | Abstract says "a **more** faithful model". | PMID 41648517 |
| 62, 179 | Resistant cells at the tumour-lung interface; death amplified FGFR-ERK; FGFR inhibitor or pazopanib "reversed it" | OVERSTATED | Context missing: resistance emerged **after an MCL1 inhibitor**, and fexagratinib/pazopanib "enhanced MCL1 inhibitor response". Hypothesis 8's "add an FGFR inhibitor to a cytotoxic" is not what was tested. | PMID 42856637 |
| 74 | Inhaled GM-CSF, 43 patients, to 1,750 ug BID, no DLT; 3-yr EFS 7.8%, OS 35.4%; Fas/FasL fell; quote | CONFIRMED | (Registry shows 49 enrolled, 43 eligible.) | PMID 20576718; NCT00066365 |
| 75 | Inhaled lipid cisplatin: 19 pts, no renal/ear/blood toxicity; 11 bulky all progressed before cycle 7; of 8 small, 1 PR, 2 SD -> surgery, recurrence-free at 1 yr | CONFIRMED | | PMID 23255417 |
| 77 | Aerosol IL-2 raised NK cells only in the lung, no systemic toxicity; IL-2 + NK beat either alone | CONFIRMED | | PMID 24136885, 24610870 |
| 78 | Aerosol gemcitabine "worked in mice and in **dogs**"; 48 h after amputation, no wound-healing impairment | OVERSTATED | The cited abstract is mice only. The dog claim needs a separate citation or should go. | PMID 29610563 |
| 79 | Inhaled IL-15 phase 1 dogs: 21/18 evaluable, MTD 50 ug BID, 1 CR >1 yr, 1 PR, 5 SD, CBR 39% | CONFIRMED | Included melanoma dogs too. | PMID 35680383 |
| 80 | COTC030: DFS and OS statistically inferior to historical control, halted for futility; cytotoxicity -18.2 +/- 16.1%, p<0.001; IL-6 rose after both | CONFIRMED | See l.7 caveats. | PMID 41209004 |
| 81 | IL-15 + doxorubicin: 10 dogs, 8 evaluable, CBR 30%, ORR 10%, lymphodepletion added nothing | CONFIRMED | Melanoma and bone tumours. | PMID 41041167 |
| 93 | Saracatinib: 37 analysed; PFS 19.4 vs 8.6 months, p=0.47; OS not reached | CONFIRMED | | PMID 32398945 |
| 7, 102 | "a 19.4 vs 8.6 month difference ... that nobody ever followed up"; "10.8-month median PFS gap that nobody pursued" | OVERSTATED | p=0.47, 18 vs 19 patients; the authors' own conclusion is "no apparent impact ... on OS". Presenting the gap as a lost signal without the p-value (summary) is misleading. "Nobody" is unverifiable. | PMID 32398945 |
| 94 | AOST1421 dinutuximab + GM-CSF: 39, 28% event-free at 12 months, below the 16 required | CONFIRMED | 11/39 = 28.2%; success needed >=16/39 | PMID 35809374; NCT02484443 results |
| 95 | AOST1321 denosumab cohort 2: 38, 26% | CONFIRMED | 10/38 = 26.3% | NCT02470091 results |
| 97 | Dog HER2-Listeria vaccine, 118 dogs, no significant DFI/OS difference; long survivors had fever and IL-6/TNF rises; short survivors caught up after repeat dosing | CONFIRMED | "Caught up" refers to fever/cytokine responses, not survival; make that explicit. | PMID 39955616 |
| 98 | MISTOSUS: pilot of 9, 55% post-relapse EFS, median 84 months | CONFIRMED | | PMID 41789811 |
| 108 | SBRT 24 pts / 71 lesions, 1-yr local failure 13.6% (6.6-23.2), no acute grade 3; 17% of lesions in lung | CONFIRMED | "parenchymal (17%)" | PMID 41531260 |
| 108 | Smaller series: LC 88%, all 4 failures BED <=48 Gy, distant PFS 2.4 months | CONFIRMED | 7 patients, 34 courses; only 29% pulmonary/mediastinal | PMID 40509558 |
| 112 | Pulmonary suffusion early safety data | CONFIRMED | 31 patients, sarcoma and colorectal | PMID 40940977 |
| 122 | Surveillance RCT: 500 pts; OS 67% vs 66% (HR 0.9, upper 1.13); 64% vs 69% (HR 1.2, upper 1.47); ~90% local recurrences self-found; 6-monthly non-inferiority not shown | CONFIRMED | | PMID 24249538 |
| 123 | 69 pts (35 OS), 1,279 images, 9 relapses, 2 symptomatic, PPV 0.5, quote | CONFIRMED | | PMID 38345039 |
| 125 | ctDNA phase 2: 18 pts, all CTC+, 10 ctDNA+, all 8 MYC-amplified progressed, PFS-4 28% (13-59) | CONFIRMED | Trial was of gemcitabine + nab-paclitaxel in measurable relapse, not surveillance. | PMID 39360936 |
| 126 | 5-hmC 262-gene signature, sensitivity 65%, specificity 64% | CONFIRMED | | PMID 41673231 |
| 127 | 2026 review quotes | CONFIRMED | | PMID 42824543 |
| 129 | Meta-analysis 21 retrospective studies: HR 0.29, 0.21, 1.56, VATS 1.69 | CONFIRMED | Bilateral HR 1.56 is for PMOS; for PRS it was not significant. | PMID 42036655 |
| 129 | Systematic review: level IV, selection bias | CONFIRMED | | PMID 38375639 |
| 129 | 463 consecutive, 5-yr 34.0%, 20-yr 29.7%, 42 of 138 survivors cured by repeat surgery | CONFIRMED | | PMID 34674575 |
| 131 | 159 pts / 229 metastasectomies, 79-month follow-up; responders 41.1% vs 0.0%, HR 0.22; 43.4% vs 6.8%, p=0.004; no survival difference; 2-3 month window | CONFIRMED | Single-centre retrospective | PMID 42723688 |
| 158 | Tissue factor in 73.6% of 53 biopsies; knockdown lowered IL-8, CXCL1, SNAI1, MMP2; antibodies reduced lung metastasis | CONFIRMED | | PMID 26763081 |
| 159 | Platelet LPA, LPAR1 KO abolished early foci, ONO-7300243 prevented pulmonary metastasis | CONFIRMED | | PMID 34302117 |
| 160 | AP201 humanized anti-podoplanin suppressed growth and metastasis "without significant adverse events"; PDGFR | CONFIRMED | | PMID 35381070 |
| 175 | FAK downstream of integrins (CD248-ITGB1) and LOX | CONFIRMED | | PMID 36997926, 37013056 |
| 175 | ZEB1/IQGAP3 axis "where FAK inhibition reduced lung metastasis in vivo" | OVERSTATED | The in-vivo experiment in the abstract is FAK **activation** rescuing IQGAP3 knockdown; FAK inhibition is described only for GSK-3beta signalling. | PMID 42520958 |

### 2c. Trials (ClinicalTrials.gov API v2, pulled 2026-11-14)

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 76 | NCT01650090 Eleison phase 2, 28 pts, completed Nov 2018, no results, no publication | CONFIRMED | No PubMed hit for the NCT or for a phase 2 inhaled-cisplatin paper | CT.gov; PubMed |
| 77 | NCT01590069 started June 2012, ACTIVE_NOT_RECRUITING, completion April 2029, 70 planned, no results | CONFIRMED | 14.4 years | CT.gov |
| 78 | NCT03093909 44, recruiting since Nov 2017, no results | CONFIRMED | Phase 1, all solid tumours with lung mets | CT.gov |
| 82 | NCT04183062 withdrawn, 0, drug not available | CONFIRMED | | CT.gov |
| 93 | NCT00752206 randomized, 38, terminated, DSMB quote, March 2009-Dec 2017 (8.75 yr) | CONFIRMED | | CT.gov |
| 96 | NCT04974008 single arm phase 2, EFS primary, 39, ANR, no posted results, no peer-reviewed paper | CONFIRMED | PubMed has only the canine papers | CT.gov; PubMed |
| 96 | Human OST-HER2 "72.7% vs 45.8% three-year survival" press-reported | UNVERIFIABLE | No press source cited; add one or drop the numbers | - |
| 98 | NCT05726383 single arm phase 2, recruiting since May 2024, 32 | CONFIRMED | | CT.gov |
| 99 | NCT05235165 = AOST2031, phase 3 randomized, April 2022 to March 2031, 62, 4-year thoracic EFS | CONFIRMED | | CT.gov |
| 100 | NCT06114225 single arm phase 2, 43, recruiting | CONFIRMED | "Immunotherapy" is gemcitabine + penpulimab | CT.gov |
| 102 | Gaps report "lists as gap 3 ... 'no randomized test ... only single-arm trials found.'" | INTERNALLY INCONSISTENT / STALE | The gaps report's summary row (l.31) has already been corrected to "Tried once, abandoned" citing NCT00752206. Only its l.149 table still says "No randomized test", and that row reads "Only retrospective series", not "only single-arm trials found". Update the "Correction" paragraph and fix gaps l.149. | reports/Osteosarcoma and neuroblastoma research gaps.md l.31, l.149 |
| 102 | FOSTER NCT07871864, 530, randomized, recruiting | CONFIRMED | Started 7 Oct 2026 | CT.gov |
| 108 | NCT02581384 SBRT in sarcoma lung metastases terminated after 5 | CONFIRMED | Also included Wilms tumour | CT.gov |
| 112 | NCT02811523 phase 1, recruiting since 2016; NCT03965234 phase 1/2, 99, recruiting since 2020, targets MRD | CONFIRMED | | CT.gov |
| 124 | No osteosarcoma surveillance trial; NCT04751409 (227, fear of recurrence primary); NCT06526897 (ECOG-ACRIN EA7201, phase 3, 1,582, OS, not yet recruiting, 2032) | CONFIRMED | Searches for osteosarcoma + surveillance / follow-up imaging / chest CT found no randomized surveillance trial | CT.gov |
| 142 | Tocilizumab only in NCT04616248, an adult CD40-agonist basket trial, endpoints toxicity and dose | CONFIRMED | Age 18+; bone sarcoma is a listed condition | CT.gov |
| 141-151 | Zero osteosarcoma trials for anakinra, canakinumab, rilonacept, siltuximab, sarilumab, SX-682, reparixin, ladarixin, navarixin, motixafortide, mavorixafor, DKN-01, pexidartinib, emactuzumab, admilparant/BMS-986278, telaglenastat, DRP-104, simtuzumab, maraviroc, nirogacestat, AP201 | CONFIRMED | 0 hits by cond+intr and by full-text term; each name is indexed for other conditions (except AP201 and sirexatamab, which return 0 everywhere) | CT.gov |
| 144 | Defactinib 0 osteosarcoma trials | CONFIRMED (note) | The full-text search returns NCI-MATCH (NCT02465060), an adult basket with a defactinib arm; osteosarcoma is not named | CT.gov |
| 144 | Defactinib "FDA-approved 2025" | CONFIRMED (nuance) | Approved May 2025 only as a co-pack with avutometinib, for KRAS-mutated low-grade serous ovarian cancer | FDA |
| 145 | CXCR4: plerixafor 0 osteosarcoma trials | WRONG (minor) | `cond=osteosarcoma + intr=plerixafor` returns NCT03612466 (CycloSam + radiotherapy, Mozobil for stem-cell mobilization, WITHDRAWN, 0 enrolled). Say "0 anti-metastasis trials". | CT.gov |
| 162 | NCT03244020: aspirin 325 mg vs enoxaparin, est. 2,868, primary-bone-tumour stratum, Feb 2018 to July 2028, VTE primary | CONFIRMED | Adults 18+ only, so most osteosarcoma patients (adolescents) are excluded; status ENROLLING_BY_INVITATION. Matters for Hypothesis 3's "free" data request. | CT.gov |
| 175 | FAK pet-dog trial "already lead 1 of `reports/Ranked leads and research partners.md`" | WRONG (stale) | The ranked-leads report now ranks it **lead 4** ("Was lead 1"); lead 1 is IL-1/IL-6 blockade from this report. | Ranked leads l.20-23 |
| 175 | Defactinib "NIH-funded at a veterinary school" | CONFIRMED | R37CA303990, Colorado State, FY2025, $629K | NIH CSV |
| 156 | Platelet axis "did not appear in any of the project's earlier reports" | CONFIRMED | Only this report and the later ranked-leads report mention LPAR1/podoplanin/tissue factor | grep reports/ |

## 3. reports/Dog genome re-analysis scope.md

Method: for each BioProject, esearch db=sra `<PRJ>[BioProject]` (with and without `"wgs"[Strategy]` and `osteosarcoma`), esummary for run counts and `total_bases`, esummary db=bioproject for title and description. Broad query `"Canis lupus familiaris"[Organism] AND osteosarcoma AND "wgs"[Strategy]`.

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 3 | "Lead 7 of the ranked leads" | WRONG (stale) | Now **lead 11** in `reports/Ranked leads and research partners.md` (lead 7 is now the IL-8 receptor). | Ranked leads l.30 |
| 7 | SRA holds "743 whole-genome sequencing runs" from canine osteosarcoma projects | CONFIRMED (wording) | The broad query returns 743 **experiments** (747 runs, 39.4 Tbases). The table rows sum to **740**, so 3 come from projects not listed. | SRA E-utilities |
| 7 | "Instead of 24 genomes ... 743 runs" | OVERSTATED | Unlike units. 743 counts runs, including matched normals, 289 low-coverage cfDNA/blood runs and 209 low-pass tumour-only runs. High-depth tumour-normal WGS is about **55 dogs (PRJNA1374203) + the Gardner 2019 cohort (90 runs) + 8 jaw tumours + a few others**, i.e. roughly 110 dogs, not 743 genomes. Still several times the 24 assumed. | SRA |
| 7 | COTC021/022 dogs "were treated in a randomized trial with recorded outcomes" | CONFIRMED | Randomized 324-dog trial of carboplatin +/- sirolimus; no DFI/OS difference | PMID 33753454 |
| 9 | Loss of heterozygosity predicts outcome "in children" | CONFIRMED (wording) | Genome-wide LOH is "a strong prognostic indicator for high-grade osteosarcoma" in a paediatric **and adult** cohort. Add the citation. | PMID 39814020 |
| 15 | PRJNA1374203: 110 runs, 17.5 Tb, COTC021/022 | CONFIRMED | 55 tumour/normal pairs, ~66x per run; registered 4 Dec 2025 | SRA; BioProject |
| 16 | PRJNA1367604: 209 runs, 3.4 Tb, COTC021/022/026/030 | CONFIRMED (needs note) | ~16 Gbases per run, about **6-7x coverage**, and the description mentions **tumour DNA only**. That is low-pass, enough for copy number, but weak for structural-variant/chromothripsis calling without normals. | SRA; BioProject |
| 17 | PRJNA525883: 90 WGS runs, 11.5 Tb, the 2019 Gardner et al. cohort | CONFIRMED | 90 WGS (+45 WXS) runs, 11.46 Tb WGS. Gardner et al., Commun Biol 2019 (PMID 31341965) exists; BioProject has no PubMed link, so the pairing is plausible but not proven by NCBI. | SRA; PubMed |
| 18 | PRJNA1154710: 16 runs, 3.5 Tb, "Axial (spine and skull) osteosarcoma" | WRONG (detail) | Description: "Paired tumor and normal WGS from eight dogs with **mandibular** osteosarcoma". Say "jaw (mandibular)". | BioProject |
| 19 | PRJNA777126: 8 runs, 1.2 Tb, cell lines | CONFIRMED | | SRA |
| 20 | PRJNA680382: 6 runs, 0.6 Tb, primary and metastatic | CONFIRMED | 6 WGS runs from **two dogs** (project also has WXS and RNA-seq) | SRA; BioProject |
| 21 | PRJNA247491: 12 runs, 0.6 Tb | WRONG (minor) | Osteosarcoma WGS subset is 12 experiments / **16 runs / 0.74 Tb**. Multi-cancer pilot. | SRA |
| 22 | PRJNA1151136 + PRJNA1373368: 289 runs, 0.3 Tb, low-coverage blood and cfDNA | CONFIRMED | Osteosarcoma-tagged subset 177 + 112 = 289, 0.32 Tb (projects hold 770 runs in all, mostly other cancers and healthy dogs) | SRA |
| 24 | "Run counts include both tumour and matched normal samples" | OVERSTATED | True for PRJNA1374203, PRJNA1154710 and probably PRJNA525883; not for PRJNA1367604 (tumour), PRJNA777126 (cell lines) or the cfDNA projects. | BioProject descriptions |
| 24 | Liquid-biopsy projects match "lead 6" (ctDNA) | WRONG (stale) | ctDNA is now **lead 8** in the ranked leads. | Ranked leads l.27 |
| 28 | Tumour-normal genomes "total almost 40 trillion bases"; ~30 GB free | OVERSTATED / CONFIRMED | 39.4 Tb is **all** 747 runs; the tumour-normal projects total about 33 Tb. Free disk is 30 GB (`df`). | SRA; df |
| 32 | Chromothripsis and LTA patterns, Espejo Valle-Inclan et al., Cell 2025; CanFam4 | CONFIRMED | Cell 2025, PMID 39814020; LTA chromothripsis in about half of high-grade OS | PubMed |
| 33 | $1,000-5,000 compute | UNVERIFIABLE | Labelled as an estimate; reasonable for ~150 high-depth genomes | - |
| 34 | Outcome data sit with NCI COP / Integrated Canine Data Commons | CONFIRMED (plausible) | | - |

## 4. README.md

Method: every relative link resolved on disk (14/14 exist). External links tested with curl. Most non-NCBI sites are blocked by this workspace's proxy (403 on CONNECT), so those are marked UNVERIFIABLE (blocked), not wrong. DOIs and PMC IDs were checked through PubMed and the Europe PMC REST API.

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 14-28, 82-83 | 14 relative links (12 reports/briefs, LICENSE, LICENSE-CONTENT) | CONFIRMED | All targets exist | filesystem |
| 7, 28 | Scripts "rebuild every analysis from public data" | OVERSTATED | No script makes the NIH topic table (funding report l.48-60) or the SRA dog-genome counts. Sources also include NCBI SRA and PubTator, which l.7 omits. | tools/ |
| 72 | Scripts "need only Python 3 and internet access" | WRONG (minor) | `tools/pool_relapse_benchmarks.py` imports **pandas** | tools/ |
| 72 | `literature_fetch.py` output (~33,000 records) "is not stored here" | CONFIRMED | `data/literature/osteosarcoma_pubtator.jsonl` is in `.gitignore` (33,242 records locally) | .gitignore |
| 17 | Funding report: osteosarcoma vs neuroblastoma | CONFIRMED | See section 1 for its errors | - |
| 24 | Lung report: "eight untested ideas, led by IL-1/IL-6 blockade" | CONFIRMED | 8 hypotheses; #1 is IL-1 blockade (IL-6 is supporting) | lung report l.172-179 |
| 25 | "743 open canine osteosarcoma genome runs" | OVERSTATED | 743 SRA experiments (747 runs), including 289 low-coverage cfDNA and 209 low-pass tumour-only runs. Say "743 open canine osteosarcoma sequencing runs, including about 55 tumour-normal genomes from NCI trials with known outcomes". | SRA |
| 27 | "the sourced notes behind the report" | STALE (wording) | There are now 11 reports; say "the reports". | - |
| 36 | FOSTER trial platform NCT07871864 | CONFIRMED | Gustave Roussy sponsor, 530, randomized, recruiting | CT.gov |
| 36 | FOSTER "supported by the Bone Cancer Research Trust" | UNVERIFIABLE (blocked) | bcrt.org.uk blocked here; check | - |
| 37 | SARC runs SARC024 and SARC028 | CONFIRMED | SARC024 regorafenib = NCT02048371, sponsor SARC | CT.gov |
| 38, 46 | NCI COP, ICDC links | UNVERIFIABLE (blocked) | URLs look correct | - |
| 41 | Osteosarcoma Project (Count Me In) | CONFIRMED | Matches the NIH U2C "Count Me In" grant in the funding CSV | NIH CSV |
| 50, 52 | Osteosarcoma Institute (Dallas); Break Through Cancer "Defying Osteosarcoma TeamLab funded by family-led foundations" | UNVERIFIABLE (blocked) | Needs a source link | - |
| 58 | Lagmay et al., JCO 2016, PMC5012712, COG relapse benchmark | CONFIRMED | PMC5012712 = "Outcome of Patients With Recurrent Osteosarcoma Enrolled in Seven Phase II Trials ..." | Europe PMC |
| 59 | Frontiers in Immunology 2026, 864 trials from a commercial database | CONFIRMED | 864 interventional trials from Trialtrove (to Sept 2025) | Europe PMC, DOI 10.3389/fimmu.2026.1790067 |
| 60 | Plymouth evidence gap map | UNVERIFIABLE (blocked) | | - |
| 61 | Espejo Valle-Inclan et al., Cell 2025, doi 10.1016/j.cell.2024.12.005 | CONFIRMED | PMID 39814020 | PubMed |
| 67 | PubMed, PubTator3, ClinicalTrials.gov, SRA links | CONFIRMED | HTTP 200 | curl |
| 78 | Citation URL github.com/mgegen15-dev/For_John | CONFIRMED | HTTP 200 | curl |

## 5. Cross-report and stale text

| Where | Text | Verdict | Note |
|---|---|---|---|
| Gaps report l.44, l.202 | Funding tracker ranked as a to-do; "found no public figure for osteosarcoma funding" | STALE | The NIH funding report now exists; point to it. |
| Gaps report l.44 | "re-analysis of the 24 openly available dog genomes (ICDC OSA01)" | STALE | The dog scope report found far more data in SRA; cross-reference it. |
| Gaps report l.149 | Gap 3 "No randomized test of drug therapy after complete metastasis surgery" | INTERNALLY INCONSISTENT | Same report's l.31 says "Tried once, abandoned" (NCT00752206). |
| Lung l.175; Dog l.3, l.24 | Lead numbers 1, 6, 7 | STALE | Current ranking: FAK dog study = 4, ctDNA = 8, dog genomes = 11. |
| Funding l.66 vs l.71 | Dogs' $28M "mainly through two U01s" vs SPORE "excluded" | WRONG | The COP lab dominates the dog total, and a SPORE project is counted. |

## Verdict counts (sections 1-4)

| File | Rows | CONFIRMED | WRONG | OVERSTATED | INTERNALLY INCONSISTENT | UNVERIFIABLE | STALE |
|---|---|---|---|---|---|---|---|
| NIH funding | 26 | 17 | 5 | 3 | 0 | 1 | 0 |
| Lung metastasis | 84 | 65 | 3 | 11 | 4 | 1 | 0 |
| Dog genomes | 19 | 11 | 4 | 3 | 0 | 1 | 0 |
| README | 20 | 12 | 1 | 2 | 0 | 4 | 1 |
| **Total** | **149** | **105** | **13** | **19** | **4** | **7** | **1** |

Plus 5 cross-report rows (3 stale, 1 inconsistent, 1 wrong). The 10 RePORTER spot-checks (amount, year and title) matched 10/10. All 44 lung PMIDs and 21 NCT IDs exist and are on topic.

## Top 10 must-fix

1. **Funding l.21 and `tools/nih_funding_tracker.py` l.64-71: the de-duplication does not work.** It groups by `appl_id`, but each RePORTER subproject has its own appl_id, so parents and subprojects are both kept (26 OS and 28 NB parent-years). Neuroblastoma focused is overstated by $1.03M (FY2025 $30.4M, not $30.8M; decade $226.8M). Group by (fiscal_year, project_num) and re-run.
2. **Funding l.66: dogs' $28M is "mainly" NCI's in-house Comparative Oncology Program Lab** ($13.6M, a multi-cancer lab in the substantial tier), not two U01s (FY2025 canine U01s = $1.26M).
3. **Funding l.65: "Most of [genomics] is one in-house NCI project" is wrong.** That project is $20.4M of $53.2M (38%). Count Me In ($16.6M, multi-cancer) and Functional Genomics of Sarcoma ($12.0M) make up most of the rest.
4. **Funding l.46: K + F training grants total $4.77M, not "under $4M".**
5. **Funding substantial tier / "focused + substantial" ($183.2M) is padded by multi-disease programs** (Count Me In, Childhood Cancer Data Initiative, Genetic Modifiers of Cancer Risk, COP Lab). Label it an upper bound, or list those programmes. Also put the topic regexes in the tool (README says every analysis is scripted).
6. **Lung l.7 summary misstates the surveillance RCT.** X-ray was non-inferior to CT, but 6-monthly was **not** shown non-inferior to 3-monthly (as l.122 says). "Cheap chest X-rays every six months did no worse than CT every three" must go.
7. **Lung l.7, l.102: the saracatinib "19.4 vs 8.6 month difference that nobody followed up" is presented as a lost signal.** p=0.47 with 37 patients; the authors found no apparent drug effect. Put the p-value in the summary and drop "nobody".
8. **Lung l.7, l.141: "not one of them has ever been tested in an osteosarcoma trial"** should read "none has a registered osteosarcoma efficacy trial on ClinicalTrials.gov". Tocilizumab appears in NCT04616248 (bone sarcoma eligible), plerixafor in NCT03612466 (withdrawn), aspirin in NCT03244020, and other registries were not searched. Also: the dog IL-15 arm was worse than historical amputation + chemo controls, not "than doing nothing", and the paper does not "give IL-6 as the reason".
9. **Lung citation overreach (one each):** aerosol gemcitabine "in dogs" (the cited PMID 29610563 abstract is mice only); closed ezrin rescue was in zebrafish (41843652); FGFR/pazopanib reversal was with an MCL1 inhibitor (42856637); "FAK inhibition reduced lung metastasis in vivo" is not in 42520958's abstract; the anti-IL-8 antibody "mitigated", not "blocked" (38302407). Also fix the l.39 "68 osteosarcoma papers" vs table 867.
10. **Dog report: units and stale numbering.** "743 whole-genome runs ... instead of 24 genomes" compares runs (with normals, 289 cfDNA and 209 ~7x tumour-only runs) to dogs. About 110 dogs have high-depth tumour-normal WGS. PRJNA1154710 is mandibular (jaw), not "spine and skull". PRJNA247491 is 16 runs / 0.74 Tb. Lead numbers are stale: dog genomes are now lead 11, ctDNA lead 8, and FAK dog study lead 4 (lung l.175). The same "743 genome runs" wording is in README l.25 and ranked leads l.180.
