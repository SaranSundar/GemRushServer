from dataclasses import dataclass
from typing import List, Dict

from card.card_data import Card, CardColor, TokenColor


@dataclass
class PlayerState:
    cards: Dict[CardColor, List[Card]]
    tokens: Dict[TokenColor, int]
    reserved_cards: List[Card]


@dataclass
class Player:
    id: str
