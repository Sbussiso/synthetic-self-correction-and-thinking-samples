# Self Correction and Thinking

A seed library for training language models to reason with self-correction. The dataset teaches three reasoning behaviors — catching your own errors, verifying correct answers, and rejecting false doubts — across three domains and three difficulty levels.

## Structure

The dataset is organized as a 3 × 3 × 3 grid:

```
├── code/           Programming problems (Python semantics, debugging, design patterns)
│   ├── easy/       1–2 think blocks
│   ├── medium/     3 think blocks
│   └── hard/       4–5 think blocks
├── general/        Non-math, non-code (science, logic, reading, grammar, causal reasoning, ethics)
│   ├── easy/
│   ├── medium/
│   └── hard/
└── math/           Mathematical reasoning (arithmetic, algebra, probability, number theory, geometry)
    ├── easy/
    ├── medium/
    └── hard/
```

Each difficulty/mode folder contains exactly one file per reasoning mode:

| File | Pattern |
|------|---------|
| `wrong_then_fix.jsonl` | First attempt is wrong → catch the error → fix and verify |
| `right_and_confirm.jsonl` | First attempt is correct → check for errors → independently verify |
| `right_doubt_reaffirm.jsonl` | First attempt is correct → second-guess with wrong answer → realize the doubt was the error |

## Stats

| Property | Value |
|----------|-------|
| Total files | 27 |
| Records per file | 20 |
| Total records | 540 |
| Think blocks (easy) | 1–2 |
| Think blocks (medium) | 3 |
| Think blocks (hard) | 4–5 |
| System prompts | ~30% of records per file |
| Format | JSONL (one JSON object per line) |

## Format

Each record is a chat-formatted JSON object with `messages` containing `user` and `assistant` roles (and optionally a `system` role):

```json
{
  "messages": [
    {"role": "user", "content": "What is 7 x 8?"},
    {"role": "assistant", "content": "<think>\nFirst instinct: 54 (confused with 6x9).\n</think>\n\n<think>\nWait — 7x8 is 56, not 54. Seven eights are fifty-six.\n</think>\n\n56. I confused it with 6x9=54 initially."}
  ]
}
```

The assistant content uses `<think>...</think>` tags to enclose reasoning blocks. Blocks are separated by `\n</think>\n\n<think>\n`. The final answer follows the last `</think>` tag.

Newlines inside content strings are JSON-escaped (`\n`). Think tags use literal `<` and `>` characters. Files use Unix line endings.

## Design principles

1. **Reasoning is intrinsic, not instruction-gated.** No system prompt tells the model to use think tags or to self-correct. The behavior is learned from examples, not from instructions. This ensures the model reasons by default, not only when told to.

2. **Thinking depth scales with difficulty.** Easy questions get 1–2 think blocks (a quick check is enough). Medium questions get 3 (attempt, catch/verify, confirm). Hard questions get 4–5 (multiple rounds of catching, fixing, and verifying). The model learns to match effort to problem complexity.

3. **All three modes exist at all difficulty levels.** The model learns that self-correction applies regardless of difficulty — you can make careless errors on easy questions, and you can be right on hard ones. No mode is confined to a single difficulty.

4. **Verification is independent.** When the model verifies an answer, it uses a genuinely different method — not just rechecking the same calculation. A math problem verified by formula is also checked by pairing, estimation, or substitution. A code problem verified by tracing is also checked by comparing with a Pythonic one-liner or testing edge cases.

5. **Final answers include reasoning.** Complex answers briefly explain the method, not just state the result. Trivial answers stay short. The explanation depth scales with difficulty.

## Combining files

To combine all files into a single dataset:

```bash
find . -name "*.jsonl" | sort | xargs cat > combined.jsonl
```

Order does not matter for training — all files are independent.

## Domains

### Code
Python semantics, debugging, design patterns, data structures, algorithms, async/await, decorators, descriptors, metaclasses, context managers, closures, generators, and more. Covers common pitfalls (mutable defaults, late-binding closures, shallow copies, iterator exhaustion) as well as conceptual understanding (GIL, MRO, reference counting, dynamic typing).

### General
Science misconceptions (seasons, sugar/hyperactivity, glass as liquid, Mpemba effect) and science explanations derived from first principles (Olbers' paradox, mirror left-right reversal, tidal locking, Earth's core composition, square-cube law), logic (syllogisms, fallacies, knights and knaves), reading comprehension (pronoun resolution, double negatives, passage inference), causal reasoning (correlation vs causation, confounders), grammar (affect/effect, between you and I, data as plural), ethics, fact-checking, and planning.

### Math
Arithmetic, percentages, probability, combinatorics, number theory (primes, modular arithmetic, irrationality proofs), algebra (quadratics, simultaneous equations, logarithms), geometry (areas, volumes, angles), sequences and series, compound interest, optimization, and Fermi estimation. Includes common math misconceptions (compound vs simple interest, percentage base asymmetry, without-replacement probability).