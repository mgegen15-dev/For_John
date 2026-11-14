# Lost osteosarcoma trial results: search log

*Built November 14, 2026, as follow-up to `reports/Osteosarcoma clinical trials landscape.md` (Next steps, item 2). For each trial whose results appear never to have been reported, this records what was searched, what was found, and the source actually opened. "Not found" is a finding, not a gap in the log. Nothing here is inferred from a source that was not opened.*

## 1. NCT02273583 (GLATO 2006): metronomic maintenance, non-metastatic osteosarcoma, Brazil/Latin America

**Found: full paper. Result: negative.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT02273583): org study ID "GLATO 2006"; sponsor GRAACC; responsible party Antônio Sérgio Petrilli; status unknown, last updated 2016-02-11; planned 738; primary endpoint EFS; no references, no posted results.
- **Paper:** Senerchia AA, Macedo CR, Ferman S, ... Petrilli AS. "Results of a randomized, prospective clinical trial evaluating metronomic chemotherapy in nonmetastatic patients with high-grade, operable osteosarcomas of the extremities: A report from the Latin American Group of Osteosarcoma Treatment." *Cancer* 2017;123(6):1003-1010. doi:10.1002/cncr.30411. PMID 28263383 (erratum Cancer 2018;124(7):1518). Opened: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=28263383&rettype=abstract&retmode=text
- **Why it was missed:** the abstract does not give the NCT number, and the registry record was never updated with the citation. Found via Europe PMC query `Petrilli AND osteosarcoma AND metronomic`.
- **Result (from the abstract):** 422 non-metastatic patients registered, May 2006 to July 2013, 27 sites in Brazil, Argentina and Uruguay. 296 randomized after surgery: MAP plus 73 weeks of oral cyclophosphamide + methotrexate (n=139) vs MAP alone (n=157). 5-year EFS from randomization 61% (MAP+MC) vs 64% (MAP alone); Wilcoxon (Gehan) statistic 0.724, **P = 0.395**. Not superior. Poor necrosis (grades 1-2), tumour size and amputation predicted shorter EFS. The abstract gives no hazard ratio and no overall survival figure.
- **Note:** enrolment fell well short of the 738 planned (296 randomized).
- **Other searches:** Europe PMC `NCT02273583` (1 hit, an unrelated review), `GLATO`, `"GLATO 2006"`, `osteossarcoma AND metronômica` (no trial report).
- **Confidence: high.** Same design, regimen, dates, sponsor institution and PI as the registry record.

## 2. NCT03063983 (GLATO2017): metronomic chemotherapy in metastatic osteosarcoma, Brazil

**Found: nothing. No paper, abstract or press release reporting results.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT03063983): acronym GLATO2017; sponsor GRAACC; responsible party Antônio Sérgio Petrilli; overall official Cláudia F. Fontes; started 2017-01-02; status unknown (last update 2017-03-13, last known "recruiting"); planned 158; estimated completion 2022-01-31; primary endpoint EFS with added metronomic therapy. No references, no results.
- **Searched, nothing relevant:**
  - Europe PMC: `NCT03063983` (2 hits, both reviews that only list the trial as ongoing: PMID 35409176, 33809018), `GLATO2017`, `"Latin American Group of Osteosarcoma"` (only GLATO 2006 and lab papers), `metastatic osteosarcoma AND metronomic AND (Latin American OR Brazil OR GRAACC)`, author search `AUTH:"Petrilli AS" AND osteosarcoma`, `Fontes CF AND osteosarcoma`, abstracts-only filter `osteosarcoma AND metronomic AND Brazil`.
  - SIOP abstract books for 2014, 2015, 2017 and 2018 (Pediatr Blood Cancer; full text downloaded from PMC7168141, PMC7167893, PMC7167988, PMC7167781). Europe PMC matched them, but scanning the full text for "metronom" near "osteosarc" found no GLATO abstract. The match came from words scattered across the whole book.
  - PubMed: `metronomic AND osteosarcoma AND metasta* AND (Brazil OR Argentina)[ad]` (0), `Petrilli AS[au] AND osteosarcoma, 2018-2026` (9 hits, all laboratory or genetics papers).
  - Crossref bibliographic query (no relevant hit). WebSearch in English and Portuguese ("osteossarcoma metastático quimioterapia metronômica GRAACC") turned up only registry mirrors.
  - OpenAlex could not be searched: the shared daily budget for this IP was used up.
