import json
import random
import uuid
from dataclasses import dataclass
from random import shuffle

import requests
from marshmallow_dataclass import dataclass as mmdc

from app import redis_app
from db.redis_app import RedisPaths
from room.room import Room

words = []


def load_words():
    global words
    with open('./assets/words.txt') as f:
        words = f.readlines()
        for i in range(len(words)):
            words[i] = words[i].strip().lower()
        shuffle(words)
    return words


def generate_room_code():
    global words
    if len(words) == 0:
        words = load_words()
    room_code = " ".join(random.sample(words, 3))
    # Keep looping until we find room code that doesn't exist already
    while get_room("test") is not None:
        room_code = " ".join(random.sample(words, 3))
    return room_code


def generate_uid():
    return str(uuid.uuid4())


@mmdc
@dataclass
class RequestMethods:
    POST = "POST"
    GET = "GET"


@mmdc
@dataclass
class ApiMethods:
    CREATE_ROOM = "/create-room"
    JOIN_ROOM = "/join-room"
    START_GAME = "/start-game"


def get_response(method, url, body):
    payload = json.dumps(body)
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request(method, url, headers=headers, data=payload)


def parse_response(class_type, response):
    return class_type.Schema().loads(response.text)


def get_room(room_id) -> Room:
    key = RedisPaths.create_key([RedisPaths.ROOMS, room_id])
    room = redis_app.read(key, class_type=Room)
    return room
