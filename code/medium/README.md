[🏠 Home](../../README.md) / [Code](../README.md) / **Medium**

# Code / Medium

The medium tier is where the confident answer starts to fail. Questions are multi-behavior but concrete: list and dict comprehensions, slicing semantics, mutable default arguments, reference vs copy, `is` vs `==`, string methods, sorting, exception handling, and the classic pitfalls like `[1, 2, 3] * 2` producing `[1, 2, 3, 1, 2, 3]` instead of `[2, 4, 6]`. Every record runs exactly 3 think blocks (~168 words on average), and the final answer states the result *and* the reasoning in a sentence or two (~35 words). In the 3×3×3 grid this tier carries the core teaching load: semantics traps that survive a casual gut check but fall to one traced execution or type check.

## Files

| Mode | Records | File |
|------|:--:|------|
| Wrong → catch → fix | 100 | [wrong_then_fix.jsonl](wrong_then_fix.jsonl) |
| Right → scrutinize → verify | 100 | [right_and_confirm.jsonl](right_and_confirm.jsonl) |
| Right → doubt → reaffirm | 100 | [right_doubt_reaffirm.jsonl](right_doubt_reaffirm.jsonl) |

## What "medium" code looks like

Exactly three blocks — evaluate, then catch (or scrutinize, or doubt), then verify by a different route. The errors are conceptual, not slips: assuming `def foo(x=[])` builds a fresh list per call; treating `y = x` as a copy of a mutable list; expecting every element to be removed while the list shifts under the loop; reading `if x = 5:` as a comparison; assuming `list.sort()` returns the sorted list; believing `range()` materializes a list in Python 3; thinking `isinstance(True, int)` is False because `type(True)` is `bool`. The doubts are tempting in the same way — "sorted() returns a new list, so .sort() must too," "copy.copy() surely deep-copies," "Java's == is identity, maybe Python's is as well" — and block 3 explains both why they felt plausible and why Python's actual semantics say no. Verification is independent by construction: hand-tracing with shifted indices, probing with `type(...)` or `is`, rewriting the comprehension as an explicit for-loop — never the same evaluation twice.

A sample record — the mutate-while-iterating trap, caught and repaired by an index-accurate trace:

```json
{"messages": [{"role": "user", "content": "What does this Python code output?\n\nnums = [1, 2, 3, 4, 5]\nfor n in nums:\n    nums.remove(n)\nprint(nums)"}, {"role": "assistant", "content": "<think>\nThe loop iterates over nums and removes each element. Starting with [1, 2, 3, 4, 5], it removes 1, then 2, then 3, then 4, then 5. After removing all elements, nums is empty. So print(nums) outputs [].\n\nThis seems straightforward - iterate through all elements and remove each one, leaving an empty list.\n</think>\n\n\n<think>\nWait, that's wrong. I'm falling for a classic iteration-during-modification bug. When you remove elements from a list while iterating over it, the iteration index doesn't account for the removal, so elements get skipped. Let me trace through carefully.\n\nPython's for loop over a list internally uses an index. Let me trace step by step:\n- Iteration 1: index 0, n = nums[0] = 1. nums.remove(1) removes the value 1. nums is now [2, 3, 4, 5]. The internal index advances to 1.\n- Iteration 2: index 1, n = nums[1] = 3 (not 2!). After removing 1, the list shifted left. nums[1] is now 3. nums.remove(3). nums is now [2, 4, 5]. Index advances to 2.\n- Iteration 3: index 2, n = nums[2] = 5. nums.remove(5). nums is now [2, 4]. Index advances to 3.\n- Iteration 4: index 3, but len(nums) is now 2. The loop ends.\n\nSo the loop only ran 3 times and removed 1, 3, and 5. The remaining list is [2, 4]. My initial answer of [] was completely wrong.\n</think>\n\n\n<think>\nLet me verify this trace once more. The key insight: when you call nums.remove(n), all elements after the removed one shift left by one position. But the for loop's internal counter still advances by 1. So the element that moved into the position we just processed gets skipped.\n\nDetailed trace:\nnums = [1, 2, 3, 4, 5], internal index = 0\nStep 1: n = nums[0] = 1. remove(1) -> nums = [2, 3, 4, 5]. Index -> 1.\nStep 2: n = nums[1] = 3 (2 was skipped!). remove(3) -> nums = [2, 4, 5]. Index -> 2.\nStep 3: n = nums[2] = 5 (4 was skipped!). remove(5) -> nums = [2, 4]. Index -> 3.\nStep 4: index 3 >= len(nums) = 2. Loop stops.\n\nFinal nums = [2, 4]. The elements at even positions (1, 3, 5) were removed, while elements at odd positions (2, 4) were skipped because they shifted into positions the iterator had already passed. print(nums) outputs [2, 4].\n</think>\n\nThe output is **[2, 4]**. Removing elements during iteration causes the list to shift left, but the loop's internal index still advances forward, so every other element gets skipped. Tracing: remove 1 (list becomes [2,3,4,5], index moves to 1), remove 3 (list becomes [2,4,5], index moves to 2), remove 5 (list becomes [2,4], index moves to 3 which exceeds length). The remaining elements are 2 and 4. To safely remove all elements, use `nums.clear()` or iterate over a copy: `for n in nums[:]:`."}]}
```

## The tiers on either side

Medium sits between a value-check and a protocol audit. [Code / Easy](../easy/README.md) errors are careless and get caught in a single block; [Code / Hard](../hard/README.md) answers need 4–5 blocks because verification means re-deriving an MRO or hand-tracing a descriptor's precedence against the instance `__dict__`. All three modes run at all three tiers — being wrong is not a property of the question's difficulty.

---

[🏠 Home](../../README.md) · [Code](../README.md) · [Easy](../easy/README.md) · ← Medium · [Hard](../hard/README.md)
