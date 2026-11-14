# Surface targets for osteosarcoma — working notes

Built November 14, 2026. Script: `tools/surface_targets.py` (re-runnable, stages cache to
`data/surface_targets_raw/`, which is git-ignored). Output table:
`data/osteosarcoma_surface_target_candidates.csv`. Report:
`reports/New surface targets for osteosarcoma.md`.

*Note added November 14, 2026: some trial statements below are out of date (LRRC15 and PTK7 trial
statuses, MORAb-004 results, MRC2 drug programmes). The report and its change log hold the
checked versions.*

## The question

Osteosarcoma has had no new standard-of-care drug since the 1980s. The current wave of
targeted attempts is almost entirely antibody-drug conjugates (ADCs), bispecifics and CAR-T
cells, and nearly all of them point at the same short list of antigens: B7-H3 (CD276), GD2,
HER2 (ERBB2), GPNMB, EGFR, IL11RA, EPHA2, ALPL. If that list is short because it is
genuinely the whole opportunity, fine. If it is short because nobody has looked
systematically with open data, that is a cheap gap to close.

So: which cell-surface proteins are expressed high and consistently in osteosarcoma tumours
but low in the normal tissues you cannot afford to damage?

## Data sources used

| Source | What was taken | How |
|---|---|---|
| NCI GDC, project TARGET-OS | 88 open-access RNA-seq samples, STAR "augmented gene counts" files, `tpm_unstranded` column, protein-coding genes only | `files` endpoint with `data_type="Gene Expression Quantification"`, `access="open"`; bulk download via POST `/data` in chunks of 20 |
| Human Protein Atlas | surface annotation: `protein_class:Predicted membrane proteins` (5,573 genes) and `subcell_location:Plasma membrane` (2,305 genes); per-gene JSON for protein-level evidence and IHC reliability on the leaders | `api/search_download.php`, then `/{ENSG}.json` |
| GTEx v8 | median TPM in each of 54 normal adult tissues | API v2 `/reference/gene` (symbol to versioned GENCODE v26 ID) then `/expression/medianGeneExpression?datasetId=gtex_v8` |
| ClinicalTrials.gov API v2 | existing antibody / ADC / bispecific / CAR programmes naming each leading target, in any cancer | `/studies` with `query.term`, then a modality regex over title and intervention names |
| This repo | osteosarcoma literature depth and paper-mill risk per gene | `data/osteosarcoma_gene_evidence.csv`, `data/osteosarcoma_evidence_risk_genes.csv` |

### What failed, and was not done

- **GTEx bulk median-TPM GCT file**: both the v8 and v10 public URLs on
  `storage.googleapis.com` returned 403/404 from this environment, so normal-tissue medians
  were pulled gene-by-gene through the API instead. Same numbers, just slower.
- **GTEx v10**: the API's default dataset is `gtex_v10`, but `/reference/gene` only returns
  GENCODE v26 IDs, which v10 does not accept. Everything here is therefore **GTEx v8**
  (54 tissues). This is the version almost all published target-screening work uses.
- **DepMap** (step 6, optional): `depmap.org` answers every API path with an HTML
  bot-verification challenge rather than data, and the Sanger Cell Model Passports API is
  blocked by this environment's proxy (403 on CONNECT). **No cell-line expression check was
  done.** This is the one planned step that is missing; it would be worth redoing by hand,
  because an ADC or CAR candidate that no osteosarcoma cell line expresses is hard to work on
  preclinically.
- **GEO**: not needed; TARGET-OS gave all 88 open samples the plan asked for.

## Method

1. **Tumour side.** For each protein-coding gene: median TPM across the 88 tumours, the
   quartiles, and the share of tumours with TPM >= 5 (the "% expressing" column). A gene had
   to reach median TPM >= 10 to be considered at all.
2. **Surface filter.** Keep genes in the HPA membrane proteome. The strict tier used for the
   headline ranking, `surface_strong`, requires a gene to be **both** a predicted membrane
   protein **and** experimentally localised to the plasma membrane by HPA
   immunofluorescence — 952 genes. The looser union (6,926 genes) is kept in the table so a
   reader can relax the filter.
3. **Normal side.** GTEx v8 median TPM per tissue. The denominator for the window is the
   **highest median among the "vital" tissues** — the 32 tissue entries where on-target
   damage would most likely be dose-limiting or fatal: heart (2), lung, liver, kidney (2),
   brain (12), tibial nerve, colon/small intestine (3), artery (3), whole blood, oesophageal
   mucosa, stomach, pancreas, adrenal, skeletal muscle. The worst tissue across all 54 is
   also recorded, so non-vital but relevant tissues (skin, testis, thyroid) are visible.
4. **Score.** `window_score = log2((tumour_median + 1) / (max_vital_normal + 1)) x
   (% tumours expressing / 100)`. The log ratio is the therapeutic window; the multiplier
   penalises a gene that is spectacular in a third of tumours and absent in the rest, which
   is useless for a single-antigen agent. The +1 TPM pseudocount stops near-zero normals
   from producing meaningless infinite ratios.
