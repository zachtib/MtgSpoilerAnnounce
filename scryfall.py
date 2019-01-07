from typing import List

import requests
from models import Card, Expansion
from config import MtgSpoilerConfig


BASE_URL = 'https://api.scryfall.com'


class ScryfallClient:

    config: MtgSpoilerConfig

    def __init__(self, config: MtgSpoilerConfig):
        self.config = config

    def get_cards_from_set(self, code: str) -> List[Card]:
        r = requests.get(f'{BASE_URL}/cards/search?order=spoiled&q=e={code}&unique=prints')
        if r.status_code != 200:
            return []
        return [Card.from_json(j) for j in r.json()['data']]
    
    def get_all_sets(self) -> List[Expansion]:
        r = requests.get(f'{BASE_URL}/sets')
        if r.status_code != 200:
            return []
        return [Expansion.from_json(j) for j in r.json()['data']]
    
    
