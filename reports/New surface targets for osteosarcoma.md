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

## The five leads, in plain terms

### 1. LRRC15 — the screen's own validation, and already being taken

220 TPM in tumours, expressed in 97.7% of them, against 0.8 TPM in the worst vital tissue and
3.1 TPM in fibroblasts. That is a ~270-fold window, the best in the dataset, and it is not a
fluke of annotation: LRRC15 is a known ADC target. AbbVie's samrotamab vedotin (ABBV-085) was
the first attempt; the search found three current programmes naming LRRC15, and **two of them
explicitly list sarcoma**: SOT106 (NCT07801222, phase 1/2, lists osteosarcoma as a keyword) and
ZL-6201 (NCT07374848, phase 1a/b in sarcoma, recruiting), plus an imaging agent LNTH-2403
(NCT07272642). So this is not a new idea — but it is new to osteosarcoma's published literature,
which contains only 6 LRRC15 papers. **The actionable point is that these trials exist and are
recruiting now.** Anyone working on osteosarcoma should know the names.

### 2. IFITM5 — the most interesting genuinely novel hit, with a caveat built in

657 TPM in tumours, 88.6% expressing, 2.6 TPM in the worst vital tissue and **0.0 TPM in
fibroblasts**. IFITM5 (also called BRIL) is an osteoblast-specific membrane protein; mutations in
it cause osteogenesis imperfecta type V. Nothing in ClinicalTrials.gov targets it, and the
osteosarcoma literature has 9 papers. On these numbers it is the cleanest window of any
unexploited surface protein here, and the biology is coherent: osteosarcoma is a tumour of
osteoblast lineage, so an osteoblast-restricted surface protein is exactly what you would hope to
find. **But the caveat is unavoidable and specific: GTEx has no bone.** IFITM5's expression in
normal osteoblasts, growth plate and remodelling bone is simply not in this dataset, and it will
not be zero. A real assessment needs normal bone — paediatric growth plate especially, since the
patients are children who are still growing. The honest statement is "best-looking novel target
here, and the one whose risk this screen is least able to see".

### 3. ADAM12 — modest expression, excellent specificity

35 TPM in tumours but in 98.9% of them, against 1.8 TPM in the worst vital tissue (a brain
region) and 9 TPM in the worst tissue overall. HPA gives it `Enhanced` IHC reliability, the top
grade. Fibroblasts sit at 32 TPM, so part of this is mesenchymal lineage rather than tumour. No
antibody or ADC programme targets it. ADAM12 is a sheddase involved in invasion, which also
means a soluble ectodomain may circulate and soak up an antibody — worth checking before
investing.

### 4. PTK7 — the one you could test fastest

93 TPM in tumours, 98.9% expressing, 39 TPM in lung as the worst vital tissue. The window is
modest (2.3-fold), so on expression alone PTK7 would not stand out. What makes it a lead is
that **four PTK7-directed ADCs are in phase 1 right now** — HWK-007 (NCT07444814), KIVU-107
(NCT07229313, which already lists sarcoma), DAY301 (NCT06752681), and the original
PF-06647020/PTK7-ADC (NCT03243331, completed). Osteosarcoma has fewer than five PTK7 papers. A
drug that already exists and is already being given to sarcoma patients is a far cheaper
experiment than a novel antigen, and the expression data here says osteosarcoma expresses it
essentially universally.

### 5. CD248 / endosialin (TEM1) — and a piece of history worth retrieving

164 TPM, 100% of tumours, 80 TPM in coronary artery. The window is the weakest of the five, and
the fibroblast value of 578 TPM is a warning: CD248 is a pericyte and activated-fibroblast
antigen, so an antibody may be hitting stroma as much as tumour. It is on this list because the
antibody already went into children: **MORAb-004 / ontuxizumab was tested in paediatric
recurrent or refractory solid tumours (NCT01748721) and in adult solid tumours (NCT00847054),
both completed.** Those trials have results or at least safety data, and this repo's existing
work on unpublished trial results makes that a natural follow-up: find out what MORAb-004 did in
the paediatric cohort before anyone re-raises an anti-CD248 antibody.

