# Audit F: research engine (cycles 1–20), the teen-access brief and the public pages

*Independent AI review passes on November 26 and 27, 2026. Each reviewer worked read-only, did not write the files it checked, and recomputed numbers from the repository's data files and raw downloads. This record summarises each pass: its scope, every finding in one line, and how the finding was resolved. The fixes are in commits `762cbbb` (pass F1; `21d13c9` before the November 27 history rewrite) and `b9a8710` (passes F2–F4), and in each affected file's change log.*

## Pass F1, November 26: engine cycles 10–17, the brief's new line, front page, queue, predictions, audit guide

**Scope:** cycles 10–17 reports, pre-registrations, scripts and outputs; P29–P48; queue rows 21–30; audit rows E6–E12; front page; the brief's "wider pattern" line. **Result:** 25 findings, all resolved.

- ERROR: cycle 12, trial NCT07477457 (OstEvo) misread as newly diagnosed only; it has a relapse cohort. Now 58 relapse trials, 44 accepting teenagers, 32 with a US site.
- OVERSTATEMENT: "trials built for osteosarcoma" changed to "trials that list osteosarcoma"; many are wider sarcoma or childhood-cancer trials.
- ERROR: 40, not 41, solid-tumour trials start under 12; one registry age entry is an error ("18 Days" to "75 Days").
- MINOR: "anyone under 18" changed to "12- to 17-year-olds", matching the definition.
- INCONSISTENCY: phase 2/3 trials entered Set B (cycles 12 and 17); declared as deviations. No conclusion changes.
- MINOR: "recruiting" changed to "recruiting or not yet recruiting" where applicable.
- MINOR: NCT05830123 described as mainly osteosarcoma with other sarcomas eligible.
- MINOR: NCT07773454 noted as not yet open, with no sites.
- MINOR: the hand reading is attributed to a single AI reader.
- OVERSTATEMENT: cycle 11, LRRC15 changed to "no clear drop"; the pre-registered sensitivity result (−0.42) added.
- MINOR: cycle 11, post-hoc stability checks saved to `data/engine/cycle11/posthoc_checks.json`.
- ERROR: cycle 13, "DKK1 and PTK2 unchanged by either" corrected; the sensitivity check covered only the inflammation score.
- OVERSTATEMENT: cycle 13, the DKK1 selection claim narrowed to these dogs and to outcome under standard treatment.
- MINOR: cycle 13, arrays per dog stated correctly (50 dogs with two, 9 with one).
- MINOR: cycle 13, a note on download order added.
- MINOR: cycle 14, "no sign of it" changed to "little or none of it".
- Cycle 17, minor:
  - the adult-type definition now includes trials with no stated minimum age;
  - the 144 withdrawn records are described exactly;
  - "first-in-human" changed to "company-led".
- MINOR: cycle 16, the FDA guidance description aligned with the brief.
- MINOR: cycle 12, the rounding of the rule-against-reading difference corrected.
- MINOR: front page, "lost 9p21" changed to "lost CDKN2A (part of 9p21)".
- MINOR: cycle 10, MG-63's other pill results added.
- MINOR: cycle 10, the cycle 6 comparison qualified as "across all cancers".
- UNVERIFIED: queue row 25 wording, later reworded in F3.

## Pass F2, November 27: engine cycles 1–9

**Scope:** cycles 1–9 reports, pre-registrations, scripts and outputs; P15–P28; queue rows 1–20; audit rows E1–E5. All 60 cycle 4 trials and all 21 cycle 7 trials read were checked against raw registry records. **Result:** 19 findings, all resolved.

- INCONSISTENCY (fed the brief): cycle 7 counted NKT5097 (NCT07029399), which neither requires CCNE1 amplification nor tests a PKMYT1 inhibitor. Corrected: 8 trials (not 9), 5 with a US site (not 6). The brief now gives 33 trials in total (not 34), 30 others starting at 18 or older besides the three trials named in the brief (not 31), and 31 of 33 at phase 1 or 1/2.
- ERROR: cycle 8, PELO was tested in the knockdown screen (8 lines) and did not replicate. It did not "have too few lines".
- ERROR: cycle 8 recovered CCNE1 with CDK2, not cycle 6's PKMYT1 pair.
- ERROR: cycle 9, two lines (not three) were called intact for TP53; OS384 was caught by deletion.
- ERROR: cycle 6, G292 is not a low-CCNE1 line; the comparison lines are now described as "not amplified".
- INCONSISTENCY: cycle 7 contradicted cycle 4 on under-18 MTAP trials (one existed, in China).
- OVERSTATEMENT: cycle 5's summary now states that the primary measure leaned the opposite way.
- OVERSTATEMENT: cycle 3's "the deletion is set early and stays" softened; 2 of 7 patients with the deletion differed between samples.
- OVERSTATEMENT: cycle 4, "MTAP or CDKN2A deletion" narrowed to MTAP loss; "small protocol decisions" removed.
- Cycle 4, minor:
  - the search-term breakdown corrected;
  - one trial lists no sites;
  - one trial does not require MTAP loss.
