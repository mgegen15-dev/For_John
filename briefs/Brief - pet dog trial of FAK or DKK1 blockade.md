# Research brief: FAK or DKK1 blockade against lung metastasis in dogs with osteosarcoma

*For John project · November 2026 (revised after a full-text check of every cited paper) · Supporting data and methods: this repository. Not medical advice.*

## The question

Can blocking FAK or DKK1, with drugs that already exist, reduce lung metastasis after amputation in dogs with naturally occurring osteosarcoma?

## Why these two targets

We scored all 1,494 genes named in at least five of the 33,242 osteosarcoma papers in PubMed. We linked each to the 603 registered osteosarcoma treatment trials and to NIH grants, read the abstracts for the strongest untested candidates, then read the full text of every paper this brief relies on. Full verification notes: `research_notes/Osteosarcoma literature map/fak_dkk1_full_text_check.md`.

The two targets have opposite strengths:
- **FAK** has a drug already given to dogs, but no mouse evidence against metastasis.
- **DKK1** has mouse evidence against metastasis, in the same implant-amputate-watch design a dog study would copy, but no dog has received the drug.

### FAK (PTK2)

- **Mouse evidence:** PF562271, an oral FAK inhibitor, halved tumour volume and weight and reduced blood-vessel density in subcutaneous 143B xenografts (50 mg/kg twice daily, n = 6 per group; PMID 28406574). This supports FAK as a growth target, not yet as an anti-metastatic one:
  - metastasis was not measured;
  - the model was subcutaneous rather than in bone;
  - sensitivity did not track FAK activity across six cell lines;
  - the drug is not defactinib.
- **Patient evidence:**
  - Activated FAK (pY397) is high in 62% of tumours (33 of 53; PMID 28846700). It predicted outcome only in the 33 patients who already had metastases (hazard ratio 2.32, P = 0.048), not across all patients.
  - A three-protein panel (beta5 integrin, FAK, GSK3beta) separated good from poor chemotherapy responders in 36 pre-treatment biopsies (PMID 23845472). This is a single small series, and we could not obtain the full text to check whether it was validated on an independent set.
- **Contradicting evidence:** narrow. Two in-vitro papers question FAK's role in specific processes (PMIDs 16759849, 12376862). No paper tests a FAK inhibitor and reports failure.
- **Literature quality:** clean, with 1 retraction in 95 papers since 2010.
- **Drug:** defactinib, FDA-approved (accelerated approval) on 8 May 2025 with avutometinib for KRAS-mutant low-grade serous ovarian cancer.
- **In dogs:** Colorado State University's Animal Cancer Center lists a canine study adding oral defactinib to the losartan–toceranib regimen in dogs with lung-metastatic osteosarcoma, with drug-level (pharmacokinetic) sampling. We could not confirm its enrolment status or find results; that is the first question to ask.
- **Human trials:** none registered in osteosarcoma.

### DKK1

- **Mouse evidence:** three ways of blocking DKK1 have been tested, from two laboratories:
  - **An anti-DKK1 antibody, BHQ880** (Novartis; a different antibody from DKN-01), slowed growth of two patient-derived xenografts implanted in bone and then amputated (PMID 27049730). It reduced metastasis from 6 of 18 control mice to 4 of 27 treated mice. That was not significant as randomized (P = 0.17), and reached P = 0.03 only after three treated mice with local recurrence were excluded.
  - **A DKK1-blocking morpholino** reduced lung metastasis in the same patient-derived model, from 7 of 9 control lungs to 2 of 10 treated lungs positive for human tumour DNA, and preserved bone (PMID 39805917). This is the strongest single metastasis result for either target. An earlier paper from that lab preserved bone but could not detect lung metastases, so it does not support a metastasis claim (PMID 35277659).
  - **A small-molecule DKK1 inhibitor, WAY262611,** reduced metastasis in the antibody lab's own model (PMID 39781890; PMID 39713389 is its preprint, not a separate study). We could read only its abstract.
  - **An independent group** in China reported that an oral compound that lowers DKK1 reduced lung metastasis and bone destruction in an orthotopic model, compared against methotrexate (PMID 39280613).
