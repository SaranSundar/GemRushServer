import uuid
from marshmallow_dataclass import dataclass

from state.game_state import GameState


def generate_uid():
    return str(uuid.uuid4())


def generate_json(value):
    value_as_json = None
    try:
        value_as_json = value.Schema().dumps(value)
        print(value_as_json)
        return value_as_json
    except Exception as e:
        pass
    return value_as_json
