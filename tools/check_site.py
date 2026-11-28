#!/usr/bin/env python3
"""Quality gate for For John. Run before every push; also runs on GitHub for every push (.github/workflows/checks.yml).

  python3 tools/check_site.py            # all checks; exits 1 if any check fails
  python3 tools/check_site.py --list     # list public files and their review status
  python3 tools/check_site.py --record "<check>" <audit record> <file>...   # stamp files as checked, after a passed review

Checks (see PROCESS.md):
  1. review   every public file's current content is exactly what was last independently checked (content fingerprints in
              data/review_log.csv; files with a date-only check dated before LEGACY_BEFORE count as 'legacy' while not committed after that day)
  2. links    internal website links resolve to existing files, and links to repository files point to tracked files
              (external links, links inside Markdown files and links built by JavaScript are not checked)
  3. built    pages built by tools/build_site.py match their Markdown sources (re-runs it, so it can rewrite docs/)
  4. score    the predictions scorecard adds up and matches the statuses in the table
  5. commits  every commit cited in reports, pre-registrations and public Markdown files exists
  6. order    every engine pre-registration was committed before its cycle's analysis script (data opened earlier cannot be detected)
  7. wording  public files use none of the banned terms listed in BANNED
"""
import csv
import glob
import os
import re
import subprocess
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/mgegen15-dev/For_John/"
REVIEW_LOG = os.path.join(ROOT, "data", "review_log.csv")
LEGACY_BEFORE = "2026-11-27"   # date-only review entries count as legacy only if dated before this day
PUBLIC = (["reports/*.md", "briefs/*.md", "FAMILIES.md", "SUMMARY.md", "REPORTS.md", "README.md", "HOW_THIS_WAS_MADE.md",
           "AUDIT_GUIDE.md", "PREDICTIONS.md", "RESEARCH_QUEUE.md", "PROCESS.md", "docs/index.html", "docs/explorer.html"])
BANNED = [(r"\bClaude\b", "names the AI model; say \"frontier AI models\""), (r"\bAnthropic\b", "names the AI company"),
          (r"not a scientist", "owner's rule"), (r"\bAI tools\b", "say \"frontier AI models\""),
          (r"\bAI research assistants\b", "say \"frontier AI models\"")]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def public_files():
    out = []
    for pat in PUBLIC:
        out += sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, pat)))
    return out


def blob(path):
    """Fingerprint of the file's current content (git blob hash of the working-tree file)."""
    return git("hash-object", "--", path).strip()


def last_changed_day(path):
    """Day (UTC) the file last changed: its last commit, or today if it has uncommitted changes."""
    import datetime
    if git("status", "--porcelain", "--", path).strip():
        return datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    iso = git("log", "-1", "--format=%cI", "--", path).strip()
    return datetime.datetime.fromisoformat(iso).astimezone(datetime.timezone.utc).date().isoformat() if iso else ""


def status(path, row):
    """ok      : the reviewed content fingerprint equals the file's current content
       legacy  : a date-only check dated before LEGACY_BEFORE, and no commit to the file after that day;
                 such fixes were not separately verified, so the weekly audit re-checks legacy files over time
       DUE     : anything else"""
    if row and row.get("reviewed_blob"):
        return "ok" if row["reviewed_blob"] == blob(path) else "DUE"
    checked = (row or {}).get("last_checked", "")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", checked or "") and checked < LEGACY_BEFORE and checked >= last_changed_day(path):
        return "legacy"
    return "DUE"


def read_log():
    return {r["path"]: r for r in csv.DictReader(open(REVIEW_LOG))} if os.path.exists(REVIEW_LOG) else {}


def check_review(fail, listing=False):
    log = read_log()
    for p in public_files():
        st = status(p, log.get(p))
        if listing:
            r = log.get(p) or {}
            print(f"{st:6s}  checked {r.get('last_checked') or 'never':10s}  {p}")
        elif st == "DUE":
            r = log.get(p) or {}
            fail("review", f"{p}: content differs from what was last independently checked ({r.get('last_checked') or 'never'})")


def record(paths, check, record_file):
    """Stamp files as independently checked in their current form. Use only after a review has passed and its fixes are verified."""
    import datetime
    if not paths:
        sys.exit("usage: check_site.py --record \"<check>\" <audit record> <file> [<file> ...]")
    record_file = os.path.normpath(record_file).replace(os.sep, "/")
    if not record_file.startswith("research_notes/Audit/") or not os.path.isfile(os.path.join(ROOT, record_file)):
        sys.exit(f"audit record must be a saved review under research_notes/Audit/: {record_file}")
    log = read_log()
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    for p in paths:
        p = os.path.relpath(os.path.join(ROOT, p), ROOT)
        if p not in public_files():
            sys.exit(f"not a public file: {p}")
        log[p] = {"path": p, "reviewed_blob": blob(p), "last_checked": today, "check": check, "record": record_file}
    with open(REVIEW_LOG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "reviewed_blob", "last_checked", "check", "record"])
        w.writeheader()
        for k in sorted(log):
            r = log[k]
            w.writerow({c: r.get(c, "") for c in w.fieldnames})
    print(f"recorded {len(paths)} file(s)")


