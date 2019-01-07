from typing import List

from config import MtgSpoilerConfig
from database import Database, Card as CardDbModel, Expansion as ExpansionDbModel
from scryfall import ScryfallClient
from slackclient import SlackClient

class Manager:
    config: MtgSpoilerConfig
    db: Database
    api: ScryfallClient
    slack: SlackClient

    def __init__(self, config: MtgSpoilerConfig, db: Database, api: ScryfallClient, slack: SlackClient):
        self.config = config
        self.db = db
        self.api = api
        self.slack = slack
    

    def handle(self, action: str, args: List[str], sets: bool = False):
        print(f'Running {action} {args}')
        if action == 'watch':
            pass
        elif action == 'unwatch':
            pass
        elif action == 'refresh':
            pass
        elif action == 'db_test':
            self.db_test()
        elif action == 'api_test':
            self.api_test()
        else:
            print(f'Unknown action: {action}')

    def api_test(self):
        assert(self.config.debug)
        cards = self.api.get_cards_from_set("rna")[0:5]
        for card in cards:
            print(card)

    def db_test(self):
        assert(self.config.debug)
        self.db.create_cards([
            CardDbModel(name="abcde", expansion="test"),
            CardDbModel(name="fghij", expansion="test")
        ])
        cards = self.db.get_cards_in_expansion("test")
        print(cards)

    def watch_sets(self, codes):
        print(f'Watching  {codes}')


    def unwatch_sets(self, codes):
        print(f'Unwatching  {codes}')


    def refresh_sets(self): 
        known_set_codes = [ s.code for s in self.db.get_all_sets() ]
        api_sets = self.api.get_all_sets()
        new_sets = [s for s in api_sets if s.code not in known_set_codes]


    def check_for_spoilers(self):
        for set_ in self.db.get_watched_sets():
            self.check_set_for_spoilers(set_.code)

    def check_set_for_spoilers(self, code):
        all_cards = self.api.get_cards_from_set(code)
        previous_card_names = [card.name for card in self.db.get_cards_from_set(code)]
        new_cards = [card for card in all_cards if card.name not in previous_card_names]
        
        self.slack.post_cards(new_cards)
