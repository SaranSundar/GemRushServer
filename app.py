import logging
import random
from datetime import datetime
from random import shuffle

from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS

from card.deck import Deck
from db.redis_app import get_redis_app, RedisPaths
from enums.EndTurnAction import EndTurnAction
from game.game_manager import GameManager
from game.game_state import GameState
from json_requests.create_room_request import CreateRoomRequest
from json_requests.end_turn_request import EndTurnRequest
from json_requests.join_room_request import JoinRoomRequest
from json_requests.start_game_request import StartGameRequest
from player.player import PlayerState
from room.room import Room
from utils.utils import generate_uid, load_words


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class MyFlask(Flask):
    json_encoder = MyJSONEncoder


words = load_words()

redis_app = get_redis_app()
application = MyFlask(__name__)
application.config['SECRET_KEY'] = "I am a very interesting pokemon called pikachu"
application.config['CORS_HEADER'] = "Content-Type"
cors = CORS(application)

if __name__ != '__main__':
    # https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)
    logging.getLogger('flask_cors').level = logging.DEBUG


@application.route('/')
def hello():
    # application.logger.debug('this is a DEBUG message')
    # application.logger.info('this is an INFO message')
    # application.logger.warning('this is a WARNING message')
    # application.logger.error('this is an ERROR message')
    # application.logger.critical('this is a CRITICAL message')
    hits: int = 0
    if redis_app.exists('hits'):
        hits = int(redis_app.read('hits'))
    hits += 1
    redis_app.write('hits', hits)
    return f'GemRush has been viewed {hits} times.'


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
@application.route('/create-room', methods=['POST'])
def create_room():
    create_room_request = CreateRoomRequest(**request.json)
    room_code = generate_room_code()
    room: Room = Room.request_to_dto(create_room_request, room_code)
    application.logger.debug('Room value in create-room is')
    application.logger.debug(room)
    save_room(room)
    print(room.id)
    return jsonify(room)


@application.route('/get-room/<room_id>', methods=['GET'])
def get_room_json(room_id):
    room = get_room(room_id)
    application.logger.debug('Room value in get-room is')
    application.logger.debug(room)
    return jsonify(room)


def save_room(room: Room):
    key = RedisPaths.create_key([RedisPaths.ROOMS, room.id])
    redis_app.write(key, room, class_type=Room)


def get_room(room_id) -> Room:
    key = RedisPaths.create_key([RedisPaths.ROOMS, room_id])
    room = redis_app.read(key, class_type=Room)
    return room


def generate_room_code():
    room_code = " ".join(random.sample(words, 3))
    # Keep looping until we find room code that doesn't exist already
    while get_room(room_code) is not None:
        room_code = " ".join(random.sample(words, 3))
    return room_code


@application.route('/join-room/<room_id>', methods=['POST'])
def join_room(room_id):
    room_id = room_id.lower()
    join_room_request = JoinRoomRequest(**request.json)
    room = get_room(room_id)
    # Can't join game that's already started
    joined_room = room.join(join_room_request.player_id, join_room_request.password)
    application.logger.debug('Room value in join-room is')
    application.logger.debug(room)
    if joined_room:
        save_room(room)
        return jsonify(room)
    else:
        return jsonify(None)


@application.route('/start-game', methods=['POST'])
def start_game():
    start_game_request = StartGameRequest(**request.json)
    room = get_room(start_game_request.room_id)
    num_of_players = len(room.players)
    deck = Deck(
        tiered_cards=Deck.load_card_data(),
        noble_cards=Deck.load_nobles_data(),
        bank=Deck.create_bank(num_of_players=num_of_players)
    )
    deck.create_board()

    player_to_state = dict()
    shuffle(room.players)
    # https://stackoverflow.com/questions/52390576/how-can-i-make-a-python-dataclass-hashable-without-making-them-immutable
    for player in room.players:
        player_to_state[player.id] = PlayerState(PlayerState.init_cards(), PlayerState.init_tokens(), [], [], None)

    time_game_started = datetime.utcnow()

    game_state = GameState(
        id=generate_uid(),
        player_states=player_to_state,
        deck=deck,
        turn_number=0,
        turn_order=room.players,
        time_game_started=time_game_started,
        time_last_move_completed=time_game_started,
        winners=[]
    )
    room.game_state_id = game_state.id
    save_room(room)
    save_game_state(game_state)
    return jsonify(game_state)


