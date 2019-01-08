from logging import Logger
from typing import List

import requests
from models import Card, Expansion
from config import MtgSpoilerConfig


BASE_URL = 'https://api.scryfall.com'


def card_from_json(json: dict) -> Card:
    try:
        oracle_text = json.get('oracle_text', None)
        if oracle_text is None:
            if 'card_faces' in json.keys():
                faces = json['card_faces']
                faces_text = [face['oracle_text'] for face in faces]
                oracle_text = '\n//\n'.join(faces_text)
            else:
                oracle_text = 'Error parsing oracle text'
        return Card(
            name=json['name'],
            image_url=json["image_uris"]["normal"],
            source_url=json["scryfall_uri"].split('?')[0],
            mana_cost=json['mana_cost'],
            type_line=json['type_line'],
            oracle_text=oracle_text,
            power=json.get('power', None),
            toughness=json.get('toughness', None),
            scryfall_id=json['id']
        )
    except KeyError as error:
        print(f'Error parsing: ' + str(json))
        print(error)
        raise


def expansion_from_json(json: dict) -> Expansion:
    try:
        return Expansion(
            name=json['name'],
            code=json['code'],
            scryfall_id=json['id']
        )
    except KeyError as error:
        print(f'Error parsing: ' + str(json))
        print(error)
        raise


class ScryfallClient:

    config: MtgSpoilerConfig
    logger: Logger

    def __init__(self, config: MtgSpoilerConfig, logger: Logger):
        self.config = config
        self.logger = logger

    def get_cards_from_set(self, code: str) -> List[Card]:
        r = requests.get(f'{BASE_URL}/cards/search?order=spoiled&q=e={code}&unique=prints')
        if r.status_code != 200:
            return []
        return [card_from_json(j) for j in r.json()['data']]

    def get_all_sets(self) -> List[Expansion]:
        r = requests.get(f'{BASE_URL}/sets')
        if r.status_code != 200:
            return []
        return [expansion_from_json(j) for j in r.json()['data']]

    def test_mapping(self) -> Card:
        assert self.config.debug
        cls_ = Card
        r = requests.get('https://api.scryfall.com/cards/named?fuzzy=aust+com')
        json = r.json()
        print(json)
        result = cls_()
        for key, value in json.items():
            if hasattr(result, key):
                setattr(result, key, value)
        return result
