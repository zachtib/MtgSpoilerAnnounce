from typing import List

from config import MtgSpoilerConfig
from dataclasses import dataclass

from sqlalchemy import create_engine, Column, String, Integer, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    expansion = Column(String(3), nullable=False)
    scryfall_id = Column(String(60), nullable=True)

    def __repr__(self):
        return f'<Card {self.name}>'


class Expansion(Base):
    __tablename__ = 'expansions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    code = Column(String(4), nullable=False)
    kind = Column(String(20), nullable=False)
    watched = Column(Boolean, default=False)
    release_date = Column(Date)
    scryfall_id = Column(String(60), nullable=True)

    def __repr__(self):
        return f'<Expansion {self.name}>'

class Database:

    config: MtgSpoilerConfig

    def __init__(self, config: MtgSpoilerConfig):
        self.config = config
        engine = create_engine(config.db_uri)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def get_all_expansions(self) -> List[Expansion]:
        return []
    
    def get_watched_expansions(self) -> List[Expansion]:
        return []

    def get_cards_in_expansion(self, code) -> List[Card]:
        return self.session \
            .query(Card) \
            .filter_by(expansion=code) \
            .all()
    
    def watch_expansions(self, codes: List[str]):
        pass

    def create_cards(self, cards: List[Card]):
        for card in cards:
            self.session.add(card)
        self.session.commit()