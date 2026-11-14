# NIH funding for osteosarcoma, 2015–2025

*Built from the NIH RePORTER API on November 14, 2026 with `tools/nih_funding_tracker.py`. Every grant is listed in `data/nih_osteosarcoma_projects.csv` and, for comparison, `data/nih_neuroblastoma_projects.csv`. Re-run the script to refresh it.*

## Summary

NIH spent **about $18.0 million in fiscal 2025 on grants that name osteosarcoma in their title**, across 30 projects. That is four times the 2015 level ($4.5 million, 12 projects), but it is still small: roughly a quarter of one percent of the National Cancer Institute's budget of about $7.2 billion. Neuroblastoma, a childhood cancer with a similar number of US cases a year, received **$30.8 million across 51 focused projects** in the same year, and about twice as much as osteosarcoma over the whole decade ($228 million against $108 million).

Two features stand out. A third of the decade's osteosarcoma-focused money ($36.6 million) went to NCI's own in-house labs, and one of those projects, a long-running genome study, accounts for $20.4 million on its own. And the topics this project's research report flagged as the biggest gaps get the least money: ctDNA and liquid biopsy received $3.3 million over eleven years, and clinical-trial and outcomes research $4.7 million.

## How grants were counted

A plain text search overcounts badly, because U2OS, an osteosarcoma cell line, is used throughout general cell biology. Each grant is therefore sorted into a tier:

| Tier | Rule | FY2025 |
|---|---|---|
| **Focused** | "Osteosarcoma" or "osteogenic sarcoma" in the project title | 30 projects, $18.0M |
| **Substantial** | Named 3 or more times in the abstract or public-health statement | 9 projects, $10.9M |
| Incidental | Named once or twice only | 208 projects, $116.1M (mostly unrelated work; not counted below) |

Multi-project grants are not double counted: where a subproject matches, only that subproject's amount is counted.

## Osteosarcoma against neuroblastoma, by year

| Fiscal year | Osteosarcoma focused | Osteosarcoma focused + substantial | Neuroblastoma focused |
|---|---|---|---|
| 2015 | $4.5M (12) | $8.1M | $10.0M (31) |
| 2016 | $5.0M (16) | $8.5M | $12.1M (32) |
| 2017 | $7.9M (20) | $11.3M | $15.1M (33) |
| 2018 | $6.1M (19) | $9.4M | $17.5M (42) |
| 2019 | $6.4M (16) | $10.3M | $15.9M (39) |
| 2020 | $7.9M (20) | $13.9M | $23.5M (41) |
| 2021 | $11.3M (27) | $20.7M | $24.7M (48) |
| 2022 | $12.7M (27) | $20.6M | $27.0M (49) |
| 2023 | $13.9M (28) | $25.6M | $22.7M (51) |
| 2024 | $14.5M (29) | $25.9M | $28.6M (55) |
| 2025 | $18.0M (30) | $28.9M | $30.8M (51) |
| **2015–2025** | **$108.2M** | **$183.2M** | **$227.9M** |

Numbers in brackets are projects funded that year.

## Where the osteosarcoma money goes

**By funder:** NCI provided $101.3M of the $108.2M focused total (94%). The rest came in small amounts from NIGMS, the NIH Director's office, NIBIB, NICHD and NCATS.

**By grant type:** standard investigator grants (R01) $37.2M; NCI in-house research $36.6M; cooperative agreements (U01) $10.8M; exploratory grants (R21) $4.7M; small-business grants (R44) $4.1M. Career-development and training awards (K and F grants) together are under $4M, which means few new osteosarcoma scientists are being trained on NIH money.

**By topic**, classified from grant titles (focused and substantial tiers, 2015–2025; one grant can fall in several topics):

| Topic | Project-years | Funding |
|---|---|---|
| Genomics and epigenetics | 47 | $53.2M |
| Drugs and targets | 127 | $45.4M |
| Dogs and comparative oncology | 32 | $28.0M |
| Immunotherapy and the immune system | 51 | $26.5M |
| Metastasis and the lung | 83 | $23.2M |
| Germline and inherited risk | 18 | $15.3M |
| Laboratory models (PDX, 3D, mouse) | 35 | $9.9M |
| Clinical trials and outcomes | 12 | $4.7M |
| ctDNA and liquid biopsy | 8 | $3.3M |

## What this means for the research gaps

- **The thinnest funding lines match the report's main gaps.** Adapting treatment on early markers such as ctDNA (gap 4) has one current grant, at Dana-Farber. Trial methodology and pooled outcome data (gaps 1, 3 and 6) barely appear as NIH-funded projects at all.
- **Genomics is well funded but concentrated.** Most of it is one in-house NCI project. That fits the finding that the big genome re-analysis has already been done, and suggests marginal money is better spent elsewhere.
- **Dog studies get steady support** ($28M), mainly through two U01 cooperative agreements in fiscal 2025, which makes the open canine genome re-analysis a natural fit for existing NIH-funded groups.

## What this tracker cannot see

- **Cooperative-group trial money.** Children's Oncology Group trials are paid through network grants that are not labelled by disease, so NIH spending on osteosarcoma *trials* is undercounted here.
- **Big grants that cover osteosarcoma among other cancers**, such as the Sarcoma SPORE or the Pediatric Oncology Branch, land in the incidental tier and are excluded.
- **Non-NIH money:** foundations, the Department of Defense and companies are not included.
- **Title-based topics are approximate.** Some grants fit several topics and some fit none.
- The NCI budget figure is approximate and was not pulled from the API.
