from dataclasses import dataclass
from enum import Enum
from typing import Dict

from serde import serialize, deserialize

from card.color import CardColor, TokenColor


@dataclass
@deserialize
@serialize
class Tier(Enum):
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

@deserialize
@serialize
@dataclass
class Card:
    points: int
    tier: Tier
    color: CardColor
    cost: Dict[TokenColor, int]
