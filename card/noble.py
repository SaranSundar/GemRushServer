from dataclasses import dataclass
from typing import Dict

from serde import serialize, deserialize

from card.card_data import CardColor

@deserialize
@serialize
@dataclass
class Noble:
    points: int
    cost: Dict[CardColor, int]
