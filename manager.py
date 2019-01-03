
from database import Database
from scryfall import ScryfallClient

class SlackClient:
    pass

class Manager:
    db: Database
    api: ScryfallClient
    slack: SlackClient

    def __init__(self, db: Database, api: ScryfallClient, slack: SlackClient):
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
        pass