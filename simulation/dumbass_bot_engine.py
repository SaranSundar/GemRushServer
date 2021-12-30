import heapq
from typing import Dict, List

from card.card_data import Card
from card.noble import Noble
from enums.Tier import Tier
from enums.TokenColor import TokenColor
from game.game_state import GameState
from player.player import PlayerState
from room.room import Room

"""Unfinished dumbass engine made by our very own Saran S.

If your purpose isn't to embarass yourself with the use of this bot, avoid.
"""


class DumbassBotEngine:
    def _calc_weight_of_all_cards(self, game_state: GameState, player_id: str):
        # points of card
        # cost of card, number of tokens needed
        # does card color get closer to noble
        # tokens bank has
        player_state: PlayerState = game_state.player_states[player_id]
        # colors needed for nobles
        # colors needed for more expensive cards on board
        # Cost to buy card, points card offers when bought, does card get you closer to noble
        pq = []
        deck = game_state.deck
        board: Dict[Tier, List[Card]] = deck.board
        for tier in board:
            tier_cards = board[tier]
            for card in tier_cards:
                heapq.heappush(pq, self._calc_weight_of_card(player_state, card, deck.bank, deck.noble_cards))
        return pq

    def _calc_weight_of_card(self, player_state: PlayerState, card: Card, bank: Dict[TokenColor, int],
                             nobles: List[Noble]):
        card_points = card.points
        # Calculate token cost for card and what tokens bank has
        needed_tokens_that_are_in_bank: int = 0
        card_token_cost = 0
        for token_color in card.cost:
            discount = player_state.calculate_permanent_token_discount(token_color)
            if discount >= card.cost[token_color]:
                # Requires no tokens of this color
                pass
            else:
                # Requires number of tokens minus number of cards of that color
                needed_tokens = card.cost[token_color] - discount
                card_token_cost += needed_tokens
                if token_color in bank:
                    # Add if bank has an available token of the color that is needed
                    needed_tokens_that_are_in_bank += 1

        # Check if card gets you closer to a noble
        closer_to_noble = False
        for noble in nobles:
            if card.color in noble.cost:
                closer_to_noble = True
                break

        return card_points - card_token_cost - needed_tokens_that_are_in_bank + closer_to_noble

    def take_turn(self, room: Room, player_id: str, game_state: GameState) -> Dict:
        pq = self._calc_weight_of_all_cards(game_state, player_id)
        return dict()
