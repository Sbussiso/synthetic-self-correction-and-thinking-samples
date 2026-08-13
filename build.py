#!/usr/bin/env python3
"""Rebuild dataset.jsonl and eval.jsonl from the 27 source files.

Run from the repository root:

    python build.py

The split is grouped by prompt, not by record index. The library deliberately
reuses the same question across reasoning modes (a question asked in
right_and_confirm may also appear in wrong_then_fix, which is what teaches that
being right or wrong is not a property of the question). An index-based split
therefore scatters copies of one prompt across both files, so the model meets
the exact question during training and is then scored on it. Assigning whole
prompt groups keeps every copy on the same side.

Selection is by hash of the prompt, so the split is deterministic and stable:
re-running after editing one record does not reshuffle the rest.
"""
import glob
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EVAL_FRACTION = 0.10

groups = defaultdict(list)
order = []
for path in sorted(glob.glob("*/*/*.jsonl")):
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        prompt = rec["messages"][-2]["content"]
        if prompt not in groups:
            order.append(prompt)
        groups[prompt].append(json.dumps(rec, ensure_ascii=False))

total = sum(len(v) for v in groups.values())
target = round(total * EVAL_FRACTION)

# deterministic, stable ordering independent of file order
ranked = sorted(order, key=lambda q: hashlib.sha1(q.encode("utf-8")).hexdigest())

eval_prompts, count = set(), 0
for q in ranked:
    if count >= target:
        break
    eval_prompts.add(q)
    count += len(groups[q])

train, ev = [], []
for q in order:
    (ev if q in eval_prompts else train).extend(groups[q])

for name, rows in (("dataset.jsonl", train), ("eval.jsonl", ev)):
    Path(name).write_bytes(("\n".join(rows) + "\n").encode("utf-8"))

tp = {json.loads(r)["messages"][-2]["content"] for r in train}
ep = {json.loads(r)["messages"][-2]["content"] for r in ev}
assert not (tp & ep), f"prompt leakage: {len(tp & ep)}"
assert len(train) + len(ev) == total, "split does not partition the source"

print(f"source        : {total} records, {len(groups)} distinct prompts")
print(f"dataset.jsonl : {len(train)} records ({len(tp)} prompts)")
print(f"eval.jsonl    : {len(ev)} records ({len(ep)} prompts, "
      f"{100 * len(ev) / total:.1f}%)")
print("prompt overlap: 0")
