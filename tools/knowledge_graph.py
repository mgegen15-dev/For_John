"""Literature knowledge graph for osteosarcoma: contradictions and hidden links.

The systematic version of "connecting the dots". It builds a graph from the
33,242-paper osteosarcoma corpus (tools/literature_fetch.py), then looks for
  (a) contradictions: a gene or drug reported to push an outcome (metastasis,
      proliferation, ...) up in some papers and down in others, and
  (b) hidden links (Swanson-style A -> B -> C): an approved drug A acts on a
      gene B (broad literature, any disease), B moves an osteosarcoma outcome C
      (this corpus), and no osteosarcoma paper links A to C directly.

Run from the repository root (standard library only):
  python3 tools/knowledge_graph.py fetch      # PubTator3 relations, ~25 min, resumable
  python3 tools/knowledge_graph.py build      # graph + contradictions (offline)
  python3 tools/knowledge_graph.py abc        # hidden links (queries PubTator3 + PubMed, cached)
  python3 tools/knowledge_graph.py all        # all three in order

Inputs
  data/literature/osteosarcoma_pubtator.jsonl  titles, abstracts, PubTator gene and
      chemical mentions (duplicate PMIDs are dropped, first copy kept)
  data/osteosarcoma_paper_tags.csv             retracted, review, ncrna, in_vivo, patients, dog
  data/osteosarcoma_repurposing_candidates.csv approved-drug -> target gene mappings (ChEMBL-derived)
  tools/literature_map.py                      the PubTator gene-symbol correction table (imported
                                               textually: CORRECTIONS / ALIAS / symbol())
Caches (git-ignored)
  data/literature/pubtator_relations.jsonl     one line per PMID: PubTator3 document-level relations
  data/literature/kg_abc_cache.json            PubTator3 search + PubMed counts for the ABC step
Outputs
  data/osteosarcoma_knowledge_graph_edges.csv  one row per (source, target, direction, relation, evidence layer)
  data/osteosarcoma_contradictions.csv         gene/drug -> outcome pairs reported in both directions
  data/osteosarcoma_hidden_links.csv           drug -> gene -> outcome chains with no direct OS paper

Two evidence layers (column `layer` in the edge file)
  pubtator   PubTator3's own relation extraction (BioREx model), document level. Types:
             Positive_Correlation, Negative_Correlation, Association, Bind, Cotreatment,
             Drug_Interaction, Comparison, Conversion. (The task brief's inhibit/stimulate/treat/
             cause/prevent labels are the older BioRED/CTD names; PubTator3 returns the eight
             above, so "inhibit" appears as Negative_Correlation, etc.) Outcome nodes come from
             disease entities PubTator links, e.g. "Neoplasm Metastasis".
  sentence   our own rule-based extraction, needed because PubTator does not tag outcomes
             such as proliferation, apoptosis or chemoresistance. Within one sentence that
             names a gene or chemical and an outcome keyword, a trigger word sets direction:
             increase triggers (promot*, enhanc*, increas*, induc*, activat*, facilitat*,
             stimulat*, drive*, upregulat*, accelerat*, contribut*) = +1; decrease triggers
             (inhibit*, suppress*, reduc*, decreas*, attenuat*, block*, impair*, abolish*,
             abrogat*, prevent*, repress*, downregulat*, diminish*, restrain*) = -1. A negation
             or knockdown word before the gene flips the sign ("knockdown of X inhibited
             metastasis" => X promotes metastasis). Sentences with both or neither trigger are
             skipped. This is crude; see the report's limits.

Evidence weight per paper (column `weight`; summed per edge)
  base 1.0; x1.5 if in vivo, x1.5 if patient data, x1.5 if dog; x0.5 if microRNA-type
  (ncrna) paper; x0.5 if review; retracted papers are excluded entirely; sentence-layer
  edges in the title count x1.5 (titles state the main finding).
"""
import csv, json, os, re, sys, time, urllib.parse, urllib.request, collections as C

L = "data/literature/"
CORPUS = L + "osteosarcoma_pubtator.jsonl"
REL_CACHE = L + "pubtator_relations.jsonl"
ABC_CACHE = L + "kg_abc_cache.json"
PT_EXPORT = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?full=false&pmids="
PT_SEARCH = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/search/?"
PT_REL = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/relations?"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
UA = {"User-Agent": "open-science-literature-graph/1.0"}
DELAY = 0.4


def get(url, tries=5, timeout=180):
    """GET with retries and back-off; returns bytes."""
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:  # network errors, 429, 5xx
            err = e
            time.sleep(5 * (a + 1))
    raise RuntimeError(f"{url}: {err}")


def corpus_pmids():
    seen = []
    s = set()
    for line in open(CORPUS):
        p = json.loads(line)["pmid"]
        if p not in s:
            s.add(p); seen.append(p)
    return seen


def _ent(role):
    return {"type": role.get("type"), "id": str(role.get("identifier")), "name": role.get("name")}


