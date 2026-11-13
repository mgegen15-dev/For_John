# Osteosarcoma clinical gaps: registry and literature check

Date of check: 2026-11-13. Checks the "gaps" (1, 2, 3, 4, 5, 6, 11, 12) and the "untested transfers" table in `reports/Osteosarcoma and neuroblastoma research gaps.md`.

Verdict key: STILL OPEN (nothing found where I could search) / PARTLY ADDRESSED / ALREADY DONE or UNDER WAY.

## Access limits (read this first)

This session could not open ANY registry or literature site directly. Direct requests (curl and WebFetch) were refused by the session's network policy for: clinicaltrials.gov (API and pages), eutils.ncbi.nlm.nih.gov, pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov, europepmc.org, euclinicaltrials.eu (CTIS), isrctn.com, chictr.org.cn, trialsearch.who.int (WHO ICTRP), cancer.gov, ctv.veeva.com, onclive.com, fiercebiotech.com, oncodaily.com, biopharma-asia.com.

Everything below therefore comes from web-search result summaries only. No page was opened and read in full. URLs given are the ones the search engine returned as sources, not pages I read. Consequences:

- "ALREADY DONE / UNDER WAY" verdicts are reasonably safe, because a trial that is found exists. Trial IDs, statuses and numbers still need a one-click check on the registry.
- "STILL OPEN" verdicts are weak. They mean "not surfaced by web search", NOT "absent from ClinicalTrials.gov / CTIS / ISRCTN / ChiCTR". No structured registry query was run for any gap.

## Status of the three named programmes

**COG AOST2032 (cabozantinib + MAP, newly diagnosed), NCT05691478.** Phase 2/3, NCI/COG. Listed as RECRUITING on site mirrors (Cancer Council Victoria listing "last updated 25 May 2026"; Canadian portal; several US hospital listings). The feasibility (dose-finding) part is reported closed to accrual as of 5 Sep 2025; the randomized efficacy part (MAP vs MAP + cabozantinib, with cabozantinib maintenance) is enrolling. No results found. Sources: https://trials.cancervic.org.au/details/vctl_nct05691478 ; https://clinical-trials-search.canada.ca/en/clinical-trial/276782-osteosarcoma ; https://clinicaltrials.gov/study/NCT05691478

**FOSTER-CabOS, NCT07871864 (EU CT number reported as 2023-505575-69-01, not confirmed on CTIS).** Sponsor Gustave Roussy (coordinator N. Gaspar). Registered as "Fight Osteosarcoma Through European Research Evolving Study Platform From Diagnosis to Relapse"; Part 2 is FOSTER-CabOS, an international randomized phase 3 of cabozantinib MAINTENANCE versus best supportive care after completion of standard first-line treatment. Listed as enrolling, about 530 patients, age 4+. CORRECTION TO THE REPORT: the report calls this "a randomized cabozantinib trial at diagnosis"; it is a post-first-line maintenance randomization, not cabozantinib added to chemotherapy. A Gustave Roussy page says "placebo", the registry says best supportive care; registry is more authoritative. A possibly separate record NCT06341712 ("Effects of Maintenance Cabozantinib+BSC Versus BSC in Children and AYA With Osteosarcoma", with a statistical analysis plan on file) also exists; relationship to NCT07871864 not verified. Sources: https://clinicaltrials.gov/study/NCT07871864 ; https://www.gustaveroussy.fr/en/foster-cabos-project-has-received-funding-clinical-trial-concerning-osteosarcoma ; https://cdn.clinicaltrials.gov/large-docs/12/NCT06341712/SAP_001.pdf

**B7-H3 ADC phase 3 (risvutatug rezetecan, "ris-rez", HS-20093 / GSK5764227).** ARTEMIS-011, NCT06935409, Hansoh, China only, randomized 2:1 versus gemcitabine + docetaxel in relapsed/refractory osteosarcoma after 2+ lines, 122 patients (80 vs 42). Topline announced July 2026; primary results PRESENTED at ESMO Congress, October 2026. PFS hazard ratio reported as 0.33 in most coverage and 0.36 (95% CI 0.21-0.59) in one; median PFS 5.5 months on the ADC; overall survival immature, no survival benefit shown yet. So this is now a conference-presented randomized result, no longer only a press release, but no peer-reviewed paper was found. Not approved anywhere for osteosarcoma; Hansoh plans a China filing; FDA breakthrough designation (Jan 2025). No GLOBAL phase 3 in osteosarcoma found: GSK's global work is phase 1b/2 (EMBOLD Sarcoma-202, NCT07602777, GSK study 300640, June 2026 to Nov 2029) and a phase 1 (NCT06551142). Ifinatamab deruxtecan (Daiichi/Merck): only a phase 1/2 with an osteosarcoma cohort reported, no phase 3. Sources: https://www.cancernetwork.com/view/risvutatug-rezetecan-improves-pfs-in-relapsed-refractory-osteosarcoma ; https://oncodaily.com/oncolibrary/artemis-011 ; https://www.targetedonc.com/view/risvutatug-rezetecan-improves-pfs-phase-3-osteosarcoma ; https://www.gsk-studyregister.com/trials/300640

