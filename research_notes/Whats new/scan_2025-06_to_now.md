# What's new in osteosarcoma, June 1, 2025 to November 19, 2026: scan notes

*Working notes, November 19, 2026. Purpose: catch papers, preprints, trial results and new trials
that matter for this project's leads or would change a report. Labels: (registry), (paper, full
text), (paper, abstract only), (press release only), (our calculation). A preprint is marked
"(preprint, abstract only)".*

## Search log

| Source | Query | Hits | Notes |
|---|---|---|---|
| PubMed E-utilities | `osteosarcoma[tiab]` with `("2025/06/01"[dp] : "2026/12/31"[dp])` | 2,665 | Too many to read; triaged by the topic queries below |
| PubMed | osteosarcoma + trial terms (clinical trial[pt], phase 1/2/3, randomized) | 38 | All titles read |
| PubMed | osteosarcoma + B7-H3 / CD276 / named B7-H3 ADCs | 17 | All titles read |
| PubMed | osteosarcoma + named kinase inhibitors | 38 | All titles read |
| PubMed | osteosarcoma + dog/canine + trial/study | 17 | All titles read |
| PubMed | osteosarcoma + genome/copy number/ecDNA/single-cell/spatial/germline/methylation/classifier (title-restricted, no reviews) | 121 | Titles read; bioinformatic "prognostic signature" papers skipped |
| PubMed | osteosarcoma + ctDNA / cell-free DNA / liquid biopsy | 38 | Titles read |
| PubMed | osteosarcoma + CAR-T / bispecific / ADC | 61 | Titles read |
| PubMed | osteosarcoma + IL-6 / IL-1 / CXCR1/2 / IL-8 | 27 | Titles read |
| PubMed | osteosarcoma + FAK / DKK1 | 9 | Titles read |
| PubMed | osteosarcoma + relapsed cohorts; + PD-1/PD-L1 | 112; 29 | First 60 / all titles read |
| Europe PMC | `TITLE:osteosarcoma AND SRC:PPR AND FIRST_PDATE:[2025-06-01 TO 2026-11-19]` | 114 | First 100 titles read; abstracts fetched for 7 |
| bioRxiv / medRxiv API | `api.biorxiv.org/details/{server}/{doi}` | — | Used to confirm the two key preprints (authors, date, version). The API has no keyword search, so discovery went through Europe PMC |
| ClinicalTrials.gov API v2 | `query.cond=osteosarcoma`, `StudyFirstPostDate` ≥ 2025-06-01 | 63 (49 interventional) | Each NCT checked against this repository |
| ClinicalTrials.gov API v2 | `query.cond=osteosarcoma`, `ResultsFirstPostDate` ≥ 2025-06-01 | 21 | Two osteosarcoma-specific ones read in full |

"In repo" below means the PMID or NCT already appears somewhere in this repository. Most PMIDs
appear only in the bulk literature tables in `data/` (`osteosarcoma_pubtator.jsonl`,
`osteosarcoma_paper_tags.csv`), which are automated; "discussed" means a report or note actually
uses the finding.

## Triage: the 25 items that matter most

Effect: **+** strengthens the named lead or report, **−** weakens it, **±** mixed, **0** context.

### A. Trial results in people

1. **ARTEMIS-011, B7-H3 ADC risvutatug rezetecan vs gemcitabine–docetaxel, phase 3, China.**
   Xie et al., Ann Oncol, online Oct 26, 2026 (PMID 42933637; paper, abstract only). Patients ≥12
   years with relapsed/refractory osteosarcoma after ≥2 prior lines, randomised 2:1, 80 vs 42.
   Median PFS by blinded central review **5.5 vs 1.4 months, HR 0.33**; median follow-up 7.1
   months; "numerical trend" in overall survival. Grade ≥3 treatment-related events 93% vs 83%,
   serious ones 64% vs 29% (mostly haematological); dose reductions 71% vs 26%. **The abstract
   prints the 95% CI as "0.21-1.23"**, which cannot be right for a "statistically significant"
   HR of 0.33; `data/osteosarcoma_relapse_benchmarks_published.csv` records 0.20–0.55. One of the
   two is a transcription error; check the full paper. *In repo: data tables; the landscape report
   still says "there is no journal paper yet (press release only)".* Effect: **+** for
   antigen-directed drugs (lead 5) and for randomising in relapse (lead 6); updates the landscape,
   pooled-control and trials reports.