def fetch_relations():
    """Download PubTator3 relations for every corpus PMID (resumable cache)."""
    pmids = corpus_pmids()
    done = set()
    if os.path.exists(REL_CACHE):
        done = {json.loads(l)["pmid"] for l in open(REL_CACHE)}
    todo = [p for p in pmids if p not in done]
    print(f"{len(pmids)} unique PMIDs, {len(done)} cached, {len(todo)} to fetch", flush=True)
    with open(REL_CACHE, "a") as f:
        for i in range(0, len(todo), 100):
            batch = todo[i:i + 100]
            raw = get(PT_EXPORT + ",".join(batch)).decode()
            try:
                d = json.loads(raw)
                docs = d.get("PubTator3", []) if isinstance(d, dict) else d
            except json.JSONDecodeError:
                docs = [json.loads(l) for l in raw.splitlines() if l.strip()]
            got = set()
            for doc in docs:
                p = str(doc.get("pmid") or doc.get("id"))
                if p not in batch or p in got:  # PubTator occasionally returns an unrequested doc
                    continue
                got.add(p)
                rels = []
                for r in doc.get("relations", []):
                    inf = r.get("infons", {})
                    if "role1" not in inf or "role2" not in inf:
                        continue
                    rels.append({"type": inf.get("type"), "score": inf.get("score"),
                                 "e1": _ent(inf["role1"]), "e2": _ent(inf["role2"])})
                f.write(json.dumps({"pmid": p, "relations": rels}) + "\n")
            for p in batch:
                if p not in got:
                    f.write(json.dumps({"pmid": p, "relations": [], "missing": True}) + "\n")
            f.flush()
            if (i // 100) % 20 == 0:
                print(f"  {i + len(batch)}/{len(todo)}", flush=True)
            time.sleep(DELAY)



# ---------------------------------------------------------------- shared inputs
def load_corrections():
    """Re-use the PubTator gene-symbol correction table from tools/literature_map.py.

    literature_map.py is a script (it runs on import), so the CORRECTIONS and ALIAS
    literals are read from its source text instead of importing it."""
    src = open("tools/literature_map.py").read()
    alias = eval(re.search(r"^ALIAS = (\{.*?\})$", src, re.M).group(1))
    block = re.search(r"^CORRECTIONS = (\[\n.*?\n\])$", src, re.M | re.S).group(1)
    corr = [(a, re.compile(b), c) for a, b, c in eval(block)]
    return alias, corr


ALIAS, CORRECTIONS = load_corrections()


def gene_symbol(sym, mention):
    """Corrected symbol for a PubTator gene (symbol, mention text); '' means drop."""
    s = ALIAS.get((sym or "").upper(), (sym or "").upper())
    m = (mention or "").lower().strip()
    for a, pat, new in CORRECTIONS:
        if s == a and pat.search(m):
            return new or ""
    return s


def load_tags():
    tags = {}
    for r in csv.DictReader(open("data/osteosarcoma_paper_tags.csv")):
        t = {k: r[k] == "True" for k in ("retracted", "review", "ncrna", "in_vivo", "patients", "dog", "cell_only")}
        t["year"] = int(r["year"]) if r["year"].isdigit() else None
        tags[r["pmid"]] = t
    return tags


def paper_weight(t):
    """Evidence-quality weight of one paper (0 for retracted)."""
    if t["retracted"]:
        return 0.0
    w = 1.0
    for k in ("in_vivo", "patients", "dog"):
        if t[k]:
            w *= 1.5
    if t["ncrna"]:
        w *= 0.5
    if t["review"]:
        w *= 0.5
    return w


def load_corpus():
    """De-duplicated corpus: {pmid: record}, first copy of each PMID kept."""
    docs = {}
    for line in open(CORPUS):
        d = json.loads(line)
        docs.setdefault(d["pmid"], d)
    return docs


# ---------------------------------------------------------------- outcome concepts
# Each outcome is named so that +1 means "more of it". For "poor_prognosis", +1 means
# the entity goes with worse survival. Patterns with polarity -1 name the opposite
# ("chemosensitivity" = less chemoresistance).
OUTCOMES = {
    "metastasis": [(r"metasta\w*|invasi(?:on|ve(?:ness)?)|migrat\w*", 1)],
    "proliferation": [(r"proliferat\w*|tumou?r growth|cell growth|(?:cell )?viability|colony formation|"
                       r"clonogenic\w*|tumou?rigen\w*|xenograft growth|tumou?r volume", 1)],
    "apoptosis": [(r"apoptos[ie]s|apoptotic(?! resistance)|cell death", 1)],
    "chemoresistance": [(r"chemo-?resist\w*|(?:multi-?)?drug resistance|resistance to|-resistant|"
                         r"resistant to", 1),
                        (r"chemo-?sensitiv\w*|sensitivity to|sensiti[sz]\w*", -1)],
    "angiogenesis": [(r"angiogen\w*|vasculogen\w*|tube formation|neovascular\w*", 1)],
    "stemness": [(r"stemness|stem[- ]like|cancer stem cells?|\bCSCs?\b|sphere[- ]formation|"
                  r"tumou?rsphere\w*|self-renewal", 1)],
    "immune_evasion": [(r"immune (?:evasion|escape|suppression)|immunosuppress\w*|t[- ]cell exhaustion", 1),
                       (r"anti-?tumou?r immun\w*|t[- ]cell infiltration|immune infiltration|"
                        r"cytotoxic t[- ]|immunogenic cell death", -1)],
}
OUTCOME_RE = [(o, re.compile(p, re.I), pol) for o, pats in OUTCOMES.items() for p, pol in pats]
# "anti-metastatic", "pro-apoptotic": the outcome word carries its own direction.
SELF_SIGNED = [
    (re.compile(r"\banti-?metasta\w*", re.I), "metastasis", -1),
    (re.compile(r"\banti-?proliferat\w*|\banti-?tumou?r(?:al)? (?:effect|activit|efficac|propert)\w*|"
                r"\banti-?(?:osteo)?sarcoma (?:effect|activit)\w*|\banti-?cancer (?:effect|activit)\w*", re.I),
     "proliferation", -1),
    (re.compile(r"\bpro-?apoptotic", re.I), "apoptosis", 1),
    (re.compile(r"\banti-?apoptotic", re.I), "apoptosis", -1),
    (re.compile(r"\banti-?angiogen\w*", re.I), "angiogenesis", -1),
    (re.compile(r"\bpro-?angiogen\w*", re.I), "angiogenesis", 1),
    (re.compile(r"\bpro-?metasta\w*", re.I), "metastasis", 1),
]
PROG_BAD = re.compile(r"\b(?:poor|poorer|worse|shorter|short|unfavou?rable|adverse|reduced|lower|decreased|inferior)"
                      r"(?:\s+\w+){0,3}?\s+(?:prognosis|survival|outcomes?|os\b|dfs|efs|mfs)", re.I)
PROG_GOOD = re.compile(r"\b(?:better|favou?rable|longer|good|improved|prolonged|increased|higher|superior)"
                       r"(?:\s+\w+){0,3}?\s+(?:prognosis|survival|outcomes?)", re.I)
ASSOC = re.compile(r"associat|correlat|predict|linked|related|indicat|independent|prognos|hazard", re.I)
UP = re.compile(r"\b(?:promot(?!er)|enhanc|increas|induc|activat|facilitat|stimulat|driv|up-?regulat|accelerat|"
                r"contribut|augment|potentiat|elevat|trigger|boost|aggravat|exacerbat)\w*", re.I)
DOWN = re.compile(r"\b(?:inhibit(?!ors?\b)|suppress(?!or)|reduc|decreas|attenuat|block|impair|abolish|abrogat|prevent|"
                  r"repress|down-?regulat|diminish|restrain|limit|hamper|hinder|lower|reverse|revers|"
                  r"overc[oa]m|counteract|antagoni[sz]|curb|retard)\w*", re.I)
NEG = re.compile(r"\b(?:not|no|neither|nor|failed|without|unaffected|independent of|did not|does not|cannot|"
                 r"minimal|little|marginal|negligible|unchanged|whether)\b", re.I)
# Words around a gene mention that invert its role: "knockdown of X inhibited ..."
FLIP_BEFORE = re.compile(r"(?:knock[- ]?down|disrupt\w* (?:of )?|silenc\w*|deplet\w*|knock[- ]?out|loss of|inhibit\w* (?:of )?|"
                         r"block\w* (?:of )?|blockade of|suppress\w* of|down-?regulat\w* (?:of )?|deficien\w* "
                         r"(?:of |in )?|si-?rna|sh-?rna|(?:low|lower|reduced|decreased) (?:expression|levels?) of|"
                         r"targeting|ablat\w* (?:of )?|antagoni\w* (?:of )?|abrogat\w* (?:of )?|anti-|"
                         r"neutrali[sz]\w* (?:of )?|delet\w* (?:of )?)\s*(?:the |of )?(?:\w+[- ])?$", re.I)
FLIP_AFTER = re.compile(r"^[\s-]*(?:knock[- ]?down|inhibitors?|inhibition|blockade|blocking|silencing|"
                        r"deficien\w*|depletion|antagonists?|(?:monoclonal )?antibod\w*|neutrali[sz]\w*|"
                        r"deletion|null|-/-|knock[- ]?out|siRNA|shRNA|loss|low expression)\b", re.I)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[])")