- **Side note:** WebSearch surfaced a 2011 abstract titled "Preliminary safety and outcome report of the metronomic therapy from the Latin American..." on aminer.org. That host is blocked in this session, so I never opened it. Its search snippet suggests it covers the earlier GLATO 2006 programme, not GLATO2017. Unverified.
- **Confidence: moderate** that no results are public in indexed literature. Results could still sit in SIOP 2019-2025 abstract books (not scanned here) or in Brazilian theses. Next step: contact GRAACC (Petrilli or Fontes).

## 3. NCT01669369 (Li2CO3): lithium carbonate added to neoadjuvant chemotherapy, China

**Found: nothing. No results paper or abstract.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT01669369): acronym Li2CO3; study ID Lithium-5010; sponsor Sun Yat-sen University with five collaborating hospitals (Qilu, Nanfang, Shenzhen Second People's, Guangdong Provincial TCM, Shanghai 6th People's); PI and responsible party Jin Wang, First Affiliated Hospital of Sun Yat-sen University. Started 2013-01; status unknown (last update 2016-11-01); planned 400; estimated completion 2023-12. Co-primary endpoints: PFS and incidence of chemotherapy-induced myelosuppression. The only reference is a DERIVED review (PMID 31401903) that lists the trial as ongoing.
- **Probable rationale paper (not a trial result):** Tang QL, Xie XB, Wang J, ... Kang T. "Glycogen synthase kinase-3β, NF-κB signaling, and tumorigenesis of human osteosarcoma." *J Natl Cancer Inst* 2012. PMID 22534782 (abstract opened via PubMed efetch). Preclinical work plus immunohistochemistry on 74 patient tumours: hyperactive GSK-3β with nuclear NF-κB went with shorter median OS (49.2 vs 109.2 months). It is from the same Sun Yat-sen group and contains no trial data.
- **Searched, nothing relevant:**
  - Europe PMC: `NCT01669369` (6 hits, all reviews mentioning the trial), `TITLE:lithium AND TITLE:osteosarcoma` (1 hit, a Korean cell-line paper), `lithium carbonate AND osteosarcoma`, `lithium AND osteosarcoma AND "Sun Yat-sen" AND (myelosuppression OR ...)`, Chinese terms `碳酸锂 骨肉瘤` and `锂 骨肉瘤` (no relevant hits).
  - PubMed: `lithium[tiab] AND osteosarcoma[tiab] AND (patients OR trial)` (1 hit, 1985 in vitro).
  - WebSearch in English and Chinese ("碳酸锂 骨肉瘤 新辅助化疗 临床试验 中山大学"): only registry mirrors.
- **Not reachable:** a WebSearch hit pointed to Sun Yat-sen Cancer Center award-nomination documents for the project "骨肉瘤精准诊疗技术创新及推广应用" (2007-2019), which might mention the trial. The host www.sysucc.org.cn is blocked in this session (proxy 403 / DNS), so these were not read. CNKI, Wanfang and ChiCTR were not searched.
- **Confidence: moderate** that no result is in English-indexed literature; **low** for Chinese-language literature. Next steps: CNKI/Wanfang search for 碳酸锂 + 骨肉瘤 + 王晋 (probable Chinese name of Jin Wang, unverified); contact Jin Wang.

## 4. NCT04359550: ZKAB001 (socazolimab, anti-PD-L1) maintenance vs placebo, Lee's Pharmaceutical, China

