from typing import List

from marshmallow_dataclass import dataclass as mmdc

from player.player import Player


@mmdc
class EndTurnRequest:
    room_id: str
    player: Player
    # Example of actions
    # Buying card
    # Buying card, meets nobles requirements so gets 1 noble
    # Getting gold token, reserving card
    # Getting 3 tokens of different colors
    # Getting 2 tokens of same color if 4 or more of that token exist
    # Getting tokens, owning greater than 10 tokens, so return some tokens
    actions: List[str]
