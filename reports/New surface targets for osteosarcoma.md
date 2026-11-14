# New surface targets for osteosarcoma

*Built November 13–14, 2026 from open data: 88 TARGET-OS tumour RNA-seq samples (NCI GDC), GTEx v8
normal-tissue medians, Human Protein Atlas surface annotation, ClinicalTrials.gov API v2 (trial
statuses re-checked November 14, 2026). Script: `tools/surface_targets.py`. Full table:
`data/osteosarcoma_surface_target_candidates.csv` (2,434 genes). Working notes:
`research_notes/Surface targets/notes.md`.*

## Summary

Antibodies, antibody-drug conjugates (ADCs) and CAR-T cells need a protein that sits on the
tumour cell surface and is scarce in vital organs. We scored every surface protein expressed in
88 osteosarcoma tumours by how high and how consistently it is expressed and how much of it
appears in normal heart, brain, lung, gut and other vital tissues. Of the antigens already in
osteosarcoma programmes, B7-H3 scores well, but HER2, GD2 synthase, IL11RA and EGFR score below
average, because in these tumours they are expressed at low levels while being abundant in some
normal tissues. The top hit, LRRC15, already has four registered trials, two of them recruiting,
including one specifically in relapsed osteosarcoma. Below it the screen points to IFITM5,
ADAM12, MRC2, PTK7 and CD248. This is RNA, not protein, from 88 diagnostic biopsies, compared
against adult tissue that contains no bone, so every lead needs checking in tumour tissue before
anyone acts on it.

**How to read the labels.** Key numbers carry one of these tags:
- **(registry)**: read directly from an official registry or public database: ClinicalTrials.gov,
  PubMed, GTEx, Human Protein Atlas, EMA/FDA approval records.
- **(paper, full text)**: we read the full paper.
- **(paper, abstract only)**: we read only the abstract.
- **(press release only)**: the only source is a press release or a company or institution web
  page.
- **(our calculation)**: we computed it from this repository's data files with the script named
  above.

## Why this screen

No new agent has become standard treatment for osteosarcoma in the US since the 1980s;
mifamurtide was approved in the EU in 2009 for non-metastatic disease (registry). Most of the
drug trials are not antibodies at all. The most-trialled targets are blood-vessel receptors hit
by multi-kinase pills (VEGFR2 in 57 trials) and PD-1 (at least 29) (our calculation; see the
literature map). Antigen-directed agents are a smaller, newer group, and most of them aim at a
handful of antigens, chiefly GD2 (22 osteosarcoma trials), B7-H3 (13), HER2 (7) and EGFR (5)
(our calculation from the repository's drug map). Others have been tried or proposed: GPNMB's ADC
completed a phase 2 trial in osteosarcoma that did not meet its goal (paper, abstract only), and
we found no registered osteosarcoma trial against IL11RA, EPHA2 or ALPL (registry). Several of
these antigens were chosen because an antibody already existed for another cancer. A systematic
open-data pass is cheap, so the question is whether it turns up anything the field has not
already landed on.

## Method

The screen is a therapeutic-window calculation over three public datasets.

1. **Tumour expression.** All 88 open-access RNA-seq samples in the NCI GDC project TARGET-OS
   (STAR gene counts, `tpm_unstranded`, protein-coding genes only; every one a primary tumour).
   For each gene: median TPM across tumours, quartiles, and the share of tumours above 5 TPM.
   A gene had to reach median 10 TPM to be considered.
2. **Surface filter.** Human Protein Atlas annotation. A gene is kept if it is a predicted
   membrane protein. It is graded *high* confidence if the plasma membrane is one of its main
   HPA locations or it is a curated CD marker, *medium* if the plasma membrane appears only as a
   secondary location, and *low* otherwise. The headline list uses high plus medium.
3. **Normal tissue.** GTEx v8 median TPM in each of 54 tissues. The window denominator is the
   **highest median among 32 "vital" tissue entries**: heart, lung, liver, kidney, 12 brain
   regions and the cervical spinal cord, tibial nerve, colon and small intestine, arteries,
   whole blood, oesophageal mucosa, stomach, pancreas, adrenal and skeletal muscle. The worst
   tissue across all 54 is reported separately, as is GTEx's cultured-fibroblast sample. For a
   mesenchymal tumour the fibroblast value is a useful comparator: an antigen that is also high
   in fibroblasts is probably a lineage marker rather than a tumour marker.
4. **Score.** `window_score = log2((tumour median + 1) / (worst vital normal + 1)) ×
   (fraction of tumours expressing)`. The log ratio is the window; the multiplier penalises a
   gene that is high in a third of tumours and absent in the rest, which is of little use for a
   single-antigen agent.
5. **Context.** For the leading candidates, ClinicalTrials.gov API v2 was searched for antibody,
   ADC, bispecific or CAR programmes naming the target in any cancer. Osteosarcoma literature
   depth was taken from this repository's evidence tables, which inherit their limitations (see
   the literature map).
