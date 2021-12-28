from marshmallow_dataclass import dataclass


@dataclass
class JoinRoomRequest:
    name: str
    password: str
    player_id: str
