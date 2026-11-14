"""For every finished interventional osteosarcoma trial (completed, terminated
or status unknown), search Europe PMC (abstracts and full text, including
PubMed) for its NCT number, to find trials whose results were never published.
Writes data/osteosarcoma_trials_publications.csv."""
import csv, json, time, urllib.parse, urllib.request

R = [r for r in csv.DictReader(open("data/osteosarcoma_trials.csv"))
     if r["study_type"] == "INTERVENTIONAL" and r["status"] in ("COMPLETED", "TERMINATED", "UNKNOWN")]
EP = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&pageSize=5&query="

with open("data/osteosarcoma_trials_publications.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["nct_id", "status", "phase", "scope", "enrollment", "completion", "has_results",
                "papers_citing_nct", "first_paper", "title"])
    for i, r in enumerate(R):
        for a in range(4):
            try:
                d = json.load(urllib.request.urlopen(EP + urllib.parse.quote(f'"{r["nct_id"]}"'), timeout=60)); break
            except Exception:
                time.sleep(3 * (a + 1))
        else:
            d = {"hitCount": -1, "resultList": {"result": []}}
        res = d["resultList"]["result"]
        first = f'{res[0].get("pmid") or res[0].get("id")} {res[0].get("title","")[:90]}' if res else ""
        w.writerow([r["nct_id"], r["status"], r["phase"], r["scope"], r["enrollment"], r["completion"],
                    r["has_results"], d["hitCount"], first, r["title"]])
        time.sleep(0.25)
print(len(R), "trials checked")
