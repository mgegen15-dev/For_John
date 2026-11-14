# Research brief: FAK or DKK1 blockade against lung metastasis in dogs with osteosarcoma

*For John project · November 2026 · Every paper this brief relies on was read in full where it was available, and the brief was checked by an independent audit on November 14, 2026. Supporting data and methods: this repository. Not medical advice.*

## Summary

Most children who die of osteosarcoma die because it spreads to the lungs, and in forty years no drug added to standard chemotherapy has clearly reduced that. FAK and DKK1 are two of the best-supported drug targets against lung spread that have not reached a human osteosarcoma trial: in mice, blocking either one reduced lung metastasis in small studies. Pet dogs get the same cancer naturally, and work in dogs on both targets has already begun: Colorado State University has given the approved FAK drug defactinib to dogs with osteosarcoma, and Texas A&M is preparing a dog version of a DKK1-blocking drug for trials in pet dogs. This brief asks what those programmes have found, and what a study aimed at *preventing* lung spread after amputation would still need. It is based on published work, not new experiments.

**How to read the labels.** After key numbers we say where they come from:

- **(registry)**: an official database record, such as ClinicalTrials.gov, NIH RePORTER or an FDA notice.
- **(paper, full text)**: read in the full published paper.
- **(paper, abstract only)**: read only in the abstract.
- **(press release only)**: from a company announcement, conference coverage or a web listing, with no peer-reviewed paper.
- **(our calculation)**: counted or computed by this project.

## The question

Can blocking FAK or DKK1, with drugs that already exist or are being built for dogs, reduce lung metastasis after amputation in dogs with naturally occurring osteosarcoma?

## Why these two targets

We scored all 1,494 genes named in at least five of the 33,242 osteosarcoma papers we downloaded from PubMed (our calculation; a PubMed title/abstract search returned 33,367 on November 14, 2026). We linked each gene to the 603 registered osteosarcoma treatment trials and to NIH grants (our calculation; `data/`), read the abstracts for the strongest untested candidates, then read the full text of every paper this brief relies on. Verification notes: `research_notes/Osteosarcoma literature map/fak_dkk1_full_text_check.md`.

The two targets have different strengths:
- **FAK** has an approved drug, defactinib, that has already been given to dogs with osteosarcoma, and one small mouse study in which defactinib itself reduced lung metastasis.
- **DKK1** has more mouse evidence against metastasis, including in the implant-amputate-watch design a dog study would copy, and a dog-specific DKK1 drug is in preclinical development. The clinical anti-DKK1 antibody has not, as far as we found, been given to dogs.

### FAK (PTK2)

- **Mouse evidence:** two studies, one with each kind of readout.
  - **Defactinib against lung metastasis** (Chen et al., Genes & Diseases 2023, Baylor College of Medicine; PMID 37013056). Human 143B osteosarcoma cells engineered to overexpress LOX, an enzyme that raises FAK activity, were injected into the shin bone of immune-deficient mice, 6 per arm. Oral defactinib from one week after injection, twice daily for three weeks, left 2 of 6 mice with microscopic lung metastases against 6 of 6 controls (P = 0.03), with no significant change in primary tumour weight (P = 0.108) (paper, full text). Limits: very small, one engineered cell line chosen for high LOX, no amputation step, and a dose printed as 50 μg/kg, far below usual mouse doses, which we cannot explain from the paper.
  - **PF562271 against growth** (PMID 28406574). This oral FAK inhibitor halved tumour volume and weight and reduced blood-vessel density in 143B tumours under the skin (50 mg/kg twice daily, n = 6 per group). Metastasis was not measured, the model was not in bone, and sensitivity did not track FAK activity across six cell lines (paper, full text).
  - A 2026 study reports that FAK activation mediates IQGAP3-driven lung metastasis in osteosarcoma (paper, abstract only; PMID 42520958).
- **Patient evidence:**
  - Activated FAK (pY397) is high in 62% of tumours (33 of 53). It predicted survival only in the 33 patients who had metastases (hazard ratio 2.32, P = 0.048), not across all 53, although it was linked to poor response to chemotherapy in all patients (paper, full text; PMID 28846700). The planned dog population, after amputation, is the setting where this marker was *not* prognostic.
  - A three-protein panel (beta5 integrin, FAK, GSK3beta) separated good from poor chemotherapy responders in 36 pre-treatment biopsies (paper, abstract only; PMID 23845472). It is a single small series, and without the full text we could not check whether it was validated on an independent set.
