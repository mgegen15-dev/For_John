# New surface targets for osteosarcoma

*Built November 14, 2026 from open data: 88 TARGET-OS tumour RNA-seq samples (NCI GDC), GTEx v8
normal-tissue medians, Human Protein Atlas surface annotation, ClinicalTrials.gov API v2.
Script: `tools/surface_targets.py`. Full table: `data/osteosarcoma_surface_target_candidates.csv`
(2,434 genes). Working notes: `research_notes/Surface targets/notes.md`.*

## Summary

Almost every new osteosarcoma drug in trials today is an antibody, antibody-drug conjugate
(ADC) or CAR-T cell aimed at one of eight antigens, and nobody seems to have asked publicly
whether those eight are the best eight. So we did the obvious screen: for every protein on the
cell surface, how high and how consistently is it expressed in osteosarcoma tumours, and how
much of it sits in the organs you cannot afford to damage? The answer is that the field's
current favourites are a mixed bag — B7-H3 (CD276) genuinely scores well, but HER2, GD2
synthase, IL11RA and EGFR all score *worse than average*, because in these 88 tumours they are
barely expressed while being abundant in normal heart, nerve and gut. Meanwhile the screen's
top hit, **LRRC15**, is already being pursued by two companies in sarcoma trials that opened in
the last year, which is the strongest evidence that the method is tracking something real.
Below LRRC15 the screen surfaces a short list of targets that osteosarcoma has largely ignored:
**IFITM5**, a bone-specific membrane protein expressed at 657 TPM in tumours and essentially
zero everywhere GTEx looks; **ADAM12**; **PTK7**, which already has four ADCs in phase 1 for
other cancers and so could be tested in osteosarcoma without building a new antibody; and
**CD248/endosialin**, whose antibody was already given to children with refractory solid
tumours a decade ago. The caveats are serious and listed at the end — this is RNA, not protein,
from 88 diagnostic biopsies, compared against adult normal tissue that contains no bone.

## Why this screen

Osteosarcoma has had no new standard-of-care agent since the 1980s. The modern pipeline is
dominated by surface-antigen therapeutics against a short, largely borrowed list: B7-H3
(CD276), GD2, HER2 (ERBB2), GPNMB, EGFR, IL11RA, EPHA2 and ALPL. Several of these were chosen
because an antibody already existed for another cancer, not because osteosarcoma expression was
checked first. A systematic open-data pass is cheap, so the only question is whether it turns up
anything the field has not already landed on.

## Method

The screen is a therapeutic-window calculation, run over three public datasets.

1. **Tumour expression.** All 88 open-access RNA-seq samples in the NCI GDC project TARGET-OS
   (STAR gene counts, `tpm_unstranded`, protein-coding genes only; every one a primary tumour).
   For each gene: median TPM across tumours, quartiles, and the share of tumours above 5 TPM.
   A gene had to reach median 10 TPM to be considered.
2. **Surface filter.** Human Protein Atlas annotation. A gene is kept if it is a predicted
   membrane protein; it is graded *high* confidence if the plasma membrane is one of its main
   HPA locations or it is a curated CD marker, *medium* if the plasma membrane appears only as a
   secondary location, *low* otherwise. The headline list uses high plus medium.
3. **Normal tissue.** GTEx v8 median TPM in each of 54 tissues. The window denominator is the
   **highest median among 32 "vital" tissue entries** — heart, lung, liver, kidney, 12 brain
   regions, tibial nerve, colon and small intestine, arteries, whole blood, oesophageal mucosa,
   stomach, pancreas, adrenal and skeletal muscle. The worst tissue across all 54 is reported
   separately, as is GTEx's cultured-fibroblast sample, which is the single most useful
   comparator here: a mesenchymal tumour antigen that is also high in fibroblasts is probably a
   lineage marker rather than a tumour marker.
4. **Score.** `window_score = log2((tumour median + 1) / (worst vital normal + 1)) ×
   (fraction of tumours expressing)`. The log ratio is the window; the multiplier penalises a
   gene that is high in a third of tumours and absent in the rest, which is useless for a
   single-antigen agent.
5. **Context.** For the leading candidates, ClinicalTrials.gov API v2 was searched for existing
   antibody / ADC / bispecific / CAR programmes against that target in any cancer, and
   osteosarcoma literature depth was taken from this repo's own evidence tables.
6. **Controls.** The eight antigens already in osteosarcoma trials, plus LRRC15, MMP14 and
   CDH11, were scored alongside and are flagged in the output table. Where they land is the only
   available check on whether the score means anything.

## How the known targets ranked — the validation check

This is the part to read first, because it decides whether the rest is worth anything. The
numbers below are produced by exactly the same pipeline as the candidate list.

