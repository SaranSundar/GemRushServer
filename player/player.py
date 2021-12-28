from typing import List, Dict

from marshmallow_dataclass import dataclass

from card.card_data import Card


@dataclass
class PlayerState:
    cards: Dict[str, List[Card]]
    tokens: Dict[str, int]
    reserved_cards: List[Card]


@dataclass
class Player:
    id: str

    def __hash__(self):
        return hash(self.id)
