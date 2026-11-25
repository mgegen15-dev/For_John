# Engine cycle 4: which MTAP-selected drug trials could an osteosarcoma patient join?

*Run November 24, 2026. The fourth cycle of the For John research engine, and a descriptive one: a registry count with the search terms and counting rules fixed in advance. Pre-registration: `research_notes/Engine/cycle-04-mtap-trials/PREREGISTRATION.md`, committed at 20:11 UTC (commit `2676040`) before the search. Script: `tools/engine_cycle04_mtap_trials.py`. Table of every trial: `data/engine/cycle04/trials_classified.csv`.*

**Not medical advice.** This is what the ClinicalTrials.gov records said on November 24, 2026. Records can lag behind what a trial actually does, and a trial that takes "any solid tumour" can still turn away a rare one. Whether a trial suits a particular patient is a question for that patient's oncologist and the trial team.

## Summary

Cycle 3 estimated that about one in seven relapsed osteosarcomas has lost the gene MTAP. Drugs aimed at exactly that weakness are in trials, so we asked whether those trials would take an osteosarcoma patient. The registry lists 25 trials, recruiting now or about to, that such a patient could join on paper. One of them names bone sarcoma: a study of vopimetostat (TNG462) has a group for MTAP-deleted sarcoma, soft tissue or bone, with sites in the United States, France and Spain. The other 24 take any advanced solid tumour that has lost MTAP. Twelve of the 25 have a site in the United States. The gap is age. Twenty-four of the 25 start at age 18. Only one accepts patients from age 12, and its sites are all in China. Osteosarcoma is most often diagnosed in the teenage years (general knowledge), so the patients this disease takes youngest are the ones these trials leave out.

**How to read the labels.** Counts are **(our calculation)** from registry records (registry). Trial details are quoted from the records.

## What was counted

- **Search:** 23 terms on ClinicalTrials.gov (MTAP, PRMT5, MAT2A, and 20 drug names), fixed in advance. It returned 97 trials.
- **Counted:** 60 trials that were open in some form (recruiting, about to, by invitation, or running but closed to new patients) and that either require MTAP or 9p21 loss or test a PRMT5 or MAT2A inhibitor. One of the 60 was a false match, a dental study in which "MTAP" means an antibiotic paste.
- **Classified by reading each record's entry rules:** open to osteosarcoma "yes, named", "yes, by tumour-agnostic entry", "no" or "unclear". The classification of every trial, with a note on why, is in `data/engine/cycle04/classification.csv`.

## Results

| | Trials |
|---|---|
| A. Recruiting or about to, and open on paper to an osteosarcoma patient with MTAP loss | **25** (23 recruiting, 2 not yet) |
| … of which name sarcoma of bone | 1 |
| … of which take any solid tumour with MTAP loss | 24 |
| … of which require MTAP loss to be shown before entry | 24 |
| B. Of A, accept patients under 18 | **1** (from age 12; China only) |
| C. Of A, have a site in the United States | **12** |
| Open to any MTAP-lost solid tumour but closed to new patients | 3 |
| Unclear from the record | 1 |
| Limited to other tumour types, healthy volunteers, or people already in an earlier trial | 30 |

**The twelve with a United States site,** all for adults aged 18 and over:

| Registry number | Drug | Sponsor | Phase | Note |
|---|---|---|---|---|
| NCT05732831 | Vopimetostat (TNG462) | Tango Therapeutics | 1/2 | **Has a group for MTAP-deleted sarcoma, soft tissue or bone.** Sites also in France and Spain |
| NCT05245500 | Navlimetostat (BMS-986504, MRTX1719) | Bristol-Myers Squibb | 1 | Any solid tumour with MTAP deletion |
| NCT07492680 | Navlimetostat, alone or with other drugs | Bristol-Myers Squibb | 2 | Groups may be organised by tumour type; the record does not list them |
| NCT07382544 | Navlimetostat with olaparib | M.D. Anderson Cancer Center | 1 | Any solid tumour with MTAP loss |
| NCT06130553 | AZD3470 | AstraZeneca | 1/2 | One part takes any MTAP-deficient solid tumour |
| NCT06810544 | TNG456, alone or with abemaciclib | Tango Therapeutics | 1/2 | Any tumour with confirmed MTAP loss |
| NCT06914128 | BAY 3713372 | Bayer | 1/2 | MTAP-deleted solid tumours |
| NCT06589596 | BGB-58067 | BeOne Medicines | 1 | MTAP-deficient solid tumours |
| NCT06414460 | ISM3412 | InSilico Medicine | 1/2 | Solid tumours with MTAP deletion |
| NCT07128303 | GS-5319 | Gilead Sciences | 1 | MTAP-deficient solid tumours |
| NCT07601243 | GS-2426 | Gilead Sciences | 1 | MTAP-deficient solid tumours |
| NCT06630416 | Pemetrexed (an older chemotherapy, not a PRMT5 drug) | Northwestern University | 2 | Second group takes any solid tumour with MTAP loss |

