# Engine cycle 16: since the FDA's 2019 guidance, are new early-phase cancer trials more likely to take teenagers?

*Pre-registered November 26, 2026. This cycle reuses the registry records saved by engine cycle 12 on November 26, 2026. Cycle 12 read their age limits, sponsors, phases and countries, but not their start dates, and no start date has been read for this cycle. This file is committed to git before the start dates are read; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

In March 2019 the US Food and Drug Administration issued guidance recommending that adolescents aged 12 to 17 be included in adult cancer trials relevant to their disease or to the drug's target. For first-in-human trials, it recommends this once some adult dosing data exist (FDA guidance; quoted in `briefs/Brief - trial access for teenagers with osteosarcoma.md`).

Cycle 12 found that 78 of 1,434 recruiting early-phase "solid tumour" drug trials (5.4%) accept anyone under 18. If the guidance changed practice, trials started after it should accept teenagers more often than trials started before it.

## Data

Set B of engine cycle 12 (`data/engine/cycle12/set_b.csv`, raw records in `data/engine/cycle12/raw/set_B.json`, not in git): 1,434 recruiting or not-yet-recruiting early-phase drug trials for solid tumours. Each trial's start date is read from the registry record (actual or anticipated).

## Groups

- **Before the guidance:** start date before January 1, 2020. Trials designed after March 2019 would mostly start in 2020 or later.
- **After the guidance:** start date on or after January 1, 2020.
- Trials with no start date are excluded and counted.

**A built-in bias, stated in advance.** Every trial here is still recruiting in November 2026. A trial that started before 2020 and is still recruiting is unusual: long-running, often an academic or children's trial that adds groups over time. That may make the "before" group look *more* open to teenagers than pre-2019 trials were in general. The comparison is therefore conservative for detecting an increase.

## Measures

- **Main (H1):** odds ratio for accepting teenagers (as defined in cycle 12), after against before, with a 95% interval (Woolf, with 0.5 added to every cell if any cell is zero), and Fisher's exact p.
- **Secondary:**
  - the same comparison within company-led trials only, and within trials not led by companies;
  - the share accepting teenagers by start year (descriptive);
  - the same comparison after removing trials whose minimum age is under 12 (mostly children's trials), so that the question is about adult trials opening to teenagers.

## Verdict rules, fixed now (H1)

| Verdict | Rule |
|---|---|
| **Supported** | odds ratio above 1, with the whole 95% interval above 1 |
| **Refuted** | the upper end of the 95% interval is below 1.5 (an increase in the odds of 50% or more is ruled out) |
| **Inconclusive** | anything else |

## Predictions, recorded before the data

In `PREDICTIONS.md`:
- **P45:** H1 is supported (30%).
- **P46:** among company-led trials started in 2020 or later, fewer than 5% accept teenagers (75%).

## Deviations

Recorded November 27, 2026, after the run.

1. **Phase filter.** Set B from cycle 12 includes 16 phase 2/3 trials. Without them the odds ratio is 0.18 (0.07–0.47). Reported in the cycle report.
