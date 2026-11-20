# Repurposing screen: working notes

*Started November 19, 2026. Working notes behind `reports/Approved drugs worth testing in osteosarcoma.md`. Script: `tools/repurposing_screen.py`. Output: `data/osteosarcoma_repurposing_candidates.csv`. Raw pulls cached (git-ignored) in `data/repurposing_raw/`.*

Every candidate below is a hypothesis for laboratory testing, not a treatment recommendation, and nothing here is medical advice.

## 1. Data pulled

- **ChEMBL REST API**, November 19, 2026: 4,225 molecule records with max_phase 4 and 1,892 with max_phase 3 (salts and parents counted separately), and all 7,561 mechanism-of-action records, with the 1,518 targets they name (registry). Raw JSON: `chembl_molecules_phase4.json`, `chembl_molecules_phase3.json`, `chembl_mechanisms.json`, `chembl_targets.json`.
- Kept: mechanisms with max_phase 3 or 4 acting on a human protein target. Dropped: vaccines, replacement enzymes, collagen- or clot-digesting enzymes, fusion-protein targets (ChEMBL lists repotrectinib against "CD74-ROS1", which would credit CD74), and imaging agents.
- **Caveat found while building**: ChEMBL's `therapeutic_flag` is False for every phase 3 molecule, so it can only be used to remove diagnostics among approved drugs. ChEMBL also lags recent approvals: defactinib still reads max_phase 3 although the FDA granted accelerated approval on May 8, 2025 (registry).
- Mutant-selective drugs (a mechanism with a variant sequence, or sotorasib/adagrasib/ivosidenib/vorasidenib-type names) are not credited to the wild-type gene. Osteosarcoma rarely carries those mutations.

## 2. Joins

