# Cross-Disease and Cross-Field Transfer Opportunities for Osteosarcoma (and Neuroblastoma)

Evidence tags: [STRONG] = randomized or replicated clinical data; [CLIN-EARLY] = phase I/II or single-arm; [PRECLIN] = cell or animal only; [SPEC] = speculation or inference.
Search scope: 11 tool calls (web search snippets plus aggregator pages). Primary papers were not fetched in full, so verify numbers against the originals before citing.

## 1. Genomically similar adult cancers (HGSOC, TNBC): PARP, ATR/WEE1, ADCs

### Takeaway
OS has "BRCAness-like" genomic scars, but HRD scores do not track HR-gene mutations and PARPi sensitivity in models follows RB1 loss, not HRD. The main human test (olaparib plus ceralasertib, NCT04417106) had reported only as an abstract in what I found. HER2 and GPNMB ADCs, both borrowed from breast cancer, failed in recurrent OS.

### Cited Findings
- In 48 OS samples the median HRD score was 45, a distribution resembling BRCA1/2-deficient breast cancer, yet HR-gene alterations were not associated with higher scores. The authors suggest the scores may reflect TP53-driven chromosomal instability rather than true HRD [PRECLIN/correlative] — [AACR 2022 abstract 2590](https://www.aminer.org/pub/64a0d8d2d68f896efabf9473/abstract-analysis-of-homologous-recombination-deficiency-hrd-scores-in-osteosarcoma)
- PARPi caused extensive cell death in RB1-defective backgrounds and prolonged survival of mice carrying RB1-defective human OS grafts. Sensitivity was not associated with canonical HRD signatures [PRECLIN] — [Nature Communications 2021](https://www.nature.com/articles/s41467-021-27291-8.pdf); [PMC8642453](https://pmc.ncbi.nlm.nih.gov/articles/PMC8642453)
- A phase II trial of olaparib plus ceralasertib (ATR inhibitor) in recurrent or refractory OS (NCT04417106) included prospective correlative biomarkers. A 2025 JCO/ASCO abstract exists, but I could not retrieve its efficacy results [CLIN-EARLY] — [NCI listing](https://www.cancer.gov/clinicaltrials/NCI-2020-13346); [ASCO COI](https://coi.asco.org/Report/ViewAbstractCOI?id=508822)
- HER2 is overexpressed in about 30% of OS. In COG PEPN1924, trastuzumab deruxtecan was tested in HER2-expressing recurrent OS (41 of 50 screened were eligible) and did not show sufficient efficacy; only one patient had prolonged stable disease (12 cycles) [CLIN-EARLY, negative] — [Review PMC10706029](https://pmc.ncbi.nlm.nih.gov/articles/PMC10706029); [COG](https://childrensoncologygroup.org/publications/pepn1924-a-phase-ii-study-of-trastuzumab-deruxtecan-in-patients-with-recurrent-human-epidermal-growth-factor-receptor-2-osteosarcoma-a-childrens-oncology-group-pediatric-early-phase-clinical-trial/)
- GPNMB was expressed in 92.5% of OS samples and the ADC glembatumumab vedotin killed 74% of OS cell lines. In the clinic (COG AOST1521, 22 patients) there was 1 partial response and 2 stable disease, and expression did not correlate with response [CLIN-EARLY, negative] — [Preclinical 2016](https://www.medchemexpress.com/publications/26305408.html); [CancerNetwork](https://cancernetwork.com/view/novel-agent-fails-show-sufficient-activity-recurrent-osteosarcoma)

### Inferences
- [SPEC] Borrowing "HRD score leads to PARPi" from ovarian cancer is likely the wrong transfer for OS. The more defensible biomarker is RB1 loss, or replication-stress markers (ATR/WEE1 logic). A biomarker-stratified trial (RB1-null vs intact) has not been reported.
- [SPEC] Both ADC failures show that target expression alone is not enough in OS. Payload choice, antigen density thresholds and delivery to bone or lung matter. Next-generation ADCs against antigens with high density in OS (B7-H3, for example) are an under-tested transfer from adult solid tumors.

### Gaps
- Efficacy results of NCT04417106 were not retrieved. WEE1 (adavosertib) results in pediatric OS, and platinum-sensitivity mapping versus ovarian cancer, were not searched.

## 2. Other sarcomas and bone diseases (Ewing IGF-1R, GCTB/denosumab, bone-metastasis therapies)

### Takeaway
The denosumab success in giant-cell tumor of bone did not transfer: single-agent denosumab was inactive in recurrent OS despite on-target RANKL inhibition. Ewing IGF-1R trials show that an unselected phase II signal (about 10% response rate) did not survive phase III. Radium-223, approved in prostate cancer, has only phase I OS data.

### Cited Findings
- Not written in this pass: see Gaps.

### Gaps
- The findings for this section (denosumab, Ewing IGF-1R, multikinase inhibitors, radiopharmaceuticals) were not saved to this file; the write was interrupted. They are summarised with URLs in the researcher handback message to the coordinator.

## 3. Other species: elephants, TP53 and LIF6 (Peto's paradox)

### Takeaway
Elephant cancer resistance is a cell-culture finding with no demonstrated OS application; I found no study testing elephant p53 or LIF6 in OS cells in this search.

### Cited Findings
- Elephants carry about 20 TP53 copies, many of them retrogenes, some encoding truncated p53 [PRECLIN] — [Science News](https://www.sciencenews.org/article/resurrected-gene-may-protect-elephants-cancer)
- LIF6, a re-activated pseudogene, is up-regulated by TP53 after DNA damage, moves to mitochondria and induces apoptosis; it is required for the enhanced elephant cell-death response. Evidence is from cell experiments, largely one lab [PRECLIN] — [bioRxiv preprint](https://www.biorxiv.org/content/10.1101/187922v2); [PMC6369797](https://pmc.ncbi.nlm.nih.gov/articles/6369797)

### Inferences
- [SPEC] OS is a TP53-loss disease, so the idea of restoring a p53-like death signal is conceptually relevant, but delivery of any such gene or protein to tumors is unsolved. Treat as hypothesis-generating only.

### Gaps
- Reports of elephant p53 delivered to human OS cells (work associated with J. Schiffman's group) were not retrieved or verified here.

## 4. Metastasis biology: lung niche and dormancy

### Takeaway
OS has its own lung-niche mechanism (IL-1 alpha from lung epithelium driving tumor IL-6 and CXCL8) with mouse evidence that blocking it reduces metastasis; approved drugs against these pathways exist in other diseases but no OS trial was found. Dormancy concepts from breast cancer (NR2F1, TGF-beta2) returned nothing in OS.

### Cited Findings
- IL-6 and CXCL8 are higher in OS lung metastases than matched primaries; combined blockade had little effect on proliferation but inhibited metastasis across several mouse models [PRECLIN] — [JCI Insight 2018](https://content.jci.org/articles/view/99791/pdf); [PMC6141177](https://pmc.ncbi.nlm.nih.gov/articles/PMC6141177)
- A hypoproliferative OS subpopulation initiates metastasis by sustaining IL-6/CXCL8 output in response to lung epithelial IL-1 alpha; disrupting IL-1 signaling reduced metastatic progression [PRECLIN; preprint, reported as later published in Cancer Research 2025] — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.06.09.597967.full.pdf)

### Inferences
- [SPEC] The transfer is from rheumatology: IL-6 and IL-1 blockers are licensed for inflammatory disease, so an adjuvant anti-metastasis trial could use existing agents. The endpoint would have to be metastasis-free survival, not tumor shrinkage, since these agents did not slow proliferation.
- [SPEC] The "hypoproliferative initiating cell" finding is the closest OS analogue to breast-cancer dormancy work; nobody appears to have asked whether NR2F1-type dormancy programs operate in it.

### Gaps
- No OS-specific results for NR2F1 or TGF-beta2 dormancy were found. ctDNA and circulating tumor cell findings were not written to this file (see handback).

## 5. Immunotherapy transfers: TIL therapy, mRNA and neoantigen vaccines, GD2 (from neuroblastoma)

### Takeaway
TIL therapy and personalized vaccines have reached early OS trials but have no controlled efficacy data. The neuroblastoma GD2 antibody dinutuximab was tested in recurrent OS and was negative.

### Cited Findings
- Adoptive TIL plus anti-PD-1 in chemotherapy-resistant metastatic OS was reported safe with manageable adverse events [CLIN-EARLY, uncontrolled] — [PMC7547340](https://pmc.ncbi.nlm.nih.gov/articles/PMC7547340)
- An MD Anderson TIL manufacturing protocol for soft tissue sarcoma and OS (CD3/CD28 activator replacing anti-CD137) has FDA clearance for trial use (IND 30562) [PRECLIN/manufacturing] — [Frontiers in Immunology 2025](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2025.1557006/epub)
- A phase I trial tests a personalized neoantigen vaccine (SarcVac) with lymphocyte reinfusion and sintilimab in advanced sarcomas including OS; primary aim is safety [CLIN-EARLY, no results] — [Trial listing](https://www.trialx.com/clinical-trials/listings/342586/tumor-neoantigen-vaccine-sarvac/)
- Houston Methodist announced a personalized mRNA vaccine for OS (May 2026). This is a press release; no peer-reviewed efficacy data or registration was found [unverified] — [EurekAlert](https://www.eurekalert.org/news-releases/1128080)
- COG phase 2 of dinutuximab plus GM-CSF in recurrent OS: 11 of 39 event-free at 12 months (28.2%), no evidence of efficacy [CLIN-EARLY, negative] — [eScholarship](https://escholarship.org/uc/item/8dx5s3gd)
- Naxitamab plus GM-CSF is being tested in recurrent OS in second or later remission (NCT02502786); final results not found — [MSK Synapse](https://synapse.mskcc.org/synapse/works/156520)

### Inferences
- [SPEC] OS has high structural variation but few point-mutation neoantigens; vaccine pipelines built for melanoma may need to prioritise fusion and breakpoint-derived neoantigens. I found no source testing this.
- [SPEC] The minimal-residual-disease setting (after resection of lung metastases) is where vaccines worked in melanoma and pancreatic cancer and is the logical OS setting; the naxitamab trial already uses that design.

### Gaps
- No bispecific T-cell engager trial in OS was found; searches for B7-H3 bispecifics returned nothing. Macrophage reprogramming and "cold tumor" lessons from pancreatic cancer and glioblastoma were not researched. B7-H3 CAR T findings are in the handback, not this file.

## 6. Computational and AI approaches; open datasets

### Takeaway
Deep learning for necrosis scoring is the one AI transfer with published OS validation. I could not document the open datasets or which cross-dataset analyses are missing; that part remains a gap.

### Cited Findings
- A deep learning model trained on 103 OS cases (3,134 H&E slides) estimated necrosis ratio in close agreement with pathologists and stratified overall and progression-free survival; model and code were released [retrospective validation] — [arXiv 2208.04910](https://arxiv.org/abs/2208.04910v1)
- A related study reported network versus pathologist agreement for necrosis quantification of R2 = 0.899 [retrospective] — [BVS listing, PMID 36563747](https://pesquisa.bvsalud.org/infofrontera/resource/en/mdl-36563747)

### Inferences
- [SPEC] Necrosis is the main prognostic marker but is scored by eye; a prospective multi-centre validation of the released model is a cheap, concrete next step.
- [SPEC] Candidate un-done analyses (not confirmed by search): joint human-canine somatic analysis, and linking slide-based necrosis scores to genomics in the same patients.

### Gaps
- No sources retrieved on connectivity map/LINCS repurposing in OS, digital twins, federated learning, or the contents of TARGET-OS, St. Jude Cloud, CCDI, Kids First, DepMap or canine datasets.

## 7. Repurposed drugs: disulfiram, ivermectin, itraconazole, statins, nelfinavir

### Takeaway
All evidence found is cell-line or mouse work. None of these drugs has clinical trial results in OS, and none should be presented as a treatment.

### Cited Findings
- Disulfiram/copper inhibited OS growth via reactive oxygen species in vitro and in vivo; a 2018 mouse study reported reduced metastatic burden [PRECLIN] — [Oncotarget](https://oncotarget.com/article/25733/pdf)
- Ivermectin was synergistic with doxorubicin in OS cells and inhibited growth in a mouse model [PRECLIN] — [PubMed 36503300](https://pubmed.ncbi.nlm.nih.gov/36503300/)
- Itraconazole appears only inside a proposed nine-drug regimen (OSR9) in a review, not a trial [SPEC] — [IJMS 2023](https://mdpi.com/1422-0067/24/20/15474)
- Simvastatin appeared only in a combination screening paper calling for further study [PRECLIN] — [J Res Pharm](https://jrespharm.com/pdf.php?id=1233)

### Inferences
- In vitro activity of ivermectin and similar drugs is common across cancers and often occurs at concentrations not reachable in patients; the sources found do not address achievable dosing. Online claims go well beyond this evidence.
- [SPEC] The canine trial network is the fastest route to a fair test of a cheap repurposed drug in spontaneous OS.

### Gaps
- Nothing found for nelfinavir or for statin epidemiology in OS.

## 8. Paget's disease, fibrous dysplasia, chondrosarcoma (IDH)

### Takeaway
Paget's-associated OS is a rare, near-uniformly fatal natural experiment linking osteoclast-pathway germline variants to OS, but its mechanism is unknown. Chondrosarcoma IDH and fibrous dysplasia GNAS were not covered.

### Cited Findings
- OS is the most frequent tumor arising in Paget's disease, with 5-year survival described as almost nil and mechanism unknown — [PMC4746367](https://pmc.ncbi.nlm.nih.gov/articles/PMC4746367)
- Common Paget's disease is linked to SQSTM1 (p62) mutations; Paget's with giant cell tumor is SQSTM1-negative and caused by a ZNF687 founder mutation (P937R) — [PMC4746367](https://pmc.ncbi.nlm.nih.gov/articles/PMC4746367); [Bone Research 2023](https://www.nature.com/articles/s41413-023-00250-3.pdf)

### Inferences
- [SPEC] p62 sits in autophagy and NF-kB signaling; whether sporadic OS shares these pathways is a testable question in existing genomic cohorts.

### Gaps
- Not retrieved: ivosidenib results in IDH1-mutant chondrosarcoma, GNAS and malignant transformation in fibrous dysplasia.

## 9. Neuroblastoma

### Takeaway
The only neuroblastoma-linked evidence gathered is the GD2 transfer into OS (Section 5). Transfers into neuroblastoma were not researched.

### Cited Findings
- See Section 5 for dinutuximab and naxitamab in OS — [eScholarship](https://escholarship.org/uc/item/8dx5s3gd)

### Inferences
- None beyond Section 5.

### Gaps
- Neuroblastoma-directed transfers (ALK inhibitors from lung cancer, MYCN targeting, differentiation therapy, ctDNA) were not searched.

## Addendum: findings for section 2 and related topics (from search summaries; verify before quoting)

These were gathered during research but not saved in the first pass. All rest on search-result summaries, not full papers.

- **Denosumab (RANKL):** a COG phase 2 trial in recurrent osteosarcoma was negative. Source link not saved; verify.
- **Ewing sarcoma IGF-1R:** in phase III trial AEWS1221, adding ganitumab gave no benefit (3-year event-free survival 37.4% vs 39.1%). [NCT02306161](https://clinicaltrials.gov/study/NCT02306161)
- **Multikinase inhibitors:** regorafenib improved progression-free survival in SARC024 (3.6 vs 1.7 months) and in REGOBONE, but not overall survival. Cabozantinib gave an 11.9% response rate in CABONE. [TargetedOnc](https://targetedonc.com/view/cabozantinib-prolongs-survival-in-patients-with-advanced-osteosarcoma-and-ewing-sarcoma)
- **Bone-seeking radiopharmaceuticals:** radium-223 has only a phase I osteosarcoma trial (Subbiah, Clin Cancer Res 2019). Samarium-153-EDTMP has older high-dose studies. [Review](https://www.pubmed.gov/24924181/)
- **ctDNA:** Shulman et al. 2018 (Br J Cancer, COG) found ctDNA in about 57% of newly diagnosed osteosarcoma; higher levels meant more risk. [eScholarship](https://escholarship.org/uc/item/4s89v1k6). Audinot et al. 2024 (Ann Oncol) studied 183 patients from OS2006; ctDNA at diagnosis predicted outcome independently of metastatic status, and they built a prediction tool (PRONOS) whose external validation was still underway. [PMC6162271](https://pmc.ncbi.nlm.nih.gov/articles/PMC6162271)
- **Comparative oncology (dogs):**
  - No published COTC021 rapamycin results found. A separate randomized trial of 324 dogs found adjuvant sirolimus did not improve outcome. [PMC7020630](https://pmc.ncbi.nlm.nih.gov/articles/PMC7020630)
  - ADXS-HER2 Listeria vaccine data in dogs are small and mostly company-reported, with conflicting historical controls. [FiercePharma](https://www.fiercepharma.com/r-d/advaxis-sees-encouraging-results-for-immuno-oncology-treatment-dogs-bone-cancer)
  - Losartan plus toceranib gave a 50% clinical benefit rate in 28 dogs with lung metastases; it needed about 10 times the usual blood-pressure dose to block monocyte recruitment. [PMC8866227](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866227)
  - Mifamurtide (L-MTP-PE) extended survival in dogs; its human use rests on INT-0133.
- **Growth and genetics:** dogs over 40 kg have about 45 times the odds of osteosarcoma compared with dogs under 10 kg. A 2024 study carried a canine GWAS region over to humans and found a GRB10 locus (rs17454681) tied to osteosarcoma risk, height and pubertal timing. [PMC11402579](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402579)
- **B7-H3 CAR T:** St. Jude trials in osteosarcoma (NCT04897321, NCT07428993, RAD3CAR with radiation); Illinois is testing B7-H3 CAR T in dogs. No B7-H3 bispecific trial in osteosarcoma was found.
- **Repurposed drugs:** propranolol and metformin have only cell and mouse data in osteosarcoma. [PMC9458647](https://pmc.ncbi.nlm.nih.gov/articles/PMC9458647)
