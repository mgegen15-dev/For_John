# Full-text verification: FAK (PTK2) and DKK1 claims in the pet-dog trial brief

*Verification pass, November 2026. Scope: read the full papers behind every FAK and DKK1
claim in `briefs/Brief - pet dog trial of FAK or DKK1 blockade.md`, which until now rested on
abstracts only. Sources: Europe PMC full-text XML where open access, bioRxiv API, publisher
pages, ClinicalTrials.gov API v2, web search. PubMed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov
(CAPTCHA), sciencedirect.com, aacrjournals.org and csuanimalcancercenter.org were not
reachable from this session; where that mattered it is stated per paper.*

## Summary of what changed

Three findings change the brief materially:

1. **Defactinib has already been given to dogs with metastatic osteosarcoma.** A Colorado State
   University Animal Cancer Center trial combines oral defactinib with losartan and toceranib in
   dogs with pulmonary-metastatic OS, including an 8-hour pharmacokinetic sampling after the
   first defactinib dose. The brief's "What neither target has: any dog data, any test of the
   actual clinical drug in osteosarcoma, or a trial" is false for FAK/defactinib.
2. **PMIDs 39781890 and 39713389 are the same paper** (Mol Cancer Ther 2025 and its bioRxiv
   preprint). The brief and the close-read count one result twice.
3. **The "three different ways of blocking DKK1 reduced metastasis" sentence does not hold.**
   One of the three (PMID 35277659) explicitly failed to measure metastasis; the antibody paper's
   metastasis result is significant only after a post-hoc exclusion; and the antibody and
   small-molecule papers are the same laboratory, using the same PDX that the morpholino lab
   also adopted.

Offsetting those, one paper the close-read filed as *contradicting* DKK1 blockade is in fact
*supporting* and from an independent group (PMID 39280613), which strengthens the DKK1 case.

---

## FAK (PTK2)

### PMID 28406574 — PF562271 in xenografts (Hu et al., Cancer Sci 2017, Ruijin Hospital, Shanghai). Full text read.

- **Model:** subcutaneous flank xenograft, **143B only**, 4-week-old male BALB/c nude mice.
  Not orthotopic, not tail-vein, no amputation, no spontaneous-metastasis arm.
- **n:** 6 per group (PF562271 vs vehicle). Single dose level.
- **Dose/route:** PF562271 50 mg/kg by oral gavage, **twice daily**, started at ~100 mm3 mean
  volume, 21 days.
- **Primary tumour:** tumour volume and weight significantly reduced (weight ***P < 0.001*);
  volume by Student's t-test per time point. CD31 microvessel density reduced, TUNEL-positive
  cells increased, p-FAK-Y397 suppressed in tumour sections (total FAK unchanged).
- **Metastasis: not measured at all.** The word does not appear in any in vivo result; the only
  metastasis content is the human tissue-microarray correlation.
- **In vitro:** 6 cell lines, IC50 1.76–3.83 uM; HUVEC tube formation inhibited.
- **Patient tissue:** TMA of 109 OS cases; p-FAK-Y397 intensity higher in metastatic cases and
  inversely correlated with overall survival.
- **COI:** "The authors have no conflict of interest." Funding not stated in the text.
- **What the abstract overstated / the paper's own weak points:**
  - "Dramatically reduced" is the authors' word for a subcutaneous single-cell-line experiment
    with n=6 and one dose.
  - **Target-independence concern:** IC50s were similar across lines with high p-FAK-Y397
    (143B, WELL5, MG63, U2OS) and low p-FAK-Y397 (HOS, MG63.2) — 1.76–3.83 uM across all six.
    If p-FAK level does not predict sensitivity, the biomarker logic in the brief's endpoint
    section is not supported by this paper.
  - **Selectivity concern:** the HUVEC IC50 (1.118 uM, 24 h) is *lower* than every tumour-line
    IC50 (1.76–3.83 uM, 72 h). Normal endothelium was the most sensitive cell type tested.
  - The paper mis-cites its own anchor: it says Ren et al. (PMID 26393679) found p-FAK-Y397 high
    in "37% of primary human OS tissues (42/113)", which is lower than the 62–90% figures the
    close-read reported from other abstracts.

### PMID 28846700 — pFAK-Y397 in 62.3% (Thanapprapasr et al., PLoS One 2017, Ramathibodi Hospital, Bangkok). Full text read.

- **Cohort:** 53 high-grade primary OS patients, single centre, April 2005 – March 2014.
  **33 of the 53 had metastases** at diagnosis or during follow-up, so the cohort is enriched
  for metastatic disease.
