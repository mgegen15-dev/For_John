# Orphan targets: critical close read of the osteosarcoma literature

For John — osteosarcoma research project. Four candidate "orphan" targets (substantial OS
literature, clinical-stage drug elsewhere, no OS trial registered): **DKK1, CCNE1, PTK2 (FAK),
MDM2**.

Everything below is based only on the abstract sets in the project scratchpad
(`abstracts/DKK1.txt`, `CCNE1.txt`, `PTK2.txt`, `MDM2.txt`) — 36 / 34 / 105 / 249 records.
Where an abstract does not say something, that is stated plainly rather than filled in.
Counts are counts of *abstracts*, not of independent experiments; abstracts routinely omit
cell-line numbers, animal numbers and effect sizes, so every "strength" judgement below is
capped by what abstracts can show.

A recurring caution: the auto-tags (`in_vivo=`, `patients=`) are generous. `in_vivo=True`
often means a xenograft of any kind, including one used only to confirm that knocking a gene
down shrinks a tumour, which is not the same as efficacy data from a drug. `patients=True`
often means a TCGA/TARGET re-analysis or an immunohistochemistry series, not a trial cohort.
Each section separates those.

---

## 1. DKK1 — Dickkopf-1 (drug: DKN-01 / sirexatamab, anti-DKK1 antibody)

36 abstracts. Two are retracted; one is an author correction with no content.

### 1.1 Direction and consistency

