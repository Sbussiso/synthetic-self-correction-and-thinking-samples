#!/usr/bin/env python3
"""Structural validator for the Self Correction and Thinking seed library.

Run from the repository root:

    python validate.py

Exits non-zero if any hard invariant is violated. Soft observations (duplicate
prompts, stock-phrase repetition) are reported but do not fail the run.
"""
import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TIER_BLOCKS = {"easy": {1, 2}, "medium": {3}, "hard": {4, 5}, "mix": {1, 2, 3, 4, 5}}
# any system prompt naming the target behaviour is instruction-gating
GATED = re.compile(
    r"\b(think|thinking|step by step|reason|reasoning|verif|double.?check|"
    r"self.?correct|analy[sz]e|show your work|check your)\b", re.I)

errors = []
rows = []

for path in sorted(glob.glob("*/*/*.jsonl")):
    parts = Path(path).parts
    domain, tier = parts[0], parts[1]
    for i, line in enumerate(open(path, encoding="utf-8")):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{path}[{i}] invalid JSON: {e}")
            continue
        msgs = rec.get("messages")
        loc = f"{path}[{i}]"
        if not msgs:
            errors.append(f"{loc} missing messages")
            continue

        roles = [m["role"] for m in msgs]
        body = roles[1:] if roles and roles[0] == "system" else roles
        # optional system, then strictly alternating user/assistant, ending on assistant
        ok = (len(body) >= 2 and len(body) % 2 == 0
              and all(r == ("user" if k % 2 == 0 else "assistant")
                      for k, r in enumerate(body)))
        if not ok:
            errors.append(f"{loc} unexpected role sequence {roles}")
            continue

        if roles[0] == "system" and GATED.search(msgs[0]["content"]):
            errors.append(f"{loc} system prompt instructs the behaviour: "
                          f"{msgs[0]['content'][:70]!r}")

        # every assistant turn must satisfy the block invariants, not just the last
        assistants = [m["content"] for m in msgs if m["role"] == "assistant"]
        all_blocks, per_turn, broken = [], [], False
        for t, a in enumerate(assistants):
            where = f"{loc} turn {t + 1}" if len(assistants) > 1 else loc
            blocks = re.findall(r"<think>(.*?)</think>", a, re.S)
            if a.count("<think>") != a.count("</think>") or len(blocks) != a.count("<think>"):
                errors.append(f"{where} unbalanced or nested think tags")
                broken = True
                break
            if not blocks:
                errors.append(f"{where} no think block")
                broken = True
                break
            if not a.startswith("<think>"):
                errors.append(f"{where} content before the first think block")
            if a.rstrip().endswith("</think>"):
                errors.append(f"{where} ends inside a think block, no final answer")
            if "<think>" in a.split("</think>")[-1]:
                errors.append(f"{where} think tag after the final block")
            if not a.split("</think>")[-1].strip():
                errors.append(f"{where} empty final answer")
            stray = [x.strip() for x in re.split(r"</?think>", a)[:-1:2] if x.strip()]
            if stray:
                errors.append(f"{where} prose between think blocks: {stray[0][:60]!r}")
            if len(blocks) not in TIER_BLOCKS[tier]:
                errors.append(f"{where} {tier} tier requires "
                              f"{sorted(TIER_BLOCKS[tier])} blocks per assistant turn, "
                              f"found {len(blocks)}")
            all_blocks += blocks
            per_turn.append(len(blocks))
        if broken:
            continue

        first_user = next(m["content"] for m in msgs if m["role"] == "user")
        rows.append(dict(path=path, i=i, domain=domain, tier=tier,
                         prompt=first_user, blocks=all_blocks,
                         turns=len(assistants), per_turn=per_turn,
                         has_sys=roles[0] == "system"))

# ---- per-file summary -------------------------------------------------
by_file = defaultdict(list)
for r in rows:
    by_file[r["path"]].append(r)

