# Lung metastasis in osteosarcoma — working notes

*Started 2026-11-14. Separate FINDING (seen in a source) from HYPOTHESIS (my inference).
Every finding carries a PMID / NCT / URL. "abstract-only" marks claims read only from an abstract.*

Context already read (not redone): `reports/Osteosarcoma research landscape and gaps.md`,
`reports/Osteosarcoma literature map.md`, `reports/Osteosarcoma pooled control dataset.md`,
`reports/Ranked leads and research partners.md`.

## 1. Local quantification (script: `tools/lung_metastasis_map.py`)

Run 2026-11-14 on `data/literature/osteosarcoma_pubtator.jsonl`.

FINDING (own computation, keyword-based):
- 35,078 lines -> **33,242 unique PMIDs**; **29,305** after removing PubMed-flagged reviews and retracted papers.
- Metastasis-focused (title+abstract matches `metasta|lung|pulmonary|pleural`): **10,808** all / **9,130** research.
- Lung-specific wording: **4,194** all / **3,579** research.
- Papers with an **in vivo metastasis endpoint** (animal term AND metastasis wording AND an explicit
  metastasis-model phrase such as tail vein / orthotopic / intratibial / lung nodules / metastatic burden):
  **1,153** all / **1,093** research. That is **12.0%** of metastasis-focused research papers.
- Single-cell/spatial + metastasis: 169 papers. Dog/canine + metastasis: 498 papers.
- By 5-year block, metastasis-focused research papers: 2005-09 728, 2010-14 1,169, 2015-19 2,016,
  2020-24 2,478, 2025-26 (partial) 726. In-vivo-metastasis papers: 94, 147, 267, 322, 94.
  So the *share* with an in vivo metastasis endpoint has stayed near 13% for 20 years.

Outputs written: `data/lung_metastasis_mechanisms.csv`, `data/lung_metastasis_papers.csv`,
`data/lung_metastasis_trials.csv`.

### Per-mechanism counts (research papers only; ivm = in vivo metastasis endpoint)

| Mechanism | papers | metastasis | lung | **ivm** | cell-only | patient | dog |
|---|---|---|---|---|---|---|---|
| VEGF / VEGFR | 867 | 437 | 166 | 106 | 55 | 291 | 42 |
| mTOR / PI3K / AKT | 1203 | 445 | 152 | 92 | 96 | 276 | 33 |
| MMPs | 652 | 403 | 119 | 72 | 110 | 225 | 17 |
| Radiotherapy / SBRT | 2214 | 851 | 282 | 67 | 82 | 700 | 114 |
| EMT | 546 | 336 | 103 | 65 | 69 | 211 | 6 |
| Imaging surveillance | 1074 | 529 | 318 | 52 | 37 | 470 | 124 |
| Wnt / beta-catenin | 592 | 260 | 70 | 50 | 49 | 172 | 12 |
| CSF1R / macrophages (TAM) | 225 | 98 | 42 | 35 | 7 | 71 | 6 |
| Integrins | 267 | 117 | 47 | 32 | 30 | 55 | 3 |
| Dormancy / micrometastasis | 234 | 102 | 55 | 32 | 6 | 85 | 19 |
| Cancer stem cells | 312 | 144 | 53 | 32 | 24 | 88 | 14 |
| Oxidative stress / ferroptosis | 889 | 179 | 56 | 31 | 38 | 106 | 10 |
| PD-1 / PD-L1 | 253 | 122 | 48 | 31 | 4 | 98 | 12 |
| TGF-beta | 361 | 136 | 44 | 29 | 36 | 77 | 11 |
| Autophagy | 496 | 129 | 38 | 28 | 23 | 80 | 5 |
| NK cells | 162 | 63 | 39 | 27 | 0 | 51 | 17 |
| Exosomes / EVs | 237 | 93 | 42 | 27 | 15 | 56 | 12 |
| Single-cell / spatial | 467 | 169 | 53 | 27 | 21 | 138 | 16 |
| STAT3 | 280 | 125 | 39 | 26 | 27 | 66 | 15 |
| **FAK (PTK2)** | 119 | 71 | 30 | **24** | 19 | 40 | 1 |
| **CXCR4 / CXCL12** | 139 | 82 | 40 | **24** | 15 | 47 | 5 |
| Glycolysis / HK2 / LDHA | 412 | 152 | 47 | 23 | 14 | 112 | 12 |
| **Inhaled / aerosol delivery** | 41 | 33 | 30 | **22** | 0 | 20 | 13 |
| **IL-6** | 259 | 80 | 28 | **20** | 19 | 48 | 8 |
| Hypoxia / HIF1A | 405 | 153 | 45 | 19 | 29 | 93 | 15 |
| IL-2 | 83 | 43 | 21 | 17 | 1 | 35 | 11 |
| **Ezrin** | 103 | 73 | 26 | **17** | 15 | 42 | 6 |
| ROCK / RhoA | 99 | 56 | 18 | 15 | 15 | 33 | 0 |
| MET / HGF | 291 | 116 | 46 | 15 | 11 | 93 | 34 |
| Platelets / coagulation | 427 | 144 | 63 | 15 | 16 | 116 | 29 |
| **Neutrophils / NETs / MDSC** | 242 | 90 | 41 | **14** | 3 | 80 | 10 |
| NOTCH | 135 | 65 | 22 | 14 | 10 | 45 | 4 |
| IGF1R / IGF2 | 321 | 84 | 23 | 13 | 16 | 50 | 13 |
| ctDNA / liquid biopsy | 98 | 57 | 21 | 13 | 2 | 49 | 10 |
| **IL-8 / CXCL8** | 89 | 33 | 20 | **11** | 7 | 23 | 6 |
| Anoikis | 51 | 34 | 12 | 11 | 10 | 17 | 0 |
| SRC | 114 | 52 | 20 | 10 | 18 | 24 | 4 |
| RANKL | 140 | 42 | 12 | 9 | 8 | 26 | 4 |
| uPA / PLAU | 71 | 41 | 10 | 9 | 17 | 13 | 5 |
| CCL2 / CCR2 | 51 | 19 | 9 | 8 | 3 | 12 | 4 |
| Fibroblasts / CAF | 121 | 48 | 25 | 8 | 11 | 32 | 2 |
| Fatty acid / lipid metabolism | 160 | 42 | 13 | 8 | 11 | 28 | 4 |
| **IL-1 (IL1A/IL1B)** | 216 | 50 | 22 | **7** | 16 | 27 | 2 |
| LOX | 39 | 17 | 10 | 7 | 0 | 13 | 0 |
| CXCR3 / CXCL9-10 | 30 | 18 | 8 | 6 | 0 | 12 | 1 |
| GD2 | 54 | 24 | 10 | 6 | 2 | 16 | 3 |
| Metastasectomy / lung surgery | 250 | 244 | 234 | 6 | 7 | 237 | 7 |
| IL-11 | 23 | 9 | 7 | 5 | 0 | 8 | 1 |
| **DKK1** | 38 | 14 | 1 | **5** | 3 | 10 | 0 |
| Glutamine metabolism | 69 | 16 | 6 | 5 | 3 | 10 | 2 |
| HER2 / ERBB2 | 107 | 55 | 14 | 4 | 1 | 49 | 12 |
| IL-15 | 21 | 10 | 3 | 2 | 0 | 10 | 8 |
| B7-H3 / CD276 | 36 | 15 | 4 | 2 | 1 | 11 | 4 |
| GM-CSF (CSF2) | 37 | 7 | 5 | 0 | 2 | 5 | 2 |

