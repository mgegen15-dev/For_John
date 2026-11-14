# NIH funding for osteosarcoma, 2015–2025

*Built from the NIH RePORTER API on November 14, 2026 with `tools/nih_funding_tracker.py`. Every grant is listed in `data/nih_osteosarcoma_projects.csv` and, for comparison, `data/nih_neuroblastoma_projects.csv`. The topic table is rebuilt with `python3 tools/nih_funding_tracker.py --topics`. Re-run the script to refresh everything.*

## Summary

In fiscal 2025 NIH spent **about $18.0 million on 30 grants that name osteosarcoma in their title**, four times the 2015 level but still only about a quarter of one percent of the National Cancer Institute's budget. Neuroblastoma, a childhood cancer of broadly similar size, received $28–30 million on the same basis, and roughly twice as much as osteosarcoma over the decade ($212–227 million against $108 million). A third of the osteosarcoma money went to NCI's own in-house laboratories, and one long-running genome project accounts for $20.4 million of it. The areas this project's other reports flag as the biggest gaps get the least: ctDNA and liquid-biopsy work received $3.3 million, all since 2020 and all at one institution, and clinical-trial and outcomes research $4.7 million. NIH money for osteosarcoma trials through the Children's Oncology Group is not visible here, so trial funding is undercounted.

**How to read the labels.** Each key number carries one of these tags: **(registry)** means taken directly from a public record, here NIH RePORTER; **(our calculation)** means we added up or derived the figure from those records; **(paper, full text)**, **(paper, abstract only)** and **(press release only)** mark figures taken from publications. Most numbers in this report are our sums of RePORTER records.

## How grants were counted

A plain text search overcounts badly, because U2OS, an osteosarcoma cell line, is used throughout general cell biology. The tool searches RePORTER for "osteosarcoma" and for "osteogenic sarcoma" (the second search added no grants that the first had missed) and sorts each grant into a tier:

| Tier | Rule | FY2025 |
|---|---|---|
| **Focused** | "Osteosarcoma" or "osteogenic sarcoma" in the project title | 30 projects, $18.0M (our calculation) |
| **Substantial** | Named 3 or more times in the abstract or public-health statement | 8 projects, $7.4M (our calculation) |
| Incidental | Named once or twice only | 205 projects, $109.9M (our calculation; mostly unrelated work, not counted below) |

**Multi-project grants.** In RePORTER, each component of a programme grant (P01, P50, U54 and similar) has its own record and award amount, and the parent record's amount already includes them. Records are grouped by core project number, fiscal year and full award number. If any component of that award matched the search, only the matching components are counted; otherwise the parent award is counted. Administrative supplements have their own award numbers and are counted separately.

**The "substantial" tier is an upper bound, not osteosarcoma money.** Of its $58.3M over the decade, about $55.3M (95%) comes from programmes that cover many cancers (our calculation): NCI's Genetic Modifiers of Cancer Risk ($13.7M), the Comparative Oncology Program laboratory ($15.3M across three in-house records), Functional Genomics of Sarcoma ($12.0M), the Childhood Cancer Data Initiative ($3.4M), a co-clinical macrophage-imaging resource ($3.2M), and several smaller in-house and paediatric-tumour programmes. The "focused + substantial" column below is therefore the most that could be attributed to osteosarcoma, and the real figure is much closer to the focused column.

## Osteosarcoma against neuroblastoma, by year

| Fiscal year | Osteosarcoma focused | Osteosarcoma focused + substantial (upper bound) | Neuroblastoma focused |
|---|---|---|---|
| 2015 | $4.5M (12) | $8.1M | $10.0M (31) |
| 2016 | $5.0M (16) | $8.5M | $12.1M (32) |
| 2017 | $7.9M (20) | $11.3M | $12.8M (32) |
| 2018 | $6.1M (19) | $9.5M | $15.3M (41) |
| 2019 | $6.4M (16) | $10.3M | $13.8M (38) |
| 2020 | $7.9M (20) | $10.8M | $21.3M (40) |
| 2021 | $11.3M (27) | $17.5M | $22.6M (47) |
| 2022 | $12.7M (27) | $18.6M | $27.0M (49) |
| 2023 | $13.9M (28) | $23.8M | $22.7M (51) |
| 2024 | $14.5M (29) | $22.9M | $25.8M (53) |
| 2025 | $18.0M (30) | $25.5M | $28.4M (50) |
| **2015–2025** | **$108.3M** | **$166.6M** | **$211.8M** |

*All figures are our calculation from RePORTER records. Numbers in brackets are projects funded that year.*

**A note on the neuroblastoma comparison.** Neuroblastoma has large programme grants whose title names the disease but whose individual components mostly do not, such as a long-running neuroblastoma P01. Under the counting rule above, only components whose own title names neuroblastoma count as focused, which gives the $211.8M shown. If every matched component of a neuroblastoma-titled programme grant is counted as focused, the decade total is $226.8M and FY2025 is $30.4M (our calculation). Either way neuroblastoma received about twice as much (2.0–2.1 times). No osteosarcoma total changes under the alternative rule.

The NCI budget used for the quarter-of-one-percent comparison (about $7.2 billion in fiscal 2025) is approximate and was not pulled from the API. The comparison sets title-named NIH grants against the NCI budget alone, so it is a rough scale, not a precise share.

## Where the osteosarcoma money goes

All figures in this section are focused-tier totals for 2015–2025 unless stated (our calculation).

**By funder:** NCI provided $101.3M of the $108.3M (94%). The rest came in small amounts from NIGMS ($3.2M), the NIH Director's office ($2.9M), NIBIB, NICHD and NCATS.

