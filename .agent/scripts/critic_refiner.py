#!/usr/bin/env python3
"""
Critic Refiner
--------------
Reads a quality-gate result JSON and emits prioritized remediation actions.

Usage:
  python .agent/scripts/critic_refiner.py --quality-result .agent/benchmarks/quality.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTION_MAP = {
    "security": "Run security_scan.py and patch auth/input validation issues first.",
    "lint": "Run lint_runner.py and fix all blocking static issues.",
    "tests": "Increase unit/integration coverage for changed paths and failing flows.",
    "performance": "Run lighthouse/bundle analysis and optimize critical hot paths.",
    "docs": "Update README/ADR/change notes to reflect behavior changes.",
    "accessibility": "Run accessibility checker and fix contrast/keyboard/screen-reader issues.",
}

PRIORITY = ["security", "lint", "tests", "performance", "accessibility", "docs"]


def extract_failed_dimensions(result: dict) -> list[str]:
    # 1) direct quality gate payload
    failed = result.get("failed", [])
    if failed:
        return list(failed)

    # 2) benchmark report payload (aggregate real failed dimensions from each task)
    if "tasks" in result:
        aggregate: list[str] = []
        for task in result.get("tasks", []):
            if task.get("quality_passed", True):
                continue
            task_failed = task.get("quality_failed_checks") or []
            required_failed = task.get("quality_required_failed") or []
            if task_failed:
                aggregate.extend(task_failed)
            if required_failed:
                aggregate.extend(required_failed)

        if aggregate:
            counts = Counter(aggregate)
            ordered = []
            for dim in PRIORITY:
                if dim in counts:
                    ordered.extend([dim] * counts[dim])
            return ordered

    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate remediation plan from quality result")
    parser.add_argument("--quality-result", required=True)
    parser.add_argument("--max-actions", type=int, default=6, help="Limit number of remediation actions")
    args = parser.parse_args()

    result = json.loads(Path(args.quality_result).read_text(encoding="utf-8"))
    failed = extract_failed_dimensions(result)

    counts = Counter(failed)
    ordered_unique = [dim for dim in PRIORITY if dim in counts]
    ordered_unique = ordered_unique[: max(args.max_actions, 1)]
    plan = [
        {
            "dimension": dim,
            "occurrences": counts.get(dim, 0),
            "action": ACTION_MAP.get(dim, "Investigate and remediate."),
        }
        for dim in ordered_unique
    ]

    output = {
        "score": result.get("score"),
        "threshold": result.get("threshold"),
        "needs_refinement": bool(ordered_unique),
        "actions": plan,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if not ordered_unique else 1


if __name__ == "__main__":
    raise SystemExit(main())
