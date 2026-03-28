#!/usr/bin/env python3
"""
Laravel Map
-----------
Fast, deterministic Laravel structure discovery to avoid ad-hoc shell/regex loops.

Usage:
  python .agent/scripts/laravel_map.py --root .
  python .agent/scripts/laravel_map.py --root . --controller UserController
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def is_laravel_root(root: Path) -> bool:
    return (root / "artisan").exists() and (root / "routes").is_dir() and (root / "app").is_dir()


def list_controllers(root: Path) -> list[str]:
    controller_dir = root / "app" / "Http" / "Controllers"
    if not controller_dir.is_dir():
        return []
    return sorted(
        str(path.relative_to(root))
        for path in controller_dir.rglob("*Controller.php")
        if path.is_file()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover Laravel structure and controllers")
    parser.add_argument("--root", default=".", help="Laravel project root")
    parser.add_argument("--controller", help="Controller name filter (contains match), ex: UserController")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    detected = is_laravel_root(root)

    controllers = list_controllers(root) if detected else []
    if args.controller and controllers:
        term = args.controller.lower()
        controllers = [item for item in controllers if term in item.lower()]

    payload = {
        "root": str(root),
        "laravel_detected": detected,
        "key_paths": {
            "artisan": str(root / "artisan"),
            "routes_web": str(root / "routes" / "web.php"),
            "routes_api": str(root / "routes" / "api.php"),
            "controllers_dir": str(root / "app" / "Http" / "Controllers"),
            "models_dir": str(root / "app" / "Models"),
        },
        "controller_count": len(controllers),
        "controllers": controllers,
        "next_step": (
            "Use artisan + direct file reads. Avoid ad-hoc PowerShell regex discovery loops."
            if detected
            else "Laravel structure not detected from this root. Confirm project path before deeper investigation."
        ),
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
