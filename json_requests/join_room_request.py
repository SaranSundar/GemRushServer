from marshmallow_dataclass import dataclass as mmdc


@mmdc
class JoinRoomRequest:
    name: str
    password: str
    player_id: str
