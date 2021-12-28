from dataclasses import dataclass


@dataclass
class JoinRoomRequest:
    name: str
    password: str
    player_id: str
