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

    @property
    def power_toughness(self):
        if self.power is None and self.toughness is None:
            return ''
        else:
            return f'\n{self.power}/{self.toughness}'