PT_OUTCOME = {"MESH:D009362": "metastasis", "MESH:D009361": "metastasis"}  # Neoplasm Metastasis / Invasiveness
PT_TUMOUR = {"MESH:D012516", "MESH:D009369", "MESH:D012509", "MESH:D001859", "MESH:D063646"}  # OS, neoplasms, sarcoma, bone neoplasms, carcinogenesis
BENEFICIAL_SIGN = {o: -1 for o in list(OUTCOMES) + ["poor_prognosis", "osteosarcoma_tumour"]}
BENEFICIAL_SIGN["apoptosis"] = 1  # for a drug, more apoptosis of tumour cells is the wanted effect
CHEMO_DRUGS = re.compile(r"cisplatin|doxorubicin|adriamycin|methotrexate|ifosfamide|etoposide|carboplatin|"
                         r"paclitaxel|docetaxel|gemcitabine|vincristine|cyclophosphamide|platinum|anthracycline", re.I)


def mention_regex(m):
    """Word-bounded regex for a mention; case-sensitive when short (e.g. 'MET', 'OS')."""
    esc = re.escape(m.strip())
    flags = 0 if len(m.strip()) <= 4 else re.I
    return re.compile(r"(?<![\w-])" + esc + r"(?![\w])", flags)


def doc_entities(d):
    """[(node_id, node_type, label, mention)] for a corpus record, corrections applied."""
    ents = {}
    for gid, mention, sym in d["genes"]:
        s = gene_symbol(sym, mention)
        if s and mention and len(mention.strip()) >= 2:
            ents[(mention.strip(), "gene")] = s
    for cid, mention in d["chemicals"]:
        if cid and cid != "-" and mention and len(mention.strip()) >= 3:
            ents[(mention.strip(), "chemical")] = cid
    return [(nid, typ, m) for (m, typ), nid in ents.items()]


