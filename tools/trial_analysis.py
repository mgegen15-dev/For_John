"""Analyse data/osteosarcoma_trials.csv (from trial_miner.py) for patterns,
gaps and inconsistencies. Prints a JSON blob of the main tables and writes
data/osteosarcoma_trials_flags.csv listing every flagged trial and why."""
import csv, json, re, collections as C

R = list(csv.DictReader(open("data/osteosarcoma_trials.csv")))
IV = [r for r in R if r["study_type"] == "INTERVENTIONAL"]
yr = lambda d: int(d[:4]) if d[:4].isdigit() else None


def stop_reason(t):
    t = t.lower()
    if not t.strip(): return "No reason given"
    if re.search(r"accru|enrol|recruit|screening", t): return "Poor recruitment"
    if re.search(r"business|strateg|sponsor|corporate|reprior|portfolio|rights|program|funding|fund", t): return "Business or funding decision"
    if re.search(r"supply|ind |ind$|not available|manufacturer", t): return "Drug supply or IND withdrawn"
    if re.search(r"efficacy|benefit|stopping rule|expectations|lackluster|primary objective", t): return "Lack of efficacy"
    if re.search(r"toxic|safety", t): return "Safety review"
    if re.search(r"covid", t): return "COVID-19"
    return "Other"


out = {}
stopped = [r for r in IV if r["status"] in ("TERMINATED", "WITHDRAWN", "SUSPENDED")]
out["stop_reasons"] = C.Counter(stop_reason(r["why_stopped"]) for r in stopped).most_common()
out["patients_in_stopped_trials"] = sum(int(r["enrollment"] or 0) for r in stopped)

# results posting: completed, phase 2+, at least one US site, completed 2018 or later
def needs_results(r):
    return (r["status"] == "COMPLETED" and re.search(r"PHASE2|PHASE3|PHASE4", r["phase"])
            and "United States" in r["countries"] and (yr(r["completion"]) or 0) >= 2018)
due = [r for r in IV if needs_results(r)]
out["us_phase2plus_completed_2018on"] = len(due)
out["of_which_no_results"] = sum(r["has_results"] != "True" for r in due)

# stale records: status unknown
out["status_unknown"] = sum(r["status"] == "UNKNOWN" for r in IV)

# design by decade, osteosarcoma-only
by = C.defaultdict(lambda: C.Counter())
for r in IV:
    y = yr(r["start"])
    if not y: continue
    dec = f"{y//5*5}-{y//5*5+4}"
    by[dec]["all"] += 1
    by[dec]["os_only"] += r["scope"] == "os_only"
    by[dec]["randomized_os_only"] += r["scope"] == "os_only" and r["allocation"] == "RANDOMIZED"
    by[dec]["china"] += "China" in r["countries"]
    by[dec]["us"] += "United States" in r["countries"]
out["by_period"] = {k: dict(v) for k, v in sorted(by.items())}

# drugs: how often each drug appears in osteosarcoma-only interventional trials
def drugs(r):
    return {re.sub(r"\s+", " ", n.split(":", 1)[1]).strip().lower()
            for n in r["interventions"].split(" | ") if n.startswith(("DRUG", "BIOLOGICAL"))}
dc = C.Counter(d for r in IV if r["scope"] == "os_only" for d in drugs(r))
out["drug_mentions_os_only_top"] = dc.most_common(40)

# primary endpoints in osteosarcoma-only phase 2+
ep = C.Counter()
for r in IV:
    if r["scope"] != "os_only" or not re.search(r"PHASE2|PHASE3", r["phase"]): continue
    t = r["primary_outcomes"].lower()
    ep["event-free / progression-free survival" if re.search(r"event.free|progression.free|pfs|efs|disease.free|relapse.free", t)
       else "overall survival" if re.search(r"overall survival", t)
       else "response rate" if re.search(r"response|orr|recist", t)
       else "toxicity / safety" if re.search(r"toxic|adverse|safety|dose", t)
       else "other"] += 1
out["primary_endpoints_os_only_phase2plus"] = ep.most_common()

flags = []
for r in IV:
    if r in stopped: flags.append((r, "stopped: " + stop_reason(r["why_stopped"])))
    if needs_results(r) and r["has_results"] != "True": flags.append((r, "completed US phase 2+ trial, no results posted"))
    if r["status"] == "UNKNOWN": flags.append((r, "status unknown (record not updated)"))
with open("data/osteosarcoma_trials_flags.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["nct_id", "flag", "status", "phase", "enrollment", "sponsor", "last_update", "title"])
    for r, why in flags:
        w.writerow([r["nct_id"], why, r["status"], r["phase"], r["enrollment"], r["sponsor"], r["last_update"], r["title"]])
out["flags_written"] = len(flags)
print(json.dumps(out, indent=1))
