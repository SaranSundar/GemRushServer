from marshmallow_dataclass import dataclass as mmdc


@mmdc
class StartGameRequest:
    room_id: str
