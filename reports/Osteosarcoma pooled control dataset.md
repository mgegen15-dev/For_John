# A first pooled control dataset for osteosarcoma trials

*Built from arm-level results that sponsors posted to ClinicalTrials.gov, then extended with published papers and with osteosarcoma cohorts pulled out of basket trials. Last revised November 14, 2026, after an independent audit. Scripts: `tools/pooled_controls.py` (registry extract), `tools/pool_relapse_benchmarks.py` (class pooling). Raw extract: `data/osteosarcoma_posted_outcomes.csv`, with 2,783 efficacy rows from 117 trials. Curated tables:*

- *`data/osteosarcoma_relapse_benchmarks.csv`: registry results.*
- *`data/osteosarcoma_relapse_benchmarks_published.csv`: 60 rows from published papers.*
- *`data/osteosarcoma_relapse_benchmarks_basket.csv`: 33 rows from basket trials.*

*Each row records its source and whether the full text or only the abstract was read. Notes: `research_notes/Pooled controls/published_results_notes.md`, `research_notes/Pooled controls/basket_trials_notes.md`.*

## Summary

Osteosarcoma has no shared, standardized set of control outcomes against which to judge small single-arm trials, a gap the European FOSTER consortium names. This dataset is a first public version, built from registry results, published papers and basket trials. In measurable relapsed disease, drugs without a VEGFR-blocking kinase inhibitor leave about **14% of patients event-free at four months**, close to the historical benchmark of 12%. VEGFR-blocking kinase-inhibitor pills given alone reach roughly **40–50%**, depending on how the cabozantinib trial is counted. But ifosfamide plus etoposide (IE) chemotherapy alone also reaches **42–66%**, so combinations with IE must be judged against IE, not against 12%. In the two randomized pill-plus-IE trials, adding the pill delayed progression but did not improve overall survival.

**How to read the labels.** After each key number we say where it comes from:

- **(registry)**: read from the ClinicalTrials.gov record.
- **(paper, full text)**: read in the full published paper.
- **(paper, abstract only)**: read only in the abstract.
- **(press release only)**: reported by a company or the media, not in a peer-reviewed paper.
- **(our calculation)**: counted or computed by this project from the files above.

## What is in the dataset

- **Registry.** 147 studies in the osteosarcoma trial file have posted results. 117 of them report efficacy outcomes, and 34 report them for osteosarcoma patients specifically: an arm named for osteosarcoma, or a trial that enrols only osteosarcoma (registry; our calculation).
- **Published papers.** These add 26 trials not in the registry file (about 740 patients), plus paper figures for registry trials. The 26 are the seven COG trials pooled in Lagmay 2016, the AOST0221 resected-relapse trial and 18 others (our calculation). The Lagmay pooled row and its seven component trials describe the same 96 patients, so we count them once. Leaving out ARTEMIS-011, a phase 3 trial in patients with two or more earlier treatments, gives about 620.
- **Basket trials.** We searched the 114 basket trials with posted results and their papers. This adds 16 basket trials with about 400 osteosarcoma patients in separate arms: 332 in measurable relapse and 68 in resected relapse (our calculation). It also adds one St Jude trial, wrongly tagged as basket, which is in fact osteosarcoma-only.

## Measurable relapsed disease

Patients with relapsed osteosarcoma that can be measured on scans and cannot be fully removed by surgery.

**Single-arm and per-arm results:**

