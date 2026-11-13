# Computational, genomic and data gaps (7-10) — verification and data-access feasibility

Verification pass run 2026-11-13. Every verdict cites a URL that was actually opened (marked OPENED) or only seen in search results (marked SEARCH-ONLY).

## 0. Access limits of this pass (read first)

- WebFetch could not open any page: www.biorxiv.org, pmc.ncbi.nlm.nih.gov and pubmed.ncbi.nlm.nih.gov all failed DNS resolution (outside the session's allowed network domains). Direct curl to eutils.ncbi.nlm.nih.gov, www.ebi.ac.uk (Europe PMC), api.gdc.cancer.gov, www.ncbi.nlm.nih.gov (GEO), api.reporter.nih.gov, ega-archive.org, www.cbioportal.org, pedcbioportal.kidsfirstdrc.org, depmap.org, caninecommons.cancer.gov, treehousegenomics.soe.ucsc.edu, www.stjude.cloud, osproject.org, api.crossref.org, api.openalex.org and api.semanticscholar.org was refused by the proxy (403 on CONNECT).
- Consequence: NO page was opened in full. Everything below comes from WebSearch result summaries (titles, URLs and the search tool's digest of the page). Every URL is therefore SEARCH-ONLY. Sample counts, accession numbers and access rules must be re-checked on the source page before being quoted or acted on.
- "Not found" means not found in the searches listed, not proven absent.

## 1. Gap 7 — re-reading published genomes with the 2025 LTA chromothripsis framework

### 1a. The 2025 paper (citation confirmed from search records of PubMed, Cell and UCL Discovery)
- Espejo Valle-Inclan J, De Noon S, Trevers K, ... Flanagan AM, Cortés-Ciriano I. "Ongoing chromothripsis underpins osteosarcoma genome complexity and clonal evolution." Cell 2025 Jan 23;188(2):352-370.e22. doi:10.1016/j.cell.2024.12.005. PMID 39814020. Online 14 Jan 2025. Preprint: bioRxiv 10.1101/2023.12.29.573403 ("Mechanisms underpinning osteosarcoma genome complexity and evolution").
  - https://pubmed.ncbi.nlm.nih.gov/39814020/ (SEARCH-ONLY)
  - https://www.cell.com/cell/fulltext/S0092-8674(24)01418-1 (SEARCH-ONLY)
  - Open-access author copy: https://discovery.ucl.ac.uk/id/eprint/10211808 (SEARCH-ONLY)
- Headline figures seen in search digests: ongoing subclonal chromothripsis in 74% of osteosarcomas (multi-region WGS); LTA chromothripsis in 48% (68/141) of high-grade osteosarcomas across paediatric and adult cohorts; TP53 altered in 136/197 tumours (69%), "primarily by rearrangements in intron 1" (preprint wording); genome-wide LOH prognostic.
- Cohorts named in search digests: Genomics England 100,000 Genomes Project (G100k, core cohort), plus previously published WGS: Behjati et al. 2017, MDACC, TARGET, and Kids First ("46 from the G100k cohort ... 10 from the KidsFirst cohort" appears in a methods excerpt). TCGA pan-cancer used as comparator (dbGaP phs000178). St. Jude as a separate cohort was NOT seen in the digests — unverified.
- Data availability (from digests; re-check on the Cell page):
  - New nanopore WGS: EGA EGAD50000000925 (controlled).
  - Behjati cohort: EGAD00001000107, EGAS00001000196, EGAD00001000147 (controlled, Sanger DAC).
  - MDACC cohort: EGAS00001003247 (controlled).
  - G100k: only inside the Genomics England Research Environment (requires membership of a GeCIP/Research Network institution; no individual route).
  - Code repository: not confirmed in search results.

### 1b. Corrections to the report's wording of gap 7
- The report says "No source links the TP53 intron-1 hotspot to the new mechanism". This is WRONG AS STATED: the 2025 paper itself does. The preprint text says TP53 is altered "primarily by rearrangements in intron 1", and LTA events are detected by searching for translocations between 17p (the TP53 locus) and other chromosomes. So the Ribi 2015 intron-1 hotspot is, in effect, explained by LTA in the source paper. What remains unanswered (not found in any search) is WHY intron 1 is the preferred break site (Ribi's open-chromatin/transcription hypothesis).
- The report implies TARGET had not been re-read. Search digests indicate TARGET and Kids First WGS WERE included in the 2025 paper's analysis. So "apply to TARGET-OS" is ALREADY DONE by the original authors (to be confirmed from the methods).

### 1c. Has anyone applied LTA to dogs?
- No paper using the term "loss-translocation-amplification" / "LTA chromothripsis" in canine osteosarcoma was found (two targeted searches).
- Closest canine work:
  - "Satellite DNA fragility accompanies complex genome rearrangements and ecDNA oncogene amplification in canine osteosarcomas", bioRxiv 10.64898/2025.12.31.697157 (posted 31 Dec 2025), PMC12776269. PacBio HiFi long-read WGS of 4 purebred dogs, tumour + blood; clustered rearrangements, ecDNA carrying oncogenes. LTA not mentioned in digests. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12776269/ (SEARCH-ONLY)
  - Nanopore multi-site WGS of 2 dogs (NCM 2023 talk, later 2024 record): chromothripsis-like chr11 events deleting CDKN2A, subclonal TP53/ATRX SVs. https://nanoporetech.com/resource-centre/ncm-2023-houston-nanopore-sequencing-reveal-structural-heterogeneity-canine (SEARCH-ONLY)
  - "Multi-omic Longitudinal Analysis of Canine Osteosarcoma..." bioRxiv 10.64898/2026.01.05.696411 (SEARCH-ONLY) and "Integrated Multiomic Profiling Enhances Risk Stratification and Prognostication in Canine Osteosarcoma", Clin Cancer Res 2026;32(16):3668 (SEARCH-ONLY) — neither seen to test LTA.
  - Gardner 2019 (Commun Biol, 59 dogs; WGS on a subset) https://www.nature.com/articles/s42003-019-0487-2 and the PLoS ONE 2021 canine appendicular OS paper https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0246443 (SEARCH-ONLY). IMPORTANT BIOLOGICAL CAVEAT from the PLoS ONE digest: canine TP53 loss was typically a missense mutation with LOH, whereas human TP53 loss is often a translocation. If true, LTA (which starts from a TP53-locus break) may be genuinely rarer in dogs — that would itself be a publishable negative/contrast finding, but it lowers the odds of a "same mechanism" result.
- Mouse: "Murine osteosarcoma recapitulates the driver landscape and genomic complexity of osteosarcoma evolution in humans" (Smith GA, van Belzen IAEM, ... Jacks T; bioRxiv 10.64898/2026.04.27.721100): multi-region WGS, 35 tumours from 24 Sp7-Cre Trp53fl Rb1fl mice, ~158 SVs/tumour. https://sciety.org/articles/activity/10.64898/2026.04.27.721100 (SEARCH-ONLY). This weakens the report's line "No engineered mouse is known to reproduce the 2025 shattering mechanism" — a 2026 preprint with a co-author from the 2025 paper now addresses genomic complexity in mouse; whether it reports LTA specifically was not visible.

### 1d. ecDNA in osteosarcoma
- Chapman, Chavez et al., "Extrachromosomal DNA associates with poor survival across a broad spectrum of childhood solid tumors", medRxiv 10.1101/2025.07.22.24308163, PMC12330472: AmpliconArchitect/AmpliconClassifier on WGS of 3,630 tumours / 2,967 children / 39 tumour types (CCDI, St. Jude, Kids First data). Osteosarcoma about 47% ecDNA-positive (n=55-57 across abstract versions). Open browsable resource: https://ccdi-ecdna.org/ . https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12330472/ (SEARCH-ONLY)
- Osteosarcoma PDX study with optical genome mapping + Hi-C + WGS over 11 lines reporting dozens of candidate ecDNA amplicons (SEARCH-ONLY, citation not pinned down).
- The 2025 Cell paper attributes amplification mainly to breakage-fusion-bridge cycles, which is in some tension with a 47% ecDNA call rate from short-read AmpliconArchitect — a reconciliation of "BFB vs ecDNA" in the same tumours was not found and is a small open question.

### 1e. Verdict, gap 7
- Human published genomes (TARGET, Behjati, MDACC, Kids First): ALREADY DONE by the 2025 paper itself (per search digests; confirm in methods). St. Jude PCGP genomes: not confirmed either way.
- TP53 intron-1 link: ALREADY DONE in substance (the report's claim should be removed); the "why intron 1" question is STILL OPEN.
- Canine genomes with the LTA framework: STILL OPEN (nothing found), with long-read canine data only now appearing (n=4, n=2).
- ecDNA: PARTLY ADDRESSED (pan-paediatric preprint incl. osteosarcoma; canine long-read preprint).

## 2. New large WGS re-analysis that the report missed (relevant to gaps 7 and 8)

- "Clustered structural variant hotspots enable oncogenic addiction and plasticity in osteosarcoma", PMC13596379 (2026; journal not confirmed from search digest; Shulman/Dana-Farber group suggested by search hits). 236 osteosarcoma whole genomes pooled from TARGET, ICGC and St. Jude (per digest). Five hotspots of clustered SVs (CCND3, MYC, CDK4/MDM2, CCNE1, and a region upstream of TP53) altered in 58% of tumours; enriched for early truncal SVs; explicitly flags LTA chromothripsis as "TP53-upstream clustered SVs linked to other interchromosomal connections"; proposes ctDNA tracking. https://pmc.ncbi.nlm.nih.gov/articles/PMC13596379 (SEARCH-ONLY)
- Implication: an independent US group HAS already re-read TARGET + St. Jude + ICGC genomes with an SV-clustering lens that incorporates the LTA concept. This moves the human half of gap 7 firmly to ALREADY DONE.
- Also seen: "Short Inverted Repeats as Mutational Hotspots and Putative Drivers of Genome Instability in Osteosarcoma", PMC12562434 (SEARCH-ONLY) — sequence-context work that may bear on "why these breakpoints"; and review "Chromoanagenesis in Osteosarcoma", Biomolecules 2025, doi:10.3390/biom15060833 (SEARCH-ONLY).

## 3. Gap 8 — molecular subtyping

### 3a. Competing schemes found (all SEARCH-ONLY; sample numbers from search digests)
| Scheme | Groups | Data layer | Samples | URL |
|---|---|---|---|---|
| Jiang et al., Nat Commun 2022 "Multi-omics analysis identifies osteosarcoma subtypes with distinct prognosis indicating stratified treatment" | 4 (immune-activated, immune-suppressed, HRD-dominant, MYC-driven) | CNV + methylation + mRNA + mutation, integrative clustering | 121 Shanghai patients — an INDEPENDENT Chinese cohort, not TARGET | https://www.nature.com/articles/s41467-022-34689-5 |
| "Osteosarcoma Multi-Omics Landscape and Subtypes", Cancers 2023;15:4970 (PMID 37894336) | 3 | SCNA + expression + methylation | 86 tumours (TARGET); "validated on another cohort" | https://www.mdpi.com/2072-6694/15/20/4970 |
| Lietz et al., "Genome-wide DNA methylation patterns reveal clinically relevant predictive and prognostic subtypes in human osteosarcoma" (Commun Biol 2022; medRxiv 2020.11.26.20238584) | 2 (hypo- vs hyper-methylated; hypo = worse OS, p=5e-4) | 450K methylation only | 83 TARGET primaries; reproduced in independent datasets | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8904843/ |
| Song et al. 2021 "Gene Expression Classifier Reveals Prognostic Osteosarcoma Microenvironment Molecular Subtypes" | 2 (S1 infiltration, S2 escape) | expression | TARGET/GEO bulk | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8093635/ |
| Zheng et al., Front Oncol 2023 (10.3389/fonc.2023.1111570) | (as cited in report) | expression-based | TARGET/GEO | https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2023.1111570/full |
| "Identification of a pro-protein synthesis osteosarcoma subtype..." (PMC11252356, 2024) | expression-defined subtype | expression | public bulk | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11252356/ |
| Age-stratified transcriptomic phenotypes (PMC12937902) and age-associated genomic architectures (Guo & Xie, Cancer 2026;132(14), 653 FoundationOne Heme cases, doi:10.1002/cncr.70522; Bousquet et al., Cancer 2026, doi:10.1002/cncr.70500) | age-linked routes: CDK4/MDM2 in young adults vs MYC/CCND3/CCNE1 in children | targeted panel | 653 | https://acsjournals.onlinelibrary.wiley.com/doi/10.1002/cncr.70522 |
| Koelsche et al., Nat Commun 2021 "Sarcoma classification by DNA methylation profiling" (DKFZ sarcoma classifier) | diagnostic classes (62 sarcoma classes; osteosarcoma high-grade is one class) | methylation array | 1,077 training profiles, 428 validation | https://discovery-pp.ucl.ac.uk/id/eprint/10119933 |

### 3b. Does any scheme use SV burden, LOH or methylation?
- Methylation: YES (Lietz 2-group; Jiang and Cancers-2023 use it as one layer). The DKFZ sarcoma classifier is DIAGNOSTIC (is it osteosarcoma?) and was not seen to provide prognostic sub-classes within high-grade osteosarcoma.
- Copy number: YES as a layer (Jiang, Cancers 2023).
- Structural-variant-defined groups: PARTLY — the 2026 236-WGS hotspot paper defines 5 SV hotspot groups (58% of tumours) and the 2025 Cell paper defines LTA-positive vs negative; neither was seen to be offered as a formal subtype classifier or cross-walked to the expression/methylation schemes.
- LOH burden as prognostic: proposed in the 2025 Cell paper (preprint section "Chromosomal losses precede whole-genome doubling and predict prognosis"). Search digests suggest the LOH analysis touched G100k, TARGET and Kids First data. NO independent (different-author) validation of LOH burden was found in two searches. An older array-based genome-wide LOH/"chromosomal alteration staging" study exists (Smida et al., 2010-era; link seen: https://mediatum.ub.tum.de/1073416 SEARCH-ONLY), which is a historical precedent rather than validation.

### 3c. Corrections to the report
- "all built largely on the same 86 to 98 samples" is too strong: Jiang 2022 used 121 independent Shanghai patients. It IS fair that most expression-only schemes recycle TARGET (about 86-98 with RNA-seq) plus GEO arrays.
- No paper was found that formally tests concordance between the schemes on the same tumours, or tests whether SV/LOH burden explains the expression subtypes.

### 3d. Verdict, gap 8
PARTLY ADDRESSED. SV-based grouping (236-WGS hotspots paper; LTA status) and LOH prognosis (Cell 2025) now exist; methylation subtypes exist. STILL OPEN: (i) a head-to-head concordance analysis of the published schemes on one cohort; (ii) independent validation of LOH burden against outcome; (iii) testing whether LOH/SV burden outperforms or explains expression subtypes. TARGET-OS is the natural test bed because it has RNA-seq, methylation, copy number and outcome on overlapping cases — and its open-tier files may suffice (see section 8).

## 4. Gap 9 — single-cell / spatial datasets and reuse

### 4a. Independent human datasets identified (SEARCH-ONLY; confirm each on its GEO page — GEO was not reachable from this session)
| Accession | Source study | Patients/samples | Notes |
|---|---|---|---|
| GSE152048 | Zhou et al., Nat Commun 2020 | 11 patients (7 primary, 2 recurrent, 2 lung met); 100,987 cells | mostly post-chemotherapy; the most reused set |
| GSE162454 | Liu et al., Front Oncol 2021 | 6 treatment-naive primaries; ~29,278 cells | second most reused |
| GSE198896 | Theranostics 2022 (recurrent OS, CAF study) | 4 samples (1 primary, 3 recurrent) | https://www.thno.org/v12p5877.htm |
| (in-house, NCC China) | "A single-cell and spatially resolved atlas of human osteosarcomas", J Hematol Oncol 2024 | 10 new scRNA samples + spatial; pooled with the two above = 27 samples, 194,083 cells | https://link.springer.com/article/10.1186/s13045-024-01598-7 ; deposit accession not seen |
| GSE299023 | "Immunosuppressive tumor microenvironment of osteosarcoma" (2025) | 6 new biopsies (+6 prior from same group) + spatial validation | |
| GSE234187, GSE250015 | named in a pooled atlas of 247,774 cells ("Molecular characterization of cell dynamics during osteosarcoma progression", PMC13380119) | counts not seen | |
| GSE217792, GSE283885 | named as inputs to the 2026 cross-species bioRxiv integration | counts not seen | |
| (accession not seen) | bioRxiv 10.1101/2025.06.27.661729 "Single-Cell and Spatial Profiling of TME Heterogeneity in Human Osteosarcomas" | 14 samples (8 post-chemo, 6 naive); 78,838 cells | |
| (accession not seen) | Osteoblastic OS study 2022: 166,012 OS cells + 49,555 healthy bone cells from 28 patients | 28 patients (incl. healthy bone donors) | cited via search digest; verify |
| (accession not seen) | "Single-cell fixed RNA profiling of the osteosarcoma clinical spectrum identifies ADAMTS12 and RNASE1..." (2026, ScienceDirect S2212137426000436) | not seen | FFPE-compatible, new cohort |
| GSE293065 | "Spatial transcriptomic atlas of aggressive osteosarcomas...", Nat Commun 2026 (s41467-026-74603-x) | 26 samples / 19 patients, spatial | code on Zenodo record 19369637 |
| Canine: GSE299494 (Visium, 14 dogs), GSE295311 (GeoMx Canine Cancer Atlas, trial-linked) | | | outcome-linked |
| Mouse: GSE270231 (lung niche scRNA) | | | |

Rough count: at least 8-10 independent human single-cell cohorts and 3+ human spatial cohorts now exist (roughly 80-120 patients in total, with overlap unresolved), versus the "17 samples" baseline the report cites. Most were deposited in 2024-2026.

### 4b. Integrated atlases already published
- J Hematol Oncol 2024 atlas: 27 samples, scRNA + spatial. (SEARCH-ONLY)
- "Molecular characterization of cell dynamics during osteosarcoma progression" (PMC13380119): pools GSE152048, GSE162454, GSE198896, GSE234187, GSE250015, GSE299023 — 247,774 cells. (SEARCH-ONLY)
- bioRxiv 10.64898/2026.01.13.698472 "Integrative Single-cell and Spatial Transcriptomic Analysis of Osteosarcoma Reveals Conserved and Distinct Ecosystems Across Sites and Species": >1 million cells/nuclei from human, canine, PDX and mouse, bone and lung; six conserved tumour-cell states; concludes dog is the more faithful model for tumour-host signalling. (SEARCH-ONLY) https://www.biorxiv.org/content/10.64898/2026.01.13.698472v1
- Reviews: "New biological insights into osteosarcoma — lessons from single cell sequencing studies" (PMC13149624) notes the low number of public OS scRNA-seq datasets; "Single-cell RNA-seq reveals intratumoral heterogeneity in osteosarcoma patients: A review" (PMC10074210).

### 4c. Dataset-reuse audit
- NOT FOUND. One extended search for a systematic review / meta-research audit counting how many osteosarcoma single-cell papers rely on GSE152048 and/or GSE162454 returned none. Authors of individual papers acknowledge the limit ("only seventeen single-cell tumor samples can be found in public repositories") but nobody has quantified the reuse or checked which published claims replicate in the newer independent cohorts.
- One good-practice example: a cross-cohort CCL13-ACKR4 reproducibility repo with SHA-256 manifests (https://github.com/ouyangzhengxiao-bit/osteosarcoma-ccl13-ackr4-reproducibility, SEARCH-ONLY).

### 4d. Verdict, gap 9
- Integrated atlas: ALREADY DONE / in progress (three integrations, incl. a >1M-cell cross-species preprint). An independent team should not build another atlas.
- Reuse audit ("how many papers, which claims replicate"): STILL OPEN, and now more valuable because independent cohorts exist to test the recycled claims against. The report's "17 samples" figure is out of date and should be updated.

## 5. Gap 10 — germline risk, structural variants and non-European cohorts

### 5a. Report figures checked
- Mirabello et al., JAMA Oncol 2020 (PMID 32191290): 1,244 patients were sequenced. The 28.0% figure (281/1,004) is for the 1,004 patients of European ancestry, compared with 12.1% of controls; TP53 accounts for 4.4%. So BOTH numbers in the report are right: 1,244 is the whole cohort and 1,004 is the European-ancestry subset used for the burden estimate. https://pubmed.ncbi.nlm.nih.gov/32191290/ and https://jamanetwork.com/journals/jamaoncology/fullarticle/2762589 (SEARCH-ONLY). Data came from exome and targeted sequencing, not WGS.
- The NCI PDQ quotes 18% for autosomal-dominant genes only (a different denominator). https://www.cancer.gov/types/bone/hp/osteosarcoma-treatment-pdq (SEARCH-ONLY)

### 5b. Germline SV-aware work that already exists
- Gillani R, ... Van Allen EM et al., "Rare germline structural variants increase risk for pediatric solid tumors", Science 2025;387(6729):eadq0071, doi:10.1126/science.adq0071. Germline WGS of 1,765 affected children (Ewing sarcoma, neuroblastoma, osteosarcoma), 943 unaffected parents and 6,665 adult controls. It found 84 large (>1 Mb) unbalanced chromosomal abnormalities linked to risk, 82% inherited; germline SVs explain 1.1-5.6% of liability. The osteosarcoma-specific n and any TP53 intron-1 result were NOT visible in the digests. https://www.science.org/doi/10.1126/science.adq0071 (SEARCH-ONLY)
- Ribi et al. 2015 (PMC4480712): a germline 445 kb TP53 intron-1 inversion segregating in a 4-generation LFS family; exome and panel tests miss copy-neutral intronic rearrangements.
- An ongoing long-read (Oxford Nanopore) WGS study of 290 International Sarcoma Kindred Study individuals with suspected LFS who tested negative on short-read sequencing; no yield reported yet. https://nanoporetech.com/resource-centre/improving-diagnosis-in-li-fraumeni-syndrome-using-long-read-whole-genome-and-integrated-multiomic-sequencing-lc26 (SEARCH-ONLY)
- Fischer et al., "TP53 variant clusters stratify phenotypic diversity in germline carriers and reveal an osteosarcoma-prone subgroup", Nat Commun 2025;16:8546 (5 clusters; a "monomeric" subgroup enriched for osteosarcoma). This covers coding variants only; intron 1 is not addressed. https://www.nature.com/articles/s41467-025-63528-6 (SEARCH-ONLY)

### 5c. Non-European cohorts
- India: a single-centre paediatric series found germline TP53 P/LP variants in 13% (3/23), which the authors say is higher than Western series. The cohort is very small. https://ecancer.org/en/journal/article/2214-should-all-paediatric-osteosarcoma-patients-be-tested-for-germline-tp53-variants-insights-from-a-single-centre-sarcoma-unit-from-india/pdf (SEARCH-ONLY)
- No Chinese, Japanese, Latin American or African osteosarcoma germline-prevalence cohort was found in two searches. A related lead not followed up: the Jiang 2022 Shanghai multi-omics cohort (121 patients) probably has matched normals, which would allow a germline call.

### 5d. Verdict, gap 10
- SV-aware germline analysis: PARTLY ADDRESSED. Gillani 2025 (Science) did germline SV analysis of WGS including osteosarcoma, and a 290-person long-read LFS study is under way. STILL OPEN: an osteosarcoma-specific estimate of how many germline TP53 intron-1 inversions or other SVs are missed by panels.
- Non-European prevalence: STILL OPEN (one 23-patient Indian series only).
- Feasibility for an independent team: low with open data. Germline reads are controlled-access everywhere (dbGaP, St. Jude Cloud, Kids First), and the open tier holds somatic data only.

## 6. AI and drug-repurposing analyses in osteosarcoma

### 6a. Already published (all SEARCH-ONLY)
- Connectivity map / LINCS signature reversal: Andrade RC et al. 2021, "New drug candidates for osteosarcoma: Drug repurposing based on gene expression signature" (Comput Biol Med). It built a 266-gene GEO signature and ran L1000CDS2; top hits were afatinib, BRD-K95196255, DG 041 and CA-074 Me. Computational only, with no in-house validation. https://www.arca.fiocruz.br/handle/icict/48690
- Cao et al. 2020: L1000 + DGIdb applied to metastasis genes (TLR7 validated, but not the drugs). PMC7434575 (inferred from the search listing)
- Multi-objective ChEMBL model, Pharmaceuticals 2020;13(11):409, using HOS, MG63, SAOS2 and U2OS; top hits were temsirolimus, sirolimus, everolimus, paclitaxel and cabazitaxel. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7700154/
- Human and canine comparative drug screen: Parrales et al., PLoS ONE 2018. 13 drugs selective in both species; auranofin led to in vivo work. https://doaj.org/article/fcfb7274e7014e86bedf45880a5e58f5
- ML on GDSC + PRISM sensitivity applied to 12 paediatric FFPE samples: ESMO Sarcoma 2025 Abstract 85P; validation still pending. https://oncologypro.esmo.org/meeting-resources/esmo-sarcoma-and-rare-cancers-congress-2025/use-of-artificial-intelligence-ai-to-explore-online-gene-expression-profiles-databases-related-to-drug-sensitivity-in-multiple-tumor-cell-lines
- Anti Cancer Fund review of osteosarcoma repurposing: https://www.anticancerfund.org/en/news/drug-repurposing-source-innovative-therapies-osteosarcoma

### 6b. DepMap dependency work
- J Transl Med 2022 (s12967-022-03571-9): 785 common-essential genes in DepMap OS lines (CERES < -1 in >75% of lines); LARS validated. https://link.springer.com/doi/10.1186/s12967-022-03571-9
- RPS28 identified as essential using Chronos (PMC10776981).
- Paediatric genome-scale CRISPR screen of 82 paediatric lines including osteosarcoma (Dharia et al., Nat Genet 2021; PMC8049517).
- SMARCAL1 synthetic lethality in ALT+ osteosarcoma: AACR 2024 abstract and bioRxiv 2024.02.01.578345, using 13 DepMap OS lines.

### 6c. Verdict
PARTLY ADDRESSED. Signature-reversal and DepMap essential-gene analyses exist but are small, single-signature and mostly unvalidated. STILL OPEN and feasible with open data:
- a systematic, pre-registered repurposing analysis that combines (a) LINCS signature reversal using several signatures (TARGET bulk, the single-cell malignant-cell states, LTA-positive vs LTA-negative if labels are published), (b) DepMap CRISPR selective dependencies, and (c) PRISM/GDSC sensitivity, cross-checked against canine OS lines in the same screens and against the list of drugs already failed in osteosarcoma trials;
- a DepMap test of whether dependencies differ by copy-number state, for example CDK4/MDM2-amplified vs MYC-amplified vs CCNE1-amplified lines, mapped onto the 2026 SV-hotspot groups.
Caveat: DepMap has only about 13-20 osteosarcoma lines (exact count to be checked on depmap.org, which was blocked), so statistical power is low and the lines are mostly adult-derived and long-passaged.

## 7. Osteosarcoma funding analyses (NIH RePORTER)
- No published aggregate analysis of the NIH osteosarcoma portfolio was found in one search. The hits were individual grant records on third-party aggregators (opengrants.io, ai-analytics.org), for example a P50 on antibody-drug conjugates at MD Anderson and an R01 on metastatic colonization at Nationwide Children's. These figures are unverified against RePORTER.
- api.reporter.nih.gov was blocked from this session (403 on proxy CONNECT), so I could not run a query.
- Verdict: STILL OPEN (no published portfolio analysis found). Feasibility is high: the RePORTER API is open, needs no key, and returns project text, fiscal year, institute and award amount. NCI's annual "Funding for Research Areas" pages give a disease-level figure only for larger categories, and osteosarcoma is not separately listed there (unverified; check). A small team could build the tracker in days.

## 8. Data-access feasibility (part 1: human genomic resources)

Rule of thumb, from general knowledge of dbGaP and confirmed for St. Jude by search: controlled-access genomic data (reads, germline calls, unfiltered somatic calls) needs a PI with an eRA Commons account (dbGaP) or an equivalent, plus a signature from the institution's Signing Official. An unaffiliated individual cannot apply alone; the usual route is a collaborating academic PI who applies and lists the independent researcher as an internal collaborator. Open-tier data needs no application.

| Resource | Data types (OS) | OS n | Access | What an unaffiliated person needs | Source (SEARCH-ONLY) |
|---|---|---|---|---|---|
| TARGET-OS on GDC (dbGaP phs000468; to be checked) | WGS, WXS, mRNA-seq, miRNA-seq, methylation 450K, copy-number arrays, expression arrays, clinical | 282-297 cases in the catalog; ~86-98 with RNA-seq; 83 with methylation and survival | MIXED. OPEN: RNA-seq gene quantification, miRNA quantification, clinical/biospecimen, methylation beta values (inferred, verify), verified somatic variants ("made available as open-access"; verify). CONTROLLED: BAM/FASTQ, raw/unfiltered VCFs, germline | Open tier: nothing (GDC portal or AWS open data registry). Controlled: dbGaP via an institutional PI | https://www.cancer.gov/ccg/research/genome-sequencing/target/studied-cancers/osteosarcoma ; https://datacatalog.ccdi.cancer.gov/dataset/TARGET-OS ; https://registry.opendata.aws/target/ ; https://ccgdata.cancer.gov/programs/target/data-matrix |
| St. Jude Cloud (PCGP osteosarcoma WGS; also EGA EGAD00001000160 "SJACT WGS") | WGS, WES, RNA-seq; somatic and germline | count not confirmed | CONTROLLED, with a Data Access Committee. The DAA must be signed by an Institutional Authority; it is valid for 1 year; no for-profit access; the applicant must not be a postdoc or staff scientist; a work email is required | Institutional PI and Signing Official. An individual cannot apply | https://docs.stjude.cloud/genomics-platform/getting-started/filling-out-the-daa ; https://ega-archive.org/datasets/EGAD00001000160 |
| St. Jude Cloud visualisation (PeCan / ProteinPaint) | browsable somatic variant summaries | — | OPEN to browse | nothing | (portal blocked; not opened) |
| Kids First osteosarcoma "treatment failure" (dbGaP phs001714) | WGS on serial pre-treatment, post-treatment and relapse/metastasis samples, plus RNA-seq | not confirmed (the 2025 Cell paper used 10 patients / 26 regions) | CONTROLLED (dbGaP). Processed somatic data may appear on PedcBioPortal | Institutional PI | https://www.omicsdi.org/dataset/dbgap/phs001714 |
| CCDI Molecular Characterization Initiative (phs002790; not confirmed) | targeted panel, methylation array, RNA fusion panel, some WGS/WES | not found | Not confirmed. Expected to be controlled for reads, with summary data in the CCDI Hub and portals | likely an institutional PI | search failed to return MCI-specific pages |
| CCDI ecDNA resource | AmpliconArchitect calls on 3,630 paediatric WGS incl. osteosarcoma (n~55-57) | ~57 | OPEN to browse | nothing | https://ccdi-ecdna.org/ |
| dbGaP phs000699 "Osteosarcoma Genomics" | tumour/normal exome or WGS | 58 pairs from Brazil, Spain, Mexico and the US | CONTROLLED | Institutional PI. Note: a rare non-European/Latin American subset, relevant to gap 10 | https://www.omicsdi.org/dataset/dbgap/phs000699 |
| EGA, 2025 Cell paper | nanopore WGS (EGAD50000000925); Behjati (EGAD00001000107/000147, EGAS00001000196); MDACC (EGAS00001003247) | Behjati ~112 tumours (Nat Commun 2017); others not confirmed | CONTROLLED, through each study's DAC (Sanger etc.) | an institutional applicant and DAA | Cell paper digests |
| Genomics England 100,000 Genomes (core cohort of the Cell paper) | WGS, multi-region | ~>100 osteosarcomas (G100k; exact n to be checked) | CONTROLLED. Analysis happens only inside the Research Environment | membership via an approved institution or Research Network; no individual route | Cell paper digests |
| EGA EGAS00001003201 | WGS + RNA-seq of paediatric OS primaries and PDXs | not seen | CONTROLLED | institutional | https://www.omicsdi.org/dataset/ega/EGAS00001003201 |
| MSK-IMPACT osteosarcoma (Suehara 2019) and AACR GENIE | targeted panel | 71 samples / 66 patients (MSK); GENIE larger | OPEN on cBioPortal (MSK study); GENIE is open after free registration | free registration (GENIE) | https://typeset.io/pdf/clinical-genomic-sequencing-of-pediatric-and-adult-15lij0zd4i.pdf |
| cBioPortal / PedcBioPortal osteosarcoma studies (TARGET 2018 pan-cancer OS, MSK, others) | processed mutations, CNA, expression, clinical | TARGET ~87-98 | OPEN (cBioPortal). PedcBioPortal has public studies plus some that need login | none, or a free login | portals blocked; the study list was not verified |
| Count Me In Osteosarcoma Project (OSproject) | WES of tumour and germline, clinical, patient-reported outcomes | no current count found; the award targets 3,000 | stated as "freely available" via cBioPortal and GDC, in batches | likely none for processed data; no confirmed release was found in this pass | https://danafarberbostonchildrens.org/news/count-me-launches-osteosarcoma-project |
| Treehouse (UCSC) | harmonised RNA-seq expression (TPM) across a paediatric compendium, incl. osteosarcoma | not confirmed; a UCSC dissertation claims "the largest publicly available harmonized RNA-seq dataset for osteosarcoma" | OPEN expression compendium (from prior knowledge; site blocked) | nothing | https://escholarship.org/uc/item/9ss9t40b |
| DepMap | CRISPR (Chronos), RNAi, expression, CN, mutations, PRISM drug response, for cell lines | ~13-20 OS lines (to be checked) | OPEN (CC BY 4.0) | nothing | https://depmap.org/broad (site blocked from the shell) |
| LINCS / CMap (clue.io, L1000CDS2, SigCom LINCS) | drug perturbation signatures | U2OS is a profiled line in L1000 (inferred) | OPEN (clue.io needs a free academic login) | nothing or a free login | not opened |

## 8. Data-access feasibility (part 2: single-cell, canine, funding)

| Resource | Data | n | Access | Needs | Source (SEARCH-ONLY) |
|---|---|---|---|---|---|
| GEO human OS single-cell / spatial (GSE152048, GSE162454, GSE198896, GSE234187, GSE250015, GSE299023, GSE293065, ...) | count matrices; some raw FASTQ in SRA | about 8-10 cohorts, roughly 80-120 patients combined | OPEN. Note: several Chinese-origin datasets deposit raw reads in GSA-Human (controlled) and only processed matrices in GEO | nothing for the matrices | section 4 |
| ICDC OSA01 (Gardner 2019 canine) | WGS (BAM + VCF), WXS, RNA-seq | 59 dogs: WGS 24, WXS 13, RNA-seq 54 | OPEN. "All data in the ICDC are open-access"; BAMs are listed. Download is via the CRDC cloud resources (Seven Bridges Cancer Genomics Cloud), which may charge compute costs; direct download not confirmed | a free CRDC cloud account (NIH login or ORCID-type login; verify) | https://datacommons.cancer.gov/repository/integrated-canine-data-commons ; https://scholars.uthscsa.edu/en/datasets/a-multi-platform-sequencing-analysis-of-canine-appendicular-osteo/ |
| Other ICDC canine OS studies (e.g. COTC trial-linked samples) | varies | not checked | OPEN | as above | ICDC listing not opened |
| SRA canine OS (PLoS ONE 2021 multi-platform canine study; Satellite-DNA HiFi preprint, 4 dogs; canine OS cell-line genomes, PMC9469990) | WGS / long-read | small | usually OPEN in SRA (canine data are not human-subject protected); accessions not confirmed | nothing | sections 1c and 5 |
| GEO canine spatial: GSE299494 (Visium, 14 dogs), GSE295311 (GeoMx, trial-linked) | spatial | 14+ | OPEN | nothing | section 4 |
| NIH RePORTER API / ExPORTER bulk files | grants, abstracts, amounts, fiscal year, institute | all NIH | OPEN, no key | nothing | api.reporter.nih.gov (blocked from here) |

### 8a. Which gap analyses can be done TODAY with fully open data
1. Canine LTA/chromothripsis re-analysis (gap 7, the canine half). ICDC OSA01 offers open BAMs for 24 tumour/normal WGS pairs. Run SV and copy-number callers and look for 17p-centred (TP53) translocations with downstream BFB amplification, then compare with the human published rates (48% LTA). Also look at ecDNA with AmpliconArchitect. This is the one genuinely open genomic gap that open data covers in full. Caveats: likely low coverage (to be checked), short reads, and canine TP53 loss may be mostly point mutation + LOH.
2. Single-cell reuse audit and replication test (gap 9). Count papers by GEO accession (literature mining via Europe PMC full text), then test whether headline claims from the GSE152048/GSE162454-based papers replicate in the independent newer cohorts (GSE299023, GSE234187, GSE250015, GSE198896, GSE293065 spatial), all open as matrices.
3. Subtype concordance on TARGET-OS open tier (gap 8). Open RNA-seq, methylation and clinical data allow the 2-, 3- and 4-group schemes to be reproduced and cross-tabulated on the same ~85 tumours. A copy-number LOH proxy is possible ONLY if segment files are open; GDC usually makes masked copy-number segments open (verify for TARGET-OS). If so, a crude genome-wide LOH fraction versus survival check is possible, but allele-specific LOH needs BAMs (controlled).
4. NIH RePORTER osteosarcoma funding tracker (section 7). Fully open.
5. Multi-source repurposing screen (section 6). DepMap + PRISM + LINCS + TARGET expression are all open. The key limit is the small number of OS lines.
NOT feasible with open data: SV-aware germline analysis (gap 10), allele-specific LOH validation (gap 8), and re-analysis of human WGS for LTA (gap 7 human half; already done anyway). All need dbGaP, EGA, St. Jude or Genomics England controlled access through an institutional PI.