## Gap 1. No pooled, standardized historical-control dataset for relapse trials

**Verdict: PARTLY ADDRESSED (pieces exist; no single pooled, patient-level, standardized relapse dataset found).**

What exists:
- FOSTER work package 3 has kept working on exactly this. A 2025 systematic review of prognostic factors in relapsed high-grade osteosarcoma (Rubio-San-Simon, Wilson et al., Br J Cancer 2025, doi 10.1038/s41416-025-03118-x; 19 studies, 3,245 patients) states its results "will be included in the development of a solid framework for development of new phase-II clinical trials". It is a literature-level pooling, not individual patient data. It is the same paper the report cites as the "FOSTER meta-analysis". https://discovery.ucl.ac.uk/id/eprint/10220907
- FOSTER also updated its trial-design review to 2017-2022 (71 phase 2 trials). https://discovery.ucl.ac.uk/10191813/1/1-s2.0-S2772610X23000272-main.pdf
- COG's own benchmark was refreshed: three later trials (AOST1321 unresected cohort, AOST1322, AOST1521) were compared against the Lagmay 96-patient benchmark and COG concluded 4-month EFS "remains a robust primary endpoint". https://ace.asco.org/content/344819/abstract/197938
- The French OS2006/Sarcome-09 relapse cohort was published as a de facto historical reference, with design recommendations. https://pmc.ncbi.nlm.nih.gov/articles/PMC8038261
- The Pediatric Cancer Data Commons lists a bone-tumour consortium, HIBiSCus, among its disease groups. Web search found no publication or osteosarcoma relapse dataset from it. https://commons.cri.uchicago.edu/pcdc
- Osteosarcoma Explorer (UT Southwestern/COG, JCO Clin Cancer Inform 2023, PMID 37956387): a data commons of 573 paediatric patients with clinical, genomic and imaging data. Mainly newly diagnosed trial patients; not a relapse-trial control set. https://pubmed.ncbi.nlm.nih.gov/37956387/
- A commercial sponsor has built its own: OS Therapies compares OST-HER2 against a "combined historical control" drawn from five prior trials (10 to 339 patients each), and an FDA Type C meeting in Sept 2026 was to decide whether pooled published historical controls are acceptable versus concurrent natural-history data from its OST-400 study. That is a live regulatory test of this exact question, in the resected-lung-relapse setting. https://www.cancernetwork.com/view/fda-type-c-meeting-granted-for-pulmonary-metastatic-osteosarcoma-therapy

Not found: any open, patient-level, harmonized relapsed-osteosarcoma control dataset. Could not check the PCDC data portal, HIBiSCus pages or FOSTER site directly. A direct question to FOSTER WP3 and the PCDC is the quickest way to settle this; they may have one in preparation.

## Gap 2. No randomized comparison in the resected-lung-metastasis setting

**Verdict: PARTLY ADDRESSED (a randomized SURGERY trial is running; a "confirmatory phase 3" of OST-HER2 is announced but its control arm is unconfirmed; no randomized DRUG trial confirmed).**