print(f"{'file':46s} {'n':>4s} {'blocks':>14s} {'sys':>5s} {'avg':>6s}")
for path, rs in sorted(by_file.items()):
    counts = sorted(Counter(n for r in rs for n in r["per_turn"]).items())
    n_sys = sum(r["has_sys"] for r in rs)
    mt = sum(r["turns"] > 1 for r in rs)
    avg = sum(sum(len(b.strip()) for b in r["blocks"]) for r in rs) // len(rs)
    flag = "" if len(rs) == 100 else f"  <- {100 - len(rs)} to write"
    if mt:
        flag = f"  [{mt} multi-turn]" + flag
    print(f"{'/'.join(Path(path).parts):46s} {len(rs):4d} {str(counts):>14s} "
          f"{n_sys:5d} {avg:6d}{flag}")

print(f"\n{len(rows)} records in {len(by_file)} files")

# ---- soft observations ------------------------------------------------
seen = defaultdict(list)
for r in rows:
    seen[r["prompt"]].append(r)

within = [(p, v) for p, v in seen.items()
          if len({x["path"] for x in v}) == 1 and len(v) > 1]
cross_tier = [(p, v) for p, v in seen.items()
              if len({(x["domain"], x["tier"]) for x in v}) > 1]
if within:
    print(f"\nduplicate prompt within a single file ({len(within)}) - always a defect")
    for p, v in within[:10]:
        print(f"  {'/'.join(Path(v[0]['path']).parts)}  {[x['i'] for x in v]}  {p[:52]!r}")
if cross_tier:
    print(f"\nsame prompt at two difficulty tiers ({len(cross_tier)}) - conflicts with "
          f"principle 2, since difficulty is a property of the question")
    for p, v in cross_tier[:10]:
        print(f"  {v[0]['domain']}  {sorted({x['tier'] for x in v})}  {p[:56]!r}")

# A file can pass the repeated-sentence check and still be templated, because
# every block opens the same way and then diverges. Check openings separately.
print("\nblock openings sharing the same first four words (template risk):")
openings = []
for path, rs in by_file.items():
    depth = max(len(r["blocks"]) for r in rs)
    for pos in range(depth):
        at = [r["blocks"][pos].strip() for r in rs if len(r["blocks"]) > pos]
        if len(at) < 20:
            continue
        phrase, n = Counter(" ".join(b.split()[:4]) for b in at).most_common(1)[0]
        openings.append((n / len(at), n, len(at), path, pos + 1, phrase))
for share, n, tot, path, pos, phrase in sorted(openings, reverse=True)[:8]:
    mark = "  <-- templated" if share >= 0.5 else ""
    print(f"  {share:4.0%} ({n}/{tot})  {'/'.join(Path(path).parts):40s} block {pos}  "
          f"{phrase!r}{mark}")

print("\nmost repeated reasoning sentence per file (template risk):")
worst = []
for path, rs in by_file.items():
    sents = [s.strip() for r in rs for b in r["blocks"]
             for s in re.split(r"(?<=[.?!])\s+", b.strip()) if len(s.strip()) > 28]
    if sents:
        s, n = Counter(sents).most_common(1)[0]
        worst.append((n, path, s))
for n, path, s in sorted(worst, reverse=True)[:8]:
    print(f"  {n:4d}x  {'/'.join(Path(path).parts):42s} {s[:56]!r}")

# ---- train/eval split ------------------------------------------------
if Path("dataset.jsonl").exists() and Path("eval.jsonl").exists():
    def prompts(path):
        out = []
        for line in open(path, encoding="utf-8"):
            if line.strip():
                ms = json.loads(line)["messages"]
                # key on the FIRST user turn, matching build.py
                out.append(next(m["content"] for m in ms if m["role"] == "user"))
        return out

    tr, ev = prompts("dataset.jsonl"), prompts("eval.jsonl")
    leak = set(tr) & set(ev)
    print(f"\nsplit: dataset.jsonl {len(tr)} records, eval.jsonl {len(ev)} records")
    if len(tr) + len(ev) != len(rows):
        errors.append(f"split holds {len(tr) + len(ev)} records but the source has {len(rows)}")
    if leak:
        errors.append(f"{len(leak)} prompt(s) appear in BOTH dataset.jsonl and eval.jsonl, "
                      f"so the model is scored on questions it trained on "
                      f"(e.g. {sorted(leak)[0][:50]!r}). Rebuild with build.py.")
    else:
        print("       no prompt appears in both files")

if errors:
    print(f"\n{len(errors)} STRUCTURAL ERROR(S):")
    for e in errors[:40]:
        print(f"  {e}")
    sys.exit(1)
print("\nall structural invariants hold")
