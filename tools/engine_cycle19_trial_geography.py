#!/usr/bin/env python3
"""Engine cycle 19: where in the United States can a teenager with relapsed osteosarcoma reach a trial?

Pre-registered in research_notes/Engine/cycle-19-trial-geography/PREREGISTRATION.md (commit 1b53b9a).
Reuses engine cycle 12's saved records and corrected classification. Reads country, state, city and site status only.

Outputs: data/engine/cycle19/states.csv, trials.csv, results.json
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C12 = os.path.join(ROOT, "data", "engine", "cycle12")
OUT = os.path.join(ROOT, "data", "engine", "cycle19")
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida",
          "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
          "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
          "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
CLOSED = {"WITHDRAWN", "COMPLETED", "TERMINATED"}


def main():
    os.makedirs(OUT, exist_ok=True)
    a = {r["nct"]: r for r in csv.DictReader(open(os.path.join(C12, "set_a.csv")))}
    hand = {r["nct"]: r for r in csv.DictReader(open(os.path.join(C12, "hand_classification.csv")))}
    chosen = [n for n, h in hand.items() if h["hand_relapse_eligible"] == "yes" and h["treatment_trial"] == "yes"
              and a[n]["accepts_teenagers"] == "True" and a[n]["us_site"] == "True"]
    raw = {s["protocolSection"]["identificationModule"]["nctId"]: s for s in json.load(open(os.path.join(C12, "raw", "set_A.json")))["studies"]}
    per_trial, per_state, cities, unknown_state = {}, {st: set() for st in STATES}, set(), 0
    for n in chosen:
        locs = raw[n]["protocolSection"].get("contactsLocationsModule", {}).get("locations", [])
        sts = set()
        for l in locs:
            if l.get("country") != "United States" or str(l.get("status", "")).upper() in CLOSED:
                continue
            st = l.get("state")
            if st in per_state:
                sts.add(st)
                per_state[st].add(n)
                cities.add((l.get("city", ""), st))
            else:
                unknown_state += 1
        per_trial[n] = sorted(sts)
    covered = [st for st in STATES if per_state[st]]
    S = {"preregistration_commit": "1b53b9a", "trials": len(chosen), "trials_with_open_us_site": sum(1 for v in per_trial.values() if v),
         "states_and_dc_with_site": len(covered), "of": len(STATES), "cities": len(cities), "us_sites_without_recognised_state": unknown_state,
         "states_without_site": [st for st in STATES if not per_state[st]],
         "trials_5_plus_states": sum(1 for v in per_trial.values() if len(v) >= 5),
         "trials_1_or_2_states": sum(1 for v in per_trial.values() if 1 <= len(v) <= 2),
         "max_states_and_dc_one_trial": max((len(v) for v in per_trial.values()), default=0),
         "trials_20_plus_states_and_dc": sum(1 for v in per_trial.values() if len(v) >= 20)}
    S["P52"] = "right" if S["states_and_dc_with_site"] <= 25 else "wrong"
    S["P53"] = "right" if S["trials_20_plus_states_and_dc"] >= 1 else "wrong"
    json.dump(S, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    with open(os.path.join(OUT, "states.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state", "trials_with_a_site"])
        for st in sorted(STATES, key=lambda s: (-len(per_state[s]), s)):
            w.writerow([st, len(per_state[st])])
    with open(os.path.join(OUT, "trials.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nct", "title", "sponsor_class", "states_and_dc_with_site", "states"])
        for n in sorted(chosen, key=lambda n: -len(per_trial[n])):
            w.writerow([n, a[n]["title"], a[n]["sponsor_class"], len(per_trial[n]), "; ".join(per_trial[n])])
    print(json.dumps(S, indent=1))
    print([(st, len(per_state[st])) for st in sorted(STATES, key=lambda s: -len(per_state[s]))[:12]])
    print([(n, len(v)) for n, v in sorted(per_trial.items(), key=lambda x: -len(x[1]))[:8]])


if __name__ == "__main__":
    main()
