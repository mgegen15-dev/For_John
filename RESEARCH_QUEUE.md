# Research Queue

*The For John research engine, in public. Each question is something public data or a partner laboratory can answer. Each is written down with its success and failure rules before the data are examined, then tested on patients it was not built from. Results are posted whatever they show. Last updated November 24, 2026.*

## How a question moves through the queue

| Status | Meaning |
|---|---|
| **Proposed** | A question worth testing, with the data that could answer it. Not yet pre-registered. |
| **Pre-registered** | Hypothesis, data, analysis and verdict rules are committed to git before the data are examined. |
| **Replicated** | Held up in independent patients by the rules set in advance. Promoted to a lead and handed towards a laboratory test. |
| **Refuted** | A meaningful effect ruled out by the rules set in advance. Closed. |
| **Inconclusive** | Neither, by the rules set in advance. Recorded with what it would take to decide. |
| **Needs a partner** | Cannot be answered from public data; needs samples, records or a laboratory. |

The checks get stronger in this order: a prediction written down before looking, a test in independent patient data, then a laboratory experiment. Only the last one is proof.

## Tested

| # | Question | Result | Date |
|---|---|---|---|
| 1 | Does tumour RAMP1 RNA predict relapse in patients outside the study it was found in? | **Inconclusive.** Pooled hazard ratio 0.99 (0.74–1.32) across three independent cohorts, 53 events, against 2.30 in the discovery cohort. The large effect is ruled out; a small one is not. [Full result](reports/Engine%20cycle%201%20-%20does%20RAMP1%20predict%20relapse.md) | Nov 24, 2026 |
| 2 | Do lung metastases carry more CXCR4 and less CXCL12 than primary tumours? | **Inconclusive, both.** Across six datasets (29 lung metastases, 51 primaries) CXCR4 leaned higher in lung metastases, +0.43 standard deviations (−0.05 to +0.91), but the lean disappeared once immune cells were accounted for (+0.06). CXCL12 was not lower (−0.08, −0.55 to +0.39). Lead 14 gains no support. [Full result](reports/Engine%20cycle%202%20-%20do%20lung%20metastases%20carry%20more%20CXCR4.md) | Nov 24, 2026 |
| 3 | Are deletions of the 9p21 region (CDKN2A and MTAP) more common at relapse than in primary tumours? | **Inconclusive.** In two hospital cohorts (130 relapse-stage patients, 211 with primary samples) the odds ratio was 1.10 (0.59–2.06). About one in five relapsed osteosarcomas carries the CDKN2A deletion (35 of 179), and in 30 patients tested twice it matched between primary and later sample in 28. MTAP itself was measured in only 24 patients. [Full result](reports/Engine%20cycle%203%20-%20is%209p21%20deletion%20more%20common%20at%20relapse.md) | Nov 24, 2026 |
| 9 | Which drug trials that select patients by MTAP loss accept osteosarcoma, and from what age? | **Answered (a count, not a test).** 25 trials recruiting or about to would take an osteosarcoma patient with MTAP loss on paper; one names bone sarcoma; 12 have a United States site; only one accepts under-18s, and it is in China. [Full result](reports/Engine%20cycle%204%20-%20MTAP-selected%20trials%20open%20to%20osteosarcoma.md) | Nov 24, 2026 |
| 10 | Do osteosarcoma cell lines without MTAP depend on PRMT5 more than those with it? | **Inconclusive, underpowered.** The link reproduced across all cancers, but only 3 of 27 osteosarcoma lines have lost MTAP. The one with knockdown data was the most PRMT5-dependent of five. [Full result](reports/Engine%20cycle%205%20-%20do%20osteosarcoma%20cells%20without%20MTAP%20depend%20on%20PRMT5.md) | Nov 24, 2026 |
| 4 | Do osteosarcoma cells with extra copies of CCNE1 depend on PKMYT1? | **Inconclusive.** Across 17 lines the trend ran the expected way (slope −0.06, −0.15 to +0.03) but could be chance. Four amplified lines identified for a direct drug test. [Full result](reports/Engine%20cycle%206%20-%20do%20osteosarcoma%20cells%20with%20more%20CCNE1%20depend%20on%20PKMYT1.md) | Nov 24, 2026 |
| 12 | How often is CCNE1 amplified in relapsed osteosarcoma, and would the trials take such a patient? | **Frequency: about one in ten** (17 of 179 on hospital tests); not clearly more common than in primaries (odds ratio 1.14, 0.52–2.48, inconclusive). **Trials: nine** would take such a patient on paper, six with a United States site, and one, of the PKMYT1 inhibitor lunresertib, from age 12. [Full result](reports/Engine%20cycle%207%20-%20CCNE1%20amplification%20at%20relapse%20and%20the%20trials%20open%20to%20it.md) | Nov 24, 2026 |
| 13 | Which other gene changes in osteosarcoma have a matching dependency across all cancer cell lines? | **Scan done (discovery, not a test).** 1.2 million comparisons, 14 replicated hits. Seven are established pairs, which shows the method works; no unknown druggable weakness turned up. Pointers: tumours whose 9p21 deletion reaches FOCAD depend on HBS1L (published 2025, drug in development; about 4% of osteosarcomas), and PTEN loss with FERMT2 needs an independent test. [Full result](reports/Engine%20cycle%208%20-%20a%20scan%20for%20drug%20weaknesses%20that%20go%20with%20osteosarcoma%27s%20gene%20changes.md) | Nov 24, 2026 |
| 16 | A second scan for the tumour-suppressor genes osteosarcoma loses most often (RB1, TP53, ATRX, PTEN, NF1) | **Scan done (discovery, not a test).** Both built-in checks passed; RB1 loss with SKP2, E2F3 and CDK2 recovered; no new druggable weakness. Without microsatellite-unstable lines, ATRX loss goes with FANCM, SMARCAL1 and ATR, as known. Osteosarcoma's own way of breaking TP53 and ATRX, large rearrangements, is invisible to these data. [Full result](reports/Engine%20cycle%209%20-%20weaknesses%20that%20go%20with%20the%20tumour-suppressor%20genes%20osteosarcoma%20loses.md) | Nov 24, 2026 |
| 21 | Do the gene-change weaknesses from the knockout screens hold up with real drugs? | **Checks passed; both tests inconclusive.** In a public drug screen of hundreds of cell lines, TP53-altered lines resisted all four MDM2 inhibitors and RB1-lost lines all three CDK4/6 inhibitors, so the method works. CCNE1-amplified lines were not clearly more sensitive to the WEE1 inhibitor adavosertib (−0.21 SD, −0.73 to +0.30, 16 lines), and MTAP-lost lines showed little or no response to an early PRMT5 drug not built for them (−0.05, −0.29 to +0.19). [Full result](reports/Engine%20cycle%2010%20-%20do%20the%20gene-change%20weaknesses%20hold%20up%20with%20real%20drugs.md) | Nov 25, 2026 |
| 22 | Do lung metastases keep the surface targets that new drugs aim at (LRRC15, B7-H3 and six others)? | **LRRC15 maintained by the rule, with a caveat; B7-H3 inconclusive.** No analysis showed LRRC15 dropping in 29 lung metastases against 51 primaries. B7-H3 was lower in whole-tissue samples but not clearly in tumour cells. The pre-registered adjustment for lung tissue proved unstable, so the next such test should measure tumour cells directly. [Full result](reports/Engine%20cycle%2011%20-%20do%20lung%20metastases%20keep%20the%20surface%20targets.md) | Nov 25, 2026 |
| 23 | Across the whole registry, how often can a teenager with osteosarcoma get into a drug trial? | **Answered (a count, not a test).** Of 57 recruiting drug trials naming osteosarcoma that take relapsed disease, 43 accept 12- to 17-year-olds (31 with a US site). Of 1,434 early-phase "solid tumour" drug trials, where new drugs first enter people, 78 (5%) do, and companies lead fewer of those. [Full result](reports/Engine%20cycle%2012%20-%20how%20often%20can%20a%20teenager%20with%20osteosarcoma%20get%20into%20a%20drug%20trial.md) | Nov 26, 2026 |
| 24 | In pet dogs with osteosarcoma, does tumour inflammation (IL6, IL1B, CXCL8), DKK1 or FAK RNA go with faster relapse? | **Inflammation inconclusive; DKK1 refuted; FAK inconclusive.** In 59 dogs treated with amputation and chemotherapy, the inflammation score leaned towards faster relapse (hazard ratio 1.24, 0.93–1.66); DKK1 did not (0.92, 0.67–1.26). IL1B alone leaned harder (1.34, 1.04–1.72), an unplanned single-gene result. The built-in check was weak. [Full result](reports/Engine%20cycle%2013%20-%20in%20pet%20dogs%20does%20tumour%20inflammation%20go%20with%20faster%20relapse.md) | Nov 26, 2026 |
| 26 | Does tumour macrophage signal go with a better outcome in patients outside the Leiden study that found it? | **Inconclusive.** The Leiden result reproduces in its own data (hazard ratio 0.63, 0.44–0.91) but pools to 0.85 (0.67–1.08) across three independent cohorts, 155 patients and 74 events. CD163 alone and TARGET-OS lean the expected way. [Full result](reports/Engine%20cycle%2014%20-%20does%20tumour%20macrophage%20signal%20predict%20a%20better%20outcome%20in%20new%20patients.md) | Nov 26, 2026 |
| 27 | Do tumours with MYC gain, CCNE1 gain or 9p21 loss respond worse to chemotherapy before surgery? | **MYC supported (modestly); CCNE1 refuted; 9p21 inconclusive.** In three cohorts (109 patients), more MYC RNA went with poor response: odds ratio 1.58 per SD (1.05–2.40), the same direction in all three. Not corrected for three tests; needs replication with MYC copy number. [Full result](reports/Engine%20cycle%2015%20-%20do%20tumours%20with%20MYC%20gain%20respond%20worse%20to%20chemotherapy.md) | Nov 26, 2026 |
| 29 | Since the FDA's 2019 adolescent guidance, are new early-phase solid-tumour trials more likely to take teenagers? | **No sign of it (refuted by the rule, weak design).** Of recruiting trials started in 2020 or later, 5.1% accept teenagers, and 2.4% of company-led ones; the 28 older trials still recruiting are more open, but that group is biased. A fair test of all trials registered in each period is next. [Full result](reports/Engine%20cycle%2016%20-%20since%20the%20FDA%20guidance%20are%20new%20trials%20more%20open%20to%20teenagers.md) | Nov 26, 2026 |
| 30 | Across trials of every status, did early-phase solid-tumour trials open to teenagers more often after the FDA's 2019 guidance? | **No; the share fell.** 10.9% of 905 trials started in 2014–2018 accepted teenagers, against 5.0% of 2,028 started in 2020–2024 (odds ratio 0.43, 0.32–0.58). The fall holds for company-led trials, for others, and for trials built for adults. [Full result](reports/Engine%20cycle%2017%20-%20before%20and%20after%20the%20FDA%20guidance%20across%20all%20trials.md) | Nov 26, 2026 |