def check_links(fail):
    tracked = set(git("ls-files").split("\n"))
    docs = os.path.join(ROOT, "docs")
    for root, _, files in os.walk(docs):
        for f in files:
            if not f.endswith(".html"):
                continue
            page = os.path.join(root, f)
            body = open(page, errors="replace").read()
            for h in re.findall(r'(?:href|src)="([^"#]+)', body):
                if h.startswith(("mailto:", "data:", "//")):
                    continue
                if h.startswith(REPO):
                    rest = h[len(REPO):]
                    m = re.match(r"(?:blob|tree)/main/(.*)", rest)
                    if m:
                        path = urllib.parse.unquote(m.group(1)).rstrip("/")
                        if path and path not in tracked and not any(t.startswith(path + "/") for t in tracked):
                            fail("links", f"{os.path.relpath(page, ROOT)} -> GitHub path not in git: {path}")
                    continue
                if h.startswith("http"):
                    continue
                target = os.path.normpath(os.path.join(root, urllib.parse.unquote(h)))
                if not os.path.exists(target):
                    fail("links", f"{os.path.relpath(page, ROOT)} -> missing {h}")


def _docs_hashes():
    import hashlib
    out = {}
    for root, _, files in os.walk(os.path.join(ROOT, "docs")):
        for f in files:
            p = os.path.join(root, f)
            out[p] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def check_built(fail):
    """Re-runs tools/build_site.py (so it can rewrite pages under docs/) and fails if any page changed or the build failed.
    docs/index.html, docs/explorer.html and docs/data/explorer.json are maintained separately and are not rebuilt here."""
    before = _docs_hashes()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_site.py")], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        fail("built", f"tools/build_site.py failed: {r.stderr.strip()[-300:]}")
        return
    after = _docs_hashes()
    changed = sorted(os.path.relpath(p, ROOT) for p in set(before) | set(after) if before.get(p) != after.get(p))
    if changed:
        fail("built", f"website pages were out of date with their Markdown sources; rebuilt now, commit them: {changed[:5]}")


def check_score(fail):
    s = open(os.path.join(ROOT, "PREDICTIONS.md")).read()
    rows = [l for l in s.splitlines() if re.match(r"\| P\d+ \|", l)]
    right = sum("**Right**" in l.split("|")[-2] for l in rows)
    wrong = sum("**Wrong**" in l.split("|")[-2] for l in rows)
    m = re.search(r"\| Resolved \| Right \| Wrong \| Unresolved \|\n\|---\|---\|---\|---\|\n\| (\d+) \| (\d+) \| (\d+) \| (\d+) \|", s)
    if not m:
        fail("score", "scorecard table not found in PREDICTIONS.md")
        return
    res, r, w, u = map(int, m.groups())
    if (r, w) != (right, wrong):
        fail("score", f"scorecard says {r} right / {w} wrong; table statuses give {right} / {wrong}")
    if res != r + w or res + u != len(rows):
        fail("score", f"scorecard arithmetic: {res} resolved, {u} unresolved, {len(rows)} predictions")


def check_commits(fail):
    files = glob.glob(os.path.join(ROOT, "reports", "*.md")) + glob.glob(os.path.join(ROOT, "research_notes", "Engine", "*", "PREREGISTRATION.md"))
    files += [os.path.join(ROOT, p) for p in public_files() if p.endswith(".md")]
    for f in sorted(set(files)):
        body = open(f).read()
        cited = set(re.findall(r"commit `([0-9a-f]{7,40})`", body))
        bare = {h for h in re.findall(r"`([0-9a-f]{7,40})`", body) if re.search(r"[a-f]", h) and re.search(r"[0-9]", h)}
        hashes = cited | bare
        for h in hashes:
            if git("cat-file", "-t", h).strip() != "commit":
                fail("commits", f"{os.path.relpath(f, ROOT)} cites commit {h}, which does not exist")


def check_order(fail):
    for d in sorted(glob.glob(os.path.join(ROOT, "research_notes", "Engine", "cycle-*"))):
        n = int(re.search(r"cycle-(\d+)", d).group(1))
        pre = git("log", "--format=%cI", "--", os.path.relpath(os.path.join(d, "PREREGISTRATION.md"), ROOT)).split()
        pat = "tools/engine_cycle05_06*" if n == 6 else f"tools/engine_cycle{n:02d}*"
        scr = git("log", "--diff-filter=A", "--format=%cI", "--", pat).split()
        if not pre:
            fail("order", f"cycle {n}: pre-registration not committed")
        elif scr and min(pre) > min(scr):
            fail("order", f"cycle {n}: script committed {min(scr)} before the pre-registration {min(pre)}")


def check_wording(fail):
    for p in public_files():
        body = open(os.path.join(ROOT, p), errors="replace").read()
        for pat, why in BANNED:
            for m in re.finditer(pat, body, re.I if pat == "not a scientist" else 0):
                line = body.count("\n", 0, m.start()) + 1
                fail("wording", f"{p}:{line}: '{m.group(0)}' ({why})")


def main():
    if "--list" in sys.argv:
        check_review(lambda *a: None, listing=True)
        return
    if "--record" in sys.argv:
        # python3 tools/check_site.py --record "<check description>" <audit record path> <file> [<file> ...]
        i = sys.argv.index("--record")
        if len(sys.argv) < i + 4:
            sys.exit("usage: check_site.py --record \"<check>\" <audit record> <file> [<file> ...]")
        record(sys.argv[i + 3:], sys.argv[i + 1], sys.argv[i + 2])
        return
    problems = []
    fail = lambda kind, msg: problems.append((kind, msg))
    for name, fn in [("review", check_review), ("links", check_links), ("built", check_built), ("score", check_score),
                     ("commits", check_commits), ("order", check_order), ("wording", check_wording)]:
        n0 = len(problems)
        fn(fail)
        print(f"{'PASS' if len(problems) == n0 else 'FAIL'}  {name}")
    for kind, msg in problems:
        print(f"  [{kind}] {msg}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
