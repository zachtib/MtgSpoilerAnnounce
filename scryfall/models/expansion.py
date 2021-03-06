from dataclasses import dataclass


@dataclass
class Expansion:
    name: str
    code: str
    scryfall_id: str
    released_at: str
    set_type: str