**Found: no phase 3 result. The earlier phase I/II trial is published. The drug is approved in China for other cancers, not osteosarcoma.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT04359550): sponsor Lee's Pharmaceutical Limited; study ID NTL-LEES-2019-08; planned 362; primary endpoint one-year DFS rate; estimated start 2020-06-01 and completion 2023-06-01. The record was last updated 2020-04-29 and lists no sites and no officials. No references, no results. Nothing in the registry shows whether the trial ever enrolled.
- **Phase 3 result: not found.**
  - Europe PMC: `NCT04359550` (8 hits, all reviews listing it, e.g. Yu & Yao, *Mol Cancer* 2024, PMID 39245737, table shows "Unknown, Phase 3"), `ZKAB001`, `socazolimab`, `socazolimab AND osteosarcoma`, `(ZKAB001 OR socazolimab) AND osteosarcoma AND (placebo OR "phase 3")`.
  - WebSearch in English and Chinese ("索卡佐利单抗 骨肉瘤 III期 维持治疗") found no phase 3 osteosarcoma result.
- **Related published trial (not this one): phase I/II, single arm.** Zhou Y, Yang Q, ... Hu H, Yao Y. "First-in-Maintenance Therapy for Localized High-Grade Osteosarcoma: An Open-Label Phase I/II Trial of the Anti-PD-L1 Antibody ZKAB001." *Clin Cancer Res* 2023;29(4):764-774. doi:10.1158/1078-0432.CCR-22-2470. PMID 36469563. Opened the PubMed abstract.
  - Shanghai Sixth People's Hospital. 21 patients (9 dose escalation at 5/10/15 mg/kg every 2 weeks, 12 expansion at 10 mg/kg), enrolled October 2018 to 2019. MTD not reached; recommended dose 10 mg/kg.
  - Thyroiditis 76.2%, dermatitis 42.9%, one grade 3 rash (4.8%). 24-month EFS 71.4% (95% CI 47.2-86.0); 2-year OS 100%. 6 patients progressed. Preliminary signal in PD-L1-positive and MSI-H patients.
  - No control arm, so it cannot answer the phase 3 question.
- **Regulatory status in China** (sources opened: open-access full texts via Europe PMC):
  - Kaplon et al., "Antibodies to watch in 2022," *MAbs* 2022 (PMC8765076): socazolimab "was granted Breakthrough designation by the NMPA". The text does not say for which indication. An NDA for recurrent or metastatic **cervical cancer** was accepted by NMPA in November 2021 (citing a Sorrento press release of 2021-11-01). The review lists "maintenance therapy for high-grade osteosarcoma after adjuvant chemotherapy" among indications under evaluation.
  - Chen Z et al., phase 3 ES-SCLC trial, *Signal Transduct Target Ther* 2025 (PMID 39800716, PMC11725569): "NMPA granted conditional approval of Socazolimab launch in December 2023" for recurrent or metastatic cervical cancer.
  - WebSearch summaries say NMPA approved a second indication, first-line ES-SCLC with carboplatin and etoposide (reportedly around July 2025). The press sources (flcube.com, itiger.com, pharnexcloud.com) are blocked in this session and were **not opened**, so this is unverified.
  - **No evidence found of any osteosarcoma filing or approval.**
- **Not reachable:** larvol.com (has a socazolimab/osteosarcoma page), pharnexcloud.com (Chinese drug database), flcube.com. All are blocked in this session. Lee's Pharm annual reports (HKEX filings) would state whether the osteosarcoma phase 3 enrolled or stopped; not checked.
- **Confidence: moderate** that no phase 3 result is public. **High** for the phase I/II numbers and the December 2023 cervical cancer approval.

## 5. NCT01002092: Endostar (rh-endostatin) + chemotherapy, China