6. **Comparison set.** **We chose these comparison genes ourselves; they were not pre-specified
   positives.** They are the eight antigens with osteosarcoma programmes or proposals (B7-H3,
   GD2 via its synthase B4GALNT1, HER2, GPNMB, EGFR, IL11RA, EPHA2, ALPL) plus LRRC15, MMP14 and
   CDH11, which we added because they are known mesenchymal or sarcoma antigens. They are scored
   alongside the candidates and flagged in the output table.

## How the comparison genes ranked

These numbers come from the same pipeline as the candidate list (our calculation).

| Target | Status (registry, November 14, 2026) | Tumour median TPM | % tumours expressing | Worst vital normal TPM | Score | Rank of 2,434 |
|---|---|---|---|---|---|---|
| **LRRC15** | 4 registered trials: 2 recruiting (one in relapsed osteosarcoma), 2 not yet recruiting | 220 | 97.7% | 0.8 (stomach) | **6.77** | **1** |
| **MMP14** | No osteosarcoma trial found | 1,629 | 100% | 237.5 (tibial artery) | 2.77 | 7 |
| **CD276 / B7-H3** | ADC, CAR-T and imaging trials in osteosarcoma (13 in the drug map) | 196 | 100% | 41.8 (aorta) | 2.20 | 15 |
| **CDH11** | No osteosarcoma trial found | 97 | 98.9% | 27.2 (lung) | 1.78 | 21 |
| **ALPL** | No osteosarcoma trial found | 1,315 | 100% | 597.6 (whole blood) | 1.14 | 70 |
| **GPNMB** | ADC phase 2 in osteosarcoma (NCT02487979) completed; 1 of 22 responded, did not proceed to stage 2 (paper, abstract only; PMID 31586757) | 155 | 100% | 177.0 (aorta) | −0.19 | 617 |
| **EPHA2** | No osteosarcoma trial found; an EphA2-targeted liposome (MM-310, NCT03076372) in other solid tumours, status unknown | 102 | 98.9% | 197.6 (oesophageal mucosa) | −0.94 | 1,263 |
| **EGFR** | CAR-T and other trials (5 in the drug map) | 10.5 | 68.2% | 43.1 (tibial nerve) | −1.32 | 1,554 |
| **IL11RA** | No osteosarcoma trial found | 6.0 | 59.1% | 80.6 (aorta) | −2.10 | 1,998 |
| **B4GALNT1 (GD2 synthase)** | Antibody and CAR-T trials (22 in the drug map) | 6.3 | 61.4% | 93.6 (cerebellum) | −2.26 | 2,062 |
| **ERBB2 / HER2** | ADC and CAR-T trials (7 in the drug map) | 15.3 | 87.5% | 130.1 (tibial nerve) | −2.63 | 2,178 |

*Expression, score and rank are our calculation. GTEx values are GTEx v8 (registry). Trial counts
"in the drug map" are from `data/osteosarcoma_gene_evidence.csv`. "No osteosarcoma trial found"
means a ClinicalTrials.gov search by target and drug names with condition "osteosarcoma"
returned nothing relevant.*

Three things follow from this table.

**The genes we expected to score well did.** LRRC15, MMP14, B7-H3 and CDH11 come out at ranks 1,
7, 15 and 21 of 2,434, and B7-H3 is in the top 1%. This is a weak check, not a validation. We
chose LRRC15, MMP14 and CDH11 knowing they are mesenchymal antigens, so their good ranks partly
restate that choice, and the antigens actually in trials mostly rank poorly. None of the four is
truly osteosarcoma-specific either. B7-H3 is found across many cancers and is 63 TPM in GTEx
fibroblasts, and MMP14 is 237.5 TPM in tibial artery (registry).

