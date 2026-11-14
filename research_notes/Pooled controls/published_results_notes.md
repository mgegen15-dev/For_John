# Published results added to the pooled control dataset

*November 14, 2026. Rows are in `data/osteosarcoma_relapse_benchmarks_published.csv` (60 rows; same columns as `osteosarcoma_relapse_benchmarks.csv`). Each row's `source_note` gives the PMID or DOI and says whether the number came from the full text or only the abstract.*

## What was added

- **26 trials not in the registry-only dataset, about 738 patients.** That is 616 patients if you leave out ARTEMIS-011, which is a phase 3 trial limited to patients with at least two prior lines of treatment.
  - Lagmay 2016 (full text): all 7 component COG trials with their own 4-month EFS, plus AOST0221, the resected-relapse benchmark.
  - Other trials: REGOBONE, Italian sorafenib, sorafenib + everolimus, apatinib, APFAO, SARC003, ET-743, the Norway/Italy pembrolizumab trial, pazopanib, gemcitabine + nab-paclitaxel, OAIE, ARTEMIS-011, PEPN1924, ESMMO, saracatinib, SARC028 (osteosarcoma subset), anlotinib and inhaled lipid cisplatin.
- **Extra numbers for registry trials:**
  - 4-month and median PFS from the papers for CABONE, OLIE, ITCC-050 (single-agent lenvatinib and the combination) and APFAO.
  - The 95% CI for AOST1421.
  - The hazard ratio for SARC024.

## Surprises and conflicts

1. **Lagmay Table 2 is not uniform.** The pooled figure is 12% (6–19%), but the trials differ a lot. Docetaxel (CCG-0962) gave 23% and oxaliplatin (ADVL0421) 31%, with 2 patients still event-free at 8 and 46 months. Topotecan, irinotecan and imatinib had no patient event-free at 4 months. Docetaxel was the only agent with radiographic responses (2 of 21).
2. **The randomized ifosfamide/etoposide (IE) control arms sit far above the 12% benchmark.** OLIE IE: 66.0% PFS at 4 months (n=41). OAIE IE: 41.6% (n=28). So the single-arm TKI + IE results (51–76%) are mostly what IE does by itself. The OLIE gap is 76.3% against 66.0%. This is the main reason the 12% benchmark should not be used for chemotherapy-containing regimens.
3. **CABONE: the paper and the registry use different measures.** The registry posts 33.3% "6-month non-progression", a crude count. The paper's Kaplan–Meier figures are 71.4% PFS at 4 months and 52.4% at 6 months. APFAO has the same split: 13 of 43 (30%) were progression-free at 6 months by crude count, against a 50.9% KM estimate. Crude and KM rates should not be mixed in one comparison.
4. **ITCC-050: the registry and the papers disagree on the denominator.**
   - Single-agent lenvatinib: the registry gives 32.1% (n=28). The ESMO Open paper gives 29.0% by binomial estimate (n=31) and 37.8% by KM.
   - Lenvatinib + IE: the registry gives 66.7% (n=15, cohort 3B only). The Lancet Oncol paper pools 35 patients treated at the recommended dose and gives 51% (34–69%).
   - For pooling I used the paper values, because they are larger and cover the whole full analysis set.
5. **The "FOSTER ~3,245 patients" BJC 2025 review is about prognostic factors, not phase 2 efficacy.** Rubio-San-Simón et al. (PMID 40731087) covers 19 studies and 3,245 patients and has no per-trial efficacy table. The FOSTER phase 2 review is van Ewijk et al., Cancer Treat Rev 2023 (PMID 37738712). It reports efficacy data on 1,361 osteosarcoma patients in 58 trials, and 21% of those trials were called positive, mostly multi-kinase inhibitor trials. Its per-trial table could not be reached: cancertreatmentreviews.com and nature.com are blocked in this session, and Europe PMC and PMC have no full text. That table is the main source still to add.
6. **No later COG pooled osteosarcoma benchmark paper was found.** COG published comparable pooled benchmarks for rhabdomyosarcoma (PBC 2024, PMID 38627882) and non-rhabdomyosarcoma soft-tissue sarcoma (Cancer 2024, PMID 38470405), but none for osteosarcoma. The AOST1421 paper restates the AOST0221 figure (20%, 10–34%).
7. **Olaparib + ceralasertib has only been published as an ASCO 2025 abstract** (Forrest, J Clin Oncol 43 suppl 16, abstr 10005). ascopubs.org is blocked here. Two reviews cite it as "4-month EFS about 15%, ORR 5.3%", and an ACCELERATE review says 1 of 37 patients responded. That is consistent with the registry row (5/34). No new row was added.
8. **ARTEMIS-011 (B7-H3 ADC against gemcitabine/docetaxel, phase 3, 2026):** median PFS was 1.4 months in the gemcitabine/docetaxel arm (n=42). This is the first randomized gemcitabine/docetaxel control, and it backs up the older view that this regimen does little in later lines.
9. **Resected relapse:** the saracatinib placebo arm (NCT00752206) had a median PFS of 8.6 months (n=19) after metastasectomy. That fits the 12-month EFS benchmark of about 20–30%.

## Not added

- No numbers could be reached for prospective trials of high-dose ifosfamide. Only retrospective series exist (PMIDs 33142760, 32297446, 38898388), and none was extracted.
- I excluded outcomes from basket trials with osteosarcoma n ≤ 3 (ADVL1412 nivolumab, ADVL1412 nivolumab + ipilimumab).
- REGOBONE has no 4-month value. Only 8-week non-progression was reachable, from the abstract.

## 4-month EFS/PFS in measurable relapse, pooled by drug class (patient-weighted)

One row per arm, with no arm counted twice; paper values are used where they replace registry values. This mixes KM and binomial estimates. The CIs are rough normal approximations.

| Class | Arms | n | Weighted 4-month rate | Arm range |
|---|---|---|---|---|
| Cytotoxic / older agents (COG pooled, eribulin, gemcitabine + nab-paclitaxel) | 3 | 133 | 12.5% (about 7–18%) | 0–28% |
| Biologic / ADC / DNA-repair (denosumab, glembatumumab, olaparib + ceralasertib) | 3 | 71 | 12.7% (about 5–20%) | 7–15% |
| VEGFR TKI alone (sorafenib, apatinib, lenvatinib, cabozantinib) | 4 | 145 | 52.5% (about 44–61%) | 29–71% |
| VEGFR TKI + IE (ITCC-050, OLIE, OAIE) | 3 | 128 | 65.0% (about 57–73%) | 51–76% |
| VEGFR TKI + PD-1 (APFAO) | 1 | 43 | 66.3% | — |
| IE alone (OLIE and OAIE control arms) | 2 | 69 | 56.1% (about 44–68%) | 42–66% |

Script: the pooling calculation was a one-off in the scratchpad. Rerun it from the CSV if the dataset changes.
