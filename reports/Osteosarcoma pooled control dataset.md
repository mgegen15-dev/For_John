# A first pooled control dataset for osteosarcoma trials

*Built on November 14, 2026 from arm-level results posted on ClinicalTrials.gov, then extended with published papers. Script: `tools/pooled_controls.py`. Raw extract: `data/osteosarcoma_posted_outcomes.csv` (2,783 efficacy rows from 117 trials). Curated tables: `data/osteosarcoma_relapse_benchmarks.csv` (registry) and `data/osteosarcoma_relapse_benchmarks_published.csv` (60 rows from published papers covering 32 trials, 26 of them new, about 738 more patients; each row records its PubMed ID or DOI and whether the full text or only the abstract was read). Notes on conflicts: `research_notes/Pooled controls/published_results_notes.md`.*

## Summary

The research report found that osteosarcoma has no shared, standardized set of control outcomes against which to judge small single-arm trials. The European FOSTER consortium names this gap. This is a first, public version built from results that sponsors posted to ClinicalTrials.gov.

Of 147 osteosarcoma trials with posted results, 117 report efficacy outcomes and 41 report them for osteosarcoma patients specifically. Placed side by side, they show the relapse benchmark at work. Most new agents in measurable relapsed disease leave **0–15% of patients event-free at four months**, matching the historical benchmark of about 12%. In the resected-relapse setting, two very different drugs (dinutuximab and denosumab) left **26–28% event-free at 12 months**, close to the historical 20%. Only the kinase-inhibitor pills clearly sit above the line.

The dataset also recovers a result the earlier research could not find. The olaparib plus ceralasertib trial (NCT04417062) left **5 of 34 patients (15%)** event-free at four months, no better than the benchmark.

## Measurable relapsed disease

Patients with relapsed osteosarcoma that can be measured on scans and cannot be fully removed by surgery.

| Agent | Trial | Patients | Event-free or progression-free at about 4 months |
|---|---|---|---|
| Eribulin | NCT02097238 (COG AOST1322) | 19 | 0% |
| Denosumab | NCT02470091 (COG AOST1321) | 15 | 7% (1 patient) |
| Glembatumumab vedotin | NCT02487979 (COG AOST1521) | 22 | 14% (3 patients; first six cycles) |
| Olaparib + ceralasertib | NCT04417062 | 34 | 15% (5 patients) |
| Lenvatinib alone | NCT02432274 | 28 | 32% (95% CI 16–52%) |
| Lenvatinib + ifosfamide + etoposide | NCT02432274 | 15 | 67% (95% CI 38–88%) |
| Cabozantinib | NCT02243605 (CABONE) | 42 | 33% non-progression at **6 months** (95% CI 20–50%) |

**Historical benchmark** (Lagmay 2016, pooled COG trials): about 12% event-free at four months.

Randomized and median-based results in the same setting:

| Comparison | Trial | Median progression-free survival |
|---|---|---|
| Regorafenib against placebo | NCT02048371 (SARC024), osteosarcoma cohort | 3.6 months (n=22) against 1.7 months (n=20) |
| Lenvatinib + ifosfamide/etoposide against ifosfamide/etoposide | NCT04154189 (OLIE) | 6.5 months (n=40) against 5.5 months (n=41) |
| Avelumab, single arm | NCT03006848 | 8.0 weeks (n=18), no responses |

OLIE shows why randomized controls matter. The single-arm lenvatinib combination looked striking (67% at four months), but once ifosfamide and etoposide alone were given to a control group, the gap shrank to about one month.

## Resected relapse

Patients whose relapse has been completely removed by surgery, so there is nothing to measure.

| Agent | Trial | Patients | Event-free at 12 months |
|---|---|---|---|
| Dinutuximab + GM-CSF | NCT02484443 (COG AOST1421) | 39 | 28% (11 patients) |
| Denosumab | NCT02470091 (COG AOST1321), cohort 2 | 38 | 26% (10 patients) |

**Historical benchmark** (COG): about 20% (range 10–34%) event-free at 12 months.

Two drugs with completely different mechanisms, an anti-GD2 antibody and a bone-targeted RANKL antibody, gave almost identical results in this setting. Both sit inside the benchmark range. That suggests the 12-month figure mostly reflects who gets enrolled after surgery, not the drug, and strengthens the case for a randomized trial in this setting (gap 2 in the research report).

## Newly diagnosed disease

| Group | Trial | Patients | 3-year event-free survival |
|---|---|---|---|
| Good responders, MAP | NCT00134030 (EURAMOS-1) | 359 | 74% (69–79%) |
| Good responders, MAP + pegylated interferon | NCT00134030 | 357 | 77% (72–81%) |
| Poor responders, MAP | NCT00134030 | 310 | 55% (49–60%) |
| Poor responders, MAP + ifosfamide/etoposide | NCT00134030 | 308 | 53% (47–59%) |

These four arms are the best available controls for any new first-line trial.

## What this connects to

- **Kinase-inhibitor pills are the only class above the line**, and only before randomization. COG's front-line test of cabozantinib (AOST2032) is suspended, and the industry maintenance trial CabOSTar closed after 10 patients. The one class with a repeatable signal has no randomized trial currently enrolling in the US.
- **ATR and PARP inhibitors show no single-agent signal so far.** Olaparib plus ceralasertib (15%) and elimusertib (no responses in 22 patients across three groups, NCT05071209) both sit at the benchmark. This tempers the DNA-repair transfer ideas in the research report: if they work, it is likely only in a biomarker-selected group, which has not been tested.
- **Resected-relapse results cluster tightly.** Any new claim in this setting, including the OST-HER2 vaccine's press-reported results, should be compared with these arms and with the 10–34% range before it is believed.

