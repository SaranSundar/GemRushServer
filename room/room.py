from dataclasses import dataclass
from datetime import datetime
from typing import List

from json_requests.create_room_request import CreateRoomRequest
from player.player import Player
from utils.utils import generate_uid


@dataclass
class Room:
    id: str
    name: str
    password: str
    min_players: int
    max_players: int
    owner: Player
    players: List[Player]
    time_room_created: datetime
    game_state_id: str

    @staticmethod
    def request_to_dto(create_room_request: CreateRoomRequest):
        owner = Player(create_room_request.creator_id)
        return Room(
            id=generate_uid(),
            name=create_room_request.name,
            password=create_room_request.password,
            min_players=create_room_request.min_players,
            max_players=create_room_request.max_players,
            owner=owner,
            players=[owner],
            time_room_created=datetime.utcnow(),
            game_state_id=""
        )

    def join(self, player_id: str, password: str):
        assert password == self.password, 'Incorrect password to join the room'
        assert len(self.players) <= self.max_players - 1, 'Maximum player reached'

        self.players.append(Player(player_id))
