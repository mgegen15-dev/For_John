# Engine cycle 17: before and after the FDA's 2019 guidance, across all trials, not just those recruiting today

*Pre-registered November 26, 2026, before the registry was searched for this cycle. This file is committed to git before the search; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycle 16 compared trials recruiting today by start year. It found no sign that the US Food and Drug Administration's March 2019 guidance on including adolescents had made new early-phase trials more open to teenagers. But that design was biased: the few older trials still recruiting are unusual ones.

The fair comparison takes every trial that started in a period, whatever its status now.

## Data

ClinicalTrials.gov API v2, searched once on the day of the run, with these filters:
- condition search "solid tumor";
- interventional;
- start date from January 1, 2014 to December 31, 2018 (**before**) or from January 1, 2020 to December 31, 2024 (**after**).

2019, the year the guidance was issued, is left out. Trials withdrawn before enrolling anyone are excluded.

The same filters as cycle 12's Set B then apply:
- a condition reading "solid tumor", "solid tumour" or "solid neoplasm";
- phase 1, 1/2, early phase 1 or 2;
- at least one drug, biological or genetic intervention.

Raw records stay out of git because they include staff contact details.

## Definitions

As in cycle 12. "Accepts teenagers" means the minimum age is 17 or younger (or none is given) and any maximum age is 12 or older. Sponsor type is the registry's lead-sponsor class. The age limits are those in the record today, which may reflect later amendments. That is a caveat.

## Measures

- **H1 (main):** odds ratio for accepting teenagers, after against before, with a 95% interval (Woolf) and Fisher's exact p.
- **Secondary:**
  - company-led trials only;
  - adult-type trials only, leaving out those whose minimum age is under 12, so the question is whether trials built for adults opened down to teenagers;
  - the share by start year.

## Verdict rules, fixed now (H1)

| Verdict | Rule |
|---|---|
| **Supported** | odds ratio above 1, with the whole 95% interval above 1 |
| **Refuted** | the upper end of the 95% interval is below 1.5 |
| **Inconclusive** | anything else |

## Predictions, recorded before the search

In `PREDICTIONS.md`:
- **P47:** H1 is supported (35%).
- **P48:** fewer than 5% of company-led trials that started in 2020–2024 accept teenagers (80%).

## Deviations

Recorded November 26, 2026, after the run.

1. **Phase filter.** The code kept any trial with an early phase among its phases, so 15 phase 2/3 trials entered. Without them the odds ratio is 0.41. Reported in the cycle report.
