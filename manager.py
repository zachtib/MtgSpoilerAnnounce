from datetime import date, datetime
from inspect import signature
from logging import Logger
from typing import List

from config import MtgSpoilerConfig
from database import Database
from database.models import Card as CardDbModel
from database.models import Expansion as ExpansionDbModel
from scryfall import ScryfallClient
from slackclient import SlackClient


class Manager:
    config: MtgSpoilerConfig
    db: Database
    api: ScryfallClient
    slack: SlackClient
    logger: Logger

    def __init__(self, config: MtgSpoilerConfig, db: Database, api: ScryfallClient, slack: SlackClient, logger: Logger):
        self.config = config
        self.db = db
        self.api = api
        self.slack = slack
        self.logger = logger

    def handle(self, action: str, args: List[str]):
        try:
            func = getattr(self, action)
            sig = signature(func)
            p = len(sig.parameters)
            if p == 0:
                self.logger.debug(f'Running {action}')
                func()
            elif p == 1:
                self.logger.debug(f'Running {action} {args}')
                func(args)
        except AttributeError as error:
            print(error)

    def watch_test(self, args):
        assert self.config.debug
        self.refresh_sets()
        self.watch(('rna', ))
        results = self.db.get_watched_expansions()
        print(results)

    def api_test(self):
        assert self.config.debug
        cards = self.api.get_cards_from_set("rna")[0:5]
        for card in cards:
            print(card)
        print(self.api.test_mapping())

    def db_test(self):
        assert self.config.debug
        self.db.create_cards([
            CardDbModel(name="abcde", expansion="test"),
            CardDbModel(name="fghij", expansion="test")
        ])
        cards = self.db.get_cards_in_expansion("test")
        print(cards)

    def watch(self, codes):
        print(f'Watching  {codes}')
        self.db.watch_expansions(codes)

    def unwatch(self, codes):
        print(f'Unwatching  {codes}')
        self.db.unwatch_expansions(codes)

    def refresh_sets(self):
        self.db.unwatch_released_expansions()
        known_set_codes = [s.code for s in self.db.get_all_expansions()]
        api_sets = self.api.get_all_sets()
        new_sets = [s for s in api_sets if s.code not in known_set_codes]
        print(f'Found {len(new_sets)} new sets')
        exps = []
        for e in new_sets:
            self.slack.post_message(f'Found new set: {e.name}')
            released_at = datetime.strptime(e.released_at, '%Y-%m-%d').date()
            new_set = ExpansionDbModel(
                    name=e.name,
                    code=e.code,
                    kind="",
                    watched=True,
                    release_date=released_at,
                    scryfall_id=e.scryfall_id
                )
            exps.append(new_set)

        self.db.insert_expansions(exps)

    def refresh(self, args):
        if 'sets' in args:
            self.refresh_sets()
        for expansion in self.db.get_watched_expansions():
            self.check_set_for_spoilers(expansion.code)

    def check_set_for_spoilers(self, code, post_to_slack=True):
        print(f'Refreshing {code}')
        all_cards = self.api.get_cards_from_set(code)
        print(f'API returned {len(all_cards)} cards for {code}')
        previous_card_ids = [card.scryfall_id
                             for card in
                             self.db.get_cards_in_expansion(code)]

        if None in previous_card_ids:
            print('None is stored as a scryfall_id!')

        new_cards = [card
                     for card in all_cards
                     if card.scryfall_id not in previous_card_ids]

        print(f'Found {len(new_cards)} new cards')

        if post_to_slack:
            new_cards = self.slack.post_cards(new_cards)
        else:
            print('Skipping post to slack')

        new_cards_db = [CardDbModel(
                name=card.name,
                expansion=code,
                scryfall_id=card.scryfall_id
            ) for card in new_cards]

        self.db.create_cards(new_cards_db)

    def show_watched(self):
        for expansion in self.db.get_watched_expansions():
            print(f'Watching {str(expansion)}')
    
    def show_cards(self, args):
        for card in self.db.get_cards_in_expansion(args[0]):
            print(card)

    def init_db(self, args):
        self.refresh_sets()
        self.watch(args)
        for code in args:
            self.check_set_for_spoilers(code, False)