| Agent | Trial | Patients | Event-free or progression-free at about 4 months |
|---|---|---|---|
| Eribulin | NCT02097238 (COG AOST1322) | 19 | 0% (registry) |
| Denosumab | NCT02470091 (COG AOST1321), cohort 1 | 15 | 7%, 1 patient (registry) |
| Glembatumumab vedotin | NCT02487979 (COG AOST1521) | 22 | 14%, 3 patients, over the first six cycles (registry) |
| Olaparib + ceralasertib | NCT04417062 | 34 | 15%, 5 patients (registry). The same record gives a Kaplan–Meier estimate of 15.8% in 38 patients |
| Lenvatinib alone | NCT02432274 (ITCC-050) | 28 | 32% (95% CI 16–52%) (registry). The paper gives 29% in 31 patients by simple count and 38% by Kaplan–Meier (paper, full text) |
| Lenvatinib + IE | NCT02432274 (ITCC-050), cohort 3B | 15 | 67% (95% CI 38–88%) (registry). The paper gives 51% across 35 patients at the recommended dose (paper, abstract only) |
| Cabozantinib | NCT02243605 (CABONE) | 42 | Primary endpoint: 33% (14 of 42) free of progression at **6 months** (95% CI 20–50%) (registry; same figure in the paper, abstract only). Kaplan–Meier progression-free survival: 71% at 4 months and 52% at 6 months (paper, full text) |

**Historical benchmark:** Lagmay 2016 pooled seven COG phase 2 trials, 96 patients, and found about 12% event-free at four months (95% CI 6–19%) (paper, full text).

**About CABONE's two figures.** These measure different things; they are not a conflict between registry and paper. The trial's own primary endpoint is a simple count at 6 months, 33%, and it is the same in the registry and the paper. The 71% and 52% figures are Kaplan–Meier estimates from the same paper. Using the 71% figure raises the pooled "pill alone" rate (see the class table below).

**Randomized and median-based results:**

| Comparison | Trial | Median progression-free survival | Overall survival |
|---|---|---|---|
| Regorafenib against placebo | NCT02048371 (SARC024), osteosarcoma cohort | 3.6 months (n=22) against 1.7 months (n=20) (registry); HR 0.42 (paper, abstract only) | No difference shown; placebo patients could cross over |
| Lenvatinib + IE against IE | NCT04154189 (OLIE) | 6.5 months (n=40) against 5.5 months (n=41) (registry). HR 0.54 (0.27–1.08); one-sided P = 0.04, which missed the trial's 0.025 threshold (paper, full text) | Median 11.9 against 17.4 months, HR 1.28, at the primary analysis. HR 0.93 (0.53–1.62) at the final analysis requested by the FDA (paper, full text) |
| Apatinib + IE against IE | NCT05277480 (OAIE, China, randomized 2:1) | 5.5 against 3.4 months, HR 0.60 (paper, full text) | Median 18.1 against 22.9 months, HR 1.48, favouring IE alone (paper, full text) |
| Avelumab, single arm | NCT03006848 | 8.0 weeks (n=18), no responses (registry) | — |

OLIE shows why randomized controls matter. The single-arm lenvatinib + IE result looked striking (67% at four months), but IE alone gave 66% in OLIE's control arm. On progression-free survival at four months the gap was 76% against 66% (paper, full text).

OAIE showed a larger gap, 66% against 42% at four months (paper, full text). Three points temper it:

- **Survival.** Overall survival favoured IE alone (HR 1.48).
- **Less chemotherapy in the pill arm.** The control arm received IE on days 1–5 of each cycle, while the apatinib arm received the same daily doses on days 1–3 only, about 40% less chemotherapy per cycle (paper, abstract only).
- **Exploratory.** The authors call the results exploratory.

## Pooled 4-month rate in measurable relapse, by drug class

One row per trial arm, weighted by patients. Paper values replace registry values where both exist. The table mixes Kaplan–Meier estimates and simple counts, so treat it as approximate. The ranges are rough normal approximations and ignore differences between trials (our calculation; `tools/pool_relapse_benchmarks.py`).

