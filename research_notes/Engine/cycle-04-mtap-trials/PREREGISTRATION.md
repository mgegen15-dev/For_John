# Engine cycle 4: which MTAP-selected drug trials could an osteosarcoma patient join?

*Pre-registered November 24, 2026, before any search of ClinicalTrials.gov for these trials. This file is committed to git before the search; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycle 3 found that about one in five relapsed osteosarcomas has lost CDKN2A, and estimated that about one in seven has also lost the neighbouring gene MTAP. Drugs aimed at tumours without MTAP (PRMT5 inhibitors that act only when MTAP is missing, and MAT2A inhibitors) are in trials in adults. Most osteosarcoma patients are teenagers and young adults. Whether any of those trials would take them is a factual question the registry can answer, and it matters now for patients whose tumour report shows the deletion.

This is a descriptive cycle. It has no hypothesis to support or refute, only counting rules fixed in advance and one prediction.

## Search, fixed now

ClinicalTrials.gov, through its public API, searching all fields for each of these terms: MTAP; methylthioadenosine phosphorylase; PRMT5; MAT2A; and the drug names MRTX1719, BMS-986504, AMG 193, TNG908, TNG462, TNG456, AZD3470, IDE397, S095035, PRT811, PRT543, GSK3326595, JNJ-64619178, PF-06939999, AG-270, SCR-6920, SH3765, BGB-58067, ISM3412. Any further drug of the same two classes that the search turns up is added and listed.

## Which trials count

- Interventional studies whose status is recruiting, not yet recruiting, enrolling by invitation, or active but not recruiting. Completed, terminated, withdrawn and unknown-status trials are listed separately and not counted.
- The trial must either require MTAP loss or 9p21 (CDKN2A) deletion for entry in at least one group, or test a PRMT5 or MAT2A inhibitor.

## What is recorded for each trial

Read from the registry record's conditions, entry criteria and age fields:

1. **Open to osteosarcoma?** One of: "yes, named" (osteosarcoma or bone sarcoma is listed); "yes, by tumour-agnostic entry" (any advanced solid tumour with MTAP loss, with no list that leaves osteosarcoma out); "no" (limited to named tumour types that do not include it, or to blood cancers or brain tumours only); "unclear".
2. **Minimum age** as registered.
3. Phase, status, sponsor type (company or academic), countries with sites, and the drug.
4. Whether MTAP loss must be shown before entry, and by what test if stated.

## The numbers to report

- A. Trials currently recruiting (or about to) that an osteosarcoma patient with MTAP loss could join by criteria 1.
- B. Of A, how many accept patients under 18, and the youngest age accepted.
- C. Of A, how many have a site in the United States.

## Prediction, recorded before the search

P19 in `PREDICTIONS.md`: at least one trial in A accepts patients under 18. Probability 35%. Wrong if none does.

## Limits known in advance

Registry records can lag behind what a trial actually does, entry criteria are often summarised, and "any solid tumour" trials can still turn away rare tumours in practice. This cycle lists what the registry says; it is not advice about joining a trial. Not medical advice.

## Deviations

Recorded November 24, 2026, after the search.

1. **Drugs added.** As the plan allowed, drugs of the same two classes found through the general terms were included: GH56, BAY 3713372, HRS-6719, HSK41959, CTS3497, PEP08, DC50292A, GS-5319, GS-2426, ABSK131, SY-9453, HS-10587, CS08399, IDE892 and JBI-778.
2. **One false match removed.** A dental study in which "MTAP" stands for an antibiotic paste met the text rule and was classed "not relevant".
3. **A trial of an older chemotherapy counted.** One trial gives pemetrexed, not a PRMT5 or MAT2A inhibitor, but requires MTAP loss in one group, so it meets the rule as written and is counted, with a note.
4. **One reader.** Each record was classified once, by reading its conditions, entry criteria and study groups. The classification file is public.
