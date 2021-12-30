from dataclasses import dataclass
from typing import Dict

from marshmallow_dataclass import dataclass as mmdc

from enums.CardColor import CardColor
from enums.Tier import Tier
from enums.TokenColor import TokenColor


@dataclass
@mmdc
class Card:
    points: int
    tier: Tier
    color: CardColor
    cost: Dict[TokenColor, int]

    def get_token_cost(self):
        tokens = 0
        for tier in self.cost:
            tokens += self.cost[tier]
        return tokens
