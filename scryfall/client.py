from typing import List

import requests
from models import Card, Set


class ScryfallClient:
    def get_cards_from_set(self, code: str) -> List[Card]:
        r = requests.get(f'https://api.scryfall.com/cards/search?order=spoiled&q=e={code}&unique=prints')
        if r.status_code != 200:
            return []
        json = r.json()
        results = []
        for card_json in json['data']:
            results.append(Card(
                name=card_json['name'], 
                image_url=card_json["image_uris"]["normal"]
            ))
        return results
    
    def get_all_sets(self) -> List[Set]:
        pass
