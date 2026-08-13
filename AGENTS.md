# AGENTS.md

Guidance for AI agents working in this repository.

---

## The golden rule

**Never edit `dataset.jsonl` directly.** It is a derived artifact, rebuilt from the source library. Always edit the source files (the 27 JSONL files under `math/`, `code/`, `general/`) and then rebuild.

`eval.jsonl` is different — it may be edited directly, because it can contain records that don't exist in any source file. The eval set is truly held-out data: records the model has never seen during training. You can add new evaluation records to `eval.jsonl` by hand, or regenerate it from the source library (see below). Either way, ensure no record appears in both `dataset.jsonl` and `eval.jsonl`.

```
source files (canonical)  →  dataset.jsonl (generated, never edit)
source files + hand-written eval records  →  eval.jsonl (editable)
```

### Rebuilding after any source change

```bash
python -c "
import json, os
train, eval = [], []
for root, dirs, files in sorted(os.walk('.')):
    if '.git' in root or 'charts' in root or '__pycache__' in root: continue
    for fn in sorted(files):
        if not fn.endswith('.jsonl') or fn in ('dataset.jsonl','eval.jsonl'): continue
        with open(os.path.join(root, fn), encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line: continue
                json.loads(line)
                if i % 10 == 0: eval.append(line)
                else: train.append(line)
with open('eval.jsonl','w',encoding='utf-8') as f:
    for l in eval: f.write(l+'\n')
with open('dataset.jsonl','w',encoding='utf-8') as f:
    for l in train: f.write(l+'\n')
print(f'dataset.jsonl: {len(train)} training, eval.jsonl: {len(eval)} eval')
"
```

**Note:** the rebuild script regenerates `eval.jsonl` from the source files (every 10th record). If you've hand-added evaluation records to `eval.jsonl` that don't exist in the source library, the rebuild will overwrite them. To preserve hand-written eval records, either add them to a source file first, or manage `eval.jsonl` separately from the rebuild.

Then validate:

```bash
python validate.py
```

If `validate.py` fails, fix the source files — not `dataset.jsonl`.

---

## Project overview

A seed library of 2,700 training records that teach language models to reason with self-correction. Three reasoning modes (wrong-then-fix, right-and-confirm, right-doubt-reaffirm) across three domains (math, code, general) and three difficulty tiers (easy 1–2 blocks, medium 3 blocks, hard 4–5 blocks). 27 source files, 100 records each.

Built by S'Bussiso Dube (human supervision and review), GLM-5.2, Kimi-k3, and Claude Opus 5.

---

## Structure

```
math/easy/wrong_then_fix.jsonl        ← source file (canonical)
math/easy/right_and_confirm.jsonl     ← source file (canonical)
math/easy/right_doubt_reaffirm.jsonl  ← source file (canonical)
... (24 more source files)
dataset.jsonl                         ← DERIVED — do not edit directly
eval.jsonl                            ← DERIVED — do not edit directly
validate.py                           ← structural validator
charts/                               ← generated charts + generation script
```

---

## Format rules (enforced by validate.py)

1. **One JSON object per line** (JSONL format). Each object has a `messages` array.
2. **Roles are `system` (optional) → `user` → `assistant`**. No other roles, no other ordering.
3. **Assistant content opens with `imd` and the final answer lives after the last `**`. Nothing visible between blocks.
4. **Block count matches the tier**: easy = 1–2, medium = 3, hard = 4–5.
5. **Final answer is non-empty**. Every record answers the question.
6. **System prompts are persona only** — "You are a helpful assistant." is fine. Anything containing "think", "reason", "verify", "check", "analyze", "step by step", "self-correct", or "show your work" is instruction-gating and will be rejected.
7. **No `[Block N: ...]` labels** inside think blocks. Natural prose reasoning only.
8. **Newlines inside content strings are JSON-escaped (`\n`)**. Think tags use literal `<` and `>`.
9. **Unix line endings** (`\n`, not `\r\n`).

---

## What each mode requires

### `wrong_then_fix.jsonl`
- Block 1: A plausible WRONG first attempt (a mistake a careful person could make — wrong operation, wrong base rate, wrong rule — not a typo)
- Block 2: CATCH — name what went wrong and why it was tempting
- Block 3 (or more): FIX — correct approach with full working, then verify by a genuinely different method
- Final answer: states the correct answer with brief reasoning

### `right_and_confirm.jsonl`
- Block 1: A CORRECT first attempt (requires real thinking)
- Block 2: Genuine error check (examining for common mistakes, edge cases — not a rubber stamp)
- Block 3: INDEPENDENT verification using a DIFFERENT method (never just recompute the same way)
- Final answer: states the answer with brief reasoning

### `right_doubt_reaffirm.jsonl`
- Block 1: A CORRECT first answer
- Block 2: A genuinely tempting DOUBT — a plausible wrong alternative someone knowledgeable might voice
- Block 3: Realize the doubt was the error, explain why the original holds
- (Hard tier: Blocks 4–5 add deeper verification or a second rejected doubt)
- Final answer: states the (original) correct answer with brief reasoning

---

## Quality bar

- **Wrong answers must be plausible.** "I thought 3 × 5 was 8" is too stupid. "I confused 6 × 9 with 7 × 8 because they're adjacent on the multiplication table" is real.
- **Verification must be independent.** If block 1 used the formula, block 3 uses estimation, substitution, or a different framing. Same-path recomputation is not verification.
- **Doubts must be tempting.** The wrong alternative should be something a knowledgeable person might genuinely consider. Confusing n² with 2n, confusing -1² with (-1)², confusing "some" with "all."
- **No template phrases.** No sentence should repeat 4+ times in a file. Vary how you say "the original answer was correct" — use different words each time.
- **Final answers scale with difficulty.** Trivial: bare answer. Medium: answer + method in 1–2 sentences. Hard: 60–150 words explaining the answer and key insight.

---

## What NOT to do

- ❌ Do not edit `dataset.jsonl` or `eval.jsonl` directly
- ❌ Do not use scripts to generate record content — records are authored, not generated
- ❌ Do not add instruction-gated system prompts ("think step by step", "verify carefully", etc.)
- ❌ Do not add `[Block 1: ...]` labels inside think blocks
- ❌ Do not make the wrong first answer obviously wrong — the catch must emerge from reasoning
- ❌ Do not pad blocks with filler ("Let me carefully examine this...")
- ❌ Do not repeat the same closing sentence across a file
- ❌ Do not add new roles (`tool`, `retriever`, etc.)
- ❌ Do not let prose appear between think blocks — only the final answer lives outside the tags
- ❌ Do not change the block count for a tier (easy must be 1–2, medium 3, hard 4–5)

---

## When you're done editing

1. Run `python validate.py` — must exit 0
2. Rebuild `dataset.jsonl` and `eval.jsonl` from the source files (see above)
3. Commit with a message naming the files changed and what was done
4. Push