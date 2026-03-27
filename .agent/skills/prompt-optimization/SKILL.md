---
name: prompt-optimization
description: Systematic prompt refinement for reliability, latency, and output quality.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Prompt Optimization

> Optimize prompts like production systems: hypotheses, tests, and regression checks.

## Optimization Loop
1. Define failure modes.
2. Create prompt variants.
3. Evaluate on fixed benchmark.
4. Adopt only variants with measurable improvement.

## Heuristics
- Explicit success criteria.
- Structured output schema.
- Constraint-first instructions.
- Minimal but sufficient examples.

## Anti-Patterns
- Constant ad-hoc prompt edits without benchmark evidence.
- Overfitting to a single demo case.
