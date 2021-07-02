from src.auction import auction
from src.creative import Creative
import numpy as np

from pprint import pprint


def sample_run() -> None:
    creatives = [
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
    number_winners = 3
    rng = np.random.default_rng(42)
    result = auction(creatives, number_winners, None, rng)
    pprint(result)

sample_run()
