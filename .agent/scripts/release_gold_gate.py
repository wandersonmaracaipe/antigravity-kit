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


def _trim(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}... [truncated {len(text) - max_chars} chars]"


def run(cmd: list[str], max_output_chars: int) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    raw = (result.stdout or result.stderr).strip()
    return result.returncode, _trim(raw, max_output_chars)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final gold release gate")
    parser.add_argument("--tasks", default=".agent/benchmarks/tasks.json")
    parser.add_argument("--quality-input", default=".agent/quality/sample.json")
    parser.add_argument("--thresholds", default=".agent/quality/thresholds.json")
    parser.add_argument("--profile", default="feature", choices=["bugfix", "feature", "deploy", "orchestrate"])
    parser.add_argument("--report", default=".agent/benchmarks/report.json")
    parser.add_argument("--max-output-chars", type=int, default=500, help="Trim nested check outputs to reduce token usage")
    args = parser.parse_args()

    checks = []

    code, out = run(["python", ".agent/scripts/integrity_audit.py"], args.max_output_chars)
    checks.append({"check": "integrity", "passed": code == 0, "output": out})

    code, out = run([
        "python", ".agent/scripts/benchmark_runner.py",
        "--tasks", args.tasks,
        "--quality-input", args.quality_input,
        "--thresholds", args.thresholds,
        "--out", args.report,
    ], args.max_output_chars)
    checks.append({"check": "benchmark", "passed": code == 0, "output": out})

    code, out = run([
        "python", ".agent/scripts/quality_gate.py",
        "--input", args.quality_input,
        "--profile", args.profile,
        "--thresholds", args.thresholds,
    ], args.max_output_chars)
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
