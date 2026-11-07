# Logo brief: seatpack

## 0. Routing

- **Mode:** one_shot
- **Kit tier:** lite
- **Library category:** oss_repo_mark
- **Clichés to avoid:** GitHub octocat, GitLab fox, GNU head, single-letter monogram (Go), Chrome's circle, a generic suitcase-plus, Murk the mug
- **Grill mode:** skip (one_shot, copy and tokens locked)
- **Intent:** The four README assets should tell a person who already has Chrome signed in on the next laptop that this bag carries profiles and editor plugins, and that restore matches the email on the luggage tag. Mode is one_shot, kit tier lite. The mark is a satchel with three bands and an email tag. Column 3 is a terminal narrative (inventory, then merge by email). Tokens, type, and the flat background are fixed. Library marks were study-only.
- **Context sources:**
  - `levistack/docs/assets/logo.svg` (hex tokens, IBM Plex, card-as-terminal)
  - `logo-kit-svg/references/token-table.md` (roles; omit `--del` / `--add` when column 3 is not `diff-hunks`)
  - `logo-kit-svg/references/svg-blueprints.md` (512 and 904 grids, column x=184 and x=456, 24px gutter)
  - `logo-kit-svg/references/banner-column-3.md` (`feature-summary`, no red/green hunks)
  - `logo-kit-svg/references/animation-choreography.md` (4.6s icon, 6s banner, stroke-dash, reduced motion)
  - `logo-kit-svg/references/brand-kit-tiers.md` and `deliverables.md` (lite still ships platform PNG and social SVG+PNG)
  - `logo-kit-svg/scripts/svglib_repo.py` `pill_width_chars` (`chars * 7.2 + 32`)
  - Skill tree: `SKILL.md`, `references/safety-notes.md`, `scripts/merge_chrome_profiles.py`
- **Unknown after lookup:** `--dim` has no hex in the cited token list. Motto uses `--muted` `#98a2b6` from the levistack logo. `social_cards.py` hardcodes muted `#a99b83`; generated social SVG text was recolored to `#98a2b6` after the script ran.
- **Preview artifacts:** none (lite). `kit_build.py` still writes a tiles board and a preview sheet.
- **Platform pack:** favicon + iOS + Android (`assets/kit/platform/`)
- **Gallery publish:** skip
- **Social cards:** `assets/kit/social/` SVG + PNG
- **Banner column 3 mode:** `feature-summary` (terminal narrative: inventory, then merge by email). Not `diff-hunks`.
- **Library reference slugs (study only):** github, gitlab, gnu, mozilla, go. No copies under `assets/kit/library-samples/`.

## 1. Brand and copy

- **Wordmark:** `seat` in `#e8e4f4` + `pack` in `#c99d48` (8 letters)
- **Wordmark cursor x:** `328` (about 8px after the lowercase word; the 38px formula `184 + ceil(8 * 20.2) = 346` overshoots lowercase)
- **README tagline:** Chrome profiles and editor plugins, in one bag. Restore merges by email.
- **Banner tagline (fits column 2):** `one bag. merge by email.` (24 chars)
- **Pill 1:** `profiles` (8 chars) width `90` (`8 * 7.2 + 32 = 89.6`, ceil). Dot included. x starts at 186.
- **Pill 2:** `editor plugins` (14 chars) width `133` (`14 * 7.2 + 32 = 132.8`, ceil). x = `98` inside the pill group (90 + 8 gap).
- **Group end:** 186 + 90 + 8 + 133 = 417. Gutter to column 3 at x=456 is 39px.
- **Motto:** A bag that refuses to sit on the wrong person. Wrapped on two lines so it stays left of x=432.

## 2. Column 3 card copy

No red or green rows. No `-` or `+`.

- **Topbar chip:** `inventory` (9 chars). Width `90` (`ceil(9 * 6.8) + 28`).
- **Topbar aside:** `merge by email`
- **List:** `Default` / `ada@example.com`, `Profile 1` / `budi@example.com`
- **Merge:** `ada@example.com` keep, `budi@example.com` Profile N
- **Pipeline:** `list` then `quit` then `pack` then `merge`, chip `by email`

Samples are Ada Example and Budi Example. Profile folders stay `Default` and `Profile 1`.

## 3. Color tokens

Source file: `levistack/docs/assets/logo.svg`.

| Role | Hex | Where that file uses it |
|---|---|---|
| `--bg` | `#17152e` | banner fill, tile fill |
| `--surface` / card | `#3a3358` | border token; that logo fills the terminal card with it |
| `--surface2` / topbar | `#4a4f7a` | fog; that logo fills the top bar with fog |
| `--line` | `#3a3358` | banner stroke |
| `--line2` | `#4a4f7a` | card stroke on this banner (fog) |
| `--fg` | `#e8e4f4` | `levi` wordmark |
| `--muted` | `#98a2b6` | tagline |
| `--dim` | `#98a2b6` | no separate hex in the cited list |
| `--accent` | `#c99d48` | `stack` wordmark, cursor |
| `--amber-bg` | `#3a3358` | pill fill on that logo |
| `--accent-dim` | `#b2853a` | pill stroke, gold band |
| teal band | `#3c7f7c` | middle mug band |
| purple band | `#66589a` | lower mug band |
| gold band | `#b2853a` | upper mug band |

`--del` and `--add` are omitted. `token-table.md` says those roles are for `diff-hunks` only.

Flat `#17152e` only. No scanlines, no fog filters, no mug.

## 4. Mark

A satchel: strap, flap, three horizontal bands in the levistack band order (gold, teal, purple), and a luggage tag that reads `ada@example.com`. The tag is the merge key. Sibling of levistack. Not Murk.

## 5. Research

`search_library.py --category oss_repo_mark --summary` returned 20 marks (github, gitlab, gnu, mozilla, go, and others). `search_examples.py --has-animation true --summary` returned applydiff and logo-kit-svg. Studied for weight only. Nothing from `library/svg/` is pasted into the four deliverables.
