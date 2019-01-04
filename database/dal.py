from typing import List

from config import MtgSpoilerConfig
from .data_models import Card, Set

class Database:

    config: MtgSpoilerConfig

    def __init__(self, config: MtgSpoilerConfig):
        self.config = config

    def get_all_sets(self) -> List[Set]:
        return []
    
    def get_watched_sets(self) -> List[Set]:
        return []

    def get_cards_in_set(self, code) -> List[Card]:
        return []
