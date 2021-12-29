from enum import Enum

from marshmallow_dataclass import dataclass as mmdc


@mmdc
class Action(Enum):
    GET_CHIPS = "get_chips"
    RESERVE_CARD = "reserve_card"
    BUY_CARD = "buy_card"
