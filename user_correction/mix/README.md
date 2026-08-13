[🏠 Home](../../README.md) / **User correction**

# User correction

Multi-turn conversations where the **user** actively corrects, challenges, or asks the assistant to verify an answer. This is the only category that teaches a behavior the other three domains cannot: responding to *external* feedback rather than only internal self-correction. Every other record in the library is a single user turn followed by the assistant reasoning in private; here the user speaks twice, and what they say on the second turn shapes what the assistant does next.

This is also the only category that does **not** separate difficulty into easy/medium/hard folders. It lives in a single `mix/` folder with an even blend of all three depths in each file — roughly 33 easy, 34 medium, and 33 hard records per mode — so that the assistant's response length is driven by the question's difficulty, not by the folder it was filed in.

## In this folder

| Tier | Blocks | Records | Folder |
|------|:--:|:--:|------|
| Mix | 1–5 (even blend) | 300 | [mix/](mix/) |

300 records across 3 files, exactly 100 per file. Roughly 30% of records carry a persona-only system prompt ("You are a knowledgeable assistant.") — never a reasoning instruction. Every record is multi-turn: four messages, two of them from the user.

## The four-message structure

Every record follows the same shape:

```
1. user      → the question
2. assistant → an initial answer (with its own think blocks + final answer)
3. user      → a correction, a challenge, or a request to verify
4. assistant → the response to that feedback (with its own think blocks + final answer)
```

The second user turn is where the teaching happens. It falls into one of three shapes, and each of the three mode files trains one of them:

| File | Second user turn | What the assistant learns |
|------|------------------|---------------------------|
| `wrong_then_fix.jsonl` | A correction: "no, the answer is X, because..." | Accept the correction gracefully, name the exact mistake, and re-derive correctly |
| `right_and_confirm.jsonl` | A request to verify: "are you sure? show me another way" | Provide independent verification by a genuinely different method, not a recompute |
| `right_doubt_reaffirm.jsonl` | A challenge: "that's wrong, it's actually Y" where Y is the *wrong* alternative | Defend the correct answer firmly, show why the challenge itself is the error |

The split between "the user is right" (`wrong_then_fix`) and "the user is wrong" (`right_doubt_reaffirm`) is deliberate. A model that only ever concedes to users becomes sycophantic; a model that only ever defends itself never learns from feedback. This category holds both, in equal measure, so the lesson is: the assistant follows the evidence, not the user's confidence.

## Difficulty is mixed within each file

Each file holds an even blend of depths. The block count of the *second* assistant turn (the one that responds to feedback) tracks the difficulty of that particular record:

| Depth | Second-turn blocks | Approx. records per file |
|-------|:--:|:--:|
| Easy | 1–2 | ~33 |
| Medium | 3 | ~34 |
| Hard | 4–5 | ~33 |

Easy records: a quick catch and a one-line fix. Medium records: the fix is worked across three blocks with an independent check. Hard records: four-to-five blocks that restate the givens, diagnose the error, re-derive, verify by a second method, and substitute back into the premise.

## A sample record from each mode

### `wrong_then_fix` — accepting a correction ([file](wrong_then_fix.jsonl))

The assistant halves a substitution, the user corrects it, and the assistant names exactly what it skipped:

```json
{"messages": [{"role": "user", "content": "what is 5 x 5 if 5 is now 2 instead of 5"}, {"role": "assistant", "content": "<think>\nThe question redefines 5 as 2, so I should substitute. 5 x 5 becomes 2 x 5 = 10.\n</think>\n\n10."}, {"role": "user", "content": "no, the answer is 4. I said 5 is now 2, so it is 2 x 2, not 2 x 5."}, {"role": "assistant", "content": "<think>\nThat is right and my substitution was half-done. If 5 is redefined as 2, the redefinition applies to every occurrence of 5, not just the first. Both operands are the same symbol, so both become 2.\n</think>\n\n<think>\nRedoing it: 5 x 5 with 5 replaced throughout gives 2 x 2 = 4. I substituted into the left operand and left the right one at its old value, which is what produced 10.\n</think>\n\n4. You are right: substituting 5 with 2 everywhere gives 2 x 2 = 4. I replaced only the first operand."}]}
```

The concession names the specific failure ("I substituted into the left operand and left the right one at its old value"), not a generic "sorry, you're right."

### `right_and_confirm` — verifying on request ([file](right_and_confirm.jsonl))

The assistant's first answer is correct; the user asks for proof, and the assistant confirms by a different route:

