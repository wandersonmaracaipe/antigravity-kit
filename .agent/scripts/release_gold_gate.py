#!/usr/bin/env python3
"""
Release Gold Gate
-----------------
Final gate that chains integrity + benchmark + quality checks to decide
if the system is ready for "gold" release.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.returncode, (result.stdout or result.stderr).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final gold release gate")
    parser.add_argument("--tasks", default=".agent/benchmarks/tasks.json")
    parser.add_argument("--quality-input", default=".agent/quality/sample.json")
    parser.add_argument("--thresholds", default=".agent/quality/thresholds.json")
    parser.add_argument("--profile", default="feature", choices=["bugfix", "feature", "deploy", "orchestrate"])
    parser.add_argument("--report", default=".agent/benchmarks/report.json")
    args = parser.parse_args()

    checks = []

    code, out = run(["python", ".agent/scripts/integrity_audit.py"])
    checks.append({"check": "integrity", "passed": code == 0, "output": out})

    code, out = run([
        "python", ".agent/scripts/benchmark_runner.py",
        "--tasks", args.tasks,
        "--quality-input", args.quality_input,
        "--thresholds", args.thresholds,
        "--out", args.report,
    ])
    checks.append({"check": "benchmark", "passed": code == 0, "output": out})

    code, out = run([
        "python", ".agent/scripts/quality_gate.py",
        "--input", args.quality_input,
        "--profile", args.profile,
        "--thresholds", args.thresholds,
    ])
    checks.append({"check": "quality_gate", "passed": code == 0, "output": out})

    summary = {
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
        "profile": args.profile,
    }

    Path(".agent/benchmarks").mkdir(parents=True, exist_ok=True)
    Path(".agent/benchmarks/gold-gate.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
