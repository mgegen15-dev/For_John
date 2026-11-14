# Audit B: trials landscape, pooled controls, kinase-inhibitor pills

Independent fact-check, 2026-11-14. Scope: three reports in `reports/`. Method: recompute from repo CSVs; check against ClinicalTrials.gov API v2, PubMed/Europe PMC. Verdicts: CONFIRMED, WRONG, OVERSTATED, UNVERIFIABLE, INTERNALLY INCONSISTENT. Reports were not edited.

(In progress; sections appended file by file.)

## File 1: `reports/Osteosarcoma clinical trials landscape.md`

Recomputation: `tools/trial_analysis.py` was re-run on a scratch copy of `data/osteosarcoma_trials.csv`; its output (stop reasons, period table, endpoint counts, 45/4 US compliance, 168 flags) reproduces the report and the committed flags file byte-for-byte. Problems below are in interpretation, not arithmetic.

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 3 | 758 studies, 603 interventional | CONFIRMED | CSV: 758 rows, 603 INTERVENTIONAL, 148 observational, 7 expanded access | data/osteosarcoma_trials.csv |
| 7 | 99 interventional trials terminated, withdrawn or suspended | CONFIRMED | 65 terminated + 26 withdrawn + 8 suspended = 99 | CSV |
| 7, 17-24 | Stop reasons 44 / 20 / 9 / 8 / 7 / 7 / 2 / 2 | CONFIRMED (arithmetic) | Regex output reproduced exactly. Classification caveats in next rows | tools/trial_analysis.py |
| 7, 21 | "only 7 stopped because the treatment did not work" | OVERSTATED | Regex is first-match: NCT00752206 ("slow accrual and futility", DSMB) and NCT01313884 ("did not reach primary objective") are binned as recruitment; NCT06566092 (Iovance, "reviewing safety and efficacy data") is binned as efficacy but line 28 calls it a company decision; NCT03468075 "stopping rules met" may be toxicity. Say "about 7-9 cited lack of efficacy" | CSV why_stopped; https://clinicaltrials.gov/api/v2/studies/NCT06566092 |
| 7 | "Those 99 trials had enrolled about 3,500 patients" | WRONG | Sum is 3,488 but 1,521 of it is the *estimated* (planned) enrolment of 8 SUSPENDED trials, incl. 1,122 for COG AOST2032 cabozantinib (NCT05691478, suspended "to extend observation", still planned); 26 withdrawn trials enrolled 0. Actually enrolled in terminated trials: 1,967 (63 actual + 2 estimated). Fair: "terminated trials had enrolled about 2,000 patients" | https://clinicaltrials.gov/api/v2/studies/NCT05691478 ; CSV enrollment_type |
| 9, 32-38 | 32 randomized osteosarcoma-only trials; period table (85/17/8/59/2 ... 62/23/5/33/13) | CONFIRMED | 1+8+3+4+11+5 = 32 across 1990-2029; table reproduced exactly. Report itself notes it is a floor (line 40) | CSV |
| 9 | "just one uses overall survival as its main measure" | WRONG | Artefact of first-match regex (EFS/PFS checked before OS). 4 os-only phase 2/3 trials name OS as a primary outcome: NCT00978471 (primary endpoint = OS, per its own paper cited at line 78), NCT07477457, NCT05691478, NCT05042934 (pattern match). Fair: "OS is the sole primary endpoint in only one; it is a primary endpoint in about four" | CSV primary_outcomes; PMID 31838406 abstract ("Primary endpoint was overall survival") |
| 42 | Endpoints EFS/PFS 45, response 24, other 20, toxicity 13, OS 1 | CONFIRMED (arithmetic) / OVERSTATED | Counts reproduce, but categories are mutually exclusive by priority order; should be labelled "first-matching endpoint" | tools/trial_analysis.py |
| 9 | China trials 1 (2010-14) to 32 (2020-24), "about one in five" | CONFIRMED | 32/165 = 19% | CSV |
| 28 | CabOSTar NCT06341712, 2024, closed after 10 patients | CONFIRMED | Ipsen, start 2024-11-22, 10 actual, terminated for recruitment | https://clinicaltrials.gov/api/v2/studies/NCT06341712 |
| 28 | Robatumumab NCT00617890, 219 enrolled, "strategic reasons, not for a safety concern" | CONFIRMED | Merck, 219 actual; quote exact. Note it HAS posted results, so "question left unanswered" (line 28) is overstated for this trial | https://clinicaltrials.gov/api/v2/studies/NCT00617890 |
| 28 | TIL trial in children NCT06566092 closed after 5 patients on a company decision | CONFIRMED / INTERNALLY INCONSISTENT | 5 actual, Iovance decision; but this trial is one of the 7 "lack of efficacy" in the table at line 21 | https://clinicaltrials.gov/api/v2/studies/NCT06566092 |
| 50 | NCT02273583, 2006, 738 planned, GRAACC | CONFIRMED | Start 2006-05, 738 estimated, sponsor GRAACC | https://clinicaltrials.gov/api/v2/studies/NCT02273583 |
| 51 | NCT01669369, 2013, 400, lithium, Chinese hospital | CONFIRMED | Sun Yat-sen University, phase 4, 400 estimated | https://clinicaltrials.gov/api/v2/studies/NCT01669369 |
| 52 | NCT04359550, 2020, 362, ZKAB001 vs placebo, Lee's Pharmaceutical | CONFIRMED | Phase 3, 362 estimated, status UNKNOWN | https://clinicaltrials.gov/api/v2/studies/NCT04359550 |
| 53 | NCT01002092, 2009, 160, Endostar, sponsor "Chinese hospital" | WRONG (sponsor) | Lead sponsor is Shandong Simcere-Medgenn Bio-pharmaceutical Co. (the Endostar manufacturer), not a hospital | https://clinicaltrials.gov/api/v2/studies/NCT01002092 |
| 54 | NCT03063983, 2017, 158, metastatic, GRAACC | CONFIRMED | GLATO2017 | https://clinicaltrials.gov/api/v2/studies/NCT03063983 |
| 46 | "Each of these enrolled or planned hundreds of patients" | OVERSTATED | Two of five planned 158-160; all five numbers are planned (estimated), none actual | CT.gov records above |
| 56 vs 50/77 | Brazilian trials "together planning nearly 900" | CONFIRMED | 738+158 = 896 | CT.gov |
| 58 | 23 trials ending 2010-2023 with no results and no citing paper, about 950 patients | CONFIRMED (arithmetic) / OVERSTATED | 23 trials, 949 patients. But the list includes non-therapeutic studies (exercise, analgesia, imaging, shock-wave on cells, observer presence) and NCT07893041; "work the field has lost" overstates | data/osteosarcoma_trials_publications.csv |
| 62 | NCT03909776 "Completed 2019, 99, intra-arterial cisplatin" | CONFIRMED / note | Registered as non-randomized, start 2019-01, completion 2019-04: a retrospective series (published, line 79). Line 58 heading "finished trials" is misleading for it | https://clinicaltrials.gov/api/v2/studies/NCT03909776 |
| 63 | NCT00978471 completed 2018, 44, thiotepa randomized | CONFIRMED | Population was *relapsed* osteosarcoma; wording omits this | https://clinicaltrials.gov/api/v2/studies/NCT00978471 |
| 64 | NCT02022358 terminated 2015, 34, glucarpidase | CONFIRMED | UCL, randomized, start 2007 | https://clinicaltrials.gov/api/v2/studies/NCT02022358 |
| 65 | NCT02718482 terminated 2019, 7, relapsed, randomized | CONFIRMED | Italian Sarcoma Group, OsteoREC2015 | https://clinicaltrials.gov/api/v2/studies/NCT02718482 |
| 69 | 45 US phase 2+ trials completed since 2018, 4 without results | CONFIRMED | Reproduced | CSV |
| 46-66 vs 73-85 | Line 46 "none has posted results"... "Some may have published"; line 58-65 tables list NCT02273583, NCT00978471, NCT03909776 as missing | INTERNALLY INCONSISTENT (stale text) | Update (lines 71-85) shows 3 of these were published. Lines 50, 56, 62-63 and Next step 2 (line 104: "five unknown ... four highlighted unpublished") are stale and should be struck through or rewritten | lines 50, 56, 62, 63, 104 vs 77-79 |
| 77 | GLATO 2006: 296 randomized; 5-y EFS 61% vs 64%, P=0.40; Senerchia, Cancer 2017, PMID 28263383 | CONFIRMED | Abstract: 296 randomized (139 vs 157), 61% vs 64%, P=.395. (Published Cancer 2017; erratum 2018) | https://pubmed.ncbi.nlm.nih.gov/28263383/ |
| 85, 90 | "tested in 296 children" | OVERSTATED | Eligibility was age 30 or younger; say "296 children and young adults" | PMID 28263383 |
| 78 | Thiotepa: 44 randomized, 2-y OS 66.7% vs 50.0%, P=0.61, Marec-Bérard EJC 2020, PMID 31838406 | CONFIRMED | P=0.6123 is the OS hazard-ratio test; relapsed population | https://pubmed.ncbi.nlm.nih.gov/31838406/ |
| 79 | IA cisplatin: retrospective, 48 vs 51, no benefit; Xie, Cancer Manag Res 2019, PMID 31447583 | CONFIRMED | IV arm were historical controls | https://pubmed.ncbi.nlm.nih.gov/31447583/ |
| 80 | ZKAB001 phase 1/2, 21 pts, 71% EFS at 24 mo; Zhou CCR 2023 PMID 36469563 | CONFIRMED | 24-mo EFS 71.4% (47.2-86.0) | https://pubmed.ncbi.nlm.nih.gov/36469563/ |
| 89, 103 | "The 92 trials with posted results on ClinicalTrials.gov" | WRONG / OVERSTATED | 147 studies in the CSV have posted results; 92 is the subset with status COMPLETED. The pooled-controls extraction (`data/osteosarcoma_posted_outcomes.csv`) covers 117 trials | CSV has_results; data/osteosarcoma_posted_outcomes.csv |
| 91 | Poor recruitment ended "six times as many trials as lack of efficacy" | CONFIRMED (arithmetic) | 44/7 = 6.3; subject to the classification caveat above | CSV |
| 91 | FOSTER platform NCT07871864 | CONFIRMED | Gustave Roussy, phase 3 randomized platform, recruiting, start 2026-10-07, 530 planned | https://clinicaltrials.gov/api/v2/studies/NCT07871864 |
| 92 | China trials "often without posted results" | UNVERIFIABLE (not quantified) | Easy to quantify from CSV; add a number | - |

