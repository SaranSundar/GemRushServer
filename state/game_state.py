from dataclasses import dataclass
from typing import List, Dict

from card.card_data import Card, Tier
from card.color import TokenColor
from card.noble import Noble
from player.player import Player, PlayerState


@dataclass
class GameState:
    id: str
    player_states: Dict[Player, PlayerState]
    nobles: List[Noble]
    cards: Dict[Tier, List[Card]]
    tokens: Dict[TokenColor, int]
    current_turn: Player
    turn_order: List[Player]
