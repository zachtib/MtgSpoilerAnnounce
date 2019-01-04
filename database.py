from typing import List

from config import MtgSpoilerConfig
from dataclasses import dataclass

from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker


@dataclass
class Card:
    id: int
    name: str
    expansion: str


@dataclass
class Expansion:
    id: int
    name: str
    code: str
    kind: str
    watched: bool
    release_date: str


class Database:

    config: MtgSpoilerConfig

    def __init__(self, config: MtgSpoilerConfig):
        self.config = config
        self.engine = create_engine(config.db_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_all_sets(self) -> List[Set]:
        return []
    
    def get_watched_sets(self) -> List[Set]:
        return []

    def get_cards_in_set(self, code) -> List[Card]:
        return []
