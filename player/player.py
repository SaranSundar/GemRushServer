from dataclasses import dataclass
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card
from card.noble import Noble
from enums.CardColor import CardColor
from enums.TokenColor import TokenColor


@mmdc
@dataclass
class PlayerState:
    cards: Dict[CardColor, List[Card]]
    tokens: Dict[TokenColor, int]
    reserved_cards: List[Card]
    nobles: List[Noble]


@mmdc
@dataclass
class Player:
    id: str

    def __hash__(self):
        return hash(self.id)
