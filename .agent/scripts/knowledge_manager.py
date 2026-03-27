#!/usr/bin/env python3
"""
Knowledge Manager
-----------------
Simple knowledge base manager for .agent/knowledge.

Commands:
  add --type adr|postmortem|success|failure --title "..." --content "..."
  list --type <type>
  search --query "..."
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / ".agent" / "knowledge"
MAP = {
    "adr": BASE / "decisions",
    "postmortem": BASE / "postmortems",
    "success": BASE / "patterns",
    "failure": BASE / "patterns",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text[:80] or "entry"


def ensure_dirs() -> None:
    for p in {BASE, *MAP.values()}:
        p.mkdir(parents=True, exist_ok=True)


def cmd_add(args: argparse.Namespace) -> int:
    ensure_dirs()
    folder = MAP[args.type]
    ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    name = f"{ts}-{slugify(args.title)}.md"
    path = folder / name

    prefix = "SUCCESS" if args.type == "success" else "FAILURE" if args.type == "failure" else args.type.upper()
    body = f"# {prefix}: {args.title}\n\nDate: {dt.datetime.utcnow().isoformat()}Z\n\n{args.content}\n"
    path.write_text(body, encoding="utf-8")
    print(path.relative_to(ROOT))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    ensure_dirs()
    folder = MAP[args.type]
    for f in sorted(folder.glob("*.md")):
        print(f.relative_to(ROOT))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    ensure_dirs()
    q = args.query.lower()
    found = False
    for f in sorted(BASE.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore").lower()
        if q in text:
            print(f.relative_to(ROOT))
            found = True
    return 0 if found else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Manage .agent knowledge base")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--type", choices=["adr", "postmortem", "success", "failure"], required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--content", required=True)
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list")
    l.add_argument("--type", choices=["adr", "postmortem", "success", "failure"], required=True)
    l.set_defaults(func=cmd_list)

    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.set_defaults(func=cmd_search)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
