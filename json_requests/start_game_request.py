from dataclasses import dataclass


@dataclass
class StartGameRequest:
    room_id: str
