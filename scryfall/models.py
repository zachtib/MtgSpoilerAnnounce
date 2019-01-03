
from dataclasses import dataclass

@dataclass
class Card:
    name: str


@dataclass
class Set:
    name: str
    code: str