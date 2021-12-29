import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List

import requests
from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Tier, Card
from card.color import CardColor, TokenColor
from card.deck import Deck
from player.player import Player
from room.room import Room
from state.game_state import GameState
from utils.utils import generate_uid


@dataclass
@mmdc
class RequestMethods:
    POST = "POST"
    GET = "GET"


def get_json_from_request(method, url, body):
    payload = json.dumps(body)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.json()


class TestEnum(str, Enum):
    TEST1 = "test1"
    TEST2 = "test2"

    def __str__(self):
        return self.value


@dataclass
@mmdc
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
        "creator_id": "uniqueidhere"
    }

    response_json = get_json_from_request(RequestMethods.POST, url, body)

    data = json.loads(response_json)
    # Assert game state is valid in 2 different ways
    room = Room.Schema().loads(response_json)
    room = Room(**data)
    print(room)


def test_start_game():
    # TODO: Automatically get room id
    url = "http://0.0.0.0:9378/start-game"
    body = {
        "room_id": "b711bb9e-6dd2-4a9b-a3c2-cf004b78753b"
    }

    response_json = get_json_from_request(RequestMethods.POST, url, body)

    data = json.loads(response_json)
    # Assert game state is valid in 2 different ways
    game_state = GameState.Schema().loads(response_json)
    game_state = GameState(**data)
    print(game_state)
