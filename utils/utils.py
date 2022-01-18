import json
import uuid
from dataclasses import dataclass
from random import shuffle

import requests
from marshmallow_dataclass import dataclass as mmdc


def load_words():
    with open('./assets/words.txt') as f:
        words = f.readlines()
        for i in range(len(words)):
            words[i] = words[i].strip().lower()
        shuffle(words)
    return words


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