**Several current favourites score badly.** HER2, GD2 synthase, IL11RA and EGFR rank in the
bottom half. For HER2 and EGFR this matches the clinical record: both have underwhelmed in
osteosarcoma, and HER2 expression in osteosarcoma has been disputed for twenty years. HER2 sits
at 15 TPM in tumours against 130 TPM in tibial nerve and 21–38 TPM in heart (registry). That is
the wrong direction for a target whose agents' dose-limiting toxicities include cardiac and
nerve damage. Ignore the GD2 rank. GD2 is a glycolipid, not a protein, so the synthase mRNA is a
poor proxy for how much antigen is on the cell. IL11RA at 6 TPM in 59% of tumours is a genuine
concern.

**ALPL shows the screen's biggest blind spot.** It ranks 70th, held back by 598 TPM in whole
blood (neutrophils are full of alkaline phosphatase) and 52 TPM in liver (registry). But GTEx
contains no bone, cartilage or osteoblast tissue. Any bone-restricted antigen therefore looks
cleaner here than it is. That applies most of all to IFITM5 below.

## Results: top 25 surface candidates outside the comparison set

Ranked by therapeutic-window score (our calculation). This is the `rank_shortlist` column in the
CSV: genes outside the comparison set, with plasma-membrane support (high or medium tier), after
dropping genes the HPA classes as housekeeping. That filter mostly removes nuclear-pore, Golgi,
lysosomal and cytochrome-P450 proteins that a membrane-prediction filter lets through. It also
removes two genuine surface proteins, CD320 (the transcobalamin receptor) and MPZL1. All of them
are still in the CSV (`rank_novel_surface` ignores the housekeeping filter), so the choice can be
reversed. "Outside the comparison set" does not mean untested in osteosarcoma: see the notes on
SMO and ITGA4 below the table.

