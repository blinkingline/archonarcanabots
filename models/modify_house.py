# Some cards like AS skybeasts can appear in every house
# of the set, but the raw skyjedi JSON doesn't encode this.

MOMU_HOUSES = "Dis • Logos • Sanctum • Saurian • Shadows • Star Alliance • Untamed"
ÆS_HOUSES = "Brobnar • Dis • Ekwidon • Geistoid • Logos • Mars • Skyborn"
CC_HOUSES = "Brobnar • Dis • Mars • Sanctum • Saurian • Skyborn • Untamed"

CARDS_TO_MODIFY_HOUSE = {
    479: {
        "Dark Æmber Vault":       MOMU_HOUSES,
    },
    874: {
        "Build Your Champion":    MOMU_HOUSES,
        "Digging Up the Monster": MOMU_HOUSES,
        "Tomes Gigantica":        MOMU_HOUSES,
        "Dark Æmber Vault":       MOMU_HOUSES,
    },
    800: {
        "Akugyo":            ÆS_HOUSES,
        "Alien Puffer":      ÆS_HOUSES,
        "Anvil Crawler":     ÆS_HOUSES,
        "Beehemoth":         ÆS_HOUSES,
        "Blue Æmberdrake":   ÆS_HOUSES,
        "Colossipede":       ÆS_HOUSES,
        "Falcron":           ÆS_HOUSES,
        "Grinder Swarm":     ÆS_HOUSES,
        "Grizzled Wyvern":   ÆS_HOUSES,
        "Hungry Hippogriff": ÆS_HOUSES,
        "Icarus 2.0":        ÆS_HOUSES,
        "Impzilla":          ÆS_HOUSES,
        "Lancet":            ÆS_HOUSES,
        "Malifi Dragon":     ÆS_HOUSES,
        "Naja":              ÆS_HOUSES,
        "Red Æmberdrake":    ÆS_HOUSES,
        "Rorqual":           ÆS_HOUSES,
        "Screeyan":          ÆS_HOUSES,
        "Sentient Cloud":    ÆS_HOUSES,
        "Titanarpon":        ÆS_HOUSES,
        "Tyrannus Aquilae":  ÆS_HOUSES,
        "Volax":             ÆS_HOUSES,
        "Yellow Æmberdrake": ÆS_HOUSES,
    },
    918: {
        "Akugyo":            CC_HOUSES,
        "Alien Puffer":      CC_HOUSES,
        "Anvil Crawler":     CC_HOUSES,
        "Beehemoth":         CC_HOUSES,
        "Blue Æmberdrake":   CC_HOUSES,
        "Colossipede":       CC_HOUSES,
        "Falcron":           CC_HOUSES,
        "Grinder Swarm":     CC_HOUSES,
        "Grizzled Wyvern":   CC_HOUSES,
        "Hungry Hippogriff": CC_HOUSES,
        "Icarus 2.0":        CC_HOUSES,
        "Impzilla":          CC_HOUSES,
        "Lancet":            CC_HOUSES,
        "Malifi Dragon":     CC_HOUSES,
        "Naja":              CC_HOUSES,
        "Red Æmberdrake":    CC_HOUSES,
        "Rorqual":           CC_HOUSES,
        "Screeyan":          CC_HOUSES,
        "Sentient Cloud":    CC_HOUSES,
        "Titanarpon":        CC_HOUSES,
        "Tyrannus Aquilae":  CC_HOUSES,
        "Volax":             CC_HOUSES,
        "Yellow Æmberdrake": CC_HOUSES,
    },
}

def as_needed(card):
    if card["expansion"] in CARDS_TO_MODIFY_HOUSE:
        if card["card_title"] in CARDS_TO_MODIFY_HOUSE[
                card["expansion"]
        ]:
            return CARDS_TO_MODIFY_HOUSE[
                card["expansion"]
            ][
                card["card_title"]
            ]

    return card["house"]