- MINOR: cycle 7, "hospital tests" corrected; one of the three cohorts is a research trial.
- MINOR: cycle 9, the description of the RB1 hits and the ALT share corrected.
- MINOR: rounding in cycles 1, 5, 8 and 9 aligned with the output files.
- MINOR: cycle 1, the GSE39058 / GSE39055 relationship explained in the pre-registration.
- MINOR: cycle 1, probe percentiles corrected (53rd to 78th).
- MINOR: cycle 2, "no difference" changed to "no clear difference".
- PROCESS: for cycles 4–9, the Deviations sections were committed together with the results; this is stated in the audit guide.
- Not resolved, noted: cycle 8's automatic P25 flag reads false while P25 is recorded as ambiguous.
- Not resolved, noted: some literature identifiers were not re-checked online.

## Pass F3, November 27: engine cycles 18–20 and the F1 fixes

**Scope:** cycles 18–20; verification that every F1 fix was applied everywhere; P49–P55; the scorecard. **Result:** 22 findings, all resolved.

- ERROR: cycle 12, 19 relapse trials (not 18) have osteosarcoma in the title.
- OVERSTATEMENT: cycle 19, NCT04616560's 22 states include suspended sites; it recruits in 17. P53 is "right by its rule".
- ERROR: cycle 20, T-cell interval 0.55 (not 0.56).
- ERROR: cycle 20, GSE14827 was not in cycle 14; corrected, with a deviation note.
- INCONSISTENCY: cycle 20 now reports random effects, has a download-order note and shows its figure.
- MINOR: cycle 20, the scale of the score stated.
- MINOR: cycle 20, CD68 flagged as exploratory.
- OVERSTATEMENT: cycle 18, the within-"other sarcoma" gap marked borderline; 8 trials there are not bone or soft-tissue sarcomas.
- MINOR: cycle 18, company-led shares stated exactly.
- INCONSISTENCY: old LRRC15 wording updated in README and REPORTS.
- INCONSISTENCY: cycle 11, B4GALNT1 and ADAM12 immune-only readings added.
- MINOR: "supporting datasets" changed to "sensitivity datasets".
- INCONSISTENCY: cycle 16, phase 2/3 deviation declared (odds ratio 0.18 without them).
- MINOR: cycle 13, the limits wording aligned.
- MINOR: cycle 12, the figure's basis stated.
- MINOR: state counts now 33 states and DC.
- MINOR: "anyone under 18" in the cycles 4 and 7 summary changed to "patients under 18 (both from age 12)".
- MINOR: brief header dates.
- MINOR: cycle 10, AUC 1.0 for sorafenib and regorafenib.
- MINOR: data manifest out of date.
- ERROR: 36 broken report links on the All Reports page, present since version 1.1. The site builder now resolves links to site pages and files.
- MINOR: scorecard footnote.

## Pass F4, November 27: public pages and top-level documents

**Scope:** front page, For Families, the teen-access brief and its PDF, audit guide (including the history rewrite), README, REPORTS, HOW_THIS_WAS_MADE, research queue, data manifest, site integrity, wording rules. **Result:** 25 findings, all resolved except where noted.

- ERROR: broken links on the All Reports, For Families and brief pages (same cause as F3); fixed in the site builder.
- MINOR: links to raw-data folders that are not in git; the builder now links only tracked paths.
- ERROR: the software requirements described wrongly in HOW_THIS_WAS_MADE, README and `requirements.txt`.
- ERROR: the cycle 19 summary corrected to 33 states and DC.
- OVERSTATEMENT: the audit guide's "only counts are published" narrowed; the open-access TARGET-OS per-patient table remains, as in version 1.0.
- FREEZE PREPARATION: freeze references updated; version 1.1 tagged on November 27 at `b9a8710`.
- FREEZE PREPARATION: the data manifest updated; it no longer lists its own changing checksum file.
- OVERSTATEMENT: the audit description in HOW_THIS_WAS_MADE and README now says the audits were run by AI and lists the November 25–27 passes.
- MINOR: the audit guide's report count (36) and a typo corrected.
- MINOR: the history-rewrite paragraph now notes signed commits after the rewrite and the need to re-clone.
- MINOR: the front-page date, the social-media description and the queue date updated.
- OVERSTATEMENT: front page, "halved since 2019" now names the two trial sets compared.
- MINOR: front page, "1.3 million gene comparisons in all", with a cycle 9 link.
- OVERSTATEMENT: "relapsed tumours on clinical gene tests" changed to "relapsed or metastatic tumours on tumour gene tests" (front page and brief).
- OVERSTATEMENT: README and queue no longer call the 9p21 deletion "stable".
- MINOR: front page, the IL line phrased as a question, with the registry named.
- MINOR: front page, the B7-H3 result qualified as progression-free survival.
- MINOR: For Families, the EU trial register (CTIS) and "any solid tumour" trials added.
- MINOR: For Families, two glossary definitions made precise.
- MINOR: "AI tools" and "AI research assistants" changed to "frontier AI models", per the owner's rule.
- Noted for the owner: the git history credits commits to the AI model by name.
- MINOR: the brief's header dates, its drug-type column, and its PDF re-exported.
- MINOR: the HOW_THIS_WAS_MADE tool table now says per-patient tables are kept local, and lists `build_manifest.py`.
- MINOR: the audit guide now uses `git diff` to compare the manifest.
- MINOR: README links moved to "What's here".
- MINOR: the audit guide's order-of-events command now notes that cycle 6 shares cycle 5's script.
