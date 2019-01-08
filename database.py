from logging import Logger
from typing import List

from config import MtgSpoilerConfig

from sqlalchemy import create_engine, Column, String, Integer, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    expansion = Column(String(4), nullable=False)
    scryfall_id = Column(String(60), nullable=True)

    def __repr__(self):
        return f'<Card: {self.name}>'


class Expansion(Base):
    __tablename__ = 'expansions'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    code = Column(String(10), nullable=False)
    kind = Column(String(20), nullable=False)
    watched = Column(Boolean, default=False)
    release_date = Column(Date)
    scryfall_id = Column(String(60), nullable=True)

    def __repr__(self):
        return f'<Expansion: {self.name}>'


class Database:

    config: MtgSpoilerConfig
    logger: Logger

    def __init__(self, config: MtgSpoilerConfig, logger: Logger):
        self.config = config
        self.logger = logger
        engine = create_engine(config.db_uri)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def get_all_expansions(self) -> List[Expansion]:
        return self.session.query(Expansion).all()

    def get_watched_expansions(self) -> List[Expansion]:
        return self.session.query(Expansion).filter_by(watched=True).all()

    def get_cards_in_expansion(self, code) -> List[Card]:
        return self.session \
            .query(Card) \
            .filter_by(expansion=code) \
            .all()

    def watch_expansions(self, codes: List[str]):
        expansions = self.session.query(Expansion).filter(Expansion.code.in_(codes)).all()
        for e in expansions:
            e.watched = True
            self.session.add(e)
        self.session.commit()

    def create_cards(self, cards: List[Card]):
        for card in cards:
            self.session.add(card)
        self.session.commit()

    def insert_expansions(self, expansions: List[Expansion]):
        for e in expansions:
            self.session.add(e)
        self.session.commit()
