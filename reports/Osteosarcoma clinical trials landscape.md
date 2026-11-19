# Osteosarcoma clinical trials: what 40 years of registrations show

*Step 1 of the For John dot-connecting plan. Built from every study on ClinicalTrials.gov that lists osteosarcoma as a condition (758 studies, 603 of them interventional trials), a Europe PMC search of each finished trial's registry number, and a one-by-one follow-up search of nine trials whose results looked missing. Last revised November 14, 2026, after an independent audit; JCOG0905 note added November 19, 2026. Data: `data/osteosarcoma_trials.csv`, `data/osteosarcoma_trials_flags.csv`, `data/osteosarcoma_trials_publications.csv`. Scripts: `tools/trial_miner.py`, `tools/retag_trial_scope.py`, `tools/trial_analysis.py`, `tools/trial_publication_check.py`. Follow-up search log: `research_notes/Lost trial results/lost_trials_search.md`.*

## Summary

Osteosarcoma trials mostly fail to finish rather than fail to work. Of the 99 interventional trials that were terminated, withdrawn or suspended, 44 stopped mainly for poor recruitment and 20 for business or funding reasons, while only about 7 to 9 cited lack of efficacy; the 65 terminated trials had enrolled about 1,970 patients before they stopped. Randomized evidence is thin: we count 27 randomized trials devoted to osteosarcoma alone across about four decades, and the five largest have not updated their records in years. Trials with a site in China now make up about a fifth of new trials, yet none has posted results on ClinicalTrials.gov. Three trials that first looked unpublished turned out to be published, all with negative results. Four large randomized trials, together planning about 1,080 patients, still have no public results.

**How to read the labels.** After each key number we say where it comes from:

- **(registry)**: read from the ClinicalTrials.gov record.
- **(paper, full text)**: read in the full published paper.
- **(paper, abstract only)**: read only in the abstract.
- **(press release only)**: reported by a company or the media, not in a peer-reviewed paper.
- **(our calculation)**: counted or computed by this project from the files above.

## Why trials stop

Among the 99 interventional trials that were terminated (65), withdrawn before enrolling anyone (26) or suspended (8) (registry):

| Main reason in the registry, grouped automatically | Trials |
|---|---|
| Poor recruitment | 44 |
| Business or funding decision | 20 |
| No reason given | 9 |
| Other | 8 |
| Lack of efficacy | 7 |
| Drug supply ran out, or IND withdrawn | 7 |
| COVID-19 | 2 |
| Safety review | 2 |

(our calculation)

The grouping takes the first matching keyword in each free-text reason, so mixed reasons are counted once. Two trials grouped under recruitment also cite futility or a missed primary objective (NCT00752206, NCT01313884). One trial grouped under efficacy, the tumour-infiltrating-lymphocyte trial NCT06566092, was in fact closed on a company decision "after reviewing the available safety and efficacy data". Another, NCT03468075, says only "stopping rules met". So **about 7 to 9 trials stopped for lack of efficacy**, depending on how these mixed reasons are read (our calculation). Poor recruitment ended roughly five to six times as many trials. Each trial and its stated reason is in `data/osteosarcoma_trials_flags.csv`.

**Patients in stopped trials.** Terminated, suspended and withdrawn trials report enrolment differently, so we count them separately (our calculation, from registry enrolment fields):

| Status | Trials | Patients | What the number means |
|---|---|---|---|
| Terminated | 65 | about 1,970 | Actually enrolled: 1,813 in 63 trials that report an actual count, plus 154 planned in 2 trials that report only an estimate |
| Suspended | 8 | 1,521 | **Planned**, not enrolled. 1,122 of these are COG AOST2032 (cabozantinib, NCT05691478), suspended to "extend the observation period for current patients" |
| Withdrawn | 26 | 0 | Withdrawn trials enrolled nobody |

Some cases are telling. Ipsen's 2024 cabozantinib maintenance trial CabOSTar (NCT06341712) closed after 10 patients because of "ongoing recruitment challenges" (registry). Merck's robatumumab IGF-1R trial (NCT00617890) enrolled 219 people before stopping "for strategic reasons, not for a safety concern" (registry). It did post results, which are used in the pooled control dataset. Iovance's TIL trial in children (NCT06566092) closed after 5 patients (registry).

## How trial design changed over time

| Start years | Interventional trials | Osteosarcoma-only | Randomized, osteosarcoma-only | Bone sarcoma, osteosarcoma not named | With a US site | With a site in China |
|---|---|---|---|---|---|---|
| 2005–2009 | 85 | 14 | 7 | 0 | 59 | 2 |
| 2010–2014 | 93 | 16 | 3 | 1 | 66 | 1 |
| 2015–2019 | 120 | 17 | 4 | 3 | 81 | 16 |
| 2020–2024 | 165 | 31 | 9 | 2 | 82 | 32 |
| 2025–2029 (so far) | 62 | 12 | 3 | 4 | 33 | 13 |

