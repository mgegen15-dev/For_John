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

