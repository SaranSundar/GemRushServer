from datetime import datetime
from random import shuffle

from flask import Flask, request, jsonify

from card.deck import Deck
from db.redis_app import get_redis_app, RedisPaths
from json_requests.create_room_request import CreateRoomRequest
from json_requests.join_room_request import JoinRoomRequest
from json_requests.start_game_request import StartGameRequest
from player.player import PlayerState
from room.room import Room
from state.game_state import GameState
from utils.utils import generate_uid

redis_app = get_redis_app()
app = Flask(__name__)


@app.route('/')
def hello():
    redis_app.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis_app.read('hits')


# Player 1 creates a room
# Other players join the room
# Player 1 decides to start game
# Turn order is randomly created
#
#
#
#
# http://localhost:5000/create_room
# curl -X POST http://localhost:5000/create-room
# {
#     "name": "Happy Hour",
#     "password": "test123",
#     "min_players": 2,
#     "max_players": 4,
#     "creator_id": "uniqueidhere"
# }

# curl -X POST http://localhost:5000/create-room/abc -d @temp.json -H "Content-Type: application/json"
# curl -X POST http://localhost:5000/create-room/test123
@app.route('/create-room', methods=['POST'])
def create_room():
    create_room_request = CreateRoomRequest(**request.json)
    room: Room = Room.request_to_dto(create_room_request)
    save_room(room)
    print(room.id)
    return jsonify(room)


@app.route('/get-room/<room_id>', methods=['GET'])
def get_room_json(room_id):
    return jsonify(get_room(room_id))


def save_room(room: Room) -> Room:
    key = RedisPaths.create_key([RedisPaths.ROOMS, room.id])
    redis_app.write(key, room)


def get_room(room_id) -> Room:
    key = RedisPaths.create_key([RedisPaths.ROOMS, room_id])
    return redis_app.read(key)


@app.route('/join-room/<room_id>', methods=['POST'])
def join_room(room_id):
    join_room_request = JoinRoomRequest(**request.json)
    room = get_room(room_id)
    room.join(join_room_request.player_id, join_room_request.password)
    save_room(room)


@app.route('/start-game', methods=['POST'])
def start_game():
    start_game_request = StartGameRequest(**request.json)
    room = get_room(start_game_request.room_id)
    deck = Deck()

    player_to_state = dict()
    shuffle(room.players)
    for player in room.players:
        player_to_state[player] = PlayerState({}, {}, [])

    time_game_started = datetime.utcnow()

    game_state = GameState(
        id=generate_uid(),
        player_states=player_to_state,
        deck=deck,
        turn_number=0,
        turn_order=room.players,
        time_game_started=time_game_started,
        time_last_move_completed=time_game_started
    )
    room.game_state_id = game_state.id
    save_room(room)


@app.route('/make-move', methods=['POST'])
def make_move():
    pass


@app.route('/get-game-state', methods=['POST'])
def get_game_state():
    # TODO
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=9375)
