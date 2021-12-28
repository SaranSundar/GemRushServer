from typing import Dict

from marshmallow_dataclass import dataclass

from card.card_data import CardColor


@dataclass
class Noble:
    points: int
    cost: Dict[str, int]
