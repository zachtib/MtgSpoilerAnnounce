from typing import List

from .data_models import Card, Set

class Database:

    def get_all_sets(self) -> List[Set]:
        pass
    
    def get_watched_sets(self) -> List[Set]:
        pass

    def get_cards_in_set(self, code) -> List[Card]:
        pass
