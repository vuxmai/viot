FROM python:3.11-slim-bullseye AS python-base

ARG PROJECT_DIR=./viot


FROM python-base AS builder

ARG INSTALL_DEV=false

WORKDIR /tmp

RUN pip install poetry

COPY ${PROJECT_DIR}/pyproject.toml ${PROJECT_DIR}/poetry.lock /tmp/

RUN if [ "$INSTALL_DEV" = "true" ]; then \
        poetry export --without-hashes --with dev -f requirements.txt -o requirements.txt; \
    else \
        poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt; \
    fi


FROM python-base AS production

WORKDIR /viot

COPY --from=builder /tmp/requirements.txt /viot/requirements.txt

RUN pip install --no-cache-dir -r /viot/requirements.txt

COPY ${PROJECT_DIR}/app /viot/app

ENV PYTHONPATH=':$PYTHONPATH:.'

RUN groupadd -r viot && useradd -r -m -g viot viot
USER viot

CMD ["python", "app/main.py"]
