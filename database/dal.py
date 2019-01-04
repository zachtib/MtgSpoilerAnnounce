from typing import List

from .data_models import Card, Set

class Database:

    db_uri: str

    def __init__(self, db_uri):
        self.db_uri = db_uri

    def get_all_sets(self) -> List[Set]:
        return []
    
    def get_watched_sets(self) -> List[Set]:
        return []

    def get_cards_in_set(self, code) -> List[Card]:
        return []
