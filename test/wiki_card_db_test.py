import unittest
import copy

from models import wiki_card_db
from models import skyjedi_model


class WikiCardDbTests(unittest.TestCase):

    def setUp(self):
        # unittest suggests this when test data diffs
        # were too long.
        self.maxDiff = None
        self.setUpMasterVaultJSON()

    def setUpMasterVaultJSON(self):
        local_json = skyjedi_model.LocalJson()
        local_json.add_file(
            "data/test_data/wiki_card_db_examples.json"
        )
        self.mv_cards = local_json.get_cards()

        # In MM: Cre1/2, Rare/FIXED, and
        # both halves have the card text.
        self.ultra1_mm = self.mvFind(
            "f8b21c6a-56a4-4e1e-8a4a-ca4bcb8e3b68"
        )
        self.ultra2_mm = self.mvFind(
            "2520f79b-ad48-47ba-b96e-1b34a528ed5e"
        )
        # In MoMu: Cre/Cre, Rare/Special,
        # and only one half has the card text.
        self.ultra1_momu = self.mvFind(
            "0afebc37-1f09-4544-9bca-d3ee05855c21"
        )
        self.ultra2_momu = self.mvFind(
            "ef7e2d21-cb1b-413a-8f8b-bc37335d19ee"
        )

        self.grim_anomaly = self.mvFind(
            "62427579-c56b-4665-b1a1-85c04e16ba6e"
        )
        self.grim_gr = self.mvFind(
            "6448ac87-5019-4bfd-9a8f-021de5a7e3e3"
        )

        self.johnny_mm = self.mvFind(
            "e955f15e-168f-4b9a-a17a-7a6191d62390"
        )
        self.johnny_toc_redem = self.mvFind(
            "f74a8d23-d941-4aaa-8030-8eff3dc0dd64"
        )

        self.chuff_cota = self.mvFind(
            "2948a6fc-f7fa-45f2-b73d-fdf5f4216e46"
        )
        self.chuff_mcw = self.mvFind(
            "ed4f373a-512b-4dbc-8e99-7771fdd61ed0"
        )
        self.taengoo_mcw = self.mvFind(
            "0051e976-e65e-48e1-9f1e-b025e281528b"
        )

        # Prophecies and Archon Powers just get some
        # schema manipulation.
        self.heads = self.mvFind(
            "55c0bed1-320e-4024-811b-b3f1005e385a"
        )
        self.chari = self.mvFind(
            "70bd430f-6bd4-46bf-a041-c54647886c3c"
        )

        # Agamignus is a Redemption card that is new
        # and debuts in Redemption. It should not have
        # the "Agamignus (Redemption)" title modification.
        self.agami = self.mvFind(
            "e0e33161-59f5-407c-83c9-e90f2efee752"
        )

        # Bandit Culver has a house enhancement. We
        # should convert the house-by-house unicode into
        # per-house template.
        self.culv = self.mvFind(
            "0c26d682-793b-43b2-bfd8-2b5636a83567"
        )
        self.batch = self.mvFind(
            "6dfc4bae-d3ce-4027-a21c-5addaebe8aed"
        )
        # And two house enhancers from the same house, but
        # different sets and the raw JSON uses different
        # Unicode case.
        self.sear = self.mvFind(
            "d319d78f-c136-4781-9d3b-33acae49ebca"
        )
        self.skor = self.mvFind(
            "4c7c5150-d0cd-4c6a-8763-551cd21c9a04"
        )

        # Example of non-house multi enhance.
        self.skald = self.mvFind(
            "bc6f4a2a-c0d4-40b4-84c2-846750b10310"
        )

        # Skybeasts are in multiple houses per set,
        # and across sets those are different sets.
        # so the wiki card page combines them.
        self.falcron_as = self.mvFind(
            "b8b7adc3-a6c3-4ffc-8df3-6b0ad641da08"
        )
        self.falcron_cc = self.mvFind(
            "68bef9c0-09bb-482a-adb9-aaec1e21c6ef"
        )

        # And some cards that don't need special
        # bifurcation
        self.dew_cota = self.mvFind(
            "f0c4cb0f-8e5f-454c-a6ad-35f35ac3c98a"
        )
        self.fear_cota = self.mvFind(
            "10715fd2-031a-47ca-9119-9b7b2ec1d2c0"
        )

    def mvFind(self, card_id):
        for card in self.mv_cards:
            if card["id"] == card_id:
                return card
        raise Exception("Missing id")


    def makeDeepCopies(self, card_list):
        return [copy.deepcopy(c) for c in card_list]


    def test_bifurcate_giants(self):
        # Returns (is_giant, merged_halves)
        expected = (
            False,
            []
        )
        actual = wiki_card_db.bifurcate_giants(
            self.makeDeepCopies([self.dew_cota])
        )
        self.assertEqual(expected, actual)

        ultra_mm_merged = copy.deepcopy(self.ultra1_mm)
        ultra_mm_merged["card_type"] = "Creature"
        ultra_momu_merged = copy.deepcopy(self.ultra2_momu)
        ultra_momu_merged["rarity"] = "Rare"
        expected = (
            True,
            [ultra_mm_merged, ultra_momu_merged]
        )
        actual = wiki_card_db.bifurcate_giants(
            self.makeDeepCopies(
                [self.ultra1_mm, self.ultra2_mm,
                 self.ultra1_momu, self.ultra2_momu]
            )
        )
        self.assertEqual(expected, actual)


    def test_bifurcate_anomalies(self):
        # Returns (has_anomaly, anomalies, other)
        expected = (
            False,
            [],
            [self.dew_cota]
        )
        actual = wiki_card_db.bifurcate_anomalies(
            self.makeDeepCopies([self.dew_cota])
        )
        self.assertEqual(expected, actual)

        expected = (
            True,
            [self.grim_anomaly],
            [self.grim_gr]
        )
        actual = wiki_card_db.bifurcate_anomalies(
            self.makeDeepCopies(
                [self.grim_gr, self.grim_anomaly]
            )
        )
        self.assertEqual(expected, actual)


    def test_bifurcate_redemption(self):
        # Returns (has_mixed_redemption, redemption, other)
        expected = (
            False,
            [],
            [self.dew_cota]
        )
        actual = wiki_card_db.bifurcate_redemption(
            self.makeDeepCopies([self.dew_cota])
        )
        self.assertEqual(expected, actual)

        johnny_toc_redem_updated = \
            copy.deepcopy(self.johnny_toc_redem)
        johnny_toc_redem_updated["card_title"] = \
            "Johnny Longfingers (Redemption)"
        expected = (
            True,
            [johnny_toc_redem_updated],
            [self.johnny_mm]
        )
        actual = wiki_card_db.bifurcate_redemption(
            self.makeDeepCopies(
                [self.johnny_mm, self.johnny_toc_redem]
            )
        )
        self.assertEqual(expected, actual)

        expected = (
            False,
            [],
            [self.agami]
        )
        actual = wiki_card_db.bifurcate_redemption(
            self.makeDeepCopies([self.agami])
        )
        self.assertEqual(expected, actual)


    def test_bifurcate_martian_faction(self):
        # Returns (has_martian_faction, faction, other)
        expected = (
            False,
            [],
            [self.dew_cota]
        )
        actual = wiki_card_db.bifurcate_martian_faction(
            self.makeDeepCopies([self.dew_cota])
        )
        self.assertEqual(expected, actual)

        chuff_mcw_updated = copy.deepcopy(self.chuff_mcw)
        chuff_mcw_updated["card_title"] = "Chuff Ape (Elders)"
        expected = (
            True,
            [chuff_mcw_updated],
            [self.chuff_cota]
        )
        actual = wiki_card_db.bifurcate_martian_faction(
            self.makeDeepCopies(
                [self.chuff_cota, self.chuff_mcw]
            )
        )
        self.assertEqual(expected, actual)

        taengoo_mcw_updated = copy.deepcopy(self.taengoo_mcw)
        taengoo_mcw_updated["card_title"] = \
            "Agent Taengoo (Ironyx Rebels)"
        expected = (
            True,
            [taengoo_mcw_updated],
            []
        )
        actual = wiki_card_db.bifurcate_martian_faction(
            self.makeDeepCopies([self.taengoo_mcw])
        )
        self.assertEqual(expected, actual)


    def test_bifurcate_multi_house(self):
        # Returns (multi_house, merged)
        expected = (
            False,
            [self.dew_cota]
        )
        actual = wiki_card_db.bifurcate_multi_house(
            self.makeDeepCopies([self.dew_cota])
        )
        self.assertEqual(expected, actual)

        falcron_as_merged = copy.deepcopy(self.falcron_as)
        falcron_as_merged["house"] = "Brobnar • Dis • Ekwidon • "\
                                     "Geistoid • Logos • Mars • "\
                                     "Sanctum • Saurian • Skyborn • Untamed"
        falcron_cc_merged = copy.deepcopy(self.falcron_cc)
        falcron_cc_merged["house"] = "Brobnar • Dis • Ekwidon • "\
                                     "Geistoid • Logos • Mars • "\
                                     "Sanctum • Saurian • Skyborn • Untamed"
        expected = (
            True,
            [falcron_as_merged, falcron_cc_merged]
        )
        actual = wiki_card_db.bifurcate_multi_house(
            self.makeDeepCopies(
                [self.falcron_as, self.falcron_cc]
            )
        )
        self.assertEqual(expected, actual)


    def test_bifurcate_38s(self):
        # Returns (has_38s, the38s, other)

        # First a card left untouched.
        expected = (
            False,
            [],
            [self.dew_cota]
        )
        actual = wiki_card_db.bifurcate_38s(
            self.makeDeepCopies([self.dew_cota])
        )
        self.assertEqual(expected, actual)

        # Next a prophecy.
        heads_updated = copy.deepcopy(self.heads)
        heads_updated["house"] = None
        heads_updated["card_type"] = "38th Card"
        expected = (
            True,
            [heads_updated],
            []
        )
        actual = wiki_card_db.bifurcate_38s(
            self.makeDeepCopies([self.heads])
        )
        self.assertEqual(expected, actual)

        # And an Archon Power.
        chari_updated = copy.deepcopy(self.chari)
        chari_updated["house"] = None
        chari_updated["card_type"] = "38th Card"
        expected = (
            True,
            [chari_updated],
            []
        )
        actual = wiki_card_db.bifurcate_38s(
            self.makeDeepCopies([self.chari])
        )
        self.assertEqual(expected, actual)


    # This test covers the transformation and batching of MV raw
    # JSON to still MV JSON, meaning the key names and schema.
    def test_process_skyjedi_card_batch(self):
        # From other tests above, get all the inputs and all
        # the expectations. Together run the whole shebang
        # here so the interactions between bifurcate functions
        # comes out correctly.
        # NOTE this test seems verbose and duplicative with the
        # tests above, but it keeps catching bugs where the
        # sequence of bifurcates has an issue. Worth it!

        ultra_mm_merged = copy.deepcopy(self.ultra1_mm)
        ultra_mm_merged["card_type"] = "Creature"
        ultra_momu_merged = copy.deepcopy(self.ultra2_momu)
        ultra_momu_merged["rarity"] = "Rare"

        johnny_toc_redem_updated = \
            copy.deepcopy(self.johnny_toc_redem)
        johnny_toc_redem_updated["card_title"] = \
            "Johnny Longfingers (Redemption)"

        chuff_mcw_updated = copy.deepcopy(self.chuff_mcw)
        chuff_mcw_updated["card_title"] = "Chuff Ape (Elders)"
        taengoo_mcw_updated = copy.deepcopy(self.taengoo_mcw)
        taengoo_mcw_updated["card_title"] = \
            "Agent Taengoo (Ironyx Rebels)"

        falcron_as_merged = copy.deepcopy(self.falcron_as)
        falcron_as_merged["house"] = "Brobnar • Dis • Ekwidon • "\
                                     "Geistoid • Logos • Mars • "\
                                     "Sanctum • Saurian • Skyborn • Untamed"
        falcron_cc_merged = copy.deepcopy(self.falcron_cc)
        falcron_cc_merged["house"] = "Brobnar • Dis • Ekwidon • "\
                                     "Geistoid • Logos • Mars • "\
                                     "Sanctum • Saurian • Skyborn • Untamed"

        # Prophecies and Archon Powers just get some
        # schema manipulation.
        heads_updated = copy.deepcopy(self.heads)
        heads_updated["house"] = None
        heads_updated["card_type"] = "38th Card"
        chari_updated = copy.deepcopy(self.chari)
        chari_updated["house"] = None
        chari_updated["card_type"] = "38th Card"

        expected = [
            # Some single no-bifurcate cards.
            self.dew_cota, self.fear_cota,
            # Giants per-set merge.
            ultra_mm_merged, ultra_momu_merged,
            # Anomalies do not combine into one card.
            self.grim_anomaly, self.grim_gr,
            # Redemption variant becomes a new card.
            self.johnny_mm, johnny_toc_redem_updated,
            # Redemption processing *doesn't* change
            self.agami,
            # Original card stays the same, while MCW
            # variants become a new card. A debut MCW
            # card also starts with the suffix.
            self.chuff_cota,
            chuff_mcw_updated, taengoo_mcw_updated,
            falcron_as_merged, falcron_cc_merged,
            # Prophecies and Archon Powers just get some
            # schema manipulation.
            heads_updated, chari_updated,
        ]

        actual = wiki_card_db.process_skyjedi_card_batch(
            self.makeDeepCopies([
                self.dew_cota, self.fear_cota,
                self.ultra1_mm, self.ultra2_mm,
                self.ultra1_momu, self.ultra2_momu,
                self.grim_anomaly, self.grim_gr,
                self.johnny_mm, self.johnny_toc_redem,
                self.agami,
                self.chuff_cota,
                self.chuff_mcw, self.taengoo_mcw,
                self.falcron_as, self.falcron_cc,
                self.heads, self.chari,
            ])
        )

        # Ignores order of lists.
        self.assertCountEqual(expected, actual)



    # These test covers additional schema and text transforms,
    # like keyword templates, that happen during the MV JSON
    # to AA JSON:
    #     card_data = wiki_model.card_data(card)
    #
    # They are more end-to-end than the above tests, mixing
    # more steps together. But also focused on specific
    # fields.
    #
    # To get example expected text visit the CardData: page
    # and then view source and you'll see the text and search
    # text that matches the processing at this stage.
    #
    # Note that there are *still* differences between this
    # AA JSON and the final JSON on the site when you pull
    # it like so:
    # https://archonarcana.com/api.php?action=cargoquery&format=json&limit=1&tables=CardData&fields=Name%2C+Text&where=name='Dew Faerie'
    # Such as making the characters websafe and replacing
    # {Aember} with the link to the aember icon image.
    def assertAttribute(self, actualCard, field, expected):
        expansionKey = list(actualCard.keys())[0]
        self.assertEqual(
            actualCard[expansionKey][field],
            expected
        )

    def test_mv2aa_json_enhancements(self):
        # Cards that give house enhancements should
        # get text rewritten with a template. Look in
        # wiki_model.card_data(...)
        #
        # Raw MV JSON:
        #   Enhance \uF379 \uF379
        #
        # AA JSON:
        #   [[Enhance|Enhance]]
        #   {{Enhance|Enhance=Mars}} {{Enhance|Enhance=Mars}}

        card_datas = wiki_card_db.process_skyjedi_card_batch(
            self.makeDeepCopies([
                self.dew_cota,
                self.skald,
                self.culv,
                self.batch,
                self.skor
            ])
        )

        cards = {}
        for card_data in card_datas:
            wiki_card_db.add_card(card_data, cards)

        # A simpler card to check first.
        self.assertAttribute(
            cards['Dew Faerie'],
            'card_text',
            '[[Elusive|Elusive]]. (The first time '
            'this creature is attacked each turn, no '
            "damage is dealt.) <p> '''Reap:''' Gain "
            '1{{Aember}}.'
        )

        # We also need a non-house multi enhance to check
        # as well.
        self.assertAttribute(
            cards['Rowdy Skald'],
            'card_text',
            '[[Enhance|Enhance]] '
            '{{Aember}}{{Damage}}{{Damage}}. (These icons '
            'have already been added to cards in your deck.)'
        )

        # Single house enhancement.
        self.assertAttribute(
            cards['Bandit Culver'],
            'card_text',
            '[[Elusive|Elusive]]. '
            '[[Enhance|Enhance]] {{Enhance|Enhance=Shadows}}. '
            '<p> After you discard a Shadows card, if it is the first time '
            'you have discarded a Shadows card this turn, steal 1{{Aember}}.'
        )
        self.assertAttribute(
            cards['Bandit Culver'],
            'card_text_search',
            'Elusive. Enhance Shadows. '
            '<p> After you discard a Shadows card, if it is the first time '
            'you have discarded a Shadows card this turn, steal 1A.'
        )

        self.assertAttribute(
            cards['Skorpeon'],
            'card_text',
            '[[Enhance|Enhance]] {{Enhance|Enhance=Dis}}. '
            "<p> '''After Reap:''' Deal 2{{Damage}} to an enemy creature "
            '[[For each|for each]] of Skorpeon’s Dis neighbors.'
        )
        self.assertAttribute(
            cards['Skorpeon'],
            'card_text_search',
            'Enhance Dis. '
            '<p> After Reap: Deal 2D to an enemy creature for each '
            'of Skorpeon’s Dis neighbors.'
        )

        # Double house enhancement transforms the text and
        # search text differently.
        self.assertAttribute(
            cards['Eldest Batchminder'],
            'card_text',
            '[[Enhance|Enhance]] '
            '{{Enhance|Enhance=Mars}} {{Enhance|Enhance=Mars}}. '
            '(These icons have already been added to cards in '
            'your deck.) <p> At the end of your turn, give each '
            'other Mars creature two +1 power counters.'
        )
        self.assertAttribute(
            cards['Eldest Batchminder'],
            'card_text_search',
            'Enhance Mars Enhance Mars. '
            '(These icons have already been added to cards in '
            'your deck.) <p> At the end of your turn, give each '
            'other Mars creature two +1 power counters.'
        )