## File 2: `reports/Osteosarcoma pooled control dataset.md`

Recomputation: `tools/pool_relapse_benchmarks.py` (print-only) re-run; the class table at lines 77-84 and the 14.2% / 271 and 49.6% / 174 figures at line 98 reproduce exactly. 16 registry numbers were re-derived directly from ClinicalTrials.gov `resultsSection` (marked "CT.gov re-derived").

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 3 | Raw extract: 2,783 efficacy rows from 117 trials | CONFIRMED | 2,783 rows, 117 unique NCT | data/osteosarcoma_posted_outcomes.csv |
| 3 | Published file: 60 rows, 32 trials, 26 new, about 738 more patients | OVERSTATED | 60 rows and 32 trial labels confirmed; 27 labels are not in the registry file (26 if one is excluded). Patient total double-counts Lagmay 2016: the pooled row (96) and its 7 component strata (96) are both present. Unique patients nearer 640 | data/osteosarcoma_relapse_benchmarks_published.csv |
| 9 | 147 trials with posted results, 117 report efficacy, 41 for osteosarcoma patients specifically | CONFIRMED (counts) / note | 147 / 117 / 41 reproduce. But the 41 includes trials mis-tagged `os_only` by `tools/trial_miner.py` (its BONE_OK regex accepts "recurrent", "metastatic", "neoplasm"), e.g. NCT05071209 (elimusertib: Ewing, ARMS, DDR tumours; no osteosarcoma condition). 28 of 140 interventional `os_only` trials list no osteosarcoma condition | tools/trial_miner.py; CSV conditions |
| 9, 19 | Eribulin AOST1322: 0/19 at 4 months | CONFIRMED (CT.gov re-derived) | Disease control success 0 of 19 | https://clinicaltrials.gov/api/v2/studies/NCT02097238 |
| 20 | Denosumab AOST1321 cohort 1: 1/15 (7%) | CONFIRMED (CT.gov re-derived) | 1 of 15 at 4 months | https://clinicaltrials.gov/api/v2/studies/NCT02470091 |
| 21 | Glembatumumab AOST1521: 3/22 (14%), first six cycles | CONFIRMED (CT.gov re-derived) | 3 of 22 | https://clinicaltrials.gov/api/v2/studies/NCT02487979 |
| 11, 22 | Olaparib + ceralasertib NCT04417062: 5/34 (15%) event-free at 4 months | CONFIRMED (CT.gov re-derived) | 5 of 34. Same record also gives KM EFS 15.8% (n=38) and a resected cohort 2 with 4/10 (40%) event-free at 12 months, omitted from the resected table | https://clinicaltrials.gov/api/v2/studies/NCT04417062 |
| 23-24 | Lenvatinib alone 32% (16-52), n=28; lenvatinib+IE 67% (38-88), n=15 | CONFIRMED (CT.gov re-derived) | 32.1 (15.9-52.4), 66.7 (38.4-88.2) | https://clinicaltrials.gov/api/v2/studies/NCT02432274 |
| 25 | CABONE 33% non-progression at 6 months (20-50%), n=42 | CONFIRMED (CT.gov re-derived) | 33.3 (19.6-49.6); paper abstract also 14/42 (33%) | https://clinicaltrials.gov/api/v2/studies/NCT02243605 ; https://pubmed.ncbi.nlm.nih.gov/32078813/ |
| 27 | Lagmay 2016: about 12% event-free at 4 months | CONFIRMED | 96 patients, 12% (95% CI 6-19%) | https://pubmed.ncbi.nlm.nih.gov/27400942/ |
| 33 | SARC024 regorafenib 3.6 mo (n=22) vs placebo 1.7 (n=20) | CONFIRMED (CT.gov re-derived) | 3.6 (2.0-7.6) vs 1.7 (1.2-1.8) | https://clinicaltrials.gov/api/v2/studies/NCT02048371 |
| 34 | OLIE median PFS 6.5 (n=40) vs 5.5 (n=41) | CONFIRMED (CT.gov re-derived) | HR 0.54 (0.27-1.08), 1-sided P=.04, did not meet significance threshold of .025. **Omitted:** median OS 11.9 vs 17.4 mo (HR 1.28) favouring IE alone; registry 1-y OS 49.2% vs 72.1% | https://clinicaltrials.gov/api/v2/studies/NCT04154189 ; https://pubmed.ncbi.nlm.nih.gov/39418029/ |
| 35 | Avelumab NCT03006848: median PFS 8.0 weeks, n=18, no responses | CONFIRMED (CT.gov re-derived) | 8.0 (6.7-9.1); response 0% | https://clinicaltrials.gov/api/v2/studies/NCT03006848 |
| 37 | OLIE "gap shrank to about one month" | CONFIRMED | Median 6.5 vs 5.5 | as above |
| 45 | Dinutuximab AOST1421: 11/39 (28%) at 12 months | CONFIRMED (CT.gov re-derived) | 11 of 39 | https://clinicaltrials.gov/api/v2/studies/NCT02484443 |
| 46 | Denosumab cohort 2: 10/38 (26%) | CONFIRMED (CT.gov re-derived) | 10 of 38 | https://clinicaltrials.gov/api/v2/studies/NCT02470091 |
| 48, 67, 91 | Resected-relapse benchmark "about 20% (range 10-34%)" | WRONG (wording) | 10-34% is the **95% confidence interval** of one trial (AOST0221, n=42), not a range across trials. Line 67's "the 10-34% range" inherits the error | https://pubmed.ncbi.nlm.nih.gov/27400942/ |
| 50, 67 | Resected-relapse results "cluster tightly"; the 12-month figure "mostly reflects who gets enrolled" | OVERSTATED | Two arms only (28%, 26%); NCT04417062 cohort 2 gave 40% (4/10), saracatinib/placebo trial (published file) medians 19.4 vs 8.6 mo. Present as a hypothesis | NCT04417062 record; published CSV rows 49-50 |
| 56-59 | EURAMOS-1 3-y EFS 74 (69-79) n=359; 77 (72-81) n=357; 55 (49-60) n=310; 53 (47-59) n=308 | CONFIRMED (CT.gov re-derived) | Exact match | https://clinicaltrials.gov/api/v2/studies/NCT00134030 |
| 9, 65, 86 | "Only the kinase-inhibitor pills clearly sit above the line"; "the only class above the line" | OVERSTATED / INTERNALLY INCONSISTENT | The update (line 84) shows IE chemotherapy alone at 56% in randomized controls, i.e. also far "above the line"; and imatinib (a kinase-inhibitor pill) is inside the 12% Lagmay pool at 0% and 18.5% in SARC (pool script). Say "VEGFR-targeting TKIs" | lines 81-84; tools/pool_relapse_benchmarks.py |
| 65 | AOST2032 suspended; CabOSTar closed after 10; no randomized TKI trial enrolling in the US | CONFIRMED | NCT05691478 SUSPENDED; NCT06341712 terminated at 10; no recruiting randomized TKI trial with a US site in the CSV | CT.gov records; CSV |
| 66 | "elimusertib (no responses in 22 patients across three groups, NCT05071209) ... sit at the benchmark" as osteosarcoma evidence | WRONG | The 22 phase-2 patients are Ewing/EWS-fusion (10), PAX3-FOXO1 ARMS (9) and DDR-altered solid tumours (3). The trial lists no osteosarcoma condition. It says nothing about osteosarcoma | https://clinicaltrials.gov/api/v2/studies/NCT05071209 |
| 66 | ATR/PARP "no single-agent signal" | OVERSTATED | Olaparib + ceralasertib is a combination, not single agent; with elimusertib removed, there is one ATR/PARP data point | NCT04417062 |
| 73 | OLIE IE alone 66% at 4 months; OAIE 42%; OLIE 76% vs 66% | CONFIRMED | OLIE 76.3% vs 66.0% (abstract); OAIE 65.8% vs 41.6% (full text) | https://pubmed.ncbi.nlm.nih.gov/39418029/ ; https://europepmc.org/article/PMC/PMC12647724 |
| 77-84 | Class table: 3/133/12.5%; 3/71/12.7%; 4/145/52.5%; 3/128/65.0%; 1/43/66.3%; 2/69/56.1% | CONFIRMED (arithmetic) / OVERSTATED (label) | Reproduced exactly. "Older chemotherapy (single agents)" includes the gemcitabine + nab-paclitaxel doublet and imatinib within the Lagmay pool. "Pill alone" mixes KM estimates (CABONE 71.4%, sorafenib, apatinib) with a binomial rate (lenvatinib 29%); using CABONE's crude primary endpoint (33% at 6 mo) instead of the 71.4% KM 4-month estimate would pull the class rate down substantially | tools/pool_relapse_benchmarks.py |
| 86 | OAIE 65.8% vs 41.6%, "a larger gap than OLIE's and deserves attention" | CONFIRMED / OVERSTATED | Numbers right. Omitted: OAIE median OS 18.1 vs 22.9 mo (HR 1.48) favouring IE alone; IE control had a 2:1 randomization (n=28); authors call results exploratory | https://europepmc.org/article/PMC/PMC12647724 ; https://pubmed.ncbi.nlm.nih.gov/41290609/ |
| 89 | Lagmay Table 2: docetaxel 23%, oxaliplatin 31%, ixabepilone 9%, rebeccamycin 6%, topotecan/irinotecan/imatinib 0% | UNVERIFIABLE (this pass) | Full text (PMC5012712) is not open access via API and pmc.ncbi.nlm.nih.gov was blocked from this workspace. Values are internally consistent with the 96-patient pooled 12% | https://pubmed.ncbi.nlm.nih.gov/27400942/ |
| 90 | "CABONE's registry figure is 33% at six months, against 52% at six months (and 71% at four) in the paper" ("registry and paper disagree") | OVERSTATED / misleading | The paper's own primary endpoint is also 33% (14/42) 6-month non-progression, the same as the registry. 52%/71% are KM PFS estimates from the same paper, a different estimator. So there is no conflict, and swapping in the KM figure inflates the pooled pill rate | https://pubmed.ncbi.nlm.nih.gov/32078813/ |
| 91 | "No newer COG pooled benchmark for osteosarcoma exists" | UNVERIFIABLE (absolute) | Soften to "we found no newer..." | - |
| 92 | 27 of 60 rows "abstract only" | CONFIRMED | 27 rows contain "abstract only" | published CSV |
| 96 | 114 basket trials with posted results searched; 16 basket trials and about 400 osteosarcoma patients added | CONFIRMED / OVERSTATED | 114 confirmed. Basket file has 17 NCTs (16 basket + St Jude); summing the largest arm per trial gives about 320 in basket trials (about 360 with St Jude); "about 400" is high unless multiple arms and the St Jude trial are counted | data/osteosarcoma_relapse_benchmarks_basket.csv |
| 96 | St Jude bevacizumab + MAP 3-y EFS 57.5% | CONFIRMED (CT.gov re-derived) | 0.575 (0.402-0.747), stratum A, n=31 | https://clinicaltrials.gov/api/v2/studies/NCT00667342 |
| 98 | Non-pill, non-IE arms: 8 arms, 271 pts, 14.2%; pills 49.6% / 174 with ADVL1622 | CONFIRMED (arithmetic) / OVERSTATED | Reproduced. But the ADVL1622 value (35%) is "response + disease control over first 6 cycles", not a 4-month PFS rate; its own 1-y PFS is 14.7% | https://clinicaltrials.gov/api/v2/studies/NCT02867592 |
| 101 | PAZOTOP 69.6% PFS at 12 weeks, 28 osteosarcoma patients | CONFIRMED in CSV / partly re-derived | Registry gives the osteosarcoma median PFS 4.47 mo (n=28); the 12-week 69.6% rate is from the paper abstract (Br J Cancer 2021, PMID 34050255), not checked in full | https://clinicaltrials.gov/api/v2/studies/NCT02357810 |
| 102 | ADVL1622: about 35% response or stable disease; 14.7% PFS at 1 year | CONFIRMED (CT.gov re-derived) | 35.18% (20.16-48.27) "Response + Disease Control"; 1-y PFS 14.71% (4.66-30.19); 1-y OS 35.86% | https://clinicaltrials.gov/api/v2/studies/NCT02867592 |
| 103 | Cixutumumab + temsirolimus 3/24 adults vs 0/10 children | CONFIRMED in CSV | Basket rows: Schwartz Lancet Oncol 2013 (PMID 23477833) 3/24; ADVL1221 0/10 registry. Different trials and IGF-1R selection, so not a like-for-like age comparison | https://clinicaltrials.gov/api/v2/studies/NCT01614795 |
| 104 | "Checkpoint inhibitors are confirmed inactive": nivolumab 0/10, nivo+ipi 0/10, pembrolizumab+cyclophosphamide 1/15 | OVERSTATED | Counts match CSV, but cohorts of 10-15 cannot "confirm" inactivity; SARC028 (1/22) and pembrolizumab (0/12) support "minimal single-agent activity". Combinations with TKIs (APFAO 66% at 4 mo) are listed elsewhere in the same report | basket CSV; https://clinicaltrials.gov/api/v2/studies/NCT02304458 |
| 110 | "Only trials that posted results are included" | INTERNALLY INCONSISTENT (stale) | Lines 69-106 added 60 published-paper rows and basket rows | lines 69-98 |
| 112 | "Basket-trial arms that mix cancers are ... excluded from the tables above" | INTERNALLY INCONSISTENT (stale) | Line 98 pools basket arms (R1507, imatinib, ADVL1622) | line 98 |
| 113 | "The historical benchmarks come from the research report's sources, not from this dataset" | INTERNALLY INCONSISTENT (stale) | Lagmay 2016 and AOST0221 are now rows in the published CSV | published CSV rows 0-8 |
| 117 | Next step: add Lagmay 2016 arm-level results | INTERNALLY INCONSISTENT (stale) | Already done (published CSV rows 0-8, line 89) | - |