2. **PEPN1924, trastuzumab deruxtecan in HER2-positive relapsed osteosarcoma (COG).** Reed et al.,
   JCO Oncol Adv 2025 (PMID 42131734, PMC13166107; paper, abstract read). 41 of 50 screened met a
   lenient HER2 IHC criterion; 9 treated; 1 with stable disease past 24 weeks (11.1%); did not go
   to stage 2. *In repo: data tables; the landscape report cites PMID 40911899 for this result, but
   that is the preclinical PDX paper (Mol Cancer Ther 2026), which only mentions the trial in
   passing.* Effect: **+** for the surface report's view that HER2 is a poor target; citation should
   be swapped.
3. **COG benchmark update for resected lung-only relapse.** Chou et al., medRxiv, Nov 16, 2026
   (doi 10.64898/2026.11.13.26368045; preprint, abstract only; confirmed via medRxiv API). 99
   patients from three COG single-arm phase 2 trials: median EFS 4.8 months, **12-month EFS 22%
   (95% CI 15–31%)**, ranging 14–29% across trials; relapse within two years of diagnosis worse
   (p = 0.009). Authors: "single arm trials of new approaches will only be able to identify large
   effect sizes. Smaller effect sizes will require randomization." *Not in repo.* Effect: **+** for
   lead 6 and for the landscape report's design argument; the AOST0221 benchmark quoted there
   (20%, 10–34%, n = 42) can now be replaced by 22% (15–31%, n = 99).
4. **JCOG0905, MAP vs MAP + ifosfamide in poor responders, randomised.** JCO 2025 (PMID 40138604,
   PMC12118622; paper, abstract only). 103 randomised; DFS HR 1.05 (0.55–1.98); OS numerically
   worse with ifosfamide (HR 1.48); 9 vs 0 stopped for toxicity. *In repo: data tables only.*
   Effect: **0/+** confirms EURAMOS-1 that intensifying for poor responders does not help; one more
   osteosarcoma randomised trial for the trials-landscape count.
5. **CabOSTar (Ipsen, NCT06341712), cabozantinib maintenance vs supportive care.** Results posted
   Oct 29, 2026 (registry): 10 patients (5 vs 3 in the safety groups), and "planned analyses …
   were not performed as the study was terminated early". *In repo: termination already noted.*
   Effect: **0**; no efficacy data will ever come from it, so it adds nothing to lead 2.
6. **Real-world TKIs in bone sarcoma, TOGBONE (Turkey).** JCO Glob Oncol 2026 (PMID 42715501; paper,
   abstract only). 72 patients, mostly regorafenib or pazopanib in second line or later; median
   PFS 4.4 months in osteosarcoma. *In repo: data tables only.* Effect: **0/+** consistent with the
   kinase report's "works briefly".
7. **Genomic-subtype umbrella pilot, China (ChiCTR2000036618).** NPJ Precis Oncol 2025 (PMID
   41372533; paper, abstract only). 19 refractory patients assigned by exome sequencing and IHC to
   PD-1 + gem/doc, PARP inhibitor + temozolomide, or the Aurora kinase inhibitor tinengotinib;
   median PFS 50 days overall. Effect: **0**; feasibility only.
8. **SBRT plus checkpoint inhibitor, retrospective.** Int J Radiat Oncol Biol Phys 2026 (PMID
   41325874; paper, abstract only). 62 relapsed patients; SBRT + ICI median PFS 5.68 months,
   better systemic response than ICI alone or with conventional radiation; grade 3–4 pneumonitis
   4/18. Effect: **0**; uncontrolled, single institution.
