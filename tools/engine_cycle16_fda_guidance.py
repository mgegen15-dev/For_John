#!/usr/bin/env python3
"""Engine cycle 16: since the FDA's 2019 adolescent guidance, are new early-phase trials more likely to take teenagers?

Pre-registered in research_notes/Engine/cycle-16-fda-guidance/PREREGISTRATION.md (commit 3a71706).
Reuses engine cycle 12's saved registry records (run tools/engine_cycle12_teen_access.py fetch first).

Outputs: data/engine/cycle16/results.json, by_year.csv, docs/figures/engine16_years.svg
"""
import csv
import json
import math
import os
import sys

from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_cycle12_teen_access as c12     # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "engine", "cycle16")
FIG = os.path.join(ROOT, "docs", "figures")


def odds(a, b, c, d):
    """a,b = after (teen, not); c,d = before (teen, not)."""
    if 0 in (a, b, c, d):
        a, b, c, d = a + .5, b + .5, c + .5, d + .5
    o = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return o, math.exp(math.log(o) - 1.96 * se), math.exp(math.log(o) + 1.96 * se)


def compare(rows):
    aft = [r for r in rows if r["year"] >= 2020]
    bef = [r for r in rows if r["year"] < 2020]
    a, b = sum(r["accepts_teenagers"] for r in aft), sum(not r["accepts_teenagers"] for r in aft)
    c, d = sum(r["accepts_teenagers"] for r in bef), sum(not r["accepts_teenagers"] for r in bef)
    o, lo, hi = odds(a, b, c, d)
    return {"after": {"teen": a, "n": a + b, "share": a / (a + b) if a + b else float("nan")},
            "before": {"teen": c, "n": c + d, "share": c / (c + d) if c + d else float("nan")},
            "odds_ratio": o, "lo": lo, "hi": hi, "fisher_p": float(stats.fisher_exact([[a, b], [c, d]])[1])}


def verdict(m):
    if m["odds_ratio"] > 1 and m["lo"] > 1:
        return "Supported"
    if m["hi"] < 1.5:
        return "Refuted"
    return "Inconclusive"


def bars(by_year, path, subtitle=None, guidance_after_year=2019):
    W, H, left, bottom, top = 820, 300, 60, 50, 50
    years = sorted(by_year)
    bw = (W - left - 20) / len(years)
    mx = max(v["share"] for v in by_year.values()) or 1
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui, sans-serif" font-size="12" role="img" '
         f'aria-label="Share of recruiting early-phase solid-tumour drug trials accepting teenagers, by start year">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="16" y="24" font-size="13" font-weight="600" fill="#1d2430">Share accepting anyone aged 12–17, by the year the trial started</text>',
         f'<text x="16" y="40" fill="#525b6b">{subtitle or "Recruiting early-phase &quot;solid tumour&quot; drug trials on November 26, 2026. Dashed line: FDA guidance, March 2019."}</text>']
    ph = H - top - bottom
    for i, y in enumerate(years):
        v = by_year[y]
        h = ph * v["share"] / mx * 0.9
        x = left + i * bw
        col = "#1c5cab" if y >= 2020 else "#6a7384"
        s.append(f'<rect x="{x + 3:.1f}" y="{top + ph - h:.1f}" width="{bw - 6:.1f}" height="{h:.1f}" fill="{col}"/>')
        s.append(f'<text x="{x + bw / 2:.1f}" y="{H - bottom + 16}" text-anchor="middle" fill="#525b6b">{"before 2020" if y == 2019 else "2027+" if y == 2027 else y}</text>')
        s.append(f'<text x="{x + bw / 2:.1f}" y="{top + ph - h - 4:.1f}" text-anchor="middle" fill="#1d2430">{v["teen"]}/{v["n"]}</text>')
    xg = left + bw * sum(1 for y in years if y <= guidance_after_year)
    s.append(f'<line x1="{xg:.1f}" y1="{top - 4}" x2="{xg:.1f}" y2="{H - bottom}" stroke="#a3401a" stroke-dasharray="4 4"/>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


def main():
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(os.path.join(c12.RAW, "set_B.json")))
    a_ids = {r["nct"] for r in csv.DictReader(open(os.path.join(c12.OUT, "set_a.csv")))}
    b_ids = {r["nct"] for r in csv.DictReader(open(os.path.join(c12.OUT, "set_b.csv")))}
    rows, missing = [], 0
    for s in data["studies"]:
        r = c12.record(s)
        if r["nct"] not in b_ids or r["nct"] in a_ids:
            continue
        sd = s["protocolSection"]["statusModule"].get("startDateStruct", {}).get("date", "")
        if not sd:
            missing += 1
            continue
        r["year"] = int(sd[:4])
        rows.append(r)
    S = {"preregistration_commit": "3a71706", "trials": len(rows), "missing_start_date": missing}
    S["H1"] = compare(rows)
    S["verdict_H1"] = verdict(S["H1"])
    ind = [r for r in rows if r["sponsor_class"] == "Industry"]
    S["industry"] = compare(ind)
    S["academic_or_other"] = compare([r for r in rows if r["sponsor_class"] != "Industry"])
    S["adult_floor_12_or_more"] = compare([r for r in rows if r["min_years"] is None or r["min_years"] >= 12])
    S["P45"] = "right" if S["verdict_H1"] == "Supported" else "wrong"
    S["P46"] = "right" if S["industry"]["after"]["share"] < 0.05 else "wrong"
    by = {}
    for r in rows:
        y = 2019 if r["year"] < 2020 else min(r["year"], 2027)     # display groups: before 2020; 2027 and later
        b = by.setdefault(y, {"teen": 0, "n": 0})
        b["teen"] += r["accepts_teenagers"]
        b["n"] += 1
    for v in by.values():
        v["share"] = v["teen"] / v["n"]
    S["by_year"] = {str(k): v for k, v in sorted(by.items())}
    json.dump(S, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    with open(os.path.join(OUT, "by_year.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start_year (2019 = before 2020; 2027 = 2027 or later)", "trials", "accept_teenagers", "share"])
        for y, v in sorted(by.items()):
            w.writerow([y, v["n"], v["teen"], f'{v["share"]:.3f}'])
    bars(by, os.path.join(FIG, "engine16_years.svg"))
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
