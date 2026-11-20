# Protein-level check of the surface-target leads (leads 5 and 6; lead 5 before the November 20, 2026 split)

*Working notes, November 19, 2026. Question: are the RNA-ranked leads in
`reports/New surface targets for osteosarcoma.md` (LRRC15, IFITM5, ADAM12, PTK7, plus MRC2, CD248,
CD109 for context) actually present as protein in osteosarcoma, and absent from vital normal
tissue? Labels as in the reports: (registry), (paper, full text), (paper, abstract only),
(press release only), (our calculation).*

## Sources used, and how

| Source | What | How |
|---|---|---|
| Human Protein Atlas v26 | Normal-tissue IHC by cell type, cancer-atlas IHC counts, antibody reliability, RNA-consistency grade, blood MS concentration | `https://www.proteinatlas.org/{ENSG}.json` (summary) and `/{ENSG}.xml` (per-antibody IHC); parsed with a throwaway script in the session scratchpad |
| PubMed E-utilities | Abstracts | `esearch` + `efetch rettype=abstract` |
| Europe PMC REST | Full text of open-access papers | `/{PMCID}/fullTextXML` |
| ClinicalTrials.gov API v2 | Trial status | `/studies/{NCT}` and `/studies?query.term=` |
| Web search | Company news for SOT106, ZL-6201, LNTH-2403 | Search-engine summaries only. Company and trade-press pages (sotio.com PDFs, oncologypro.esmo.org, targetedonc.com) were blocked by this environment's proxy, so **nothing from them was read directly** |

**HPA has no sarcoma in its cancer atlas.** Its 20 cancer types are carcinomas, glioma, lymphoma,
melanoma and testis cancer, so HPA cannot answer "is it in osteosarcoma". It can only tell us
about normal tissue.

## 1. Human Protein Atlas, normal tissue (registry)

| Gene | HPA tissue IHC? | Reliability (IHC / IF) | What the IHC shows in normal tissue | Blood level by mass spec |
|---|---|---|---|---|
| LRRC15 | **No IHC in the tissue atlas** (antibody HPA035503 used for IF only) | none / Approved | Not assessed. HPA's mass-spec tissue proteome calls it "tissue enriched" in skin | 0.64 µg/L |
| IFITM5 | **No IHC in the tissue atlas** (HPA039258, IF only) | none / Supported | Not assessed. Mass-spec tissue proteome: not detected | not listed |
| ADAM12 | Yes, 3 antibodies | Enhanced / Supported | The three antibodies **disagree**. HPA030866: strong in placenta trophoblast, medium in bone-marrow haematopoietic cells and testis, little else. HPA030868: strong in chondrocytes and late spermatids, medium in adrenal and placenta. HPA030867: **high in cerebral cortex and hippocampus (glia and neurons), caudate glia, cerebellar granular layer, colon/duodenum/small-intestine/rectum/appendix glands and kidney glomeruli**, medium in liver hepatocytes and skeletal muscle. All three: "medium consistency with RNA" | 14 µg/L (secreted form exists) |
| PTK7 | Yes, 1 antibody (HPA003222) | Approved / Supported | "Most normal tissues showed weak to moderate cytoplasmic positivity"; strong in basal oesophageal squamous cells; high in endometrial stroma; medium in kidney tubules, pancreas, stomach, brain neurons (caudate, hippocampus, Purkinje), fibroblasts. **"Low consistency between antibody staining and RNA"** | 5.6 µg/L ("secreted to blood") |
| MRC2 | Yes (HPA041991) | Enhanced / none | Strong in monocyte-derived, endothelial and stromal cells, fibroblasts (soft tissue high), endometrial stroma; medium in lung type II cells and macrophages, glomeruli | 24 µg/L |
| CD248 | Yes (HPA051856) | Enhanced / Approved | Strong in exocrine pancreas subset, Paneth cells, skin fibrohistiocytic cells; **medium in cardiomyocytes**, glomeruli, fibroblasts | 12 µg/L |
| CD109 | Yes (HPA015723) | Enhanced / Approved | Strong only in hair-follicle outer root sheath and parathyroid; "remaining normal tissues essentially negative"; **high consistency with RNA** | 130 µg/L |
| CD276 (B7-H3), comparison | Yes, 3 antibodies | Enhanced / Approved | Weak to moderate in most tissues, strong in prostate, adrenal, hepatocytes, islets (HPA017139) | 3.7 µg/L |

