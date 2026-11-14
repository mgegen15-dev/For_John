# Osteosarcoma clinical trials: what 40 years of registrations show

*Step 1 of the For Johnny dot-connecting plan. Built on November 14, 2026 from every study on ClinicalTrials.gov that lists osteosarcoma as a condition (758 studies, 603 of them interventional trials), plus a Europe PMC search of each finished trial's ID. Data: `data/osteosarcoma_trials.csv`, `data/osteosarcoma_trials_flags.csv`, `data/osteosarcoma_trials_publications.csv`. Scripts: `tools/trial_miner.py`, `tools/trial_analysis.py`, `tools/trial_publication_check.py`.*

## Summary

The registry confirms the research report's central claim with hard numbers: **osteosarcoma trials mostly fail to finish, not to work.** Of the 99 interventional trials that were terminated, withdrawn or suspended, 44 stopped for poor recruitment and 20 for business or funding reasons; only 7 stopped because the treatment did not work. Those 99 trials had enrolled about **3,500 patients** between them.

Randomized evidence is scarce. A strict filter finds only **32 randomized trials devoted to osteosarcoma alone in about four decades**, and several of the largest have status "unknown", meaning nobody has updated the record. Among osteosarcoma-only phase 2 and 3 trials, just **one** uses overall survival as its main measure. And the field has moved geographically: trials with a site in China went from 1 in 2010–2014 to 32 in 2020–2024, about one in five new trials.

Results reporting looks better than feared for recent US trials, but older and non-US trials hide a trail of unreported work. The leads below are where a careful follow-up could recover data the field has lost.

## Why trials stop

| Reason given in the registry | Trials |
|---|---|
| Poor recruitment | 44 |
| Business or funding decision | 20 |
| No reason given | 9 |
| Other | 8 |
| Lack of efficacy | 7 |
| Drug supply ran out, or IND withdrawn | 7 |
| COVID-19 | 2 |
| Safety review | 2 |

Reasons were grouped automatically from free-text fields, so a few may be misclassified. Each trial and its stated reason is in `data/osteosarcoma_trials_flags.csv`.

Some cases are telling. The 2024 cabozantinib maintenance trial CabOSTar (NCT06341712) closed after 10 patients. A robatumumab IGF-1R trial (NCT00617890) enrolled 219 people before stopping "for strategic reasons, not for a safety concern". A tumour-infiltrating-lymphocyte trial in children (NCT06566092) closed after 5 patients on a company decision. In each case, patients took part and the question was left unanswered.

## How trial design changed over time

| Start years | Interventional trials | Osteosarcoma-only | Randomized, osteosarcoma-only | With a US site | With a site in China |
|---|---|---|---|---|---|
| 2005–2009 | 85 | 17 | 8 | 59 | 2 |
| 2010–2014 | 93 | 19 | 3 | 66 | 1 |
| 2015–2019 | 120 | 29 | 4 | 81 | 16 |
| 2020–2024 | 165 | 44 | 11 | 82 | 32 |
| 2025–2029 (so far) | 62 | 23 | 5 | 33 | 13 |

"Osteosarcoma-only" means every listed condition is osteosarcoma or a close synonym; the rest are basket trials that include osteosarcoma among other cancers. The filter is strict, so some osteosarcoma trials (for example OS2006) are counted as basket trials, and the randomized counts are a floor, not an exact figure.

**Main endpoints in osteosarcoma-only phase 2 and 3 trials:** event-free or progression-free survival 45; response rate 24; other 20; toxicity or safety 13; overall survival 1. Response rate remains the second most common endpoint, even though, as the research report notes, osteosarcoma's bony matrix rarely shrinks on scans.

## Leads: trials whose results may be missing

**Large randomized trials with status "unknown".** Each of these enrolled or planned hundreds of patients, and none has posted results to the registry. Some may have published without citing their registry number. Each one is worth a direct check with the sponsor or in conference abstracts.

