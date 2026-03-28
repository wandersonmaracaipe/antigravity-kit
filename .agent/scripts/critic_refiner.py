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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate remediation plan from quality result")
    parser.add_argument("--quality-result", required=True)
    args = parser.parse_args()

    result = json.loads(Path(args.quality_result).read_text(encoding="utf-8"))

    # Accept either raw quality_gate output or benchmark report.
    failed = result.get("failed", [])
    if not failed and "tasks" in result:
        # infer recurring failure dimensions from benchmark tasks where quality gate failed
        recurring = []
        for t in result.get("tasks", []):
            if not t.get("quality_passed", True):
                recurring.append("performance")
        failed = sorted(set(recurring))

    ordered = [f for f in PRIORITY if f in failed]
    plan = [{"dimension": dim, "action": ACTION_MAP.get(dim, "Investigate and remediate.")} for dim in ordered]

    output = {
        "score": result.get("score"),
        "threshold": result.get("threshold"),
        "needs_refinement": bool(ordered),
        "actions": plan,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if not ordered else 1


if __name__ == "__main__":
    raise SystemExit(main())
