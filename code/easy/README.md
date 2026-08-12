[🏠 Home](../../README.md) / [Code](../README.md) / **Easy**

# Code / Easy

The easy tier is Python you should get right — and sometimes don't. Questions are single-step: the value of `len('hello')`, `2 + 2`, `bool(0)`, what `10 // 3` returns, whether `range(5)` includes 5, what `print()` returns. Reasoning runs 1–2 think blocks (~51 words on average) and the final answer is usually a bare value (~4 words). In the 3×3×3 grid this tier supplies the overconfidence guardrail: careless errors are not a difficulty-dependent phenomenon, so `wrong_then_fix` records exist here precisely because "obvious" questions are where misread operators and half-remembered facts actually bite.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "easy" code looks like

One or two blocks, a quick recall check as the catch, and errors that are plausibly careless rather than conceptual. The recurring failure modes: counting the quote marks as characters of `'hello'`; reading `//` as ordinary division; assuming all numbers are truthy so `bool(0)` must be True; thinking `True + True` can't be 2 "because they're booleans"; assuming `range(5)` starts at 1 or ends at 5; believing `print()` returns the string it printed; expecting `3 + '4'` to coerce like it does in JavaScript. The doubts import conventions from other languages — "maybe `==` checks identity like Java," "maybe Python ignores case like SQL" — and get refuted on Python's own rules. The catch is immediate and names the misapplied rule; the fix is a single fact closed by a confirmation. Roughly 30% of records carry a persona-only system prompt ("You are a helpful programming assistant.") — never a reasoning instruction.

A sample record — a "count the quotes" misconception caught in the second block:

```json
{"messages": [{"role": "user", "content": "What does `len('hello')` return in Python?"}, {"role": "assistant", "content": "<think>\nLet me count the characters in 'hello'. h, e, l, l, o - that's 5. But the string literal includes the quote marks, so maybe len() counts those too. 5 + 1 = 6.\n</think>\n\n<think>\nWait, that's wrong. The quotes are delimiters that tell Python where the string starts and ends. They are not part of the string content. Python strings also don't have a null terminator. len('hello') just counts the characters: h, e, l, l, o = 5. My answer of 6 was incorrect.\n</think>\n\n5"}]}
```

## What "medium" code looks like

One tier up, the confident answer starts to fail on semantics: a mutable default list shared across calls, `y = x` aliasing instead of copying, elements skipped while a list mutates under iteration. The contract widens to exactly 3 blocks with an independent verification. See [Code / Medium](../medium/README.md), or jump to [Code / Hard](../hard/README.md) where verification means hand-tracing the descriptor protocol or the MRO.

---

[🏠 Home](../../README.md) · [Code](../README.md) · ← Easy · [Medium](../medium/README.md) · [Hard](../hard/README.md)
