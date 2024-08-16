from celery import Celery

from .config import celery_settings


def create_celery_app() -> Celery:
    app = Celery(
        "viot_celery",
        broker=celery_settings.BROKER_URL,
        backend=celery_settings.RESULT_BACKEND,
        broker_connection_retry_on_startup=True,
        include=celery_settings.TASK_PACKAGES,
    )

    return app


celery_app = create_celery_app()
