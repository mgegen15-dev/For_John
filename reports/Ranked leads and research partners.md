# For John: the best leads, and who could test them

*Revised November 14, 2026 (second ranking), after four further research threads: kinase-inhibitor pills, tumour-surface targets, lung metastasis, and a full-text check of the FAK and DKK1 evidence. This ranks every open lead from the project's reports and matches each to the groups best placed to act on it. Partners come from public NIH grant records (`data/nih_osteosarcoma_projects.csv`), ClinicalTrials.gov sponsors and the published literature. Nobody named here has been contacted or has endorsed anything in this document.*

**Scope.** Osteosarcoma is the target. Ideas are borrowed from anywhere: other sarcomas, neuroblastoma, adult cancers, other diseases, and dogs.

## How leads are scored

Each lead is scored 1 to 3 on four things, for a total out of 12:

- **Evidence:** how well the underlying finding holds up after checking.
- **Open:** whether it is still undone. A lead already under way scores low.
- **Feasibility:** how cheaply and quickly it could be done.
- **Impact:** whether it could change outcomes for patients with metastatic or relapsed disease, the patients osteosarcoma kills.

## The ranking

| Rank | Lead | Evidence | Open | Feasibility | Impact | Total | Change since first ranking |
|---|---|---|---|---|---|---|---|
| 1 | Block IL-1 or IL-6 after surgery to stop lung metastasis | 2 | 3 | 2 | 3 | **10** | New, from the lung metastasis report |
| 2 | Test whether gene amplifications predict who benefits from kinase-inhibitor pills | 2 | 3 | 2 | 3 | **10** | New, from the kinase-inhibitor report |
| 3 | Publish the pooled control dataset | 3 | 2 | 3 | 2 | **10** | Was lead 2; much of the work is now done |
| 4 | Pet-dog study of FAK or DKK1 blockade | 2 | 2 | 2 | 3 | **9** | Was lead 1. Defactinib has already been given to dogs; mouse evidence is thinner than first thought |
| 5 | Confirm LRRC15 and PTK7 as new surface targets | 2 | 2 | 2 | 3 | **9** | New, from the surface-targets report |
| 6 | Randomized trial after lung-metastasis surgery, run inside a platform | 3 | 2 | 1 | 3 | **9** | Was lead 4; one earlier attempt was found, abandoned for slow recruitment |
| 7 | Block the IL-8 receptor (CXCR1/2) against lung metastasis | 2 | 3 | 2 | 2 | **9** | New |
| 8 | Treatment adapted on ctDNA blood tests | 2 | 2 | 2 | 3 | **9** | Unchanged |
| 9 | Add metastasis to an existing aspirin-versus-blood-thinner trial | 2 | 3 | 2 | 2 | **9** | New |
| 10 | Chase the remaining unreported trials | 2 | 2 | 3 | 1 | **8** | Was lead 3; three "lost" trials turned out to be published |
| 11 | Re-analyse dog genomes from NCI's canine trials | 2 | 3 | 2 | 1 | **8** | Unchanged |

**Done:** the paper-mill risk flag (`reports/Evidence risk flags for osteosarcoma genes.md`).

**Dropped:**
- **MDM2 inhibitors.** The evidence rests on one cell line, and the target is common only in low-grade osteosarcoma that surgery usually cures.
- **Cyclin E1 (CDK2 inhibitors).** The weakest of the four targets read in full.
- **Metronomic maintenance chemotherapy.** Tested in 296 children in Brazil, with no benefit (published 2017).

## The leads in detail

### 1. Block IL-1 or IL-6 after surgery to stop lung metastasis

**Why:**
- Lung tissue releases IL-1α, which drives osteosarcoma cells to make IL-6 and IL-8 and colonize the lung. Blocking IL-1, or IL-6 together with IL-8, cut lung metastasis in mice (PMIDs 40882022, 30135299).
- A canine trial of the opposite approach, boosting immunity with inhaled IL-15 after amputation, was stopped for futility and did *worse* than historical controls (NCI-COTC030, PMID 41209004). Its own data showed surgery and chemotherapy raise IL-6.
- That suggests the weeks after surgery may be the time to *block* inflammation, not stimulate it.
- The drugs are approved and inexpensive: anakinra (IL-1) and tocilizumab (IL-6), the latter available as biosimilars. Neither has an osteosarcoma trial.
- IL-6 has a clean osteosarcoma literature (3% template papers, `reports/Evidence risk flags for osteosarcoma genes.md`).