## Next

| # | Question | Why it matters | How it can be tested | Status |
|---|---|---|---|---|
| 28 | Does MYC amplification (copy number, not RNA) go with poor response to chemotherapy before surgery in a larger cohort? | Cycle 15 found MYC RNA modestly linked to poor response in three small cohorts. Copy number is what a clinical test reports. | A cohort with both tumour copy number and histologic response, such as a sarcoma centre's sequencing records | Proposed; needs a cohort with both |
| 25 | Does tumour IL1B RNA go with faster relapse in a second group of pet dogs with osteosarcoma? | Cycle 13 saw this as an unplanned single-gene result in 59 dogs (hazard ratio 1.34, 1.04–1.72). It bears on the IL-1 half of lead 1. | A second public dog dataset with tumour RNA and outcomes, such as the 186-dog COTC022 RNA-seq set if its outcome data can be obtained | Proposed; needs outcome data. Checked Nov 26: the only other public dog set with outcomes (GSE14033) does not measure IL1B, and the COTC022 outcome tables sit on the publisher's site, which this session could not download |
| 20 | Rerun the tumour-suppressor scan with structural-variant calls, so that osteosarcoma lines that lost TP53 or ATRX by rearrangement are counted | Cycle 9 showed these routes are invisible to mutation and RNA calls, and they are how osteosarcoma usually breaks both genes. | Whole-genome structural-variant calls for DepMap cell lines, if a public source exists | Proposed; needs a data source |
| 17 | Is MCL1 amplification more common in relapsed osteosarcoma than in primary tumours? | Cycle 7 saw this as an unplanned observation (15 of 130 against 6 of 211), with some evidence against it. It needs a planned test on patients not used there. | A hospital cohort with primary and relapse samples that was not part of cycle 7 | Proposed; needs an independent cohort. Checked Nov 25: every public MSK osteosarcoma cohort on cBioPortal shares its patients with the one already used, and the others have too few relapse samples |
| 18 | Do cells without PTEN depend on FERMT2 in an independent screen? | The one replicated pair from cycle 8 with no paper behind it. | The Sanger Institute's independent CRISPR screens | Proposed; needs access to that dataset |

