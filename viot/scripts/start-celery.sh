#!/usr/bin/env bash

celery -A app.celery_worker.celery worker -l info -B &
celery -A app.celery_worker.celery flower --port=80 --basic-auth=admin:admin
