# archonarcanabots

Python automation tools for the [Archon Arcana](https://archonarcana.com) KeyForge wiki (MediaWiki + Cargo).

Originally written by [saluk](https://github.com/saluk) — forked from [saluk/archonarcanabots](https://github.com/saluk/archonarcanabots) and updated after the 2024–2025 migration from self-hosted to MyWikis hosting.

---

## Setup

Copy `passwords_example.py` to `passwords.py` and fill in your credentials:

```
WIKI_BOT_NAME     — bot account username (e.g. "MyBot")
WIKI_BOT_LOGIN    — bot password login name (e.g. "MyBot@mybotpassword")
WIKI_BOT_PASSWORD — bot password value
DISCORD_WEBHOOK   — Discord webhook URL for alerts (optional)
DOK_API_KEY       — Decks of KeyForge API key (only needed if using dok.py)

# Reddit bot (only needed if running reddit.py)
REDDIT_BOT_NAME, REDDIT_BOT_USER_NAME, REDDIT_CLIENT_ID,
REDDIT_CLIENT_SECRET, REDDIT_USER_PASSWORD
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Entry Point: `wiki_page_updater.py`

The main CLI dispatcher. Connects to the wiki on startup, then routes to the right tool based on the command argument.

```
python wiki_page_updater.py <command> [options]
```

### Global options

| Flag | Description |
|---|---|
| `--batch` | Skip confirmation prompts between edits (default: pause after each) |
| `--search TEXT` | Filter cards/pages by name regex |
| `--restrict_expansion N` | Limit to a specific expansion number |
| `--restricted FIELDS` | Pipe-separated list of card fields to update (e.g. `CardData.Text\|CardData.Traits`) |
| `--excluded FIELDS` | Pipe-separated list of card fields to skip |
| `--locale LOCALE` | Two-part locale code, e.g. `es-es`. Comma-separate for multiple. |
| `--change_comment TEXT` | Edit summary written to the wiki (default: `"bot update"`) |
| `--prevent_spoilers` | Force card pages to non-spoiler values when promoting a set |
| `--sheet NAME` | Spreadsheet name to target (used by `merge_spreadsheets`) |
| `--testfile PATH` | JSON file of test card data (used by some commands) |

---

### Commands

#### Card data

**`read_card_changes`** — Diff local card JSON against live wiki `CardData:` pages and write detected changes to `data/changed_cards_<expansion>.json`. Requires `--restrict_expansion`.

```
python wiki_page_updater.py read_card_changes --restrict_expansion 341
python wiki_page_updater.py read_card_changes --restrict_expansion 341 --restricted "CardData.Text|CardData.Traits"
python wiki_page_updater.py read_card_changes --restrict_expansion 341 --prevent_spoilers
```

The output JSON has one entry per changed card. Each entry has a `reason` field:
- `update` — field change on a card that exists in one set
- `revision` — field change on a card that appears in multiple sets
- `addset` — new set data being added to an existing card

You can manually edit the JSON before writing (e.g. change `reason` to `skip` to exclude a card).

---

**`write_card_changes`** — Apply a previously generated changes JSON to the wiki. Requires `--restrict_expansion` to identify the filename (`data/changed_cards_<expansion>.json`). Sends a Discord alert for each updated page.

```
python wiki_page_updater.py write_card_changes --restrict_expansion 341
python wiki_page_updater.py write_card_changes --restrict_expansion 341 --change_comment "Errata update"
```

---

**`list_cards`** — Export all cards in an expansion to a CSV (`data/list_cards_<expansion>.csv`), sorted by card number. Requires `--restrict_expansion`.

```
python wiki_page_updater.py list_cards --restrict_expansion 341
```

---

#### Wiki tables

**`table_to_cargo`** — Parse the "Local Groups and Shops" wiki page (a hand-edited table organized by continent/country/region) and write the rows into Cargo database records.

```
python wiki_page_updater.py table_to_cargo
```

---

#### Spreadsheets

**`merge_spreadsheets`** — Pull a published Google Sheet and merge its rows into a wiki Cargo table. Sheet URLs are configured in `data/spreadsheets.json`. The sheet's metadata row controls which Cargo table is targeted and how duplicates are handled.

```
python wiki_page_updater.py merge_spreadsheets --sheet "TranslationTable"
python wiki_page_updater.py merge_spreadsheets --sheet "TranslationTable" --batch
```

---

#### Static files

**`javascript`** — Upload JavaScript files from `javascript/` to the wiki.

**`lua`** — Upload Lua modules from `scribunto/` to the wiki.

---

### Archived / non-functional commands

These commands are still present in `wiki_page_updater.py` but depend on the PostgreSQL master vault infrastructure that no longer exists. They will fail to import. They are documented here for reference only.

| Command | Why it's broken |
|---|---|
| `build_wiki_db` | Requires PostgreSQL DB via `wiki_card_db.build_json()` |
| `eventdecks` | Requires `tool_update_decks` (archived — needs DB session for deck objects) |
| `new_cards` | Requires mastervault workers (archived — needs PostgreSQL card records) |
| `deck_scrape_lag` | Requires mastervault workers (archived — was a DB health check) |

---

## Adding a New Set

When a new KeyForge set is released, use this pipeline to import it into the wiki:

**Step 1 — Scrape card data from the Ghost Galaxy API**

```
python -m mastervault.mvlite --expansion=N --pages=10
```

Run repeatedly (incrementing `--pages`) until the script reports no more new cards found. Card data is saved to `data/mvlite_cards_N.json`. The expansion number (`N`) is the numeric ID used by the keyforgegame.com API (e.g. 800, 855, 886, 939).

**Step 2 — Build the local card database from the scraped data**

```
python wiki_page_updater.py build_wiki_db_skyjedi
```

**Step 3 — Diff against the wiki and review changes**

```
python wiki_page_updater.py read_card_changes --restrict_expansion N
```

Outputs `data/changed_cards_N.json`. Review this file and set `"reason": "skip"` on any entries you want to exclude.

**Step 4 — Write changes to the wiki**

```
python wiki_page_updater.py write_card_changes --restrict_expansion N
```

**Step 5 — Upload card images**

```
python wiki_page_updater.py upload_images --restrict_expansion N --batch
```

---

## `mastervault/mvlite.py` — Ghost Galaxy API Scraper

Scrapes card data for a specific expansion directly from the keyforgegame.com API with no database required. Saves progress across runs so it can be stopped and resumed.

```
python -m mastervault.mvlite --expansion=907 --pages=5
```

| Flag | Description |
|---|---|
| `--expansion` | Expansion ID (required) |
| `--pages` | Number of API pages to fetch in this run (default: 1) |

Output files: `data/mvlite_cards_{expansion}.json` and `data/mvlite_progress_{expansion}.json`.

---

## `reddit.py` — Reddit Bot

Monitors r/KeyforgeGame for `[[Card Name]]` syntax in posts and comments. Looks the name up in the wiki (with fuzzy matching) and replies with a link.

```
python reddit.py
```

Tracks replied posts in `reddit_post_index.json` to avoid duplicate replies. Runs continuously; uses exponential backoff on failures.

Requires Reddit credentials in `passwords.py`.

---

## Library Modules

These are not run directly — they are imported by the tools above.

### `connections.py`

Provides authenticated connections:

- `get_wiki()` — returns a logged-in `mw_api_client` wiki object pointed at `archonarcana.mywikis.wiki/w139/api.php`
- `get_reddit()` — returns an authenticated PRAW Reddit instance with `r/KeyForgeGame` and `r/testingground4bots` preloaded

### `wikibase.py`

Core wiki I/O layer.

- `MediawikiManager` — reads and writes wiki pages, skips no-op edits
- `CargoTable` — parses and formats MediaWiki Cargo table markup; handles create/update/sort of structured records
- `Section` — parses wiki section structure (headers, categories)
- `update_page()` — writes a page only if content has changed; optionally pauses for confirmation

### `util.py`

- `cargo_query(params)` — sends a `cargoquery` API request and returns the JSON result; results are cached in-process
- `dequote(text)` — normalizes typographic quotes in card text
- `sanitize_deck_name(name)` — strips punctuation and normalises whitespace for deck name comparisons

### `alerts.py`

- `discord_alert(msg)` — posts a message to the Discord webhook configured in `passwords.py`. Used by tools to notify when pages are updated or errors occur.

### `preprocessors.py`

- `deprecated_markup(page_name)` — finds `<!-- mvdecklink -->` comment markers on a wiki page and updates the stale deck URLs on the following line using a fresh Master Vault lookup.

### `tool_update_cards.py`

Bulk card page updater, used by several `wiki_page_updater.py` commands. Reads card data from the JSON files in `data/` via `wiki_card_db.load_json()` — no PostgreSQL required. Key functions:

- `update_card_views(wp, card_title)` — writes the `{{#invoke: luacard | viewcard}}` template to a card's wiki page
- `update_card_page_cargo(wp, card, data_to_update)` — reads/writes a card's `CardData:` cargo page; supports modes `carddb`, `relink`, `insert_search_text`, `reprint_pull`, `reprint_write`
- `upload_image_for_card(wp, locale, card)` — downloads a card image from the CDN and uploads it to the wiki
- `update_cards_v2(wp, ...)` — iterates all cards (with optional filters) and dispatches to the above functions
- `show_cards_with_extra(wp)` — lists card pages that contain content beyond the standard cargo template

### `models/wiki_card_db.py`

Builds and manages the local card database. In the current (post-migration) setup, `load_json()` loads pre-built card data from the `data/` directory rather than rebuilding from PostgreSQL. Key functions:

- `load_json()` — loads card data from JSON files into memory
- `get_cargo(card, cargo_table)` — populates a `CargoTable` object with a card's data
- `link_card_titles()` / `link_card_traits()` — generates wiki-style `[[links]]` within card text
- `fuzzyfind(name)` — fuzzy card name matching (used by the Reddit bot)

---

## `dok.py`

Fetches your deck list from the [Decks of KeyForge](https://decksofkeyforge.com) public API.

```python
from dok import get_decks
decks = get_decks(passwords.DOK_API_KEY)
```

Requires `DOK_API_KEY` in `passwords.py`.

---

## `archive/`

Contains modules that depend on the PostgreSQL master vault infrastructure removed during the MyWikis migration. Kept for reference.

| Path | What it was |
|---|---|
| `archive/mastervault/` | Scraper that pulled deck/card data from keyforgegame.com into PostgreSQL |
| `archive/wormhole/` | FastAPI wrapper around the scraped data + deck page writer |
| `archive/tool_update_decks.py` | Tournament deck stats importer (required a live DB session) |
| `archive/mv_model.py` | SQLAlchemy ORM models for the PostgreSQL database |
