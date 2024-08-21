FROM python:3.11-slim-bullseye AS python-base

ARG PROJECT_DIR=./viot


FROM python-base AS builder

WORKDIR /tmp

RUN pip install poetry

COPY ${PROJECT_DIR}/pyproject.toml ${PROJECT_DIR}/poetry.lock /tmp/

RUN poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt;


FROM python-base AS production

WORKDIR /code

COPY --from=builder /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ${PROJECT_DIR}/app /code/app
COPY ${PROJECT_DIR}/scripts/start-celery.sh /code/celery-entrypoint.sh

# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#worker-doesn-t-start-permission-error
RUN ln -s /run/shm /dev/shm && \
    mkdir -p /code/app/logs && \
    chmod +x /code/celery-entrypoint.sh && \
    groupadd -r viot && \
    useradd -r -m -g viot viot && \
    chown -R viot:viot /code

USER viot

EXPOSE 8555

CMD ["./celery-entrypoint.sh"]
