from dataclasses import dataclass
from enum import Enum
from typing import Dict

from card.color import CardColor, TokenColor


@dataclass
class Tier(Enum):
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'


@dataclass
class Card:
    points: int
    tier: Tier
    color: CardColor
    cost: Dict[TokenColor, int]
