import dataclasses
import numpy as np

from typing import Dict, Generator, List, Optional

import src.creative as creative


Creative = creative.Creative
PriceType = creative.PriceType
IdType = creative.IdType
CountryType = creative.CountryType
IdCreativesMapType = Dict[IdType, List[Creative]]
PriceIdMapType = Dict[PriceType, List[IdType]]

RNG = np.random.default_rng(42)


def get_creatives_filtered_by_country(
    creatives: List[Creative], country: Optional[CountryType] = None,
) -> Generator[Creative, None, None]:
    if country is None:
        for entity in creatives:
            yield entity
    else:
        for entity in creatives:
            if entity.country is None or entity.country == country:
                yield entity


def get_unique_advertises_with_lowest_price(
    creatives: List[Creative], country: Optional[CountryType] = None,
) -> IdCreativesMapType:
    unique_creatives: IdCreativesMapType = {}
    for entity in get_creatives_filtered_by_country(creatives, country):
        existing_entities = unique_creatives.get(entity.advertiser_id)
        if existing_entities is None:
            unique_creatives[entity.advertiser_id] = [entity]
        else:
            existing_entity = existing_entities[0]
            if entity.price < existing_entity.price:
                unique_creatives[entity.advertiser_id] = [entity]
            elif entity.price == existing_entity.price:
                existing_entities.append(entity)

    return unique_creatives


def get_price_id_map(unique_creatives: IdCreativesMapType) -> PriceIdMapType:
    price_id_map: PriceIdMapType = {}
    for id, entity in unique_creatives.items():
        list_ids = price_id_map.get(entity[0].price)
        if list_ids is not None:
            list_ids.append(id)
        else:
            price_id_map[entity[0].price] = [id]

    return price_id_map


@dataclasses.dataclass
class Candidate:
    price: PriceType
    ids: List[IdType]


def get_candidates(price_id_map: PriceIdMapType,) -> List[Candidate]:
    return sorted(
        (Candidate(price, ids) for price, ids in price_id_map.items()),
        key=lambda candidate: candidate.price,
    )


def get_probabilities(list_ids, unique_creatives):
    # Calculate probabilities using number of id met in distribution
    total_weight = sum([len(unique_creatives[id]) for id in list_ids])
    probabilities = [len(unique_creatives[id]) / total_weight for id in list_ids]

    return probabilities


def pick_next_winners(
    candidate: Candidate,
    number_to_pick: int,
    unique_creatives: IdCreativesMapType,
    rng: np.random.Generator,
):
    list_ids = candidate.ids
    winner_ids: list[IdType]
    if len(list_ids) <= number_to_pick:
        winner_ids = list_ids
    else:
        # Pick ids equiprobable
        probabilities = get_probabilities(list_ids, unique_creatives)
        winner_ids = rng.choice(list_ids, number_to_pick, p=probabilities)

    return winner_ids


def get_winner_entities(
    candidates: List[Candidate],
    unique_creatives: IdCreativesMapType,
    number_winners: int,
    rng: np.random.Generator,
) -> List[Creative]:
    number_won = 0
    winner_entities = []
    for candidate in candidates:
        winner_ids = pick_next_winners(
            candidate, number_winners - number_won, unique_creatives, rng
        )
        for winner_id in winner_ids:
            list_winner_creatives = unique_creatives[winner_id]
            len_creatives = len(list_winner_creatives)
            assert len_creatives > 0
            # Each creative has an equal probability within same id group
            winner_index = rng.integers(0, len_creatives)
            winner_entities.append(list_winner_creatives[winner_index])
        number_won += len(winner_ids)
        if number_won >= number_winners:
            break

    return winner_entities


def auction(
    creatives: List[Creative],
    number_winners: int,
    country: Optional[CountryType] = None,
    rng: Optional[np.random.Generator] = None,
) -> List[Creative]:
    if rng is None:
        rng = RNG
    # Build a dict of unique advertiser creatives with lowest price
    unique_creatives = get_unique_advertises_with_lowest_price(creatives, country)
    # Build a dict of unique prices with id lists
    price_id_map = get_price_id_map(unique_creatives)
    # Build a list of winner candidates
    candidates = get_candidates(price_id_map)
    # Build final winner list
    winner_entities = get_winner_entities(
        candidates, unique_creatives, number_winners, rng
    )

    return winner_entities

