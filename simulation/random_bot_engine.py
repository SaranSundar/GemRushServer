import random
from typing import Dict

from game.game_state import GameState
from simulation.bot_engine import BotEngine
from utils.game_utils import get_valid_moves

"""Random Bot Engine. Makes random move at each turn"""


class RandomBotEngine(BotEngine):
    def take_turn(self, game_state: GameState, player_id: str) -> Dict:
        return random.choice(get_valid_moves(game_state.deck, game_state.player_states[player_id]))