9. **AcSé-ESMART arm D, olaparib + irinotecan.** Clin Cancer Res 2026 (PMID 41591981; paper, abstract
   only). 70 children and young adults; ORR 9.1%; one osteosarcoma partial response; response may
   track aneuploidy. Effect: **0**.

### B. Pet-dog studies

10. **Palliative radiation plus Listeria-HER2 (Lm-LLO-HER2) in 15 dogs.** Mol Ther Oncol 2026 (PMID
    42291138, PMC13264224; paper, abstract only). Treatment-naive dogs without metastases;
    well tolerated; primary-tumour progression delayed and survival prolonged in **5 of 15**;
    baseline immune status separated long from short survivors. Single-arm, no control. Effect:
    **±** for the landscape report's OST-HER2 paragraph: a small signal in a different setting,
    after the 118-dog adjuvant trial showed no benefit.
11. **Histotripsy (focused-ultrasound ablation) in canine osteosarcoma.** Cancers 2026 (PMID
    42588726; paper, abstract only). Local and systemic immune activation within 5 days; "a subset"
    exceeded the expected 10–12-month survival. No numbers in the abstract. Effect: **0**.
12. **NCI-COTC030 inhaled IL-15 after amputation (already in repo).** Front Immunol 2025 (PMID
    41209004; abstract re-read): halted for futility, outcomes worse than historical controls;
    IL-6 rose after amputation and chemotherapy and tracked loss of blood-cell cytotoxicity.
    Effect: **+** for lead 1 (inflammation after surgery), already used in the lung report.

### C. New targets and antigen-directed drugs (detail in `research_notes/Surface targets/protein_check.md`)

13. **Surface and global proteomics of 22 PDXs (BC Cancer, CHOP, COG).** Mooney et al., Cell Rep
    2026 (PMID 42647168; paper, full text). Top new candidates SGCD, ROR2, TMEM119; LRRC15, MRC2,
    CADM1, CD109, MMP14, ALPL, EPHA3, EPHB2 confirmed at protein level; ROR2 and TMEM119 nearly
    absent from normal paediatric tissue by IHC. *Data tables only.* Effect: **+** for lead 5;
    **−** for our HPA surface filter, which excluded TMEM119.
14. **LRRC15 CAR-T cells (St. Jude).** O'Reilly et al., Clin Cancer Res 2026 (PMID 41627173; paper,
    full text). 18 paediatric primaries, median H-score 113.5; CAR-T active and non-toxic in mice;
    antigen-loss escape. Effect: **+** lead 5.
15. **Spatial transcriptomic atlas of aggressive osteosarcoma (19 patients, 26 samples).**
    Moquin-Beaudry et al., Nat Commun 2026 (PMID 42399228; paper, full text). 9-gene surface
    signature including LRRC15 and IFITM5, stable at relapse; IHC shows components in different
    tumour compartments; systematic lymphoid exclusion, a type I interferon signature, and
    monocyte-to-osteoclast differentiation in lung metastases. Effect: **+** lead 5 (LRRC15);
    **±** single-antigen drugs; context for the lung report.
16. **CADM1-tesirine ADC.** Mol Cancer Ther 2026 (PMID 41517891; paper, abstract only). Active in
    all six CADM1-positive osteosarcoma PDXs, three complete responses. Effect: **0/+** new target
    with a drug.
17. **Paediatric Therapeutic Development Workshop on osteosarcoma (LifeArc, ITCC, CRUK).** Baxter
    et al., Br J Cancer 2026 (PMID 42613365; paper, abstract only). Expert consensus: an **LRRC15 ADC
    "with an osteosarcoma-relevant payload"** is promising; SMARCAL1 inhibitors/degraders "very high
    priority"; KIF18A preclinical work required; eIF4A1 inhibitor early-phase study warranted;
    RUNX2 and MYC high priority. Effect: **+** lead 5, independent of us.
18. **Meflin (ISLR) ADC.** Oncogene 2025 (PMID 41120731; paper, abstract only). Meflin high in
    recurrent, doxorubicin-resistant cells; MMAE ADC effective in mice. Effect: **0**.