(our calculation, from registry fields)

Across all start years there are 98 osteosarcoma-only interventional trials, 27 of them randomized (our calculation). The remaining interventional trials are 10 "bone sarcoma" trials that never name osteosarcoma and 495 basket trials, which include osteosarcoma among other cancers.

**A randomized trial outside this count: JCOG0905.** The Japan Clinical Oncology Group's randomized trial of MAP chemotherapy with or without ifosfamide for poor responders is registered only in the Japan Registry of Clinical Trials (jRCTs031180126, as given in the paper); searches of ClinicalTrials.gov for "JCOG0905" and for that jRCT number return nothing, and it is not in `data/osteosarcoma_trials.csv` (registry, November 19, 2026). So it is not among the 27. It randomized 103 poor responders (51 to MAP, 52 to MAP plus ifosfamide): disease-free survival did not differ (HR 1.05, 95% CI 0.55–1.98), overall survival was numerically worse with ifosfamide (HR 1.48, 95% CI 0.68–3.22), and 9 against 0 patients stopped treatment for adverse events (paper, abstract only; *J Clin Oncol* 2025, PMID 40138604). Like EURAMOS-1, it found that intensifying chemotherapy for poor responders does not help. Counting trials registered outside ClinicalTrials.gov would raise the randomized total to at least 28; we did not search jRCT, UMIN or other registries systematically.

**How the tags work.** A trial is "osteosarcoma-only" if every listed condition names osteosarcoma (or osteogenic sarcoma), or is a generic bone-sarcoma term or a bare site descriptor such as "Lung Metastases", and at least one condition names osteosarcoma. It is "bone sarcoma" if the conditions are generic bone-sarcoma or bone-tumour terms that never name osteosarcoma. Everything else is "basket". The earlier version of the tag also accepted any condition containing "recurrent", "refractory", "metastatic", "lung" or "neoplasm". That let Ewing sarcoma, rhabdomyosarcoma and even lung-cancer trials in. The corrected tag errs toward exclusion. Some true osteosarcoma trials are still counted as basket: OS2006 lists only "Sarcoma", and NCT03909776 lists endpoint names instead of a disease. So the osteosarcoma-only counts are more likely to be slight undercounts than overcounts, but they remain approximate.

**China.** Trials with a site in China rose from 1 in 2010–2014 to 32 in 2020–2024, about one in five new trials (registry; our calculation). None of the 64 interventional trials with a Chinese site has posted results on ClinicalTrials.gov (registry). By comparison, 131 of 384 trials with a US site have (registry).

**Main endpoints in osteosarcoma-only phase 2 and 3 trials** (79 trials; our calculation). A trial counts once for every endpoint type its primary outcomes name, so the numbers add up to more than 79:

| Primary endpoint names | Trials |
|---|---|
| Event-free, progression-free, disease-free or relapse-free survival | 40 |
| Response rate | 20 |
| Toxicity, safety or dose | 16 |
| Overall survival | 4 |
| None of these | 14 |

Overall survival is a primary endpoint in 4 trials: NCT00978471 (high-dose thiotepa), NCT05691478 (AOST2032), NCT07477457 and NCT04319874. It is the only primary endpoint in 2 of them (our calculation, keyword matching on registry text). Response rate is still the second most named endpoint, even though, as the research report notes, osteosarcoma's bony matrix rarely shrinks on scans.

## Trials whose results looked missing, and what a follow-up search found

The automated check had two kinds of lead:

- Large randomized osteosarcoma-only trials with status "unknown", where nobody has updated the record.
- Finished trials with neither posted results nor any Europe PMC paper that cites their registry number.

Nine of these were then searched one by one: PubMed, Europe PMC, conference abstract books, theses and web searches in English, Portuguese and Chinese. **Three had in fact been published.** None of the three cites its registry number where the automated check could see it. So every "no paper found" row below is a lead to check, not proof that results went unpublished.

**Large randomized trials with status "unknown".** All five numbers are planned enrolment; none of these trials has posted results (registry).