HYPOTHESIS: the ranking is dominated by mechanisms that had a convenient drug
(VEGF, mTOR) or are generic (MMP, EMT); the lung-niche cytokine axis that the
mechanistic work points to (IL-1 7 ivm, CXCL8 11, IL-6 20) has an order of
magnitude less in vivo metastasis work than VEGF, and no trial.

### Mechanism drug name present in the 758-trial file (own cross-check)

Present: bevacizumab (VEGF), sirolimus/everolimus (mTOR), radium-223, vactosertib (TGF-beta),
hydroxychloroquine/chloroquine (autophagy), metformin, tocilizumab (one trial, NCT04616248 —
checked, it is CDX-301/CDX-1140 immunomodulation, tocilizumab only as a toxicity rescue drug,
**not** an IL-6 efficacy test), aldesleukin, cabozantinib/crizotinib (MET), aspirin,
ganitumab (IGF1R), dasatinib/saracatinib (SRC), denosumab (RANKL).

**Zero drug presence** for: MMP, EMT, Wnt/beta-catenin, CSF1R, integrins, dormancy,
cancer stem cells, ferroptosis, NK-cell agents, STAT3, **FAK**, **CXCR4/CXCL12**,
**IL-8/CXCR1-2**, **IL-1**, neutrophils/NETs, NOTCH, **DKK1**, uPA, LOX, **ezrin**,
hypoxia, CCL2/CCR2, CAF/FAP.

## 2. Biology: which mechanisms have in vivo METASTASIS evidence

All abstract-only unless marked. Each entry says what the in vivo metastasis endpoint was.

### 2a. The lung niche cytokine circuit (IL-1alpha -> IL-6 / CXCL8) — strongest mechanistic chain