What this means:
- For the two top leads, **HPA gives no normal-tissue protein map at all.** The screen's "HPA
  protein evidence: IHC n/a" for LRRC15 and IFITM5 is correct, and it is a real gap, not a
  formatting issue.
- ADAM12's `Enhanced` IHC grade, which the surface report cites as a strength, comes from three
  antibodies whose staining patterns do not agree, and one of them stains brain, gut and kidney
  strongly. We cannot tell from HPA which antibody is right. Treat the grade as uninformative.
- PTK7's HPA IHC is broad and cytoplasmic and HPA itself rates it low-consistency with RNA, so the
  normal-tissue picture for PTK7 is uncertain in both directions.
- B7-H3, which is in a positive phase 3 trial (below), also stains most normal tissues weakly to
  moderately in HPA. Broad weak normal staining therefore does not by itself rule a target out.
- CD109 is the only candidate whose HPA normal-tissue IHC is both clean and RNA-consistent.

## 2. LRRC15: published protein data

**In osteosarcoma tissue**
- **Cui et al., J Orthop Res 2020 (PMID 32902907; paper, abstract only).** Tissue microarray of 69
  osteosarcomas: 63/69 (91.3%) stained; 0 in 6 (8.7%), 1+ in 12 (17.4%), 2+ in 25 (36.2%), 3+ in
  26 (37.7%). So 51/69 (74%) were 2+ or 3+ (our calculation). Higher LRRC15 went with more
  metastasis, chemoresistance and shorter 5-year survival. Antibody, cut-offs and primary vs
  metastasis split not given in the abstract.
- **O'Reilly et al., Clin Cancer Res 2026 (PMID 41627173, PMC13080327; paper, full text).** St. Jude
  TMA of archived **paediatric primary** resections, antibody Abcam EPR8188(2), automated H-score:
  n = 18, **median H-score 113.5, range 0–236**; "a majority" above H-score 100, the threshold St.
  Jude uses for solid-tumour CAR-T eligibility. No metastasis or relapse samples. In normal mouse
  tissue, Lrrc15 RNA (in-situ hybridisation; no antibody validated for mouse protein) was limited to
  **hair follicles, bone-marrow mesenchymal stem cells and osteoblasts**; none in brain, heart, lung,
  liver or kidney. Mouse-and-human cross-reactive LRRC15 CAR-T cells caused no detectable toxicity
  in immunocompetent mice. Antigen-loss variants appeared in tumours that escaped two of the three
  CAR designs.
- **Moquin-Beaudry et al., Nat Commun 2026 (PMID 42399228, PMC13470005; paper, full text).** Spatial
  transcriptomics of 9 primary tumours and 17 metastatic or local relapses from 19 patients. LRRC15
  is one of 18 genes enriched in cancer regions across all samples and one of a 9-gene
  osteosarcoma-specific surface signature that held its score **at relapse** (MAPPYACTS cohort) as
  well as at diagnosis (OS2006). LRRC15 was among six signature genes checked by IHC (Cell
  Signaling E4X8J); "protein expression closely matched mRNA expression for most targets", but the
  authors stress that signature proteins sit in **different tumour compartments** and "no single
  target is uniformly expressed throughout the tumor". No per-gene positivity rates in the text.
