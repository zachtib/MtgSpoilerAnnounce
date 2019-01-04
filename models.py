from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Card:
    name: str
    image_url: str
    source_url: str

    @classmethod
    def from_json(cls, json: dict) -> Card:
        return Card(
            name=json['name'], 
            image_url=json["image_uris"]["normal"],
            source_url=json["scryfall_uri"].split('?')[0]
        )


@dataclass
class Set:
    name: str
    code: str