FINDING. **PMID 30135299** (Gross/Roberts, JCI Insight 2018, "IL-6 and CXCL8 mediate osteosarcoma-lung
interactions critical to metastasis"): DeltaNp63 overexpression in OS cells drives IL-6 and CXCL8;
both were higher in **lung metastases than in matched primary tumours from the same patients**;
expression in cell lines "correlated strongly with lung colonization efficiency in murine xenograft
models"; lentiviral expression made poorly metastatic cells metastatic. Blocking IL-6 and CXCL8
(genetic or pharmacological) had **minimal effect on proliferation in vitro or in vivo** but the
**combination inhibited metastasis across multiple models**. Feed-forward amplification came from
OS interactions with **primary bronchial epithelial cells and bronchial smooth muscle cells**.
(no per-animal numbers in the abstract; abstract-only)

FINDING. **PMID 40882022** (Cancer Res 2025, "Metastasis-Initiating Osteosarcoma Subpopulations
Establish Paracrine Interactions with Lung and Tumor Cells to Create a Metastatic Niche"):
organotypic metastasis model + scRNA-seq + human xenograft + **murine immunocompetent** models.
Metastasis is initiated by a **hypo-proliferative subpopulation** that sustains IL-6 and CXCL8
production **in response to lung-epithelial-derived IL-1alpha**. "Genomic and pharmacologic
disruption of IL1 signaling in osteosarcoma cells significantly reduced metastatic progression."
This is the paper that makes IL-1 the upstream, druggable node (anakinra / canakinumab exist).
(abstract-only; no effect size in the abstract)

FINDING. **PMID 38031171** (J Exp Clin Cancer Res 2023, premetastatic lung remodelling): mice bearing
OS, or merely **preconditioned with OS cell secretome**, developed airway damage, inflammation,
**neutrophil infiltration** and ECM remodelling (fibronectin, collagens) by **resident activated
fibroblasts**, which favoured adhesion of disseminated cells and **accelerated metastasis formation**.
Identified **EFEMP1**, secreted only by metastatic cells, in plasma of tumour-bearing mice and in
patient biopsies (poorer OS). **Depleting EFEMP1 from the secretome prevented lung metastasis.**
(abstract-only)

FINDING. **PMID 38302407** (Cell Death Dis 2024): TAMs were more prevalent in lung metastases than
primary tumours; OS+TAM co-culture medium raised IL-8; in vivo the conditioned medium promoted
lung metastasis and **anti-IL-8 antibody mitigated it**; mechanism via FAK. (abstract-only)

FINDING. **PMID 32079335** (Cancers 2020) and **PMID 34760697** (Front Oncol 2021): in a lung
metastasis model, **lung blood vessels express CXCL1 and OS cells express CXCR2**; CXCL1 from human
pulmonary artery endothelial cells drove OS motility via VCAM-1, requiring CXCR2 and FAK/PI3K/Akt/NF-kB.
In vivo CXCL1 "serves as a critical promoter in osteosarcoma metastasis to the lung". CXCR2 expression
correlated with pathology stage in human specimens. (abstract-only)
**So the IL-8/CXCL8 family signal is receptor-level druggable: CXCR1/2 inhibitors (reparixin,
ladarixin, SX-682) exist and have never been tested in osteosarcoma.**

FINDING. **PMID 41083282** (J Immunother Cancer 2025): syngeneic BALB/c K7M3-luc lung metastasis
model. Particulate beta-glucan **before** tumour infusion gave fewer lung tumours and longer
survival and "prevented tumour cell seeding in the lungs"; in tumour-bearing mice it suppressed
growth and prolonged survival. Effect **depended on macrophages and NK cells** (depletion studies);
adding a **CD40 agonist** increased it further. (abstract-only)
Note: beta-glucan is an over-the-counter-grade agent and CD40 agonists are in human trials.

HYPOTHESIS: the strongest in vivo-validated, drug-matched node in the whole lung-niche story is
IL-1 signalling (PMID 40882022) feeding IL-6/CXCL8 (PMID 30135299), and the three drug classes
that hit it — IL-1 blockers, IL-6 blockers, CXCR1/2 blockers — have **zero osteosarcoma trials**
(own cross-check of `data/osteosarcoma_trials.csv`, 758 studies; the single tocilizumab hit is
NCT04616248, a phase 1 adult CD40-agonist/Flt3L/radiation basket trial whose primary outcomes are
adverse events and MTD — tocilizumab there is supportive care, not an IL-6 efficacy test).

### 2b. Ezrin — the oldest lung-metastasis mechanism in osteosarcoma, still no drug

FINDING. 103 ezrin papers, 73 metastasis-focused, **17 with an in vivo metastasis endpoint** (own count).
- **PMID 21706056** (Oncogene 2012): NSC305787 and NSC668394 bind ezrin at low micromolar affinity,
  inhibit ezrin phosphorylation, actin binding and motility, and **after tail-vein injection both
  inhibited lung metastasis of ezrin-sensitive but not ezrin-resistant OS cells**. (abstract-only)
- **PMID 22147261** (Cancer Res 2012): cells expressing open (T567D) ezrin formed **neither primary
  orthotopic tumours nor lung metastases**; closed (T567A) cells were metastasis-deficient with
  intact primary growth. Single-cell lung imaging showed **increased early apoptosis after arrival
  in the lung** for both. Also altered carbohydrate/amino-acid metabolism, lactate production and
  oxygen consumption — i.e. ezrin ties motility to metabolic adaptation. (abstract-only)
- **PMID 24326277** (Bioorg Med Chem 2014): analogues 21k/21m of NSC668394 — still tool compounds.
- **PMID 41843652** (Sci Signal 2026): the *closed* form of ezrin is itself an RNA-binding protein
  with affinity for G-quadruplex RNA; closed ezrin **rescued metastatic capability of ezrin-null
  OS xenografts in zebrafish**. Overturns the "closed = inactive" assumption. (abstract-only)
FINDING. 5 of the top 10 ezrin-titled papers in the dataset are retractions / expressions of concern
(PMIDs 41640460, 38376414, 37477177, 36324370 flagged in their own titles) — the ezrin literature
also carries paper-mill contamination.
HYPOTHESIS: ezrin has ~20 years of in vivo metastasis evidence and **no clinical-grade inhibitor**.
That is a medicinal-chemistry gap, not an evidence gap, and it is probably why it never reached a trial.

### 2c. Pre-metastatic niche: neutrophils, macrophages, fibroblasts

FINDING. Neutrophils/NETs/MDSC: 242 papers, 14 with an in vivo metastasis endpoint (own count).
- **PMID 39296147** (Heliyon 2024): AOC3 accelerates lung metastasis by recruiting tumour-associated
  neutrophils and NETs (title-level).
- **PMID 39695851** (J Hematol Oncol 2024): tumour-derived **G-CSF** makes an immunosuppressive
  microenvironment in an OS model and **reduces response to CAR.GD2 T cells** (title-level).
  HYPOTHESIS: this is a direct, testable explanation for why GD2 therapy underperformed in
  osteosarcoma (AOST1421) but works in neuroblastoma.
FINDING. Macrophages are by far the best-studied niche cell: 225 CSF1R/TAM papers, **35 with in vivo
metastasis endpoints**, and 71 if "macrophage" is matched broadly. No CSF1R inhibitor
(pexidartinib, emactuzumab) appears in any of the 758 trials (own cross-check).
FINDING. **PMID 39526499** (Vet Comp Oncol 2024): in **naturally occurring canine osteosarcoma**,
pre-metastatic lungs (n=10 dogs with OS, no metastases) had significantly more CD204+ and CD206+
macrophages, monocytes and CD11d+ bone-marrow-derived cells than control dogs (n=10); CD11d+ BMDCs
were **lower** once metastases were established, i.e. recruitment is transient. Authors conclude dogs
"may represent ideal candidates for assessing new PMN-targeting therapies". (abstract-only)
FINDING. Fibroblasts/CAF: 121 papers but only **8 with in vivo metastasis endpoints** — the least
developed of the three niche cell types despite PMID 38031171 implicating resident activated
fibroblasts and PMID 41648517 implicating lung epithelium/fibronectin.

### 2d. Dormancy — well-recognised clinically, barely modelled

FINDING. 234 dormancy/micrometastasis papers, 102 metastasis-focused, **32 with in vivo metastasis
endpoints**, only **6 cell-only** — so the dormancy literature is unusually in-vivo-heavy.
But only **14 papers have dormancy in the title**, and several are generic (angiogenic switch models,
quantitative phase imaging). Osteosarcoma-specific dormancy mechanism papers found:
- **PMID 25273088** (Cancer Res 2014): IGF2 preserves OS cell survival by creating an **autophagic
  state of dormancy** protecting against chemotherapy (title+abstract-level).
- **PMID 41365861** (Cell Death Dis 2025): **chloroquine** overcomes chemotherapy resistance and
  suppresses metastasis "by eradicating dormant cancer cells" (title-level; not OS-exclusive).
- **PMID 26815014** (ACS Nano 2016): dormancy-associated microRNAs for OS-targeted nanopolyplexes.
FINDING (methodological, important). **PMID 29601385** (Clin Orthop Relat Res 2018): the widely used
**intratibial K7M2 model is not a spontaneous metastasis model**. Pulmonary metastases were detectable
in 100% of mice **as early as 1 week**; metastatic burden rose (0.88%+-0.58 wk1, 6.6%+-5.3 wk2,
16.1%+-12.5 wk3, 40.3%+-14.83 wk4) but the **number of foci did not** (36.4+-33.6 wk1 vs 49.3+-26.3
wk4, p=0.18); and **amputating the injected limb 30 minutes after injection left metastatic burden
unchanged** (48.9%+-6.1% vs 40.9%+-15.3%, p=0.819). Conclusion: immediate seeding independent of a
primary tumour; "should not be used to study the early components of the metastatic cascade".
HYPOTHESIS: this single paper undercuts a large fraction of the 1,093 in vivo-metastasis papers,
because tail-vein and intratibial designs both measure **colonization/outgrowth**, not dissemination
or dormancy exit. Almost nothing in the osteosarcoma literature models the clinically important
state: a patient with no visible disease after surgery whose lungs hold dormant cells.

### 2e. CXCR4 / CXCL12

FINDING. 139 papers, 82 metastasis-focused, **24 with in vivo metastasis endpoints** (own count) —
equal to FAK and more than IL-6. Direction of effect is **contested**:
- **PMID 27300512** (J Cancer Res Clin Oncol 2016): "Altered CXCL12 expression reveals a **dual role**
  of CXCR4 in osteosarcoma primary tumor growth and metastasis" (title-level).
- **PMID 29735547** (Cancer Res 2018): epigenetic regulation of CXCL12 mediates tumour progression
  and the immune response in osteosarcoma (title-level).
- **PMID 31571016** (Clin Exp Metastasis 2020): PTEN loss activates an AKT/CXCR4 axis potentiating
  lung metastasis (title-level).
- **PMID 25997540** (Oncol Rep 2015) and **PMID 28038429**: AMD3100 (plerixafor) reduced
  CXCR4-mediated survival and metastasis (title-level).
HYPOTHESIS: plerixafor is cheap, approved and mobilises stem cells, so any trial must be designed
around the dual-role problem (blocking CXCR4 could also mobilise tumour cells). This is the most
"ready" drug with the least settled biology.

### 2f. FAK / integrins / adhesion

FINDING. FAK: 119 papers, **24 in vivo metastasis** — and unlike the Osteosarcoma literature map's
general FAK count, the metastasis-specific slice is dense and recent:
PMID 42520958 (Am J Pathol 2026, ZEB1/IQGAP3/FAK/beta-catenin drives lung metastasis; FAK inhibition
reduced metastasis in vivo), 37013056 (LOX->FAK phosphorylation), 36997926 (CD248/ITGB1/FAK-paxillin),
35524311 and 35280793 (tetraspanins -> FAK-Src-Ras-ERK), 38302407 (IL-8/TAM -> FAK),
32079335/34760697 (CXCL1/CXCR2 -> FAK -> VCAM-1).
HYPOTHESIS: FAK is the **convergence node** of the lung-niche signals (IL-8, CXCL1, integrins, LOX),
and defactinib is FDA-approved (2025). That makes FAK the single best drug-to-mechanism match for
lung metastasis, and the Osteosarcoma literature map already flagged it as untrialled with an NIH
grant behind it (Regan, Colorado State, a veterinary school).
FINDING. Integrins: 267 papers, 32 in vivo metastasis, **zero drug presence in the 758 trials**.
PMID 41648517 (below) nominates tumour-derived **fibronectin (FN1) -> integrin/syndecan on lung
epithelium** as the colonization step, which makes integrin blockade a niche-level target.

### 2g. Metabolic adaptation

FINDING. Split by pathway (own counts, in vivo metastasis endpoints): glycolysis/HK2/LDHA 23,
oxidative stress/ferroptosis 31, hypoxia/HIF1A 19, fatty-acid/lipid 8, **glutamine 5**.
PMID 22147261 (ezrin, above) directly links the metastasis phenotype to lactate production and
oxygen consumption. PMID 40983627 (Br J Cancer 2025, ENO1 promotes metastasis via metabolic
reprogramming) and PMID 38292199 (LETM1 -> mitochondrial function -> lung metastasis) are the
clearest recent in vivo entries (title-level).
HYPOTHESIS: metabolic adaptation in the lung specifically (as opposed to generic Warburg biology)
is almost unstudied — glutamine metabolism has 5 in vivo metastasis papers in 33,000, while
telaglenastat and DRP-104 are clinical-stage.

### 2h. Single-cell, spatial and canine data — the newest and most under-used

FINDING. 467 single-cell/spatial papers, 169 metastasis-focused, **27 with in vivo metastasis endpoints**.
- **PMID 41648517** (bioRxiv 2026, preprint — NOT peer-reviewed): cross-species single-cell atlas,
  **>1 million cells/nuclei** from human, canine, PDX and syngeneic mouse at **both bone and lung**
  sites. Six conserved tumour transcriptional states; conserved macrophage, fibroblast and endothelial
  populations with site- and species-specific reprogramming. Two conclusions matter most:
  (i) **canine osteosarcoma is the most faithful model** of human tumour-host communication of those
  compared; (ii) **lung metastases showed more intense ECM signalling than primary bone tumours**,
  with tumour-derived **FN1 engaging integrin and syndecan receptors on lung epithelial cells**,
  driving a profibrotic state that promotes the fibrotic niche and lung colonization. (abstract-only, preprint)
- **PMID 42856637** (bioRxiv 2026, preprint): live-cell imaging of biosensor-expressing OS **lung
  metastases ex vivo**. MCL1 inhibition killed most cells but **ERK-high/Fra-1-high cells persisted,
  enriched at the tumour-lung interface**. Tumour-cell lysis itself amplified **FGFR-mediated ERK
  signalling in neighbouring cells**. Adding fexagratinib (FGFR) or pazopanib suppressed the adaptive
  signal and improved efficacy ex vivo and in vivo. (abstract-only, preprint)
  HYPOTHESIS: this is a mechanism for why single agents plateau in lung metastasis — the lung
  interface is where resistance is born, and it is pharmacologically reachable.
- **PMID 40940877** (Cancers 2025): multiplex imaging mass cytometry, prognostic immunosuppressive
  subpopulations and macrophage-driven metastasis (title-level).
FINDING. Canine: 498 dog+metastasis papers, 137 with in vivo metastasis endpoints. Dogs carry the
only naturally occurring, spontaneously metastasising, immunocompetent osteosarcoma at scale.

## 3. Clinical: every trial aimed at lung metastasis or the resected-metastasis setting

Own cross-check of `data/osteosarcoma_trials.csv` (758 studies): **224** mention lung/metastasis/
inhaled terms; **73** are explicitly lung-directed or lung-local. Plus ClinicalTrials.gov API v2
searches run 2026-11-14 (`tools/lung_metastasis_map.py` writes `data/lung_metastasis_trials.csv`).

### 3a. Lung-directed delivery (inhaled / aerosol) — the longest-running idea in the field

| Agent | Trial / paper | n | Result |
|---|---|---|---|
| Inhaled GM-CSF (sargramostim) | NCT00066365, COG; **PMID 20576718** | 43 eligible | Doses 250–1,750 ug BID feasible, no DLT. **3-year EFS 7.8%, OS 35.4%.** Fas/FasL scores *fell* after treatment (1.3/0.88 pre vs 0.78/0.62 post); only 11/30 nodules CD1a+, 4/30 S100+, 6/30 clusterin+. Conclusion: "no detectable immunostimulatory effect in pulmonary metastases or improved outcome postrelapse" |
| Inhaled lipid cisplatin (ILC) | NCT00102531 ph1b/2a; **PMID 23255417** | 19 treated | No haematologic/renal/oto toxicity; minimal systemic cisplatin. **11/19 had bulky disease and all progressed before cycle 7.** Of 8 with all lesions <=2 cm: 1 sustained PR, 2 stable then metastasectomy and pulmonary-recurrence-free at 1 year. "3 of 8 with less bulky disease had sustained benefit" |
| Inhaled lipid cisplatin, phase 2 | **NCT01650090** (Eleison), completed Nov 2018, n=28, primary outcome "observed relapse-free interval vs historical controls" | 28 | **No results posted, no publication found** (Europe PMC search 2026-11-14). A registered CT.gov search found **no phase 3 of ILC in osteosarcoma**. |
| Aerosol IL-2 (aldesleukin) | **NCT01590069**, MD Anderson, phase 1/2, started 2012-06-28, estimated n=70, completion pushed to **2029-04-30**, last update 2026-10-09 | — | **ACTIVE_NOT_RECRUITING, no results after 14 years.** Preclinical basis: PMID 24136885 and 24610870 — aerosol IL-2 raised NK numbers *only in lung*, no systemic toxicity, and aerosol IL-2 + NK cells beat either alone on tumour number/size/apoptosis and survival |
| Aerosol gemcitabine | **NCT03093909** (MD Anderson), phase 1, recruiting since 2017-11, n=44, no results | — | Preclinical: PMID 15800950 (inhibits primary OS and lung metastases), 19803732 (safe + active in OS-bearing **dogs**), **29610563** (aerosol GCB started 48 h after amputation inhibited lung metastases and did **not** impair wound healing in skin, tail or bone) |
| Inhaled rhIL-15 (dogs) | **PMID 35680383**, phase 1, 21 dogs, 18 evaluable | 18 | MTD 50 ug BID x14 d. **1 CR >1 year, 1 PR, 5 SD = clinical benefit rate 39%.** Low pretreatment lymphocyte count predicted benefit; PBMC cytotoxicity rise correlated with OS |
| Inhaled rhIL-15, adjuvant (dogs) | **PMID 41209004**, NCI-COTC030 **phase 2**, planned 40 dogs | — | Designed to cut metastatic failure from a historical 40% to 20%. **DFS and OS were statistically INFERIOR to a validated historical control and the trial was halted for futility.** PBMC cytotoxicity fell after surgery and after chemotherapy (−18.2 +- 16.1%, p<0.001); IL-6 rose after amputation and after chemotherapy, correlating with falling cytotoxicity |
| Inhaled rhIL-15 + doxorubicin preconditioning (dogs) | **PMID 41041167**, 10 dogs, 8 evaluable | 8 | 1 CR >1 yr, 2 SD: **CBR 30%, ORR 10%**. Doxorubicin lymphodepletion did **not** improve on monotherapy |
| BIO-11006 (inhaled, MARCKS) | **NCT04183062** | 0 | WITHDRAWN — "the drug for this study was not available" |

FINDING, and it is the most important negative result I found: **PMID 41209004** shows that giving
an immune-stimulating inhaled drug *in the adjuvant window right after amputation* made dogs do
**worse** than historical controls, and the correlative data say why — surgery and chemotherapy each
suppress PBMC cytotoxicity and raise IL-6.
HYPOTHESIS: the post-surgical window is immunosuppressed *and* IL-6-high, which is exactly the
state that PMID 30135299 and 40882022 say favours lung colonization. Immune stimulation there may
be the wrong move; **IL-6 / IL-1 blockade there may be the right one.** This is a testable,
mechanism-linked prediction that nobody appears to have tried, and it unifies three separate
findings in this file.

### 3b. The resected-lung-metastasis setting

| Agent | Trial | Design | n | Result |
|---|---|---|---|---|
| Inhaled GM-CSF | NCT00066365 (COG) | single arm, after thoracotomy | 43 | 3-yr EFS 7.8% (PMID 20576718) |
| **Saracatinib (SRC inhibitor)** | **NCT00752206** (SARC) | **randomized, double-blind, PLACEBO-CONTROLLED, phase 2.5**, randomized within 6 weeks of complete resection of all lung nodules, 175 mg/day up to thirteen 28-day cycles | 38 randomized, 37 analysed (18 vs 19) | **Median PFS 19.4 mo (saracatinib) vs 8.6 mo (placebo), p=0.47**; median OS not reached in either arm. **TERMINATED: "DSMB recommended study termination for slow accrual and futility."** Ran 2009-03 to 2017-12 — **8.75 years for 38 patients.** (registry + **PMID 32398945**, Sarcoma 2020, open access) |
| Dinutuximab + GM-CSF | NCT02484443 (COG AOST1421) | single arm | 39 | 28% EFS at 12 mo (11/39), below the required 16 — see `reports/Osteosarcoma pooled control dataset.md` |
| Denosumab | NCT02470091 (COG AOST1321) cohort 2 | single arm | 38 | 26% EFS at 12 mo (10/38) — same source |
| **OST-HER2 / OST31-164** (Listeria-HER2 vaccine) | **NCT04974008**, Emerald Clinical, phase 2, **ACTIVE_NOT_RECRUITING**, started 2021-10-21, primary outcome **event-free survival** | 39 | Press-reported 3-yr OS 72.7% vs 45.8% historical (see gaps report); **no peer-reviewed publication found**. Registry has **no posted results** |
| **Viscum album extract (Iscador P, mistletoe)** | **NCT05726383** "MISTOSUS", phase 2, recruiting since 2024-05, n=32; **PMID 41789811** (Future Oncol 2026, OA) | 32 planned | Not yet reported. Rationale: pilot of **9** PAYA patients, **55% post-relapse EFS** at median 84 months follow-up. Stated benchmark: 30% PREFS-12 |
| Thoracotomy vs VATS | **NCT05235165 = COG AOST2031**, phase 3 randomized, recruiting since 2022-04-01, completion 2031-03-31, n=62 estimated; design paper **PMID 36085388** | 62 | Primary outcome **4-year thoracic event-free survival**. Randomizes the *surgical approach*, not a drug |
| Metastasectomy + pre-op immunotherapy + SBRT | NCT06114225 (Ruijin), phase 2 single arm, n=43, recruiting | 43 | Primary outcome 12-month PFS rate. No results |
| Anti-angiogenics + chemo, resectable pulmonary mets | NCT03742193, phase 2, n=43, **status UNKNOWN** since 2019-08 | 43 | No results |
| Canine ADXS31-164 (same vaccine as OST-HER2) | **PMID 39955616** (Mol Ther 2025) | **1-arm, multicentre, 118 dogs**, SOC then vaccine | 118 | **No significant difference in median DFI or OS vs a historical SOC cohort.** "Elite survivors" (DFI >490 d) had transient temperature and IL-6/TNF-alpha rises and robust PBMC cytotoxicity; short-term survivors caught up on repeat dosing |

FINDING / CORRECTION to the earlier gaps report. `reports/Osteosarcoma and neuroblastoma research
gaps.md` lists as gap 3 "No randomized test of drug therapy after complete metastasis surgery —
only single-arm trials found." **That is not accurate.** NCT00752206 / PMID 32398945 was exactly
that trial: randomized, double-blind, placebo-controlled, drug after complete pulmonary
metastasectomy. The real finding is worse than "never tried": it **was** tried, it took almost nine
years to randomize 38 patients, it was stopped for slow accrual and futility, and it left a
**10.8-month median PFS difference (19.4 vs 8.6) with p=0.47** that nobody has followed up.
HYPOTHESIS: the binding constraint in this setting is **accrual, not willingness to randomize**.
Any new proposal has to solve 38-patients-in-9-years, which means either an international platform
(FOSTER NCT07871864, 530 patients, randomized, recruiting) or pet dogs.

FINDING. The canine ADXS31-164 result (**PMID 39955616**, 118 dogs, no DFI/OS benefit vs historical
control) sits awkwardly beside the press-reported human OST-HER2 benefit against a historical
control. Both are single-arm against historical controls; the larger, peer-reviewed one is negative.

### 3c. Radiotherapy / SBRT to lung metastases

FINDING. **PMID 41531260** (Pediatr Blood Cancer 2026): 24 patients, 71 lesions, 2015–2023; median
40 Gy/5 fractions; **1-year cumulative local failure 13.6% (95% CI 6.6–23.2)**, 6-month 10.3%
(4.5–18.9). 11 local failures: 4 in-field, 3 marginal, 4 out-of-field. Spine SBRT (HR 3.39,
1.03–11.14) and larger PTV (HR 1.003 per unit, 1.001–1.006) predicted failure. 6- and 12-month OS
87.5% and 64.1%. Grade 2 acute toxicity 5.6%, no acute grade >=3. Only **17% of lesions were
parenchymal** (66% osseous).
FINDING. **PMID 40509558** (Pediatr Blood Cancer 2025): 7 patients, 34 SBRT courses, 29% of sites
pulmonary/mediastinal. Local control 88% of lesions; **all 4 local failures had BED <=48 Gy**;
**median distant PFS 2.4 months.**
HYPOTHESIS: SBRT controls what it irradiates and does nothing about what it does not — distant PFS
of 2.4 months is the whole problem in one number. SBRT is therefore a *local* tool that needs a
systemic partner, which is what NCT06492954 (atezolizumab + SBRT + surgery) and NCT06114225 test.
Registry trials found: NCT02880319 (SBRT oligometastatic bone, n=150, has results), NCT02581384
(SBRT pulmonary mets in Ewing/RMS/osteosarcoma, **TERMINATED after 5 patients**), NCT01586104
(IMRT for lung metastases in younger patients, n=20, has results), NCT06074692 (PARP + SBRT +
immunotherapy, recruiting), NCT06492954 (atezolizumab + SBRT + surgery, phase 1, n=12).

### 3d. Regional / organ-directed delivery beyond inhalation (rarely discussed)

FINDING, from own trial-file scan: two surgical-delivery programmes exist and are almost absent
from osteosarcoma reviews:
- **NCT02811523** "In Vivo Lung Perfusion for Pulmonary Metastases of Sarcoma", phase 1, recruiting since 2016-02, n=17.
- **NCT03965234** "Pulmonary Suffusion in Controlling Minimal Residual Disease in Patients With Sarcoma or Colorectal Metastases", phase 1/2, recruiting since 2020-07, n=99. Preliminary phase 1 safety/drug analyses: **PMID 40940977** (Cancers 2025).
HYPOTHESIS: pulmonary suffusion explicitly targets **minimal residual disease in the lung**, which
is the dormancy state nothing else addresses. It deserves far more attention than it gets.

### 3e. Maintenance after resection (lung-relevant but not lung-directed)

Registry, own search: regorafenib maintenance **NCT04055220** (randomized, n=168) and **NCT04698785**
(n=36); cabozantinib maintenance **NCT05135975** (n=86) and **NCT06341712** (randomized cabozantinib+BSC
vs BSC, **TERMINATED after 10 patients**, has results — "the sponsor has decided to terminate");
metformin maintenance **NCT04758000** (n=67); DFMO maintenance **NCT06892678** (n=15) and **NCT07321912**
(n=406); ZKAB001 PD-L1 maintenance phase 3 **NCT04359550** (n=362, status UNKNOWN, no results —
already flagged as a lost trial in the earlier reports); pazopanib maintenance within **NCT06239272**
(NRSTS2021); FOSTER platform **NCT07871864** (phase 3, randomized, n=530, recruiting from 2026-10).

## 4. Detection: does finding lung relapse earlier help?

FINDING. **PMID 24249538** (Clin Orthop Relat Res 2014, Tata Memorial, open abstract): prospective
randomized **noninferiority** trial, **500 non-metastatic extremity sarcoma patients**, 2006–2010,
2x2 of **chest radiograph vs CT** and **3-monthly vs 6-monthly** follow-up; 178 deaths; median
follow-up 42 months. 3-year OS/DFS overall 67% / 52%. **Chest radiograph 67% vs CT 66% 3-year OS**
(HR 0.9, upper 90% CI 1.13); DFS 54% vs 49% (HR 0.82, upper 90% CI 0.97). **6-monthly 64% vs
3-monthly 69% OS** (HR 1.2, upper 90% CI 1.47); DFS 51% vs 52%. ~90% of local recurrences were
found by patients themselves. Conclusion: "inexpensive imaging detects the vast majority of
recurrent disease ... without deleterious effects on eventual outcomes", though noninferiority of
6-monthly on OS was **not conclusively demonstrated**.
  LIMIT: "extremity sarcomas" — the abstract does not break down histology, and I could not retrieve
  the full text (PMC blocked a captcha, europepmc.org host not reachable from this workspace), so
  **the osteosarcoma fraction of those 500 patients is unverified.** Treat as sarcoma-wide evidence.

FINDING. **PMID 38345039** (Pediatr Hematol Oncol 2024): 69 patients (35 osteosarcoma, 34 Ewing),
**1,279 follow-up images**. 9 relapses: 5 in osteosarcoma (4 pulmonary, 1 local). **Only 2 of 9
relapses were symptomatic; the rest were found on imaging.** Positive predictive value for relapse
0.5 in osteosarcoma, 0.44 in Ewing. Probability of *any* anomaly 6% (95% CI 4–8) in osteosarcoma
and 12% (10–15) in Ewing (Ewing patients were followed with MRI, osteosarcoma mostly with X-rays).
"Abnormal findings on follow-up images rarely represent relapse."

FINDING. No randomized surveillance trial in osteosarcoma is registered. The two randomized
surveillance trials I found are **soft tissue sarcoma only**: **NCT04751409** (MD Anderson, limited
vs intense follow-up, n=227, recruiting since 2020-12 — and its **primary outcome is fear of cancer
recurrence**, not survival) and **NCT06526897** (ECOG-ACRIN, **phase 3 chest CT vs chest X-ray**,
n=1,582, primary outcome overall survival, NOT_YET_RECRUITING, completion 2032-11).

### ctDNA / liquid biopsy

FINDING. 98 ctDNA/liquid-biopsy papers in 33,242; 57 metastasis-focused; 13 with an in vivo
metastasis endpoint (own counts).
- **PMID 39360936** (Clin Cancer Res 2024, National Pediatric Cancer Foundation): phase 2
  gemcitabine + nab-paclitaxel in recurrent osteosarcoma, 18 patients, **PFS-4 28% (95% CI 13–59%)**,
  2/18 confirmed PR. Serial CTC and ctDNA by ultralow-pass WGS was **feasible**; all 18 had
  detectable CTCs, 10 had detectable ctDNA; **all 8 patients with MYC amplification at entry
  progressed.** This is the only prospective multi-institution osteosarcoma trial I found with
  serial liquid biopsy embedded.
- **PMID 41673231** (NPJ Precis Oncol 2026): **5-hydroxymethylcytosine** in plasma cfDNA; 262-gene
  signature; in validation, cluster 1 held 10/12 samples from patients with active disease and
  cluster 2 held 26/33 from patients without. **Sensitivity 65%, specificity 64%** for active
  disease. Honest conclusion: feasible, needs larger cohorts.
- **PMID 42824543** (J Bone Oncol 2026, review): tumour-informed ctDNA gives the strongest
  osteosarcoma MRD signal; postoperative positivity is associated with inferior EFS and in selected
  patients precedes imaging relapse. Methylation is a mutation-independent adjunct; CTCs, EVs and
  circulating miRNAs "remain exploratory signals without validated postoperative surveillance
  actions". Explicitly states the field's open question: "Future studies should test whether
  biomarker-triggered reassessment improves clinically meaningful outcomes ... rather than simply
  documenting recurrence earlier." (abstract-only, review)

**ANSWER to "does earlier detection change survival?"** FINDING: there is **no evidence in
osteosarcoma that it does**, and the one randomized sarcoma trial (PMID 24249538) found that
cheaper, less frequent imaging did not worsen 3-year OS. The mechanism by which earlier detection
*could* help is well documented though: complete resection is the dominant survival factor
(**PMID 42036655**, meta-analysis of 21 retrospective studies: metastasectomy vs none HR 0.29,
95% CI 0.18–0.46; complete resection HR 0.21, 0.12–0.38 for post-relapse survival and HR 0.31,
0.23–0.42 for post-metastasectomy OS; bilateral mets HR 1.56, 1.27–1.93; **VATS HR 1.69, 1.01–2.82**),
and smaller/fewer nodules are more completely resectable.
HYPOTHESIS: the untested clinical question is therefore not "can we detect relapse earlier" but
"does ctDNA-triggered earlier *surgery* raise the complete-resection rate". That is a trial design
nobody has registered.

FINDING, selection-bias caution on the surgery data: **PMID 38375639** (Ann Surg 2024, systematic
review): 11 studies, 1984–2017, all retrospective, none designed to compare metastasectomy vs none.
3-year survival 0–54% with metastasectomy and 0–16% without, but "no PM patients were usually those
with unresectable disease and/or considered to have a poor prognosis"; **all studies at high risk of
bias; evidence level IV**. Authors call for an RCT while noting it is ethically challenging.
Counterpoint on the upside: **PMID 34674575** (Tumori 2023), 463 consecutive children/AYA at three
Italian centres, 1973–2014, median follow-up 18.6 years: **5-year OS 34.0%, 20-year OS 29.7%
(95% CI 25.5–34.0)**; of 138 alive, **42 (30.4%) had recurrence cured by repeated metastasectomies.**
FINDING. **PMID 42723688** (Transl Lung Cancer Res 2026, 159 patients, 229 metastasectomies,
median follow-up 79.1 months): 3- and 5-year post-metastasis survival 52.2% and 36.0%.
Palpation-assisted mini-thoracotomy found far more occult lesions than VATS (**43.4% vs 6.8%,
p=0.004**) with comparable complications but **no survival difference**. The strongest independent
predictor was **response to pre-operative systemic therapy: 5-year survival 41.1% in responders vs
0.0% in non-responders (HR 0.22, p<0.001)**. Modelling suggested **2–3 months** as the optimal
pre-operative surveillance window.
HYPOTHESIS: that 41.1% vs 0.0% split is a ready-made biology-defined risk stratifier for the
resected setting — the thing the earlier gaps report says osteosarcoma lacks — and it is available
*before* surgery. A trial that enrolled only pre-operative non-responders would be enriching for
an event rate near 100%, which fixes the power problem that killed NCT00752206.

## 5. Drugs that exist and have never reached an osteosarcoma trial

FINDING. ClinicalTrials.gov API v2 queries run 2026-11-14, `query.cond=osteosarcoma` +
`query.intr=<drug>`. Count = number of osteosarcoma studies returned.

| Drug | Target | Osteosarcoma trials |
|---|---|---|
| anakinra, canakinumab, rilonacept | IL-1 | **0, 0, 0** |
| tocilizumab, siltuximab, sarilumab | IL-6 / IL-6R | **1** (NCT04616248, supportive care in an adult CD40-agonist basket trial), 0, 0 |
| reparixin, ladarixin, SX-682, navarixin | CXCR1/2 (IL-8 receptor) | **0, 0, 0, 0** |
| defactinib, VS-6063, IN10018 | FAK | **0, 0, 0** |
| plerixafor, motixafortide, mavorixafor | CXCR4 | **0** (the one "plerixafor" hit, NCT03612466, is a 153Sm-DOTMP trial, WITHDRAWN before enrolment — false match), 0, 0 |
| DKN-01 / sirexatamab, BHQ880 | DKK-1 | **0, 0** |
| pexidartinib, emactuzumab | CSF1R | **0, 0** |
| telaglenastat (CB-839), DRP-104 | glutaminase / glutamine | **0, 0** |
| galunisertib | TGF-beta R1 | **0** (vactosertib does appear in the local trial file) |
| simtuzumab | LOXL2 | **0** |
| maraviroc | CCR5 | **0** |
| nirogacestat | NOTCH / gamma-secretase | **0** |
| beta-glucan, selicrelumab (CD40 agonist) | innate immunity | **0, 0** |
| **admilparant / BMS-986278 (phase 3 in IPF)** | **LPAR1** | **0** |
| AP201 (humanized anti-podoplanin) | PDPN / CLEC-2 | **0** (not registered in any indication) |
| WAY262611, NSC305787/NSC668394 | DKK-1 small molecule, ezrin | tool compounds, no clinical programme |

### The platelet axis — the most complete untested chain I found

FINDING. **PMID 26763081** (Thromb Haemost 2016): tissue factor was highly expressed in **73.6% of
53 pre-treatment osteosarcoma biopsies** and expression associated significantly with disease-free
survival; knockdown reduced **IL-8, CXCL1, SNAI1 and MMP2**; blocking antibodies in 143B-bearing
mice reduced tumour growth, microvessel density and **significantly reduced lung metastasis**.
FINDING. **PMID 34302117** (Oncogene 2021): osteosarcoma cells commonly induce platelet activation;
activated platelets release abundant **lysophosphatidic acid**; **LPAR1** is upregulated in
osteosarcoma (public datasets + in-house PDX); LPAR1 knockout abolished platelet-mediated invasion
and **early pulmonary metastatic foci**; and the **orally available LPAR1 antagonist ONO-7300243
prevented pulmonary metastasis in mouse models**.
FINDING. **PMID 35381070** (Clin Cancer Res 2022): **podoplanin** activates platelets through
CLEC-2; the neutralizing antibody PG4D2 "significantly suppressed tumor growth and pulmonary
metastasis in osteosarcoma xenograft models highly expressing PDPN", and a **humanized IgG4
anti-PDPN antibody, AP201**, suppressed growth and metastasis in vivo "without significant adverse
events". Mechanism: platelet releasate activates PDGFR.
FINDING (own count): platelets/coagulation = 427 papers, 144 metastasis-focused, 15 with in vivo
metastasis endpoints. No osteosarcoma trial of any anti-platelet or LPAR1 agent.
FINDING (a free natural experiment). **NCT03244020** (Massachusetts General Hospital, phase 4,
**randomized, n=2,868 estimated, ENROLLING_BY_INVITATION since 2018-02, completion 2028-07**)
randomizes **aspirin 325 mg daily vs enoxaparin** for VTE prophylaxis after orthopaedic oncology
surgery, with a **dedicated "primary bone tumor" stratum**. Primary outcome is venous
thromboembolism, not metastasis.
HYPOTHESIS: this trial is already randomizing bone-sarcoma patients to an anti-platelet drug versus
an anticoagulant in the peri-operative window. An **exploratory metastasis-free-survival analysis
of the primary-bone-tumour stratum costs nothing but a data request**, and it is the cheapest
possible test of the platelet-metastasis hypothesis in humans. (It is not a clean test: aspirin vs
LMWH is not aspirin vs nothing, LMWH has its own anti-metastatic literature, and the trial is not
powered or stratified for this.)

## 6. Top overlooked opportunities (HYPOTHESES, each with evidence, drug, cheapest test)

See the report for the written-up version. Ranked list:
1. IL-1 blockade in the post-surgical window (anakinra/canakinumab). Evidence PMID 40882022
   (IL-1alpha from lung epithelium initiates the IL-6/CXCL8 programme; pharmacologic IL1
   disruption reduced metastatic progression), PMID 30135299, PMID 41209004 (IL-6 rises after
   amputation and after chemotherapy and tracks falling cytotoxicity). Drug: anakinra, generic-ish,
   paediatric safety record in systemic JIA. Cheapest test: pet-dog adjuvant study after amputation.
2. CXCR1/2 blockade (SX-682 oral, reparixin, ladarixin). Evidence PMID 30135299, 38302407
   (anti-IL-8 antibody reduced lung metastasis in vivo), 32079335 + 34760697 (lung-endothelial
   CXCL1 -> CXCR2 -> FAK -> VCAM-1). Zero trials. Cheapest test: SX-682 in the K7M3 syngeneic
   lung-colonization model, then dogs.
3. The platelet axis (LPAR1 antagonist, anti-PDPN). Evidence PMIDs 26763081, 34302117, 35381070.
   Drug: admilparant/BMS-986278 is in phase 3 for IPF. Cheapest test: the NCT03244020 secondary
   analysis, plus admilparant in an orthotopic-amputation mouse model.
4. Defactinib (FAK) as the convergence node. Evidence PMID 42520958, 37013056, 36997926, 38302407,
   32079335 — FAK sits downstream of IL-8, CXCL1, integrins and LOX. FDA-approved 2025, zero
   osteosarcoma trials, NIH-funded at a veterinary school (Regan, Colorado State).
   Cheapest test: pet-dog adjuvant trial — this is lead 4 of `Ranked leads` (the note originally said lead 1, which is IL-1/IL-6 blockade).
5. Re-run the resected-lung randomized question, enriched on pre-operative non-response.
   Evidence PMID 42723688 (5-year survival 41.1% responders vs 0.0% non-responders, HR 0.22,
   p<0.001) + NCT00752206 (38 patients in 8.75 years, stopped for accrual). Cheapest test: a
   FOSTER-platform arm (NCT07871864) restricted to non-responders, where event rates approach 100%.
6. ctDNA-triggered *earlier surgery*, not earlier drugs. Evidence PMID 42036655 (complete
   resection HR 0.21), PMID 42824543, PMID 39360936. Cheapest test: a single-arm feasibility study
   measuring complete-resection rate against the retrospective rate.
7. The pre-metastatic niche in dogs as a ready-made platform. Evidence PMID 39526499 (CD204+,
   CD206+ macrophages and CD11d+ BMDCs raised in pre-metastatic canine lung; recruitment transient),
   PMID 41648517 (canine OS the most faithful cross-species model). Cheapest test: use lung biopsy
   / BAL macrophage counts as the pharmacodynamic endpoint for any niche-directed drug in dogs,
   which turns a 2-year survival endpoint into a 4-week biomarker endpoint.
8. Lung interface adaptive resistance (FGFR). Evidence PMID 42856637 (preprint): ERK-high cells
   enriched at the tumour-lung interface; tumour lysis amplifies FGFR-ERK in neighbours;
   fexagratinib or pazopanib suppressed it. Cheapest test: add an FGFR inhibitor to an existing
   cytotoxic in the ex vivo pulmonary metastasis culture that paper already built.
9. Glutamine metabolism: 5 in vivo metastasis papers in 33,242; telaglenastat and DRP-104 are
   clinical-stage; zero trials. Cheapest test: a lab experiment, not a trial.
10. Ezrin: ~20 years of in vivo metastasis evidence (17 papers), zero clinical-grade inhibitor.
   This is a medicinal-chemistry gap. Cheapest useful act: say so publicly so nobody mistakes
   "no trial" for "no evidence".

## 7. Limits of this analysis

- All mechanism counts are **keyword matches on title+abstract**, not curation. "In vivo metastasis"
  means the abstract contains an animal term, metastasis wording and a metastasis-model phrase; it
  does **not** mean the mechanism was blocked and metastasis measured as the endpoint.
- Mechanism regexes overlap deliberately (a paper can count under IL-6, STAT3 and macrophages), so
  columns do not sum.
- Abstracts only for essentially everything. Full text was retrieved for nothing except what Europe
  PMC returned as an abstract; PMC HTML was blocked by a captcha and europepmc.org was not
  reachable through this workspace's proxy.
- The 33k PubTator file is a snapshot; "no trial exists" claims rest on ClinicalTrials.gov only
  (no EudraCT, ISRCTN, ChiCTR or jRCT), so a Chinese or Japanese registry trial of, say,
  tocilizumab in osteosarcoma would be missed.
- Two of the strongest mechanistic papers (PMID 41648517, 42856637) are **bioRxiv preprints**.
- Dog trial results are single-arm against historical controls, with the same bias problem as the
  human single-arm trials.

## 8. A worked check on the method's error rate

My script counts **37 GM-CSF (CSF2) papers and 0 with an in vivo metastasis endpoint.** Taken at
face value that would say inhaled GM-CSF reached a 43-patient COG trial on no animal metastasis
evidence. But PMID 20576718's own first sentence is "Based on preliminary data on the antitumor
effects of GM-CSF in animal models, and promising phase I trials, we embarked on a feasibility
study". So the preclinical work exists and my regex missed it (indexed under other terms, or in
papers without "osteosarcoma" in title/abstract).
CONCLUSION: every zero in the mechanism table should be read as "these keywords found none in this
33k corpus", not "none exists". The trial-level zeros (ClinicalTrials.gov drug-by-drug queries in
section 5) are much more reliable than the paper-level zeros, because they are exact-name lookups
against a single registry rather than regex over abstracts.

## 9. Files produced

- `tools/lung_metastasis_map.py` — the analysis script (re-runnable, no network needed).
- `data/lung_metastasis_mechanisms.csv` — 56 mechanisms x paper counts, with up to 40 in-vivo-metastasis PMIDs each.
- `data/lung_metastasis_papers.csv` — one row per metastasis-focused research paper (9,130 rows) with flags.
- `data/lung_metastasis_trials.csv` — the 224 lung/metastasis-mentioning trials, with a `lung_directed` flag marking the 73 explicitly lung-directed ones.
- `reports/Stopping lung metastasis in osteosarcoma.md` — the reader-facing report.
