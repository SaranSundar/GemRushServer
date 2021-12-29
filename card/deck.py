import json
import os
from dataclasses import dataclass, field
from random import shuffle
from typing import Dict, List

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Tier, Card
from card.noble import Noble
from enums.CardColor import CardColor
from enums.TokenColor import TokenColor


@dataclass
@mmdc
class Deck:
    tiered_cards: Dict[Tier, List[Card]]
    noble_cards: List[Noble]
    # Cards drawn from tiered_cards end up in board
    board: Dict[Tier, List[Card]] = field(default_factory=lambda: {})

    @staticmethod
    def load_card_data(filepath='./assets/deck-data.json'):
        print(os.getcwd())
        with open(filepath) as f:
            data = json.load(f)

        def _get_cost(cost_json: Dict) -> Dict[TokenColor, int]:
            colors = {
                TokenColor.WHITE,
                TokenColor.BLUE,
                TokenColor.GREEN,
                TokenColor.RED,
                TokenColor.BLACK,
            }

            cost_dict = dict()
            for color in colors:
                cost_dict[TokenColor(color)] = cost_json.get(color.value)

            return cost_dict

        tiered_cards_dict = {}
        for card_data in data['cards']:
            cost = _get_cost(card_data['cost'])
            card = Card(
                card_data['points'],
                Tier(card_data['tier']),
                CardColor(card_data['color']),
                cost=cost
            )
            if card.tier in tiered_cards_dict:
                tiered_cards_dict[card.tier].append(card)
            else:
                tiered_cards_dict[card.tier] = []
                tiered_cards_dict[card.tier].append(card)

        return tiered_cards_dict

    @staticmethod
    def load_nobles_data(filepath='./assets/nobles-data.json'):
        with open(filepath) as f:
            data = json.load(f)

        def _get_cost(cost_json: Dict) -> Dict[CardColor, int]:
            colors = {
                CardColor.WHITE,
                CardColor.BLUE,
                CardColor.GREEN,
                CardColor.RED,
                CardColor.BLACK,
            }

            cost_dict = dict()
            for color in colors:
                cost_dict[CardColor(color)] = cost_json.get(color.value)

            return cost_dict

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
        # Place card on board if tiered list is not empty
        if len(self.tiered_cards[tier]) > 0:
            if tier in self.board:
                self.board[tier].append(self.tiered_cards[tier].pop(0))
            else:
                self.board[tier] = []
                self.board[tier].append(self.tiered_cards[tier].pop(0))