**Found: no report of this trial. Other Chinese groups published Endostar results in osteosarcoma, but none matches this trial.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT01002092): sponsor Shandong Simcere-Medgenn Bio-pharmaceutical (Endostar's maker), study ID SIM-65. Randomized, open-label phase 2; planned 160. PIs Sujia Wu and Xin Shi, Nanjing PLA General Hospital. Sites: Nanjing General Hospital of Nanjing Military Command, General Hospital of Jinan Military Command, Xijing Hospital (Xi'an), Military General Hospital of Beijing PLA (postcode 100700). Started 2009-02; status unknown (last update 2014-09-03). Non-metastatic, ages 12-60. Endostar 7.5 mg/m²/day on days 1-14 of weeks 1-2 and 5-6 of each cycle, added to MTX/cisplatin/doxorubicin/ifosfamide. Primary endpoint PFS at 5 years. No references, no results.
- **Papers found that are NOT this trial** (abstracts opened via PubMed efetch):
  - Xu M, Xu CX, Bi WZ, ... Wang Y. "Effects of endostar combined multidrug chemotherapy in osteosarcoma." *Bone* 2013;57(1):111-5. PMID 23912049. General Hospital of the Chinese PLA (301 Hospital), Beijing, postcode 100853. 116 newly diagnosed patients, 54 with Endostar and 62 without. Endostar at 15 mg/day for 2 weeks per cycle, a different schedule from the registry. The abstract does not say the trial was randomized and gives no NCT number. No difference in histologic response. EFS improved and metastases fell; OS unaffected. The abstract gives no numbers or p-values for EFS. **Probably not NCT01002092:** different hospital (the registry's Beijing site has a different postcode), dose and size. Low possibility that it reports one site's patients; unverified.
  - Xu H, Huang Z, Li Y, Zhang Q, Hao L, Niu X. "Perioperative rh-endostatin with chemotherapy improves the survival of conventional osteosarcoma patients: a prospective non-randomized controlled study." *Cancer Biol Med* 2019;16(1):166-172. PMID 31119057. Beijing Jishuitan Hospital, 2008-2012, 58 Endostar vs 272 controls, non-randomized. 5-year DMFS 79% vs 61% (P = 0.013); 5-year OS 87% vs 74% (P = 0.029). Different institution and design.
  - Sui W, Lin G. *J Oncol* 2023, PMID 36880008. Retrospective, Xiangyang, 2018-2019, 76 vs 65. Not this trial.
- **Other searches, nothing relevant:**
  - Europe PMC: `NCT01002092` (4 hits, all reviews), `endostar AND osteosarcoma`, `(endostar OR endostatin) AND osteosarcoma AND (Simcere OR "Nanjing General Hospital" OR "Jinling Hospital")`, Chinese `恩度 骨肉瘤` and `重组人血管内皮抑制素 骨肉瘤` (noise only).
  - PubMed: `(endostar OR endostatin) AND osteosarcoma` (25 hits, checked by title), with Nanjing/Jinan/Xijing/Simcere affiliation (0 relevant), `Wu S[au] AND Shi X[au] AND osteosarcoma` (lab papers only).
  - WebSearch in English and Chinese ("恩度 联合化疗 骨肉瘤 多中心 随机 南京军区南京总医院 吴苏稼"): registry mirrors only. CNKI and Wanfang were not reachable or searched.
- **Confidence: moderate** that no English-language report exists; **low** for Chinese-language journals. Next step: CNKI search for 恩度 + 骨肉瘤 + 南京总医院 (Jinling Hospital) or Simcere.

## 6. NCT03909776: intra-arterial cisplatin limb infusion, Peking University People's Hospital

**Found: full paper, and the registry links to it. Result: no survival benefit. This was a false positive in the landscape scan.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT03909776): sponsor Peking University People's Hospital; PI Wei Guo; study ID CBTRA-03/PKUPH-sarcoma 06; 99 patients (actual). Listed dates 2019-01-01 to 2019-04-08, which is consistent with a retrospective analysis registered after the fact. The registry's own reference list includes the paper below with type RESULT (PMID 31447583). The landscape check missed it because that check looked for Europe PMC records that cite the NCT number, and the paper's text does not cite it (Europe PMC query `NCT03909776` returns 0).
- **Paper:** Xie L, Xu J, Dong S, Gao J, Tang X, Yan T, Yang R, Guo W. "Gain and loss from transcatheter intra-arterial limb infusion of cisplatin for extremity osteosarcoma: a retrospective study of 99 cases in the past six years." *Cancer Manag Res* 2019;11:7183-7195. doi:10.2147/CMAR.S214604. PMID 31447583, PMC6684488. Opened the PubMed abstract.
- **Result:** Retrospective, not randomized. Patients treated December 2009 to August 2014: intra-arterial cisplatin (n=48) vs historical controls with intravenous cisplatin (n=51). No local-control benefit (P = 0.336) and no overall survival benefit (P = 0.173). Serial arteriography predicted good histologic response (accuracy 73.1%, sensitivity 100%). Skin and muscle necrosis were more common than earlier reports suggested, with catheter malposition a cause.
- **Confidence: high** (the registry itself links the paper).

