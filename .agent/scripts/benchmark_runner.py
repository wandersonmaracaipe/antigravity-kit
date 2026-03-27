#!/usr/bin/env python3
"""
Benchmark Runner
----------------
Runs repeatable routing/quality benchmark tasks and generates aggregate metrics.

Usage:
  python .agent/scripts/benchmark_runner.py \
    --tasks .agent/benchmarks/tasks.json \
    --quality-input .agent/quality/sample.json \
    --thresholds .agent/quality/thresholds.json \
    --out .agent/benchmarks/report.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run_routing(prompt: str) -> dict:
    cmd = ["python", ".agent/scripts/routing_score.py", prompt]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"error": result.stderr or result.stdout}
    return json.loads(result.stdout)


def run_quality(profile: str, quality_input: str, thresholds: str) -> dict:
    cmd = [
        "python",
        ".agent/scripts/quality_gate.py",
        "--input",
        quality_input,
        "--profile",
        profile,
        "--thresholds",
        thresholds,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    payload = {}
    try:
        payload = json.loads(result.stdout)
    except Exception:
        payload = {"raw": result.stdout.strip()}
    payload["passed"] = result.returncode == 0
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run benchmark scenarios")
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--quality-input", required=True)
    parser.add_argument("--thresholds", required=True)
    parser.add_argument("--out", default=".agent/benchmarks/report.json")
    args = parser.parse_args()

    tasks = json.loads(Path(args.tasks).read_text(encoding="utf-8"))
    rows = []

    for task in tasks:
        routing = run_routing(task["prompt"])
        quality = run_quality(task.get("profile", "feature"), args.quality_input, args.thresholds)

        selected = set(routing.get("selected_agents", []))
        expected = set(task.get("expected_agents", []))
        routing_match = bool(selected.intersection(expected)) if expected else True

        rows.append(
            {
                "id": task["id"],
                "prompt": task["prompt"],
                "selected_agents": routing.get("selected_agents", []),
                "confidence": routing.get("confidence", 0),
                "needs_clarification": routing.get("needs_clarification", True),
                "suggested_workflow": routing.get("suggested_workflow", "direct-answer"),
                "routing_match": routing_match,
                "quality_profile": task.get("profile", "feature"),
                "quality_passed": quality.get("passed", False),
                "quality_score": quality.get("score"),
                "quality_threshold": quality.get("threshold"),
            }
        )

    total = len(rows) or 1
    routing_accuracy = round(sum(1 for r in rows if r["routing_match"]) / total, 2)
    quality_pass_rate = round(sum(1 for r in rows if r["quality_passed"]) / total, 2)
    avg_confidence = round(sum(float(r.get("confidence", 0)) for r in rows) / total, 2)

    report = {
        "summary": {
            "total_tasks": len(rows),
            "routing_accuracy": routing_accuracy,
            "quality_pass_rate": quality_pass_rate,
            "avg_confidence": avg_confidence,
        },
        "tasks": rows,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))
    print(f"report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