Addendum to File 1:

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 40 | "The filter is strict, so ... the randomized counts are a floor" | WRONG | The `os_only` filter in `tools/trial_miner.py` is leaky as well as strict: its BONE_OK regex accepts any condition containing "recurrent", "refractory", "metastatic", "lung" or "neoplasm". So 28 of 140 interventional `os_only` trials list no osteosarcoma condition (e.g. NCT05071209, NCT05042934, NCT07194044 are Ewing/ARMS trials; NCT01291017 is lung cancer). 4 of the 32 "randomized osteosarcoma-only" trials (NCT00538239 soft-tissue + bone sarcoma, NCT04963517, NCT07619950, NCT07888244 bone sarcoma/tumour) do not name osteosarcoma. Counts are neither floors nor ceilings | tools/trial_miner.py lines 14-16, 41; CSV conditions |
| 80 | ZKAB001 (socazolimab) "approved in China for cervical cancer" | UNVERIFIABLE | Sources conflict: Lee's Pharm announced NMPA acceptance of the NDA; one antibody database lists it as approved. No NMPA notice found | https://www.leespharm.com/announcements/voluntary-announcement-new-drug-application-of-socazolimab-for-treatment-of-recurrent-or-metastatic-cervical-cancer-submitted-and-accepted-by-nmpa ; https://db.antibodysociety.org/db0/161 |

