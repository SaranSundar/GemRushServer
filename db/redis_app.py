import json
from dataclasses import dataclass
from functools import lru_cache

import redis
from serde.json import to_json

# https://newbedev.com/error-99-connecting-to-localhost-6379-cannot-assign-requested-address
REDIS_HOST = "redis"
REDIS_PORT = 6379


@dataclass
class RedisPaths:
    ROOMS = "rooms"
    GAME_STATES = "game_states"

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

    def read(self, key):
        return json.loads(self.redis_app.get(key))

    def incr(self, key):
        self.redis_app.incr(key)
