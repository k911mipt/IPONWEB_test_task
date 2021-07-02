import collections
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
        cls.equiprobability_test_set = [
            Creative(100, "0"),
            Creative(100, "0", "Russia"),
            Creative(100, "0", "Canada"),
            Creative(100, "0", "Netherlands"),
            Creative(100, "0", "USA"),
            Creative(100, "1"),
            Creative(100, "1", "Russia"),
            Creative(100, "1", "Canada"),
            Creative(100, "1", "Netherlands"),
            Creative(100, "2"),
            Creative(100, "2", "Russia"),
            Creative(100, "2", "Canada"),
            Creative(100, "3", "Canada"),
            Creative(100, "3", "Netherlands"),
            Creative(100, "4", "Russia"),
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
        self._test_unique_id(self.extended_test_set, 10)
        self._test_unique_id(self.equiprobability_test_set, 3)

    def test_country_filter(self):
        country = "Russia"
        result = auction(
            self.extended_test_set, 10, country=country, rng=self.rng
        )
        for entity in result:
            self.assertTrue(entity.country is None or entity.country == country)

    def test_equaprobability_over_different_id(self):
        creatives = self.equiprobability_test_set
        source_total_objects = len(creatives)
        source_counter = collections.Counter(
            (entity.advertiser_id for entity in creatives)
        )
        source_probabilities = {
            id: value / source_total_objects
            for id, value in source_counter.items()
        }
        number_winners = 4

        self.assertLess(
            number_winners,
            len(source_counter),
            "If number winners is equal or greater than number of unique ids, test would be incorrect",
        )

        number_samples = 100000
        counter = collections.Counter()
        for _ in range(number_samples):
            result = auction(creatives, number_winners, rng=self.rng)
            for entity in result:
                counter.update(entity.advertiser_id)
        result_total_objects = sum(counter.values())
        result_probabilities = {
            id: value / result_total_objects for id, value in counter.items()
        }
        for key, value in result_probabilities.items():
            v1 = float(value)
            v2 = float(source_probabilities[key])
            # TODO read an arcticle about confidence interval and provide a better formula for `delta`
            delta = 30 / np.sqrt(number_samples)
            self.assertAlmostEqual(v1, v2, delta=delta)

    def _test_unique_id(self, test_set, number_winners):
        result = auction(test_set, number_winners, rng=self.rng)
        unique_ids = set(entity.advertiser_id for entity in result)
        self.assertEqual(len(result), len(unique_ids))
