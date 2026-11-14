# Osteosarcoma clinical gaps: registry and literature check

Date of check: 2026-11-13. Checks the "gaps" (1, 2, 3, 4, 5, 6, 11, 12) and the "untested transfers" table in `reports/Osteosarcoma research landscape and gaps.md`.

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

## Gap 11. Signals in existing trials never followed up (camrelizumab + apatinib; PD-L1 >=5%, lung-only disease)

**Verdict: PARTLY ADDRESSED (the PD-1 + anti-angiogenic pairing has been carried forward into new trials; the specific PD-L1 / lung-only subgroup signal has not been tested prospectively, as far as I could find).**

- The 2020 phase 2 (Xie et al., JITC; 43 patients, response rate 20.9%, missed the 6-month PFS target) remains the only published camrelizumab + apatinib osteosarcoma result found. No 2023-2026 update surfaced. https://pmc.ncbi.nlm.nih.gov/articles/PMC7223462
- MAPAC, NCT04351308 (China): randomized phase 2 in poor responders: MAPI + camrelizumab vs MAPI + apatinib vs MAPI alone. Separates the two drugs' contributions, which is what the report says was never done, but moves them to first line. Status "unknown", no results found. https://mayo.trials.co/clinical-trials-details/-/NCT04351308
- SARC038, NCT04803877: regorafenib + nivolumab in relapsed osteosarcoma, single arm, compared against historical regorafenib-alone controls (4-month PFS). Active, not recruiting; no results found. https://api.ai-analytics.org/clinical/NCT04803877
- PEMBROCABOSARC, NCT05182164 (France): pembrolizumab + cabozantinib, includes osteosarcoma; no osteosarcoma results found.
- IMMUNOSARC (sunitinib + nivolumab, bone sarcomas, Italian/Spanish): published 2024; osteosarcoma cohort details not read. https://iris.unito.it/retrieve/b9ed9024-8873-4a05-a6e6-ded9cf7b3bf2/2024%20-%20Nivolumab%20and%20sunitinib%20in%20bone%20sarcomas.pdf
- Not found: any trial that selects patients by PD-L1 >=5% or lung-only disease. Chinese registry not directly searched, so a ChiCTR study is possible.

## Gap 12. Lung-directed delivery is almost unexplored in people

**Verdict: PARTLY ADDRESSED IN THE PAST (several human inhaled trials were run 2003-2012); inhaled IL-15 is STILL OPEN in humans.** The report's wording "almost unexplored in people" overstates the gap.

- Inhaled GM-CSF (sargramostim): COG AOST0221, NCT00066365, completed; 43 patients with first lung recurrence of osteosarcoma. Published (Arndt et al., Pediatr Blood Cancer 2010, PMC2989183); no immune effect or benefit shown in lung. https://pmc.ncbi.nlm.nih.gov/articles/PMC2989183
- Inhaled lipid cisplatin: phase Ib/IIa in recurrent osteosarcoma with lung-only metastases (Transave, NCT00102531; published Chou et al., Pediatr Blood Cancer 2013), and a phase 2 (NCT01650090, Eleison Pharmaceuticals) of ILC to delay lung relapse after metastasectomy. Status of NCT01650090 not confirmed. https://webarchive.library.unt.edu/eot2008/20090813030239/http://clinicaltrials.gov/ct2/show/NCT00102531
- Aerosol IL-2 (aldesleukin): MD Anderson phase 1/2 in lung metastases including osteosarcoma (JITC 2013 abstract). https://jitc.bmj.com/content/1/Suppl_1/P251
- Aerosol gemcitabine: preclinical (mouse) work from MD Anderson; no osteosarcoma human result found.
- Inhaled IL-15: canine phase 1 only (UC Davis, 2022; 50 ug twice daily for 14 days; 1 complete and 1 partial response in 18 dogs). NIH grants (R. Canter, UC Davis) fund mouse work on inhaled IL-15 plus TIGIT blockade. No human trial or NCT number found. https://escholarship.org/uc/item/7d7091vm
- Regional CAR-T: none found for osteosarcoma. St. Jude 3CAR4OS (B7-H3 CAR-T after first-line chemotherapy) is intravenous. A canine trial at Penn gives B7-H3 CAR-iNKT cells to dogs with lung metastases. https://www.stjude.org/care-treatment/clinical-trials/3car4os-osteosarcoma.html ; https://www.vet.upenn.edu/clinical-trial/cell-therapy-for-metastatic-osteosarcoma/

