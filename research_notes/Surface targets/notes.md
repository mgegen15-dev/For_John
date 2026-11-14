# Surface targets for osteosarcoma — working notes

Built November 14, 2026. Script: `tools/surface_targets.py` (re-runnable, stages cache to
`data/surface_targets_raw/`, which is git-ignored). Output table:
`data/osteosarcoma_surface_target_candidates.csv`. Report:
`reports/New surface targets for osteosarcoma.md`.

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