- **Mooney et al., Cell Rep 2026 (PMID 42647168, PMC13671662; paper, full text).** Mass-spec
  surfaceome and global proteome of **22 osteosarcoma PDXs**. LRRC15 was enriched by both methods
  and "among the top hits"; their own top-ranked new candidates were SGCD, ROR2 and TMEM119.
- **Hingorani et al., Mol Cancer Ther 2021 (PMID 33298592; paper, abstract only).** 7 PDXs; IHC in 3;
  ABBV-085 slowed 6 of 7 and response tracked LRRC15 RNA.
- **Purcell et al., Cancer Res 2018 (PMID 29764866; paper, abstract only).** LRRC15 is on cancer-
  associated fibroblasts in many carcinomas and directly on cancer cells of mesenchymal origin
  including sarcoma; induced by TGF-β.

**Toxicity seen with LRRC15 drugs in people**
- **ABBV-085 (samrotamab vedotin), NCT02565758 (registry: completed 2019, no results posted);
  Demetri et al., Clin Cancer Res 2021 (PMID 33820780; paper, abstract only).** 85 patients;
  3.6 mg/kg every 14 days was "safe and tolerable"; commonest treatment-related events fatigue,
  nausea, decreased appetite. **ORR 20% (4 confirmed partial responses) in 20 patients with
  osteosarcoma or UPS** (10 each) at 3.6 mg/kg; no monotherapy responses in other cancers. The
  abstract does not split responses between osteosarcoma and UPS, and does not mention bone,
  skin or marrow toxicity. O'Reilly et al. summarise its side effects as "mainly attributed to the
  ADC chemotherapeutic payload" (paper, full text).
- **[177Lu]Lu-DUNP19 = LNTH-2403.** Storey et al., Signal Transduct Target Ther 2025 (PMID 41022704,
  PMC12480655; paper, abstract only for data): humanised antibody, rapidly internalised, imaging
  and radiotherapy in xenografts "with minimal toxicity". Their competing-interest statement says
  the compound "(LNTH2403) is currently undergoing preclinical evaluation for potential
  first-in-human use in osteosarcoma" and that the work was supported by Lantheus. No human data.

**Open questions the literature does not answer**
1. Protein level in **lung metastases and relapses**, measured as positivity rates. The spatial
   paper shows the RNA signature persists at relapse; nobody has published LRRC15 IHC rates in
   paired primary/metastasis tissue that we could find.
2. Protein in **human osteoblasts and growth plate**. Mouse RNA says osteoblasts and marrow MSCs
   express it. For a lutetium-177 antibody that matters more than for a CAR, because radiation dose
   to marrow and bone surfaces would be the expected limit (our inference, not reported anywhere).
3. Heterogeneity: CAR escape variants in mice and compartmentalised staining in patients both
   suggest LRRC15-low cells will exist in many tumours.

**LRRC15 trial status, ClinicalTrials.gov API v2, checked November 19, 2026 (registry)**

| NCT | Agent / sponsor | Population | Status | Dates | Notes |
|---|---|---|---|---|---|
| NCT07357519 (Lu-TARGO) | LNTH-2403, Lantheus | Relapsed/refractory osteosarcoma, ≥12 y (first cohort ≥18 y) | Recruiting | Start 2026-02-03; primary completion est. 2027-08; last update 2026-05-01 | 55 planned, 2 US sites; bone-only disease allowed if FDG-PET avid |
| NCT07374848 | ZL-6201 ADC, Zai Lab | Sarcoma and selected solid tumours, ≥18 y; sarcoma ≤2 prior metastatic lines | Recruiting | Start 2026-03-02; last update 2026-11-18 | 180 planned, 12 sites, China and US; biopsy or archived tissue required |
| NCT07801222 | SOT106 ADC, SOTIO | LRRC15-positive osteosarcoma or soft-tissue sarcoma, ≥12 y | Not yet recruiting | Planned start 2026-09-30, not updated since 2026-09-03 | 70 planned; 1 listed site (Moldova) |
| NCT07272642 | LNTH-2403 imaging, Radiopharm Theranostics | CRC, HNSCC, NSCLC, TNBC, ≥18 y | Not yet recruiting | Planned start 2026-10-30; last update 2026-08-12 | **The record now names the agent "LNTH-2403 (177Lu-DOTA-DUNP19)"**, so it is the same antibody as Lu-TARGO. The surface report and ranked-leads report still say "NTH-2403 … could not confirm" |
| NCT07651020 | LRRC15 SPECT imaging agent, Union Hospital Wuhan | Several cancers incl. sarcoma | Completed, **1 patient enrolled** | First posted 2026-06-16 | Not in the repo's LRRC15 list; trivial |
| NCT02565758 | ABBV-085, AbbVie | Solid tumours incl. UPS | Completed 2019 | No results posted | Published (above) |