def sentence_edges(d):
    """Yield (node_id, node_type, outcome, sign, in_title, sentence) from one abstract."""
    title, abstract = d["title"] or "", d["abstract"] or ""
    ents = doc_entities(d)
    if not ents:
        return
    regs = [(nid, typ, mention_regex(m)) for nid, typ, m in ents]
    sents = [(title, True)] + [(s, False) for s in SENT_SPLIT.split(abstract) if s]
    for sent, in_title in sents:
        if len(sent) > 1500:
            continue
        occ = []  # entity occurrences
        for nid, typ, rg in regs:
            for mt in rg.finditer(sent):
                occ.append((mt.start(), mt.end(), nid, typ))
        if not occ:
            continue
        outs = [(mt.start(), mt.end(), o, pol, False) for o, rg, pol in OUTCOME_RE for mt in rg.finditer(sent)]
        outs += [(mt.start(), mt.end(), o, pol, True) for rg, o, pol in SELF_SIGNED for mt in rg.finditer(sent)]
        bad = [(mt.start(), mt.end(), 1) for mt in PROG_BAD.finditer(sent)]
        good = [(mt.start(), mt.end(), -1) for mt in PROG_GOOD.finditer(sent)]
        found = {}
        for es, ee, nid, typ in occ:
            flip = 1
            if typ == "gene":
                if FLIP_BEFORE.search(sent[max(0, es - 45):es]) or FLIP_AFTER.search(sent[ee:ee + 25]):
                    flip = -1
            for os_, oe, o, pol, selfsig in outs:
                if os_ < ee and oe > es:  # overlapping spans
                    continue
                if typ == "chemical" and o == "chemoresistance" and (
                        CHEMO_DRUGS.search(sent[es:ee]) or abs(os_ - ee) < 25 or abs(es - oe) < 25):
                    continue  # "cisplatin resistance": the drug is part of the outcome phrase
                if selfsig:
                    gap = sent[ee:os_] if es < os_ else sent[oe:es]
                    if len(gap) > 120 or NEG.search(gap):
                        continue
                    sign = pol
                elif es < os_:  # "X promotes metastasis"
                    gap = sent[ee:os_]
                    if len(gap) > 150 or NEG.search(gap):
                        continue
                    ups = [m.end() for m in UP.finditer(gap)]
                    downs = [m.end() for m in DOWN.finditer(gap)]
                    if not ups and not downs:
                        continue
                    sign = 1 if max(ups or [-1]) > max(downs or [-1]) else -1
                    sign *= pol
                else:  # "metastasis was inhibited by X", "X-induced apoptosis"
                    gap = sent[oe:es]
                    post = sent[ee:ee + 12]
                    if len(gap) <= 3 and re.match(r"^-?(?:induced|mediated|promoted|driven|dependent)", post):
                        continue  # direction of "X-mediated apoptosis" is the outcome itself; ambiguous for X
                    mt = re.search(r"\b(\w+ed) by\b[^.;]{0,60}$", gap)
                    if not mt or len(gap) > 100 or NEG.search(gap):
                        continue
                    v = mt.group(1)
                    sign = 1 if UP.match(v) else -1 if DOWN.match(v) else 0
                    if not sign:
                        continue
                    sign *= pol
                found.setdefault((nid, typ, o), []).append(sign * flip)
            # prognosis: needs an association word in the sentence
            if ASSOC.search(sent):
                for ps, pe, sign in bad + good:
                    if abs(ps - ee) > 150 and abs(es - pe) > 150:
                        continue
                    found.setdefault((nid, typ, "poor_prognosis"), []).append(sign * flip)
        for (nid, typ, o), signs in found.items():
            s = sum(signs)
            if s:
                yield nid, typ, o, (1 if s > 0 else -1), in_title, sent


# ---------------------------------------------------------------- build the graph
PT_SIGN = {"Positive_Correlation": 1, "Negative_Correlation": -1}


def pubtator_edges(rec, doc_gene_map):
    """Yield (src, src_type, tgt, tgt_type, sign, relation) from one cached PubTator record.

    Gene symbols are corrected with the mention texts of the same document
    (doc_gene_map: PubTator symbol -> corrected symbol, '' = drop)."""
    for r in rec["relations"]:
        ends = []
        for e in (r["e1"], r["e2"]):
            t = e["type"]
            if t == "Gene":
                s = (e["name"] or "").upper()
                s = doc_gene_map.get(s, gene_symbol(s, ""))
                if not s:
                    break
                ends.append((s, "gene"))
            elif t == "Chemical":
                ends.append((e["id"], "chemical"))
            elif t == "Disease":
                if e["id"] in PT_OUTCOME:
                    ends.append((PT_OUTCOME[e["id"]], "outcome"))
                elif e["id"] in PT_TUMOUR:
                    ends.append(("osteosarcoma_tumour", "outcome"))
                else:
                    ends.append((e["id"], "disease"))
            else:
                ends.append((f"{t}:{e['id']}", t.lower()))
        if len(ends) != 2 or ends[0] == ends[1]:
            continue
        # put the outcome/disease on the target side; otherwise order alphabetically
        rank = {"outcome": 3, "disease": 2}
        a, b = sorted(ends, key=lambda x: (rank.get(x[1], 0), x[0]))
        yield a[0], a[1], b[0], b[1], PT_SIGN.get(r["type"], 0), r["type"]


