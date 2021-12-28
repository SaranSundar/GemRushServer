import json
import os
from collections import deque
from dataclasses import dataclass
from random import shuffle
from typing import Dict, List

from card.card_data import Tier, Card
from card.color import CardColor, TokenColor
from card.noble import Noble


@dataclass
class Deck:
    tiered_cards: Dict[Tier, List[Card]]

    def __init__(self):
        self.tiered_cards = {}
        self.noble_cards = []
        self._load_card_data()
        self._shuffle()

    def _load_card_data(self):
        print(os.getcwd())
        with open('./assets/deck-data.json') as f:
            data = json.load(f)

        def _get_cost(cost_json: Dict) -> Dict[TokenColor, int]:
            colors = {
                TokenColor.WHITE,
                TokenColor.BLUE,
                TokenColor.GREEN,
                TokenColor.RED,
                TokenColor.BLACK,
            }

            cost = dict()
            for c in colors:
                cost[c] = cost_json.get(c.value, 0)

            return cost

        for card_data in data['cards']:
            card = Card(
                card_data['points'],
                Tier(card_data['tier']),
                CardColor(card_data['color']),
                _get_cost(card_data['cost'])
            )
            self.tiered_cards.get(card.tier, deque()).append(card)

    def _load_nobles_data(self):
        with open('../assets/nobles-data.json') as f:
            data = json.load(f)

        def _get_cost(cost_json: Dict) -> Dict[CardColor, int]:
            colors = {
                TokenColor.WHITE,
                TokenColor.BLUE,
                TokenColor.GREEN,
                TokenColor.RED,
                TokenColor.BLACK,
            }

            cost = dict()
            for c in colors:
                cost[c] = cost_json.get(c.value, 0)

            return cost

        for card_data in data['cards']:
            noble = Noble(
                card_data['points'],
                _get_cost(card_data['cost'])
            )
            self.noble_cards.append(noble)

    def _shuffle(self):
        for tier, cards in self.tiered_cards:
            shuffle(cards)
        shuffle(self.noble_cards)

    def draw(self, tier: Tier):
        assert len(self.tiered_cards[tier]) != 0
        return self.tiered_cards[tier].pop(0)
