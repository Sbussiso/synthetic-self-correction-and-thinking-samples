[🏠 Home](../../README.md) / [Math](../README.md) / **Medium**

# Math / Medium

The medium tier is where the wrong approach starts to feel right. Questions are multi-step but concrete: compound percentages, probability with confounders, inclusion–exclusion, simultaneous equations, ratio and unit conversion, number-theory basics. Every record runs exactly 3 think blocks (~168 words on average), and the final answer states the result *and* the method in a sentence or two (~35 words). In the 3×3×3 grid this tier carries the core teaching load: traps that survive a casual gut check but fall to one independent verification.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "medium" math looks like

Exactly three blocks — compute, then catch (or scrutinize, or doubt), then verify by a different route. The errors are conceptual, not slips: taking "15% of 240" as Tuesday's total instead of adding the increase on; assuming a 25% fall plus a 25% rise returns to the start; averaging 60 and 80 while ignoring the 30/70 weights; dividing distance by fuel rate and calling the result litres; drawing two marbles without replacement but multiplying as if the bag were unchanged; adding P(A) + P(B) without subtracting the intersection. Verification is independent by construction — a bracketing estimate, a unit conversion, substitution back into the original numbers — never the same computation twice.

A sample record — the compound-percentage trap, caught by naming the shifting base:

```json
{"messages": [{"role": "system", "content": "You are a careful assistant."}, {"role": "user", "content": "A jacket costs 80 pounds. It is reduced by 25% in a sale. Later the sale price is increased by 25%. What is the final price?"}, {"role": "assistant", "content": "<think>\nStart at 80. A 25% reduction removes 25% of 80 = 20, leaving 60.\nMy instinct is that a 25% rise now returns it to 80, since it went down 25% and back up 25%.\n</think>\n<think>\nThat instinct is worth distrusting. The two percentages are taken from different bases. The reduction was 25% of 80. The increase is 25% of 60.\n25% of 60 = 15, so the final price is 60 + 15 = 75, not 80.\n</think>\n<think>\nConfirm the asymmetry is real rather than an arithmetic slip. To get from 60 back to 80 you need to add 20, and 20 out of 60 is 33%, not 25%. So a 25% rise cannot undo a 25% fall. The two operations are genuinely not inverses.\n</think>\nThe final price is 75 pounds, not 80. The increase is calculated on the reduced price, so it adds less than the discount took away."}]}
```

## The tiers on either side

Medium sits between a sanity check and a proof. [Math / Easy](../easy/README.md) errors are careless and get caught in a single block; [Math / Hard](../hard/README.md) answers need 4–5 blocks because verification is itself a computation. All three modes run at all three tiers — being wrong is not a property of the question's difficulty.

---

[🏠 Home](../../README.md) · [Math](../README.md) · [Easy](../easy/README.md) · ← Medium · [Hard](../hard/README.md)
