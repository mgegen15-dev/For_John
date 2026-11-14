"""Build a first pooled control dataset: arm-level efficacy outcomes posted
on ClinicalTrials.gov by osteosarcoma trials (data/osteosarcoma_trials.csv
rows with has_results=True). Writes data/osteosarcoma_posted_outcomes.csv,
one row per trial x outcome x arm (and category, where an outcome is split).

`os_arm` marks arms whose title names osteosarcoma, or arms of trials that
enrol only osteosarcoma; basket-trial arms that mix cancers are kept but
flagged so they can be excluded."""
import csv, json, re, time, urllib.request

EFF = re.compile(r"event.free|progression.free|disease.free|relapse.free|overall survival|survival|"
                 r"response|remission|disease control|progression|recurrence|relapse|efs|pfs|orr|"
                 r"necrosis|histolog", re.I)
SKIP = re.compile(r"pharmacokin|concentration|half.life|t ?1/2|auc|cmax|clearance|toxicit|adverse|"
                  r"tolerab|dose.limiting|maximum tolerated|quality of life|pain", re.I)
OS = re.compile(r"osteosarcoma|osteogenic", re.I)


def setting(text):
    t = text.lower()
    if re.search(r"newly diagnosed|front.?line|first.?line|upfront|localized|non.?metastatic", t): return "newly diagnosed"
    if re.search(r"recurren|relaps|refractory|progressive", t): return "relapsed/refractory"
    if re.search(r"metasta|advanced", t): return "advanced/metastatic"
    return "unclear"


trials = [r for r in csv.DictReader(open("data/osteosarcoma_trials.csv"))
          if r["has_results"] == "True" and r["study_type"] == "INTERVENTIONAL"]
out = []
for t in trials:
    for a in range(4):
        try:
            d = json.load(urllib.request.urlopen(
                f"https://clinicaltrials.gov/api/v2/studies/{t['nct_id']}", timeout=120)); break
        except Exception:
            time.sleep(3 * (a + 1))
    else:
        continue
    for o in d.get("resultsSection", {}).get("outcomeMeasuresModule", {}).get("outcomeMeasures", []):
        name = f"{o.get('title','')} {o.get('description','')}"
        if not EFF.search(name) or SKIP.search(o.get("title", "")):
            continue
        groups = {g["id"]: g for g in o.get("groups", [])}
        denom = {}
        for dn in o.get("denoms", []):
            if dn.get("units", "").lower().startswith("particip"):
                denom = {c["groupId"]: c["value"] for c in dn.get("counts", [])}
        for cl in o.get("classes", []) or [{}]:
            for cat in cl.get("categories", []) or [{}]:
                for m in cat.get("measurements", []):
                    g = groups.get(m["groupId"], {})
                    gtxt = f"{g.get('title','')} {g.get('description','')}"
                    out.append({
                        "nct_id": t["nct_id"], "trial_title": t["title"], "phase": t["phase"],
                        "allocation": t["allocation"], "trial_scope": t["scope"],
                        "setting": setting(t["title"] + " " + t["conditions"]),
                        "outcome_type": o.get("type"), "outcome": o.get("title", ""),
                        "time_frame": o.get("timeFrame", ""), "param_type": o.get("paramType", ""),
                        "unit": o.get("unitOfMeasure", ""), "class": cl.get("title", ""),
                        "category": cat.get("title", ""), "arm": g.get("title", ""),
                        "os_arm": bool(OS.search(gtxt)) or t["scope"] == "os_only",
                        "n_analyzed": denom.get(m["groupId"], ""), "value": m.get("value", ""),
                        "lower": m.get("lowerLimit", ""), "upper": m.get("upperLimit", ""),
                        "arm_description": g.get("description", "")[:300],
                    })
    time.sleep(0.3)
with open("data/osteosarcoma_posted_outcomes.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)
print(len(trials), "trials with results;", len(out), "efficacy rows;",
      len({r["nct_id"] for r in out}), "trials with efficacy outcomes;",
      len({r["nct_id"] for r in out if r["os_arm"]}), "with osteosarcoma-specific arms")
