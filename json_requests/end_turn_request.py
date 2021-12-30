from dataclasses import dataclass, field
from typing import List

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card
from card.noble import Noble
from enums.EndTurnAction import EndTurnAction
from enums.TokenColor import TokenColor


@mmdc
@dataclass
class EndTurnRequestPayload:
    tokens_bought: List[TokenColor] = field(default_factory=lambda: [])
    tokens_returned: List[TokenColor] = field(default_factory=lambda: [])
    bought_card: Card = field(default=None)
    reserved_card: Card = field(default=None)
    bought_noble: Noble = field(default=None)


@mmdc
@dataclass
class EndTurnRequest:
    room_id: str
    game_state_id: str
    player_id: str
    # Example of actions, any action can get a noble if player chooses to at that turn
    # Buying card
    # Getting gold token, reserving card
    # Getting 3 tokens of different colors
    # Getting 2 tokens of same color if 4 or more of that token exist
    # Getting tokens, owning greater than 10 tokens, so return some tokens
    # Getting 1-2 different tokens when you have 8 or 9 tokens already
    action: EndTurnAction
    payload: EndTurnRequestPayload
