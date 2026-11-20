# Dog genome re-analysis: what's available and what it would take

*Lead 12 of `reports/Ranked leads and research partners.md`. Scoped on November 14, 2026 from NCBI's Sequence Read Archive (SRA) and BioProject databases through E-utilities. No genomes have been analysed yet.*

## Summary

Far more open genome data from pet dogs with osteosarcoma exists than the project first assumed (24 genomes). By our count, about **91 dogs have deep whole-genome sequencing of both tumour and normal tissue** in the SRA, and about 230 more dogs (about 227 by the table below) have shallow tumour-only genomes, mostly from trials. The most valuable set is new: deep tumour–normal genomes from 55 dogs enrolled in the **NCI Comparative Oncology Trials Consortium studies COTC021 and COTC022**, a randomized trial with recorded outcomes, so their genomes could in principle be linked to how long each dog lived. That turns the lead from "is the genome-shattering pattern recently described in human osteosarcoma present in dogs?" into a better question: **does it predict outcome in dogs, as genome-wide loss of heterozygosity does in people?** If it does, dogs become a validated model for testing drugs aimed at that biology.

**How to read the labels.** **(registry)** means taken directly from a public database record, here NCBI SRA or BioProject; **(our calculation)** means we derived it from those records, for example by counting distinct dogs from sample names; **(paper, full text)**, **(paper, abstract only)** and **(press release only)** mark figures from publications.

## What the SRA holds

A search for dog (*Canis lupus familiaris*) records mentioning osteosarcoma with whole-genome sequencing as the strategy returns **743 sequencing experiments (747 runs, 39.4 trillion bases)** across ten projects (registry). These are runs, not dogs, and they mix very different kinds of data:

| Kind of data | Runs | Dogs (approx.) | Data volume | Use |
|---|---|---|---|---|
| Deep tumour + matched normal WGS | 220 | ~91 | ~33.7 Tbases | Structural variants, chromothripsis, LOH |
| Shallow tumour-only WGS (~2–7x) | 227 | ~227 | ~3.4 Tbases | Copy number only |
| Ultra-low-pass plasma cell-free DNA and blood | 289 | not counted | 0.3 Tbases | Liquid biopsy |
| Cell lines | 11 | n/a | ~2.0 Tbases | Laboratory models |

*Runs and bases are registry figures; dog counts and the split into kinds are our calculation from sample and library names. The deep row includes 24 lower-depth tumour replicate runs from PRJNA525883. Rows add to 747 runs.*

### Project by project

| Project | WGS runs | Data volume | What it is |
|---|---|---|---|
| PRJNA1374203 | 110 | 17.5 Tbases | **55 tumour–normal pairs** from COTC021/022 trial dogs, sampled at amputation; about 66x per run; registered December 2025 |
| PRJNA525883 | 90 | 11.5 Tbases | Tumour–normal WGS (and exome and RNA data) from a 2019 cohort, probably Gardner et al., *Commun Biol* 2019 (NCBI does not link the paper). **24 dogs** have deep tumour and normal genomes plus a lower-depth tumour replicate; 18 further runs are shallow tumour-only |
| PRJNA1367604 | 209 | 3.4 Tbases | **Tumour-only** WGS from 209 dogs in COTC021, 022, 026 and 030, about 16 Gbases per run (roughly 6–7x). Good for copy number, weak for structural-variant calling without normals. None of these dogs is in PRJNA1374203 |
| PRJNA1154710 | 16 | 3.5 Tbases | Tumour–normal pairs from **8 dogs with mandibular (jaw) osteosarcoma** |
| PRJNA247491 | 16 runs (12 experiments) | 0.74 Tbases | Osteosarcoma subset of a multi-cancer canine pilot: tumour and normal from 2 dogs |
| PRJNA680382 | 6 | 0.6 Tbases | Primary tumour, lung metastasis and normal from **2 dogs** (project also has exome and RNA-seq) |
| PRJNA777126 | 8 | 1.2 Tbases | Canine osteosarcoma cell lines |
| PRJNA1469753 | 3 | 0.8 Tbases | Cell lines, from a 2026 palbociclib study |
| PRJNA1151136, PRJNA1373368 | 177 + 112 | 0.3 Tbases | Ultra-low-pass plasma cell-free DNA and blood (osteosarcoma-tagged subset; the projects hold 770 runs in all, mostly other cancers and healthy dogs) |

