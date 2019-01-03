from typing import List

from scryfall.models import Card, Set

class ScryfallClient:
    def get_cards_from_set(self, code: str) -> List[Card]:
        pass
    
    def get_all_sets(self) -> List[Set]:
        pass