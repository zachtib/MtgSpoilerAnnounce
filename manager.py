from datetime import date
from typing import List
from inspect import signature

from config import MtgSpoilerConfig
from database import Card as CardDbModel
from database import Database
from database import Expansion as ExpansionDbModel
from scryfall import ScryfallClient
from slackclient import SlackClient


class Manager:
    config: MtgSpoilerConfig
    db: Database
    api: ScryfallClient
    slack: SlackClient

    def __init__(self, config: MtgSpoilerConfig, db: Database,
                 api: ScryfallClient, slack: SlackClient):
        self.config = config
        self.db = db
        self.api = api
        self.slack = slack

    def handle(self, action: str, args: List[str], sets: bool = False):
        print(f'Running {action} {args}')
        try:
            callable = getattr(self, action)
            sig = signature(callable)
            print(sig)
            callable(args)
        except AttributeError as error:
            print(error)
            print(f'Unknown action: {action}')

    def watch_test(self, args):
        assert(self.config.debug)
        self.refresh_sets(args)
        self.watch_sets(('rna', ))
        results = self.db.get_watched_expansions()
        print(results)

    def api_test(self, args):
        assert(self.config.debug)
        cards = self.api.get_cards_from_set("rna")[0:5]
        for card in cards:
            print(card)
        print(self.api.test_mapping())

    def db_test(self, args):
        assert(self.config.debug)
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

    def refresh_sets(self, args):
        known_set_codes = [s.code for s in self.db.get_all_expansions()]
        api_sets = self.api.get_all_sets()
        new_sets = [s for s in api_sets if s.code not in known_set_codes]
        print(f'Found {len(new_sets)} new sets')
        exps = [ExpansionDbModel(
                    name=e.name,
                    code=e.code,
                    kind="",
                    watched=False,
                    release_date=date.today(),
                    scryfall_id=""
                ) for e in new_sets]
        self.db.insert_expansions(exps)

    def refresh(self, args):
        if 'sets' in args:
            self.refresh_sets()
        for expansion in self.db.get_watched_expansions():
            self.check_set_for_spoilers(expansion.code)

    def check_set_for_spoilers(self, code, post_to_slack=True):
        print(f'Refreshing {code}')
        all_cards = self.api.get_cards_from_set(code)
        previous_card_ids = [card.scryfall_id
                             for card in
                             self.db.get_cards_in_expansion(code)]
        new_cards = [card
                     for card in all_cards
                     if card.scryfall_id not in previous_card_ids]

        print(f'Found {len(new_cards)} new cards')

        if post_to_slack:
            self.slack.post_cards(new_cards)

        new_cards_db = [CardDbModel(
                name=card.name,
                expansion=code,
                scryfall_id=card.scryfall_id
            ) for card in new_cards]

        self.db.create_cards(new_cards_db)

    def show_watched(self, args):
        for expansion in self.db.get_watched_expansions():
            print(f'Watching {str(expansion)}')

    def init_db(self, args):
        self.refresh_sets(args)
        for code in args:
            self.check_set_for_spoilers(code, False)