def build():
    tags = load_tags()
    docs = load_corpus()
    rels = {}
    if os.path.exists(REL_CACHE):
        for line in open(REL_CACHE):
            d = json.loads(line)
            rels[d["pmid"]] = d
    else:
        print("WARNING: no PubTator relation cache; sentence layer only (run `fetch` first)")
    print(f"{len(docs)} unique papers; {len(rels)} with cached PubTator relations "
          f"({sum(1 for r in rels.values() if r['relations'])} with at least one relation)")

    chem_name = C.defaultdict(C.Counter)
    for d in docs.values():
        for cid, m in d["chemicals"]:
            chem_name[cid][m.lower()] += 1
    label = {cid: c.most_common(1)[0][0] for cid, c in chem_name.items()}

    # per-paper evidence: (src, src_type, tgt, tgt_type, relation, layer) -> {pmid: sign}
    ev = C.defaultdict(dict)
    sent_store = C.defaultdict(list)  # (src, outcome, pmid) -> [(sign, sentence)]
    for n, (p, d) in enumerate(docs.items()):
        t = tags.get(p)
        if not t or t["retracted"]:
            continue
        per = C.defaultdict(float)
        for nid, typ, o, sign, in_title, sent in sentence_edges(d):
            per[(nid, typ, o)] += sign * (1.5 if in_title else 1.0)
            sent_store[(nid, o, p)].append((sign, sent[:400]))
        for (nid, typ, o), s in per.items():
            if s:
                ev[(nid, typ, o, "outcome", "directional", "sentence")][p] = 1 if s > 0 else -1
        if p in rels:
            gmap = {}
            for gid, m, sym in d["genes"]:
                gmap.setdefault((sym or "").upper(), C.Counter())[gene_symbol(sym, m)] += 1
            gmap = {k: v.most_common(1)[0][0] for k, v in gmap.items()}
            for a, at, b, bt, sign, rel in pubtator_edges(rels[p], gmap):
                key = (a, at, b, bt, rel, "pubtator")
                ev[key][p] = sign
        if n % 5000 == 0:
            print(f"  {n}/{len(docs)} papers", flush=True)

    # aggregate to edge rows (one row per key and direction)
    rows = []
    for (a, at, b, bt, rel, layer), papers in ev.items():
        by_sign = C.defaultdict(list)
        for p, s in papers.items():
            by_sign[s].append(p)
        for s, ps in by_sign.items():
            ts = [tags[p] for p in ps]
            ys = [t["year"] for t in ts if t["year"]]
            rows.append({
                "source": a, "source_type": at, "source_label": label.get(a, a) if at == "chemical" else a,
                "target": b, "target_type": bt, "target_label": label.get(b, b) if bt == "chemical" else b,
                "direction": {1: "+", -1: "-", 0: "0"}[s], "relation": rel, "layer": layer,
                "n_papers": len(ps), "n_nonreview": sum(not t["review"] for t in ts),
                "weight": round(sum(paper_weight(t) for t in ts), 2),
                "n_in_vivo": sum(t["in_vivo"] for t in ts), "n_patients": sum(t["patients"] for t in ts),
                "n_dog": sum(t["dog"] for t in ts), "n_ncrna": sum(t["ncrna"] for t in ts),
                "first_year": min(ys) if ys else "", "last_year": max(ys) if ys else "",
                "pmids": ";".join(sorted(ps, key=int))})
    rows.sort(key=lambda r: (-r["weight"], r["source"], r["target"]))
    with open("data/osteosarcoma_knowledge_graph_edges.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} edge rows -> data/osteosarcoma_knowledge_graph_edges.csv")
    contradictions(ev, tags, label, sent_store, docs)
    return ev, tags, label


# ---------------------------------------------------------------- contradictions
LEAD_GENES = {"IL6", "IL1A", "IL1B", "CXCL8", "CXCR1", "CXCR2", "CXCR4", "CXCL12", "PTK2", "DKK1", "AKT1", "AKT2",
              "AKT3", "MYC", "VEGFA", "KDR", "LRRC15", "PTK7", "CCNE1", "MDM2"}
CONTRA_OUTCOMES = set(OUTCOMES) | {"poor_prognosis"}  # 'osteosarcoma_tumour' is too vague (expression vs effect)
RAW = "data/repurposing_raw/"


def chembl_drug_names(min_phase=3):
    """{lower-case name or synonym: (chembl_id, pref_name, max_phase)} from the repurposing screen's ChEMBL cache."""
    names = {}
    for ph in ("4", "3"):
        path = f"{RAW}chembl_molecules_phase{ph}.json"
        if int(ph) < min_phase or not os.path.exists(path):
            continue
        for m in json.load(open(path)):
            if not m.get("pref_name"):
                continue
            pid = (m.get("molecule_hierarchy") or {}).get("parent_chembl_id") or m["molecule_chembl_id"]
            entry = (pid, m["pref_name"].lower(), int(float(m.get("max_phase") or ph)))
            for n in [m["pref_name"]] + [s.get("molecule_synonym") or "" for s in m.get("molecule_synonyms") or []]:
                n = n.lower().strip()
                if len(n) >= 5 and not n.replace("-", "").isdigit():
                    names.setdefault(n, entry)
    return names


# Hand classification of the top contradictions after reading the abstracts
# (filled in from research_notes/Knowledge graph/notes.md; key = (entity, outcome)).
CLASSIFICATION = {}


