from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc

from card.deck import Deck
from player.player import Player, PlayerState


@mmdc
@dataclass
class GameState:
    id: str
    # Player id -> PlayerState
    player_states: Dict[str, PlayerState]
    deck: Deck
    turn_number: int
    turn_order: List[Player]
    time_game_started: datetime
    time_last_move_completed: datetime
    # Could have ties
    # winners -> Player ids
    winners: List[str]

    def __hash__(self):
        return hash(self.id)
