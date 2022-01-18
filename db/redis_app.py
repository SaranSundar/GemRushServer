from dataclasses import dataclass
from functools import lru_cache

import redis
from marshmallow_dataclass import dataclass as mmdc

# https://newbedev.com/error-99-connecting-to-localhost-6379-cannot-assign-requested-address
# TODO: Make redis_host "redis" on prod build, and localhost on local development

REDIS_HOST = "redis"
REDIS_PORT = 6379


@mmdc
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


@mmdc
@dataclass
class RedisApp:
    redis_app = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    # https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
    def write(self, key, value, class_type=None):
        if class_type is None:
            self.redis_app.set(key, value)
            return value
        else:
            value_dump = value.Schema().dumps(value)
            self.redis_app.set(key, value_dump)
            return value_dump

    def read(self, key, class_type=None):
        json_value = self.redis_app.get(key)
        if json_value is None:
            return None
        if class_type is None:
            return json_value
        else:
            return class_type.Schema().loads(json_value)

    def exists(self, key):
        return self.redis_app.exists(key)
