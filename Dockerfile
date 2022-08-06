# pull official base image
FROM python:3.9-slim-buster

# set working directory
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/ml
WORKDIR /usr/src/app

# set environment variables
ENV POETRY_VERSION=1.1.12 \
    WANDB_API_KEY=c18bb77e35f2d62462ec243c5bd687b0f12dc458

# install python dependencies
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /usr/src/app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# add ml source code
COPY ml /usr/src/app/ml/
COPY train.py /usr/src/app/