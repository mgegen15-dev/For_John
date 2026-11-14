"""Re-tag the `scope` column of data/osteosarcoma_trials.csv from its own
`conditions` column, using the same rule as tools/trial_miner.py
(`scope_for`): os_only / bone_sarcoma / basket. No download needed.

Prints how many trials changed tag and lists them, then rewrites the CSV in
place (same columns, same row order).

Usage: python3 tools/retag_trial_scope.py [--dry-run]   (run from the repo root)
"""
import csv, sys, collections as C
sys.path.insert(0, "tools")
from trial_miner import scope_for

PATH = "data/osteosarcoma_trials.csv"


def main(dry=False):
    with open(PATH, newline="") as f:
        rd = csv.DictReader(f)
        fields, rows = rd.fieldnames, list(rd)
    moves = C.Counter()
    changed = []
    for r in rows:
        new = scope_for(r["conditions"].split("; "))
        if new != r["scope"]:
            changed.append((r["nct_id"], r["scope"], new, r["study_type"], r["allocation"], r["conditions"]))
            moves[(r["scope"], new)] += 1
            r["scope"] = new
    print("scope counts:", dict(C.Counter(r["scope"] for r in rows)))
    print("changes:", {f"{a} -> {b}": n for (a, b), n in moves.items()})
    for c in changed:
        print(" ", " | ".join(c))
    if not dry:
        with open(PATH, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"rewrote {PATH}")


if __name__ == "__main__":
    main(dry="--dry-run" in sys.argv)
