from dataclasses import dataclass


@dataclass
class CreateRoomRequest:
    name: str
    password: str
    min_players: int
    max_players: int
    creator_id: str
