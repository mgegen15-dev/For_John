# Osteosarcoma results pulled out of basket trials

*November 14, 2026. New rows are in `data/osteosarcoma_relapse_benchmarks_basket.csv` (33 rows, same 13 columns as the other two benchmark files). Every row's `source_note` says whether the number came from ClinicalTrials.gov posted results, a paper's full text or its abstract only, with the PMID, PMCID or DOI. No trial in this file was already in `osteosarcoma_relapse_benchmarks.csv` or `osteosarcoma_relapse_benchmarks_published.csv`.*

## How the trials were chosen

1. From `data/osteosarcoma_trials.csv` I took the interventional trials with scope = basket and status completed, terminated or active-not-recruiting. That gave 305 trials, 154 of them phase 2 or phase 1/2.
2. I downloaded the full ClinicalTrials.gov v2 record for all 114 of these with `has_results=True`. Then I searched every outcome group, class and category title or description for "osteo".
3. For the trials with an osteosarcoma cohort or stratum, plus the sarcoma-wide, COG/ADVL, Pediatric MATCH and Chinese trials named in the brief, I searched PubMed and Europe PMC. I read the full text from PMC wherever it was open access, and only the abstract otherwise.

Scripts and downloaded records are in the session scratchpad and were not kept in the project.

## What was added

- **17 trials, about 440 osteosarcoma patients.** One of them, NCT00667342 (St Jude bevacizumab + MAP), is in fact an osteosarcoma-only, newly diagnosed trial that was tagged basket by mistake. Leaving it out gives **16 true basket trials and about 400 patients**: 332 in measurable relapse and 68 in resected relapse (robatumumab Group 1).
- By setting:
  - Measurable relapse: 16 trials.
  - Resected relapse: 1 trial (robatumumab Group 1, median overall survival only).
  - Newly diagnosed: 1 trial (the St Jude trial).

| Trial | Agent | OS n | Key osteosarcoma number | Source |
|---|---|---|---|---|
| NCT00642941 SARC/Roche R1507 | anti-IGF-1R antibody | 38–40 | PFS rate at 18 weeks 19.7%; 2/38 PR (paper) vs 2.5% of 40 (registry); median PFS 5.7 weeks | registry + full text |
| NCT00617890 robatumumab | anti-IGF-1R antibody | 29 (unresectable), 68 (resected) | 0/29 responses, disease control 6/29; resected group median OS 18 and 22 months | registry + full text |
| NCT01016015 cixutumumab + temsirolimus (adult) | IGF-1R + mTOR | 24 | **3/24 PR (12.5%)**; median PFS 6.0 weeks | full text |
| NCT01614795 COG ADVL1221, same combination in children | IGF-1R + mTOR | 10 | 0/10 responses; KM PFS 9.1% | registry + full text |
| NCT00831844 COG ADVL0821 cixutumumab | anti-IGF-1R antibody | 9–10 | 0 responses | registry + full text |
| NCT01154816 COG ADVL0921 alisertib | aurora A inhibitor | 10 | 0/10 responses (2 SD) | registry + full text |
| NCT00520936 COG/Lilly pemetrexed | antifolate | 10 | 0/10 responses (1 SD) | registry + full text |
| NCT02304458 COG ADVL1412 | nivolumab; nivolumab + ipilimumab | 10 + 10 | 0/10 and 0/10 responses | registry + full text |
| NCT02406781 PEMBROSARC | pembrolizumab + metronomic cyclophosphamide | 15 | 1 PR (6.7%); 6-month non-progression 13.3% | registry + abstract |
| NCT03277924 IMMUNOSARC bone cohort | sunitinib + nivolumab | 17 | median PFS 3.5 months; 1/17 PR centrally | full text |
| NCT00464620 SARC009 | dasatinib | 46 | 5/46 progression-free at 6 months (10.9%) | registry |
| NCT00031915 imatinib, 10-subtype trial | imatinib | 27 | clinical benefit at 4 months 5/27 (18.5%) | abstract |
| NCT02357810 Northwestern PAZOTOP | pazopanib + oral topotecan | 28 | **12-week PFR 69.6%; median PFS 4.5 months** | registry + abstract |
| NCT02867592 COG ADVL1622 | cabozantinib | 29 | **response + disease control 35.2% (20–48%)**; 1-year PFS 14.7% | registry only |
| NCT03213678 Pediatric MATCH arm D | samotolisib | 6 | 0/6 responses | full text |
| NCT04074564 MASCT-I-1005 (China, phase 1) | cell therapy + camrelizumab + apatinib | 6 | 2/6 PR; median PFS 5.7 months | full text |
| NCT00667342 St Jude (OS-only) | MAP + bevacizumab | 31 / 42 | 3-year EFS 57.5% (localized); 2-year EFS 61.7% (all) | registry |

