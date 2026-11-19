# What's new in osteosarcoma research

*A scan of papers, preprints and trials from June 1, 2025 to November 19, 2026, checked against
this project's reports and leads, plus a protein-level check of the new surface targets. Built
November 19, 2026 from PubMed, Europe PMC, bioRxiv/medRxiv, ClinicalTrials.gov API v2 and the
Human Protein Atlas. Working notes: `research_notes/Whats new/scan_2025-06_to_now.md` and
`research_notes/Surface targets/protein_check.md`.*

## Summary

The biggest news is a randomised phase 3 trial in relapsed osteosarcoma in which a drug aimed at
B7-H3 held off progression for a median 5.5 months against 1.4 with chemotherapy, at the cost of
heavier side effects. A Children's Oncology Group analysis of 99 patients confirms that only about
one in five stays relapse-free a year after lung metastases are removed, and its authors conclude
that only randomised trials can detect modest gains. LRRC15, the top hit in our surface-target
screen, now has protein evidence from three independent 2026 studies, two of them in patient tumours,
so the trials already testing it look well aimed. The other RNA leads are weaker than they looked: PTK7
has been stained in only two osteosarcoma models, and IFITM5 and ADAM12 have never been measured
as protein in human osteosarcoma. New genetic work shows that MYC amplification predicts poor
survival and, in a mouse preprint, that MYC-driven tumour cells resist cabozantinib, which any test of our kinase-pill lead
needs to account for.

**How to read the labels.** Key numbers carry one of these tags:
- **(registry)**: read directly from an official registry or database (ClinicalTrials.gov, PubMed
  counts, Human Protein Atlas).
- **(paper, full text)**: we read the full paper.
- **(paper, abstract only)**: we read only the abstract. Preprints are marked **(preprint, abstract
  only)** and are not peer-reviewed.
- **(press release only)**: the only source is a company or press page.
- **(our calculation)**: computed by us from the sources or this repository's data.

## The five items most likely to change what this project says