## File 3: `reports/Why kinase-inhibitor pills work in osteosarcoma.md`

| Line | Claim | Verdict | Correct wording / note | Source |
|---|---|---|---|---|
| 1, 7 | Title "Why kinase-inhibitor pills work"; "Eight oral multi-kinase inhibitors ... are the only drug class that clearly keeps relapsed osteosarcoma in check better than older drugs" | OVERSTATED | Non-VEGFR kinase-inhibitor pills did not work: imatinib (0% in COG, 18.5% in SARC), dasatinib (10.9% 6-mo PFS, SARC009), alisertib 0/10. Evidence for sunitinib (only with nivolumab, n=17, median PFS 3.5 mo) and pazopanib (n=8; or with topotecan) is thin. IE chemotherapy alone also gave 42-66% at 4 months. Fair: "VEGFR2-targeting TKIs, with the best evidence for regorafenib, cabozantinib, sorafenib, apatinib and lenvatinib" | basket/published CSVs; PMID 31013172, 30477937 |
| 7, 17, 74 | CABONE: 71% PFS at 4 months, 52% at 6, 9.5% at 12; median OS 10.6 mo; 12% PR | CONFIRMED | Full text: 71.4 / 52.4 / 9.5%; median OS 10.6 (registry posts 10.4); 5/42 PR. **But** the trial's own primary endpoint, 6-month non-progression, was 33% (14/42); the report never states it | https://europepmc.org/article/PMC/PMC8763616 ; https://pubmed.ncbi.nlm.nih.gov/32078813/ |
| 7, 25 | In both randomized pill+IE trials "overall survival was numerically shorter in the pill arms"; "both point the same way" | OVERSTATED | True for medians, but OLIE's final analysis at FDA request gave OS HR 0.93 (0.53-1.62), i.e. no difference; only the earlier HR was 1.28. Line 78 says this, so the summary is inconsistent with the body | https://europepmc.org/article/PMC/PMC11581622 |
| 7 | "PET scans dim within four weeks" | CONFIRMED | 64.5% (20/31) partial metabolic response after one 28-day cycle | PMC8763616 |
| 7, 38, 151 | About 40% of tumours carry VEGFA (6p21) or 4q12 (KDR/PDGFRA/KIT) amplification | CONFIRMED | MSK-IMPACT, 66 patients: 4q12 13/66 (20%), VEGFA 14/66 (24%); authors: "at least 40%" | https://pubmed.ncbi.nlm.nih.gov/31175097/ |
| 15 | SARC024: 42 pts, PFS 3.6 vs 1.7 mo, HR 0.42, no OS difference with crossover | CONFIRMED | HR 0.42 (0.21-0.85), P=.017 | https://pubmed.ncbi.nlm.nih.gov/31013172/ |
| 16 | REGOBONE: 38 evaluable, 65% vs 0% non-progressive at 8 weeks | CONFIRMED | 17/26 vs 0/12 | https://pubmed.ncbi.nlm.nih.gov/30477937/ |
| 18 | ADVL1622: 29 pts, response or disease control 35%; 1-y PFS 14.7%; 1-y OS 35.9%; no paper found | CONFIRMED (CT.gov re-derived) / UNVERIFIABLE ("no paper") | 35.18%, 14.71%, 35.86%. No osteosarcoma paper found in this audit either | https://clinicaltrials.gov/api/v2/studies/NCT02867592 |
| 19 | Apatinib: 37 pts, 4-mo PFS 57%, ORR 43%, median PFS 4.5 | CONFIRMED | 56.76%, 16/37, 4.50 mo. Single centre, age 16 or older | https://pubmed.ncbi.nlm.nih.gov/30559126/ |
| 20 | Sorafenib: 35 pts, 4-mo PFS 46%, median PFS 4 | CONFIRMED | | https://pubmed.ncbi.nlm.nih.gov/21527590/ |
| 21 | Lenvatinib ITCC-050: 31, 4-mo PFS 29-38%, median 3.0 | CONFIRMED (CSV; abstract partly) | Registry for cohort 2B: 32.1% (n=28) | https://pubmed.ncbi.nlm.nih.gov/34562750/ ; NCT02432274 |
| 22 | OLIE: 81, PFS 6.5 vs 5.5, HR 0.54 not significant; OS 11.9 vs 17.4 | CONFIRMED | 1-sided P=.04 vs threshold .025 | https://pubmed.ncbi.nlm.nih.gov/39418029/ |
| 23 | OAIE: 81, PFS 5.5 vs 3.4, HR 0.60; OS 18.1 vs 22.9, HR 1.48 | CONFIRMED | Full text | https://europepmc.org/article/PMC/PMC12647724 |
| 33 | VEGFA 23% in Sayles whole genomes | UNVERIFIABLE | PMC7134333 full text returned errors (Europe PMC 500; PMC host blocked) | PMC7134333 |
| 35 | FGFR1 amplified in 18.5% of poor responders, none of good responders, 352 samples | CONFIRMED | 352 samples from 288 patients, FISH | https://pubmed.ncbi.nlm.nih.gov/24861215/ |
| 36 | MET first cloned from an osteosarcoma cell line | CONFIRMED | TPR-MET from the MNNG-treated HOS osteosarcoma line (Cooper et al., 1984), standard history | - |
| 41, 38, 42-43, 48, 64, 68, 89-92 | Lab and small-series claims (Sayles PDX; PMIDs 37812025, 24687604, 29520051, 20003259, 32021426, 32215805, 37724607, 37073613, 42856637, ...) | UNVERIFIABLE (not checked in this pass) | Not re-read; the report itself flags several as abstract-only. 42856637 is described as a preprint but carries a PMID; confirm what it is | - |
| 46 | CABONE: 12 of 90 had a collapsed lung, all with sub-pleural metastases; 7 cavitated; one resected responder had no live tumour | CONFIRMED / note | 12/90 (13.3%), but 8 of the 12 were Ewing sarcoma and 4 osteosarcoma | PMC8763616 |
| 47 | 65% partial metabolic response after one cycle; median PFS 7.2 vs 1.8 mo | CONFIRMED | 64.5%; 7.2 (PMR) vs 1.8 (PMD), p<.0001 | PMC8763616 |
| 49 | Apatinib "gave the highest response rate (43%)" | OVERSTATED | Cross-trial comparison: single centre, investigator-assessed, adults 16 and older. The 43% includes unconfirmed responses; not comparable with CABONE's centrally reviewed 12% | PMID 30559126 |
| 51, 105 | APFAO did not reach target: 6-mo PFS 51% vs target 60% | CONFIRMED | 50.9% (34.6-65.0); target P1 60% | https://europepmc.org/article/PMC/PMC7223462 |
| 55 | Quote "despite responses in up to 40% of patients, there are as yet no validated predicted biomarkers..." | CONFIRMED | Verbatim | https://europepmc.org/article/PMC/PMC11334773 |
| 59 | Lung-only 6.9 vs 2.1 mo with bone/soft-tissue lesions only; lesion site only independent factor | CONFIRMED | "musculoskeletal lesions only" 2.1; multivariate p=0.004 | PMC7223462 |
| 62 | PD-L1 ≥5%: p=0.004; 6 of 28 positive | CONFIRMED | | PMC7223462 |
| 77 | Crossover: 10 of 20 (SARC024) and 10 of 12 (REGOBONE) | CONFIRMED | Abstracts: 10 placebo patients crossed over in each | PMID 31013172; 30477937 |
| 78 | OLIE 12-mo OS 49% vs 72% (HR 1.28); final analysis at FDA request HR 0.93; more IE patients went to surgery/later treatment | CONFIRMED | Registry 1-y OS 49.2 vs 72.1; paper text | NCT04154189; PMC11581622 |
| 79 | OAIE: 30% vs 19% received no further treatment | CONFIRMED | 30.2% vs 18.9% | PMC12647724 |
| 102 | Sorafenib + everolimus 6-mo PFS 45%, missed 50% target | CONFIRMED | 17/38 (45%, 95% CI 28-61) | https://pubmed.ncbi.nlm.nih.gov/25498219/ |
| 104 | OAIE "lower ifosfamide dose given for longer" | OVERSTATED / incomplete | The relevant fact is that the **control** arm got IE on days 1-5 while the apatinib arm got the same daily doses on days 1-3 only (40% less chemotherapy per cycle). "Longer" refers to more cycles than OLIE. State the asymmetry | https://pubmed.ncbi.nlm.nih.gov/41290609/ |
| 108 | Sunitinib + losartan (NCT03900793); toceranib + losartan 50% clinical benefit in 28 dogs | CONFIRMED | Phase 1, recruiting; CBR 50% in dogs with lung metastases | NCT03900793; https://pubmed.ncbi.nlm.nih.gov/34580111/ |
| 108 | SARC038 active not recruiting; NCT05019703, NCT05182164, NCT06156410 running; NCT07619950 not yet open | CONFIRMED | Statuses match registry | CT.gov API records |
| 111-115 | No trial of pill + selective FGFR, MET or FAK blocker; no biomarker-selected trial | CONFIRMED (within CT.gov osteosarcoma set) | No combination found in `osteosarcoma_trials.csv` interventions; excludes non-CT.gov registries | CSV |
| 116 | Resected-relapse benchmark "20% event-free at 12 months, range 10-34%" | WRONG | 10-34% is the 95% CI of AOST0221 (n=42), not a range (same error as pooled report lines 48/67/91) | https://pubmed.ncbi.nlm.nih.gov/27400942/ |
| 116, 144 | NCT04055220 randomizes regorafenib maintenance vs observation, recruiting since 2020 | CONFIRMED | REGOSTA, start 2020-03-03, 168 planned. This contradicts pooled-report line 65 only in part: it is French, not US | https://clinicaltrials.gov/api/v2/studies/NCT04055220 |
| 121-122 | NCCN v3.2023 lists regorafenib/sorafenib (second line), cabozantinib and sorafenib+everolimus; ESMO 2021 | UNVERIFIABLE | Secondhand, as the report says | - |
| 123 | No regulator has approved any of these for osteosarcoma; cabozantinib FDA-approved from age 12 for thyroid and neuroendocrine cancers; 40 mg under 40 kg, 60 mg above | CONFIRMED | Current label uses a 40 kg bodyweight cut-off (older 2021 label used BSA 1.2 m²) | https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/208692s017lbl.pdf |
| 125 | US cash price US$26,000-48,000 / 30 tablets; NHS £5,143 | UNVERIFIABLE (not checked) | Cited to price sites | - |
| 131 | Growth plates: 5 of 53 (9.4%), sunitinib/pazopanib, reversible | CONFIRMED | 1 sunitinib, 4 pazopanib | https://pubmed.ncbi.nlm.nih.gov/25257751/ |
| 132 | Apatinib severe wound breakdown 11% | CONFIRMED | Grade 3-4 wound dehiscence 4/37 (10.8%) | PMID 30559126 |
| 133 | Collapsed lung 9% (cabozantinib) to 18% (lenvatinib + IE) | CONFIRMED / note | Cabozantinib figure is grade 3-4 in osteosarcoma (4/45); any-grade across CABONE 13%. OLIE 17.9% treatment-related, 28.2% any cause | PMC8763616; PMC11581622 |
| 141 | AOST2032: 1,122 planned; suspended "Extend the observation period..." updated 27 Oct 2026; dose-finding closed May 2025 | CONFIRMED | Last update 2026-10-27; feasibility arm "CLOSED TO ACCRUAL 05/09/2025" | https://clinicaltrials.gov/api/v2/studies/NCT05691478 |
| 142 | CabOSTar terminated after 10 patients (Nov 2024 - Feb 2026), recruitment | CONFIRMED | | NCT06341712 |
| 143 | FOSTER-CabOS: 12 months cabozantinib vs BSC, 530 planned, 8 European countries, recruiting since 7 Oct 2026 | CONFIRMED / note | 12 x 28-day cycles; 8 countries. 530 is the whole FOSTER platform enrolment, not the CabOS randomization | https://clinicaltrials.gov/api/v2/studies/NCT07871864 |
| 145 | NCT04351308 status unknown since 2020 | CONFIRMED | Start 2020-05, UNKNOWN | https://clinicaltrials.gov/api/v2/studies/NCT04351308 |
| 147 | "the gain is about two months of disease control" | CONFIRMED (approx.) | SARC024 +1.9 mo, OAIE +2.1, OLIE +1.0 median PFS | as above |
| 3 vs pooled report | "their numbers are not re-derived here" yet the kinase report presents CABONE 71% (KM) while the pooled report line 90 presents the same data as a registry-vs-paper conflict | INTERNALLY INCONSISTENT | Use one framing in both reports: primary endpoint 33% at 6 months (crude), KM PFS 71% at 4 months | pooled line 25, 90; kinase line 17 |

