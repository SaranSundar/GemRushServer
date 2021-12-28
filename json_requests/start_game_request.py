from marshmallow_dataclass import dataclass


@dataclass
class StartGameRequest:
    room_id: str