**Cheapest test:** a pet-dog study after amputation, using lung macrophage changes at four weeks as an early readout (PMID 39526499).

**Partners:**
- NCI Comparative Oncology Program, which ran COTC030 and holds its data.
- Ryan Roberts, Nationwide Children's, who holds an NIH grant on mechanisms of metastatic colonization.
- UC Davis (Robert Rebhun, Robert Canter), who ran the canine inhaled IL-15 work.

**Details:** `reports/Stopping lung metastasis in osteosarcoma.md`.

### 2. Do gene amplifications predict who benefits from kinase-inhibitor pills?

**Why:**
- Kinase-inhibitor pills are the only drug class clearly above the relapse benchmark, but the benefit lasts months. In both randomized pill-plus-chemotherapy trials, overall survival was numerically shorter with the pill.
- About 40% of osteosarcomas carry extra copies of the genes these pills target (VEGFA, or KDR/PDGFRA/KIT).
- No clinical study has checked whether those patients are the ones who respond. If they are, the pills could be given to the patients they help, and not to the rest.

**Cheapest test:** genotype archived tumour or banked blood DNA from the randomized trials (SARC024, REGOBONE, OLIE, OAIE) and the single-arm trials (CABONE, COG ADVL1622). Using the randomized trials allows a true drug-versus-control comparison.

**Partners:**
- SARC (SARC024).
- The French Sarcoma Group (REGOBONE).
- Eisai and the ITCC consortium (OLIE).
- COG (ADVL1622).
- Richard Gorlick, MD Anderson, who runs NIH-funded genomically selected drug testing in patient-derived models.

**Details:** `reports/Why kinase-inhibitor pills work in osteosarcoma.md`.

### 3. Publish the pooled control dataset

**Why:**
- The dataset now holds results from about 60 trials, roughly half from the registry and half from papers. It shows the 12% benchmark is wrong for chemotherapy combinations, because ifosfamide and etoposide alone keep 42–66% of patients progression-free at four months.
- A short paper or preprint would make the dataset citable.

**Partners:**
- FOSTER, through the Bone Cancer Research Trust, which funds it.
- COG bone tumour committee.
- Pediatric Cancer Data Commons.

**We can do most of this ourselves**, ideally with a scientist co-author.

### 4. Pet-dog study of FAK or DKK1 blockade

**Why:** these are still the best-supported untested drug targets, but the full-text check changed the picture.
- **FAK:**
  - Defactinib, FDA-approved in 2025, has already been given to dogs with metastatic osteosarcoma in a Colorado State study; results not yet found.
  - The only mouse study did not measure metastasis.
- **DKK1:**
  - The best mouse result held up: lung metastasis in 2 of 10 treated against 7 of 9 untreated.
  - An independent group reported the same direction.
  - The drug, DKN-01, has never been given to a dog.
- The lung metastasis report adds a reason to favour FAK: it sits where several metastasis signals converge (IL-8, CXCL1, integrins).

**Partners:**
- Daniel Regan, Colorado State: holds the NIH FAK grant and is at the veterinary center running the defactinib dog study.
- David Loeb, Einstein, and Carl Gregory, Texas A&M: hold the NIH DKK-1 grants.
- NCI Comparative Oncology Program.

**Details:** `briefs/Brief - pet dog trial of FAK or DKK1 blockade.md`.

### 5. Confirm LRRC15 and PTK7 as new surface targets

**Why:**
- In 88 patient tumours compared with 54 normal tissues, LRRC15 and PTK7 were made in almost every osteosarcoma and very little in vital organs. The same method ranked B7-H3, the current leading target, 15th, and HER2, which failed, near the bottom.
- **LRRC15:** drug companies have just opened two sarcoma trials, one naming osteosarcoma. Following them matters more than starting anything new.
- **PTK7:** four antibody-drug conjugates are already in early trials for other cancers, but osteosarcoma has fewer than five papers on it.

**Cheapest test:** stain banked osteosarcoma tumours, including lung metastases and relapses, for PTK7 and LRRC15 protein. The finding so far is based on RNA only.

**Partners:**
- The companies developing PTK7 drugs (HWK-007, KIVU-107, DAY301).
- The LRRC15 trial sponsors (SOT106, ZL-6201).
- Any group with an osteosarcoma tissue microarray, such as COG's biobank or FOSTER's sample programme.

