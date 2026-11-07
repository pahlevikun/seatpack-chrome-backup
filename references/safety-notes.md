# Safety notes (from a real Chrome + plugin migrate)

## Full Disk Access

Chrome under `~/Library/Application Support/Google/Chrome` is TCC-protected.
`listdir` / `cp` / Finder copy all fail with Operation not permitted until
Terminal (and the agent host, if it is doing the copy) has Full Disk Access.
Probe `Local State` with an 8-byte read before rsync. If it fails, stop and
ask the user to enable FDA. Do not claim the backup is complete.

## macOS bash 3.2 and CRLF

`/bin/bash` on macOS is 3.2. `log() {^M` from a CRLF script is a syntax error.
Always write `.sh` / `.command` / `.tmpl` with LF. Check with
`file script.sh` and `bash -n`. Do not rely on bash 4 associative arrays.

## openrsync flags

System rsync is openrsync. `--info=stats2` is invalid. `--exclude pattern`
is treated as extra source files. Use `--exclude=pattern`. `-E` is Apple
extended attributes; GNU rsync (Homebrew) wants `--xattrs`. Detect from
`--help`.

## ZIP64, not ditto, not zip32

`ditto -c -k` / classic zip die on files over 4GB. Chrome's
`OptGuideOnDeviceModel` `weights.bin` hit that. Exclude that folder at copy
and at zip time. Build the archive with Python `zipfile` and `allowZip64=True`.

## Restore merges by email, does not replace

On the new Mac, emails / Gaia ids already signed in stay. Missing emails
become a new `Profile N`. If Chrome has never been opened (no `Local State`),
copy the full backup. Do not overwrite `Default` by folder name.

## Chrome Safe Storage

Keychain item `Chrome Safe Storage` encrypts cookies/passwords. Export with
`security find-generic-password -s "Chrome Safe Storage" -w` into `private/`
mode 600. That command can hang on a Keychain UI prompt: abort it, skip
passwords, tell the user to use Chrome Sync. On restore, only write the
keychain item when this Mac had no Chrome data. If Chrome already exists,
leave Safe Storage alone so current passwords stay valid.

## Cursor plugins and nested .git

rsync of `~/.cursor/plugins` can fail on nested `.git` permission. Use
`--exclude=.git`.

## Running apps

Quit Chrome, Cursor, VS Code, Android Studio before backup and restore.
Copying a live profile can miss files or restore into a locked tree.

## Do not upload `private/`

Chrome Safe Storage is a secret. Keep it off public Drive. The staging
folder can live on Desktop or a USB.
