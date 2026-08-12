# Contributing

[🏠 Back to README](README.md)

This library is hand-written by design. Every record is authored deliberately, and the validator enforces the structure strictly. Use this page to add records without breaking the dataset's invariants.

---

## The quality bar

Each record must pass all of these:

| Rule | Why |
|------|-----|
| ✅ Valid JSON, one record per line | JSONL requires it |
| ✅ Messages are `user` + `assistant`, optionally preceded by `system` | No other roles, no other orders |
| ✅ Assistant content opens with `<think>` and the final answer lives after the last `</think>` | Nothing visible between blocks |
| ✅ Block count matches the tier: easy 1–2, medium 3, hard 4–5 | Depth must scale with difficulty |
| ✅ Final answers are non-empty | Every record answers the question |
| ✅ System prompts, when present, are persona only | "You are a careful mathematician." is fine. "You verify carefully." is not — it's instruction-gating |

Run the gate before committing:

```bash
python validate.py
```

Any structural violation fails the run. Soft observations (duplicate prompts within a file, template-phrase repetition) don't fail but should be addressed — repetition across a file trains the model to reuse stock phrases.

---

## Authoring rules

### What belongs in each mode

Each file is one of three reasoning modes, and every record in it must express that mode:

| Mode | Trajectory |
|------|-----------|
| `wrong_then_fix` | A plausible error, a genuine catch (a sanity check that fails), a corrected answer |
| `right_and_confirm` | A correct first answer, a genuine error check that finds nothing, then verification by a *genuinely different* method |
| `right_doubt_reaffirm` | A correct first answer, a tempting wrong second-guess, then recognizing the *doubt itself* was the error |

Modes are not interchangeable. "Wrong then fix" needs an error that a careful person could plausibly commit — wrong operation, wrong base rate, wrong rule — not a typo. "Right and confirm" needs verification that doesn't just recompute the same way. "Right doubt reaffirm" needs a doubt someone with real understanding might actually voice.

### Wrong answers need to be plausible

Bad: "I thought 3 × 5 was 8." Nobody thinks that.

Good: "I applied the formula without checking whether the premise held." Or: "I confused 6 × 9 with 7 × 8 because they're adjacent on the multiplication table." Those are the errors people actually make.

The error should also be *diagnosable*. Block 2 should name *why* the first attempt was wrong — not just "wait, that's wrong," but what assumption, rule, or instinct led the answer astray.

### Verification must be independent

If block 1 used the formula, block 3 must use something else: estimation, substitution, counting, inversion, a different framing, a special case, a parallel argument. If block 1 derived it from first principles, block 3 can verify against observed consequences.

Never: "Let me recompute the same way and see if I get the same answer." Same-path recomputation is not a check.

### Doubts need to be tempting

The wrong alternative in `right_doubt_reaffirm` should be something a knowledgeable person might genuinely consider after a second look. Confusing `n²` with `2n`. Confusing the empty-product convention with "0 of anything is 0." Confusing "some" with "all." Confusing -1² with (−1)². Confusing the principal square root with the solution set of x² = k.

The reaffirmation in block 3 must explain *why* the doubt felt plausible and *why* it nonetheless fails. This is the teaching moment.

### Final answers

Scale with difficulty. Trivial question: a bare number is fine. Medium: state the answer *and* the method in a sentence or two. Hard: explain the answer and the key insight, 60–150 words, without restating the thinking verbatim.

> The same question may appear across modes. If it does, both paths must reach the same final answer. Divergent answers for identical prompts are contradictory training data and will be rejected.

### System prompts

Use ~30% of the time. Persona only:

```
"You are a careful mathematician."
"You are a helpful assistant."
"You are a Python expert. Answer concisely."
```

Never anything that names reasoning, verification, checking, analysis, or step-by-step instruction. The validator rejects gated prompts on sight.

---

## Step-by-step for a new record

1. Pick the domain, tier, and mode file (e.g. `code/medium/wrong_then_fix.jsonl`).
2. Write the question. Ask something a real person would actually ask.
3. Write Block 1 as the *wrong* path — plausible, specific, diagnosable.
4. Write Block 2 as the catch — what failed, and why it was tempting.
5. Write Block 3 as the fix — complete, correct, then verified independently.
6. (Hard only) Write Blocks 4–5 as additional verification rounds with different methods.
7. Append as a JSONL line. `python validate.py`. If it flags the record, fix it before committing.
8. Commit with a message naming the file and the change, e.g. `Add 1 record to code/medium/wrong_then_fix: late-binding closure`. 

---

## What *not* to do

- ❌ Don't make the first block obviously wrong. The catch has to emerge from the reasoning, not be planted for it.
- ❌ Don't pad blocks with filler ("Let me carefully examine this..."). Substance only.
- ❌ Don't repeat the same closing sentence across a file. Repetition is a training-template risk.
- ❌ Don't add new roles (`tool`, `retriever`, etc.). Only `system`, `user`, `assistant`.
- ❌ Don't let an instruction-gated system prompt slip in. Persona is the whole role.
- ❌ Don't answer a different question than the user asked. If the record is misread in block 1, the fix must re-read the original question, not silently swap it.

---

## When unsure

Look at the existing records in the same file first. The style that already lives there is the one the validator was tuned against, and the one the model already saw.

[🏠 Back to README](README.md)
