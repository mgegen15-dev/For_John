# Knowledge graph: working notes

*November 22, 2026. Working notes behind `reports/Contradictions and hidden links in the osteosarcoma literature.md`. Script: `tools/knowledge_graph.py`. Outputs: `data/osteosarcoma_knowledge_graph_edges.csv`, `data/osteosarcoma_contradictions.csv`, `data/osteosarcoma_hidden_links.csv`. Caches (git-ignored): `data/literature/pubtator_relations.jsonl`, `data/literature/kg_abc_cache.json`.*

## 1. Relations from PubTator3

- The relations API worked. `publications/export/biocjson?pmids=...&full=false` returns a `relations` list per document. All 33,242 unique PMIDs were requested in batches of 100 with a 0.4 s pause (about 15 minutes). The corpus file holds 35,078 lines for 33,242 PMIDs; duplicates were dropped, first copy kept.
- Every requested PMID came back. 18,576 papers (56%) carry at least one relation; 102,827 relations in total. Older papers (before about 2005) and papers without abstracts mostly have none.
- PubTator3 returns eight relation types, not the twelve listed in the brief: Association (26,136 paper-level edges after aggregation), Negative_Correlation (15,920), Positive_Correlation (13,083), Cotreatment (788), Bind (438), Comparison (318), Drug_Interaction (5), and Conversion (none here). The brief's inhibit / stimulate / treat / cause / prevent are the older BioRED/CTD names; in PubTator3 they fold into Positive_ or Negative_Correlation.
- Relations are document-level (no sentence or direction of causation), between genes, chemicals, diseases and variants. Gene-gene and chemical-gene pairs are stored as undirected (alphabetical order).
- Outcome nodes from PubTator disease entities: "Neoplasm Metastasis" (MESH:D009362) and "Neoplasm Invasiveness" (D009361) map to `metastasis`; Osteosarcoma, Neoplasms, Sarcoma, Bone Neoplasms and Carcinogenesis map to `osteosarcoma_tumour`. The latter is kept in the edge file but not used for contradictions, because a positive gene-osteosarcoma correlation can mean "expressed in the tumour" as easily as "drives it". PubTator gives no outcome nodes for proliferation, apoptosis, chemoresistance, angiogenesis, stemness or immune evasion, so a second, rule-based layer was needed.
- Gene symbols in relations are corrected with `literature_map.py`'s table: the mention texts of the same document decide what each PubTator symbol becomes (majority vote), so "protein kinase B" tagged PTK2B becomes AKT1 in that paper only.

## 2. The sentence layer (our extraction)

Rules are in the module docstring and in `sentence_edges()`. In short: within one sentence that names a gene or chemical (PubTator mention texts, corrected symbols) and an outcome keyword, a trigger word between them sets the sign; knockdown/inhibitor/antibody/"loss of" words around a gene flip it; a verb acting on the gene ("curcumin inhibited AKT and reduced proliferation") also flips it. Pairs are skipped when another gene or drug sits between the two (the named entity is then usually not the agent), when a pathway is named as a mediator ("via the PI3K/AKT pathway") without a verb acting on it, when a negation or "minimal/little" sits in the gap, and when the gap contains "-induced / -mediated / effect of / rescued / restored". Prognosis edges need an association word plus "poor/shorter/unfavourable ... survival/prognosis/outcome" (sign +) or "better/longer/favourable ..." (sign −). Titles count 1.5x. One sign per paper per pair (majority of its sentences).

Iterations. The first pass gave AKT1 → proliferation 33 up and 71 down; reading the "down" sentences showed almost all were AKT named as a mediator of a drug's effect. The mediator, between-entity, pathway, "reduced stimulation" (adjective-on-noun trigger) and knockdown-word fixes reduced the sentence layer to 6,738 gene → outcome and 2,903 chemical → outcome edge rows (from 7,962 papers) and cut most of those artefacts, at a cost in recall.