## 7. NCT00978471 (OSII-TTP): adjuvant high-dose thiotepa with stem cell rescue in relapsed osteosarcoma, France

**Found: full paper. Result: negative. This was a false positive in the landscape scan.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT00978471): acronym OSII-TTP; EudraCT 2009-009899-12; sponsor Centre Léon Bérard; PI Perrine Marec-Bérard. Completed 2018-10-29 with 44 patients (actual). Primary endpoint OS. No results posted; the reference list holds only background citations.
- **Paper:** Marec-Bérard P, Dalban C, Gaspar N, ... Blay JY, Pérol D; OSII Thiotepa study group (SFCE and GSF-GETO). "A multicentric randomized phase II clinical trial evaluating high-dose thiotepa as adjuvant treatment to standard chemotherapy in patients with resectable relapsed osteosarcoma." *Eur J Cancer* 2020;125:58-68. doi:10.1016/j.ejca.2019.11.007. PMID 31838406. Opened the PubMed abstract.
- **Why it was missed:** the PubMed record carries no NCT number, and Europe PMC `NCT00978471` returns 0 hits. Found via `Marec-Berard AND osteosarcoma AND (thiotepa OR "high-dose")`.
- **Result:** 44 randomized, September 2009 to November 2016: standard chemotherapy + high-dose thiotepa + autologous transplant (Arm A, n=22) vs standard chemotherapy alone (Arm B, n=22). Median age 16.
  - 2-year OS 66.7% (95% CI 42.5-82.5) vs 50.0% (28.2-68.4).
  - Median OS 27.4 vs 24.8 months; **HR 0.826 (95% CI 0.393-1.734), p = 0.6123**.
  - Median PFS 15.6 vs 7.2 months, p = 0.3845.
  - Grade ≥3 adverse events 72.7% vs 81.8%; no toxic deaths.
  - Authors' conclusion: thiotepa cannot be recommended.
- **Confidence: high.** Same sponsor, PI, design, size and dates.

## 8. NCT02022358 (GLU 1): glucarpidase after high-dose methotrexate in bone sarcoma, UCL