- COG AOST2031, NCT05235165, phase 3, NCI/COG, RECRUITING per hospital listings. Randomizes open thoracotomy versus thoracoscopic (VATS) resection in patients with resectable oligometastatic lung osteosarcoma (4 or fewer nodules per lung, each 3 cm or less); primary endpoint thoracic event-free survival. This IS a randomized comparison in this clinical state, but of the operation, not of a drug. It will also generate a prospective, uniformly followed control-like cohort for this setting. https://www.fredhutch.org/en/research/clinical-trials/trial-details.fh_trial_id_14485.thoracotomy-versus-thoracoscopic-management-of-pulmonary-metastases-in-patients-with-osteosarcoma.html ; https://es.renown.org/clinical-trials-directory/NCT05235165
- OST-HER2 (OS Therapies). Company press releases (2026) say FDA, MHRA, EMA and TGA have "aligned" on an adaptive confirmatory phase 3 in fully resected pulmonary metastatic osteosarcoma, to start late 2026 in the UK or Australia (sources disagree), with a BLA/accelerated-approval filing and an EMA conditional-approval rolling review also claimed. I could not confirm that the phase 3 has a randomized concurrent control, its size, or an NCT number. All of this is company-reported. The phase 2b (NCT04974008) is single-arm; the latest figures are 3-year survival 72.7% (final) versus 45.8% in a combined historical control. https://www.cancernetwork.com/view/ost-her2-shows-significant-final-3-year-os-benefit-in-osteosarcoma-trial ; https://www.biopharmawatch.com/news/OSTX/os-therapies-phase-3-trial-ost-her2-osteosarcoma
- Single-arm work continues in this state: PROACH (NCT03742193, China, apatinib + gemcitabine/docetaxel around metastasectomy then apatinib maintenance, 43 patients, ESMO Asia 2023, 18 of 39 progression-free at 12 months). Not randomized. https://oncologypro.esmo.org/meeting-resources/esmo-asia-congress-2023/pulmonary-resectable-metastases-of-osteosarcoma-with-apatinib-and-chemotherapy-proach-an-open-label-single-arm-phase-ii-clinical-trial
- Not found: any randomized drug-versus-control trial in second complete remission on COG, European or Chinese lists surfaced by web search. Registries not directly searched.

Action: check ClinicalTrials.gov for the OST-HER2 phase 3 record. If it has a concurrent control arm, this gap is closing.

## Gap 3. No randomized test of drug therapy after complete metastasis surgery

**Verdict: STILL OPEN on web-search evidence (weak negative), with the same OST-HER2 caveat as gap 2.**

- Web search found only retrospective series (COSS, Rizzoli, St. Jude, Shanghai Ruijin, Peking University NCT04546243 which is retrospective) and single-arm trials (AOST1421, AOST1321 resected cohort, OST-HER2 phase 2b, PROACH).
- Nearest randomized evidence is in a different state: FOSTER-CabOS (NCT07871864) randomizes maintenance cabozantinib versus best supportive care after FIRST-line treatment, including patients metastatic at diagnosis. It does not cover relapse after metastasectomy, but its metastatic stratum is the closest randomized data that will exist.
- A randomized placebo-controlled phase 3 of PD-L1 antibody maintenance after adjuvant chemotherapy exists in China (see gap 5), again first-line, not post-metastasectomy.
- Could not query ClinicalTrials.gov, CTIS, ISRCTN or ChiCTR directly, so a small national randomized trial could have been missed.

## Gap 4. Therapy has never been adapted on an early, dynamic marker (ctDNA, early PET)

**Verdict: PARTLY ADDRESSED (the marker is now prospectively validated and embedded in the main trial; no trial yet CHANGES treatment on it).**

- LEOPARD, NCT06068075, Dana-Farber, recruiting, observational (listed completion Jan 2027). ASCO abstract 11510 (year not confirmed, 2025 or 2026): 138 patients with localized osteosarcoma, 133 evaluable, 63% had detectable ctDNA at diagnosis, detectable ctDNA predicted worse event-free survival (2-year EFS 56% in the detectable group). Authors call baseline ctDNA "the first prospectively validated molecular biomarker" in osteosarcoma and position it for risk-stratified trials. This also updates the report's "about 57% detectable (Shulman 2018)" figure. https://coi.asco.org/Report/ViewAbstractCOI?id=439782 ; https://trials.braintumor.org/trials/NCT06068075
- AOST2032 (NCT05691478) carries ctDNA objectives, including whether ctDNA at or above 3% after the start of therapy and before surgery predicts events. That is the dynamic marker being measured inside the randomized trial, as a correlative, not as a treatment switch.
- France: OS2006 translational study built the PRONOS tool adding ctDNA to clinical factors; external validation in Sarcome-13 reported as under way. https://pesquisa.bvsalud.org/sms/resource/pt/mdl-38142939
- China: tumor-informed deep-sequencing ctDNA study (59 patients) detected relapse a mean 92.6 days before imaging; commentators say it does not yet justify changing treatment. https://www.onclive.com/view/tumor-informed-ctdna-sequencing-could-identify-osteosarcoma-relapse-months-before-radiographic-detection
- "An international framework for clinical translation of molecular classifiers in osteosarcoma" (npj Precision Oncology, 5 May 2026, doi 10.1038/s41698-026-01456-4, senior author R. Roberts) ranks pretreatment ctDNA as the most clinically mature classifier and sets risk-adapted trials as the goal. https://pediatricsnationwide.org/2026/07/30/international-framework-establishes-path-toward-risk-adapted-osteosarcoma-treatment/
- Seattle Children's SC-B615: prospective ctDNA prognostic study in newly diagnosed osteosarcoma/Ewing. Observational.
- Early PET: only observational studies found (e.g. 73-patient series showing PET after one cycle predicts outcome, EJNMMI Res 2020). No PET-adapted trial found.
- Not found: any registered interventional trial that escalates, de-escalates or switches osteosarcoma therapy on ctDNA or PET. Registries not directly searched.

