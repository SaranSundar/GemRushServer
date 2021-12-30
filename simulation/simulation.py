from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import dataclass as mmdc

from card.deck import Deck
from game.game_state import GameState
from room.room import Room
from simulation.bot_engine import BotEngine
from utils.utils import get_response, RequestMethods, parse_response, ApiMethods


@dataclass
@mmdc
class SimulationPlayer:
    id: str
    engine: BotEngine


@dataclass
@mmdc
class Simulation:
    deck: Deck
    room: Room
    game_state: GameState
    players: List[SimulationPlayer]
    host_ip: str = "http://207.246.122.46"
    port: str = "9378"

    def create_host(self) -> SimulationPlayer:
        host = SimulationPlayer(id="Saran")
        self.players = [host]
        return host

    def create_other_players(self):
        other_players = ["Vishruth", "Juwhan", "Rooshi", "Joseph Mama"]
        for player_id in other_players:
            self.players.append(SimulationPlayer(id=player_id))

    def create_room(self, host: SimulationPlayer) -> Room:
        create_room_response = get_response(
            RequestMethods.POST,
            f"{self.host_ip}:{self.port}{ApiMethods.CREATE_ROOM}",
            {
                "name": "Simulation Testing Room",
                "password": "computers-fight",
                "min_players": 2,
                "max_players": 4,
                "creator_id": host.id,
                "score_to_win": 15
            })

        return parse_response(Room, create_room_response)

    def join_room(self, player: SimulationPlayer, room: Room) -> Room:
        join_room_response = get_response(
            RequestMethods.POST,
            f"{self.host_ip}:{self.port}{ApiMethods.JOIN_ROOM}/{room.id}",
            {
                "name": room.name,
                "password": room.password,
                "player_id": player.id
            })
        return parse_response(Room, join_room_response)

    def start_game(self, room: Room) -> GameState:
        start_game_response = get_response(
            RequestMethods.POST,
            f"{self.host_ip}:{self.port}{ApiMethods.START_GAME}",
            {
                'room_id': room.id
            })

        return parse_response(GameState, start_game_response)

    def start_simulation(self):
        # The host creates the room
        host = self.create_host()
        self.room = self.create_room(host)
        # Other players join the room
        for player in self.players:
            if player.id != host.id:
                self.room = self.join_room(player, self.room)

        # Host starts game
        self.game_state = self.start_game(self.room)
