# Auditor's guide

*For a third-party reviewer. Version 1.1, frozen on November 25, 2026 (git tag `v1.1`). Check against that tag, not the live `main` branch, so that your findings line up with what you are reading. Version 1.0 (tag `v1.0`, November 23) is the original review without the research engine.*

This project makes many claims across 25 reports and 2 briefs. This page lists the 18 from the original review that matter most, then how to check the research engine added in version 1.1. The 18 are the ones the ones the one-page summary, the website and the ranked leads depend on. For each one it gives where the claim is made, its primary source, and the fastest way to check it. If these hold, the project's main conclusions hold. If any fail, please tell us.

## Before you start

- **Get the frozen version:**
  ```bash
  git clone https://github.com/mgegen15-dev/For_John
  ```
  ```bash
  cd For_John && git checkout v1.1
  ```
- **Set up:** Python 3.10 or newer, plus `pip install -r requirements.txt` (pandas, numpy, scipy, matplotlib, h5py and the Markdown tools that build the website; versions pinned).
- **Check the data is unchanged:** run `python3 tools/build_manifest.py` and compare its output with the checksums in `DATA_MANIFEST.md` as committed at `v1.1`. Raw downloads are not in git, so they must be re-downloaded. Live databases change, so expect small differences from the retrieval dates listed there.
- **Read first:** `HOW_THIS_WAS_MADE.md` (methods, limits, how AI was used) and `SUMMARY.md` (the claims in plain language).
- **Earlier internal checks:** `research_notes/Audit/` holds the AI-run audits and their findings. They are a record, not a substitute for your review.

**Labels used in the reports:**
- **(registry):** an official database record.
- **(paper, full text):** read in the full published paper.
- **(paper, abstract only):** read only in the abstract.
- **(preprint, abstract only):** an unreviewed preprint.
- **(press release only):** no peer-reviewed source.
- **(our calculation):** computed by this project.

Claims labelled abstract-only, preprint or press-release-only are the weakest, and the most worth checking.

## The 18 key claims

### Trials and benchmarks