*Run counts and volumes: registry. Dog counts and coverage estimates: our calculation.*

**Deep tumour–normal dogs, by our count:** 55 (PRJNA1374203) + 24 (PRJNA525883) + 8 (PRJNA1154710) + 2 (PRJNA680382) + 2 (PRJNA247491) = **about 91 dogs** (our calculation). That is several times the 24 genomes first assumed. The liquid-biopsy projects are a separate opportunity, for a canine version of ctDNA monitoring (lead 8 of the ranked leads).

**The trial link.** COTC021/022 randomized 324 dogs to carboplatin with or without sirolimus after amputation and found no difference in disease-free interval or survival (PMID 33753454, paper, abstract only). Because outcomes were recorded for every dog, the 55 deep genomes and the 209 shallow ones from COTC trials can, in principle, be tested against survival.

**The human comparison.** In human osteosarcoma, a 2025 *Cell* paper (Espejo Valle-Inclan et al., PMID 39814020, paper, abstract only) described a recurring pattern of chromosome shattering combined with loss and amplification (loss–translocation–amplification, LTA, chromothripsis) in about half of high-grade tumours, and found genome-wide loss of heterozygosity to be a strong prognostic indicator in a cohort of children and adults.

## Why it can't be done in this workspace

The deep tumour–normal genomes total about 33 trillion bases, many terabytes of raw reads, against about 30 GB of free disk here. The analysis has to run in the cloud, where the SRA keeps copies that can be read without downloading.

## What it would take

1. **Compute:** align each genome to the dog reference (CanFam4), call structural variants and copy number, then look for the chromothripsis and LTA patterns described in human osteosarcoma. Standard open-source tools exist for every step. The shallow tumour-only genomes can add copy-number calls for many more trial dogs.
2. **Rough cost:** a few dollars to low tens of dollars per genome on cloud spot instances, so **roughly $1,000–5,000** for about 180 deep genomes (our estimate, to be confirmed with a bioinformatician).
3. **Outcome data:** the dogs' treatment and survival data from COTC021/022 sit with the NCI Comparative Oncology Program and its Integrated Canine Data Commons, and may need a data request.
4. **People:** a bioinformatician who knows structural-variant calling, and a collaborating group, for example the NCI Comparative Oncology Program or the team behind the 2025 *Cell* paper, to check the results.

## Recommended next step

Contact the NCI Comparative Oncology Program, which also appears in the pet-dog trial brief. Ask whether a chromothripsis analysis of the COTC021/022 genomes is already planned, and whether linked outcome data can be shared. If it isn't planned, this is a well-defined, fundable project of a few thousand dollars in compute.

## Change log

- **November 13–14, 2026:** first version.
- **November 14, 2026, after an independent audit, with a fresh NCBI E-utilities query:**
  - The headline "743 whole-genome sequencing runs ... instead of 24 genomes" compared runs with dogs. It now separates deep tumour–normal, shallow tumour-only, cell-free DNA and cell-line data, and counts dogs: about 91 dogs have deep tumour–normal genomes.
  - The 743 figure is SRA experiments (747 runs). Three runs from a 2026 cell-line project (PRJNA1469753) were missing from the table and are now listed.
  - PRJNA1154710 is mandibular (jaw) osteosarcoma, not "spine and skull".
  - PRJNA247491 is 16 runs and 0.74 Tbases from 2 dogs, not 12 runs and 0.6 Tbases.
  - PRJNA1367604 is tumour-only at about 6–7x; the earlier note that run counts "include both tumour and matched normal samples" held only for some projects.
  - The deep tumour–normal data volume is about 33 Tbases, not "almost 40" (39.4 is all runs).
  - Lead numbers updated: dog genomes are lead 11 (was 7) and ctDNA is lead 7 (was 6, then briefly 8).
  - The loss-of-heterozygosity claim now cites its source (PMID 39814020) and says it was a paediatric and adult cohort.
- **November 20, 2026.** Lead numbers updated after the ranked leads were re-ranked (lead 5 split into LRRC15 and PTK7): dog genomes are now lead 12 (was 11) and ctDNA is lead 8 (was 7). The ctDNA reference in the liquid-biopsy paragraph had said lead 8 while ctDNA was lead 7; under the new numbering it is correct. Summary counts now match the table: about 91 deep tumour–normal dogs and about 230 (table: ~227) shallow tumour-only dogs.