- **Figures confirmed exactly:** total FAK overexpressed in 48/53 (90.6%); pFAK-Y397
  overexpressed in 33/53 (**62.3%**). Detectable (as opposed to overexpressed) pFAK-Y397 was
  47/53 (88.7%).
- **Prognostic value — important nuance the abstract blurs:** in the **whole 53-patient cohort
  pFAK-Y397 did not affect survival** (P > 0.05, univariate Cox, S3 Table). The prognostic
  signal exists only in the **33-patient metastatic subgroup**: Kaplan-Meier P = 0.044;
  univariate HR 2.32, P = 0.048; multivariate HR 2.60, P = 0.034. All three P values sit just
  under 0.05 in a subgroup of 33.
- pFAK-Y397 overexpression did correlate with poor histologic response to neoadjuvant
  chemotherapy regardless of metastasis status.
- **Independence:** no author overlap with 28406574 or 23845472.
- **COI/funding:** no competing-interests or funding statement located in the retrieved
  full text.

### PMID 23845472 — beta5/FAK/GSK3beta panel (Le Guellec et al., Hum Pathol 2013, CHU Toulouse). **Full text NOT available** (not in PMC; ScienceDirect and doi.org unreachable from this session). Abstract only.

- From the abstract: 36 pre-treatment biopsies, three-marker immunohistochemical panel
  (beta5 integrin + FAK + GSK3beta), AUC 89.9%, diagnostic accuracy 90.3% for discriminating
  good from poor responders to neoadjuvant chemotherapy.
- **Unverified:** n per response group, whether the panel was validated on an independent set
  or only fitted on the same 36 biopsies, the cut-offs, and COI. A 3-marker panel fitted and
  evaluated on 36 cases is at high risk of optimistic over-fitting; with no full text this
  cannot be checked. The brief's sentence should not lean on the AUC.
- No author overlap with the other two FAK papers (independent French group).

### FAK contradicting papers

| PMID | Full text? | What it actually shows | Weight |
|---|---|---|---|
| 16759849 | Abstract only (Eur J Cancer, not OA) | SAOS-2 anoikis resistance runs through Src and PI3K/Akt; FAK dephosphorylates normally, so FAK activity "not essential". **In vitro only.** | Genuine but narrow: about anoikis, not about whether FAK inhibition shrinks tumours. |
| 20814573 | **Full text read** | **Not an osteosarcoma FAK paper.** The FAK-null experiments are in **mouse embryonic fibroblasts**; U2OS is used only as a GFP-actin chassis for live stretch microscopy. Bovine aortic endothelial cells for the rest. | Should be dropped from the contradiction list — it is noise, as the close-read suspected. (Incidental: R. Kaunas, senior author here, is also an author on the DKK1 paper 39805917.) |
| 12376862 | Abstract only (Der Pathologe 2002, German, not OA) | FAK protein expressed in high-grade OS but **no transcriptional overexpression**; Pyk2 mRNA decreased. | Genuine tension with the 90.6% total-FAK IHC figure; n and methods unverifiable. Supports measuring *activity* (pY397) rather than abundance. |
| 15485819 | Abstract only (JBC 2004, not OA) | An **ILK** paper. FAK appears as a negative regulator of RhoA; FAK activation was reduced in WT-ILK U2OS cells and FAK overexpression rescued spreading/polarity defects. In vitro. | FAK is incidental to the paper's question. Weak as a contradiction. |
| 35008585 | **Full text read** | U2OS only, in vitro, overexpressing STIM1 variants. Constitutively active STIM1 raised calpain activity and FAK/paxillin/vinculin **turnover** while impeding migration. **FAK itself was never perturbed** — it is a readout. | Shows FAK turnover does not track migration; says nothing about FAK inhibition as therapy. Weak as a contradiction. |

**Net on FAK contradictions:** of the five, one (20814573) is not about osteosarcoma FAK at all,
two (15485819, 35008585) are cell-biology papers in which FAK is incidental, and two
(16759849, 12376862) are real but narrow — one about anoikis in vitro, one about mRNA abundance.
None tests a FAK inhibitor and reports failure. The close-read's framing ("a target so
pleiotropic that its necessity varies by context") survives, but the contradiction list is
weaker than it looked from abstracts.

---

## DKK1

### Author / laboratory map (this is the key result for the DKK1 cluster)

