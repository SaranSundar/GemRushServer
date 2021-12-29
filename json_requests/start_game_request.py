from dataclasses import dataclass

from marshmallow_dataclass import dataclass as mmdc


@mmdc
@dataclass
class StartGameRequest:
    room_id: str
