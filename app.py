import logging
from datetime import datetime
from random import shuffle

from flask import Flask, request, jsonify
from flask.json import JSONEncoder

from card.deck import Deck
from db.redis_app import get_redis_app, RedisPaths
from enums.EndTurnAction import EndTurnAction
from json_requests.create_room_request import CreateRoomRequest
from json_requests.end_turn_request import EndTurnRequest
from json_requests.join_room_request import JoinRoomRequest
from json_requests.start_game_request import StartGameRequest
from player.player import PlayerState
from room.room import Room
from state.game_manager import GameManager
from state.game_state import GameState
from utils.utils import generate_uid


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return super().default(o)


class MyFlask(Flask):
    json_encoder = MyJSONEncoder


redis_app = get_redis_app()
app = MyFlask(__name__)

if __name__ != '__main__':
    # https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/')
def hello():
    # application.logger.debug('this is a DEBUG message')
    # application.logger.info('this is an INFO message')
    # application.logger.warning('this is a WARNING message')
    # application.logger.error('this is an ERROR message')
    # application.logger.critical('this is a CRITICAL message')
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
    app.logger.debug('Room value in create-room is')
    app.logger.debug(room)
    save_room(room)
    print(room.id)
    return jsonify(room)


@app.route('/get-room/<room_id>', methods=['GET'])
def get_room_json(room_id):
    room = get_room(room_id)
    app.logger.debug('Room value in get-room is')
    app.logger.debug(room)
    return jsonify(room)


def save_room(room: Room):
    key = RedisPaths.create_key([RedisPaths.ROOMS, room.id])
    redis_app.write(key, room, class_type=Room)


def get_room(room_id) -> Room:
    key = RedisPaths.create_key([RedisPaths.ROOMS, room_id])
    room = redis_app.read(key, class_type=Room)
    return room


@app.route('/join-room/<room_id>', methods=['POST'])
def join_room(room_id):
    join_room_request = JoinRoomRequest(**request.json)
    room = get_room(room_id)
    room.join(join_room_request.player_id, join_room_request.password)
    app.logger.debug('Room value in join-room is')
    app.logger.debug(room)
    save_room(room)
    return jsonify(room)


@app.route('/start-game', methods=['POST'])
def start_game():
    start_game_request = StartGameRequest(**request.json)
    room = get_room(start_game_request.room_id)
    deck = Deck(
        tiered_cards=Deck.load_card_data(),
        noble_cards=Deck.load_nobles_data()
    )
    deck.shuffle()

    player_to_state = dict()
    shuffle(room.players)
    # https://stackoverflow.com/questions/52390576/how-can-i-make-a-python-dataclass-hashable-without-making-them-immutable
    for player in room.players:
        player_to_state[player.id] = PlayerState({}, {}, [], [])

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
    return jsonify(game_state)


@app.route('/end-turn', methods=['POST'])
def end_turn():
    end_turn_request = EndTurnRequest(**request.json)


def validate_and_end_turn(end_turn_request: EndTurnRequest):
    game_state = get_game_state(end_turn_request.game_state_id)
    # TODO: Validate request
    # Check that player id exists in room and game state
    # Check that it is this player ids turn
    # Check if the action they choose was a valid action
    # Send back new game state with updated turn if action was valid
    # If last players turn, check if anyone won
    if end_turn_request.action == EndTurnAction.BuyingCard:
        GameManager.buy_card(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.BuyingGoldToken:
        GameManager.buy_gold_token_and_reserve_card(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.Buying3DifferentTokens:
        pass
    elif end_turn_request.action == EndTurnAction.Buying2SameTokens:
        pass
    elif end_turn_request.action == EndTurnAction.BuyingAndReturningTokens:
        pass
    elif end_turn_request.action == EndTurnAction.BuyingLimitedTokens:
        pass

    # At any turn a player can choose to buy a noble if they meet the requirements
    if end_turn_request.payload.bought_noble:
        game_state.player_states[end_turn_request.player_id].nobles.append(end_turn_request.payload.bought_noble)


@app.route('/get-game-state/<game_state_id>', methods=['GET'])
def get_game_state_json(game_state_id):
    game_state = get_game_state(game_state_id)
    app.logger.debug('Game state value in get-game-state is')
    app.logger.debug(game_state)
    return jsonify(game_state)


def save_game_state(game_state: GameState):
    key = RedisPaths.create_key([RedisPaths.GAME_STATES, game_state.id])
    return redis_app.write(key, game_state, class_type=GameState)


def get_game_state(game_state_id) -> GameState:
    key = RedisPaths.create_key([RedisPaths.GAME_STATES, game_state_id])
    game_state = redis_app.read(key, class_type=GameState)
    return game_state


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
