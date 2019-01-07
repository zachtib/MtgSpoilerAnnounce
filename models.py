from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Card:
    name: str
    image_url: str
    source_url: str

    mana_cost: str
    type_line: str
    oracle_text: str
    power: str
    toughness: str

    scryfall_id: str

    @classmethod
    def from_json(cls, json: dict) -> Card:
        try:
            return Card(
                name=json['name'], 
                image_url=json["image_uris"]["normal"],
                source_url=json["scryfall_uri"].split('?')[0],
                mana_cost=json['mana_cost'],
                type_line=json['type_line'],
                oracle_text=json.get('oracle_text', [face['oracle_text'] for face in json.get('card_faces', [])]),
                power=json.get('power', None),
                toughness=json.get('toughness', None),
                scryfall_id=json.get('scryfall_id', None)
            )
        except:
            print(f'Error parsing: ' + str(json))
            raise


    @property
    def power_toughness(self):
        if self.power is None and self.toughness is None:
            return ''
        else:
            return f'\n{self.power}/{self.toughness}'

@dataclass
class Expansion:
    name: str
    code: str

    @classmethod
    def from_json(cls, json: dict) -> Expansion:
        try:
            return Expansion(
                name=json['name'], 
                code=json['code']
            )
        except:
            print(f'Error parsing: ' + str(json))
            raise