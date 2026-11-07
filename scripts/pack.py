#!/usr/bin/env python3
"""Zip a staging folder with ZIP64. Skip OptGuide on-device model weights.

ditto/zip32 dies on files over 4GB. Use this instead.

Usage:
    python3 pack.py /path/to/staging --output ~/Desktop/chrome-plugin-backup-YYYY-MM-DD.zip
"""
from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path

SKIP_DIR_NAMES = {"OptGuideOnDeviceModel", "__pycache__"}


def should_skip(rel: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in rel.parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    src = Path(os.path.expanduser(args.src)).resolve()
    out = Path(os.path.expanduser(args.output))
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    skipped = 0
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for root, dirs, files in os.walk(src):
            rel_root = Path(root).relative_to(src)
            dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
            for name in files:
                full = Path(root) / name
                rel = rel_root / name
                if should_skip(rel):
                    skipped += 1
                    continue
                zf.write(full, str(rel))
                count += 1
    print("wrote %s (%d files, skipped %d)" % (out, count, skipped))
    print("size %s" % (out.stat().st_size,))


if __name__ == "__main__":
    main()
