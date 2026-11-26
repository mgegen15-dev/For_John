# Engine cycle 12: across the whole trial registry, how often can a teenager with osteosarcoma get into a drug trial?

*Pre-registered November 26, 2026, before the registry was searched for this cycle. This file is committed to git before the search; its commit time is the evidence of order. Any change after that commit is listed under "Deviations" with a reason.*

## Why this question

Cycles 4 and 7 found that, of 34 targeted-drug trials an osteosarcoma patient with MTAP loss or CCNE1 amplification could join on paper, two accepted anyone under 18 (`briefs/Brief - trial access for teenagers with osteosarcoma.md`). That covered two drug classes. This cycle asks the same question across the whole registry:

- Do the trials that name osteosarcoma take teenagers?
- How often do the broad "any solid tumour" trials, where most new drugs first enter people, take anyone under 18?
- Who runs the ones that do?

Osteosarcoma is most often diagnosed in teenagers (general knowledge).

## Data

ClinicalTrials.gov API v2, searched once on the day of the run. Raw records stay out of git because they include trial staff contact details. Published tables carry the registry number, title, phase, status, age limits, sponsor type, countries and the classifications below.

## Sets

Common filters for both sets:
- Interventional.
- Status "Recruiting" or "Not yet recruiting".
- At least one intervention of type Drug, Biological or Genetic. This covers small molecules, antibodies, antibody–drug conjugates, radioligands, vaccines and cell therapies.

**Set A, trials that name osteosarcoma.**
- Found by the registry's condition search for "osteosarcoma", and kept only if "osteosarcoma" appears in the conditions, keywords, titles or eligibility text. This drops trials the registry's synonym expansion pulls in without mentioning osteosarcoma.
- **Relapse-eligible:** each Set A trial is flagged as open to relapsed disease if its titles, conditions or eligibility text contain any of: relapse, relapsed, recurrent, recurrence, refractory, progressive, progression, metastatic, "previously treated", "prior therapy", advanced, unresectable. Otherwise it is flagged frontline or other.
- **Hand check:** a random sample of 30 Set A trials (random seed 12) is read by hand to estimate how often this text rule is wrong. The rule's result is reported whatever the check shows, with the check alongside.

**Set B, early-phase "solid tumour" trials.**
- Found by the registry's condition search for "solid tumor", kept only if a condition contains "solid tumor", "solid tumour" or "solid neoplasm".
- Restricted to phase 1, phase 1/2, early phase 1 or phase 2.
- Trials already in Set A are removed.
- These are the broad trials where new drugs are first given to people. Whether a given trial would accept osteosarcoma is not read here, because many exclude particular cancers in text this cycle does not classify. Set B describes the age limits of the trials themselves, not osteosarcoma eligibility.

## Definitions

- **Accepts teenagers:** the minimum age is 17 years or younger, or no minimum age is given, and the maximum age, if any, is 12 or older. A trial with no stated minimum age is counted as accepting and flagged.
- **Sponsor type:** the registry's lead-sponsor class. "Industry" means a company. Everything else (universities, hospitals, cooperative groups, the US National Institutes of Health, other) is "academic or other".
- **US site:** at least one location in the United States.

## Measures (descriptive counts with 95% Wilson intervals)

1. Set A, relapse-eligible: number of trials and share that accept teenagers; the same with a US site.
2. Set B: number of trials and share that accept teenagers; the same with a US site.
3. Set B trials that accept teenagers: share with an industry lead sponsor, against the share of all Set B trials with an industry lead sponsor.
4. The age floors in Set B, in four bands: under 12, 12 to 17, 18, over 18.

## Predictions, recorded before the search

In `PREDICTIONS.md`:
- **P35:** fewer than 10% of Set B trials accept teenagers (65%).
- **P36:** at least half of Set A relapse-eligible trials accept teenagers (75%).
- **P37:** among Set B trials that accept teenagers, the share with an industry lead sponsor is lower than among all Set B trials (80%).

## What happens next

The counts go into the trial-access brief as a wider frame, if they hold up. If Set A trials that take teenagers with relapsed disease are few, the brief's ask widens from two drug classes to early-phase trials generally.

## Deviations

Recorded November 26, 2026, after the run.

1. **Phase filter.** The code kept any trial with an early phase among its phases, so 16 phase 2/3 trials entered Set B. Without them: 72 of 1,418 accept teenagers. Reported in the cycle report.
2. **Full reading of Set A.** All 72 trials were classified by reading each record, beyond the planned sample of 30. One error found by an independent check was corrected (NCT07477457).