**Hand check of precision.** Two random samples of sentence-layer gene → outcome edges (seeds 20261122 and 7; 50 and 40 edges) were judged against the sentence:
- Sample 1 (before the last two fixes): 34 of 50 correct (68%). Errors: wrong entity from PubTator normalisation (p27 tagged DCTN6 twice; HDAC6 inhibitor tagged 9930021J03RIK), miRNA/lncRNA "sponge" chains read the wrong way (MALAT1, E2F3), "X knockdown decreased ..." double-flipped (RUNX3, SOX18; fixed afterwards), "target both PI3K and mTOR" not flipped, T-cell and NK-cell contexts, "good performance in survival prediction" read as good prognosis (fixed afterwards).
- Sample 2 (after the fixes): 27 of 40 correct (68%). Errors: antisense oligonucleotide not recognised as a flip (TNKS), "rescued the decreased ... induced by ROCK2 knockdown", "increased resistance to cell death" read as more apoptosis, GLUT-1 tagged as CSE, "Rac1 increased in tissues" read as prognosis, ceRNA sentences.
- So roughly **two in three sentence-layer edges are right** (61 of 90, 68%; our calculation). Single edges are unreliable; only aggregates over many papers mean anything, and every contradiction below was read by hand.

Other PubTator normalisation errors met while reading (not in the correction table): "p27" → DCTN6 (should be CDKN1B); "Dickkopf 3" → DKK1 (15087387); "TGF-alpha" → TNF (24685520); "GLUT-1" → CSE; "HDAC6" → 9930021J03RIK (a mouse gene). They are worth adding to `literature_map.py`'s table in a later pass; they were not added here so the gene table stays comparable with the literature map.

## 3. Evidence weights

Per paper: 1.0, times 1.5 each for in vivo, patient and dog tags, times 0.5 for a microRNA-type (ncrna) paper, times 0.5 for a review; retracted papers (PubMed list) are excluded entirely. Reviews are kept in the edge file but excluded from contradiction and hidden-link scoring. Note that retraction *notices* and corrigenda have their own PMIDs and are not on the retracted list, so a few slip in (e.g. 38464341, "[Retracted] miR-133b ...", 33901310 a retraction notice for an ASBEL lncRNA paper).

## 4. Contradictions

Definition: a gene or ChEMBL phase 3-4 drug and one of the eight outcomes, with at least 2 non-review, non-retracted papers on each side. 172 pairs qualify (151 gene, 21 drug; our calculation). Score = the evidence weight of the weaker side; lead genes count double and read-out markers (caspases, BAX/BCL2, MMPs, cadherins, cyclins and similar) count 0.3, so the top 20 is not filled with apoptosis read-outs. Every top-20 pair was read by hand (minority side in full, majority side in part). Classifications are stored in `CLASSIFICATION` in the script and written to the CSV.