- **Contradicting evidence:** narrow. Two in-vitro papers question FAK's role in specific processes (PMIDs 16759849, 12376862). In a PubMed search of FAK inhibitors in osteosarcoma animal models, we found no study reporting failure.
- **Literature quality:** 1 retraction in 95 FAK osteosarcoma papers since 2010 (our calculation).
- **Drug:** defactinib, FDA accelerated approval on 8 May 2025 with avutometinib for KRAS-mutant recurrent low-grade serous ovarian cancer (registry).
- **In dogs:** Colorado State University's Flint Animal Cancer Center lists a study adding oral defactinib to the losartan–toceranib regimen in dogs with lung-metastatic osteosarcoma, with drug-level (pharmacokinetic) sampling (press release only: web listing; enrolment status and results not found). Colorado State's NIH FAK grant (R37 CA303990, September 2025 to August 2030) separately plans to test a FAK inhibitor with platinum chemotherapy in dogs with naturally occurring osteosarcoma (registry).
- **Human trials:** none registered in osteosarcoma (registry).

### DKK1

- **Mouse evidence:** three ways of blocking DKK1 have been tested, from two laboratories, plus one independent group.
  - **An anti-DKK1 antibody, BHQ880** (Novartis; a different antibody from DKN-01), slowed growth of two patient-derived tumours implanted in bone and then amputated (PMID 27049730). Metastasis fell from 6 of 18 control mice to 4 of 27 treated mice, which was not significant as randomized (P = 0.17); it reached P = 0.03 only after three treated mice with local recurrence were excluded (paper, full text).
  - **A DKK1-blocking morpholino** reduced lung metastasis in the same patient-derived model, from 7 of 9 control lungs to 2 of 10 treated lungs positive for human tumour DNA, and preserved bone (paper, full text; PMID 39805917). This is the strongest single metastasis result for DKK1. An earlier paper from that laboratory preserved bone but could not detect lung metastases, so it does not support a metastasis claim (paper, full text; PMID 35277659).
  - **A small-molecule DKK1 inhibitor, WAY262611,** reduced metastasis in the antibody laboratory's own model (paper, abstract only; PMID 39781890; PMID 39713389 is its preprint, not a separate study). A free preprint version exists (PMC11661202), so its numbers can be checked; we have not yet done so.
  - **An independent group** in China reported that an oral compound that lowers DKK1 reduced lung metastasis and bone destruction in an orthotopic model, with methotrexate as an active comparator (paper, full text; PMID 39280613).
- **Caution:**
  - The decisive work comes from two laboratories (Loeb, Johns Hopkins then Albert Einstein; Gregory, Texas A&M), and they are less independent than they look. The antibody and small-molecule results come from the same laboratory, and the morpholino laboratory deliberately used the antibody laboratory's patient-derived model so the results could be compared.
  - One older paper found that *raising* DKK1 inhibits osteosarcoma growth (paper, abstract only; PMID 24859848).
  - Two of 28 DKK1 osteosarcoma papers since 2010 are retracted (our calculation).
  - Independent replication, in a model neither laboratory owns, is the priority.
- **Drugs:**
  - DKN-01 (sirexatamab), an anti-DKK1 antibody in clinical trials for gastric and other cancers. We found no report of it being given to dogs.
  - A canine DKK1 morpholino (cDkkMo) is being developed at Texas A&M under NIH grant R21 CA286523 (January 2025 to December 2027), "with the ultimate goal of performing veterinary clinical trials in client-owned dogs with OS". The grant tests it in canine osteosarcoma cell lines and canine patient-derived tumours in mice, alone and with cisplatin (registry).
- **Human trials:** none registered in osteosarcoma (registry).

### What neither target has yet

No published study has reported FAK, activated FAK or DKK1 protein in dog osteosarcoma tumours (PubMed search, November 2026). RNA levels could already be read from public canine osteosarcoma RNA sequencing (for example Gardner et al. 2019, PMID 31341965), and the Texas A&M grant's first aim characterises DKK1 in canine osteosarcoma models.

## Why dogs

- Pet dogs develop osteosarcoma far more often than people, about ten times as often by a commonly cited estimate, and the disease is biologically similar.
- Most dogs die of lung metastases within a year or two even with chemotherapy (review, PMID 32165755). In a 324-dog randomized trial of standard care with or without sirolimus, median survival was about 282 days (paper, abstract only; PMID 33753454).
- A post-amputation study can test anti-metastatic drugs, the gap that matters most for children, within one to two years.
- NIH funds canine osteosarcoma studies through the NCI Comparative Oncology Program and cooperative agreements at UC Davis (U01 CA281905) and Tufts (U01 CA272268) (registry). Break Through Cancer's family-funded Defying Osteosarcoma TeamLab, launched in 2025, also includes comparative canine trials (press release only).

