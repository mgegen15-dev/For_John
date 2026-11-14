# Lung metastasis in osteosarcoma — working notes

*Started 2026-11-14. Separate FINDING (seen in a source) from HYPOTHESIS (my inference).
Every finding carries a PMID / NCT / URL. "abstract-only" marks claims read only from an abstract.*

Context already read (not redone): `reports/Osteosarcoma and neuroblastoma research gaps.md`,
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