| # | Gene | Tumour median TPM | % tumours expressing | Worst vital normal TPM (tissue) | Worst normal tissue overall | GTEx fibroblast TPM | log2 window | Score | HPA protein evidence | Surface tier |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **LRRC15** | 220 | 97.7% | 0.8 (Stomach) | 3 (Skin Not Sun Exposed Suprapubic) | 3.14 | 6.93 | 6.772 | IHC n/a, IF Approved | medium |
| 2 | **IFITM5** | 657 | 88.6% | 2.6 (Pancreas) | 3 (Pancreas) | 0.0 | 7.5 | 6.641 | IHC n/a, IF Supported | high |
| 3 | **ADAM12** | 35 | 98.9% | 1.8 (Brain Caudate basal ganglia) | 9 (Ovary) | 31.65 | 3.68 | 3.638 | IHC Enhanced, IF Supported | high |
| 4 | **MRC2** | 436 | 100.0% | 153.4 (Artery Aorta) | 153 (Artery Aorta) | 259.09 | 1.5 | 1.5 | IHC Enhanced, IF n/a | high |
| 5 | **PTK7** | 93 | 98.9% | 38.9 (Lung) | 116 (Uterus) | 71.61 | 1.23 | 1.216 | IHC Approved, IF Supported | high |
| 6 | **ULBP2** | 17 | 93.2% | 6.7 (Esophagus Mucosa) | 7 (Esophagus Mucosa) | 9.97 | 1.21 | 1.128 | IHC Approved, IF Supported | high |
| 7 | **CD109** | 38 | 96.6% | 16.3 (Esophagus Mucosa) | 21 (Skin Not Sun Exposed Suprapubic) | 117.69 | 1.16 | 1.125 | IHC Enhanced, IF Approved | high |
| 8 | **EPHB2** | 19 | 78.4% | 7.0 (Colon Transverse) | 7 (Colon Transverse) | 2.65 | 1.33 | 1.046 | IHC Approved, IF Supported | high |
| 9 | **CD248** | 164 | 100.0% | 80.4 (Artery Coronary) | 365 (Adipose Subcutaneous) | 578.09 | 1.02 | 1.02 | IHC Enhanced, IF Approved | high |
| 10 | **CD84** | 18 | 81.8% | 7.8 (Lung) | 18 (Spleen) | 0.01 | 1.13 | 0.928 | IHC Enhanced, IF Enhanced | high |
| 11 | **SDC2** | 359 | 100.0% | 190.3 (Artery Tibial) | 231 (Thyroid) | 62.14 | 0.91 | 0.912 | IHC Uncertain, IF Enhanced | high |
| 12 | **ROBO1** | 27 | 96.6% | 13.7 (Artery Tibial) | 22 (Vagina) | 25.01 | 0.92 | 0.885 | IHC Uncertain, IF Supported | high |
| 13 | **SLC16A1** | 65 | 100.0% | 36.8 (Colon Sigmoid) | 38 (Testis) | 63.16 | 0.82 | 0.815 | IHC Enhanced, IF Enhanced | high |
| 14 | **EPHA3** | 26 | 84.1% | 14.1 (Artery Coronary) | 19 (Prostate) | 0.5 | 0.87 | 0.728 | IHC Approved, IF Supported | high |
| 15 | **SMO** † | 58 | 100.0% | 35.0 (Nerve Tibial) | 63 (Cervix Endocervix) | 8.83 | 0.71 | 0.709 | IHC Approved, IF Supported | high |
| 16 | **VANGL1** | 16 | 97.7% | 9.5 (Esophagus Mucosa) | 9 (Esophagus Mucosa) | 13.27 | 0.72 | 0.704 | IHC Approved, IF Approved | high |
| 17 | **LHFPL2** | 36 | 100.0% | 21.9 (Artery Tibial) | 24 (Cervix Endocervix) | 14.09 | 0.69 | 0.687 | IHC Uncertain, IF Approved | high |
| 18 | **RELL1** | 23 | 97.7% | 14.2 (Brain Spinal cord cervical c-1) | 15 (Adipose Subcutaneous) | 6.76 | 0.67 | 0.651 | IHC Approved, IF Supported | high |
| 19 | **ITGA4** † | 17 | 93.2% | 10.3 (Lung) | 23 (Spleen) | 35.0 | 0.68 | 0.635 | IHC n/a, IF Approved | high |
| 20 | **CSF1R** | 75 | 96.6% | 49.7 (Nerve Tibial) | 207 (Spleen) | 0.45 | 0.59 | 0.57 | IHC Approved, IF Supported | high |
| 21 | **EMP3** | 353 | 100.0% | 241.9 (Whole Blood) | 242 (Whole Blood) | 344.26 | 0.54 | 0.542 | IHC n/a, IF Approved | high |
| 22 | **ADGRA2** | 53 | 98.9% | 36.1 (Nerve Tibial) | 113 (Cervix Endocervix) | 94.05 | 0.55 | 0.539 | IHC n/a, IF Supported | high |
| 23 | **SLC1A5** | 144 | 100.0% | 106.4 (Esophagus Mucosa) | 163 (Bladder) | 282.64 | 0.43 | 0.428 | IHC Enhanced, IF Supported | high |
| 24 | **TMEM101** | 52 | 100.0% | 39.0 (Kidney Cortex) | 39 (Kidney Cortex) | 26.86 | 0.41 | 0.406 | IHC n/a, IF Approved | high |
| 25 | **PIGW** | 14 | 97.7% | 10.1 (Esophagus Mucosa) | 10 (Esophagus Mucosa) | 12.72 | 0.39 | 0.386 | IHC n/a, IF Approved | high |

*† Already tested or proposed in osteosarcoma. SMO, a small-molecule drug target rather than an
antibody antigen, was targeted by vismodegib in a completed NCI sarcoma trial that included
extraskeletal osteosarcoma (NCT01154452). ITGA4 was the target of a planned natalizumab trial in
pulmonary-metastatic osteosarcoma (NCT03811886), withdrawn (registry).*

All 25 have "evidence at protein level" in HPA, meaning the protein itself has been observed,
not merely predicted from the transcript (registry). "IHC" and "IF" are HPA's own reliability
grades for its antibody staining and immunofluorescence. `Enhanced` and `Supported` are the
strong grades; `Uncertain` means HPA itself does not trust the staining. The IF grades come from
a per-gene HPA download that is not in the published CSV (its `hpa_reliability_if` column is
empty), so they cannot be checked from the data file alone. A spot-check of nine genes against
the live HPA agreed.

Two genes with higher overall scores, PANX3 and TMEM119 (overall ranks 3 and 5), are not in this
list because HPA gives them only low surface confidence.

## How much the ranking depends on our choices