**By grant type:** standard investigator grants (R01) $37.2M; NCI in-house research (ZIA) $36.6M; cooperative agreements (U01) $10.8M; exploratory grants (R21) $4.7M; small-business grants (R44) $4.1M; R37 merit awards $3.4M. Career-development and training awards (K and F grants) total **$4.8M**: K01 $2.3M, K08 $1.1M, F30 $0.6M, F31 $0.6M and F32 $0.3M. That is a small share of the total; whether it means too few osteosarcoma scientists are being trained is a judgement these data cannot settle.

**By topic**, classified from grant titles (focused and substantial tiers, 2015–2025; one grant can fall in several topics; regexes are in `tools/nih_funding_tracker.py`):

| Topic | Project-years | Funding | Largest single programme |
|---|---|---|---|
| Drugs and targets | 133 | $47.9M | DKK-1 metastasis R01, $3.3M (7%) |
| Genomics and epigenetics | 43 | $37.5M | NCI in-house genome project, $20.4M (54%) |
| Dogs and comparative oncology | 31 | $28.5M | NCI Comparative Oncology Program laboratory, $13.6M (48%) |
| Immunotherapy and the immune system | 51 | $26.5M | NCI in-house immune-evasion project, $4.9M (19%) |
| Metastasis and the lung | 83 | $23.2M | DKK-1 metastasis R01, $3.3M (14%) |
| Germline and inherited risk | 18 | $14.8M | Genetic Modifiers of Cancer Risk (multi-cancer, in-house), $13.7M (93%) |
| Laboratory models (PDX, 3D, mouse) | 35 | $9.9M | MD Anderson PDX U01, $2.0M (20%) |
| Clinical trials and outcomes | 12 | $4.7M | Testicular effects of chemotherapy R01, $3.2M (68%) |
| ctDNA and liquid biopsy | 8 | $3.3M | Dana-Farber liquid-biopsy R37, $2.8M (85%) |

*All our calculation. Title keywords are approximate: some grants fit several topics and some fit none.*

## What this means for the research gaps

- **The thinnest funding lines match the project's main gaps.** Adapting treatment on early markers such as ctDNA has two current grants, both at Dana-Farber: an R37 ($814K in FY2025, focused tier) and a K08 career award ($254K, substantial tier) (registry). Every ctDNA dollar in the decade was awarded from FY2020 on. Trial methodology and pooled outcome data barely appear as NIH-funded projects at all ($4.7M, mostly one grant on testicular effects of chemotherapy).
- **Genomics money is concentrated in NCI's in-house programme.** Two in-house projects, the osteosarcoma genome project ($20.4M) and Functional Genomics of Sarcoma ($12.0M, which covers sarcomas generally), make up 86% of the genomics topic (our calculation). Extramural genomics grants are small.
- **About half the dog money is NCI's own comparative oncology laboratory, which studies many cancers.** The Comparative Oncology Program's in-house records total $15.3M of the $28.5M dog topic (54%) (our calculation). The three canine osteosarcoma U01 cooperative agreements (Colorado State, Tufts, UC Davis) total $7.2M over the decade, and the two active in FY2025 (Tufts, UC Davis) total $1.26M that year (registry). Dog work is supported, but extramural canine osteosarcoma funding is modest.

## What this tracker cannot see

- **Cooperative-group trial money.** Children's Oncology Group trials are paid through network grants that are not labelled by disease, so NIH spending on osteosarcoma *trials* is undercounted here.
- **Big grants that cover osteosarcoma among other cancers** mostly fall outside the focused tier. The MD Anderson Sarcoma SPORE parent award is incidental, but its Project 3 (antibody-drug conjugates, $478K in FY2025) names osteosarcoma in its title and is counted in the focused tier. The Count Me In programme, which runs the patient-partnered Osteosarcoma Project, names osteosarcoma often in its parent abstract, but its matching components do not, so under the counting rule it falls in the incidental tier and is not counted.
- **Non-NIH money:** foundations, the Department of Defense and companies are not included.
- **Title-based topics are approximate.** Some grants fit several topics and some fit none.
- **The NCI budget figure is approximate** and was not pulled from the API.

## Change log

- **November 13–14, 2026:** first version, built with the original tracker.
- **November 14, 2026, after an independent audit:**
  - **De-duplication fixed in the tool.** The original code grouped records by application ID, but every component of a programme grant has its own ID, so parent awards and their components were both kept (26 osteosarcoma and 28 neuroblastoma parent-years). The tool now groups by core project number, fiscal year and award number, and the CSVs were regenerated. Osteosarcoma focused totals are unchanged. Neuroblastoma focused FY2025 changed from $30.8M (51 projects) to $28.4M (50), or $30.4M if programme-grant components inherit the parent's tier; the decade total changed from $227.9M to $211.8M (or $226.8M). Osteosarcoma "focused + substantial" changed from $183.2M to $166.6M, mainly because the Count Me In parent award is no longer counted, and is now labelled an upper bound with its multi-cancer programmes named.
  - **Search widened** to "osteogenic sarcoma" as well as "osteosarcoma" (no new grants found).
  - **Topic classifier added to the tool** so the topic table can be rebuilt. Topic figures changed slightly with the new regexes and de-duplication; genomics fell from $53.2M to $37.5M because Count Me In left the substantial tier.
  - **Corrections:** K and F training grants total $4.8M, not "under $4M"; the dog total is about half NCI's in-house Comparative Oncology Program laboratory, not "mainly two U01s"; ctDNA has two current grants, not one, and all its funding is since 2020; the Sarcoma SPORE is partly counted, not wholly excluded. The opinion that few scientists are being trained, and an unsupported cross-report claim that "the big genome re-analysis has already been done", were removed. FY2018 and FY2024 upper-bound figures were re-rounded.
