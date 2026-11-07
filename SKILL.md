---
name: seatpack-chrome-backup
description: Backs up Google Chrome profiles (history, cookies, extensions, logins) and editor plugins (Cursor, VS Code, Android Studio), then restores with merge-by-email so already-signed-in Chrome profiles are not replaced. Use when migrating laptops, backing up Chrome profiles, copying Cursor/VS Code/Android Studio plugins, or restoring those packs onto a new Mac.
---

<objective>
I copy Chrome profiles and editor plugins so the next Mac can pick them up. I list what exists first. You pick which buckets to include. On restore I merge Chrome by email / Gaia id. I do not overwrite an account that is already signed in.
</objective>

<essential_principles>
- **This is not `seatsweep-macos-cleanup`.** Cleanup wipes leftovers. This skill only copies and restores Chrome + plugins.
- **List, then wait.** Run `scripts/list.py` and show profile emails + plugin sizes before any rsync.
- **Quit the apps** (Chrome, Cursor, VS Code, Android Studio) before copy or restore.
- **Full Disk Access** is required to read Chrome. If `Local State` is unreadable, stop and say so.
- **Merge on restore, never replace by folder name.** `Default` on the new Mac is not the same person as `Default` in the backup.
- **LF-only shell.** macOS bash is 3.2. CRLF breaks `log() {`. Write restore scripts with `newline="\n"`.
- **ZIP64.** Do not use `ditto -c -k` for the archive. Exclude `OptGuideOnDeviceModel`.
- **`private/` is secret.** Chrome Safe Storage does not go to a public Drive.
</essential_principles>

<intake>
What do you want to do?

1. Inventory (default: list Chrome profiles and plugin packs)
2. Backup the buckets I already named
3. Pack an existing staging folder into a ZIP64 zip
4. Restore from a pack onto this Mac
</intake>

<routing>
| Choice | Start at |
|--------|----------|
| 1, "backup chrome", "backup plugin", "migrate chrome" | `<process>` step 1 |
| 2, named buckets this session | `<process>` step 3 |
| 3, "zip", "pack" | `<process>` step 5 |
| 4, "restore" | `<process>` step 6 |
</routing>

<quick_start>
Read [safety-notes.md](references/safety-notes.md). Then:

```
python3 scripts/list.py --home "$HOME" --output /tmp/chrome-plugin-inventory.json
```

Show the bucket table and Chrome emails. Wait for `--include` picks (`chrome`, `cursor`, `vscode`, `android-studio`). Then backup, then optional zip.
</quick_start>

<process>
**Step 1. Inventory.**
```
python3 scripts/list.py --home "$HOME" --output /tmp/chrome-plugin-inventory.json
```
Print each bucket: present / size / readable. For Chrome, list `folder`, email, display name. If Chrome is `TCC`, grant Full Disk Access to Terminal (and Cursor if this agent will copy) and rerun. Do not copy yet.

**Step 2. Confirm buckets.**
Ask which of `chrome`, `cursor`, `vscode`, `android-studio` to include. Default if they said "chrome and plugins" in this chat: all four that `list.py` marked present and readable.

**Step 3. Quit apps, then copy.**
Confirm Chrome / Cursor / VS Code / Android Studio are not running (`pgrep`). Staging default: `~/Desktop/chrome-plugin-backup-<YYYY-MM-DD>/`.

```
python3 scripts/backup.py --home "$HOME" --dest "$STAGE" \
  --include chrome --include cursor --include vscode --include android-studio
```
Only pass `--include` for picked buckets. `backup.py` writes `restore.sh`, `Restore.command`, `RESTORE.md`, and copies `merge_chrome_profiles.py` into the pack. Shell files must stay LF. Run `bash -n "$STAGE/restore.sh"`.

If `security find-generic-password -w` hangs on Keychain UI, kill it, skip Safe Storage, tell them Chrome Sync covers passwords.

**Step 4. Report staging.**
Give path, `du -sh` of each subfolder, Chrome profile count, and a reminder that `private/` stays off public Drive.

**Step 5. Zip (if they want a single file).**
```
python3 scripts/pack.py "$STAGE" --output "$STAGE.zip"
```
ZIP64, skip `OptGuideOnDeviceModel`. Do not use `ditto`. Copy the zip to Desktop or `/Users/Shared` if a later home wipe would delete Desktop.

**Step 6. Restore (new Mac or this Mac).**
Quit the apps. Prefer `Restore.command` inside the pack. If Chrome already has `Local State`, restore merges by Gaia id then email then name. Existing profiles stay. New emails land as `Profile N`. If Chrome was never opened, copy the full tree and optionally restore Safe Storage from `private/`.
</process>

<watch_for>
- TCC: Operation not permitted on Chrome until Full Disk Access.
- CRLF on `.sh` / `.command` → `syntax error near unexpected token '{^M'`.
- openrsync: `--exclude=pattern`, no `--info=stats2`.
- Zip32 / ditto: 4GB `weights.bin` in OptGuide corrupts the archive.
- Cursor plugins: exclude nested `.git`.
- Restore by `Default` folder name overwrites the wrong Google account.
- `security -w` can hang. Abort. Chrome Sync is the fallback.
</watch_for>

<reference_guides>
- [safety-notes.md](references/safety-notes.md)
- Scripts: `scripts/list.py`, `scripts/backup.py`, `scripts/pack.py`, `scripts/merge_chrome_profiles.py`
- Template: `templates/restore.sh.tmpl`
</reference_guides>

<success_criteria>
- Inventory printed before copy.
- Only picked buckets were copied.
- Restore script is LF, `bash -n` clean, merge-by-email documented in RESTORE.md.
- Zip (if requested) is ZIP64 and does not contain OptGuide weights.
- Chat names the staging path and warns about `private/`.
</success_criteria>