| Trial | Started | Planned patients | Question | Sponsor | What the follow-up found |
|---|---|---|---|---|---|
| NCT02273583 (GLATO 2006) | 2006 | 738 | Metronomic oral cyclophosphamide and methotrexate maintenance after standard therapy | GRAACC, Brazil (Latin American Group of Osteosarcoma Treatment) | **Published, negative.** 296 children and young adults up to age 30 were randomized (fewer than planned). 5-year event-free survival 61% with maintenance against 64% without, P = 0.40 (paper, abstract only). Senerchia et al., *Cancer* 2017, PMID 28263383 |
| NCT01669369 | 2013 | 400 | Lithium carbonate added to chemotherapy before surgery | Sun Yat-sen University, China | Nothing found in English-language sources. Chinese databases (CNKI, Wanfang) could not be searched |
| NCT04359550 | 2020 | 362 | PD-L1 antibody ZKAB001 (socazolimab) maintenance against placebo, phase 3 | Lee's Pharmaceutical | **Phase 3 not reported.** The earlier single-arm phase 1/2 (21 patients) reported 71% event-free at 24 months (paper, abstract only; Zhou et al., *Clin Cancer Res* 2023, PMID 36469563). Its registry record was last updated in April 2020 and lists no sites (registry) |
| NCT01002092 | 2009 | 160 | Endostar (recombinant endostatin) with chemotherapy | Shandong Simcere-Medgenn Bio-pharmaceutical (Endostar's maker), with military hospitals in Nanjing, Jinan, Xi'an and Beijing | Nothing found. Other Chinese Endostar studies in osteosarcoma exist, but none matches this trial's sites, dose or size |
| NCT03063983 (GLATO2017) | 2017 | 158 | Metronomic chemotherapy in metastatic disease | GRAACC, Brazil | Nothing found, including in four SIOP abstract books |

On socazolimab's status: a 2025 phase 3 paper in lung cancer states that China's regulator gave it conditional approval for cervical cancer in December 2023 (paper, full text). We did not find the regulator's own notice. We found no osteosarcoma filing.

**Finished trials with no posted results and no paper citing their registry number.** Among interventional trials that ended between 2010 and 2023, the automated check found 23, covering 949 patients (our calculation). The follow-up search found two of them published:

| Trial | Status | Patients | Question | What the follow-up found |
|---|---|---|---|---|
| NCT00978471 (OSII-TTP) | Completed 2018 | 44 | High-dose thiotepa with stem-cell rescue added to chemotherapy, randomized, in **relapsed** osteosarcoma | **Published, negative.** 2-year overall survival 66.7% against 50.0%; hazard ratio 0.83, P = 0.61 (paper, abstract only). Marec-Bérard et al., *Eur J Cancer* 2020, PMID 31838406 |
| NCT03909776 | Registered as completed 2019 | 99 | Intra-arterial cisplatin infused into the limb | **Published, negative.** A retrospective series registered after the fact: 48 intra-arterial patients against 51 historical intravenous controls, with no gain in local control (P = 0.34) or survival (P = 0.17) (paper, abstract only). Xie et al., *Cancer Manag Res* 2019, PMID 31447583 |
| NCT02022358 (GLU 1) | Terminated 2015 | 34 | Glucarpidase to reduce methotrexate side effects in bone sarcoma, randomized | **Partly found.** A 2013 University College London MD(Res) thesis reports an interim analysis. We could open only a truncated abstract, so its figures are unverified |
| NCT02718482 (OsteoREC2015) | Terminated 2019 | 7 | Gemcitabine + docetaxel against prolonged ifosfamide in relapsed osteosarcoma, randomized | Stopped at 7 patients for poor accrual; nothing to report |

That leaves 21 trials and about 810 patients with no results found (our calculation). Many are not anticancer treatment trials. They include supportive-care, imaging, exercise, analgesia and survivorship studies, and one cell-culture study registered as interventional. The full list is in `data/osteosarcoma_trials_publications.csv`. Older papers often omit registry numbers, so the list is limited to trials ending in 2010 or later, and it still has false positives.

**What remains genuinely unreported.** Four large randomized trials have no public results, together planning about 1,080 patients: the PD-L1 maintenance phase 3, the lithium trial, the Endostar trial and the Brazilian metastatic trial (our calculation). Each needs a direct question to its sponsor. For the Chinese trials, that means searching Chinese-language journals and registries too.

**Results reporting for recent US trials is good.** Of 45 US phase 2-and-later trials completed since 2018, 4 have no results posted (registry; our calculation).

## What this connects to

- **The pooled control dataset (gap 1 in the research report).** In total, 147 studies in the registry file have posted results. 92 of them are marked completed, and 117 report efficacy outcomes in a standard arm-level format. Extracting these is the cheapest first version of the historical-control dataset that the European FOSTER consortium says is missing. That extraction is now done: `reports/Osteosarcoma pooled control dataset.md`.
- **Low-cost maintenance strategies.** Metronomic maintenance after standard therapy was tested in 296 randomized children and young adults in Latin America and did not help (paper, abstract only). DFMO is being tested now. The 400-patient lithium trial remains unreported.
- **Recruitment is the bottleneck, not ideas.** Poor recruitment ended five to six times as many trials as lack of efficacy. So platform designs and pooled controls matter more than any single new drug. The new FOSTER platform (NCT07871864, Gustave Roussy, recruiting since October 2026, 530 planned across the whole platform) is one such design (registry).
- **The China shift.** About a fifth of new trials now run in China, and none of them has posted results on ClinicalTrials.gov. Following them requires Chinese-language conference abstracts, journals and the Chinese trial registry, which this project has not yet searched.

## Limits

- The scope tags, the stop-reason groups and the endpoint groups were assigned automatically from free text. They are approximate, though the scope tag was tightened on November 14, 2026 (see How the tags work).
- "No paper found" means no Europe PMC record cites the trial's registry number. It is not proof of non-publication: three of nine trials checked by hand had been published.
- ClinicalTrials.gov does not hold every trial. European-only trials registered elsewhere (EU CTR, ISRCTN) and Chinese trials registered only in China are missing.
- Enrolment for suspended and unknown-status trials is the planned number, not the actual one.
- The follow-up search could not reach several sources: Chinese databases, the EU trials register results pages, and a university thesis repository.

## Next steps

1. Contact the sponsors of the four unreported randomized trials (Lee's Pharmaceutical, Sun Yat-sen University, Simcere, GRAACC), and search CNKI, Wanfang and the Chinese trial registry for the three Chinese trials.
2. Read the GLU 1 thesis and the EU trials register results page for NCT02022358 when access allows.
3. Step 2 of the plan: extract claims from the osteosarcoma literature and link them to these trials and to the NIH grants.

## Change log

**November 19, 2026.** Checked whether JCOG0905 (randomized, Japan) is in the trial file: it is not, because it is registered only in jRCT (jRCTs031180126), so it is outside ClinicalTrials.gov and not among the 27 randomized osteosarcoma-only trials. Its published result (JCO 2025, PMID 40138604; paper, abstract only) was added below the count. The count itself is unchanged.

**November 13–14, 2026.** The report was consolidated into one current version after an independent audit (`research_notes/Audit/audit_B_trials_controls_pills.md`). Earlier "Update" sections were folded into the text.

- **Scope tag fixed.** The old osteosarcoma-only tag also accepted any condition containing "recurrent", "refractory", "metastatic", "lung", "pulmonary" or "neoplasm". It counted Ewing sarcoma, rhabdomyosarcoma, multi-tumour paediatric baskets and one lung-cancer trial as osteosarcoma-only. The tag was rewritten, and a third tag ("bone sarcoma") was added. Effects:
  - Osteosarcoma-only randomized trials: 32 → 27.
  - Osteosarcoma-only phase 2/3 trials used for endpoints: 103 → 79.
  - Period table columns re-counted.
  - "The randomized counts are a floor" removed; the tag was leaky in both directions.
- **Endpoint counting fixed.** Each trial used to count only for its first matching endpoint type, so overall survival was checked after event-free survival and almost never counted. "Just one trial uses overall survival as its main measure" became "overall survival is a primary endpoint in 4 trials, and the only one in 2".
- **Patients in stopped trials.** "About 3,500 patients" became about 1,970 enrolled in terminated trials, reported separately from 1,521 planned in suspended trials (1,122 of them in AOST2032); withdrawn trials enrolled 0.
- **Stop reasons.** "Only 7 stopped because the treatment did not work" became "about 7 to 9", with the misgrouped trials named. "Six times" became "five to six times".
- **Three trials first listed as unpublished were found published**, all negative: GLATO 2006, high-dose thiotepa and intra-arterial cisplatin. They were removed from the "missing" lists, and the remaining unreported trials were restated.
- "92 trials with posted results" became 147 with posted results (92 is the completed subset).
- Endostar trial sponsor corrected from "Chinese hospital" to Shandong Simcere-Medgenn. Lithium trial sponsor named (Sun Yat-sen University).
- "296 children" became "296 children and young adults up to age 30".
- The claim that every large unknown-status trial "enrolled or planned hundreds" was changed to "planned", since all five numbers are estimates and two are about 160.
- The thiotepa trial is now described as a trial in relapsed osteosarcoma. The intra-arterial cisplatin study is now described as a retrospective series.
- Robatumumab is no longer described as leaving its question unanswered, since it posted results.
- Socazolimab's approval for cervical cancer is now sourced, with the caveat that we did not find the regulator's own notice.
- "China trials often without posted results" became a number: 0 of 64.
