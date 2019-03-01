from logging import Logger
from typing import List

import requests

from config import MtgSpoilerConfig
from scryfall.converters import card_from_json, expansion_from_json
from scryfall.models import Card, Expansion

BASE_URL = 'https://api.scryfall.com'


class ScryfallClient:
    config: MtgSpoilerConfig
    logger: Logger

    def __init__(self, config: MtgSpoilerConfig, logger: Logger):
        self.config = config
        self.logger = logger

    def get_cards_from_set(self, code: str) -> List[Card]:
        r = requests.get(f'{BASE_URL}/cards/search?order=spoiled&q=e={code}&unique=prints')
        if r.status_code != 200:
            return []
        return [card_from_json(j) for j in r.json()['data']]

    def get_all_sets(self) -> List[Expansion]:
        r = requests.get(f'{BASE_URL}/sets')
        if r.status_code != 200:
            return []
        return [expansion_from_json(j) for j in r.json()['data']]

    def test_mapping(self) -> Card:
        assert self.config.debug
        cls_ = Card
        r = requests.get('https://api.scryfall.com/cards/named?fuzzy=aust+com')
        json = r.json()
        print(json)
        result = cls_()
        for key, value in json.items():
            if hasattr(result, key):
                setattr(result, key, value)
        return result
