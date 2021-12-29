import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List

import requests
from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Tier, Card
from card.deck import Deck
from enums.CardColor import CardColor
from enums.TokenColor import TokenColor
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
    response = requests.request(method, url, headers=headers, data=payload)
    return response


class TestEnum(str, Enum):
    TEST1 = "test1"
    TEST2 = "test2"

    def __str__(self):
        return self.value


@dataclass
@mmdc
@dataclass
class TestDC:
    test_dict: Dict[TestEnum, str]
    tiered_str: Dict[Tier, str]
    card: Card
    # tiered_cards: Dict[Tier, List[Card]]


def test_generating_test_dc():
    enum_dict: Dict[TestEnum, str] = {
        TestEnum.TEST1: "hi1",
        TestEnum.TEST2: "hi2"
    }
    tiered_cards: Dict[Tier, List[Card]] = Deck.load_card_data('.././assets/deck-data.json')
    tiered_str: Dict[Tier, str] = {
        Tier.GREEN: "test1",
        Tier.BLUE: "test2"

    }
    points: int = 5
    tier: Tier = Tier.GREEN
    color: CardColor = CardColor.BLUE
    cost: Dict[TokenColor, int] = {
        TokenColor.GREEN: 3
    }
    card = Card(points, tier, color, cost)  # tiered_cards[Tier.GREEN][0]
    original_card = tiered_cards[Tier.GREEN][0]
    test = TestDC(enum_dict, tiered_str, original_card)
    value_dump = test.Schema().dumps(test)
    print(value_dump)

    value = TestDC.Schema().loads(value_dump)
    print(value)


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
        time_last_move_completed=time_game_started
    )

    value_dump = game_state.Schema().dumps(game_state)
    print(value_dump)


def test_create_room():
    url = "http://0.0.0.0:9378/create-room"
    body = {
        "name": "Happy Hour",
        "password": "test123",
        "min_players": 2,
        "max_players": 4,
        "creator_id": "uniqueidhere",
        "score_to_win": 15
    }
    response = get_response(RequestMethods.POST, url, body)
    # Assert game state is valid in 2 different ways
    room = Room.Schema().loads(response.text)
    room = Room(**response.json())
    print(room)


def test_start_game():
    # TODO: Automatically get room id
    url = "http://0.0.0.0:9378/start-game"
    body = {
        "room_id": "b711bb9e-6dd2-4a9b-a3c2-cf004b78753b"
    }

    response_json = get_response(RequestMethods.POST, url, body)
    # Assert game state is valid in 2 different ways
    game_state = GameState.Schema().loads(response_json.text)
    game_state = GameState(**response_json.json())
    print(game_state)


def test_all():
    creation = get_response(
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
    get_room = get_response(
        RequestMethods.GET,
        f'http://0.0.0.0:9378/get-room/{creation.json()["id"]}',
        {})
    join_room = get_response(
        RequestMethods.POST,
        f'http://0.0.0.0:9378/join-room/{creation.json()["id"]}',
        {
            "name": "test user",
            "password": "test69",
            "player_id": "testuid"
        })
    start_game = get_response(
        RequestMethods.POST,
        f'http://0.0.0.0:9378/start-game',
        {
            'room_id': get_room.json()['id']
        })
    get_game_state = get_response(
        RequestMethods.GET,
        f'http://0.0.0.0:9378/get-game-state/{start_game.json()["id"]}',
        {})
