from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card
from card.noble import Noble
from enums.EndTurnAction import EndTurnAction
from enums.TokenColor import TokenColor


@mmdc
@dataclass
class EndTurnRequestPayload:
    bought_card: Card
    reserved_card: Card
    bought_noble: Noble
    tokens_bought: List[TokenColor]
    tokens_returned: List[TokenColor]


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
