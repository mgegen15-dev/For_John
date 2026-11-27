# Engine cycle 19: where in the United States can a teenager with relapsed osteosarcoma reach a trial?

*Run November 27, 2026. The nineteenth cycle of the For John research engine. Pre-registration: `research_notes/Engine/cycle-19-trial-geography/PREREGISTRATION.md`, committed at commit `1b53b9a` before any site location was read. Script: `tools/engine_cycle19_trial_geography.py`. Results: `data/engine/cycle19/`. Uses the ClinicalTrials.gov records saved by engine cycle 12 on November 26, 2026. A description for families and advocates to discuss with care teams; not a guide to any trial, and not medical advice.*

## Summary

Cycle 12 found 32 recruiting or soon-to-recruit drug trials that list osteosarcoma, take relapsed disease, accept 12- to 17-year-olds and have a US site. This cycle counted where those sites are, using only the state and city of each site that is not marked closed.

- **33 states and DC (34 of 51) have at least one site** (66 cities). The count includes sites the registry marks as suspended or not recruiting; only withdrawn, completed and terminated sites were left out, as planned.
- **17 states have none:** Alaska, Delaware, Idaho, Iowa, Louisiana, Maine, Mississippi, Montana, Nebraska, Nevada, New Hampshire, New Mexico, North Dakota, South Dakota, Vermont, West Virginia and Wyoming. Teenagers in those states would have to travel to another state for any of these trials.
- **Most trials are in few places.** 20 of the 32 have sites in only one or two states. 7 have sites in five or more. One, a US National Cancer Institute–sponsored trial of the antibody–drug conjugate DS-8201a (trastuzumab deruxtecan) for recurrent osteosarcoma and other tumours in young people (NCT04616560), lists sites in 22 states, though in 5 of them (Alabama, Colorado, Indiana, Minnesota, Utah) the registry marks every site as suspended or not recruiting; its recruiting sites are in 17 states.
- **The states with the most of these trials:**
  - Texas: 13 of the 32;
  - California: 9;
  - New York and Tennessee: 8 each;
  - Ohio and Pennsylvania: 7 each.
- **Predictions:** P52 (25 or fewer states) was wrong, since 33 states and DC (34 of 51) have a site. P53 (at least one trial in 20 or more states) was right by its rule; counting only sites marked recruiting or not yet recruiting, no trial reaches 20 states.

**How to read the labels.** Every number here is **(our calculation)** from **(registry)** records.

## What this means

- **For families:** relapse trials that take teenagers exist in most states, but each trial is usually at one or a few hospitals. The registry's location list and the care team are the place to check. Children's cancer centres can often refer patients across state lines (general knowledge).
- **For advocates:** the trial with the widest reach is sponsored by the National Cancer Institute. Trials run at one or two centres concentrate access in a few cities. Travel cost is a real barrier for families, and help with it is an advocacy question.

## Limits

- Registry site lists can be out of date, and a listed site may not be taking new patients.
- States are a rough stand-in for travel distance.
- Each trial has its own further entry rules.
- Only ClinicalTrials.gov was searched, on one day.

## Files and reproduction

- `python3 tools/engine_cycle19_trial_geography.py` runs in seconds after cycle 12's registry download.
- Outputs:
  - `data/engine/cycle19/states.csv` (trials per state);
  - `data/engine/cycle19/trials.csv` (states per trial);
  - `data/engine/cycle19/results.json`.
- No contact details are read or published.

**Data source.** ClinicalTrials.gov API v2 (US National Library of Medicine).

## Change log

- 2026-11-27: after an independent check, suspended and not-recruiting sites made explicit; the 22-state trial recruits in 17.
- 2026-11-27: cycle run and reported. P52 wrong, P53 right. No deviations.