- **Tumour RNA**: `data/surface_targets_raw/tumour_summary.json` (TARGET-OS, 88 tumour RNA-seq files from GDC, STAR `tpm_unstranded`, protein-coding genes; built by `tools/surface_targets.py gdc`). "Expressing" = TPM >= 5 in that tumour, the same floor as the surface-target screen. Bulk RNA includes stroma and immune cells, which matters for CXCR4, CSF1R and CD4 below.
- **GTEx**: only cached for the ~2,400 surface genes in `data/surface_targets_raw/gtex_medians.json`, so the GTEx columns are blank for most genes.
- **Literature**: `data/osteosarcoma_gene_evidence.csv` (papers, in vivo, patients, dog, % cell-line-only or microRNA-type, retractions, NIH grants), `data/osteosarcoma_evidence_risk_genes.csv` (risk flag).
- **Drug literature**: PubMed count of `osteosarcoma[tiab] AND "<drug>"[tiab]` for every phase 3-4 drug with a human target (salt words stripped), and a second count with up to eight non-trade synonyms OR-ed, run November 19, 2026 (`pubmed_drug_counts.json`, `pubmed_drug_counts_syn.json`). Added because gene tagging misses papers that name only the drug: ADRB2 has 7 gene-tagged papers but propranolol has its own small literature; ATP1A1 has none but digoxin/ouabain have some. Endogenous substances (adenosine, estradiol, dopamine ...) get no credit because those papers are almost never about the drug.
- **Trials, local**: every drug name and ChEMBL synonym (5+ characters) looked up as an n-gram in the title + interventions of the 758 trials in `data/osteosarcoma_trials.csv` (interventional and expanded access only), plus the hand-curated map in `data/drug_targets_curated.json`. The 154 matched names are in `data/repurposing_raw/trial_name_matches.json`; I read the list and found no false matches.
- **Trials, ClinicalTrials.gov API v2**: for the top genes (by provisional score, after hand review) the four best drugs per gene were searched with `query.cond=osteosarcoma&query.intr=<drug>`; hits were kept only when the drug name appears in the intervention list or title (the API's fuzzy match otherwise pulls in unrelated drugs). The same call with `filter.advanced=AREA[StdAge]CHILD AND AREA[StudyType]INTERVENTIONAL` gives the number of interventional trials of the drug that enrol children, used as the paediatric-experience proxy.
- openFDA and DailyMed were not reachable from this environment, so label details (age limits, boxed-warning text) are not checked against labels; boxed warnings come from ChEMBL's `black_box_warning` flag.

## 3. What the screen produced (run of November 19, 2026)

- 2,400 drugs (1,693 approved, 707 phase 3 only) acting on 1,141 human genes (our calculation, from ChEMBL).
- 293 of those genes are hit by a drug that appears in at least one osteosarcoma or osteosarcoma-eligible trial in our trial table; 80 genes have a drug against them named in the title of an osteosarcoma or bone-sarcoma trial (untested score 0), 160 in the title of a basket trial (6), 40 only indirectly (10), and 861 never (20) (our calculation).
- Automatic exclusions: 608 genes with no osteosarcoma literature by either route, 80 already named in an osteosarcoma trial, 28 chemotherapy/steroid targets, 25 heavily trialled classes, 3 mutant-only (genes can carry more than one flag).
- **Hand review removed or labelled 156 genes** (`review_note` column). Of the 60 highest raw scores, 23 needed a review note. The raw number 1 was CD4 (ibalizumab, an HIV entry blocker; the "evidence" is papers about CD4+ T cells). The commonest problems: ChEMBL annotation artefacts (luspatercept credited to TGF-beta1, abciximab to alphav integrin, lomitapide to P4HB), drugs that failed phase 3 and are not marketed (edasalonexent, marimastat, obatoclax, odanacatib), classes already trialled under another gene name (PI3K, HDAC, FGFR, CDK, proteasome), and wrong direction (agonists or drugs that switch the pathway on).
- **The screen caught a dead end that ClinicalTrials.gov could not**: IMPDH (mycophenolate) ranked 7th overall with "no trial", but reading the abstracts turned up ESMMO, a Thai phase II trial (TCTR20190701001) published as negative in 2025 (PMID 40938558): 15 patients, most at 3 g/day because higher doses were not tolerated; 40% progression-free at 16 weeks but only 1 patient (6.7%) with stable disease as best response, and the authors call it a negative trial (paper, abstract only). Preclinical basis: PMID 31609477 (143B xenograft growth inhibition 57%, fewer lung nodules after tail-vein injection; paper, abstract only).
- Only **9 genes / 8 drug ideas** come out of the 20-row shortlist as genuine new candidates; the other 11 rows are high scorers shown with a "wrong direction", "dead end" or "weak" verdict so readers can see why they are not worth pursuing. The shortlist is thin because most druggable osteosarcoma biology has already been trialled (VEGFR, mTOR, PI3K, CDK4/6, HDAC, PARP, checkpoint, IGF1R) or is reachable only with drugs that are not marketed.

## 4. Close reading of the top candidates (abstracts, PubMed / Europe PMC, November 19, 2026)

All entries are abstract-only unless stated. Europe PMC pulls are cached in `data/repurposing_raw/abstracts_*.json`.

### 4.1 AKT1/2 -- capivasertib (approved 2023, oral; ChEMBL)
- PPTP, two different AKT inhibitors: MK-2206 prolonged event-free survival in 6 of 6 osteosarcoma xenografts, more consistently than any other panel, with no objective responses (PMID 22102563). GSK690693 likewise increased EFS "most notably in all 6 osteosarcoma models", no objective responses (PMID 20740623). Two drugs, same programme, same signal: osteosarcoma slows but does not shrink.
- Bone Research 2025 (PMID 39994220): AKT stabilises SOX2 protein; MK-2206 plus cisplatin synergistic in a PDX model.
- Kinome profiling of osteosarcoma cell lines points to AKT signalling (PMID 24447333).
- Against: AKT inhibition increased cisplatin-induced apoptosis only in p53 wild-type lines, not p53-null (PMID 25482935), and most osteosarcomas have lost p53 function. Downstream mTOR inhibitors have 21 osteosarcoma trials with largely negative results (literature map), so pathway-level benefit is not new. AKT1's literature is 44% cell-line-only or microRNA-type and carries an "elevated" paper-mill flag (our calculation).
- No osteosarcoma trial of any AKT inhibitor on ClinicalTrials.gov (registry); 2 interventional capivasertib trials enrol children (registry).
- Cheapest next step: free -- check AKT1/AKT2 dependency of osteosarcoma lines in DepMap CRISPR data; then capivasertib + cisplatin or + doxorubicin in an existing PDX panel, with a lung-metastasis endpoint.

### 4.2 CXCR4 -- mavorixafor (approved 2024, oral), plerixafor (approved 2008, injection)
- For: lung tissue is rich in CXCL12. CXCR4 mRNA in 63% of 47 high-grade tumours and inversely related to survival (PMID 15814634); CXCR4 positive in 33% of primaries against 67% of matched lung metastases in 30 patients (PMID 16528367). Blocking peptides reduced lung metastasis in mice: CTCE-9908, 50% fewer gross nodules after tail-vein injection (PMID 18071913) and T134 (PMID 15701832). AMD3100 (plerixafor) plus doxorubicin was synergistic in an orthotopic model (PMID 34080667).
- Against: the effect of CTCE-9908 "could only be consistently reproduced when the cells were pre-treated" (PMID 18071913). Forcing CXCL12 retention increased primary growth while reducing metastasis -- a "dual role" (PMID 27300512, paper, abstract only). CXCL12 in the tumour draws CD8 T cells in, and CXCL12-CXCR4 blockade abolished the anti-metastatic effect of DNMT1 inhibition in immunocompetent mice (PMID 29735547). CXCR7 takes over invasion when CXCR4 is blocked in a bone-marrow co-culture (PMID 28468584). Bulk RNA cannot separate tumour CXCR4 from immune-cell CXCR4.
- Trials: plerixafor appears only for stem-cell mobilisation in NCT03612466 (registry). The lung-metastasis report already lists CXCR4 as "the most ready drug with the least settled biology"; this screen agrees.
- Cheapest next step: mavorixafor (oral, so dosing in drinking water or gavage is easy) given after primary-tumour removal in an immunocompetent spontaneous-metastasis model (K7M2 in BALB/c), with lung metastasis and tumour CD8 T-cell counts as endpoints -- the T-cell question decides whether this helps or harms.

### 4.3 HIF-2alpha -- belzutifan (approved 2021, oral, boxed warning)
- The score is driven by RNA (median 68 TPM, every tumour) and druggability, not evidence: 17 gene-tagged papers, 7 with animal data (our calculation), none testing belzutifan or any HIF-2 inhibitor (PubMed search: 0 papers).
- What exists points both ways: HIF-2alpha reported downregulated in osteosarcoma lines in a microRNA-type paper (PMID 30966832); HIF inhibition in tumour vessels accelerated osteosarcoma growth in mice (PMID 18300418); HIF-2alpha found as a "latent marker" in a humanised bone model (PMID 30836200).
- Verdict: weak. Cheapest next step is to stain a tissue microarray for HIF-2alpha protein before any drug work; drop it if negative.

### 4.4 ROCK -- belumosudil (approved 2021, oral, age 12+ per our understanding of the label; not checked), fasudil (approved in Japan/China; phase 3 in ChEMBL)
- For: ROCK2 silencing "completely abolished" metastasis of U-2OS cells in NSG mice, and ROCK2/YAP activity was studied in 175 primary tumours (PMID 31878963, Rizzoli group). Fasudil suppressed growth and tumorigenicity of chemoresistant mouse osteosarcoma-initiating cells by forcing adipocyte differentiation (PMID 30992323, Cancer Res 2019). Fasudil reduced vasculogenic mimicry in U2OS in vitro (PMID 28225457).
- Against: in the metastatic LM8 model, the ROCK inhibitor Y-27632 *increased* migration, which depended on Cdc42 rather than ROCK (PMID 20872237). ROCK1's literature carries a high paper-mill flag (our calculation). No study used belumosudil.
- Cheapest next step: belumosudil versus fasudil in a spontaneous lung-metastasis model, including LM8, the model where ROCK inhibition looked harmful.

### 4.5 CSF1R -- pexidartinib (approved 2019, oral, boxed warning for liver injury per ChEMBL flag)
- For: pexidartinib suppressed primary growth and lung metastasis in an orthotopic LM8 model, depleted macrophages and regulatory T cells and increased CD8 T cells (PMID 34088832, MSKCC; the senior author consults for Daiichi Sankyo, the maker). A second group found autocrine CSF1R-CSF1 signalling in a subset of tumours and less metastatic burden with pexidartinib in cell-line and PDX models (PMID 32251854).
- Against, and important: in 53 patients, macrophage-related genes were higher in those who did not develop metastases, and tumour-associated macrophages were associated with better overall survival in two further cohorts (PMID 21372215). That is why mifamurtide, a macrophage activator, is approved in Europe for osteosarcoma. Zoledronate, which also targets macrophages/osteoclasts, trended toward harm in OS2006 (PMID 33498676 and the literature map). Depleting macrophages could therefore be the wrong move in patients even though it works in mice.
- Trials: sunitinib and pazopanib, which hit CSF1R among many kinases, have been trialled; no selective CSF1R drug has (registry).
- Cheapest next step: re-analyse existing patient data (TARGET-OS RNA, which this repository already holds) for macrophage subtype (M1/M2) signatures against outcome before any animal work.

### 4.6 Vitamin D -- calcitriol, calcipotriol, cholecalciferol (approved; oral; huge paediatric experience)
- The gene count is inflated: most of VDR's 106 osteosarcoma papers use osteosarcoma lines as stand-ins for normal osteoblasts (Europe PMC top-cited list, read by hand).
- For: calcipotriol inhibited metastasis and growth in a xenograft metastasis model (PMID 37228489); a single dose of calcitriol shrank a mouse osteosarcoma line in vivo, but caused weight loss and high calcium, and the effect was weaker in human cells (PMID 28643892); vitamin D reduced growth and invasion in vitro (PMID 42598195).
- Patients: in 57 Indonesian patients VDR staining was associated with metastasis (P < 0.001), interpreted as receptor without enough vitamin D (PMID 41872253). In 20 dogs with osteosarcoma, serum 25-hydroxyvitamin D did not differ from matched controls (PMID 27810204).
- Delivery: active vitamin D's dose is capped by hypercalcaemia; a non-calcaemic analogue or simple correction of deficiency are the realistic options.
- Cheapest next step: measure 25-hydroxyvitamin D in banked diagnostic serum from a cooperative-group trial and relate it to metastasis-free survival.

### 4.7 Retinoids -- tretinoin (ATRA; approved, oral, boxed warning), alitretinoin
- For: ATRA reduced pulmonary metastatic nodes in both intravenous and orthotopic K7M2 models by blocking M2 macrophage polarisation (PMID 28515123, Cancer Immunol Res 2017; erratum published 2020, PMID 32015014) and blocked M2-macrophage-driven tumour initiation (PMID 31296953). ATRA inhibited human osteosarcoma growth by driving osteogenic differentiation (PMID 22485251). A 2008 canine report combined ATRA with chemotherapy (PMID 18712486; no abstract available).
- Against: a 29-compound nuclear-receptor screen found that a RARbeta *antagonist* (LE135) inhibited osteosarcoma growth in vitro and in vivo (PMID 36681687), the opposite direction. ATRA resistance has been described (PMID 35810559). Note the macrophage tension with 4.5: ATRA reprogrammes rather than removes macrophages, which fits the patient data better than CSF1R depletion does.
- Paediatric precedent: 142 interventional trials of tretinoin enrol children (registry), mostly acute promyelocytic leukaemia; the related isotretinoin is standard maintenance in high-risk neuroblastoma (general knowledge, not re-checked here).
- Cheapest next step: repeat the K7M2 post-resection metastasis experiment with ATRA in an independent laboratory.

### 4.8 Tissue factor -- tisotumab vedotin (approved 2021, antibody-drug conjugate, boxed warning)
- For: tissue factor highly expressed in 73.6% of 53 pre-treatment biopsies and associated with shorter disease-free survival; blocking antibodies reduced 143B growth, tumour vessel density and lung metastasis from the primary tumour (PMID 26763081). Platelet-derived TGF-beta induces tissue factor on osteosarcoma cells; low-molecular-weight heparin suppressed tumour growth (PMID 29949655).
- Against: in GTEx, normal lung has a median of 96.7 TPM against 12.8 TPM in tumours (our calculation, from the surface-target data), so an MMAE-carrying ADC would meet more target in healthy lung than in tumour. That fits a *blocking* antibody (no payload) better than tisotumab.
- Links to the project's platelet lead (lead 10; lead 9 before the November 20, 2026 re-ranking): the same platelet -> TGF-beta -> tissue factor -> thrombin circuit.
- Cheapest next step: tissue factor staining of matched lung metastases and adjacent normal lung.

### 4.9 IMPDH -- mycophenolate: dead end (tested)
See section 3: negative phase II (PMID 40938558).

### 4.10 High scorers that are dead ends
- **Dimethyl fumarate / bardoxolone (KEAP1, NRF2)**: these drugs switch NRF2 on; NRF2 is a chemoresistance pathway. Wrong direction.
- **MMP inhibitors (MMP2/9/13)**: 357 MMP9 and 347 MMP2 osteosarcoma papers, but the class failed in phase 3 trials across cancers around 1997-2002 (general knowledge) and marimastat/andecaliximab are not available for this use.
- **Teriparatide / abaloparatide (PTH1R) and romosozumab (sclerostin)**: bone-building drugs that switch on the pathways osteosarcoma uses; teriparatide caused osteosarcoma in rats and WIF1 loss accelerates osteosarcoma in mice (PMID 19307728). Wrong direction, and a reminder that the expression score cannot tell agonists from antagonists by itself.
- **JAK inhibitors, midostaurin (PKC)**: JAK2 papers are mostly natural-product cell-line studies; no osteosarcoma study of an approved JAK inhibitor found; median JAK2 6.8 TPM.
- **Abatacept, dinoprost, oprelvekin, dibotermin alfa**: immune suppressants or pathway agonists; listed only so a reader can see why they score.

## 5. Cross-check with the project's existing leads

Existing leads are kept out of the shortlist (flag `existing_lead`) but scored the same way (our calculation):

| Lead | Gene (best drug) | Score | Place in the 20 if inserted alone | Note |
|---|---|---|---|---|
| FAK (lead 4) | PTK2 (defactinib) | 75.4 | 7th | Agrees: evidence 21.7/30, RNA in every tumour. ChEMBL still lists defactinib as phase 3 |
| IL-6 (lead 1) | IL6ST (satralizumab) 73.0; IL6 (siltuximab) 62.4; IL6R (tocilizumab) 45.9 | | 7th (IL6ST) | IL-6 itself has a large clean literature (evidence 24.3) but almost no tumour RNA (median 0.3 TPM), which fits the lead's logic: IL-6 comes from the lung and the host after surgery, not the tumour |
| IL-1 (lead 1) | IL1R1 (anakinra) 67.4; IL1B (canakinumab) 60.1 | | 9th (IL1R1) | Receptor made by almost every tumour (median 45.9 TPM); IL-1beta ligand barely (1.4 TPM) |
| CXCR1/2 (lead 9; was 8) | CXCR2 (ladarixin) 37.8; CXCR1 33.2 | | below 20th | Almost no tumour RNA (0.6-0.7 TPM; neutrophil receptors) and no approved drug (ladarixin is phase 3) |
| Platelets / anticoagulants (lead 10; was 9) | ITGB3 (abciximab) 69.3; F2R (vorapaxar) 68.2; PTGS1 (aspirin) 61.7 | | 9th (ITGB3, F2R) | Platelet receptor genes are expressed by tumours (F2R 36 TPM, ITGB3 33 TPM); tissue factor (new, 4.8) joins this circuit |
| DKK1 (lead 4), LPAR1 | -- | -- | -- | No phase 3-4 drug in ChEMBL (DKN-01 is phase 2), so the screen cannot see them |

So the screen independently ranks the project's FAK, IL-6/IL-1 and platelet leads in the same band as its own best new candidates, which is a useful sanity check on the scoring. CXCR4 overlaps the lung-metastasis report's list of ready drugs but is not one of the eleven ranked leads.

New candidates that the existing leads do not cover: AKT (capivasertib), CXCR4 (mavorixafor), ROCK (belumosudil/fasudil), vitamin D, retinoids (ATRA), tissue factor (as a platelet-circuit extension), and, weakly, HIF-2alpha and CSF1R.

## 6. Below the line, noted for completeness

- **Propranolol (ADRB2)**: slowed xenograft growth with metronomic cisplatin (PMID 36075937, Sci Rep 2022); carvedilol radiosensitised canine osteosarcoma cells (PMID 31778284). But median ADRB2 RNA is 1.8 TPM, so it fails the expression rule; any effect may be on vessels or nerves rather than tumour cells.
- **Statins (HMGCR)**: reversed doxorubicin-induced stemness and metastasis via KLF4 (PMID 28552603) and doubled doxorubicin's effect on growth and metastasis in mice (PMID 34831022); simvastatin has already been in a paediatric phase 1 basket trial that enrolled osteosarcoma (NCT02390843; registry), so not "untested".
- **Pioglitazone (PPAR-gamma agonist)**: reversed doxorubicin resistance in PDOX models from one laboratory (PMIDs 31545293, 31882549, 33015747), but a PPAR-gamma *antagonist* inhibited osteosarcoma in the nuclear-receptor screen (PMID 36681687).
- **Metformin**: already in a bone-sarcoma maintenance trial (NCT04758000; registry).
- **Disulfiram**: already in two trials (NCT05210374, NCT07477457; registry).
- **Sulfasalazine**: ferroptosis via xCT in cell lines (PMIDs 35441682, 40825957); poorly absorbed.
- **Digoxin**: no in vivo osteosarcoma study; failed to inhibit osteosarcoma lines in the mycophenolate screen (PMID 31609477).

## 7. Choices made while building, recorded so they can be challenged

- First pass ranked by gene evidence only. Added the drug-literature route after seeing that ADRB2/propranolol and ATP1A1/digoxin had no gene-tagged papers; then added synonym-OR searches because "tretinoin" alone returns 0 osteosarcoma papers while "all-trans retinoic acid" returns 39.
- The expression rule (>= 5 TPM in at least half of tumours) was added after the drug-literature route let in targets the tumours do not make (opioid receptors via naloxone, calcium channels via verapamil, GABA receptors via flumazenil and propofol). Tightening it from 25% to 50% removed DRD4, GRIN2D and GABA-receptor subunits.
- One row per best drug was added after metformin filled 14 shortlist places with complex I subunits.
- The best drug for a gene is chosen by: not withdrawn > acts on normal protein > inhibits > approved > selective (<= 3 mechanisms) > has its own osteosarcoma papers > oral > no boxed warning > paediatric trials. Without the selectivity step CSF1R's best drug was sunitinib.
- `untested_pts >= 10` for the shortlist means basket-trial drugs (statins, metformin, DFMO, vismodegib, selinexor) are treated as already tested.
- Raw scores before review put CD4, TGF-beta1 and KEAP1 at the top. The review list is long (156 notes) because ChEMBL mechanism records attach many drugs to proteins that are not their anti-cancer target.

## 8. Change log

- **November 19, 2026.** First version: screen, CSV, close reading of the top candidates, report.