| Drug class | Trial arms | Patients | 4-month rate | Range across arms |
|---|---|---|---|---|
| Older chemotherapy: COG pooled single agents (which include imatinib), eribulin, gemcitabine + nab-paclitaxel | 3 | 133 | 12.5% | 0–28% |
| Antibodies, drug conjugates, DNA-repair drugs (denosumab, glembatumumab, olaparib + ceralasertib) | 3 | 71 | 12.7% | 7–15% |
| IGF-1R antibody (R1507, basket trial) | 1 | 40 | 19.7% | — |
| Kinase inhibitor that does not target VEGFR (imatinib, adult basket trial) | 1 | 27 | 18.5% | — |
| **VEGFR-blocking kinase inhibitor alone** (sorafenib, apatinib, lenvatinib, cabozantinib) | 4 | 145 | **52.5%** | 29–71% |
| VEGFR-blocking kinase inhibitor + IE (ITCC-050, OLIE, OAIE) | 3 | 128 | 65.0% | 51–76% |
| VEGFR-blocking kinase inhibitor + PD-1 antibody (APFAO) | 1 | 43 | 66.3% | — |
| IE alone (OLIE and OAIE randomized control arms) | 2 | 69 | 56.1% | 42–66% |

**Sensitivity checks** (our calculation):

- **CABONE primary endpoint.** Using CABONE's primary endpoint (33% at 6 months) instead of its 4-month Kaplan–Meier estimate (71%) lowers the pill-alone rate from 52.5% to **41.4%**. The true 4-month figure for the class therefore lies roughly between 40% and 50%.
- **Adding ADVL1622.** Adding the second cabozantinib cohort, COG ADVL1622, gives 49.6% across 174 patients. Its 35% is a "response or disease control over six cycles" rate, not a 4-month progression-free rate, so it is left out of the main table.
- **All arms without a VEGFR inhibitor or IE.** Pooling the 8 arms that contain neither a VEGFR-blocking pill nor IE (271 patients) gives **14.2%**, close to the 12% benchmark.

**What this shows.**

- **Pills alone versus other single agents.** VEGFR-blocking kinase-inhibitor pills given alone sit well above every single-agent class without a VEGFR inhibitor. That is the most consistent signal in relapsed osteosarcoma.
- **The class is VEGFR inhibitors, not kinase inhibitors in general.** Imatinib, which does not block VEGFR2, sat at 0% in the COG pool and 18.5% in an adult basket trial (paper, abstract only).
- **IE sets the bar for combinations.** IE chemotherapy alone also sits well above 12%, so any regimen containing IE, or a similar chemotherapy partner, must be compared with IE's 42–66%, not with 12%.

## Resected relapse

Patients whose relapse has been completely removed by surgery, so there is nothing to measure.

| Agent | Trial | Patients | Event-free at 12 months |
|---|---|---|---|
| Dinutuximab + GM-CSF | NCT02484443 (COG AOST1421) | 39 | 28%, 11 patients (registry) |
| Denosumab | NCT02470091 (COG AOST1321), cohort 2 | 38 | 26%, 10 patients (registry) |
| Olaparib + ceralasertib | NCT04417062, cohort 2 | 10 | 40%, 4 patients (registry) |

**Historical benchmark:** in COG AOST0221, 42 patients with a first, completely resected lung relapse, 20% were event-free at 12 months. The 95% confidence interval was 10–34% (paper, full text). That interval is the uncertainty around one trial's estimate, not a range across trials.

The only randomized comparison found is a small one. In the SARC saracatinib trial after lung metastasis surgery, median progression-free survival was 19.4 months with saracatinib (n=18) and 8.6 months with placebo (n=19), P = 0.47 (paper, full text).

Two drugs with very different mechanisms, an anti-GD2 antibody and a bone-targeted RANKL antibody, gave similar 12-month results in the two larger arms (26–28%). One possible explanation is that the 12-month figure depends more on which patients are enrolled after surgery than on the drug. *This is a hypothesis.* There are only two comparable arms, and the small olaparib + ceralasertib cohort reached 40%. Either way, a randomized trial in this setting (gap 2 in the research report) is the only way to tell drug effect from patient selection.

## Newly diagnosed disease

