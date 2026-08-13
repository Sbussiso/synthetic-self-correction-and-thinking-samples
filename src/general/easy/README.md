[🏠 Home](../../../README.md) / [General](../README.md) / **Easy**

# General / Easy

The easy tier is general knowledge you should get right — and sometimes don't. Questions are single-step: What is the capital of Australia? Does the sun orbit the Earth? Is a spider an insect? Which is heavier, a kilogram of feathers or a kilogram of steel? These are questions where the wrong answer is a common myth or a surface-level assumption, not a miscalculation. Reasoning runs 1–2 think blocks (~51 words on average) and the final answer is usually a bare name or a yes/no (~4 words). In the 3×3×3 grid this tier supplies the overconfidence guardrail: careless errors are not a difficulty-dependent phenomenon, so `wrong_then_fix` records exist here precisely because "obvious" questions are where myths and half-remembered facts actually bite.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "easy" general reasoning looks like

One or two blocks, a quick recall check as the catch, and errors that are plausibly careless rather than conceptual. The recurring failure modes: answering "Sydney" because it is the most famous Australian city; saying the sun orbits the earth because that is what the sky looks like; answering "Spanish" for Brazil because most of South America speaks Spanish; counting Pluto as a ninth planet from a childhood mnemonic; treating a kilogram of steel as heavier than a kilogram of feathers because steel is denser; classifying a spider as an insect because it is small and many-legged. The doubts are tempting in the same way — "maybe parts of the Great Wall cross into Mongolia," "maybe the moon glows a little on its own," "maybe supercooling means 0°C is not really freezing" — and get refuted on the standard fact, with the exception named for what it is. The catch is immediate and names the wrong association; the fix is a single fact closed by a confirmation. Roughly 30% of records carry a persona-only system prompt ("You are a geography expert.") — never a reasoning instruction.

A sample record — a geocentrism-by-appearance misconception caught in the second block:

```json
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Does the sun orbit the Earth?"}, {"role": "assistant", "content": "<think>\nThe sun appears to move across the sky every day, rising in the east and setting in the west. So yes, the sun orbits the Earth.\n</think>\n\n\n<think>\nWait, that's wrong. The sun doesn't orbit the Earth. The Earth orbits the sun. The apparent daily motion of the sun across the sky is due to Earth's rotation on its axis, not the sun orbiting us.\n</think>\n\nNo, the sun does not orbit the Earth. The Earth orbits the sun. The sun appears to move across the sky because the Earth rotates on its axis."}]}
```

## What "medium" general reasoning looks like

One tier up, the confident surface answer starts to fail on content: an ice-cream correlation that hides summer heat, a syllogism whose valid form conceals a false premise, "between you and I" sounding formal but failing the preposition rule. The contract widens to exactly 3 blocks with an independent verification. See [General / Medium](../medium/README.md), or jump to [General / Hard](../hard/README.md) where the reaffirmation has to be a proof or a mechanism, not a reassurance.

---

[🏠 Home](../../../README.md) · [General](../README.md) · ← Easy · [Medium](../medium/README.md) · [Hard](../hard/README.md)
