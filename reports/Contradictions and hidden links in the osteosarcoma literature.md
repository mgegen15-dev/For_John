# Contradictions and hidden links in the osteosarcoma literature

*Built November 22, 2026 from the same 33,242 PubMed papers as the literature map (every paper with "osteosarcoma" in its title or abstract), using relations extracted by NCBI's PubTator3 service plus our own sentence-level rules. It is the systematic version of "connecting the dots": a map of which genes and drugs the papers say push which outcomes up or down. Data: `data/osteosarcoma_knowledge_graph_edges.csv` (66,329 edge rows), `data/osteosarcoma_contradictions.csv` (172 pairs reported in both directions), `data/osteosarcoma_hidden_links.csv` (the top 400 of 1,913 drug → gene → outcome chains: the top 300 untested and the top 100 class-tested). Script: `tools/knowledge_graph.py`. Working notes with every PMID: `research_notes/Knowledge graph/notes.md`.*

## Summary

We turned 33,242 osteosarcoma papers into a map of "this gene or drug pushes this outcome up or down", then looked for places where papers disagree and for drug-to-outcome chains nobody has tested. Of the 20 strongest disagreements, half turned out to be our software misreading sentences; the real ones are mostly known two-sided biology (TGF-beta, MYC, beta-catenin, TNF) or lab conditions that differ from the clinic, such as low doses of chemotherapy making cells more mobile in a dish. The one disagreement that changes a project lead is about CXCR4: in mice it drives lung metastasis, but in 223 patients' tumours high CXCR4 and CXCL12 went with a better outcome. Published abstracts point consistently in the direction the IL-6/IL-8, FAK, DKK1 and AKT leads assume: every paper that seemed to point the other way was a misreading. That is agreement in the literature, not a test: this project's own tests found DKK1 RNA did not mark dogs that relapse sooner (engine cycle 13), and more AKT2 RNA leaned towards longer survival in patients, though not after correction for multiple tests (`reports/Do the leads predict survival.md`). The surviving untested chains are hypotheses, not findings; the most useful new ones point to the platelet lead (caplacizumab against von Willebrand factor, abciximab against integrin alpha-v) and to STAT3 (fedratinib), and two warn of possible harm (carbamazepine and emapalumab).

**How to read the labels.** After key numbers we say where they come from:

- **(registry)**: an official database record, such as PubMed's own listings and search counts, ChEMBL's drug mechanisms, ClinicalTrials.gov or an FDA notice.
- **(paper, full text)**: read in the full published paper.
- **(paper, abstract only)**: read only in the abstract.
- **(preprint, abstract only)**: read only in the abstract of a preprint, which has not been peer-reviewed.
- **(press release only)**: from a company announcement, conference coverage or a web listing, with no peer-reviewed paper.
- **(our calculation)**: counted or computed by this project from the files named above.

Everything in this report is (paper, abstract only) or (our calculation) unless marked otherwise: no full texts were read for it.

## What we built

- **Nodes:** genes (with the literature map's corrections for PubTator's known naming mistakes), drugs and other chemicals, and eight outcomes defined from abstract wording: metastasis (including invasion and migration), proliferation (including tumour growth), apoptosis, chemoresistance, survival/prognosis, angiogenesis, stemness and immune evasion.
- **Edges, two layers.** PubTator3, NCBI's text-mining service, supplied 102,827 relations for 18,576 of the papers, labelled positive correlation, negative correlation, association, binding, co-treatment, comparison or drug interaction (registry). PubTator does not tag outcomes such as proliferation or apoptosis, so we added our own sentence-level rules: a gene or drug and an outcome word in the same sentence, with a direction word between them ("promotes", "inhibits") and corrections for "knockdown of", "inhibitor of" and similar. In a hand check of 90 random edges, about two in three (61 of 90) were right (our calculation).
- **Evidence weights:** each paper counts 1, multiplied by 1.5 for each of animal, patient or dog data, and halved for microRNA-type papers (the kind most often retracted) and reviews. Retracted papers are left out.
- **Result:** 66,329 edge rows (56,688 from PubTator, 9,641 sentence-level) linking 5,601 genes, 3,501 chemicals, 1,472 diseases, 655 variants, the 8 outcomes and a general "osteosarcoma" node from PubTator (our calculation).