| Group | Trial | Patients | 3-year event-free survival |
|---|---|---|---|
| Good responders, MAP | NCT00134030 (EURAMOS-1) | 359 | 74% (69–79%) (registry) |
| Good responders, MAP + pegylated interferon | NCT00134030 | 357 | 77% (72–81%) (registry) |
| Poor responders, MAP | NCT00134030 | 310 | 55% (49–60%) (registry) |
| Poor responders, MAP + ifosfamide/etoposide | NCT00134030 | 308 | 53% (47–59%) (registry) |
| MAP + bevacizumab, localized disease | NCT00667342 (St Jude) | 31 | 57.5% (registry) |

The four EURAMOS-1 arms are the best available controls for any new first-line trial.

## Findings from papers and basket trials

- **The 12% benchmark hides large differences between drugs.** Lagmay 2016, Table 2, gives per-trial 4-month rates: docetaxel 23%, oxaliplatin 31%, ixabepilone 9%, rebeccamycin analogue 6%, and 0% for topotecan, irinotecan and imatinib (paper, full text; the audit could not re-open this table).
- **Pazopanib + oral topotecan (PAZOTOP, NCT02357810).** 69.6% progression-free at 12 weeks in 28 osteosarcoma patients (paper, abstract only); median progression-free survival 4.5 months (registry). The regimen includes chemotherapy, and 12 weeks is earlier than 4 months. So it compares with the IE arms, not with 12%.
- **Cabozantinib in children and young adults (COG ADVL1622, NCT02867592).** About 35% had a response or disease control over the first six cycles. Only 14.7% were progression-free at one year (registry). This is the same short-lived pattern as CABONE.
- **Cixutumumab + temsirolimus.** 3 of 24 adults with osteosarcoma responded (paper, full text), against 0 of 10 children in a separate COG trial (registry). The trials differed in design and in IGF-1R selection, so this is not a like-for-like age comparison.
- **Checkpoint inhibitors showed minimal activity in small cohorts.** These cohorts are too small to rule activity out:
  - nivolumab: 0 of 10 responded;
  - nivolumab + ipilimumab: 0 of 10;
  - pembrolizumab + cyclophosphamide: 1 of 15 (registry);
  - pembrolizumab in SARC028: 1 of 22 (paper, abstract only);
  - pembrolizumab in a Norway/Italy trial: 0 of 12 had clinical benefit at 18 weeks (paper, abstract only).

  The one immunotherapy combination with clear activity so far pairs a VEGFR-blocking pill with a PD-1 antibody (APFAO, 66% at 4 months), and it missed its own 6-month target.
- **The ATR/PARP evidence in osteosarcoma is a single combination.** Olaparib + ceralasertib sits at the benchmark (15% at 4 months). No single-agent ATR or PARP inhibitor cohort in osteosarcoma has reported. This tempers the DNA-repair transfer ideas in the research report: if these drugs work, it may only be in a biomarker-selected group, which has not been tested.
- **No newer COG pooled benchmark.** We found no newer COG pooled benchmark for osteosarcoma. COG has published such benchmarks for rhabdomyosarcoma and for non-rhabdomyosarcoma soft-tissue sarcoma.

## What this connects to

- **Front-line testing of the pills has stalled in the US.** COG's front-line cabozantinib trial, AOST2032, is suspended (registry). Ipsen's maintenance trial CabOSTar closed after 10 patients (registry). We found no randomized kinase-inhibitor trial currently enrolling at a US site (registry; our calculation). In Europe, FOSTER-CabOS (part of NCT07871864) and a French regorafenib maintenance trial (NCT04055220) are recruiting (registry).
- **Resected relapse.** Any new claim in this setting should be compared with these arms and with the AOST0221 benchmark (20%, 95% CI 10–34%) before it is believed. That includes the OST-HER2 vaccine's reported results (press release only).
- **The kinase-inhibitor report** (`reports/Why kinase-inhibitor pills work in osteosarcoma.md`) uses these same figures.

