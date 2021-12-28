from dataclasses import field
from datetime import datetime
from typing import List, Dict

from marshmallow_dataclass import dataclass

from card.deck import Deck
from player.player import Player, PlayerState


@dataclass(eq=True, frozen=True)
class GameState:
    id: str
    player_states: Dict[Player, PlayerState]
    deck: Deck
    turn_number: int
    turn_order: List[Player]
    time_game_started: datetime
    time_last_move_completed: datetime

    def __hash__(self):
        return hash(self.id)