## Update: published results added, and a correction

Adding published papers more than doubled the dataset and changed one conclusion.

**The 12% benchmark is the wrong yardstick for chemotherapy combinations.** In two randomized trials, patients given ifosfamide and etoposide (IE) alone, the usual relapse chemotherapy, did far better than 12%. In OLIE, 66% were progression-free at four months; in OAIE, 42%. So most of what looked like a striking effect of "pill + IE" in single-arm trials was the IE itself. In OLIE the difference was 76% against 66%.

**4-month event-free or progression-free rate in measurable relapse, pooled by drug class** (weighted by patients; mixes two estimation methods, so treat as approximate):

| Drug class | Trial arms | Patients | 4-month rate | Range across arms |
|---|---|---|---|---|
| Older chemotherapy and cytotoxics (single agents) | 3 | 133 | 12.5% | 0–28% |
| Antibodies, drug conjugates, DNA-repair drugs | 3 | 71 | 12.7% | 7–15% |
| Kinase-inhibitor pill alone | 4 | 145 | **52.5%** | 29–71% |
| Kinase-inhibitor pill + IE | 3 | 128 | 65.0% | 51–76% |
| Kinase-inhibitor pill + PD-1 antibody (camrelizumab + apatinib) | 1 | 43 | 66.3% | — |
| IE alone (randomized control arms) | 2 | 69 | 56.1% | 42–66% |

**What still holds:** kinase-inhibitor pills given alone sit far above the older single agents, confirming them as the one class with real activity. **What changes:** combinations must be judged against IE, not against 12%. Among the randomized evidence, the Chinese OAIE trial (apatinib + IE against IE) showed 65.8% against 41.6%. That is a larger gap than OLIE's and deserves attention.

**Other findings from the papers:**
- The 12% benchmark itself breaks down by drug: docetaxel 23%, oxaliplatin 31%, ixabepilone 9%, rebeccamycin 6%, and topotecan, irinotecan and imatinib 0% (Lagmay 2016, Table 2).
- Registry and paper figures disagree for several trials, because the registry often posts crude counts while papers report Kaplan–Meier estimates. For example, CABONE's registry figure is 33% non-progression at six months, against 52% at six months (and 71% at four) in the paper. Where both exist, the published file uses the paper's figure and the notes record the difference.
- No newer COG pooled benchmark for osteosarcoma exists. The resected-relapse figure of 20% (10–34%) still comes from the AOST0221 trial.
- Several papers could be read only as abstracts because some publisher sites were unreachable from this workspace, so 27 of 60 rows are marked "abstract only".

## Update: osteosarcoma results pulled out of basket trials

Many osteosarcoma patients are enrolled in "basket" trials that mix several cancers, which the first pass set aside. A second pass searched all 114 such trials with posted results, plus their papers, and added **16 basket trials and about 400 osteosarcoma patients** (`data/osteosarcoma_relapse_benchmarks_basket.csv`; notes: `research_notes/Pooled controls/basket_trials_notes.md`). One trial tagged as basket, a St. Jude trial of bevacizumab with MAP, turned out to be osteosarcoma-only; it is kept as a first-line row (3-year event-free survival 57.5%).

**The main picture holds.** Across all eight arms without a kinase-inhibitor pill or ifosfamide/etoposide, 271 patients, 14.2% were event-free or progression-free at about four months, close to the 12% benchmark. The pills alone remain around 50% (49.6% across 174 patients, once a second cabozantinib cohort, COG ADVL1622, is included).

**Signals found inside basket trials:**
- **Pazopanib + oral topotecan (PAZOTOP, NCT02357810):** 69.6% progression-free at 12 weeks in 28 osteosarcoma patients. It includes chemotherapy, so it compares with the ifosfamide/etoposide arms (42–66%), not with 12%. Abstract only.
- **Cabozantinib in children and young adults (COG ADVL1622, NCT02867592):** about 35% had a response or stable disease, but only 14.7% were progression-free at one year, the same short-lived pattern as CABONE.
- **Cixutumumab + temsirolimus:** 3 of 24 adults with osteosarcoma responded, against 0 of 10 children given the same drugs.
- **Checkpoint inhibitors are confirmed inactive** in osteosarcoma cohorts: nivolumab 0 of 10, nivolumab + ipilimumab 0 of 10, and pembrolizumab + cyclophosphamide 1 of 15.

Caveats: many basket arms have 10 or fewer osteosarcoma patients, adult basket trials enrolled more heavily pretreated patients than COG trials, and endpoint definitions differ.

## Limits

- **Only trials that posted results are included.** Many osteosarcoma trials, including the large unknown-status trials in the trials report, never posted results, so this is a biased subset.
- Outcome definitions differ: "disease control", "event-free", "progression-free" and "non-progression" are close but not identical, and time points range from four to six months. Treat cross-trial comparisons as rough.
- Basket-trial arms that mix cancers are flagged in the raw file and excluded from the tables above.
- The historical benchmarks come from the research report's sources, not from this dataset.

## Next steps

Add arm-level results from published papers for trials that never posted to the registry, starting with the COG relapse trials pooled in Lagmay 2016. That would turn this into a patient-count-weighted benchmark anyone can cite.
