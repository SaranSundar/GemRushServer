import json
from dataclasses import dataclass
from datetime import datetime

import requests
from marshmallow_dataclass import dataclass as mmdc

from card.deck import Deck
from player.player import Player
from room.room import Room
from state.game_state import GameState
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
        noble_cards=Deck.load_nobles_data('.././assets/nobles-data.json')
    )
    time_game_started = datetime.utcnow()
    deck.shuffle()
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

    room = parse_response(Room, join_room_response)

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

    game_state = parse_response(GameState, get_game_state_response)