@application.route('/end-turn', methods=['POST'])
def end_turn():
    # end_turn_request = EndTurnRequest(**request.json)
    data = request.data
    print("data is")
    print(data)
    end_turn_request = EndTurnRequest.Schema().loads(data)
    game_state = validate_and_end_turn(end_turn_request)
    save_game_state(game_state)
    return jsonify(game_state)


def validate_and_end_turn(end_turn_request: EndTurnRequest) -> GameState:
    game_state = get_game_state(end_turn_request.game_state_id)
    room: Room = get_room(end_turn_request.room_id)
    # TODO: Validate request
    # Check that player id exists in room and game game
    # Check that it is this player ids turn
    # Check if the action they choose was a valid action
    # Send back new game game with updated turn if action was valid
    if end_turn_request.action == EndTurnAction.BuyingCard:
        GameManager.buy_card(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.BuyingReservedCard:
        GameManager.buy_reserved_card(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.BuyingGoldToken:
        GameManager.buy_gold_token_and_reserve_card(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.Buying3DifferentTokens:
        GameManager.buy_3_different_tokens(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.Buying2SameTokens:
        GameManager.buy_2_same_tokens(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.BuyingLimitedTokens:
        GameManager.buy_limited_tokens(game_state, end_turn_request)
    elif end_turn_request.action == EndTurnAction.DiscardTokens:
        GameManager.discard_tokens(game_state, end_turn_request)

    # At any turn a player can choose to buy a noble if they meet the requirements
    if end_turn_request.payload.bought_noble:
        game_state.player_states[end_turn_request.player_id].nobles.append(end_turn_request.payload.bought_noble)
        game_state.deck.noble_cards.remove(end_turn_request.payload.bought_noble)

    # If last players turn, check if anyone won
    if game_state.turn_number == len(game_state.turn_order) - 1:
        winning_players = []
        for player_id in game_state.player_states:
            player_state: PlayerState = game_state.player_states[player_id]
            points, total_num_cards = player_state.get_total_weight()
            if points >= room.score_to_win:
                winning_players.append((points, total_num_cards, player_id))
        winning_players = sorted(winning_players, key=lambda wp: (wp[0], -wp[1]))

        if winning_players:
            max_score = 0
            for wp in winning_players:
                max_score = max(max_score, wp[0])
            least_cards = 100
            winner = None
            for wp in winning_players:
                if wp[0] == max_score:
                    # Possible winner
                    if wp[1] < least_cards:
                        least_cards = wp[1]
                        winner = wp
            game_state.winners = [winner[2]]

    # Go to next players turn
    game_state.turn_number += 1
    if game_state.turn_number >= len(game_state.turn_order):
        game_state.turn_number = 0

    return game_state


@application.route('/get-game-state/<game_state_id>', methods=['GET'])
def get_game_state_json(game_state_id):
    game_state = get_game_state(game_state_id)
    application.logger.debug('Game game value in get-game-game is')
    application.logger.debug(game_state.id)
    result = jsonify(game_state)
    return result


def save_game_state(game_state: GameState):
    key = RedisPaths.create_key([RedisPaths.GAME_STATES, game_state.id])
    return redis_app.write(key, game_state, class_type=GameState)


def get_game_state(game_state_id) -> GameState:
    key = RedisPaths.create_key([RedisPaths.GAME_STATES, game_state_id])
    game_state = redis_app.read(key, class_type=GameState)
    return game_state


if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True, threaded=True)