## Contradictions: where papers point opposite ways

We looked for gene → outcome and drug → outcome pairs reported in opposite directions by at least two non-retracted research papers on each side. **172 pairs qualify**: 151 gene–outcome pairs (99 genes) and 21 drug–outcome pairs (10 drugs) (our calculation). We ranked them by the evidence weight of the weaker side, counted the project's lead genes double, and pushed down genes that are mostly used as read-outs (caspases, BAX/BCL2 and similar). For the top 20 we read the abstracts on both sides and sorted each into one of four kinds:

| Kind | What it means | Top 20 |
|---|---|---|
| Extraction artefact | Our rules misread the sentence, usually a gene named as a step in a drug's pathway, or PubTator gave the wrong gene | 10 |
| Genuine biological context-dependence | The gene really does both, depending on dose, cell state or form | 6 |
| Model difference | Lab conditions or study populations differ (low-dose drug in a dish against the clinic; mice against patients) | 4 |
| Likely error or low-quality side | One side looks wrong or weak | 0 |

*Our calculation, from hand reading (paper, abstract only).*

| Rank | Pair | Papers saying up | Papers saying down | Kind | What is going on |
|---|---|---|---|---|---|
| 1 | MYC → proliferation | 10 | 6 | Artefact | "Rb knockdown and MYC overexpression increased proliferation" read as knockdown of MYC |
| 2 | AKT1 → proliferation | 21 | 7 | Artefact | AKT named as a pathway step in a drug's effect; no abstract reports AKT slowing osteosarcoma growth |
| 3 | TGF-beta1 → proliferation | 11 | 13 | Genuine | Growth inhibition in 1987–1995 culture work (PMIDs 3480288, 7768643) against stimulation and pro-tumour effects later, including canine osteosarcoma (14633705, 24684686) |
| 4 | MYC → apoptosis | 7 | 5 | Genuine | MYC primes drug-induced cell death, yet MYC knockdown also kills osteosarcoma cells (18375382; 19996588) |
| 5 | Doxorubicin → metastasis | 10 | 57 | Model | Low doses made cells more mobile and stem-like in a dish (28454389, 28552603, 38064181); treatment doses reduce metastasis in dogs and mice |
| 6 | Doxorubicin → poor prognosis | 14 | 9 | Artefact | "Poor-prognosis osteosarcoma" describes the patients, not the drug |
| 7 | Cisplatin → apoptosis | 80 | 10 | Artefact | Resistance genes that "inhibit cisplatin-induced apoptosis" |
| 8 | DKK1 → metastasis | 5 | 3 | Artefact | "An antibody against DKK-1 prevented metastasis" misread; one paper is Dickkopf-3, mis-tagged as DKK1 (15087387) |
| 9 | VEGFA → angiogenesis | 34 | 5 | Artefact | Sentences about anti-VEGF therapy; one real nuance, IL-8 rather than VEGF-A drove blood-vessel cell migration in a 3D model (24372172) |
| 10 | Beta-catenin → proliferation | 18 | 8 | Genuine | Wnt/beta-catenin was inactive in 90% of 52 high-grade tumours, and switching it on slowed growth and induced differentiation (19882675); many other papers find the opposite |
| 11 | Methotrexate level → prognosis | 7 | 9 | Model | Higher blood levels went with better outcome in Scandinavian cohorts (12751380) but peaks above 1,500 µM with worse event-free survival in 107 patients at one centre, 58.5% against 75.5% at 5 years (15073863) |
| 12 | Beta-catenin → metastasis | 16 | 7 | Genuine | The beta-catenin blocker ICG-001 slowed cell growth in a dish but, in mice, did not slow the tumour and increased lung spread (34062831); higher cytoplasmic beta-catenin went with less metastasis (24690154) |
| 13 | mTOR → proliferation | 13 | 6 | Artefact | Inhibitor names ("mammalian target of rapamycin") |
| 14 | AKT1 → metastasis | 15 | 5 | Artefact | Pathway-step sentences |
| 15 | Doxorubicin → apoptosis | 74 | 6 | Artefact | Resistance and sensitiser sentences |
| 16 | p53 → proliferation | 6 | 27 | Genuine | The minority is mutant p53, which gains cancer-promoting functions; normal and mutant p53 share one node |
| 17 | CXCL12 → metastasis | 4 | 3 | Model | In 223 untreated tumours, strong CXCL12 and CXCR4 went with a better outcome and fewer metastases (22173290); in mice the pair drives lung metastasis (18071913, 27300512) |
| 18 | TNF → proliferation | 7 | 9 | Genuine | High-dose TNF used to kill tumours in limb perfusion against low-level TNF that feeds osteosarcoma cells (10732774; 2450880) |
| 19 | Cisplatin → metastasis | 8 | 54 | Model | Low concentrations induced a mobile, mesenchymal state in a dish (28105207, 33757752) |
| 20 | Cisplatin → proliferation | 7 | 91 | Artefact | "Cisplatin-induced" phrases; one real effect, cisplatin expanding a tumour-forming stem-like fraction (18332870) |

