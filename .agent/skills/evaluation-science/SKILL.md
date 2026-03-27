---
name: evaluation-science
description: Benchmark design, metric quality, and experiment methodology for agent systems.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Evaluation Science

> What you cannot measure, you cannot improve.

## Benchmark Design
- Use representative tasks across domains and difficulty.
- Separate dev benchmark and holdout benchmark.
- Prevent leakage from training/edit loops.

## Metrics
- Routing accuracy
- Quality pass rate
- Cost/time per task
- Rework rate
- Failure severity

## Experiment Rules
- Change one variable at a time.
- Keep baseline snapshots.
- Require statistically meaningful deltas before rollout.
