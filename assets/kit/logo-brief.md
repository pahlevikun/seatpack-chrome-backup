# Logo brief: seatpack

## 0. Routing

- **Mode:** one_shot
- **Kit tier:** lite
- **Library category:** oss_repo_mark
- **Clichés to avoid:** GitHub octocat, GitLab fox, GNU head, single-letter monogram (Go), Chrome multicolor circle logo, a generic suitcase-plus, Murk the mug
- **Grill mode:** skip (one_shot, copy and tokens locked)
- **Intent:** The four README assets should tell a person who already has Chrome signed in on the next laptop that this bag carries profiles and editor plugins, and that restore matches the email on the luggage tag. Mode is one_shot, kit tier lite. The mark is a satchel with three bands and an email tag. Column 3 is a terminal narrative (inventory, then merge by email). Tokens, type, and the flat background are fixed. Library marks were study-only.
- **Context sources:**
  - Google Chrome brand color vocabulary (study only; **not** official Google branding): Blue `#4285F4`, Red `#EA4335`, Yellow `#FBBC04`, Green `#34A853` ([Google brand color guidelines](https://about.google/brand-resource-center/brand-elements/))
  - Material / Google gray text tokens: `#202124`, `#5F6368`, surfaces `#F8F9FA`, `#F1F3F4`, `#E8EAED`, `#DADCE0`
  - Prior generation cited `levistack/docs/assets/logo.svg` for layout only; palette superseded by Chrome-inspired bright theme (2026-11-07)
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

- **Wordmark:** `seat` in `#202124` + `pack` in `#4285F4` (8 letters). Cursor strip: four 7px bands (blue, red, yellow, green).
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

Source: Chrome-inspired palette (not official Google branding). Layout roles still follow `logo-kit-svg/references/token-table.md`.

| Role | Hex | Where |
|---|---|---|
| `--bg` | `#F8F9FA` | banner fill, icon tile, social cards |
| `--surface` / card | `#FFFFFF` | terminal card, merge panel, luggage tag |
| `--surface2` / topbar | `#F1F3F4` | terminal title bar |
| `--line` | `#DADCE0` | banner stroke, rules |
| `--line2` | `#E8EAED` | card stroke, timeline rail |
| `--fg` | `#202124` | wordmark `seat`, terminal primary text |
| `--muted` | `#5F6368` | tagline, motto, secondary terminal |
| `--dim` | `#9AA0A6` | pipeline arrows |
| `--accent` | `#4285F4` | wordmark `pack`, chip labels, merge highlights |
| chrome-red | `#EA4335` | strap, cord, window dot, pill dot |
| chrome-yellow | `#FBBC04` | upper bag band, profiles pill stroke |
| chrome-green | `#34A853` | middle band, `keep`, editor-plugins pill stroke |
| chrome-blue | `#4285F4` | lower band, tag stroke |
| pill fill | `#F1F3F4` | column 2 pills |
| ink stroke | `#3C4043` | bag outline |

`--del` and `--add` are omitted. Column 3 is `feature-summary`, not `diff-hunks`.

Flat `#F8F9FA` only. No scanlines. No Chrome circle mark.

## 4. Mark

A satchel: red strap, gray flap, three horizontal bands (yellow, green, blue), and a luggage tag that reads `ada@example.com`. The tag is the merge key. Not Murk. Not the Chrome logo.

## 5. Research

`search_library.py --category oss_repo_mark --summary` returned 20 marks (github, gitlab, gnu, mozilla, go, and others). `search_examples.py --has-animation true --summary` returned applydiff and logo-kit-svg. Studied for weight only. Nothing from `library/svg/` is pasted into the four deliverables.
