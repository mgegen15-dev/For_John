# For John

*In memory of my little brother and best friend, John.*

An open, independent effort focused on osteosarcoma: to tie together the research on it and find what has been overlooked. That means untested ideas, contradictions, lost trial results, and places where funding, trials and the literature don't line up. Osteosarcoma is the target; ideas are borrowed from anywhere: other sarcomas, neuroblastoma, adult cancers, other diseases, and dogs.

Everything here is built from public sources (PubMed, PubTator3, ClinicalTrials.gov, NIH RePORTER, Europe PMC, the NCI Genomic Data Commons, GTEx, the Human Protein Atlas, ChEMBL, NCBI Sequence Read Archive, and preprint servers). Most analyses have scripts in `tools/` that anyone can re-run; a few counts were made with one-off database queries described in the report concerned. Findings are leads for researchers to check, not conclusions. The reports were checked against primary sources by independent audits in November 2026, the newest three reports on November 20 together with a repo-wide consistency check (`research_notes/Audit/`).

> **Not medical advice.** Nothing in this repository is a recommendation about any patient's care. Families should discuss treatment and trial options with their child's oncology team.


## What's here

- **Website:** https://mgegen15-dev.github.io/For_John/
- **Start here:** [One-page summary](SUMMARY.md) · [How this was made](HOW_THIS_WAS_MADE.md)
- **Predictions:** [Dated, testable predictions](PREDICTIONS.md), so anyone can check our hit rate as results come in
- **For auditors:** [Auditor's guide](AUDIT_GUIDE.md) · [Data manifest](DATA_MANIFEST.md) · frozen version: git tag `v1.0`
- [The best leads, and who could test them](reports/Ranked%20leads%20and%20research%20partners.md): fourteen leads, scored, each matched to the institutions best placed to test it.

- [Osteosarcoma research landscape and gaps](reports/Osteosarcoma%20research%20landscape%20and%20gaps.md): the state of the field, lessons from neuroblastoma, and twelve candidate gaps with where each stands now.
- [NIH funding for osteosarcoma, 2015–2025](reports/NIH%20funding%20for%20osteosarcoma.md): where NIH money for osteosarcoma goes, compared with neuroblastoma.
- [Osteosarcoma clinical trials: what 40 years of registrations show](reports/Osteosarcoma%20clinical%20trials%20landscape.md): every registered osteosarcoma trial, why they stop, and trials whose results may be missing.
- [A first pooled control dataset for osteosarcoma trials](reports/Osteosarcoma%20pooled%20control%20dataset.md): posted trial results placed side by side against historical benchmarks.
- [The osteosarcoma literature map](reports/Osteosarcoma%20literature%20map.md): 33,000 papers scored by evidence quality and linked to trials and grants, with a close reading of four untested drug targets.
- [Evidence risk flags for osteosarcoma genes](reports/Evidence%20risk%20flags%20for%20osteosarcoma%20genes.md): which genes' literature leans on the paper type most often retracted.
- [Why kinase-inhibitor pills work in osteosarcoma](reports/Why%20kinase-inhibitor%20pills%20work%20in%20osteosarcoma.md): how VEGFR2-blocking kinase pills, the most consistently active targeted drugs in relapse, work, who might respond, why the benefit is short, and why it never became standard.
- [New surface targets for osteosarcoma](reports/New%20surface%20targets%20for%20osteosarcoma.md): an open-data screen of 88 patient tumours against normal tissues for proteins that antibody drugs or CAR-T could target.
- [Stopping lung metastasis in osteosarcoma](reports/Stopping%20lung%20metastasis%20in%20osteosarcoma.md): what is known about how osteosarcoma spreads to the lung, every trial aimed at it, and eight untested ideas, led by IL-1/IL-6 blockade after surgery.
- [Approved drugs worth testing in osteosarcoma](reports/Approved%20drugs%20worth%20testing%20in%20osteosarcoma.md): a screen of 2,400 approved and late-stage drugs for ones with an osteosarcoma rationale but no trial, including the dead ends.
- [Copy-number changes and the kinase-pill biomarker](reports/Copy-number%20changes%20and%20the%20kinase-pill%20biomarker.md): how often tumours carry extra copies of pill-target genes, and how many trial patients a biomarker test would need.
- [What's new in osteosarcoma research](reports/Whats%20new%20in%20osteosarcoma%20research.md): papers, preprints and trials from June 2025 to November 2026 checked against this project's leads, with a protein-level check of the new surface targets.
- [Dog genome re-analysis: what's available and what it would take](reports/Dog%20genome%20re-analysis%20scope.md): 743 open canine osteosarcoma sequencing experiments, including deep tumour–normal genomes from 55 dogs in NCI trials with known outcomes.
- `briefs/`: short research briefs for researchers and funders, starting with [a pet-dog trial of FAK or DKK1 blockade](briefs/Brief%20-%20pet%20dog%20trial%20of%20FAK%20or%20DKK1%20blockade.md).
- `research_notes/`: the sourced notes behind the reports, including the verification pass and the November 2026 audit.
- `tools/`: scripts that rebuild most analyses from public data (NIH RePORTER, ClinicalTrials.gov, Europe PMC, PubTator3, NCI GDC, ChEMBL). Their output is in `data/`.

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
- **Re-running the analyses:** the scripts in `tools/` need Python 3 and internet access; `tools/pool_relapse_benchmarks.py` also needs pandas (`pip install pandas`). `tools/literature_fetch.py` downloads about 33,000 PubMed records, so it is not stored here.

## Cite this

If you use this work, please credit it as:

> For John (2026). Open research on osteosarcoma. https://github.com/mgegen15-dev/For_John

## License

- **Reports, briefs, research notes and data:** [CC BY 4.0](LICENSE-CONTENT). Reuse freely with credit.
- **Code in `tools/`:** [MIT](LICENSE).
- Data drawn from PubMed, ClinicalTrials.gov, NIH RePORTER and other public sources remains subject to their own terms.