## Needs a partner

| # | Question | What is needed |
|---|---|---|
| 5 | Do extra copies of the kinase-pill target genes predict who benefits from those pills (lead 2)? | Stored tumour samples from past pill trials |
| 6 | Does the share of dead tumour in removed lung metastases predict outcome after surgery? | Archived lung-surgery slides from a bone-tumour centre |
| 7 | Did the inhaled IL-15 dog trial fail because it delayed chemotherapy? | Individual records from NCI's Comparative Oncology Program |
| 8 | Is CXCR4 protein on tumour cells, not immune cells, higher in lung metastases than in the same patient's primary tumour? (Follows cycle 2, where whole-tissue RNA could not separate the two.) | Stained sections of matched primary tumours and lung metastases, scored on tumour cells only, from a bone-tumour pathology archive |
| 11 | What share of relapsed osteosarcomas have lost MTAP protein? (Follows cycle 3, where the gene was measured in only 24 patients.) | MTAP staining of stored relapse or primary samples, or the newer gene panel run on them, at a sarcoma centre. A hospital in Beijing has registered such a study (NCT07593573); its result is awaited |
| 14 | Does an MTAP-selective PRMT5 inhibitor kill MTAP-lost osteosarcoma cells (143B or HOS, HSOS1) more than MTAP-intact ones? (Follows cycle 5, where gene screens had too few lines.) | A laboratory that grows osteosarcoma cell lines, and access to one of the trial drugs or a research-grade equivalent |
| 19 | Do osteosarcoma cells that have lost FOCAD (the line HSOS1) die when HBS1L or PELO is removed? (Follows cycle 8.) | A laboratory that grows osteosarcoma cell lines and can knock genes down |
| 15 | Does a PKMYT1 inhibitor kill CCNE1-amplified osteosarcoma cells (OS526, OS457, OS186, NOS1) more than low-CCNE1 ones? (Follows cycle 6.) | The same kind of laboratory; lunresertib or a research-grade PKMYT1 inhibitor |

