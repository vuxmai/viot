FROM python:3.11-slim-bullseye AS python-base

ARG PROJECT_DIR=./viot


FROM python-base AS builder

WORKDIR /tmp

RUN pip install poetry

COPY ${PROJECT_DIR}/pyproject.toml ${PROJECT_DIR}/poetry.lock /tmp/

RUN poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt;


FROM python-base AS production

WORKDIR /viot

COPY --from=builder /tmp/requirements.txt /viot/requirements.txt

RUN pip install --no-cache-dir -r /viot/requirements.txt

COPY ${PROJECT_DIR}/app /viot/app
COPY ${PROJECT_DIR}/scripts/start-celery.sh /viot/celery-entrypoint.sh

# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#worker-doesn-t-start-permission-error
RUN ln -s /run/shm /dev/shm && \
    mkdir -p /viot/app/logs && \
    chmod +x /viot/celery-entrypoint.sh && \
    groupadd -r viot && \
    useradd -r -m -g viot viot && \
    chown -R viot:viot /viot

USER viot

EXPOSE 8555

CMD ["./celery-entrypoint.sh"]