| # | Item | Source | Label | Affects | Effect |
|---|---|---|---|---|---|
| 1 | **ARTEMIS-011.** B7-H3 ADC risvutatug rezetecan vs gemcitabine–docetaxel after ≥2 prior lines, 80 vs 42 patients: median PFS **5.5 vs 1.4 months, HR 0.33**; grade ≥3 treatment-related events 93% vs 83%, serious 64% vs 29%; overall survival immature | Ann Oncol, Oct 2026, PMID 42933637 | (paper, abstract only) | Landscape and gaps report (says "no journal paper yet"); pooled controls; trials landscape; lead 5 | **Strengthens** the antigen-directed route and randomising in relapse |
| 2 | **COG resected lung-only relapse benchmark.** 99 patients from three phase 2 trials: 12-month event-free **22% (95% CI 15–31%)**, median EFS 4.8 months; early relapse (within 2 years) worse | medRxiv, Nov 16, 2026 | (preprint, abstract only) | Landscape report and pooled controls (quote AOST0221's 20%, 10–34%, n = 42); lead 6 | **Strengthens** lead 6: the authors themselves say smaller effects "will require randomization" |
| 3 | **LRRC15 protein confirmed** in 18 paediatric primaries (median H-score 113.5), across a spatial cohort that includes relapses, and in 22 PDXs by mass spec; expert workshop names an LRRC15 ADC with an osteosarcoma-suited payload as promising | Clin Cancer Res 2026; Nat Commun 2026; Cell Rep 2026; Br J Cancer 2026 | (paper, full text) ×3; workshop (paper, abstract only) | Surface report; lead 5 | **Strengthens** LRRC15 |
| 4 | **MYC.** Amplification in 16% of 105 patients, 3-year survival 27% vs 74% (adjusted HR 3.4); MYC-driven mouse osteosarcoma cells about 8-fold more resistant to cabozantinib in vitro | Cancer 2025, PMID 41199591; bioRxiv Sep 2026 | (paper, abstract only); (preprint, abstract only); fold change (our calculation) | Kinase-pill report; lead 2 | **Complicates** lead 2: amplification studies of pill benefit should record MYC |
| 5 | **PEPN1924 published.** T-DXd: 41 of 50 relapsed tumours passed a lenient HER2 IHC screen, 1 of 9 treated had stable disease past 24 weeks | JCO Oncol Adv 2025, PMID 42131734 | (paper, abstract only) | Landscape report, which cites the preclinical paper (PMID 40911899) for this result | **Strengthens** the surface report's view of HER2; citation fix |

## Everything else worth knowing, by lead

"In repo" means the source already appears somewhere in this repository; "new" means it does not.

| Item | Source | Label | Lead or report | Effect | In repo? |
|---|---|---|---|---|---|
| JCOG0905: adding ifosfamide for poor responders did not help (103 randomised; DFS HR 1.05, 95% CI 0.55–1.98) | JCO 2025, PMID 40138604 | (paper, abstract only) | Trials landscape (randomised-trial count) | Confirms EURAMOS-1 | Data tables only |
| CabOSTar cabozantinib maintenance: results posted, 10 patients, efficacy "not collected and analyzed" | NCT06341712 | (registry) | Kinase-pill report; lead 2 | No usable efficacy data | Termination noted; results posting new |
| Real-world TKIs in Turkey: median PFS 4.4 months in osteosarcoma (72 bone-sarcoma patients) | JCO Glob Oncol 2026, PMID 42715501 | (paper, abstract only) | Kinase-pill report | Consistent with "works briefly" | Data tables only |
| Genomic-subtype umbrella pilot: 19 patients, median PFS 50 days | NPJ Precis Oncol 2025, PMID 41372533 | (paper, abstract only) | Lead 2, gaps report | Feasibility only | Data tables only |
| SBRT plus checkpoint inhibitor: median PFS 5.68 months in 18 patients, pneumonitis 4/18 | Int J Radiat Oncol Biol Phys 2026, PMID 41325874 | (paper, abstract only) | Landscape (immunotherapy) | Uncontrolled | Data tables only |
| Olaparib + irinotecan, AcSé-ESMART: ORR 9.1% in 70; one osteosarcoma partial response | Clin Cancer Res 2026, PMID 41591981 | (paper, abstract only) | Landscape (DNA repair) | Minor | Data tables only |
| Dogs: palliative radiation + Listeria-HER2 helped 5 of 15 (no control) | Mol Ther Oncol 2026, PMID 42291138 | (paper, abstract only) | Landscape (OST-HER2 paragraph) | Small, uncontrolled signal | Data tables only |
| Dogs: histotripsy ablation caused immune activation; "a subset" outlived expectations | Cancers 2026, PMID 42588726 | (paper, abstract only) | Dog genome / comparative work | Context | Data tables only |
| Dogs: inhaled IL-15 after amputation did worse than controls; IL-6 rose after surgery | Front Immunol 2025, PMID 41209004 | (paper, abstract only) | Lead 1 | Supports lead 1 | Discussed |
| PDX surface proteomics: ROR2 and TMEM119 nearly absent from 25 and 22 normal paediatric tissues by IHC | Cell Rep 2026, PMID 42647168 | (paper, full text) | Surface report | New targets; our filter wrongly dropped TMEM119 | Data tables only |
| CADM1 ADC: all six CADM1-positive PDXs responded, three completely | Mol Cancer Ther 2026, PMID 41517891 | (paper, abstract only) | Surface report | New target with a drug | Data tables only |
| B7-H3 ADC vobramitamab: active in paediatric xenografts, response not linked to B7-H3 level | Clin Cancer Res 2026, PMID 41941262 | (paper, abstract only) | Surface report | Caution: antigen level may not predict ADC benefit | Data tables only |
| Meflin (ISLR) ADC in recurrent-like osteosarcoma models | Oncogene 2025, PMID 41120731 | (paper, abstract only) | Surface report | Context | Data tables only |
| Workshop priorities: LRRC15 ADC, SMARCAL1, KIF18A, eIF4A1, RUNX2, MYC | Br J Cancer 2026, PMID 42613365 | (paper, abstract only) | Lead 5; landscape | Independent support for LRRC15 | Data tables only |
| SMARCAL1 germline variants in 1.8–3% of osteosarcoma patients across four cohorts | JCO 2025, PMID 41066719 | (paper, abstract only) | Landscape (biology) | New predisposition gene and target | Not discussed |
| Early vs late osteoblast-like epigenetic states with different drug responses | Cancer Discov 2026, PMID 41037662 | (paper, abstract only) | Literature map; surface report | Context | Data tables only |
| Metastases and treated tumours lose the osteoblastic cell state (24 tumours) | bioRxiv Jun 2026 | (preprint, abstract only) | Surface report (IFITM5); lung report | Weakens IFITM5 for metastatic disease (our inference) | New |
| International working group: pre-treatment ctDNA "positioned for clinical implementation" | NPJ Precis Oncol 2026, PMID 42086782 | (paper, abstract only) | Lead 7 | Supports lead 7 | Data tables only |
| Plasma DKK1 fell 12.4% per 30 days on treatment (34 patients); tumour DKK1 linked to worse OS (HR 1.35 per SD) | medRxiv Nov 2026 | (preprint, abstract only) | Lead 4 | Human support for DKK1 | New |
| Lung fibroblasts build an inflammatory niche; doxorubicin switches on an IL-1β/COX-2 loop | Research Square 2025 and 2026 | (preprint, abstract only) | Lead 1 | Mechanistic support | New |
| KIF18A inhibitor active in genome-doubled osteosarcoma cells and xenografts | Cancer Biol Ther 2026, PMID 42328720 | (paper, abstract only) | Landscape (new targets) | Matches workshop priority | Data tables only |

## New trials

Of 49 new interventional ClinicalTrials.gov records naming osteosarcoma since June 1, 2025, most
were already in this repository's trial tables (registry). Four were not:

| Trial | What | Status (registry, November 19, 2026) |
|---|---|---|
| FIERCe, NCT07227571 | FOLR1 CAR-T cells for relapsed or refractory osteosarcoma (Fred Hutch), ages 1–75 | Recruiting since January 2026 |
| NCT07596693 | KXV01, a TCR delivered by in-body lentivirus, solid tumours "including osteosarcoma" | Recruiting |
| NCT07774533 | B7-H3 nanobody PET scan in osteosarcoma (Peking University First Hospital) | Recruiting; primary completion August 2026 |
| NCT07787429 | Mifamurtide vs sorafenib in high-risk osteosarcoma (Poland), 40 planned | Recruiting |

FOLR1 ranks 1,924th of 2,434 in our RNA screen (17.8 TPM, 77% of tumours; our calculation), so
FIERCe will be a real-world test of whether a low RNA rank rules a target out.

## Part A: do the surface targets exist as protein?

Our screen ranked targets from RNA. We checked each lead against the Human Protein Atlas and the
published staining literature. HPA has no sarcoma tissue, so it speaks only to normal tissue, and
it has **no tissue staining at all for LRRC15 or IFITM5** (registry).

| Target | Protein in osteosarcoma | Normal-tissue safety picture | Verdict | Cheapest next experiment |
|---|---|---|---|---|
| **LRRC15** | 63 of 69 tumours stained, 51 (74%) at 2+ or 3+ (paper, abstract only; percentage our calculation); 18 paediatric primaries, median H-score 113.5 (paper, full text); seen by staining across a spatial cohort that includes relapses, and by mass spec in 22 PDXs (paper, full text) | Mouse tissue: only hair follicles, marrow stem cells and osteoblasts, none in brain, heart, lung, liver or kidney (paper, full text). In 85 adults the earlier LRRC15 ADC, ABBV-085, caused payload-type side effects (fatigue, nausea, poor appetite); 4 partial responses among 20 osteosarcoma or UPS patients (paper, abstract only) | **Strong** for primary tumours; **partial** for metastases, relapses and normal bone | Stain paired primary, lung metastasis and relapse samples plus children's growth plate and marrow. First ask the SOT106 and Lu-TARGO sponsors to publish their screening data |
| **PTK7** | Two PDXs (one from a relapse) and two cell lines positive (paper, full text); named in the PDX mass-spec ranking (paper, full text). **No series of patient tumours** | Children's normal-tissue array negative or weak in every organ (paper, full text); adult HPA staining weak to moderate in most tissues, which HPA rates as poorly matching RNA (registry). The PTK7 ADC cofetuzumab caused grade ≥3 neutropenia in 25%, plus hair loss and nausea (paper, abstract only) | **Partial** | Stain an osteosarcoma tissue array with the PTK7 test and cut-off used in the lung-cancer trials |
| **IFITM5** | **Never measured** as protein in human osteosarcoma; one group could not find a validated antibody (paper, full text) | Unknown; bone is missing from GTEx and HPA, and it is an osteoblast protein. A preprint finds metastases lose the osteoblast state (preprint, abstract only) | **Absent** | RNA in-situ staining of tumours, metastases and children's growth plate, since no antibody is ready |
| **ADAM12** | **Never measured** in human osteosarcoma (mouse model only, paper, abstract only) | HPA's three antibodies disagree; one stains brain, gut and kidney strongly; a shed form circulates (registry) | **Absent** | Two antibodies side by side on a tissue array, plus a serum ADAM12 measurement |

Two other proteins look better at protein level than our RNA list suggested. **TMEM119** ranks 5th
overall by RNA but was dropped because HPA gives it low surface confidence (our calculation); a
2026 study shows surface staining in osteosarcoma and little in 21 of 22 normal children's tissues
(paper, full text). **ROR2** (our shortlist rank 55) was nearly absent from 25 normal children's
tissues (paper, full text). Five of our top 25 RNA candidates (MRC2, CD109, EPHB2, EPHA3, EMP3)
were independently found enriched as protein in the PDX study (our calculation from the paper's
text).

**One tissue array would settle most of this:** osteosarcoma primaries with paired lung metastases
and relapses, plus normal growth plate, stained for LRRC15, PTK7, TMEM119 and CD109, with IFITM5 by
RNA in-situ staining. COG's and St. Jude's osteosarcoma arrays already exist.

**LRRC15 trials (registry, November 19, 2026).** Lu-TARGO (LNTH-2403, NCT07357519) recruiting at 2
US sites; ZL-6201 (NCT07374848) recruiting at 12 sites in China and the US, record updated
November 18; SOT106 (NCT07801222) still "not yet recruiting", its planned September 30 start not
yet updated; NCT07272642 not yet recruiting. That last record now names its drug as
"LNTH-2403 (177Lu-DOTA-DUNP19)", so it is the same antibody as Lu-TARGO. None has posted results.
Company news about SOT106 designations and posters was seen only in search summaries, because the
pages were blocked here, so we do not quote it. Two PTK7 drugs were missing from our surface
report: IDE034, a B7-H3 × PTK7 ADC (NCT07503808, recruiting), and Lilly's LY4175408
(NCT07046923), which we take to be a PTK7 drug because its exclusion criteria bar earlier PTK7
ADCs with the same payload class (registry; the target is our inference).

## What should change in existing reports

We did not edit other reports. These are the corrections and updates we found:

1. **Osteosarcoma research landscape and gaps.** ARTEMIS-011 is now a journal paper (Ann Oncol 2026,
   PMID 42933637); replace "no journal paper yet (press release only)". The abstract prints the
   hazard ratio's 95% CI as 0.21–1.23, which conflicts with the 0.20–0.55 in
   `data/osteosarcoma_relapse_benchmarks_published.csv`; check the full paper before quoting either.
2. **Same report.** The PEPN1924 result is cited to PMID 40911899, a preclinical paper. Cite the
   trial paper, PMID 42131734 (1 of 9 with stable disease past 24 weeks).
3. **Same report and the pooled control dataset.** The resected lung-relapse benchmark (20%, 95% CI
   10–34%, n = 42, AOST0221) has a larger update: 22% (15–31%), n = 99 (preprint, abstract only).
4. **New surface targets** and **Ranked leads.** NCT07272642 is LNTH-2403, the same antibody as
   Lu-TARGO; drop "could not confirm". Add the LRRC15 protein data; state that IFITM5 and ADAM12
   have no human protein data; note that ADAM12's "Enhanced" HPA grade rests on antibodies that
   disagree; add IDE034 and LY4175408; note cofetuzumab's NCT04189614 was terminated. The "6
   osteosarcoma papers name LRRC15" figure is out of date: PubMed returns 11 for "LRRC15 AND
   osteosarcoma", 7 of them from 2025–26 (registry).
5. **New surface targets.** The HPA surface filter excluded TMEM119, which now has surface staining
   in patient tumours. Consider re-running the shortlist with TMEM119 admitted.
6. **Why kinase-inhibitor pills work.** Add MYC status to the proposed amplification test (lead 2):
   MYC amplification predicts poor survival and, in mice, cabozantinib resistance. CabOSTar's
   posted results contain no efficacy data.
7. **Osteosarcoma clinical trials landscape.** JCOG0905 (randomised, negative) is one more
   osteosarcoma-only randomised trial to check against the count of 27.

## Limits

- Most items were read as abstracts only. We read the full text of four papers: Mooney 2026,
  O'Reilly 2026, Moquin-Beaudry 2026 and Lee 2023.
- About 450 PubMed titles, 100 preprint titles and 63 trial records were screened, out of 2,665
  PubMed osteosarcoma records in the window. Single-gene laboratory papers and herbal-compound
  studies were skipped on purpose, so a relevant laboratory paper could have been missed.
- We did not search conference abstract books (ASCO, ESMO, CTOS) directly. Company and trade-press
  pages were blocked from this environment, so the SOT106, ZL-6201 and LNTH-2403 company updates
  were not read.
- The Human Protein Atlas has no sarcoma or bone tissue, and no tissue staining for LRRC15 or
  IFITM5. Its normal-tissue maps are from adults.
- Preprints are not peer-reviewed.
- Counts of "new" vs "in repo" depend on PMID and NCT matching against this repository's files.

## Change log

- **November 19, 2026.** First version. Part B scan of June 1, 2025 to November 19, 2026; Part A
  protein check of LRRC15, PTK7, IFITM5 and ADAM12, with MRC2, CD109, CD248 and B7-H3 for context.