The other 13 trials in group A have sites only outside the United States, mostly in China, with others in Japan, Australia, Taiwan, Hungary and Spain.

**Age.**

- The one trial in group A that takes patients under 18 is NCT06796699 (GH56, a company study in China), from age 12.
- Two trials outside group A show that younger patients are not excluded on principle: an investigator-led, single-centre navlimetostat trial for malignant peripheral nerve sheath tumour, another sarcoma, takes patients from age 12 in the United States (NCT07549022); and AstraZeneca's AZD3470 lymphoma trial takes patients from 12 (at least 40 kg) in one Hodgkin lymphoma part (NCT06137144).

**Someone is already measuring MTAP loss in osteosarcoma.** The search also turned up an observational study at a hospital in Beijing that is staining stored tumour samples from about 100 patients with advanced, relapsed osteosarcoma for MTAP protein (NCT07593573; listed as active, with no results posted as of its last update in May 2026). That is the measurement cycle 3 said was missing. Its result, when published, should replace this project's estimate of one in seven.

## What this means

- **For an adult with relapsed osteosarcoma whose tumour report shows MTAP or CDKN2A deletion, there are trials to ask about now,** including one that has made room for bone sarcoma by name. Most hospital gene-panel reports show CDKN2A; MTAP has to be looked for specifically, by a newer panel or a tissue stain.
- **For patients under 18 there is almost nothing,** and nothing in the United States or Europe that this search found. The nerve-sheath-tumour trial shows an adolescent trial of one of these drugs can be opened.
- **The practical ask,** for an advocacy group or a sarcoma network: ask the sponsors of the tumour-agnostic trials to lower the entry age to 12 for sarcoma, and ask the sarcoma group in the vopimetostat trial to report osteosarcoma separately. Both are small protocol decisions, and the frequency numbers from cycle 3 are the argument.
- **This is not evidence that these drugs work in osteosarcoma.** No osteosarcoma result has been reported for any of them that this project has found, and cycle 5 could not confirm the underlying dependency in osteosarcoma cell lines because too few lines have lost MTAP.
- **Prediction P19** (at least one such trial accepts under-18s) is resolved as right, on the single trial in China.

## Limits

- A registry snapshot on one day. Trials open and close; sites listed may not be enrolling.
- Entry rules are summarised in the registry. "Any solid tumour" may hide cohort limits, prior-treatment rules or site-level decisions that exclude bone sarcoma in practice.
- The search terms were fixed in advance and will have missed drugs registered only under a code name not on the list. More than a dozen such drugs turned up through the general terms and are included; they are listed in the pre-registration's deviations.
- One reader classified the records. The table is public so that anyone can check a row against its registry entry.

## Files and reproduction

- `python3 tools/engine_cycle04_mtap_trials.py fetch` repeats the search (the results will differ as the registry changes); `python3 tools/engine_cycle04_mtap_trials.py` rebuilds the tables from the saved search and `data/engine/cycle04/classification.csv`.
- Outputs: `data/engine/cycle04/trials.csv` (all 97), `data/engine/cycle04/trials_classified.csv` (the 60, with classification), `data/engine/cycle04/summary.json`. Sponsors that are individual doctors are listed as "investigator-sponsored".

## Change log

- 2026-11-24: search run, records read and classified, report written.
- 2026-11-25: corrected after an independent check. A UK mesothelioma trial (NCT07602946) had been described as taking patients from 16; its screening platform does, but its drug arm starts at 18, so it was removed as an example.
