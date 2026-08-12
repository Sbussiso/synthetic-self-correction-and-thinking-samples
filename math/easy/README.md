[🏠 Home](../../README.md) / [Math](../README.md) / **Easy**

# Math / Easy

The easy tier is math you should get right — and sometimes don't. Questions are single-step: a multiplication fact, a percentage of a round number, a parity or primality call on a small integer. Reasoning runs 1–2 think blocks (~51 words on average) and the final answer is usually a bare number (~4 words). In the 3×3×3 grid this tier supplies the overconfidence guardrail: careless errors are not a difficulty-dependent phenomenon, so `wrong_then_fix` records exist here precisely because "obvious" questions are where misreads and misremembered facts actually happen.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "easy" math looks like

One or two blocks, a quick sanity check as the catch, and errors that are plausibly careless rather than conceptual. The recurring failure modes: confusing 6 × 9 with 7 × 8 because they sit adjacent on the multiplication table; rounding 346 up to 400 when the tens digit says round down; counting an extra decimal place in 0.5 × 0.5; declaring 51 prime because nothing *obvious* divides it; treating 1 as prime because it fits the informal definition. The catch is immediate and names the skipped rule; the fix is a single computation closed by a confirmation. Roughly 30% of records carry a persona-only system prompt ("You are a math tutor.") — never a reasoning instruction.

A sample record — a primality misconception caught in the second block:

```json
{"messages": [{"role": "user", "content": "Is 1 a prime number?"}, {"role": "assistant", "content": "<think>\nIs 1 prime? It's only divisible by 1 and itself, which matches the informal definition. So yes, 1 is prime.\n</think>\n\n<think>\nWait, the proper definition of a prime is a number with exactly two distinct positive divisors. 1 has only one positive divisor (1 itself), so it doesn't meet that criterion. 1 is not prime by the standard definition.\n</think>\n\nNo, 1 is not prime. It has only one positive divisor."}]}
```

## What "medium" math looks like

One tier up, the wrong approach starts to *feel* right: a 25% discount followed by a 25% rise that doesn't return to the start, marbles drawn without replacement, averages that ignore their weights. The contract widens to exactly 3 blocks with an independent verification. See [Math / Medium](../medium/README.md), or jump to [Math / Hard](../hard/README.md) where verification itself becomes a computation.

---

[🏠 Home](../../README.md) · [Math](../README.md) · ← Easy · [Medium](../medium/README.md) · [Hard](../hard/README.md)
