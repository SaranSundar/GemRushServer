from dataclasses import dataclass
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card
from card.color import CardColor, TokenColor


@dataclass
@mmdc
class PlayerState:
    # CardColor
    cards: Dict[CardColor, List[Card]]
    # TokenColor
    tokens: Dict[TokenColor, int]
    reserved_cards: List[Card]


@dataclass
@mmdc
class Player:
    id: str

    def __hash__(self):
        return hash(self.id)