| Target | Status in osteosarcoma | Tumour median TPM | % tumours expressing | Worst vital normal TPM | Score | Rank of 2,434 |
|---|---|---|---|---|---|---|
| **LRRC15** | ADC target, sarcoma trials opening | 220 | 97.7% | 0.8 (stomach) | **6.77** | **1** |
| **MMP14** | preclinical interest | 1,629 | 100% | 237.5 (artery) | 2.77 | 7 |
| **CD276 / B7-H3** | ADCs + CAR-T in trials | 196 | 100% | 41.8 (nerve) | 2.20 | 15 |
| **CDH11** | preclinical interest | 97 | 98.9% | 27.2 (artery) | 1.78 | 21 |
| **ALPL** | in trials | 1,315 | 100% | 597.6 (liver) | 1.14 | 70 |
| **GPNMB** | ADC in trials | 155 | 100% | 177.0 (nerve) | −0.19 | 617 |
| **EPHA2** | in trials | 102 | 98.9% | 197.6 (nerve) | −0.94 | 1,263 |
| **EGFR** | in trials | 10.5 | 68.2% | 43.1 (liver) | −1.32 | 1,554 |
| **IL11RA** | ADC in trials | 6.0 | 59.1% | 80.6 (liver) | −2.10 | 1,998 |
| **B4GALNT1 (GD2 synthase)** | CAR-T + antibody in trials | 6.3 | 61.4% | 93.6 (brain) | −2.26 | 2,062 |
| **ERBB2 / HER2** | ADC + CAR-T in trials | 15.3 | 87.5% | 130.1 (heart) | −2.63 | 2,178 |

Three things fall out of this table.

**The method works where it should.** The four antigens that are genuinely osteosarcoma- or
mesenchyme-specific — LRRC15, MMP14, B7-H3, CDH11 — come out at ranks 1, 7, 15 and 21 of 2,434.
A screen that put B7-H3 at rank 1,800 would be worthless; this one puts it in the top 1%.

**The method is also telling us something uncomfortable.** HER2, GD2 synthase, IL11RA and EGFR
rank in the bottom half. For HER2 and EGFR this matches the clinical record: both have
repeatedly failed or underwhelmed in osteosarcoma, and HER2 expression in osteosarcoma has been
disputed in the literature for twenty years. Here HER2 sits at 15 TPM in tumours against 130 TPM
in heart — the wrong direction for a cardiotoxic ADC. GD2 is a special case and the ranking
should be ignored for it: GD2 is a glycolipid, not a protein, so `B4GALNT1` mRNA is a poor proxy
for how much antigen is on the cell, and GD2-directed agents can work regardless of what the
synthase transcript does. IL11RA at 6 TPM in 59% of tumours is a genuine concern, not an
artefact.

**ALPL illustrates the screen's biggest blind spot.** It ranks 70th, held back by 598 TPM in
liver — and that is real, bone and liver both make alkaline phosphatase. But GTEx contains no
bone, cartilage or osteoblast tissue at all. Any bone-restricted antigen therefore looks cleaner
here than it is. That applies most of all to IFITM5 below.

## Results: top 25 candidates not already in osteosarcoma trials

Ranked by therapeutic-window score. This is the "shortlist" column in the CSV: novel targets
with plasma-membrane support, after dropping genes the HPA classes as housekeeping proteins —
nuclear-pore, Golgi, lysosomal and cytochrome-P450 proteins that a membrane-prediction filter
lets through and that nobody would raise an antibody against. They are still in the CSV
(`rank_novel_surface` ignores the housekeeping filter) so the choice can be reversed.

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
| 15 | **SMO** | 58 | 100.0% | 35.0 (Nerve Tibial) | 63 (Cervix Endocervix) | 8.83 | 0.71 | 0.709 | IHC Approved, IF Supported | high |
| 16 | **VANGL1** | 16 | 97.7% | 9.5 (Esophagus Mucosa) | 9 (Esophagus Mucosa) | 13.27 | 0.72 | 0.704 | IHC Approved, IF Approved | high |
| 17 | **LHFPL2** | 36 | 100.0% | 21.9 (Artery Tibial) | 24 (Cervix Endocervix) | 14.09 | 0.69 | 0.687 | IHC Uncertain, IF Approved | high |
| 18 | **RELL1** | 23 | 97.7% | 14.2 (Brain Spinal cord cervical c-1) | 15 (Adipose Subcutaneous) | 6.76 | 0.67 | 0.651 | IHC Approved, IF Supported | high |
| 19 | **ITGA4** | 17 | 93.2% | 10.3 (Lung) | 23 (Spleen) | 35.0 | 0.68 | 0.635 | IHC n/a, IF Approved | high |
| 20 | **CSF1R** | 75 | 96.6% | 49.7 (Nerve Tibial) | 207 (Spleen) | 0.45 | 0.59 | 0.57 | IHC Approved, IF Supported | high |
| 21 | **EMP3** | 353 | 100.0% | 241.9 (Whole Blood) | 242 (Whole Blood) | 344.26 | 0.54 | 0.542 | IHC n/a, IF Approved | high |
| 22 | **ADGRA2** | 53 | 98.9% | 36.1 (Nerve Tibial) | 113 (Cervix Endocervix) | 94.05 | 0.55 | 0.539 | IHC n/a, IF Supported | high |
| 23 | **SLC1A5** | 144 | 100.0% | 106.4 (Esophagus Mucosa) | 163 (Bladder) | 282.64 | 0.43 | 0.428 | IHC Enhanced, IF Supported | high |
| 24 | **TMEM101** | 52 | 100.0% | 39.0 (Kidney Cortex) | 39 (Kidney Cortex) | 26.86 | 0.41 | 0.406 | IHC n/a, IF Approved | high |
| 25 | **PIGW** | 14 | 97.7% | 10.1 (Esophagus Mucosa) | 10 (Esophagus Mucosa) | 12.72 | 0.39 | 0.386 | IHC n/a, IF Approved | high |
All 25 have "evidence at protein level" in HPA, i.e. the protein itself has been observed, not
merely predicted from the transcript. "IHC"/"IF" are HPA's own reliability grades for its
antibody staining and immunofluorescence — `Enhanced` and `Supported` are the strong grades,
`Uncertain` means HPA itself does not trust the staining.
