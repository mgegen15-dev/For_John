#!/usr/bin/env python3
"""Quality gate for For John. Run before every push; also runs on GitHub for every push (.github/workflows/checks.yml).

  python3 tools/check_site.py            # all checks; exits 1 if any check fails
  python3 tools/check_site.py --list     # list public files and their review status

Checks (see PROCESS.md):
  1. review   every public file has been independently checked on or after the day it last changed (data/review_log.csv)
  2. links    every link in the website resolves: relative links to existing files, GitHub links to tracked files
  3. built    the website pages match their Markdown sources (re-runs tools/build_site.py, then looks for changes)
  4. score    the predictions scorecard adds up and matches the statuses in the table
  5. commits  every commit cited as `abc1234` in reports and pre-registrations exists
  6. order    every engine pre-registration was committed before its cycle's script
  7. wording  public files follow the owner's wording rules
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


def last_changed(path):
    """Day the file's content last changed in a commit, or today if it has uncommitted changes."""
    if git("status", "--porcelain", "--", path).strip():
        import datetime
        return datetime.date.today().isoformat()
    return git("log", "-1", "--format=%cs", "--", path).strip()


def check_review(fail, listing=False):
    log = {r["path"]: r for r in csv.DictReader(open(REVIEW_LOG))} if os.path.exists(REVIEW_LOG) else {}
    for p in public_files():
        changed = last_changed(p)
        r = log.get(p)
        checked = r["last_checked"] if r else ""
        ok = bool(checked) and checked >= changed
        if listing:
            print(f"{'ok ' if ok else 'DUE'}  changed {changed}  checked {checked or 'never':10s}  {p}")
        elif not ok:
            fail("review", f"{p}: changed {changed}, last independent check {checked or 'never'}")


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


def check_built(fail):
    before = git("status", "--porcelain", "--", "docs")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_site.py")], cwd=ROOT, capture_output=True)
    after = git("status", "--porcelain", "--", "docs")
    if after != before:
        changed = sorted(set(after.splitlines()) - set(before.splitlines()))
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
    for f in files:
        for h in set(re.findall(r"commit `([0-9a-f]{7,40})`", open(f).read())):
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
            for m in re.finditer(pat, body):
                line = body.count("\n", 0, m.start()) + 1
                fail("wording", f"{p}:{line}: '{m.group(0)}' ({why})")


def main():
    if "--list" in sys.argv:
        check_review(lambda *a: None, listing=True)
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
