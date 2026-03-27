#!/usr/bin/env python3
"""
Integrity Audit - Antigravity Kit
=================================
Validates integrity of .agent configuration:
- Agent skills map to existing skill folders/files
- Master scripts reference existing skill scripts
- mcp_config.json is valid JSON
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = ROOT / ".agent"


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_skills_from_agent(agent_file: Path) -> list[str]:
    text = _load_text(agent_file)
    match = re.search(r"^skills:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        return []
    return [s.strip() for s in match.group(1).split(",") if s.strip()]


def _skill_exists(skill_ref: str) -> bool:
    """
    Supports both top-level skill names and nested paths like:
    - game-development
    - game-development/web-games
    """
    candidate = AGENT_DIR / "skills" / skill_ref
    if candidate.is_dir():
        return (candidate / "SKILL.md").exists() or any(candidate.glob("*.md"))

    top_level = AGENT_DIR / "skills" / skill_ref
    return top_level.is_dir()


def _extract_script_paths(files: Iterable[Path]) -> set[str]:
    pattern = re.compile(r"\.agent/skills/[\w\-/]+/scripts/[\w\-]+\.py")
    refs: set[str] = set()
    for f in files:
        refs.update(pattern.findall(_load_text(f)))
    return refs


def audit_agent_skill_refs() -> list[str]:
    errors: list[str] = []
    for agent in sorted((AGENT_DIR / "agents").glob("*.md")):
        for skill in _extract_skills_from_agent(agent):
            if not _skill_exists(skill):
                errors.append(f"{agent.relative_to(ROOT)} -> missing skill: {skill}")
    return errors


def audit_script_refs() -> list[str]:
    files = [AGENT_DIR / "scripts" / "checklist.py", AGENT_DIR / "scripts" / "verify_all.py"]
    refs = _extract_script_paths(files)
    errors: list[str] = []
    for ref in sorted(refs):
        if not (ROOT / ref).exists():
            errors.append(f"Missing script reference: {ref}")
    return errors


def audit_mcp_json() -> list[str]:
    p = AGENT_DIR / "mcp_config.json"
    if not p.exists():
        return [".agent/mcp_config.json not found"]
    try:
        json.loads(_load_text(p))
        return []
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in .agent/mcp_config.json: {exc}"]




def audit_knowledge_assets() -> list[str]:
    required = [
        AGENT_DIR / "knowledge" / "README.md",
        AGENT_DIR / "knowledge" / "templates" / "adr-template.md",
        AGENT_DIR / "knowledge" / "templates" / "postmortem-template.md",
        AGENT_DIR / "quality" / "sample.json",
        AGENT_DIR / "quality" / "thresholds.json",
    ]
    errors: list[str] = []
    for p in required:
        if not p.exists():
            errors.append(f"Missing knowledge/quality asset: {p.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(audit_agent_skill_refs())
    errors.extend(audit_script_refs())
    errors.extend(audit_mcp_json())
    errors.extend(audit_knowledge_assets())

    if errors:
        print("❌ Integrity audit failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("✅ Integrity audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
