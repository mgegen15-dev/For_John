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
# Patients in stopped trials. Terminated trials usually report ACTUAL enrolment;
# suspended trials report the PLANNED (estimated) number; withdrawn trials enrolled 0.
# Report these separately rather than as one sum.
def _n(r): return int(r["enrollment"] or 0)
pst = {}
for st in ("TERMINATED", "SUSPENDED", "WITHDRAWN"):
    g = [r for r in stopped if r["status"] == st]
    pst[st.lower()] = {
        "trials": len(g),
        "patients_total": sum(_n(r) for r in g),
        "patients_actual": sum(_n(r) for r in g if r["enrollment_type"] == "ACTUAL"),
        "trials_with_actual": sum(r["enrollment_type"] == "ACTUAL" for r in g),
        "patients_estimated": sum(_n(r) for r in g if r["enrollment_type"] != "ACTUAL"),
        "trials_with_estimated": sum(r["enrollment_type"] != "ACTUAL" for r in g),
    }
out["patients_in_stopped_trials"] = pst

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
    by[dec]["bone_sarcoma"] += r["scope"] == "bone_sarcoma"
    by[dec]["china"] += "China" in r["countries"]
    by[dec]["us"] += "United States" in r["countries"]
out["by_period"] = {k: dict(v) for k, v in sorted(by.items())}

# drugs: how often each drug appears in osteosarcoma-only interventional trials
def drugs(r):
    return {re.sub(r"\s+", " ", n.split(":", 1)[1]).strip().lower()
            for n in r["interventions"].split(" | ") if n.startswith(("DRUG", "BIOLOGICAL"))}
dc = C.Counter(d for r in IV if r["scope"] == "os_only" for d in drugs(r))
out["drug_mentions_os_only_top"] = dc.most_common(40)

# primary endpoints in osteosarcoma-only phase 2+.
# A trial counts once for EVERY endpoint type its primary outcomes name, so the
# columns do not sum to the number of trials. "other" = names none of the types.
EP_TYPES = [
    ("event-free / progression-free survival", r"events?.free|progress(ion)?.free|\bpfs\b|\befs\b|disease.free|relapse.free"),
    ("overall survival", r"overall survival|\bos rate\b|(?<!free )\bsurvival rate"),
    ("response rate", r"response|\borr\b|recist"),
    ("toxicity / safety", r"toxic|adverse|safety|dose"),
]
ep, ep_sole = C.Counter(), C.Counter()
ep_trials = C.defaultdict(list)
n_ep = 0
for r in IV:
    if r["scope"] != "os_only" or not re.search(r"PHASE2|PHASE3", r["phase"]): continue
    n_ep += 1
    t = r["primary_outcomes"].lower()
    hit = [name for name, pat in EP_TYPES if re.search(pat, t)] or ["other"]
    for h in hit:
        ep[h] += 1
        ep_trials[h].append(r["nct_id"])
    if len(hit) == 1: ep_sole[hit[0]] += 1
out["primary_endpoints_os_only_phase2plus"] = {"trials": n_ep, "any_mention": ep.most_common(),
                                               "sole_type": ep_sole.most_common(),
                                               "overall_survival_trials": ep_trials["overall survival"]}

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
