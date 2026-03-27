---
name: uncertainty-calibration
description: Confidence calibration and abstention strategy for safer autonomous decisions.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Uncertainty Calibration

> High intelligence requires honest uncertainty.

## Calibration Policy
- Use confidence bands: low (<0.55), medium (0.55-0.8), high (>0.8).
- Low confidence => ask clarifying questions.
- High-risk + low confidence => abstain or escalate.
- Track confidence vs actual outcomes to recalibrate thresholds.

## Decision Protocol
1. Estimate confidence.
2. Estimate risk.
3. Pick action: execute / clarify / escalate.
4. Record outcome for calibration drift checks.

## Anti-Patterns
- Acting with false certainty.
- Ignoring contradiction signals.
- Using same threshold for all domains.