**Found: a 2013 UCL MD(Res) thesis reporting an interim analysis of this trial. No journal paper. I could open only part of the thesis abstract; the interim numbers below are unverified.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT02022358): sponsor University College London, collaborator Richard Scowcroft Foundation; study ID 06/085; PI Jeremy Whelan (UCLH). Started 2007-07; terminated 2015-06; 34 patients (actual). Primary endpoint: difference in the proportion of patients ready for chemotherapy on day 15 of each cycle, standard folinic acid rescue vs glucarpidase plus folinic acid. No results, no references. The landscape report also pointed to an EU CTR entry, 2006-003203-40: WebSearch matched it to the same objective (2007 start, April 2015 end) and showed it has a results page, which I could not open (see below).
- **Thesis found** (Europe PMC record ETH 626417, opened via the Europe PMC REST API): Perisoglou M. "Efficacy and safety of glucarpidase for routine use after high dose methotrexate in patients with bone sarcoma." MD(Res) thesis, University College London, 2013. UCL Discovery eprint 1416302.
  - The part of the abstract returned by Europe PMC (truncated) describes GLU 1 as "a double blind randomised crossover clinical trial … to determine the efficacy and safety of routine use of glucarpidase after HD-MTX".
  - It also describes baseline work: a review of 56 UCH bone sarcoma patients treated with HD-MTX in 2004-2005, an age comparison (17 patients aged 40 or over vs 25 under 40, 2002-2007), and validation of an HPLC assay for MTX and DAMPA. The truncated text stops before the trial results.
- **Interim results: NOT verified.** A WebSearch summary of the thesis said 16 patients were analysed at interim. It said MTX toxicity delayed 43% of glucarpidase + folinic acid cycles vs 77% of folinic-acid-only cycles, that glucarpidase did not lower MTX AUC, and that the author called glucarpidase "a promising addition". I could not open the thesis PDF or the UCL record (discovery.ucl.ac.uk blocked, proxy 403). **Treat these numbers as unconfirmed until someone reads the thesis.** The abstract I opened gives no p-value.
- **Not reachable:** EU Clinical Trials Register results page for 2006-003203-40 (https://www.clinicaltrialsregister.eu/ctr-search/trial/2006-003203-40/results, proxy 403). A results summary may be posted there, covering all 34 patients.
- **Other searches, nothing relevant:** Europe PMC `NCT02022358` (0), `glucarpidase AND (osteosarcoma OR "bone sarcoma")` (case reports and reviews), `glucarpidase AND Whelan`. PubMed `glucarpidase AND (sarcoma OR osteosarcoma)` (10, none from this trial). Author search on Perisoglou in PubMed and Crossref: no glucarpidase journal paper.
- **Confidence:** high that the thesis exists and is about this trial (same design, same institution). Low for the interim numbers. Next steps: allow access to discovery.ucl.ac.uk and clinicaltrialsregister.eu, then read both.

## 9. NCT02718482 (OsteoREC2015): relapsed osteosarcoma, gemcitabine + docetaxel vs prolonged ifosfamide, Italian Sarcoma Group

**Found: nothing. The trial closed after 7 patients, and no outcome report was found.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT02718482): sponsor Italian Sarcoma Group; PI Stefano Ferrari (Istituto Ortopedico Rizzoli). Randomized phase 2: gemcitabine 900 mg/m² (days 1, 8) + docetaxel 75 mg/m² (day 8) every 3 weeks vs ifosfamide 14 g/m² continuous infusion over 14 days. Primary endpoint PFS. Ran 2016-04-06 to 2019-01-07 and was terminated with 7 patients. Why stopped: "Not adequate enrollment (sample size not possible to reach)". No results posted.
- **Searched:** Europe PMC `NCT02718482` (0), `OsteoREC2015 OR "OsteoREC 2015"` (0), `Ferrari S AND relapsed osteosarcoma AND (ifosfamide OR "Italian Sarcoma Group")`, 2019-2026 (19 hits).
- **Closest paper, not this trial:** Palmerini E, ... Ferrari S. "High Dose Ifosfamide in Relapsed and Unresectable High-Grade Osteosarcoma Patients: A Retrospective Series." *Cells* 2020;9(11):2389. PMID 33142760, PMC7692098 (abstract and full text opened). Retrospective series, 51 patients, ifosfamide 3 g/m²/day days 1-5, a different schedule. ORR 20%, median PFS 6 months, 2-year OS 30%. The full text does not mention OsteoREC2015 or the NCT number.
- **Confidence: high** that no trial report exists. With 7 patients, a formal report is unlikely to exist. The value here is the stop reason: a randomized relapsed-osteosarcoma trial in a major sarcoma centre could not recruit.

