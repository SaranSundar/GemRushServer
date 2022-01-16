from random import shuffle
from typing import Dict, List

from card.card_data import Card
from card.deck import Deck
from enums.Tier import Tier
from enums.TokenColor import TokenColor
from game.game_state import GameState
from json_requests.end_turn_request import EndTurnRequest, EndTurnRequestPayload
from player.player import PlayerState


class GameManager:

    @staticmethod
    def buy_card(game_state: GameState, end_turn_request: EndTurnRequest):
        # Player adds card to hand
        player_state: PlayerState = game_state.player_states[end_turn_request.player_id]
        bought_card: Card = end_turn_request.payload.bought_card
        player_state.cards[bought_card.color].append(bought_card)

        # Player returns tokens to bank to purchase card
        returned_tokens: List[TokenColor] = end_turn_request.payload.tokens_returned
        for token in returned_tokens:
            player_state.tokens[token] -= 1
            game_state.deck.bank[token] += 1

        # Deck draws new card to board
        deck: Deck = game_state.deck
        board: Dict[Tier, List[Card]] = deck.board
        tiered_cards_on_board: List[Card] = board[bought_card.tier]
        tiered_cards_on_board.remove(bought_card)
        deck.draw(bought_card.tier)

    @staticmethod
    def buy_gold_token_and_reserve_card(game_state: GameState, end_turn_request: EndTurnRequest):
        # Buy gold token
        player_state: PlayerState = game_state.player_states[end_turn_request.player_id]
        payload: EndTurnRequestPayload = end_turn_request.payload
        gold_token = payload.tokens_bought[0]
        player_state.tokens[gold_token] += 1
        # Remove 1 gold token from bank
        game_state.deck.bank[gold_token] -= 1
        # Reserve card
        player_state.reserved_cards.append(payload.reserved_card)

        # Deck draws new card to board
        deck: Deck = game_state.deck
        board: Dict[Tier, List[Card]] = deck.board
        tiered_cards_on_board: List[Card] = board[payload.reserved_card.tier]
        tiered_cards_on_board.remove(payload.reserved_card)
        deck.draw(payload.reserved_card.tier)

        # Check if over 10 tokens, if so return some tokens
        tokens_to_remove: List[TokenColor] = payload.tokens_returned
        for token_color in tokens_to_remove:
            player_state.tokens[token_color] -= 1
            # Add token to bank
            game_state.deck.bank[token_color] += 1

    @staticmethod
    def buy_reserved_card(game_state: GameState, end_turn_request: EndTurnRequest):
        # Player adds card to hand
        player_state: PlayerState = game_state.player_states[end_turn_request.player_id]
        bought_card: Card = end_turn_request.payload.bought_card
        player_state.cards[bought_card.color].append(bought_card)

        # Player returns tokens to bank to purchase card
        returned_tokens: List[TokenColor] = end_turn_request.payload.tokens_returned
        for token in returned_tokens:
            player_state.tokens[token] -= 1
            game_state.deck.bank[token] += 1

        # Remove bought card from players reserved cards
        player_state.reserved_cards.remove(end_turn_request.payload.bought_card)

    @staticmethod
    def buy_tokens(game_state: GameState, end_turn_request: EndTurnRequest):
        player_state: PlayerState = game_state.player_states[end_turn_request.player_id]
        payload: EndTurnRequestPayload = end_turn_request.payload

        # Buy tokens
        tokens_to_buy: List[TokenColor] = payload.tokens_bought
        for token_color in tokens_to_buy:
            player_state.tokens[token_color] += 1
            # Every token player buys needs to be removed from bank
            game_state.deck.bank[token_color] -= 1

        # Check if over 10 tokens, if so return some tokens
        tokens_to_remove: List[TokenColor] = payload.tokens_returned
        for token_color in tokens_to_remove:
            player_state.tokens[token_color] -= 1
            # Add token to bank
            game_state.deck.bank[token_color] += 1

    @staticmethod
    def buy_3_different_tokens(game_state: GameState, end_turn_request: EndTurnRequest):
        GameManager.buy_tokens(game_state, end_turn_request)

    @staticmethod
    def buy_2_same_tokens(game_state: GameState, end_turn_request: EndTurnRequest):
        GameManager.buy_tokens(game_state, end_turn_request)

    @staticmethod
    def buy_limited_tokens(game_state: GameState, end_turn_request: EndTurnRequest):
        GameManager.buy_tokens(game_state, end_turn_request)

    @staticmethod
    def discard_tokens(game_state: GameState, end_turn_request: EndTurnRequest):
        player_state: PlayerState = game_state.player_states[end_turn_request.player_id]
        random_keys = []
        for token_color in player_state.tokens:
            if player_state.tokens[token_color] > 0:
                random_keys.append(token_color)
        shuffle(random_keys)
        if len(random_keys) > 3:
            random_keys = random_keys[0:3]
        for key in random_keys:
            player_state.tokens[key] -= 1