### Also worth a look

**MRC2** (Endo180/uPARAP, 436 TPM, 100% of tumours, `Enhanced` IHC, no drug programme anywhere)
is a collagen-internalising receptor — mechanistically attractive for an ADC because it
internalises by design, which is what an ADC needs. Its fibroblast value of 259 TPM is the
problem. **CD109** (38 TPM, 96.6%, `Enhanced` IHC, no programme, under five osteosarcoma papers)
is a GPI-anchored TGF-β co-receptor. **ULBP2** is an NKG2D ligand with a clean window (17 vs 6.7
TPM) — interesting for NK-cell approaches rather than ADCs, but it is stress-induced and shed,
so surface levels are unstable. **EPHB2** and **EPHA3** both score above EPHA2, the Eph receptor
actually in trials. **ROBO1** has three CAR-NK trials (NCT03931720, NCT03941457, NCT03940820),
though all are listed with unknown status from a single centre, which is a reason for caution
rather than enthusiasm.

### Candidates that are probably artefacts, named so nobody wastes time

Three entries in the top 25 are likely to be bulk-RNA confounds rather than tumour antigens.
**CD84**, **CSF1R** and **ITGA4** are immune-lineage markers, and HPA classes CD84 and CSF1R as
immune-cell enriched or enhanced. Osteosarcoma biopsies contain abundant macrophages, so these
may be measuring infiltrate, not tumour. CSF1R in particular is a macrophage marker; targeting
it is a tumour-microenvironment strategy, not an antigen strategy. **SDC2**, **EMP3**,
**SLC1A5** and **SLC16A1** are broadly expressed and their windows are under 2-fold. And one
rank above the cut, **NDC1** and **LAPTM4A** pass the surface filter only because HPA lists the
plasma membrane as a secondary location — NDC1 is a nuclear-pore protein. They are flagged
`housekeeping` in the CSV and excluded from the shortlist for that reason.

## Caveats

These are ordered by how much they should change your reading.

**RNA is not protein.** Everything here is transcript abundance. Antigen density on the cell
surface — which is what an ADC or CAR actually sees, and what determines whether it works — can
differ from mRNA by orders of magnitude, and depends on trafficking, shedding and turnover. The
HPA columns are the only protein-level evidence in this report, and they say "this protein has
been detected somewhere", not "this protein is on the surface of osteosarcoma cells at N copies".
No candidate here is actionable without immunohistochemistry or flow cytometry on osteosarcoma
tissue.

**The normal-tissue reference contains no bone.** GTEx has 54 tissues and none of them is bone,
cartilage, periosteum or growth plate. For a tumour of osteoblast lineage this is the single
biggest gap: the normal cells most likely to share a surface antigen with the tumour are not in
the comparison at all. IFITM5 and ALPL are both directly affected. Any bone-restricted antigen's
window is overstated by this screen.

**GTEx is adult; the patients are children.** The donors are adults, most of them middle-aged or
older. Osteosarcoma occurs at the adolescent growth spurt, when bone is remodelling fast. A
target that is quiet in adult tissue may be active in a growing child, and the screen cannot see
that.

**TARGET-OS is small and nearly all diagnostic biopsies.** 88 samples, all primary tumour, all
treatment-naive or near it. Osteosarcoma kills mainly through lung metastases that appear after
chemotherapy, and antigen expression can change under treatment and at metastatic sites. Nothing
here says whether these targets are still expressed in the relapsed, metastatic disease that is
the actual clinical problem. With n=88 the confidence interval on any "% of tumours expressing"
figure is roughly ±10 points.

