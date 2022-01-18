from dataclasses import dataclass
from datetime import datetime
from typing import List

from marshmallow_dataclass import dataclass as mmdc

from json_requests.create_room_request import CreateRoomRequest
from player.player import Player


@mmdc
@dataclass
class Room:
    id: str
    name: str
    password: str
    min_players: int
    max_players: int
    owner: Player
    players: List[Player]
    # "time_room_created": "Wed, 29 Dec 2021 19:21:59 GMT"
    # "time_room_created": "2021-12-29T19:21:59.553236"
    time_room_created: datetime
    game_state_id: str
    score_to_win: int

    @staticmethod
    def request_to_dto(create_room_request: CreateRoomRequest, room_code):
        owner = Player(create_room_request.creator_id)
        return Room(
            id=room_code,
            name=create_room_request.name,
            password=create_room_request.password,
            min_players=create_room_request.min_players,
            max_players=create_room_request.max_players,
            owner=owner,
            players=[owner],
            time_room_created=datetime.utcnow(),
            game_state_id="",
            score_to_win=create_room_request.score_to_win
        )

    def join(self, player_id: str, password: str):
        assert password == self.password, 'Incorrect password to join the room'
        assert len(self.players) <= self.max_players - 1, 'Maximum players reached'

        # Don't re-add same player to room if player disconnects and rejoins
        for player in self.players:
            if player.id == player_id:
                return

        self.players.append(Player(player_id))