Posted or presented results: none on ClinicalTrials.gov for any current LRRC15 trial. A search
found Zai Lab's AACR 2026 **preclinical** poster for ZL-6201 (abstract 4331) and SOTIO posters at
ESMO Sarcoma 2025 and CTOS 2025, plus FDA orphan-drug and fast-track designations for SOT106 in
osteosarcoma/soft-tissue sarcoma reported in trade press (press release only; **seen only as
search-engine summaries**; the pages were blocked here). The search summary of the SOTIO poster
said 77% of adult and 59% of paediatric osteosarcomas had ≥10% LRRC15-positive cells. **We did not
read the poster, so this number must not be quoted** until someone opens it.

## 3. PTK7

**In osteosarcoma**
- **Lee et al., Cell Rep Med 2023 (PMID 37343516, PMC10314120; paper, full text).** A neuroblastoma
  paper. Two osteosarcoma PDXs from the authors' lab, **one from a relapse (OSx-2r)**, stained
  PTK7-positive by IHC; 143B and MG-63 cell lines expressed it by Western blot; PTK7 CAR-T cells
  killed osteosarcoma cells in a 4-hour assay. A purpose-built **paediatric normal-tissue TMA** was
  negative or weak (score 1 against 3+ colon cancer control) in every organ; lung, liver, brain,
  adrenal, endometrium, testis, prostate, ovary, cervix and oesophagus were 0. Blood: lymphocytes
  and monocytes negative by flow; neutrophils slightly positive.
- **Mooney et al. 2026 (full text).** Names PTK7 among "less characterized proteins" highlighted by
  their PDX surfaceome ranking (their Figure 3D). No IHC.
- **No series of patient osteosarcomas stained for PTK7 was found** in PubMed (9 hits for PTK7 and
  osteosarcoma or sarcoma; none is an osteosarcoma IHC study) or Europe PMC.
- Adult soft-tissue sarcoma: Bertucci et al., ESMO Open 2025 (PMID 41046759; paper, abstract only):
  PTK7 RNA overexpressed in 81% of 476 liposarcomas; IHC confirmed four ADC targets, which ones not
  stated in the abstract. No osteosarcoma.

**Toxicity of PTK7 drugs in people**
- **Cofetuzumab pelidotin (PF-06647020, auristatin), Maitland et al., Clin Cancer Res 2021
  (PMID 34083232; paper, abstract only).** Commonest related events nausea, alopecia, fatigue,
  headache, neutropenia, vomiting (25–45%); grade ≥3 neutropenia 25%; DLTs grade 3 headache and
  fatigue; RP2D 2.8 mg/kg every 3 weeks; ORR 27% ovarian, 19% NSCLC, 21% TNBC; responders tended to
  have moderate or high PTK7 IHC.
- **Phase 1b in PTK7-expressing NSCLC (Cho et al., Lung Cancer 2025, PMID 40086026; paper, abstract
  only).** Alopecia 52%, neutrophil decrease 43%, grade ≥3 events 69%, grade ≥3 neutropenia 25%,
  no fatal related events; ORR 18%; PTK7 cut-off ≥90% of tumour cells at ≥2+. The registry entry
  NCT04189614 was **terminated for "strategic considerations"**, primary completion 2026-05-07
  (registry).
