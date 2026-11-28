# Audit I: verification of the audit H fixes, and of those fixes

*Two independent frontier-AI review passes, November 28, 2026, on branch `process-gate`. Both were read-only and recomputed numbers from the data, re-running the analysis functions in a scratch clone.*

## Pass I1: verification of the audit H fixes (`e6d1274..ae560d5`)

**Confirmed:**
- per-SD effects for cycle 20 (0.72, 0.52–1.01; 0.79, 0.57–1.10) and for cycle 15's 9p21 score (1.29, 0.85–1.97);
- cycle 14's hazard ratios are per SD;
- NCT04616560: 21 states and DC, and 16 states and DC with recruiting sites;
- cycle 4's 5 of 19;
- cycle 6's lowest-CCNE1 screened lines;
- the brief PDF matches its Markdown;
- the audit F record edits;
- the gate code.

**Files found clean and stamped:** engine cycles 4, 6, 7, 14 and 19.

**17 findings, fixed in `b1443f8`:**
1. Cycle 20's figure was titled per SD but plotted per-unit values, and said "three cohorts"; cycle 15's figure had the same issue for the 9p21 row. Captions are now parameters, and both figures were regenerated.
2. Cycle 15: the 9p21 score's scale is declared as a deviation, with the per-SD result in the summary.
3. Cycle 20: GSE289059 rounding.
4. Cycle 20 pre-registration: the deviation date.
5. SUMMARY: the recruiting count and the all-status trend are separated.
6. SUMMARY: the engine's supported and maintained results are described exactly.
7. PROCESS: the commit-ID rule described exactly.
8. PROCESS rule 1: "before its data are opened" changed to "before its analysis is run", with disclosure.
9. PROCESS and gate:
   - the PDF note added;
   - `--record` now requires a record under `research_notes/Audit/`;
   - docstrings corrected.
10. AUDIT_GUIDE: the header now says corrections after the freeze are recorded.
11. AUDIT_GUIDE: "before each cycle's analysis was run"; a contradictory phrase fixed.
12. PREDICTIONS: a change-log entry for the P53 and P54 edits; P55 per-SD added.
13. HOW_THIS_WAS_MADE and README: the audit dates, and the teen-access brief named, not "briefs".
14. README: "tested on independent patients" removed from the Research Queue line.
15. Front-page date.
16. REPORTS: "almost never" changed to "rarely (about 1 in 18)".
17. Data columns relabelled: per unit of z-score (cycles 15 and 20), and states and DC (cycle 19).

## Pass I2: verification of those fixes (`ae560d5..b1443f8`)

**Confirmed:**
- every recomputed number: 9p21 per SD 1.29 (0.85–1.97), random effects 1.32 (0.76–2.28); cycle 20 per SD 0.72 and 0.79; 0.27 and 0.85; 78 of 1,434, about 1 in 18; 21 states and DC;
- both regenerated figures;
- the changed scripts reproduce their outputs exactly;
- the gate passes in a clean clone apart from the files due for review.

**Files found clean:** SUMMARY, PROCESS, docs/index.html, REPORTS, README, HOW_THIS_WAS_MADE, PREDICTIONS.

**5 findings:**
1. Cycle 20 summary: one lower limit still read 0.28. Fixed to 0.27.
2. Figure screen-reader labels and cycle 15's alt text still said "per standard deviation". `aria-label` is now built from the caption; the alt text and the Measures line are updated.
3. Audit trail:
   - Files had been stamped against the audit H record, which does not document these verification rounds. This record now does, and those files are re-stamped against it.
   - The AUDIT_GUIDE header overstated that every file has a change log. Now worded as "each report's change log and the audit records".
4. Cycle 12 report: "almost never" changed to "rarely (5.4%)", to match the other pages.
5. `--record`: the path is normalised before the folder check.

**Rule followed:** the fixes for findings 1, 2 and 4 change wording or a number, so they were checked again before stamping (pass I3, below).