**Details:** `reports/New surface targets for osteosarcoma.md`.

### 6. Randomized trial after lung-metastasis surgery, run inside a platform

**Why:**
- Single-arm trials in this setting cannot separate a drug's effect from who gets enrolled. Two very different drugs gave almost identical results (26% and 28% event-free at 12 months).
- A randomized, placebo-controlled saracatinib trial was tried (NCT00752206). It needed over eight years to enrol 38 patients and was abandoned, with a non-significant 19.4 against 8.6 months progression-free.
- So the obstacle is recruitment. The question needs a large platform such as FOSTER's new one (NCT07871864), possibly enriched for patients whose metastases did not respond to chemotherapy before surgery.

**Partners:** FOSTER; COG bone tumour committee.

### 7. Block the IL-8 receptor (CXCR1/2)

**Why:**
- An anti-IL-8 antibody blocked lung metastasis in mice (PMID 38302407).
- Signalling through the CXCR2 receptor helps osteosarcoma cells stick to lung blood vessels (PMIDs 32079335, 34760697).
- Oral CXCR1/2 blockers exist (SX-682, reparixin, ladarixin), and none has an osteosarcoma trial.
- This fits naturally alongside lead 1.

**Partners:** same as lead 1.

### 8. Treatment adapted on ctDNA blood tests

**Why:**
- Tumour DNA in the blood predicts relapse; the LEOPARD study (NCT06068075) validated it at diagnosis.
- The lung metastasis report adds a specific use: ctDNA could trigger earlier lung surgery, with complete removal as the outcome.
- No trial yet changes treatment based on ctDNA. Earlier detection by scans alone has not been shown to improve survival.

**Partners:** Brian Crompton and David Shulman, Dana-Farber, who hold the NIH ctDNA grants and lead LEOPARD.

### 9. Add metastasis to an existing aspirin-versus-blood-thinner trial

**Why:**
- Platelets help osteosarcoma cells survive in the bloodstream and settle in the lung.
- Blocking tissue factor, LPAR1 or podoplanin reduced lung metastasis in mice (PMIDs 26763081, 34302117, 35381070).
- An oral LPAR1 blocker, admilparant, is in phase 3 for lung fibrosis.
- Separately, a large trial at Massachusetts General Hospital is randomizing about 2,868 orthopaedic oncology patients, including bone sarcoma, to aspirin or enoxaparin to prevent blood clots (NCT03244020, enrolling until 2028). Recording metastasis-free survival as an extra outcome in its bone-sarcoma patients would cost little.

**Partners:** the NCT03244020 investigators at Massachusetts General Hospital.

### 10. Chase the remaining unreported trials

**Why:** four trials still have no public results:
- a 362-patient PD-L1 antibody maintenance phase 3 (ZKAB001, NCT04359550);
- a 400-patient lithium trial (NCT01669369);
- an Endostar trial (NCT01002092);
- the Brazilian metastatic metronomic trial (NCT03063983).

Two more surfaced since:
- a completed pediatric trial of the CD248 antibody MORAb-004 (NCT01748721);
- an inhaled lipid cisplatin phase 2 completed in 2018 (NCT01650090).

**Partners:** each trial's sponsor. A short, polite email asking whether results exist.

### 11. Re-analyse dog genomes from NCI's canine trials

**Why:**
- 743 open canine osteosarcoma genome runs include dogs from NCI's COTC021/022 trials, whose outcomes are known.
- Checking whether the 2025 genome-shattering pattern predicts survival in dogs would strengthen dogs as a model for testing therapies.

**Partners:** NCI Comparative Oncology Program; Paul Meltzer (NCI).

**Details:** `reports/Dog genome re-analysis scope.md`.

## Suggested order

1. **Do now, ourselves:**
   - write up the pooled control dataset (lead 3);
   - pull osteosarcoma results out of sarcoma "basket" trials to enlarge it;
   - send the unreported-trial emails (lead 10).
2. **First outreach:**
   - the NCI Comparative Oncology Program, which connects to leads 1, 4, 7 and 11 at once;
   - Colorado State, to ask what the defactinib dog study showed;
   - MIB Agents, for a scientist to review the work and for introductions.
3. **Second outreach:**
   - the sarcoma trial groups holding kinase-inhibitor samples (lead 2);
   - the PTK7 and LRRC15 drug developers (lead 5).
