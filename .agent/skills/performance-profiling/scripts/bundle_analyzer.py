#!/usr/bin/env python3
"""
Bundle Analyzer
---------------
Performs a lightweight static bundle check by scanning common build output folders.
Fails if any JS asset exceeds the configured threshold.
"""

from __future__ import annotations

import sys
from pathlib import Path

MAX_FILE_MB = 1.5
SEARCH_DIRS = [".next/static", "dist", "build"]


def iter_js_files(base: Path):
    for rel in SEARCH_DIRS:
        root = base / rel
        if root.exists():
            yield from root.rglob("*.js")


def main() -> int:
    project = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    files = list(iter_js_files(project))

    if not files:
        print("⚠️ No built JS assets found (.next/static, dist, build). Skipping bundle analysis")
        return 0

    oversized = []
    for f in files:
        size_mb = f.stat().st_size / (1024 * 1024)
        if size_mb > MAX_FILE_MB:
            oversized.append((f, size_mb))

    if oversized:
        print("❌ Oversized JS bundles detected:")
        for f, mb in sorted(oversized, key=lambda x: x[1], reverse=True)[:20]:
            print(f"  - {f.relative_to(project)}: {mb:.2f} MB")
        return 1

    print(f"✅ Bundle analysis passed ({len(files)} JS files scanned, threshold={MAX_FILE_MB}MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
