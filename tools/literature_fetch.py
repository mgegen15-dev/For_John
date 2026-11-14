"""Fetch every PubMed paper with 'osteosarcoma' in title/abstract, with
PubTator3 gene and chemical annotations, and save one JSON line per paper
(data/literature/osteosarcoma_pubtator.jsonl, git-ignored because of size)
plus PMID lists of reviews and retracted papers.

Usage: python3 tools/literature_fetch.py"""
import json, os, time, urllib.parse, urllib.request

EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PT = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?pmids="
OUT = "data/literature"
os.makedirs(OUT, exist_ok=True)


def get(url, tries=5):
    for a in range(tries):
        try:
            return urllib.request.urlopen(url, timeout=180).read()
        except Exception:
            time.sleep(5 * (a + 1))
    raise RuntimeError(url)


def esearch(term):
    ids = []
    for y0, y1 in [(1900, 1999), (2000, 2009), (2010, 2014), (2015, 2017), (2018, 2019), (2020, 2020),
                   (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2027)]:
        q = {"db": "pubmed", "term": f"({term}) AND {y0}:{y1}[dp]", "retmax": 9999, "retmode": "json"}
        d = json.loads(get(EU + "?" + urllib.parse.urlencode(q)))["esearchresult"]
        assert int(d["count"]) <= 9999, (y0, y1, d["count"])
        ids += d["idlist"]
        time.sleep(0.4)
    return ids


base = "osteosarcoma[tiab]"
pmids = list(dict.fromkeys(esearch(base)))  # de-duplicate (overlapping year windows)
for name, extra in [("reviews", "review[pt]"), ("retracted", "retracted publication[pt]")]:
    with open(f"{OUT}/osteosarcoma_{name}_pmids.txt", "w") as f:
        # The year windows above can overlap at their edges for papers with two
        # publication dates (print and electronic), so de-duplicate before writing.
        f.write("\n".join(sorted(set(esearch(f"{base} AND {extra}")), key=int)) + "\n")
print(len(pmids), "papers")

done = set()
path = f"{OUT}/osteosarcoma_pubtator.jsonl"
if os.path.exists(path):
    done = {json.loads(l)["pmid"] for l in open(path)}
todo = [p for p in pmids if p not in done]
with open(path, "a") as f:
    for i in range(0, len(todo), 100):
        batch = todo[i:i + 100]
        raw = get(PT + ",".join(batch)).decode()
        try:
            docs = json.loads(raw)
            docs = docs.get("PubTator3", docs) if isinstance(docs, dict) else docs
        except json.JSONDecodeError:
            docs = [json.loads(l) for l in raw.splitlines() if l.strip()]
        for d in docs:
            title = abstract = ""
            genes, chems, species = [], [], []
            year = None
            for p in d.get("passages", []):
                ty = p.get("infons", {}).get("type", "")
                if ty == "title":
                    title = p.get("text", "")
                    year = p.get("infons", {}).get("year") or year
                elif ty == "abstract":
                    abstract += p.get("text", "")
                for a in p.get("annotations", []):
                    inf = a.get("infons", {})
                    t = inf.get("type")
                    if t == "Gene":
                        genes.append([inf.get("identifier"), a.get("text"), inf.get("name") or ""])
                    elif t == "Chemical":
                        chems.append([inf.get("identifier"), a.get("text")])
                    elif t == "Species":
                        species.append(inf.get("identifier"))
            f.write(json.dumps({"pmid": str(d.get("id") or d.get("pmid")), "year": year or d.get("year"),
                                "journal": d.get("journal", ""), "title": title, "abstract": abstract,
                                "genes": genes, "chemicals": chems, "species": sorted(set(filter(None, species)))}) + "\n")
        if i % 2000 == 0:
            print(f"{i + len(batch)}/{len(todo)}", flush=True)
        time.sleep(0.4)
print("done")