| # | Claim | Where | Primary source | How to check |
|---|---|---|---|---|
| 1 | Of 99 osteosarcoma trials that stopped early, 44 stopped mainly for poor recruitment and about 7–9 for lack of efficacy | Trials report, summary, website | ClinicalTrials.gov stop reasons (`data/osteosarcoma_trials.csv`) | `python3 tools/trial_analysis.py`. Stop reasons were grouped by keyword; spot-check the free-text reasons in `data/osteosarcoma_trials_flags.csv` |
| 2 | 27 randomized trials devoted to osteosarcoma alone on ClinicalTrials.gov | Trials report, summary | Same data, after the scope fix in `tools/retag_trial_scope.py` | Same script. Judge whether the osteosarcoma-only rule in `tools/trial_miner.py` (`scope_for`) is reasonable |
| 3 | Drugs other than VEGFR2-blocking pills or IE chemotherapy keep about 14% of measurable-relapse patients progression-free at four months (271 patients) | Pooled control report, website chart | Registry results and papers, one row per arm in `data/osteosarcoma_relapse_benchmarks*.csv` | `python3 tools/pool_relapse_benchmarks.py`. Check that each arm in the `sel` list is the right one, and that the source in each row's `source_note` says what the row says |
| 4 | VEGFR2-blocking pills alone: 52.5% at four months (41.4% using CABONE's primary endpoint); IE chemotherapy alone: 56.1% (42–66%) | Pooled control and kinase reports, chart | As claim 3 | As claim 3. CABONE's 12-month figure (9.5%) could not be verified by us (paywalled) |
| 5 | Resected lung-only relapse: about 20–22% event-free at 12 months | Pooled control, landscape and lung reports | AOST0221 (n = 42); COG pooled analysis (n = 99, medRxiv preprint, Chou et al., November 2026) | Search medRxiv for the COG preprint; check AOST0221 in Lagmay et al., *J Clin Oncol* 2016 (PMC5012712) |

### Kinase-inhibitor pills and the biomarker

| # | Claim | Where | Primary source | How to check |
|---|---|---|---|---|
| 6 | In both randomized pill + IE trials, survival was not improved: OLIE HR 1.28 at primary analysis and 0.93 at final; OAIE 18.1 months with apatinib + IE against 22.9 with IE alone (HR 1.48) | Kinase report, ranked leads | OLIE and OAIE papers (cited in the kinase report) | Read the papers' survival sections |
| 7 | In 81 TARGET-OS tumours at diagnosis, 23.5% carry an amplification of VEGFA, KDR, PDGFRA or KIT at twice the tumour's ploidy, and 46.9% at a looser 1.5× threshold | Copy-number report, summary, website | NCI GDC open TARGET-OS copy-number files | `python3 tools/copy_number_map.py`. Judge the ploidy-relative threshold; compare with published cohorts (about 40%) |
| 8 | About 309 patients across past pill trials; enough for 80% power to detect HR ≤ 0.5 between amplified and non-amplified patients, but not for a drug × biomarker interaction test | Copy-number report, ranked leads lead 2 | Trial enrolment from the registry and papers; Schoenfeld formula | `power` stage of `tools/copy_number_map.py`. Check the assumptions, especially 60% usable DNA (our guess) |

### Targets and leads

| # | Claim | Where | Primary source | How to check |
|---|---|---|---|---|
| 9 | Defactinib reduced lung metastasis in an orthotopic mouse model (2 of 6 treated against 6 of 6 untreated, P = 0.03) | Brief, ranked leads, literature map | PMID 37013056 (*Genes & Diseases* 2023) | Read the paper. Note the engineered (LOX-overexpressing) cells and the unusual printed dose |
| 10 | A DKK1-blocking morpholino reduced lung metastasis (2 of 10 treated against 7 of 9 untreated lungs) | Brief, ranked leads | PMID 39805917 | Read the paper. Note the two DKK1 laboratories share one patient-derived model |
| 11 | Colorado State lists a study giving defactinib to dogs with metastatic osteosarcoma | Brief, literature map | Web listing only (press release only) | We could not open the page or find results; please confirm with the investigators |
| 12 | Approved IL-1 and IL-6 blockers have no registered efficacy trial in osteosarcoma on ClinicalTrials.gov | Lung report, summary, lead 1 | ClinicalTrials.gov | Search the registry for anakinra, canakinumab, tocilizumab, sarilumab and siltuximab with "osteosarcoma". Tocilizumab appears only within a combination trial (NCT04616248) |
| 13 | A canine trial of inhaled IL-15 after amputation (NCI-COTC030) did worse than historical controls | Lung report, lead 1 | PMID 41209004 | Read the paper. Note it is a comparison with historical controls, and that IL-6 rose after treatment without being named as the cause |
| 14 | LRRC15 is present as protein in most patient osteosarcomas (e.g. 63 of 69 tumours stained) and has a recruiting trial in relapsed osteosarcoma | Surface-targets and what's-new reports, lead 5 | Cui 2020 (abstract only); O'Reilly 2026 (full text); NCT07357519 | Check the papers cited in the surface report and the registry record |
| 15 | The B7-H3 antibody-drug conjugate (ARTEMIS-011) beat gemcitabine–docetaxel: PFS 5.5 against 1.4 months, HR 0.33 (0.20–0.55) | Landscape and what's-new reports, summary | PMID 42933637 (*Ann Oncol* 2026; abstract only) | Read the abstract. Note it is open-label and run in China only |

### Literature and funding

| # | Claim | Where | Primary source | How to check |
|---|---|---|---|---|
| 16 | Since 2010, 8.7% of microRNA-type osteosarcoma papers have been retracted, against 1.0% of others (8.4-fold) | Risk flags report, summary | PubMed retraction status; paper types tagged by keyword | `python3 tools/paper_mill_flag.py` (needs the literature download). Sample papers in `data/osteosarcoma_paper_tags.csv` to judge the keyword tags; retraction count: search PubMed for `osteosarcoma[tiab] AND retracted publication[pt]` (418 as of retrieval) |
| 17 | NIH spent about $18.0 million on osteosarcoma-focused grants in FY2025 and $108 million over 2015–2025, against $212–227 million for neuroblastoma | Funding report, summary, website | NIH RePORTER | `python3 tools/nih_funding_tracker.py`. Judge the "focused" rule (disease named in the grant title) and the de-duplication of multi-project grants |
| 18 | MDM2 inhibitors are a weak lead for high-grade osteosarcoma: MDM2 amplification is common in low-grade tumours but rare in high-grade ones (2.5% of 81 in TARGET-OS) | Ranked leads (dropped leads), copy-number report | TARGET-OS copy number; literature close reading | As claim 7, plus the close reading in `research_notes/Osteosarcoma literature map/orphan_targets_close_read.md` |

## The research engine (added in version 1.1)

Seventeen cycles, each in `research_notes/Engine/cycle-NN-*/PREREGISTRATION.md` with a report in `reports/Engine cycle N - ....md`. The engine's central promise is that each plan was committed before its data were opened. That is checkable:

- **Order of events.** For each cycle, compare the commit time of its `PREREGISTRATION.md` (`git log --format="%h %cI" -- research_notes/Engine/cycle-NN-*/PREREGISTRATION.md`) with the first commit of its data and script (`git log --diff-filter=A --format="%h %cI" -- tools/engine_cycleNN*`). The plan should come first. Changes made after the plan are listed under "Deviations" in each file. Commit times are set by the committer's clock, so they show order within this repository, not proof against a determined forger.
- **Re-running.** Each report's last section gives the commands. Most need the raw downloads listed in `DATA_MANIFEST.md`, which are not in git.
- **Predictions.** P15 to P48 in `PREDICTIONS.md` were written before each cycle's data; outcomes are recorded there with the rule each was judged by.

| # | Claim | Where | How to check |
|---|---|---|---|
| E1 | RAMP1 did not replicate: pooled hazard ratio 0.99 (0.74–1.32) across three independent cohorts, against 2.30 in discovery | Cycle 1 report | `python3 tools/engine_cycle01_ramp1.py` after downloading the GEO files listed |
| E2 | CDKN2A deep deletion in 35 of 179 metastatic or relapsed patients (19.6%); odds ratio relapse against primary 1.10 (0.59–2.06) | Cycle 3 report, front page | `python3 tools/engine_cycle03_9p21.py fetch`, then without `fetch` |
| E3 | 25 recruiting or soon-to-recruit trials open on paper to an osteosarcoma patient with MTAP loss; 12 with a US site; 1 accepting under-18s | Cycle 4 report, brief, front page | `tools/engine_cycle04_mtap_trials.py`; check each row of `data/engine/cycle04/classification.csv` against its ClinicalTrials.gov record. A single reader classified these |
| E4 | 9 such trials for CCNE1 amplification; 6 with a US site; 1 (NCT04855656) from age 12 | Cycle 7 report, brief | As E3, with `tools/engine_cycle07_ccne1.py` and `data/engine/cycle07/classification.csv` |
| E5 | The dependency scans recovered the known pairs (9p21 loss with PRMT5 and WDR77; CCNE1 gain with CDK2; RB1 loss with SKP2, E2F3 and CDK2) and no unknown druggable pair | Cycle 8 and 9 reports | `python3 tools/engine_cycle08_scan.py` and `tools/engine_cycle09_suppressor_scan.py` after the DepMap downloads |
| E6 | In the PRISM drug screen, TP53-altered lines resisted all four MDM2 inhibitors and RB1-lost lines all three CDK4/6 inhibitors; CCNE1 amplification with adavosertib was inconclusive (−0.21 SD, −0.73 to +0.30) | Cycle 10 report | `python3 tools/engine_cycle10_prism.py fetch`, then without `fetch`; needs the DepMap downloads |
| E7 | No analysis showed LRRC15 RNA dropping in 29 lung metastases against 51 primaries; the pre-registered lung-tissue adjustment proved unstable | Cycle 11 report | `python3 tools/engine_cycle11_targets.py` after cycle 2's downloads; compare the adjusted and unadjusted rows |
| E8 | 43 of 57 recruiting relapse trials naming osteosarcoma accept 12- to 17-year-olds; 78 of 1,434 early-phase solid-tumour drug trials do | Cycle 12 report, brief | `python3 tools/engine_cycle12_teen_access.py fetch` gives the registry on the day it is run; check the hand classification in `data/engine/cycle12/hand_classification.csv` against each record. A single reader classified these |
| E9 | In 59 pet dogs, tumour DKK1 RNA did not go with faster relapse (hazard ratio 0.92, 0.67–1.26); the inflammation score was inconclusive (1.24, 0.93–1.66) | Cycle 13 report | `python3 tools/engine_cycle13_dog_inflammation.py fetch`, then without `fetch`. Judge the censoring rule, which the dataset forces |
| E10 | The tumour macrophage gene score reproduced in the Leiden cohort (0.63, 0.44–0.91) but pooled to 0.85 (0.67–1.08) in three independent cohorts | Cycle 14 report | `python3 tools/engine_cycle14_macrophages.py` after cycle 1's downloads |
| E11 | More tumour MYC RNA went with poor chemotherapy response: odds ratio 1.58 per SD (1.05–2.40) across three cohorts, 109 patients; not corrected for three tests | Cycle 15 report | `python3 tools/engine_cycle15_chemo_response.py` after cycle 1's downloads. Check the response coding in each cohort |
| E12 | Of early-phase solid-tumour drug trials, 10.9% started in 2014–2018 accepted teenagers, against 5.0% started in 2020–2024 | Cycle 17 report, brief | `python3 tools/engine_cycle17_fda_all_trials.py fetch`, then without `fetch`; a later run gives a later registry |

## Known weak points

These are the places we already know the work is weakest:
- **Abstracts, not full texts.** Many papers could be read only as abstracts, because some publishers block automated access.
- **Keyword tagging.** Paper types and trial scope were assigned by keyword rules. The internal audit found roughly 1 in 4 to 1 in 3 tags wrong in a small hand sample.
- **Gene mislabelling.** Automated text mining mislabels some genes. A correction table is in `tools/literature_map.py`, but more errors likely remain.
- **Narrow registry coverage.** ClinicalTrials.gov only; European-only and China-only registries were not searched systematically.
- **Unverified sources.** Several leads rest on press releases or web listings: the Colorado State dog studies, and the OST-HER2 vaccine results.
- **Trial classification by one reader.** The trial counts in engine cycles 4 and 7 rest on one reading of each registry record. One error was found and corrected on November 25, 2026 (see the cycle 4 change log).
- **Unplanned observations.** Some engine reports describe things that were not in the plan (MCL1 in cycle 7, the microsatellite check in cycle 9). They are labelled as such and should not be read as results.
- **Not independent people.** All internal checks were run by AI models, not by independent people. Your review is the first independent check.

## How to report findings

Please [open an issue on GitHub](https://github.com/mgegen15-dev/For_John/issues), quoting the claim number above, or the file and line, and what you found. Corrections will be logged in the affected report's change log, with credit if you want it.
