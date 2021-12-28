from flask import Flask, request, jsonify

from db.redis_app import get_redis_app, RedisPaths
from json_requests.create_room_request import CreateRoomRequest
from room.room import Room

redis_app = get_redis_app()
app = Flask(__name__)


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
@app.route('/create-room/<user_id>', methods=['POST'])
def create_room(user_id):
    print("User id", user_id)
    create_room_request = CreateRoomRequest(**request.json)
    room: Room = Room.request_to_dto(create_room_request)
    key = RedisPaths.create_key([RedisPaths.ROOMS, room.id])
    redis_app.write(key, room)
    return jsonify(room)


@app.route('/get-room/<room_id>', methods=['GET'])
def get_room(room_id):
    key = RedisPaths.create_key([RedisPaths.ROOMS, room_id])
    room: Room = redis_app.read(key)
    return jsonify(room)


@app.route('/join-room/<room_id>', methods=['POST'])
def join_room(room_id):
    redis_app.read(RedisPaths.ROOMS, )
    pass


@app.route('/start-game', methods=['POST'])
def start_game():
    # TODO
    pass


@app.route('/make-move', methods=['POST'])
def make_move():
    # TODO
    pass


@app.route('/get-game-state', methods=['POST'])
def get_game_state():
    # TODO
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
