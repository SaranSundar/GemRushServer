from dataclasses import dataclass
from typing import List, Dict

from serde import serialize, deserialize

from card.card_data import Card, CardColor, TokenColor


@deserialize
@serialize
@dataclass
class PlayerState:
    cards: Dict[CardColor, List[Card]]
    tokens: Dict[TokenColor, int]


@deserialize
@serialize
@dataclass
class Player:
    id: str
