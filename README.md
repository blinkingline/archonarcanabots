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
| `build_wiki_db_skyjedi` | Same |
| `upload_images` | Requires `tool_update_cards` (archived) |
| `import_cards_locale` | Requires `tool_update_cards` (archived) |
| `update_card_views` | Requires `tool_update_cards` (archived) |
| `reprint_pull` / `reprint_write` | Requires `tool_update_cards` (archived) |
| `relink` | Requires `tool_update_cards` (archived) |
| `insert_search_text` | Requires `tool_update_cards` (archived) |
| `debut_sets` | Requires `tool_update_cards` (archived) |
| `eventdecks` | Requires `tool_update_decks` (archived) |
| `new_cards` | Requires mastervault workers (archived) |
| `deck_scrape_lag` | Requires mastervault workers (archived) |

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

### `models/wiki_card_db.py`

Builds and manages the local card database. In the current (post-migration) setup, `load_json()` loads pre-built card data from the `data/` directory rather than rebuilding from PostgreSQL. Key functions:

- `load_json()` — loads card data from JSON files into memory
- `get_cargo(card, cargo_table)` — populates a `CargoTable` object with a card's data
- `link_card_titles()` / `link_card_traits()` — generates wiki-style `[[links]]` within card text
- `fuzzyfind(name)` — fuzzy card name matching (used by the Reddit bot)

---

## `archive/`

Contains modules removed from the active codebase after the migration away from self-hosted infrastructure:

| Path | What it was |
|---|---|
| `archive/mastervault/` | Scraper that pulled deck/card data from keyforgegame.com into PostgreSQL |
| `archive/wormhole/` | FastAPI wrapper around the scraped data + Decks of KeyForge API client |
| `archive/tool_update_cards.py` | Bulk card page updater (depended on the Postgres card DB) |
| `archive/tool_update_decks.py` | Tournament deck stats importer (depended on a DB session) |
| `archive/mv_model.py` | SQLAlchemy ORM models for the PostgreSQL database |