**Bulk RNA-seq cannot separate tumour from stroma or immune infiltrate.** This is why the
fibroblast column is in the table and why the immune-marker hits above are flagged. A high bulk
TPM can come from tumour cells, from carcinoma-associated fibroblasts, from pericytes, or from
macrophages, and the therapeutic consequences are completely different. Single-cell data would
resolve this and was not used.

**The surface annotation is noisy in both directions.** HPA's immunofluorescence localisation
excluded CD276 — a target with ADCs and CAR-T in the clinic — because it saw only vesicles, and
it excluded MMP14 and CDH11 from the plasma-membrane tier entirely. That is why the headline list
uses a loose tier and why the tier is printed in the table. The intended cross-checks for this,
the Cell Surface Protein Atlas / SURFY surfaceome and UniProt's curated subcellular locations,
were both unreachable from this environment, so there is only one annotation source here where
there should be three.

**The score is a heuristic, not a model.** The log-ratio form, the 1 TPM pseudocount, the 10 TPM
floor, the 5 TPM expression threshold and the choice of which 32 tissues count as "vital" are all
judgement calls. Different choices reorder the middle of the list. They do not change the top
few or the position of the controls, which is the main reason to believe the ranking at all.

**Expression is necessary but nowhere near sufficient.** A real target also needs to internalise
(for an ADC), not to be shed as a soluble decoy, to be homogeneously expressed within a tumour
rather than patchy, and to be absent from haematopoietic stem cells. None of that is assessed
here. ADAM12, CD248 and ULBP2 all have known shedding or soluble forms.

**DepMap was not checked.** The plan included confirming that osteosarcoma cell lines express
the top candidates, which matters because a target no cell line expresses is hard to work on
preclinically. `depmap.org` returns an HTML bot-verification challenge instead of data from this
environment, and the Sanger Cell Model Passports API is blocked by the proxy. **This step was
not done by any route.** It is the main gap in the analysis.

**Literature counts are incomplete by construction.** The repo's gene table only includes genes
with at least five osteosarcoma papers, so "n/a" above means "fewer than five", not zero. That
is still the informative direction for a novelty claim, but it is not a precise count.

**The trial search matches text, not curated target fields.** ClinicalTrials.gov has no
structured "target" field, so a target is counted when its name appears in a study's title,
interventions, keywords or summary. That misses programmes that never name the target (early
ABBV-085 records are an example of how easily this happens) and can over-count studies that
merely mention a gene as a biomarker. The counts are a floor, and the specific NCT numbers
quoted above were read individually.

## Reproducing this

```
python3 tools/surface_targets.py all        # or: gdc hpa gtex rank hpadetail context
```

Stages cache into `data/surface_targets_raw/` (git-ignored, ~350 MB of GDC files), so re-runs are
cheap and individual stages can be repeated. Two environment-specific notes: GTEx's bulk
median-TPM files on `storage.googleapis.com` returned 403/404 here, so normals come through the
API gene by gene; and the GTEx API defaults to the v10 dataset while its gene-lookup endpoint
only returns GENCODE v26 identifiers, so everything is pinned to **GTEx v8** explicitly.

## What would make this real

In rough order of value per unit effort:

1. **Immunohistochemistry on an osteosarcoma tissue microarray** for IFITM5, MRC2, CD109 and
   ADAM12. This is the step that converts the whole exercise from a hypothesis to evidence.
2. **Normal paediatric bone and growth plate expression** for IFITM5 and any other
   bone-restricted candidate. Without it the top of this list cannot be assessed for safety.
3. **Ask whether PTK7 ADCs can be tested in osteosarcoma.** Four are in phase 1; KIVU-107 already
   lists sarcoma. This needs no new molecule.
4. **Retrieve the MORAb-004 paediatric results** (NCT01748721) — an anti-CD248 antibody has
   already been given to children with refractory solid tumours.
5. **Single-cell or spatial data** to settle which of these signals is tumour and which is
   stroma or macrophage.
6. **Relapsed and metastatic samples**, since that is the disease that needs treating.
