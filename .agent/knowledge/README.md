# Knowledge Base

Use this folder for long-term learning artifacts:

- `decisions/` → ADRs and architectural decisions
- `postmortems/` → incidents and lessons learned
- `patterns/` → successes and failures

CLI helper:

```bash
python .agent/scripts/knowledge_manager.py add --type adr --title "API versioning" --content "Use URL versioning for public APIs"
python .agent/scripts/knowledge_manager.py list --type adr
python .agent/scripts/knowledge_manager.py search --query "versioning"
```

## Templates

- `templates/adr-template.md`
- `templates/postmortem-template.md`

Use these as starting points for decision and incident records.

## Benchmark Loop

Use benchmark + critic loop to continuously improve:

```bash
python .agent/scripts/benchmark_runner.py \
  --tasks .agent/benchmarks/tasks.json \
  --quality-input .agent/quality/sample.json \
  --thresholds .agent/quality/thresholds.json \
  --out .agent/benchmarks/report.json

python .agent/scripts/critic_refiner.py --quality-result .agent/benchmarks/report.json
```

## Golden Release Gate

```bash
python .agent/scripts/release_gold_gate.py --profile feature
```

This command runs integrity + benchmark + quality gate in one shot.