**Lineage A — Loeb lab** (David M. Loeb; Johns Hopkins, later Albert Einstein College of Medicine):
- **27049730** BHQ880 antibody — Goldstein SD, Trucco M, Bautista Guzman W, Hayashi M, **Loeb DM**.
- **39781890 / 39713389** WAY262611 small molecule — Tal A, ... Cahan P, **Loeb DM**. Its own
  abstract says "**Our lab** previously demonstrated that an mAb against DKK-1 prevented
  metastatic disease in a mouse model", i.e. it cites 27049730 as the same lab.

**Lineage B — Gregory lab** (Carl A. Gregory, Texas A&M):
- **35277659** DkkMo morpholino 2022 — Pan S, ..., **Gregory CA**.
- **39805917** DkkMo antisense 2025 — Haskell A, Pan S, ..., Kaunas R, **Gregory CA**.

**Shared model, not independent models.** 39805917 states plainly: "The DAR PDX-OS was
specifically selected because the results from DkkMo could be compared to previously published
studies with the monoclonal antibody BHQ880." The DAR PDX is the Loeb lab's model (both DAR and
LR were gifts from Chand Khanna, NCI). So Lineage B's strongest in vivo result was deliberately
run in Lineage A's model.

**Lineage C — Shenzhen group** (Hu C, Shen Y, Xie Q, Liang J, Wang Y, Tao H):
- **39280613** XD23 (iScience 2024) and **37716273** compound 7m (Bioorg Chem 2023) share
  authors. Notably, **this group also wrote the key FAK paper 28406574** (Hu C, Liang J, Shen Y,
  Wang J all appear on it). The same group therefore supplies the brief's single best FAK in vivo
  paper *and* two DKK1 papers that point in opposite directions from each other.

So the brief's "three different ways of blocking DKK1" comes from **two laboratories**, and the
antibody and small-molecule arms are the **same** laboratory. The modality count is three; the
independent-laboratory count is two, and the independent-model count is effectively one for the
decisive experiments.

### PMID 27049730 — BHQ880 antibody (Goldstein et al., Oncotarget 2016, Johns Hopkins). Full text read.

- **Model:** two patient-derived xenografts, **DAR** (from a malignant pleural effusion) and
  **LR** (from a resected pulmonary metastasis), both gifts from Chand Khanna (NCI). 3 mm
  fragments implanted **orthotopically in the pretibial space** of NSG mice, then **hindlimb
  amputation** through the proximal femur at 20 mm leg diameter, then post-operative observation
  — the closest existing mouse analogue of the proposed dog design. A separate subcutaneous
  flank cohort was used for the serum-DKK1 kinetics.
- **n:** LR — control 10, immediate treatment 5, delayed 5. DAR — control 8, immediate 5,
  delayed 12. Totals 18 control vs 27 treated.
- **Dose/route:** BHQ880 (human neutralising **IgG1** anti-DKK-1 mAb, supplied by Novartis)
  10 mg/kg intraperitoneally three times weekly.
- **Primary tumour:** growth slowed in both PDX; the authors' own summary is "**modestly**
  decreases primary tumour growth". In the subcutaneous cohort the effect existed only during the
  early phase, while control serum DKK-1 was high (0.47% vs 0.95% volume increase per 3 days,
  P < 0.0001); during the late phase, when control serum DKK-1 had fallen to undetectable,
  BHQ880 had **no effect** on growth velocity.
- **Metastasis: measured, and this is where the brief overstates.**
  - **Full cohort, as randomised: 6/18 control vs 4/27 treated, P = 0.17 — not significant.**
    The paper says so in its own figure legend: "This difference approaches, but does not reach,
    statistical significance."
  - The significant result requires **excluding 3 treated mice that had local recurrence**:
    1/24 vs 6/18, P = 0.03, Fisher's exact. All three excluded treated mice had metastases, so
    the exclusion moves events out of the treated arm only.
  - Survival benefit was seen in the **LR model only** (DAR was administratively censored).
- **Mechanism:** nuclear beta-catenin in 4.4% of control vs 45% of treated tumour cells;
  osteopontin in 8% vs 25.8%. Wnt PCR array: multiple Wnt genes up. The paper's conclusion is
  that **Wnt signalling is anti-tumorigenic in osteosarcoma** — the opposite of the premise in
  24859848 and 37716273.
- **COI:** "Study drug, BHQ880, was supplied by Novartis, but the company played no role in the
  design, conduct, or interpretation of experiments, nor in the writing of the manuscript."
- **Funding:** NCI 1R01CA138212-01 (Loeb), 2P30CA006973 (Johns Hopkins), Pablove Foundation,
  Giant Food Children's Cancer Research Fund.
