from dataclasses import dataclass
from enum import Enum
from typing import Dict

from marshmallow_dataclass import dataclass as mmdc

from card.color import TokenColor, CardColor


class Tier(str, Enum):
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    def __str__(self):
        return self.value


@dataclass
@mmdc
class Card:
    points: int
    tier: Tier
    color: CardColor
    cost: Dict[TokenColor, int]