## Limits

- **Selection.** The registry part includes only trials that posted results; many trials, including the large unknown-status trials in the trials report, never did. Papers and basket trials were added where we could find and read them. The dataset is therefore still a biased subset of all osteosarcoma trials.
- **Basket trials.** Basket-trial arms were included only where results were reported for osteosarcoma patients specifically. Many such arms have 10 or fewer osteosarcoma patients, and adult basket trials enrolled more heavily pretreated patients than COG trials.
- **Endpoints differ.** "Disease control", "event-free", "progression-free" and "non-progression" are close but not identical. Time points range from 12 weeks to 6 months. Kaplan–Meier estimates and simple counts are mixed. Treat cross-trial comparisons as rough.
- **Abstract-only sources.** 27 of the 60 published-paper rows are marked "abstract only", because some publisher sites were unreachable from this workspace.
- **Benchmark source.** The historical benchmarks (Lagmay 2016 and AOST0221) are now rows in the published-paper file.

## Next steps

1. Add the per-trial efficacy table from the FOSTER phase 2 review (van Ewijk et al., *Cancer Treat Rev* 2023, PMID 37738712; 58 trials, 1,361 osteosarcoma patients). It is the largest source still missing.
2. Re-read abstract-only rows in full text when publisher access allows, starting with REGOBONE, SARC024 and the sorafenib trials.
3. Ask COG for the ADVL1622 definition of "disease control", so it can enter the 4-month table.

## Change log

**November 13–14, 2026.** The report was consolidated into one current version after an independent audit (`research_notes/Audit/audit_B_trials_controls_pills.md`). Earlier "Update" sections were folded into the text.

- **Elimusertib removed: not osteosarcoma patients.** NCT05071209's 22 phase 2 patients had Ewing sarcoma, alveolar rhabdomyosarcoma or DNA-repair-altered solid tumours. It had been mis-tagged as osteosarcoma-only. The ATR/PARP statement now rests on one combination.
- **Osteosarcoma-specific registry trials: 41 → 34.** This follows the scope-tag fix described in the trials report. Seven trials, including elimusertib, a lung-cancer trial and paediatric multi-tumour baskets, no longer count.
- **"Only the kinase-inhibitor pills sit above the line" corrected.** IE chemotherapy alone also sits far above 12%, and imatinib, a kinase-inhibitor pill, does not. The class is now named "VEGFR-blocking kinase inhibitors".
- **CABONE framing unified.** Its 33% (registry) and 71% (paper) are a primary endpoint and a Kaplan–Meier estimate from the same trial, not a registry-paper conflict. Added the sensitivity result: 41.4% for the pill-alone class using CABONE's primary endpoint.
- **"Range 10–34%" corrected.** It is the 95% confidence interval of one 42-patient trial (AOST0221), not a range across trials.
- **Resected relapse.** "Results cluster tightly" softened to a hypothesis. Olaparib + ceralasertib cohort 2 (4 of 10 event-free at 12 months) and the saracatinib randomized result added.
- **OLIE and OAIE.** Overall survival added (OLIE HR 1.28 at the primary analysis, 0.93 at the final analysis; OAIE HR 1.48), along with OAIE's dosing difference (IE on days 1–5 in the control arm, days 1–3 with apatinib).
- **"Checkpoint inhibitors are confirmed inactive"** became "showed minimal activity in small cohorts".
- **"No newer COG pooled benchmark exists"** became "we found no newer…".
- **Patient counts.**
  - Published-paper additions: about 740 patients. The audit suspected double counting of Lagmay 2016; a recount found the 96 patients counted once.
  - Basket additions: about 400 osteosarcoma patients across separate arms (332 measurable, 68 resected).
- **Stale limits and next steps removed:** "only registry results included", "basket arms excluded", "benchmarks not from this dataset" and "add Lagmay 2016", which had already been done.
