from typing import Dict

from marshmallow_dataclass import dataclass as mmdc

from card.color import CardColor


@mmdc
class Noble:
    points: int
    cost: Dict[CardColor, int]
