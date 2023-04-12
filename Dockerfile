FROM python:3.9.7-slim-buster AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_NOSPIN=true \
    WORKON_HOME=/opt/venv \
    LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG USER_NAME=app-data
ARG USER_ID=1000

WORKDIR /app

RUN pip install --no-cache-dir pipenv
RUN useradd --home $WORKON_HOME --uid $USER_ID $USER_NAME

USER $USER_NAME

CMD ["pipenv", "shell"]