*Paper counts are our calculation (non-review, non-retracted; one direction per paper). Weights and every PMID are in `data/osteosarcoma_contradictions.csv`; reading notes in the research notes.*

**What the real contradictions say.** Three are worth carrying forward:
- **CXCR4 and CXCL12 in patients** (rank 17). This is the only contradiction that cuts against a project lead (lead 14, CXCR4 blockers). The study's authors suggest that tumour cells making CXCL12 may be held in the bone. Our software missed the CXCR4 half of the same sentence, so CXCR4 itself shows 19 papers for promoting metastasis and 1 against.
- **Beta-catenin** (ranks 10 and 12). Blocking beta-catenin-driven transcription increased lung spread in mice (34062831). This is a caution for any Wnt-blocking idea, and it is indirectly reassuring for DKK1 blockade (lead 4), which releases Wnt signalling rather than blocking it.
- **Low-dose chemotherapy** (ranks 5 and 19). Several groups found that sublethal doxorubicin or cisplatin makes osteosarcoma cells more mobile. This is a lab effect, not a clinical one, but it fits lead 1's argument that treatment can switch on programmes that help metastasis.

**The lead genes outside the top 20.** We also read the minority side for VEGFA → metastasis, AKT1 → apoptosis, FAK (PTK2) → metastasis, MDM2 → proliferation, IL-1beta → proliferation and IL-6 → metastasis. All were misreadings except IL-1beta, which slowed osteosarcoma cell growth while making the cells more bone-like in two 1989 culture studies (2521862, 2786815). That is a growth result, not a lung-colonisation one, so it does not weaken lead 1. For FAK and IL-6 the "against" sentences actually support the lead: FAK *activation* rescued metastasis (42520958), and added IL-6 restored migration (30385323).

## Hidden links: untested drug → gene → outcome chains

This is the Swanson approach, named after the information scientist who in the 1980s linked fish oil to Raynaud's disease by joining two literatures that never cited each other. Here: an approved drug **A** acts on a gene **B**; osteosarcoma papers say **B** moves an outcome **C**; and no osteosarcoma abstract names **A** together with **C**.

