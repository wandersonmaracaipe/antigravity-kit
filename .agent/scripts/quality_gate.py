#!/usr/bin/env python3
"""
Quality Gate
------------
Computes a weighted quality score from check outcomes and enforces a threshold.

Input format (JSON):
{
  "security": true,
  "lint": true,
  "tests": false,
  "performance": true,
  "docs": true
}

Usage:
  python .agent/scripts/quality_gate.py --input .agent/quality/sample.json --threshold 85
  python .agent/scripts/quality_gate.py --input results.json --profile deploy --thresholds .agent/quality/thresholds.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

WEIGHTS = {
    "security": 30,
    "lint": 20,
    "tests": 20,
    "performance": 15,
    "docs": 10,
    "accessibility": 5,
}

PROFILE_REQUIRED_CHECKS = {
    "bugfix": ["security", "lint", "tests"],
    "feature": ["security", "lint", "tests"],
    "deploy": ["security", "lint", "tests", "performance", "accessibility"],
    "orchestrate": ["security", "lint", "tests", "performance"],
}


def compute_score(results: dict) -> tuple[int, list[str]]:
    score = 0
    failed = []
    for key, weight in WEIGHTS.items():
        ok = bool(results.get(key, False))
        if ok:
            score += weight
        else:
            failed.append(key)
    return score, failed


def resolve_threshold(args: argparse.Namespace) -> int:
    if args.profile and args.thresholds:
        thresholds = json.loads(Path(args.thresholds).read_text(encoding="utf-8"))
        if args.profile in thresholds:
            return int(thresholds[args.profile])
    return int(args.threshold)


def resolve_required_checks(args: argparse.Namespace) -> list[str]:
    if args.require:
        return [check.strip() for check in args.require.split(",") if check.strip()]
    if args.profile:
        return PROFILE_REQUIRED_CHECKS.get(args.profile, [])
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Quality gate scoring")
    parser.add_argument("--input", required=True, help="JSON file with check outcomes")
    parser.add_argument("--threshold", type=int, default=85)
    parser.add_argument("--profile", choices=["bugfix", "feature", "deploy", "orchestrate"], help="Threshold profile")
    parser.add_argument("--thresholds", help="JSON file with profile thresholds")
    parser.add_argument(
        "--require",
        help="Comma separated checks that must pass (example: security,tests). If omitted, defaults per profile are used.",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    score, failed = compute_score(data)
    threshold = resolve_threshold(args)
    required_checks = resolve_required_checks(args)
    required_failed = [check for check in required_checks if check in failed]

    passed = score >= threshold and not required_failed
    summary = {
        "score": score,
        "threshold": threshold,
        "profile": args.profile,
        "passed": passed,
        "failed": failed,
        "required_checks": required_checks,
        "required_failed": required_failed,
    }

    print(json.dumps(summary, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
