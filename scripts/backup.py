#!/usr/bin/env python3
"""Copy selected Chrome / editor plugin buckets into a staging folder.

Writes LF-only restore.sh into the pack. macOS bash 3.2 compatible.

Usage:
    python3 backup.py --home ~ --dest ~/Desktop/chrome-plugin-backup-YYYY-MM-DD \
        --include chrome --include cursor --include vscode --include android-studio
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

CHROME_EXCLUDES = [
    ".DS_Store",
    "Crashpad/",
    "BrowserMetrics*",
    "GraphiteDawnCache/",
    "GrShaderCache/",
    "ShaderCache/",
    "GPUCache/",
    "Cache/",
    "Code Cache/",
    "component_crx_cache/",
    "optimization_guide_hint_cache_store/",
    "optimization_guide_model_store/",
    "optimization_guide_prediction_model_downloads/",
    "OptGuideOnDeviceModel/",
    "ScreenAI/",
    "PnaclTranslationCache/",
    "FileTypePolicies/",
    "Safe Browsing/",
    "Safe Browsing Network/",
    "Crowd Deny/",
    "MEIPreload/",
    "PKIMetadata/",
    "OnDeviceHeadSuggestModel/",
    "WasmTtsEngine/",
    "AmountExtractionHeuristicRegexes/",
    "CertificateRevocation/",
    "SSLErrorAssistant/",
    "Subresource Filter/",
    "ZxcvbnData/",
    "hyphen-data/",
    "Default/Service Worker/CacheStorage/",
    "Profile */Service Worker/CacheStorage/",
    "Guest Profile/Service Worker/CacheStorage/",
    "Default/Service Worker/ScriptCache/",
    "Profile */Service Worker/ScriptCache/",
    "Guest Profile/Service Worker/ScriptCache/",
]


def log(msg):
    print(msg, flush=True)


def rsync_bin():
    if Path("/opt/homebrew/bin/rsync").is_file():
        return "/opt/homebrew/bin/rsync"
    return "/usr/bin/rsync"


def rsync_flags(rsync):
    help_text = subprocess.run([rsync, "--help"], capture_output=True, text=True).stdout
    flags = ["-a"]
    if "--xattrs" in help_text:
        flags.append("--xattrs")
    elif "-E, --extended-attributes" in help_text:
        flags.append("-E")
    return flags


def run_rsync(src, dest, extra_excludes=None):
    rsync = rsync_bin()
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [rsync] + rsync_flags(rsync)
    for ex in extra_excludes or []:
        cmd.append("--exclude=" + ex)
    cmd += ["--", str(src).rstrip("/") + "/", str(dest).rstrip("/") + "/"]
    log("    rsync %s -> %s" % (src, dest))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        log("    rsync exited %s (copy may still be usable)" % r.returncode)
    return r.returncode


def write_lf(path: Path, text: str):
    path.write_text(text, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def copy_chrome(home: Path, dest: Path):
    src = home / "Library/Application Support/Google/Chrome"
    out = dest / "chrome/Google-Chrome"
    if not src.is_dir():
        log("skip chrome: not found")
        return False
    try:
        with (src / "Local State").open("rb") as f:
            f.read(8)
    except OSError:
        log("Cannot read Chrome. Grant Full Disk Access to Terminal, then rerun.")
        return False
    run_rsync(src, out, CHROME_EXCLUDES)
    lists = dest / "lists"
    lists.mkdir(exist_ok=True)
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name("list.py")), "--home", str(home), "--output", str(lists / "inventory.json")],
        check=False,
    )
    priv = dest / "private"
    priv.mkdir(exist_ok=True)
    secret = priv / "chrome-safe-storage.txt"
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "Chrome Safe Storage", "-w"],
        capture_output=True,
        text=True,
    )
    if r.returncode == 0 and r.stdout.strip():
        secret.write_text(r.stdout.strip() + "\n", encoding="utf-8")
        secret.chmod(0o600)
        log("    saved Chrome Safe Storage to private/ (do not upload this folder)")
    else:
        log("    Chrome Safe Storage not exported. Use Chrome Sync for passwords on restore.")
    return True


def copy_cursor(home: Path, dest: Path):
    root = dest / "cursor"
    root.mkdir(parents=True, exist_ok=True)
    pairs = [
        (home / ".cursor/extensions", root / "extensions", [".git"]),
        (home / ".cursor/plugins", root / "plugins", [".git"]),
        (home / "Library/Application Support/Cursor/User", root / "User", []),
    ]
    any_ok = False
    for src, out, ex in pairs:
        if src.exists():
            run_rsync(src, out, ex)
            any_ok = True
    return any_ok


def copy_vscode(home: Path, dest: Path):
    root = dest / "vscode"
    root.mkdir(parents=True, exist_ok=True)
    pairs = [
        (home / ".vscode/extensions", root / "extensions", []),
        (home / "Library/Application Support/Code/User", root / "User", []),
    ]
    any_ok = False
    for src, out, ex in pairs:
        if src.exists():
            run_rsync(src, out, ex)
            any_ok = True
    return any_ok


def copy_android_studio(home: Path, dest: Path):
    google = home / "Library/Application Support/Google"
    out_root = dest / "android-studio"
    out_root.mkdir(parents=True, exist_ok=True)
    any_ok = False
    if not google.is_dir():
        return False
    for p in sorted(google.iterdir()):
        if p.is_dir() and p.name.startswith("AndroidStudio"):
            run_rsync(p, out_root / p.name, [])
            any_ok = True
    return any_ok


def emit_restore(dest: Path, included):
    skill_dir = Path(__file__).resolve().parent
    shutil.copy2(skill_dir / "merge_chrome_profiles.py", dest / "scripts" / "merge_chrome_profiles.py")
    tmpl = (skill_dir.parent / "templates" / "restore.sh.tmpl").read_text(encoding="utf-8")
    write_lf(dest / "restore.sh", tmpl)
    write_lf(
        dest / "Restore.command",
        "#!/bin/bash\ncd \"$(dirname \"$0\")\"\nexec /bin/bash ./restore.sh\n",
    )
    packs = ", ".join(included)
    readme = """# Restore

