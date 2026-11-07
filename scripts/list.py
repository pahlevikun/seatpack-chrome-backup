#!/usr/bin/env python3
"""Inventory Chrome profiles and editor plugins. No copy.

Usage:
    python3 list.py --home ~ --output /tmp/chrome-plugin-inventory.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

PROFILE_PREFIXES = ("Default",)


def human(n):
    n = float(n)
    for unit in ["B", "K", "M", "G", "T"]:
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}{unit}"
        n /= 1024
    return f"{n:.1f}P"


def du_bytes(path):
    try:
        out = subprocess.run(
            ["du", "-sk", str(path)], capture_output=True, text=True, check=True
        ).stdout
        return int(out.split()[0]) * 1024
    except Exception:
        return 0


def readable(path: Path) -> bool:
    try:
        if path.is_file():
            with path.open("rb") as f:
                f.read(8)
            return True
        os.listdir(path)
        return True
    except OSError:
        return False


def chrome_profiles(chrome: Path):
    profiles = []
    ls = chrome / "Local State"
    cache = {}
    if ls.is_file() and readable(ls):
        try:
            state = json.loads(ls.read_text(encoding="utf-8"))
            cache = (state.get("profile") or {}).get("info_cache") or {}
        except Exception:
            cache = {}
    names = []
    if (chrome / "Default").is_dir():
        names.append("Default")
    names += sorted(
        p.name for p in chrome.iterdir() if p.is_dir() and p.name.startswith("Profile ")
    )
    for folder in names:
        meta = cache.get(folder) or {}
        path = chrome / folder
        profiles.append(
            {
                "folder": folder,
                "email": meta.get("user_name") or "",
                "gaia_id": str(meta.get("gaia_id") or ""),
                "name": meta.get("name") or "",
                "size_bytes": du_bytes(path),
                "size_str": human(du_bytes(path)),
            }
        )
    return profiles, cache


def count_dirs(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for p in path.iterdir() if p.is_dir() and not p.name.startswith("."))


def editor_bucket(home: Path, key, label, paths):
    present = []
    total = 0
    readable_ok = True
    for rel, note in paths:
        p = home / rel if not str(rel).startswith("/") else Path(rel)
        if not p.exists():
            continue
        size = du_bytes(p)
        total += size
        if not readable(p):
            readable_ok = False
        n = count_dirs(p) if p.is_dir() else 0
        present.append(
            {
                "path": str(p),
                "note": note,
                "size_bytes": size,
                "size_str": human(size),
                "child_dirs": n,
            }
        )
    return {
        "id": key,
        "label": label,
        "present": bool(present),
        "readable": readable_ok,
        "size_bytes": total,
        "size_str": human(total),
        "paths": present,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default="~")
    ap.add_argument("--output", default="/tmp/chrome-plugin-inventory.json")
    args = ap.parse_args()
    home = Path(os.path.expanduser(args.home))
    chrome = home / "Library/Application Support/Google/Chrome"
    buckets = []

    chrome_readable = chrome.is_dir() and readable(chrome / "Local State" if (chrome / "Local State").exists() else chrome)
    profiles, _ = chrome_profiles(chrome) if chrome.is_dir() and chrome_readable else ([], {})
    chrome_size = du_bytes(chrome) if chrome.is_dir() else 0
    buckets.append(
        {
            "id": "chrome",
            "label": "Google Chrome profiles",
            "present": chrome.is_dir(),
            "readable": chrome_readable,
            "size_bytes": chrome_size,
            "size_str": human(chrome_size),
            "profile_count": len(profiles),
            "profiles": profiles,
            "note": None
            if chrome_readable
            else "Cannot read Chrome. Grant Full Disk Access to Terminal (and Cursor if the agent is copying).",
        }
    )
    buckets.append(
        editor_bucket(
            home,
            "cursor",
            "Cursor extensions + plugins + settings",
            [
                (".cursor/extensions", "extensions"),
                (".cursor/plugins", "plugins (exclude nested .git on copy)"),
                ("Library/Application Support/Cursor/User", "settings/keybindings/snippets"),
            ],
        )
    )
    buckets.append(
        editor_bucket(
            home,
            "vscode",
            "VS Code extensions + User settings",
            [
                (".vscode/extensions", "extensions"),
                ("Library/Application Support/Code/User", "settings"),
            ],
        )
    )
    as_paths = []
    as_root = home / "Library/Application Support/Google"
    if as_root.is_dir():
        for p in sorted(as_root.iterdir()):
            if p.is_dir() and p.name.startswith("AndroidStudio"):
                as_paths.append(
                    (str(p.relative_to(home)), p.name)
                )
    buckets.append(
        editor_bucket(home, "android-studio", "Android Studio config + plugins", as_paths)
    )

    data = {
        "home": str(home),
        "buckets": buckets,
        "total_bytes": sum(b["size_bytes"] for b in buckets if b.get("present")),
    }
    data["total_str"] = human(data["total_bytes"])
    Path(args.output).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"written {args.output}")
    print(f"total {data['total_str']}")
    for b in buckets:
        flag = "OK" if b.get("present") and b.get("readable", True) else ("TCC" if b.get("present") else "absent")
        extra = ""
        if b["id"] == "chrome" and b.get("profiles"):
            extra = f", {b['profile_count']} profiles"
        print(f"  [{flag}] {b['id']:16} {b['size_str']:>8}{extra}")


if __name__ == "__main__":
    main()
