# How work is checked before it is published

*The rules every change to For John follows. Adopted November 28, 2026, after independent checks in one week each found errors in published work. The aim: nothing reaches a family, researcher or funder until a reviewer other than its author has checked it.*

**Who does the checking.** The reviews described here are run by separate frontier-AI review sessions, not by people. No human expert has yet reviewed this work; clinician and researcher review is being sought.

## The rules

1. **Plan before data.** Every new test is written down, with the result that would count against it, and committed to git before its analysis is run (`research_notes/Engine/cycle-NN-*/PREREGISTRATION.md`). Any data downloaded or read before the plan is disclosed in the report. Changes after that are listed under "Deviations".
2. **Independent check before publishing.** Every new or changed public file is checked by a separate frontier-AI review session that did not write it. The reviewer reads the file, its data and its sources fresh. It may read the project's working notes, but it does not share the author's session. It checks:
   - every number against the data;
   - every claim against its source;
   - every sentence for overstatement.

   The full review is saved in `research_notes/Audit/`. Its findings are fixed or answered, and the fixes themselves are checked. Only then is the file stamped as checked: `python3 tools/check_site.py --record "<check>" <audit record> <file>...` stores a fingerprint of the exact content reviewed in `data/review_log.csv`. Any later change to the file, however small, makes it due again.
3. **The gate must pass.** `python3 tools/check_site.py` is run by hand before every push, and runs automatically on GitHub after every push and once a week. It fails if:
   - a public file's content differs from the content last stamped as independently checked. Files whose last check is dated before November 27, 2026, before fingerprints were recorded, count as "legacy" if they were not committed after the day of that check. Edits made on the check day itself cannot be detected, so the weekly audit re-checks legacy files, oldest first;
   - an internal website link or a link to a repository file is broken. External links, links inside the Markdown files and links built by the explorer's JavaScript are not checked;
   - a page built by `tools/build_site.py` is out of date with its Markdown source, or the build fails. The gate re-runs the build, so it can rewrite pages under `docs/`;
   - the predictions scorecard does not add up;
   - a commit cited in a report, pre-registration or public Markdown file (written as the word "commit" followed by a commit ID in code formatting, or as a 7–40 character commit ID in code formatting containing at least one letter and one digit) does not exist;
   - an engine plan was committed after its analysis script. Data opened before the plan cannot be detected this way;
   - public text uses a banned term (the list is `BANNED` in `tools/check_site.py`; for example, naming the AI model or its maker).

   The gate cannot judge whether a sentence is true or reads as medical advice. Only the reviews do that.
4. **Fix, log, re-check.** A correction is made in the source file and noted in that file's change log with the date and reason. If the correction changes a number or a claim, the file is checked again.
5. **Periodic audits.**
   - **Weekly:** a scheduled frontier-AI review session runs on Mondays. It is set up in the owner's account, not in this repository. It reviews every public file the gate reports as due, the three oldest "legacy" files, and five older claims chosen at random and checked from scratch. It saves its record on a separate branch and never edits public files.
   - **Before every frozen release:** a full independent audit of every public file, split among separate reviewers, with all findings fixed before the release is tagged.
6. **Family-facing text gets the most care.**
   - The For Families page and the briefs give no medical advice.
   - They carry no statistics a family could misread as a personal prognosis.
   - They say where each fact comes from.
   - Clinician review is sought before wider outreach.
7. **When in doubt, say less.** If a claim cannot be checked, it is labelled "unverified" or removed.

## What a public file is

**The list:**
- every file under `reports/` and `briefs/`;
- `FAMILIES.md`, `SUMMARY.md`, `REPORTS.md`, `README.md`, `HOW_THIS_WAS_MADE.md`, `AUDIT_GUIDE.md`, `PREDICTIONS.md`, `RESEARCH_QUEUE.md` and this file;
- `docs/index.html` and `docs/explorer.html`.
- The one-page PDF of the teen-access brief (`docs/briefs/For-John-brief-trial-access-for-teenagers.pdf`) is re-exported and compared with the brief's Markdown whenever the brief changes; the gate does not check it.

**How the website is made from them:**
- Most pages under `docs/` are built from the Markdown files by `tools/build_site.py`.
- `docs/index.html` and `docs/explorer.html` are maintained by hand.
- The explorer's data, `docs/data/explorer.json`, is built by `tools/build_explorer_data.py`. It was built on November 22, 2026, with its survival field names corrected by hand on November 28; the page says it covers what the project had gathered by November 22.

## Running the gate

```bash
python3 tools/check_site.py
```

```bash
python3 tools/check_site.py --list
```

The first runs every check. The second lists each public file as ok, legacy or due, with the date it was last independently checked.
