import json
from dataclasses import dataclass
from datetime import datetime

import requests
from marshmallow_dataclass import dataclass as mmdc

from card.deck import Deck
from enums.EndTurnAction import EndTurnAction
from enums.TokenColor import TokenColor
from game.game_state import GameState
from json_requests.end_turn_request import EndTurnRequest, EndTurnRequestPayload
from player.player import Player
from room.room import Room
from utils.utils import generate_uid


@dataclass
@mmdc
@dataclass
class RequestMethods:
    POST = "POST"
    GET = "GET"


def get_response(method, url, body):
    payload = json.dumps(body)
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request(method, url, headers=headers, data=payload)


def test_generating_game_state_json():
    deck = Deck(
        tiered_cards=Deck.load_card_data('.././assets/deck-data.json'),
        noble_cards=Deck.load_nobles_data('.././assets/nobles-data.json'),
        tokens=Deck.load_tokens()
    )
    time_game_started = datetime.utcnow()
    deck.create_board()
    game_state = GameState(
        id=generate_uid(),
        player_states={},
        deck=deck,
        turn_number=0,
        turn_order=[Player(generate_uid())],
        time_game_started=time_game_started,
        time_last_move_completed=time_game_started,
        winners=[]
    )

    value_dump = game_state.Schema().dumps(game_state)
    print(value_dump)


def parse_response(class_type, response):
    return class_type.Schema().loads(response.text)


def test_all():
    create_room_response = get_response(
        RequestMethods.POST,
        "http://0.0.0.0:9378/create-room",
        {
            "name": "Happy Hour",
            "password": "test123",
            "min_players": 2,
            "max_players": 4,
            "creator_id": "uniqueidhere",
            "score_to_win": 15
        })

    room = parse_response(Room, create_room_response)

    get_room_response = get_response(
        RequestMethods.GET,
        f'http://0.0.0.0:9378/get-room/{room.id}',
        {})

    room = parse_response(Room, get_room_response)

    assert len(room.players) == 1
    assert room.players[0].id == "uniqueidhere"

    join_room_response = get_response(
        RequestMethods.POST,
        f'http://0.0.0.0:9378/join-room/{room.id}',
        {
            "name": "test user",
            "password": "test123",
            "player_id": "testuid"
        })

    room: Room = parse_response(Room, join_room_response)

    assert len(room.players) == 2
    assert room.players[0].id == "uniqueidhere"
    assert room.players[1].id == "testuid"

    start_game_response = get_response(
        RequestMethods.POST,
        f'http://0.0.0.0:9378/start-game',
        {
            'room_id': room.id
        })

    game_state = parse_response(GameState, start_game_response)

    get_game_state_response = get_response(
        RequestMethods.GET,
        f'http://0.0.0.0:9378/get-game-state/{game_state.id}',
        {})

    game_state: GameState = parse_response(GameState, get_game_state_response)

    # Game has started now, player 1 takes his turn

    player1_end_turn_1 = get_response(
        RequestMethods.POST,
        f'http://0.0.0.0:9378/end-turn',
        {
            "room_id": room.id,
            "player_id": room.players[0].id,
            "game_state_id": game_state.id,
            "action": "Buying3DifferentTokens",
            "payload": {
                "bought_noble": None,
                "bought_card": None,
                "reserved_card": None,
                "tokens_returned": [],
                "tokens_bought": [
                    "GREEN",
                    "BLUE",
                    "BLACK"
                ]
            }
        })

    assert game_state.turn_number == 0
    game_state: GameState = parse_response(GameState, player1_end_turn_1)
    assert game_state.player_states[room.players[0].id].tokens[TokenColor.GREEN] == 1
    assert game_state.player_states[room.players[0].id].tokens[TokenColor.BLUE] == 1
    assert game_state.player_states[room.players[0].id].tokens[TokenColor.BLACK] == 1
    assert game_state.turn_number == 1

    # Player 2 takes his turn

    player2_end_turn_1 = get_response(
        RequestMethods.POST,
        f'http://0.0.0.0:9378/end-turn',
        {
            "room_id": room.id,
            "player_id": room.players[1].id,
            "game_state_id": game_state.id,
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
        })

    assert game_state.turn_number == 1
    game_state: GameState = parse_response(GameState, player2_end_turn_1)
    assert game_state.player_states[room.players[1].id].tokens[TokenColor.RED] == 1
    assert game_state.player_states[room.players[1].id].tokens[TokenColor.BLUE] == 1
    assert game_state.player_states[room.players[1].id].tokens[TokenColor.GREEN] == 1
    assert game_state.turn_number == 0