5. **Controls.** The eight antigens already in osteosarcoma trials, plus LRRC15, MMP14 and
   CDH11, are scored alongside and flagged in the table, but excluded from the "novel" rank.
   Where they land is the only check available on whether the score means anything.

## What came out

Counts at each step:

- 88 open TARGET-OS expression files, all `Primary Tumor`, 19,962 protein-coding genes present
  in all 88 (genes absent from any sample were dropped rather than imputed).
- HPA surface universe 6,926 genes: 1,053 high confidence, 119 medium, 5,754 low.
- 2,499 surface genes cleared median TPM >= 10; GTEx v8 medians were retrieved for 2,434 of them
  (the misses are symbols GTEx's gene endpoint does not resolve to a v26 GENCODE ID).
- 376 novel surface-supported candidates; 258 after dropping HPA housekeeping proteins.

Control ranks out of 2,434 (the validation): LRRC15 **1**, MMP14 **7**, CD276 **15**,
CDH11 **21**, ALPL **70**, then GPNMB 617, EPHA2 1,263, EGFR 1,554, IL11RA 1,998,
B4GALNT1 2,062, ERBB2 2,178.

Shortlist top 10: LRRC15, IFITM5, ADAM12, MRC2, PTK7, ULBP2, CD109, EPHB2, CD248, CD84.

## Things found along the way that matter more than the ranking

**LRRC15 is already in sarcoma trials.** Three programmes name it; SOT106 (NCT07801222) lists
osteosarcoma as a keyword and ZL-6201 (NCT07374848) is a phase 1a/b in sarcoma, recruiting.
Both opened recently. The repo's literature table has only 6 LRRC15 osteosarcoma papers, so
this is a case where industry is ahead of the published academic literature.

**PTK7 has four ADCs in phase 1** (HWK-007, KIVU-107, DAY301, PF-06647020), one of which
already lists sarcoma, and fewer than five osteosarcoma papers. Cheapest possible experiment
in the whole list.

**CD248 antibody already went into children**: MORAb-004 / ontuxizumab, NCT01748721, paediatric
recurrent/refractory solid tumours, completed. Connects directly to this repo's work on trials
whose results were never published — worth adding to that list if it is not there.

**HER2 ranks 2,178 of 2,434.** 15 TPM in tumours against 130 TPM in heart. This is a
quantitative statement of something the clinical record already hints at, and it is the most
provocative single number in the analysis.

## Decisions made, and why

- **Why "worst vital tissue" rather than mean or median normal.** Toxicity is set by the most
  exposed organ, not the average one. A gene at 500 TPM in heart and 0 elsewhere is not a target
  however good its average looks.
- **Why multiply by % expressing.** A single-antigen agent needs the antigen present in
  essentially every tumour cell of essentially every patient. EGFR (68% of tumours) and IL11RA
  (59%) are penalised for this and should be.
- **Why a +1 TPM pseudocount.** Without it, any gene with a normal median of 0.0 gets an
  infinite window and the top of the list fills with noise.
- **Why the housekeeping filter is a separate column, not a filter.** It drops NDC1 (nuclear
  pore), LAPTM4A (Golgi), CYP20A1 (a cytochrome P450), TMEM50A, CD320, NUS1 and TMEM65, which
  are clearly not ADC targets. But it is a judgement call applied to an HPA label, so it is
  reversible: `rank_novel_surface` keeps them, `rank_shortlist` does not.
- **Why the surface tier is loose (high + medium).** Restricting to "high" drops LRRC15, which
  has clinical-stage ADCs. HPA's immunofluorescence has real false negatives; CD276 is only
  rescued into "high" because it is a curated CD marker, and MMP14 and CDH11 are not rescued at
  all. The tier is an annotation statement, not biology, so it is reported rather than enforced.
- **Why GTEx's cultured fibroblasts got their own column.** For a mesenchymal tumour it is the
  most informative single comparator in GTEx. It separates LRRC15 (3 TPM) and IFITM5 (0 TPM),
  which look tumour-restricted, from CD248 (578 TPM), MRC2 (259) and CD109 (118), which look
  like mesenchymal lineage markers. It is a cell line, not a tissue, so it is excluded from the
  "worst normal tissue" column.

## Open ends

1. **DepMap was never checked** — see the failures section. Highest-value missing piece.
2. **No normal bone anywhere in the normal-tissue reference.** This is a limitation of GTEx, not
   of the script. Candidate sources to try: HPA's own bone-marrow and bone data, or a published
   osteoblast RNA-seq series from GEO.
3. **Immune-infiltrate confound is flagged but not resolved.** CD84, CSF1R and ITGA4 are
   probably macrophage/leukocyte signal. Single-cell osteosarcoma data (there are published
   datasets) would settle it.
4. **No relapse or metastasis samples.** TARGET-OS open data is primary tumour only.
5. **Soluble/shed ectodomains not assessed** for ADAM12, CD248, ULBP2 — all three are known to
   shed, which can neutralise an antibody.
6. The score's weights were not tuned or cross-validated against the controls; doing so would be
   circular with n=11 controls, but a sensitivity analysis over the thresholds would be fair.