- **A → B** comes from ChEMBL's drug-mechanism records for approved drugs (registry), or, at half weight, from PubTator3's counts of papers across all of PubMed reporting that a drug lowers or raises a gene (at least 10 papers, at least 70% in one direction).
- **B → C** comes from this corpus: at least 3 papers on one side and at least 70% of the evidence weight on that side.
- **Not tested** means no osteosarcoma abstract in the corpus names the drug with the outcome. Chains whose mechanism has already been tried with a sibling drug (ranibizumab through bevacizumab, pertuzumab through trastuzumab) are counted separately and not as hidden; the top 100 of them are in the data file.

That gave **1,913 chains across 89 genes and 445 drugs; 972 of them are "class already tested"** (our calculation). We checked the top 30 untested chains in PubMed (`"drug" AND osteosarcoma`, and the same with outcome words) and read the titles that came back (registry, November 22, 2026), then kept 12 and dropped 18. Drops included plicamycin (mithramycin), with 20 or more osteosarcoma papers; drugs off the market; a diagnostic peptide; and chains resting on a confusion, such as calcitonin against the migraine target CGRP, which come from the same gene.

**Every chain below is a hypothesis.** None has been tested in osteosarcoma, and the middle link rests on automated reading of abstracts.

| # | Drug (approved for) | Acts on | Osteosarcoma papers: gene → outcome (for / against) | Direction for patients | PubMed "drug AND osteosarcoma" | Key supporting PMIDs | Note |
|---|---|---|---|---|---|---|---|
| 1 | Capivasertib (breast cancer) | Blocks AKT (registry) | AKT → growth 21 / 7; → metastasis 15 / 5 | Beneficial | 0 | 16142341, 22102563, 20740623 | Already lead 13; all "against" papers were misreadings |
| 2 | Mavorixafor (WHIM syndrome) | Blocks CXCR4 (registry) | CXCR4 → poor survival 7 / 0 | Beneficial | 0 | 26546437, 32314796, 36816176 | Already lead 14; contradicted by 223 patient tumours (22173290) |
| 3 | Nelfinavir (HIV) | Lowers AKT in 40 papers, any disease | AKT → less apoptosis 14 / 3 | Beneficial | 0 | 21617855, 28316059 | Oral, generic; a second route to the AKT chain |
| 4 | Fedratinib (myelofibrosis) | Lowers STAT3 in 13 papers | STAT3 → growth 18 / 2 | Beneficial | 0 | 28423603, 21340507, 20546860 | STAT3 is an orphan target with 308 papers and no trial; ruxolitinib is the same idea |
| 5 | Siltuximab (Castleman disease) | Blocks IL-6 (registry) | IL-6 → growth 4 / 0 | Beneficial | 1 (a computer prediction, 39833053) | 22743617, 26623559 | Fits lead 1; tocilizumab is already named with metastasis in the corpus |
| 6 | Belumosudil (graft-versus-host disease); the chain was found through netarsudil, an eye drop, and belumosudil was substituted by hand as a systemic ROCK inhibitor. Belumosudil acts mainly on ROCK2 (general knowledge), while the chain runs through ROCK1 | Blocks ROCK (registry) | ROCK1 → metastasis 10 / 2 | Beneficial | 0 (fasudil 4, none on metastasis) | 29753317, 33225581 | Weakest: mostly microRNA-type papers, and ROCK1 has a high paper-mill flag; ROCK inhibitors made bone cells *more* mobile in one study (21394446) |
| 7 | Caplacizumab (a clotting disorder, aTTP) | Blocks von Willebrand factor (registry) | VWF → metastasis 3 / 1 | Beneficial | 0 | 33101888, 15467717 | Fits lead 10: in cell experiments, VWF binding platelets' GPIb drove osteosarcoma cell migration and invasion (33101888, abstract only), the step caplacizumab blocks |
| 8 | Abciximab (heart procedures) | Blocks integrin alpha-v/beta-3 and platelet GPIIb/IIIa (registry) | Integrin alpha-v → metastasis 5 / 0 (4 of the 5 papers are about osteosarcoma) | Beneficial | 0 | 12384999, 30691475, 34884541 | Fits lead 10 (the integrin alpha-v row of the repurposing screen scores 76.0, with abciximab its best drug); check whether it is still marketed |
| 9 | Carbamazepine (epilepsy) | Raises P-glycoprotein in 18 papers | P-glycoprotein → poor survival 15 / 0 | **Harmful** | 2 (not about this) | 17088985, 11294418 | A known drug-interaction question for a treating team; not tested here. The link is tumour P-glycoprotein as a marker, not drug-induced P-glycoprotein |
| 10 | Emapalumab (HLH) | Blocks interferon-gamma (registry) | Interferon-gamma → less growth 7 / 3 | **Harmful** | 0 | 1932372, 2121483, 24612598 | Interferon-gamma slows osteosarcoma cells in culture; blocking it could remove a brake. Low practical relevance |