1. Copy this folder (or the zip) to the new Mac.
2. Double-click Restore.command. If macOS blocks it: System Settings → Privacy & Security → Open Anyway.
3. Quit Chrome / Cursor / VS Code / Android Studio first.

Included: %s

## Chrome

Restore does not replace accounts already signed in on the new Mac.
Emails / Gaia ids that already exist are skipped. Missing emails are copied as new Profile N folders.
If Chrome was never opened on the new Mac, the full backup is copied.

`private/` holds Chrome Safe Storage if export succeeded. Do not upload `private/` to a public Drive.

## Editors

Cursor / VS Code: extensions + User settings.
Android Studio: Application Support folders named AndroidStudio*.
""" % packs
    write_lf(dest / "RESTORE.md", readme)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default="~")
    ap.add_argument("--dest")
    ap.add_argument("--include", action="append", default=[], choices=["chrome", "cursor", "vscode", "android-studio"])
    args = ap.parse_args()
    home = Path(os.path.expanduser(args.home))
    included = args.include or ["chrome", "cursor", "vscode", "android-studio"]
    dest = Path(os.path.expanduser(args.dest or str(home / "Desktop" / ("chrome-plugin-backup-" + date.today().isoformat()))))
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "scripts").mkdir(exist_ok=True)
    log("staging %s" % dest)
    log("include %s" % ", ".join(included))
    copied = []
    mapping = {
        "chrome": copy_chrome,
        "cursor": copy_cursor,
        "vscode": copy_vscode,
        "android-studio": copy_android_studio,
    }
    for key in included:
        log("==> %s" % key)
        if mapping[key](home, dest):
            copied.append(key)
        else:
            log("    skipped")
    emit_restore(dest, copied)
    manifest = {"included": copied, "dest": str(dest)}
    (dest / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log("done. copied: %s" % ", ".join(copied) or "(none)")
    print(str(dest))


if __name__ == "__main__":
    main()