```json
{"messages": [{"role": "user", "content": "What is 15% of 60?"}, {"role": "assistant", "content": "<think>\n10% of 60 is 6, and 5% is half of that, 3. Adding gives 6 + 3 = 9.\n</think>\n\n9."}, {"role": "user", "content": "are you sure? show me another way"}, {"role": "assistant", "content": "<think>\nHappy to check it by a different route rather than repeating the same split.\n</think>\n\n<think>\nConverting to a fraction: 15% is 15/100, so 15/100 x 60 = 900/100 = 9. As a decimal, 0.15 x 60 = 9. A rough sanity check also fits, since 15% is a little under a sixth and a sixth of 60 is 10, so a value just under 10 is expected.\n</think>\n\n9. Confirmed three ways: 10% plus 5% gives 6 + 3, the fraction 15/100 x 60 gives 900/100, and 0.15 x 60 gives 9 directly."}]}
```

The verification uses a fraction conversion, a decimal multiplication, and a magnitude sanity check — three genuinely different routes, not the original split repeated.

### `right_doubt_reaffirm` — defending a correct answer ([file](right_doubt_reaffirm.jsonl))

The user insists the assistant is wrong; the assistant checks the challenge seriously, finds the challenge itself is the error, and holds its ground:

```json
{"messages": [{"role": "user", "content": "What is 0.1 + 0.2 in Python?"}, {"role": "assistant", "content": "<think>\nPython uses binary floating point, so 0.1 and 0.2 cannot be represented exactly. Their sum carries a small error and displays as 0.30000000000000004.\n</think>\n\n0.30000000000000004."}, {"role": "user", "content": "that's wrong, it's 0.3. you're overcomplicating a simple sum."}, {"role": "assistant", "content": "<think>\nWorth taking seriously, since 0.3 is the correct value mathematically and most calculators show it. If Python rounded the display, 0.3 would be what appears.\n</think>\n\n<think>\nBut it does not round at that precision. Entering 0.1 + 0.2 at the interpreter prints 0.30000000000000004, and 0.1 + 0.2 == 0.3 evaluates to False, which would be impossible if the sum were exactly 0.3. The arithmetic is right; the representation is the point. I stand by the original answer.\n</think>\n\nIt really is 0.30000000000000004 in Python. Mathematically the sum is 0.3, but binary floating point cannot represent 0.1 or 0.2 exactly, which is why 0.1 + 0.2 == 0.3 returns False."}]}
```

The challenge is taken seriously first ("Worth taking seriously, since 0.3 is the correct value mathematically") — the assistant does not dismiss the user — and then refuted with a check the user can run themselves (`0.1 + 0.2 == 0.3` returns `False`). Defending a correct answer is not stubbornness; it is reasoning that survives being checked.

## What the hard records add

At the hard end, the second assistant turn opens by restating the givens before doing anything else — the same anchoring rule that governs the single-turn domains. A representative hard `right_and_confirm` record: a medical test with 99% sensitivity and 95% specificity at a 1-in-1,000 base rate, where the user pushes for a precise answer verified two ways. The assistant restates sensitivity, specificity, and the prior; computes via Bayes' theorem (~1.9%); confirms with a 100,000-person frequency table (99 true positives against 4,995 false positives); and finally substitutes the 95% guess back into the population to show it is inconsistent with the base rate. Five blocks, three independent methods, one concession to the base rate the first answer ignored.

Hard `right_doubt_reaffirm` records work the same way at the other end: the user's challenge is examined on its own terms before it is rejected, and the rejection rests on a mechanism (e.g. why the night sky is dark is *not* because stars are sparse but because of finite light travel time and cosmic expansion), not on restating the original answer louder.

## Topic coverage

Because this category is about the *interaction* rather than a subject, the questions span all three other domains:

- **Math:** unit redefinition and substitution (`5 is now 2`), operator precedence (`7 - 3 + 2`), primality of 1, percentage compounding (markup-then-discount, stock drop-then-rise), base-rate neglect in medical testing, negative-number squaring, floating-point representation (`0.1 + 0.2`).
- **Code:** Python floating point, equality semantics, type behavior — the same misconceptions that appear in `code/` but here surfaced by a user who pushes back.
- **General:** capitals misremembered by fame (Turkey → Istanbul vs Ankara), February's leap-day exception, ice floating and *why* it's less dense, Earth-Sun orbit and the barycenter, whether 0 is an even prime, why the night sky is dark.

The same question sometimes appears in a `user_correction` record and in a single-turn domain record. That is intentional, just as it is across the other modes: the question does not determine whether the assistant is right or wrong, or whether it concedes or holds.

---

[🏠 Home](../../README.md)