| Rank | Pair | Papers up (weight) | Papers down (weight) | Classification |
|---|---|---|---|---|
| 1 | MYC → proliferation | 10 (14.1) | 6 (8.8) | extraction artefact |
| 2 | AKT1 → proliferation | 21 (28.3) | 7 (8.5) | extraction artefact |
| 3 | TGFB1 → proliferation | 11 (14.8) | 13 (15.5) | genuine biological context-dependence |
| 4 | MYC → apoptosis | 7 (8.5) | 5 (6.6) | genuine biological context-dependence |
| 5 | doxorubicin → metastasis | 10 (13.0) | 57 (87.5) | model difference |
| 6 | doxorubicin → poor prognosis | 14 (17.4) | 9 (12.3) | extraction artefact |
| 7 | cisplatin → apoptosis | 80 (96.4) | 10 (12.1) | extraction artefact |
| 8 | DKK1 → metastasis | 5 (7.3) | 3 (6.0) | extraction artefact |
| 9 | VEGFA → angiogenesis | 34 (46.5) | 5 (6.0) | extraction artefact |
| 10 | CTNNB1 → proliferation | 18 (20.8) | 8 (10.9) | genuine biological context-dependence |
| 11 | methotrexate → poor prognosis | 7 (10.5) | 9 (12.5) | model difference |
| 12 | CTNNB1 → metastasis | 16 (17.1) | 7 (10.0) | genuine biological context-dependence |
| 13 | MTOR → proliferation | 13 (17.3) | 6 (10.0) | extraction artefact |
| 14 | AKT1 → metastasis | 15 (19.5) | 5 (4.8) | extraction artefact |
| 15 | doxorubicin → apoptosis | 74 (94.5) | 6 (9.4) | extraction artefact |
| 16 | TP53 → proliferation | 6 (9.3) | 27 (37.5) | genuine biological context-dependence |
| 17 | CXCL12 → metastasis | 4 (6.3) | 3 (4.5) | model difference |
| 18 | TNF → proliferation | 7 (8.9) | 9 (14.0) | genuine biological context-dependence |
| 19 | cisplatin → metastasis | 8 (8.5) | 54 (83.5) | model difference |
| 20 | cisplatin → proliferation | 7 (8.5) | 91 (136.3) | extraction artefact |

Tally: 10 extraction artefacts, 6 genuine context-dependence, 4 model differences, 0 where one side looked like an error or a low-quality paper (our calculation). Paper-mill-type papers did appear on minority sides (e.g. 30844369, 37237370), but in every case the sentence was also misread, so "artefact" is the better label.

Reading notes on the ones that are real (PMIDs; all abstract only):
- **TGF-beta1 → proliferation.** Growth inhibition of MG-63 and rat osteoblastic osteosarcoma cells in 1987-1995 culture work (3480288, 2246323, 7768643) against stimulation of MG-63 proliferation (14633705, 2003) and pro-tumorigenic effects in canine osteosarcoma (24684686). The "down" side is almost all pre-1996 culture experiments; recent in vivo work points the other way. Classic dose- and cell-state-dependent TGF-beta biology.
- **MYC → apoptosis.** MYC primes drug- and stress-induced apoptosis (18375382, 26528706, 9218867), and MYC knockdown also raises apoptosis in osteosarcoma cells (19996588, 33125136). Both are textbook MYC.
- **beta-catenin (CTNNB1).** Nuclear beta-catenin was absent in 90% of 52 high-grade biopsies and all four lines tested, and activating the pathway reduced growth and induced differentiation (19882675, J Pathol 2010). The beta-catenin/CBP blocker ICG-001 cut proliferation in vitro but increased lung dissemination in a mouse model (34062831, 2021). Genistein-raised cytoplasmic beta-catenin went with less LM8 metastasis (24690154). Many other papers report beta-catenin driving growth and metastasis. This is a genuine, unresolved disagreement, and the ICG-001 result is a warning for anyone proposing Wnt blockade against metastasis.
- **CXCL12/CXCR4 → metastasis.** In 223 pre-treatment osteosarcoma samples, strong CXCL12 and CXCR4 expression went with a better long-term outcome and fewer metastases (22173290, Mod Pathol 2012); the authors suggest CXCL12-expressing tumour cells may be held in bone. Mouse models show CXCL12/CXCR4 driving lung metastasis (18071913, 27300512). Note: our extraction missed the CXCR4 half of 22173290 ("better long-term outcome": the hyphen defeats the regex), so CXCR4 itself shows 19 papers for and 1 against and no contradiction row. This is a real contradiction for lead 14.
- **TNF → proliferation.** High-dose TNF as a cytotoxic agent in isolated limb perfusion in rats (10732774, 7779705) against low-level TNF stimulating osteosarcoma cells and keeping them undifferentiated (2450880, 24336323). Dose and setting, not a conflict.
- **TP53 → proliferation.** The minority is mutant p53 gain-of-function (24373920, 16778209, 35320355). The node merges wild-type and mutant p53.
- **Chemotherapy → metastasis (doxorubicin, cisplatin).** Low or sublethal concentrations induced EMT, migration and stemness in vitro (doxorubicin 28454389, 28552603, 38064181; cisplatin 28105207, 33757752), and cisplatin expanded a tumorigenic side population via VEGF/FLT1 (18332870). Therapeutic doses reduce metastasis in dogs and mice. Low-dose in vitro exposure is not the clinical setting, but it is a recurring mechanism that fits lead 1's idea that treatment-induced inflammation may help metastasis.
- **Methotrexate exposure → prognosis.** Higher serum methotrexate went with better outcome in Scandinavian Sarcoma Group cohorts (12751380: 24-h level above 4.5 microM an independent favourable factor; 1622872), while in 107 single-institution patients mean peak levels above 1,500 microM went with worse 5-year event-free survival, 58.5% against 75.5% (15073863). Different exposure ranges and cohorts.