- With gedatolisib in TNBC (PMID 35551360; abstract only): 18 patients, ORR 16.7%, myelosuppression
  uncommon.
- None of these abstracts reports an organ toxicity that points to on-target damage in a PTK7-rich
  normal tissue; the pattern reads as auristatin payload toxicity (our interpretation).

**PTK7 programmes (registry, November 19, 2026)**: HWK-007 (NCT07444814), KIVU-107 (NCT07229313)
and DAY301 (NCT06752681) all recruiting, adults only. Two not in the surface report:
**IDE034 (IDEAYA, NCT07503808)**, a B7-H3 × PTK7 bispecific ADC in carcinomas, recruiting since
2026-02-24; and **LY4175408 (Lilly, NCT07046923)**, active not recruiting; its exclusion criteria
bar prior "PTK7 ADC with a topoisomerase I inhibitor payload", which suggests (our inference, not
stated) that it is one. None lists osteosarcoma.

## 4. IFITM5

- HPA: no tissue IHC, IF only (above). Mass-spec tissue proteome: not detected, which fits a
  bone-restricted protein in an atlas without bone (registry).
- PubMed: 8 papers on IFITM5 and osteosarcoma; all are case reports of osteosarcoma in
  IFITM5-variant osteogenesis imperfecta, transcriptomics, or one 2017 cell-line overexpression
  study (PMID 28123530). **No published IHC or flow measurement of IFITM5 protein in osteosarcoma
  tissue was found.**
- Moquin-Beaudry 2026 (full text): IFITM5 is in the 9-gene osteosarcoma surface signature, present
  at diagnosis and relapse by RNA, and low in all GTEx tissues "notably in the lungs". It was **not**
  among the six genes they could stain, because they validated IHC only "when validated
  IHC-compatible antibodies could be obtained".
- Tanaka et al., bioRxiv 2026 (doi 10.64898/2026.06.10.731352; preprint, abstract only, checked via
  the bioRxiv API): single-nucleus RNA from 24 tumours. The osteoblastic cell state predominated in
  primaries but was **dampened in metastases and in post-treatment tumours**. IFITM5 is an
  osteoblast gene, so this is a reason to expect lower IFITM5 in exactly the lesions a drug would
  treat (our inference; the preprint does not name IFITM5).
- Visser et al., bioRxiv 2026 (preprint, abstract only): osteoblastic-like, chondroblastic-like and
  fibroblastic-like tumour-cell states with "variable expression" of immunotherapy targets across
  states.

## 5. ADAM12

- HPA: discordant antibodies (above); cancer atlas "essentially negative" across 20 carcinoma types
  with all three antibodies; blood MS 14 µg/L.
- PubMed: 4 papers on ADAM12 and osteosarcoma or sarcoma; the only osteosarcoma study is a mouse
  model (Georges et al., Eur J Cancer 2013, PMID 23490646; abstract only) showing ADAM12 promotes
  tumour growth and osteolysis. **No human osteosarcoma IHC found.**
- Not among the PDX surface proteins named in Mooney 2026's text.

## 6. Context: other surface proteins with new protein data (all 2025–26)

