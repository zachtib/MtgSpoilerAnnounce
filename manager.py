from config import MtgSpoilerConfig
from database import Database
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


    def watch_sets(self, codes):
        print(f'Watching  {codes}')


    def unwatch_sets(self, codes):
        print(f'Unwatching  {codes}')


    def refresh_sets(self): 
        known_sets = db.get_all_sets()
        known_set_codes = [ s.code for s in known_sets ]
        api_sets = api.get_all_sets()
        new_sets = list(filter(lambda x: x.code not in known_set_codes, api_sets))


    def check_for_spoilers(self):
        for set_ in self.db.get_watched_sets():
            self.check_set_for_spoilers(set_.code)

    def check_set_for_spoilers(self, code):
        all_cards = self.api.get_cards_from_set(code)
        previous_cards = self.db.get_cards_from_set(code)
        previous_card_names = [card.name for card in previous_cards]
        new_cards = list(filter(lambda card: card.name in previous_card_names, all_cards))
        
        self.slack.post_cards(new_cards)
