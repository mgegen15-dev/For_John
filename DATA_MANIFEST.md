# Data manifest

*Generated 2026-11-20 by `tools/build_manifest.py`. Re-run it on your copy and compare the SHA-256 checksums to confirm you have the same files.*

Files in git are the analysed outputs. The large raw downloads are not stored in git; their checksums are listed so a re-download can be compared. Live databases change, so a fresh download will usually differ slightly: the retrieval dates below say when each was taken.

## Files in the repository

| File | Rows | Size (KB) | First added | SHA-256 |
|---|---|---|---|---|
| `data/drug_targets_curated.json` |  | 3 | 2026-11-14 | `a890fa40cf5f84c309d3b0bf79018d3df42afb66fa75a49486a36dddc783acfd` |
| `data/lung_metastasis_mechanisms.csv` | 56 | 13 | 2026-11-14 | `a234feab8116566d80b4af0fa833a5f5aad397d604e647414cb060f87c13f71e` |
| `data/lung_metastasis_papers.csv` | 9130 | 1492 | 2026-11-14 | `7e1a998890c14dfd9be756607a2e5be0cdd420366f8011a0c5796fe216002bd8` |
| `data/lung_metastasis_trials.csv` | 224 | 160 | 2026-11-14 | `159cc88ffd2bf7e58a05414efde3da56eda17975d08937c1d9044a33549520b9` |
| `data/nih_neuroblastoma_projects.csv` | 2919 | 684 | 2026-11-14 | `fa477a2d793ae682cd36f876b1ae06b1444359dc1dcad5efebb8b0ef037f1a98` |
| `data/nih_osteosarcoma_projects.csv` | 2697 | 642 | 2026-11-14 | `d2d6f5dbcc4cca47a949e2a0be44be61a625bb3f9e32ecd607f5e8446c5f2b6f` |
| `data/osteosarcoma_copy_number_frequencies.csv` | 71 | 9 | 2026-11-19 | `72b9a5c1cced2e5d26fd5b15abd97a460507ee89419c23826a7399a93cfe4473` |
| `data/osteosarcoma_evidence_risk_genes.csv` | 362 | 15 | 2026-11-14 | `4dfb669ff8e0c2ca1af709eeee70bd1455e16d62b63df53a8cfad30bba94cfa9` |
| `data/osteosarcoma_evidence_risk_journals.csv` | 130 | 3 | 2026-11-14 | `f6464e695923d68931eb08a761074ee1901c6254cfb09e4957c527e0a7fac581` |
| `data/osteosarcoma_gene_evidence.csv` | 1487 | 63 | 2026-11-14 | `63a9a165cb0ae0634b23493fd242fb3db10abb920c134e5f44ff8aa8dec91fcf` |
| `data/osteosarcoma_literature_periods.csv` | 8 | 0 | 2026-11-14 | `c44be9dfe3aff62bc95f4a3838170cba750fb9fae7c09efc2bf1a9d6f01fc072` |
| `data/osteosarcoma_paper_tags.csv` | 33242 | 2101 | 2026-11-14 | `8df6752a5da98ced48a2985d683a484512a8fa0d68721739eee9d3962f39312f` |
| `data/osteosarcoma_posted_outcomes.csv` | 5254 | 1958 | 2026-11-14 | `4808a2bf4bb5ca018a63fe0c362c25c77853c0736c25b87bccd8ef3b3ac0ee32` |
| `data/osteosarcoma_relapse_benchmarks.csv` | 19 | 3 | 2026-11-14 | `30b8ce1e6c3a1606aaa755bf59ac18593d04a106a3f60cffbc03436506e836a6` |
| `data/osteosarcoma_relapse_benchmarks_basket.csv` | 33 | 10 | 2026-11-14 | `9240951c6824e6a0a6b7b2882b9387239b04830255ebf7ee236b0a5d94b9dfcc` |
| `data/osteosarcoma_relapse_benchmarks_published.csv` | 60 | 13 | 2026-11-14 | `07e2a99516d7b0df60466bea950f8479bb6c9c27068c3b77b77f0b9c3c0d0dd8` |
| `data/osteosarcoma_repurposing_candidates.csv` | 1141 | 375 | 2026-11-19 | `64d7d945c5ffe051c5f7052c1eba594f7b3d77713c21ee1b4741c3ddda57659c` |
| `data/osteosarcoma_surface_target_candidates.csv` | 2434 | 781 | 2026-11-14 | `e520ce548bbab89695caab028200f10586fefa2e1fc82494563b21957c57f6b6` |
| `data/osteosarcoma_trials.csv` | 758 | 489 | 2026-11-14 | `9211e126d7639ce788846226754b1efe2083dd68a28f155b5358297c2b2790ff` |
| `data/osteosarcoma_trials_flags.csv` | 168 | 34 | 2026-11-14 | `d3c5fb8cf09d19e7b4a2061a74dd0522e41563cc0eff3ce59cef4c2b4bebf90b` |
| `data/osteosarcoma_trials_publications.csv` | 387 | 88 | 2026-11-14 | `12890fc385cb3b8f682a81df1d465bc70a45450bbb4776c8b682625a3a539205` |
| `data/raw_checksums.txt` | 325 | 43 | not in git | `3ff56672730aa0c663e021bcac0b9ae24207017e8501999cfd8debf59a8ee3cd` |
| `data/literature/osteosarcoma_retracted_pmids.txt` | 418 | 3 | 2026-11-14 | `62bddf36921d30de8c1be3c69fd14ef10352a2819a17cc4026ef057c260ee2ec` |
| `data/literature/osteosarcoma_reviews_pmids.txt` | 3533 | 30 | 2026-11-14 | `155b2b30719c789a8718476cccc456c6cf94b4a382feaa6511c54a149595adaf` |

## Raw downloads kept out of git

| Location | Source | Files | Size (MB) | Combined SHA-256 of file checksums |
|---|---|---|---|---|
| `data/literature/osteosarcoma_pubtator.jsonl` | PubMed + PubTator3, via tools/literature_fetch.py; retrieved 2026-11-14 | 1 | 65 | `ac01e96998d3eccb1e79aeb25708a66667e9a6f13f1f2c26c3e56e6f3b1d0089` |
| `data/copy_number_raw` | NCI GDC, TARGET-OS open copy-number files, via tools/copy_number_map.py; retrieved 2026-11-19 | 197 | 287 | `6aede47fd6a452cb23ce361a4c656dd2b97e045edd013a1430ad4ae5164d09f7` |
| `data/surface_targets_raw` | NCI GDC TARGET-OS RNA-seq, GTEx v8, Human Protein Atlas, via tools/surface_targets.py; retrieved 2026-11-14 | 100 | 389 | `65b740105d96fa3adf8fcdb6cd227fe3234b131aaf10d61c49020ca16ec51981` |
| `data/repurposing_raw` | ChEMBL, ClinicalTrials.gov and PubMed caches, via tools/repurposing_screen.py; retrieved 2026-11-19 | 27 | 22 | `eb0e4b8011ee179877fabb0697564a3d04a638ae046aa0ce1178e8bcee542101` |

**Other retrieval dates:** ClinicalTrials.gov trial list 2026-11-14 (individual records re-checked through 2026-11-20); NIH RePORTER 2026-11-14; NCBI SRA dog genome metadata 2026-11-14; Europe PMC publication checks 2026-11-14.

Per-file checksums for the raw downloads are in `data/raw_checksums.txt`.
