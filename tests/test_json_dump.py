import json
from dataclasses import dataclass

import requests
from marshmallow_dataclass import dataclass as mmdc

from room.room import Room
from state.game_state import GameState


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
