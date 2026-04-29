import requests
import wikitextparser as wtp

MV_API = "https://www.keyforgegame.com/api/decks/"


def master_vault_lookup(deck_name):
    r = requests.get(MV_API, params={"search": deck_name, "page_size": 1})
    data = r.json().get("data", [])
    if not data:
        return None
    deck = data[0]
    return {"url": "https://www.keyforgegame.com/deck-details/{}".format(deck["id"])}


def deprecated_markup(wp, page_name):
    p = wp.page(page_name)
    existing = p.read()
    lines = existing.split('\n')
    new = []
    while lines:
        next_line = lines.pop(0)
        new.append(next_line)
        if "<!-- mvdecklink " in next_line:
            alter_line = lines.pop(0)
            parse = wtp.parse(alter_line)
            for link in parse.external_links:
                print(link.text, link.url)
                result = master_vault_lookup(deck_name=link.text)
                if result:
                    link.url = result["url"]
            new.append(parse.pprint())
    updated = "\n".join(new)
    if updated != existing:
        p.edit(updated, "deck lookups")
