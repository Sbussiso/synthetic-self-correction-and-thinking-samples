#!/usr/bin/env python3
"""Report how often reasoning quotes the prompt it is reasoning about.

Run from the repository root:

    python grounding_report.py

Not part of validate.py: this is a quality signal to steer writing by, not a
structural invariant, and it is slow enough that it should not gate every run.

Keyword detectors kept lagging my own phrasing and undercounting. A verbatim
overlap test needs no vocabulary: if block 1 reproduces a run of characters from
the question, it is demonstrably working from the question rather than from
memory of it.
"""
import glob
import json
import re
from pathlib import Path

MIN = 18   # a run this long is a quote, not a coincidence


def longest_common_run(a, b):
    """Longest substring of a that also occurs in b, capped for speed."""
    best = 0
    for i in range(len(a)):
        if len(a) - i <= best:
            break
        j = best
        while i + j < len(a) and a[i:i + j + 1] in b:
            j += 1
        best = max(best, j)
    return best


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


WORDY = re.compile(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}\s+[A-Za-z]{3,}")
rows_out = []
for p in sorted(glob.glob("src/*/*/*.jsonl")):
    need = q1 = qlast = 0
    for line in open(p, encoding="utf-8"):
        if not line.strip():
            continue
        msgs = json.loads(line)["messages"]
        prompt = norm(next(m["content"] for m in msgs if m["role"] == "user"))
        if not (WORDY.search(prompt) and re.search(r"\d", prompt)):
            continue
        need += 1
        asst = [m["content"] for m in msgs if m["role"] == "assistant"]
        blocks = re.findall(r"<think>(.*?)</think>", asst[0], re.S)
        if blocks and longest_common_run(norm(blocks[0])[:1200], prompt) >= MIN:
            q1 += 1
        allb = re.findall(r"<think>(.*?)</think>", " ".join(asst), re.S)
        if allb and longest_common_run(norm(allb[-1])[:1200], prompt) >= MIN:
            qlast += 1
    if need:
        rows_out.append(("/".join(Path(p).parts[1:]), need, q1, qlast))

print(f"{'file':44s} {'premise':>8s} {'b1 quotes':>10s} {'last quotes':>12s}")
t = [0, 0, 0]
for f, n, a, b in sorted(rows_out, key=lambda r: -(r[1] - r[2])):
    t[0] += n; t[1] += a; t[2] += b
    print(f"{f:44s} {n:8d} {a:10d} {b:12d}")
print(f"\n{'TOTAL':44s} {t[0]:8d} {t[1]:10d} {t[2]:12d}")
print(f"{'as % of premise-bearing':44s} {'':8s} {100*t[1]//t[0]:9d}% {100*t[2]//t[0]:11d}%")