## Rules the engine follows

1. A question enters testing only with a written prediction and the result that would count against it.
2. The data used to test an idea are never the data it came from.
3. Every result is published, including null and inconclusive ones.
4. Ideas that survive are handed to people who can run the experiment; the engine does not claim a treatment works.
5. Not medical advice.

## Change log

- 2026-11-24: queue started. Cycle 1 (RAMP1) tested and reported inconclusive.
- 2026-11-24: cycle 2 (CXCR4 and CXCL12 in lung metastases) tested and reported inconclusive. Question 8 added from its result. Questions 3 and 4 still wait on data access.
- 2026-11-24: cycle 3 (9p21 deletion at relapse) tested through cBioPortal and reported inconclusive. Questions 9, 10 and 11 added from its result.
- 2026-11-24: cycles 4 (MTAP trial count), 5 (MTAP and PRMT5 in cell lines) and 6 (CCNE1 and PKMYT1 in cell lines) run. Questions 12 to 15 added from their results.
- 2026-11-24: cycles 7 (CCNE1 at relapse and its trials) and 8 (systematic dependency scan) run. Questions 16 to 19 added from their results.
- 2026-11-24: cycle 9 (tumour-suppressor scan) run. Question 20 added from its result.
- 2026-11-25: cycle 10 (the knockout links tested with real drugs in the PRISM screen) run.
- 2026-11-25: question 17 checked for a public independent cohort; none found. Cycle 11 (surface targets in lung metastases) run.
- 2026-11-26: cycle 12 (registry-wide teen access) run.
- 2026-11-26: cycle 13 (pet-dog inflammation, DKK1 and FAK) run. Question 25 added from its result.
- 2026-11-26: question 25 checked for data; blocked. Cycle 14 (macrophage signal in independent cohorts) run.
- 2026-11-26: cycle 15 (gene changes and chemotherapy response) run. Question 28 added from its result.
- 2026-11-26: cycle 16 (trials before and after the FDA guidance, recruiting snapshot) run.
- 2026-11-26: cycle 17 (before and after the FDA guidance, all statuses) run.