## Cross-report inconsistencies

| Where | Conflict | Fix |
|---|---|---|
| Landscape lines 89, 103 vs pooled line 9 | "92 trials with posted results" vs "147 osteosarcoma trials with posted results" | 147 have results; 92 are the completed subset. Use 147 |
| Landscape line 7 vs CSV | "about 3,500 patients" in stopped trials includes 1,521 planned patients in 8 suspended trials (1,122 in AOST2032, which the kinase report rightly calls "1,122 planned") | Say about 2,000 actually enrolled in terminated trials |
| Pooled lines 48, 67, 91; kinase line 116 | "range 10-34%" | 95% CI of a single trial |
| Pooled line 25/90 vs kinase lines 7/17 | CABONE 33% vs 71%/52% presented as a registry-vs-paper conflict in one report and as the headline in the other | State both: 33% crude primary endpoint at 6 months; KM PFS 71% at 4 months |
| Pooled line 66 vs registry | Elimusertib used as osteosarcoma evidence | Delete; not an osteosarcoma cohort |

## Top 10 must-fix

1. **Elimusertib (pooled report line 66) is not osteosarcoma evidence.** NCT05071209's 22 phase-2 patients are Ewing, ARMS and DDR-altered solid tumours. Delete it from the ATR/PARP argument. The root cause is #2.
2. **The `os_only` tag is leaky (landscape line 40, all derived counts).** `tools/trial_miner.py` treats "recurrent/refractory/metastatic/lung/neoplasm" conditions as osteosarcoma synonyms. 28 of 140 interventional "osteosarcoma-only" trials list no osteosarcoma condition, and 4 of the "32 randomized" trials do not either. Fix the regex, re-run, and remove the claim that the counts are "a floor".
3. **"Just one uses overall survival as its main measure" is wrong (landscape line 9).** It is an artefact of first-match classification; at least NCT00978471 (whose paper the report itself cites) has OS as its primary endpoint. About four trials name OS.
4. **"Those 99 trials had enrolled about 3,500 patients" is wrong (landscape line 7).** 1,521 are planned numbers for suspended trials (1,122 for AOST2032 alone) and withdrawn trials enrolled 0. Terminated trials enrolled about 2,000.
5. **"Range 10-34%" is a 95% confidence interval (pooled lines 48, 67, 91; kinase line 116).**
6. **CABONE framing (pooled line 90; kinase lines 7, 17).** The paper's own primary endpoint (33% non-progression at 6 months) matches the registry. The 71%/52% figures are KM estimates. Using 71.4% inflates the pooled "pill alone" class rate (52.5%). State the primary endpoint and consider a sensitivity analysis.
7. **Stale text the Updates overturn.**
   - Landscape lines 46, 50, 56, 62-63 and 104 still list GLATO 2006, thiotepa and IA cisplatin as missing or unpublished.
   - Pooled lines 110, 112, 113 and 117 say only registry results and no basket arms are included, and propose adding Lagmay, which is already done.
   - Pooled lines 9/65 ("only the pills sit above the line") are contradicted by IE alone at 56% (line 84).
