
from dataclasses import dataclass

@dataclass
class Card:
    name: str
    image_url: str
    source_url: str


@dataclass
class Set:
    name: str
    code: str