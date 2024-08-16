from contextvars import ContextVar, Token
from typing import Generic, TypeVar

from fastapi import BackgroundTasks, Request

T = TypeVar("T")


# https://github.com/fastapi/fastapi/discussions/8628
class ContextWrapper(Generic[T]):
    def __init__(self, value: ContextVar[T]) -> None:
        self.__value: ContextVar[T] = value

    def set(self, value: T) -> Token[T]:
        return self.__value.set(value)

    def reset(self, token: Token[T]) -> None:
        self.__value.reset(token)

    @property
    def value(self) -> T:
        try:
            return self.__value.get()
        except LookupError:
            raise ValueError(f"Context {self.__value.name} is not set, please use the dependency.")


request_ctx = ContextWrapper[Request](ContextVar("request"))
background_tasks_ctx = ContextWrapper[BackgroundTasks](ContextVar("background_tasks"))
