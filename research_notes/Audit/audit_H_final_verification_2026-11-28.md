# Audit H: final verification before the process gate went live

*Independent frontier-AI review, November 28, 2026, of branch `process-gate` at `e6d1274`. Read-only; numbers recomputed from the data files; PMIDs 33101888, 22173290 and 15814634 checked against PubMed. Two scopes:*

- *the fixes from the audit G verification round (`a6845d3..e6d1274`), including the new content-fingerprint review check;*
- *the fixes of November 27 (passes F2–F4, commit `b9a8710`, diffed from `762cbbb`), which had not been verified.*

## Confirmed

- **Counts recomputed from the data, all correct:**
  - cycle 7: 8 CCNE1 trials, 5 with a US site;
  - totals: 33 trials, 2 open from age 12, 31 of 33 at phase 1 or 1/2;
  - cycle 12: 58 / 44 / 32, 78 of 1,434;
  - cycle 17: 10.9% against 5.0%;
  - cycle 3: 35 of 179;
  - cycles 8 and 9: about 1.3 million comparisons;
  - survival, cycle 15 and cycle 20 figures.
- **The brief's PDF** matches its Markdown, apart from one dropped source label (finding 15).
- **21 public files found clean in their current form**, and stamped with their content fingerprints:
  - the contradictions, survival and ranked-leads reports;
  - the evidence explorer;
  - For Families;
  - the teen-access brief;
  - the Research Queue;
  - engine cycles 1, 2, 3, 5 and 8–18. Cycle 14 was held for the per-SD check in finding 7: its model standardises the score, so it is per SD as stated.

## Findings and resolution (16)

1. **SUMMARY:** "one … was modestly supported" overlooked other supported or right results. Reworded to the biological questions, with the trial-access counts noted. Fixed.
2. **PROCESS and the gate:** date-only review entries made on a check day still covered same-day edits. Date-only entries now count as legacy only if dated before November 27, 2026, and the wording is exact. Fixed.
3. **Gate code, minor issues:**
   - `--record` now requires files and an existing audit record.
   - Bare backticked hashes must contain both a letter and a digit, so 7-digit numbers are not taken for commits.
   - The PDF brief is not a gate-checked public file; the brief's PDF is re-exported with every brief change.

   Fixed or noted.
4. **Front page:** the 1,434 recruiting count and the all-status 5%-against-11% trend read as one set. Separated. Fixed.
5. **Front page, REPORTS and AUDIT_GUIDE:** "before the data were opened" overstated what can be shown. Now "planned in writing and committed before its analysis was run", with downloads before the plan disclosed. Fixed.
6. **REPORTS:** cycle 19 described in centres instead of states. Fixed.
7. **Cycle 20 and P54:** the plan said per standard deviation, but the effect was per unit of an averaged score.
   - Per SD: macrophage 0.72 (0.52–1.01), T-cell 0.79 (0.57–1.10); verdicts unchanged.
   - Declared as a deviation.
   - The same applied to cycle 15's 9p21 score: per SD 1.29 (0.85–1.97), verdict unchanged.
   - Cycle 14's hazard ratios were already per SD.

   Fixed.
8. **Cycle 4:** an unsourced "a quarter to a half", and a garbled, advice-like sentence. Replaced with the project's own 5 of 19. Fixed.
9. **Cycle 7:** "would qualify" replaced with what was measured. Fixed.
10. **Cycle 6:** the lowest-CCNE1 lines qualified as "among lines in the knockout screen". Fixed.
11. **Cycle 19 and P53:** 22 states included DC. Now 21 states and DC, and recruiting sites in 16 states and DC. Fixed.
12. **AUDIT_GUIDE E7:** "supporting" changed to "sensitivity datasets". Fixed.
13. **HOW_THIS_WAS_MADE:** "review dates" changed to content fingerprints, and "both rounds" made specific. Fixed.
14. **README:** the brief's cycles and the audit history completed. Fixed.
15. **Brief PDF:** re-exported with the dropped source label restored. Fixed.
16. **Audit F record:** the pre-rewrite commit ID mapped, and the "30 starting at 18" wording made exact. Fixed.

## Not reviewed

The 13 older reports and the pet-dog brief, unchanged since November 20. They are "legacy" in the review log, and the weekly audit re-checks them three at a time.