- **Limitation the authors state:** NSG mice have no lymphocytes or NK cells.
- **BHQ880 is not "close to DKN-01".** BHQ880 is a Novartis **IgG1**; DKN-01/sirexatamab is a
  Leap Therapeutics **IgG4**. They are different molecules from different sponsors with different
  isotypes and therefore different effector function. "Another anti-DKK1 antibody" is accurate;
  "close to DKN-01" is not supported.

### PMID 35277659 — DkkMo morpholino (Pan et al., Br J Cancer 2022, Texas A&M). Full text read.

- **Model:** **MOSJ-Dkk-1** cells — murine MOS-J osteosarcoma cells **engineered to
  overexpress Dkk-1** — implanted orthotopically in hindlimbs of nude mice, dsRed-labelled,
  tracked by fluorescence. The target is forced into the model, which limits what the result
  says about tumours with native DKK1 levels.
- **n:** 8–9 tumours per group.
- **Dose/route:** DkkMo (vivo morpholino) 12.5 mg/kg; doxorubicin 5 mg/kg; or both;
  intraperitoneally every 48 h. **Controls were "no treatment"**, not a scrambled morpholino —
  scrMo was used in vitro only, with the justification that "the systemic effects of the backbone
  morpholino are negligible". So the in vivo comparison is not vehicle- or sequence-controlled.
- **Results:** reduced rate of tumour expansion; necrotic foci; by micro-CT, preserved bone
  topology, bone mineral density and reduced bone absorption (ANOVA, P values per panel).
- **Metastasis: NOT measured — and the attempt failed.** Verbatim: "little is known about their
  ability to metastasize. **Attempts to detect MOSJ-Dkk-1 cells in the lungs of mice by PCR were
  unsuccessful**, but DkkMo perturbed expression of several genes involved in cell attachment,
  migration and metastasis"; and "**these data do not provide definitive proof that DkkMo
  inhibits metastasis**". The metastasis content of this paper is gene-ontology terms and
  Arpc2 downregulation, nothing more.
- **COI:** "The authors declare no competing interests."
- **Funding:** CPRIT RP160765 and RP170496 (Texas, not NIH).

### PMID 39805917 — DkkMo antisense (Haskell et al., Sci Rep 2025, Texas A&M). Full text read.

