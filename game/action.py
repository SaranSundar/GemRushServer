from dataclasses import dataclass
from enum import Enum

from serde import serialize, deserialize


@deserialize
@serialize
@dataclass
class Action(Enum):
    GET_CHIPS = "get_chips"
    RESERVE_CARD = "reserve_card"
    BUY_CARD = "buy_card"
