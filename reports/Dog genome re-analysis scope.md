# Dog genome re-analysis: what's available and what it would take

*Lead 7 of the ranked leads. Scoped on November 14, 2026 from NCBI's Sequence Read Archive (SRA). No genomes have been analysed yet.*

## Summary

The open dog data is much larger than the research report assumed. Instead of 24 genomes, the SRA holds **743 whole-genome sequencing runs** from canine osteosarcoma projects. The most valuable set is new in 2025–2026: whole genomes from dogs enrolled in the **NCI Comparative Oncology Trials Consortium studies COTC021 and COTC022**. Those dogs were treated in a randomized trial with recorded outcomes, so their genomes can be linked to how long each dog lived.

That turns the lead from "is the 2025 genome-shattering pattern present in dogs?" into a better question: **does it predict outcome in dogs, as loss of heterozygosity does in children?** If it does, dogs become a validated model for testing drugs aimed at that biology.

## Open canine osteosarcoma whole-genome data in the SRA

| Project | WGS runs | Data volume | Description |
|---|---|---|---|
| PRJNA1374203 | 110 | 17.5 Tbases | Osteosarcoma samples from COTC021/022 clinical trials |
| PRJNA1367604 | 209 | 3.4 Tbases | Osteosarcoma samples from COTC021/022/026/030 |
| PRJNA525883 | 90 | 11.5 Tbases | Canine osteosarcoma (the 2019 Gardner et al. cohort) |
| PRJNA1154710 | 16 | 3.5 Tbases | Axial (spine and skull) osteosarcoma |
| PRJNA777126 | 8 | 1.2 Tbases | Canine osteosarcoma cell lines |
| PRJNA680382 | 6 | 0.6 Tbases | Primary and metastatic samples |
| PRJNA247491 | 12 | 0.6 Tbases | Canine tumour sequencing pilot |
| PRJNA1151136, PRJNA1373368 | 289 | 0.3 Tbases | Low-coverage blood and cell-free DNA (liquid biopsy) |

*Counts from NCBI E-utilities. Run counts include both tumour and matched normal samples. The two low-coverage liquid-biopsy projects are a separate opportunity, for a canine version of ctDNA monitoring (lead 6).*

## Why it can't be done in this workspace

The tumour–normal genomes total almost 40 trillion bases, many terabytes of raw reads, against about 30 GB of free space here. The analysis has to run in the cloud, where the SRA keeps copies that can be read without downloading.

## What it would take

1. **Compute:** align each genome to the dog reference (CanFam4), call structural variants and copy number, then look for the chromothripsis and loss-translocation-amplification (LTA) patterns described in human osteosarcoma (Espejo Valle-Inclan et al., Cell 2025). Standard open-source tools exist for every step.
2. **Rough cost:** a few dollars to low tens of dollars per genome on cloud spot instances, so **roughly $1,000–5,000** for the trial cohorts. This is an estimate to confirm with a bioinformatician.
3. **Outcome data:** the dogs' treatment and survival data from COTC021/022 sit with the NCI Comparative Oncology Program and its Integrated Canine Data Commons, and may need a data request.
4. **People:** a bioinformatician who knows structural-variant calling, and a collaborator from the Comparative Oncology Program or the 2025 Cell paper's team to check the results.

## Recommended next step

Contact the NCI Comparative Oncology Program, which also appears in the pet-dog trial brief. Ask whether a chromothripsis analysis of the COTC021/022 genomes is already planned, and whether linked outcome data can be shared. If it isn't planned, this is a well-defined, fundable project of a few thousand dollars in compute.
