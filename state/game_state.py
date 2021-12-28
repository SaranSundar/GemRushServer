from dataclasses import dataclass
from typing import List, Dict

from card.card_data import Card, Tier
from card.color import TokenColor
from card.deck import Deck
from card.noble import Noble
from player.player import Player, PlayerState


@dataclass
class GameState:
    id: str
    player_states: Dict[Player, PlayerState]
    deck: Deck
    turn_number: int
    turn_order: List[Player]
