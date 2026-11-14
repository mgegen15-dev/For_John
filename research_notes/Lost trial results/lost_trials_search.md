# Lost osteosarcoma trial results: search log

*Built November 14, 2026, as follow-up to `reports/Osteosarcoma clinical trials landscape.md` (Next steps, item 2). For each trial whose results appear never to have been reported, this records what was searched, what was found, and the source actually opened. "Not found" is a finding, not a gap in the log. Nothing here is inferred from a source that was not opened.*

## 1. NCT02273583 (GLATO 2006): metronomic maintenance, non-metastatic osteosarcoma, Brazil/Latin America

**Found: full paper. Result: negative.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT02273583): org study ID "GLATO 2006"; sponsor GRAACC; responsible party Antônio Sérgio Petrilli; status unknown, last updated 2016-02-11; planned 738; primary endpoint EFS; no references, no posted results.
- **Paper:** Senerchia AA, Macedo CR, Ferman S, ... Petrilli AS. "Results of a randomized, prospective clinical trial evaluating metronomic chemotherapy in nonmetastatic patients with high-grade, operable osteosarcomas of the extremities: A report from the Latin American Group of Osteosarcoma Treatment." *Cancer* 2017;123(6):1003-1010. doi:10.1002/cncr.30411. PMID 28263383 (erratum Cancer 2018;124(7):1518). Opened: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=28263383&rettype=abstract&retmode=text
- **Why it was missed:** the abstract does not give the NCT number, and the registry record was never updated with the citation. Found via Europe PMC query `Petrilli AND osteosarcoma AND metronomic`.
- **Result (from the abstract):** 422 non-metastatic patients registered, May 2006 to July 2013, 27 sites in Brazil, Argentina and Uruguay. 296 randomized after surgery: MAP plus 73 weeks of oral cyclophosphamide + methotrexate (n=139) vs MAP alone (n=157). 5-year EFS from randomization 61% (MAP+MC) vs 64% (MAP alone); Wilcoxon (Gehan) statistic 0.724, **P = 0.395**. Not superior. Poor necrosis (grades 1-2), tumour size and amputation predicted shorter EFS. The abstract gives no hazard ratio and no overall survival figure.
- **Note:** enrolment fell well short of the 738 planned (296 randomized).
- **Other searches:** Europe PMC `NCT02273583` (1 hit, an unrelated review), `GLATO`, `"GLATO 2006"`, `osteossarcoma AND metronômica` (no trial report).
- **Confidence: high.** Same design, regimen, dates, sponsor institution and PI as the registry record.

## 2. NCT03063983 (GLATO2017): metronomic chemotherapy in metastatic osteosarcoma, Brazil

**Found: nothing. No paper, abstract or press release reporting results.**

- **Registry record** (opened https://clinicaltrials.gov/api/v2/studies/NCT03063983): acronym GLATO2017; sponsor GRAACC; responsible party Antônio Sérgio Petrilli; overall official Cláudia F. Fontes; started 2017-01-02; status unknown (last update 2017-03-13, last known "recruiting"); planned 158; estimated completion 2022-01-31; primary endpoint EFS with added metronomic therapy. No references, no results.
- **Searched, nothing relevant:**
  - Europe PMC: `NCT03063983` (2 hits, both reviews that only list the trial as ongoing: PMID 35409176, 33809018), `GLATO2017`, `"Latin American Group of Osteosarcoma"` (only GLATO 2006 and lab papers), `metastatic osteosarcoma AND metronomic AND (Latin American OR Brazil OR GRAACC)`, author search `AUTH:"Petrilli AS" AND osteosarcoma`, `Fontes CF AND osteosarcoma`, abstracts-only filter `osteosarcoma AND metronomic AND Brazil`.
  - SIOP abstract books for 2014, 2015, 2017 and 2018 (Pediatr Blood Cancer; full text downloaded from PMC7168141, PMC7167893, PMC7167988, PMC7167781). Europe PMC matched them, but scanning the full text for "metronom" near "osteosarc" found no GLATO abstract. The match came from words scattered across the whole book.
  - PubMed: `metronomic AND osteosarcoma AND metasta* AND (Brazil OR Argentina)[ad]` (0), `Petrilli AS[au] AND osteosarcoma, 2018-2026` (9 hits, all laboratory or genetics papers).
  - Crossref bibliographic query (no relevant hit). WebSearch in English and Portuguese ("osteossarcoma metastático quimioterapia metronômica GRAACC") turned up only registry mirrors.
  - OpenAlex could not be searched: the shared daily budget for this IP was used up.
- **Side note:** WebSearch surfaced a 2011 abstract titled "Preliminary safety and outcome report of the metronomic therapy from the Latin American..." on aminer.org. That host is blocked in this session, so I never opened it. Its search snippet suggests it covers the earlier GLATO 2006 programme, not GLATO2017. Unverified.
- **Confidence: moderate** that no results are public in indexed literature. Results could still sit in SIOP 2019-2025 abstract books (not scanned here) or in Brazilian theses. Next step: contact GRAACC (Petrilli or Fontes).

