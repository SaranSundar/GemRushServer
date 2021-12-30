from typing import Dict

from game.game_state import GameState

"""Bot Engine interface."""


class BotEngine:
    # TODO: for now, returns JSON representation of a move
    # refactor to a data class
    def take_turn(self, game_state: GameState, player_id: str) -> Dict:
        pass
