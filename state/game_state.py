from datetime import datetime
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc
from dataclasses import dataclass

from card.deck import Deck
from player.player import Player, PlayerState


@dataclass
@mmdc
class GameState:
    id: str
    # Player id
    player_states: Dict[str, PlayerState]
    deck: Deck
    turn_number: int
    turn_order: List[Player]
    time_game_started: datetime
    time_last_move_completed: datetime

    def __hash__(self):
        return hash(self.id)
