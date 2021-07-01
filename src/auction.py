from typing import Dict, Generator, List, Optional, Tuple

import src.creative as creative

import operator
import random


Creative = creative.Creative
PriceType = creative.PriceType
IdType = creative.IdType
CountryType = creative.CountryType
IdCreativesMapType = Dict[IdType, List[Creative]]
PriceIdMapType = Dict[PriceType, List[IdType]]


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
        list_of_ids = price_id_map.get(entity[0].price)
        if list_of_ids is not None:
            list_of_ids.append(id)
        else:
            price_id_map[entity[0].price] = [id]
    return price_id_map


def get_candidates(
    price_id_map: PriceIdMapType,
) -> List[tuple[PriceType, List[IdType]]]:
    return sorted(
        ((price, list_of_ids) for price, list_of_ids in price_id_map.items()),
        key=operator.itemgetter(0),
    )


def get_weighted_candidates(
    candidates: List[tuple[PriceType, List[IdType]]],
    unique_creatives: IdCreativesMapType,
) -> List[dict]:
    weighted_candidates = []
    for price, list_of_ids in candidates:
        accumulated_weight = 0
        list_weighted_ids = []
        for id in list_of_ids:
            weight = len(unique_creatives[id])
            accumulated_weight += weight
            list_weighted_ids.append(
                {"id": id, "win_treshold": accumulated_weight}
            )
        weighted_candidates.append(
            {
                "price": price,
                "total_weight": accumulated_weight,
                "list_weighted_ids": list_weighted_ids,
            }
        )
    return weighted_candidates


def pick_next_winner(weighted_candidates, price_index):
    item = weighted_candidates[price_index]
    list_weighted_ids = item["list_weighted_ids"]
    if len(list_weighted_ids) == 1:
        price_index += 1
        winner_id = list_weighted_ids[0]["id"]
    else:
        total_weight = list_weighted_ids[-1]["win_treshold"]
        winner_weight = random.randint(0, total_weight - 1)
        winner_item = None
        for item in list_weighted_ids:
            if item["win_treshold"] > winner_weight:
                winner_item = item
                break
        assert winner_item is not None
        winner_id = winner_item["id"]
        list_weighted_ids.remove(winner_item)
    return winner_id, price_index


def get_winner_entities(weighted_candidates, unique_creatives, number_winners):
    price_index = 0
    number_won = 0
    winner_entities = []
    while number_won < number_winners and price_index < len(weighted_candidates):
        winner_id, price_index = pick_next_winner(
            weighted_candidates, price_index
        )
        list_winner_creatives = unique_creatives[winner_id]
        len_creatives = len(list_winner_creatives)
        winner_index = (
            random.randint(0, len_creatives - 1) if len_creatives > 1 else 0
        )
        winner_entities.append(list_winner_creatives[winner_index])
        number_won += 1
    return winner_entities


def auction(
    creatives: List[Creative],
    number_winners: int,
    country: Optional[CountryType] = None,
    seed: Optional[int] = None,
):
    if seed is not None:
        random.seed(seed)
    # Build a dict of unique advertiser creatives with lowest price
    unique_creatives = get_unique_advertises_with_lowest_price(creatives, country)
    # Build a dict of unique prices with id lists
    price_id_map = get_price_id_map(unique_creatives)
    # Build a list of winner candidates
    candidates = get_candidates(price_id_map)
    # Calculate weights of multiple ids with same price
    weighted_candidates = get_weighted_candidates(candidates, unique_creatives)
    # Build final winner list
    winner_entities = get_winner_entities(
        weighted_candidates, unique_creatives, number_winners
    )

    return winner_entities