Reading: the open question is why the 2000s inhaled programmes stopped and whether modern agents (IL-15, ADCs) would do better. That is a sharper gap than "unexplored".

## Untested transfers table

### T1. Pre-treatment biological risk classifier and shared data commons (from INRG)

**Verdict: PARTLY ADDRESSED.** Commons: Osteosarcoma Explorer (573 patients, JCO CCI 2023, PMID 37956387) and PCDC's HIBiSCus bone-tumour consortium exist. Neither is an INRG-style international pooled risk classification. Classifier: the May 2026 npj Precision Oncology "international framework" ranks pretreatment ctDNA as the most mature classifier, LEOPARD prospectively validated baseline ctDNA, and PRONOS (France) combines ctDNA with clinical factors. Not yet used for pre-treatment risk ASSIGNMENT in a trial. https://pediatricsnationwide.org/2026/07/30/international-framework-establishes-path-toward-risk-adapted-osteosarcoma-treatment/ ; https://childrensoncologygroup.org/publications/osteosarcoma-explorer-a-data-commons-with-clinical-genomic-protein-and-tissue-imaging-data-for-osteosarcoma-research/

### T2. External-control approval route for a cheap drug (DFMO model)

**Verdict: ALREADY UNDER WAY, for DFMO itself and for OST-HER2.**
- NCT07321912, "Eflornithine (DFMO) for Ewing Sarcoma and Osteosarcoma", Penn State Milton S. Hershey Medical Center (the Beat Childhood Cancer consortium that ran the neuroblastoma DFMO trial). Phase 2 basket, five cohorts, about 406 patients, start Apr 2026, recruitment reported open late May 2026. Cohort 3 is osteosarcoma relapsing in the lung after resection of lung metastases, DFMO twice daily for 730 days. Design (single-arm with external control) not confirmed. https://clinicaltrials.gov/study/NCT07321912 ; https://trial.medpath.com/clinical-trial/c4bc274b9b8de98f/nct07321912-eflornithine-dfmo-ewing-sarcoma-osteosarcoma
- NCT06892678, Montefiore Medical Center, phase 1/2 DFMO maintenance in relapsed/refractory Ewing or osteosarcoma with no evidence of disease after therapy; feasibility primary, EFS secondary; recruiting (NCI-2025-05478). https://clinicaltrials.gov/study/NCT06892678 ; https://www.cancer.gov/clinicaltrials/NCI-2025-05478
- OST-HER2 is testing the same regulatory route against a pooled historical control (FDA Type C statistical meeting Sept 2026; see gap 1).
These DFMO trials also bear on gaps 2 and 3: they are new drug trials in the resected-lung-relapse state, but not randomized as far as found.

### T3. Project-directed parent fund plus dedicated early-trial consortium (Band of Parents model)

**Verdict: ALREADY UNDER WAY.** Break Through Cancer's "Defying Osteosarcoma TeamLab" (launched Sept 2025): $15M from patient-driven foundations (including The Osteosarcoma Institute and MIB Agents), over 20 researchers at 8 institutions, early platform trials of ADCs and DNA-damage-response agents, with a canine trial arm (Tufts joined June 2026). Press-release sourced. https://breakthroughcancer.org/2025/09/largest-ever-investment-in-pediatric-osteosarcoma-research/ ; https://now.tufts.edu/2026/06/03/finding-better-answers-patients-deadly-bone-cancer

### T4. GD2 antibody with chemotherapy in GD2-selected patients; GD2 as ADC/radioligand/bispecific handle