19. **Vobramitamab duocarmazine (B7-H3 ADC), paediatric xenografts.** Clin Cancer Res 2026 (PMID
    41941262; paper, abstract only). Responses across tumour types including osteosarcoma, **with
    no clear link between B7-H3 protein level and response.** Effect: **±** — supports B7-H3 ADCs,
    but like T-DXd it suggests payload and delivery, not antigen level, may drive ADC activity in
    these tumours. That is a caution for the RNA-window logic of the surface screen.

### D. Genomics, subtypes and biomarkers

20. **SMARCAL1 is an osteosarcoma predisposition gene.** JCO 2025 (PMID 41066719, PMC12643103; paper,
    abstract only). Germline pathogenic SMARCAL1 variants in 2.6% of 230 osteosarcoma cases in
    discovery and 1.8–3% in three replication cohorts; the second allele was deleted in 3 of 4
    tumours. The 2026 workshop then ranked SMARCAL1 drugs "very high priority". Effect: **0/+**
    new biology and a new target with a germline handle; not in any report.
21. **MYC amplification predicts poor survival.** Cancer 2025 (PMID 41199591; paper, abstract only).
    105 patients: amplification (>7 copies) in 16%, high protein in 22%; 3-year OS 27% vs 74% with
    vs without amplification (adjusted HR 3.4); 0% vs 79% when both. Related: MYC ecDNA in a
    155-xenograft sarcoma PDX biobank (Adv Sci 2026, PMID 42864811; abstract only), and **MYC-driven
    mouse osteosarcoma lines were about 8-fold more resistant to cabozantinib** in vitro (our calculation from the IC50s) than p53-driven
    lines (mean IC50 5.51 vs 0.65 µM) (Kappa et al., bioRxiv Sep 2026; preprint, abstract only).
    Effect: **±** for lead 2. Any test of "do VEGFR-pathway amplifications predict TKI benefit"
    should record MYC status too, since MYC-amplified tumours do worse and may resist cabozantinib.
22. **Two epigenetic osteosarcoma states.** Cancer Discov 2026 (PMID 41037662, PMC12877751; paper,
    abstract only). "Early" and "late osteoblast-derived" chromatin states, coexisting in one
    tumour, with different drug responses in PDXs and linked to survival. With item 23 and Visser
    et al. (bioRxiv Jun 2026; preprint, abstract only: osteoblastic/chondroblastic-like states
    predict worse survival), three groups now describe lineage states that matter for treatment.
    Effect: **0**; context for the literature map and surface report.
23. **Metastases lose osteoblastic lineage.** Tanaka et al., bioRxiv Jun 2026 (doi
    10.64898/2026.06.10.731352; preprint, abstract only; confirmed via bioRxiv API). Single-nucleus
    RNA from 24 tumours: the osteoblastic state is dampened in metastases and after treatment.
    Effect: **−** for IFITM5 (an osteoblast gene) as a target for metastatic disease (our
    inference); relevant to the lung report.
24. **International framework for molecular classifiers.** Marinoff et al., NPJ Precis Oncol 2026
    (PMID 42086782; paper, abstract only). An international working group concludes that
    **pre-treatment ctDNA is "positioned for clinical implementation"** while other classifiers
    need prospective validation. Effect: **+** lead 7 (ctDNA-adapted treatment).

### E. Lung metastasis and the inflammation leads

25. **DKK1 in patients.** Uceda Arias-Stella et al., medRxiv Nov 4, 2026 (doi
    10.64898/2026.11.03.26367177; preprint, abstract only). Plasma DKK1 in 34 patients fell 12.4% per
    30 days on treatment, higher with metastatic presentation and poor necrosis; tumour DKK1 RNA
    linked to worse OS (HR 1.35 per SD) and metastasis-free survival (HR 1.48) in two cohorts; made
    mainly by malignant cells. Effect: **+** lead 4 (DKK1), as human correlative support.