Lead genes outside the top 20, read the same way: VEGFA → metastasis (rank 23), AKT1 → apoptosis (22), PTK2/FAK → metastasis (26), MDM2 → proliferation (36), IL1B → proliferation (66), IL6 → metastasis (67). All minority sides were artefacts except IL-1beta, which inhibited osteosarcoma cell proliferation while inducing an osteoblastic phenotype in two 1989 culture studies (2521862, 2786815). For FAK the only "against" papers are a sentence where FAK *activation* rescued metastasis (42520958, which supports FAK) and a methods sentence (29849782). For IL-6 both "against" sentences ("Irisin reverses the IL-6 induced EMT", 29048621; "rIL-6 can attenuate G-1 suppressed migration", 30385323) actually support IL-6 promoting migration. CXCR4, CXCL8, IL1A, CCNE1 and KDR had no outcome reported in both directions by two or more papers. LRRC15 has 3 sentence-level edges in total and PTK7 none, so the graph says nothing about either.

## 5. Hidden links (A → B → C)

Construction (`abc_candidates()` and `abc()`):
- **B → C** from this corpus: a gene and outcome with at least 3 non-review papers on the dominant side and at least 70% of the evidence weight on that side. Read-out markers (the `READOUT` set) and TP53 (wild-type and mutant merged) are excluded as middle links.
- **A → B**, two sources. (1) ChEMBL mechanisms of approved (max_phase 4) therapeutic drugs, from the repurposing screen's cached ChEMBL download (`data/repurposing_raw/`): inhibitor/antagonist/blocker = −, agonist/activator/opener = +; partial agonists are left out because ChEMBL files plerixafor, a CXCR4 blocker in practice, as one; mutant-only drugs, diagnostics and complexes of more than 5 proteins are dropped. (2) The broad PubMed literature: for each B gene, PubTator3's `relations?e1=@GENE_x&e2=Chemical` counts; an approved, oral or injectable drug with at least 10 papers of `negative_correlate` (or `positive_correlate`) and at least 70% of the directional papers in that direction is linked (2,091 links added). Literature-derived chains count half, because co-mention is weaker evidence than pharmacology.
- **"No direct link"**: the drug's names (ChEMBL preferred name and synonyms, salt words stripped) must not appear in any non-retracted osteosarcoma abstract that also names the outcome. 1,559 drugs, 506 of them named somewhere in the corpus, gave 1,913 chains across 89 genes and 445 drugs (our calculation).
- **"Class already tested"**: another drug with the same ChEMBL target is named with that outcome in an osteosarcoma abstract, or the target is in the curated osteosarcoma trial drug map. 972 of the 1,913 chains are in this group (ranibizumab via bevacizumab, pertuzumab via trastuzumab, and so on). They are kept in the CSV at a 0.3 weight but not sent to the PubMed check, because the mechanism is not hidden.
- **Score** = B → C dominant-side weight × consistency ÷ √(number of the drug's targets), × 0.5 if the drug is named anywhere in the corpus, × 0.3 if the class was tested, × 0.5 for literature-derived A → B, × (1 + 0.25 log10(1 + broad-literature drug-gene papers)).
- **Check**: the top 30 untested chains (one per gene-outcome-direction, at most 3 per gene and 2 per drug) were searched in PubMed as `"drug" AND osteosarcoma` and `"drug" AND osteosarcoma AND (outcome words)`, titles inspected, and each kept or dropped by hand (`ABC_REVIEW` in the script). 12 kept, 18 dropped. Extra PubMed checks on November 22, 2026: belumosudil 0, fasudil 4 (none on metastasis; 21394446 shows ROCK inhibitors *stimulating* migration of osteoblastic cells), ruxolitinib 3 (none an osteosarcoma experiment), fedratinib 0, nelfinavir 0, tocilizumab 6, siltuximab 1 (a bioinformatic prediction, 39833053), capivasertib 0, mavorixafor 0, caplacizumab 0, abciximab 0, emapalumab 0 (registry).

Dropped (18): plicamycin/mithramycin (20 PubMed osteosarcoma papers, not hidden), telaprevir (off the market; P-gp reversal), certolizumab and isoniazid via TNF (TNF-as-cytotoxic artefact), guselkumab via IL-12/23 (evidence is IL-12 given as therapy), ceruletide (diagnostic), givinostat (HDAC-inhibitor class tested, valproate), aluminium hydroxide (adjuvant), fremanezumab via CALCA (calcitonin vs CGRP), liothyronine via HIF1A (weak), probucol (withdrawn in the US), vemurafenib via ERK (mutant-context), seladelpar via ALP (alkaline phosphatase is a marker), and duplicate rows of these.

Supporting B → C papers read for the survivors (titles; abstract only):
- VWF → metastasis: "von Willebrand factor promotes platelet-induced metastasis of osteosarcoma through activation of the VWF-GPIb axis" (33101888); VWF expression in osteosarcoma metastasis (15467717). Caplacizumab blocks exactly the VWF-GPIb binding.
- ITGAV → metastasis: integrin alpha-v overexpression promotes migration (12384999), alphavbeta3 prognostic in primary tumours (30691475), CCL4 via alphavbeta3 (34884541); 40018050 is a digestive-cancer paper that entered the corpus.
- STAT3 → proliferation: mesenchymal stem cells promote osteosarcoma growth and metastasis via STAT3 (28423603, 27340780), small-molecule STAT3 inhibitors suppress tumour growth in mice (21340507), STAT3 expression prognostic (20546860).
- IL6 → proliferation: MSC-derived IL-6 activates STAT3 and promotes proliferation and metastasis (22743617, 20874851); IL-6 suppression reduces tumour self-seeding in mice (26623559).
- CXCR4 → poor prognosis: 6 patient papers and a meta-analysis (36816176) against one 223-sample study pointing the other way (22173290).
- ROCK1 → metastasis: mostly lncRNA/miRNA "sponge" papers (29753317, 33225581, 32863912, 32660450); ROCK1 has a high paper-mill flag. Weakest of the kept chains.
- NFE2L2 → metastasis: eIF4A inhibition blocks NRF2 synthesis and prevents osteosarcoma metastasis (39078310); one supporting paper (32891613) is about thyroid cancer.

## 6. Cross-check against the ranked leads

Counts are papers (non-review, non-retracted) for / against, both layers combined, one sign per paper; our calculation.
- **Lead 1 (IL-1/IL-6 after surgery): supported.** IL6 → metastasis 7 / 2, and both "against" sentences actually support IL-6 promoting migration; IL6 → poor prognosis 5 / 0; CXCL8 → metastasis 5 / 0; IL1A → metastasis 1 / 0. The only IL-1 contrary evidence is two 1989 culture studies where IL-1beta slowed growth while inducing differentiation (2521862, 2786815), which does not address lung colonisation. The chemotherapy contradictions add a related point: sublethal doxorubicin and cisplatin induce EMT and migration in vitro (28454389, 28552603, 28105207, 33757752), consistent with the idea that treatment can switch on pro-metastatic programmes.
- **Lead 2 (amplification and VEGFR2 pills): consistent, not tested.** VEGFA → angiogenesis 34 / 5, → metastasis 21 / 3, → poor prognosis 20 / 1; every minority sentence read was an artefact. KDR has only 11 sentence-level paper edges. MYC → proliferation is consistent once artefacts are removed; MYC → apoptosis runs both ways, which is normal MYC biology. Nothing here says whether amplification predicts benefit.
- **Lead 4 (FAK, DKK1): supported, with one indirect point in DKK1's favour.** PTK2 → metastasis 5 / 2 and DKK1 → metastasis 5 / 3, all minority sentences artefacts (including Dickkopf-3 mis-tagged as DKK1). The genuine beta-catenin contradiction bears on DKK1, a Wnt inhibitor: high-grade osteosarcoma has a largely inactive Wnt pathway whose activation reduced growth and induced differentiation (19882675), and blocking beta-catenin-dependent transcription with ICG-001 increased lung dissemination in mice (34062831). If that holds, releasing Wnt by blocking DKK1 is at least not expected to promote metastasis. The opposite older finding the literature map lists (24859848, DKK1 overexpression potentiating oridonin) is a proliferation result.
- **Leads 5 and 6 (LRRC15, PTK7): no information.** LRRC15 has 3 sentence-level edges and PTK7 none.
- **Lead 9 (CXCR1/2): supported.** CXCL8 → metastasis 5 / 0. CXCR2 has only 2 sentence-level edges, neither on metastasis.
- **Lead 10 (platelets): new support.** Two of the surviving hidden links are platelet-axis drugs: caplacizumab (VWF → metastasis, 33101888 shows VWF-GPIb-driven platelet-induced metastasis) and abciximab (ITGAV → metastasis).
- **Lead 13 (AKT blockers): supported by the graph, and the contradiction is an artefact.** AKT1 → proliferation 21 / 7, → metastasis 15 / 5, → apoptosis 3 / 14 (that is, AKT lowers apoptosis); every minority sentence read was AKT named as a pathway mediator. Capivasertib → AKT1 → proliferation is the top-scoring surviving hidden link, and nelfinavir (an oral generic HIV drug reported to lower AKT in 40 papers) is an alternative route to the same chain. This does not answer lead 13's real problem, the p53-dependence of the AKT-cisplatin synergy (25482935).
- **Lead 14 (CXCR4 blockers): contradicted in patients.** Mouse data are one-sided (CXCR4 → metastasis 19 / 1), but in 223 pre-treatment tumours strong CXCR4 and CXCL12 expression went with a better outcome and fewer metastases (22173290). Lead 14 already lists primary-growth (27300512), T-cell (29735547) and CXCR7 (28468584) contradictions; this patient-level one is not in the leads page and should be.
- **Dropped MDM2 lead: nothing new.** MDM2 → proliferation 3 / 3 and → apoptosis are inhibitor-sentence artefacts.
- **STAT3 (an orphan target in the literature map):** a new hidden link, fedratinib (JAK2 inhibitor) → STAT3 → proliferation, with STAT3 → proliferation 18 / 2.

## 7. What I would do next

1. Add the five new mis-normalisations (p27, Dickkopf-3, TGF-alpha, GLUT-1, HDAC6) to `literature_map.py`'s correction table, and split TP53 into wild-type and mutant mentions.
2. Replace the rule-based sentence layer with a trained relation model, or ask PubTator3 for outcome-type entities if it gains them; at about 68% precision, single edges are not usable.
3. Add the CXCL12/CXCR4 patient finding (22173290) to lead 14 in `reports/Ranked leads and research partners.md`.
4. Read the full text of 22173290, 19882675, 34062831 and 33101888, the four papers that most change how leads 4, 10 and 14 read.

## Change log

- **November 22, 2026.** First version.