**Verdict: STILL OPEN (web-search level).** Current GD2 osteosarcoma trials are still antibody without chemotherapy and without GD2 selection: naxitamab + GM-CSF, MSK, NCT02502786, active not recruiting, estimated completion Jul 2026, no results found; dinutuximab beta maintenance after relapse therapy, NCT05558280 (sponsor Prof. F. Fagioli, Turin; single arm, 22 patients; listed suspended or not yet recruiting). No GD2 ADC, radioligand, bispecific or GD2 CAR-T osteosarcoma trial surfaced. Note that the GD2 >95% expression figure makes "GD2 selection" less useful than "GD2 level" selection. https://ctv.veeva.com/study/humanized-monoclonal-antibody-3f8-hu3f8-with-granulocyte-macrophage-colony-stimulating-factor-gm ; https://clinicaltrials.gov/study/NCT05558280

### T5. Chromosome-end (telomere) maintenance type as a prognostic axis; ATR / ALT-directed trials

**Verdict: PARTLY ADDRESSED.** ALT is reported in up to 50-60% of osteosarcomas (M6620/VX-970 protocol NCT03718091, which enrolled ALT-type tumours including osteosarcoma). Dana-Farber NCT04417062, olaparib + ceralasertib (ATR) in recurrent osteosarcoma, phase 2, recruiting, not ALT-selected. Preclinical: short telomeres predict ATR-inhibitor sensitivity in 17 osteosarcoma lines (UCL). No study linking ALT status to osteosarcoma survival was found, so the PROGNOSTIC axis is still open. https://cdn.clinicaltrials.gov/large-docs/91/NCT03718091/Prot_SAP_000.pdf ; https://trials.co/clinical-trials-details/-/NCT04417062

### T6. Existing IL-1 / IL-6 blockers to prevent lung spread

**Verdict: STILL OPEN.** Only cell-line and mouse data (tocilizumab with anlotinib, Front Oncol 2023; tocilizumab + ladarixin ASCO 2022 abstract; anakinra in mouse tail-vein models). No human trial found. https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2023.1192472/full

### T7. RB1 status (not a BRCA-like score) to select patients for PARP-inhibitor trials

**Verdict: PARTLY ADDRESSED (trial in design, not registered).** A Bone Cancer Research Trust grant (Prof. S. Mittnacht, UCL, 2023) funds an RB1 test and "the design of a clinical trial utilising PARP inhibitors" in osteosarcoma. No registered RB1-selected trial found. The existing PARP trial (NCT04417062, olaparib + ceralasertib) is unselected. https://bcrt.org.uk/news/2023/4099/research-grant-awarded-aimed-at-developing-new-treatment-for-osteosarcoma

### T8. Biomarker-selected retest of IGF1R inhibitors

**Verdict: STILL OPEN.** Nothing after the 2017 Sanger genome study found. Not searched in the Chinese registry.

### T9. Pet-dog trials as a fast, fair test bed

**Verdict: ALREADY DONE AND CONTINUING (a well-used route, not a gap).** NCI's Comparative Oncology Trials Consortium has run osteosarcoma trials for years: COTC021/022 sirolimus (324 dogs, randomized, negative) and COTC030 inhaled IL-15 added to amputation + carboplatin (phase 2, 2025), STOPPED FOR FUTILITY, with DFS and OS worse than historical controls. Break Through Cancer's TeamLab includes canine trials (T3); Penn runs a B7-H3 CAR-iNKT trial in dogs with lung metastases. https://veterinaryoncology.biomedcentral.com/articles/10.1186/s44356-024-00004-1 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8172450

Addendum to gap 12: the COTC030 futility result weakens the report's case for inhaled IL-15 as a lung-directed lead. Verify the source before relying on it.

### T10. Automated necrosis scoring, validated prospectively

**Verdict: STILL OPEN.** The MSK model (Ho et al., Am J Pathol 2023; 103 cases, 3,134 slides) remains retrospective, single-centre. No prospective or multicentre validation found for 2024-2026. https://emergentmind.com/papers/2208.04910

