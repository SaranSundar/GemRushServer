from dataclasses import dataclass
from typing import Dict

from marshmallow_dataclass import dataclass as mmdc

from enums.CardColor import CardColor


@mmdc
@dataclass
class Noble:
    points: int
    cost: Dict[CardColor, int]
