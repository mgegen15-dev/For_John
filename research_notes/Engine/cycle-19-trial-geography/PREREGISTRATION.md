# Engine cycle 19: where in the United States can a teenager with relapsed osteosarcoma reach a trial?

*Pre-registered November 27, 2026. This cycle reuses the registry records saved by engine cycle 12 on November 26, 2026. Cycle 12 read whether each trial had a US site, but not the site locations. This file is committed to git before any site's state or city is read; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycle 12 (as corrected) found 44 recruiting or soon-to-recruit drug trials that list osteosarcoma, take relapsed disease and accept 12- to 17-year-olds; 32 have a US site. A family's real question is how far they would have to travel. This cycle counts where those US sites are.

## Data

- The 32 trials from cycle 12's corrected classification (`data/engine/cycle12/hand_classification.csv` together with `set_a.csv`) that are relapse-eligible treatment trials, accept teenagers and have a US site.
- Locations from the saved raw records: country, state and city only.
  - A site counts if it is in the United States and its own status is not "withdrawn", "completed" or "terminated".
  - A site with no status given counts.
- No contact details are read or published.

## Measures (descriptive)

1. The number of distinct US states (plus the District of Columbia) with at least one site of any of these trials, and the number of distinct cities.
2. For each state, the number of these trials with a site there.
3. The number of trials with sites in 5 or more states, against those with sites in only one or two.
4. The states with no site.

## Predictions, recorded before the data

In `PREDICTIONS.md`:
- **P52:** fewer than half of the 50 states plus DC (that is, 25 or fewer) have a site of any of these trials (55%).
- **P53:** at least one trial has sites in 20 or more states (60%). Children's Oncology Group trials run at many centres (general knowledge).

## Limits stated in advance

- Registry site lists can be out of date, and a listed site may not be open to new patients.
- Travel distance is not computed; states are a rough proxy.
- This is a description for advocates and families to discuss with care teams, not a guide to any trial.

## Deviations

*None yet.*
