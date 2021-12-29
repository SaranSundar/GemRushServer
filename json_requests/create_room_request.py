from dataclasses import dataclass

from marshmallow_dataclass import dataclass as mmdc


@mmdc
@dataclass
class CreateRoomRequest:
    name: str
    password: str
    min_players: int
    max_players: int
    creator_id: str
    score_to_win: int
