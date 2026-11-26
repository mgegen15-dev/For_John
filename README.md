# For John

*In memory of my little brother and best friend, John.*

An open, independent effort focused on osteosarcoma: to tie together the research on it and find what has been overlooked. That means untested ideas, contradictions, lost trial results, and places where funding, trials and the literature don't line up. Osteosarcoma is the target; ideas are borrowed from anywhere: other sarcomas, neuroblastoma, adult cancers, other diseases, and dogs.

Everything here is built from public sources (PubMed, PubTator3, ClinicalTrials.gov, NIH RePORTER, Europe PMC, the NCI Genomic Data Commons, GTEx, the Human Protein Atlas, ChEMBL, NCBI Sequence Read Archive, and preprint servers). Most analyses have scripts in `tools/` that anyone can re-run; a few counts were made with one-off database queries described in the report concerned. Findings are leads for researchers to check, not conclusions. The reports were checked against primary sources by independent audits in November 2026, the newest three reports on November 20 together with a repo-wide consistency check (`research_notes/Audit/`).

> **Not medical advice.** Nothing in this repository is a recommendation about any patient's care. Families should discuss treatment and trial options with their child's oncology team.


## What's here

- **Website:** https://mgegen15-dev.github.io/For_John/
- **Evidence explorer:** https://mgegen15-dev.github.io/For_John/explorer.html: type a gene, drug or target to see its papers, paper-mill risk flag, trials, tumour expression, copy-number changes, approved drugs and the reports that discuss it (built by `tools/build_explorer_data.py`).
- **Start here:** [One-page summary](SUMMARY.md) · [How this was made](HOW_THIS_WAS_MADE.md)
- **Predictions:** [Dated, testable predictions](PREDICTIONS.md), so anyone can check our hit rate as results come in
- **For auditors:** [Auditor's guide](AUDIT_GUIDE.md) · [Data manifest](DATA_MANIFEST.md) · frozen version: git tag `v1.1`
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
- [Do the leads predict survival?](reports/Do%20the%20leads%20predict%20survival.md): a pre-registered test of 20 lead-related markers against outcome in 89 patients; none survives correction for multiple testing.
- [Research Queue](RESEARCH_QUEUE.md): the research engine's questions, each pre-registered and tested on independent patients, with every result published.
- [Engine cycle 1: does RAMP1 predict relapse?](reports/Engine%20cycle%201%20-%20does%20RAMP1%20predict%20relapse.md): first engine result; the discovery signal did not replicate in three independent cohorts.
- [Engine cycle 2: do lung metastases carry more CXCR4?](reports/Engine%20cycle%202%20-%20do%20lung%20metastases%20carry%20more%20CXCR4.md): second engine result; a lean in whole tissue that immune cells explain, so lead 14 gains no support.
- [Engine cycle 3: is 9p21 deletion more common at relapse?](reports/Engine%20cycle%203%20-%20is%209p21%20deletion%20more%20common%20at%20relapse.md): third engine result; not clearly more common, but present in about one in five relapsed tumours and stable from primary to relapse.
- [Engine cycle 4: MTAP-selected trials open to osteosarcoma](reports/Engine%20cycle%204%20-%20MTAP-selected%20trials%20open%20to%20osteosarcoma.md): 25 trials an adult patient could ask about, one naming bone sarcoma; almost none for under-18s.
- [Engine cycle 5: do osteosarcoma cells without MTAP depend on PRMT5?](reports/Engine%20cycle%205%20-%20do%20osteosarcoma%20cells%20without%20MTAP%20depend%20on%20PRMT5.md): too few MTAP-lost lines to tell; lists the lines a laboratory would need.
- [Engine cycle 6: do osteosarcoma cells with more CCNE1 depend on PKMYT1?](reports/Engine%20cycle%206%20-%20do%20osteosarcoma%20cells%20with%20more%20CCNE1%20depend%20on%20PKMYT1.md): leans the expected way, not confirmed; four amplified lines identified.
- [Engine cycle 7: CCNE1 amplification at relapse and the trials open to it](reports/Engine%20cycle%207%20-%20CCNE1%20amplification%20at%20relapse%20and%20the%20trials%20open%20to%20it.md): about one in ten relapsed tumours; nine trials on paper, one taking patients from age 12.
- [Engine cycle 8: a scan for drug weaknesses that go with osteosarcoma's gene changes](reports/Engine%20cycle%208%20-%20a%20scan%20for%20drug%20weaknesses%20that%20go%20with%20osteosarcoma%27s%20gene%20changes.md): 1.2 million comparisons; recovers the known pairs, finds no hidden one, and points to FOCAD loss with HBS1L.
- [Engine cycle 9: weaknesses that go with the tumour-suppressor genes osteosarcoma loses](reports/Engine%20cycle%209%20-%20weaknesses%20that%20go%20with%20the%20tumour-suppressor%20genes%20osteosarcoma%20loses.md): recovers the known RB1 pairs; nothing new; shows that public cell-line data miss how osteosarcoma breaks TP53 and ATRX.
- [Engine cycle 10: do the gene-change weaknesses hold up with real drugs?](reports/Engine%20cycle%2010%20-%20do%20the%20gene-change%20weaknesses%20hold%20up%20with%20real%20drugs.md): in a public drug screen the known drug–gene links show up clearly; CCNE1 with a WEE1 inhibitor and MTAP loss with an early PRMT5 drug are inconclusive.
- [Engine cycle 11: do lung metastases keep the surface targets?](reports/Engine%20cycle%2011%20-%20do%20lung%20metastases%20keep%20the%20surface%20targets.md): no sign that LRRC15 is lost in lung metastases; B7-H3 lower in whole tissue but not clearly in tumour cells; the lung-tissue adjustment proved unstable.
- [Engine cycle 12: how often can a teenager with osteosarcoma get into a drug trial?](reports/Engine%20cycle%2012%20-%20how%20often%20can%20a%20teenager%20with%20osteosarcoma%20get%20into%20a%20drug%20trial.md): 43 of 57 relapse trials naming osteosarcoma accept teenagers; 78 of 1,434 early-phase solid-tumour trials do.
- [Engine cycle 13: in pet dogs, does tumour inflammation go with faster relapse?](reports/Engine%20cycle%2013%20-%20in%20pet%20dogs%20does%20tumour%20inflammation%20go%20with%20faster%20relapse.md): 59 dogs; inflammation score inconclusive, DKK1 refuted, FAK inconclusive; IL1B alone leans towards faster relapse (unplanned).
- [Engine cycle 14: does tumour macrophage signal predict a better outcome in new patients?](reports/Engine%20cycle%2014%20-%20does%20tumour%20macrophage%20signal%20predict%20a%20better%20outcome%20in%20new%20patients.md): the 2011 Leiden finding reproduces in its own data (0.63) but pools to 0.85 (0.67–1.08) in three independent cohorts.
- [Engine cycle 15: do tumours with MYC gain respond worse to chemotherapy?](reports/Engine%20cycle%2015%20-%20do%20tumours%20with%20MYC%20gain%20respond%20worse%20to%20chemotherapy.md): MYC RNA modestly linked to poor response (1.58, 1.05–2.40) in three cohorts; CCNE1 refuted; 9p21 inconclusive.
- [Engine cycle 16: since the FDA guidance, are new trials more open to teenagers?](reports/Engine%20cycle%2016%20-%20since%20the%20FDA%20guidance%20are%20new%20trials%20more%20open%20to%20teenagers.md): no sign of an increase; 26 of 1,083 company-led early-phase trials started since 2020 accept teenagers.
- [Engine cycle 17: before and after the FDA guidance, across all trials](reports/Engine%20cycle%2017%20-%20before%20and%20after%20the%20FDA%20guidance%20across%20all%20trials.md): of early-phase solid-tumour drug trials, 10.9% started in 2014–2018 accepted teenagers, against 5.0% started in 2020–2024.
- [Engine cycle 18: do sarcoma trials take teenagers, and who leaves them out?](reports/Engine%20cycle%2018%20-%20do%20sarcoma%20trials%20take%20teenagers%20and%20who%20leaves%20them%20out.md): 88% of Ewing and rhabdomyosarcoma trials accept teenagers, 21% of other sarcoma trials; company-led trials less often (odds ratio 0.30).
- [Contradictions and hidden links in the osteosarcoma literature](reports/Contradictions%20and%20hidden%20links%20in%20the%20osteosarcoma%20literature.md): a knowledge graph of 33,242 papers; where papers disagree, and untested drug → gene → outcome chains (hypotheses).
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
- [For Families](FAMILIES.md): plain-language page for parents and patients, with questions to bring to a care team.
- [All Reports](REPORTS.md): every report and brief, grouped by what you are looking for.
- [Research brief: new targeted-drug trials mostly leave out teenagers with osteosarcoma](briefs/Brief%20-%20trial%20access%20for%20teenagers%20with%20osteosarcoma.md): one page for advocacy groups, from engine cycles 3, 4 and 7.