The ranks of the top two candidates hold up; most of the others depend on which normal tissues
count. Re-ranking the same table under alternative choices gives these overall ranks out of
2,434 (our calculation; `python3 tools/surface_targets.py sensitivity`):

| Gene | As published (32 vital tissues) | All 54 GTEx tissues | All 54 plus fibroblasts | Pseudocount 0.1 / 5 | No %-expressing multiplier |
|---|---|---|---|---|---|
| LRRC15 | 1 | 3 | 3 | 2 / 2 | 3 |
| IFITM5 | 2 | 1 | 1 | 3 / 1 | 1 |
| ADAM12 | 4 | 16 | 213 | 4 / 7 | 4 |
| MRC2 | 38 | 22 | 49 | 39 / 30 | 39 |
| PTK7 | 64 | 551 | 474 | 68 / 57 | 69 |
| CD248 | 98 | 1,230 | 1,741 | 102 / 86 | 101 |
| CDH11 | 21 | 189 | 119 | 23 / 18 | 23 |

Changing the pseudocount or dropping the multiplier barely moves anything. Using all 54 tissues
as the denominator moves PTK7 from 64 to 551 and CD248 from 98 to 1,230, because PTK7 is high in
uterus (116 TPM) and CD248 in fat (365 TPM). Adding fibroblasts moves ADAM12 to 213. So three of
the five leads below (ADAM12, PTK7, CD248) depend on treating those tissues as acceptable
exposure. LRRC15 and IFITM5 stay in the top three under every variant we tried.

## The five leads, in plain terms

### 1. LRRC15: the top hit, and already in osteosarcoma trials

220 TPM in tumours, expressed in 97.7% of them, against 0.8 TPM in the worst vital tissue and 3.1
TPM in fibroblasts (our calculation). That is a 122-fold window as scored (272-fold on the raw
medians, before the pseudocount), the best in the dataset. LRRC15 is a known ADC target, and
AbbVie's samrotamab vedotin (ABBV-085) was an earlier attempt. ClinicalTrials.gov now lists four
LRRC15 programmes (registry, November 14, 2026):

- **LNTH-2403** (Lantheus), a lutetium-177-labelled anti-LRRC15 antibody, in a phase 1/2 trial
  in **relapsed or refractory osteosarcoma** (NCT07357519): **recruiting** since February 2026.
- **ZL-6201** (Zai Lab), an LRRC15 ADC, phase 1a/b in sarcoma and selected solid tumours
  (NCT07374848): **recruiting** since March 2026.
- **SOT106** (SOTIO), an LRRC15 ADC, phase 1/2 in LRRC15-positive osteosarcoma and soft-tissue
  sarcoma (NCT07801222): **not yet recruiting** (planned start September 2026, not yet updated).
- **NTH-2403** (Radiopharm Theranostics), a lutetium-177 anti-LRRC15 antibody imaging and safety
  study in other solid tumours (NCT07272642): **not yet recruiting**; it does not list sarcoma.
  It appears to be the same antibody as LNTH-2403, but we did not confirm this.

So this is not a new idea, and industry is ahead of the published osteosarcoma literature, which
has only 6 papers naming LRRC15 (our calculation). Anyone working on osteosarcoma should know
these trials.

### 2. IFITM5: the most interesting new hit, with a built-in caveat

657 TPM in tumours, 88.6% expressing, 2.6 TPM in the worst vital tissue and **0.0 TPM in
fibroblasts** (our calculation; GTEx registry). IFITM5 (also called BRIL) is an osteoblast
membrane protein, and a recurrent variant in it causes osteogenesis imperfecta type V (paper,
abstract only). We found no ClinicalTrials.gov study naming it (registry), and the osteosarcoma
literature has 9 papers naming it (our calculation). On these numbers it has the cleanest window
of any surface protein here that no programme targets yet. The biology is coherent: osteosarcoma
is a tumour of the osteoblast lineage. **But GTEx has no bone.** IFITM5's expression in normal
osteoblasts, growth plate and remodelling bone is not in this dataset, and it is unlikely to be zero.
A real assessment needs normal bone, especially paediatric growth plate, since the patients are
still growing. In short, it is the best-looking new target here, and the one whose risk this
screen is least able to see.

### 3. ADAM12: modest expression, good specificity on our main measure

