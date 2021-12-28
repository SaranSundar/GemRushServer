import json
from random import shuffle
from typing import Dict, List

from marshmallow_dataclass import dataclass

from card.card_data import Tier, Card
from card.color import CardColor, TokenColor
from card.noble import Noble


@dataclass
class Deck:
    tiered_cards: Dict[str, List[Card]]
    noble_cards: List[Noble]

    @staticmethod
    def load_card_data():
        with open('./assets/deck-data.json') as f:
            data = json.load(f)

        def _get_cost(cost_json: Dict) -> Dict[str, int]:
            colors = {
                TokenColor.WHITE,
                TokenColor.BLUE,
                TokenColor.GREEN,
                TokenColor.RED,
                TokenColor.BLACK,
            }

            cost = dict()
            for c in colors:
                cost[c] = cost_json.get(c)

            return cost

        tiered_cards_dict = {}
        for card_data in data['cards']:
            card = Card(
                card_data['points'],
                card_data['tier'],
                card_data['color'],
                _get_cost(card_data['cost'])
            )
            if card.tier in tiered_cards_dict:
                tiered_cards_dict[card.tier].append(card)
            else:
                tiered_cards_dict[card.tier] = []
                tiered_cards_dict[card.tier].append(card)

        return tiered_cards_dict

    @staticmethod
    def load_nobles_data():
        with open('./assets/nobles-data.json') as f:
            data = json.load(f)

        def _get_cost(cost_json: Dict) -> Dict[str, int]:
            colors = {
                CardColor.WHITE,
                CardColor.BLUE,
                CardColor.GREEN,
                CardColor.RED,
                CardColor.BLACK,
            }

            cost = dict()
            for c in colors:
                cost[c] = cost_json.get(c)

            return cost

        noble_cards_list = []
        for card_data in data['cards']:
            noble = Noble(
                card_data['points'],
                _get_cost(card_data['cost'])
            )
            noble_cards_list.append(noble)

        return noble_cards_list

    def shuffle(self):
        for tier, cards in self.tiered_cards.items():
            shuffle(cards)
        shuffle(self.noble_cards)

    def draw(self, tier: Tier):
        assert len(self.tiered_cards[tier]) != 0
        return self.tiered_cards[tier].pop(0)
