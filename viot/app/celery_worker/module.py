from celery import Celery
from injector import Binder, Module, SingletonScope

from .celery import celery_app


class CeleryWorkerModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Celery, to=celery_app, scope=SingletonScope)