35 TPM in tumours but in 98.9% of them, against 1.8 TPM in the worst vital tissue (a brain
region) and 9 TPM in the worst tissue overall (our calculation). HPA gives it `Enhanced` IHC
reliability, the top grade (registry). Fibroblasts sit at 32 TPM, so part of this signal is
mesenchymal lineage rather than tumour, and counting fibroblasts drops it to rank 213 (see the
sensitivity table). We found no antibody or ADC programme against it; the only registered trial
naming ADAM12 uses it as a biomarker (registry). ADAM12 is a sheddase involved in invasion, which
also means a soluble form may circulate and soak up an antibody. That is worth checking before
investing.

### 4. PTK7: the one you could test fastest

93 TPM in tumours, 98.9% expressing, 39 TPM in lung as the worst vital tissue (our calculation).
The window is modest (2.3-fold), and PTK7 is also 116 TPM in uterus and 72 TPM in fibroblasts,
so its rank depends on which tissues count. What makes it a lead is that **three PTK7-directed
ADCs are in phase 1 now**: HWK-007 (NCT07444814), KIVU-107 (NCT07229313) and DAY301
(NCT06752681), all recruiting (registry). They follow Pfizer's earlier PTK7 ADC, PF-06647020,
whose trials are completed (NCT02222922; NCT03243331, with gedatolisib). KIVU-107 lists sarcoma
among eligible tumours. We have no evidence that any sarcoma patient has been dosed. Fewer than
five osteosarcoma papers name PTK7 (our calculation). Testing an existing drug is a cheaper
experiment than building one for a new antigen.

### 5. CD248 / endosialin (TEM1): an antibody already tested, and it did not help in sarcoma

164 TPM, 100% of tumours, 80 TPM in coronary artery (our calculation). The window is the weakest
of the five, and the fibroblast value of 578 TPM is a warning: CD248 is a pericyte and
activated-fibroblast antigen, so an antibody may hit stroma as much as tumour. Its rank also
collapses when all 54 tissues are used (98 to 1,230).

The anti-CD248 antibody ontuxizumab (MORAb-004) has already been tested, and the results are
published:
- **Children:** a Children's Oncology Group phase 1 trial (NCT01748721) treated 27 patients aged
  3–21 with relapsed or refractory solid tumours. 12 mg/kg weekly was tolerated, with
  dose-limiting bacteraemia and hyponatraemia in 2 of 10 patients at that dose, and drug levels
  similar to adults' (paper, abstract only; Norris et al., *Pediatr Blood Cancer* 2018, PMID
  29292843). The abstract reports no responses and does not say how many patients had
  osteosarcoma.
- **Adult soft-tissue sarcoma:** a randomised phase 2 trial in 209 patients found no benefit
  from adding ontuxizumab to gemcitabine and docetaxel: progression-free survival 4.3 against 5.6
  months, hazard ratio 1.07 (paper, abstract only; Jones et al., *Cancer* 2019, PMID 31034598).
  Phase 2 trials in melanoma (PMID 29127533) and colorectal cancer (PMID 29084918) were also
  published.

So a plain anti-CD248 antibody was safe in children and did not work in a randomised sarcoma
trial. CD248 stays on the list only as an expression observation. Any new attempt would need a
different kind of agent, such as an ADC, and a reason to expect a different result.

### Also worth a look

**MRC2** (Endo180/uPARAP; 436 TPM, 100% of tumours, `Enhanced` IHC) is a collagen-internalising
receptor. It internalises by design, which is what an ADC needs. We found no clinical
programme, but **preclinical MRC2 ADCs exist, including one developed for sarcoma**. Evans et
al., *Mol Cancer Ther* 2023 (PMID 36399638) reported tumour regression and less metastatic
spread to lungs, liver and lymph nodes in a sarcoma xenograft. They also reported strong MRC2
staining in many of 625 soft-tissue sarcomas, and gene-expression data showing higher MRC2 in
soft-tissue and bone sarcomas than in normal tissue (paper, abstract only). Earlier uPARAP ADC work dates from 2017 (PMID 28574834), and a
2026 mesothelioma study followed (PMID 41366685). The fibroblast value of 259 TPM is the concern.