8. **Title and summary of the kinase report overstate the class.** "Kinase-inhibitor pills work" ignores the imatinib, dasatinib and alisertib failures and the thin sunitinib/pazopanib data. Say "VEGFR2-targeting TKIs". The summary's "OS numerically shorter in both randomized trials" should note OLIE's final OS HR of 0.93.
9. **OLIE/OAIE survival omitted in the pooled report (lines 34, 73, 86).** Its praise of OAIE's larger PFS gap omits that OS favoured IE alone in both trials (HR 1.28 then 0.93; HR 1.48). It also omits that OAIE's control arm received 5 days of IE against 3 days in the apatinib arm (kinase line 104 garbles this).
10. **"92 trials with posted results" (landscape lines 89, 103) conflicts with 147 in the pooled report.** Also fix:
    - Endostar NCT01002092's sponsor is Shandong Simcere-Medgenn, not "Chinese hospital" (landscape line 53).
    - "296 children" should be "296 children and young adults up to age 30".
    - "Checkpoint inhibitors are confirmed inactive" should be "showed minimal activity in small cohorts".

## Method notes and limits of this audit

- Re-derived from ClinicalTrials.gov API v2 `resultsSection`: NCT02097238, NCT02470091 (both cohorts), NCT02487979, NCT04417062, NCT02432274 (2 cohorts), NCT02243605, NCT02048371, NCT04154189 (PFS and OS), NCT03006848, NCT02484443, NCT00134030 (4 arms), NCT02867592, NCT00667342, NCT02357810, NCT05071209. That is 16 trials and more than 25 numbers.
- Not verified, because pmc.ncbi.nlm.nih.gov was blocked and Europe PMC full text failed for some IDs: Lagmay 2016 Table 2 per-drug values, Sayles 2019 (PMC7134333), and most preclinical PMIDs in the kinase report.
- Stop-reason and endpoint arithmetic was checked by re-running `tools/trial_analysis.py` on a scratch copy; the committed flags file is byte-identical.
