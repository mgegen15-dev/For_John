# How work is checked before it is published

*The rules every change to For John follows. Adopted November 28, 2026, after three independent checks in one week each found errors in published work. The aim: nothing reaches a family, researcher or funder until someone other than its author has checked it.*

## The rules

1. **Plan before data.** Every new test is written down, with the result that would count against it, and committed to git before its data are opened (`research_notes/Engine/cycle-NN-*/PREREGISTRATION.md`). Changes after that are listed under "Deviations".
2. **Independent check before publishing.** Every new or changed public file is checked by a separate review that did not write it and does not see the author's reasoning. The review checks every number against the data, every claim against its source, and every sentence for overstatement. The full review is saved in `research_notes/Audit/`. Its findings are fixed or answered, then the file's date is recorded in `data/review_log.csv`.
3. **The gate must pass.** `python3 tools/check_site.py` runs before every push and runs again on GitHub after every push. It fails if any public file changed after its last independent check, if any website link is broken, if the website is out of date with its sources, if the predictions scorecard does not add up, if a cited commit does not exist, if a plan was committed after its analysis, or if public text breaks the wording rules.
4. **Fix, log, re-check.** A correction is made in the source file, noted in that file's change log with the date and reason, and the file is checked again if the correction changes a number or a claim.
5. **Periodic audits.**
   - **Weekly:** a scheduled review of every public file the gate reports as due, plus a fresh sample of five older claims checked from scratch, whether or not they changed.
   - **Before every frozen release:** a full independent audit of every public file, split among separate reviewers, with all findings fixed before the release is tagged.
6. **Family-facing text gets the most care.** The For Families page and the briefs give no medical advice, carry no statistics a family could misread as a personal prognosis, and say where each fact comes from. Clinician review is sought before wider outreach.
7. **When in doubt, say less.** If a claim cannot be checked, it is labelled "unverified" or removed.

## What a public file is

Every file under `reports/` and `briefs/`, plus `FAMILIES.md`, `SUMMARY.md`, `REPORTS.md`, `README.md`, `HOW_THIS_WAS_MADE.md`, `AUDIT_GUIDE.md`, `PREDICTIONS.md`, `RESEARCH_QUEUE.md`, this file (`PROCESS.md`), `docs/index.html` and `docs/explorer.html`. The website pages under `docs/` are built from these files by `tools/build_site.py`.

## Running the gate

```bash
python3 tools/check_site.py
```

```bash
python3 tools/check_site.py --list
```

The first runs every check; the second lists each public file with the date it last changed and the date it was last independently checked.
