Skill name:        seatpack-chrome-backup
Goal:              Reusable backup of Chrome profiles and editor plugins, with restore that does not replace emails already signed in on the new Mac.
Trigger words:     backup chrome, chrome profiles, cursor plugins, vscode plugins, android studio plugins, migrate chrome
Not for:           wiping the macOS account (seatsweep-macos-cleanup); full laptop migrate of Bruno/TablePlus/shell

Inputs needed:     which buckets (chrome / cursor / vscode / android-studio); staging path
Steps that worked:
  1. List profiles + plugin sizes, check FDA
  2. Quit apps
  3. rsync with cache/OptGuide excludes, LF scripts
  4. merge-by-email restore
  5. Python ZIP64 pack
Corrections:       do not replace existing Chrome emails; exclude OptGuide; LF not CRLF; --exclude= for openrsync
Traps hit:         TCC on Chrome; CRLF bash 3.2; ditto 4GB zip; nested .git in Cursor plugins; Keychain hang on Safe Storage
Output shape:      inventory table, then staging folder + Restore.command, optional zip
Done when:         picked buckets copied, restore docs in the pack, zip ZIP64 if requested

Dropped:           Bruno/TablePlus/Atuin/Brewfile (separate migrate); factory reset
Save to:           ~/.claude/skills/seatpack-chrome-backup and Cursor user Agent Store