- **Model:** **DAR human PDX-OS** (the Loeb lab's model) implanted adjacent to the femoral
  diaphysis of NSG mice. Orthotopic, **no amputation step**; follow-up 12 days.
- **n:** 9 vehicle vs 10 DkkMo for the metastasis endpoint.
- **Dose/route:** DkkMo 12.5 mg/kg intraperitoneally every 48 h; controls received **vehicle**
  (an improvement on the 2022 paper's untreated controls).
- **Primary tumour:** growth kinetics by ultrasound reduced (two-sided ANOVA), but
  **tumour volume at endpoint by micro-CT was not significantly reduced.** The authors describe
  tumour mass as "modestly affected", with the main histological finding being extensive necrosis.
- **Metastasis: genuinely measured.** Lung human GAPDH by qRT-PCR, normalised to murine GAPDH:
  signal significantly lower in DkkMo lungs, and **7/9 vehicle lungs vs 2/10 DkkMo lungs** had
  detectable human GAPDH. Micro-metastases confirmed on H&E in vehicle lungs. This is the
  cleanest metastasis result in the DKK1 set.
- **Bone:** reduced bone destruction and product-of-inertia changes closer to contralateral.
- **COI:** "The authors declare no competing interests."
- **Funding:** **R21 CA286523 (NCI)** plus CPRIT RP170496/RP160765 — this confirms the brief's
  "Texas A&M (R21)".
- **Note:** the article carries a **correction** (errors in Table 1 references).
- **Authors' own limitation:** "evaluation in spontaneous genetic OS models in immune competent
  hosts is warranted."

### PMIDs 39781890 and 39713389 — WAY262611 (Tal et al.). **Same paper.**

- 39713389 is the **bioRxiv preprint** (doi 10.1101/2024.12.10.627181, posted 11 Dec 2024);
  39781890 is the **Mol Cancer Ther 2025** version (doi 10.1158/1535-7163.mct-24-0744,
  PMC12048250). Identical title, identical author list (one name rendered "Perez NM" vs
  "Munoz Perez N"). They must be counted as one result.
- **Full text could not be retrieved**: the Europe PMC full-text endpoint returns HTTP 500 for
  PMC12048250, the PMC page serves a CAPTCHA, aacrjournals.org is behind Cloudflare, and
  bioRxiv returned HTTP 429 / Cloudflare error 1015 on every attempt. **Abstract only.**
- From the abstract: WAY262611 activates canonical Wnt signalling, enhances nuclear beta-catenin
  localisation and transcriptional activity, slows proliferation of OS cell lines; in vivo it uses
  "our orthotopic implantation/amputation model of osteosarcoma metastasis" to assess "primary
  tumour progression and metastatic outgrowth of disseminated tumour cells"; it "induces
  osteoblastic differentiation of a patient-derived xenograft of osteosarcoma in vivo, as well as
  inhibiting metastasis". Differentiation status by single-cell RNA-seq.
- **Unverified:** cell lines, PDX identity, n per group, dose, route, effect sizes, statistics,
  whether the metastasis result needed exclusions as in 27049730, and COI. Given that the same
  lab's earlier antibody paper reported a non-significant primary comparison that became
  significant only after excluding 3 of 27 treated mice, the WAY262611 metastasis claim should
  not be treated as verified until the full text is read.
- **Funding (Europe PMC grant list):** NCI **R01 CA262802** (Loeb, Einstein) — confirms the
  brief's "Albert Einstein College of Medicine (R01)" — plus P30 CA013330, and several NIA/NIGMS
  grants attached to co-authors (R01 AG061917, R01 AG068232, U19 AG055373, P20 GM109036).
- The abstract says nothing about bone preservation.

### DKK1 "contradicting" papers — one reclassification

- **PMID 39280613 (XD23, iScience 2024). Full text read. This is NOT a contradiction; it
  supports DKK1 blockade, and it is the only such result from a group outside Lineages A and B.**
  XD23 *downregulates* DKK1 and *activates* Wnt/beta-catenin, and the paper reports reduced
  proliferation, reduced lung metastasis, reduced bone destruction and increased apoptosis.
  Model: orthotopic intratibial inoculation of rat **UMR-106** cells into male BALB/c nude mice,
  **5 groups of 6** (vehicle, sham, methotrexate 10 mg/kg, XD23-low 10 mg/kg, XD23-high
  15 mg/kg), **oral** dosing 2–3x weekly for four weeks, with high-dose methotrexate as an
  active comparator. Causal attribution to DKK1: Dkk1-overexpressing 143B cells were
  **2.9-fold less sensitive** to XD23 than wild type. Mechanism direction matches 27049730 and
  39805917 exactly. The close-read filed this as a contradiction on the strength of a phrase;
  on reading, it belongs in the supporting column.
- **PMID 37716273 (compound 7m, Bioorg Chem 2023). Abstract only (Elsevier unreachable).
  Genuine contradiction, but weak and self-undermining.** The data direction is that 7m
  **increased** DKK1 expression and **decreased** p-beta-catenin while killing 143B cells — the
  opposite of the blockade rationale — even though the title says "by inhibiting DKK1-Wnt/
  beta-catenin pathway". **In vitro only** (143B, MG63, HSF); no animal arm. Decisively, it is
  from the **same group** as 39280613, which published the opposite direction a year later. A
  lab contradicting itself in vitro is weaker evidence than its own in vivo result.
- **PMID 24859848 (oridonin, Int J Oncol 2014, Chongqing). Abstract only (not OA). Genuine
  contradiction.** Oridonin inhibits 143B proliferation by **suppressing** Wnt/beta-catenin,
  **upregulating** Dkk-1 and enhancing GSK3beta; crucially, **Dkk-1 overexpression potentiated**
  the anti-proliferative effect and beta-catenin overexpression attenuated it. A xenograft
  confirmed growth inhibition (metastasis not assessed; n, route and dose not in the abstract).
  This is the cleanest surviving contradiction of the DKK1-blockade direction, because the
  epistasis experiment points the wrong way for the blockade hypothesis.

**Net on DKK1 direction:** the therapeutic direction (block DKK1, activate Wnt, less metastasis)
now has an independent third group behind it (39280613, in vivo, oral agent, active comparator),
which is a real gain. Against it stands one in vitro paper that contradicts its own group's later
work (37716273) and one older paper with a well-designed epistasis experiment pointing the other
way (24859848). The controversy is narrower than the close-read implied, but it is not resolved.

---

## New searches: 2024–2026 drugs, dogs, canine expression

### Defactinib or VS-4718 in osteosarcoma (2024–2026)

- **No published preclinical study of defactinib or VS-4718 in any osteosarcoma model** was
  found. The 2025–2026 FAK-inhibitor metastasis literature is in melanoma (VS-4718 +/-
  avutometinib reducing lung and brain metastases), NF2-related schwannomatosis, and a 2026
  bioRxiv preprint on ECM remodelling and CD8 T-cell trafficking (VS-4718 reducing lung
  metastatic burden from ~0.7% to ~0.05% of lung area) — none in OS.
- Note for the brief's drug choice: VS-4718, not defactinib, is the FAK inhibitor normally used
  in mouse work because of better murine pharmacokinetics; and one review states VS-4718's own
  clinical development was discontinued. The brief's mouse evidence uses a third compound again
  (PF562271). No single FAK inhibitor has both the OS mouse data and the clinical path.

### Has either drug been used in dogs?

- **Defactinib: yes, in dogs with osteosarcoma.** The Colorado State University Animal Cancer
  Center lists "Focal Adhesion Kinase (FAK) Inhibition to Improve Losartan-Toceranib
  Immunotherapy in Canine Metastatic Osteosarcoma": dogs with pulmonary-metastatic OS receive
  **oral losartan twice daily, oral defactinib once daily and oral toceranib (Palladia) every
  other day**, with **blood sampling over 8 hours after the first defactinib dose** (i.e. a
  canine PK arm) and rechecks at 2 and 4 weeks; study drugs supplied plus $750 toward
  study-related diagnostics. The question it asks is whether the three-drug combination beats
  the established two-drug losartan-toceranib regimen.
  - The CSU page could not be fetched directly (host not resolvable from this session); these
    details come from search-engine extraction of that page, which was reported as roughly
    913 days old (≈ mid-2023). **Enrolment status and any results are unconfirmed**, and no
    publication or AAHSD registry entry was found. This needs a direct check with CSU.
  - Background: the losartan + toceranib backbone is published (Regan et al., 28 dogs with
    lung-metastatic OS, ~50% clinical benefit, ~30% measurable response), and the losartan +
    sunitinib version moved into a human phase 1/1b in relapsed/refractory OS (NCT03900793).
- **DKN-01/sirexatamab: no veterinary use found**, in dogs or any other species outside humans.

### Registered trials

- ClinicalTrials.gov API v2: **no study of defactinib or DKN-01 in osteosarcoma** (condition
  "osteosarcoma", intervention either drug: zero hits). The only defactinib sarcoma study is
  NCT07743554, avutometinib + defactinib in malignant peripheral nerve sheath tumour, status
  NOT_YET_RECRUITING. So "no registered human osteosarcoma trial" holds for both drugs; "no
  trial at all" does not, because of the CSU canine study.
- **Defactinib approval confirmed:** FDA accelerated approval **8 May 2025**, avutometinib +
  defactinib (Avmapki Fakzynja Co-pack) for adults with recurrent KRAS-mutated low-grade serous
  ovarian cancer after prior systemic therapy; basis RAMP 201 (57 patients, 44% response rate);
  defactinib 200 mg orally twice daily, 3 weeks of each 4-week cycle. Accelerated approval, so
  continued approval may depend on a confirmatory trial. The brief's wording is accurate.

### Canine FAK and DKK1 expression data

- **No canine osteosarcoma tissue study of FAK or pFAK** (IHC or otherwise) was found, and
  **no canine osteosarcoma DKK1 data at all** — not tumour expression, not serum.
- Partial canine FAK material that does exist:
  - **Canine haemangiosarcoma** (Marley et al., Vet Comp Oncol 2012): phosphotyrosine enrichment
    showed FAK **constitutively autophosphorylated at Y397**; a FAK inhibitor reversed Y397 and
    Y576/577 phosphorylation, reduced migration and was cytotoxic. Different tumour, but it
    establishes that the Y397 assay works in dog tissue.
  - **Canine OS cell lines** (D17 and two others): sulforaphane reduced p-FAK (Rizzo et al., via
    review). Cell lines only.
- Nearest canine Wnt work: Piskun et al., PLoS One 2011, Wnt/beta-catenin in archived canine OS
  tissue and cell lines — **DKK1 was not measured**. Canine DKK1 work exists only in a prostate
  cancer model.
- **This confirms and sharpens the brief's "Before the dog study" step.** The expression survey
  it proposes is genuinely missing for both targets, and for DKK1 it is missing completely.

---

## Verdict on each claim in the brief, with proposed wording

### Holds as written

- "activated FAK (pY397) is high in about 62% of tumours (PMID 28846700)" — 33/53 = 62.3%,
  exact. (But see the suggested addition below about where the prognostic signal lives.)
- "defactinib, FDA-approved in 2025 with avutometinib for KRAS-mutant low-grade serous ovarian
  cancer" — correct; accelerated approval, 8 May 2025.
- "DKN-01 (sirexatamab), in clinical trials for gastric and other cancers" — correct.
- "NIH already funds osteosarcoma work on both targets: ... DKK-1 at Albert Einstein College of
  Medicine (R01) and Texas A&M (R21)" — confirmed in the papers' own grant records:
  R01 CA262802 (Loeb) and R21 CA286523 (Gregory).
- "Trials: none in osteosarcoma" for each target, **if read as registered human trials** — the
  ClinicalTrials.gov check returns zero. See the correction below for dogs.

### Needs changing

**1. Line 21, the DKK1 mouse-evidence sentence. Currently:**

> **Mouse evidence:** three different ways of blocking DKK1 reduced metastasis and preserved bone
> in mice. These were an anti-DKK1 antibody close to DKN-01 in patient-derived orthotopic models
> (PMID 27049730), a morpholino (PMIDs 35277659, 39805917) and a small molecule (PMIDs 39781890,
> 39713389).

Four separate problems: metastasis was not measured in 35277659; the antibody result is
significant only after a post-hoc exclusion; BHQ880 is not close to DKN-01; and 39781890 and
39713389 are one paper. **Proposed replacement:**

> **Mouse evidence:** three modalities of DKK1 blockade have been tested in mouse osteosarcoma,
> from two laboratories. A different anti-DKK1 antibody, BHQ880 (Novartis, IgG1; DKN-01 is an
> IgG4), slowed growth of two patient-derived xenografts implanted orthotopically and amputated,
> and reduced metastasis — 6 of 18 control versus 4 of 27 treated mice, which was not significant
> as randomised (P = 0.17) and reached P = 0.03 only after excluding three treated mice with
> local recurrence (PMID 27049730). A vivo morpholino against Dkk-1 reduced lung metastasis in
> the same patient-derived model, 7 of 9 control versus 2 of 10 treated lungs positive for human
> GAPDH, and preserved bone (PMID 39805917); an earlier paper from that lab preserved bone in a
> Dkk-1-overexpressing mouse line but could not detect lung metastases at all, so it does not
> support a metastasis claim (PMID 35277659). A small-molecule DKK1 inhibitor, WAY262611, reduced
> metastasis in the antibody lab's own model (PMID 39781890; PMID 39713389 is its preprint, not a
> separate study) — we have read only its abstract. Separately, an independent Chinese group
> reported that an oral compound that lowers DKK1 reduced lung metastasis and bone destruction in
> an orthotopic intratibial model against a methotrexate comparator (PMID 39280613).

**2. Line 26. Currently:**

> **What neither target has:** any dog data, any test of the actual clinical drug in
> osteosarcoma, or a trial.

This is false for FAK. **Proposed replacement:**

> **What neither target has:** any canine osteosarcoma expression data — no study has measured
> FAK, pFAK or DKK1 in dog tumours — and no registered human osteosarcoma trial. For FAK this is
> no longer a blank sheet: Colorado State University's Animal Cancer Center has a canine trial
> adding oral defactinib to the established losartan-toceranib regimen in dogs with lung-
> metastatic osteosarcoma, including canine pharmacokinetic sampling. We have not been able to
> confirm its enrolment status or see results, and that is the first thing to ask. DKN-01 has
> never been given to a dog, and neither drug has been tested in any published osteosarcoma
> model — the mouse FAK data use PF562271, and the mouse DKK1 antibody data use BHQ880.

**3. Line 24, the DKK1 caution. Currently:**

> **Caution:** the work comes largely from one research lineage, a few papers report the opposite
> direction, and two of 28 papers since 2010 are retracted. Independent replication is the
> priority.

"One research lineage" is wrong in one direction and the paper count is inflated in another;
and the independent support from 39280613 is missing. **Proposed replacement:**

> **Caution:** the decisive in vivo work comes from two laboratories (Loeb, Johns Hopkins then
> Albert Einstein; Gregory, Texas A&M), and they are less independent than they look — the
> antibody and small-molecule results are the same lab, and the morpholino lab deliberately used
> the antibody lab's patient-derived xenograft so the results could be compared. One group
> outside both reports the same direction with an oral compound (PMID 39280613), which is the
> most useful independent signal so far. Against the rationale, an older paper found that raising
> Dkk-1 and suppressing Wnt inhibits osteosarcoma growth, with the epistasis pointing the wrong
> way for blockade (PMID 24859848). Two of 28 papers since 2010 are retracted. Independent
> replication, in a model neither lab owns, is the priority.

**4. Line 14, FAK mouse evidence. Currently:**

> **Mouse evidence:** a clinical-stage FAK inhibitor given by mouth reduced osteosarcoma
> xenograft growth and blood-vessel formation (PMID 28406574).

True but it reads as stronger than it is, and the missing metastasis endpoint matters because
metastasis is the brief's whole endpoint. **Proposed replacement:**

> **Mouse evidence:** PF562271, an oral FAK inhibitor, halved tumour volume and weight and
> reduced microvessel density in subcutaneous 143B xenografts (50 mg/kg twice daily, n = 6 per
> group, PMID 28406574). Metastasis was not measured, the model was subcutaneous rather than
> orthotopic, and sensitivity did not track pFAK level across six cell lines — so this supports
> FAK as a growth target, not yet as an anti-metastatic one. The agent is also not defactinib.

**5. Line 15, the chemotherapy-response panel. Currently:**

> and a FAK-pathway panel separated chemotherapy responders from non-responders (PMID 23845472).

The full text was unreachable, so the AUC cannot be checked for over-fitting on 36 biopsies.
**Proposed replacement:**

> and a three-protein panel (beta5 integrin, FAK, GSK3beta) separated good from poor
> chemotherapy responders in 36 pre-treatment biopsies (PMID 23845472) — a single small series,
> and we could not obtain the full text to check whether the reported accuracy was validated on
> an independent set.

**6. Optional addition to line 15, on where the prognostic signal lives.** PMID 28846700's
pFAK-Y397 result was not significant across all 53 patients; it was significant only in the
33-patient metastatic subgroup (HR 2.32, P = 0.048; multivariate HR 2.60, P = 0.034). If the
brief wants to use pFAK as the FAK arm's enrichment marker, that is worth stating, since the
proposed dog population is post-amputation, i.e. the pre-metastatic setting where this marker
was *not* prognostic.

**7. Line 42, endpoints.** "plus activated FAK or serum DKK1 measured at baseline and during
treatment, to define who benefits" — serum DKK1 is better supported than the brief implies
(27049730 tracked it in mice, it fell to undetectable on treatment, and it rose sharply just
before clinical metastasis), but no canine assay or threshold exists. Worth one clause saying the
canine assay has to be built first.

**8. Line 54 caveat.** "Mouse results were often from single laboratories" can now be made
specific rather than hedged: for DKK1 the decisive results are two labs sharing one model.

### Overall

**The FAK case got weaker on the science and stronger on the practicalities.** Weaker because
its only in vivo efficacy paper never measured metastasis, used one cell line subcutaneously at
one dose with n=6, showed no relationship between pFAK level and drug sensitivity, and killed
endothelial cells at lower concentrations than tumour cells; and because its biomarker's
prognostic value sits in a 33-patient subgroup at P values just under 0.05. Stronger because
defactinib has already been dosed orally in dogs with metastatic osteosarcoma with PK sampling,
at a veterinary centre that NIH already funds for FAK work — which removes the drug-availability
and tolerability unknowns that the brief lists as a caveat, and turns "would you do this?" into
"what happened in the study you already ran?".

**The DKK1 case is roughly where it was, but for different reasons than the brief gives.** It
lost the "three independent ways" framing — one modality never measured metastasis, the antibody
paper's headline statistic depends on a post-hoc exclusion, the small-molecule paper is one
paper counted twice and its full text is unreadable from here, and the two labs share a model.
It gained a genuinely independent in vivo confirmation with an oral agent and an active
comparator (39280613), and the strongest single metastasis result in the whole set (39805917,
7/9 vs 2/10) survived full-text reading intact. The direction of the Wnt mechanism is now
consistent across three groups, with one real dissenter (24859848).

**For the brief's purpose, the ordering changes.** FAK is now the target with a dog already on
the drug and no anti-metastatic mouse data; DKK1 is the target with anti-metastatic mouse data
in the exact implant-amputate-watch design the dog study would copy, and no dog has ever
received the drug. That is a cleaner, more honest pitch than "two targets, neither has dog data",
and it gives each of the three questions at the end of the brief a sharper form: for FAK, ask CSU
what their defactinib study showed; for DKK1, ask Leap Therapeutics whether sirexatamab can be
supplied for a canine study, and ask whether anyone will run the independent replication.
