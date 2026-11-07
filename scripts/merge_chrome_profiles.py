#!/usr/bin/env python3
"""Merge backup Chrome profiles into an existing Chrome user-data dir.

Match by Gaia id, then email, then profile display name.
Existing destination profiles are left untouched.
Missing backup profiles are copied into a new Profile N folder.
"""
from __future__ import print_function

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROFILE_DIR_RE = re.compile(r"^(Default|Profile \d+)$")


def log(msg):
    print(msg, flush=True)


def load_local_state(path):
    return json.loads(path.read_text(encoding="utf-8"))


def info_cache(state):
    return ((state.get("profile") or {}).get("info_cache") or {})


def identity_keys(meta):
    if not isinstance(meta, dict):
        return []
    keys = []
    gaia = meta.get("gaia_id")
    if gaia:
        keys.append("gaia:" + str(gaia))
    email = (meta.get("user_name") or "").strip().lower()
    if email and "@" in email:
        keys.append("email:" + email)
    name = (meta.get("name") or "").strip().lower()
    if name:
        keys.append("name:" + name)
    return keys


def dest_identities(state):
    found = set()
    for meta in info_cache(state).values():
        found.update(identity_keys(meta))
    return found


def next_profile_dir(dest_root):
    nums = [1]
    for p in dest_root.iterdir():
        m = re.fullmatch(r"Profile (\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return "Profile %d" % (max(nums) + 1)


def copy_profile(src, dest):
    dest.mkdir(parents=True, exist_ok=True)
    cmd = ["/usr/bin/rsync", "-aE", "--", str(src) + "/", str(dest) + "/"]
    subprocess.check_call(cmd)


def main(src_root, dest_root):
    src_root = Path(src_root)
    dest_root = Path(dest_root)
    src_ls = src_root / "Local State"
    dest_ls = dest_root / "Local State"
    if not src_ls.is_file() or not dest_ls.is_file():
        log("Local State missing; cannot merge Chrome profiles")
        return 1

    backup = load_local_state(src_ls)
    dest = load_local_state(dest_ls)
    existing = dest_identities(dest)
    dest.setdefault("profile", {})
    dest["profile"].setdefault("info_cache", {})
    dest["profile"].setdefault("profiles_order", [])

    bak = dest_ls.with_name("Local State.restore-bak")
    if not bak.exists():
        shutil.copy2(dest_ls, bak)
        log("    kept existing Local State backup at %s" % bak.name)

    added = 0
    skipped = 0
    for folder, meta in sorted(info_cache(backup).items()):
        if not PROFILE_DIR_RE.match(folder):
            continue
        src_dir = src_root / folder
        if not src_dir.is_dir():
            log("    skip %s (folder missing in backup)" % folder)
            skipped += 1
            continue
        keys = identity_keys(meta)
        hit = next((k for k in keys if k in existing), None)
        label = meta.get("user_name") or meta.get("name") or folder
        if hit:
            log("    skip %s (%s already on this Mac, keep current profile)" % (folder, label))
            skipped += 1
            continue
        new_dir = next_profile_dir(dest_root)
        while (dest_root / new_dir).exists() or new_dir in dest["profile"]["info_cache"]:
            n = int(new_dir.split()[1]) + 1
            new_dir = "Profile %d" % n
        log("    add  %s -> %s (%s)" % (folder, new_dir, label))
        copy_profile(src_dir, dest_root / new_dir)
        dest["profile"]["info_cache"][new_dir] = meta
        if new_dir not in dest["profile"]["profiles_order"]:
            dest["profile"]["profiles_order"].append(new_dir)
        for k in keys:
            existing.add(k)
        added += 1

    tmp = dest_ls.with_name("Local State.restore-tmp")
    tmp.write_text(json.dumps(dest, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    os.replace(str(tmp), str(dest_ls))
    log("    Chrome merge done: added %d, skipped %d" % (added, skipped))
    log("    existing accounts were not replaced. Open Chrome and pick the extra profiles.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("usage: merge_chrome_profiles.py SRC_CHROME DEST_CHROME\n")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