## Why it is timely

- NIH funds osteosarcoma work on both targets: FAK inhibition at Colorado State's veterinary school (R37 CA303990, to August 2030), DKK-1 at Albert Einstein College of Medicine (R01 CA262802, funded through June 2026) and the canine DKK1 morpholino at Texas A&M (R21 CA286523, to December 2027) (registry).
- VEGFR2-blocking kinase pills are the only drug class clearly above the historical benchmark in relapsed osteosarcoma, but their benefit is brief and they have not improved survival (`reports/Why kinase-inhibitor pills work in osteosarcoma.md`). New anti-metastatic candidates are needed.
- Our close reading of MDM2, the most-studied untested target, found its osteosarcoma evidence weaker than its paper count suggests (`research_notes/Osteosarcoma literature map/orphan_targets_close_read.md`), which leaves FAK and DKK1 as the stronger candidates.

## A possible design, for discussion

- **Population:** client-owned dogs with limb osteosarcoma, after amputation and standard carboplatin, with no visible lung metastases.
- **Arms:** standard care with or without defactinib (or a DKK1 blocker: the canine morpholino once ready, or DKN-01 if it can be supplied), randomized, or single-arm against the large historical canine control data.
- **Endpoint:** time to lung metastasis. Activated FAK in the amputated tumour, or DKK1 in blood, would be measured to define who benefits. In the BHQ880 mouse study, human DKK1 was measurable in mouse blood and tracked tumour growth (paper, full text); whether it gives early warning of metastasis is not established, and no canine assay or threshold exists yet, so one would have to be built first.
- **Before the dog study:** measure FAK, activated FAK and DKK1 in banked canine osteosarcoma tissue, read their RNA levels from public canine data, and confirm drug activity in canine osteosarcoma cell lines. These are small, cheap steps, and for DKK1 the Texas A&M programme is already doing part of the last one.

## What we are asking

1. **FAK:** what did the Colorado State defactinib study in dogs show, and is it still enrolling? Could the canine FAK study planned under the R37 grant include dogs after amputation with metastasis-free survival as an endpoint?
2. **DKK1:** when might the canine DKK1 morpholino be ready for client-owned dogs, and would an independent expression survey or replication help? Could DKN-01 (sirexatamab) be supplied for a canine study?
3. **Both:** would a post-amputation pet-dog study be feasible through an existing consortium, and roughly what would it cost? What evidence would you need first?

## Caveats

- These findings come from analysis of published work, not from new experiments.
- For FAK, the only mouse study that measured metastasis is small (6 mice per arm), uses one engineered cell line and reports an unusual dose; it needs repeating.
- For DKK1, the decisive mouse results come from two laboratories sharing one model; the independent result uses a different compound and a rat cell line.
- The Colorado State canine study details come from a web listing we could not open directly.
- Two papers (PMIDs 23845472 and 39781890) were read only as abstracts.

**Supporting files:**
- `research_notes/Osteosarcoma literature map/fak_dkk1_full_text_check.md`
- `research_notes/Osteosarcoma literature map/orphan_targets_close_read.md`
- `research_notes/Audit/audit_A_gaps_leads_brief.md`
- `reports/Osteosarcoma literature map.md`
- `reports/Evidence risk flags for osteosarcoma genes.md`
- `reports/Ranked leads and research partners.md` (lead 4)

## Change log

- **November 14, 2026 (independent audit).**
  - FAK: the brief said there was no mouse evidence against metastasis and that the only mouse efficacy study used a different drug. That was wrong. Defactinib itself reduced lung metastasis in an orthotopic mouse model (2 of 6 against 6 of 6, P = 0.03; PMID 37013056, read in full). The framing of the two targets was rewritten.
  - DKK1: added the canine DKK1 morpholino being developed for trials in pet dogs (NIH R21 CA286523), which the brief had missed. "DKN-01 has never been given to a dog" softened to "we found no report".
  - Added Colorado State's R37 plan for a canine FAK study; the Einstein DKK-1 grant is now described as funded through June 2026, its project end date.
  - "No study has measured FAK or DKK1 in dog tumours" narrowed to protein in published studies, noting that public canine RNA data exist.
  - "Over 90% of dogs die within two years" replaced with a sourced statement.
  - The serum DKK1 endpoint claim was narrowed to what the mouse paper shows.
  - The questions now ask about the existing dog programmes, and the design now specifies dogs without visible metastases.
- **Earlier in November 2026 (full-text check).** Every cited paper was read in full where available. This corrected the DKK1 evidence (two laboratories, not three; one paper counted twice; one antibody result significant only after exclusions) and added the Colorado State defactinib dog study.
