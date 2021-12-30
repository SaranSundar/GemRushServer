from typing import Dict, List

from card.card_data import Card
from card.deck import Deck
from enums.EndTurnAction import EndTurnAction
from enums.TokenColor import TokenColor
from player.player import PlayerState
import json

"""Utility method to get all valid moves given a game state.

For move format, temporarily using
    "action": "Buying3DifferentTokens",
    "payload": {
        "bought_noble": None,
        "bought_card": None,
        "reserved_card": None,
        "tokens_returned": [],
        "tokens_bought": [
            "RED",
            "BLUE",
            "GREEN"
        ]
    }
    
TODO: refactor to a Move data class

Valid moves currently supported:
    BuyingCard
    BuyingGoldToken
    Buying3DifferentTokens
    Buying2SameTokens
    BuyingLimitedTokens
"""

MAX_TOKEN_COUNT = 10
MOVE_JSON_TEMPLATE = '''
"action": "",
"payload": {
    "bought_noble": "",
    "bought_card": "",
    "reserved_card": "",
    "tokens_returned": [],
    "tokens_bought": []
}
'''


def get_valid_moves(deck: Deck, player_state: PlayerState) -> List[Dict]:
    valid_moves = []
    valid_moves.extend(_get_buy_card_moves(deck, player_state))
    # TODO: implement
    # valid_moves.extend(_get_buy_gold_card_moves(deck, player_state))
    # valid_moves.extend(_get_buy_3_tokens_moves(deck, player_state))
    # valid_moves.extend(_get_buy_2_same_tokens_moves(deck, player_state))
    # valid_moves.extend(_get_buy_limited_tokens_moves(deck, player_state))

    return valid_moves


def _get_buy_card_moves(deck: Deck, player_state: PlayerState) -> List[Dict]:
    player_tokens = player_state.tokens
    all_cards = []
    for _, cards in deck.board:
        all_cards.extend(cards)
    buyable_cards = list(filter(lambda card: _can_buy_card(player_tokens, card), all_cards))

    moves = []
    for card in buyable_cards:
        move_json = json.loads(MOVE_JSON_TEMPLATE)
        move_json['action'] = EndTurnAction.BuyingCard.name
        move_json['bought_card'] = card.Schema().dumps(card)
        moves.append(move_json)

    # TODO: implement buy nobles

    return moves


def _can_buy_card(player_tokens: Dict[TokenColor, int], card: Card) -> bool:
    lacking = 0
    for t, c in card.cost:
        lacking += max(0, c - player_tokens[t])
        if lacking > player_tokens[TokenColor.GOLD]:
            return False
    return True