- **Mooney 2026 (full text):** 31 surface proteins enriched in osteosarcoma PDXs by both mass-spec
  methods. Named in the text: MRC2, CADM1, CD109, MMP14, ALPL, EPHA3, EPHB2, EPHB3, GPC4, SMPD3,
  EMP3, ROR2, TMEM119. Five of those (MRC2, CD109, EPHB2, EPHA3, EMP3) are in our RNA top-25
  shortlist (ranks 4, 7, 8, 14, 21), which is independent support at the protein level (our
  calculation from the two lists).
  - **TMEM119:** ranked 4/190 by them; "robust staining" with "distinct surface staining" on a COG
    osteosarcoma TMA; limited staining in 21 of 22 normal paediatric tissues (tonsil the
    exception). In our screen TMEM119 ranks **5th overall** (565 TPM, 98.9% of tumours) but is
    excluded from the shortlist because HPA gives it only low surface confidence (our
    calculation, `data/osteosarcoma_surface_target_candidates.csv`). The protein data say that
    filter call was wrong for TMEM119.
  - **ROR2:** ranked 2/190; "virtually no expression" in 25 normal paediatric tissues by IHC; strong
    in osteosarcoma; ROR2 ADCs with PBD or PNU payloads killed PDX-derived cells in vitro. In our
    screen ROR2 is shortlist rank 55 (38 TPM, 97.7%), held back by 50 TPM in GTEx sigmoid colon
    (our calculation). Ozuriftamab vedotin (BioAtla) has adult trials (NCT03504488 completed;
    NCT05271604 completed) (registry).
  - **CADM1:** Wang et al., Mol Cancer Ther 2026 (PMID 41517891; abstract only): a CADM1-tesirine
    ADC shrank all six CADM1-expressing osteosarcoma PDXs, with 3 complete responses. CADM1 is
    shortlist rank 30 in our screen.
  - Both Mooney 2026 and the LRRC15 PNU work report that **MMAE is a poor payload for
    osteosarcoma** cells relative to PNU-159682 or PBD. ABBV-085 and SOT106 both carry MMAE
    (SOT106 per search summary only).
- **Meflin (ISLR):** Esaki et al., Oncogene 2025 (PMID 41120731; abstract only): high in tumour cells
  of progressive/recurrent osteosarcoma and doxorubicin-resistant cells; an MMAE ADC worked in mice
  without obvious toxicity.
- **B7-H3:** ARTEMIS-011 (see the "What's new" notes) is the first randomised proof that an
  antigen-directed drug beats chemotherapy in relapsed osteosarcoma.
- **HER2:** PEPN1924 (PMID 42131734, PMC13166107; paper, abstract read): 41 of 50 screened relapsed
  osteosarcomas met the IHC criterion (>10% of cells, any intensity, membranous or cytoplasmic), yet
  only 1 of 9 treated patients had stable disease beyond 24 weeks. So "positive by IHC" at a lenient
  cut-off did not predict benefit, which is a caution for any IHC-based go/no-go on new targets.

## 7. Verdicts

