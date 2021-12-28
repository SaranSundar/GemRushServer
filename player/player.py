from typing import List, Dict

from marshmallow_dataclass import dataclass

from card.card_data import Card, CardColor, TokenColor


@dataclass
class PlayerState:
    cards: Dict[CardColor, List[Card]]
    tokens: Dict[TokenColor, int]
    reserved_cards: List[Card]


@dataclass(eq=True, frozen=True)
class Player:
    id: str

    def __hash__(self):
        return hash(self.id)
