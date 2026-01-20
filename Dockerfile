FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --only main

COPY . /app
