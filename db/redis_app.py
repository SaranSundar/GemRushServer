from functools import lru_cache

import redis
from marshmallow_dataclass import dataclass as mmdc

# https://newbedev.com/error-99-connecting-to-localhost-6379-cannot-assign-requested-address
# TODO: Make redis_host "redis" on prod build, and localhost on local development

REDIS_HOST = "localhost"
REDIS_PORT = 6379


@mmdc
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
class RedisApp:
    redis_app = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    # https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
    def write(self, key, value, class_type=None):
        if class_type is None:
            self.redis_app.set(key, value)

        print(class_type)
        value_dump = value.Schema().dumps(value)
        print(value_dump)
        # value_dump = str(value_dump)
        self.redis_app.set(key, value_dump)
        return value_dump

    def read(self, key, class_type=None):
        json_value = self.redis_app.get(key)
        if class_type is None:
            return json_value
        return class_type.Schema().loads(json_value)

    def incr(self, key):
        self.redis_app.incr(key)
