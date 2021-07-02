import unittest
import numpy as np

from src.auction import auction
from src.creative import Creative


class TestAuction(unittest.TestCase):
    def setup_class(cls):
        cls.small_test_set = [
            Creative(100, "1"),
            Creative(100, "2", "Russia"),
            Creative(100, "3", "Russia"),
            Creative(100, "4", "Russia"),
        ]
        cls.extended_test_set = [
            Creative(100, "1"),
            Creative(100, "2", "Russia"),
            Creative(100, "3", "Netherlands"),
            Creative(100, "4", "Canada"),
            Creative(110, "5"),
            Creative(110, "5", "Russia"),
            Creative(110, "4", "Netherlands"),
            Creative(110, "6", "Canada"),
            Creative(120, "1"),
            Creative(120, "3", "Russia"),
            Creative(120, "2", "Netherlands"),
            Creative(120, "4", "Canada"),
            Creative(130, "1"),
            Creative(130, "3", "Russia"),
            Creative(130, "4", "Netherlands"),
            Creative(130, "2", "Canada"),
            Creative(140, "1"),
            Creative(140, "4", "Russia"),
            Creative(140, "2", "Netherlands"),
            Creative(140, "3", "Canada"),
            Creative(150, "1"),
            Creative(150, "4", "Russia"),
            Creative(150, "3", "Netherlands"),
            Creative(150, "2", "Canada"),
        ]

    def setup_method(self, method):
        self.rng = np.random.default_rng(42)

    def test_form(self) -> None:
        result = auction(self.small_test_set, 2, rng=self.rng)
        for entity in result:
            self.assertIsInstance(entity, Creative)

    def test_number_winners(self) -> None:
        number_winners = 5
        result = auction(self.extended_test_set, number_winners, rng=self.rng)
        self.assertEqual(number_winners, len(result))

    def test_number_winners_not_exceeded(self):
        number_winners = 5
        result = auction(self.small_test_set, number_winners, rng=self.rng)
        self.assertGreater(number_winners, len(result))

    def test_winners_have_unique_id(self):
        result = auction(self.extended_test_set, 10, rng=self.rng)
        unique_ids = set(entity.advertiser_id for entity in result)
        self.assertEqual(len(result), len(unique_ids))

    def test_country_filter(self):
        country = "Russia"
        result = auction(
            self.extended_test_set, 10, country=country, rng=self.rng
        )
        for entity in result:
            self.assertTrue(entity.country is None or entity.country == country)