| Target | Protein in osteosarcoma | Absent from vital normal tissue? | Verdict | Cheapest next experiment |
|---|---|---|---|---|
| **LRRC15** | Yes: 63/69 tumours stained, 74% at 2+/3+ (abstract only); 18 paediatric primaries median H-score 113.5 (full text); proteomics top hit in 22 PDXs (full text); IHC in a spatial cohort including relapses (full text, no rates) | Probably, for vital organs: mouse RNA ISH negative in brain, heart, lung, liver, kidney; GTEx low. Not shown for human osteoblasts, growth plate or marrow MSCs. No HPA IHC. ABBV-085 in 85 adults had payload-type toxicity only (abstract only) | **Strong** in primaries; **partial** for metastases/relapse and for normal bone | Stain a TMA of **paired primary, lung metastasis and relapse** tissue plus **paediatric growth plate and marrow** with the EPR8188(2) clone, scoring H-score and % positive cells. Before that, ask Lantheus and SOTIO whether they will publish their screening IHC (SOT106 requires LRRC15-positive tumours, so SOTIO must have an assay and data) |
| **PTK7** | Partial: 2 PDXs (1 relapse) and 2 cell lines positive (full text); PDX proteomics names it (full text). **No patient tumour series** | Paediatric normal TMA negative or 1+ in all organs (full text) vs adult HPA weak–moderate in most tissues with low RNA consistency; human ADC toxicity looks payload-driven (abstract only); PTK7 is shed (HPA "secreted to blood") | **Partial** | Stain an osteosarcoma TMA with the clinical-trial PTK7 IHC assay and cut-off (≥90% of cells ≥2+, as in the NSCLC trial). Ask Kivu whether any sarcoma patient has entered KIVU-107 |
| **IFITM5** | **Absent** (no measurement exists): RNA only; one group could not get a validated IHC antibody | Unknown: no HPA tissue IHC; bone is not in GTEx or HPA; biology says osteoblasts express it | **Absent** | No antibody is ready, so use **RNA in-situ hybridisation** (RNAscope) for IFITM5 on an osteosarcoma TMA with metastases, plus paediatric growth plate and remodelling bone. In parallel, test 2–3 commercial antibodies against IFITM5-knockout or -overexpressing osteosarcoma cells |
| **ADAM12** | **Absent** in human tumours (mouse model only) | Unclear: three HPA antibodies disagree, one stains brain, gut and kidney strongly; a shed form circulates (14 µg/L) | **Absent** | Stain an osteosarcoma TMA with two of the HPA antibodies side by side; measure serum ADAM12 in a few patients to size the antibody "sink" |
| MRC2 (context) | Yes: enriched in PDX surfaceome by both methods (full text) | No: strong in fibroblasts, endothelium, macrophages (HPA) | Partial | Same TMA, with normal-fibroblast-rich tissue alongside |
| CD109 (context) | Yes: PDX surfaceome, both methods (full text) | Mostly: HPA clean except hair follicle and parathyroid, high RNA consistency | Partial, cleanest normal-tissue profile of the set | Same TMA |
| TMEM119 (not in shortlist) | Yes: surface IHC on a COG TMA (full text) | Mostly: 21/22 normal paediatric tissues limited (full text) | **Strong-ish; currently filtered out of our list** | Re-run the screen with TMEM119 admitted, and ask the BC Cancer group for per-sample scores |

**Overall:** LRRC15 is the only one of the four leads with protein evidence in patient tumours, and
it is now supported by three independent 2026 data sets. PTK7 is plausible but untested in patient
tissue. IFITM5 and ADAM12 have no human osteosarcoma protein data at all, so their RNA ranks should
not be read as target validation.

One tissue microarray could answer most of this at once: osteosarcoma primaries, paired lung
metastases and relapses, plus paediatric normal bone/growth plate, stained for LRRC15, PTK7,
TMEM119 and CD109, with IFITM5 by RNA in-situ hybridisation. COG's osteosarcoma TMA (used by
Mooney 2026) and the St. Jude TMA (O'Reilly 2026) already exist.

## 8. What should change in existing reports (not edited here)

- `reports/New surface targets for osteosarcoma.md` and `reports/Ranked leads and research partners.md`:
  NCT07272642's record now names **LNTH-2403 (177Lu-DOTA-DUNP19)**, so "NTH-2403 … same antibody, not
  confirmed" can be resolved: it is the same agent (registry; also Storey 2025 COI statement).
- Surface report: add the protein evidence for LRRC15 (Cui 2020, O'Reilly 2026, Moquin-Beaudry 2026,
  Mooney 2026); say plainly that IFITM5 and ADAM12 have no human protein data; note the discordant
  ADAM12 antibodies behind its "Enhanced" grade.
- Surface report: TMEM119's exclusion by the HPA surface filter is contradicted by surface IHC in
  Mooney 2026; ROR2 has protein-level normal-tissue data better than its GTEx-based rank suggests.
- Surface report: two PTK7 programmes are missing (IDE034, NCT07503808; LY4175408, NCT07046923) and
  cofetuzumab's NCT04189614 is terminated.
- Surface report: "the osteosarcoma literature has only 6 papers naming LRRC15" is now out of date
  (PubMed returns 11 for "LRRC15 AND osteosarcoma" on November 19, 2026, 7 of them from 2025–26;
  registry).