---

## Summary table

| Trial | Found? | Result | Source opened | Confidence |
|---|---|---|---|---|
| NCT02273583 GLATO 2006 (metronomic maintenance, non-metastatic, Brazil/LatAm) | **Yes, full paper** | 296 randomized (139 MAP+MC vs 157 MAP). 5-yr EFS 61% vs 64%, P = 0.395. No benefit | Senerchia et al., *Cancer* 2017, PMID 28263383 | High |
| NCT03063983 GLATO2017 (metronomic, metastatic, Brazil) | No | — | Registry only. Searched Europe PMC, PubMed, SIOP 2014/15/17/18 books, Crossref, web (EN/PT) | Moderate |
| NCT01669369 lithium + neoadjuvant chemo (Sun Yat-sen) | No | — | Registry; JNCI 2012 rationale paper only (PMID 22534782). Chinese sources partly unreachable | Moderate (EN) / low (CN) |
| NCT04359550 ZKAB001/socazolimab maintenance vs placebo (phase 3) | No phase 3 result | Phase I/II (n=21, single arm): 24-mo EFS 71.4%, 2-yr OS 100%. No osteosarcoma filing or approval found; NMPA conditional approval Dec 2023 for cervical cancer; NMPA Breakthrough designation (indication not stated) | Zhou et al., *Clin Cancer Res* 2023, PMID 36469563; PMC8765076; PMC11725569 | Moderate (phase 3 absent); high (phase I/II and approval facts) |
| NCT01002092 Endostar + chemo (Simcere, Nanjing) | No | — (other Endostar studies exist: *Bone* 2013 n=116 at 301 Hospital; Jishuitan 2019 non-randomized n=330; neither matches) | Registry; PMIDs 23912049, 31119057 checked and excluded | Moderate (EN) / low (CN) |
| NCT03909776 intra-arterial cisplatin (Peking Univ. People's) | **Yes, full paper** (the registry links it) | Retrospective: IA (48) vs IV (51) cisplatin. No local (P = 0.336) or OS (P = 0.173) benefit | Xie et al., *Cancer Manag Res* 2019, PMID 31447583 | High |
| NCT00978471 OSII-TTP high-dose thiotepa (France) | **Yes, full paper** | 44 randomized (22/22). 2-yr OS 66.7% vs 50.0%; HR 0.826 (0.393-1.734), p = 0.61; PFS p = 0.38. Not recommended | Marec-Bérard et al., *Eur J Cancer* 2020, PMID 31838406 | High |
| NCT02022358 GLU 1 glucarpidase (UCL) | **Partly: 2013 MD(Res) thesis** | Interim figures (16 patients, delays 43% vs 77%) seen only in a search summary, **unverified** | Europe PMC ETH 626417 (truncated abstract); thesis PDF and EU CTR results page blocked | High (thesis exists) / low (numbers) |
| NCT02718482 OsteoREC2015 (Italian Sarcoma Group) | No | Terminated at 7 patients for poor accrual | Registry; Europe PMC | High |

**Bottom line:** of nine "lost" trials, three have full journal reports. All three are negative, and none cites its NCT number in a way the landscape check could catch: GLATO 2006, OSII-TTP, and the intra-arterial cisplatin study. One (GLU 1) has a thesis that holds interim data. Five have no findable results: GLATO2017, lithium, ZKAB001 phase 3, Endostar and OsteoREC2015. The two cheap-maintenance leads split: Brazilian metronomic maintenance was tested in 296 randomized patients and failed, and lithium remains unreported.

**Hosts blocked in this session that would help:** discovery.ucl.ac.uk, clinicaltrialsregister.eu, sysucc.org.cn, larvol.com, pharnexcloud.com, flcube.com, aminer.org. OpenAlex hit its shared daily budget. CNKI, Wanfang and ChiCTR were not searched.
