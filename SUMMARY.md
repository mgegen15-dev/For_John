# For John: one-page summary

*November 2026. An open, independent analysis of osteosarcoma research, built from public data by a family member working with frontier AI models, then audited claim by claim. Not peer-reviewed yet, and not medical advice. Methods and limits: [HOW_THIS_WAS_MADE.md](HOW_THIS_WAS_MADE.md).*

## Why this exists

Survival for osteosarcoma that has spread or come back has barely changed since the 1980s. A great deal of research exists, but it is scattered across papers, trial registries and grant records. We connected them to look for what has been missed.

## What we found

**Labels:**
- **Confirmed:** checked against original sources and recomputed from data.
- **Lead:** supported by evidence, but needs a scientist to test it.
- **Hypothesis:** a reasoned idea, not yet tested.

1. **Trials mostly fail to finish, not to work.** *Confirmed.*
   - Of 99 osteosarcoma trials that stopped early, 44 stopped mainly for poor recruitment and only about 7–9 for lack of efficacy.
   - About four decades of ClinicalTrials.gov records hold 27 randomized trials devoted to osteosarcoma alone.
   - A Children's Oncology Group preprint of 99 patients finds that only about 1 in 5 stays relapse-free a year after lung metastases are removed, and that modest gains will need randomized trials.
   - [Trials report](reports/Osteosarcoma%20clinical%20trials%20landscape.md)
2. **Kinase-inhibitor pills: active, but briefly.** *Confirmed; who benefits is a Lead.*
   - In relapsed disease, VEGFR2-blocking pills keep roughly 40–50% of patients free of progression at four months, against about 14% for other single drugs, but the effect fades within months. Standard relapse chemotherapy also reaches 42–66%.
   - In open data from 81 tumours at diagnosis, about a quarter carry extra copies of the pills' target genes by a strict definition and nearly half by a looser one (one US cancer-centre cohort reports at least 40%). No study has checked whether those patients are the ones who benefit.
   - Past trials treated about 309 patients with these pills, enough to test whether amplified tumours stay controlled longer on the pill; proving the pill is what helps would need more randomized patients than exist.
   - [Kinase-inhibitor report](reports/Why%20kinase-inhibitor%20pills%20work%20in%20osteosarcoma.md) · [Copy-number report](reports/Copy-number%20changes%20and%20the%20kinase-pill%20biomarker.md)
3. **The weeks after surgery may be the moment to block inflammation, not boost immunity.** *Hypothesis.*
   - In mice, lung tissue triggers IL-1, IL-6 and IL-8 signals that help osteosarcoma colonize the lung, and blocking them reduced metastasis.
   - A canine trial that instead boosted immunity after amputation did worse than historical controls.
   - Approved IL-1 and IL-6 blockers have no registered efficacy trial in osteosarcoma on ClinicalTrials.gov.
   - [Lung metastasis report](reports/Stopping%20lung%20metastasis%20in%20osteosarcoma.md)
4. **FAK and DKK1 are the best-supported untested drug targets.** *Lead.*
   - Blocking either reduced lung metastasis in small mouse studies.
   - Dog programmes for both are listed or planned; their results are not yet public.
   - A screen of 2,400 approved and late-stage drugs adds two weaker ideas, AKT and CXCR4 blockers, both with consistent mouse data and real contradictions.
   - [Brief](briefs/Brief%20-%20pet%20dog%20trial%20of%20FAK%20or%20DKK1%20blockade.md) · [Approved drugs](reports/Approved%20drugs%20worth%20testing%20in%20osteosarcoma.md)
5. **One antibody-drug conjugate slowed relapsed osteosarcoma in a randomized trial, and LRRC15 is now confirmed as protein.** *Lead.*
   - A B7-H3 conjugate beat chemotherapy in a randomized phase 3 in relapse (5.5 against 1.4 months without progression), with heavier side effects. It was one open-label trial in China; whether it helps people live longer is not yet known.
   - Our screen of 88 tumours against 54 normal tissues ranked LRRC15 top; three studies have stained it as protein in patient tumours, and three registered treatment trials target it (one only for relapsed osteosarcoma), plus an imaging study.
   - PTK7 ranked high too, but no series of patient tumours has been stained for it.
   - [Surface targets](reports/New%20surface%20targets%20for%20osteosarcoma.md) · [What's new](reports/Whats%20new%20in%20osteosarcoma%20research.md)
6. **Part of the literature is unreliable.** *Confirmed.*
   - Since 2010, 8.7% of microRNA-type osteosarcoma papers have been retracted, against 1.0% of other papers.
   - We flag which genes' evidence leans on that kind of paper.
   - [Risk flags](reports/Evidence%20risk%20flags%20for%20osteosarcoma%20genes.md)
7. **Funding is thin.** *Confirmed.*
   - NIH spent about $18 million on osteosarcoma-focused grants in 2025. Over 2015–2025 it spent about half as much on osteosarcoma ($108 million) as on neuroblastoma ($212–227 million).
   - The areas flagged above as gaps get the least.
   - [Funding report](reports/NIH%20funding%20for%20osteosarcoma.md)
8. **Testing ideas against data.** *Results.*
   - Since November 24 the project has run 20 research-engine cycles, each planned in writing and committed before its analysis was run. Most were inconclusive or refuted. Of the biological questions, one (MYC and chemotherapy response) met its "Supported" rule, modestly, and needs replication; LRRC15 (cycle 11) met its "Maintained" rule on a measure that proved unstable. The trial counts (cycles 4, 7, 12 and 16–19) are listed in the Research Queue.
   - Early trials of new cancer drugs rarely take teenagers: 78 of 1,434 early-phase solid-tumour trials recruiting or about to recruit accept 12- to 17-year-olds. Across trials of all statuses, those started in 2020–2024 took teenagers half as often as those started in 2014–2018.
   - None of the markers behind the leads was convincingly linked to survival in 89 young patients, in a small study that could miss modest links.
   - [Research Queue](RESEARCH_QUEUE.md) · [Survival test](reports/Do%20the%20leads%20predict%20survival.md)

## What we're asking for

1. **A sarcoma scientist to review this work** and tell us what is wrong or useful.
2. **Groups holding stored samples** from relapsed-osteosarcoma kinase-inhibitor trials (SARC024, REGOBONE, OLIE, OAIE, CABONE, ADVL1622, ITCC-050), to test whether gene amplifications predict benefit.
3. **Comparative oncology groups,** to discuss a post-amputation pet-dog study of IL-1 or IL-6 blockade, and to share what the listed canine FAK studies have shown.
4. **Groups with osteosarcoma tissue arrays,** to stain paired primaries, lung metastases and relapses for LRRC15 and PTK7, and LRRC15 trial sponsors, to publish their screening data.
5. **Trial sponsors** with unreported osteosarcoma trials, to make their results public.
6. **Consortia such as FOSTER and COG,** to use, correct and extend the pooled control dataset.

**Contact:** [open an issue on GitHub](https://github.com/mgegen15-dev/For_John/issues).

**Full ranking of leads:** [Ranked leads and research partners](reports/Ranked%20leads%20and%20research%20partners.md)

*In memory of my little brother and best friend, John.*