The dominant claim is that **DKK1 is pro-tumorigenic in OS and that blocking it helps** —
and, unusually, the mechanism offered is that Wnt/beta-catenin signalling is *anti*-tumorigenic
in bone, so relieving DKK1's inhibition of Wnt pushes OS cells toward osteoblastic
differentiation. That is the explicit conclusion of PMID 27049730 ("these findings suggest
that Wnt signaling is anti-tumorigenic in osteosarcoma") and of PMID 39781890 / 39713389
(same group, WAY262611, "activates canonical Wnt signaling... induces osteoblastic
differentiation... inhibiting metastasis").

Papers aligned with pro-tumour DKK1 / blockade helps:
- 17987039 — serum Dkk-1 significantly elevated in paediatric OS patients; DKK1 maximal at
  tumour periphery; immunodepletion of Dkk-1 attenuates its anti-osteogenic effect. First
  statement of the hypothesis.
- 12740383 — antibodies to Dkk-1 lengthened the lag phase (i.e. reduced proliferation) of an
  osteosarcoma line expressing it.
- 24577091 — Dkk-1 overexpression in MOS-J *increased* proliferation, stress resistance and
  produced larger, more destructive orthotopic tumours, via ALDH1 and non-canonical
  Jun-mediated Wnt. Mechanistically the keystone paper.
- 27049730 — anti-DKK-1 antibody BHQ880 in patient-derived orthotopic xenografts: slowed
  growth, inhibited metastasis.
- 35277659 — vivo morpholino (DkkMo) reduced tumour expansion, preserved bone, stimulated
  necrosis, with or without doxorubicin.
- 39805917 (correction 40038476) — DkkMo as single agent in a PDX model: slowed expansion,
  increased necrosis, inhibited metastases, preserved bone.
- 39781890 / 39713389 — small-molecule WAY262611, orthotopic implantation-amputation model:
  inhibited metastatic outgrowth, induced osteoblastic differentiation of a PDX.
- 39280613 — XD23 inhibits OS "by suppressing DKK1 expression, which in turn activates the
  WNT-beta/Catenin pathway".
- 39633066 — RBM39/c-Jun transcriptionally upregulates DKK1 -> GSK3beta-NF-kappaB; E7820
  (RBM39 degrader) suppresses growth and sensitises to cisplatin in vivo.
- 42769034 — DKK1 silencing in MG-63 reduced proliferation, colony formation, migration,
  invasion; DKK1 flagged as a candidate prognostic factor.
- 31525734 — TTN-AS1/miR-376a/DKK1 axis; DKK1 restoration reverses the tumour-suppressive
  effect of miR-376a (ncRNA paper, see 1.2).
- 28682874 — Dkk-1 *increased* in OS tissue vs adjacent (n=67); miR-107 mimic (lowering DKK1)
  reduced proliferation and tumorigenicity.

**Direct contradictions.** These are real and they matter:

1. **Oridonin, PMID 24859848, vs the whole blockade literature.** Oridonin's anti-OS effect is
   attributed to *upregulating* Dkk-1; explicitly, "Dkk-1 overexpression... can potentiate the
   proliferation inhibitory effect of ORI". Dkk-1 here is a tumour suppressor effector. This
   is the exact opposite of 24577091, where Dkk-1 overexpression made tumours bigger and more
   destructive.
2. **Compound 7m, PMID 37716273, vs XD23, PMID 39280613.** Both are small-molecule
   medicinal-chemistry papers in 143B/MG63 claiming anti-OS activity through the
   DKK1-Wnt/beta-catenin pathway — but 37716273 reports "the expression of DKK1 increased"
   as its mechanism, while 39280613 reports anti-OS activity "via downregulation of DKK1".
   Opposite directions, same pathway, same cell lines, two years apart.
3. **Is Wnt activation good or bad in OS?** 27049730 and 39781890 say Wnt activation is
   anti-tumorigenic (hence block DKK1). But 35635031 (**retracted**) and 22550000 treat
   Wnt/beta-catenin/TCF activation as pro-tumour and chemoresistance-promoting, and 22550000
   reports that *adding* DKK1 (with sFRP-1) "altered doxorubicin action in sensitive cells"
   while TCF inhibition increased doxorubicin sensitivity in vitro and in vivo. 30737824 also
   has BMP-2 driving OS growth *through* Wnt activation with Dkk-1 downregulated — i.e. low
   DKK1 / high Wnt is the pro-tumour state, the reverse of the blockade rationale.
4. **miR-152, PMID 29845282**, is internally incoherent: miR-152 overexpression is said to
   target DKK1 and inhibit proliferation "through inactivation of the Wnt/beta-catenin
   signaling pathway". Knocking down DKK1, a Wnt antagonist, should *activate* Wnt. This
   contradicts the mechanism in 28682874 even though both label DKK1 pro-tumour.

So: the therapeutic direction (block DKK1) is supported by a reasonably coherent body of
in vivo work from a small number of groups, but the underlying pathway logic is contested and
at least two anti-OS compound papers claim the opposite directionality.

### 1.2 Evidence strength

**Real in vivo efficacy from blocking DKK1 — 5 abstracts, and they are the best evidence here:**
27049730 (BHQ880 antibody, PDX, orthotopic), 35277659 (DkkMo), 39805917 (DkkMo, PDX),
39781890 and its preprint 39713389 (WAY262611, orthotopic implantation-amputation metastasis
model, PDX differentiation by scRNA-seq). Three distinct modalities — antibody, antisense
morpholino, small molecule — converge on reduced metastasis and preserved bone. That
convergence across modalities is the single strongest feature of the DKK1 case.
Add 39633066 (E7820 in vivo, but that targets RBM39, with DKK1 as a downstream node, so it is
indirect evidence for DKK1).

Caveat visible in the abstracts: 27049730, 39713389, 39781890 and plausibly 39805917 come from
the same laboratory lineage ("our lab previously demonstrated that a monoclonal antibody
against DKK-1 prevented metastatic disease"), and 24577091 / 35277659 / 39805917 share the
Dkk-1-ALDH1A1 mechanism. **Independent replication by an unaffiliated group is not visible in
this abstract set.**

**Patient tissue / outcome data — thin but real:** 17987039 (serum Dkk-1 elevated in paediatric
OS patients, median age 13.4 y; no n, no cutoff, no outcome correlation in the abstract);
28682874 (67 OS vs adjacent tissues, DKK1 up); 15087387 (earlier clinical samples, LRP5 and
metastasis); 42769034 (scRNA-seq, 140,562 cells / 17 patients, plus deconvolution in
independent cohorts — DKK1 linked to an adverse niche and shorter overall survival);
36225939 and 38622876 (DKK1 as one of the same five genes — BAMBI, TMCC2, NOX4, DKK1, CBS —
in two near-identical LASSO prognostic panels from TARGET/GEO; the second, 38622876, looks
like a re-run of the first and should not be counted as independent); 42564761 (DKK1 up under
osteoporosis-simulating conditions; the abstract itself concedes weak module-trait
correlations and an AUC of 0.693 with a CV lower bound of 0.48, i.e. worse than chance in
some folds — this paper supports nothing).

**Dog data: none.** No abstract in the DKK1 set has `dog=True`. For a target whose pitch is
metastasis prevention in a paediatric bone tumour, the absence of canine OS data is a notable
gap, since spontaneous canine OS is the standard comparative model.

**Retracted: 2.** 35635031 (Bioengineered 2022, convallatoxin/PTHR1/DKK1, MG63+U2OS,
no in vivo) and 36944905 (J Cell Commun Signal 2023, CKAP4 network map — a database/curation
paper, retracted). Neither is load-bearing for the DKK1 case, but 35635031 is one of the
sources of the "Wnt is pro-tumour" counter-current, which weakens that counter-current.

**Paper-mill-like / formulaic ncRNA:** 4 abstracts are tagged `ncrna=True` — 28682874 (miR-107,
Medicine (Baltimore)), 29845282 (miR-152, Oncol Rep), 31525734 (TTN-AS1/miR-376a/DKK1, Aging),
33789678 (miR-302b/DKK1, but in multiple myeloma, not OS). 29845282 and 28682874 are the
formulaic pattern: single miRNA, luciferase 3'UTR assay, mimic/inhibitor panel, CCK-8 and
flow cytometry, no independent model; 29845282 additionally has the backwards mechanism noted
above. 31525734 at least adds in vivo growth and survival correlation. Proportionally, DKK1 is
*less* contaminated by sponge-axis papers than is typical — roughly 1 in 9.

**Noise:** a substantial minority of the set is not about OS at all and merely uses an
osteosarcoma-derived cell line (Saos-2, UMR-106) as an osteoblast surrogate — 15962290 (PTH),
20399290 (Wnt and mitochondria), 31639434 (bile acids), 33062020 (a Chinese-medicine fracture
capsule), 36229414 (DKK1 and mineralisation), 33794753 (ganetespib, where DKK1 is one of 14
genes on an array). These should not be counted as osteosarcoma DKK1 papers. Realistically the
OS-specific DKK1 literature here is about 18-20 papers, not 36.

### 1.3 Biomarker

**This is the weakest part of the DKK1 case.** There is a plausible biomarker *modality* —
circulating DKK1 — but no usable threshold or frequency anywhere in these abstracts.

- 17987039: serum Dkk-1 "significantly elevated" in paediatric OS patients. No n, no
  percentage above a cutoff, no control distribution given in the abstract.
- 27049730: human DKK-1 detectable in the blood of tumour-bearing mice and "a correlation
  between DKK-1 level and tumour proliferation" — a preclinical pharmacodynamic marker, not a
  patient selection marker.
- 28682874: DKK1 increased in OS vs adjacent tissue across 67 patients — direction only, no
  frequency of "DKK1-high".
- 42769034: DKK1 associated with the IBSP+/SPARC+ double-high niche and shorter overall
  survival; no DKK1-high frequency given.
- 36225939 / 38622876: DKK1 is 1 of 5 genes in a risk score — a score, not a selectable
  subgroup, and the two papers are effectively one result.

**No abstract reports what fraction of osteosarcomas are DKK1-high, nor a serum cutoff with
sensitivity/specificity.** A trial could in principle enrich on serum DKK1, but nothing here
tells you where to set the bar or how many patients would qualify. By contrast with MDM2 and
CCNE1, where amplification gives a binary biomarker, DKK1 offers only a continuous
expression/secretion marker of undefined distribution.

### 1.4 Has the clinical-stage drug been tested in OS models?

**DKN-01 / sirexatamab itself: not in this abstract set.** No abstract mentions DKN-01.

**Close analogues: yes, three, all positive.**
- **BHQ880**, a different anti-DKK1 monoclonal antibody, in patient-derived orthotopic
  xenografts (27049730): slowed primary growth, inhibited metastasis, increased nuclear
  beta-catenin and osteopontin. This is the closest existing read-out for what DKN-01 might do.
- **WAY262611**, small-molecule DKK1 inhibitor (39781890 / 39713389): inhibited metastatic
  outgrowth of disseminated tumour cells, induced osteoblastic differentiation of a PDX in vivo.
- **DkkMo**, vivo morpholino knocking down Dkk-1 transcription (35277659, 39805917): single-agent
  reduction of tumour expansion and metastases, bone preservation, additive with doxorubicin.

Nothing reports a failure of DKK1 blockade in an OS model. No abstract reports toxicity
limiting DKK1 blockade, though 39805917's claim to "safely target" is an assertion about mice.

### 1.5 Verdict — **moderate (the strongest non-MDM2 case here, and the most trial-ready)**

Three independent modalities of DKK1 blockade — antibody, morpholino, small molecule — reduce
metastasis and preserve bone in orthotopic and patient-derived xenograft models, which is
exactly the endpoint that matters clinically, and a clinical-stage antibody analogue (BHQ880)
has already produced that result. Against that: the work traces to a narrow set of related
groups with no visible independent replication, the pathway rationale is directly contradicted
by papers in which DKK1 upregulation is the *anti*-tumour mechanism (24859848, 37716273), and
there is no quantified patient-selection biomarker and no canine data at all.

**Single most important missing experiment:** an independent-laboratory test of DKN-01 (not an
analogue) in at least two patient-derived orthotopic OS models with a metastasis endpoint,
reporting pre-treatment tumour and serum DKK1 so that a selection threshold and the fraction of
DKK1-high tumours can be defined. A spontaneous canine OS arm would simultaneously close the
comparative-model gap.

---

## 2. CCNE1 — cyclin E1 (drugs: CDK2 inhibitors BLU-222, INX-315, PF-07104091)

34 abstracts. Three are retracted.

### 2.1 Direction and consistency

**Direction is consistent and essentially uncontested: CCNE1 is oncogenic in OS, amplified,
overexpressed, and associated with worse outcome.** No abstract in this set claims a tumour-
suppressive role for cyclin E1 in osteosarcoma, and no abstract reports that raising CCNE1 is
beneficial. In that narrow sense CCNE1 is the cleanest of the four targets.

The anchor papers:
- 21458381 — whole-genome tiling-path aCGH on 22 OS tumours; CCNE1 emerged from GISTIC as a
  novel amplified target, confirmed by FISH and immunohistochemistry. Title is literally
  "Cyclin E1 is amplified and overexpressed in osteosarcoma".
- 32162720 — 69-patient tissue microarray; cyclin E1 high in 61%; expression correlated with
  disease status, inversely with prognosis *and* with response to neoadjuvant chemotherapy;
  independent prognostic factor; siRNA knockdown reduced proliferation and increased
  chemosensitivity.
- 40959067 — a cytoplasmic low-molecular-weight cyclin E1 isoform (LMW-cyclin E1) generated by
  neutrophil elastase (ELA2) cleavage, associated with poor overall and progression-free
  survival; 34 primary and 33 lung-metastasis tissues; depleting neutrophils or inhibiting ELA2
  suppressed malignancy, validated in BALB/c mice.
- 29109143 — loss of miR-874-mediated restraint on CCNE1 is described as "a general feature of
  osteosarcomas", with elevated CCNE1 producing aggressive phenotypes.

**The one genuine contradiction is about the biomarker, not the biology.** 33969640 (multi-region
WGS of a 4-year-old index case plus reanalysis of 258 high-grade OS) concludes that focal MYC
amplification is enriched in children "but not CCNE1", and that "CCNE1 appears recurrently
amplified independent of age". 42424099 (653 patients, Foundation Medicine) and 39688743
(204 patients, C-CAT) both report the opposite: CCNE1 alterations are *significantly* more
frequent in paediatric/adolescent and younger patients. Since the whole point of a CCNE1 trial
would be selecting an enriched population, this disagreement is practically important and
unresolved in these abstracts. 33969640 also calls MYC/CCNE1 co-amplification "a rare driver
event", which sits awkwardly with the larger cohorts' framing of CCNE1 as recurrent.

### 2.2 Evidence strength

**This is where CCNE1 collapses. There is no in vivo efficacy data from blocking CCNE1 or CDK2
in osteosarcoma anywhere in this abstract set.**

- The only direct CCNE1 perturbation with a functional read-out is **siRNA in vitro** (32162720):
  reduced proliferation, increased chemosensitivity. No animal arm.
- Three xenograft studies exist but perturb a microRNA, not CCNE1: 24449507 (miR-132, in vivo
  tumour growth suppressed, CCNE1 as the 3'UTR target), 29109143 (miR-874 restoration, xenograft
  tumours suppressed), 32000044 (miR-154-5p -> E2F5 -> cyclin E1/CDK2, xenograft). In each, CCNE1
  is downstream of a pleiotropic miRNA; none isolates CCNE1 as the effector in vivo.
- 40959067 has genuine in vivo work, but the intervention is neutrophil depletion / ELA2
  inhibition — i.e. it targets the protease that *creates* LMW-cyclin E1, not cyclin E1 or CDK2.

**Nearly half the set does not study CCNE1 at all.** In roughly 16 of 34 abstracts cyclin E1 is
only a downstream western-blot band that falls when something else is inhibited — a cyclin
checked off alongside cyclin D1, CDK2, CDK4, SKP2 and p21: 19455146 (Notch / gamma-secretase
inhibitor), 20067614 (SMO / cyclopamine), 27840911 (USP1), 25578779 (UCHL1), 31737187 (Angptl2),
29636527 (viscumTT mistletoe extract), 32970611 (p38gamma), 32774476 (SLC25A10), 34474553 (POGZ),
26478521 (dihydrotanshinone I), 31948366 (baicalein), 35744840 (dihydrotanshinone I again),
22682620 (miRNA profiling in six cell lines), plus the three retracted ones below. These say
nothing about whether blocking cyclin E1 helps; they are evidence that OS cells proliferate.

**Patient tissue / outcome data — paradoxically the strongest of the four targets, and all of it
genomic:** 21458381 (n=22), 32162720 (n=69 TMA with survival and chemo-response), 36996377
(n=92 primary + n=86 validation, OncoPanel/MSK-IMPACT), 37812025 and its preprint 36711976
(n=37 samples from 8 patients, longitudinal WGS), 39688743 (n=204), 35756627 (n=357 bone
tumours, prospective multicentre), 42424099 (n=653), 42779977 (n=236 WGS), 38884816 (n=15
craniofacial), 33969640 (n=258 reanalysed), 40959067 (n=34 + 33), 32299473 (single case report).
That is a large, genuinely clinical evidence base — but it is all descriptive genomics. It
establishes that CCNE1 is amplified and bad, not that inhibiting it works.

**Dog data: none.**

**Retracted: 3.** 31001861 (J Cell Physiol 2019, nimotuzumab/EGFR, MG-63+U2OS — note the
mangled drug name "Nimotuzuma" throughout), 30733679 (Front Pharmacol 2018, DDX5/TCF12/cyclin
E1, MG63), 35005025 (Biomed Res Int 2021, PAK4, U2-OS+MG-63, MTT and wound healing only).
All three are exactly the pattern to distrust: two cell lines, no in vivo, CCNE1 as a
downstream band. 35005025 additionally reports PAK4 positively correlating with both p21 and
the cyclins, which is incoherent.

**Paper-mill-like / formulaic ncRNA: 4 tagged `ncrna=True`** — 24449507 (miR-132, Tumour Biol),
22682620, 29109143 (J Biol Chem, the most substantial of them), 30425578 (CDR1as/miR-7
circRNA sponge axis in U2OS+MG63, with CCNE1 as one of four listed miR-7 targets alongside
EGFR, PI3KCD and RAF1 — the canonical sponge-paper shape). 30425578 is the clearest paper-mill
signature in this set.

### 2.3 Biomarker

**A selectable biomarker clearly exists in principle — CCNE1 amplification is binary, detectable
on standard clinical NGS panels, and even detectable in liquid biopsy (42779977). But the key
number is missing from every abstract.**

What the abstracts actually give:
- **61%** of 69 OS tumours have high cyclin E1 **protein** by IHC (32162720). This is
  overexpression, not amplification, and 61% is high enough that it barely selects anyone.
- **58%** of 236 WGS tumours carry at least one of five clustered structural-variant hotspots,
  of which CCNE1 amplification is one of four oncogene hotspots (42779977). The CCNE1-specific
  share is not broken out.
- **43%** of 15 craniofacial OS cases had "potentially actionable" amplifications — but that is
  a pooled figure across CCNE1, AKT2, MET, NTRK1, PDGFRA, KDR, KIT, MAP3K14, FGFR1 and AURKA
  (38884816), so it tells you nothing about CCNE1 alone.
- CCNE1 is listed among the most frequently altered genes in 92 advanced OS patients (36996377),
  357 bone tumours (35756627) and 653 young OS patients (42424099) — **named but never
  quantified in any of these abstracts.**
- Enriched in paediatric/adolescent (42424099) and younger (39688743) patients; contradicted by
  33969640 as above.

Two further complications a trial would have to confront, both visible in the abstracts:
1. **Subclonality.** CCNE1 amplification is reported specifically in treatment-*resistant*
   subclones that emerge at relapse (37812025 / 36711976). A single diagnostic biopsy may miss
   it, and its presence may be a marker of a clone rather than of the tumour.
2. **Isoform.** The prognostically important species may be LMW-cyclin E1, a cleavage product
   (40959067), which no amplification assay or standard IHC distinguishes.

So: **no abstract in this set reports the frequency of CCNE1 amplification in osteosarcoma.**
That figure is the single thing a trial design would need first, and it is absent.

### 2.4 Has the clinical-stage drug been tested in OS models?

**No. Zero abstracts.** Neither BLU-222, INX-315 nor PF-07104091 appears anywhere in the CCNE1
set, and no other CDK2-selective inhibitor does either. There is not even an older or dirtier
analogue tested — no CDK2/CDK1 tool compound, and no CDK4/6 inhibitor used as a comparator.
The closest thing to a pharmacological cell-cycle intervention in these abstracts are
non-specific natural products (baicalein 31948366, dihydrotanshinone I 26478521 / 35744840,
viscumTT 29636527) and pathway inhibitors upstream of the cyclins (gamma-secretase inhibitor
19455146, cyclopamine 20067614), none of which speaks to CDK2 dependence.

The question "is CCNE1-amplified osteosarcoma dependent on CDK2?" has, on this evidence, never
been asked. That is a striking gap for a target with this much patient genomic data behind it.

### 2.5 Verdict — **weak as a trial case today, despite the best biomarker (call it "biomarker
without a drug rationale")**

CCNE1 has the most consistent direction and by far the most patient genomic data of the four
targets — amplified, overexpressed in 61% by IHC, prognostic, present in resistant subclones,
detectable by routine panels and liquid biopsy — and three CDK2 inhibitors are in the clinic.
But the functional osteosarcoma evidence is one in-vitro siRNA experiment (32162720) plus three
microRNA xenografts that do not isolate CCNE1, and **no CDK2 inhibitor has ever been reported
in an osteosarcoma model**; half the abstract set only uses cyclin E1 as a proliferation
read-out. The amplification frequency — the number the trial would be sized on — appears in
none of these abstracts.

**Single most important missing experiment:** test a clinical CDK2 inhibitor (BLU-222, INX-315
or PF-07104091) across a panel of CCNE1-amplified versus CCNE1-non-amplified osteosarcoma PDX
models for a dependency signal, and in the same work report CCNE1 amplification frequency by
FISH/NGS in a defined OS cohort so the selectable fraction is known. Without a demonstrated
amplification-dependent response, the biomarker selects a subgroup for a drug with no evidence
of activity in this disease.

---

## 3. PTK2 / FAK (drug: defactinib, FDA-approved 2025 with avutometinib for KRAS-mutant
low-grade serous ovarian cancer)

105 abstracts — the largest set after MDM2. One is retracted.

### 3.1 Direction and consistency

**The consensus direction is that FAK is pro-tumorigenic in OS — specifically pro-invasive and
pro-metastatic — and that inhibiting it reduces migration, invasion and lung metastasis.** This
is supported very broadly but almost entirely *indirectly*: the overwhelming majority of these
abstracts study some other molecule and report FAK phosphorylation as the downstream conduit.

Papers where FAK itself is perturbed and the direction is pro-tumour:
- 24092571 — shRNA knockdown of FAK in SAOS-2 induced caspase-dependent apoptosis and reduced
  proliferation; additive with cisplatin.
- 24798118 — the same experiment in rat OSR-6 cells, same result (same group, essentially a
  companion paper).
- 26393679 — siRNA knockdown of FAK in MG63 and 143B reduced migration, invasion, proliferation
  and increased apoptosis; FAK/pFAK overexpressed in 113 patient tumours.
- 29849782 — siRNA knockdown reduced invasion and proliferation, promoted apoptosis;
  FAK higher in OS tissue than paired normal.
- 26137126 — among 143B subclones, higher FAK tracked with stronger migration; FAK siRNA cut
  migration and lamellipodia from 35% to 11%.
- 22158627 — siRNA depletion of PTK2 (or RUNX2, or TLN1) diminished U2OS motility.
- 28406574 — the FAK inhibitor **PF562271** suppressed proliferation and colony formation,
  induced apoptosis, and reduced xenograft tumour volume, weight and angiogenesis in vivo.
- 37013056 — FAK inhibition reduced proliferation and migration in vitro and LOX-mediated lung
  metastasis in an orthotopic model.
- 38641310 — platelet-specific FAK-deficient mice; FAK inhibition suppressed OS progression via
  an F3/TGF-beta loop.
- 42520958 — FAK inhibition suppressed IQGAP3-driven migration and lung metastasis in vivo;
  pharmacological FAK *activation* rescued it, a proper two-way test.
- 39279704 — the FAK inhibitor Y15 reversed COL12A1-driven proliferation and invasion.
- 33799345 — the FAK inhibitor PF-573228 synergised with timosaponin AIII against migration
  and invasion.

**Direct contradictions, and there are several substantive ones:**

1. **FAK is not required for anoikis resistance — PMID 16759849.** In SAOS-2 cells, Src and
   PI3K/Akt drive anoikis resistance while FAK shows a normal dephosphorylation pattern,
   concluding survival is mediated "in a manner independent of FAK activity". Directly against
   the apoptosis results of 24092571 / 24798118 in the same SAOS-2 background.
2. **FAK is not overexpressed in OS at all — PMID 12376862.** Immunohistochemistry plus
   real-time PCR in high-grade osteosarcomas: FAK is expressed but "an overexpression at the
   transcriptional level could not be detected", with Pyk2 mRNA decreased. This flatly
   contradicts 26393679, 29849782 and 28846700, which report FAK overexpression in 90%+ of
   cases. Unresolved in these abstracts, and it matters: if FAK is not overexpressed, the
   therapeutic rationale rests on activity rather than abundance.
3. **Total FAK carries no prognostic information — PMID 28846700.** Total FAK was overexpressed
   in 90.6% of 53 cases but "was not correlated with any clinicopathologic characteristics or OS";
   only pFAK-Y397 (62.3%) was prognostic. 26393679, by contrast, found the FAK expression
   profile itself an independent predictor in 113 patients. These two are in tension about
   what to measure.
4. **FAK as a brake rather than an accelerator — PMID 15485819.** In U2OS, FAK is described as
   a negative regulator of RhoA; FAK activation was *reduced* in cells with suppressed spreading
   and motility, and FAK overexpression *rescued* the motility defect. Here more FAK means more
   normal motility, not more malignancy.
5. **Non-monotonic FAK — PMID 11346466.** Low LPA raises FAK phosphorylation and increases
   invasion; high LPA lowers FAK phosphorylation and *decreases* invasion, while also
   suppressing MMP2. The authors call Rho's effect on invasion "dual". A target with a
   non-monotonic dose-response is awkward to drug.
6. **FAK dispensable for mechanotransduction — PMID 20814573.** Cyclic stretch induced stress
   fibre alignment and MAPK phosphorylation "to comparable levels in FAK-null and FAK-expressing"
   cells, explicitly against the prevailing view cited in that abstract.
7. **High FAK turnover can impede migration — PMID 35008585.** Constitutively active STIM1
   dramatically increased turnover of FAK, paxillin and vinculin yet *impeded* migration, while
   dominant-negative STIM1 decreased turnover and *promoted* migration — the authors themselves
   flag these as "unexpected results".
8. **Opposite effects depending on how YAP is removed — PMID 31376525.** In Saos cells,
   verteporfin strikingly reduced FAK protein and phosphorylation while YAP RNAi *increased*
   both. The same nominal intervention produces opposite FAK outcomes by method.

So the direction is broadly consistent at the level of "FAK phosphorylation accompanies
invasion", but the abstracts contain repeated, named exceptions where FAK is dispensable,
not overexpressed, non-prognostic, or protective. This is a different kind of weakness from
DKK1's: not a disputed therapeutic direction, but a target so pleiotropic that its necessity
varies by context and cell line.

### 3.2 Evidence strength

**In vivo efficacy from pharmacologically blocking FAK — only about 4 abstracts, and only one
is a clean single-agent test:**
- **28406574** is the key paper: PF562271, orally administered, dramatically reduced xenograft
  tumour volume, weight and angiogenesis. This is the strongest single piece of evidence that a
  clinical-type FAK inhibitor does something in OS.
- 37013056 — FAK inhibition reduced LOX-mediated metastasis in an orthotopic xenograft model
  (FAK inhibition as a mechanistic arm, not a dedicated efficacy study).
- 42520958 — FAK inhibition reduced IQGAP3-driven lung metastasis in vivo.
- 38641310 — genetic, not pharmacological: platelet-specific FAK knockout mice.

**The rest of the in vivo tally is illusory.** 44 abstracts are tagged `in_vivo=True`, but in
nearly all of them the intervention is something else entirely and FAK is a western-blot band
in the mechanism figure. Representative: TSP1 knockdown (29100277), SPON1 knockdown (26032498),
CD248 knockdown (36997926), Tspan7 (35524311), Tspan9 (35280793), NELL1 deletion (35700263),
CD155 antibody (29725446), NRP1 silencing (39427726), SLC25A22 (30482097), PDGFRB (39505287),
ZIP10 (34706747), SQLE/FR194738 (38372422), CXCL1 (32079335, 34760697), IL-8 antibody
(38302407, 29625612), HSP90 inhibitor PF4942847 (26712686), cobimetinib (32736683),
romidepsin (39427726), larotrectinib (39247831). Each of these tells you FAK sits in a
metastasis pathway; none tells you that blocking FAK is sufficient.

**The natural-product layer is large and low-value.** At least 15 abstracts are
plant-extract/compound screens in one or two cell lines reporting reduced p-FAK among a long
list of downregulated proteins: silibinin (17116726), deguelin (25322282), Corni Fructus
(23955962), Yangzheng Xiaoji (23828123), 3-hydroxyflavone (27600294), fisetin (31028200),
indirubin-3'-monoxime (31050877), timosaponin AIII (33799345), cinnamaldehyde (35678522),
psoralidin (37004120), Paris polyphylla (28385078), melatonin (29766567 — which explicitly
found *no* effect on FAK), reversine (38706714), benzamil (38569602), zoledronate (26848867),
plus two vanadium-complex papers (27175625, 33107537) and assorted nanoparticle studies
(31263675, 32618992 with correction 34236351, 42734289). Several of these list 15-20 proteins
all moving in the convenient direction, which is a hallmark of weak specificity. 23955962 and
31028200 are near-identical in structure (U-2 OS, MMP-2/-9, long western panel) and
25322282 ends by conceding it provides only "the rationale for in vivo studies".

**Patient tissue / outcome data — the best of the four targets for this target class, and
genuinely useful:**
- 26393679 — 113 primary OS patients; FAK and pFAK both overexpressed; FAK/pFAK profile an
  independent predictor of overall *and* metastasis-free survival.
- 28846700 — 53 patients; total FAK overexpressed in **90.6%** (48/53), pFAK-Y397 in **62.3%**
  (33/53); pFAK-Y397 an independent prognostic predictor of OS and post-metastasis OS, and it
  separated good from poor responders to neoadjuvant chemotherapy.
- 23845472 — 36 pre-treatment biopsies; a three-marker panel of **beta5 integrin + FAK +
  GSK3beta** discriminated good from poor chemotherapy responders with AUC **89.9%** and
  diagnostic accuracy **90.3%**. The abstract explicitly proposes this to "select patients for
  whom an alternative protocol using inhibitors of this pathway can be proposed" — i.e. a
  ready-made enrichment strategy.
- 28406574 — pFAK-Y397 high in primary human tumours and associated with prognosis and lung
  metastasis.
- 25123071 — FAK higher in vasculogenic-mimicry-positive tumours (15/66, 22.7%), and VM itself
  an independent adverse prognostic factor.
- 12376862 — the dissenting series above.

**Dog data: none in the PTK2 set.** All four canine abstracts in this whole collection sit in
the MDM2 file. This is a real missed opportunity given that the NIH-funded FAK work is at
Colorado State, a veterinary school, and canine OS is the obvious bridging model.

**Retracted: 1.** 31122179 (Technol Cancer Res Treat 2018, AURKB proteomics, U2-OS+143B), which
happens to be one of the few abstracts that names PTK2 explicitly as the mediator —
so the retraction removes a PTK2-specific claim rather than a peripheral one.

**Paper-mill-like / formulaic ncRNA: 7 tagged `ncrna=True`**, a low proportion (7%) — 24391788
(miR-133b), 27812189, 27826039 (chondrosarcoma, not OS), 28406476 (WISP-1/miR-381), 33342156
(lncRNA-SRLR, U2OS only, Chinese-language journal, FAK/STAT3 axis), 34884541 (CCL4/miR-3927-3p),
39247831 (NGF/miR-513c-5p). 33342156 is the clearest formulaic single-cell-line axis paper.
Several of the Taiwanese chemokine papers (28406476, 34884541, 39247831, 32079335, 34760697)
share an identical template — chemokine, FAK/PI3K/Akt, a miRNA, VCAM-1 or VEGF-A — and should be
treated as one body of work rather than five independent findings.

**Noise:** a meaningful slice of the set uses U2OS or MG-63 purely as a convenient
cell-biology chassis and is not about osteosarcoma: 17997086 (perlecan peptide), 14584897
(BK channel mechanotransduction), 25550780 (mechanical strain), 23754369 (focal adhesions under
stretch), 35594862 (MARK2), 38801098 (paxillin/Hic-5 interactome), 22028271 (HIV-1 and CCR5!),
20814573. Realistically the OS-specific FAK literature is perhaps 70-80 papers, of which
roughly a dozen manipulate FAK itself.

### 3.3 Biomarker

**FAK offers the most immediately usable patient-selection biomarker of the four targets — but
it is an immunohistochemical activity marker, not a genomic one, and the field disagrees about
which form to measure.**

Frequencies actually reported:
- **90.6%** total FAK overexpression and **62.3%** pFAK-Y397 overexpression in 53 patients
  (28846700). pFAK-Y397 is the prognostic one; total FAK is not.
- FAK and pFAK both overexpressed in 113 patients, with four strata (FAK-/pFAK-, FAK+/pFAK-,
  FAK+/pFAK+) separating overall and metastasis-free survival (26393679). No percentage given
  per stratum in the abstract.
- A **three-protein panel (beta5 integrin, FAK, GSK3beta)** in 36 pre-treatment biopsies
  predicting chemotherapy response at AUC 89.9% / accuracy 90.3% (23845472).
- FAK elevated in the **22.7%** of osteoblastic OS showing vasculogenic mimicry (25123071).
- Against all of this, 12376862 reports no transcriptional overexpression of FAK.

So a trial could plausibly select on pFAK-Y397-high by IHC (~62% of patients) or on the
beta5/FAK/GSK3beta profile (which selects poor chemotherapy responders — arguably the right
population for a new agent). The weaknesses are that pFAK-Y397 IHC is notoriously
preanalytically fragile (phospho-epitopes degrade; the abstracts do not address assay
standardisation), 62% is a weak enrichment, and no abstract reports a *genomic* PTK2 alteration
frequency in OS at all. There is no PTK2 amplification figure anywhere in this set.

### 3.4 Has the clinical-stage drug been tested in OS models?

**Defactinib itself: not in this abstract set.** No abstract mentions defactinib, VS-4718,
GSK2256098 or avutometinib.

**Close analogues: yes, and the results are encouraging but thin.**
- **PF562271** (PF-562271, a clinical-stage FAK/Pyk2 inhibitor from the same generation as
  defactinib), 28406574: oral dosing dramatically reduced xenograft tumour volume, weight and
  angiogenesis; in vitro it suppressed proliferation and colony formation, induced apoptosis
  and downregulated Akt/mTOR. **This is the single most relevant experiment in the PTK2 file.**
  Limitations visible in the abstract: subcutaneous xenografts, no metastasis endpoint stated,
  no biomarker-stratified comparison, single study.
- **PF-573228** (33799345): used only as a mechanistic co-treatment with timosaponin AIII;
  synergistic on migration/invasion, no single-agent in vivo efficacy reported.
- **Y15** (1,2,4,5-benzenetetraamine tetrahydrochloride): 21056138 (blocked pressure-stimulated
  adhesion in vitro) and 39279704 (reversed COL12A1 effects in vitro). No in vivo.
- Unnamed "FAK inhibition" in 37013056 and 42520958 reduced metastasis in vivo.

Nothing reports a failure of FAK inhibition in an OS model. No abstract addresses the
avutometinib-style combination rationale directly, though 32736683 (cobimetinib, a MEK
inhibitor, synergising with doxorubicin and acting partly through FAK inhibition) is
suggestive that MEK and FAK blockade intersect in OS — the closest thing in this collection to
support for the approved defactinib + MEK-inhibitor pairing.

### 3.5 Verdict — **moderate, and the most immediately actionable of the four**

FAK's direction is consistent across a very large literature, there is a clinical-stage
analogue with positive single-agent in vivo activity in OS (PF562271, 28406574), an approved
drug is available now, and — uniquely among these four — there are validated patient-selection
assays in hand: pFAK-Y397 IHC in 62.3% of patients (28846700) and a beta5/FAK/GSK3beta panel
that predicts poor chemotherapy response at 90% accuracy (23845472). Against that, almost all
of the 105 abstracts are FAK-as-a-downstream-band rather than FAK-as-a-target, only about a
dozen manipulate FAK itself, and there are repeated credible reports that FAK is dispensable
(16759849, 20814573), not overexpressed (12376862), non-prognostic in its total form
(28846700) or even protective (15485819, 35008585).

**Single most important missing experiment:** defactinib itself in orthotopic/PDX osteosarcoma
models with a **lung-metastasis** endpoint (not just subcutaneous tumour volume), stratified by
baseline pFAK-Y397, and tested both alone and combined with a MEK inhibitor to mirror the
approved regimen. A spontaneous canine OS arm is the natural second step and is wholly absent.

---

## 4. MDM2 (drugs: milademetan, brigimadlin, idasanutlin, navtemadlin — all require wild-type TP53)

249 abstracts, by far the largest set, and the only one containing canine data (4 papers).
Three are retracted. Read by triage: amplification/frequency papers, MDM2-inhibitor papers,
patient series and in vivo work read in full; the large tail of 1990s-2000s p53 cell-biology
papers that merely use U2OS or Saos-2 as a p53-wild-type / p53-null pair was skimmed.

### 4.1 Direction and consistency

**Direction is not in dispute.** MDM2 is an oncogene that restrains p53; amplification or
overexpression inactivates p53 indirectly; disrupting the MDM2-p53 interaction reactivates p53
and kills MDM2-amplified, TP53-wild-type cells. Every relevant abstract agrees, and I found
**no paper claiming MDM2 is tumour-suppressive in osteosarcoma or that blocking it is harmful
to tumour control.** On pure consistency, MDM2 is the cleanest of the four.

The contradictions here are not about direction but about **whether the drug mechanism matches
the disease**, and they are serious:

1. **MDM2 has p53-independent oncogenic functions that an MDM2-p53 interaction inhibitor would
   not touch — PMID 14610316.** In the MDM2-overexpressing, p53-wild-type osteosarcoma line
   OsACL, UV raised p53 levels but that p53 was *transcriptionally inactive*, and the induced
   rise in MDM2 was itself p53-independent; antisense MDM2 restored apoptosis. If part of MDM2's
   contribution is p53-independent, nutlin-class drugs address only a fraction of it.
2. **MDM2-amplified osteosarcoma is biologically distinct from TP53-mutant osteosarcoma —
   PMID 12972634.** TP53 mutation correlates strongly with high genomic instability in human OS,
   but "osteosarcomas harboring an amplification of the HDM2 oncogene... do not display high
   levels of genomic instability". The authors conclude the two routes to p53 inactivation "may
   have different cellular consequences". MDM2-amplified OS may simply be a different, more
   indolent disease — which 4.3 below confirms.
3. **Resistance arises by the obvious route — PMID 26070072.** SJSA-1 cells under prolonged
   SAR405838 acquire TP53 DNA-binding-domain mutations in vitro; in vivo, tumours regrow and the
   sublines carry a heterozygous C176F TP53 mutation. Notably, in vitro resistance was
   *profound* while in vivo resistance was only 3-5 fold — the abstract explicitly flags this
   discrepancy, which is a warning about how much weight to put on in vitro potency.
4. **On-target bone toxicity — PMID 17592964.** Nutlin-3 suppresses proliferation *and
   differentiation* of human pre-osteoclasts through p53, and reduced osteoclast formation in
   SaOS-2 co-culture. Framed there as a therapeutic bonus for osteolytic disease, but in a
   growing child with a bone tumour, p53 activation in the osteoclast/osteoblast compartment is
   a toxicity question no abstract here addresses.
5. **Opposing modifier effects — PMID 28696156.** The IGF-1R/AKT pathway has "opposing effects"
   on nutlin-3a-induced apoptosis in MDM2-amplified MHM osteosarcoma cells: it suppresses
   apoptosis as a survival pathway, yet inhibiting it *reduces* p53 accumulation and increases
   protective autophagy. Combination strategy is therefore not straightforward.

### 4.2 Evidence strength

**In vivo efficacy from blocking MDM2 — the richest of the four targets by volume, and the most
dramatic single results, but concentrated in one cell line.**

- **SAR405838 / MI-77301** (25145672): a *single oral dose* achieved complete tumour regression
  in the SJSA-1 osteosarcoma xenograft. This is the most striking efficacy result anywhere in
  all four files.
- **RG7112** (23400593): across a solid-tumour panel, "the best response observed in
  osteosarcoma cells with MDM2 gene amplification"; oral dosing produced tumour inhibition and
  regression.
- **Nutlin-3a** (22843172): p53-dependent G1 arrest and apoptosis in OS lines in vitro and in
  vivo, abolished by p53 siRNA; the authors conclude it "might be beneficial for OS patients
  with MDM2 amplification and wt p53 status" — an explicitly biomarker-conditioned claim.
- **MK-8242** (27238606), Pediatric Preclinical Testing Program — **and this is the most
  important negative result in the entire collection.** Median IC50 was 0.07 µM in TP53-wild-type
  lines versus >10 µM in TP53-mutant lines, and the in vivo activity figure is reported as
  "10 of 17 (59%) of TP53 wild-type solid tumour xenografts, **excluding osteosarcoma xenografts
  that have very low TP53 expression**". The paediatric preclinical panel's osteosarcoma models
  had to be set aside because they were not p53-competent.
- **SAR405838 resistance study** (26070072) and **HDM201 translational modelling** (as indexed at
  line 762) add mechanism and schedule rather than new efficacy.
- **RG7388 (= idasanutlin) derivatives** (41962329): fluorinated analogues as 18F PET probes;
  [18F]1 showed high uptake and specificity in SJSA-1 and U2OS and higher uptake in SJSA-1
  xenografts than muscle. This is an imaging rather than an efficacy study, but it is direct
  evidence that an idasanutlin scaffold engages MDM2 in osteosarcoma models in vivo.
- A large medicinal-chemistry tail (the AMG 232 and AM-7209 discovery papers,
  piperidinones, morpholinones, sulfamide/triazole benzodiazepines, the fluorinated indole
  30715803) uses SJSA-1 and the U2OS-versus-SAOS-2 pair as the standard potency and
  p53-selectivity assay.

**The single-cell-line problem is acute.** SJSA-1 appears 18 times in this file. It is an
MDM2-amplified, TP53-wild-type osteosarcoma line, and it is the field's *generic* MDM2-inhibitor
test system — used because it is the most MDM2-dependent cell line available in any tumour type,
not because anyone is developing a drug for osteosarcoma. Much of this apparent osteosarcoma
evidence is pharmacology that happens to be done in an osteosarcoma cell. 30715803 is
explicit about the design: p53wt U-2 OS and SJSA-1 versus p53del SAOS-2. **No abstract reports
an MDM2 inhibitor in a patient-derived or orthotopic osteosarcoma model, and none reports a
metastasis endpoint.**

**Patient tissue / outcome data — large, old, and mostly small cohorts:** 86 abstracts carry
`patients=True`. The substantive ones are listed with their numbers in 4.3. Much of this is
1990s-2000s Southern-blot and immunohistochemistry work on 20-90 tumours, plus a long tail of
single-case diagnostic reports (dedifferentiated liposarcoma versus osteosarcoma, craniofacial
lesions, GLI1-rearranged neoplasms) where MDM2 FISH is a *diagnostic* test rather than a
therapeutic biomarker. There is no modern large-cohort MDM2 amplification frequency paper in
this set comparable to the 653-patient CCNE1 cohort.

**Dog data — 4 papers, all of which argue *against* MDM2 as a canine-bridgeable target:**
- 9891508 — 21 canine osteosarcomas: no p53 or Rb deletions/rearrangements; "the MDM2 gene
  appeared to be duplicated in one canine tumor but no cases of significant amplification were
  detected"; TP53 point mutations in 38%.
- 10643981 — five canine OS cell lines: p53 function defective in *every* line, with mdm2
  itself failing to be induced; three lines had DNA-binding-domain mutations.
- 11453492 — centrosome hyperamplification in spontaneous canine tumours.
- 24200963 — CREBZF/unfolded protein response acting through p53.
So the comparative model has essentially no MDM2 amplification and near-universal p53
dysfunction. A canine trial of an MDM2 inhibitor would have almost no eligible patients.

**Retracted: 3.** 31126199 and 30942624 (both Artif Cells Nanomed Biotechnol 2019, a Ras/K-Ras
histone-modification pair from what looks like one group) and 30005830 (Life Sci 2018,
GRIM-19/p53 stabilisation, in vivo). None is load-bearing.

**Paper-mill-like / formulaic ncRNA: 8 tagged `ncrna=True`** out of 249 — the lowest proportion
of the four (3%). Example: lncRNA PCAT6 "promotes the development of osteosarcoma by increasing
MDM2 expression" (2020). The MDM2 literature is relatively clean of sponge-axis papers,
probably because it is dominated by pharmaceutical-industry chemistry and diagnostic pathology
rather than by low-cost cell-line work.

### 4.3 Biomarker — defined, quantified, and pointing at the wrong patients

**MDM2 has the best-characterised biomarker of all four targets, with a validated clinical FISH
assay and real frequency figures. The problem is where those frequencies land.**

**In low-grade osteosarcoma, MDM2 amplification is near-universal:**
- Parosteal osteosarcoma: **27/29 = 91.3%** by FISH (38433050); **4/5** (9989829); all classic
  and dedifferentiated POS in a 22-case series (30001240).
- Low-grade central osteosarcoma: **8/14 = 57.1%** (38433050); but only **4/21 = 19.0%** in an
  earlier series (15310147) — a genuine discrepancy between series.
- Low-grade osteosarcoma overall: **sensitivity 81.3%, specificity 100%** against 58 mimics
  (38433050); **22/22 = 100%** MDM2-amplified with 95% also FRS2-amplified (30001240).
- MDM2 amplification is rare enough in mimics to be diagnostic: 1/44 craniofacial ossifying
  fibromas (35546651); 0/58 bone-tumour controls (38433050).
- Co-amplification partners are consistent: CDK4 (9989829, 39322633), FRS2 (95%, 30001240),
  GLI1 (**13/15 = 87%**, 40318859).

**In conventional high-grade osteosarcoma — the disease with the unmet need — it is uncommon:**
- **6.6%** of 83 OS by quantitative Southern blot, essentially mutually exclusive with p53
  positivity (26.5%); combined p53/MDM2 pathway alteration 34% (9118036).
- **2/16** classical intramedullary OS had any 12q amplification, and that involved SAS, not
  MDM2, versus 4/5 parosteal cases (9989829).
- **0/30** osteosarcomas showed MDM2 amplification, while TP53 was altered in **15/30 = 50%**
  (10942797).
- **3/23 = 13%** in OS patients over 40 (12181274); **5/37** with only 2-3-fold copy gain
  (8781571).
- **5/49** mandibular high-grade OS, and the abstract's reading is that these were probably
  unrecognised dedifferentiated low-grade tumours (26997440) — a point 30001240 makes
  explicitly: "some so-called 'high-grade osteosarcomas harboring 12q13-15 amplification' may be
  unrecognized dedifferentiated LGOSs."
- Germline modifier: MDM2 SNP309 GG raises OS risk (OR **2.09**, 95% CI 1.15-3.78; in females
  OR **4.26**, 95% CI 1.61-11.25) in 201 patients (19451596) — a risk allele, not a treatment
  biomarker.
- 21159888 (192 bone/soft-tissue sarcomas) found an inverse relationship between MDM2
  amplification and TP53 mutation and recommends exactly the right thing: "MDM2 markers along
  with TP53 sequencing should be considered as patient biomarkers in clinical trials of sarcomas
  using MDM2 antagonists."

**The resulting trap, stated plainly.** A trial of milademetan, brigimadlin, idasanutlin or
navtemadlin in osteosarcoma must select MDM2-amplified *and* TP53-wild-type patients. That
population is concentrated in parosteal and low-grade central osteosarcoma — indolent tumours,
often cured by surgery alone, with good prognosis even in their soft-tissue homologue
(22749040: disease-free at 13 years). In high-grade conventional osteosarcoma, MDM2
amplification runs roughly **6-13%**, TP53 is disrupted in most tumours, and the two events are
mutually exclusive, so the eligible fraction is small and the drug's mechanism fails in exactly
the patients who are dying. The PPTP had to exclude osteosarcoma models for low TP53 expression
(27238606). This is a well-defined biomarker that selects the patients who need the drug least.

### 4.4 Has the clinical-stage drug been tested in OS models?

**Yes — more thoroughly than for any of the other three targets, and the results are
spectacular but almost entirely in one MDM2-amplified cell line.**

- **Idasanutlin (RG7388)**: its direct precursor RG7112 regressed MDM2-amplified osteosarcoma
  xenografts with the panel's best apoptotic response (23400593); RG7388 itself appears as the
  scaffold for 18F PET probes with high specific uptake in SJSA-1 xenografts (41962329).
- **SAR405838** (a clinical-stage MDM2 inhibitor, phase I): complete tumour regression in SJSA-1
  from a single oral dose (25145672), with resistance arising through TP53 mutation (26070072).
- **MK-8242**: active in TP53-wild-type paediatric models but **osteosarcoma models were excluded
  for low TP53 expression** (27238606).
- **AMG 232, HDM201, AM-7209, nutlin-3/3a** and numerous unnamed analogues: activity in
  SJSA-1 and p53-wild-type U2OS, inactivity in p53-null SAOS-2 (22843172, 30715803, and the
  discovery-chemistry tail).
- **Milademetan, brigimadlin and navtemadlin by name: absent from this abstract set.**

So the answer is: MDM2 inhibitors unquestionably work on MDM2-amplified, p53-wild-type
osteosarcoma cells, and unquestionably do not work when p53 is disrupted. The osteosarcoma
result is strong; the osteosarcoma *population* result is the problem.

### 4.5 Verdict — **contradictory: the strongest drug evidence attached to the weakest patient rationale**

MDM2 is directionally uncontested, has a validated clinical FISH biomarker with real frequency
figures, and clinical-stage MDM2 inhibitors produce complete tumour regression in osteosarcoma
xenografts from a single oral dose (25145672, 23400593) — the best preclinical efficacy anywhere
in these four files. But that efficacy is almost entirely one MDM2-amplified, TP53-wild-type
cell line (SJSA-1, 18 appearances), the biomarker-eligible population sits in indolent
parosteal/low-grade osteosarcoma (91.3% amplified, 38433050) rather than in lethal high-grade
disease (6-13%, and mutually exclusive with the TP53 disruption most patients have — 9118036,
10942797, 21159888), the paediatric preclinical panel excluded osteosarcoma models for low TP53
(27238606), and canine osteosarcoma has essentially no MDM2 amplification with near-universal
p53 dysfunction (9891508, 10643981), closing off the comparative model.

**Single most important missing experiment:** prospectively determine, in a modern, adequately
powered high-grade conventional osteosarcoma cohort, the joint frequency of MDM2 amplification
*and* functionally wild-type TP53 — the actual eligible fraction, which no abstract here reports
— and then test one named clinical agent (milademetan or brigimadlin) in patient-derived
orthotopic models drawn from that double-positive group, with a metastasis endpoint and
bone-toxicity monitoring given the pre-osteoclast effect (17592964). If that eligible fraction
is a few percent, the honest conclusion is that this is a basket-trial question, not an
osteosarcoma trial.

---

## 5. Comparison

| Target | Verdict | Biomarker and frequency | Key missing experiment |
|---|---|---|---|
| **DKK1** (DKN-01 / sirexatamab) | **Moderate** — most trial-ready. Three modalities of blockade (antibody BHQ880 27049730, morpholino DkkMo 35277659/39805917, small molecule WAY262611 39781890) all cut metastasis and preserve bone; but one narrow group lineage, no independent replication, and directly contradicted by papers where DKK1 *up*regulation is the anti-tumour mechanism (24859848, 37716273). | **Weakest of the four.** Serum DKK1 "significantly elevated" in paediatric OS, no n or cutoff (17987039); DKK1 up in 67 OS vs adjacent tissue (28682874); prognostic in scRNA-seq of 17 patients (42769034) and in a 5-gene LASSO score (36225939, duplicated in 38622876). **No abstract reports a DKK1-high frequency or a serum threshold.** | DKN-01 itself (not an analogue) in ≥2 patient-derived orthotopic models with a metastasis endpoint, by an independent lab, reporting baseline tumour and serum DKK1 to define a cutoff and the DKK1-high fraction. Add a spontaneous canine OS arm — there is zero dog data. |
| **CCNE1** (BLU-222, INX-315, PF-07104091) | **Weak** — biomarker without a drug rationale. Direction uncontested and the largest patient genomic base of the four, but functional evidence is one in-vitro siRNA (32162720) plus three miRNA xenografts that don't isolate CCNE1; ~16/34 abstracts use cyclin E1 only as a proliferation band; 3 retracted. | **Best-defined in principle, key number missing.** Cyclin E1 protein high in **61%** of 69 tumours by IHC (32162720); CCNE1 one of four oncogene hotspots within SVs affecting **58%** of 236 WGS tumours (42779977); enriched in paediatric/adolescent patients (42424099, 39688743) but contradicted by 33969640. **No abstract reports CCNE1 *amplification* frequency in OS.** Complicated by subclonality in resistant clones (37812025) and by the LMW-cyclin E1 cleavage isoform (40959067). | A clinical CDK2 inhibitor across CCNE1-amplified vs non-amplified OS PDX panels to show amplification-dependent response — this has **never been done** — reported alongside CCNE1 amplification frequency by FISH/NGS in a defined OS cohort. |
| **PTK2 / FAK** (defactinib, approved 2025) | **Moderate** — most immediately actionable. Clinical-stage analogue PF562271 reduced xenograft volume, weight and angiogenesis orally (28406574); drug is approved and available. But only ~12 of 105 abstracts manipulate FAK itself, and credible papers report FAK dispensable (16759849, 20814573), not overexpressed (12376862), non-prognostic as total protein (28846700) or protective (15485819, 35008585). | **Most usable today, though IHC-based not genomic.** Total FAK overexpressed in **90.6%** (48/53) and pFAK-Y397 in **62.3%** (33/53), with only pFAK-Y397 prognostic (28846700); FAK/pFAK profile an independent predictor in 113 patients (26393679); a **beta5-integrin + FAK + GSK3beta** panel separates good from poor chemotherapy responders at **AUC 89.9% / accuracy 90.3%** in 36 pre-treatment biopsies (23845472). No PTK2 amplification frequency reported. | Defactinib itself in orthotopic/PDX models with a **lung-metastasis** endpoint (not just subcutaneous volume), stratified by baseline pFAK-Y397, alone and with a MEK inhibitor to mirror the approved avutometinib regimen. Canine arm absent. |
| **MDM2** (milademetan, brigimadlin, idasanutlin, navtemadlin) | **Contradictory** — best drug evidence, worst patient rationale. Single oral dose of SAR405838 gave complete regression (25145672) and RG7112's best panel response was MDM2-amplified OS (23400593), but almost all of it is one cell line (SJSA-1, 18 appearances); the paediatric preclinical panel **excluded** OS models for low TP53 (27238606). | **Best-quantified and pointing at the wrong patients.** MDM2 amplification in **91.3%** (27/29) of parosteal OS and 8/14 LGCOS, with **81.3% sensitivity / 100% specificity** for low-grade OS (38433050); 22/22 LGOS (30001240). But only **6.6%** of 83 conventional OS (9118036), **0/30** (10942797), **13%** over age 40 (12181274), 2/16 intramedullary (9989829) — and mutually exclusive with the TP53 mutation most patients carry (9118036, 21159888). Canine OS: no significant amplification in 21 tumours (9891508). | Prospectively measure the **joint** frequency of MDM2 amplification *and* functionally wild-type TP53 in a modern high-grade conventional OS cohort — the true eligible fraction, reported nowhere here — then test milademetan or brigimadlin in PDX models from that double-positive group with a metastasis endpoint and bone-toxicity monitoring (17592964). |

### Cross-cutting observations

- **Nobody has tested the actual named clinical drug in osteosarcoma for any of the four.**
  DKN-01, BLU-222/INX-315/PF-07104091, defactinib, milademetan/brigimadlin/navtemadlin are all
  absent from these abstracts. Only close analogues (BHQ880, PF562271, RG7112/SAR405838) appear.
  For CCNE1 there is not even an analogue.
- **The two NIH-funded targets (DKK1, FAK) are also the two with usable in vivo blockade data
  and the two with no canine data.** Given that one grant is at a veterinary school and canine
  OS is the standard comparative model, a dog study is the cheapest high-value experiment
  available for either.
- **Metastasis endpoints are rare.** DKK1 is the only target where blockade has been tested
  against metastatic outgrowth specifically (27049730, 39781890, 39805917). FAK has it only as
  a mechanistic arm (37013056, 42520958); CCNE1 and MDM2 have none.
- **Biomarker quality runs inversely to drug-rationale quality.** MDM2 and CCNE1 have crisp
  binary genomic biomarkers and little or no target-specific functional evidence in OS; DKK1 has
  the functional evidence and no quantified biomarker. FAK is the only target with both a
  usable patient-selection assay (23845472, 28846700) and positive in vivo pharmacology
  (28406574) — which is the main reason it reads as the most actionable despite its messy
  mechanism literature.
- **Retraction and paper-mill load by target:** DKK1 2/36 retracted and ~11% formulaic ncRNA;
  CCNE1 3/34 retracted and ~12% ncRNA, plus roughly half the set using cyclin E1 only as a
  western-blot band; PTK2 1/105 retracted and ~7% ncRNA, but a large low-value natural-product
  layer (~15 abstracts) and several near-duplicate chemokine/miRNA papers from one template;
  MDM2 3/249 retracted and ~3% ncRNA, the cleanest, though heavily weighted to industry
  chemistry and diagnostic pathology rather than osteosarcoma therapeutics.
- **Where these abstracts are insufficient:** abstracts almost never give animal numbers, effect
  sizes, the number of independent cell lines, or assay cutoffs. Specifically unavailable here:
  CCNE1 amplification frequency in OS; any DKK1-high frequency or serum cutoff; the joint
  MDM2-amplified/TP53-wild-type fraction in high-grade OS; PTK2 genomic alteration frequency;
  and, for every target, whether the in vivo work used orthotopic or subcutaneous models in
  cases where the abstract does not say. These gaps should be closed from full texts before any
  of this is used for trial design.