def paper_signs(ev, entity, outcome):
    """{pmid: (sign, layer)} for entity -> outcome; the sentence layer wins over PubTator in the same paper."""
    out = {}
    for layer, rel in (("pubtator", "Positive_Correlation"), ("pubtator", "Negative_Correlation"),
                       ("sentence", "directional")):
        for et in ("gene", "chemical"):
            for p, s in ev.get((entity, et, outcome, "outcome", rel, layer), {}).items():
                if s:
                    out[p] = (s, layer)
    return out


def contradictions(ev, tags, label, sent_store, docs):
    drugs = chembl_drug_names()
    pairs = {(a, at, b) for (a, at, b, bt, rel, layer) in ev if bt == "outcome" and b in CONTRA_OUTCOMES}
    rows = []
    for a, at, o in pairs:
        if at == "chemical":
            names = {label.get(a, "")}
            if not any(n in drugs for n in names):
                continue  # lab reagents, metals, materials: only ChEMBL phase 3-4 drugs are compared
        ps = {p: v for p, v in paper_signs(ev, a, o).items() if not tags[p]["review"]}
        pos = [p for p, (s, _) in ps.items() if s > 0]
        neg = [p for p, (s, _) in ps.items() if s < 0]
        if len(pos) < 2 or len(neg) < 2:
            continue
        wp = sum(paper_weight(tags[p]) for p in pos)
        wn = sum(paper_weight(tags[p]) for p in neg)
        minority = min(wp, wn)

        def ex(pl):
            best = sorted(pl, key=lambda p: -paper_weight(tags[p]))[:3]
            out = []
            for p in best:
                ss = sent_store.get((a, o, p))
                out.append(f"{p}: {ss[0][1][:220]}" if ss else f"{p}: [PubTator relation] {docs[p]['title'][:160]}")
            return " || ".join(out)
        lead = a in LEAD_GENES
        rows.append({
            "entity": a, "entity_type": at, "label": label.get(a, a) if at == "chemical" else a,
            "outcome": o, "lead_gene": lead, "n_up": len(pos), "n_down": len(neg),
            "weight_up": round(wp, 2), "weight_down": round(wn, 2),
            "majority": "+" if wp > wn else "-", "minority_share": round(minority / (wp + wn), 3),
            "score": round(minority, 2), "priority_score": round(minority * (2 if lead else 1), 2),
            "n_up_in_vivo_patient_dog": sum(tags[p]["in_vivo"] or tags[p]["patients"] or tags[p]["dog"] for p in pos),
            "n_down_in_vivo_patient_dog": sum(tags[p]["in_vivo"] or tags[p]["patients"] or tags[p]["dog"] for p in neg),
            "n_up_ncrna": sum(tags[p]["ncrna"] for p in pos), "n_down_ncrna": sum(tags[p]["ncrna"] for p in neg),
            "n_from_pubtator": sum(1 for p, (s, l) in ps.items() if l == "pubtator"),
            "up_pmids": ";".join(sorted(pos, key=int)), "down_pmids": ";".join(sorted(neg, key=int)),
            "up_examples": ex(pos), "down_examples": ex(neg),
            "classification": CLASSIFICATION.get((a, o), ("", ""))[0],
            "classification_note": CLASSIFICATION.get((a, o), ("", ""))[1]})
    rows.sort(key=lambda r: -r["priority_score"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    with open("data/osteosarcoma_contradictions.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank"] + [k for k in rows[0] if k != "rank"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} contradiction candidates -> data/osteosarcoma_contradictions.csv")


# ---------------------------------------------------------------- hidden links (A -> B -> C)
NEG_ACTIONS = {"INHIBITOR", "ANTAGONIST", "BLOCKER", "NEGATIVE ALLOSTERIC MODULATOR", "INVERSE AGONIST",
               "ANTISENSE INHIBITOR", "RNAI INHIBITOR", "DEGRADER", "NEGATIVE MODULATOR", "DISRUPTING AGENT"}
POS_ACTIONS = {"AGONIST", "ACTIVATOR", "POSITIVE ALLOSTERIC MODULATOR", "OPENER", "PARTIAL AGONIST",
               "STABILISER", "POSITIVE MODULATOR"}
SKIP_ACTIONS = {"VACCINE ANTIGEN", "EXOGENOUS PROTEIN", "EXOGENOUS GENE", "SUBSTRATE", "HYDROLYTIC ENZYME",
                "PROTEOLYTIC ENZYME", "OXIDATIVE ENZYME", "REDUCING AGENT"}
DIAGNOSTIC = re.compile(r"technetium|indium in|gallium ga|tc[ -]?99m|\bf[ -]?18\b|zirconium|copper cu|florbeta|"
                        r"flortau|flutemetamol|iodine i|lutetium|yttrium", re.I)
MUTANT_ONLY = re.compile(r"mutant|G12C|G12D|V600|vorasidenib|ivosidenib|enasidenib|olutasidenib|sotorasib|"
                         r"adagrasib|divarasib", re.I)
OUTCOME_WORDS = {  # PubMed query terms for the direct-link check
    "metastasis": "(metastasis OR metastatic OR invasion OR migration)",
    "proliferation": "(proliferation OR growth OR viability)",
    "apoptosis": "(apoptosis OR apoptotic)",
    "chemoresistance": "(resistance OR chemoresistance OR sensitivity OR sensitization)",
    "angiogenesis": "(angiogenesis OR angiogenic)",
    "stemness": "(stem cell OR stemness OR sphere)",
    "immune_evasion": "(immune OR immunity OR T cell)",
    "poor_prognosis": "(survival OR prognosis)",
}
TOK = re.compile(r"[a-z0-9][a-z0-9\-]*")


def approved_drug_targets():
    """{chembl_id: {"name", "names", "targets": {gene: (sign, action, mechanism)}}} for max_phase 4 drugs.

    From the repurposing screen's ChEMBL cache (data/repurposing_raw/, written by
    `python3 tools/repurposing_screen.py chembl`). Falls back to the shortlist file
    data/osteosarcoma_repurposing_candidates.csv when the raw cache is absent."""
    drugs = {}
    if os.path.exists(RAW + "chembl_mechanisms.json"):
        mols = {m["molecule_chembl_id"]: m for m in json.load(open(RAW + "chembl_molecules_phase4.json"))}
        targets = json.load(open(RAW + "chembl_targets.json"))
        for me in json.load(open(RAW + "chembl_mechanisms.json")):
            act = me.get("action_type") or ""
            if act in SKIP_ACTIONS or me.get("variant_sequence"):
                continue
            pid = me.get("parent_molecule_chembl_id") or me["molecule_chembl_id"]
            m = mols.get(pid) or mols.get(me["molecule_chembl_id"])
            t = targets.get(me.get("target_chembl_id") or "")
            if not m or not m.get("pref_name") or not t or t.get("organism") != "Homo sapiens":
                continue
            if m.get("therapeutic_flag") is False or DIAGNOSTIC.search(m["pref_name"]) or \
                    MUTANT_ONLY.search((me.get("mechanism_of_action") or "") + " " + m["pref_name"]):
                continue
            comps = [c for c in t["components"] if c["symbols"]]
            if not comps or len(comps) > 5 or t.get("target_type") == "CHIMERIC PROTEIN":
                continue  # large complexes (GABA-A, ribosome ...) would credit many genes
            sign = -1 if act in NEG_ACTIONS else 1 if act in POS_ACTIONS else 0
            d = drugs.setdefault(pid, {"name": m["pref_name"].lower(), "first_approval": m.get("first_approval"),
                                       "names": set(), "targets": {}})
            d["names"].add(m["pref_name"].lower())
            for s in m.get("molecule_synonyms") or []:
                n = (s.get("molecule_synonym") or "").lower()
                if len(n) >= 5 and not n.replace("-", "").isdigit() and s.get("syn_type") in (
                        "INN", "USAN", "BAN", "FDA", "ATC", "TRADE_NAME", "OTHER", "MERCK_INDEX", "JAN"):
                    d["names"].add(n)
            for c in comps:
                d["targets"][c["symbols"][0].upper()] = (sign, act, me.get("mechanism_of_action") or "")
    else:
        for r in csv.DictReader(open("data/osteosarcoma_repurposing_candidates.csv")):
            if r["best_drug_phase"] != "4" or r["excluded"]:
                continue
            sign = -1 if r["best_drug_action"] in NEG_ACTIONS else 1 if r["best_drug_action"] in POS_ACTIONS else 0
            d = drugs.setdefault(r["best_drug"], {"name": r["best_drug"], "first_approval": r["best_drug_first_approval"],
                                                  "names": {r["best_drug"]}, "targets": {}})
            d["targets"][r["gene"]] = (sign, r["best_drug_action"], r["best_drug_mechanism"])
    return drugs


def gene_outcome_evidence():
    """{(gene, outcome): {pmid: sign}} from the edge file, sentence layer overriding PubTator."""
    tags = load_tags()
    ev = C.defaultdict(dict)
    rows = list(csv.DictReader(open("data/osteosarcoma_knowledge_graph_edges.csv")))
    for layer in ("pubtator", "sentence"):
        for r in rows:
            if r["layer"] != layer or r["source_type"] != "gene" or r["target_type"] != "outcome" \
                    or r["direction"] == "0" or r["target"] not in CONTRA_OUTCOMES:
                continue
            s = 1 if r["direction"] == "+" else -1
            for p in r["pmids"].split(";"):
                if not tags[p]["review"]:
                    ev[(r["source"], r["target"])][p] = s
    return ev, tags


def corpus_drug_hits(drugs, docs, tags):
    """{chembl_id: {pmid: set(outcomes named in that abstract)}} by name n-gram match."""
    name_to = C.defaultdict(set)
    for cid, d in drugs.items():
        for n in d["names"]:
            name_to[" ".join(TOK.findall(n))].add(cid)
    hits = C.defaultdict(dict)
    for p, d in docs.items():
        if tags.get(p, {}).get("retracted"):
            continue
        txt = (d["title"] or "") + " " + (d["abstract"] or "")
        toks = TOK.findall(txt.lower())
        found = set()
        for k in (1, 2, 3):
            for i in range(len(toks) - k + 1):
                g = " ".join(toks[i:i + k])
                if g in name_to:
                    found |= name_to[g]
        if not found:
            continue
        outs = {o for o, rg, _ in OUTCOME_RE if rg.search(txt)}
        if PROG_BAD.search(txt) or PROG_GOOD.search(txt) or re.search(r"surviv|prognos", txt, re.I):
            outs.add("poor_prognosis")
        for cid in found:
            hits[cid][p] = outs
    return hits


def _cache():
    return json.load(open(ABC_CACHE)) if os.path.exists(ABC_CACHE) else {}


def _cached_get(cache, key, url, parse=json.loads):
    if key not in cache:
        try:
            cache[key] = parse(get(url, tries=3, timeout=60).decode())
        except Exception as e:  # keep going; record the failure
            cache[key] = {"error": str(e)[:200]}
        time.sleep(DELAY)
        json.dump(cache, open(ABC_CACHE, "w"))
    return cache[key]


def broad_drug_gene(cache, drug_name):
    """PubTator3 relation counts for a drug against every gene, across all of PubMed.

    Returns {gene_symbol: {"negative_correlate": n, "positive_correlate": n, ...}}."""
    ac = _cached_get(cache, "ac:" + drug_name, "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/entity/"
                     "autocomplete/?" + urllib.parse.urlencode({"query": drug_name, "concept": "chemical"}))
    if not isinstance(ac, list) or not ac:
        return {}
    eid = ac[0]["_id"]
    rel = _cached_get(cache, "rel:" + eid, PT_REL + urllib.parse.urlencode({"e1": eid, "e2": "Gene"}))
    out = C.defaultdict(C.Counter)
    if isinstance(rel, list):
        for r in rel:
            g = r["target"].replace("@GENE_", "").upper() if r["source"] == eid else r["source"].replace("@GENE_", "").upper()
            out[g][r["type"]] += r["publications"]
    return out


def pubmed_count(cache, term):
    d = _cached_get(cache, "pm:" + term, EUTILS + urllib.parse.urlencode(
        {"db": "pubmed", "term": term, "retmode": "json", "retmax": 20}))
    if "esearchresult" not in d:
        return None, []
    return int(d["esearchresult"]["count"]), d["esearchresult"]["idlist"]


def pubmed_titles(cache, pmids):
    if not pmids:
        return {}
    d = _cached_get(cache, "sum:" + ",".join(pmids), "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
                    + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}))
    res = d.get("result", {})
    return {p: res.get(p, {}).get("title", "") for p in pmids}


