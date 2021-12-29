from marshmallow_dataclass import dataclass as mmdc


@mmdc
class CreateRoomRequest:
    name: str
    password: str
    min_players: int
    max_players: int
    creator_id: str
