from dataclasses import dataclass
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card


@dataclass
@mmdc
class PlayerState:
    # CardColor
    cards: Dict[str, List[Card]]
    # TokenColor
    tokens: Dict[str, int]
    reserved_cards: List[Card]


@dataclass
@mmdc
class Player:
    id: str

    def __hash__(self):
        return hash(self.id)