# Hand review of the top chains after the PubMed check (key = (drug, gene, outcome)):
# ("keep" | "drop", note). Filled in from research_notes/Knowledge graph/notes.md.
ABC_REVIEW = {}


def abc(n_check=30):
    tags = load_tags()
    docs = load_corpus()
    bc, _ = gene_outcome_evidence()
    drugs = approved_drug_targets()
    hits = corpus_drug_hits(drugs, docs, tags)
    print(f"{len(drugs)} approved drugs with a human target; {len(hits)} named in at least one OS abstract")
    # B -> C: consistent gene -> outcome evidence
    bcs = {}
    for (g, o), ps in bc.items():
        pos = [p for p, s in ps.items() if s > 0]
        neg = [p for p, s in ps.items() if s < 0]
        wp, wn = sum(paper_weight(tags[p]) for p in pos), sum(paper_weight(tags[p]) for p in neg)
        dom, wd, wm = (1, wp, wn) if wp >= wn else (-1, wn, wp)
        dom_ps = pos if dom > 0 else neg
        if len(dom_ps) < 3 or wd / (wp + wn) < 0.7:
            continue
        strong = sum(tags[p]["in_vivo"] or tags[p]["patients"] or tags[p]["dog"] for p in dom_ps)
        bcs[(g, o)] = {"sign": dom, "w": wd, "consistency": wd / (wp + wn), "pmids": dom_ps,
                       "n_against": len(neg if dom > 0 else pos), "n_strong": strong}
    by_gene = C.defaultdict(list)
    for (g, o), v in bcs.items():
        by_gene[g].append((o, v))
    chains = []
    for cid, d in drugs.items():
        os_papers = hits.get(cid, {})
        for g, (sab, act, mech) in d["targets"].items():
            if sab == 0 or g not in by_gene:
                continue
            for o, v in by_gene[g]:
                direct = [p for p, outs in os_papers.items() if o in outs]
                if direct:
                    continue  # an OS abstract already names this drug together with this outcome
                eff = sab * v["sign"]
                chains.append({"drug": d["name"], "chembl_id": cid, "first_approval": d["first_approval"],
                               "action": act, "mechanism": mech, "gene": g, "drug_to_gene": "+" if sab > 0 else "-",
                               "outcome": o, "gene_to_outcome": "+" if v["sign"] > 0 else "-",
                               "drug_effect_on_outcome": "+" if eff > 0 else "-",
                               "beneficial": eff == BENEFICIAL_SIGN[o],
                               "bc_weight": round(v["w"], 2), "bc_consistency": round(v["consistency"], 2),
                               "bc_papers": len(v["pmids"]), "bc_papers_against": v["n_against"],
                               "bc_in_vivo_patient_dog": v["n_strong"],
                               "bc_pmids": ";".join(sorted(v["pmids"], key=lambda p: -paper_weight(tags[p]))[:12]),
                               "n_drug_targets": len(d["targets"]),
                               "os_corpus_papers_naming_drug": len(os_papers),
                               "os_corpus_pmids_naming_drug": ";".join(sorted(os_papers, key=int)[:10])})
    print(f"{len(chains)} candidate chains with no direct drug-outcome OS abstract")
    for c in chains:
        c["score"] = round(c["bc_weight"] * c["bc_consistency"] / (c["n_drug_targets"] ** 0.5)
                           * (1.0 if c["os_corpus_papers_naming_drug"] == 0 else 0.5), 3)
    chains.sort(key=lambda c: -c["score"])
    return chains, tags
