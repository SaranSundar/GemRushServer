from dataclasses import dataclass
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card
from card.noble import Noble
from enums.CardColor import CardColor
from enums.TokenColor import TokenColor


@mmdc
@dataclass
class PlayerState:
    cards: Dict[CardColor, List[Card]]
    tokens: Dict[TokenColor, int]
    reserved_cards: List[Card]
    nobles: List[Noble]

    @staticmethod
    def init_tokens():
        tokens: Dict[TokenColor, int] = {}
        for token_color in TokenColor:
            tokens[token_color] = 0
        return tokens

    def get_total_weight(self):
        points = 0
        # Sum up points of cards in each tier and nobles
        total_num_cards = 0
        for card_color in self.cards:
            tier_cards: List[Card] = self.cards[card_color]
            total_num_cards += len(tier_cards)
            points += sum(tier_card.points for tier_card in tier_cards)
        points += sum(noble.points for noble in self.nobles)

        return points, total_num_cards


@mmdc
@dataclass
class Player:
    id: str

    def __hash__(self):
        return hash(self.id)