*Paper counts and scores: our calculation. Drug mechanisms: ChEMBL (registry) or PubTator3 counts (our calculation). PubMed counts: registry, November 22, 2026. A third harm-direction chain, omaveloxolone (an NRF2 activator) → NRF2 → metastasis, rests on 3 papers, one of them about thyroid cancer.*

**Reading the table.** The method found the project's two newest repurposing leads (AKT and CXCR4 blockers) as its top two chains by a partly separate route (the same ChEMBL drug mechanisms as the repurposing screen, but outcome evidence from sentence-level reading of abstracts), a weak consistency check. The genuinely new ideas are the two platelet-axis drugs, which strengthen lead 10 with a specific mechanism, and JAK inhibitors as a way to reach STAT3. The two harm-direction chains matter only if a patient is already taking the drug, and the carbamazepine one is known pharmacology rather than a discovery.

## What this means for the ranked leads

Counts are osteosarcoma research papers for / against, after removing reviews and retracted papers (our calculation).

| Lead (from `reports/Ranked leads and research partners.md`) | What the graph says | Verdict (direction of published abstracts, not a test) |
|---|---|---|
| 1. Block IL-1 or IL-6 after surgery | IL-6 → metastasis 7 / 2, and both "against" sentences actually support IL-6 driving migration; IL-6 → poor survival 5 / 0; IL-8 → metastasis 5 / 0. The only contrary IL-1 data are two 1989 culture studies on growth, not lung spread. Low-dose chemotherapy making cells more mobile (above) fits the lead's logic | **Supports** |
| 2. Gene amplification and VEGFR2 pills | VEGF-A → angiogenesis 34 / 5, → metastasis 21 / 3, → poor survival 20 / 1, every minority sentence a misreading. The graph cannot say whether amplification predicts benefit | Consistent, not tested |
| 4. FAK or DKK1 in pet dogs | FAK → metastasis 5 / 2 and DKK1 → metastasis 5 / 3, all minority sentences misreadings. The beta-catenin findings suggest that releasing Wnt signalling, which DKK1 blockade does, is unlikely to promote metastasis | **Supports** |
| 5–6. LRRC15, PTK7 | Too few papers: LRRC15 has 3 sentence-level links and PTK7 none | No information |
| 9. Block CXCR1/2 | IL-8 → metastasis 5 / 0 | Supports, thinly |
| 10. Platelets and metastasis | Two of the surviving hidden links are platelet-axis drugs: caplacizumab (von Willebrand factor) and abciximab (integrin alpha-v and GPIIb/IIIa) | **Supports, adds candidates** |
| 13. AKT blockers | AKT → growth 21 / 7, → metastasis 15 / 5, → less apoptosis 14 / 3; every minority sentence was AKT named as a pathway step. Capivasertib → AKT → growth is the top hidden link. This does not address the lead's real problem: the AKT-cisplatin synergy needed normal p53 (25482935) | **Supports** |
| 14. CXCR4 blockers | Mouse data one-sided (CXCR4 → metastasis 19 / 1), but in 223 untreated patient tumours strong CXCR4 and CXCL12 went with better outcome and fewer metastases (22173290). This patient-level contradiction was added to lead 14 on November 22 | **Contradicts, in patients** |
| Dropped: MDM2 | MDM2 → growth 3 / 3, all inhibitor-sentence misreadings | Nothing new |

