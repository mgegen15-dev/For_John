# For John

*In memory of my little brother and best friend, John.*

An open, independent effort focused on osteosarcoma: to tie together the research on it and find what has been overlooked. That means untested ideas, contradictions, lost trial results, and places where funding, trials and the literature don't line up. Neuroblastoma appears where its progress holds lessons for osteosarcoma.

Everything here is built from public sources (PubMed, ClinicalTrials.gov, NIH RePORTER, Europe PMC) with scripts that anyone can re-run. Findings are leads for researchers to check, not conclusions.

> **Not medical advice.** Nothing in this repository is a recommendation about any patient's care. Families should discuss treatment and trial options with their child's oncology team.


## What's here

- **Start here:** [The ten best leads, and who could test them](reports/Ranked%20leads%20and%20research%20partners.md)

- [Research report: osteosarcoma and neuroblastoma research gaps](reports/Osteosarcoma%20and%20neuroblastoma%20research%20gaps.md): the research landscape, twelve candidate gaps, and how each held up when checked.
- [NIH funding for osteosarcoma, 2015–2025](reports/NIH%20funding%20for%20osteosarcoma.md): where NIH money for osteosarcoma goes, compared with neuroblastoma.
- [Osteosarcoma clinical trials: what 40 years of registrations show](reports/Osteosarcoma%20clinical%20trials%20landscape.md): every registered osteosarcoma trial, why they stop, and trials whose results may be missing.
- [A first pooled control dataset for osteosarcoma trials](reports/Osteosarcoma%20pooled%20control%20dataset.md): posted trial results placed side by side against historical benchmarks.
- [The osteosarcoma literature map](reports/Osteosarcoma%20literature%20map.md): 33,000 papers scored by evidence quality and linked to trials and grants, with a close reading of four untested drug targets.
- [Evidence risk flags for osteosarcoma genes](reports/Evidence%20risk%20flags%20for%20osteosarcoma%20genes.md): which genes' literature leans on the paper type most often retracted.
- [Dog genome re-analysis: what's available and what it would take](reports/Dog%20genome%20re-analysis%20scope.md): 743 open canine osteosarcoma genome runs, including dogs from NCI trials with known outcomes.
- `briefs/`: short research briefs for researchers and funders, starting with [a pet-dog trial of FAK or DKK1 blockade](briefs/Brief%20-%20pet%20dog%20trial%20of%20FAK%20or%20DKK1%20blockade.md).
- `research_notes/`: the sourced notes behind the report, including the verification pass.
- `tools/`: scripts that rebuild every analysis from public data (NIH RePORTER, ClinicalTrials.gov, Europe PMC). Their output is in `data/`.

## Related work

This project builds on, and hopes to feed into, the work of many others. If you know of something that belongs here, please open an issue.

**Research consortia and trial groups**
- [Children's Oncology Group (COG)](https://childrensoncologygroup.org/): runs most US paediatric osteosarcoma trials.
- FOSTER (Fight Osteosarcoma Through European Research): the European osteosarcoma consortium, supported by the Bone Cancer Research Trust. Its new trial platform is [NCT07871864](https://clinicaltrials.gov/study/NCT07871864).
- [Sarcoma Alliance for Research through Collaboration (SARC)](https://sarctrials.org/): runs sarcoma trials, including SARC024 and SARC028.
- [NCI Comparative Oncology Program](https://ccr.cancer.gov/comparative-oncology-program): runs pet-dog cancer trials through the Comparative Oncology Trials Consortium.

**Data and patient-partnered research**
- [The Osteosarcoma Project (Count Me In)](https://osproject.org/): patients and families share samples and records for genomic research.
- [Childhood Cancer Data Initiative (CCDI)](https://www.cancer.gov/research/areas/childhood/childhood-cancer-data-initiative): NCI's paediatric cancer data infrastructure.
- [Pediatric Cancer Data Commons](https://commons.cri.uchicago.edu/): harmonized paediatric trial data, including bone tumours.
- [St. Jude Cloud](https://www.stjude.cloud/) and [Gabriella Miller Kids First](https://kidsfirstdrc.org/): paediatric genomic data.
- [PedcBioPortal](https://pedcbioportal.kidsfirstdrc.org/) and [cBioPortal](https://www.cbioportal.org/): browsable cancer genomics.
- [Integrated Canine Data Commons](https://caninecommons.cancer.gov/): canine cancer data, including osteosarcoma.

**Foundations and advocacy**
- [MIB Agents](https://www.mibagents.org/): osteosarcoma-specific family community and research funder.
- Osteosarcoma Institute (Dallas): a virtual institute that funds osteosarcoma trials and research.
- [QuadW Foundation](https://quadw.org/), [Sarcoma Foundation of America](https://www.curesarcoma.org/), [Bone Cancer Research Trust](https://www.bcrt.org.uk/), [St. Baldrick's Foundation](https://www.stbaldricks.org/), [Alex's Lemonade Stand Foundation](https://www.alexslemonade.org/).
- [Break Through Cancer](https://breakthroughcancer.org/): its Defying Osteosarcoma TeamLab is funded by family-led foundations.

**Drug repurposing**
- [Every Cure](https://everycure.org/): uses AI to find new uses for existing drugs.

**Published analyses this project overlaps with**
- Lagmay et al., [*J Clin Oncol* 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5012712/): the COG relapse benchmark used throughout this project.
- [*Frontiers in Immunology* 2026](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2026.1790067/full): the clinical trial landscape of osteosarcoma, 864 trials from a commercial database.
- [Evidence gap map across osteosarcoma tumour types](https://researchportal.plymouth.ac.uk/en/publications/evidence-distribution-across-osteosarcoma-tumour-types-an-evidenc/): built to inform the WHO classification.
- Espejo Valle-Inclan et al., [*Cell* 2025](https://doi.org/10.1016/j.cell.2024.12.005): ongoing chromothripsis in osteosarcoma.

**Tools for checking research and trials**
- [Retraction Watch Database](https://retractionwatch.com/retraction-watch-database-user-guide/) and the [Problematic Paper Screener](https://www.irit.fr/~Guillaume.Cabanac/problematic-paper-screener): retractions and suspect papers.
- [FDAAA TrialsTracker](https://fdaaa.trialstracker.net/): tracks unreported US trials.
- [Open Targets](https://platform.opentargets.org/): evidence linking targets to diseases.
- Data sources used here: [PubMed](https://pubmed.ncbi.nlm.nih.gov/), [PubTator3](https://www.ncbi.nlm.nih.gov/research/pubtator3/), [Europe PMC](https://europepmc.org/), [ClinicalTrials.gov](https://clinicaltrials.gov/), [NIH RePORTER](https://reporter.nih.gov/), [NCBI Sequence Read Archive](https://www.ncbi.nlm.nih.gov/sra).

## How to help

- **Researchers:** if a lead matches your work, or you find an error, please open an issue. Corrections are as valuable as confirmations.
- **Re-running the analyses:** the scripts in `tools/` need only Python 3 and internet access. `tools/literature_fetch.py` downloads about 33,000 PubMed records, so it is not stored here.

## Cite this

If you use this work, please credit it as:

> For John (2026). Open research on osteosarcoma. https://github.com/mgegen15-dev/For_John

## License

- **Reports, briefs, research notes and data:** [CC BY 4.0](LICENSE-CONTENT). Reuse freely with credit.
- **Code in `tools/`:** [MIT](LICENSE).
- Data drawn from PubMed, ClinicalTrials.gov, NIH RePORTER and other public sources remains subject to their own terms.
