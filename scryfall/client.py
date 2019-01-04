from typing import List

import requests
from models import Card, Set


class ScryfallClient:
    def get_cards_from_set(self, code: str) -> List[Card]:
        r = requests.get(f'https://api.scryfall.com/cards/search?order=spoiled&q=e={code}&unique=prints')
        if r.status_code != 200:
            return []
        return [Card.from_json(j) for j in r.json()['data']]
    
    def get_all_sets(self) -> List[Set]:
        pass