## Signals hidden in basket trials

1. **Pazopanib + oral topotecan (PAZOTOP, NCT02357810).** In the exploratory osteosarcoma cohort, 69.6% were progression-free at 12 weeks and the median PFS was 4.5 months (n=28). The authors themselves set this against the 12% benchmark. It fits the multi-kinase VEGFR inhibitor pattern, but topotecan is a chemotherapy partner. It should be judged against the IE control arms (42–66% at 4 months), not against 12%. The rate is also at 12 weeks, not 4 months. Abstract only: the PMC record had no body text.
2. **Cabozantinib in COG ADVL1622 (NCT02867592), 29 osteosarcoma patients.**
   - The "response + disease control" rate was 35.2% (20–48%). This is a second, independent cabozantinib osteosarcoma cohort alongside CABONE. Only the registry result and a 2021 ASCO abstract exist, and ascopubs.org is blocked here (HTTP 403).
   - The registry defines disease control by "protocol section 9.3.2", which I could not see. So this rate is not counted as a 4-month rate in the main table.
   - The 1-year PFS of 14.7% shows that the benefit does not last.
3. **IGF-1R antibodies are mostly inactive, with one partial exception.**
   - Cixutumumab + temsirolimus in adults (Schwartz 2013) gave **3/24 osteosarcoma partial responses (13%)**, against 0/10 for the same combination in children (ADVL1221).
   - R1507 gave 2/38 PR. In that trial, osteosarcoma was independently linked with longer survival (HR 0.57).
   - Robatumumab gave 3 PRs before surgery in the resectable osteosarcoma group, but 0/29 in unresectable disease.
   - So IGF-1R blockade may help a little in low-burden disease, but none of these trials reached its efficacy bar in osteosarcoma.
4. **Checkpoint inhibitors are confirmed inactive in osteosarcoma:**
   - nivolumab 0/10 and nivolumab + ipilimumab 0/10 (ADVL1412);
   - pembrolizumab + cyclophosphamide, 1/15 PR and 13% non-progression at 6 months (PEMBROSARC);
   - sunitinib + nivolumab, median PFS 3.5 months (IMMUNOSARC).
   This matches SARC028 and the Norway/Italy pembrolizumab trial, which are already in the dataset. The only immunotherapy combination with activity remains a VEGFR TKI paired with a PD-1 antibody (APFAO, and the 6-patient MASCT-I pilot).

## Conflicts and corrections

- **ADVL1412:** the earlier notes said ADVL1412 had osteosarcoma n ≤ 3. That count is only the Part A dose-finding cohort. Part B2 (nivolumab) and Part D2 (nivolumab + ipilimumab) each treated 10 osteosarcoma patients, and neither had a response. Both arms are now in the file.
- **R1507:** the registry gives 2.5% response in 40 osteosarcoma patients, which is 1 responder. The paper (Table 2) gives 2 PR in 38. Both rows are kept.
- **ADVL0821 cixutumumab:** the registry denominator is 9 and the paper's is 10 evaluable. Both have 0 responses.
- **SARC003 (NCT00073983, already in the published file):** the registry posts "5" for osteosarcoma (n=14) under "objective response rate". The outcome mixes response, stable and failure categories, and the paper reports 1/14 PR, so I did not add this value.

## Trials checked with no usable osteosarcoma-specific data

- **Registry results with no osteosarcoma split:**
  - NCT02500797 Alliance A091401: the paper lists 1 osteosarcoma patient in the dual-agent arm.
  - NCT02945800 Moffitt nab-paclitaxel + gemcitabine: a single pooled group; this appears to be the NPCF trial already in the published file.
  - NCT03718091 berzosertib: cohorts are defined by gene, not histology.
  - NCT00474994 sunitinib (MSKCC), NCT00802880 dacarbazine, NCT00024258 arsenic trioxide, NCT03458728 copanlisib (terminated before phase 2), NCT04751383 magrolimab + dinutuximab (osteosarcoma expansion has no posted efficacy), NCT05093322 surufatinib + gemcitabine, NCT04238819 abemaciclib, NCT03441360 eribulin (no osteosarcoma stratum) and NCT00070109 trabectedin (no osteosarcoma stratum).
  - NCT03860207 Hu3F8-BsAb: phase 1 only; 4 osteosarcoma patients across dose levels.
  - NCT02162732: "rare tumours" group only.
- **Paper without a usable osteosarcoma denominator:**
  - NCT00093080 ridaforolimus (Chawla JCO 2012, abstract only): 2 of the 4 confirmed PRs were in osteosarcoma, but the abstract gives no osteosarcoma denominator or clinical benefit rate.
  - SARC009 dasatinib paper (abstract): gives no osteosarcoma figures, so only the registry 6-month count was used.
