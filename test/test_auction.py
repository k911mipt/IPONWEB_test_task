import unittest
from src.auction import auction
from src.creative import Creative


class TestAuction(unittest.TestCase):
    def test_returning_form(self) -> None:
        creatives = [
            Creative(100, "1"),
            Creative(100, "2", "Russia"),
            Creative(100, "3", "Russia"),
            Creative(100, "4", "Russia"),
        ]
        number_winners = 2
        result = auction(creatives, number_winners)
        for entity in result:
            self.assertIsInstance(entity, Creative)
