import unittest

from models import wiki_model
from models import skyjedi_model


class WikiModelTests(unittest.TestCase):

    def setUp(self):
        # unittest suggests this when test data diffs
        # were too long.
        self.maxDiff = None

        local_json = skyjedi_model.LocalJson()
        local_json.add_file(
            "data/test_data/wiki_model_examples.json"
        )
        self.cards = local_json.get_cards()

        # No power/armor
        self.wave = self.find(
            "ac3a1d32-f21d-4336-b263-ac55817c59f6"
        )
        # X power
        self.picaroon = self.find(
            "a9479b8e-710e-420f-aac4-de1d2d10aeb5"
        )
        # Power/armor >0
        self.sinder = self.find(
            "4e1beaa4-9ab3-4764-b8e9-229f0b9c81bd"
        )

    def find(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                return card
        raise Exception("Missing id")


    # Early processing like fancy_quotes has already happened,
    # but we haven't gotten to, say, bifurcate yet.
    def test_card_data(self):

        # Cards without power left alone.
        self.assertEqual(self.wave["power"], None)
        self.assertEqual(self.wave["armor"], None)
        self.wave = wiki_model.card_data(self.wave)
        self.assertEqual(self.wave["power"], None)
        self.assertEqual(self.wave["armor"], None)

        # Cards with integer power and armor
        # get integer values.
        self.assertEqual(self.sinder["power"], "6")
        self.assertEqual(self.sinder["armor"], "2")
        self.sinder = wiki_model.card_data(self.sinder)
        self.assertEqual(self.sinder["power"], 6)
        self.assertEqual(self.sinder["armor"], 2)

        # X-power gets turned into integer zero.
        self.assertEqual(self.picaroon["power"], "X")
        self.assertEqual(self.picaroon["armor"], "0")
        self.picaroon = wiki_model.card_data(self.picaroon)
        self.assertEqual(self.picaroon["power"], 0)
        self.assertEqual(self.picaroon["armor"], 0)

    def test_artist_recovery(self):
        # Card with missing artist should be recovered from CSV
        # "Daughter" is a known card in illustrators.csv with artist "Roman Semenenko"
        daughter_card = {
            "card_title": "Daughter",
            "card_type": "Action",
            "card_text": "",
            "flavor_text": "",
            "expansion": "341",
            "card_number": "001",
            "house": "Logos",
            "rarity": "Common",
            "traits": "",
            "power": "",
            "armor": "",
            "artist": ""
        }
        processed = wiki_model.card_data(daughter_card)
        self.assertEqual(processed["artist"], "Roman Semenenko")

        # Card with existing artist should not be overwritten
        son_card = daughter_card.copy()
        son_card["card_title"] = "Son"
        son_card["artist"] = "Someone Else"
        processed = wiki_model.card_data(son_card)
        self.assertEqual(processed["artist"], "Someone Else")