**CD109** (38 TPM, 96.6%, `Enhanced` IHC; fewer than five osteosarcoma papers; no programme
found) is a GPI-anchored TGF-β co-receptor. **ULBP2** is an NKG2D ligand with a clean window (17
against 6.7 TPM). It is interesting for NK-cell approaches rather than ADCs, but it is
stress-induced and shed, so surface levels are unstable. **EPHB2** and **EPHA3** both score
above EPHA2 (1.05 and 0.73 against −0.94). **ROBO1** has three CAR-NK trials (NCT03931720,
NCT03941457, NCT03940820), all from one sponsor, started in 2019 and now of unknown status
(registry), which is a reason for caution.

### Candidates that are probably artefacts

**CD84**, **CSF1R** and **ITGA4** are immune-cell receptors. Osteosarcoma biopsies contain many
macrophages and other immune cells, so these signals may come from those cells, not tumour. HPA
classes CSF1R as "immune cell enhanced" (registry). CD84 is classed as "low immune cell
specificity", so the argument for CD84 rests on its known biology as a leukocyte SLAM-family
receptor, not on HPA. CSF1R is a macrophage marker; targeting it is a tumour-microenvironment
strategy, not an antigen strategy. **SDC2**, **EMP3**, **SLC1A5** and **SLC16A1** are broadly
expressed and their windows are under 2-fold.

The housekeeping filter matters more than its size suggests. Eight housekeeping-flagged genes
fall within the first 30 places of the unfiltered list (NDC1 at 4, CYP20A1, TMEM50A, LAPTM4A at
13, MPZL1, CD320, TMEM65, NUS1). Most are not plausible antibody targets: NDC1 is a nuclear-pore
protein that passes the surface filter only because HPA lists the plasma membrane as a secondary
location.

## Caveats

These are ordered by how much they should change your reading.

**RNA is not protein.** Everything here is transcript abundance. Antigen density on the cell
surface, which is what an ADC or CAR actually sees, can differ greatly from mRNA levels and
depends on trafficking, shedding and turnover. The HPA columns are the only protein-level
evidence in this report. They say "this protein has been detected somewhere", not "this protein
is on the surface of osteosarcoma cells at a given density". No candidate here is actionable
without immunohistochemistry or flow cytometry on osteosarcoma tissue.

**The normal-tissue reference contains no bone.** GTEx's 54 tissues include no bone, cartilage,
periosteum or growth plate. For a tumour of the osteoblast lineage this is the biggest gap: the
normal cells most likely to share a surface antigen with the tumour are not in the comparison.
IFITM5 and ALPL are directly affected. The windows of bone-restricted antigens are overstated.

**GTEx is adult; the patients are children.** Most GTEx donors are middle-aged or older.
Osteosarcoma occurs at the adolescent growth spurt, when bone is remodelling fast. A target that
is quiet in adult tissue may be active in a growing child.

**TARGET-OS is small and nearly all diagnostic biopsies.** 88 samples, all primary tumour.
Osteosarcoma kills mainly through lung metastases that appear after chemotherapy, and antigen
expression can change under treatment and at metastatic sites. Nothing here shows whether these
targets are still expressed in relapsed, metastatic disease. With n = 88, the 95% confidence
interval on a "% of tumours expressing" figure is about ±6 points near 90% and ±10 points near
50% (our calculation).

**Bulk RNA-seq cannot separate tumour from stroma or immune cells.** A high bulk TPM can come
from tumour cells, fibroblasts, pericytes or macrophages, and the therapeutic consequences are
very different. Single-cell data would resolve this and were not used.

**The surface annotation is noisy in both directions.** HPA's immunofluorescence missed CD276
(it saw only vesicles; CD276 is rescued only as a curated CD marker) and placed MMP14 and CDH11
in the low tier. That is why the headline list uses a loose tier and prints it. The intended
cross-checks, the Cell Surface Protein Atlas / SURFY surfaceome and UniProt subcellular
locations, could not be reached from this environment, so there is one annotation source where
there should be three.

**The score is a heuristic, and the comparison is not a validation.** The log-ratio form,
pseudocount, thresholds and the choice of vital tissues are judgement calls, and the comparison
genes were chosen by us. The sensitivity table above shows which conclusions survive other
choices. The top-25 list is the extreme tail of 2,434 ratios estimated from 88 samples, so ranks
below the top few are not stable.

**Expression is necessary but far from sufficient.** A real target also needs to internalise
(for an ADC), not be shed as a soluble decoy, be expressed evenly within a tumour, and be absent
from blood stem cells. None of that is assessed here. ADAM12, CD248 and ULBP2 have known shed or
soluble forms.