- **Caution:**
  - The decisive work comes from two laboratories (Loeb, Johns Hopkins then Albert Einstein; Gregory, Texas A&M), and they are less independent than they look. The antibody and small-molecule results come from the same lab, and the morpholino lab deliberately used the antibody lab's patient-derived model so the results could be compared.
  - One older paper found that *raising* DKK1 inhibits osteosarcoma growth (PMID 24859848).
  - Two of 28 papers since 2010 are retracted.
  - Independent replication, in a model neither lab owns, is the priority.
- **Drug:** DKN-01 (sirexatamab), in clinical trials for gastric and other cancers. It has never been given to a dog.
- **Human trials:** none registered in osteosarcoma.

**Neither target has any canine osteosarcoma expression data.** No study has measured FAK, activated FAK or DKK1 in dog tumours.

## Why dogs

- Pet dogs develop osteosarcoma about ten times as often as people, and the disease is biologically similar.
- Over 90% of dogs die of lung metastases within two years of amputation.
- A post-amputation study can test anti-metastatic drugs, the gap that matters most for children, within one to two years.
- NIH already funds canine osteosarcoma studies through the NCI Comparative Oncology Program and cooperative agreements at UC Davis and Tufts.

## Why it is timely

- NIH already funds osteosarcoma work on both targets: FAK inhibition at Colorado State (a veterinary school, R37), and DKK-1 at Albert Einstein College of Medicine (R01 CA262802) and Texas A&M (R21 CA286523).
- Kinase-inhibitor pills are the only drug class clearly above the historical benchmark in relapsed osteosarcoma, but their benefit is brief (`reports/Why kinase-inhibitor pills work in osteosarcoma.md`). New anti-metastatic candidates are needed.
- MDM2, the most-studied untested target, does not hold up on close reading, which narrows the field to these two.

## A possible design, for discussion

- **Population:** client-owned dogs with appendicular osteosarcoma, after amputation and standard carboplatin.
- **Arms:** standard care with or without defactinib (or DKN-01), randomized, or single-arm against the large historical canine control data.
- **Endpoints:** time to lung metastasis. Activated FAK in the amputated tumour, or serum DKK1, would be measured to define who benefits. DKK1 in blood fell to undetectable on treatment in mice and rose just before metastasis, but no canine assay or threshold exists yet, so one would have to be built first.
- **Before the dog study:** measure FAK, activated FAK and DKK1 in banked canine osteosarcoma tissue, and confirm drug activity in canine osteosarcoma cell lines. Both are small, cheap steps.

## What we are asking

1. **FAK:** what did the Colorado State defactinib study in dogs show, and is it still enrolling?
2. **DKK1:** could DKN-01 (sirexatamab) be supplied for a canine study, and who could run an independent replication in a model neither lab owns?
3. **Both:** would a post-amputation pet-dog study be feasible through an existing consortium, and roughly what would it cost? What evidence would you need first?

## Caveats

- These findings come from analysis of published work, not from new experiments.
- For DKK1, the decisive mouse results come from two laboratories sharing one model.
- For FAK, the only mouse efficacy study did not measure metastasis.
- The Colorado State canine study details come from a web listing we could not open directly.
- Two papers (PMIDs 23845472 and 39781890) could be read only as abstracts.

**Supporting files:**
- `research_notes/Osteosarcoma literature map/fak_dkk1_full_text_check.md`
- `research_notes/Osteosarcoma literature map/orphan_targets_close_read.md`
- `reports/Osteosarcoma literature map.md`
- `reports/Evidence risk flags for osteosarcoma genes.md`
- `reports/Ranked leads and research partners.md`
