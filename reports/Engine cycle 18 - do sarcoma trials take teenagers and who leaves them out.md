# Engine cycle 18: do trials for Ewing sarcoma, rhabdomyosarcoma and other sarcomas take teenagers, and who leaves them out?

*Run November 26, 2026. The eighteenth cycle of the For John research engine. Pre-registration: `research_notes/Engine/cycle-18-sarcoma-teen-access/PREREGISTRATION.md`, committed at commit `ec7d1b6` before the registry was searched. Script: `tools/engine_cycle18_sarcoma_teen_access.py`. Results: `data/engine/cycle18/`. Based on ClinicalTrials.gov records read on November 26, 2026. Not medical advice.*

## Summary

Cycle 12 found that trials naming osteosarcoma usually take teenagers, while early trials of new drugs for "solid tumours" rarely do. This cycle looked at recruiting drug trials for the other sarcomas.

- **Trials naming Ewing sarcoma or rhabdomyosarcoma, the other two common sarcomas of the young, usually take teenagers:**
  - Ewing: 45 of 51 (88%; 95% CI 77–94%);
  - rhabdomyosarcoma: 36 of 41 (88%; 74–95%).
- **Trials for other sarcomas mostly do not:** 32 of 155 (21%; 15–28%).
- **Company-led trials leave teenagers out more often.**
  - Across all three sets, 11 of 51 company-led trials accept teenagers (22%), against 86 of 179 others (48%). Odds ratio 0.30 (0.14–0.62); **supported** by the pre-registered rule.
  - The gap holds within the "other sarcoma" set alone: 4 of 42 against 28 of 113 (odds ratio 0.32, 0.10–0.97).
- **Predictions:** P49, P50 and P51 were all right.

**How to read the labels.** Every number here is **(our calculation)** from **(registry)** records.

## What was counted

- **Filters:** recruiting or not-yet-recruiting interventional trials with at least one drug, biological or genetic intervention.
- **Sets,** each found by the registry's condition search and kept only if the disease is named in the record:
  - Ewing sarcoma;
  - rhabdomyosarcoma;
  - "other sarcoma": a condition contains "sarcoma", and the record does not mention osteosarcoma, Ewing, rhabdomyosarcoma or Kaposi sarcoma.
- **Overlap:** a trial may be in both the Ewing and rhabdomyosarcoma sets. The combined comparison counts each trial once (230 trials).
- **Accepts teenagers:** as in cycle 12. All drug trials were counted, not only those for relapsed disease.

## Results

| Set | Trials | Accept teenagers | Of those, with a US site | Company-led share of the set |
|---|---|---|---|---|
| Ewing sarcoma | 51 | 45 (88%) | 29 | 14% |
| Rhabdomyosarcoma | 41 | 36 (88%) | 23 | 5% |
| Other sarcoma | 155 | 32 (21%) | 15 | 27% |
| *Osteosarcoma, relapse trials (cycle 12, read record by record)* | *58* | *44 (76%)* | *32* | |

| Comparison | Company-led | Others | Odds ratio (95% CI) |
|---|---|---|---|
| **All three sets (H1)** | **11 of 51 (22%)** | **86 of 179 (48%)** | **0.30 (0.14–0.62)** |
| Other sarcoma only | 4 of 42 (10%) | 28 of 113 (25%) | 0.32 (0.10–0.97) |

## What this means

- **The pattern is the same across the sarcomas of the young.** Trials that list osteosarcoma, Ewing sarcoma or rhabdomyosarcoma usually take teenagers. Few of them are company-led (5% to 14% in these sets).
- **Where companies lead, teenagers are left out more often.** That matches cycles 12 and 17 and is the gap the brief addresses.
- **A fair caveat:** "other sarcoma" includes many adult sarcomas, such as leiomyosarcoma and liposarcoma, which are rare in teenagers. So a low share there is partly expected. The company-against-others gap within that set is the more telling number.
- **The brief's request** (open tumour-agnostic and sarcoma trials to 12- to 17-year-olds once adult dosing allows) applies across sarcoma, not only to osteosarcoma.

## Limits

- Text-matched sets, without hand reading.
- Only the age fields were read.
- One registry on one day.
- Small company-led counts in the Ewing and rhabdomyosarcoma sets.

## Files and reproduction

- `python3 tools/engine_cycle18_sarcoma_teen_access.py fetch` searches ClinicalTrials.gov. Raw records are not in git.
- `python3 tools/engine_cycle18_sarcoma_teen_access.py` builds `data/engine/cycle18/trials.csv` and `results.json`.

**Data source.** ClinicalTrials.gov API v2 (US National Library of Medicine).

## Change log

- 2026-11-26: cycle run and reported. H1 supported; P49 to P51 right. No deviations.
