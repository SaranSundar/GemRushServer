from dataclasses import dataclass
from typing import Dict

from card.card_data import CardColor


@dataclass
class Noble:
    points: int
    cost: Dict[CardColor, int]