**Suggested follow-ups.** The 223-patient CXCR4/CXCL12 result was added to lead 14 on November 22. Caplacizumab and abciximab are noted under lead 10: caplacizumab blocks the VWF–GPIb step that drove osteosarcoma cell migration and invasion in cell experiments (33101888, abstract only); abciximab acts elsewhere on platelets (GPIIb/IIIa) and on integrin alpha-v/beta-3. Read in full the four papers that most change how leads 4, 10 and 14 read: 22173290, 19882675, 34062831 and 33101888.

## Limits

- **Automated relation extraction makes many errors.** In a hand check of 90 random sentence-level links, 61 (68%) were right (our calculation); the first sample of 50 was taken before the last two rule fixes, so the two samples come from slightly different rule versions. The commonest errors: a gene named as a step in someone else's pathway, chains of microRNA "sponges" read the wrong way round, "rescue" and "reverse" sentences, and genes that PubTator names wrongly. We found five new naming errors beyond the literature map's correction table: "p27" tagged as DCTN6, "Dickkopf-3" as DKK1, "TGF-alpha" as TNF, "GLUT-1" as CSE and "HDAC6" as a mouse gene. Single links are unreliable; only patterns across many papers mean anything, and every contradiction and chain reported here was read by hand.
- **Abstracts only.** No full texts were read for this report. An abstract can overstate or leave out the result that matters.
- **Direction is inferred, not measured.** PubTator3's relations are document-level, and its "positive correlation" can mean "is higher in the tumour" as easily as "drives it". Our sentence rules infer direction from words such as "promotes" and "inhibits". Neither distinguishes cause from correlation, a cell line from a patient, or a high dose from a low one.
- **Outcomes are broad.** "Metastasis" includes cell migration and invasion in a dish; "proliferation" includes cell viability; "poor prognosis" includes any association with shorter survival. Normal and mutant p53 share one node.
- **Recall is low.** The rules skip any sentence where another gene sits between the gene and the outcome, so many real findings are missing, such as the CXCR4 half of the 223-patient study.
- **"Not tested" means not in an abstract.** A drug could have been tested in a paper whose abstract does not name it, in a conference abstract or in an unpublished study. The PubMed check covers only the top 30 chains.
- **Hidden links are hypotheses.** A → B links from the wider literature are co-mention counts. B → C links rest on a few papers, some of them microRNA-type papers of the kind most often retracted (ROCK1 especially). A plausible chain is a reason to look, not a reason to treat.
- **Retraction notices slip through.** Notices and corrections have their own PubMed IDs and are not on the retracted list, so a few entered the data (for example 38464341).

## Reproducing this

```
python3 tools/knowledge_graph.py fetch   # PubTator3 relations (about 15 minutes; cache is git-ignored)
python3 tools/knowledge_graph.py build   # edge file and contradictions (offline, about 30 seconds)
python3 tools/knowledge_graph.py abc     # hidden links (PubTator3 and PubMed queries, cached)
```

The hidden-link step uses the ChEMBL download cached by `python3 tools/repurposing_screen.py chembl` in `data/repurposing_raw/`; without it, it falls back to `data/osteosarcoma_repurposing_candidates.csv`.

## Change log

- 2026-11-28: corrected after its first independent check: gene and drug counts (99 genes, 10 drugs, not 151 and 21); two cell-experiment results no longer described as mouse results; the ICG-001 mouse result stated exactly; lead verdicts relabelled as the direction of published abstracts, with the two contrary project tests named; the route to the top chains described as partly shared; the belumosudil substitution disclosed; a treatment-sounding line removed; graph and data-file counts made complete; stale follow-ups updated.
- **November 22, 2026.** First version.
