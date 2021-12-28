import json

import requests

from state.game_state import GameState


def test_start_game():
    url = "http://0.0.0.0:9378/start-game"
    payload = json.dumps({
        "room_id": "b049c20f-ef10-4b1f-9239-6e5193c0a0ad"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.json())
    data['player_states'] = {}
    print(data)
    game_state = GameState.Schema().loads(response.json())

    # game_state = GameState(**data)

    print(game_state)
