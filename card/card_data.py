from enum import Enum
from typing import Dict

from marshmallow_dataclass import dataclass

from card.color import CardColor, TokenColor


# TODO: This was an enum, currently not being used
@dataclass
class Tier:
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'


@dataclass
class Card:
    points: int
    tier: str
    color: str
    cost: Dict[str, int]