Reading: the report's wording ("never been adapted") still appears true, but "overlooked" is no longer fair. The field has named this as the next step and done the validation work.

## Gap 5. Front-line immune stimulation never got a clean confirmatory trial

**Verdict: ALREADY UNDER WAY (one randomized mifamurtide trial fully enrolled and in follow-up; one randomized PD-L1 maintenance phase 3 of unknown status). The report's "no confirmatory randomized trial was ever run" needs correcting.**

- Sarcome-13/OS2016, NCT03643133, EudraCT 2017-001165-24, sponsor UNICANCER (France). Multicentre randomized open-label phase 2: postoperative chemotherapy with or without 36 weeks of mifamurtide in newly diagnosed HIGH-RISK osteosarcoma (metastatic at diagnosis or poor histological response), age up to 50. Design: 126 patients, 51 events, 80% power to detect 3-year EFS 52% vs 70%, with a planned Bayesian analysis borrowing historical data. Status ACTIVE, NOT RECRUITING (registry verified Dec 2025), started Oct 2018. No results found in ASCO/ESMO/CTOS coverage to date. One mirror shows enrollment 60, which conflicts with the 126 in the protocol; check the registry. It is a phase 2 sized for a large effect, so it may not settle the question, but it is a genuine randomized test. https://clinicaltrials.gov/study/NCT03643133 ; https://www.clinicaltrialsregister.eu/ctr-search/trial/2017-001165-24/FR ; protocol: BMJ Open 2019 (PMC6530327)
- ZKAB001 (socazolimab, anti-PD-L1), NCT04359550, Lee's Pharmaceutical, China. Randomized double-blind placebo-controlled phase 3 of one year of maintenance after adjuvant chemotherapy in high-grade osteosarcoma, 362 patients planned, primary endpoint 1-year disease-free survival. Registry status "Unknown" (anticipated completion 2022-2023); no results found. A checkpoint drug, so a different kind of immune therapy from mifamurtide/interferon, but it is a front-line randomized immunotherapy trial the report does not mention. https://decentrialz.com/clinical-trials/NCT04359550/study-of-zkab001-for-maintenance-therapy-in-patients-with-high-grade-osteosarcoma-after-adjuvant-chemotherapy
- MAPAC, NCT04351308 (China): randomized phase 2 in poor responders: chemotherapy + camrelizumab vs chemotherapy + apatinib vs chemotherapy alone. Status unknown, no results.
- Interferon: nothing after EURAMOS-1 found.
- St. Jude B7-H3 CAR-T consolidation after front-line chemotherapy is single-arm (already in the report).

## Gap 6. The four-month EFS benchmark may discard drugs that act on residual disease

**Verdict: PARTLY ADDRESSED (the criticism is published and alternatives are in use; no agreed replacement benchmark).**

- The French group made the same argument in print: the analysis of successive relapses after OS2006/Sarcome-09 recommends RANDOMIZED phase 2 trials, open to all ages, NOT limited to measurable disease (stratified by disease status), with PFS as primary endpoint and surgical complete remission as a secondary endpoint. https://pmc.ncbi.nlm.nih.gov/articles/PMC8038261
- COG already uses a separate benchmark for patients without measurable disease: 12-month event-free rate in the completely resected cohort (AOST1321 cohort 2, AOST1421; benchmark 20%). So the "residual disease" population is not judged on 4-month EFS in COG trials; the weakness there is the width of the 12-month benchmark (see gap 2).
- COG re-examined the 4-month benchmark with three newer trials and kept it ("remains a robust primary endpoint"). https://ace.asco.org/content/344819/abstract/197938
- Practice has moved toward randomization in relapse: SARC024 and REGOBONE (placebo-controlled regorafenib), OLIE (lenvatinib + chemo vs chemo), ARTEMIS-011 (ADC vs gemcitabine/docetaxel, PFS endpoint).
- FOSTER WP3 says a "framework for new phase 2 trials" is in development (see gap 1).
- Not found: a published FOSTER/COG consensus replacing the benchmark, or a validated ctDNA-based response endpoint.

