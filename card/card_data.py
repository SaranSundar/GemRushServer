from dataclasses import dataclass
from typing import Dict

from marshmallow_dataclass import dataclass as mmdc


# TODO: This was an enum, currently not being used
@mmdc
class Tier:
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'


@dataclass
@mmdc
class Card:
    points: int
    tier: str
    color: str
    cost: Dict[str, int]
