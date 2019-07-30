from datetime import datetime
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
            self.logger.error(error)

    def watch_test(self, args):
        assert self.config.debug
        self.refresh_sets()
        self.watch(('rna', ))
        results = self.db.get_watched_expansions()
        self.logger.debug(results)

    def api_test(self):
        assert self.config.debug
        cards = self.api.get_cards_from_set("rna")[0:5]
        for card in cards:
            self.logger.debug(card)
        self.logger.debug(self.api.test_mapping())

    def db_test(self):
        assert self.config.debug
        self.db.create_cards([
            CardDbModel(name="abcde", expansion="test"),
            CardDbModel(name="fghij", expansion="test")
        ])
        cards = self.db.get_cards_in_expansion("test")
        self.logger.debug(cards)

    def watch(self, codes):
        self.logger.debug(f'Watching  {codes}')
        self.db.watch_expansions(codes)

    def unwatch(self, codes):
        self.logger.debug(f'Unwatching  {codes}')
        self.db.unwatch_expansions(codes)

    def force_refresh_sets(self):
        existing_sets = self.db.get_all_expansions()
        api_sets = self.api.get_all_sets()

        to_update = []
        for expansion in existing_sets:
            filtered = list(filter(lambda e: e.scryfall_id == expansion.scryfall_id, api_sets))
            if len(filtered) == 1:
                api_set = filtered[0]
                expansion.name = api_set.name
                expansion.release_date = api_set.released_at
                expansion.code = api_set.code
                expansion.kind = api_set.set_type
                to_update.append(expansion)
            else:
                self.logger.debug(f'Could not match: {expansion.name}')
        self.db.insert_expansions(to_update)

    def refresh_sets(self):
        self.db.unwatch_released_expansions()
        known_set_codes = [s.code for s in self.db.get_all_expansions()]
        api_sets = self.api.get_all_sets()

        def is_set_new(s):
            if s.code in known_set_codes:
                return False
            dt = datetime.strptime(s.released_at, '%Y-%m-%d')
            if dt < datetime.now():
                return False
            return True

        new_sets = [s for s in api_sets if is_set_new(s)]

        self.logger.debug(f'Found {len(new_sets)} new sets')
        exps = []
        for e in new_sets:
            released_at = datetime.strptime(e.released_at, '%Y-%m-%d').date()
            should_watch = released_at > datetime.now()
            if should_watch:
                self.slack.post_message(f'Found new set: {e.name}')
            new_set = ExpansionDbModel(
                    name=e.name,
                    code=e.code,
                    kind=e.set_type,
                    watched=should_watch,
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
        self.logger.debug(f'Refreshing {code}')
        all_cards = self.api.get_cards_from_set(code)
        self.logger.debug(f'API returned {len(all_cards)} cards for {code}')

        cards_in_expansion = self.db.get_cards_in_expansion(code)

        old_names = [card.name for card in cards_in_expansion]
        old_ids = [card.scryfall_id for card in cards_in_expansion]

        if None in old_ids:
            self.logger.debug('None is stored as a scryfall_id!')

        def is_card_new(card):
            if card.name in old_names:
                return False
            if card.scryfall_id in old_ids:
                return False
            return True

        new_cards = list(filter(is_card_new, all_cards))

        self.logger.debug(f'Found {len(new_cards)} new cards')

        if post_to_slack:
            new_cards = self.slack.post_cards(new_cards)
        else:
            self.logger.debug('Skipping post to slack')

        new_cards_db = [CardDbModel(
                name=card.name,
                expansion=code,
                scryfall_id=card.scryfall_id
            ) for card in new_cards]

        self.db.create_cards(new_cards_db)

    def show_watched(self):
        for expansion in self.db.get_watched_expansions():
            self.logger.debug(f'Watching {str(expansion)}')
    
    def show_cards(self, args):
        for card in self.db.get_cards_in_expansion(args[0]):
            self.logger.debug(card)

    def init_db(self, args):
        self.refresh_sets()
        self.watch(args)
        for code in args:
            self.check_set_for_spoilers(code, False)
