import json

import requests

from state.game_state import GameState


def test_start_game():
    # TODO: Automatically get room id
    url = "http://0.0.0.0:9378/start-game"
    payload = json.dumps({
        "room_id": "b711bb9e-6dd2-4a9b-a3c2-cf004b78753b"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.json())

    # Assert game state is valid in 2 different ways
    game_state = GameState.Schema().loads(response.json())
    game_state = GameState(**data)
    print(game_state)