**DepMap was not checked.** The plan included confirming that osteosarcoma cell lines express the
top candidates. `depmap.org` returned a bot-verification page instead of data from this
environment, and the Sanger Cell Model Passports API was blocked by the proxy. This step was not
done.

**Literature counts are incomplete by construction.** The repository's gene table includes only
genes named in at least five osteosarcoma papers, so "fewer than five" is the most we can say for
some genes. The counts also inherit the text-mining limits described in the literature map.

**The trial search matches text, not curated target fields.** ClinicalTrials.gov has no
structured "target" field, so a target is counted when its name appears in a study's text. That
misses programmes that never name the target and can over-count studies that mention a gene only
as a biomarker. The specific NCT numbers quoted above were read individually on November 14,
2026.

## Reproducing this

```
python3 tools/surface_targets.py all          # or: gdc hpa gtex rank hpadetail context sensitivity
python3 tools/surface_targets.py sensitivity  # re-rank the published CSV under other choices
```

Stages cache into `data/surface_targets_raw/` (git-ignored, about 350 MB of GDC files), so re-runs
are cheap. GTEx's bulk median-TPM files returned 403/404 here, so normals come through the API gene
by gene. The GTEx API defaults to v10, but its gene-lookup endpoint returns only GENCODE v26
identifiers, so everything is pinned to **GTEx v8**.

## What would make this real

In rough order of value per unit effort:

1. **Immunohistochemistry on an osteosarcoma tissue microarray** for IFITM5, MRC2, CD109 and
   ADAM12. This is the step that would turn these hypotheses into evidence. For MRC2, start from
   the published sarcoma staining (PMID 36399638).
2. **Normal paediatric bone and growth-plate expression** for IFITM5 and any other
   bone-restricted candidate. Without it, the top of this list cannot be assessed for safety.
3. **Follow the LRRC15 trials**, especially the recruiting osteosarcoma trial of LNTH-2403
   (NCT07357519).
4. **Ask whether PTK7 ADCs can be tested in osteosarcoma.** Three are in phase 1, and KIVU-107
   already lists sarcoma. This needs no new molecule.
5. **Single-cell or spatial data** to settle which signals are tumour and which are stroma or
   macrophage.
6. **Relapsed and metastatic samples**, since that is the disease that needs treating.

## Change log

- **November 13, 2026.** First version.
- **November 14, 2026.** Revised after an independent audit
  (`research_notes/Audit/audit_C_literature_risk_surface.md`) and a live re-check of
  ClinicalTrials.gov:
  - **LRRC15 trial status.** The earlier text said the LRRC15 trials "are recruiting now". SOT106
    and the NCT07272642 imaging study are not yet recruiting, and ZL-6201 is recruiting. The
    re-check also found a recruiting LNTH-2403 trial in relapsed osteosarcoma (NCT07357519),
    which the earlier search had missed.
  - **PTK7.** Three PTK7 ADCs are active, not four. NCT03243331 is completed.
  - **CD248.** The MORAb-004 results were described as still to be retrieved. They are
    published: safe in children, and no benefit in a randomised sarcoma trial.
  - **MRC2.** "No drug programme anywhere" was wrong. A preclinical sarcoma ADC is published.
  - **Framing.** The claim that almost every new osteosarcoma drug is an antibody, ADC or CAR-T
    aimed at eight antigens contradicted the trial data, which are dominated by kinase
    inhibitors and PD-1. It has been rewritten, and the comparison antigens now have registry
    statuses; ALPL, EPHA2 and IL11RA have no osteosarcoma trial.
  - **Comparison set.** It is now described plainly as chosen by us, not as a validation.
  - **Sensitivity.** We added a sensitivity table and script stage. The earlier text said other
    choices "do not change the top few"; in fact PTK7, CD248 and ADAM12 move a long way.
  - **SMO, ITGA4, CD84 and the housekeeping filter.** SMO and ITGA4 are marked as previously
    tested or proposed in osteosarcoma. CD84's HPA class is corrected. The housekeeping filter
    is described accurately.
  - **Wording.** "No new standard of care since the 1980s" is qualified for mifamurtide (EU,
    2009), and "osteosarcoma-specific" and "already being given to sarcoma patients" are
    softened.
