# Engine cycle 18: do trials for Ewing sarcoma, rhabdomyosarcoma and other sarcomas take teenagers, and who leaves them out?

*Pre-registered November 26, 2026, before the registry was searched for this cycle. This file is committed to git before the search; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycle 12 found that most recruiting drug trials naming osteosarcoma accept teenagers, but early trials of new drugs for "solid tumours" almost never do. Cycle 17 found that this second share has fallen since 2019.

Ewing sarcoma and rhabdomyosarcoma also strike teenagers often, and many other sarcomas affect adolescents and young adults (general knowledge). If the same split shows across these diseases, and if company-led trials are the ones that leave teenagers out, the brief's request applies to sarcoma generally, not only to osteosarcoma.

## Data

ClinicalTrials.gov API v2, searched once on the day of the run. Filters:
- interventional;
- recruiting or not yet recruiting;
- at least one drug, biological or genetic intervention, as in cycle 12.

Raw records stay out of git because they include staff contact details.

## Sets (by the registry's condition search, then kept only if the word appears in the record's conditions, keywords, titles or eligibility text)

- **Ewing:** condition search "Ewing sarcoma"; text contains "ewing".
- **Rhabdomyosarcoma:** condition search "rhabdomyosarcoma"; text contains "rhabdomyosarcoma".
- **Other sarcoma:**
  - Condition search "sarcoma"; a condition contains "sarcoma".
  - Trials mentioning osteosarcoma, Ewing or rhabdomyosarcoma anywhere in that text are removed, as are Kaposi sarcoma trials.
- A trial can be in both the Ewing and the rhabdomyosarcoma sets.

Relapse eligibility is not classified, since cycle 12 showed the text rule over-counts; all drug trials in each set are counted. This is a description of the trials, not of who can enrol.

## Definitions

"Accepts teenagers" and sponsor type are as in cycle 12.

## Measures

1. For each set: number of trials and the share accepting teenagers (95% Wilson interval), and the share with a US site among those that accept teenagers.
2. **H1 (main test):** across the three sets combined (each trial counted once), the odds ratio for accepting teenagers, company-led against all others, with a 95% interval (Woolf) and Fisher's exact p.
3. Within "other sarcoma": the same odds ratio.

## Verdict rule for H1, fixed now

| Verdict | Rule |
|---|---|
| **Supported** (company-led trials accept teenagers less often) | odds ratio below 1, with the whole 95% interval below 1 |
| **Refuted** | the lower end of the 95% interval is above 0.67 |
| **Inconclusive** | anything else |

## Predictions, recorded before the search

In `PREDICTIONS.md`:
- **P49:** at least 60% of trials in the Ewing set accept teenagers (80%).
- **P50:** fewer than 40% of trials in the "other sarcoma" set accept teenagers (60%).
- **P51:** H1 is supported (70%).

## Deviations

*None yet.*
