import json
from dataclasses import dataclass
from functools import lru_cache

from typing import Type
import redis
from serde.json import to_json

REDIS_HOST = "localhost"
REDIS_PORT = 6379


@dataclass
class RedisPaths:
    ROOMS = "rooms"

    @staticmethod
    def create_key(paths):
        return "/".join(paths)


@lru_cache(maxsize=1)
def get_redis_app():
    return RedisApp()


@dataclass
class RedisApp:
    redis_app = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def write(self, key, value):
        self.redis_app.set(key, to_json(value))

    def read(self, c: Type, key):
        return json.loads(self.redis_app.get(key))
