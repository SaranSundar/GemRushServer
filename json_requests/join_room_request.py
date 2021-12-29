from dataclasses import dataclass

from marshmallow_dataclass import dataclass as mmdc


@mmdc
@dataclass
class JoinRoomRequest:
    name: str
    password: str
    player_id: str
