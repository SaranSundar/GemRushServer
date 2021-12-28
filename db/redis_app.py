from dataclasses import dataclass
from functools import lru_cache

import redis

# https://newbedev.com/error-99-connecting-to-localhost-6379-cannot-assign-requested-address
# TODO: Make redis_host "redis" on prod build, and localhost on local development

REDIS_HOST = "localhost"
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

    def write(self, key, value, class_type=None):
        if class_type is None:
            self.redis_app.set(key, value)

        value = value.Schema().dumps(value)
        self.redis_app.set(key, value)

    def read(self, key, class_type=None):
        json_value = self.redis_app.get(key)
        if class_type is None:
            return json_value
        return class_type.Schema().loads(json_value)

    def incr(self, key):
        self.redis_app.incr(key)