| Trial | Started | Planned patients | Question | Sponsor |
|---|---|---|---|---|
| NCT02273583 | 2006 | 738 | Metronomic oral cyclophosphamide and methotrexate maintenance after standard therapy | Brazilian pediatric cancer group (GRAACC) |
| NCT01669369 | 2013 | 400 | Lithium added to chemotherapy before surgery | Chinese hospital |
| NCT04359550 | 2020 | 362 | PD-L1 antibody (ZKAB001) maintenance against placebo | Lee's Pharmaceutical |
| NCT01002092 | 2009 | 160 | Endostar (endostatin) with chemotherapy | Chinese hospital |
| NCT03063983 | 2017 | 158 | Metronomic chemotherapy in metastatic disease | Brazilian pediatric cancer group (GRAACC) |

The two Brazilian metronomic trials stand out: together they planned nearly 900 patients on a cheap oral regimen, exactly the kind of low-cost maintenance strategy the research report highlights as under-tested.

**Finished trials with no paper citing them and no posted results.** Among interventional trials that ended between 2010 and 2023, 23 have neither results on ClinicalTrials.gov nor any paper in Europe PMC that cites their registry number, covering about 950 patients. The most notable:

| Trial | Status | Patients | Question |
|---|---|---|---|
| NCT03909776 | Completed 2019 | 99 | Intra-arterial cisplatin infused into the limb for extremity osteosarcoma |
| NCT00978471 | Completed 2018 | 44 | High-dose thiotepa with stem-cell rescue added to chemotherapy (randomized) |
| NCT02022358 | Terminated 2015 | 34 | Glucarpidase to reduce methotrexate side effects |
| NCT02718482 | Terminated 2019 | 7 | Treatment of relapsed osteosarcoma (randomized) |

The full list is in `data/osteosarcoma_trials_publications.csv`. **This method has false positives:** papers, especially older ones, do not always cite the registry number. Two spot checks of pre-2010 trials found that one likely was published without citing it, which is why the list above is limited to trials ending in 2010 or later. Treat every row as a lead to check, not as proof the trial went unpublished.

**Results compliance for recent US trials is good.** Of 45 US phase 2-and-later trials completed since 2018, only 4 have no results posted.

## What this connects to

- **The pooled control dataset (gap 1 in the research report).** The 92 trials with posted results on ClinicalTrials.gov already hold arm-level outcomes in a standard format. Extracting them is the cheapest first version of the historical-control dataset the European consortium says is missing.
- **Low-cost maintenance strategies.** Metronomic chemotherapy (nearly 900 planned patients in Brazil), DFMO, and lithium were all tested or are being tested, but the larger results are not in the registry. Recovering them would show whether any cheap maintenance approach deserves a definitive trial.
- **Recruitment is the bottleneck, not ideas.** With poor recruitment ending six times as many trials as lack of efficacy, platform designs such as the new FOSTER platform (NCT07871864) and pooled controls matter more than any single new drug.
- **The China shift.** About a fifth of new trials now run in China, often without posted results. Following them requires Chinese-language conference abstracts and journals, which the research so far has not covered.

## Limits

- The osteosarcoma-only versus basket tags, the stop-reason groups and the endpoint groups were assigned automatically and are approximate.
- "No paper found" means no Europe PMC record cites the trial's registry number. It is not proof of non-publication.
- ClinicalTrials.gov does not hold every trial: European-only trials registered elsewhere (EU CTR, ISRCTN) and Chinese trials registered only in China are missing.
- Enrollment for unfinished trials is the planned number, not the actual one.

## Next steps

1. Extract arm-level outcomes from the 92 trials with posted results as a first pooled control dataset.
2. Check the five "unknown" randomized trials and the four highlighted unpublished trials one by one (conference abstracts, sponsor contact).
3. Step 2 of the plan: extract claims from the osteosarcoma literature and link them to these trials and to the NIH grants.
