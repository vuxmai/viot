from injector import Binder, Module, SingletonScope

from .client import RedisClient, get_redis_client


class RedisModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(RedisClient, to=get_redis_client(), scope=SingletonScope)