- **No publication found:**
  - Chinese trials NCT05106777 (surufatinib, OS + STS, Sun Yat-sen) and NCT04690725 (TQB3525, PI3K bone sarcoma).
  - NCT05395741 (regorafenib, Polish bone-tumour trial).
- **Duplicates of the Lagmay 2016 COG pool, so not re-added:** NCT00003745 (topotecan continuous infusion), NCT00002825 (docetaxel), NCT00004078 (irinotecan), NCT00030667 (imatinib), NCT00091182 (oxaliplatin) and NCT00331643 (ixabepilone).
- **Other Pediatric MATCH arms:** olaparib, vemurafenib, selpercatinib, tipifarnib and tazemetostat had no osteosarcoma responders or no osteosarcoma patients. The palbociclib (NCT03526250) and larotrectinib arms are tagged os_only and fall outside this pass.
- **Not reachable:** ADVL1622 and the olaparib + ceralasertib ASCO abstracts (ascopubs.org blocked).

## Updated 4-month EFS/PFS in measurable relapse, by drug class (all three CSVs)

**Methods**
- I took one row per arm from the three CSVs and used no arm twice. Paper values replace registry values where both exist, as in the earlier table.
- I weighted each arm by its patient count.
- Rates within 4 months ± 2 weeks were accepted. R1507's 18-week landmark PFS rate (about 4.1 months) qualifies. Imatinib's "clinical benefit" also qualifies: response at 2 months, or stable disease or better at 4 months, which is in effect non-progression at 4 months.
- CIs are rough normal approximations on the pooled proportion. They ignore between-trial differences, so they are too narrow.
- The arm list is fixed in a scratchpad script that asserts exactly one matching row per arm.

| Drug class | Arms | Patients | Weighted 4-month rate | Range across arms |
|---|---|---|---|---|
| Older cytotoxics (COG pooled, eribulin, gemcitabine + nab-paclitaxel) | 3 | 133 | 12.5% (about 7–18%) | 0–28% |
| Antibodies, ADC, DNA-repair (denosumab, glembatumumab, olaparib + ceralasertib) | 3 | 71 | 12.7% (about 5–20%) | 7–15% |
| **New:** IGF-1R antibody (R1507) | 1 | 40 | 19.7% (about 7–32%) | — |
| **New:** non-VEGFR kinase inhibitor (imatinib, adult basket) | 1 | 27 | 18.5% (about 4–33%) | — |
| VEGFR TKI alone (sorafenib, apatinib, lenvatinib, cabozantinib) | 4 | 145 | 52.5% (about 44–61%) | 29–71% |
| VEGFR TKI + IE (ITCC-050, OLIE, OAIE) | 3 | 128 | 65.0% (about 57–73%) | 51–76% |
| VEGFR TKI + PD-1 (APFAO) | 1 | 43 | 66.3% | — |
| IE alone (OLIE and OAIE control arms) | 2 | 69 | 56.1% (about 44–68%) | 42–66% |

**Groupings and sensitivity checks**
- All antibody, ADC and DNA-repair arms together, R1507 included (4 arms, 111 patients): 15.2% (about 9–22%).
- Older cytotoxics plus imatinib (4 arms, 160 patients): 13.5%.
- **All non-VEGFR, non-IE arms together (8 arms, 271 patients): 14.2% (about 10–18%).** This sits close to the 12% Lagmay benchmark, so the basket trials back up the benchmark for drugs without a VEGFR kinase inhibitor.
- Adding ADVL1622 (35.2%, n=29) to the TKI-alone row: 5 arms, 174 patients, 49.6% (about 42–57%). It is left out of the main table because its endpoint definition was not seen.
- PAZOTOP (69.6% at 12 weeks, n=28) is left out because 12 weeks is too early. If counted, it would sit with the VEGFR TKI + chemotherapy group, at the level of IE.

**Caveats**
- Kaplan–Meier estimates and crude counts are mixed.
- Response-based "disease control" endpoints differ between trials.
- Patients were more heavily pretreated in the adult basket trials (R1507, imatinib) than in the COG trials.
- Basket cohorts are small; 4 of the new arms have n ≤ 10, which is why they appear only as response rows.
- The imatinib and PEMBROSARC figures come from abstracts only.
- Several basket trials report only 6-month or 12-week rates or a median PFS, so they cannot enter the 4-month table. Those numbers are dasatinib 10.9% at 6 months, PEMBROSARC 13.3% at 6 months, PAZOTOP median PFS 4.5 months, IMMUNOSARC median PFS 3.5 months, and cixutumumab + temsirolimus median PFS 6 weeks.

**Bottom line:** nothing in the basket trials changes the picture. Agents without a VEGFR kinase inhibitor cluster at about 12–20% at 4 months. VEGFR TKIs given alone sit around 50%. Anything combined with IE should be compared with IE's 42–66%.
