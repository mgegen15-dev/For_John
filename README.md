# For Johnny

An open, independent effort to tie together the research on childhood osteosarcoma (and, secondarily, neuroblastoma) and find what has been overlooked: untested ideas, contradictions, lost trial results, and places where funding, trials and the literature don't line up.

Everything here is built from public sources (PubMed, ClinicalTrials.gov, NIH RePORTER, Europe PMC) with scripts that anyone can re-run. Findings are leads for researchers to check, not conclusions.

> **Not medical advice.** Nothing in this repository is a recommendation about any patient's care. Families should discuss treatment and trial options with their child's oncology team.


## What's here

- **Start here:** [The ten best leads, and who could test them](reports/Ranked%20leads%20and%20research%20partners.md)

- [Research report: osteosarcoma and neuroblastoma research gaps](reports/Osteosarcoma%20and%20neuroblastoma%20research%20gaps.md): the research landscape, twelve candidate gaps, and how each held up when checked.
- [NIH funding for osteosarcoma, 2015–2025](reports/NIH%20funding%20for%20osteosarcoma.md): where NIH money for osteosarcoma goes, compared with neuroblastoma.
- [Osteosarcoma clinical trials: what 40 years of registrations show](reports/Osteosarcoma%20clinical%20trials%20landscape.md): every registered osteosarcoma trial, why they stop, and trials whose results may be missing.
- [A first pooled control dataset for osteosarcoma trials](reports/Osteosarcoma%20pooled%20control%20dataset.md): posted trial results placed side by side against historical benchmarks.
- [The osteosarcoma literature map](reports/Osteosarcoma%20literature%20map.md): 33,000 papers scored by evidence quality and linked to trials and grants, with a close reading of four untested drug targets.
- `research_notes/`: the sourced notes behind the report, including the verification pass.
- `tools/`: scripts that rebuild every analysis from public data (NIH RePORTER, ClinicalTrials.gov, Europe PMC). Their output is in `data/`.

## How to help

- **Researchers:** if a lead matches your work, or you find an error, please open an issue. Corrections are as valuable as confirmations.
- **Re-running the analyses:** the scripts in `tools/` need only Python 3 and internet access. `tools/literature_fetch.py` downloads about 33,000 PubMed records, so it is not stored here.