## Summary of verdicts

All verdicts rest on web-search summaries; no registry was directly queryable. "Still open" means not found by web search only.

| Item | Verdict | Key evidence |
|---|---|---|
| Gap 1 pooled relapse control dataset | PARTLY ADDRESSED | FOSTER WP3 BJC 2025 review + framework in development; COG benchmark refresh; Osteosarcoma Explorer; OST-HER2 pooled control at FDA |
| Gap 2 randomized trial, resected lung mets | PARTLY ADDRESSED | AOST2031 NCT05235165 (randomized surgery, recruiting); OST-HER2 "confirmatory phase 3" announced, control arm unconfirmed |
| Gap 3 randomized drug after metastasectomy | STILL OPEN (weak) | Only single-arm (PROACH, AOST1421, OST-HER2, DFMO NCT07321912 cohort 3) |
| Gap 4 adapt therapy on ctDNA/PET | PARTLY ADDRESSED | LEOPARD NCT06068075 validates ctDNA; AOST2032 ctDNA correlatives; npj 2026 framework; no adaptive trial |
| Gap 5 front-line immune stimulation RCT | UNDER WAY | Sarcome-13/OS2016 NCT03643133 (UNICANCER, randomized mifamurtide, active not recruiting); ZKAB001 NCT04359550 phase 3 (status unknown) |
| Gap 6 replace 4-month EFS benchmark | PARTLY ADDRESSED | French randomized-PFS proposal (PMC8038261); COG 12-month resected-cohort endpoint; COG kept 4-month EFS |
| Gap 11 camrelizumab/apatinib follow-up | PARTLY ADDRESSED | MAPAC NCT04351308; SARC038 NCT04803877; PEMBROCABOSARC NCT05182164; no PD-L1/lung-only selection |
| Gap 12 lung-directed delivery | PARTLY ADDRESSED (past) | Inhaled GM-CSF AOST0221, inhaled lipid cisplatin, aerosol IL-2 trials; inhaled IL-15 no human trial and canine COTC030 futility |
| T1 risk classifier + commons | PARTLY ADDRESSED | ctDNA framework 2026; Osteosarcoma Explorer; HIBiSCus |
| T2 external-control route / DFMO | UNDER WAY | NCT07321912 (Penn State, 2026); NCT06892678 (Montefiore); OST-HER2 |
| T3 parent fund + consortium | UNDER WAY | Break Through Cancer Defying Osteosarcoma TeamLab, $15M (2025) |
| T4 GD2 + chemo / new GD2 formats | STILL OPEN | Only naxitamab+GM-CSF NCT02502786, dinutuximab beta NCT05558280 |
| T5 telomere type / ATR | PARTLY ADDRESSED | NCT04417062 olaparib+ceralasertib (unselected); no ALT-prognosis study |
| T6 IL-1/IL-6 blockers | STILL OPEN | Preclinical only |
| T7 RB1-selected PARP | PARTLY ADDRESSED | BCRT/UCL grant designing trial; none registered |
| T8 IGF1R biomarker retest | STILL OPEN | Nothing since 2017 |
| T9 dog trials | ALREADY DONE / ONGOING | COTC021/022, COTC030 (futility), TeamLab canine arm |
| T10 prospective necrosis AI | STILL OPEN | Only retrospective MSK model |

Programmes: AOST2032 NCT05691478 recruiting (feasibility closed Sept 2025). FOSTER-CabOS NCT07871864 enrolling, MAINTENANCE vs best supportive care (report mislabels it "at diagnosis"). ARTEMIS-011 NCT06935409 positive PFS (HR about 0.33), presented ESMO Oct 2026, China only, no peer-reviewed paper, OS immature; no global B7-H3 ADC phase 3 found. B7-H3 ADC + checkpoint: ARTEMIS-103 NCT06699576 (HS-20093 + adebrelimab, phase 1b sarcoma, Hansoh).

Skipped items: none.
