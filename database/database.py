from datetime import date
from logging import Logger
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import MtgSpoilerConfig
from database.models import Expansion, Card, Base


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
            self.logger.debug(f'Watching {e.name}')
            e.watched = True
            self.session.add(e)
        self.session.commit()

    def unwatch_expansions(self, codes: List[str]):
        expansions = self.session.query(Expansion).filter(Expansion.code.in_(codes)).all()
        for e in expansions:
            self.logger.debug(f'Unwatching {e.name}')
            e.watched = False
            self.session.add(e)
        self.session.commit()

    def unwatch_released_expansions(self):
        expansions = self.session.query(Expansion).filter(Expansion.release_date < date.today())
        for e in expansions:
            self.logger.debug(f'Unwatching {e.name}')
            e.watched = False
            self.session.add(e)
        self.session.commit()

    def create_cards(self, cards: List[Card]):
        self.logger.debug(f'Saving {len(cards)} new cards to the database')
        for card in cards:
            self.session.add(card)
        self.session.commit()

    def insert_expansions(self, expansions: List[Expansion]):
        for e in expansions:
            self.session.add(e)
        self.session.commit()
