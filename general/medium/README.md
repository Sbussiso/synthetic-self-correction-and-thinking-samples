[🏠 Home](../../README.md) / [General](../README.md) / **Medium**

# General / Medium

The medium tier is where the plausible answer starts to outrun the true one. Questions are conceptual but concrete: a causal correlation hiding a confounder (ice cream and drowning, sugar and hyperactivity), a syllogism whose valid form conceals a false premise, a litotes that flips polarity twice ("not insignificant"), a hypercorrected grammar form, a famous fact that is subtly wrong — Napoleon was not unusually short, Edison did not invent the light bulb from nothing, the Great Wall is not visible from space with the naked eye. Every record runs exactly 3 think blocks (~168 words on average), and the final answer states the result *and* the reasoning in a sentence or two (~35 words). In the 3×3×3 grid this tier carries the core teaching load: content traps that survive a casual gut check but fall to one independent check against the passage, the rule, or the physics.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "medium" general reasoning looks like

Exactly three blocks — answer, then catch (or scrutinize, or doubt), then verify by a different route. The errors are conceptual, not slips: reading a correlation as causation without hunting the confounder; treating a valid syllogism as sound ("all birds can fly, penguins are birds"); resolving a pronoun to the nearest noun instead of the one the grammar forces ("She was happy" after "John gave the book to Mary"); preferring "between you and I" because it sounds educated; collapsing a double negation the wrong way; trusting famous-fact memory over the actual record. The doubts are tempting in the same way — "don't Earth and sun orbit a barycenter, not each other?", "if Coriolis sets hurricane rotation, why not a sink's?", "if we share 98% of our DNA with chimps, isn't 'we evolved from them' close enough?" — and block 3 explains both why the doubt felt plausible and why the mechanics still favor the first answer. Verification is independent by construction: gender agreement resolved against sentence structure, a leap-year rule checked against 400-year arithmetic, buoyancy checked against how a balloon is actually piloted, a confounder hunted by asking what would happen if ice cream were banned — never the same reasoning restated.

A sample record — a correlation-as-causation trap, caught by hunting the confounder:

```json
{"messages": [{"role": "user", "content": "Ice cream sales and drowning deaths rise together. Does ice cream cause drowning?"}, {"role": "assistant", "content": "<think>\nIce cream sales and drowning deaths are positively correlated - they rise and fall together. When two things are correlated, it often means one causes the other. Since ice cream sales rise before or alongside drowning deaths, it is plausible that ice cream consumption leads to more drowning. Perhaps eating ice cream makes people go swimming, or sugar causes recklessness. So yes, ice cream likely causes drowning.\n</think>\n<think>\nI made a classic error: I jumped from correlation to causation. Just because two variables rise together does not mean one causes the other. I need to look for a confounding variable - a third factor that causes both.\n\nWhat causes both ice cream sales and drowning deaths to rise? Summer heat and warm weather. In summer:\n- More people buy ice cream (hot weather leads to desire for cold treats)\n- More people swim, leading to more drowning deaths\n\nThe confounder is warm weather. Both variables are effects of the same cause, not causes of each other.\n</think>\n<think>\nVerification:\n- Is there a mechanism by which ice cream causes drowning? No plausible direct mechanism.\n- Is there a common cause? Yes - warm summer weather increases both ice cream consumption and swimming activity.\n- This is a textbook example of 'correlation does not imply causation' with a confounding variable.\n- If ice cream caused drowning, banning ice cream would reduce drownings - clearly absurd.\n\nThe correct explanation: summer weather is the common cause of both.\n</think>\n**No**, ice cream does not cause drowning. The correlation between ice cream sales and drowning deaths is due to a confounding variable: warm summer weather. In summer, people both buy more ice cream and swim more frequently (leading to more drowning accidents). The two variables share a common cause but do not cause each other. This is a classic example of 'correlation does not imply causation.'"}]}
```

## The tiers on either side

Medium sits between a sanity check and a mechanism-level defense. [General / Easy](../easy/README.md) errors are careless myths caught in a single block; [General / Hard](../hard/README.md) answers need 4–5 blocks because the reaffirmation is a proof or a physical mechanism, not a reassurance. All three modes run at all three tiers — being wrong is not a property of the question's difficulty.

---

[🏠 Home](../../README.md) · [General](../README.md) · [Easy](../easy/README.md) · ← Medium · [Hard](../hard/README.md)
