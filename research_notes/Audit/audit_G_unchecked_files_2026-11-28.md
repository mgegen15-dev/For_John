# Audit G: five never-checked or stale public files, the written process and the gate

*Independent frontier-AI review, November 28, 2026. Read-only; numbers recomputed from the repository's data files; PMIDs checked against PubMed abstracts. Scope: the five public files that the new review log showed had never been independently checked or had changed since their last check, plus `PROCESS.md`, `tools/check_site.py`, and the November 28 additions to `README.md`, `HOW_THIS_WAS_MADE.md` and `AUDIT_GUIDE.md`. Result: 41 findings as numbered by the reviewer (some are grouped below). The fixes were made the same day and sent to a separate verification review before publishing (rule 4 of `PROCESS.md`).*

## Contradictions and hidden links (never checked before)

- **ERROR:** "151 genes, 21 drugs" counted pairs. The correct counts are 99 genes and 10 drugs. Fixed.
- **OVERSTATEMENT:** a cell-experiment result (33101888) was described as a mouse result in two places. Fixed.
- **OVERSTATEMENT:** ICG-001 "slowed growth" in mice. It slowed growth in cells but not the tumour in mice. Fixed.
- **INCONSISTENCY:** stale follow-ups; the 223-patient study was already on lead 14. Fixed.
- **OVERSTATEMENT:** "a different route" from the repurposing screen. The route is partly shared. Fixed.
- **MINOR:** the belumosudil substitution was not disclosed in the table. Fixed.
- **OVERSTATEMENT:** the carbamazepine row read as treatment guidance. Fixed.
- **MINOR:** abciximab score and paper count. Fixed.
- **MINOR:** the edge-file description was incomplete. Fixed.
- **MINOR:** the hidden-links file holds the top 400 of 1,913 chains. Fixed.
- **MINOR:** the two hand-check samples used different rule versions. Fixed.
- **MINOR:** the plicamycin/mithramycin count. Fixed.
- **OVERSTATEMENT:** "the graph supports" leads. It is agreement in abstracts, not a test, and two project tests point the other way. Fixed and named.

## Do the leads predict survival (never checked before)

- **MINOR:** the scope of the lifelines cross-check. Fixed.
- **INCONSISTENCY:** the 223-tumour CXCR4 study was omitted. Fixed.
- **POLICY (owner):** the TARGET-OS per-patient table is still published, although cBioPortal per-patient tables were withdrawn. This is open-tier data. Left for the owner to decide.

## Ranked leads (changed since its November 20 check)

- **MINOR:** "genuine" against "model difference" wording. Fixed.
- **MINOR:** the header and the change-log order. Fixed.
- **INCONSISTENCY:** the change log named caplacizumab and abciximab for lead 10, but the lead did not. Fixed.
- **INCONSISTENCY:** later results bearing on leads 1, 2, 4, 5, 12 and 13 were missing. Added; no scores changed.

## SUMMARY (changed since its November 20 check)

- **OVERSTATEMENT:** "309 patients, enough to test it". Narrowed to what that sample can show. Fixed.
- **OVERSTATEMENT (family-facing):** "Antibody-drug conjugates are working". This rests on one open-label trial in China, with overall survival not yet known. Fixed.
- **MINOR:** "2,400 approved drugs" should be "approved and late-stage". Fixed.
- **MINOR:** "published cohorts report about 40%" should be "one cohort, at least 40%". Fixed.
- **MINOR:** the LRRC15 trial count (three treatment trials plus an imaging study). Fixed.
- **OMISSION:** no mention of the research engine or the survival test. Item 8 added.

## Evidence explorer (changed since built; never checked)

- **INCONSISTENCY:** "Corrected q" showed a different correction from the report's. Fields renamed and split, in the builder and the data. Fixed.
- **OVERSTATEMENT:** "everything this project has gathered", although the data were built November 22 and lack the engine results. Dated on the page. Fixed.

## PROCESS.md and the gate

- **OVERSTATEMENT:** "independent check" did not say the reviews are by AI. Fixed, with a statement that no human expert has reviewed the work yet.
- **OVERSTATEMENTS:** the scope of the link, build, commit, order and wording checks was described more broadly than the script implements. Each is now stated exactly.
- **INCONSISTENCY:** the gate can rewrite `docs/`, which was not stated. Fixed.
- **Gate fixes in code:**
  - the build check now detects build failures, and compares file contents so a rebuild that changes an already-modified page is caught;
  - review times are compared to the minute, not the day, for new entries;
  - cited commits are also checked in public Markdown;
  - "not a scientist" is matched in any case.
- **MINOR:** "runs before every push" was not automated. It now says "run by hand", plus the automatic GitHub run.
- **MINOR:** the weekly review is a scheduled session outside the repository. Stated.
- **MINOR:** `docs/index.html` and `docs/explorer.html` are hand-maintained. Stated.
- **MINOR:** the HOW_THIS_WAS_MADE row wording. Fixed.
- **MINOR:** review-log wording for never-checked files. Fixed.

## Verification of these fixes

A separate verification review on November 28 confirmed the fixes and found 14 further problems: wording on the AKT2 result and the platelet drugs, the summary's description of the research engine, two errors in the review log, the explorer's meta description, and weaknesses in the gate (date-only review entries covered later same-day edits; the timestamp and commit-hash checks could be fooled). All were fixed, and the review log now records a fingerprint of the exact content reviewed instead of a date.
