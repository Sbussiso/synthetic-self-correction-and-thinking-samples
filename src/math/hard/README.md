[🏠 Home](../../../README.md) / [Math](../README.md) / **Hard**

# Math / Hard

The hard tier is mathematics where the answer is a proof, not a number: the irrationality of e and φ, convergence debates (harmonic, alternating harmonic, p-series), calculus identities and the scope of their hypotheses, linear algebra counterfactuals, independence results (the continuum hypothesis, the axiom of choice), the halting problem. Records run 4–5 think blocks (~552 words on average) and close with 60–150-word final answers that carry the key insight (~96 words on average). In the 3×3×3 grid this tier teaches effort-matching from the top: deep problems earn multiple rounds of catching, fixing, and verifying before an answer is allowed to stand.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "hard" math looks like

The first attempt commits to an approach that is wrong *in an interesting way*: simple interest instead of compound; reading "95% accurate" as a 95% probability of disease against a 1% base rate; integrating x^2 − 2x without checking which curve sits on top; declaring a series convergent because its terms go to zero. Blocks 2–3 catch and repair; blocks 4–5 verify by genuinely different methods — a population-of-1000 table set against the Bayes formula, year-by-year recomputation against the closed form, numerical bracketing against exact integration, Oresme grouping against the integral test against ln(n) asymptotics. Doubts at this tier are deep and get rejected by proofs rather than gut checks: "does 0.999... really equal 1?", "did someone prove the twin prime conjecture?", "maybe a stronger axiom system settles the continuum hypothesis."

A sample record — a calculus sign error, caught, repaired, then verified twice more by independent methods:

```json
{"messages": [{"role": "user", "content": "Find the area between the curves y = x^2 and y = 2x from x = 0 to x = 2."}, {"role": "assistant", "content": "<think>\nArea = integral from 0 to 2 of (x^2 - 2x) dx.\n= [x^3/3 - x^2] from 0 to 2\n= (8/3 - 4) - (0 - 0)\n= 8/3 - 12/3\n= -4/3\nThe area is -4/3, so the absolute value is 4/3.\n</think>\n\n\n<think>\nWait, I need to be more careful. The \"area between curves\" should be the integral of the absolute difference, not just the integral of the difference. The curves might cross within the interval, meaning one function is above the other in some regions and below in others. Let me check where they intersect.\nx^2 = 2x gives x^2 - 2x = 0, so x(x - 2) = 0, meaning x = 0 or x = 2. So they intersect at the endpoints. But I need to know which is above which in between. At x = 1: x^2 = 1, 2x = 2. So 2x is above x^2 on (0, 2). My integral of (x^2 - 2x) gave a negative value because x^2 is below 2x in this range. The absolute area should use |x^2 - 2x| = 2x - x^2 in this interval.\n</think>\n\n\n<think>\nCorrect approach: Since 2x is above x^2 on (0, 2), the area is:\nintegral from 0 to 2 of (2x - x^2) dx\n= [x^2 - x^3/3] from 0 to 2\n= (4 - 8/3) - (0 - 0)\n= 4 - 8/3\n= 12/3 - 8/3\n= 4/3\nThe area is 4/3.\n</think>\n\n\n<think>\nLet me verify numerically. At x = 0: both curves are at 0. At x = 1: gap = 2(1) - 1^2 = 1. At x = 2: both curves are at 4 (they meet). The gap starts at 0, goes up to a maximum, then back to 0. The maximum gap is at d/dx(2x - x^2) = 2 - 2x = 0, so x = 1, gap = 1. The shape is roughly triangular with base 2 and height 1, so area is approximately 1/2 times 2 times 1 = 1. Our answer of 4/3 is about 1.33, which is in the right ballpark (the curve bulges above the triangle). Confirmed.\n</think>\n\n\n<think>\nFinal check: the function 2x - x^2 = -(x^2 - 2x) = -(x-1)^2 + 1. So the area is integral of (1 - (x-1)^2) from 0 to 2. Substituting u = x - 1: integral from -1 to 1 of (1 - u^2) du = [u - u^3/3] from -1 to 1 = (1 - 1/3) - (-1 - (-1/3)) = (2/3) - (-2/3) = 4/3. Confirmed by yet another method.\n</think>\n\nThe area between the curves is **4/3** square units.\n\nThe key correction: the curves y = x^2 and y = 2x intersect at x = 0 and x = 2. On the interval (0, 2), 2x is above x^2 (e.g., at x = 1: 2x = 2 vs x^2 = 1). The area is the integral of the upper curve minus the lower curve:\n\nArea = integral from 0 to 2 of (2x - x^2) dx = [x^2 - x^3/3] from 0 to 2 = (4 - 8/3) = 4/3\n\nThe initial error was integrating (x^2 - 2x) without checking which function is on top, which gave a negative value (-4/3). The correct area uses the absolute difference: |x^2 - 2x| = 2x - x^2 on this interval."}]}
```

## The easier tiers

Hard is where the three modes stretch furthest apart: a wrong first block costs two more blocks of repair, and a confirmed answer can accumulate four independent verifications. [Math / Medium](../medium/README.md) carries the same contract at 3 blocks against conceptual traps; [Math / Easy](../easy/README.md) compresses it to 1–2 blocks against careless errors. Difficulty changes the depth of the reasoning, never whether the reasoning happens.

---

[🏠 Home](../../../README.md) · [Math](../README.md) · [Easy](../easy/README.md) · [Medium](../medium/README.md) · ← Hard
