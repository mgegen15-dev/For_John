# For John: one-page summary

*November 2026. An open, independent analysis of osteosarcoma research, built from public data by a family member working with AI research assistants, then audited claim by claim. Not peer-reviewed yet, and not medical advice. Methods and limits: [HOW_THIS_WAS_MADE.md](HOW_THIS_WAS_MADE.md).*

## Why this exists

Survival for osteosarcoma that has spread or come back has barely changed since the 1980s. A great deal of research exists, but it is scattered across papers, trial registries and grant records. We connected them to look for what has been missed.

## What we found

**Labels:**
- **Confirmed:** checked against original sources and recomputed from data.
- **Lead:** supported by evidence, but needs a scientist to test it.
- **Hypothesis:** a reasoned idea, not yet tested.

1. **Trials mostly fail to finish, not to work.** *Confirmed.*
   - Of 99 osteosarcoma trials that stopped early, 44 stopped mainly for poor recruitment and only about 7–9 for lack of efficacy.
   - Across about four decades there have been 27 randomized trials devoted to osteosarcoma alone.
   - Several large trials have never reported results.
   - [Trials report](reports/Osteosarcoma%20clinical%20trials%20landscape.md)
2. **One drug class clearly beats the benchmark, briefly.** *Confirmed; who benefits is a Lead.*
   - In relapsed disease, VEGFR2-blocking kinase-inhibitor pills keep roughly 40–50% of patients free of progression at four months, against about 14% for other drugs.
   - The effect fades within months.
   - About 40% of tumours carry extra copies of the genes these pills target, but no study has checked whether those patients are the ones who benefit.
   - That can be tested with samples already stored from past trials.
   - [Pooled controls](reports/Osteosarcoma%20pooled%20control%20dataset.md) · [Kinase-inhibitor report](reports/Why%20kinase-inhibitor%20pills%20work%20in%20osteosarcoma.md)
3. **The weeks after surgery may be the moment to block inflammation, not boost immunity.** *Hypothesis.*
   - In mice, lung tissue triggers IL-1, IL-6 and IL-8 signals that help osteosarcoma colonize the lung, and blocking them reduced metastasis.
   - A canine trial that instead boosted immunity after amputation did worse than historical controls.
   - Approved IL-1 and IL-6 blockers have no registered efficacy trial in osteosarcoma.
   - [Lung metastasis report](reports/Stopping%20lung%20metastasis%20in%20osteosarcoma.md)
4. **FAK and DKK1 are the best-supported untested drug targets.** *Lead.*
   - Blocking either reduced lung metastasis in mice.
   - Dog programmes for both already exist or are planned.
   - [Brief](briefs/Brief%20-%20pet%20dog%20trial%20of%20FAK%20or%20DKK1%20blockade.md)
5. **New surface targets for antibody drugs.** *Lead.*
   - Comparing 88 patient tumours with 54 normal tissues ranked LRRC15 and PTK7 near the top.
   - A radioactive anti-LRRC15 antibody trial for relapsed osteosarcoma is already recruiting.
   - PTK7 has antibody-drug conjugates in trials for other cancers, but almost no osteosarcoma research.
   - [Surface targets](reports/New%20surface%20targets%20for%20osteosarcoma.md)
6. **Part of the literature is unreliable.** *Confirmed.*
   - Since 2010, 8.7% of microRNA-type osteosarcoma papers have been retracted, against 1.0% of other papers.
   - We flag which genes' evidence leans on that kind of paper.
   - [Risk flags](reports/Evidence%20risk%20flags%20for%20osteosarcoma%20genes.md)
7. **Funding is thin.** *Confirmed.*
   - NIH spent about $18 million on osteosarcoma-focused grants in 2025, about half of what neuroblastoma received over the decade.
   - The areas flagged above as gaps get the least.
   - [Funding report](reports/NIH%20funding%20for%20osteosarcoma.md)

## What we're asking for

1. **A sarcoma scientist to review this work** and tell us what is wrong or useful.
2. **Groups holding stored samples** from relapsed-osteosarcoma kinase-inhibitor trials (SARC024, REGOBONE, OLIE, OAIE, CABONE, ADVL1622), to test whether gene amplifications predict benefit.
3. **Comparative oncology groups,** to discuss a post-amputation pet-dog study of IL-1 or IL-6 blockade, and to share what existing canine FAK studies have shown.
4. **Trial sponsors** with unreported osteosarcoma trials, to make their results public.
5. **Consortia such as FOSTER and COG,** to use, correct and extend the pooled control dataset.

**Contact:** [open an issue on GitHub](https://github.com/mgegen15-dev/For_John/issues).

**Full ranking of leads:** [Ranked leads and research partners](reports/Ranked%20leads%20and%20research%20partners.md)

*In memory of my little brother and best friend, John.*
