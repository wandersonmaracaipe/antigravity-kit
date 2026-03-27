---
name: context-engineering
description: Advanced context design patterns for AI tasks. Focuses on context pruning, relevance ranking, retrieval boundaries, and anti-bloat strategies.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Context Engineering

> Better context beats bigger context.

## Core Rules
- Load only what changes the decision.
- Rank sources by recency, reliability, and task relevance.
- Separate immutable constraints from volatile runtime signals.
- Prefer compact state summaries over raw transcript dumps.

## Retrieval Strategy
1. Gather candidate context.
2. Score by relevance and risk impact.
3. Keep top-k evidence.
4. Produce concise decision context package.

## Anti-Patterns
- Dumping full logs into every prompt.
- Mixing outdated and fresh constraints.
- Forgetting to preserve original user intent.