Also read, lower priority:
- Lung-fibroblast inflammatory niche drives dormancy, stemness and doxorubicin resistance
  (Research Square, Jul 2025; preprint, abstract only) and doxorubicin-induced IL-1β/COX-2 loop
  (Research Square, Aug 2026; preprint, abstract only). Both **+** for lead 1 in mechanism only.
- IL-1α from lung epithelium drives IL-6/CXCL8 in metastasis-initiating cells; IL-1 blockade cut
  metastasis (Cancer Res 2025, PMID 40882022; abstract only). **Already in the lung report.**
- KIF18A inhibitor active in whole-genome-doubled osteosarcoma cells and xenografts (Cancer Biol
  Ther 2026, PMID 42328720; abstract only), matching the workshop's KIF18A recommendation.
- Denosumab AOST1321 (PMID 41159913), OAIE apatinib (PMID 41290609), NCI-COTC030, MISTOSUS, ESMMO:
  already covered by existing reports.

## New trials registered since June 1, 2025 (registry, ClinicalTrials.gov, November 19, 2026)

Of 49 new interventional records naming osteosarcoma, most already appear in this repository's
trial tables (FOSTER-CabOS NCT07871864, 3CAR4OS NCT07428993, RAD3CAR NCT07222735, Lu-TARGO,
SOT106, ZAMBONE NCT07193550, the DFMO trial NCT07321912, and others). Those that do not appear in
any report or note, and touch the leads:

| NCT | What | Status | Why it matters |
|---|---|---|---|
| NCT07227571 (FIERCe) | FOLR1 CAR-T, Fred Hutch, relapsed/refractory osteosarcoma, ages 1–75 | Recruiting since 2026-01-16 | Another antigen beyond B7-H3/GD2/HER2; FOLR1 is in the Mooney 2026 known-protein list. FOLR1 RNA is low in our screen (rank 1,924; 17.8 TPM, 77% of tumours; our calculation), so this is a test of whether RNA ranks mislead |
| NCT07596693 | KXV01, in-vivo lentiviral TCR, TCRx Therapeutics, solid tumours "including osteosarcoma" | Recruiting since 2025-12-19 | New modality; target not given in the summary |
| NCT07774533 | 68Ga-B7-H3 nanobody PET in osteosarcoma, Peking University First Hospital | Recruiting; primary completion 2026-08-05 (actual) | Imaging could select B7-H3-high patients for ARTEMIS-type drugs |
| NCT07787429 | Mifamurtide vs sorafenib in high-risk osteosarcoma, Poland | Recruiting, 40 planned | A small randomised comparison of two existing drugs |

## Apparent contradictions with the project

- **ADC activity may not track antigen level** (T-DXd PDXs, PMID 40911899; vobramitamab PDXs, PMID
  41941262; both abstract only). That does not contradict the surface screen's ranking, but it
  weakens the inference "a bigger RNA window means a better ADC target".
- **TMEM119 surface protein** (Mooney 2026) contradicts the HPA-based surface filter that kept it
  out of the shortlist.
- **ARTEMIS-011 CI** in the PubMed abstract (0.21–1.23) disagrees with the repo's data table
  (0.20–0.55). Needs the full paper. *Resolved November 19, 2026: re-reading the abstract, 0.20–0.55 is the progression-free
  survival HR's CI and 0.21–1.23 belongs to the overall-survival HR (0.51). No conflict, no typo.*
- Nothing found contradicts the lung-metastasis inflammation lead, the kinase-pill benefit
  estimate, or the trials-fail-to-finish finding.

## Limits of this scan

- Triage was by title for about 450 PubMed records, 100 preprints and 63 trial records; most of the 2,665 PubMed osteosarcoma records were not
  screened individually. Laboratory-only papers on single genes or herbal compounds were skipped
  on purpose.
- Conference abstracts (ASCO, ESMO, CTOS 2025–26) were not searched directly; company and
  trade-press sites were blocked from this environment.
- Most items were read as abstracts only. Full text was read for Mooney 2026, O'Reilly 2026,
  Moquin-Beaudry 2026 and Lee 2023.
- Preprints are not peer-reviewed.
